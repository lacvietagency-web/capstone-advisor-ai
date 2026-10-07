# 05-thuc-nghiem.md — Giải thích thực nghiệm RQ1–RQ3

## 1. RQ1 — Mỗi thành phần M1–M5 đóng góp thế nào?

### (a) Câu hỏi nghiên cứu bằng lời thường

Hệ thống gợi ý sử dụng nhiều nguồn thông tin cùng lúc:

- **M1 — Kỹ năng:** sinh viên có đáp ứng kỹ năng đề tài yêu cầu không.
- **M2 — Học lực:** GPA và các môn học liên quan có phù hợp không.
- **M3 — Lĩnh vực:** đề tài có thuộc lĩnh vực sinh viên quan tâm không.
- **M4 — Embedding:** nội dung hồ sơ sinh viên và đề tài có gần nhau về mặt ngữ nghĩa không.
- **M5 — LLM:** LLM đọc tổng thể hồ sơ và chấm theo rubric định trước.

RQ1 muốn trả lời câu hỏi:

> Nếu bỏ từng thành phần khỏi hệ thống thì chất lượng danh sách Top 5 thay đổi như thế nào? Hệ thống kết hợp có khác gì so với chỉ dùng TF-IDF hoặc Embedding?

### (b) Làm thế nào — ví dụ đời thường

Có thể hình dung như đánh giá một chiếc điện thoại bằng nhiều tiêu chí: màn hình, pin, camera, hiệu năng và phần mềm.

Muốn biết camera có đóng góp hay không, ta giữ nguyên mọi thứ nhưng bỏ điểm camera rồi xem kết quả xếp hạng thay đổi thế nào. Sau đó làm tương tự với pin, màn hình và các thành phần khác.

Trong đồ án, cách làm tương tự:

1. Chạy hệ thống đầy đủ M1–M5.
2. Lần lượt bỏ M1, M2, M3, M4 hoặc M5.
3. Thử cấu hình trọng số đều.
4. So với hai baseline đơn giản là TF-IDF only và Embedding only.
5. Đánh giá bằng Hit@5, MRR và NDCG@5.

Nhãn phù hợp trong thực nghiệm này là **pseudo ground truth**:

- đề tài phải thuộc một trong các lĩnh vực sinh viên quan tâm cao nhất;
- đồng thời M1 phải đạt ít nhất 70.

### (c) Bảng kết quả

| Cấu hình | Hit@5 | MRR | NDCG@5 |
| --- | --- | --- | --- |
| Đủ M1–M5 | 0.883 | 0.813 | 0.679 |
| Bỏ M1 (Kỹ năng) | 0.692 | 0.500 | 0.395 |
| Bỏ M2 (Học lực) | 0.883 | 0.821 | 0.682 |
| Bỏ M3 (Lĩnh vực) | 0.830 | 0.758 | 0.640 |
| Bỏ M4 (Embedding) | 0.872 | 0.831 | 0.701 |
| Bỏ M5 (LLM) | 0.883 | 0.838 | 0.702 |
| Trọng số đều | 0.872 | 0.802 | 0.656 |
| TF-IDF only | 0.575 | 0.398 | 0.256 |
| Embedding only | 0.447 | 0.301 | 0.175 |

**Độ phủ M5:** 75/94 sinh viên có điểm M5 thật từ LLM; các trường hợp còn lại M5 trống do LLM lỗi hoặc hết hạn mức.

### (d) Đọc kết quả thế nào?

Điểm dễ thấy nhất là khi **bỏ M1**, cả ba chỉ số giảm mạnh:

- Hit@5: từ 0.883 xuống 0.692.
- MRR: từ 0.813 xuống 0.500.
- NDCG@5: từ 0.679 xuống 0.395.

Bỏ M3 cũng làm kết quả giảm:

- Hit@5 còn 0.830.
- MRR còn 0.758.
- NDCG@5 còn 0.640.

Hai baseline đơn lẻ thấp hơn rõ rệt:

