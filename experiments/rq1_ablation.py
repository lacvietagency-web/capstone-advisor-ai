"""Thực nghiệm RQ1: Nghiên cứu cắt bỏ thành phần (Ablation Study) cho hệ thống gợi ý.

Mục tiêu:
Đánh giá đóng góp của từng thành phần gợi ý (M1 kỹ năng, M3 lĩnh vực,
M4 ngữ nghĩa, M5 LLM) trên tập dữ liệu mô phỏng có nhãn giả.

Nhãn giả (Pseudo Ground Truth):
Đề tài được xem là phù hợp với sinh viên nếu thỏa mãn đồng thời:
1. Đề tài thuộc ít nhất một trong các lĩnh vực mà sinh viên quan tâm nhất.
2. Sinh viên đáp ứng >= 70% kỹ năng đề tài yêu cầu (điểm M1 >= 70.0).

LƯU Ý: Nhãn giả chỉ dùng để kiểm thử quy trình thực nghiệm kỹ thuật;
nhãn thật trong thực tế được thu thập từ khảo sát và phản hồi của giảng viên hướng dẫn.

Các cấu hình đánh giá:
1. Đủ M1–M5 (Full model): w = (0.25, 0.20, 0.15, 0.20, 0.20)
2. Bỏ M1 (No skill): w1 = 0
4. Bỏ M3 (No field): w3 = 0
5. Bỏ M4 (No semantic): w4 = 0
6. Bỏ M5 (No LLM): w5 = 0
7. TF-IDF only: chỉ xếp hạng theo độ tương đồng TF-IDF cosine giữa giới thiệu SV và đề tài
8. Embedding only: chỉ xếp hạng theo độ tương đồng cosine vector MiniLM (M4)
9. Trọng số đều (Equal weights): w = (0.20, 0.20, 0.20, 0.20, 0.20)

Chỉ số đo lường:
- Hit@5: Tỷ lệ sinh viên có ít nhất 1 đề tài phù hợp trong Top 5.
- MRR: Nghịch giá trị thứ hạng đề tài phù hợp đầu tiên (Mean Reciprocal Rank).
- NDCG@5: Điểm tích lũy chiết khấu chuẩn hóa tại vị trí 5 (Normalized Discounted Cumulative Gain).
"""

import argparse
import csv
import os
import time
from pathlib import Path

import django
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Thiết lập môi trường Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.core.management import call_command  # noqa: E402

from catalog.models import Student, Topic  # noqa: E402
from experiments.metrics import compute_hit_at_k, compute_mrr, compute_ndcg_at_k  # noqa: E402
from recommend.engine import (  # noqa: E402
    DEFAULT_WEIGHTS,
    Profile,
    SemanticModel,
    eligible,
    m1_skill,
    m3_field,
    m4_semantic,
)
from recommend.llm import batch_score_llm, get_cache_key  # noqa: E402
from recommend.models import LLMScore  # noqa: E402

RESULTS_DIR = Path(__file__).resolve().parent / "results"

DEFAULT_CONFIGS = [
    ("Đủ M1,M3,M4,M5", {"skill": 0.42, "field": 0.12, "semantic": 0.23, "llm": 0.23}),
    ("Bỏ M1 (Kỹ năng)", {"skill": 0.0, "field": 0.12, "semantic": 0.23, "llm": 0.23}),
    ("Bỏ M3 (Lĩnh vực)", {"skill": 0.42, "field": 0.0, "semantic": 0.23, "llm": 0.23}),
    ("Bỏ M4 (Embedding)", {"skill": 0.42, "field": 0.12, "semantic": 0.0, "llm": 0.23}),
    ("Bỏ M5 (LLM)", {"skill": 0.42, "field": 0.12, "semantic": 0.23, "llm": 0.0}),
    ("Trọng số đều", {"skill": 0.25, "field": 0.25, "semantic": 0.25, "llm": 0.25}),
]


def ensure_dataset(min_students: int = 50) -> None:
    """Kiểm tra và khởi tạo dữ liệu mô phỏng nếu cơ sở dữ liệu chưa có đủ dữ liệu."""
    if Student.objects.count() < min_students or Topic.objects.count() < 20:
        print("Dữ liệu hiện tại chưa đủ, tiến hành chạy seed_demo (100 SV, 15 GV, 50 đề tài)...")
        call_command("seed_demo", students=100, lecturers=15, topics=50, seed=42, verbosity=0)


