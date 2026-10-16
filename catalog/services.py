"""Dịch vụ nghiệp vụ và logic truy vấn cho đề tài tốt nghiệp (catalog).

Bao gồm các hàm:
- Lấy danh sách đề tài mở công khai.
- Lọc đề tài theo lĩnh vực, giảng viên, độ khó, từ khóa tên.
- Phân trang kết quả tìm kiếm đề tài.
- Đếm số lượt đăng ký nguyện vọng 1 (NV1).
- Lấy điểm phù hợp (AI recommendation) của sinh viên với đề tài.
- Kiểm tra quyền truy cập đề tài (đề tài nháp DRAFT chỉ tác giả được xem).
- Hồ sơ giảng viên: khoá chỉ tiêu, phân quyền, lưu kèm nhật ký [UC09].
"""

from django.core.exceptions import PermissionDenied
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404

from catalog.models import AuditLog, Lecturer, Preference, RegistrationPeriod, Topic
from recommend.models import Recommendation


def get_visible_topics():
    """Lấy danh sách đề tài đang mở (OPEN) phục vụ tra cứu.

    Công thức tập hợp:
        T_open = { t in Topic | t.status = Topic.Status.OPEN }
    """
    return (
        Topic.objects.filter(status=Topic.Status.OPEN)
        .select_related("lecturer__user")
        .prefetch_related("fields", "skills__skill", "prerequisites__course")
        .order_by("title", "id")
    )


def filter_by_field(queryset, field_id):
    """Lọc danh sách đề tài theo lĩnh vực chuyên môn.

    Công thức toán học:
        T_field = { t in queryset | field_id in t.fields }
    """
    if field_id:
        return queryset.filter(fields__id=field_id)
    return queryset


def filter_by_lecturer(queryset, lecturer_id):
    """Lọc danh sách đề tài theo giảng viên hướng dẫn.

    Công thức toán học:
        T_lecturer = { t in queryset | t.lecturer_id = lecturer_id }
    """
    if lecturer_id:
        return queryset.filter(lecturer_id=lecturer_id)
    return queryset


def filter_by_difficulty(queryset, difficulty):
    """Lọc danh sách đề tài theo độ khó (1: Dễ, 2: Trung bình, 3: Khó).

    Công thức toán học:
        T_diff = { t in queryset | t.difficulty = difficulty }
    """
    if difficulty:
        return queryset.filter(difficulty=difficulty)
    return queryset


def filter_by_search(queryset, query):
    """Tìm kiếm đề tài theo tên đề tài (không phân biệt hoa thường).

    Công thức toán học:
        T_search = { t in queryset | lower(query) in lower(t.title) }
    """
    if query and query.strip():
        return queryset.filter(title__icontains=query.strip())
    return queryset


def filter_topics(queryset, *, field_id=None, lecturer_id=None, difficulty=None, query=None):
    """Lọc danh sách đề tài theo các tiêu chí kết hợp.

    Công thức giao tập hợp:
        T_filtered = T_field ∩ T_lecturer ∩ T_diff ∩ T_search
    """
    queryset = filter_by_field(queryset, field_id)
    queryset = filter_by_lecturer(queryset, lecturer_id)
    queryset = filter_by_difficulty(queryset, difficulty)
    queryset = filter_by_search(queryset, query)
    return queryset.distinct().order_by("title", "id")


def annotate_topics_nv1(queryset):
    """Gán số lượng đăng ký NV1 cho mỗi đề tài trong danh sách.

    Công thức toán học:
        t.nv1_count = Count(p in Preference | p.topic = t and p.rank = 1)
    """
    return queryset.annotate(
        nv1_count=Count("preference", filter=Q(preference__rank=1, preference__submitted=True), distinct=True)
    )


