"""Thực nghiệm RQ3: So sánh hiệu năng và chất lượng giữa thuật toán Greedy và ILP.

Mục tiêu:
Đánh giá thuật toán Quy hoạch nguyên tuyến tính (ILP) và thuật toán tham lam (Greedy)
trên các quy mô sinh viên khác nhau (100, 300, 1000 sinh viên) với dữ liệu mô phỏng theo
quy luật seed_demo (phân phối nguyện vọng lũy thừa, độ cạnh tranh cao).

Các cấu hình tham số thỏa dụng U(s, t) = alpha * (score / 100) + beta * Bonus(rank) + eps * (gpa / 4):
1. Bộ 1 (Ưu tiên điểm phù hợp AI): alpha = 0.7, beta = 0.3
2. Bộ 2 (Cân bằng / Chuẩn hệ thống): alpha = 0.4, beta = 0.6
3. Bộ 3 (Ưu tiên nguyện vọng SV): alpha = 0.2, beta = 0.8

So sánh thuật toán:
- Greedy: Sắp xếp SV theo điểm cao nhất của NV (hòa điểm xét GPA), gán lần lượt NV1 -> NV2 -> NV3.
- ILP (PuLP/CBC): Tối ưu hóa hàm mục tiêu toàn cục, ưu tiên tối đa số lượng SV được xếp (lam = 2.0).

Chỉ số đánh giá:
- assigned_rate: Tỷ lệ sinh viên được xếp thành công (%)
- nv1_rate: Tỷ lệ sinh viên đạt nguyện vọng 1 (%)
- top3_rate: Tỷ lệ sinh viên đạt một trong 3 nguyện vọng (%)
- mean_rank: Thứ hạng nguyện vọng trung bình (1.0 đến 3.0)
- avg_match: Điểm phù hợp trung bình (0 đến 100)
- p10_match: Phân vị thứ 10 điểm phù hợp (đo tính công bằng)
- quota_violations: Số lượng vi phạm chỉ tiêu GV và sức chứa đề tài (phải = 0)
- runtime_seconds: Thời gian giải bài toán (giây)
"""

import argparse
import csv
import os
import random
import time
from pathlib import Path

import django
import matplotlib.pyplot as plt
import numpy as np

# Thiết lập môi trường Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from allocate.solver import metrics, solve_greedy, solve_ilp  # noqa: E402

RESULTS_DIR = Path(__file__).resolve().parent / "results"

ALPHA_BETA_SETS = [
    ("Bộ 1 (Ưu tiên điểm phù hợp)", 0.7, 0.3),
    ("Bộ 2 (Cân bằng mặc định)", 0.4, 0.6),
    ("Bộ 3 (Ưu tiên nguyện vọng)", 0.2, 0.8),
]


def generate_benchmark_instance(num_students: int, seed: int = 42) -> tuple[dict, dict, dict, dict, dict, dict]:
    """Sinh bộ dữ liệu phân công quy mô lớn mô phỏng đúng đặc tả của seed_demo.

    Đặc điểm:
    - Khoảng 20% đề tài 'hot' nhận ~80% nguyện vọng 1 theo luật lũy thừa: hotness[k] = 1 / (k + 1)^1.2.
    - Sức chứa đề tài: 1 hoặc 2 SV (tỷ lệ 2:1).
    - Chỉ tiêu giảng viên: ngẫu nhiên trong [4, 5, 6, 8].
    - Tỷ lệ: 100 SV / 15 GV / 50 đề tài (tỷ lệ 1 : 0.15 : 0.5).
    """
    rnd = random.Random(seed)
    num_lecturers = max(5, int(num_students * 0.15))
    num_topics = max(10, int(num_students * 0.50))

    quota = {g: rnd.choice([4, 5, 6, 8]) for g in range(1, num_lecturers + 1)}
    owner = {t: rnd.randint(1, num_lecturers) for t in range(1, num_topics + 1)}
    cap = {t: rnd.choice([1, 1, 2]) for t in range(1, num_topics + 1)}

    hotness = [1.0 / ((k + 1) ** 1.2) for k in range(num_topics)]
    rnd.shuffle(hotness)
    all_topics = list(range(1, num_topics + 1))

    prefs = {}
    scores = {}
    gpa = {}

    for s in range(1, num_students + 1):
        gpa[s] = round(min(4.0, max(1.5, rnd.gauss(2.8, 0.5))), 2)
        chosen = []
        while len(chosen) < 3:
            t = rnd.choices(all_topics, weights=hotness)[0]
            if t not in chosen:
                chosen.append(t)
        prefs[s] = chosen

        for rank_idx, t in enumerate(chosen, start=1):
            base_score = rnd.gauss(65.0, 15.0) - (rank_idx - 1) * 5.0
            scores[s, t] = round(min(98.0, max(25.0, base_score)), 1)

    return prefs, scores, cap, owner, quota, gpa


