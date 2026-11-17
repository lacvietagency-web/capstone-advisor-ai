from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .chat import answer, role_key, warm_up
from .models import ChatLog

MAX_LEN = 800
WINDOW = 600
# Hạn mức theo vai (câu / 10 phút, câu / ngày): SV đông người nhất nên hẹp nhất — giữ hạn mức API khi mở link công khai
LIMITS = {"STUDENT": (15, 60), "LECTURER": (30, 150), "ADMIN": (60, 300)}
LIMIT = LIMITS["STUDENT"][0]


@login_required
@require_POST
def ask(request):
    """POST q=<câu hỏi> (hoặc reset=1 để bắt đầu cuộc mới) → JSON {answer, sources, mode}."""
    if request.POST.get("warm"):
        warm_up()
        return JsonResponse({"ok": True})
    if request.POST.get("reset"):
        request.session["chat"] = []
        return JsonResponse({"ok": True})
    q = (request.POST.get("q") or "").strip()
    if not q:
        return JsonResponse({"error": "Bạn chưa nhập câu hỏi."}, status=400)
    if len(q) > MAX_LEN:
        return JsonResponse({"error": f"Câu hỏi tối đa {MAX_LEN} ký tự."}, status=400)
    per_window, per_day = LIMITS.get(role_key(request.user), LIMITS["STUDENT"])
    for key, limit, ttl, msg in (
        (f"chat-rate:{request.user.pk}", per_window, WINDOW, "Bạn hỏi nhanh quá, nghỉ vài phút rồi hỏi tiếp nhé."),
        (
            f"chat-day:{request.user.pk}",
            per_day,
            86400,
            f"Bạn đã dùng hết {per_day} câu hỏi hôm nay, mai hỏi tiếp nhé.",
        ),
    ):
        cache.add(key, 0, ttl)
        if cache.incr(key) > limit:
            return JsonResponse({"error": msg}, status=429)
    history = request.session.get("chat", [])
    res = answer(request.user, q, history)
    request.session["chat"] = (history + [[q, res["answer"]]])[-6:]
    ChatLog.objects.create(
        user=request.user,
        role=getattr(request.user, "role", ""),
        question=q,
        answer=res["answer"],
        sources=res["sources"],
        mode=res["mode"],
        model=res["model"][:80],
        ms=res["ms"],
    )
    return JsonResponse({k: res[k] for k in ("answer", "sources", "mode")})
