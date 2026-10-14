"""Biến dùng chung cho mọi template: bộ trọng số AHP đang áp dụng (để giải thích điểm M1–M5)."""

from django.utils.functional import SimpleLazyObject

from recommend.engine import get_active_weights, get_active_weights_version

CRITERIA = [
    ("skill", "M1", "Kỹ năng"),
    ("academic", "M2", "Học lực"),
    ("field", "M3", "Lĩnh vực"),
    ("semantic", "M4", "Ngữ nghĩa"),
    ("llm", "M5", "Đánh giá LLM"),
]


def _ahp():
    weights = get_active_weights()
    return {
        "version": get_active_weights_version(),
        "criteria": [
            {
                "key": key,
                "code": code,
                "label": label,
                "percent": round(100 * weights.get(key, 0)),
                "ratio": round(weights.get(key, 0), 2),
            }
            for key, code, label in CRITERIA
        ],
    }


def ahp(request):
    """`ahp.version` và `ahp.criteria` (mã, nhãn, %, ratio dạng 0,25) — chỉ truy vấn CSDL khi template dùng."""
    return {"ahp": SimpleLazyObject(_ahp)}