def get_pseudo_ground_truth(profile: Profile, topics: list[Topic]) -> set[int]:
    """Xác định tập đề tài liên quan giả định cho sinh viên theo tiêu chí đề bài.

    Điều kiện:
        Rel(s) = { t | (fields(t) giao TopInterests(s) != rong) và M1(s, t) >= 70.0 }
    """
    if not profile.interests:
        return set()
    max_level = max(profile.interests.values())
    top_fields = {fid for fid, level in profile.interests.items() if level == max_level and level > 0}

    relevant_ids = set()
    for topic in topics:
        topic_fields = {f.id for f in topic.fields.all()}
        if not (topic_fields & top_fields):
            continue
        skill_score, _ = m1_skill(profile, topic)
        if skill_score >= 70.0:
            relevant_ids.add(topic.id)
    return relevant_ids


def compute_tfidf_matrix(students: list[Student], topics: list[Topic]):
    """Huấn luyện mô hình TF-IDF và tính vector đặc trưng cho sinh viên và đề tài."""
    topic_texts = [f"{t.title}. {t.description}" for t in topics]
    student_texts = [s.about if s.about.strip() else "Công nghệ thông tin" for s in students]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    vectorizer.fit(topic_texts + student_texts)
    topic_vecs = vectorizer.transform(topic_texts).toarray()
    student_vecs = vectorizer.transform(student_texts).toarray()
    return topic_vecs, student_vecs


def compute_student_candidate_scores(
    student: Student,
    topics: list[Topic],
    topic_idx_map: dict[int, int],
    tfidf_topic_vecs: np.ndarray,
    tfidf_student_vec: np.ndarray,
) -> list[dict]:
    """Tính toán trước các điểm thành phần M1-M5 và TF-IDF cho các đề tài đủ điều kiện của sinh viên."""
    profile = Profile(student)
    student_vec = SemanticModel.encode([student.about])[0] if student.about.strip() else None
    topic_vecs = SemanticModel.topic_vectors(topics) if student_vec is not None else []

    candidate_records = []

    for idx, topic in enumerate(topics):
        is_ok, _ = eligible(profile, topic)
        if not is_ok:
            continue
        s1, _ = m1_skill(profile, topic)
        s3 = m3_field(profile, topic)
        s4 = m4_semantic(student_vec, topic_vecs[idx]) if student_vec is not None else 0.0
        s5 = None  # M5 điền sau, chỉ cho Top-K giống hệ thống thật

        t_idx = topic_idx_map[topic.id]
        cos_sim = float(np.dot(tfidf_student_vec, tfidf_topic_vecs[t_idx]))
        s_tfidf = 100.0 * max(0.0, cos_sim)

        candidate_records.append(
            {
                "topic_id": topic.id,
                "scores": {"skill": s1, "field": s3, "semantic": s4, "llm": s5},
                "tfidf": s_tfidf,
                "embedding": s4,
            }
        )
    _fill_llm_top_k(student, candidate_records, {t.id: t for t in topics})
    return candidate_records


def _fill_llm_top_k(student, records, topics_by_id, k=15):
    """M5 THẬT (LLM theo settings.LLM_PROVIDER, có cache LLMScore) cho Top-K theo M1–M4 — đúng quy trình 2 giai đoạn.
    Đề tài ngoài Top-K hoặc LLM lỗi → M5 = None, điểm cuối tự chia lại trọng số trên M1–M4."""
    stage1 = {k_: v for k_, v in DEFAULT_WEIGHTS.items() if k_ != "llm"}
    top = sorted(records, key=lambda r: _weighted(r["scores"], stage1), reverse=True)[:k]
    pace = float(os.getenv("LLM_PACE", "60"))  # Groq miễn phí: 8.000 token/phút ≈ 1 lượt chấm 15 đề tài/phút
    topics = [topics_by_id[r["topic_id"]] for r in top]
    keys = [get_cache_key(student, t) for t in topics]
    for _attempt in range(3):
        all_cached = LLMScore.objects.filter(cache_key__in=keys).count() == len(keys)
        scored, _invalid = batch_score_llm(student, topics)
        if not all_cached:
            time.sleep(pace)  # vừa gọi mạng (thành công hay 429) → nghỉ cho đủ hạn mức/phút
        if len(scored) + len(_invalid) >= len(top) or all_cached:
            break  # đủ kết quả (điểm sai rubric không chấm lại)
    for r in top:
        if r["topic_id"] in scored:
            r["scores"]["llm"] = scored[r["topic_id"]].total


