from django.apps import AppConfig


def _danh_dau_vua_dang_nhap(sender, request, user, **kwargs):
    """Đánh dấu phiên vừa đăng nhập → trang chủ GV hiện popup "SV chờ duyệt" đúng một lần (chốt 18/11/2026)."""
    if request is not None and hasattr(request, "session"):
        request.session["vua_dang_nhap"] = True


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        from django.contrib.auth.signals import user_logged_in

        user_logged_in.connect(_danh_dau_vua_dang_nhap, dispatch_uid="capstone-popup-dang-nhap")
