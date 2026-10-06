"""Mô-đun tính toán các chỉ số đo lường đánh giá chất lượng và độ ổn định.

Bao gồm:
- Hit@K, MRR, NDCG@K: Đánh giá chất lượng xếp hạng gợi ý đề tài (Information Retrieval).
- MAE, Spearman Rank Correlation: Đánh giá độ ổn định và tính nhất quán của điểm số LLM.
"""

import math

import numpy as np
from scipy.stats import spearmanr


def compute_hit_at_k(ranked_ids: list[int], relevant_ids: set[int], k: int = 5) -> float:
    """Tính chỉ số Hit@K (tỷ lệ có ít nhất một đề tài phù hợp nằm trong Top K).

    Công thức:
        Hit@K = 1.0 nếu tồn tại đề tài t trong ranked[:k] sao cho t thuộc relevant_ids,
                ngược lại bằng 0.0.
    """
    if not relevant_ids:
        return 0.0
    for topic_id in ranked_ids[:k]:
        if topic_id in relevant_ids:
            return 1.0
    return 0.0


def compute_mrr(ranked_ids: list[int], relevant_ids: set[int]) -> float:
    """Tính chỉ số Mean Reciprocal Rank (MRR) — nghịch giá trị thứ hạng đề tài phù hợp đầu tiên.

    Công thức:
        RR = 1 / rank_first
        với rank_first là vị trí (bắt đầu từ 1) của đề tài phù hợp đầu tiên trong danh sách xếp hạng.
        Nếu không có đề tài phù hợp nào trong danh sách: RR = 0.0.
    """
    if not relevant_ids:
        return 0.0
    for idx, topic_id in enumerate(ranked_ids, start=1):
        if topic_id in relevant_ids:
            return 1.0 / idx
    return 0.0


def compute_ndcg_at_k(ranked_ids: list[int], relevant_ids: set[int], k: int = 5) -> float:
    """Tính chỉ số Normalized Discounted Cumulative Gain tại vị trí K (NDCG@K).

    Công thức:
        DCG@K = sum_{i=1}^{min(K, |ranked|)} (rel_i / log2(i + 1))
        IDCG@K = sum_{i=1}^{min(K, |relevant|)} (1 / log2(i + 1))
        NDCG@K = DCG@K / IDCG@K (nếu IDCG@K > 0, ngược lại bằng 0.0).
        Ở đây rel_i in {0, 1} là độ liên quan nhị phân.
    """
    if not relevant_ids:
        return 0.0

    dcg = 0.0
    for idx, topic_id in enumerate(ranked_ids[:k], start=1):
        if topic_id in relevant_ids:
            dcg += 1.0 / math.log2(idx + 1)

    ideal_count = min(k, len(relevant_ids))
    if ideal_count == 0:
        return 0.0

    idcg = sum(1.0 / math.log2(idx + 1) for idx in range(1, ideal_count + 1))
    return dcg / idcg if idcg > 0 else 0.0


def compute_mae(y_true: list[float], y_pred: list[float]) -> float:
    """Tính sai số tuyệt đối trung bình (Mean Absolute Error - MAE).

    Công thức:
        MAE = (1 / N) * sum_{i=1}^N |y_true[i] - y_pred[i]|
    """
    if not y_true or len(y_true) != len(y_pred):
        return 0.0
    return float(np.mean(np.abs(np.array(y_true) - np.array(y_pred))))


def compute_spearman(y1: list[float], y2: list[float]) -> float:
    """Tính hệ số tương quan thứ hạng Spearman giữa hai dãy điểm.

    Công thức:
        rho = 1 - (6 * sum(d_i^2)) / (n * (n^2 - 1))
        với d_i là độ chênh lệch thứ hạng của phần tử thứ i giữa hai lần chấm.
        Nếu tất cả các giá trị bằng nhau hoàn toàn ở cả hai dãy: rho = 1.0.
    """
    if len(y1) < 2 or len(y1) != len(y2):
        return 1.0
    if y1 == y2:
        return 1.0
    res = spearmanr(y1, y2)
    stat = getattr(res, "statistic", getattr(res, "correlation", None))
    if stat is None or np.isnan(stat):
        return 1.0 if np.allclose(y1, y2) else 0.0
    return float(stat)