- TF-IDF only: Hit@5 = 0.575, MRR = 0.398, NDCG@5 = 0.256.
- Embedding only: Hit@5 = 0.447, MRR = 0.301, NDCG@5 = 0.175.

Tuy nhiên, **không được kết luận rằng M4 hoặc M5 vô ích chỉ vì khi bỏ chúng, một vài chỉ số không giảm**. Bỏ M4 cho NDCG@5 = 0.701 và bỏ M5 cho NDCG@5 = 0.702, thậm chí cao hơn cấu hình đầy đủ 0.679. Nguyên nhân quan trọng là cách tạo nhãn giả đang ưu tiên trực tiếp cho M1 và M3.

Kết quả RQ1 vì vậy chủ yếu cho thấy:

- pipeline ablation hoạt động;
- hệ thống có thể đo độ nhạy khi bỏ từng thành phần;
- M1 và M3 có ảnh hưởng rất rõ dưới bộ nhãn hiện tại;
- chưa đủ bằng chứng để đánh giá công bằng giá trị thực tế của M4 và M5.

M5 trong RQ1 là điểm LLM thật từ Groq `openai/gpt-oss-120b`, temperature 0. M5 chỉ được chấm cho Top 15 ứng viên sau M1–M4. Đề tài ngoài Top 15 hoặc trường hợp LLM lỗi không có M5 và hệ thống chia lại trọng số. Điểm đã chấm được lưu cache.

### (e) Giới hạn phải nói thật

**Giới hạn lớn nhất của RQ1 là nhãn giả có tính vòng tròn.**

Nhãn được tạo từ chính:

- M1 — kỹ năng;
- M3 — lĩnh vực.

Vì vậy các cấu hình sử dụng M1 và M3 có lợi thế ngay từ cách định nghĩa đáp án đúng. Do đó không thể dùng bảng này để khẳng định M1 hoặc M3 chắc chắn quan trọng hơn M4 hay M5 trong thực tế.

Ngoài ra, M5 chưa phủ toàn bộ dữ liệu: chỉ **75/94 sinh viên** có điểm M5 thật. Các trường hợp còn lại bị thiếu do lỗi LLM hoặc giới hạn lượt gọi.

Muốn đánh giá công bằng hơn cần nhãn thật từ sinh viên và giảng viên thay vì chỉ dùng pseudo ground truth.

### (f) Một câu để nói khi bảo vệ

> “RQ1 cho thấy pipeline ablation hoạt động và M1, M3 ảnh hưởng mạnh dưới bộ nhãn hiện tại, nhưng em không khẳng định M4 hay M5 kém hơn vì pseudo ground truth được tạo trực tiếp từ M1 và M3 nên tồn tại thiên lệch vòng tròn.”

---

## 2. RQ2 — LLM có bị ảnh hưởng bởi thứ tự đề tài không?

### (a) Câu hỏi nghiên cứu bằng lời thường

RQ2 kiểm tra:

> Nếu vẫn là cùng một sinh viên và cùng các đề tài, nhưng đổi thứ tự đề tài trong prompt, LLM có chấm giống nhau hay không?

Đây là kiểm tra **position bias**, tức LLM có thể vô tình ưu tiên hoặc thay đổi đánh giá chỉ vì một đề tài được đặt trước hay đặt sau.

### (b) Làm thế nào — ví dụ đời thường

Giả sử đưa cho một giám khảo ba bài A, B, C.

Lần đầu đưa theo thứ tự:

> A → B → C

Lần sau đưa đúng ba bài đó nhưng đảo thành:

> C → B → A

Nếu người chấm thực sự ổn định, điểm và thứ tự đánh giá không nên thay đổi nhiều.

Trong RQ2:

- mỗi sinh viên được chấm hai lần;
- lần A dùng thứ tự thuận;
- lần B dùng thứ tự đảo ngược;
- không dùng cache CSDL;
- so bằng MAE và Spearman ρ.