def _weighted(scores, weights):
    """Trung bình có trọng số, bỏ thành phần không có điểm (None) và chia lại trọng số."""
    active = {k: w for k, w in weights.items() if w > 0 and scores.get(k) is not None}
    total = sum(active.values())
    return sum(scores[k] * w for k, w in active.items()) / total if total else 0.0


def rank_candidates(candidates: list[dict], mode: str, weights: dict | None = None) -> list[int]:
    """Xếp hạng đề tài theo từng cấu hình ablation cụ thể.

    Công thức kết hợp có trọng số:
        Score = sum(w_i * s_i) / sum(w_i) với w_i > 0
    """
    if mode == "tfidf":
        sorted_cands = sorted(candidates, key=lambda c: c["tfidf"], reverse=True)
    elif mode == "embedding":
        sorted_cands = sorted(candidates, key=lambda c: c["embedding"], reverse=True)
    else:
        assert weights is not None

        sorted_cands = sorted(candidates, key=lambda c: _weighted(c["scores"], weights), reverse=True)

    return [c["topic_id"] for c in sorted_cands]


def evaluate_ablation_system(
    students: list[Student],
    topics: list[Topic],
    configs: list[tuple[str, dict]],
) -> list[dict]:
    """Thực hiện đánh giá toàn bộ các cấu hình thực nghiệm trên tập sinh viên."""
    topic_idx_map = {t.id: i for i, t in enumerate(topics)}
    tfidf_topic_vecs, tfidf_student_vecs = compute_tfidf_matrix(students, topics)

    eval_data = []
    for s_idx, student in enumerate(students):
        profile = Profile(student)
        gt = get_pseudo_ground_truth(profile, topics)
        if not gt:
            continue
        cands = compute_student_candidate_scores(
            student, topics, topic_idx_map, tfidf_topic_vecs, tfidf_student_vecs[s_idx]
        )
        if not cands:
            continue
        eval_data.append((student, gt, cands))

    print(f"Tổng số sinh viên đánh giá hợp lệ (có nhãn giả & ứng viên): {len(eval_data)} / {len(students)}")
    with_m5 = sum(1 for _, _, cands in eval_data if any(c["scores"]["llm"] is not None for c in cands))
    coverage = f"{with_m5}/{len(eval_data)} SV có điểm M5 thật từ LLM; còn lại M5 trống (LLM lỗi/hết hạn mức)"
    print("Độ phủ M5:", coverage)
    (RESULTS_DIR / "rq1_m5_coverage.txt").write_text(coverage + "\n", encoding="utf-8")
    results = []

    # 1. Đánh giá các cấu hình trọng số M1-M5
    for name, weights in configs:
        hits, mrrs, ndcgs = [], [], []
        for _student, gt, cands in eval_data:
            ranked = rank_candidates(cands, mode="weights", weights=weights)
            hits.append(compute_hit_at_k(ranked, gt, k=5))
            mrrs.append(compute_mrr(ranked, gt))
            ndcgs.append(compute_ndcg_at_k(ranked, gt, k=5))
        results.append(
            {
                "Configuration": name,
                "Hit@5": float(np.mean(hits)),
                "MRR": float(np.mean(mrrs)),
                "NDCG@5": float(np.mean(ndcgs)),
            }
        )

    # 2. Đánh giá TF-IDF only
    hits_tf, mrrs_tf, ndcgs_tf = [], [], []
    for _student, gt, cands in eval_data:
        ranked = rank_candidates(cands, mode="tfidf")
        hits_tf.append(compute_hit_at_k(ranked, gt, k=5))
        mrrs_tf.append(compute_mrr(ranked, gt))
        ndcgs_tf.append(compute_ndcg_at_k(ranked, gt, k=5))
    results.append(
        {
            "Configuration": "TF-IDF only",
            "Hit@5": float(np.mean(hits_tf)),
            "MRR": float(np.mean(mrrs_tf)),
            "NDCG@5": float(np.mean(ndcgs_tf)),
        }
    )

    # 3. Đánh giá Embedding only
    hits_emb, mrrs_emb, ndcgs_emb = [], [], []
    for _student, gt, cands in eval_data:
        ranked = rank_candidates(cands, mode="embedding")
        hits_emb.append(compute_hit_at_k(ranked, gt, k=5))
        mrrs_emb.append(compute_mrr(ranked, gt))
        ndcgs_emb.append(compute_ndcg_at_k(ranked, gt, k=5))
    results.append(
        {
            "Configuration": "Embedding only",
            "Hit@5": float(np.mean(hits_emb)),
            "MRR": float(np.mean(mrrs_emb)),
            "NDCG@5": float(np.mean(ndcgs_emb)),
        }
    )

    return results


