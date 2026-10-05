"""Dịch vụ nghiệp vụ phân công — gọi từ views và management commands.

Bao gồm các hàm:
- run_allocation: chạy thuật toán phân công (ILP / Greedy), cập nhật kết quả nháp và đợt.
- calculate_period_metrics: đo lường các chỉ số của đợt phân công hiện tại.
- get_phase2_suggestions: gợi ý các đề tài còn chỗ cho sinh viên chưa được xếp ở Pha 2.
- manual_assign: Khoa chỉnh tay gán đề tài cho sinh viên.
- publish_allocations: chốt kết quả phân công và công bố đợt.
"""

import time

from django.db import transaction

from catalog.models import AuditLog, Lecturer, Preference, RegistrationPeriod, Student, Topic
from recommend.engine import DEFAULT_WEIGHTS, Profile, eligible, score_student
from recommend.models import Recommendation

from .models import Allocation
from .solver import metrics as calculate_metrics
from .solver import solve_greedy, solve_ilp


def _prepare_solver_data(period, students):
    """Chuẩn bị dữ liệu đầu vào cho bộ giải (khoá là id): prefs, scores, cap, owner, quota, gpa.

    - prefs[sv] = danh sách đề tài theo thứ tự NV, ĐÃ BỎ các NV giảng viên từ chối (UC12).
      SV bị từ chối hết vẫn có mặt với danh sách rỗng → được ghi nhận "chưa xếp".
    - scores lấy từ bảng Recommendation; cặp nào chưa có (SV chọn ngoài Top gợi ý) thì tính bù bằng M1–M4.
    """
    prefs = {s.id: [] for s in students}
    for sid, tid, status in (
        Preference.objects.filter(period=period, student__in=students)
        .order_by("student_id", "rank")
        .values_list("student_id", "topic_id", "status")
    ):
        if status != Preference.Status.REJECTED:
            prefs[sid].append(tid)
    all_topic_ids = {t for ts in prefs.values() for t in ts}

    recs = Recommendation.objects.filter(student__in=students, topic_id__in=all_topic_ids)
    scores = {(r.student_id, r.topic_id): float(r.final_score) for r in recs}

    topics_map = Topic.objects.in_bulk(all_topic_ids)
    for s in students:
        missing = [topics_map[t] for t in prefs[s.id] if (s.id, t) not in scores]
        if missing:  # không gọi LLM ở đây: phân công phải nhanh và tái lập được
            for c in score_student(s, missing, semantic=False, llm=False):
                scores[s.id, c.topic.id] = float(c.final(DEFAULT_WEIGHTS))

    topics = Topic.objects.all()
    cap = {t.id: t.capacity for t in topics}
    owner = {t.id: t.lecturer_id for t in topics}
    quota = {lec.id: lec.max_students for lec in Lecturer.objects.all()}
    gpa = {s.id: float(s.gpa) for s in students}
    return prefs, scores, cap, owner, quota, gpa


def _save_allocation_results(period, students, assign, prefs, scores, algorithm):
    """Lưu kết quả phân công nháp vào bảng Allocation và cập nhật trạng thái đợt."""
    topics_map = {t.id: t for t in Topic.objects.filter(id__in=[t_id for t_id in assign.values() if t_id])}
    source = Allocation.Source.ILP if algorithm == "ILP" else Allocation.Source.GREEDY
    real_rank = {
        (sid, tid): rank
        for sid, tid, rank in Preference.objects.filter(period=period).values_list("student_id", "topic_id", "rank")
    }

    with transaction.atomic():
        for s in students:
            assigned_topic_id = assign.get(s.id)
            topic_obj = topics_map.get(assigned_topic_id)
            rank = real_rank.get((s.id, assigned_topic_id))  # số NV gốc (NV bị từ chối làm danh sách ngắn lại)
            score_val = scores.get((s.id, assigned_topic_id)) if assigned_topic_id else None

            Allocation.objects.update_or_create(
                period=period,
                student=s,
                defaults={
                    "topic": topic_obj,
                    "preference_rank": rank,
                    "match_score": score_val,
                    "status": Allocation.Status.DRAFT,
                    "source": source,
                },
            )
        period.status = RegistrationPeriod.Status.OPTIMIZED
        period.save()


def run_allocation(period: RegistrationPeriod, algorithm: str = "ILP", user=None) -> dict:
    """Chạy thuật toán phân công cho đợt đăng ký và lưu kết quả nháp.

    Hàm dùng chung cho giao diện Khoa và lệnh dòng lệnh allocate_period.
    """
    students_qs = Student.objects.filter(preferences__period=period).distinct()
    if not students_qs.exists():
        students_qs = Student.objects.all()
    students = list(students_qs.select_related("user"))

    prefs, scores, cap, owner, quota, gpa = _prepare_solver_data(period, students)

    t0 = time.perf_counter()
    if algorithm == "ILP":
        assign = solve_ilp(prefs, scores, cap, owner, quota, gpa)
    else:
        assign = solve_greedy(prefs, scores, cap, owner, quota, gpa)
    elapsed_time = round(time.perf_counter() - t0, 3)

    metrics_result = calculate_metrics(assign, prefs, scores, cap, owner, quota)
    metrics_result["elapsed_time"] = elapsed_time

    _save_allocation_results(period, students, assign, prefs, scores, algorithm)

    AuditLog.objects.create(
        user=user,
        action="run_allocation",
        entity="RegistrationPeriod",
        entity_id=str(period.pk),
        detail={"algorithm": algorithm, "metrics": metrics_result},
    )

    return {"assign": assign, "metrics": metrics_result, "elapsed_time": elapsed_time}