def paginate_topics(queryset, page_number=1, per_page=10):
    """Phân trang danh sách đề tài.

    Công thức toán học:
        offset = (page - 1) * per_page
        limit = per_page
        items = queryset[offset : offset + limit]
        total_pages = ceil(total_items / per_page)
    """
    paginator = Paginator(queryset, per_page)
    try:
        return paginator.page(page_number)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def get_topic_nv1_count(topic, period=None):
    """Đếm số lượng sinh viên đã đăng ký đề tài ở nguyện vọng 1 (NV1).

    Công thức toán học:
        nv1_count(t) = |{ p in Preference | p.topic = t and p.rank = 1 (and p.period = period) }|
    """
    qs = Preference.objects.filter(topic=topic, rank=1, submitted=True)
    if period is not None:
        qs = qs.filter(period=period)
    return qs.count()


def get_student_match_score(student, topic):
    """Lấy bản ghi gợi ý và điểm phù hợp của sinh viên với một đề tài nếu có.

    Công thức toán học:
        match_score(s, t) = Recommendation(student=s, topic=t).final_score
        Thang điểm: [0, 100]
    """
    if not student:
        return None
    return Recommendation.objects.filter(student=student, topic=topic).first()


def get_student_recommendations_map(student):
    """Lấy từ điển điểm phù hợp của sinh viên cho toàn bộ đề tài.

    Công thức toán học:
        scores_map = { rec.topic_id: rec for rec in Recommendation where student = student }
    """
    if not student:
        return {}
    return {r.topic_id: r for r in Recommendation.objects.filter(student=student)}


def check_topic_view_permission(user, topic):
    """Kiểm tra quyền truy cập xem chi tiết đề tài.

    Đề tài công khai (OPEN, CLOSED) cho phép mọi người xem.
    Đề tài nháp (DRAFT) chỉ cho phép chính giảng viên tạo đề tài hoặc quản trị viên Khoa xem.

    Công thức logic:
        allow_view(u, t) = (t.status != DRAFT) or
                           (u.is_authenticated and (
                               (u.is_lecturer and t.lecturer.user_id = u.id) or
                               u.is_faculty_admin or
                               u.is_superuser
                           ))
    """
    if topic.status != Topic.Status.DRAFT:
        return True
    if not user or not user.is_authenticated:
        return False
    if getattr(user, "is_faculty_admin", False) or user.is_superuser:
        return True
    if getattr(user, "is_lecturer", False) and hasattr(user, "lecturer"):
        return topic.lecturer_id == user.lecturer.id
    return False


def is_quota_locked(period=None, lecturer=None) -> bool:
    """Kiểm tra chỉ tiêu hướng dẫn của giảng viên có bị khoá hay không [UC09].

    Công thức logic:
        locked = is_closed(period) or getattr(lecturer, 'is_quota_locked', False)
    trong đó:
        is_closed(p) = (p.status in {CLOSED, OPTIMIZED, PUBLISHED})

    Quy tắc nghiệp vụ:
        - Nếu lecturer hoặc period có cờ `is_quota_locked` gán thủ công -> True.
        - Nếu truyền period cụ thể: khoá khi trạng thái thuộc nhóm đã đóng (status != OPEN).
        - Nếu không truyền period:
            + Tồn tại đợt đang mở (OPEN) -> False (chưa khoá, GV được sửa).
            + Không có đợt nào OPEN và đợt mới nhất đã đóng -> True (đã khoá).
            + Không có đợt đăng ký nào trong hệ thống -> False.
    """
    if lecturer and getattr(lecturer, "is_quota_locked", False):
        return True
    if period and getattr(period, "is_quota_locked", False):
        return True

    closed_statuses = (
        RegistrationPeriod.Status.CLOSED,
        RegistrationPeriod.Status.OPTIMIZED,
        RegistrationPeriod.Status.PUBLISHED,
        "CLOSED",
        "OPTIMIZED",
        "PUBLISHED",
    )

    if period is not None:
        return period.status in closed_statuses

    if RegistrationPeriod.objects.filter(status=RegistrationPeriod.Status.OPEN).exists():
        return False

    latest = RegistrationPeriod.objects.order_by("-start_at", "-id").first()
    return bool(latest and latest.status in closed_statuses)


