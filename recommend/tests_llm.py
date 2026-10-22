"""Kiểm thử cho mô-đun LLM chấm điểm M5 (recommend/llm.py và tích hợp engine/services).

Các kịch bản kiểm thử:
1. Fake provider: xáo trộn thứ tự đề tài trước khi gửi nhưng ghép lại đúng topic_id.
2. Cache LLMScore theo sha256(profile_version|topic.version|PROMPT_VERSION|model): không gọi lại khi đã có đệm.
3. Lỗi mạng/JSON sau 1 lần thử lại: m5=None, engine tự chia lại trọng số các thành phần còn lại.
4. Tổng sai rubric hoặc ngoài 0..100: bỏ điểm M5 của đề tài đó, đề tài vẫn được gợi ý bằng M1–M4.
5. Cài đặt RECOMMEND_LLM=0 tắt hoàn toàn M5 khi chạy kiểm thử khác.
6. Hàm score_pair: tính bù M5 cho 1 cặp (sinh viên, đề tài) ngoài Top-K.
7. Lý do hiển thị: kết hợp lý do của LLM với 'Cần bổ sung: …' từ M1.
"""

from django.test import TestCase, override_settings

from accounts.models import User
from catalog.models import (
    Course,
    Field,
    Lecturer,
    Major,
    Skill,
    Student,
    StudentCourseResult,
    StudentInterest,
    StudentSkill,
    Topic,
    TopicPrerequisite,
    TopicSkill,
)
from recommend.engine import DEFAULT_WEIGHTS, Candidate, explain, score_pair, score_student
from recommend.llm import FakeLLMProvider, get_cache_key
from recommend.models import LLMScore


