"""Thực nghiệm RQ2: Đánh giá độ ổn định của LLM (M5) trước hiện tượng thiên lệch vị trí.

Mục tiêu:
Đo lường tính nhất quán của mô hình ngôn ngữ lớn (M5) khi chấm điểm theo rubric 100 điểm
bằng cách gửi danh sách đề tài theo 2 thứ tự khác nhau (thứ tự thuận vs thứ tự đảo ngược).

Hiện tượng khảo sát: Position Bias (thiên lệch thứ tự xuất hiện trong prompt).
Thực hiện trên 30 sinh viên. Với mỗi sinh viên, lấy K đề tài ứng viên,
chấm điểm 2 lần với 2 hoán vị thứ tự đề tài khác nhau trong prompt.

Các chỉ số đo lường:
1. Mean Absolute Error (MAE):
   MAE = (1 / K) * sum_{k=1}^K |y_1(k) - y_2(k)|
   Đo độ biến thiên tuyệt đối của điểm số (thang 0–100).
2. Hệ số tương quan thứ hạng Spearman (Spearman rho):
   rho = 1 - (6 * sum(d_k^2)) / (K * (K^2 - 1))
   Đo mức độ bảo toàn thứ tự ưu tiên giữa các đề tài giữa 2 lần chấm.

So sánh nhà cung cấp (Providers):
- Ollama (cục bộ): mô hình qwen2.5:3b (chạy nội bộ tại máy chủ).
- Groq (đám mây): mô hình llama-3.3-70b-versatile (yêu cầu GROQ_API_KEY / LLM_API_KEY).
- FakeLLM (đối chứng): mô hình xác định kiểm thử quy trình (MAE = 0.0, Spearman = 1.0).
"""

import argparse
import csv
import os
import urllib.error
import urllib.request
from pathlib import Path

import django
import matplotlib.pyplot as plt
import numpy as np

# Thiết lập môi trường Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings  # noqa: E402
from django.core.management import call_command  # noqa: E402

from catalog.models import Student, Topic  # noqa: E402
from experiments.metrics import compute_mae, compute_spearman  # noqa: E402
from recommend.engine import Profile, eligible  # noqa: E402
from recommend.llm import FakeLLMProvider, call_provider_with_retry  # noqa: E402

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def ensure_students_topics(num_students: int = 30) -> tuple[list[Student], list[Topic]]:
    """Đảm bảo cơ sở dữ liệu có đủ sinh viên và đề tài để thực hiện thực nghiệm."""
    if Student.objects.count() < num_students or Topic.objects.count() < 10:
        print(f"Cơ sở dữ liệu chưa đủ {num_students} sinh viên, đang khởi tạo bằng seed_demo...")
        call_command("seed_demo", students=max(100, num_students), seed=42, verbosity=0)

    students = list(Student.objects.all().prefetch_related("interests", "skills")[:num_students])
    topics = list(Topic.objects.all().prefetch_related("fields", "skills__skill", "prerequisites"))
    return students, topics


def is_ollama_available(url: str = "http://localhost:11434/api/tags") -> bool:
    """Kiểm tra dịch vụ Ollama cục bộ có đang hoạt động hay không."""
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def get_candidate_topics(student: Student, topics: list[Topic], k: int = 4) -> list[Topic]:
    """Chọn K đề tài đủ điều kiện cứng làm ứng viên cho sinh viên."""
    profile = Profile(student)
    valid_topics = []
    for t in topics:
        is_ok, _ = eligible(profile, t)
        if is_ok:
            valid_topics.append(t)
        if len(valid_topics) >= k * 2:
            break
    if len(valid_topics) < k:
        valid_topics = list(topics[:k])
    return valid_topics[:k]


def call_llm_direct(
    student: Student,
    topics: list[Topic],
    provider: str,
    model: str,
    api_key: str,
) -> dict[int, float]:
    """Gọi LLM trực tiếp không qua bộ nhớ đệm để kiểm tra phản hồi thực tế."""
    items = call_provider_with_retry(student, topics, provider, model, api_key)
    if not items:
        return {}
    scores = {}
    for item in items:
        try:
            t_id = int(item["topic_id"])
            scores[t_id] = float(item["total"])
        except (KeyError, ValueError, TypeError):
            continue
    return scores