def export_results(results: list[dict], csv_path: Path, png_path: Path) -> None:
    """Lưu kết quả ra file CSV và vẽ biểu đồ cột so sánh bằng Matplotlib."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    # Ghi CSV
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Configuration", "Hit@5", "MRR", "NDCG@5"])
        writer.writeheader()
        for r in results:
            writer.writerow(
                {
                    "Configuration": r["Configuration"],
                    "Hit@5": f"{r['Hit@5']:.4f}",
                    "MRR": f"{r['MRR']:.4f}",
                    "NDCG@5": f"{r['NDCG@5']:.4f}",
                }
            )
    print(f"Đã lưu kết quả CSV: {csv_path}")

    # Vẽ biểu đồ cột
    configs = [r["Configuration"] for r in results]
    hit_vals = [r["Hit@5"] for r in results]
    mrr_vals = [r["MRR"] for r in results]
    ndcg_vals = [r["NDCG@5"] for r in results]

    x = np.arange(len(configs))
    width = 0.25

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.bar(x - width, hit_vals, width, label="Hit@5", color="#1f77b4")
    ax.bar(x, mrr_vals, width, label="MRR", color="#2ca02c")
    ax.bar(x + width, ndcg_vals, width, label="NDCG@5", color="#ff7f0e")

    ax.set_title("RQ1: Nghiên cứu cắt bỏ thành phần gợi ý đề tài (Ablation Study)", fontsize=14, fontweight="bold")
    ax.set_ylabel("Điểm số (0.0 – 1.0)", fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(configs, rotation=30, ha="right", fontsize=10)
    ax.set_ylim(0.0, 1.05)
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    ax.legend(fontsize=11)

    plt.tight_layout()
    plt.savefig(png_path, dpi=300)
    plt.close()
    print(f"Đã lưu biểu đồ PNG: {png_path}")


def main() -> None:
    """Hàm chính thực thi kịch bản ablation RQ1."""
    parser = argparse.ArgumentParser(description="Chạy thực nghiệm RQ1: Ablation Study")
    parser.add_argument("--students", type=int, default=100, help="Số lượng sinh viên đánh giá")
    args = parser.parse_args()

    ensure_dataset(min_students=args.students)
    students = list(Student.objects.all().prefetch_related("interests", "skills", "course_results")[: args.students])
    topics = list(Topic.objects.all().prefetch_related("fields", "skills__skill", "prerequisites"))

    print(f"Bắt đầu thực nghiệm RQ1 trên {len(students)} sinh viên và {len(topics)} đề tài...")
    results = evaluate_ablation_system(students, topics, DEFAULT_CONFIGS)

    print("\n--- KẾT QUẢ THỰC NGHIỆM RQ1 ---")
    for r in results:
        print(f"{r['Configuration']:<22} | Hit@5: {r['Hit@5']:.4f} | MRR: {r['MRR']:.4f} | NDCG@5: {r['NDCG@5']:.4f}")

    export_results(results, RESULTS_DIR / "rq1_ablation.csv", RESULTS_DIR / "rq1_ablation.png")


if __name__ == "__main__":
    main()