@override_settings(RECOMMEND_SEMANTIC=False, LLM_PROVIDER="fake", RECOMMEND_LLM=True)
class LLMScoringTests(TestCase):
    """Bộ kiểm thử cho đánh giá LLM M5 theo rubric 100 điểm."""

    @classmethod
    def setUpTestData(cls):
        web = Field.objects.create(name="Web")
        ai = Field.objects.create(name="AI")
        java = Skill.objects.create(name="Java")
        py = Skill.objects.create(name="Python")
        db = Course.objects.create(code="DB01", name="Cơ sở dữ liệu", field=web)

        lec_user = User.objects.create_user("gv_test", role="LECTURER")
        lec = Lecturer.objects.create(user=lec_user)

        major = Major.objects.create(name="Công nghệ thông tin")
        st_user = User.objects.create_user("sv_test", role="STUDENT")
        st = Student.objects.create(
            user=st_user,
            student_code="SV999",
            major=major,
            gpa=3.5,
            about="Tôi thích phát triển web backend và nghiên cứu AI.",
        )
        StudentSkill.objects.create(student=st, skill=java, level=4)
        StudentSkill.objects.create(student=st, skill=py, level=2)
        StudentInterest.objects.create(student=st, field=web, level=3)
        StudentCourseResult.objects.create(student=st, course=db, score=8.5)

        t1 = Topic.objects.create(
            lecturer=lec,
            title="Hệ thống thương mại điện tử",
            description="Xây dựng sàn TMĐT với Java và Spring",
            min_gpa=2.5,
        )
        t1.fields.set([web])
        TopicSkill.objects.create(topic=t1, skill=java, required_level=3)
        TopicPrerequisite.objects.create(topic=t1, course=db, min_score=5)

        t2 = Topic.objects.create(
            lecturer=lec,
            title="Chatbot tư vấn khách hàng",
            description="Ứng dụng NLP và học máy hỗ trợ người dùng",
            min_gpa=2.5,
        )
        t2.fields.set([ai])
        TopicSkill.objects.create(topic=t2, skill=py, required_level=3)

        t3 = Topic.objects.create(
            lecturer=lec,
            title="Cổng thông tin tuyển sinh",
            description="Web tra cứu thông tin tuyển sinh",
            min_gpa=2.0,
        )
        t3.fields.set([web])
        TopicSkill.objects.create(topic=t3, skill=java, required_level=2)

        cls.st = st
        cls.t1 = t1
        cls.t2 = t2
        cls.t3 = t3

    def setUp(self):
        FakeLLMProvider.reset()

    def test_shuffling_preserves_topic_matching(self):
        """Kiểm tra: trộn ngẫu nhiên thứ tự đề tài nhưng điểm vẫn ghép chính xác theo topic_id."""
        topics = [self.t1, self.t2, self.t3]
        cands = score_student(self.st, topics=topics, semantic=False, llm=True)

        self.assertEqual(FakeLLMProvider.call_count, 1)
        self.assertGreaterEqual(len(cands), 1)

        # Kiểm tra từng đề tài nhận đúng điểm giả định tương ứng với topic_id
        for c in cands:
            t = c.topic
            expected_f = min(35, 20 + (t.id % 15))
            expected_c = min(30, 15 + (t.id % 15))
            expected_n = min(20, 10 + (t.id % 10))
            expected_m = min(15, 10 + (t.id % 5))
            expected_total = expected_f + expected_c + expected_n + expected_m
            self.assertEqual(c.scores["llm"], float(expected_total))

    def test_cache_prevents_recalling_llm(self):
        """Kiểm tra: khi đã có cache LLMScore thì không gọi lại API."""
        topics = [self.t1, self.t2]

        # Lần 1: Chưa có cache → gọi fake LLM (call_count = 1)
        score_student(self.st, topics=topics, semantic=False, llm=True)
        self.assertEqual(FakeLLMProvider.call_count, 1)

        # Kiểm tra CSDL đã lưu các bản ghi cache
        cached_count = LLMScore.objects.filter(student=self.st).count()
        self.assertEqual(cached_count, 2)

        # Lần 2: Cùng hồ sơ và đề tài → đọc từ cache, không gọi lại provider
        score_student(self.st, topics=topics, semantic=False, llm=True)
        self.assertEqual(FakeLLMProvider.call_count, 1)

        # Đổi phiên bản hồ sơ sinh viên → cache mất hiệu lực → gọi lại provider
        self.st.profile_version += 1
        self.st.save()
        score_student(self.st, topics=topics, semantic=False, llm=True)
        self.assertEqual(FakeLLMProvider.call_count, 2)

    def test_json_error_yields_none_and_rebalances_weights(self):
        """Kiểm tra: khi phản hồi JSON lỗi sau 1 lần thử lại → m5=None và tự chia lại trọng số."""
        # Giả lập phản hồi chuỗi JSON hỏng
        FakeLLMProvider.custom_response = "BẢN TIN KHÔNG PHẢI JSON"

        cands = score_student(self.st, topics=[self.t1, self.t2], semantic=False, llm=True)

        self.assertGreaterEqual(len(cands), 1)
        for c in cands:
            # m5 phải là None vì JSON lỗi
            self.assertIsNone(c.scores["llm"])

            # Điểm cuối phải bằng tổng có trọng số chia lại cho (w_skill + w_field)
            w = {
                "skill": DEFAULT_WEIGHTS["skill"],
                "field": DEFAULT_WEIGHTS["field"],
            }
            expected_total_w = sum(w.values())
            expected_score = sum(w[k] * c.scores[k] for k in w) / expected_total_w
            self.assertAlmostEqual(c.final(DEFAULT_WEIGHTS), expected_score)

    def test_invalid_total_topic_is_eliminated(self):
        """Kiểm tra: đề tài có tổng các mục != total hoặc total ngoài 0..100 bị bỏ điểm M5."""
        # t1 có tổng sai: 20 + 20 + 10 + 10 = 60 != 99
        # t2 có tổng đúng: 20 + 20 + 10 + 10 = 60 == 60
        FakeLLMProvider.custom_scores = [
            {
                "topic_id": self.t1.id,
                "feasibility": 20,
                "career": 20,
                "nature": 10,
                "motivation": 10,
                "total": 99,
                "reason": "Tổng sai",
            },
            {
                "topic_id": self.t2.id,
                "feasibility": 20,
                "career": 20,
                "nature": 10,
                "motivation": 10,
                "total": 60,
                "reason": "Đúng tổng",
            },
        ]

        cands = score_student(self.st, topics=[self.t1, self.t2], semantic=False, llm=True)
        cand_topic_ids = [c.topic.id for c in cands]

        # Đề tài t1 tổng sai: vẫn có trong danh sách nhưng không có điểm M5
        self.assertIn(self.t1.id, cand_topic_ids)
        self.assertIsNone(next(c for c in cands if c.topic.id == self.t1.id).scores["llm"])
        # Đề tài t2 hợp lệ được giữ lại
        self.assertIn(self.t2.id, cand_topic_ids)

        # Với hàm score_pair: t1 trả về None, t2 trả về kết quả hợp lệ
        res_t1 = score_pair(self.st, self.t1)
        self.assertIsNone(res_t1)

        res_t2 = score_pair(self.st, self.t2)
        self.assertIsNotNone(res_t2)
        self.assertEqual(res_t2.total, 60.0)

    @override_settings(RECOMMEND_LLM=False)
    def test_recommend_llm_setting_disables_m5(self):
        """Kiểm tra: khi RECOMMEND_LLM=0 thì M5 bị tắt hoàn toàn, không gọi LLM."""
        cands = score_student(self.st, topics=[self.t1], semantic=False)

        self.assertEqual(FakeLLMProvider.call_count, 0)
        self.assertGreaterEqual(len(cands), 1)
        for c in cands:
            self.assertIsNone(c.scores["llm"])

    def test_score_pair_calculates_supplementary_m5(self):
        """Kiểm tra: hàm score_pair tính bù điểm M5 cho 1 cặp (sinh viên, đề tài) ngoài Top-K."""
        res = score_pair(self.st, self.t3)

        self.assertIsNotNone(res)
        self.assertEqual(FakeLLMProvider.call_count, 1)
        self.assertGreater(res.total, 0)
        self.assertTrue(res.reason.startswith("Đề tài"))

        # Kiểm tra đã lưu cache LLMScore
        k = get_cache_key(self.st, self.t3)
        self.assertTrue(LLMScore.objects.filter(cache_key=k).exists())

        # Gọi lại score_pair đọc từ cache
        res2 = score_pair(self.st, self.t3)
        self.assertEqual(FakeLLMProvider.call_count, 1)
        self.assertEqual(res.total, res2.total)

    def test_reason_formatting_with_llm_and_m1(self):
        """Kiểm tra: format lý do hiển thị = lý do LLM + 'Cần bổ sung: …' từ M1."""
        c1 = Candidate(
            self.t1,
            scores={"skill": 60, "field": 50, "llm": 80},
            reasons=["Cần bổ sung: Python"],
            llm_reason="Đề tài phù hợp với định hướng làm việc trong ngành phần mềm.",
        )
        r1 = explain(c1)
        self.assertEqual(
            r1,
            "Đề tài phù hợp với định hướng làm việc trong ngành phần mềm. Cần bổ sung: Python",
        )

        c2 = Candidate(
            self.t1,
            scores={"skill": 90, "field": 70, "llm": 90},
            reasons=[],
            llm_reason="Bạn có nền tảng rất vững chắc cho đề tài này.",
        )
        r2 = explain(c2)
        self.assertEqual(r2, "Bạn có nền tảng rất vững chắc cho đề tài này.")

        # Khi không có LLM reason, dùng mẫu câu heuristic
        c3 = Candidate(
            self.t1,
            scores={"skill": 85, "field": 60, "semantic": 40},
            reasons=["Cần bổ sung: Docker"],
            llm_reason="",
        )
        r3 = explain(c3)
        self.assertTrue(r3.startswith("Phù hợp vì"))
        self.assertIn("Cần bổ sung: Docker", r3)
