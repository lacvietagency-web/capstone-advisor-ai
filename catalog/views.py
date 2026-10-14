"""Màn hình nghiệp vụ cho Sinh viên và Giảng viên."""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from recommend.models import Recommendation
from recommend.services import ensure_recommendations, refresh_student, score_preferences

from .forms import (
    LecturerProfileForm,
    PreferenceForm,
    StudentAboutForm,
    StudentContactForm,
    StudentInterestPickForm,
    StudentSkillFormSet,
    TopicForm,
    TopicPrerequisiteFormSet,
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
    remaining_capacity,
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
    contact = StudentContactForm(request.POST or None, student=st)
    about = StudentAboutForm(request.POST or None, instance=st)
    skills = StudentSkillFormSet(request.POST or None, instance=st, prefix="skills")
    interests = StudentInterestPickForm(request.POST or None, student=st)
    forms_ok = all([contact.is_valid(), about.is_valid(), skills.is_valid(), interests.is_valid()])
    if request.method == "POST" and forms_ok:
        with transaction.atomic():
            if "email" in request.POST:  # trang cũ không có ô liên hệ → không xoá trắng email/SĐT
                contact.save()
            about.save()
            skills.save()
            if "interest-shown" in request.POST:  # biểu mẫu có lưới lĩnh vực (ô ẩn interest-shown)
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
        {
            "student": st,
            "contact_form": contact,
            "about_form": about,
            "skill_formset": skills,
            "interest_form": interests,
            **profile_completeness(st),
        },
    )


def profile_completeness(student):
    """Mức độ hoàn thiện hồ sơ: 4 mục (giới thiệu, kỹ năng, lĩnh vực quan tâm, điểm môn học) — mỗi mục 25%.
    `completeness` (0–100) và `completeness_items` [(nhãn, đã có?)] để hiển thị danh sách kiểm."""
    items = [
        ("Giới thiệu bản thân", bool(student.about.strip())),
        ("Kỹ năng và mức độ", student.skills.exists()),
        ("Lĩnh vực quan tâm", student.interests.exists()),
        ("Điểm các môn đã học", student.course_results.exists()),
    ]
    return {"completeness": 25 * sum(ok for _, ok in items), "completeness_items": items}


def _initial_preferences(request, student, period):
    """Giá trị ban đầu của form NV1–NV3: nguyện vọng đã lưu + đề tài truyền qua ?topic= vào ô trống đầu tiên."""
    initial = {f"nv{p.rank}": p.topic for p in Preference.objects.filter(student=student, period=period)}
    preset_topic_id = request.GET.get("topic") or request.GET.get("topic_id")
    if preset_topic_id and request.method == "GET":
        try:
            preset_topic = Topic.objects.get(pk=preset_topic_id, status=Topic.Status.OPEN)
        except (Topic.DoesNotExist, ValueError):
            return initial
        if preset_topic not in initial.values():
            slot = next((f"nv{r}" for r in (1, 2, 3) if not initial.get(f"nv{r}")), None)
            if slot:
                initial[slot] = preset_topic
            else:
                messages.info(
                    request,
                    f"Bạn đã chọn đủ 3 nguyện vọng. Muốn đăng ký «{preset_topic.title}» thì thay vào một ô bên dưới.",
                )
    return initial


def _save_preferences(request, student, period, form, submit):
    """Ghi lại NV1–NV3 (xoá rồi tạo lại). Đề tài GV đã duyệt giữ nguyên trạng thái, lý do và nhận xét.
    submit=False → bản nháp (GV, thống kê, thuật toán không thấy); True → nộp chính thức."""
    with transaction.atomic():
        old = Preference.objects.filter(student=student, period=period)
        kept = {p.topic_id: (p.status, p.reject_reason, p.lecturer_note) for p in old}
        old.delete()
        for rank in (1, 2, 3):
            topic = form.cleaned_data.get(f"nv{rank}")
            if topic:
                status, reason, note = kept.get(topic.pk, (Preference.Status.PENDING, "", ""))
                Preference.objects.create(
                    student=student,
                    period=period,
                    topic=topic,
                    rank=rank,
                    status=status,
                    reject_reason=reason,
                    lecturer_note=note,
                    submitted=submit,
                    submitted_at=timezone.now() if submit else None,
                )
        AuditLog.objects.create(
            user=request.user,
            action="submit_preferences" if submit else "save_preferences_draft",
            entity="Preference",
            entity_id=student.pk,
            detail={f"nv{r}": getattr(form.cleaned_data.get(f"nv{r}"), "pk", None) for r in (1, 2, 3)},
        )
    score_preferences(student)


