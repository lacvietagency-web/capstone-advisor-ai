from django.conf import settings
from django.db import models


class ChatLog(models.Model):
    """Mỗi lượt hỏi–đáp của trợ lý ảo: để đánh giá độ đúng (GĐ2) và để Khoa biết sinh viên hay hỏi gì."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField("Vai trò", max_length=10)
    question = models.TextField("Câu hỏi")
    answer = models.TextField("Câu trả lời")
    sources = models.JSONField("Nguồn đã trích", default=list)
    mode = models.CharField("Chế độ", max_length=10)  # llm | fallback
    model = models.CharField("Mô hình", max_length=80, blank=True)
    ms = models.PositiveIntegerField("Thời gian (ms)", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = "Nhật ký trợ lý ảo"
        ordering = ["-created_at"]

    def __str__(self):
        return self.question[:60]
