"""Nghiệm thu P0 #1 — ma trận phân quyền: mọi URL × {khách, SV, GV chủ đề tài, GV khác, Khoa} × {GET, POST}.

Mỗi ô là mã trả về mong đợi. "ok" = 200 (hoặc 302 sau POST hợp lệ); "deny" = không lộ trang (302 về đăng nhập/trang chủ,
403 hoặc 404). Không ô nào được 500. Ca IDOR: GV khác mở đề tài/đăng ký của GV chủ → phải "deny".
In bảng thật: QA_PRINT_MATRIX=1 python manage.py test accounts.tests_acceptance_matrix
"""

import os

from django.core.management import call_command
from django.test import TestCase, override_settings

from accounts.models import User
from catalog.models import Lecturer, RegistrationPeriod, Student, Topic

ROLES = ("anon", "sv", "gv_owner", "gv_other", "khoa")
LOGINS = {"sv": "sv001", "khoa": "khoa01"}

OK, DENY = "ok", "deny"


def _allowed(*roles):
    return {r: (OK if r in roles else DENY) for r in ROLES}


@override_settings(RECOMMEND_SEMANTIC=False, RECOMMEND_LLM=False)
class AcceptanceAuthzMatrix(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", students=12, lecturers=4, topics=10, verbosity=0)
        cls.period = RegistrationPeriod.objects.get()
        cls.topic = Topic.objects.order_by("pk").first()
        cls.owner = cls.topic.lecturer
        cls.other = Lecturer.objects.exclude(pk=cls.owner.pk).order_by("pk").first()
        cls.student = Student.objects.order_by("pk").first()
        cls.users = {
            "sv": User.objects.get(username="sv001"),
            "khoa": User.objects.get(username="khoa01"),
            "gv_owner": cls.owner.user,
            "gv_other": cls.other.user,
        }

    def urls(self):
        t, p, s, lec = self.topic.pk, self.period.pk, self.student.pk, self.owner.pk
        return [
            ("/trang-chu/", _allowed("sv", "gv_owner", "gv_other", "khoa")),
            ("/doi-mat-khau/", _allowed("sv", "gv_owner", "gv_other", "khoa")),
            ("/ho-so/", _allowed("sv")),
            ("/nguyen-vong/", _allowed("sv")),
            ("/ket-qua/", _allowed("sv")),
            # danh mục đề tài công khai (quyết định thiết kế): ai cũng xem đề tài đang mở, không lộ dữ liệu cá nhân
            ("/danh-sach-de-tai/", _allowed(*ROLES)),
            (f"/danh-sach-de-tai/{t}/", _allowed(*ROLES)),
            ("/de-tai/", _allowed("gv_owner", "gv_other")),
            ("/de-tai/them/", _allowed("gv_owner", "gv_other")),
            (f"/de-tai/{t}/sua/", _allowed("gv_owner")),
            (f"/de-tai/{t}/dang-ky/", _allowed("gv_owner")),
            ("/ho-so-giang-vien/", _allowed("gv_owner", "gv_other", "khoa")),  # Khoa sửa hồ sơ mọi GV (UC09)
            (f"/ho-so-giang-vien/{lec}/", _allowed("gv_owner", "khoa")),
            ("/khoa/phan-cong/", _allowed("khoa")),
            (f"/khoa/phan-cong/{p}/sinh-vien/{s}/", _allowed("khoa")),
            ("/khoa/nhap-excel/", _allowed("khoa")),
            ("/khoa/nhap-excel/mau.xlsx", _allowed("khoa")),
            ("/khoa/thong-ke/", _allowed("khoa")),
        ]

    def _client(self, role):
        c = self.client_class()
        if role != "anon":
            c.force_login(self.users[role])
        return c

    @staticmethod
    def _cls(code):
        if code >= 500:
            return "500"
        return OK if code == 200 else DENY

    def test_get_matrix(self):
        rows, bad = [], []
        for url, expect in self.urls():
            got = {}
            for role in ROLES:
                code = self._client(role).get(url).status_code
                got[role] = code
                self.assertLess(code, 500, f"{role} GET {url} → {code}")
                if expect and self._cls(code) != expect[role]:
                    bad.append(f"{role} GET {url}: {code}, mong đợi {expect[role]}")
            rows.append((url, got))
        if os.environ.get("QA_PRINT_MATRIX"):
            print("\nURL".ljust(46) + "".join(r.ljust(10) for r in ROLES))
            for url, got in rows:
                print(url.ljust(45) + "".join(str(got[r]).ljust(10) for r in ROLES))
        self.assertFalse(bad, "\n".join(bad))

    def test_post_matrix_never_changes_data_for_wrong_role(self):
        """POST thẳng (bỏ qua giao diện) bằng vai sai: không lỗi 500, không đổi dữ liệu."""
        t = self.topic.pk
        posts = [
            (f"/de-tai/{t}/sua/", {"title": "BỊ SỬA"}, ("sv", "gv_other", "khoa", "anon")),
            ("/de-tai/them/", {"title": "ĐỀ TÀI LẠ"}, ("sv", "khoa", "anon")),
            ("/khoa/phan-cong/", {"action": "run", "algorithm": "GREEDY"}, ("sv", "gv_owner", "anon")),
            ("/nguyen-vong/", {"action": "submit"}, ("gv_owner", "khoa", "anon")),
        ]
        before_title = Topic.objects.get(pk=t).title
        n_topics = Topic.objects.count()
        for url, data, roles in posts:
            for role in roles:
                code = self._client(role).post(url, data).status_code
                self.assertLess(code, 500, f"{role} POST {url} → {code}")
        self.assertEqual(Topic.objects.get(pk=t).title, before_title)
        self.assertEqual(Topic.objects.count(), n_topics)
        from allocate.models import Allocation

        self.assertFalse(Allocation.objects.exists(), "vai sai đã chạy được phân công")

    def test_public_catalog_hides_drafts_and_personal_data(self):
        draft = Topic.objects.create(lecturer=self.owner, title="Đề tài nháp kín", capacity=1, status="DRAFT")
        anon = self._client("anon")
        self.assertEqual(anon.get(f"/danh-sach-de-tai/{draft.pk}/").status_code, 404)
        self.assertNotIn("Đề tài nháp kín", anon.get("/danh-sach-de-tai/").content.decode())
        pages = ("/danh-sach-de-tai/", f"/danh-sach-de-tai/{self.topic.pk}/")
        html = "".join(anon.get(u).content.decode() for u in pages)
        for st in Student.objects.select_related("user"):
            for secret in (st.user.email, st.student_code):
                if secret:
                    self.assertNotIn(secret, html)
        for lec in Lecturer.objects.select_related("user"):
            for secret in (lec.user.email, lec.phone):
                if secret:
                    self.assertNotIn(secret, html)
