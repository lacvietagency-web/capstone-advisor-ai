"""Form nghiệp vụ: hồ sơ SV, nguyện vọng, đề tài của GV."""

import re

from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

from .models import Field, Lecturer, Student, StudentInterest, StudentSkill, Topic, TopicPrerequisite, TopicSkill

ABOUT_HINT = "Ví dụ: Em thích làm backend, đã làm web bán hàng bằng Django, muốn làm Backend Developer…"


class StudentContactForm(forms.Form):
    """Thông tin liên hệ SV tự sửa (ảnh duyệt 08). Họ tên, MSSV, ngành, GPA là dữ liệu phòng Đào tạo → chỉ đọc."""

    email = forms.EmailField(label="Email", required=False, max_length=254)
    phone = forms.CharField(label="Số điện thoại", required=False, max_length=20)

    def __init__(self, *args, student, **kwargs):
        self.student = student
        kwargs.setdefault("initial", {"email": student.user.email, "phone": student.phone})
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(autocomplete="email", placeholder="ten@truong.edu.vn")
        self.fields["phone"].widget.attrs.update(autocomplete="tel", inputmode="tel", placeholder="09xxxxxxxx")

    def clean_phone(self):
        phone = re.sub(r"[ .-]", "", self.cleaned_data["phone"])
        if phone and not re.fullmatch(r"(\+84|0)\d{9,10}", phone):
            raise forms.ValidationError("Số điện thoại gồm 10–11 chữ số, bắt đầu bằng 0 hoặc +84.")
        return phone

    def save(self):
        self.student.user.email = self.cleaned_data["email"]
        self.student.user.save(update_fields=["email"])
        self.student.phone = self.cleaned_data["phone"]
        self.student.save(update_fields=["phone"])


class StudentAboutForm(forms.ModelForm):
    def clean_about(self):  # giao diện giới hạn 500 ký tự → máy chủ kiểm cùng giới hạn
        about = self.cleaned_data["about"]
        if len(about) > 500:
            raise forms.ValidationError("Giới thiệu bản thân tối đa 500 ký tự.")
        return about

    class Meta:
        model = Student
        fields = ["about"]
        widgets = {
            "about": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": ABOUT_HINT,
                }
            )
        }
        help_texts = {
            "about": "Viết tự nhiên. AI đọc đoạn này để hiểu kinh nghiệm và định hướng của bạn (mô hình M4, M5)."
        }


class _NoDuplicateFormSet(BaseInlineFormSet):
    """Báo lỗi rõ ràng khi một mục (kỹ năng/lĩnh vực) được chọn ở hai dòng."""

    key_field = "skill"
    key_label = "Kỹ năng"

    def clean(self):
        # Kiểm tra trước super().clean(): validate_unique của Django chỉ báo "dữ liệu trùng lặp cho skill".
        seen = set()
        for form in self.forms:
            if not hasattr(form, "cleaned_data") or form.cleaned_data.get("DELETE"):
                continue
            item = form.cleaned_data.get(self.key_field)
            if item is None:
                continue
            if item.pk in seen:
                raise forms.ValidationError(
                    f"{self.key_label} “{item}” bị chọn ở hai dòng — hãy xoá hoặc đổi một dòng."
                )
            seen.add(item.pk)
        super().clean()


class _NoDuplicateFieldFormSet(_NoDuplicateFormSet):
    key_field = "field"
    key_label = "Lĩnh vực"


StudentSkillFormSet = inlineformset_factory(
    Student, StudentSkill, formset=_NoDuplicateFormSet, fields=["skill", "level"], extra=2, can_delete=True
)
StudentInterestFormSet = inlineformset_factory(
    Student, StudentInterest, formset=_NoDuplicateFieldFormSet, fields=["field", "level"], extra=1, can_delete=True
)

MAX_INTERESTS = 3


class StudentInterestPickForm(forms.Form):
    """Lĩnh vực quan tâm dạng lưới ô tick, tối đa 3 (ảnh duyệt 08).

    M3 cần mức quan tâm 1–3: lĩnh vực đã có giữ nguyên mức cũ, lĩnh vực mới tick = mức 3 (quan tâm)."""

    picked = forms.ModelMultipleChoiceField(
        label="Lĩnh vực quan tâm",
        queryset=Field.objects.order_by("name"),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, student, **kwargs):
        self.student = student
        kwargs.setdefault("initial", {"picked": list(student.interests.values_list("field_id", flat=True))})
        super().__init__(*args, prefix="interest", **kwargs)

    def clean_picked(self):
        picked = self.cleaned_data["picked"]
        if len(picked) > MAX_INTERESTS:
            raise forms.ValidationError(f"Chọn tối đa {MAX_INTERESTS} lĩnh vực.")
        return picked

    def save(self):
        picked = {f.pk for f in self.cleaned_data["picked"]}
        self.student.interests.exclude(field_id__in=picked).delete()
        have = set(self.student.interests.values_list("field_id", flat=True))
        StudentInterest.objects.bulk_create(
            StudentInterest(student=self.student, field_id=f, level=3) for f in picked - have
        )


