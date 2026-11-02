"""Kết quả gợi ý và cấu hình trọng số AHP:

- Recommendation: lưu điểm từng thành phần M1–M5 để hiển thị, giải thích và làm thực nghiệm.
- LLMScore: bộ nhớ đệm điểm LLM tránh gọi lại API tốn kém.
- WeightSet: lưu cấu hình trọng số AHP do Khoa thiết lập và lựa chọn áp dụng.
"""

from django.core.exceptions import ValidationError
from django.db import models

from catalog.models import Student, Topic


class WeightSet(models.Model):
    """Bộ trọng số AHP cho 4 tiêu chí: kỹ năng, lĩnh vực, ngữ nghĩa, LLM (đã bỏ M2 học lực).

    Lưu trữ vector trọng số đã chuẩn hoá, ma trận so sánh cặp gốc và tỷ số nhất quán CR.
    Chỉ một bộ trọng số duy nhất có is_active=True tại một thời điểm để hệ thống sử dụng.
    """

    name = models.CharField("Tên bộ trọng số", max_length=100, unique=True)
    weights = models.JSONField("Trọng số (JSON)", help_text="Từ điển 4 phần tử: skill, field, semantic, llm.")
    matrix = models.JSONField(
        "Ma trận so sánh cặp (JSON)",
        help_text="Ma trận 4x4 dạng danh sách 2 chiều (thứ tự skill, field, semantic, llm).",
    )
    cr = models.FloatField("Tỷ số nhất quán (CR)")
    is_active = models.BooleanField("Đang sử dụng", default=False)
    created_at = models.DateTimeField("Thời điểm tạo", auto_now_add=True)

    class Meta:
        verbose_name = "Bộ trọng số"
        verbose_name_plural = "Bộ trọng số"
        ordering = ["-is_active", "-created_at"]

    def __str__(self):
        active_str = " [Đang dùng]" if self.is_active else ""
        return f"{self.name} (CR={self.cr:.4f}){active_str}"

    def save(self, *args, **kwargs):
        if self.is_active:
            WeightSet.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.cr is not None and self.cr >= 0.1:
            raise ValidationError(
                {"cr": f"Tỷ số nhất quán CR = {self.cr:.4f} >= 0.1 (không đạt tính nhất quán AHP, bị từ chối)."}
            )
        if self.weights:
            expected = {"skill", "field", "semantic", "llm"}
            missing = expected - set(self.weights.keys())
            if missing:
                raise ValidationError({"weights": f"Thiếu các tiêu chí thành phần: {missing}"})

    @classmethod
    def from_matrix(cls, name: str, matrix, is_active: bool = False):
        """Khởi tạo và lưu WeightSet từ ma trận so sánh cặp 5x5; từ chối nếu CR >= 0.1."""
        from recommend.ahp import calculate_ahp

        result = calculate_ahp(matrix, raise_on_inconsistent=True)
        raw_matrix = matrix if isinstance(matrix, list) else matrix.tolist()
        return cls.objects.create(
            name=name,
            weights=result.weights,
            matrix=raw_matrix,
            cr=result.cr,
            is_active=is_active,
        )


class Recommendation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="recommendations")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    m1_skill = models.FloatField("M1 kỹ năng")
    m3_field = models.FloatField("M3 lĩnh vực")
    m4_semantic = models.FloatField("M4 ngữ nghĩa", null=True, blank=True)
    m5_llm = models.FloatField("M5 LLM", null=True, blank=True)  # trống nếu đề tài ngoài Top-K hoặc LLM lỗi
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

    def __str__(self):
        return f"{self.student} · #{self.rank} {self.topic} ({self.final_score:.1f})"


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

    def __str__(self):
        return f"LLM {self.model} · {self.student} · {self.topic}"
