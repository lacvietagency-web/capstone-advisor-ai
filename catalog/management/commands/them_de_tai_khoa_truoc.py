"""Nạp đề tài khoá trước mẫu vào CSDL đang chạy để minh hoạ "tư vấn cải tiến" — chỉ thêm, chạy lại không tạo trùng.

python manage.py them_de_tai_khoa_truoc                 # 4 đề tài mẫu
python manage.py them_de_tai_khoa_truoc --tu-de-tai 12  # + chép đề tài 12 thành 1 bản khoá 2024
python manage.py them_de_tai_khoa_truoc --tu-file /duong/dan/de-tai-khoa-truoc.jsonl
    # kho thật, mỗi dòng {"title","description","technologies","year","lecturer_name","result_note","future_work"}
    # — file chứa dữ liệu trường: để NGOÀI repo
"""

import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from catalog.management.commands.seed_demo import ARCHIVE_SAMPLES
from catalog.models import ArchivedTopic, Topic


class Command(BaseCommand):
    help = "Thêm đề tài khoá trước mẫu (không xoá dữ liệu, không tạo trùng)."

    def add_arguments(self, parser):
        parser.add_argument("--tu-de-tai", type=int, help="Mã (pk) đề tài đang có, chép thành 1 đề tài khoá 2024")
        parser.add_argument("--tu-file", help="File JSONL đề tài khoá trước thật (bỏ 4 đề tài mẫu)")

    def handle(self, *args, **o):
        rows = _read_jsonl(o["tu_file"]) if o["tu_file"] else list(ARCHIVE_SAMPLES)
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


def _read_jsonl(path):
    keys = ("title", "description", "technologies", "year", "lecturer_name", "result_note", "future_work")
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError as e:
        raise CommandError(f"Không đọc được {path}: {e}") from e
    rows = []
    for n, line in enumerate(lines, 1):
        if not line.strip():
            continue
        r = json.loads(line)
        if not r.get("title") or not r.get("year"):
            raise CommandError(f"Dòng {n}: thiếu title/year")
        rows.append({k: r.get(k) or "" for k in keys} | {"year": int(r["year"])})
    return rows
