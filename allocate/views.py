"""Màn hình phân công đồ án dành cho Khoa: chạy thuật toán, bảng nháp, chỉnh tay Pha 2, chốt và công bố."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import AuditLog, Field, Lecturer, Preference, RegistrationPeriod, Student, Topic
from recommend.services import ensure_recommendations

from .models import Allocation
from .services import (
    calculate_period_metrics,
    get_phase2_suggestions,
    get_student_allocation_result,
    manual_assign,
    publish_allocations,
    run_allocation,
)

ALLOCATIONS_PER_PAGE = 20  # bảng phân công: 100+ SV một trang là không dùng được


def _check_faculty_admin(user):
    """Kiểm tra quyền truy cập: chỉ tài khoản Khoa hoặc Superuser được phép."""
    if not (getattr(user, "is_faculty_admin", False) or getattr(user, "is_superuser", False)):
        raise PermissionDenied("Chỉ tài khoản Khoa mới có quyền truy cập trang này.")


def _handle_run(request, period, algorithm):
    """Xử lý yêu cầu chạy thuật toán phân công ILP hoặc Greedy."""
    res = run_allocation(period, algorithm=algorithm, user=request.user)
    m = res["metrics"]
    request.session["allocation_metrics"] = m
    messages.success(
        request,
        f"Đã chạy phân công {algorithm} cho đợt '{period.name}'. "
        f"Tỉ lệ xếp: {m['assigned_rate']:.1%}, Điểm TB: {m['avg_match']:.1f}.",
    )
    return redirect(f"/khoa/phan-cong/?period_id={period.pk}")


def _handle_manual(request, period):
    """Xử lý Khoa chỉnh tay gán đề tài cho sinh viên (Pha 2)."""
    student_id = request.POST.get("student_id")
    topic_id = request.POST.get("topic_id")
    student = get_object_or_404(Student, pk=student_id)
    topic = get_object_or_404(Topic, pk=topic_id) if topic_id and topic_id != "none" else None
    manual_assign(period, student, topic, user=request.user)
    action_text = f"vào đề tài '{topic.title}'" if topic else "thành chưa xếp"
    messages.success(request, f"Đã cập nhật phân công cho sinh viên {student.student_code} {action_text}.")
    return redirect(f"/khoa/phan-cong/?period_id={period.pk}")


def _handle_publish(request, period):
    """Xử lý chốt danh sách phân công và công bố đợt (từ chối nếu đợt đã công bố hoặc chưa chạy phân công)."""
    if period.status == RegistrationPeriod.Status.PUBLISHED:
        messages.error(request, f"Đợt '{period.name}' đã công bố trước đó — không công bố lại.")
        return redirect(f"/khoa/phan-cong/?period_id={period.pk}")
    if not Allocation.objects.filter(period=period).exists():
        messages.error(request, "Chưa có kết quả phân công để công bố — hãy chạy ILP hoặc Greedy trước.")
        return redirect(f"/khoa/phan-cong/?period_id={period.pk}")
    count = publish_allocations(period, user=request.user)
    messages.success(
        request,
        f"Đã chốt {count} kết quả phân công thành chính thức và công bố đợt '{period.name}'.",
    )
    return redirect(f"/khoa/phan-cong/?period_id={period.pk}")


def _get_selected_period(request):
    """Lấy đợt đăng ký được chọn từ query params hoặc đợt mới nhất."""
    period_id = request.GET.get("period_id")
    if period_id:
        return get_object_or_404(RegistrationPeriod, pk=period_id)
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
    return period or RegistrationPeriod.objects.order_by("-start_at").first()


SORTS = {  # tham số ?sort= → cột sắp xếp (chỉ nhận giá trị trong bảng này)
    "code": "student__student_code",
    "gpa": "-student__gpa",
    "score": "-match_score",
    "rank": "preference_rank",
}
PER_PAGE_CHOICES = (10, 20, 50)


def _status_filter(request):
    """Lọc trạng thái: ?status=assigned|unassigned (giữ tương thích ?unassigned_only=1 cũ)."""
    if request.GET.get("unassigned_only") == "1":
        return "unassigned"
    return request.GET.get("status") or "all"


def _per_page(request):
    try:
        n = int(request.GET.get("per_page") or ALLOCATIONS_PER_PAGE)
    except ValueError:
        n = ALLOCATIONS_PER_PAGE
    return n if n in PER_PAGE_CHOICES else ALLOCATIONS_PER_PAGE


def _get_allocations_and_suggestions(period, request):
    """Lấy danh sách phân công nháp và danh sách gợi ý Pha 2 nếu có yêu cầu."""
    if not period:
        return [], None, None, []

    status = _status_filter(request)
    alloc_qs = (
        Allocation.objects.filter(period=period)
        .select_related("student__user", "topic__lecturer__user")
        .order_by(SORTS.get(request.GET.get("sort"), "student__student_code"), "student__student_code")
    )
    if status in ("unassigned", "assigned"):
        alloc_qs = alloc_qs.filter(topic__isnull=status == "unassigned")
    if request.GET.get("rank") in ("1", "2", "3"):
        alloc_qs = alloc_qs.filter(preference_rank=request.GET["rank"])
    if (request.GET.get("lecturer") or "").isdigit():
        alloc_qs = alloc_qs.filter(topic__lecturer_id=request.GET["lecturer"])
    if (request.GET.get("field") or "").isdigit():
        alloc_qs = alloc_qs.filter(topic__fields__id=request.GET["field"]).distinct()
    query = (request.GET.get("q") or "").strip()
    if query:  # tìm theo mã SV, tên SV hoặc tên đề tài
        alloc_qs = alloc_qs.filter(
            Q(student__student_code__icontains=query)
            | Q(student__user__first_name__icontains=query)
            | Q(student__user__last_name__icontains=query)
            | Q(topic__title__icontains=query)
        )
    allocations = list(alloc_qs)

    suggest_student = None
    suggestions = []
    suggest_student_id = request.GET.get("suggest_student_id")
    if suggest_student_id:
        suggest_student = Student.objects.filter(pk=suggest_student_id).first()
        if suggest_student:
            suggestions = get_phase2_suggestions(period, suggest_student)

    open_topics = Topic.objects.filter(status=Topic.Status.OPEN).select_related("lecturer__user").order_by("title")
    return allocations, suggest_student, suggestions, open_topics


@login_required
def allocation_dashboard(request):
    """Trang điều hành phân công dành riêng cho Khoa."""
    _check_faculty_admin(request.user)
    periods = list(RegistrationPeriod.objects.order_by("-start_at"))
    period = _get_selected_period(request)

    if request.method == "POST" and period:
        action = request.POST.get("action")
        if action == "run_ilp":
            return _handle_run(request, period, "ILP")
        if action == "run_greedy":
            return _handle_run(request, period, "GREEDY")
        if action == "manual_assign":
            return _handle_manual(request, period)
        if action == "publish":
            return _handle_publish(request, period)

    allocations, suggest_student, suggestions, open_topics = _get_allocations_and_suggestions(period, request)
    metrics_data = None
    if period and Allocation.objects.filter(period=period).exists():
        metrics_data = request.session.pop("allocation_metrics", None)
        if not metrics_data:
            metrics_data = calculate_period_metrics(period)
            last_run = (
                AuditLog.objects.filter(action="run_allocation", entity="RegistrationPeriod", entity_id=str(period.pk))
                .order_by("-at")
                .first()
            )  # thời gian giải lấy từ lần chạy gần nhất (đo lại khi xem trang thì không có ý nghĩa)
            last_metrics = (last_run.detail.get("metrics") or {}) if last_run else {}
            metrics_data["elapsed_time"] = last_metrics.get("elapsed_time")
        metrics_data["unassigned_count"] = Allocation.objects.filter(period=period, topic__isnull=True).count()

    params = request.GET.copy()
    params.pop("page", None)
    params.pop("suggest_student_id", None)
    return render(
        request,
        "allocate/dashboard.html",
        {
            "periods": periods,
            "period": period,
            "allocations": allocations,
            "page_obj": Paginator(allocations, _per_page(request)).get_page(request.GET.get("page")),
            "status": _status_filter(request),
            "rank": request.GET.get("rank") or "",
            "sort": request.GET.get("sort") or "code",
            "per_page": _per_page(request),
            "per_page_choices": PER_PAGE_CHOICES,
            "total_count": Allocation.objects.filter(period=period).count() if period else 0,
            "q": (request.GET.get("q") or "").strip(),
            "querystring": params.urlencode(),
            "lecturers": Lecturer.objects.select_related("user").order_by("user__last_name", "user__first_name"),
            "fields": Field.objects.order_by("name"),
            "lecturer_id": request.GET.get("lecturer") or "",
            "field_id": request.GET.get("field") or "",
            "metrics": metrics_data,
            "unassigned_only": _status_filter(request) == "unassigned",
            "suggest_student": suggest_student,
            "suggestions": suggestions,
            "open_topics": open_topics,
        },
    )


@login_required
def allocation_student_detail(request, period_id, student_id):
    """Mảnh HTML cho ngăn kéo "Chi tiết sinh viên" ở trang phân công — chỉ tải khi Khoa mở, không nhúng sẵn 100 SV.

    Gồm: kết quả hiện tại, NV1–NV3 gốc (điểm phù hợp + điều kiện bắt buộc từng NV), đề tài còn chỗ cho xếp tay pha 2.
    """
    _check_faculty_admin(request.user)
    from recommend.engine import Profile, eligibility_reasons
    from recommend.models import Recommendation

    period = get_object_or_404(RegistrationPeriod, pk=period_id)
    student = get_object_or_404(Student.objects.select_related("user", "major"), pk=student_id)
    ensure_recommendations(student)
    alloc = Allocation.objects.filter(period=period, student=student).select_related("topic__lecturer__user").first()
    scores = {r.topic_id: r for r in Recommendation.objects.filter(student=student)}
    profile = Profile(student)
    prefs = [
        {"pref": p, "rec": scores.get(p.topic_id), "eligibility": eligibility_reasons(profile, p.topic)}
        for p in Preference.objects.filter(student=student, period=period)
        .select_related("topic__lecturer__user")
        .prefetch_related("topic__skills__skill", "topic__prerequisites__course")
        .order_by("rank")
    ]
    can_edit = period.status != RegistrationPeriod.Status.PUBLISHED
    return render(
        request,
        "allocate/_student_drawer.html",
        {
            "period": period,
            "student": student,
            "allocation": alloc,
            "prefs": prefs,
            "can_edit": can_edit,
            "suggestions": get_phase2_suggestions(period, student) if can_edit else [],
        },
    )


def _check_student(user):
    """Kiểm tra quyền truy cập: chỉ tài khoản sinh viên có hồ sơ mới được phép."""
    if not (getattr(user, "is_student", False) and hasattr(user, "student")):
        raise PermissionDenied("Chỉ sinh viên mới có quyền truy cập trang này.")
    return user.student


@login_required
def student_allocation_result(request):
    """Màn hình xem kết quả phân công đồ án tốt nghiệp dành cho sinh viên (UC08).

    Công thức điểm tổng hợp:
        S(s, t) = sum(w_k * M_k) theo chuẩn AHP (kỹ năng, học lực, lĩnh vực, ngữ nghĩa, AI).
    Khi đợt PUBLISHED: hiển thị đề tài được phân, GVHD, NV đạt, điểm phù hợp.
    Khi chưa công bố: hiển thị trạng thái chờ 'Hội đồng Khoa đang thẩm định phân công'.
    """
    student = _check_student(request.user)
    period_id = request.GET.get("period_id")
    result_data = get_student_allocation_result(student, period_id=period_id)
    return render(
        request,
        "allocate/student_result.html",
        {
            "student": student,
            **result_data,
        },
    )