@login_required
def student_preferences(request):
    """Nguyện vọng NV1–NV3. POST action: "draft" lưu nháp · "submit" (mặc định) nộp · "withdraw" rút về nháp."""
    st = _student(request)
    ensure_recommendations(st)
    period = _open_period()
    if period is None:
        return render(request, "catalog/student_preferences.html", _submitted_preferences(st))
    action = request.POST.get("action") or "submit"
    if request.method == "POST" and action == "withdraw":
        n = Preference.objects.filter(student=st, period=period).update(submitted=False, submitted_at=None)
        AuditLog.objects.create(user=request.user, action="withdraw_preferences", entity="Preference", entity_id=st.pk)
        messages.success(request, f"Đã rút {n} nguyện vọng về bản nháp — sửa xong nhớ nộp lại trước khi đợt đóng.")
        return redirect("student_preferences")
    form = PreferenceForm(request.POST or None, initial=_initial_preferences(request, st, period), student=st)
    if request.method == "POST" and form.is_valid():
        submit = action != "draft"
        _save_preferences(request, st, period, form, submit)
        if submit:
            messages.success(request, "Đã lưu nguyện vọng và nộp chính thức.")
        else:
            messages.success(request, "Đã lưu nháp nguyện vọng — giảng viên chưa thấy cho tới khi bạn nộp chính thức.")
        return redirect("student_preferences")
    scores = {r.topic_id: r for r in Recommendation.objects.filter(student=st)}
    top5 = Recommendation.objects.filter(student=st, rank__isnull=False).select_related("topic").order_by("rank")[:5]
    return render(
        request,
        "catalog/student_preferences.html",
        {"period": period, "form": form, "top5": top5, "scores": scores, **_preference_rows(st, period, scores)},
    )


def _preference_rows(student, period, scores):
    """Nguyện vọng đã lưu của đợt: `pref_rows` (rank, pref, rec, eligibility, remaining = chỗ còn của đề tài),
    `is_submitted` (đã nộp chính thức hết chưa), `submitted_at` (lần nộp gần nhất)."""
    prefs = list(
        Preference.objects.filter(student=student, period=period)
        .select_related("topic__lecturer__user")
        .prefetch_related("topic__skills__skill", "topic__prerequisites__course")
        .order_by("rank")
    )
    rows = [
        {
            "rank": p.rank,
            "pref": p,
            "rec": scores.get(p.topic_id),
            "eligibility": _eligibility(student, p.topic),
            "remaining": remaining_capacity(p.topic, period),
            "checklist": _checklist(student, p.topic, remaining_capacity(p.topic, period)),
        }
        for p in prefs
    ]
    return {
        "pref_rows": rows,
        "is_submitted": bool(prefs) and all(p.submitted for p in prefs),
        "submitted_at": max((p.submitted_at for p in prefs if p.submitted_at), default=None),
    }


