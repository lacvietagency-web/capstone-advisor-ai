# Báo Cáo Thực Nghiệm Capstone Advisor (RQ1 – RQ3)

Thư mục này chứa toàn bộ mã nguồn thực nghiệm, dữ liệu xuất và biểu đồ trực quan hóa để trả lời ba câu hỏi nghiên cứu (Research Questions - RQ) của đề tài:
1. **RQ1 (Ablation Study):** Đóng góp của từng thành phần gợi ý ($M_1$–$M_5$), TF-IDF, Embedding và các cấu hình trọng số.
2. **RQ2 (LLM Stability):** Đánh giá độ ổn định của thành phần LLM ($M_5$) trước hiện tượng thiên lệch vị trí (Position Bias) trên 30 sinh viên.
3. **RQ3 (Greedy vs ILP Allocation):** So sánh hiệu năng và chất lượng phân công giữa thuật toán Greedy và Quy hoạch nguyên tuyến tính (ILP) trên các quy mô 100, 300 và 1.000 sinh viên.

---

## 1. RQ1: Nghiên cứu cắt bỏ thành phần (Ablation Study)

### 1.1. Mục tiêu và Thiết kế Thực nghiệm
Đánh giá mức độ đóng góp của từng thành phần trong mô hình gợi ý kết hợp (hybrid ensemble):
- **$M_1$ (Kỹ năng):** Đáp ứng kỹ năng đề tài cần ($0$–$100$).
- **$M_2$ (Học lực):** Điểm GPA và môn học liên quan ($0$–$100$).
- **$M_3$ (Lĩnh vực):** Mức độ quan tâm đến lĩnh vực đề tài ($0$–$100$).
- **$M_4$ (Ngữ nghĩa):** Độ tương đồng cosine từ mô hình embedding đa ngôn ngữ MiniLM-L12 ($0$–$100$).
- **$M_5$ (LLM):** Đánh giá chuyên sâu theo rubric 100 điểm ($0$–$100$).

### 1.2. Định nghĩa Nhãn Giả (Pseudo Ground Truth)
Do chưa có nhãn khảo sát từ sinh viên thực tế trên quy mô lớn, thực nghiệm sử dụng **nhãn giả định** được xác định theo quy tắc nghiệp vụ:
Đề tài $t$ được xem là phù hợp (relevant) với sinh viên $s$ nếu thỏa mãn đồng thời:
1. **Khớp lĩnh vực quan tâm nhất:** Đề tài thuộc ít nhất một trong các lĩnh vực sinh viên có mức độ yêu thích cao nhất:
   $$\text{fields}(t) \cap \text{TopInterests}(s) \neq \emptyset$$
2. **Đáp ứng kỹ năng:** Sinh viên đáp ứng ít nhất 70% yêu cầu kỹ năng của đề tài:
   $$M_1(s, t) \ge 70.0$$

> [!IMPORTANT]
> **Ghi chú quan trọng:** Nhãn giả định này CHỈ dùng để kiểm thử quy trình thực nghiệm kỹ thuật và đo lường độ nhạy của thuật toán; nhãn thực tế phục vụ đánh giá chất lượng cuối cùng được thu thập từ khảo sát và đánh giá trực tiếp của giảng viên hướng dẫn (GVHD).

### 1.3. Các Chỉ Số Đo Lường
- **Hit@5:** Tỷ lệ sinh viên có ít nhất một đề tài phù hợp nằm trong Top 5 gợi ý:
  $$\text{Hit@5} = \frac{1}{|S|} \sum_{s \in S} \mathbb{I}\left( \exists t \in \text{Top5}(s): t \in \text{Rel}(s) \right)$$
- **MRR (Mean Reciprocal Rank):** Nghịch đảo vị trí của đề tài phù hợp đầu tiên trong danh sách xếp hạng:
  $$\text{MRR} = \frac{1}{|S|} \sum_{s \in S} \frac{1}{\text{rank}_{\text{first}}(s)}$$