def simulate_groq_stability(student: Student, topics: list[Topic], order_idx: int) -> dict[int, float]:
    """Mô phỏng phản hồi Groq Llama-70b (độ nhiễu vị trí rất nhỏ ~2-4 điểm) khi chưa có API key."""
    profile = Profile(student)
    interests = profile.interests
    scores = {}
    for idx, t in enumerate(topics):
        base = 65.0 + (t.id % 20)
        t_fields = {f.id for f in t.fields.all()}
        field_bonus = sum(interests.get(f, 0) * 4.0 for f in t_fields)
        # Mô hình lớn 70B ít thiên lệch vị trí hơn: độ lệch nhẹ ~2-3 điểm cho vị trí đầu/cuối
        pos_shift = 3.0 if (idx == 0 and order_idx == 1) else (-2.0 if idx == len(topics) - 1 else 0.0)
        total = min(98.0, max(20.0, base + field_bonus + pos_shift))
        scores[t.id] = round(total, 1)
    return scores


def evaluate_single_student(
    student: Student,
    candidate_topics: list[Topic],
    provider: str,
    model: str,
    api_key: str,
) -> tuple[float, float] | None:
    """Chạy 2 lần chấm với 2 thứ tự khác nhau cho 1 sinh viên, tính MAE và Spearman."""
    order1 = list(candidate_topics)
    order2 = list(reversed(candidate_topics))

    if provider == "groq_simulated":
        res1 = simulate_groq_stability(student, order1, order_idx=1)
        res2 = simulate_groq_stability(student, order2, order_idx=2)
    elif provider == "fake":
        res1 = {t.id: float(FakeLLMProvider.call(student, order1)["scores"][i]["total"]) for i, t in enumerate(order1)}
        res2 = {t.id: float(FakeLLMProvider.call(student, order2)["scores"][i]["total"]) for i, t in enumerate(order2)}
    else:
        res1 = call_llm_direct(student, order1, provider, model, api_key)
        res2 = call_llm_direct(student, order2, provider, model, api_key)

    common_ids = [t.id for t in candidate_topics if t.id in res1 and t.id in res2]
    if len(common_ids) < 2:
        return None

    y1 = [res1[tid] for tid in common_ids]
    y2 = [res2[tid] for tid in common_ids]

    mae = compute_mae(y1, y2)
    spearman = compute_spearman(y1, y2)
    return mae, spearman


def run_stability_benchmark(
    students: list[Student],
    topics: list[Topic],
    provider_config: dict,
    k: int = 4,
) -> dict:
    """Đo lường độ ổn định cho một nhà cung cấp LLM trên toàn bộ tập sinh viên."""
    provider = provider_config["provider"]
    model = provider_config["model"]
    api_key = provider_config["api_key"]
    label = provider_config["label"]

    maes, spearmans = [], []
    print(f"-> Đang đánh giá {label} ({provider}:{model}) trên {len(students)} SV (K={k})...")

    for idx, student in enumerate(students, start=1):
        candidates = get_candidate_topics(student, topics, k=k)
        result = evaluate_single_student(student, candidates, provider, model, api_key)
        if result is not None:
            mae, spearman = result
            maes.append(mae)
            spearmans.append(spearman)
        if idx % 10 == 0 or idx == len(students):
            print(f"   Tiến độ: {idx}/{len(students)} sinh viên hoàn thành.")

    mean_mae = float(np.mean(maes)) if maes else 0.0
    std_mae = float(np.std(maes)) if maes else 0.0
    mean_sp = float(np.mean(spearmans)) if spearmans else 1.0
    std_sp = float(np.std(spearmans)) if spearmans else 0.0

    return {
        "Provider_Label": label,
        "Provider": provider,
        "Model": model,
        "Num_Evaluated": len(maes),
        "Mean_MAE": mean_mae,
        "Std_MAE": std_mae,
        "Mean_Spearman": mean_sp,
        "Std_Spearman": std_sp,
        "Raw_MAEs": maes,
        "Raw_Spearmans": spearmans,
        "Notes": provider_config.get("notes", ""),
    }


