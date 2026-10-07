"""Dữ liệu nghiệp vụ: danh mục, sinh viên, giảng viên, đề tài, đợt đăng ký, nguyện vọng."""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# ---------------------------------------------------------------- danh mục
class Major(models.Model):
    name = models.CharField("Chuyên ngành", max_length=120, unique=True)

    class Meta:
        verbose_name = verbose_name_plural = "Chuyên ngành"

    def __str__(self):
        return self.name


class Field(models.Model):
    """Lĩnh vực đề tài: Web, AI, Mobile, Dữ liệu, An toàn thông tin…"""

    name = models.CharField("Lĩnh vực", max_length=80, unique=True)

    class Meta:
        verbose_name = verbose_name_plural = "Lĩnh vực"

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField("Kỹ năng", max_length=80, unique=True)
    field = models.ForeignKey(Field, verbose_name="Thuộc lĩnh vực", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "Kỹ năng"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Course(models.Model):
    code = models.CharField("Mã môn", max_length=20, unique=True)
    name = models.CharField("Tên môn", max_length=150)
    field = models.ForeignKey(Field, verbose_name="Lĩnh vực", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "Môn học"

    def __str__(self):
        return f"{self.code} – {self.name}"


# ---------------------------------------------------------------- con người
LEVEL_1_5 = [MinValueValidator(1), MaxValueValidator(5)]


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student")
    student_code = models.CharField("Mã sinh viên", max_length=20, unique=True)
    major = models.ForeignKey(Major, verbose_name="Chuyên ngành", on_delete=models.PROTECT)
    gpa = models.DecimalField(
        "GPA (thang 4)", max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(4)]
    )
    about = models.TextField("Tự giới thiệu, kinh nghiệm, định hướng nghề", blank=True)
    profile_version = models.PositiveIntegerField(default=1, editable=False)  # tăng mỗi lần sửa hồ sơ → làm mới điểm AI

    class Meta:
        verbose_name = verbose_name_plural = "Sinh viên"

    def __str__(self):
        return f"{self.student_code} – {self.user.get_full_name() or self.user.username}"


class StudentSkill(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="skills")
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT)
    level = models.PositiveSmallIntegerField("Mức (1–5)", validators=LEVEL_1_5)

    class Meta:
        unique_together = ("student", "skill")
        verbose_name = verbose_name_plural = "Kỹ năng sinh viên"

    def __str__(self):
        return f"{self.student} · {self.skill} ({self.level}/5)"


class StudentInterest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="interests")
    field = models.ForeignKey(Field, on_delete=models.PROTECT)
    level = models.PositiveSmallIntegerField(
        "Mức quan tâm (1–3)", validators=[MinValueValidator(1), MaxValueValidator(3)]
    )

    class Meta:
        unique_together = ("student", "field")
        verbose_name = verbose_name_plural = "Lĩnh vực quan tâm"

    def __str__(self):
        return f"{self.student} · {self.field} ({self.level}/3)"


class StudentCourseResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="course_results")
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    score = models.DecimalField(
        "Điểm (thang 10)", max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        unique_together = ("student", "course")
        verbose_name = verbose_name_plural = "Điểm môn học"

    def __str__(self):
        return f"{self.student} · {self.course}: {self.score}"


class Lecturer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lecturer")
    department = models.CharField("Bộ môn", max_length=120, blank=True)
    max_students = models.PositiveSmallIntegerField("Chỉ tiêu hướng dẫn tối đa", default=5)
    fields = models.ManyToManyField(Field, verbose_name="Lĩnh vực chuyên môn", blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "Giảng viên"

    def __str__(self):
        return self.user.get_full_name() or self.user.username


# ---------------------------------------------------------------- đề tài
class Topic(models.Model):
    class Difficulty(models.IntegerChoices):
        EASY = 1, "Dễ"
        MEDIUM = 2, "Trung bình"
        HARD = 3, "Khó"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Nháp"
        OPEN = "OPEN", "Đang mở"
        CLOSED = "CLOSED", "Đã đóng"

    lecturer = models.ForeignKey(Lecturer, verbose_name="Giảng viên", on_delete=models.CASCADE, related_name="topics")
    title = models.CharField("Tên đề tài", max_length=255)
    description = models.TextField("Mô tả")
    fields = models.ManyToManyField(Field, verbose_name="Lĩnh vực")
    difficulty = models.PositiveSmallIntegerField("Độ khó", choices=Difficulty.choices, default=Difficulty.MEDIUM)
    min_gpa = models.DecimalField("GPA tối thiểu", max_digits=3, decimal_places=2, default=0)
    capacity = models.PositiveSmallIntegerField("Số sinh viên tối đa", default=1)
    status = models.CharField("Trạng thái", max_length=10, choices=Status.choices, default=Status.OPEN)
    version = models.PositiveIntegerField(default=1, editable=False)

    class Meta:
        verbose_name = verbose_name_plural = "Đề tài"

    def __str__(self):
        return self.title

    def skill_weight_shares(self):
        """Tỉ lệ % trọng số từng kỹ năng yêu cầu — chỉ để HIỂN THỊ, không ép tổng = 100% (chủ dự án chốt 07/10/2026)."""
        skills = list(self.skills.select_related("skill"))
        total = sum(ts.weight for ts in skills) or 1
        return [(ts, round(100 * ts.weight / total)) for ts in skills]


class TopicSkill(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="skills")
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT)
    required_level = models.PositiveSmallIntegerField("Mức yêu cầu (1–5)", validators=LEVEL_1_5)
    weight = models.FloatField("Trọng số", default=1.0)
    is_mandatory = models.BooleanField("Bắt buộc", default=False)

    class Meta:
        unique_together = ("topic", "skill")
        verbose_name = verbose_name_plural = "Kỹ năng yêu cầu"

    def __str__(self):
        return f"{self.topic} · {self.skill} ≥ {self.required_level}"


class TopicPrerequisite(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="prerequisites")
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    min_score = models.DecimalField("Điểm tối thiểu", max_digits=4, decimal_places=2, default=5)

    class Meta:
        unique_together = ("topic", "course")
        verbose_name = verbose_name_plural = "Môn tiên quyết"

    # ---------------------------------------------------------------- đăng ký

    def __str__(self):
        return f"{self.topic} · {self.course} ≥ {self.min_score}"


class RegistrationPeriod(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Đang mở đăng ký"
        CLOSED = "CLOSED", "Đã đóng đăng ký"
        OPTIMIZED = "OPTIMIZED", "Đã chạy phân công (nháp)"
        PUBLISHED = "PUBLISHED", "Đã công bố"

    name = models.CharField("Tên đợt", max_length=120)
    start_at = models.DateTimeField("Bắt đầu")
    end_at = models.DateTimeField("Kết thúc")
    status = models.CharField("Trạng thái", max_length=10, choices=Status.choices, default=Status.OPEN)

    class Meta:
        verbose_name = verbose_name_plural = "Đợt đăng ký"

    def __str__(self):
        return self.name


class Preference(models.Model):
    """Nguyện vọng của sinh viên: tối đa 3, rank 1 là NV1."""

    class Status(models.TextChoices):
        PENDING = "PENDING", "Chờ duyệt"
        ACCEPTED = "ACCEPTED", "Đồng ý"
        REJECTED = "REJECTED", "Từ chối"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="preferences")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    period = models.ForeignKey(RegistrationPeriod, on_delete=models.CASCADE)
    rank = models.PositiveSmallIntegerField("Nguyện vọng", validators=[MinValueValidator(1), MaxValueValidator(3)])
    status = models.CharField("Trạng thái", max_length=10, choices=Status.choices, default=Status.PENDING)
    reject_reason = models.TextField("Lý do từ chối", blank=True)  # bắt buộc khi GV từ chối (chủ dự án chốt 07/10/2026)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("student", "period", "rank"), ("student", "period", "topic")]
        verbose_name = verbose_name_plural = "Nguyện vọng"

    def __str__(self):
        return f"{self.student} · NV{self.rank}: {self.topic}"


class AuditLog(models.Model):
    """Nhật ký: ai sửa gì, lúc nào — để Khoa truy vết khi có khiếu nại."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=40)
    entity = models.CharField(max_length=60)
    entity_id = models.CharField(max_length=40)
    detail = models.JSONField(default=dict, blank=True)
    at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-at"]
        verbose_name = verbose_name_plural = "Nhật ký thay đổi"

    def __str__(self):
        return f"{self.at:%d/%m/%Y %H:%M} {self.user} {self.action} {self.entity}#{self.entity_id}"
