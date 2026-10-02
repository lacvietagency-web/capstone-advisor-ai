"""Kết quả phân công. Bản nháp (DRAFT) do thuật toán tạo; Khoa chỉnh và chốt thành OFFICIAL."""

from django.db import models

from catalog.models import RegistrationPeriod, Student, Topic


class Allocation(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Nháp"
        OFFICIAL = "OFFICIAL", "Chính thức"

    class Source(models.TextChoices):
        ILP = "ILP", "Tối ưu ILP"
        GREEDY = "GREEDY", "Tham lam (Greedy)"
        MANUAL = "MANUAL", "Khoa xếp tay"

    period = models.ForeignKey(RegistrationPeriod, on_delete=models.CASCADE, related_name="allocations")
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)  # trống = chưa được xếp
    preference_rank = models.PositiveSmallIntegerField("Đạt nguyện vọng", null=True, blank=True)
    match_score = models.FloatField("Điểm phù hợp", null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    source = models.CharField(max_length=10, choices=Source.choices, default=Source.ILP)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("period", "student")
        verbose_name = verbose_name_plural = "Kết quả phân công"

    def __str__(self):
        return f"{self.period} · {self.student} → {self.topic or 'chưa xếp'}"
