"""Điểm phù hợp cho MỌI đề tài đủ điều kiện (không chỉ Top 5) và chấm bù M5 cho nguyện vọng ngoài Top-K."""

from django.core.management import call_command
from django.test import TestCase, override_settings

from catalog.models import Preference, RegistrationPeriod, Student
from recommend.llm import FakeLLMProvider
from recommend.models import Recommendation
from recommend.services import refresh_student, score_preferences


@override_settings(RECOMMEND_SEMANTIC=False, RECOMMEND_LLM=False)
class AllTopicsScoredTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", students=5, lecturers=3, topics=20, verbosity=0)
        cls.st = Student.objects.order_by("pk").first()

    def test_every_eligible_topic_has_score_and_only_top5_ranked(self):
        for st in Student.objects.all():
            refresh_student(st)
        counts = {st: Recommendation.objects.filter(student=st).count() for st in Student.objects.all()}
        st = max(counts, key=counts.get)  # SV đủ điều kiện nhiều đề tài nhất
        self.assertGreater(counts[st], 5)  # có điểm cả cho đề tài ngoài Top 5
        ranked = sorted(Recommendation.objects.filter(student=st, rank__isnull=False).values_list("rank", flat=True))
        self.assertEqual(ranked, [1, 2, 3, 4, 5])

    def test_top5_scores_not_lower_than_the_rest(self):
        refresh_student(self.st)
        recs = Recommendation.objects.filter(student=self.st)
        worst_top = min(r.final_score for r in recs if r.rank is not None)
        best_rest = max((r.final_score for r in recs if r.rank is None), default=0)
        self.assertGreaterEqual(worst_top, best_rest)


@override_settings(RECOMMEND_SEMANTIC=False, RECOMMEND_LLM=True, LLM_PROVIDER="fake")
class PreferenceM5Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", students=5, lecturers=3, topics=20, verbosity=0)
        cls.st = Student.objects.order_by("pk").first()

    def setUp(self):
        FakeLLMProvider.reset()

    def test_chosen_topic_outside_top_k_gets_m5(self):
        rec = None
        for st in Student.objects.order_by("pk"):  # tìm SV có đề tài đủ điều kiện mà chưa được LLM chấm
            refresh_student(st, top_k=1)  # chỉ 1 đề tài được LLM chấm ở giai đoạn 2
            rec = Recommendation.objects.filter(student=st, m5_llm__isnull=True).first()
            if rec:
                self.st = st
                break
        self.assertIsNotNone(rec)
        Preference.objects.filter(student=self.st).delete()
        Preference.objects.create(student=self.st, topic=rec.topic, period=RegistrationPeriod.objects.first(), rank=1)
        score_preferences(self.st)
        rec.refresh_from_db()
        self.assertIsNotNone(rec.m5_llm)
