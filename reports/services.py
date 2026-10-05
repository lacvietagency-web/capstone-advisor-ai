"""Dịch vụ tính toán báo cáo thống kê dành cho Khoa (UC17, UC21).

Các nghiệp vụ bao gồm:
1. Thống kê tình hình sinh viên đăng ký nguyện vọng (đã đăng ký / chưa đăng ký).
2. Phân bố nguyện vọng 1 (NV1) theo đề tài (xếp hạng đề tài hot).
3. Phân bố nguyện vọng 1 theo lĩnh vực nghiên cứu/công nghệ.
4. Tải hướng dẫn của giảng viên (số sinh viên được xếp / chỉ tiêu).
5. So sánh thuật toán phân công ILP vs Greedy trên cùng một đợt (chạy mô phỏng, không lưu CSDL).
"""

import time

from django.db.models import Count

from allocate.models import Allocation
from allocate.services import _prepare_solver_data
from allocate.solver import metrics as calculate_metrics
from allocate.solver import solve_greedy, solve_ilp
from catalog.models import Field, Lecturer, Preference, RegistrationPeriod, Student


def get_registration_stats(period: RegistrationPeriod | None) -> dict:
    """Thống kê số lượng sinh viên đã đăng ký nguyện vọng và chưa đăng ký trong đợt.

    Công thức toán:
    - Tổng số sinh viên trong hệ thống:
        N_total = |{s in Student}|
    - Số sinh viên đã đăng ký (ít nhất 1 nguyện vọng trong đợt):
        N_reg = |{s in Student | ton_tai p in Preference: p.student = s va p.period = period}|
    - Số sinh viên chưa đăng ký:
        N_unreg = N_total - N_reg
    - Tỷ lệ sinh viên đã đăng ký:
        R_reg = (N_reg / N_total) * 100%  (bang 0.0 neu N_total = 0)
    - Tỷ lệ sinh viên chưa đăng ký:
        R_unreg = (N_unreg / N_total) * 100%  (bang 0.0 neu N_total = 0)
    """
    total_students = Student.objects.count()
    if not period or total_students == 0:
        return {
            "total_students": total_students,
            "registered_students": 0,
            "unregistered_students": total_students,
            "registered_rate": 0.0,
            "unregistered_rate": 100.0 if total_students > 0 else 0.0,
        }

    registered_students = Student.objects.filter(preferences__period=period).distinct().count()
    unregistered_students = max(0, total_students - registered_students)
    registered_rate = round((registered_students / total_students) * 100, 1)
    unregistered_rate = round((unregistered_students / total_students) * 100, 1)

    return {
        "total_students": total_students,
        "registered_students": registered_students,
        "unregistered_students": unregistered_students,
        "registered_rate": registered_rate,
        "unregistered_rate": unregistered_rate,
    }


def get_topic_nv1_distribution(period: RegistrationPeriod | None, limit: int = 10) -> list[dict]:
    """Thống kê phân bố Nguyện vọng 1 (NV1) theo đề tài, xếp hạng các đề tài hot nhất.

    Công thức toán:
    Voi moi de tai t in Topic:
    - So luong sinh vien chon de tai t o vi tri NV1 (rank = 1):
        C_NV1(t) = |{p in Preference | p.period = period va p.topic = t va p.rank = 1}|
    - Ti le canh tranh tren suc chua (capacity):
        D(t) = C_NV1(t) / capacity(t)
    - Ti trong so voi tong so NV1 trong dot:
        P(t) = (C_NV1(t) / sum_t'(C_NV1(t'))) * 100%
    """
    if not period:
        return []

    nv1_qs = (
        Preference.objects.filter(period=period, rank=1)
        .values(
            "topic_id",
            "topic__title",
            "topic__capacity",
            "topic__lecturer__user__last_name",
            "topic__lecturer__user__first_name",
            "topic__lecturer__user__username",
        )
        .annotate(nv1_count=Count("id"))
        .order_by("-nv1_count", "topic__title")
    )

    total_nv1 = sum(item["nv1_count"] for item in nv1_qs)
    limited_items = list(nv1_qs[:limit])

    results = []
    for item in limited_items:
        cnt = item["nv1_count"]
        cap = item["topic__capacity"] or 1
        last_name = item["topic__lecturer__user__last_name"] or ""
        first_name = item["topic__lecturer__user__first_name"] or ""
        lec_name = f"{last_name} {first_name}".strip() or item["topic__lecturer__user__username"]

        results.append(
            {
                "topic_id": item["topic_id"],
                "title": item["topic__title"],
                "lecturer_name": lec_name,
                "capacity": cap,
                "nv1_count": cnt,
                "competition_rate": round(cnt / cap, 2),
                "percentage": round((cnt / total_nv1) * 100, 1) if total_nv1 > 0 else 0.0,
            }
        )

    return results