def _submitted_preferences(student):
    """Không có đợt đang mở: cho SV xem lại nguyện vọng đã nộp ở đợt gần nhất (chỉ đọc) thay vì trang trống."""
    last = Preference.objects.filter(student=student).select_related("period").order_by("-period__start_at").first()
    if last is None:
        return {"period": None, "last_period": None, "submitted": []}
    scores = {r.topic_id: r for r in Recommendation.objects.filter(student=student)}
    prefs = (
        Preference.objects.filter(student=student, period=last.period)
        .select_related("topic__lecturer__user")
        .order_by("rank")
    )
    submitted = [{"pref": p, "rec": scores.get(p.topic_id)} for p in prefs]
    return {"period": None, "last_period": last.period, "submitted": submitted}


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
    # Môn tiên quyết là phần tuỳ chọn của form: chỉ xử lý khi trang gửi kèm (có management form)
    prereq_data = request.POST if "prereqs-TOTAL_FORMS" in request.POST else None
    prereqs = TopicPrerequisiteFormSet(prereq_data, instance=topic, prefix="prereqs")
    prereqs_ok = prereq_data is None or prereqs.is_valid()
    if request.method == "POST" and form.is_valid() and skills.is_valid() and prereqs_ok:
        with transaction.atomic():
            t = form.save(commit=False)
            t.lecturer = lec
            if t.pk:
                t.version += 1  # vector ngữ nghĩa và điểm AI của đề tài sẽ được tính lại
            t.save()
            form.save_m2m()
            skills.instance = t
            skills.save()
            if prereq_data is not None:
                prereqs.instance = t
                prereqs.save()
            AuditLog.objects.create(user=request.user, action="save_topic", entity="Topic", entity_id=t.pk)
        messages.success(request, "Đã lưu đề tài.")
        return redirect("lecturer_topics")
    return render(
        request,
        "catalog/lecturer_topic_form.html",
        {"form": form, "skill_formset": skills, "prereq_formset": prereqs, "topic": topic},
    )


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
        if not 5 <= len(reason) <= 500:  # GV phải ghi lý do để SV biết và Khoa truy vết khi khiếu nại
            messages.error(request, "Lý do từ chối cần từ 5 đến 500 ký tự.")
            return redirect("lecturer_registrations", pk=topic.pk)
    else:
        messages.error(request, "Thao tác không hợp lệ.")
        return redirect("lecturer_registrations", pk=topic.pk)

    note = (request.POST.get("note") or "").strip()[:1000]  # nhận xét GV (tuỳ chọn), SV xem sau khi đã duyệt
    with transaction.atomic():
        pref.status = new_status
        pref.reject_reason = reason if new_status == Preference.Status.REJECTED else ""
        if note:
            pref.lecturer_note = note
        pref.save(update_fields=["status", "reject_reason", "lecturer_note"])
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
    reason_txt = f" Lý do: {pref.reject_reason}" if pref.reject_reason else ""  # list mặc định chỉ hiện Chờ duyệt
    messages.success(request, f"Đã {label} nguyện vọng của sinh viên {pref.student}.{reason_txt}")
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
        Preference.objects.filter(topic=topic, submitted=True)
        .select_related("student__user", "period")
        .order_by("rank", "created_at")
    )
    for p in prefs:
        ensure_recommendations(p.student)
    scores = {r.student_id: r for r in Recommendation.objects.filter(topic=topic)}
    left = remaining_capacity(topic, _open_period())
    rows = [
        {
            "pref": p,
            "rec": scores.get(p.student_id),
            "eligibility": _eligibility(p.student, topic),
            "checklist": _checklist(p.student, topic, left),
        }
        for p in prefs
    ]
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
            **lecturer_load_stats(lec),
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

    student = None
    scores_map = {}
    is_student_user = (
        request.user.is_authenticated
        and getattr(request.user, "is_student", False)
        and hasattr(request.user, "student")
    )
    if is_student_user:
        student = request.user.student
        ensure_recommendations(student)
        scores_map = get_student_recommendations_map(student)
    tab, tab_counts, filtered_qs = _eligibility_tab(request, student, filtered_qs)
    annotated_qs = _sort_topics(request, student, annotate_topics_nv1(filtered_qs))
    page_obj = paginate_topics(annotated_qs, page_number=page_num, per_page=per_page)

    for topic in page_obj:
        topic.recommendation = scores_map.get(topic.id)
        topic.match_score = topic.recommendation.final_score if topic.recommendation else None
        topic.ineligible_reason = _ineligible_reason(student, topic)
        topic.eligibility = _eligibility(student, topic)
        topic.remaining = remaining_capacity(topic, _open_period())

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
        "open_period": _open_period(),
        "tab": tab,
        "tab_counts": tab_counts,
        "sort": request.GET.get("sort") or "",
    }
    return render(request, "catalog/topic_list.html", context)


def _eligibility_tab(request, student, qs):
    """Tab Đủ / Chưa đủ điều kiện (chỉ với SV): ?dk=1 hoặc ?dk=0. Trả (tab, số đếm từng tab, queryset đã lọc)."""
    if student is None:
        return "", {}, qs
    from recommend.engine import Profile, eligible

    profile = Profile(student)
    ok_ids = [t.pk for t in qs.prefetch_related("skills", "prerequisites") if eligible(profile, t)[0]]
    counts = {"all": qs.count(), "ok": len(ok_ids)}
    counts["no"] = counts["all"] - counts["ok"]
    tab = request.GET.get("dk", "")
    if tab == "1":
        qs = qs.filter(pk__in=ok_ids)
    elif tab == "0":
        qs = qs.exclude(pk__in=ok_ids)
    return tab, counts, qs


TOPIC_SORTS = {"title": "title", "difficulty": "difficulty", "capacity": "-capacity", "nv1": "-nv1_count"}