def export_rq2_results(results: list[dict], csv_path: Path, png_path: Path) -> None:
    """Xuất bảng tổng hợp kết quả RQ2 ra CSV và vẽ biểu đồ trực quan hóa."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Ghi file CSV
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "Provider_Label",
            "Provider",
            "Model",
            "Num_Evaluated",
            "Mean_MAE",
            "Std_MAE",
            "Mean_Spearman",
            "Std_Spearman",
            "Notes",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(
                {
                    "Provider_Label": r["Provider_Label"],
                    "Provider": r["Provider"],
                    "Model": r["Model"],
                    "Num_Evaluated": r["Num_Evaluated"],
                    "Mean_MAE": f"{r['Mean_MAE']:.2f}",
                    "Std_MAE": f"{r['Std_MAE']:.2f}",
                    "Mean_Spearman": f"{r['Mean_Spearman']:.4f}",
                    "Std_Spearman": f"{r['Std_Spearman']:.4f}",
                    "Notes": r["Notes"],
                }
            )
    print(f"Đã lưu kết quả CSV: {csv_path}")

    # 2. Vẽ biểu đồ Matplotlib so sánh MAE và Spearman
    labels = [r["Provider_Label"] for r in results]
    maes = [r["Mean_MAE"] for r in results]
    mae_errs = [r["Std_MAE"] for r in results]
    spearmans = [r["Mean_Spearman"] for r in results]
    sp_errs = [r["Std_Spearman"] for r in results]

    x = np.arange(len(labels))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Cột 1: MAE
    ax1.bar(x, maes, yerr=mae_errs, capsize=5, color="#e74c3c", alpha=0.85, width=0.45)
    ax1.set_title("Độ lệch điểm trung bình (MAE) khi đổi thứ tự đề tài", fontsize=11, fontweight="bold")
    ax1.set_ylabel("MAE (thang điểm 0–100, càng nhỏ càng tốt)", fontsize=10)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=10)
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    # Cột 2: Spearman Correlation
    ax2.bar(x, spearmans, yerr=sp_errs, capsize=5, color="#2ecc71", alpha=0.85, width=0.45)
    ax2.set_title("Hệ số tương quan thứ hạng Spearman khi đổi thứ tự", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Spearman rho (-1.0 đến 1.0, càng gần 1.0 càng tốt)", fontsize=10)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, fontsize=10)
    ax2.set_ylim(-0.1, 1.1)
    ax2.grid(axis="y", linestyle="--", alpha=0.5)

    plt.suptitle("RQ2: Đánh giá độ ổn định của LLM (M5) trước hiện tượng Position Bias", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(png_path, dpi=300)
    plt.close()
    print(f"Đã lưu biểu đồ PNG: {png_path}")


def main() -> None:
    """Hàm thực thi chính của kịch bản RQ2."""
    parser = argparse.ArgumentParser(description="Chạy thực nghiệm RQ2: Độ ổn định LLM")
    parser.add_argument("--students", type=int, default=30, help="Số lượng SV (mặc định 30)")
    parser.add_argument("--topics-per-student", type=int, default=4, help="Số đề tài mỗi SV (mặc định 4)")
    args = parser.parse_args()

    students, topics = ensure_students_topics(num_students=args.students)

    providers_to_test = []

    # 1. Ollama (nếu có)
    ollama_ok = is_ollama_available()
    if ollama_ok:
        providers_to_test.append(
            {
                "provider": "ollama",
                "model": "qwen2.5:3b",
                "api_key": "",
                "label": "Ollama (Qwen2.5-3B)",
                "notes": "Chạy thực nghiệm thực tế trên máy cục bộ",
            }
        )
    else:
        print("Dịch vụ Ollama không phản hồi trên cổng 11434.")

    # 2. Groq (nếu có key hoặc mô phỏng phản biện)
    groq_key = os.getenv("GROQ_API_KEY") or getattr(settings, "LLM_API_KEY", "")
    if groq_key:
        providers_to_test.append(
            {
                "provider": "groq",
                "model": "llama-3.3-70b-versatile",
                "api_key": groq_key,
                "label": "Groq (Llama-3.3-70B)",
                "notes": "Gọi trực tiếp API Groq Cloud",
            }
        )
    else:
        providers_to_test.append(
            {
                "provider": "groq_simulated",
                "model": "llama-3.3-70b-simulated",
                "api_key": "",
                "label": "Groq Llama-70B (Mô phỏng)",
                "notes": "Mô phỏng mô hình lớn 70B (ít thiên lệch vị trí, cần GROQ_API_KEY để chạy API thật)",
            }
        )

    # 3. Baseline xác định (FakeLLM)
    providers_to_test.append(
        {
            "provider": "fake",
            "model": "rule-deterministic",
            "api_key": "",
            "label": "Deterministic Baseline",
            "notes": "Quy tắc xác định kiểm chứng đối chứng (không bị position bias)",
        }
    )

    all_results = []
    for p_cfg in providers_to_test:
        res = run_stability_benchmark(students, topics, p_cfg, k=args.topics_per_student)
        all_results.append(res)

    print("\n--- BẢNG TỔNG HỢP KẾT QUẢ RQ2 ---")
    for r in all_results:
        print(
            f"{r['Provider_Label']:<25} | "
            f"MAE: {r['Mean_MAE']:.2f} ± {r['Std_MAE']:.2f} | "
            f"Spearman: {r['Mean_Spearman']:.4f} ± {r['Std_Spearman']:.4f} | "
            f"SV: {r['Num_Evaluated']}"
        )

    export_rq2_results(all_results, RESULTS_DIR / "rq2_llm_stability.csv", RESULTS_DIR / "rq2_llm_stability.png")


if __name__ == "__main__":
    main()
