"""Bộ lọc template V3.7 (tách lý do gợi ý thành ý đánh số, chuỗi "a, b" thành thẻ). Dùng: {% load atlas_tags %}."""

import re

from django import template

register = template.Library()


@register.filter
def reason_points(text, limit=4):
    """ "Phù hợp vì a, b, c. Cần bổ sung: X" → ["A", "B", "C", "Cần bổ sung: X"] (khối "Lý do gợi ý", ảnh duyệt 11)."""
    points = []
    for sentence in re.split(r"(?<=[.!?])\s+", (text or "").strip()):
        sentence = sentence.strip().rstrip(".")
        if not sentence:
            continue
        if sentence.startswith("Phù hợp vì "):
            points += [p.strip() for p in sentence[len("Phù hợp vì ") :].split(", ") if p.strip()]
        else:
            points.append(sentence)
    return [p[0].upper() + p[1:] for p in points][: int(limit)]


@register.filter
def csv_items(text, limit=6):
    """ "Flutter, Firebase; REST" → ["Flutter", "Firebase", "REST"] — thẻ công nghệ / từ khoá từ dữ liệu thật."""
    return [p.strip() for p in re.split(r"[,;\n]", text or "") if p.strip()][: int(limit)]