**MAE càng thấp càng tốt.**

**Spearman ρ càng gần 1 càng tốt.**

### (c) Bảng kết quả

| Nhà cung cấp | Mô hình | Số SV | MAE (TB ± ĐLC) | Spearman ρ (TB ± ĐLC) |
| --- | --- | --- | --- | --- |
| Ollama (Qwen2.5-3B) | `qwen2.5:3b` | 29 | 16.65 ± 8.16 | -0.180 ± 0.298 |
| Groq (openai/gpt-oss-20b) | `openai/gpt-oss-20b` | 30 | 10.34 ± 4.86 | 0.710 ± 0.226 |
| Groq (qwen/qwen3.8-27b) | `qwen/qwen3.8-27b` | 9 | 6.17 ± 1.94 | 0.878 ± 0.090 |
| Groq (openai/gpt-oss-120b) — model M5 | `openai/gpt-oss-120b` | 30 | 7.92 ± 3.18 | 0.823 ± 0.110 |

### (d) Đọc kết quả thế nào?

`qwen2.5:3b` chạy local có:

- MAE = 16.65 ± 8.16;
- Spearman = -0.180 ± 0.298.

Điều này cho thấy thứ tự đánh giá thay đổi khá mạnh khi đảo vị trí đề tài.

`openai/gpt-oss-20b` trên Groq ổn định hơn:

- MAE = 10.34 ± 4.86;
- Spearman = 0.710 ± 0.226.

`qwen/qwen3.8-27b` có kết quả tốt nhất trong bảng đã đo:

- MAE = 6.17 ± 1.94;
- Spearman = 0.878 ± 0.090.

Tuy nhiên model này mới đo được **9 sinh viên**, nên không nên khẳng định chắc chắn nó tốt nhất cho toàn bộ tập dữ liệu.

Kết luận hợp lý của RQ2 là: **LLM không hoàn toàn bất biến với thứ tự prompt**, và mức độ ổn định khác nhau giữa các model.

### (e) Giới hạn phải nói thật

Mặc dù thiết kế ban đầu chọn 30 sinh viên, số mẫu thực tế khác nhau:

- Qwen2.5-3B: 29 sinh viên;
- gpt-oss-20b: 30 sinh viên;
- gpt-oss-120b (model M5 thật của hệ thống): 30 sinh viên — MAE 7,92, Spearman 0,823: ổn định tốt, đủ để dùng làm M5.
- qwen3.8-27b: 9 sinh viên.

Nguyên nhân là API miễn phí có giới hạn lượt gọi và giới hạn theo thời gian.

Nemotron-550B trên OpenRouter không phản hồi kịp nên không có dòng kết quả.

Vì vậy không nên xem các model trong bảng như một benchmark hoàn toàn cân bằng về số mẫu.

### (f) Một câu để nói khi bảo vệ

> “RQ2 cho thấy thứ tự đề tài thực sự có thể ảnh hưởng điểm M5; gpt-oss-20b đạt MAE 10.34 và Spearman 0.710, còn qwen3.8-27b đạt 6.17 và 0.878 nhưng mới đo được 9 sinh viên nên em không kết luận quá mức.”

---

## 3. RQ2b — Cùng một model nhưng đổi nơi chạy có ra cùng kết quả không?

### (a) Câu hỏi nghiên cứu bằng lời thường

RQ2b kiểm tra:

> Nếu cùng dùng `gpt-oss-120b`, cùng temperature 0 và cùng prompt, nhưng chạy qua hai hạ tầng khác nhau thì điểm M5 có giống hệt nhau không?

Hai nơi chạy được so sánh là:

- Groq;
- OmniRoute/Tinfoil.

### (b) Làm thế nào — ví dụ đời thường

Có thể hình dung cùng một chương trình được chạy trên hai máy khác nhau.

Về lý thuyết ta mong kết quả rất giống nhau. Nhưng trong hệ thống AI, nhà cung cấp có thể dùng phần cứng, cách lượng tử hóa hoặc phiên bản triển khai khác nhau.

