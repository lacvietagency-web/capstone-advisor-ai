"""Thực nghiệm RQ3b: so sánh 4 thuật toán phân bổ — Greedy, Gale-Shapley (SPA-student), Giải thuật di truyền (GA), ILP.

Thuyết minh đề tài (mẫu 24/SV/ĐT) nêu GA hoặc Gale-Shapley; hệ thống dùng ILP.
Thực nghiệm này lập "bảng so sánh mô hình" trên CÙNG dữ liệu với RQ3 (generate_benchmark_instance, seed 42;
100 / 300 / 1.000 SV), ILP dùng bộ trọng số mặc định (α = 0,4; β = 0,6).
GA chạy 5 hạt giống ngẫu nhiên, báo trung bình ± độ lệch chuẩn.

Chỉ số: tỷ lệ xếp, đạt NV1, thứ hạng NV TB, điểm phù hợp TB và P10, vi phạm ràng buộc, SỐ CẶP CHẶN (độ ổn định theo
Abraham và cộng sự, 2007; GV ưu tiên SV có điểm phù hợp cao hơn), ĐỘ LỆCH TẢI GV,
giá trị hàm mục tiêu của ILP, thời gian.

    python experiments/rq3b_four_algorithms.py [--scales 100,300,1000] [--ga-seeds 5]
"""

import argparse
import csv
import os
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django  # noqa: E402

django.setup()

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from allocate.solver import compute_utility, metrics, solve_greedy, solve_ilp  # noqa: E402
from experiments.baselines import blocking_pairs, load_spread, solve_gale_shapley, solve_genetic  # noqa: E402
from experiments.rq3_allocation import generate_benchmark_instance  # noqa: E402

RESULTS = Path(__file__).resolve().parent / "results"
ALPHA, BETA, EPS = 0.4, 0.6, 1e-3
KEYS = [
    "assigned_rate",
    "nv1_rate",
    "mean_rank",
    "avg_match",
    "p10_match",
    "quota_violations",
    "blocking_pairs",
    "load_spread",
    "objective",
    "runtime_seconds",
]


def objective(assign, prefs, scores, gpa):
    """Giá trị hàm mục tiêu ILP: Σ U(s, t) − λ·(số SV chưa xếp), λ = 1 + n(α + β + ε)."""
    lam = 1.0 + len(prefs) * (ALPHA + BETA + EPS)
    total = 0.0
    for s, t in assign.items():
        if t is None:
            total -= lam
        else:
            total += compute_utility(s, t, prefs[s].index(t) + 1, scores, gpa, ALPHA, BETA, EPS)
    return total


def evaluate(assign, inst, seconds):
    prefs, scores, cap, owner, quota, gpa = inst
    m = metrics(assign, prefs, scores, cap, owner, quota)
    m["blocking_pairs"] = blocking_pairs(assign, prefs, scores, cap, owner, quota, gpa)
    m["load_spread"] = load_spread(assign, owner, quota)
    m["objective"] = objective(assign, prefs, scores, gpa)
    m["runtime_seconds"] = seconds
    return m


def timed(fn, *a, **k):
    t0 = time.perf_counter()
    out = fn(*a, **k)
    return out, time.perf_counter() - t0


def run(scales, ga_seeds):
    rows = []
    for n in scales:
        inst = generate_benchmark_instance(n, seed=42)
        print(f"\n== N = {n}")
        for name, fn, kw in [
            ("Greedy", solve_greedy, {}),
            ("Gale-Shapley (SPA-student)", solve_gale_shapley, {}),
            ("ILP (α=0,4; β=0,6)", solve_ilp, {"alpha": ALPHA, "beta": BETA}),
        ]:
            a, sec = timed(fn, *inst, **kw)
            m = evaluate(a, inst, sec)
            rows.append({"Scale_N": n, "Algorithm": name, "Runs": 1, **m, **{k + "_sd": 0.0 for k in KEYS}})
            print(
                f"  {name:28} xếp {m['assigned_rate']:.1%} NV1 {m['nv1_rate']:.1%} điểm {m['avg_match']:.1f} "
                f"chặn {m['blocking_pairs']} {sec:.3f}s"
            )
        runs = []
        for seed in range(ga_seeds):
            a, sec = timed(solve_genetic, *inst, alpha=ALPHA, beta=BETA, seed=seed)
            runs.append(evaluate(a, inst, sec))
        mean = {k: statistics.mean(r[k] for r in runs) for k in KEYS}
        sd = {k + "_sd": (statistics.stdev(r[k] for r in runs) if len(runs) > 1 else 0.0) for k in KEYS}
        rows.append({"Scale_N": n, "Algorithm": "GA (di truyền)", "Runs": ga_seeds, **mean, **sd})
        print(
            f"  {'GA (di truyền)':28} xếp {mean['assigned_rate']:.1%}±{sd['assigned_rate_sd']:.1%} "
            f"NV1 {mean['nv1_rate']:.1%} điểm {mean['avg_match']:.1f} "
            f"chặn {mean['blocking_pairs']:.0f} {mean['runtime_seconds']:.1f}s"
        )
    return rows


