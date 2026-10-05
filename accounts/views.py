"""Trang chủ chia theo vai trò: sinh viên, giảng viên, Khoa thấy nội dung khác nhau."""

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect, render

from allocate.services import get_student_allocation_result
from catalog.models import Preference, RegistrationPeriod, Student, Topic


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
        return render(request, "pages/home_lecturer.html", {"topics": user.lecturer.topics.all()})
    if not hasattr(user, "student"):
        return render(request, "pages/missing_profile.html")
    student = user.student
    allocation_result = get_student_allocation_result(student)
    return render(
        request,
        "pages/home_student.html",
        {
            "student": student,
            "preferences": Preference.objects.filter(student=student).select_related("topic").order_by("rank"),
            "recommendations": student.recommendations.filter(rank__isnull=False)
            .select_related("topic")
            .order_by("rank")[:5],
            "allocation_result": allocation_result,
        },
    )


def root(request):
    return redirect("home")