def get_target_lecturer(user, pk=None, lecturer_id_param=None):
    """Xác định đối tượng giảng viên cần xem hoặc chỉnh sửa hồ sơ theo vai trò người dùng [UC09].

    Quy tắc phân quyền:
        - Sinh viên (is_student): Bị từ chối truy cập (PermissionDenied -> HTTP 403).
        - Giảng viên (is_lecturer): Chỉ được truy cập hồ sơ của chính mình (pk trùng với user.lecturer.pk).
        - Cán bộ Khoa (is_faculty_admin): Được phép xem và sửa hồ sơ của bất kỳ giảng viên nào.
    """
    if getattr(user, "is_faculty_admin", False):
        target_id = pk or int_param(lecturer_id_param)  # ?lecturer_id=abc → bỏ qua, không lỗi 500
        if target_id:
            return get_object_or_404(Lecturer, pk=target_id)
        if hasattr(user, "lecturer"):
            return user.lecturer
        first_lec = Lecturer.objects.order_by("pk").first()
        if first_lec:
            return first_lec
        raise PermissionDenied("Chưa có giảng viên nào trong hệ thống.")

    if getattr(user, "is_lecturer", False) and hasattr(user, "lecturer"):
        lec = user.lecturer
        if pk and pk != lec.pk:
            raise PermissionDenied("Giảng viên chỉ có quyền chỉnh sửa hồ sơ của chính mình.")
        return lec

    raise PermissionDenied("Bạn không có quyền truy cập trang này.")


def save_lecturer_profile(lecturer, form, user=None, is_locked=False, is_faculty_admin=False):
    """Lưu hồ sơ chuyên môn và chỉ tiêu của giảng viên kèm nhật ký kiểm toán [UC09].

    Công thức bảo vệ chỉ tiêu tối đa:
        final_max = (
            form.cleaned_data['max_students']
            if (not is_locked or is_faculty_admin)
            else lecturer.max_students
        )

    Thực hiện cập nhật trong giao dịch atomic và ghi AuditLog ghi nhận chi tiết:
    bộ môn, chỉ tiêu và danh sách các lĩnh vực chuyên môn được chọn.
    """
    with transaction.atomic():
        saved_lec = form.save()
        AuditLog.objects.create(
            user=user,
            action="update_lecturer_profile",
            entity="Lecturer",
            entity_id=str(saved_lec.pk),
            detail={
                "department": saved_lec.department,
                "max_students": saved_lec.max_students,
                "fields": list(saved_lec.fields.values_list("name", flat=True)),
            },
        )
    return saved_lec


def remaining_capacity(topic, period=None):
    """Chỗ còn của đề tài = sức chứa − số nguyện vọng đã được GV đồng ý (trong đợt nếu có). Không âm.
    "Đã đồng ý" = đang giữ chỗ dù SV vừa rút về nháp để sửa NV khác (không thì GV nhận thêm người,
    SV nộp lại → quá chỗ);
    chỉ khi SV bỏ hẳn đề tài khỏi nguyện vọng (bản ghi bị xoá) thì chỗ mới được nhả."""
    qs = Preference.objects.filter(topic=topic, status=Preference.Status.ACCEPTED)
    if period is not None:
        qs = qs.filter(period=period)
    return max(topic.capacity - qs.count(), 0)


def int_param(value, default=None, lo=None, hi=None):
    """Tham số số nguyên từ URL (?period_id=…): không phải số → default (tránh lỗi 500); kẹp [lo, hi] nếu có."""
    try:
        n = int(str(value).strip())
    except (TypeError, ValueError):
        return default
    if lo is not None:
        n = max(lo, n)
    if hi is not None:
        n = min(hi, n)
    return n
