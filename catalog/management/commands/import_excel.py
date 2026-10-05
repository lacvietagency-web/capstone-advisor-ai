"""Lệnh quản trị: nhập dữ liệu Sinh viên, Giảng viên, Đề tài, Kỹ năng từ tệp Excel (UC15).

Cú pháp:
    python manage.py import_excel <file.xlsx>

Công thức tổng hợp bản ghi:
    N_tong = N_SV + N_GV + N_DeTai + N_KyNang
"""

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from catalog.importer import import_excel_data


class Command(BaseCommand):
    help = "Nhập dữ liệu Sinh viên, Giảng viên, Đề tài, Kỹ năng từ tệp Excel (.xlsx)"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Đường dẫn đến tệp Excel (.xlsx)")

    def handle(self, *args, **options):
        file_path = Path(options["file_path"])
        if not file_path.exists():
            raise CommandError(f"Tệp không tồn tại: {file_path}")

        success, errors, stats = import_excel_data(file_path)
        if not success:
            self.stderr.write(self.style.ERROR(f"Lỗi nhập dữ liệu từ {file_path} (đã hoàn tác toàn bộ thay đổi):"))
            for err in errors:
                self.stderr.write(self.style.ERROR(f"  - {err}"))
            raise CommandError(f"Nhập dữ liệu thất bại với {len(errors)} lỗi.")

        total = stats["students"] + stats["lecturers"] + stats["topics"] + stats["skills"]
        self.stdout.write(
            self.style.SUCCESS(
                f"Đã nhập thành công tổng cộng {total} bản ghi từ {file_path}:\n"
                f"  - Sinh viên: {stats['students']}\n"
                f"  - Giảng viên: {stats['lecturers']}\n"
                f"  - Đề tài: {stats['topics']}\n"
                f"  - Kỹ năng: {stats['skills']}"
            )
        )
