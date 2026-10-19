"""Views phục vụ báo cáo thống kê dành cho Khoa (UC17, UC21).

Bao gồm:
- faculty_statistics: Xem tổng hợp số liệu đăng ký, phân bố đề tài/lĩnh vực, tải GV và so sánh thuật toán.
"""

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Max
from django.shortcuts import get_object_or_404, render

from allocate.models import Allocation
from catalog.models import AuditLog, Preference, RegistrationPeriod
from catalog.services import int_param

from .services import (
    compare_algorithms,
    get_field_distribution,
    get_lecturer_load,
    get_registration_stats,
    get_topic_nv1_distribution,
)


def _check_faculty_admin(user):
    """Kiểm tra quyền truy cập: chỉ tài khoản Khoa hoặc Superuser mới được xem báo cáo."""
    if not (getattr(user, "is_faculty_admin", False) or getattr(user, "is_superuser", False)):
        raise PermissionDenied("Chỉ tài khoản Khoa mới có quyền truy cập trang thống kê này.")


def _get_selected_period(request):
    """Lấy đợt đăng ký theo tham số GET hoặc mặc định đợt đang mở / mới nhất."""
    period_id = int_param(request.GET.get("period_id"))
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


def _prepare_chart_data(reg_stats, topic_nv1_list, field_list, comparison, lecturer_load):
    """Đóng gói dữ liệu biểu đồ dưới dạng dict cấu trúc để render qua Chart.js."""
    top_topics = topic_nv1_list[:8]
    active_fields = [f for f in field_list if f["count"] > 0][:8] or field_list[:6]
    top_lecs = lecturer_load[:10]

    return {
        "registration": {
            "labels": ["Đã đăng ký", "Chưa đăng ký"],
            "data": [reg_stats["registered_students"], reg_stats["unregistered_students"]],
        },
        "topics": {
            "labels": [t["title"][:22] + "..." if len(t["title"]) > 22 else t["title"] for t in top_topics],
            "full_titles": [t["title"] for t in top_topics],
            "counts": [t["nv1_count"] for t in top_topics],
            "capacities": [t["capacity"] for t in top_topics],
        },
        "fields": {
            "labels": [f["field_name"] for f in active_fields],
            "counts": [f["count"] for f in active_fields],
            "percentages": [f["percentage"] for f in active_fields],
        },
        "comparison": {
            "categories": ["Đạt NV1 (%)", "Đạt Top 3 (%)", "Được xếp (%)"],
            "ilp": [
                comparison["ilp"]["nv1_pct"],
                comparison["ilp"]["top3_pct"],
                comparison["ilp"]["assigned_pct"],
            ],
            "greedy": [
                comparison["greedy"]["nv1_pct"],
                comparison["greedy"]["top3_pct"],
                comparison["greedy"]["assigned_pct"],
            ],
            "unassigned_count": {
                "ilp": comparison["ilp"]["unassigned_count"],
                "greedy": comparison["greedy"]["unassigned_count"],
            },
            "unassigned_rate": {
                "ilp": comparison["ilp"]["unassigned_rate"],
                "greedy": comparison["greedy"]["unassigned_rate"],
            },
        },
        "lecturers": {
            "labels": [l["name"] for l in top_lecs],
            "assigned": [l["assigned_count"] for l in top_lecs],
            "capacity": [l["capacity"] for l in top_lecs],
            "load_rate": [l["load_rate"] for l in top_lecs],
        },
    }


def _cached_comparison(period):
    """compare_algorithms chạy cả ILP lẫn Greedy (~2 s ở 1.000 SV) — trước đây chạy lại mỗi lần mở trang, nhiều người
    cùng mở là dồn hàng (đo tải 20/10: trung bình 26 s). Lưu tạm theo dấu dữ liệu: mọi thao tác làm đổi kết quả
    (nộp/duyệt NV, sửa đề tài, phân công) đều ghi AuditLog hoặc đổi số NV, nên khoá tự đổi khi dữ liệu đổi."""
    if period is None:
        return compare_algorithms(period)
    prefs = Preference.objects.filter(period=period).aggregate(n=Count("id"), m=Max("id"))
    key = f"cmp:{period.pk}:{AuditLog.objects.aggregate(m=Max('id'))['m']}:{prefs['n']}:{prefs['m']}"
    return cache.get_or_set(key, lambda: compare_algorithms(period), 600)


@login_required
def faculty_statistics(request):
    """Màn hình báo cáo thống kê dành riêng cho Giáo vụ Khoa (UC17, UC21)."""
    _check_faculty_admin(request.user)

    periods = list(RegistrationPeriod.objects.order_by("-start_at"))
    period = _get_selected_period(request)

    reg_stats = get_registration_stats(period)
    topic_nv1_list = get_topic_nv1_distribution(period, limit=10)
    field_list = get_field_distribution(period)
    comparison = _cached_comparison(period)

    has_saved_allocations = (
        period is not None and Allocation.objects.filter(period=period, topic__isnull=False).exists()
    )
    if has_saved_allocations:
        lecturer_load = get_lecturer_load(period, assign=None)
        load_source = "Thực tế (từ kết quả phân công đã lưu)"
    else:
        lecturer_load = get_lecturer_load(period, assign=comparison["assign_ilp"])
        load_source = "Mô phỏng (thuật toán ILP)"

    chart_data = _prepare_chart_data(reg_stats, topic_nv1_list, field_list, comparison, lecturer_load)

    context = {
        "periods": periods,
        "period": period,
        "reg_stats": reg_stats,
        "topic_nv1_list": topic_nv1_list,
        "field_list": field_list,
        "lecturer_load": lecturer_load,
        "load_source": load_source,
        "comparison": comparison,
        "chart_data": chart_data,
    }
    return render(request, "reports/statistics.html", context)
