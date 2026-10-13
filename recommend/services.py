"""Tính lại gợi ý cho một sinh viên (gọi khi SV lưu hồ sơ) hoặc cho tất cả (lệnh recommend_all)."""

from django.conf import settings
from django.db import transaction

from catalog.models import Preference, Topic
from recommend.engine import (
    Candidate,
    apply_stage2_llm,
    compute_stage1_candidates,
    explain,
    get_active_weights,
    get_active_weights_version,
)
from recommend.llm import score_pair
from recommend.models import Recommendation

MODEL_VERSION = "m1-m5-v1"


def open_topics():
    return list(
        Topic.objects.filter(status=Topic.Status.OPEN).prefetch_related(
            "skills__skill", "prerequisites__course", "fields"
        )
    )


def _save(student, c, rank, weights, weights_version):
    Recommendation.objects.create(
        student=student,
        topic=c.topic,
        rank=rank,
        m1_skill=c.scores["skill"],
        m2_academic=c.scores["academic"],
        m3_field=c.scores["field"],
        m4_semantic=c.scores["semantic"],
        m5_llm=c.scores["llm"],
        final_score=c.final(weights),
        reason=explain(c),
        weights_version=weights_version,
        model_version=MODEL_VERSION,
    )


def _llm_for_preferences(student, cands):
    """Nguyện vọng SV tự chọn ngoài Top-K chưa có M5 → chấm bù từng cặp (score_pair, có cache)."""
    chosen = set(Preference.objects.filter(student=student).values_list("topic_id", flat=True))
    for c in cands:
        if c.topic.id in chosen and c.scores["llm"] is None:
            res = score_pair(student, c.topic)
            if res is not None:
                c.scores["llm"] = res.total
                c.llm_reason = res.reason


def score_preferences(student):
    """Gọi sau khi SV lưu nguyện vọng: đề tài vừa chọn mà chưa có M5 thì chấm bù rồi cập nhật điểm cuối."""
    if not getattr(settings, "RECOMMEND_LLM", True):
        return
    weights = get_active_weights()
    chosen = Preference.objects.filter(student=student).values_list("topic_id", flat=True)
    for rec in Recommendation.objects.filter(student=student, topic_id__in=chosen, m5_llm__isnull=True):
        res = score_pair(student, rec.topic)
        if res is None:
            continue
        c = Candidate(
            rec.topic,
            {
                "skill": rec.m1_skill,
                "academic": rec.m2_academic,
                "field": rec.m3_field,
                "semantic": rec.m4_semantic,
                "llm": res.total,
            },
        )
        rec.m5_llm, rec.final_score = res.total, c.final(weights)
        rec.reason = f"{res.reason} {rec.reason}".strip()
        rec.save(update_fields=["m5_llm", "final_score", "reason"])


@transaction.atomic
def refresh_student(student, topics=None, top=5, semantic=None, llm=None, top_k=15):
    """Tính lại điểm phù hợp của 1 SV với MỌI đề tài đang mở mà SV đủ điều kiện.

    - M1–M4 cho tất cả đề tài đủ điều kiện (rẻ, chạy tại chỗ) → SV xem được mức phù hợp của bất kỳ đề tài nào.
    - M5 (LLM, tốn phí) chỉ cho Top-K theo M1–M4 và cho các nguyện vọng SV đã chọn.
    - top đề tài điểm cao nhất có rank 1..top (hiển thị "Top 5 gợi ý"); các đề tài còn lại lưu rank=None.
    """
    semantic = settings.RECOMMEND_SEMANTIC if semantic is None else semantic
    llm = getattr(settings, "RECOMMEND_LLM", True) if llm is None else llm
    Recommendation.objects.filter(student=student).delete()
    weights = get_active_weights()
    weights_version = get_active_weights_version()
    cands = compute_stage1_candidates(
        student, topics if topics is not None else open_topics(), weights, top_k=None, semantic=semantic
    )
    head, rest = cands[:top_k], cands[top_k:]
    if llm and head:
        head = apply_stage2_llm(student, head, weights)
    if llm:
        _llm_for_preferences(student, rest)
    for rank, c in enumerate(head[:top], 1):
        _save(student, c, rank, weights, weights_version)
    for c in head[top:] + rest:
        _save(student, c, None, weights, weights_version)
    return min(len(head), top)


def ensure_recommendations(student):
    """Bảo đảm SV đã có điểm gợi ý: dữ liệu vào từ seed/Excel/trang quản trị không tự chạy recommend_all.

    Chỉ tính M1–M4 (chạy tại chỗ, không tốn phí); M5 (LLM) vẫn được chấm khi SV lưu hồ sơ hoặc nguyện vọng.
    """
    if not Recommendation.objects.filter(student=student).exists():
        refresh_student(student, llm=False)