def run_benchmark_trial(
    prefs: dict,
    scores: dict,
    cap: dict,
    owner: dict,
    quota: dict,
    gpa: dict,
    algorithm: str,
    alpha: float = 0.4,
    beta: float = 0.6,
) -> dict:
    """Thực thi một phép thử phân công và ghi nhận thời gian cũng như các chỉ số chất lượng."""
    t0 = time.perf_counter()
    if algorithm == "GREEDY":
        assigned = solve_greedy(prefs, scores, cap, owner, quota, gpa)
    else:
        assigned = solve_ilp(prefs, scores, cap, owner, quota, gpa, alpha=alpha, beta=beta)
    elapsed = time.perf_counter() - t0

    result_metrics = metrics(assigned, prefs, scores, cap, owner, quota)
    result_metrics["runtime_seconds"] = elapsed
    return result_metrics


def run_rq3_all_experiments(scales: list[int], seed: int = 42) -> list[dict]:
    """Chạy toàn bộ ma trận thực nghiệm: 3 quy mô (100, 300, 1000 SV) x (Greedy + 3 bộ alpha/beta ILP)."""
    rows = []
    for n in scales:
        print("\n==========================================")
        print(f"Đang chạy thực nghiệm phân công quy mô N = {n} sinh viên (seed={seed})...")
        prefs, scores, cap, owner, quota, gpa = generate_benchmark_instance(n, seed=seed)

        # 1. Thuật toán Tham lam (Greedy)
        m_greedy = run_benchmark_trial(prefs, scores, cap, owner, quota, gpa, algorithm="GREEDY")
        rows.append(
            {
                "Scale_N": n,
                "Algorithm": "Greedy",
                "Alpha": "-",
                "Beta": "-",
                "Config_Name": "Greedy",
                **m_greedy,
            }
        )
        print(
            f"  [Greedy] Xếp: {m_greedy['assigned_rate']:.1%}, NV1: {m_greedy['nv1_rate']:.1%}, "
            f"Điểm TB: {m_greedy['avg_match']:.1f}, Thời gian: {m_greedy['runtime_seconds']:.4f}s"
        )

        # 2. Thuật toán ILP với 3 bộ alpha / beta
        for label, alpha, beta in ALPHA_BETA_SETS:
            m_ilp = run_benchmark_trial(prefs, scores, cap, owner, quota, gpa, algorithm="ILP", alpha=alpha, beta=beta)
            rows.append(
                {
                    "Scale_N": n,
                    "Algorithm": "ILP",
                    "Alpha": alpha,
                    "Beta": beta,
                    "Config_Name": f"ILP ({label})",
                    **m_ilp,
                }
            )
            print(
                f"  [{label}] Xếp: {m_ilp['assigned_rate']:.1%}, NV1: {m_ilp['nv1_rate']:.1%}, "
                f"Điểm TB: {m_ilp['avg_match']:.1f}, Thời gian: {m_ilp['runtime_seconds']:.4f}s"
            )

    return rows


