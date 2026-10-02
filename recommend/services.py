"""Tính lại gợi ý cho một sinh viên (gọi khi SV lưu hồ sơ) hoặc cho tất cả (lệnh recommend_all)."""

from django.conf import settings
from django.db import transaction

from catalog.models import Topic
from recommend.engine import DEFAULT_WEIGHTS, WEIGHTS_VERSION, explain, score_student
from recommend.models import Recommendation

MODEL_VERSION = "m1-m5-v1"


def open_topics():
    return list(
        Topic.objects.filter(status=Topic.Status.OPEN).prefetch_related(
            "skills__skill", "prerequisites__course", "fields"
        )
    )


@transaction.atomic
def refresh_student(student, topics=None, top=5, semantic=None, llm=None):
    semantic = settings.RECOMMEND_SEMANTIC if semantic is None else semantic
    llm = getattr(settings, "RECOMMEND_LLM", True) if llm is None else llm
    Recommendation.objects.filter(student=student).delete()
    cands = score_student(
        student,
        topics if topics is not None else open_topics(),
        semantic=semantic,
        llm=llm,
    )[:top]

    for rank, c in enumerate(cands, 1):
        Recommendation.objects.create(
            student=student,
            topic=c.topic,
            rank=rank,
            m1_skill=c.scores["skill"],
            m2_academic=c.scores["academic"],
            m3_field=c.scores["field"],
            m4_semantic=c.scores["semantic"],
            m5_llm=c.scores["llm"],
            final_score=c.final(DEFAULT_WEIGHTS),
            reason=explain(c),
            weights_version=WEIGHTS_VERSION,
            model_version=MODEL_VERSION,
        )
    return len(cands)