RQ2b lấy các cặp **(sinh viên, đề tài)** mà cả hai nơi đều đã chấm rồi so sánh trực tiếp. Dữ liệu lấy từ cache nên thử nghiệm này không cần gọi API lại.

### (c) Bảng kết quả

| Nơi chạy A | Nơi chạy B | Số cặp | Số SV | MAE | Spearman ρ |
| --- | --- | --- | --- | --- | --- |
| Groq (openai/gpt-oss-120b) | OmniRoute/Tinfoil (gptoss120) | 268 | 18 | 9.19 | 0.634 |

### (d) Đọc kết quả thế nào?

Trên **268 cặp của 18 sinh viên**:

- MAE giữa hai nơi chạy là 9.19;
- Spearman ρ là 0.634.

Như vậy cùng tên model, cùng prompt và temperature 0 vẫn **không cho kết quả giống hệt nhau** giữa hai hạ tầng.

Điều này là lý do hệ thống không chỉ lưu tên model, mà còn cần ghi nhận nơi chạy khi lưu và phân tích điểm M5.

### (e) Giới hạn phải nói thật

RQ2b chỉ có dữ liệu giao nhau của:

- 268 cặp;
- 18 sinh viên;
- hai nơi chạy cụ thể là Groq và OmniRoute/Tinfoil.

Vì vậy kết quả chứng minh rằng sự khác biệt **có tồn tại trong thử nghiệm này**, nhưng không có nghĩa mọi nhà cung cấp hay mọi lần chạy đều khác nhau đúng mức MAE 9.19.

Temperature 0 cũng không có nghĩa là kết quả chắc chắn giống tuyệt đối.

### (f) Một câu để nói khi bảo vệ

> “RQ2b cho thấy temperature 0 không đồng nghĩa với hoàn toàn deterministic giữa các hạ tầng: cùng gpt-oss-120b nhưng Groq và Tinfoil vẫn có MAE 9.19 và Spearman 0.634 trên 268 cặp.”

---

## 4. RQ3 — ILP có tốt hơn Greedy trong phân công đề tài không?

### (a) Câu hỏi nghiên cứu bằng lời thường

Sau khi hệ thống đã có điểm phù hợp và sinh viên đã chọn nguyện vọng, Khoa phải quyết định:

> Ai được đề tài nào để vừa tôn trọng nguyện vọng, vừa giữ điểm phù hợp cao, vừa không vượt sức chứa đề tài và chỉ tiêu giảng viên?

RQ3 so sánh hai cách giải:

- **Greedy:** xử lý lần lượt, thấy phương án tốt trước mắt thì chọn.
- **ILP:** xét toàn bộ bài toán cùng lúc và tìm phương án tối ưu theo hàm mục tiêu và các ràng buộc.

### (b) Làm thế nào — ví dụ đời thường

Giả sử có nhiều sinh viên cùng muốn một đề tài hot.

Greedy giống như phát chỗ lần lượt: gặp ai trước thì cố gắng xếp người đó trước. Một lựa chọn tốt ở thời điểm hiện tại có thể làm những sinh viên phía sau mất phương án tốt.

ILP giống như Khoa nhìn toàn bộ danh sách sinh viên, nguyện vọng, sức chứa và quota cùng lúc rồi mới quyết định cách ghép tổng thể.

Thực nghiệm dùng ba quy mô:

- 100 sinh viên;
- 300 sinh viên;
- 1.000 sinh viên.

Dữ liệu được tạo theo tình huống cạnh tranh mạnh: khoảng 20% đề tài hot nhận 80% nguyện vọng 1.

ILP được thử với ba bộ trọng số:

- Bộ 1: α = 0.7, β = 0.3 — ưu tiên điểm phù hợp.
- Bộ 2: α = 0.4, β = 0.6 — cân bằng mặc định.
- Bộ 3: α = 0.2, β = 0.8 — ưu tiên nguyện vọng.

