"""Lệnh chạy phân công đề tài cho đợt đăng ký:

python manage.py allocate_period --algorithm ILP
python manage.py allocate_period --algorithm GREEDY
python manage.py allocate_period --period 1 --algorithm ILP
"""

from django.core.management.base import BaseCommand, CommandError

from allocate.services import run_allocation
from catalog.models import RegistrationPeriod


class Command(BaseCommand):
    help = "Chạy thuật toán phân công đề tài (ILP hoặc Greedy) cho đợt đăng ký."

    def add_arguments(self, parser):
        parser.add_argument(
            "--algorithm",
            type=str,
            choices=["ILP", "GREEDY"],
            default="ILP",
            help="Thuật toán phân công: ILP hoặc GREEDY (mặc định: ILP).",
        )
        parser.add_argument(
            "--period",
            type=int,
            default=None,
            help="ID đợt đăng ký. Mặc định lấy đợt đang mở/đã đóng mới nhất.",
        )

    def handle(self, *args, **options):
        algorithm = options["algorithm"].upper()
        period_id = options.get("period")

        if period_id:
            try:
                period = RegistrationPeriod.objects.get(pk=period_id)
            except RegistrationPeriod.DoesNotExist as err:
                raise CommandError(f"Không tìm thấy đợt đăng ký với ID {period_id}") from err
        else:
            period = (
                RegistrationPeriod.objects.filter(
                    status__in=[
                        RegistrationPeriod.Status.OPEN,
                        RegistrationPeriod.Status.CLOSED,
                        RegistrationPeriod.Status.OPTIMIZED,
                    ]
                )
                .order_by("-start_at")
                .first()
            )
            if not period:
                period = RegistrationPeriod.objects.order_by("-start_at").first()

        if not period:
            raise CommandError("Chưa có đợt đăng ký nào trong hệ thống.")

        self.stdout.write(f"Đang chạy phân công đợt '{period.name}' bằng thuật toán {algorithm}...")
        result = run_allocation(period, algorithm=algorithm)
        m = result["metrics"]
        msg = (
            f"Hoàn thành phân công cho đợt '{period.name}': "
            f"Tỉ lệ xếp: {m['assigned_rate']:.1%}, "
            f"NV1: {m['nv1_rate']:.1%}, "
            f"Top3: {m['top3_rate']:.1%}, "
            f"Điểm TB: {m['avg_match']:.1f}, "
            f"Vi phạm: {m['quota_violations']}, "
            f"Thời gian: {m['elapsed_time']}s"
        )
        self.stdout.write(self.style.SUCCESS(msg))
