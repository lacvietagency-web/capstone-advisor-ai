from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .chat import answer, warm_up
from .models import ChatLog

MAX_LEN = 800
LIMIT, WINDOW = 30, 600  # 30 câu / 10 phút / người — giữ hạn mức API khi mở link công khai


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
    key = f"chat-rate:{request.user.pk}"
    cache.add(key, 0, WINDOW)
    if cache.incr(key) > LIMIT:
        return JsonResponse({"error": "Bạn hỏi nhanh quá, nghỉ vài phút rồi hỏi tiếp nhé."}, status=429)
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
