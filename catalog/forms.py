"""Form nghiệp vụ: hồ sơ SV, nguyện vọng, đề tài của GV."""

from django import forms
from django.forms import inlineformset_factory

from .models import Student, StudentInterest, StudentSkill, Topic, TopicSkill

ABOUT_HINT = "Ví dụ: Em thích làm backend, đã làm web bán hàng bằng Django, muốn làm Backend Developer…"


class StudentAboutForm(forms.ModelForm):
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


StudentSkillFormSet = inlineformset_factory(Student, StudentSkill, fields=["skill", "level"], extra=2, can_delete=True)
StudentInterestFormSet = inlineformset_factory(
    Student, StudentInterest, fields=["field", "level"], extra=1, can_delete=True
)


class PreferenceForm(forms.Form):
    """Chọn tối đa 3 nguyện vọng, không trùng nhau."""

    nv1 = forms.ModelChoiceField(Topic.objects.none(), label="Nguyện vọng 1")
    nv2 = forms.ModelChoiceField(Topic.objects.none(), label="Nguyện vọng 2", required=False)
    nv3 = forms.ModelChoiceField(Topic.objects.none(), label="Nguyện vọng 3", required=False)

    def __init__(self, *args, topics=None, **kw):
        super().__init__(*args, **kw)
        for f in ("nv1", "nv2", "nv3"):
            self.fields[f].queryset = topics if topics is not None else Topic.objects.filter(status=Topic.Status.OPEN)

    def clean(self):
        data = super().clean()
        chosen = [t for t in (data.get("nv1"), data.get("nv2"), data.get("nv3")) if t]
        if len(chosen) != len(set(chosen)):
            raise forms.ValidationError("Các nguyện vọng không được trùng đề tài.")
        return data


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["title", "description", "fields", "difficulty", "min_gpa", "capacity", "status"]
        widgets = {"description": forms.Textarea(attrs={"rows": 5}), "fields": forms.CheckboxSelectMultiple}


TopicSkillFormSet = inlineformset_factory(
    Topic, TopicSkill, fields=["skill", "required_level", "weight", "is_mandatory"], extra=2, can_delete=True
)