def export_rq3_csv(rows: list[dict], csv_path: Path) -> None:
    """Lưu bảng kết quả chi tiết các kịch bản phân công ra file CSV."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "Scale_N",
        "Algorithm",
        "Alpha",
        "Beta",
        "Config_Name",
        "assigned_rate",
        "nv1_rate",
        "top3_rate",
        "mean_rank",
        "avg_match",
        "p10_match",
        "quota_violations",
        "runtime_seconds",
    ]
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(
                {
                    "Scale_N": r["Scale_N"],
                    "Algorithm": r["Algorithm"],
                    "Alpha": r["Alpha"],
                    "Beta": r["Beta"],
                    "Config_Name": r["Config_Name"],
                    "assigned_rate": f"{r['assigned_rate']:.4f}",
                    "nv1_rate": f"{r['nv1_rate']:.4f}",
                    "top3_rate": f"{r['top3_rate']:.4f}",
                    "mean_rank": f"{r['mean_rank']:.2f}",
                    "avg_match": f"{r['avg_match']:.2f}",
                    "p10_match": f"{r['p10_match']:.2f}",
                    "quota_violations": r["quota_violations"],
                    "runtime_seconds": f"{r['runtime_seconds']:.4f}",
                }
            )
    print(f"\nĐã lưu kết quả CSV: {csv_path}")


def plot_runtime_comparison(rows: list[dict], scales: list[int], png_path: Path) -> None:
    """Vẽ biểu đồ thời gian chạy so sánh giữa Greedy và ILP theo quy mô số sinh viên."""
    fig, ax = plt.subplots(figsize=(8, 5))

    greedy_times = [r["runtime_seconds"] for r in rows if r["Algorithm"] == "Greedy"]
    # Lấy thời gian trung bình của ILP qua 3 bộ tham số cho mỗi quy mô
    ilp_times = []
    for n in scales:
        t_list = [r["runtime_seconds"] for r in rows if r["Algorithm"] == "ILP" and r["Scale_N"] == n]
        ilp_times.append(float(np.mean(t_list)) if t_list else 0.0)

    ax.plot(scales, greedy_times, marker="o", linewidth=2, color="#2980b9", label="Greedy")
    ax.plot(scales, ilp_times, marker="s", linewidth=2, color="#c0392b", label="ILP (CBC Solver)")

    ax.set_title("RQ3: Thời gian chạy thuật toán phân công theo quy mô sinh viên", fontsize=12, fontweight="bold")
    ax.set_xlabel("Số lượng sinh viên (N)", fontsize=11)
    ax.set_ylabel("Thời gian chạy (giây)", fontsize=11)
    ax.set_xticks(scales)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(fontsize=11)

    plt.tight_layout()
    plt.savefig(png_path, dpi=300)
    plt.close()
    print(f"Đã lưu biểu đồ thời gian: {png_path}")


def plot_quality_metrics(rows: list[dict], scales: list[int], png_path: Path) -> None:
    """Vẽ biểu đồ so sánh chất lượng phân công (Tỷ lệ xếp, NV1, Điểm TB) giữa Greedy và ILP."""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))

    configs = [
        ("Greedy", "Greedy"),
        ("ILP (Bộ 1)", "Bộ 1"),
        ("ILP (Bộ 2)", "Bộ 2"),
        ("ILP (Bộ 3)", "Bộ 3"),
    ]
    x = np.arange(len(scales))
    width = 0.2

    for idx, (display_label, match_token) in enumerate(configs):
        if display_label == "Greedy":
            cfg_rows = [r for r in rows if r["Algorithm"] == "Greedy"]
        else:
            cfg_rows = [r for r in rows if r["Algorithm"] == "ILP" and match_token in r["Config_Name"]]

        # Sắp xếp đúng theo thứ tự scales
        cfg_rows_by_scale = {r["Scale_N"]: r for r in cfg_rows}
        ordered_rows = [cfg_rows_by_scale[n] for n in scales]

        assigned_vals = [r["assigned_rate"] * 100 for r in ordered_rows]
        nv1_vals = [r["nv1_rate"] * 100 for r in ordered_rows]
        match_vals = [r["avg_match"] for r in ordered_rows]

        offset = (idx - 1.5) * width
        ax1.bar(x + offset, assigned_vals, width, label=display_label)
        ax2.bar(x + offset, nv1_vals, width, label=display_label)
        ax3.bar(x + offset, match_vals, width, label=display_label)

    ax1.set_title("Tỷ lệ sinh viên được xếp (%)", fontsize=11, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"N={n}" for n in scales])
    ax1.set_ylabel("% Sinh viên")
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    ax2.set_title("Tỷ lệ đạt Nguyện vọng 1 (%)", fontsize=11, fontweight="bold")
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"N={n}" for n in scales])
    ax2.grid(axis="y", linestyle="--", alpha=0.5)

    ax3.set_title("Điểm phù hợp trung bình (0–100)", fontsize=11, fontweight="bold")
    ax3.set_xticks(x)
    ax3.set_xticklabels([f"N={n}" for n in scales])
    ax3.grid(axis="y", linestyle="--", alpha=0.5)
    ax3.legend(fontsize=9, loc="lower right")

    plt.suptitle("RQ3: So sánh chất lượng phân công đề tài giữa Greedy và ILP", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(png_path, dpi=300)
    plt.close()
    print(f"Đã lưu biểu đồ chất lượng: {png_path}")


def main() -> None:
    """Hàm chính thực thi kịch bản RQ3."""
    parser = argparse.ArgumentParser(description="Chạy thực nghiệm RQ3: Phân công Greedy vs ILP")
    parser.add_argument("--scales", nargs="+", type=int, default=[100, 300, 1000], help="Danh sách quy mô SV")
    parser.add_argument("--seed", type=int, default=42, help="Seed ngẫu nhiên")
    args = parser.parse_args()

    results = run_rq3_all_experiments(scales=args.scales, seed=args.seed)

    csv_out = RESULTS_DIR / "rq3_allocation.csv"
    png_time = RESULTS_DIR / "rq3_allocation_time.png"
    png_metrics = RESULTS_DIR / "rq3_allocation.png"

    export_rq3_csv(results, csv_out)
    plot_runtime_comparison(results, args.scales, png_time)
    plot_quality_metrics(results, args.scales, png_metrics)


if __name__ == "__main__":
    main()
