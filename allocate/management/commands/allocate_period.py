"""Lệnh phân công đề tài tốt nghiệp cho đợt đăng ký.

Hỗ trợ thuật toán ILP (tối ưu toàn cục) và GREEDY (tham lam).
Cách dùng:
    python manage.py allocate_period --algorithm ILP
    python manage.py allocate_period --algorithm GREEDY --period 1
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from allocate.models import Allocation
from allocate.solver import metrics, solve_greedy, solve_ilp
from catalog.models import Preference, RegistrationPeriod
from recommend.models import Recommendation


class Command(BaseCommand):
    help = "Phân công đề tài cho đợt đăng ký sử dụng thuật toán ILP hoặc GREEDY."

    def add_arguments(self, parser):
        parser.add_argument(
            "--algorithm",
            type=str,
            default="ILP",
            choices=["ILP", "GREEDY", "ilp", "greedy"],
            help="Thuật toán phân công (ILP hoặc GREEDY). Mặc định là ILP.",
        )
        parser.add_argument(
            "--period",
            type=int,
            default=None,
            help="ID của đợt đăng ký (mặc định lấy đợt mới nhất).",
        )

    def _get_period(self, period_id):
        """Lấy đợt đăng ký theo ID hoặc đợt mới nhất."""
        if period_id:
            try:
                return RegistrationPeriod.objects.get(pk=period_id)
            except RegistrationPeriod.DoesNotExist:
                raise CommandError(f"Không tìm thấy đợt đăng ký với ID {period_id}.") from None

        period = RegistrationPeriod.objects.order_by("-id").first()
        if not period:
            raise CommandError("Không tìm thấy đợt đăng ký nào trong hệ thống.")
        return period

    def _build_solver_data(self, period):
        """Dựng dữ liệu đầu vào cho bộ giải từ Preference và Recommendation."""
        preferences = (
            Preference.objects.filter(period=period)
            .select_related("student", "topic", "topic__lecturer")
            .order_by("student_id", "rank")
        )

        prefs = {}
        topics = set()
        students = set()
        self.real_rank = {}  # (SV, đề tài) → số NV gốc; NV bị từ chối làm danh sách ngắn lại nên không dùng vị trí
        for p in preferences:
            self.real_rank[p.student, p.topic] = p.rank
            students.add(p.student)
            prefs.setdefault(p.student, [])
            if p.status == Preference.Status.REJECTED:  # UC12: GV đã từ chối → không xếp vào đề tài này
                continue
            prefs[p.student].append(p.topic)
            topics.add(p.topic)

        recs = Recommendation.objects.filter(student__in=students, topic__in=topics).values_list(
            "student_id", "topic_id", "final_score"
        )
        rec_dict = {(st_id, tp_id): score for st_id, tp_id, score in recs}

        scores = {(s, t): float(rec_dict.get((s.id, t.id), 0.0)) for s in students for t in prefs.get(s, [])}

        cap = {t: t.capacity for t in topics}
        owner = {t: t.lecturer for t in topics}
        lecturers = {t.lecturer for t in topics if t.lecturer}
        quota = {lec: lec.max_students for lec in lecturers}
        gpa = {s: float(s.gpa) for s in students}

        return prefs, scores, cap, owner, quota, gpa

    def _save_allocations(self, period, assign, prefs, scores, algo):
        """Lưu kết quả phân công dưới dạng bản nháp (DRAFT)."""
        source_val = Allocation.Source.ILP if algo == "ILP" else Allocation.Source.GREEDY

        with transaction.atomic():
            Allocation.objects.filter(period=period, status=Allocation.Status.DRAFT).delete()

            allocations = []
            for s, t in assign.items():
                rank = None
                score = None
                if t is not None:
                    rank = self.real_rank.get((s, t))
                    score = scores.get((s, t), 0.0)

                allocations.append(
                    Allocation(
                        period=period,
                        student=s,
                        topic=t,
                        preference_rank=rank,
                        match_score=score,
                        status=Allocation.Status.DRAFT,
                        source=source_val,
                    )
                )
            Allocation.objects.bulk_create(allocations)

    def _print_metrics(self, period, algo, m):
        """Hiển thị các chỉ số đánh giá phân công."""
        self.stdout.write(
            self.style.SUCCESS(
                f"=== KẾT QUẢ PHÂN CÔNG ĐỢT: {period.name} ({algo}) ===\n"
                f"  - Tỷ lệ được xếp (assigned_rate):    {m['assigned_rate']:.1%}\n"
                f"  - Đạt NV1 (nv1_rate):                {m['nv1_rate']:.1%}\n"
                f"  - Đạt Top 3 (top3_rate):             {m['top3_rate']:.1%}\n"
                f"  - Thứ hạng trung bình (mean_rank):   {m['mean_rank']:.2f}\n"
                f"  - Điểm phù hợp TB (avg_match):       {m['avg_match']:.2f}\n"
                f"  - Phân vị 10 điểm (p10_match):       {m['p10_match']:.2f}\n"
                f"  - Vi phạm chỉ tiêu (quota_violations): {m['quota_violations']}"
            )
        )

    def handle(self, *args, **options):
        algo = options["algorithm"].upper()
        period = self._get_period(options.get("period"))

        prefs, scores, cap, owner, quota, gpa = self._build_solver_data(period)

        if algo == "ILP":
            assign = solve_ilp(prefs, scores, cap, owner, quota, gpa)
        elif algo == "GREEDY":
            assign = solve_greedy(prefs, scores, cap, owner, quota, gpa)
        else:
            raise CommandError(f"Thuật toán không hỗ trợ: {algo}. Chọn 'ILP' hoặc 'GREEDY'.")

        m = metrics(assign, prefs, scores, cap, owner, quota)
        self._save_allocations(period, assign, prefs, scores, algo)
        self._print_metrics(period, algo, m)