def _sort_topics(request, student, qs):
    """?sort=score (điểm phù hợp của SV, cao trước) | title | difficulty | capacity | nv1. Mặc định giữ thứ tự cũ."""
    key = request.GET.get("sort") or ""
    if key == "score" and student is not None:
        from django.db.models import OuterRef, Subquery

        score = Recommendation.objects.filter(student=student, topic=OuterRef("pk")).values("final_score")[:1]
        return qs.annotate(match=Subquery(score)).order_by(F("match").desc(nulls_last=True), "title")
    if key in TOPIC_SORTS:
        return qs.order_by(TOPIC_SORTS[key], "title")
    return qs


def _eligibility(student, topic):
    """Danh sách điều kiện bắt buộc (eligibility_reasons) cho SV đang xem; [] nếu không phải SV."""
    if student is None:
        return []
    from recommend.engine import Profile, eligibility_reasons

    if not hasattr(student, "_profile"):
        student._profile = Profile(student)
    return eligibility_reasons(student._profile, topic)


def _checklist(student, topic, remaining=None):
    """Khối "Kiểm tra điều kiện" 4 mục (recommend.engine.condition_checklist) cho SV; [] nếu không phải SV."""
    if student is None:
        return []
    from recommend.engine import Profile, condition_checklist

    if not hasattr(student, "_profile"):
        student._profile = Profile(student)
    return condition_checklist(student._profile, topic, remaining)


def _ineligible_reason(student, topic):
    """Lọc cứng cho SV đang xem: '' nếu đủ điều kiện, ngược lại là lý do (GPA / môn tiên quyết / kỹ năng bắt buộc)."""
    if student is None:
        return ""
    from recommend.engine import Profile, eligible

    if not hasattr(student, "_profile"):
        student._profile = Profile(student)
    return eligible(student._profile, topic)[1]


def _skills_with_share(topic):
    """Kỹ năng yêu cầu kèm .share = % tỉ trọng trong tổng trọng số (Topic.skill_weight_shares)."""
    out = []
    for ts, pct in topic.skill_weight_shares():
        ts.share = pct
        ts.ratio = round(pct / 100, 2)  # ảnh duyệt 11 ghi trọng số dạng 0,25
        out.append(ts)
    return out


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
    if student:
        ensure_recommendations(student)
    recommendation = get_student_match_score(student, topic)

    context = {
        "ineligible_reason": _ineligible_reason(student, topic),
        "eligibility": _eligibility(student, topic),
        "checklist": _checklist(student, topic, remaining_capacity(topic, _open_period())),
        "open_period": _open_period(),
        "remaining": remaining_capacity(topic, _open_period()),
        "topic": topic,
        "nv1_count": nv1_count,
        "is_student": is_student,
        "student": student,
        "recommendation": recommendation,
        "skills": _skills_with_share(topic),
        "prerequisites": topic.prerequisites.select_related("course").all(),
    }
    return render(request, "catalog/topic_detail.html", context)


# ---------------------------------------------------------------- Khoa: nhập dữ liệu Excel (UC15)
MAX_IMPORT_BYTES = 5 * 1024 * 1024


IMPORT_TMP = settings.BASE_DIR / "tmp" / "imports"  # tệp đã kiểm tra, chờ Khoa bấm xác nhận (gitignore)
IMPORT_LABELS = {"students": "Sinh viên", "lecturers": "Giảng viên", "topics": "Đề tài", "skills": "Kỹ năng"}


def _import_result(ok, errors, stats, filename, pending=False):
    rows = [(IMPORT_LABELS.get(k, k), v) for k, v in stats.items()]
    return {"ok": ok, "errors": errors, "stats": stats, "rows": rows, "filename": filename, "pending": pending}


def _uploaded_file(request):
    """Tệp .xlsx hợp lệ từ request, hoặc None (đã báo lỗi bằng messages)."""
    f = request.FILES.get("file")
    if not f:
        messages.error(request, "Chưa chọn tệp Excel.")
    elif not f.name.lower().endswith(".xlsx"):
        messages.error(request, "Chỉ nhận tệp .xlsx.")
    elif f.size > MAX_IMPORT_BYTES:
        messages.error(request, "Tệp lớn hơn 5 MB.")
    else:
        return f
    return None