### (c) Bảng kết quả

| N | Cấu hình | Tỷ lệ xếp | Đạt NV1 | Thứ hạng NV TB | Điểm phù hợp TB | P10 điểm | Vi phạm | Thời gian (s) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | Greedy | 50.0% | 14.0% | 1.96 | 66.5 | 44.5 | 0 | 0.0001 |
| 100 | ILP (Bộ 1 (Ưu tiên điểm phù hợp)) | 51.0% | 28.0% | 1.63 | 72.7 | 52.0 | 0 | 0.0167 |
| 100 | ILP (Bộ 2 (Cân bằng mặc định)) | 51.0% | 31.0% | 1.53 | 70.5 | 47.2 | 0 | 0.0149 |
| 100 | ILP (Bộ 3 (Ưu tiên nguyện vọng)) | 51.0% | 31.0% | 1.53 | 70.5 | 47.2 | 0 | 0.0150 |
| 300 | Greedy | 43.0% | 15.0% | 1.96 | 64.2 | 42.1 | 0 | 0.0003 |
| 300 | ILP (Bộ 1 (Ưu tiên điểm phù hợp)) | 43.7% | 21.0% | 1.74 | 68.8 | 46.8 | 0 | 0.0374 |
| 300 | ILP (Bộ 2 (Cân bằng mặc định)) | 43.7% | 23.7% | 1.63 | 66.0 | 42.1 | 0 | 0.0354 |
| 300 | ILP (Bộ 3 (Ưu tiên nguyện vọng)) | 43.7% | 23.7% | 1.62 | 65.7 | 42.1 | 0 | 0.0408 |
| 1000 | Greedy | 37.6% | 14.6% | 1.87 | 64.7 | 42.5 | 0 | 0.0012 |
| 1000 | ILP (Bộ 1 (Ưu tiên điểm phù hợp)) | 39.3% | 19.5% | 1.69 | 67.1 | 46.3 | 0 | 0.1212 |
| 1000 | ILP (Bộ 2 (Cân bằng mặc định)) | 39.3% | 21.5% | 1.61 | 65.1 | 44.7 | 0 | 0.1199 |
| 1000 | ILP (Bộ 3 (Ưu tiên nguyện vọng)) | 39.3% | 21.6% | 1.61 | 65.0 | 44.3 | 0 | 0.1192 |

### (d) Đọc kết quả thế nào?

Ở cả ba quy mô, ILP có tỷ lệ xếp cao hơn Greedy và đặc biệt cải thiện tỷ lệ đạt NV1.

#### Quy mô 100 sinh viên

Greedy:

- tỷ lệ xếp 50.0%;
- đạt NV1 14.0%;
- điểm phù hợp trung bình 66.5.

ILP:

- tỷ lệ xếp 51.0%;
- NV1 từ 28.0% đến 31.0%.

Bộ 1 ưu tiên độ phù hợp cho điểm phù hợp trung bình cao nhất: **72.7**.

Bộ 2 và Bộ 3 cho NV1 cao nhất: **31.0%**.

#### Quy mô 300 sinh viên

Greedy:

- tỷ lệ xếp 43.0%;
- NV1 15.0%;
- điểm phù hợp 64.2.

ILP:

- tỷ lệ xếp 43.7%;
- NV1 từ 21.0% đến 23.7%.

Bộ 1 tiếp tục cho điểm phù hợp cao nhất: **68.8**.

#### Quy mô 1.000 sinh viên

Greedy:

- tỷ lệ xếp 37.6%;
- NV1 14.6%;
- điểm phù hợp 64.7.

ILP:

- tỷ lệ xếp 39.3%;
- NV1 từ 19.5% đến 21.6%.

Bộ 1 cho điểm phù hợp trung bình **67.1**.

Bộ 3 cho NV1 **21.6%**.

Thời gian ILP ở quy mô 1.000 sinh viên nằm trong khoảng:

