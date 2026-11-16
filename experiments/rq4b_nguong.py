"""Thực nghiệm RQ4b: hiệu chỉnh ngưỡng trùng trên kho đề tài khoá trước THẬT, bằng 300 cặp lấy mẫu phân tầng có nhãn.

Đầu vào (để NGOÀI repo vì chứa tên đề tài của trường):
  cap_mau.jsonl  — {k, cos, w (trọng số tầng = số cặp thật mà mỗi cặp mẫu đại diện), ...}
  nhan_<ai>.jsonl — {k, nhan}: 2 = trùng/gần trùng, 1 = cùng chủ đề nhưng khác rõ, 0 = khác (mỗi AI gán độc lập)
Đo: đồng thuận Cohen's kappa giữa 2 người gán; precision/recall/F1 CÓ TRỌNG SỐ TẦNG theo ngưỡng cosine cho hai việc:
  "trùng" (nhãn 2 — cảnh báo đề tài trùng) và "giống, đáng tư vấn" (nhãn ≥ 1 — tư vấn cải tiến từ khoá trước).
Chỉ dùng cặp hai người gán CÙNG nhãn (đồng thuận) để tính precision/recall; ghi rõ độ phủ.

    python experiments/rq4b_nguong.py --mau cap_mau.jsonl --nhan nhan_gemini.jsonl nhan_openrouter.jsonl
"""

import argparse
import csv
import json
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "results"
GRID = [round(0.60 + 0.025 * i, 3) for i in range(15)]  # 0,60 … 0,95


def load(p, key="k"):
    return {o[key]: o for o in (json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip())}


def kappa(a, b, classes):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b, strict=True)) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in classes)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def prf(rows, t, pos):
    tp = sum(r["w"] for r in rows if r["cos"] >= t and pos(r["nhan"]))
    fp = sum(r["w"] for r in rows if r["cos"] >= t and not pos(r["nhan"]))
    fn = sum(r["w"] for r in rows if r["cos"] < t and pos(r["nhan"]))
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return p, r, (2 * p * r / (p + r) if p + r else 0.0)


def best_f1(scores, rows, pos):
    """F1 có trọng số tầng cao nhất khi quét ngưỡng trên chính các điểm số → (F1, P, R, ngưỡng)."""
    best = (0.0, 0.0, 0.0, None)
    for t in sorted(set(scores)):
        tp = sum(r["w"] for s, r in zip(scores, rows, strict=True) if s >= t and pos(r["nhan"]))
        fp = sum(r["w"] for s, r in zip(scores, rows, strict=True) if s >= t and not pos(r["nhan"]))
        fn = sum(r["w"] for s, r in zip(scores, rows, strict=True) if s < t and pos(r["nhan"]))
        p = tp / (tp + fp) if tp + fp else 0.0
        rc = tp / (tp + fn) if tp + fn else 0.0
        f = 2 * p * rc / (p + rc) if p + rc else 0.0
        if f > best[0]:
            best = (f, p, rc, t)
    return best


