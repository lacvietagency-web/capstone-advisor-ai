"""Lệnh quản trị tính toán và lưu bộ trọng số AHP từ file ma trận so sánh cặp:

python manage.py ahp_weights --matrix recommend/ahp_mau.json --name "Chuyên gia v1"
"""

import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from recommend.ahp import calculate_ahp
from recommend.models import WeightSet


class Command(BaseCommand):
    help = "Tính toán vector trọng số AHP và kiểm tra tỷ số nhất quán CR từ ma trận 5x5 dạng JSON."

    def add_arguments(self, parser):
        parser.add_argument(
            "--matrix",
            type=str,
            required=True,
            help="Đường dẫn đến file JSON chứa ma trận so sánh cặp 5x5.",
        )
        parser.add_argument(
            "--name",
            type=str,
            default=None,
            help="Tên bộ trọng số để lưu vào CSDL (bỏ trống nếu chỉ muốn xem kết quả tính).",
        )
        parser.add_argument(
            "--active",
            action="store_true",
            help="Đặt bộ trọng số này làm bộ đang sử dụng (is_active=True).",
        )

    def _load_matrix(self, file_path_str: str):
        """Đọc và giải mã dữ liệu JSON từ đường dẫn file."""
        file_path = Path(file_path_str)
        if not file_path.exists():
            raise CommandError(f"Không tìm thấy file ma trận: {file_path_str}")
        try:
            with open(file_path, encoding="utf-8") as f:
                return json.load(f)
        except Exception as err:
            raise CommandError(f"Không thể đọc file JSON '{file_path_str}': {err}") from err

    def _print_results(self, result):
        """In thông tin trọng số và các chỉ số AHP ra stdout."""
        self.stdout.write("Trọng số AHP:")
        for criterion, weight in result.weights.items():
            self.stdout.write(f"  - {criterion}: {weight:.4f}")
        self.stdout.write(f"CR: {result.cr:.4f} (λmax = {result.lambda_max:.4f}, CI = {result.ci:.4f})")

    def handle(self, *args, **options):
        raw_data = self._load_matrix(options["matrix"])
        try:
            result = calculate_ahp(raw_data)
        except Exception as err:
            raise CommandError(f"Lỗi tính toán AHP: {err}") from err

        self._print_results(result)

        if not result.is_consistent:
            raise CommandError(f"Ma trận thiếu nhất quán: CR = {result.cr:.4f} >= 0.1, bị từ chối.")

        name = options.get("name")
        if name:
            matrix_list = raw_data if isinstance(raw_data, list) else raw_data.get("matrix", raw_data)
            ws, created = WeightSet.objects.update_or_create(
                name=name,
                defaults={
                    "weights": result.weights,
                    "matrix": matrix_list,
                    "cr": result.cr,
                    "is_active": options.get("active", False),
                },
            )
            action = "Tạo mới" if created else "Cập nhật"
            self.stdout.write(self.style.SUCCESS(f"{action} bộ trọng số '{ws.name}' thành công."))
        else:
            self.stdout.write(self.style.SUCCESS("Ma trận đạt độ nhất quán (CR < 0.1)."))
