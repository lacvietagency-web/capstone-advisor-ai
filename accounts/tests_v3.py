"""Kiểm thử phần lõi cho giao diện V3 (ATLAS): gợi ý tự tính, hành trình SV, nguyện vọng chỉ xem, bảng phân công."""

from django.core.management import call_command
from django.test import TestCase, override_settings

from allocate.services import run_allocation
from catalog.models import RegistrationPeriod
from recommend.models import Recommendation


@override_settings(RECOMMEND_SEMANTIC=False, RECOMMEND_LLM=False)
class V3CoreTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", students=12, lecturers=4, topics=10, verbosity=0)
        cls.period = RegistrationPeriod.objects.get()

    def test_student_home_computes_recommendations_and_journey(self):
        """Dữ liệu seed chưa chạy recommend_all: mở trang chủ là có Top gợi ý, hành trình đủ 4 mục."""
        self.assertFalse(Recommendation.objects.exists())
        self.client.login(username="sv001", password="123456")
        resp = self.client.get("/trang-chu/")
        self.assertTrue(resp.context["recommendations"])
        self.assertEqual([s["label"] for s in resp.context["journey"]][2:], ["Nguyện vọng", "Kết quả phân công"])
        self.assertEqual(resp.context["journey"][0]["state"], "done")

    def test_journey_after_publish_is_all_done(self):
        RegistrationPeriod.objects.update(status=RegistrationPeriod.Status.PUBLISHED)
        self.client.login(username="sv001", password="123456")
        journey = self.client.get("/trang-chu/").context["journey"]
        self.assertEqual({s["state"] for s in journey[2:]}, {"done"})
        self.assertEqual(journey[2]["note"], "Đã nộp · chỉ xem")

    def test_preferences_readonly_when_no_open_period(self):
        """Đợt đã đóng: SV vẫn xem lại nguyện vọng đã nộp (không còn trang trống)."""
        RegistrationPeriod.objects.update(status=RegistrationPeriod.Status.CLOSED)
        self.client.login(username="sv001", password="123456")
        ctx = self.client.get("/nguyen-vong/").context
        self.assertIsNone(ctx["period"])
        self.assertEqual(ctx["last_period"], self.period)
        self.assertEqual([row["pref"].rank for row in ctx["submitted"]], [1, 2, 3][: len(ctx["submitted"])])
        self.assertTrue(ctx["submitted"])

    def test_allocation_table_search_filter_and_paging(self):
        run_allocation(self.period, algorithm="GREEDY")
        self.client.login(username="khoa01", password="123456")
        ctx = self.client.get("/khoa/phan-cong/?per_page=10").context
        self.assertEqual(ctx["total_count"], 12)
        self.assertEqual(len(ctx["page_obj"]), 10)
        self.assertEqual(ctx["page_obj"].paginator.num_pages, 2)
        one = self.client.get("/khoa/phan-cong/?q=20230001").context
        self.assertEqual([a.student.student_code for a in one["allocations"]], ["20230001"])
        assigned = self.client.get("/khoa/phan-cong/?status=assigned").context["allocations"]
        self.assertTrue(all(a.topic_id for a in assigned))
        high = self.client.get("/khoa/phan-cong/?score_min=50").context["allocations"]
        self.assertTrue(all(a.match_score >= 50 for a in high))


@override_settings(RECOMMEND_SEMANTIC=False, RECOMMEND_LLM=False)
class V34CoreTests(TestCase):
    """Phán quyết ATLAS V3.4: ngăn kéo tải riêng, điều kiện có cấu trúc, công bố có chặn, lý do từ chối 5–500."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", students=12, lecturers=4, topics=10, verbosity=0)
        cls.period = RegistrationPeriod.objects.get()

    def test_eligibility_reasons_agree_with_eligible(self):
        from catalog.models import Student, Topic
        from recommend.engine import Profile, eligibility_reasons, eligible

        for st in Student.objects.all()[:5]:
            p = Profile(st)
            for t in Topic.objects.all():
                self.assertEqual(eligible(p, t)[0], all(r["ok"] for r in eligibility_reasons(p, t)))

    def test_student_drawer_fragment(self):
        from catalog.models import Student

        run_allocation(self.period, algorithm="GREEDY")
        st = Student.objects.get(user__username="sv001")
        url = f"/khoa/phan-cong/{self.period.pk}/sinh-vien/{st.pk}/"
        self.client.login(username="sv001", password="123456")
        self.assertEqual(self.client.get(url).status_code, 403)
        self.client.login(username="khoa01", password="123456")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, "<html")
        self.assertEqual(len(resp.context["prefs"]), st.preferences.count())

    def test_publish_refused_without_allocations_and_twice(self):
        self.client.login(username="khoa01", password="123456")
        self.client.post("/khoa/phan-cong/", {"action": "publish", "period_id": self.period.pk})
        self.period.refresh_from_db()
        self.assertNotEqual(self.period.status, RegistrationPeriod.Status.PUBLISHED)
        run_allocation(self.period, algorithm="GREEDY")
        self.client.post(f"/khoa/phan-cong/?period_id={self.period.pk}", {"action": "publish"})
        self.period.refresh_from_db()
        self.assertEqual(self.period.status, RegistrationPeriod.Status.PUBLISHED)

    def test_reject_reason_max_length(self):
        from catalog.models import Preference

        pref = Preference.objects.select_related("topic__lecturer__user").first()
        self.client.force_login(pref.topic.lecturer.user)
        url = f"/de-tai/{pref.topic.pk}/dang-ky/"
        self.client.post(url, {"preference_id": pref.pk, "action": "reject", "reason": "x" * 501})
        pref.refresh_from_db()
        self.assertEqual(pref.status, Preference.Status.PENDING)
        self.client.post(url, {"preference_id": pref.pk, "action": "reject", "reason": "Thiếu kỹ năng bắt buộc."})
        pref.refresh_from_db()
        self.assertEqual(pref.status, Preference.Status.REJECTED)


@override_settings(RECOMMEND_SEMANTIC=False, RECOMMEND_LLM=False)
class V34DashboardTests(TestCase):
    def test_unassigned_count_shown(self):
        from allocate.models import Allocation

        call_command("seed_demo", students=12, lecturers=4, topics=10, verbosity=0)
        period = RegistrationPeriod.objects.get()
        run_allocation(period, algorithm="GREEDY")
        self.client.login(username="khoa01", password="123456")
        m = self.client.get("/khoa/phan-cong/").context["metrics"]
        self.assertEqual(m["unassigned_count"], Allocation.objects.filter(period=period, topic__isnull=True).count())