def calculate_period_metrics(period: RegistrationPeriod) -> dict:
    """Đo lường metrics từ các bản ghi phân công hiện có trong cơ sở dữ liệu."""
    allocations = list(Allocation.objects.filter(period=period).select_related("student", "topic"))
    if not allocations:
        return {
            "assigned_rate": 0.0,
            "nv1_rate": 0.0,
            "top3_rate": 0.0,
            "mean_rank": 0.0,
            "avg_match": 0.0,
            "p10_match": 0.0,
            "quota_violations": 0,
            "elapsed_time": 0.0,
        }

    students = [a.student for a in allocations]
    prefs, scores, cap, owner, quota, _ = _prepare_solver_data(period, students)
    assign = {a.student_id: (a.topic_id if a.topic else None) for a in allocations}

    return calculate_metrics(assign, prefs, scores, cap, owner, quota)


def _check_topic_capacity(topic, period, cap_usage, quota_usage):
    """Kiểm tra đề tài và giảng viên còn chỗ trống trong đợt hay không."""
    used_cap = cap_usage.get(topic.id, 0)
    if used_cap >= topic.capacity:
        return False, 0, 0
    lec = topic.lecturer
    used_quota = quota_usage.get(lec.id, 0)
    if used_quota >= lec.max_students:
        return False, 0, 0
    return True, topic.capacity - used_cap, lec.max_students - used_quota


def get_phase2_suggestions(period: RegistrationPeriod, student: Student) -> list[dict]:
    """Gợi ý danh sách đề tài còn chỗ mà sinh viên đủ điều kiện cho Pha 2.

    Các đề tài được lọc theo:
        1. Đề tài còn chỗ trống trong đợt và giảng viên chưa vượt chỉ tiêu.
        2. Sinh viên đủ điều kiện cứng (GPA, môn tiên quyết, kỹ năng bắt buộc).
    Kết quả được sắp xếp theo điểm phù hợp giảm dần.
    """
    allocations = Allocation.objects.filter(period=period).exclude(topic__isnull=True)
    cap_usage = {}
    quota_usage = {}
    for a in allocations:
        cap_usage[a.topic_id] = cap_usage.get(a.topic_id, 0) + 1
        lec_id = a.topic.lecturer_id
        quota_usage[lec_id] = quota_usage.get(lec_id, 0) + 1

    profile = Profile(student)
    open_topics = Topic.objects.filter(status=Topic.Status.OPEN).select_related("lecturer__user")

    valid_topics = []
    rem_map = {}
    for t in open_topics:
        is_available, rem_cap, rem_quota = _check_topic_capacity(t, period, cap_usage, quota_usage)
        if not is_available:
            continue
        is_ok, _ = eligible(profile, t)
        if is_ok:
            valid_topics.append(t)
            rem_map[t.id] = (rem_cap, rem_quota)

    if not valid_topics:
        return []

    cands = score_student(student, valid_topics, semantic=False)
    suggestions = []
    for c in cands:
        t_id = c.topic.id
        rem_cap, rem_quota = rem_map[t_id]
        suggestions.append(
            {
                "topic": c.topic,
                "score": round(c.final(DEFAULT_WEIGHTS), 1),
                "remaining_cap": rem_cap,
                "remaining_quota": rem_quota,
            }
        )
    suggestions.sort(key=lambda item: item["score"], reverse=True)
    return suggestions


def manual_assign(period: RegistrationPeriod, student: Student, topic: Topic | None, user=None) -> Allocation:
    """Khoa gán thủ công một đề tài cho sinh viên (Pha 2), nguồn là MANUAL."""
    score_val = None
    rank_val = None
    if topic:
        pref = Preference.objects.filter(period=period, student=student, topic=topic).first()
        rank_val = pref.rank if pref else None
        rec = Recommendation.objects.filter(student=student, topic=topic).first()
        if rec:
            score_val = rec.final_score
        else:
            cands = score_student(student, [topic], semantic=False, llm=False)
            if cands:
                score_val = round(cands[0].final(DEFAULT_WEIGHTS), 1)

    alloc, _ = Allocation.objects.update_or_create(
        period=period,
        student=student,
        defaults={
            "topic": topic,
            "preference_rank": rank_val,
            "match_score": score_val,
            "status": Allocation.Status.DRAFT,
            "source": Allocation.Source.MANUAL,
        },
    )

    AuditLog.objects.create(
        user=user,
        action="manual_assign",
        entity="Allocation",
        entity_id=str(alloc.pk),
        detail={
            "student_id": student.pk,
            "topic_id": topic.pk if topic else None,
            "source": Allocation.Source.MANUAL,
        },
    )
    return alloc


def publish_allocations(period: RegistrationPeriod, user=None) -> int:
    """Chốt kết quả phân công: chuyển toàn bộ DRAFT sang OFFICIAL, đợt sang PUBLISHED."""
    with transaction.atomic():
        updated_count = Allocation.objects.filter(period=period).update(status=Allocation.Status.OFFICIAL)
        period.status = RegistrationPeriod.Status.PUBLISHED
        period.save()

        AuditLog.objects.create(
            user=user,
            action="publish_allocations",
            entity="RegistrationPeriod",
            entity_id=str(period.pk),
            detail={"status": RegistrationPeriod.Status.PUBLISHED, "total_allocations": updated_count},
        )
    return updated_count
