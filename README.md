# Capstone Advisor AI

Hệ thống thông minh hỗ trợ tư vấn và tối ưu hóa quy trình đăng ký đồ án tốt nghiệp.
Đề tài sinh viên nghiên cứu khoa học 2026–2027 — SV Trịnh Hoàng Thành (20231337, DCCNTT14.4) · GVHD ThS. Đặng Khánh Trung ·
Khoa CNTT, Trường Đại học Công nghệ Đông Á (EAUT).

## Chức năng theo vai trò
- **Sinh viên:** hồ sơ năng lực (kỹ năng, lĩnh vực quan tâm, giới thiệu, liên hệ), Top 5 đề tài gợi ý kèm điểm thành phần
  (M1 kỹ năng, M3 lĩnh vực, M4 gần nghĩa, M5 LLM) và lý do,
  danh sách đề tài chia tab đủ / chưa đủ điều kiện, đăng ký 3 nguyện vọng (lưu nháp → nộp chính thức → rút về nháp trước hạn),
  xem kết quả phân công chính thức.
- **Giảng viên:** đăng / sửa đề tài (mã tự sinh, mục tiêu, công nghệ, kỹ năng yêu cầu, môn tiên quyết, sức chứa),
  bảng sinh viên chờ duyệt, ngăn kéo phân tích từng sinh viên, đồng ý (kèm nhận xét) hoặc từ chối (bắt buộc lý do), hồ sơ giảng viên;
  cảnh báo đề tài gần trùng với giảng viên khác và gợi ý hướng cải tiến khi giống đề tài khoá trước
  (dùng cả hướng phát triển mà chính khoá trước đề xuất).
- **Khoa:** bảng điều khiển, nhập Excel 2 bước (kiểm tra → xác nhận), phân công tối ưu ILP / Greedy, xếp tay pha 2,
  chốt & công bố (đợt đã công bố chỉ còn chế độ xem), thống kê có biểu đồ và bảng số liệu, rà soát đề tài trùng lặp toàn khoa.
- **Trợ lý ảo (chatbot RAG, mọi vai):** trả lời theo dữ liệu thật của hệ thống — hướng dẫn quy trình, đề tài đang mở
  (điều kiện, số chỗ, số người chọn NV1), giảng viên, kho đề tài khoá trước kèm hướng phát triển, dữ liệu của chính người hỏi —
  có trích nguồn (thẻ bấm mở đúng trang). Tìm kiếm lai Sentence-BERT + từ khoá (khớp cả khi gõ không dấu).
  **Phân quyền theo vai:** trợ lý chỉ nhận đúng phần dữ liệu giao diện của vai đó được xem; lọc thông tin cá nhân ở đầu ra;
  hạn mức câu hỏi theo vai; nhật ký hỏi–đáp để đánh giá.

## Công nghệ
Python 3.12 · Django 5.2 · SQLite (mặc định) hoặc MySQL · Bootstrap 5.3 + hệ thiết kế riêng **ATLAS** · Chart.js 4 ·
sentence-transformers (MiniLM đa ngôn ngữ, M4) · PuLP / CBC (ILP) · LLM qua API tương thích OpenAI (Groq / Gemini / Ollama, M5
và trợ lý ảo).

## Cài đặt và chạy (Windows / Linux)
```bash
git clone <địa chỉ repo>
cd capstone-advisor
python -m venv .venv
.venv\Scripts\activate            # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env            # Linux/macOS: cp .env.example .env
python manage.py migrate
python manage.py seed_demo        # dữ liệu mô phỏng: 100 SV, 15 GV, 50 đề tài, 1 đợt đang mở
python manage.py runserver
```
Kho đề tài khoá trước: `seed_demo` có 5 đề tài mẫu; kho thật nạp bằng
`python manage.py them_de_tai_khoa_truoc --tu-file <file.jsonl>` (dữ liệu của trường không kèm trong repo).

Mở http://127.0.0.1:8000 — tài khoản demo (mật khẩu `123456`): `sv001` sinh viên · `gv001` giảng viên · `khoa01` cán bộ Khoa.

Biến môi trường chính (`.env`): `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DB_ENGINE=mysql` + `DB_*` (dùng MySQL),
`LLM_PROVIDER` / `LLM_MODEL` / `LLM_API_KEY` (bật M5), `RECOMMEND_SEMANTIC=0` / `RECOMMEND_LLM=0` (tắt M4 / M5 khi chạy máy yếu),
`ASSETS_FROM_CDN=0` (chỉ dùng thư viện lưu sẵn trong dự án, chạy được khi không có Internet),
`CHAT_PROVIDER` / `CHAT_MODELS` (nhiều mô hình cách nhau dấu phẩy, mô hình đầu lỗi thì dùng mô hình sau) / `CHAT_API_KEY`
(bật trợ lý ảo; thiếu khoá thì trợ lý chạy chế độ dự phòng: trả các đoạn tìm được).

