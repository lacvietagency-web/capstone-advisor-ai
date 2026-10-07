"""Màn hình nghiệp vụ cho Sinh viên và Giảng viên."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from recommend.models import Recommendation
from recommend.services import refresh_student, score_preferences

from .forms import (
    LecturerProfileForm,
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
    get_target_lecturer,
    get_topic_nv1_count,
    get_visible_topics,
    is_quota_locked,
    paginate_topics,
    save_lecturer_profile,
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
    form = PreferenceForm(request.POST or None, initial=initial, student=st)
    scores = {r.topic_id: r for r in Recommendation.objects.filter(student=st)}
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            old = Preference.objects.filter(student=st, period=period)
            kept_status = dict(old.values_list("topic_id", "status"))  # GV đã duyệt đề tài nào thì giữ nguyên kết quả
            old.delete()
            for rank in (1, 2, 3):
                topic = form.cleaned_data.get(f"nv{rank}")
                if topic:
                    Preference.objects.create(
                        student=st,
                        period=period,
                        topic=topic,
                        rank=rank,
                        status=kept_status.get(topic.pk, Preference.Status.PENDING),
                    )
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
        score_preferences(st)
        messages.success(request, "Đã lưu nguyện vọng.")
        return redirect("student_preferences")
    top5 = Recommendation.objects.filter(student=st, rank__isnull=False).select_related("topic").order_by("rank")[:5]
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


def _handle_preference_action(request, topic):
    """Cập nhật trạng thái duyệt nguyện vọng (Đồng ý / Từ chối) và ghi AuditLog.

    Quy tắc chuyển đổi trạng thái:
        status(p) = ACCEPTED  nếu action in {ACCEPT, ĐỒNG Ý}
        status(p) = REJECTED  nếu action in {REJECT, TỪ CHỐI}
    Ghi vết kiểm toán:
        AuditLog(user, action, entity='Preference', entity_id=p.id)
    """
    pref_id = request.POST.get("preference_id") or request.POST.get("pref_id")
    student_id = request.POST.get("student_id")
    if pref_id:
        pref = get_object_or_404(Preference, pk=pref_id, topic=topic)
    elif student_id:
        pref = get_object_or_404(Preference, student_id=student_id, topic=topic)
    else:
        messages.error(request, "Thiếu thông tin nguyện vọng.")
        return redirect("lecturer_registrations", pk=topic.pk)

    action_clean = (request.POST.get("action") or request.POST.get("status") or "").strip().upper().replace(" ", "_")
    reason = ""
    if action_clean in ("ACCEPT", "ACCEPTED", "DONG_Y", "APPROVE", "ĐỒNG_Ý"):
        new_status = Preference.Status.ACCEPTED
        log_action = "accept_registration"
    elif action_clean in ("REJECT", "REJECTED", "TU_CHOI", "TỪ_CHỐI"):
        new_status = Preference.Status.REJECTED
        log_action = "reject_registration"
        reason = (request.POST.get("reason") or "").strip()
        if len(reason) < 5:  # GV phải ghi lý do để SV biết và Khoa truy vết khi khiếu nại
            messages.error(request, "Vui lòng nhập lý do từ chối (ít nhất 5 ký tự).")
            return redirect("lecturer_registrations", pk=topic.pk)
    else:
        messages.error(request, "Thao tác không hợp lệ.")
        return redirect("lecturer_registrations", pk=topic.pk)

    with transaction.atomic():
        pref.status = new_status
        pref.reject_reason = reason if new_status == Preference.Status.REJECTED else ""
        pref.save(update_fields=["status", "reject_reason"])
        AuditLog.objects.create(
            user=request.user,
            action=log_action,
            entity="Preference",
            entity_id=str(pref.pk),
            detail={
                "status": new_status,
                "student_id": pref.student_id,
                "topic_id": topic.pk,
                "rank": pref.rank,
                "reason": pref.reject_reason,
            },
        )

    label = "đồng ý" if new_status == Preference.Status.ACCEPTED else "từ chối"
    messages.success(request, f"Đã {label} nguyện vọng của sinh viên {pref.student}.")
    return redirect("lecturer_registrations", pk=topic.pk)


@login_required
def lecturer_registrations(request, pk):
    """Màn hình danh sách sinh viên đăng ký đề tài của giảng viên [UC12].

    Quyền truy cập:
        Chỉ GV sở hữu đề tài (topic.lecturer == request.user.lecturer) được xem và duyệt.
        Người khác sẽ nhận PermissionDenied (HTTP 403).
    """
    lec = _lecturer(request)
    topic = get_object_or_404(Topic, pk=pk)
    if topic.lecturer != lec:
        raise PermissionDenied

    if request.method == "POST":
        return _handle_preference_action(request, topic)

    prefs = (
        Preference.objects.filter(topic=topic).select_related("student__user", "period").order_by("rank", "created_at")
    )
    scores = {r.student_id: r for r in Recommendation.objects.filter(topic=topic)}
    rows = [{"pref": p, "rec": scores.get(p.student_id)} for p in prefs]
    return render(request, "catalog/lecturer_registrations.html", {"topic": topic, "rows": rows})


@login_required
def lecturer_profile(request, pk=None):
    """Màn hình cập nhật chuyên môn và chỉ tiêu của giảng viên [UC09].

    Quy tắc nghiệp vụ:
        - Giảng viên chỉ sửa hồ sơ của chính mình; chỉ tiêu bị khoá nếu đợt đã đóng.
        - Cán bộ Khoa có thể sửa hồ sơ của bất kỳ GV nào và có thể sửa chỉ tiêu khi đợt đã đóng.
    """
    lec = get_target_lecturer(
        request.user,
        pk=pk,
        lecturer_id_param=request.GET.get("lecturer_id") or request.GET.get("pk"),
    )
    locked = is_quota_locked(lecturer=lec)
    is_admin = bool(getattr(request.user, "is_faculty_admin", False))

    form = LecturerProfileForm(
        request.POST or None,
        instance=lec,
        is_locked=locked,
        is_faculty_admin=is_admin,
    )
    if request.method == "POST" and form.is_valid():
        saved_lec = save_lecturer_profile(
            lecturer=lec,
            form=form,
            user=request.user,
            is_locked=locked,
            is_faculty_admin=is_admin,
        )
        messages.success(request, "Đã cập nhật hồ sơ giảng viên thành công.")
        if pk:
            return redirect("lecturer_profile_detail", pk=saved_lec.pk)
        if request.GET.get("lecturer_id"):
            return redirect(f"/ho-so-giang-vien/?lecturer_id={saved_lec.pk}")
        return redirect("lecturer_profile")

    lecturers_list = (
        Lecturer.objects.select_related("user").order_by("user__last_name", "user__first_name") if is_admin else None
    )
    return render(
        request,
        "catalog/lecturer_profile.html",
        {
            "lecturer": lec,
            "form": form,
            "is_locked": locked,
            "is_faculty_admin": is_admin,
            "lecturers_list": lecturers_list,
        },
    )


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
        topic.ineligible_reason = _ineligible_reason(student, topic)

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


def _ineligible_reason(student, topic):
    """Lọc cứng cho SV đang xem: '' nếu đủ điều kiện, ngược lại là lý do (GPA / môn tiên quyết / kỹ năng bắt buộc)."""
    if student is None:
        return ""
    from recommend.engine import Profile, eligible

    if not hasattr(student, "_profile"):
        student._profile = Profile(student)
    return eligible(student._profile, topic)[1]


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
        "ineligible_reason": _ineligible_reason(student, topic),
        "topic": topic,
        "nv1_count": nv1_count,
        "is_student": is_student,
        "student": student,
        "recommendation": recommendation,
        "skills": topic.skills.select_related("skill").all(),
        "prerequisites": topic.prerequisites.select_related("course").all(),
    }
    return render(request, "catalog/topic_detail.html", context)
