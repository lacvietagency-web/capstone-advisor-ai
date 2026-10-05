"""Sinh các bảng kết quả trong experiments/README.md TỪ file CSV — không gõ tay số liệu.

    python -m experiments.make_report

Bảng nằm giữa cặp chú thích <!-- BANG:rq1 --> ... <!-- /BANG:rq1 --> (tương tự rq2, rq3).
"""

import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"


def md_table(rows, columns):
    head = "| " + " | ".join(title for title, _ in columns) + " |"
    sep = "|" + "|".join(" --- " for _ in columns) + "|"
    body = ["| " + " | ".join(fmt(r) for _, fmt in columns) + " |" for r in rows]
    return "\n".join([head, sep, *body])


def read(name):
    with open(RESULTS / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pct(key):
    return lambda r: f"{float(r[key]) * 100:.1f}%"


def num(key, nd=2):
    return lambda r: f"{float(r[key]):.{nd}f}"


TABLES = {
    "rq1": lambda: md_table(
        read("rq1_ablation.csv"),
        [
            ("Cấu hình", lambda r: r["Configuration"]),
            ("Hit@5", num("Hit@5", 3)),
            ("MRR", num("MRR", 3)),
            ("NDCG@5", num("NDCG@5", 3)),
        ],
    ),
    "rq2": lambda: md_table(
        read("rq2_llm_stability.csv"),
        [
            ("Nhà cung cấp", lambda r: r["Provider_Label"]),
            ("Mô hình", lambda r: f"`{r['Model']}`"),
            ("Số SV", lambda r: r["Num_Evaluated"]),
            ("MAE (TB ± ĐLC)", lambda r: f"{float(r['Mean_MAE']):.2f} ± {float(r['Std_MAE']):.2f}"),
            ("Spearman ρ (TB ± ĐLC)", lambda r: f"{float(r['Mean_Spearman']):.3f} ± {float(r['Std_Spearman']):.3f}"),
        ],
    ),
    "rq3": lambda: md_table(
        read("rq3_allocation.csv"),
        [
            ("N", lambda r: r["Scale_N"]),
            ("Cấu hình", lambda r: r["Config_Name"]),
            ("Tỷ lệ xếp", pct("assigned_rate")),
            ("Đạt NV1", pct("nv1_rate")),
            ("Thứ hạng NV TB", num("mean_rank")),
            ("Điểm phù hợp TB", num("avg_match", 1)),
            ("P10 điểm", num("p10_match", 1)),
            ("Vi phạm", lambda r: r["quota_violations"]),
            ("Thời gian (s)", num("runtime_seconds", 4)),
        ],
    ),
}


CSV_NAME = {"rq1": "rq1_ablation.csv", "rq2": "rq2_llm_stability.csv", "rq3": "rq3_allocation.csv"}


def main():
    readme = HERE / "README.md"
    text = readme.read_text(encoding="utf-8")
    for key, build in TABLES.items():
        if not (RESULTS / CSV_NAME[key]).exists():
            continue
        pattern = re.compile(rf"(<!-- BANG:{key} -->\n).*?(\n<!-- /BANG:{key} -->)", re.S)
        text = pattern.sub(lambda m, b=build: m.group(1) + b() + m.group(2), text)
    cov = RESULTS / "rq1_m5_coverage.txt"
    if cov.exists():
        text = re.sub(
            r"(<!-- PHU:rq1 -->).*?(<!-- /PHU:rq1 -->)",
            lambda m: m.group(1) + "Độ phủ M5: " + cov.read_text(encoding="utf-8").strip() + m.group(2),
            text,
            flags=re.S,
        )
    readme.write_text(text, encoding="utf-8")
    print("Đã cập nhật bảng trong", readme)


if __name__ == "__main__":
    main()
