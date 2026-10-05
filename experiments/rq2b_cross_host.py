"""RQ2b: cùng model gpt-oss-120b nhưng chạy ở 2 nhà cung cấp khác nhau có cho cùng điểm M5 không?

    python -m experiments.rq2b_cross_host

So các cặp (SV, đề tài) đã được chấm bởi cả hai (lấy từ cache LLMScore, không gọi API): MAE và Spearman.
"""

import csv
import os
import statistics
from pathlib import Path

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from scipy.stats import spearmanr  # noqa: E402

from recommend.models import LLMScore  # noqa: E402

A, B = "openai/gpt-oss-120b", "gptoss120"  # Groq trực tiếp / combo OmniRoute (Tinfoil)
OUT = Path(__file__).resolve().parent / "results" / "rq2b_cross_host.csv"


def main():
    a = {(s.student_id, s.topic_id): float(s.score_json["total"]) for s in LLMScore.objects.filter(model=A)}
    b = {(s.student_id, s.topic_id): float(s.score_json["total"]) for s in LLMScore.objects.filter(model=B)}
    pairs = sorted(set(a) & set(b))
    ya, yb = [a[p] for p in pairs], [b[p] for p in pairs]
    mae = statistics.mean(abs(x - y) for x, y in zip(ya, yb, strict=True)) if pairs else 0.0
    rho = spearmanr(ya, yb).statistic if len(pairs) > 2 else float("nan")
    n_sv = len({p[0] for p in pairs})
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Host_A", "Host_B", "Num_Pairs", "Num_Students", "MAE", "Spearman"])
        w.writerow([f"Groq ({A})", f"OmniRoute/Tinfoil ({B})", len(pairs), n_sv, f"{mae:.2f}", f"{rho:.3f}"])
    print(f"{len(pairs)} cặp / {n_sv} SV — MAE {mae:.2f}, Spearman {rho:.3f} → {OUT}")


if __name__ == "__main__":
    main()
