"""Trang chủ chia theo vai trò: sinh viên, giảng viên, Khoa thấy nội dung khác nhau."""

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import redirect, render

from allocate.services import get_student_allocation_result
from catalog.models import Preference, RegistrationPeriod, Student, Topic
from recommend.services import ensure_recommendations


def _get_lecturer_dashboard_context(lecturer) -> dict:
    """Tính toán số liệu thống kê cho trang chủ giảng viên.

    Công thức toán học:
    1. Số đề tài do giảng viên phụ trách:
       N_topics = |{t in Topic | t.lecturer = lecturer}|
    2. Tổng sinh viên đăng ký vào các đề tài của giảng viên:
       N_students = |{s in Student | ton_tai p in Preference: p.student = s va p.topic.lecturer = lecturer}|
    3. Số nguyện vọng đang chờ duyệt:
       N_pending = |{p in Preference | p.topic.lecturer = lecturer va p.status = 'PENDING'}|
    4. Số nguyện vọng đã đồng ý:
       N_accepted = |{p in Preference | p.topic.lecturer = lecturer va p.status = 'ACCEPTED'}|
    5. Số lượng nguyện vọng chờ duyệt của từng đề tài:
       pending_count(t) = |{p in Preference | p.topic = t va p.status = 'PENDING'}|
    """
    topics = (
        lecturer.topics.prefetch_related("fields")
        .annotate(
            pending_count=Count(
                "preference",
                filter=Q(preference__status=Preference.Status.PENDING),
            )
        )
        .order_by("title")
    )
    n_topics = topics.count()

    prefs = Preference.objects.filter(topic__lecturer=lecturer)
    n_students = prefs.values("student").distinct().count()
    n_pending = prefs.filter(status=Preference.Status.PENDING).count()
    n_accepted = prefs.filter(status=Preference.Status.ACCEPTED).count()

    return {
        "topics": topics,
        "n_topics": n_topics,
        "n_students": n_students,
        "n_pending": n_pending,
        "n_accepted": n_accepted,
    }


def student_journey(student, has_preferences, period):
    """Hành trình 4 mục của SV (hồ sơ → gợi ý AI → nguyện vọng → kết quả), tách khỏi trạng thái của đợt.

    Mỗi mục có `state` (done / current / todo / missed) và `note` — backend quyết định theo dữ liệu thật,
    template chỉ hiển thị. Ví dụ đợt đã đóng mà SV chưa nộp nguyện vọng → "Chưa nộp trong đợt này" (missed).
    """
    status = period.status if period else None
    is_open = status == RegistrationPeriod.Status.OPEN
    is_published = status == RegistrationPeriod.Status.PUBLISHED
    has_profile = student.skills.exists()
    has_recs = student.recommendations.filter(rank__isnull=False).exists()

    if has_preferences:
        pref = ("done", "Đã nộp · có thể sửa" if is_open else "Đã nộp · chỉ xem")
    elif is_open:
        pref = ("todo", "Chưa nộp · đợt đang mở")
    else:
        pref = ("missed" if period else "todo", "Chưa nộp trong đợt này" if period else "Chưa có đợt đăng ký")
    if is_published:
        result = ("done", "Đã công bố · xem kết quả")
    else:
        result = ("todo", "Khoa đang xử lý" if period and not is_open else "Chưa có kết quả")
    items = [
        (
            "Hồ sơ năng lực",
            "student_profile",
            "done" if has_profile else "todo",
            "Hoàn thành" if has_profile else "Chưa khai kỹ năng",
        ),
        (
            "Gợi ý AI",
            "topic_list",
            "done" if has_recs else "todo",
            "Đã tạo danh sách phù hợp" if has_recs else "Chưa có gợi ý",
        ),
        ("Nguyện vọng", "student_preferences", *pref),
        ("Kết quả phân công", "student_allocation_result", *result),
    ]
    first_todo = next((i for i, it in enumerate(items) if it[2] == "todo"), None)
    return [
        {
            "number": i + 1,
            "label": label,
            "url_name": url_name,
            "state": "current" if i == first_todo else state,
            "note": note,
        }
        for i, (label, url_name, state, note) in enumerate(items)
    ]


@login_required
def home(request):
    """Trang chủ chia theo vai trò người dùng (Khoa, Giảng viên, Sinh viên).

    Với sinh viên (UC08):
    - Tra cứu kết quả phân công đồ án từ đợt đăng ký qua get_student_allocation_result.
    - Hiển thị kết quả chính thức (đề tài, GVHD, NV đạt, điểm phù hợp) khi đợt PUBLISHED.
    - Hiển thị trạng thái chờ 'Hội đồng Khoa đang thẩm định phân công' khi chưa công bố.
    """
    user = request.user
    if user.is_faculty_admin:
        return render(
            request,
            "pages/home_admin.html",
            {
                "n_topics": Topic.objects.count(),
                "n_students": Student.objects.count(),
                "n_periods": RegistrationPeriod.objects.count(),
                "periods": RegistrationPeriod.objects.annotate(
                    student_count=Count("preference__student", distinct=True)
                ).order_by("-start_at")[:5],
            },
        )
    if user.is_lecturer:
        if not hasattr(user, "lecturer"):
            return render(request, "pages/missing_profile.html")
        context = _get_lecturer_dashboard_context(user.lecturer)
        return render(request, "pages/home_lecturer.html", context)
    if not hasattr(user, "student"):
        return render(request, "pages/missing_profile.html")
    student = user.student
    ensure_recommendations(student)
    allocation_result = get_student_allocation_result(student)
    preferences = Preference.objects.filter(student=student).select_related("topic__lecturer__user").order_by("rank")
    return render(
        request,
        "pages/home_student.html",
        {
            "student": student,
            "preferences": preferences,
            "journey": student_journey(student, bool(preferences), allocation_result["period"]),
            "recommendations": student.recommendations.filter(rank__isnull=False)
            .select_related("topic")
            .order_by("rank")[:5],
            "allocation_result": allocation_result,
        },
    )


def root(request):
    return redirect("home")