def get_field_distribution(period: RegistrationPeriod | None) -> list[dict]:
    """Thống kê phân bố Nguyện vọng 1 (NV1) theo lĩnh vực nghiên cứu/công nghệ.

    Công thức toán:
    Voi moi linh vuc f in Field:
    - So luong nguyen vong 1 dang ky vao de tai thuoc linh vuc f:
        C(f) = |{p in Preference | p.period = period va p.rank = 1 va f in p.topic.fields}|
    - Ti trong cua linh vuc f:
        P(f) = (C(f) / sum_f'(C(f'))) * 100%  (bang 0.0 neu tong = 0)
    """
    if not period:
        return []

    field_qs = (
        Preference.objects.filter(period=period, rank=1, topic__fields__isnull=False)
        .values("topic__fields__id", "topic__fields__name")
        .annotate(count=Count("id"))
        .order_by("-count", "topic__fields__name")
    )

    total_count = sum(item["count"] for item in field_qs)
    field_data = {item["topic__fields__id"]: item["count"] for item in field_qs}

    results = []
    for f in Field.objects.all().order_by("name"):
        cnt = field_data.get(f.id, 0)
        pct = round((cnt / total_count) * 100, 1) if total_count > 0 else 0.0
        results.append(
            {
                "field_id": f.id,
                "field_name": f.name,
                "count": cnt,
                "percentage": pct,
            }
        )

    results.sort(key=lambda x: (-x["count"], x["field_name"]))
    return results


def _build_lecturer_load_item(lec: Lecturer, assigned_count: int) -> dict:
    """Tạo bản ghi tải cho một giảng viên với các chỉ số và trạng thái.

    Công thức toán:
        load_rate = (assigned_count / max_students) * 100%
    """
    cap = lec.max_students or 1
    rate = round((assigned_count / cap) * 100, 1)

    if assigned_count > cap:
        status_text = "Quá tải"
        badge_class = "danger"
    elif assigned_count == cap and cap > 0:
        status_text = "Đầy chỉ tiêu"
        badge_class = "success"
    elif assigned_count > 0:
        status_text = "Đang nhận"
        badge_class = "info"
    else:
        status_text = "Chưa có SV"
        badge_class = "secondary"

    return {
        "lecturer_id": lec.id,
        "name": lec.user.get_full_name() or lec.user.username,
        "department": lec.department or "Chưa phân bộ môn",
        "assigned_count": assigned_count,
        "capacity": cap,
        "load_rate": rate,
        "status": status_text,
        "badge_class": badge_class,
    }


def get_lecturer_load(
    period: RegistrationPeriod | None,
    assign: dict[int, int | None] | None = None,
) -> list[dict]:
    """Thống kê tải hướng dẫn của từng giảng viên (số sinh viên được xếp / chỉ tiêu).

    Công thức toán:
    Voi moi giang vien g in Lecturer:
    - So sinh vien duoc xep huong dan:
        S(g) = |{s in Student | assigned(s) thuoc giang vien g}|
    - Ti le tai:
        L(g) = (S(g) / max_students(g)) * 100%
    """
    lecturers = list(Lecturer.objects.select_related("user").order_by("user__last_name", "user__first_name"))
    if not lecturers:
        return []

    counts: dict[int, int] = {lec.id: 0 for lec in lecturers}

    if assign is not None:
        from catalog.models import Topic

        assigned_topic_ids = [t_id for t_id in assign.values() if t_id is not None]
        topic_owner = dict(Topic.objects.filter(id__in=assigned_topic_ids).values_list("id", "lecturer_id"))
        for t_id in assigned_topic_ids:
            lec_id = topic_owner.get(t_id)
            if lec_id in counts:
                counts[lec_id] += 1
    elif period and Allocation.objects.filter(period=period, topic__isnull=False).exists():
        alloc_qs = (
            Allocation.objects.filter(period=period, topic__isnull=False)
            .values("topic__lecturer_id")
            .annotate(cnt=Count("id"))
        )
        for item in alloc_qs:
            lec_id = item["topic__lecturer_id"]
            if lec_id in counts:
                counts[lec_id] = item["cnt"]

    results = [_build_lecturer_load_item(lec, counts.get(lec.id, 0)) for lec in lecturers]
    results.sort(key=lambda x: (-x["load_rate"], -x["assigned_count"], x["name"]))
    return results


def _build_empty_comparison() -> dict:
    """Trả về cấu trúc số liệu so sánh mặc định khi không có dữ liệu."""
    empty_metric = {
        "assigned_rate": 0.0,
        "assigned_pct": 0.0,
        "nv1_rate": 0.0,
        "nv1_pct": 0.0,
        "top3_rate": 0.0,
        "top3_pct": 0.0,
        "unassigned_count": 0,
        "unassigned_rate": 0.0,
        "mean_rank": 0.0,
        "avg_match": 0.0,
        "p10_match": 0.0,
        "quota_violations": 0,
        "elapsed_time": 0.0,
    }
    return {
        "ilp": dict(empty_metric),
        "greedy": dict(empty_metric),
        "delta": {
            "nv1_pct": 0.0,
            "top3_pct": 0.0,
            "assigned_pct": 0.0,
            "unassigned_count": 0,
            "avg_match": 0.0,
        },
        "assign_ilp": {},
        "assign_greedy": {},
    }


