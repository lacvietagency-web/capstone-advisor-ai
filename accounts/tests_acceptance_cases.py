"""Nghiệm thu P0 #8 — các ca trong docs/KICH-BAN-KIEM-THU.md chưa có test máy chủ trước ngày 20/10/2026.

Tên test bắt đầu bằng mã ca (test_a02_…, test_s08_…) để biên bản truy ngược được. Các ca khác của kịch bản đã có
test từ trước; ánh xạ đầy đủ ở docs/nghiem-thu/BIEN-BAN-84-CA.md.
"""

from io import StringIO

from django.core.management import CommandError, call_command
from django.test import TestCase, override_settings

from accounts.models import User
from allocate.services import run_allocation
from catalog.models import AuditLog, Lecturer, Preference, RegistrationPeriod, Student, Topic


@override_settings(RECOMMEND_SEMANTIC=False, RECOMMEND_LLM=False)
class AcceptanceCases(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", students=12, lecturers=4, topics=10, verbosity=0)
        cls.period = RegistrationPeriod.objects.get()
        cls.sv = Student.objects.select_related("user").get(user__username="sv001")
        cls.topic = Topic.objects.filter(status=Topic.Status.OPEN).order_by("pk").first()
        cls.owner = cls.topic.lecturer
        cls.other = Lecturer.objects.exclude(pk=cls.owner.pk).order_by("pk").first()

    def login(self, username):
        self.client.login(username=username, password="123456")

    # ------------------------------------------------------------------ 1. tài khoản và phân quyền
    def test_a01_login_returns_to_requested_page(self):
        r = self.client.get("/nguyen-vong/")
        self.assertRedirects(r, "/dang-nhap/?next=/nguyen-vong/", fetch_redirect_response=False)
        r = self.client.post("/dang-nhap/?next=/nguyen-vong/", {"username": "sv001", "password": "123456"})
        self.assertRedirects(r, "/nguyen-vong/", fetch_redirect_response=False)

    def test_a02_wrong_login_same_message_keeps_username(self):
        bodies = []
        for user, pw in (("sv001", "sai-mat-khau"), ("khong-ton-tai", "123456")):
            r = self.client.post("/dang-nhap/", {"username": user, "password": pw})
            self.assertEqual(r.status_code, 200)
            self.assertFalse(r.wsgi_request.user.is_authenticated)
            self.assertEqual(r.context["form"].data["username"], user)
            bodies.append(r.context["form"].non_field_errors())
        self.assertEqual(bodies[0], bodies[1], "thông báo khác nhau → lộ tài khoản có tồn tại hay không")
        empty = self.client.post("/dang-nhap/", {"username": "", "password": ""})
        self.assertTrue(empty.context["form"].errors)

    def test_a06_password_similar_to_username_rejected(self):
        self.login("sv001")
        r = self.client.post(
            "/doi-mat-khau/",
            {"old_password": "123456", "new_password1": "sv001abc", "new_password2": "sv001abc"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertIn("new_password2", r.context["form"].errors)
        self.assertTrue(User.objects.get(username="sv001").check_password("123456"))

    def test_a07_logout_ends_session(self):
        self.login("sv001")
        self.assertEqual(self.client.get("/ho-so/").status_code, 200)
        self.client.post("/dang-xuat/")
        self.assertEqual(self.client.get("/ho-so/").status_code, 302)

    def test_a10_other_lecturer_cannot_review_by_post(self):
        pref = Preference.objects.filter(topic=self.topic, submitted=True).first() or Preference.objects.create(
            student=self.sv, topic=self.topic, rank=1, submitted=True, period=self.period
        )
        status_before = pref.status
        self.client.force_login(self.other.user)
        r = self.client.post(f"/de-tai/{self.topic.pk}/dang-ky/", {"pref_id": pref.pk, "action": "accept"})
        self.assertIn(r.status_code, (403, 404))
        pref.refresh_from_db()
        self.assertEqual(pref.status, status_before)

    def test_a13_closed_topic_viewable_without_register(self):
        closed = Topic.objects.create(
            lecturer=self.owner, title="Đề tài đã đóng", capacity=1, status=Topic.Status.CLOSED
        )
        self.login("sv001")
        r = self.client.get(f"/danh-sach-de-tai/{closed.pk}/")
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, f"/nguyen-vong/?topic={closed.pk}")

    def test_k14_admin_site_only_for_faculty(self):
        for username, ok in (("sv001", False), (self.owner.user.username, False), ("khoa01", True)):
            self.client.logout()
            self.login(username)
            code = self.client.get("/quan-tri/").status_code
            self.assertEqual(code == 200, ok, f"{username} → {code}")

    # ------------------------------------------------------------------ 2. sinh viên
    def test_s03_readonly_fields_cannot_be_tampered(self):
        self.login("sv001")
        gpa, code = self.sv.gpa, self.sv.student_code
        self.client.post("/ho-so/", {"gpa": "4.0", "student_code": "HACK", "first_name": "Hack", "about": ""})
        st = Student.objects.select_related("user").get(pk=self.sv.pk)
        self.assertEqual((st.gpa, st.student_code), (gpa, code))
        self.assertNotEqual(st.user.first_name, "Hack")

    def test_s08_about_length_and_script_escaped(self):
        from catalog.forms import StudentAboutForm

        self.assertTrue(StudentAboutForm({"about": "a" * 500}, instance=self.sv).is_valid())
        self.assertFalse(StudentAboutForm({"about": "a" * 501}, instance=self.sv).is_valid())
        Student.objects.filter(pk=self.sv.pk).update(about="<script>alert(1)</script>")
        self.login("sv001")
        html = self.client.get("/ho-so/").content.decode()
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)

    def test_s11_special_characters_in_search_never_500(self):
        self.login("sv001")
        word = self.topic.title.split()[0]
        for q in ("%", "'", '"', "%' OR 1=1 --", "đồ án", word):
            self.assertEqual(self.client.get("/danh-sach-de-tai/", {"q": q}).status_code, 200, q)
        found = self.client.get("/danh-sach-de-tai/", {"q": word}).content.decode()
        self.assertIn(self.topic.title, found)

    def test_s18_register_when_three_preferences_keeps_old_ones(self):
        Preference.objects.filter(student=self.sv).delete()
        picks = list(Topic.objects.filter(status=Topic.Status.OPEN).exclude(pk=self.topic.pk)[:3])
        for rank, t in enumerate(picks, 1):
            Preference.objects.create(student=self.sv, topic=t, rank=rank, period=self.period)
        self.login("sv001")
        r = self.client.get(f"/nguyen-vong/?topic={self.topic.pk}")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            list(Preference.objects.filter(student=self.sv).order_by("rank").values_list("topic_id", flat=True)),
            [t.pk for t in picks],
        )
        self.assertContains(r, "3")

    # ------------------------------------------------------------------ 3. giảng viên
    def test_l04_my_topics_lists_only_own(self):
        self.client.force_login(self.owner.user)
        topics = self.client.get("/de-tai/").context
        listed = [t.pk for t in (topics.get("topics") or topics.get("page_obj") or [])]
        self.assertTrue(listed)
        self.assertFalse(Topic.objects.filter(pk__in=listed).exclude(lecturer=self.owner).exists())

    def test_l07_editing_description_bumps_version(self):
        v = self.topic.version
        self.client.force_login(self.owner.user)
        ctx = self.client.get(f"/de-tai/{self.topic.pk}/sua/").context
        form = ctx["form"]
        data = {k: v2 for k, v2 in form.initial.items() if v2 is not None and not isinstance(v2, list)}
        data["fields"] = [f.pk for f in self.topic.fields.all()]
        data["description"] = (self.topic.description or "") + " (sửa)"
        for fs in (ctx["skill_formset"], ctx["prereq_formset"]):
            existing = [f for f in fs.forms if f.instance.pk]  # như trình duyệt: dòng trống dự phòng gửi rỗng
            data.update({f"{fs.prefix}-TOTAL_FORMS": len(existing), f"{fs.prefix}-INITIAL_FORMS": len(existing)})
            for f in existing:
                data.update({f.add_prefix(k): val for k, val in f.initial.items() if val is not None})
                data[f.add_prefix("id")] = f.instance.pk
        r = self.client.post(f"/de-tai/{self.topic.pk}/sua/", data)
        self.assertEqual(r.status_code, 302)
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.version, v + 1)
        self.assertTrue(self.topic.description.endswith("(sửa)"))

    def test_l08_registrations_default_to_pending(self):
        self.client.force_login(self.owner.user)
        rows = self.client.get(f"/de-tai/{self.topic.pk}/dang-ky/").context["rows"]
        statuses = {getattr(r.get("pref", r), "status", None) if isinstance(r, dict) else r.status for r in rows}
        self.assertLessEqual(statuses, {Preference.Status.PENDING})

    def test_l12_lecturer_phone_never_shown_to_students(self):
        Lecturer.objects.filter(pk=self.owner.pk).update(phone="0987654321")
        self.login("sv001")
        pages = [
            "/trang-chu/",
            "/danh-sach-de-tai/",
            f"/danh-sach-de-tai/{self.topic.pk}/",
            "/nguyen-vong/",
            "/ket-qua/",
        ]
        for url in pages:
            self.assertNotContains(self.client.get(url), "0987654321", msg_prefix=url)

    # ------------------------------------------------------------------ 5. dữ liệu
    def test_b10_audit_log_for_main_actions(self):
        AuditLog.objects.all().delete()
        self.login("sv001")
        t = self.topic
        self.client.post("/nguyen-vong/", {"nv1": t.pk, "action": "submit"})
        pref = Preference.objects.get(student=self.sv, topic=t)
        self.client.logout()
        self.client.force_login(t.lecturer.user)
        self.client.post(f"/de-tai/{t.pk}/dang-ky/", {"pref_id": pref.pk, "action": "accept"})
        self.client.logout()
        self.login("khoa01")
        self.client.post("/khoa/phan-cong/", {"action": "run_ilp", "period_id": self.period.pk})
        self.client.post("/khoa/phan-cong/", {"action": "publish", "period_id": self.period.pk})
        logged = set(AuditLog.objects.values_list("user__username", "entity"))
        users = {u for u, _ in logged}
        self.assertTrue({"sv001", t.lecturer.user.username, "khoa01"} <= users, logged)
        self.assertTrue(all(AuditLog.objects.values_list("entity_id", flat=True)))

    def test_b12_allocate_period_refuses_published(self):
        run_allocation(self.period, algorithm="GREEDY")
        RegistrationPeriod.objects.filter(pk=self.period.pk).update(status=RegistrationPeriod.Status.PUBLISHED)
        with self.assertRaises(CommandError):
            call_command("allocate_period", period=self.period.pk, stdout=StringIO())
