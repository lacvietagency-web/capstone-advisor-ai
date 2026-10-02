"""Màn hình nghiệp vụ cho Sinh viên và Giảng viên."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

from recommend.models import Recommendation
from recommend.services import refresh_student

from .forms import PreferenceForm, StudentAboutForm, StudentInterestFormSet, StudentSkillFormSet, TopicForm, TopicSkillFormSet
from .models import AuditLog, Preference, RegistrationPeriod, Student, Topic


def _student(request):
    if not getattr(request.user, "is_student", False) or not hasattr(request.user, "student"):
        raise PermissionDenied
    return request.user.student


def _lecturer(request):
    if not getattr(request.user, "is_lecturer", False) or not hasattr(request.user, "lecturer"):
        raise PermissionDenied
    return request.user.lecturer


def _open_period():
    return RegistrationPeriod.objects.filter(status=RegistrationPeriod.Status.OPEN).order_by("-start_at").first()


# ---------------------------------------------------------------- sinh viên
@login_required
def student_profile(request):
    st = _student(request)
    about = StudentAboutForm(request.POST or None, instance=st)
    skills = StudentSkillFormSet(request.POST or None, instance=st, prefix="skills")
    interests = StudentInterestFormSet(request.POST or None, instance=st, prefix="interests")
    if request.method == "POST" and about.is_valid() and skills.is_valid() and interests.is_valid():
        with transaction.atomic():
            about.save(); skills.save(); interests.save()
            Student.objects.filter(pk=st.pk).update(profile_version=F("profile_version") + 1)   # điểm AI sẽ được tính lại
            Recommendation.objects.filter(student=st).delete()
            AuditLog.objects.create(user=request.user, action="update_profile", entity="Student", entity_id=st.pk)
        refresh_student(Student.objects.get(pk=st.pk))
        messages.success(request, "Đã lưu hồ sơ và tính lại đề tài gợi ý cho bạn.")
        return redirect("student_profile")
    return render(request, "catalog/student_profile.html", {"student": st, "about_form": about,
                                                            "skill_formset": skills, "interest_formset": interests})


@login_required
def student_preferences(request):
    st = _student(request)
    period = _open_period()
    if period is None:
        return render(request, "catalog/student_preferences.html", {"period": None})
    current = {p.rank: p.topic for p in Preference.objects.filter(student=st, period=period)}
    form = PreferenceForm(request.POST or None, initial={f"nv{r}": t for r, t in current.items()})
    scores = {r.topic_id: r for r in Recommendation.objects.filter(student=st)}
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            Preference.objects.filter(student=st, period=period).delete()
            for rank in (1, 2, 3):
                topic = form.cleaned_data.get(f"nv{rank}")
                if topic:
                    Preference.objects.create(student=st, period=period, topic=topic, rank=rank)
            AuditLog.objects.create(user=request.user, action="set_preferences", entity="Preference", entity_id=st.pk,
                                    detail={f"nv{r}": (form.cleaned_data.get(f"nv{r}").pk if form.cleaned_data.get(f"nv{r}") else None)
                                            for r in (1, 2, 3)})
        messages.success(request, "Đã lưu nguyện vọng.")
        return redirect("student_preferences")
    top5 = Recommendation.objects.filter(student=st).select_related("topic").order_by("rank")[:5]
    return render(request, "catalog/student_preferences.html", {"period": period, "form": form, "top5": top5, "scores": scores})


# ---------------------------------------------------------------- giảng viên
@login_required
def lecturer_topics(request):
    lec = _lecturer(request)
    topics = lec.topics.prefetch_related("fields").order_by("title")
    return render(request, "catalog/lecturer_topics.html", {"lecturer": lec, "topics": topics})


@login_required
def lecturer_topic_edit(request, pk=None):
    lec = _lecturer(request)
    topic = get_object_or_404(Topic, pk=pk, lecturer=lec) if pk else Topic(lecturer=lec)
    form = TopicForm(request.POST or None, instance=topic)
    skills = TopicSkillFormSet(request.POST or None, instance=topic, prefix="skills")
    if request.method == "POST" and form.is_valid() and skills.is_valid():
        with transaction.atomic():
            t = form.save(commit=False); t.lecturer = lec
            if t.pk:
                t.version += 1                       # vector ngữ nghĩa và điểm AI của đề tài sẽ được tính lại
            t.save(); form.save_m2m()
            skills.instance = t; skills.save()
            AuditLog.objects.create(user=request.user, action="save_topic", entity="Topic", entity_id=t.pk)
        messages.success(request, "Đã lưu đề tài.")
        return redirect("lecturer_topics")
    return render(request, "catalog/lecturer_topic_form.html", {"form": form, "skill_formset": skills, "topic": topic})


@login_required
def lecturer_registrations(request, pk):
    """Sinh viên đã đăng ký một đề tài, kèm nguyện vọng và mức phù hợp AI tính."""
    lec = _lecturer(request)
    topic = get_object_or_404(Topic, pk=pk, lecturer=lec)
    prefs = Preference.objects.filter(topic=topic).select_related("student__user", "period").order_by("rank", "created_at")
    scores = {r.student_id: r for r in Recommendation.objects.filter(topic=topic)}
    rows = [{"pref": p, "rec": scores.get(p.student_id)} for p in prefs]
    return render(request, "catalog/lecturer_registrations.html", {"topic": topic, "rows": rows})
