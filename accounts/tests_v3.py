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