def _format_solver_metrics(
    raw_metrics: dict,
    assign: dict[int, int | None],
    total_students: int,
    elapsed_time: float,
) -> dict:
    """Định dạng kết quả metrics từ bộ giải kèm phần trăm và thời gian thực thi.

    Công thức:
        nv1_pct = nv1_rate * 100%
        top3_pct = top3_rate * 100%
        assigned_pct = assigned_rate * 100%
        unassigned_count = sum(1 cho s co assigned(s) is None)
        unassigned_rate = (unassigned_count / total_students) * 100%
    """
    unassigned_count = sum(1 for t_id in assign.values() if t_id is None)
    unassigned_rate = round((unassigned_count / total_students) * 100, 1) if total_students > 0 else 0.0

    return {
        "assigned_rate": raw_metrics.get("assigned_rate", 0.0),
        "assigned_pct": round(raw_metrics.get("assigned_rate", 0.0) * 100, 1),
        "nv1_rate": raw_metrics.get("nv1_rate", 0.0),
        "nv1_pct": round(raw_metrics.get("nv1_rate", 0.0) * 100, 1),
        "top3_rate": raw_metrics.get("top3_rate", 0.0),
        "top3_pct": round(raw_metrics.get("top3_rate", 0.0) * 100, 1),
        "unassigned_count": unassigned_count,
        "unassigned_rate": unassigned_rate,
        "mean_rank": round(raw_metrics.get("mean_rank", 0.0), 2),
        "avg_match": round(raw_metrics.get("avg_match", 0.0), 1),
        "p10_match": round(raw_metrics.get("p10_match", 0.0), 1),
        "quota_violations": raw_metrics.get("quota_violations", 0),
        "elapsed_time": elapsed_time,
    }


def compare_algorithms(period: RegistrationPeriod | None) -> dict:
    """So sánh hiệu quả thuật toán ILP vs Greedy trên cùng một đợt đăng ký.

    Chạy mô phỏng cả hai bộ giải độc lập trong bộ nhớ, KHÔNG lưu hay thay đổi CSDL.

    Công thức toán đánh giá so sánh:
    1. Tỷ lệ phân công thành công:
        R_assigned = (N_assigned / N_total) * 100%
    2. Tỷ lệ sinh viên đạt NV1:
        R_NV1 = (N_NV1 / N_total) * 100%
    3. Tỷ lệ sinh viên đạt Top 3 nguyện vọng:
        R_Top3 = (N_Top3 / N_total) * 100%
    4. Số sinh viên chưa được xếp:
        N_unassigned = N_total - N_assigned
    5. Độ chênh lệch giữa ILP và Greedy:
        Delta_NV1 = R_NV1(ILP) - R_NV1(Greedy)
        Delta_Top3 = R_Top3(ILP) - R_Top3(Greedy)
        Delta_Unassigned = N_unassigned(ILP) - N_unassigned(Greedy)
    """
    if not period:
        return _build_empty_comparison()

    students_qs = Student.objects.filter(preferences__period=period).distinct()
    if not students_qs.exists():
        students_qs = Student.objects.all()
    students = list(students_qs.select_related("user"))

    if not students:
        return _build_empty_comparison()

    prefs, scores, cap, owner, quota, gpa = _prepare_solver_data(period, students)

    # 1. Chạy ILP (mô phỏng)
    t0_ilp = time.perf_counter()
    assign_ilp = solve_ilp(prefs, scores, cap, owner, quota, gpa)
    elapsed_ilp = round(time.perf_counter() - t0_ilp, 3)
    raw_ilp = calculate_metrics(assign_ilp, prefs, scores, cap, owner, quota)

    # 2. Chạy Greedy (mô phỏng)
    t0_greedy = time.perf_counter()
    assign_greedy = solve_greedy(prefs, scores, cap, owner, quota, gpa)
    elapsed_greedy = round(time.perf_counter() - t0_greedy, 3)
    raw_greedy = calculate_metrics(assign_greedy, prefs, scores, cap, owner, quota)

    # 3. Tính toán và so sánh
    total_st = len(students)
    ilp_res = _format_solver_metrics(raw_ilp, assign_ilp, total_st, elapsed_ilp)
    greedy_res = _format_solver_metrics(raw_greedy, assign_greedy, total_st, elapsed_greedy)

    delta = {
        "nv1_pct": round(ilp_res["nv1_pct"] - greedy_res["nv1_pct"], 1),
        "top3_pct": round(ilp_res["top3_pct"] - greedy_res["top3_pct"], 1),
        "assigned_pct": round(ilp_res["assigned_pct"] - greedy_res["assigned_pct"], 1),
        "unassigned_count": ilp_res["unassigned_count"] - greedy_res["unassigned_count"],
        "avg_match": round(ilp_res["avg_match"] - greedy_res["avg_match"], 1),
    }

    return {
        "ilp": ilp_res,
        "greedy": greedy_res,
        "delta": delta,
        "assign_ilp": assign_ilp,
        "assign_greedy": assign_greedy,
    }