def compare_methods(rows, kho_path):
    """PA1 cosine Sentence-BERT · PA2 cosine TF-IDF (âm tiết 1–2 gram ≈ từ ghép) · PA3 lai (logistic, CV 5 phần)."""
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import StratifiedKFold, cross_val_predict

    kho = [json.loads(x) for x in Path(kho_path).read_text(encoding="utf-8").splitlines() if x.strip()]
    tf = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=2)
    tf.fit([f"{r['title']}. {r['description']}" for r in kho])
    va, vb = tf.transform([r["a"] for r in rows]), tf.transform([r["b"] for r in rows])
    s_tf = np.asarray(va.multiply(vb).sum(axis=1)).ravel()  # vector TF-IDF đã chuẩn hoá L2 → tích = cosine
    s_cos = np.array([r["cos"] for r in rows])
    w = np.array([r["w"] for r in rows])
    out = [
        "## So sánh phương án (cặp đồng thuận, trọng số tầng)",
        "",
        "| Việc | Phương án | AUC | F1 tốt nhất | P | R |",
        "|---|---|---|---|---|---|",
    ]
    for task, pos in (("Trùng (nhãn 2)", lambda v: v == 2), ("Cùng chủ đề (nhãn ≥ 1)", lambda v: v >= 1)):
        y = np.array([pos(r["nhan"]) for r in rows])
        feats = np.c_[s_cos, s_tf]
        if y.sum() >= 5 and (~y).sum() >= 5:
            cv = StratifiedKFold(5, shuffle=True, random_state=42)
            s_hyb = cross_val_predict(
                LogisticRegression(), feats, y, cv=cv, method="predict_proba", params={"sample_weight": w}
            )[:, 1]
        else:
            s_hyb = s_cos
        for name, s in (("PA1 Sentence-BERT", s_cos), ("PA2 TF-IDF từ khoá", s_tf), ("PA3 lai (logistic)", s_hyb)):
            auc = roc_auc_score(y, s, sample_weight=w) if 0 < y.sum() < len(y) else float("nan")
            f, p, r, _ = best_f1(list(s), rows, pos)
            out.append(f"| {task} | {name} | {auc:.3f} | {f:.3f} | {p:.3f} | {r:.3f} |")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mau", required=True)
    ap.add_argument("--nhan", nargs=2, required=True)
    ap.add_argument("--kho", help="de-tai-khoa-truoc.jsonl — để học TF-IDF và so 3 phương án (gợi ý họp vòng 2)")
    a = ap.parse_args()
    mau = load(a.mau)
    l1, l2 = (load(p) for p in a.nhan)
    both = sorted(set(l1) & set(l2) & set(mau))
    x, y = [l1[k]["nhan"] for k in both], [l2[k]["nhan"] for k in both]
    k3 = kappa(x, y, [0, 1, 2])
    k_dup = kappa([v == 2 for v in x], [v == 2 for v in y], [True, False])
    agree = [{**mau[k], "nhan": l1[k]["nhan"]} for k in both if l1[k]["nhan"] == l2[k]["nhan"]]

    out = []
    for t in GRID:
        p2, r2, f2 = prf(agree, t, lambda v: v == 2)
        p1, r1, f1 = prf(agree, t, lambda v: v >= 1)
        out.append(
            {
                "nguong": t,
                "trung_P": round(p2, 3),
                "trung_R": round(r2, 3),
                "trung_F1": round(f2, 3),
                "giong_P": round(p1, 3),
                "giong_R": round(r1, 3),
                "giong_F1": round(f1, 3),
            }
        )
    best_dup = next((o for o in out if o["trung_P"] >= 0.85), max(out, key=lambda o: o["trung_F1"]))
    best_adv = max(out, key=lambda o: o["giong_F1"])

    RESULTS.mkdir(exist_ok=True)
    with open(RESULTS / "rq4b_nguong.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    names = [Path(p).stem.removeprefix("nhan_") for p in a.nhan]
    md = [
        f"# RQ4b — Hiệu chỉnh ngưỡng trên kho thật ({len(mau)} cặp mẫu phân tầng)",
        "",
        f"Người gán nhãn: {names[0]} và {names[1]} (độc lập). Cả hai gán được {len(both)}/{len(mau)} cặp; "
        f"đồng thuận {len(agree)} cặp. Cohen's kappa 3 nhãn = {k3:.2f}; kappa 'trùng/không' = {k_dup:.2f}.",
        "Precision/recall có trọng số tầng, chỉ trên các cặp đồng thuận.",
        "",
        "| Ngưỡng | Trùng: P | R | F1 | Giống (tư vấn): P | R | F1 |",
        "|---|---|---|---|---|---|---|",
    ]
    md += [
        f"| {o['nguong']} | {o['trung_P']} | {o['trung_R']} | {o['trung_F1']} | {o['giong_P']} | {o['giong_R']} | "
        f"{o['giong_F1']} |"
        for o in out
    ]
    md += [
        "",
        f"Ngưỡng cảnh báo trùng đề xuất (P ≥ 0,85 đầu tiên, không có thì F1 cao nhất): **{best_dup['nguong']}** "
        f"(P = {best_dup['trung_P']}, R = {best_dup['trung_R']}).",
        f"Ngưỡng tư vấn khoá trước đề xuất (F1 cao nhất): **{best_adv['nguong']}** "
        f"(P = {best_adv['giong_P']}, R = {best_adv['giong_R']}, F1 = {best_adv['giong_F1']}).",
        "",
        "Giới hạn: nhãn do AI gán (chưa có người duyệt), kho chỉ gồm khoá 2024–2025 của một trường.",
    ]
    if a.kho:
        md += ["", *compare_methods(agree, a.kho)]
    (RESULTS / "rq4b_nguong.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
    for i, (key, title) in enumerate(
        (("trung", "Cảnh báo TRÙNG (nhãn 2)"), ("giong", "Tư vấn: cùng chủ đề (nhãn ≥ 1)"))
    ):
        ax[i].plot(GRID, [o[f"{key}_P"] for o in out], "o-", color="#2454B8", label="Precision")
        ax[i].plot(GRID, [o[f"{key}_R"] for o in out], "s-", color="#D97706", label="Recall")
        ax[i].plot(GRID, [o[f"{key}_F1"] for o in out], "^-", color="#176B60", label="F1")
        ax[i].set_title(title)
        ax[i].set_xlabel("Ngưỡng cosine")
    ax[0].legend()
    plt.tight_layout()
    plt.savefig(RESULTS / "rq4b_nguong.png", dpi=150)
    print("\n".join(md))


if __name__ == "__main__":
    main()
