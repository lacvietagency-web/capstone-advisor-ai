"""Kết quả gợi ý: lưu điểm từng thành phần M1–M5 để hiển thị, giải thích và làm thực nghiệm."""
from django.db import models

from catalog.models import Student, Topic


class Recommendation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="recommendations")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    m1_skill = models.FloatField("M1 kỹ năng")
    m2_academic = models.FloatField("M2 học lực")
    m3_field = models.FloatField("M3 lĩnh vực")
    m4_semantic = models.FloatField("M4 ngữ nghĩa", null=True, blank=True)
    m5_llm = models.FloatField("M5 LLM", null=True, blank=True)     # trống nếu đề tài ngoài Top-K hoặc LLM lỗi
    final_score = models.FloatField("Điểm cuối")
    rank = models.PositiveSmallIntegerField("Thứ hạng", null=True, blank=True)
    reason = models.TextField("Lý do", blank=True)
    weights_version = models.CharField(max_length=40, default="equal")
    model_version = models.CharField(max_length=80, default="v0")
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "topic")
        ordering = ["student", "rank"]
        verbose_name = verbose_name_plural = "Kết quả gợi ý"


class LLMScore(models.Model):
    """Bộ nhớ đệm điểm LLM: cùng hồ sơ + cùng đề tài + cùng prompt + cùng model thì không gọi lại API."""
    cache_key = models.CharField(max_length=64, unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    score_json = models.JSONField()
    model = models.CharField(max_length=80)
    prompt_version = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = "Điểm LLM (cache)"
