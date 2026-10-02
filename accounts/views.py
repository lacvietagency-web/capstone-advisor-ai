"""Trang chủ chia theo vai trò: sinh viên, giảng viên, Khoa thấy nội dung khác nhau."""
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect, render

from catalog.models import Preference, RegistrationPeriod, Student, Topic


@login_required
def home(request):
    user = request.user
    if user.is_faculty_admin:
        return render(request, "pages/home_admin.html", {
            "n_topics": Topic.objects.count(),
            "n_students": Student.objects.count(),
            "n_periods": RegistrationPeriod.objects.count(),
            "periods": RegistrationPeriod.objects.annotate(student_count=Count("preference__student", distinct=True))
                                                 .order_by("-start_at")[:5],
        })
    if user.is_lecturer:
        if not hasattr(user, "lecturer"):
            return render(request, "pages/missing_profile.html")
        return render(request, "pages/home_lecturer.html", {"topics": user.lecturer.topics.all()})
    if not hasattr(user, "student"):
        return render(request, "pages/missing_profile.html")
    student = user.student
    return render(request, "pages/home_student.html", {
        "student": student,
        "preferences": Preference.objects.filter(student=student).select_related("topic").order_by("rank"),
        "recommendations": student.recommendations.select_related("topic").order_by("rank")[:5],
    })


def root(request):
    return redirect("home")
