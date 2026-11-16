"""Thực nghiệm RQ4: phát hiện trùng / giống đề tài khoá trước trên KHO THẬT (báo cáo ĐATN khoá trước do GVHD cung cấp).

Dữ liệu: file JSONL của lệnh `them_de_tai_khoa_truoc --tu-file` (tên đề tài, mô tả, công nghệ, năm — KHÔNG có tên SV).
File chứa dữ liệu của trường nên để NGOÀI repo; script chỉ ghi số liệu tổng hợp vào experiments/results/.

Đo bằng đúng mô hình của hệ thống (M4: paraphrase-multilingual-MiniLM-L12-v2, cosine của vector chuẩn hoá):
1. Phân bố "độ giống với đề tài gần nhất" trong kho; tỷ lệ đề tài có ≥1 đề tài khác giống ≥ 0,70/0,75/0,80/0,85/0,90.
2. Mô phỏng dùng thật: khoá năm Y là "đề tài mới", các năm trước là kho → bao nhiêu % nhận tư vấn cải tiến (≥ 0,70).
3. Cơ cấu lĩnh vực và công nghệ (cho trang thống kê xu hướng).

    python experiments/rq4_khoa_truoc.py --file /duong/dan/de-tai-khoa-truoc.jsonl [--nam-moi 2025]
"""

import argparse
import collections
import csv
import json
from pathlib import Path

import numpy as np

RESULTS = Path(__file__).resolve().parent / "results"
MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"  # = recommend.engine.SemanticModel.NAME
THRESHOLDS = (0.70, 0.75, 0.80, 0.85, 0.90)


def embed(texts):
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(MODEL).encode(texts, normalize_embeddings=True, batch_size=32, show_progress_bar=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--nam-moi", type=int, default=2025)
    a = ap.parse_args()
    rows = [json.loads(x) for x in Path(a.file).read_text(encoding="utf-8").splitlines() if x.strip()]
    n = len(rows)
    vec = embed([f"{r['title']}. {r['description']}" for r in rows])
    vec_title = embed([r["title"] for r in rows])

    out = []
    for name, v in (("tên + mô tả", vec), ("chỉ tên", vec_title)):
        sim = v @ v.T
        np.fill_diagonal(sim, -1)
        best = sim.max(axis=1)
        iu = np.triu_indices(n, 1)
        pairs = sim[iu]
        for t in THRESHOLDS:
            out.append(
                {
                    "bieu_dien": name,
                    "nguong": t,
                    "ty_le_de_tai_co_ban_giong": round(float((best >= t).mean()), 3),
                    "so_cap": int((pairs >= t).sum()),
                }
            )
        out.append(
            {
                "bieu_dien": name,
                "nguong": "trung vị gần nhất",
                "ty_le_de_tai_co_ban_giong": round(float(np.median(best)), 3),
                "so_cap": "",
            }
        )

    # mô phỏng: khoá a.nam_moi là đề tài mới, các năm trước là kho
    new = [i for i, r in enumerate(rows) if r["year"] == a.nam_moi]
    old = [i for i, r in enumerate(rows) if r["year"] < a.nam_moi]
    sim_no = vec[new] @ vec[old].T if new and old else np.zeros((0, 0))
    nb = sim_no.max(axis=1) if sim_no.size else np.array([])
    for t in THRESHOLDS:
        out.append(
            {
                "bieu_dien": f"mô phỏng {a.nam_moi} so với kho trước {a.nam_moi}",
                "nguong": t,
                "ty_le_de_tai_co_ban_giong": round(float((nb >= t).mean()), 3) if nb.size else "",
                "so_cap": len(new),
            }
        )

    RESULTS.mkdir(exist_ok=True)
    with open(RESULTS / "rq4_khoa_truoc.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)

    years = collections.Counter(r["year"] for r in rows)
    fields = collections.Counter(
        r.get("result_note", "").removeprefix("Lĩnh vực: ").split(" · ")[0] or "?" for r in rows
    )
    tech = collections.Counter(t.strip() for r in rows for t in r.get("technologies", "").split(",") if t.strip())
    md = [
        f"# RQ4 — Đề tài khoá trước (kho thật, {n} đề tài sau khi bỏ bản trùng)",
        "",
        f"Năm: {dict(sorted(years.items()))}. Mô hình: `{MODEL}` (giống M4).",
        "",
        "| Biểu diễn | Ngưỡng | Tỷ lệ đề tài có ≥1 đề tài giống | Số cặp / số đề tài mới |",
        "|---|---|---|---|",
    ]
    md += [f"| {o['bieu_dien']} | {o['nguong']} | {o['ty_le_de_tai_co_ban_giong']} | {o['so_cap']} |" for o in out]
    md += ["", "| Lĩnh vực | Số đề tài |", "|---|---|"] + [f"| {k} | {v} |" for k, v in fields.most_common()]
    md += ["", "| Công nghệ (top 15) | Số đề tài |", "|---|---|"] + [f"| {k} | {v} |" for k, v in tech.most_common(15)]
    (RESULTS / "rq4_khoa_truoc.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sim = vec @ vec.T
    np.fill_diagonal(sim, -1)
    plt.figure(figsize=(7, 3.6))
    plt.hist(sim.max(axis=1), bins=30, color="#2454B8")
    for t, c in ((0.70, "#D97706"), (0.75, "#B91C1C")):
        plt.axvline(t, color=c, ls="--", label=f"ngưỡng {t:.2f}")
    plt.xlabel("Độ giống với đề tài gần nhất trong kho (cosine)")
    plt.ylabel("Số đề tài")
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS / "rq4_khoa_truoc.png", dpi=150)
    print("\n".join(md[:20]))


if __name__ == "__main__":
    main()