## Cấu trúc thư mục
```
capstone-advisor/
├── config/            Thiết lập Django, định tuyến URL, WSGI/ASGI
├── accounts/          Tài khoản 3 vai trò (User.role), trang chủ theo vai trò, hành trình 4 bước của SV
├── catalog/           Dữ liệu nghiệp vụ: SV, GV, đề tài, kỹ năng, môn học, đợt đăng ký, nguyện vọng, nhật ký
│   ├── models.py      Thực thể và ràng buộc (mã đề tài tự sinh, cờ nộp nguyện vọng, …)
│   ├── views.py       Màn hình SV / GV / Khoa (hồ sơ, đề tài, nguyện vọng, duyệt, nhập Excel)
│   ├── services.py    Lọc đề tài, đếm NV1, chỗ còn lại
│   ├── importer.py    Nhập Excel (chạy thử trong giao dịch rồi hoàn tác → xác nhận mới ghi)
│   ├── similarity.py  Đề tài gần trùng (Sentence-BERT) và gợi ý cải tiến so với đề tài khoá trước
│   ├── templatetags/  Bộ lọc template (tách lý do gợi ý, tách thẻ công nghệ)
│   └── management/commands/seed_demo.py   Sinh dữ liệu mô phỏng có hạt giống cố định
├── recommend/         AI gợi ý: lọc cứng + M1 kỹ năng, M3 lĩnh vực, M4 ngữ nghĩa, M5 LLM; trọng số AHP 4×4
│   ├── engine.py      Công thức M1, M3, M4, M5, lọc điều kiện, khối "Kiểm tra điều kiện", lời giải thích
│   ├── llm.py         Gọi LLM theo rubric, bộ nhớ đệm, trộn thứ tự chống thiên lệch vị trí
│   └── ahp.py         Tính vector trọng số và tỷ số nhất quán CR
├── allocate/          Phân công: mô hình ILP (PuLP/CBC), Greedy đối chứng, chỉ số chất lượng, pha 2 xếp tay, công bố
├── reports/           Thống kê cho Khoa (biểu đồ + bảng số liệu)
├── assistant/         Trợ lý ảo: chat.py (truy hồi lai, ngữ cảnh theo vai, gọi LLM, máy kiểm sau trả lời),
│                      kb/ (hướng dẫn quy trình — mỗi mục "##" là một đoạn tri thức), nhật ký ChatLog
├── templates/         Giao diện: base.html (khung chung), components/ (thành phần dùng lại), trang theo ứng dụng
├── static/
│   ├── css/atlas.css  Hệ thiết kế ATLAS: biến màu sáng/tối, chữ, khoảng cách, thành phần
│   ├── css/pages/     CSS riêng từng nhóm trang (mọi luật nằm trong lớp .pg-<mã màn>)
│   ├── js/atlas.js    Hành vi chung: chế độ sáng/tối, biểu đồ, chống bấm lặp, xác nhận công bố
│   ├── brand/ icons/ illus/   Logo, biểu tượng Lucide, minh hoạ trạng thái rỗng
│   └── vendor/        Bootstrap, Chart.js, phông Be Vietnam Pro lưu sẵn (dự phòng khi không tải được CDN)
├── experiments/       RQ1 (ablation), RQ2 (độ ổn định LLM), RQ3 (ILP – Greedy), RQ3b (Greedy, Gale-Shapley, GA, ILP),
│                      RQ4 (độ trùng và hiệu chỉnh ngưỡng trên kho đề tài khoá trước thật)
└── docs/              Giải thích từng phần, use case, sổ tay bảo vệ, phiếu khảo sát AHP, biên bản nghiệm thu
```

## Kiểm thử
```bash
python manage.py test        # 253 ca: nghiệp vụ SV/GV/Khoa, phân quyền, AHP, ILP, nhập Excel, đề tài trùng, trợ lý ảo, giao diện
ruff check .                 # kiểm tra phong cách mã + độ phức tạp hàm (McCabe ≤ 10)
```
Thực nghiệm cho báo cáo: xem `experiments/README.md`.

Giấy phép: Apache-2.0.