def export(rows):
    RESULTS.mkdir(parents=True, exist_ok=True)
    fields = ["Scale_N", "Algorithm", "Runs"] + KEYS + [k + "_sd" for k in KEYS]
    with open(RESULTS / "rq3b_four_algorithms.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{r[k]:.4f}" if isinstance(r[k], float) else r[k]) for k in fields})

    head = [
        "N",
        "Thuật toán",
        "Tỷ lệ xếp",
        "Đạt NV1",
        "Thứ hạng NV TB",
        "Điểm phù hợp TB",
        "P10",
        "Vi phạm",
        "Cặp chặn",
        "Lệch tải GV",
        "Hàm mục tiêu",
        "Thời gian (s)",
    ]
    md = ["| " + " | ".join(head) + " |", "| ---: | :--- |" + " ---: |" * (len(head) - 2)]

    def pm(r, k, fmt):  # GA chạy nhiều lần → kèm độ lệch chuẩn
        return fmt.format(r[k]) + (" ± " + fmt.format(r[k + "_sd"]) if r["Runs"] > 1 else "")

    for r in rows:
        cells = [
            r["Scale_N"],
            r["Algorithm"],
            pm(r, "assigned_rate", "{:.1%}"),
            pm(r, "nv1_rate", "{:.1%}"),
            f"{r['mean_rank']:.2f}",
            f"{r['avg_match']:.1f}",
            f"{r['p10_match']:.1f}",
            f"{r['quota_violations']:.0f}",
            pm(r, "blocking_pairs", "{:.0f}"),
            f"{r['load_spread']:.2f}",
            f"{r['objective']:.1f}",
            pm(r, "runtime_seconds", "{:.3f}"),
        ]
        md.append("| " + " | ".join(str(c) for c in cells) + " |")
    (RESULTS / "rq3b_four_algorithms.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    algs = list(dict.fromkeys(r["Algorithm"] for r in rows))
    scales = sorted({r["Scale_N"] for r in rows})
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    panels = [
        (axes[0], "nv1_rate", "Đạt nguyện vọng 1"),
        (axes[1], "blocking_pairs", "Số cặp chặn (0 = ổn định)"),
        (axes[2], "runtime_seconds", "Thời gian giải (giây, thang log)"),
    ]
    for ax, key, title in panels:
        width = 0.8 / len(algs)
        for i, alg in enumerate(algs):
            vals = [next(r[key] for r in rows if r["Algorithm"] == alg and r["Scale_N"] == n) for n in scales]
            heights = [v * 100 if key == "nv1_rate" else v for v in vals]
            ax.bar([j + i * width for j in range(len(scales))], heights, width, label=alg)
        ax.set_xticks([j + 0.4 - width / 2 for j in range(len(scales))], [f"N={n}" for n in scales])
        ax.set_title(title)
        if key == "runtime_seconds":
            ax.set_yscale("log")
        if key == "nv1_rate":
            ax.set_ylabel("%")
    axes[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(RESULTS / "rq3b_four_algorithms.png", dpi=150)
    print(f"\nĐã ghi {RESULTS / 'rq3b_four_algorithms.csv'}, .md, .png")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--scales", default="100,300,1000")
    ap.add_argument("--ga-seeds", type=int, default=5)
    a = ap.parse_args()
    export(run([int(x) for x in a.scales.split(",")], a.ga_seeds))
