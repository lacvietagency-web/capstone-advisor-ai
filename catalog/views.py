"""Màn hình nghiệp vụ cho Sinh viên và Giảng viên."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from recommend.models import Recommendation
from recommend.services import refresh_student

from .forms import (
    PreferenceForm,
    StudentAboutForm,
    StudentInterestFormSet,
    StudentSkillFormSet,
    TopicForm,
    TopicSkillFormSet,
)
from .models import AuditLog, Field, Lecturer, Preference, RegistrationPeriod, Student, Topic
from .services import (
    annotate_topics_nv1,
    check_topic_view_permission,
    filter_topics,
    get_student_match_score,
    get_student_recommendations_map,
    get_topic_nv1_count,
    get_visible_topics,
    paginate_topics,
)


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
            about.save()
            skills.save()
            interests.save()
            Student.objects.filter(pk=st.pk).update(
                profile_version=F("profile_version") + 1
            )  # điểm AI sẽ được tính lại
            Recommendation.objects.filter(student=st).delete()
            AuditLog.objects.create(user=request.user, action="update_profile", entity="Student", entity_id=st.pk)
        refresh_student(Student.objects.get(pk=st.pk))
        messages.success(request, "Đã lưu hồ sơ và tính lại đề tài gợi ý cho bạn.")
        return redirect("student_profile")
    return render(
        request,
        "catalog/student_profile.html",
        {"student": st, "about_form": about, "skill_formset": skills, "interest_formset": interests},
    )


@login_required
def student_preferences(request):
    st = _student(request)
    period = _open_period()
    if period is None:
        return render(request, "catalog/student_preferences.html", {"period": None})
    current = {p.rank: p.topic for p in Preference.objects.filter(student=st, period=period)}
    initial = {f"nv{r}": t for r, t in current.items()}
    preset_topic_id = request.GET.get("topic") or request.GET.get("topic_id")
    if preset_topic_id and request.method == "GET":
        try:
            preset_topic = Topic.objects.get(pk=preset_topic_id, status=Topic.Status.OPEN)
            if preset_topic not in initial.values():
                for slot in ("nv1", "nv2", "nv3"):
                    if slot not in initial or not initial[slot]:
                        initial[slot] = preset_topic
                        break
        except (Topic.DoesNotExist, ValueError):
            pass
    form = PreferenceForm(request.POST or None, initial=initial)
    scores = {r.topic_id: r for r in Recommendation.objects.filter(student=st)}
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            Preference.objects.filter(student=st, period=period).delete()
            for rank in (1, 2, 3):
                topic = form.cleaned_data.get(f"nv{rank}")
                if topic:
                    Preference.objects.create(student=st, period=period, topic=topic, rank=rank)
            AuditLog.objects.create(
                user=request.user,
                action="set_preferences",
                entity="Preference",
                entity_id=st.pk,
                detail={
                    f"nv{r}": (form.cleaned_data.get(f"nv{r}").pk if form.cleaned_data.get(f"nv{r}") else None)
                    for r in (1, 2, 3)
                },
            )
        messages.success(request, "Đã lưu nguyện vọng.")
        return redirect("student_preferences")
    top5 = Recommendation.objects.filter(student=st).select_related("topic").order_by("rank")[:5]
    return render(
        request, "catalog/student_preferences.html", {"period": period, "form": form, "top5": top5, "scores": scores}
    )


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
            t = form.save(commit=False)
            t.lecturer = lec
            if t.pk:
                t.version += 1  # vector ngữ nghĩa và điểm AI của đề tài sẽ được tính lại
            t.save()
            form.save_m2m()
            skills.instance = t
            skills.save()
            AuditLog.objects.create(user=request.user, action="save_topic", entity="Topic", entity_id=t.pk)
        messages.success(request, "Đã lưu đề tài.")
        return redirect("lecturer_topics")
    return render(request, "catalog/lecturer_topic_form.html", {"form": form, "skill_formset": skills, "topic": topic})


@login_required
def lecturer_registrations(request, pk):
    """Sinh viên đã đăng ký một đề tài, kèm nguyện vọng và mức phù hợp AI tính."""
    lec = _lecturer(request)
    topic = get_object_or_404(Topic, pk=pk, lecturer=lec)
    prefs = (
        Preference.objects.filter(topic=topic).select_related("student__user", "period").order_by("rank", "created_at")
    )
    scores = {r.student_id: r for r in Recommendation.objects.filter(topic=topic)}
    rows = [{"pref": p, "rec": scores.get(p.student_id)} for p in prefs]
    return render(request, "catalog/lecturer_registrations.html", {"topic": topic, "rows": rows})


# ---------------------------------------------------------------- tra cứu đề tài
def topic_list(request):
    """Xem danh sách đề tài tốt nghiệp có bộ lọc (lĩnh vực, giảng viên, độ khó, tìm kiếm tên) và phân trang."""
    field_id = request.GET.get("field") or request.GET.get("field_id") or request.GET.get("linh_vuc")
    lecturer_id = request.GET.get("lecturer") or request.GET.get("lecturer_id") or request.GET.get("gv")
    difficulty = request.GET.get("difficulty") or request.GET.get("do_kho")
    query = (
        request.GET.get("q")
        or request.GET.get("search")
        or request.GET.get("keyword")
        or request.GET.get("name")
        or request.GET.get("ten")
        or request.GET.get("title")
    )
    page_num = request.GET.get("page") or request.GET.get("p") or 1
    per_page = request.GET.get("per_page") or 10

    visible_qs = get_visible_topics()
    filtered_qs = filter_topics(
        visible_qs, field_id=field_id, lecturer_id=lecturer_id, difficulty=difficulty, query=query
    )
    annotated_qs = annotate_topics_nv1(filtered_qs)
    page_obj = paginate_topics(annotated_qs, page_number=page_num, per_page=per_page)

    student = None
    scores_map = {}
    is_student_user = (
        request.user.is_authenticated
        and getattr(request.user, "is_student", False)
        and hasattr(request.user, "student")
    )
    if is_student_user:
        student = request.user.student
        scores_map = get_student_recommendations_map(student)

    for topic in page_obj:
        topic.recommendation = scores_map.get(topic.id)
        topic.match_score = topic.recommendation.final_score if topic.recommendation else None

    get_params = request.GET.copy()
    get_params.pop("page", None)
    get_params.pop("p", None)
    querystring = get_params.urlencode()

    context = {
        "page_obj": page_obj,
        "topics": page_obj,
        "fields": Field.objects.all().order_by("name"),
        "lecturers": Lecturer.objects.select_related("user").all().order_by("user__last_name", "user__first_name"),
        "difficulties": Topic.Difficulty.choices,
        "selected_field": str(field_id) if field_id else "",
        "selected_lecturer": str(lecturer_id) if lecturer_id else "",
        "selected_difficulty": str(difficulty) if difficulty else "",
        "search_query": query.strip() if query else "",
        "querystring": querystring,
        "is_student": student is not None,
        "student": student,
    }
    return render(request, "catalog/topic_list.html", context)


def topic_detail(request, pk=None, id=None):
    """Xem chi tiết một đề tài: mô tả, kỹ năng, môn tiên quyết, sức chứa, số người đăng ký NV1."""
    topic_id = pk or id
    topic = get_object_or_404(
        Topic.objects.select_related("lecturer__user").prefetch_related("fields"),
        pk=topic_id,
    )
    if not check_topic_view_permission(request.user, topic):
        raise Http404("Đề tài không tồn tại hoặc chưa được mở.")

    nv1_count = get_topic_nv1_count(topic)
    is_student = (
        request.user.is_authenticated
        and getattr(request.user, "is_student", False)
        and hasattr(request.user, "student")
    )
    student = request.user.student if is_student else None
    recommendation = get_student_match_score(student, topic)

    context = {
        "topic": topic,
        "nv1_count": nv1_count,
        "is_student": is_student,
        "student": student,
        "recommendation": recommendation,
        "skills": topic.skills.select_related("skill").all(),
        "prerequisites": topic.prerequisites.select_related("course").all(),
    }
    return render(request, "catalog/topic_detail.html", context)
