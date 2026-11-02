"""Nạp đề tài khoá trước mẫu vào CSDL đang chạy để minh hoạ "tư vấn cải tiến" — chỉ thêm, chạy lại không tạo trùng.

python manage.py them_de_tai_khoa_truoc                 # 4 đề tài mẫu
python manage.py them_de_tai_khoa_truoc --tu-de-tai 12  # + chép đề tài 12 thành 1 bản khoá 2024
"""

from django.core.management.base import BaseCommand, CommandError

from catalog.management.commands.seed_demo import ARCHIVE_SAMPLES
from catalog.models import ArchivedTopic, Topic


class Command(BaseCommand):
    help = "Thêm đề tài khoá trước mẫu (không xoá dữ liệu, không tạo trùng)."

    def add_arguments(self, parser):
        parser.add_argument("--tu-de-tai", type=int, help="Mã (pk) đề tài đang có, chép thành 1 đề tài khoá 2024")

    def handle(self, *args, **o):
        rows = list(ARCHIVE_SAMPLES)
        if o["tu_de_tai"]:
            t = Topic.objects.filter(pk=o["tu_de_tai"]).first()
            if t is None:
                raise CommandError(f"Không có đề tài pk={o['tu_de_tai']}")
            rows.append(
                dict(
                    title=t.title,
                    description=t.description,
                    technologies=t.technologies or "",
                    year=2024,
                    lecturer_name="ThS. Khoá trước",
                    result_note="Đã bảo vệ",
                )
            )
        added = sum(ArchivedTopic.objects.get_or_create(title=r["title"], year=r["year"], defaults=r)[1] for r in rows)
        self.stdout.write(f"Đã thêm {added} đề tài khoá trước (tổng {ArchivedTopic.objects.count()}).")
