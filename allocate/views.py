"""Màn hình phân công đồ án dành cho Khoa: chạy thuật toán, bảng nháp, chỉnh tay Pha 2, chốt và công bố."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import RegistrationPeriod, Student, Topic

from .models import Allocation
from .services import (
    calculate_period_metrics,
    get_phase2_suggestions,
    manual_assign,
    publish_allocations,
    run_allocation,
)


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
    """Xử lý chốt danh sách phân công và công bố đợt."""
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


def _get_allocations_and_suggestions(period, request):
    """Lấy danh sách phân công nháp và danh sách gợi ý Pha 2 nếu có yêu cầu."""
    if not period:
        return [], None, None, []

    unassigned_only = request.GET.get("unassigned_only") == "1"
    alloc_qs = (
        Allocation.objects.filter(period=period)
        .select_related("student__user", "topic__lecturer__user")
        .order_by("student__student_code")
    )
    if unassigned_only:
        alloc_qs = alloc_qs.filter(topic__isnull=True)
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

    return render(
        request,
        "allocate/dashboard.html",
        {
            "periods": periods,
            "period": period,
            "allocations": allocations,
            "metrics": metrics_data,
            "unassigned_only": request.GET.get("unassigned_only") == "1",
            "suggest_student": suggest_student,
            "suggestions": suggestions,
            "open_topics": open_topics,
        },
    )