- 0.1192 giây;
- 0.1199 giây;
- 0.1212 giây.

Greedy nhanh hơn rất nhiều, nhưng ILP vẫn chạy rất nhanh ở quy mô thử nghiệm này.

Một điểm quan trọng khác là toàn bộ các dòng trong bảng đều có:

> **Vi phạm = 0**

Tức là các phương án được ghi nhận không vượt những ràng buộc được kiểm tra trong thực nghiệm.

### (e) Giới hạn phải nói thật

Dữ liệu RQ3 là **dữ liệu sinh**, chưa phải một đợt đăng ký thực tế của EAUT.

Tỷ lệ xếp chỉ khoảng:

- 50.0%–51.0% ở N = 100;
- 43.0%–43.7% ở N = 300;
- 37.6%–39.3% ở N = 1.000.

Điều này không có nghĩa hệ thống thật sẽ chỉ xếp được từng đó sinh viên. Kết quả phụ thuộc trực tiếp vào dữ liệu mô phỏng, nguyện vọng, sức chứa đề tài và quota được tạo cho thực nghiệm.

Ngoài ra, không nên nói “ILP luôn tốt hơn ở mọi chỉ số”. Ví dụ khi ưu tiên nguyện vọng bằng Bộ 2 hoặc Bộ 3, điểm phù hợp trung bình có thể thấp hơn Bộ 1. Đây chính là sự đánh đổi giữa **độ phù hợp** và **nguyện vọng sinh viên**.

Thời gian khoảng 0.12 giây ở N = 1.000 chỉ là kết quả trên cấu hình và dữ liệu thực nghiệm hiện tại, không phải cam kết rằng mọi bài toán 1.000 sinh viên trong mọi điều kiện đều giải trong đúng thời gian đó.

### (f) Một câu để nói khi bảo vệ

> “RQ3 cho thấy ILP khai thác bài toán toàn cục tốt hơn Greedy về tỷ lệ xếp và NV1 trong dữ liệu thử nghiệm; ở 1.000 sinh viên ILP đạt 39.3% tỷ lệ xếp, tối đa 21.6% NV1, không có vi phạm và thời gian đo được khoảng 0.12 giây.”

---

## 5. Hạn chế khi triển khai thật

### 5.1. M5 phụ thuộc dịch vụ LLM

M5 không phải phép tính nội bộ đơn giản mà cần gọi LLM. Trong thử nghiệm, hệ thống sử dụng API thật và đã gặp giới hạn lượt gọi.

Với hạn mức Groq miễn phí hiện dùng, khả năng chấm M5 thực tế chỉ khoảng **45 sinh viên/ngày**.

Nếu một đợt đăng ký có nhiều sinh viên, không thể giả định rằng toàn bộ M5 sẽ được tính tức thời chỉ bằng tài khoản miễn phí.

### 5.2. Giải pháp triển khai

Hệ thống xử lý theo ba hướng:

**1. Cache kết quả**

Điểm M5 đã chấm được lưu lại. Nếu cùng dữ liệu đã có kết quả phù hợp trong cache thì không cần gọi LLM lại.

**2. Chấm dần**

M5 chỉ chấm trên danh sách Top 15 sau M1–M4 thay vì gọi LLM cho toàn bộ đề tài. Các sinh viên cũng có thể được xử lý dần thay vì dồn tất cả lượt gọi vào một thời điểm.

**3. API trả phí khi triển khai thật**

Nếu Khoa cần xử lý số lượng lớn trong thời gian ngắn, cần sử dụng hạn mức API trả phí hoặc hạ tầng có quota phù hợp thay vì phụ thuộc hoàn toàn vào gói miễn phí.

### Câu nói khi bảo vệ

> “Bản thử nghiệm dùng API miễn phí nên M5 bị giới hạn khoảng 45 sinh viên mỗi ngày; khi triển khai thật em dùng cache, chỉ chấm Top 15, xử lý dần và nếu cần tải lớn thì chuyển sang API trả phí.”
