"""Trợ lý ảo: truy hồi + ngữ cảnh riêng + chế độ dự phòng + chặn lạm dụng. Mô hình ngữ nghĩa GIẢ (không tải 470 MB)."""

import numpy as np
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.utils import timezone

from accounts.models import User
from catalog.models import ArchivedTopic, Lecturer, Major, Preference, RegistrationPeriod, Student, Topic
from catalog.tests_similarity import _fake_vec
from recommend.engine import SemanticModel

from . import chat
from .models import ChatLog
from .views import LIMIT


@override_settings(CHAT_PROVIDER="fake", RECOMMEND_LLM=False)
class AssistantTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        major = Major.objects.create(name="CNTT")
        cls.gv = Lecturer.objects.create(user=User.objects.create_user("gv", role=User.Role.LECTURER, first_name="An"))
        cls.t1 = Topic.objects.create(lecturer=cls.gv, title="Chatbot tư vấn", description="chatbot python web")
        cls.t2 = Topic.objects.create(
            lecturer=cls.gv, title="Gợi ý phim", description="gợi ý phim học máy", min_gpa=3.5
        )
        ArchivedTopic.objects.create(
            title="Chatbot thư viện", description="chatbot thư viện", year=2024, future_work="thêm giọng nói"
        )
        now = timezone.now()
        cls.period = RegistrationPeriod.objects.create(
            name="Đợt 1", start_at=now - timezone.timedelta(days=1), end_at=now + timezone.timedelta(days=5)
        )
        cls.u1 = User.objects.create_user("sv1", password="x", role=User.Role.STUDENT)
        cls.s1 = Student.objects.create(user=cls.u1, student_code="SV1", major=major, gpa=3.0)
        u2 = User.objects.create_user("sv2", password="x", role=User.Role.STUDENT)
        cls.s2 = Student.objects.create(user=u2, student_code="SV2", major=major, gpa=3.9, about="bí mật của sv2")
        Preference.objects.create(student=cls.s1, topic=cls.t1, period=cls.period, rank=1)
        Preference.objects.create(
            student=cls.s2,
            topic=cls.t2,
            period=cls.period,
            rank=1,
            reject_reason="lý do riêng sv2",
            status=Preference.Status.REJECTED,
        )

    def setUp(self):
        cache.clear()
        SemanticModel._text_vecs.clear()
        self._orig = SemanticModel.encode
        SemanticModel.encode = classmethod(lambda cls, texts: np.array([_fake_vec(t) for t in texts]))

    def tearDown(self):
        SemanticModel.encode = self._orig

    def test_guide_chunks_parsed(self):
        chunks = chat.guide_chunks()
        self.assertGreaterEqual(len(chunks), 10)
        self.assertTrue(all(c["text"] for c in chunks))

    def test_student_ask_returns_answer_sources_and_log(self):
        self.client.login(username="sv1", password="x")
        r = self.client.post("/tro-ly/hoi/", {"q": "Đề tài chatbot nào còn chỗ?"})
        self.assertEqual(r.status_code, 200)
        d = r.json()
        self.assertEqual(d["mode"], "llm")
        self.assertEqual([s["n"] for s in d["sources"]], [1])  # chỉ trả nguồn mà câu trả lời đã trích
        log = ChatLog.objects.get()
        self.assertEqual((log.role, log.question), ("STUDENT", "Đề tài chatbot nào còn chỗ?"))

    def test_personal_context_only_own_data(self):
        ctx = chat.personal_context(self.u1, self.period)
        self.assertIn("NV1", ctx)
        self.assertIn("Chatbot tư vấn", ctx)
        self.assertNotIn("sv2", ctx)  # không lộ dữ liệu SV khác
        self.assertNotIn("SV1", ctx)  # không gửi mã SV ra mô hình

    def test_topic_line_marks_eligibility_for_student(self):
        from recommend.engine import Profile

        line = chat._topic_text(self.t2, Profile(self.s1), self.period)
        self.assertIn("CHƯA đủ điều kiện", line)
        self.assertIn("GPA tối thiểu", line)

    @override_settings(CHAT_PROVIDER="groq", CHAT_API_KEY="")
    def test_fallback_when_no_llm(self):
        res = chat.answer(self.u1, "Làm sao sửa nguyện vọng đã nộp?")
        self.assertEqual(res["mode"], "fallback")
        self.assertTrue(res["sources"])
        self.assertIn("chưa kết nối được mô hình", res["answer"])

    def test_requires_login_and_post(self):
        self.assertEqual(self.client.post("/tro-ly/hoi/", {"q": "hi"}).status_code, 302)
        self.client.login(username="sv1", password="x")
        self.assertEqual(self.client.get("/tro-ly/hoi/").status_code, 405)
        self.assertEqual(self.client.post("/tro-ly/hoi/", {"q": "  "}).status_code, 400)
        self.assertEqual(self.client.post("/tro-ly/hoi/", {"q": "a" * 801}).status_code, 400)

    def test_rate_limit(self):
        self.client.login(username="sv1", password="x")
        for _ in range(LIMIT):
            self.client.post("/tro-ly/hoi/", {"q": "hạn chót"})
        self.assertEqual(self.client.post("/tro-ly/hoi/", {"q": "hạn chót"}).status_code, 429)

    def test_history_kept_in_session_and_reset(self):
        self.client.login(username="sv1", password="x")
        self.client.post("/tro-ly/hoi/", {"q": "câu một"})
        self.assertEqual(len(self.client.session["chat"]), 1)
        self.client.post("/tro-ly/hoi/", {"reset": "1"})
        self.assertEqual(self.client.session["chat"], [])

    def test_verify_fixes_code_title_pairs(self):
        c1, c2 = self.t1.code, self.t2.code
        wrong_code = f'- {c2} "Chatbot tư vấn" [1]'  # tên đúng của t1, mã của t2 → sửa mã
        self.assertEqual(chat.verify(wrong_code), f'- {c1} "Chatbot tư vấn" [1]')
        mixed = f"- {c1} “Chatbot tư vấn bán hàng” [h]"  # tên ghép bịa → lấy tên thật theo mã, bỏ [h]
        self.assertEqual(chat.verify(mixed), f'- {c1} "Chatbot tư vấn"')

    def test_role_pages_open_and_guide_links(self):
        """ROLE_PAGES khớp quyền thật: mọi trang khai cho vai mở được (200) — nút nguồn không dẫn vào trang 403."""
        from django.urls import reverse

        User.objects.create_user("k", password="x", role=User.Role.ADMIN)
        User.objects.filter(username="gv").update(password=User.objects.get(username="sv1").password)
        for name, role in (("sv1", "STUDENT"), ("gv", "LECTURER"), ("k", "ADMIN")):
            self.client.login(username=name, password="x")
            for page in chat.ROLE_PAGES[role]:
                self.assertEqual(self.client.get(reverse(page)).status_code, 200, (role, page))
        g = next(c for c in chat.guide_chunks() if c["title"] == "Hồ sơ năng lực của sinh viên")
        self.assertEqual(chat._source("guide", g, None, None, chat.ROLE_PAGES["STUDENT"])[1], "/ho-so/")
        self.assertEqual(chat._source("guide", g, None, None, chat.ROLE_PAGES["LECTURER"])[1], "")
        self.assertIn("?lecturer=", chat._source("lecturer", self.gv, None, None, chat.ROLE_PAGES["STUDENT"])[1])

    def test_widget_on_pages_when_logged_in(self):
        self.client.login(username="sv1", password="x")
        self.assertContains(self.client.get("/trang-chu/"), 'id="tlRoot"')
        self.client.logout()
        self.assertNotContains(self.client.get("/dang-nhap/"), 'id="tlRoot"')
