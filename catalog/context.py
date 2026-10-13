"""Biến dùng chung cho mọi template: đợt đăng ký hiện hành — mọi trang cùng đọc một trạng thái đợt."""

from django.conf import settings
from django.utils.functional import SimpleLazyObject

from .models import RegistrationPeriod


def current_period(request):
    """`current_period`: đợt mới nhất (hoặc None). Chỉ truy vấn khi template dùng tới."""
    return {"current_period": SimpleLazyObject(lambda: RegistrationPeriod.objects.order_by("-start_at", "-id").first())}


def assets(request):
    """`assets_cdn`: True → template nạp Bootstrap/Chart.js từ CDN kèm dự phòng bản trong dự án."""
    return {"assets_cdn": settings.ASSETS_FROM_CDN}
