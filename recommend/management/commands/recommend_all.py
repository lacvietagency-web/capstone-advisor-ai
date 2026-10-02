"""Tính gợi ý Top 5 cho mọi sinh viên và lưu vào bảng Recommendation.

    python manage.py recommend_all
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import Student, Topic
from recommend.engine import DEFAULT_WEIGHTS, WEIGHTS_VERSION, explain, score_student
from recommend.models import Recommendation


class Command(BaseCommand):
    help = "Tính và lưu Top 5 gợi ý cho mọi sinh viên."

    def add_arguments(self, parser):
        parser.add_argument("--top", type=int, default=5)

    @transaction.atomic
    def handle(self, *args, **o):
        topics = list(Topic.objects.filter(status=Topic.Status.OPEN).prefetch_related("skills__skill", "prerequisites__course", "fields"))
        n = 0
        for st in Student.objects.prefetch_related("skills", "interests", "course_results__course"):
            Recommendation.objects.filter(student=st).delete()
            for rank, c in enumerate(score_student(st, topics)[: o["top"]], 1):
                Recommendation.objects.create(student=st, topic=c.topic, rank=rank, m1_skill=c.scores["skill"],
                                              m2_academic=c.scores["academic"], m3_field=c.scores["field"],
                                              m4_semantic=c.scores["semantic"], m5_llm=c.scores["llm"],
                                              final_score=c.final(DEFAULT_WEIGHTS), reason=explain(c),
                                              weights_version=WEIGHTS_VERSION, model_version="m1-m3-v1")
                n += 1
        self.stdout.write(self.style.SUCCESS(f"Đã lưu {n} gợi ý."))
