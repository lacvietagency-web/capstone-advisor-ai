"""Dịch vụ nghiệp vụ và logic truy vấn cho đề tài tốt nghiệp (catalog).

Bao gồm các hàm:
- Lấy danh sách đề tài mở công khai.
- Lọc đề tài theo lĩnh vực, giảng viên, độ khó, từ khóa tên.
- Phân trang kết quả tìm kiếm đề tài.
- Đếm số lượt đăng ký nguyện vọng 1 (NV1).
- Lấy điểm phù hợp (AI recommendation) của sinh viên với đề tài.
- Kiểm tra quyền truy cập đề tài (đề tài nháp DRAFT chỉ tác giả được xem).
"""

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Q

from catalog.models import Preference, Topic
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
    return queryset.annotate(nv1_count=Count("preference", filter=Q(preference__rank=1), distinct=True))


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
    qs = Preference.objects.filter(topic=topic, rank=1)
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
