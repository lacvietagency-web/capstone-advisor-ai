"""Phát hiện đề tài trùng/giống và tư vấn — theo ý kiến GVHD 22/10/2026.

Hai việc, cùng một lõi là độ gần nghĩa Sentence-BERT (cosine của vector đã chuẩn hoá):
1. `similar_open_topics`  — đề tài mới của GV có trùng/gần trùng đề tài nào ĐANG MỞ không → tư vấn phân biệt.
2. `archived_advice`      — đề tài có giống đề tài KHOÁ TRƯỚC không → tư vấn cải tiến (LLM, có bản dự phòng).
"""

from recommend.engine import SemanticModel

DUP_THRESHOLD = 0.75  # cosine ≥ 0.75: coi là trùng/gần trùng đề tài đang mở
ARCHIVE_THRESHOLD = 0.70  # cosine ≥ 0.70: giống đề tài khoá trước, đáng tư vấn cải tiến


def _topic_text(t):
    return f"{t.title}. {t.description}"


def similar_open_topics(topic, others, threshold=DUP_THRESHOLD, limit=5):
    """[(đề tài, độ giống 0..1)] trong `others` (đang mở, bỏ chính nó) có cosine ≥ threshold, cao nhất trước."""
    others = [o for o in others if o.pk != topic.pk]
    if not others:
        return []
    vecs = SemanticModel.topic_vectors([topic, *others])
    tv = vecs[0]
    sims = [(o, float(tv @ ov)) for o, ov in zip(others, vecs[1:], strict=True)]
    return sorted([(o, s) for o, s in sims if s >= threshold], key=lambda x: -x[1])[:limit]


def similar_archived(topic, archived, threshold=ARCHIVE_THRESHOLD, limit=3):
    """Trả [(đề tài khoá trước, độ giống)] giống đề tài hiện tại, cao nhất trước."""
    archived = list(archived)
    if not archived:
        return []
    tv = SemanticModel.topic_vectors([topic])[0]
    av = SemanticModel.text_vectors([(f"arch{a.id}", _topic_text(a)) for a in archived])
    sims = [(a, float(tv @ v)) for a, v in zip(archived, av, strict=True)]
    return sorted([(a, s) for a, s in sims if s >= threshold], key=lambda x: -x[1])[:limit]


def improvement_advice(topic, matches):
    """Gợi ý cải tiến so với đề tài khoá trước. `matches` = kết quả similar_archived.
    Trả {"llm": <văn bản hoặc None>, "points": [gợi ý heuristic]} — template ưu tiên LLM, thiếu thì dùng heuristic."""
    if not matches:
        return None
    best, score = matches[0]
    points = _heuristic_points(topic, best)
    return {"match": best, "score": score, "llm": _llm_advice(topic, best), "points": points}


def _heuristic_points(topic, past):
    """Gợi ý cải tiến không cần LLM: so công nghệ và phạm vi với đề tài khoá trước."""
    out = []
    new_tech = {x.strip().lower() for x in (topic.technologies or "").replace(";", ",").split(",") if x.strip()}
    old_tech = {x.strip().lower() for x in (past.technologies or "").replace(";", ",").split(",") if x.strip()}
    if old_tech and old_tech == new_tech:
        out.append(
            "Dùng công nghệ giống hệt khoá trước — nên cập nhật công nghệ mới hơn hoặc bổ sung thành phần khác biệt."
        )
    elif old_tech - new_tech:
        out.append(
            f"Khoá trước đã dùng: {', '.join(sorted(old_tech - new_tech))} — cân nhắc kế thừa hoặc nêu rõ điểm khác."
        )
    out.append("Nêu rõ phần MỚI so với đề tài khoá trước (phạm vi, dữ liệu, thuật toán, hoặc đánh giá thực nghiệm).")
    out.append("Bổ sung so sánh định lượng với kết quả khoá trước để thể hiện mức cải tiến.")
    return out


_SYS = (
    "Bạn là giảng viên phản biện đồ án tốt nghiệp ngành CNTT. Trả lời ngắn gọn bằng tiếng Việt, "
    "tối đa 4 gạch đầu dòng, chỉ ra điểm có thể cải tiến để đề tài MỚI khác và tốt hơn đề tài khoá trước. "
    "Không khen chung chung, không bịa chi tiết ngoài thông tin được cung cấp."
)


def _llm_advice(topic, past):
    from recommend.llm import advise_text

    user = (
        f"ĐỀ TÀI MỚI:\nTên: {topic.title}\nMô tả: {topic.description}\n"
        f"Công nghệ: {topic.technologies or '(chưa ghi)'}\n\n"
        f"ĐỀ TÀI KHOÁ TRƯỚC (năm {past.year}):\nTên: {past.title}\nMô tả: {past.description}\n"
        f"Công nghệ: {past.technologies or '(không rõ)'}\n\n"
        "Hãy đề xuất hướng cải tiến để đề tài mới khác biệt và có giá trị hơn."
    )
    return advise_text(_SYS, user)


def duplicate_pairs(topics, threshold=DUP_THRESHOLD):
    """Mọi cặp đề tài gần trùng trong `topics` (cosine ≥ threshold), cao nhất trước — cho trang Khoa rà soát."""
    topics = list(topics)
    if len(topics) < 2:
        return []
    vecs = SemanticModel.topic_vectors(topics)
    pairs = []
    for i in range(len(topics)):
        for j in range(i + 1, len(topics)):
            sim = float(vecs[i] @ vecs[j])
            if sim >= threshold:
                pairs.append((topics[i], topics[j], sim))
    return sorted(pairs, key=lambda x: -x[2])
