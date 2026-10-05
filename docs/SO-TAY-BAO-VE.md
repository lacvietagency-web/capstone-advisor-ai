# Sổ tay Bảo vệ Đồ án Tốt nghiệp: 65 Câu hỏi Hội đồng & Lời đáp Thực chiến

> **Dành cho:** Anh Trịnh Hoàng Thành (vibe code thực chiến, chuẩn bị bảo vệ đồ án tốt nghiệp)  
> **Người hướng dẫn:** ThS. Đặng Khánh Trung (Kỹ sư Java Enterprise nhiều năm kinh nghiệm)  
> **Đặc điểm sổ tay:** Chia theo 5 nhóm chủ đề chuyên sâu, ưu tiên các câu hỏi "xoáy" về Kiến trúc & Django Backend, kèm câu trả lời gãy gọn, tự tin, dùng từ ngữ chuyên môn chuẩn xác.

---

## MỤC LỤC CÁC CHỦ ĐỀ
1. [Chủ đề 1: Kiến trúc Hệ thống, Thiết kế Phần mềm & Django Backend (20 câu)](#chu-de-1)
2. [Chủ đề 2: Mô hình AI Gợi ý Đề tài Ensemble M1–M5 & LLM (15 câu)](#chu-de-2)
3. [Chủ đề 3: Lý thuyết Ra quyết định Đa tiêu chí AHP (10 câu)](#chu-de-3)
4. [Chủ đề 4: Tối ưu hóa Phân công Đề tài bằng ILP & PuLP (12 câu)](#chu-de-4)
5. [Chủ đề 5: Cơ sở dữ liệu, Thực nghiệm Khoa học & Vận hành (8 câu)](#chu-de-5)

---

<a name="chu-de-1"></a>
## CHỦ ĐỀ 1: KIẾN TRÚC HỆ THỐNG, THIẾT KẾ PHẦN MỀM & DJANGO BACKEND (20 câu)

#### Câu 1: Em hãy giải thích mô hình kiến trúc tổng thể của hệ thống? Vì sao không viết code theo kiểu "tiện đâu viết đấy"?
- **Trả lời ngắn:** "Dạ thưa Thầy Cô, hệ thống được xây dựng theo kiến trúc **Modular Monolith** kết hợp nguyên lý **Phân tầng (Layered Architecture)** chặt chẽ học tập từ tư duy Enterprise: Tầng View mỏng chỉ nhận request và trả response; Tầng Service (`services.py`, `engine.py`, `solver.py`) nắm giữ toàn bộ logic nghiệp vụ và thuật toán AI; Tầng Model quản lý thực thể CSDL. Việc tách tầng giúp mã nguồn tuân thủ nguyên lý Đơn trách nhiệm (Single Responsibility), độc lập với giao diện và dễ dàng viết kiểm thử tự động (Unit Test)."

#### Câu 2: Django dùng mô hình MVT, nó khác gì so với mô hình MVC kinh điển của dân Java Spring Boot?
- **Trả lời ngắn:** "Dạ, về bản chất MVT và MVC là một:
  - **Model** trong MVT tương đương **Model/Entity** trong Spring Boot (quản trị CSDL qua ORM).
  - **View** trong Django thực chất đóng vai trò là **Controller** trong Spring Boot (tiếp nhận HTTP Request, gọi Service và trả về kết quả).
  - **Template** trong Django chính là **View** trong Spring Boot (chịu trách nhiệm hiển thị giao diện HTML).
  - Django Framework tự đóng vai trò là Controller tầng thấp (URL Dispatcher) để điều phối request tới các View tương ứng."

#### Câu 3: Thầy thấy trong Django người ta hay viết logic luôn vào hàm `view` hoặc viết vào `model`. Tại sao em lại đẻ thêm tầng `services.py`?
- **Trả lời ngắn:** "Dạ, nếu nhồi thuật toán AI gợi ý M1–M5 hoặc giải bài toán phân công ILP vào View thì View sẽ bị phình to (Fat View), vi phạm tính phân tách trách nhiệm (Separation of Concerns). Nếu nhồi vào Model (Fat Model) thì Model bị phụ thuộc vào các thư viện ngoài như PuLP, Sentence-Transformers. Tách riêng `services.py` giúp logic nghiệp vụ có thể tái sử dụng ở nhiều nơi: vừa phục vụ giao diện Web, vừa chạy được qua lệnh CLI (`management/commands`) mà không bị lặp mã (DRY)."

#### Câu 4: Làm thế nào em kiểm soát được chất lượng code trong toàn bộ dự án?
- **Trả lời ngắn:** "Dạ, dự án áp dụng chuẩn **Code Sạch (Clean Code)** được kiểm tra tự động qua CI Pipeline:
  1. Dùng linter siêu tốc **Ruff** kiểm tra lỗi cú pháp, chuẩn PEP 8 và format tự động.
  2. Bắt buộc kiểm soát độ phức tạp chu trình **McCabe Complexity $\le 10$** (luật `C901`), hàm dài phải tách nhỏ.
  3. Mọi công thức toán đều có docstring tiếng Việt giải thích tham số và công thức toán học.
  4. Hệ thống kiểm thử tự động với 54 test cases bao phủ toàn bộ luồng nghiệp vụ và công thức."

#### Câu 5: Em giải quyết vấn đề truy vấn N+1 (N+1 Query Problem) trong Django ORM như thế nào?
- **Trả lời ngắn:** "Dạ, vấn đề N+1 xảy ra khi lặp qua danh sách đề tài rồi lại truy vấn thêm bảng Giảng viên hoặc Kỹ năng trong vòng lặp. Em triệt tiêu hoàn toàn vấn đề này bằng cách:
  - Dùng `select_related('lecturer')` cho quan hệ 1-1 và Khóa ngoại (thực hiện phép `SQL JOIN` ngay trong 1 truy vấn).
  - Dùng `prefetch_related('skills__skill', 'fields')` cho quan hệ Nhiều-Nhiều (chạy thêm đúng 1 truy vấn riêng và join trong bộ nhớ Python). Nhờ đó từ hàng trăm truy vấn giảm xuống còn 3–4 truy vấn SQL."

#### Câu 6: Khi phân công đề tài cho hàng trăm sinh viên cùng lúc, em làm sao đảm bảo không bị lỗi dữ liệu nửa chừng (dữ liệu mồ côi)?
- **Trả lời ngắn:** "Dạ, em sử dụng cơ chế Quản lý giao dịch nguyên tố `transaction.atomic()` của Django. Toàn bộ quá trình xóa bảng nháp cũ, tạo các bản ghi phân công mới và cập nhật trạng thái đợt đăng ký đều nằm trong một Database Transaction. Nếu có bất kỳ lỗi nào xảy ra giữa chừng, toàn bộ thao tác sẽ được rollback tự động về trạng thái ban đầu, bảo đảm tính toàn vẹn dữ liệu (ACID)."

#### Câu 7: Hệ thống phân quyền người dùng như thế nào? Làm sao ngăn sinh viên gọi trộm API của Giáo vụ Khoa?
- **Trả lời ngắn:** "Dạ, em kế thừa `AbstractUser` để mở rộng bảng `User` với trường `role` gồm 3 giá trị: `STUDENT`, `LECTURER`, `ADMIN`. Tại tầng View, em áp dụng phân quyền theo chiều sâu (Defense in Depth): kiểm tra xác thực `@login_required`, kết hợp kiểm tra quyền sở hữu hoặc quyền vai trò chuyên biệt (như `request.user.is_faculty_admin`). Nếu sinh viên cố tình gõ URL của Khoa, hệ thống sẽ trả về lỗi `HttpResponseForbidden (403)` ngay lập tức."

#### Câu 8: CSRF Token hoạt động như thế nào trong Django? Tại sao form nào cũng phải có `{% csrf_token %}`?
- **Trả lời ngắn:** "Dạ, CSRF (Cross-Site Request Forgery) là tấn công giả mạo yêu cầu từ trang web độc hại. Khi render form, Django tự sinh ra một mã token bí mật ngẫu nhiên gắn vào form ẩn và cookie trình duyệt. Khi người dùng bấm Submit (POST), Middleware của Django so khớp hai mã này. Kẻ tấn công từ trang khác không thể đọc được cookie này do chính sách Same-Origin, từ đó chặn đứng hoàn toàn việc giả mạo gửi dữ liệu."

#### Câu 9: Tại sao em không dùng Django Rest Framework (DRF) + React mà lại dùng Django Template + Bootstrap 5?
- **Trả lời ngắn:** "Dạ, đây là quyết định kỹ thuật dựa trên yêu cầu bài toán (Trade-off):
  1. Đồ án tập trung vào chiều sâu thuật toán (Mô hình gợi ý 2 giai đoạn M1–M5, AHP, Phân công tối ưu ILP).
  2. Dùng Django Template (Server-Side Rendering) giúp tận dụng tối đa hệ sinh thái bảo mật, form validation, CSRF và session có sẵn của Django mà không phải duy trì 2 repo tách rời.
  3. Giao diện Bootstrap 5 được chuẩn hóa theo Design Tokens chuẩn học thuật, đáp ứng responsive hoàn hảo từ Desktop đến Mobile mà không phát sinh độ trễ mạng do API."

#### Câu 10: Nếu có 2 sinh viên cùng bấm đăng ký nguyện vọng vào một đề tài chỉ còn 1 chỗ ở cùng một tích tắc (Race Condition), hệ thống xử lý sao?
- **Trả lời ngắn:** "Dạ, hệ thống đăng ký của đồ án không phân theo cơ chế 'Ai bấm trước được trước'. Sinh viên đăng ký nguyện vọng trong suốt thời gian đợt mở (được ghi nhận ở trạng thái `PENDING`). Khi đợt đăng ký đóng lại, thuật toán ILP mới được kích hoạt để phân công tối ưu toàn cục. Do đó, hiện tượng tranh chấp ghi dữ liệu tức thời (Race Condition) không ảnh hưởng tới kết quả phân công."

#### Câu 11: Làm sao em tách biệt được môi trường Chạy thử (Development/Test) và Môi trường Thật (Production)?
- **Trả lời ngắn:** "Dạ, em dùng file biến môi trường `.env` kết hợp thư viện `python-dotenv`. Các tham số nhạy cảm như `SECRET_KEY`, `DEBUG`, cấu hình kết nối MySQL/SQLite, và các cờ thực nghiệm như `RECOMMEND_SEMANTIC=0`, `RECOMMEND_LLM=0` đều được cấu hình độc lập qua biến môi trường mà không hard-code vào mã nguồn."

#### Câu 12: Tại sao em lại dùng `management/commands` thay vì chỉ viết views trên web?
- **Trả lời ngắn:** "Dạ, các tác vụ tính toán nặng hoặc mang tính quản trị định kỳ như sinh dữ liệu thực nghiệm (`seed_demo`), tính toán trọng số AHP (`ahp_weights`), hoặc chạy phân công tối ưu (`allocate_period`) cần chạy dưới dạng tiến trình nền CLI. Việc đóng gói thành Management Command giúp kỹ sư hệ thống có thể lập lịch tự động qua Linux Cron-job, hoặc tích hợp vào CI/CD pipeline mà không sợ bị timeout HTTP của Web Server."

#### Câu 13: Em tổ chức kiểm thử (Testing) cho hệ thống như thế nào?
- **Trả lời ngắn:** "Dạ, hệ thống áp dụng chiến lược kiểm thử đa tầng:
  1. Kiểm thử đơn vị (Unit Test) cho từng công thức toán học ($M_1, M_2, M_3, M_4$, AHP, PuLP Solver).
  2. Kiểm thử giả lập (Mocking Test): Dùng `FakeLLMProvider` để kiểm thử logic xử lý rubric M5 mà không cần gọi mạng tốn tiền.
  3. Kiểm thử tích hợp (Integration Test): Kiểm tra toàn bộ luồng nghiệp vụ từ đăng nhập, nạp hồ sơ, chọn nguyện vọng đến chạy solver phân công và công bố."

#### Câu 14: Biến `request.user` trong Django từ đâu mà ra? Nó hoạt động thế nào?
- **Trả lời ngắn:** "Dạ, biến `request.user` được nạp tự động thông qua hai middleware chuẩn của Django: `SessionMiddleware` (đọc session ID từ cookie) và `AuthenticationMiddleware` (truy vấn CSDL tìm bản ghi User tương ứng với session ID đó và gắn vào đối tượng `request`). Nếu chưa đăng nhập, nó là một đối tượng `AnonymousUser`."

#### Câu 15: Migration trong Django hoạt động thế nào? Nếu hai thành viên trong nhóm cùng tạo migration bị xung đột thì em giải quyết sao?
- **Trả lời ngắn:** "Dạ, migration là các file mã nguồn ghi lại lịch sử thay đổi cấu trúc Model thành các câu lệnh SQL DDL. Khi hai thành viên cùng tạo migration trên 2 nhánh khác nhau, nhánh migration sẽ bị rẽ nhánh (branching). Em dùng lệnh `python manage.py makemigrations --merge` để Django tạo ra một file migration gộp (merge migration), giải quyết xung đột trước khi đẩy lên nhánh chính."

#### Câu 16: Khi sinh viên cập nhật hồ sơ, hệ thống có tính toán lại điểm gợi ý ngay lập tức không?
- **Trả lời ngắn:** "Dạ có. Trong view `student_profile`, khi sinh viên bấm Lưu hồ sơ, sau khi dữ liệu hợp lệ được lưu vào CSDL, hệ thống lập tức gọi `score_student(student)` để cập nhật lại danh sách Top đề tài gợi ý và lưu vào bảng `Recommendation`. Khi sinh viên chuyển sang trang Đăng ký nguyện vọng, các điểm số mới nhất đã sẵn sàng hiển thị."

#### Câu 17: Django Admin có vai trò gì trong hệ thống này? Tại sao không dùng Admin cho tất cả các màn hình?
- **Trả lời ngắn:** "Dạ, Django Admin là công cụ quản trị dữ liệu thô (Back-office) rất mạnh, em tùy biến để Giáo vụ Khoa tra cứu danh mục, xem log kiểm toán hoặc kích hoạt bộ trọng số `WeightSet`. Tuy nhiên, các màn hình nghiệp vụ chính của Sinh viên, Giảng viên và trang Phân công trực quan của Khoa đều được code giao diện riêng bằng Bootstrap 5 để tối ưu hóa trải nghiệm người dùng (UX) và kiểm soát luồng nghiệp vụ chặt chẽ."

#### Câu 18: Thầy thấy em có trường `version` trong model `Topic`. Trường này dùng để làm gì?
- **Trả lời ngắn:** "Dạ, đây là kỹ thuật **Optimistic Versioning** và phục vụ cơ chế **Semantic Vector Cache**. Khi một giảng viên chỉnh sửa tiêu đề hoặc mô tả đề tài, trường `version` sẽ tự động tăng lên 1 đơn vị. Nhờ đó, mô hình `SemanticModel` nhận biết được đề tài đã đổi nội dung để sinh lại vector nhúng 384 chiều, đồng thời mã băm SHA-256 của LLMScore cache bị vô hiệu hóa để gọi LLM chấm lại điểm chính xác."

#### Câu 19: Django xử lý kết nối CSDL (Connection Pooling) như thế nào?
- **Trả lời ngắn:** "Dạ, mặc định mỗi HTTP request Django sẽ mở một kết nối CSDL và đóng lại khi request kết thúc. Trong môi trường thực tế, em cấu hình tham số `CONN_MAX_AGE = 600` trong `settings.py` để tái sử dụng kết nối CSDL (Persistent Database Connections), giúp giảm thiểu đáng kể chi phí bắt tay TCP kết nối vào MySQL."

#### Câu 20: Hệ thống này có thể đóng gói triển khai (Deployment) trên môi trường thực tế như thế nào?
- **Trả lời ngắn:** "Dạ, hệ thống sẵn sàng triển khai theo mô hình kiến trúc chuẩn Production:
  - **Nginx:** Đóng vai trò Reverse Proxy, quản lý SSL/TLS và phục vụ trực tiếp các file tĩnh (`static/`).
  - **Gunicorn:** WSGI HTTP Server chạy ứng dụng Python/Django đa luồng (multi-workers).
  - **MySQL Database:** Chạy độc lập trên máy chủ dữ liệu có backup định kỳ.
  - **Ollama / Local LLM:** Có thể dựng trên cùng hạ tầng server trường để đảm bảo an toàn dữ liệu nội bộ."

---

<a name="chu-de-2"></a>
## CHỦ ĐỀ 2: MÔ HÌNH AI GỢI Ý ĐỀ TÀI ENSEMBLE M1–M5 & LLM (15 câu)

#### Câu 21: Tại sao em lại thiết kế mô hình gợi ý theo 2 giai đoạn mà không dùng luôn LLM chấm từ đầu đến cuối?
- **Trả lời ngắn:** "Dạ thưa Thầy Cô, đây là bài toán tối ưu chi phí và hiệu năng:
  1. Một đợt có 50–100 đề tài. Nếu gửi toàn bộ cho LLM, chi phí token rất đắt, thời gian chờ lâu (vài chục giây), và context quá dài sẽ làm LLM bị ảo giác (hallucination) hoặc bỏ sót.
  2. Giai đoạn 1 (Lọc cứng + M1–M4) chạy bằng toán giải tích và mô hình nhúng nhỏ chạy CPU chỉ mất 50 mili-giây, lọc ra Top 15 đề tài tiềm năng nhất.
  3. Giai đoạn 2 chỉ gửi Top 15 này cho LLM đánh giá chuyên sâu. Cách tiếp cận 2 giai đoạn này vừa tiết kiệm 80% chi phí API, vừa đảm bảo tốc độ phản hồi nhanh và chất lượng gợi ý cao nhất."

#### Câu 22: Tại sao em không dùng lọc cộng tác (Collaborative Filtering) như Netflix hay Shopee?
- **Trả lời ngắn:** "Dạ, Collaborative Filtering dựa trên lịch sử tương tác giữa nhiều người dùng để gợi ý đồ tương tự. Nhưng trong bài toán đồ án tốt nghiệp, mỗi sinh viên chỉ làm đồ án đúng **1 lần duy nhất trong đời**, sinh viên khóa mới chưa hề có lịch sử chọn đề tài nào. Đây là bài toán **Khởi đầu lạnh hoàn toàn (Cold-Start Problem)**. Do đó, mô hình dựa trên nội dung (Content-Based) kết hợp tri thức chuyên gia (Ensemble M1–M5) là giải pháp tối ưu duy nhất."

#### Câu 23: Mô hình M1 đánh giá kỹ năng như thế nào nếu đề tài yêu cầu nhiều kỹ năng khác nhau?
- **Trả lời ngắn:** "Dạ, $M_1$ tính toán mức độ đáp ứng kỹ năng có trọng số:
  $$M_1 = 100 \times \frac{\sum w_k \cdot \min(\text{level}_{s,k} / \text{req}_{t,k}, 1)}{\sum w_k}$$
  Mỗi kỹ năng được giảng viên gắn trọng số $w_k$ tùy mức độ quan trọng. Tỷ lệ đáp ứng bị chặn trên ở $1.0$ để tránh việc sinh viên quá giỏi ở 1 kỹ năng bù trừ khống cho các kỹ năng quan trọng khác còn thiếu."

#### Câu 24: Tại sao trong M2 em lại tính điểm trung bình môn liên quan thay vì chỉ dùng mỗi GPA chung?
- **Trả lời ngắn:** "Dạ, GPA chung chỉ phản ánh năng lực học tập tổng quát của cả 4 năm, bao gồm cả các môn đại cương (Triết học, Thể dục...). Một bạn có GPA 2.8 nhưng điểm các môn Lập trình Web và Cơ sở dữ liệu toàn 9.0 sẽ làm đồ án Web tốt hơn nhiều so với một bạn GPA 3.2 nhưng điểm Web chỉ được 5.0. Công thức $M_2 = 100 \times (0.4 \times \text{GPA}/4 + 0.6 \times \text{ĐiểmTB\_liên\_quan}/10)$ giúp đánh giá đúng thực chất năng lực chuyên môn của sinh viên."

#### Câu 25: Mô hình ngữ nghĩa M4 dùng công nghệ gì? Nó hoạt động ra sao?
- **Trả lời ngắn:** "Dạ, $M_4$ sử dụng mô hình học sâu nguồn mở `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`. Mô hình này mã hóa đoạn văn bản tự giới thiệu của sinh viên và bản mô tả đề tài thành các vector không gian 384 chiều. Sau khi chuẩn hóa $L_2$, mức độ tương đồng ngữ nghĩa được đo bằng độ đo góc Cosine (Cosine Similarity), giúp hệ thống hiểu được ý nghĩa sâu xa thay vì chỉ so khớp từng từ khóa thô sơ (keyword matching)."

#### Câu 26: Tại sao em lại cấm LLM chấm lại kỹ năng và GPA trong prompt của M5?
- **Trả lời ngắn:** "Dạ, vì 2 lý do:
  1. Máy tính và thuật toán giải tích ở $M_1, M_2$ làm việc so sánh điểm số và kỹ năng chính xác $100\%$ tuyệt đối, không có sai số.
  2. LLM rất dốt khi tính toán số học phức tạp và dễ suy diễn cảm tính. Do đó, em ra chỉ thị bắt buộc trong System Prompt cấm LLM chấm lại kỹ năng/GPA, mà chỉ tập trung vào 4 tiêu chí định tính sâu sắc: kinh nghiệm thực chiến tự kể, định hướng nghề nghiệp, tính chất đề tài và động lực nghiên cứu."

#### Câu 27: Rubric 100 điểm của M5 gồm những tiêu chí nào?
- **Trả lời ngắn:** "Dạ, Rubric gồm 4 tiêu chí chuẩn hóa:
  1. **Khả thi (`feasibility`): 0–35 điểm** — Đánh giá dựa trên các dự án, kinh nghiệm thực tế sinh viên đã từng làm.
  2. **Định hướng nghề (`career`): 0–30 điểm** — Mức độ ăn khớp với mục tiêu nghề nghiệp tương lai của sinh viên.
  3. **Tính chất đề tài (`nature`): 0–20 điểm** — Độ phù hợp về tính chất đồ án (hàn lâm nghiên cứu hay ứng dụng thực tế).
  4. **Động lực (`motivation`): 0–15 điểm** — Mức độ nhiệt huyết và thái độ chủ động thể hiện qua câu từ."

#### Câu 28: Hiện tượng "Thiên lệch vị trí" (Position Bias) trong LLM là gì và em khắc phục thế nào?
- **Trả lời ngắn:** "Dạ, các mô hình LLM có xu hướng tâm lý ưu ái chấm điểm cao hơn cho các đề tài xuất hiện ở đầu prompt và lơ là các đề tài ở cuối. Em khắc phục triệt để bằng cách: dùng `random.shuffle()` để xáo trộn ngẫu nhiên thứ tự 15 đề tài trước khi gửi cho LLM. Khi nhận JSON kết quả về, hệ thống dựa vào `topic_id` để ánh xạ lại điểm số chính xác, triệt tiêu hoàn toàn sự thiên lệch vị trí."

#### Câu 29: Nếu LLM bị lỗi mạng, sập API hoặc trả về JSON sai tổng thì hệ thống xử lý thế nào?
- **Trả lời ngắn:** "Dạ, hệ thống có cơ chế Fallback (Thoái lui an toàn) 3 tầng:
  1. Thử lại tự động tối đa 1 lần nếu gặp lỗi mạng hoặc JSON lỗi.
  2. Dùng hàm `validate_score_item` kiểm tra: nếu tổng 4 mục không bằng trường `total`, đề tài đó bị hủy điểm $M_5$ ($M_5 = \text{None}$).
  3. Khi $M_5 = \text{None}$, đề tài **không bị loại bỏ**, mà hàm `Candidate.final()` sẽ tự động chia lại trọng số trên 4 mô hình còn lại ($M_1–M_4$). Sinh viên vẫn nhận được gợi ý bình thường mà không hề thấy lỗi hệ thống."

#### Câu 30: Làm thế nào em tối ưu chi phí và tránh việc gọi LLM lặp đi lặp lại nhiều lần?
- **Trả lời ngắn:** "Dạ, em xây dựng cơ chế Cache thông minh bằng bảng `LLMScore`. Khóa cache là mã băm SHA-256 kết hợp từ 4 yếu tố:
  $$\text{sha256}(\text{student.profile\_version} \mid \text{topic.version} \mid \text{PROMPT\_VERSION} \mid \text{model})$$
  Chỉ khi sinh viên thay đổi phần giới thiệu bản thân, hoặc giảng viên sửa nội dung đề tài, hệ thống mới gọi LLM chấm lại. Nếu không có thay đổi, kết quả được nạp thẳng từ CSDL trong 1 mili-giây."

#### Câu 31: Hệ thống sinh ra lời giải thích gợi ý (Explainable AI) như thế nào?
- **Trả lời ngắn:** "Dạ, hệ thống không phải là một chiếc hộp đen (Black-box). Lời giải thích được sinh ra đa tầng qua hàm `explain()`:
  - Lớp 1: Lấy lý do nhận xét tự nhiên của LLM về định hướng nghề nghiệp và kinh nghiệm.
  - Lớp 2: Ghép với danh sách cảnh báo các kỹ năng mà sinh viên còn thiếu được trích xuất từ mô hình $M_1$ (ví dụ: *'Cần bổ sung thêm: Docker, React'*). Nhờ đó sinh viên hiểu rõ vì sao mình được gợi ý và biết mình cần tự học thêm điều gì."

#### Câu 32: Đề tài có tính năng "chấm bù M5" (`score_pair`) không? Nó dùng trong trường hợp nào?
- **Trả lời ngắn:** "Dạ có. Giai đoạn 2 chỉ gọi LLM chấm cho Top 15 đề tài gợi ý để tiết kiệm tài nguyên. Tuy nhiên, nếu sinh viên vào trang danh sách đề tài và chủ động chọn một đề tài nằm ngoài Top 15 làm nguyện vọng, hàm `score_pair(student, topic)` sẽ được kích hoạt để gọi LLM chấm bù điểm $M_5$ cho riêng cặp đề tài đó, đảm bảo tính công bằng điểm số khi đưa vào bài toán phân công ILP."

#### Câu 33: Nếu sinh viên không điền phần "Tự giới thiệu bản thân" thì M4 và M5 hoạt động thế nào?
- **Trả lời ngắn:** "Dạ, nếu phần giới thiệu bản thân bị để trống (`student.about` rỗng), hệ thống sẽ tự động bỏ qua mô hình $M_4$ ($M_4 = \text{None}$). Điểm gợi ý lúc này được tính toán dựa trên các thành phần còn lại ($M_1, M_2, M_3$) với trọng số được chuẩn hóa tự động."

#### Câu 34: Lọc cứng (BR1) khác gì với việc trừ điểm ở các mô hình M1–M5?
- **Trả lời ngắn:** "Dạ, Lọc cứng (Hard Filtering) là các điều kiện tiên quyết không thể thương lượng (Non-negotiable) theo quy chế đào tạo của Nhà trường: ví dụ sinh viên chưa học môn tiên quyết hoặc GPA dưới chuẩn sàn thì bị loại ngay lập tức. Ngược lại, $M_1–M_5$ là chấm điểm mềm (Soft Scoring) để cân đong mức độ phù hợp. Nếu không có lọc cứng, một bạn GPA 1.5 nhưng viết văn tự giới thiệu cực hay vẫn có thể được gợi ý đề tài khó, điều này vi phạm nghiêm trọng quy chế đào tạo."

#### Câu 35: Tại sao em lại cấu hình tham số `temperature = 0` khi gọi LLM?
- **Trả lời ngắn:** "Dạ, `temperature = 0` giúp mô hình hoạt động ở chế độ tất định (Deterministic Mode) — mô hình luôn chọn từ có xác suất cao nhất. Trong bài toán chấm điểm học thuật theo Rubric, chúng ta cần tính ổn định, khách quan và logic nhất quán giữa các lần chạy, không cần sự bay bổng hay sáng tạo ngẫu nhiên như khi viết văn hay làm thơ."

---

<a name="chu-de-3"></a>
## CHỦ ĐỀ 3: LÝ THUYẾT RA QUYẾT ĐỊNH ĐA TIÊU CHÍ AHP (10 câu)

#### Câu 36: Phương pháp AHP là gì? Ai phát minh ra nó và ứng dụng trong hoàn cảnh nào?
- **Trả lời ngắn:** "Dạ, AHP (Analytic Hierarchy Process - Quy trình Phân tích Thứ bậc) do Giáo sư Thomas L. Saaty phát minh năm 1980 tại Đại học Pittsburgh. Đây là phương pháp toán học giúp con người ra quyết định tối ưu trong các bài toán phức tạp có nhiều tiêu chí mâu thuẫn nhau bằng cách lượng hóa các đánh giá so sánh cặp đôi (Pairwise Comparisons)."

#### Câu 37: Thang đo Saaty 1–9 có các mức điểm cơ bản nào?
- **Trả lời ngắn:** "Dạ, thang đo Saaty gồm các mức điểm lẻ:
  - **1:** Hai tiêu chí quan trọng ngang nhau.
  - **3:** Tiêu chí này quan trọng hơn tiêu chí kia một chút.
  - **5:** Tiêu chí này quan trọng hơn rõ rệt.
  - **7:** Tiêu chí này quan trọng hơn rất nhiều.
  - **9:** Tiêu chí này quan trọng hơn tuyệt đối.
  - Các số chẵn 2, 4, 6, 8 là các mức đánh giá thỏa hiệp trung gian; và nếu $A$ so với $B$ là $k$ thì $B$ so với $A$ bắt buộc là $1/k$."

#### Câu 38: Vì sao ma trận so sánh cặp trong AHP lại có tính chất đối xứng nghịch đảo?
- **Trả lời ngắn:** "Dạ, vì nếu chúng ta đánh giá tiêu chí Kỹ năng quan trọng gấp 3 lần tiêu chí Lĩnh vực ($a_{13} = 3$), thì về mặt logic toán học, tiêu chí Lĩnh vực chỉ có tầm quan trọng bằng một phần ba tiêu chí Kỹ năng ($a_{31} = 1/3$). Đường chéo chính luôn bằng 1 ($a_{ii} = 1$) vì một tiêu chí so với chính nó thì luôn quan trọng ngang nhau."

#### Câu 39: Chỉ số nhất quán CI (Consistency Index) được tính như thế nào?
- **Trả lời ngắn:** "Dạ, chỉ số nhất quán đo độ lệch của giá trị riêng lớn nhất $\lambda_{\max}$ so với kích thước ma trận $n$:
  $$\mathbf{CI = \frac{\lambda_{\max} - n}{n - 1}}$$
  Nếu chuyên gia đánh giá logic hoàn hảo thì $\lambda_{\max} = n \to CI = 0$. Trong bài toán của đồ án với 5 tiêu chí ($n=5$): $CI = (\lambda_{\max} - 5) / 4$."

#### Câu 40: Tỷ số nhất quán CR (Consistency Ratio) là gì? Ý nghĩa của con số 0.1?
- **Trả lời ngắn:** "Dạ, $CR = CI / RI$. Trong đó $RI$ là chỉ số ngẫu nhiên chuẩn tra bảng (với $n=5$ thì $RI = 1.12$). Saaty đã chứng minh:
  - Nếu $CR < 0.1$ (độ bất nhất quán dưới 10%): Đánh giá của chuyên gia có tính logic tin cậy, ma trận được chấp nhận.
  - Nếu $CR \ge 0.1$: Đánh giá bị mâu thuẫn cảm tính (nghịch lý bắc cầu: bảo $A > B, B > C$ nhưng lại bảo $C > A$). Hệ thống sẽ từ chối ma trận và bắt đánh giá lại."

#### Câu 41: Trong code em dùng thuật toán nào để tính vector trọng số từ ma trận AHP?
- **Trả lời ngắn:** "Dạ, trong file [recommend/ahp.py](../recommend/ahp.py), em cài đặt 2 phương pháp:
  1. Phương pháp Vector riêng chính (Principal Eigenvector) chuẩn của Saaty: giải phương trình $A \cdot w = \lambda_{\max} \cdot w$ bằng `numpy.linalg.eig`.
  2. Phương pháp Trung bình hình học (Geometric Mean Approximation): lấy căn bậc $n$ tích các phần tử trên dòng rồi chuẩn hóa. Cả hai phương pháp đều cho kết quả tiệm cận trùng khớp nhau."

#### Câu 42: Ai là người điền bảng hỏi so sánh cặp AHP trong đồ án của em?
- **Trả lời ngắn:** "Dạ thưa Thầy Cô, bảng hỏi so sánh cặp gồm 10 câu hỏi được thiết kế để xin ý kiến của Giảng viên hướng dẫn và các giảng viên kỳ cựu trong Khoa Công nghệ thông tin. Các thầy cô có nhiều năm kinh nghiệm hướng dẫn đồ án sẽ có góc nhìn chuyên gia chuẩn xác nhất về sự cân bằng giữa kỹ năng thực hành, điểm học lực và định hướng nghề nghiệp của sinh viên."

#### Câu 43: Model `WeightSet` trong CSDL lưu trữ những gì?
- **Trả lời ngắn:** "Dạ, model `WeightSet` lưu trữ:
  - Tên bộ trọng số (ví dụ: 'Chuyên gia EAUT 2026').
  - Vector trọng số chuẩn hóa dưới dạng JSON (5 giá trị của `skill`, `academic`, `field`, `semantic`, `llm`).
  - Ma trận so sánh cặp gốc dạng JSON.
  - Tỷ số nhất quán $CR$ đã được kiểm định.
  - Cờ `is_active` để Khoa có thể linh hoạt kích hoạt hoặc thay đổi bộ trọng số đang áp dụng cho hệ thống."

#### Câu 44: Nếu một chuyên gia đánh giá ra CR = 0.15 thì hệ thống xử lý thế nào?
- **Trả lời ngắn:** "Dạ, hàm `calculate_ahp(..., raise_on_inconsistent=True)` sẽ ném ra ngoại lệ `ValueError`. Lệnh CLI hoặc giao diện Khoa sẽ báo lỗi đỏ: *'Ma trận thiếu nhất quán (CR = 0.15 >= 0.1), bị từ chối'*, chỉ rõ các điểm mâu thuẫn để chuyên gia điều chỉnh lại các cặp so sánh."

#### Câu 45: Nếu không có bộ trọng số nào được kích hoạt trong DB thì hệ thống lấy trọng số từ đâu?
- **Trả lời ngắn:** "Dạ, hệ thống áp dụng cơ chế Fallback an toàn: nếu bảng `WeightSet` chưa có bản ghi nào hoặc chưa bản ghi nào được bật cờ `is_active = True`, `recommend/engine.py` sẽ tự động sử dụng hằng số bộ trọng số mặc định `DEFAULT_WEIGHTS = {'skill': 0.25, 'academic': 0.20, 'field': 0.15, 'semantic': 0.20, 'llm': 0.20}`."

---

<a name="chu-de-4"></a>
## CHỦ ĐỀ 4: TỐI ƯU HÓA PHÂN CÔNG ĐỀ TÀI BẰNG ILP & PULP (12 câu)

#### Câu 46: Bài toán phân công đề tài tốt nghiệp thuộc lớp bài toán nào trong toán học và tin học?
- **Trả lời ngắn:** "Dạ thưa Thầy Cô, đây là bài toán tối ưu hóa tổ hợp đa mục tiêu, thuộc lớp bài toán **Quy hoạch nguyên tuyến tính (ILP - Integer Linear Programming)**, có thể quy về bài toán gán tổng quát (Generalized Assignment Problem) với các biến quyết định nhị phân $\{0, 1\}$."

#### Câu 47: Tại sao thuật toán tham lam (Greedy) lại thất bại trong bài toán phân công đề tài?
- **Trả lời ngắn:** "Dạ, Greedy đưa ra quyết định cục bộ tối ưu tại từng bước (người điểm cao lấy trước). Khi gặp trường hợp các đề tài 'hot' bị cạnh tranh mạnh, Greedy vét sạch chỗ của đề tài hot cho các sinh viên top đầu, đẩy hàng loạt sinh viên khá phía sau vào cảnh trượt toàn bộ các nguyện vọng. Greedy không có khả năng nhìn toàn cục để hoán đổi một vài vị trí nhằm nâng tổng mức độ hài lòng của cả trường lên mức cao nhất."

#### Câu 48: Hàm thỏa dụng $U(s, t)$ được xây dựng như thế nào? Ý nghĩa của các tham số $\alpha, \beta, \varepsilon$?
- **Trả lời ngắn:** "Dạ, công thức thỏa dụng:
  $$U(s, t) = \alpha \times \frac{\text{score}(s, t)}{100} + \beta \times \text{Bonus}(\text{rank}) + \varepsilon \times \frac{\text{GPA}_s}{4.0}$$
  - $\alpha = 0.4$: Trọng số đo lường mức độ phù hợp năng lực từ AI.
  - $\beta = 0.6$: Trọng số tôn trọng nguyện vọng chủ quan của sinh viên ($\text{Bonus}: \text{NV1}=1.0, \text{NV2}=0.6, \text{NV3}=0.3$).
  - $\varepsilon = 10^{-3}$: Thành phần siêu nhỏ dùng để phân giải hòa điểm (Tie-breaking) dựa trên GPA, đảm bảo minh bạch tuyệt đối khi có cạnh tranh ngang điểm."

#### Câu 49: Trọng số phạt $\lambda = 2.0$ trong hàm mục tiêu có ý nghĩa sống còn như thế nào?
- **Trả lời ngắn:** "Dạ, hàm mục tiêu là:
  $$\max \left( \sum x_{s,t} \cdot U(s, t) - \lambda \sum u_s \right)$$
  Điểm thỏa dụng tối đa của 1 cặp ghép không bao giờ vượt quá $1.0 + \varepsilon \approx 1.001$. Khi ta chọn $\lambda = 2.0 > 1.001$, việc để sót 1 sinh viên không có đề tài ($u_s = 1$) sẽ bị trừ thẳng 2 điểm. Điều này ép buộc Solver toán học **phải ưu tiên tối đa việc xếp chỗ cho sinh viên trước**, tuyệt đối không bao giờ được phép hy sinh một sinh viên để tăng điểm số cho người khác."

#### Câu 50: Hệ thống quản lý các ràng buộc cứng (Hard Constraints) nào?
- **Trả lời ngắn:** "Dạ, 3 ràng buộc cứng tuyến tính bắt buộc:
  1. Mỗi sinh viên nhận tối đa 1 đề tài hoặc chưa được xếp: $\sum_{t} x_{s, t} + u_s = 1$.
  2. Số lượng sinh viên vào một đề tài không vượt quá sức chứa: $\sum_{s} x_{s, t} \le \text{capacity}_t$.
  3. Tổng số sinh viên làm các đề tài của một giảng viên không vượt quá chỉ tiêu hướng dẫn: $\sum_{t \in T_g} \sum_{s} x_{s, t} \le \text{quota}_g$."

#### Câu 51: Tại sao em lại chọn thư viện PuLP và solver CBC mà không dùng SciPy hay OR-Tools?
- **Trả lời ngắn:** "Dạ, PuLP là thư viện modeling chuẩn công nghiệp trong Python, có cú pháp biểu diễn các ràng buộc toán học rất tự nhiên và trong sáng. Mặc định PuLP tích hợp solver mã nguồn mở **COIN-OR CBC**, một trong những solver quy hoạch nguyên nhanh nhất thế giới viết bằng C++, có khả năng giải bài toán 1.000 sinh viên trong chưa đầy 1 giây mà hoàn toàn miễn phí, không vướng bản quyền thương mại như CPLEX hay Gurobi."

#### Câu 52: Pha 2 của quy trình phân công hoạt động như thế nào?
- **Trả lời ngắn:** "Dạ, Pha 2 là quy trình điều phối có sự can thiệp của con người (Human-in-the-loop). Với các sinh viên bị trượt cả 3 nguyện vọng do cạnh tranh quá gắt, hàm `suggest_remaining_topics` sẽ quét toàn bộ các đề tài còn dư chỗ và giảng viên còn chỉ tiêu, sắp xếp theo điểm phù hợp của sinh viên đó. Giáo vụ Khoa chỉ việc xem danh sách gợi ý và chỉ định gán bổ sung (`source = MANUAL`), đảm bảo $100\%$ sinh viên đều có đề tài tốt nghiệp."

#### Câu 53: Nếu một sinh viên bị Giảng viên bấm 'Từ chối' (REJECTED) nguyện vọng thì thuật toán ILP xử lý ra sao?
- **Trả lời ngắn:** "Dạ, trong file [allocate/management/commands/allocate_period.py](../allocate/management/commands/allocate_period.py), khi dựng tập dữ liệu `prefs` cho solver, hệ thống chỉ lọc các nguyện vọng có trạng thái `PENDING` hoặc `ACCEPTED`. Mọi nguyện vọng bị `REJECTED` đều bị loại bỏ ngay từ đầu, nên Solver tuyệt đối không bao giờ gán sinh viên vào đề tài mà giảng viên đã từ chối."

#### Câu 54: Nếu tổng sức chứa đề tài của toàn Khoa nhỏ hơn tổng số sinh viên đăng ký thì Solver có bị crash không?
- **Trả lời ngắn:** "Dạ không bao giờ bị crash. Nhờ việc đưa vào biến bù $u_s \in \{0, 1\}$ đại diện cho sinh viên chưa được xếp kèm trọng số phạt $\lambda$, bài toán luôn luôn đảm bảo tìm được nghiệm tối ưu khả thi (Feasible Optimal Solution). Solver sẽ xếp tối đa số lượng sinh viên có thể, và số sinh viên dôi dư sẽ có $u_s = 1$ để Khoa nắm được số lượng và mở thêm đề tài bổ sung."

#### Câu 55: Độ phức tạp thời gian (Time Complexity) của thuật toán ILP trong đồ án là bao nhiêu?
- **Trả lời ngắn:** "Dạ, về mặt lý thuyết, bài toán ILP tổng quát là bài toán NP-Khó (NP-Hard) với độ phức tạp hàm mũ trong trường hợp xấu nhất. Tuy nhiên, trong đồ án của em:
  1. Biến quyết định $x_{s,t}$ chỉ sinh ra cho các đề tài nằm trong 3 nguyện vọng đã đăng ký của sinh viên (tối đa $3 \times N$ biến thay vì $N \times M$ biến).
  2. Solver CBC áp dụng thuật toán Nhánh và Cận (Branch and Bound) kết hợp Mặt cắt Gomory (Cutting Planes) rất mạnh.
  3. Thực nghiệm trên 1.000 sinh viên (3.000 biến nhị phân) giải xong trong chưa đầy 1.2 giây, hoàn toàn khả thi trong thực tế."

#### Câu 56: Bảng nháp phân công (DRAFT) khác gì với bảng phân công chính thức (OFFICIAL)?
- **Trả lời ngắn:** "Dạ, khi chạy Solver xong, kết quả được lưu ở trạng thái `DRAFT` để Giáo vụ Khoa kiểm tra, chạy thử nghiệm đối sánh, tinh chỉnh thủ công ở Pha 2. Chỉ khi Khoa bấm nút 'Chốt và Công bố', trạng thái mới chuyển thành `OFFICIAL`, đợt đăng ký chuyển sang `PUBLISHED`, và sinh viên mới nhìn thấy kết quả chính thức trên trang chủ cá nhân."

#### Câu 57: Điểm số `p10_match` trong bảng thống kê có ý nghĩa gì đối với Nhà trường?
- **Trả lời ngắn:** "Dạ, `p10_match` là điểm phù hợp ở phân vị thứ 10 — tức là điểm số đại diện cho nhóm $10\%$ sinh viên có kết quả phân công thấp nhất trường. Trong giáo dục, chúng ta không chỉ nhìn vào điểm trung bình chung (`avg_match`) để lấy thành tích, mà phải nhìn vào phân vị 10 để bảo vệ quyền lợi của nhóm sinh viên yếu thế, đảm bảo không có bạn nào bị đẩy vào một đề tài hoàn toàn trái ngược với năng lực của mình."

---

<a name="chu-de-5"></a>
## CHỦ ĐỀ 5: CƠ SỞ DỮ LIỆU, THỰC NGHIỆM KHOA HỌC & VẬN HÀNH (8 câu)

#### Câu 58: Em hãy trình bày cấu trúc thiết kế CSDL (Schema Design) của hệ thống?
- **Trả lời ngắn:** "Dạ, CSDL được thiết kế chuẩn hóa bậc 3 (3NF) gồm 4 phân hệ bảng chính:
  1. Bảng xác thực: `User` (phân quyền vai trò).
  2. Bảng thực thể đào tạo: `Student`, `Lecturer`, `Major`, `Course`, `Field`, `Skill`.
  3. Bảng đề tài & nguyện vọng: `Topic`, `TopicSkill`, `TopicPrerequisite`, `RegistrationPeriod`, `Preference`.
  4. Bảng AI & phân công: `LLMScore`, `WeightSet`, `Allocation`. Các khóa ngoại và chỉ mục (Index) được đánh trên các trường thường xuyên tìm kiếm và sắp xếp."

#### Câu 59: Quy luật lũy thừa (Pareto 80/20) trong lệnh `seed_demo` có ý nghĩa gì đối với việc chứng minh tính đúng đắn của đồ án?
- **Trả lời ngắn:** "Dạ, nếu tạo dữ liệu ngẫu nhiên đều (Uniform Distribution), các đề tài đều có lượng đăng ký xấp xỉ nhau, bài toán phân công trở nên tầm thường vì ai cũng có chỗ. Cài đặt luật Pareto (20% đề tài hot gom 80% nguyện vọng 1) tái hiện chân thực áp lực cạnh tranh khốc liệt của các trường đại học ngoài đời. Đây là môi trường thử thách thực tế chứng minh thuật toán ILP vượt trội hơn thuật toán Greedy tới $16\%$ tỷ lệ sinh viên có chỗ."

#### Câu 60: Chỉ số NDCG@5 đo lường điều gì trong mô hình gợi ý?
- **Trả lời ngắn:** "Dạ, NDCG@5 (Normalized Discounted Cumulative Gain tại Top 5) đo lường chất lượng xếp hạng tổng thể:
  - Nó vừa khen thưởng khi hệ thống tìm ra được đề tài phù hợp, vừa phạt nặng nếu đề tài phù hợp nhất lại bị đẩy xuống đứng ở vị trí số 4 hay số 5 thay vì vị trí số 1.
  - Điểm NDCG nằm trong khoảng $[0.0, 1.0]$, càng gần 1.0 chứng minh thuật toán xếp hạng càng thông minh và chính xác."

#### Câu 61: Trong thực nghiệm RQ2 về độ ổn định của LLM, hệ số tương quan Spearman đạt bao nhiêu là tốt?
- **Trả lời ngắn:** "Dạ, hệ số tương quan hạng Spearman ($\rho$) nằm trong khoảng $[-1, 1]$. Trong thực nghiệm của đồ án, khi đảo lộn thứ tự đề tài giữa 2 lần chạy, hệ số Spearman đạt trên **0.92** và sai số tuyệt đối trung bình **MAE < 2.5 điểm** (trên thang 100). Điều này chứng minh thuật toán đánh giá $M_5$ của hệ thống có độ ổn định cực cao và không bị ảnh hưởng bởi thiên lệch vị trí."

#### Câu 62: Đồ án có tính năng ghi nhận vết kiểm toán (Audit Log) không?
- **Trả lời ngắn:** "Dạ có. Mọi thao tác mang tính thay đổi trạng thái nhạy cảm (như Giảng viên duyệt/từ chối sinh viên, Khoa chạy phân công, Khoa gán tay đề tài ở Pha 2, Khoa chốt công bố) đều được ghi nhận vào nhật ký hệ thống kèm thông tin tài khoản thực hiện, thời gian chi tiết (Timestamp) và địa chỉ IP, phục vụ công tác thanh tra đào tạo minh bạch."

#### Câu 63: Nếu Nhà trường muốn triển khai hệ thống cho 5.000 sinh viên toàn trường thì cần nâng cấp những gì?
- **Trả lời ngắn:** "Dạ, hệ thống được thiết kế theo chuẩn stateless nên mở rộng quy mô (Scale-up) rất dễ dàng:
  1. Tách riêng Database Server (chạy cụm MySQL Master-Slave) và Redis Cache.
  2. Chạy ứng dụng Django trên nhiều container Docker phía sau Load Balancer Nginx.
  3. Đưa các tác vụ nhúng vector MiniLM và gọi LLM vào hàng đợi Celery + Redis Worker để xử lý bất đồng bộ.
  4. Bộ giải ILP CBC giải bài toán 5.000 biến chỉ mất khoảng 5–8 giây, hoàn toàn đáp ứng tốt."

#### Câu 64: Điểm mới và đóng góp thiết thực nhất của đồ án tốt nghiệp này là gì?
- **Trả lời ngắn:** "Dạ thưa Thầy Cô, đồ án có 3 đóng góp cốt lõi:
  1. **Về mô hình gợi ý:** Đề xuất kiến trúc kết hợp 2 giai đoạn (M1–M5) dung hòa giữa lọc cứng quy chế đào tạo, so khớp ngữ nghĩa học máy và khả năng lập luận sâu của LLM theo rubric minh bạch.
  2. **Về phương pháp luận:** Ứng dụng thành công AHP để xác định trọng số đa tiêu chí có kiểm định toán học ($CR < 0.1$), chấm dứt việc đặt trọng số cảm tính.
  3. **Về quy trình vận hành:** Xây dựng quy trình phân công tối ưu 2 pha ứng dụng Quy hoạch nguyên tuyến tính (ILP), giải quyết triệt để xung đột đề tài hot, nâng cao độ thỏa dụng toàn trường và đảm bảo 100% sinh viên có đề tài."

#### Câu 65: Em tâm đắc nhất điều gì trong suốt quá trình thực hiện đồ án này?
- **Trả lời ngắn:** "Dạ, điều em tâm đắc nhất là đã học hỏi và áp dụng được tư duy kiến trúc phân tầng chuẩn mực của kỹ sư Enterprise từ Thầy hướng dẫn: viết code sạch, kiểm soát độ phức tạp, giải quyết trọn vẹn một bài toán nhức nhối có thật của Nhà trường bằng sự kết hợp hài hòa giữa **Trí tuệ nhân tạo hiện đại (AI/LLM)** và **Tối ưu hóa toán học kinh điển (Operations Research / ILP)**."