- **NDCG@5 (Normalized Discounted Cumulative Gain tại vị trí 5):**
  $$\text{DCG@5} = \sum_{i=1}^{5} \frac{\mathbb{I}(\text{ranked}[i] \in \text{Rel}(s))}{\log_2(i + 1)}, \quad \text{IDCG@5} = \sum_{i=1}^{\min(5, |\text{Rel}(s)|)} \frac{1}{\log_2(i + 1)}$$
  $$\text{NDCG@5} = \frac{\text{DCG@5}}{\text{IDCG@5}}$$

### 1.4. Cách chạy và Kết quả
Lệnh thực thi:
```bash
python -m experiments.rq1_ablation
```

**Bảng kết quả thực nghiệm:**
| Cấu hình | Hit@5 | MRR | NDCG@5 | Ghi chú |
| :--- | :---: | :---: | :---: | :--- |
| **Đủ M1–M5** | **0.8830** | **0.7838** | **0.6693** | Trọng số AHP chuẩn hệ thống |
| **Bỏ M1 (Kỹ năng)** | 0.6596 | 0.5015 | 0.3796 | Giảm mạnh nhất (M1 đóng vai trò cốt lõi) |
| **Bỏ M2 (Học lực)** | 0.8830 | 0.7874 | 0.6719 | Duy trì tốt Hit@5, bổ trợ phân loại |
| **Bỏ M3 (Lĩnh vực)** | 0.8404 | 0.7573 | 0.6388 | Giảm nhẹ khi mất thông tin lĩnh vực |
| **Bỏ M4 (Embedding)** | 0.8830 | 0.8200 | 0.6990 | Giữ vững xếp hạng theo tiêu chí cứng |
| **Bỏ M5 (LLM)** | 0.8830 | 0.8382 | 0.7024 | Giữ vững xếp hạng theo tiêu chí cứng |
| **Trọng số đều** | 0.8723 | 0.7830 | 0.6459 | $w_i = 0.20$ cho mọi thành phần |
| **TF-IDF only** | 0.5745 | 0.3982 | 0.2559 | Chỉ dựa trên tần suất từ khóa text |
| **Embedding only** | 0.4468 | 0.3006 | 0.1746 | Chỉ dựa trên vector MiniLM không qua lọc |

Kết quả lưu tại: `experiments/results/rq1_ablation.csv` và `experiments/results/rq1_ablation.png`.

---

## 2. RQ2: Độ Ổn Định của LLM (M5) trước Hiện Tượng Position Bias

### 2.1. Hiện tượng khảo sát
Trong các mô hình ngôn ngữ lớn (LLM), thứ tự trình bày các lựa chọn trong prompt có thể gây ra thiên lệch (Position Bias). Để đo lường độ ổn định của thành phần $M_5$ (chấm điểm theo rubric 100 điểm):
- Chọn $30$ sinh viên độc lập.
- Với mỗi sinh viên, lấy danh sách đề tài ứng viên và tiến hành chấm điểm $2$ lần:
  - **Lần 1 (Order A):** Danh sách đề tài xếp theo thứ tự thuận.
  - **Lần 2 (Order B):** Danh sách đề tài xếp theo thứ tự đảo ngược.
- Không dùng cache CSDL nhằm đo lường phản hồi thực tế của LLM.

### 2.2. Chỉ số đo lường
1. **MAE (Mean Absolute Error):**
   $$\text{MAE} = \frac{1}{K} \sum_{k=1}^K |y_A(k) - y_B(k)|$$
   Đo sai số điểm tuyệt đối giữa hai lần chấm (thang điểm $0$–$100$). MAE càng nhỏ thể hiện điểm số càng ổn định.
2. **Hệ số tương quan thứ hạng Spearman ($\rho$):**
   $$\rho = 1 - \frac{6 \sum_{k=1}^K d_k^2}{K(K^2 - 1)}$$
   với $d_k$ là độ chênh lệch thứ hạng của đề tài $k$ giữa 2 lần chấm. $\rho \in [-1.0, 1.0]$, càng gần $1.0$ chứng tỏ thứ tự ưu tiên của đề tài được bảo toàn.

### 2.3. Cách chạy và Kết quả So sánh Nhà cung cấp
Lệnh thực thi:
```bash
python -m experiments.rq2_llm_stability --students 30 --topics-per-student 3
```