def _import_check(request, f):
    """Bước 1: kiểm tra (chạy thử rồi hoàn tác). Sạch lỗi thì giữ tệp lại, chờ bước xác nhận."""
    import uuid

    from .importer import import_excel_data

    ok, errors, stats = import_excel_data(f, dry_run=True)
    if not ok:
        messages.error(request, f"Tệp có {len(errors)} lỗi — sửa rồi tải lên lại. Chưa nhập gì.")
        return _import_result(ok, errors, stats, f.name)
    IMPORT_TMP.mkdir(parents=True, exist_ok=True)
    token = uuid.uuid4().hex
    f.seek(0)
    (IMPORT_TMP / f"{token}.xlsx").write_bytes(f.read())
    request.session["import_pending"] = {"token": token, "filename": f.name}
    messages.info(request, "Tệp hợp lệ. Kiểm tra số dòng bên dưới rồi bấm Xác nhận nhập.")
    return _import_result(ok, errors, stats, f.name, pending=True)


def _import_confirm(request):
    """Bước 2: nhập thật đúng tệp đã kiểm tra ở bước 1 (cùng phiên đăng nhập)."""
    from .importer import import_excel_data

    pending = request.session.pop("import_pending", None)
    path = IMPORT_TMP / f"{pending['token']}.xlsx" if pending else None
    if not path or not path.exists():
        messages.error(request, "Không còn tệp chờ xác nhận — hãy tải lên và kiểm tra lại.")
        return None
    ok, errors, stats = import_excel_data(path)
    path.unlink(missing_ok=True)
    return _import_result(ok, errors, stats, pending["filename"])


@login_required
def faculty_import(request):
    """Khoa nhập dữ liệu Excel (UC15), 2 bước: action=check (kiểm tra, chưa ghi) → action=confirm (ghi thật).
    Không có action: kiểm tra và nhập luôn (all-or-nothing) như bản trước."""
    if not (getattr(request.user, "is_faculty_admin", False) or request.user.is_superuser):
        raise PermissionDenied("Chỉ tài khoản Khoa mới có quyền nhập dữ liệu.")
    from .importer import import_excel_data

    result = None
    action = request.POST.get("action", "")
    if request.method == "POST" and action == "confirm":
        result = _import_confirm(request)
    elif request.method == "POST":
        f = _uploaded_file(request)
        if f and action == "check":
            result = _import_check(request, f)
        elif f:
            ok, errors, stats = import_excel_data(f)
            result = _import_result(ok, errors, stats, f.name)
    if result is not None and not result["pending"]:
        AuditLog.objects.create(
            user=request.user,
            action="import_excel",
            entity="Excel",
            detail={
                "file": result["filename"],
                "ok": result["ok"],
                "stats": result["stats"],
                "n_errors": len(result["errors"]),
            },
        )
        if result["ok"]:
            done = ", ".join(f"{v} {k.lower()}" for k, v in result["rows"])
            messages.success(request, f"Đã nhập xong: {done}.")
        elif action != "check":
            messages.error(request, f"Không nhập gì vì có {len(result['errors'])} lỗi — sửa tệp rồi tải lên lại.")
    return render(
        request, "catalog/faculty_import.html", {"result": result, "max_mb": MAX_IMPORT_BYTES // (1024 * 1024)}
    )


@login_required
def faculty_import_sample(request):
    """Tải tệp Excel mẫu (4 sheet: SinhVien, GiangVien, DeTai, KyNang)."""
    if not (getattr(request.user, "is_faculty_admin", False) or request.user.is_superuser):
        raise PermissionDenied("Chỉ tài khoản Khoa mới có quyền nhập dữ liệu.")
    from .importer import create_sample_excel

    resp = HttpResponse(
        create_sample_excel(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    resp["Content-Disposition"] = 'attachment; filename="mau_nhap_lieu.xlsx"'
    return resp


def lecturer_load_stats(lecturer):
    """Số liệu hồ sơ GV: số đề tài, số SV đang hướng dẫn (nguyện vọng đã nộp được đồng ý + phân công chính thức,
    không đếm trùng), số đề tài theo lĩnh vực (`field_stats`: [(tên lĩnh vực, số đề tài)], nhiều trước)."""
    from django.db.models import Count

    from allocate.models import Allocation

    accepted = set(
        Preference.objects.filter(
            topic__lecturer=lecturer, status=Preference.Status.ACCEPTED, submitted=True
        ).values_list("student_id", flat=True)
    )
    official = set(
        Allocation.objects.filter(topic__lecturer=lecturer, status=Allocation.Status.OFFICIAL).values_list(
            "student_id", flat=True
        )
    )
    fields = (
        Field.objects.filter(topic__lecturer=lecturer)
        .annotate(n=Count("topic", distinct=True))
        .order_by("-n", "name")
        .values_list("name", "n")
    )
    return {
        "n_topics": lecturer.topics.count(),
        "n_guided": len(accepted | official),
        "field_stats": list(fields),
    }
