"""Thư thông báo (SV nộp NV → GV; GV duyệt → SV; Khoa công bố → SV).

Gửi tới email người dùng tự nhập ở trang Cài đặt; chưa nhập thì gửi về NOTIFY_EMAIL_TO (hộp chung của bản demo),
tiêu đề ghi người nhận thật. Không có cả hai thì bỏ qua. Lỗi SMTP không làm hỏng thao tác của người dùng.
"""

import threading

from django.conf import settings
from django.core.mail import send_mail

SEED_DOMAIN = "@sv.capstone.edu.vn"  # email giả của seed_demo: gửi thật sẽ bị trả về, coi như chưa nhập


def notify(user, subject, body):
    own = "" if user.email.endswith(SEED_DOMAIN) else user.email
    to = own or settings.NOTIFY_EMAIL_TO
    if not to:
        return
    if not own:
        subject = f"[gửi {user.get_full_name() or user.username} · {user.username}] {subject}"
    body = f"{body}\n\nXem trên hệ thống: {settings.SITE_URL}\n— Cố vấn Đồ án AI (thư tự động, không cần trả lời)"
    args = ("Cố vấn Đồ án AI: " + subject, body, None, [to])
    if settings.EMAIL_BACKEND.endswith("locmem.EmailBackend"):  # test: gửi ngay để kiểm mail.outbox
        send_mail(*args)
    else:  # ponytail: luồng nền mỗi thư, đủ cho vài chục thư/đợt; nhiều hơn thì dùng hàng đợi (Celery/cron)
        threading.Thread(target=send_mail, args=args, kwargs={"fail_silently": True}, daemon=True).start()