class PreferenceForm(forms.Form):
    """Chọn tối đa 3 nguyện vọng, không trùng nhau."""

    nv1 = forms.ModelChoiceField(Topic.objects.none(), label="Nguyện vọng 1")
    nv2 = forms.ModelChoiceField(Topic.objects.none(), label="Nguyện vọng 2", required=False)
    nv3 = forms.ModelChoiceField(Topic.objects.none(), label="Nguyện vọng 3", required=False)

    def __init__(self, *args, topics=None, student=None, **kw):
        super().__init__(*args, **kw)
        self.student = student
        qs = topics if topics is not None else Topic.objects.filter(status=Topic.Status.OPEN)
        if student is not None:  # chỉ hiện đề tài SV đủ điều kiện (lọc cứng) — khỏi chọn xong mới báo lỗi
            from recommend.engine import Profile, eligible

            profile = Profile(student)
            qs = qs.filter(
                pk__in=[
                    t.pk
                    for t in qs.prefetch_related("skills__skill", "prerequisites__course")  # lý do cần tên kỹ năng/môn
                    if eligible(profile, t)[0]
                ]
            )
        for f in ("nv1", "nv2", "nv3"):
            self.fields[f].queryset = qs

    def clean(self):
        data = super().clean()
        chosen = [t for t in (data.get("nv1"), data.get("nv2"), data.get("nv3")) if t]
        if len(chosen) != len(set(chosen)):
            raise forms.ValidationError("Các nguyện vọng không được trùng đề tài.")
        if self.student is not None:  # lọc cứng: không cho đăng ký đề tài chưa đủ điều kiện, nói rõ lý do
            from recommend.engine import Profile, eligible

            profile = Profile(self.student)
            for name in ("nv1", "nv2", "nv3"):
                topic = data.get(name)
                if topic:
                    ok, why = eligible(profile, topic)
                    if not ok:
                        self.add_error(name, f"Chưa đủ điều kiện đăng ký đề tài này: {why}.")
        return data


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = [
            "title",
            "description",
            "objectives",
            "technologies",
            "fields",
            "difficulty",
            "min_gpa",
            "capacity",
            "status",
            "review_note",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "objectives": forms.Textarea(attrs={"rows": 3}),
            "review_note": forms.Textarea(attrs={"rows": 3}),
            "fields": forms.CheckboxSelectMultiple,
        }
        help_texts = {
            "technologies": "Cách nhau bằng dấu phẩy, VD: Flutter, Spring Boot, MySQL.",
            "review_note": "Lưu ý khi xét sinh viên đăng ký (sinh viên không thấy).",
        }

    def clean_capacity(self):
        """Không giảm sức chứa xuống dưới số SV đã được đồng ý ở đợt chưa công bố (không thì đề tài thành quá chỗ)."""
        cap = self.cleaned_data["capacity"]
        if self.instance.pk:
            from .models import Preference, RegistrationPeriod

            n = (
                Preference.objects.filter(topic=self.instance, status=Preference.Status.ACCEPTED)
                .exclude(period__status=RegistrationPeriod.Status.PUBLISHED)
                .count()
            )
            if cap is not None and cap < n:
                raise forms.ValidationError(
                    f"Đã đồng ý {n} sinh viên cho đề tài này — sức chứa không được nhỏ hơn {n}."
                )
        return cap


TopicSkillFormSet = inlineformset_factory(
    Topic,
    TopicSkill,
    formset=_NoDuplicateFormSet,
    fields=["skill", "required_level", "weight", "is_mandatory"],
    extra=2,
    can_delete=True,
)


class _NoDuplicateCourseFormSet(_NoDuplicateFormSet):
    key_field = "course"
    key_label = "Môn học"


TopicPrerequisiteFormSet = inlineformset_factory(
    Topic,
    TopicPrerequisite,
    formset=_NoDuplicateCourseFormSet,
    fields=["course", "min_score"],
    extra=1,
    can_delete=True,
)


class LecturerProfileForm(forms.ModelForm):
    """Form cập nhật chuyên môn (bộ môn, lĩnh vực) và chỉ tiêu tối đa của GV [UC09]."""

    class Meta:
        model = Lecturer
        fields = ["academic_title", "department", "phone", "bio", "keywords", "fields", "max_students"]
        widgets = {
            "fields": forms.CheckboxSelectMultiple,
            "bio": forms.Textarea(attrs={"rows": 3}),
        }
        help_texts = {
            "phone": "Chỉ Khoa và bạn thấy số này.",
            "keywords": "Cách nhau bằng dấu phẩy, VD: học máy, xử lý ngôn ngữ tiếng Việt.",
        }

    def __init__(self, *args, is_locked=False, is_faculty_admin=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_locked = is_locked
        self.is_faculty_admin = is_faculty_admin
        if self.is_locked and not self.is_faculty_admin:
            self.fields["max_students"].required = False
            self.fields["max_students"].widget.attrs["readonly"] = True
            self.fields[
                "max_students"
            ].help_text = "Đợt đăng ký đã đóng. Chỉ tiêu đã bị khoá (chỉ Khoa mới có quyền điều chỉnh)."

    def clean_max_students(self):
        """Kiểm tra tính hợp lệ của chỉ tiêu tối đa khi đợt đã đóng.

        Công thức:
            Nếu is_locked == True và is_faculty_admin == False:
                Chỉ cho phép giữ nguyên instance.max_students.
                Nếu người dùng thay đổi giá trị -> raise ValidationError.
        """
        val = self.cleaned_data.get("max_students")
        if self.is_locked and not self.is_faculty_admin and self.instance and self.instance.pk:
            if val is None:
                return self.instance.max_students
            if val != self.instance.max_students:
                raise forms.ValidationError(
                    "Đợt đăng ký đã đóng. Chỉ tiêu đã bị khoá, chỉ Khoa mới có quyền điều chỉnh."
                )
        return val