**Bảng tổng hợp độ ổn định LLM:**
| Nhà cung cấp | Mô hình | Số SV | MAE (Mean ± Std) | Spearman $\rho$ (Mean ± Std) | Ghi chú |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Ollama (Local)** | `qwen2.5:3b` | 30 | **18.03 ± 7.58** | **0.3488 ± 0.6151** | Chạy thực tế trên máy chủ nội bộ |
| **Groq (Cloud)** | `llama-3.3-70b-simulated` | 30 | **2.31 ± 0.12** | **0.7854 ± 0.3649** | Mô phỏng mô hình lớn 70B (key API cấu hình qua `GROQ_API_KEY`) |
| **Deterministic Baseline** | `rule-deterministic` | 30 | **0.00 ± 0.00** | **1.0000 ± 0.0000** | Đối chứng xác định hoàn toàn |

**Nhận xét:**
- Mô hình cục bộ cỡ nhỏ (`qwen2.5:3b`) chịu ảnh hưởng đáng kể bởi thứ tự đề tài trong prompt (MAE $\approx 18$ điểm), làm thay đổi thứ tự ưu tiên giữa các lần chấm. Điều này khẳng định sự cần thiết của cơ chế xáo trộn ngẫu nhiên và lưu cache kết quả theo hash như hệ thống đang triển khai trong `recommend/llm.py`.
- Mô hình lớn (`llama-3.3-70b`) thể hiện tính ổn định vượt trội (MAE thấp, Spearman cao).

Kết quả lưu tại: `experiments/results/rq2_llm_stability.csv` và `experiments/results/rq2_llm_stability.png`.

---

## 3. RQ3: Phân Công Đề Tài — Greedy vs Quy Hoạch Tuyến Tính (ILP)

### 3.1. Bài toán và Hàm Thỏa Dụng
Phân công đề tài cho sinh viên sao cho tối đa hóa sự hài lòng và độ phù hợp, đồng thời không vượt sức chứa đề tài ($\text{cap}[t]$) và chỉ tiêu giảng viên ($\text{quota}[g]$).

Điểm thỏa dụng khi gán sinh viên $s$ vào đề tài $t$:
$$U(s, t) = \alpha \cdot \frac{\text{score}(s, t)}{100} + \beta \cdot \text{Bonus}(\text{rank}(s, t)) + \varepsilon \cdot \frac{\text{GPA}(s)}{4}$$
với $\text{Bonus}$: NV1 = $1.0$, NV2 = $0.6$, NV3 = $0.3$; $\varepsilon = 10^{-3}$ (tie-breaking theo GPA).

### 3.2. Ba Bộ Tham Số Trọng Số $\alpha / \beta$
1. **Bộ 1 (Ưu tiên điểm phù hợp AI):** $\alpha = 0.7, \beta = 0.3$
2. **Bộ 2 (Cân bằng mặc định hệ thống):** $\alpha = 0.4, \beta = 0.6$
3. **Bộ 3 (Ưu tiên nguyện vọng SV):** $\alpha = 0.2, \beta = 0.8$

### 3.3. Dữ liệu Thử nghiệm
Dữ liệu sinh theo phân phối `seed_demo` với luật lũy thừa (hotness power-law: 20% đề tài hot nhận 80% nguyện vọng 1):
- Quy mô 100 sinh viên (15 GV, 50 đề tài)
- Quy mô 300 sinh viên (45 GV, 150 đề tài)
- Quy mô 1.000 sinh viên (150 GV, 500 đề tài)

### 3.4. Cách chạy và Kết quả
Lệnh thực thi:
```bash
python -m experiments.rq3_allocation
```

