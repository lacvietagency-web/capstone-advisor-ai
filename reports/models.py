from django.db import models


class GopY(models.Model):
    """Góp ý của giảng viên hướng dẫn gửi từ trang trình bày /trinh-bay/ (không cần đăng nhập).

    noi_dung = {"danh_gia": {phần: {"muc": ..., "ghi_chu": ...}}, "quyet_dinh": {câu: {"chon": ..., "ghi_chu": ...}},
    "gop_y": "văn bản tự do"}. Hermes đọc bảng này để báo chủ dự án qua Telegram.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    ten = models.CharField("Người góp ý", max_length=120, blank=True)
    noi_dung = models.JSONField("Đánh giá, quyết định và góp ý")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Góp ý"
        verbose_name_plural = "Góp ý"

    def __str__(self):
        return f"Góp ý #{self.pk} · {self.ten or 'Không ghi tên'} · {self.created_at:%d/%m/%Y %H:%M}"
