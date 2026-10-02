"""Tính gợi ý Top 5 cho mọi sinh viên:  python manage.py recommend_all"""

from django.core.management.base import BaseCommand

from catalog.models import Student
from recommend.services import open_topics, refresh_student


class Command(BaseCommand):
    help = "Tính và lưu Top 5 gợi ý cho mọi sinh viên."

    def handle(self, *args, **o):
        topics = open_topics()
        n = sum(
            refresh_student(st, topics)
            for st in Student.objects.prefetch_related("skills", "interests", "course_results__course")
        )
        self.stdout.write(self.style.SUCCESS(f"Đã lưu {n} gợi ý."))