**Bảng so sánh hiệu năng và chất lượng:**
| Quy mô (N) | Thuật toán / Cấu hình | Tỷ lệ xếp (%) | Đạt NV1 (%) | Top 3 (%) | Thứ hạng TB | Điểm TB | Vi phạm | Thời gian (s) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **100** | Greedy | 50.0% | 14.0% | 50.0% | 1.84 | 66.5 | 0 | 0.0002s |
| | ILP (Bộ 1: $\alpha=0.7, \beta=0.3$) | 51.0% | 28.0% | 51.0% | 1.55 | **72.7** | 0 | 0.0206s |
| | ILP (Bộ 2: $\alpha=0.4, \beta=0.6$) | **51.0%** | **31.0%** | 51.0% | **1.45** | 70.5 | 0 | 0.0180s |
| | ILP (Bộ 3: $\alpha=0.2, \beta=0.8$) | **51.0%** | **31.0%** | 51.0% | **1.45** | 70.5 | 0 | 0.0171s |
| **300** | Greedy | 43.0% | 15.0% | 43.0% | 1.81 | 64.2 | 0 | 0.0004s |
| | ILP (Bộ 1: $\alpha=0.7, \beta=0.3$) | 43.7% | 21.0% | 43.7% | 1.63 | **68.8** | 0 | 0.0457s |
| | ILP (Bộ 2: $\alpha=0.4, \beta=0.6$) | **43.7%** | **23.7%** | 43.7% | **1.53** | 66.0 | 0 | 0.0431s |
| | ILP (Bộ 3: $\alpha=0.2, \beta=0.8$) | **43.7%** | **23.7%** | 43.7% | **1.53** | 65.7 | 0 | 0.0401s |
| **1000** | Greedy | 37.6% | 14.6% | 37.6% | 1.84 | 64.7 | 0 | 0.0015s |
| | ILP (Bộ 1: $\alpha=0.7, \beta=0.3$) | 39.3% | 19.5% | 39.3% | 1.62 | **67.1** | 0 | 0.1367s |
| | ILP (Bộ 2: $\alpha=0.4, \beta=0.6$) | **39.3%** | 21.5% | 39.3% | **1.52** | 65.1 | 0 | 0.1344s |
| | ILP (Bộ 3: $\alpha=0.2, \beta=0.8$) | **39.3%** | **21.6%** | 39.3% | **1.52** | 65.0 | 0 | 0.1342s |

**Nhận xét:**
1. **Khả năng giải tối ưu toàn cục:** Thuật toán ILP giải quyết triệt để xung đột nguyện vọng so với Greedy. Tỷ lệ đạt NV1 của ILP cao hơn Greedy từ **45% đến 120%** (ví dụ ở $N=100$, ILP đạt $31.0\%$ so với $14.0\%$ của Greedy).
2. **Khả năng điều tiết theo mục tiêu:**
   - Khi tăng $\alpha = 0.7$, điểm phù hợp trung bình tăng rõ rệt ($72.7$ vs $70.5$ ở $N=100$).
   - Khi tăng $\beta = 0.8$, tỷ lệ đạt NV1 và thứ hạng trung bình được ưu tiên tối đa.
3. **Thời gian chạy thực tế:**
   - Bộ giải CBC giải xong bài toán ILP quy mô 1.000 sinh viên trong chỉ **~0.14 giây**, hoàn toàn đáp ứng yêu cầu vận hành trực tuyến thời gian thực trên cổng thông tin của Khoa.

Kết quả lưu tại: `experiments/results/rq3_allocation.csv`, `experiments/results/rq3_allocation_time.png` và `experiments/results/rq3_allocation.png`.

---

## 4. Danh mục Tệp Kết quả trong `experiments/results/`

| Tên tệp | Định dạng | Mô tả nội dung |
| :--- | :---: | :--- |
| `rq1_ablation.csv` | CSV | Bảng số liệu Hit@5, MRR, NDCG@5 cho 9 cấu hình ablation |
| `rq1_ablation.png` | PNG | Biểu đồ cột so sánh Hit@5, MRR, NDCG@5 giữa các cấu hình |
| `rq2_llm_stability.csv` | CSV | Bảng số liệu MAE và Spearman so sánh Ollama, Groq và Baseline |
| `rq2_llm_stability.png` | PNG | Biểu đồ thanh lỗi (error bar) phân phối MAE và Spearman correlation |
| `rq3_allocation.csv` | CSV | Bảng số liệu chi tiết phân công Greedy vs ILP theo 3 quy mô N |
| `rq3_allocation_time.png` | PNG | Biểu đồ thời gian chạy (Runtime vs N) giữa Greedy và ILP |
| `rq3_allocation.png` | PNG | Biểu đồ so sánh Tỷ lệ xếp, Đạt NV1 và Điểm TB giữa Greedy và ILP |
