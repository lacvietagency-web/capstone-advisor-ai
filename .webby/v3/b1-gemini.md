**BÁO CÁO RÀ SOÁT KỸ THUẬT & KẾ HOẠCH TRIỂN KHAI ATLAS V3.3**  
*Vai trò: Trưởng nhóm Front-End*

---

### G1. Mâu thuẫn và thiếu hụt dữ liệu giữa thông số với template/backend hiện tại
* **Trang Phân công đề tài Khoa (`allocate/dashboard.html`)**:
  * *Thiếu bộ lọc backend*: Thông số đòi hỏi lọc theo Giảng viên (`lecturer_id`), Lĩnh vực (`field_id`) và khoảng điểm, nhưng `allocate/views.py` hiện chỉ nhận `status`, `rank`, `q`, `sort`.
  * *Thiếu dữ liệu chi tiết*: Bảng render từ `Allocation`. Khi sinh viên chưa xếp (`topic__isnull=True`), đối tượng này không kèm 3 nguyện vọng gốc NV1–NV3 và thiếu trường nguyên nhân chưa xếp (`unassigned_reason`). Context drawer chỉ có `suggestions` (pha 2), không đủ để đối chiếu điều kiện học thuật.
* **Trang Danh sách đề tài (`catalog/topic_list.html`) & Chi tiết (`catalog/topic_detail.html`)**:
  * *Thiếu cấu trúc điều kiện*: `_ineligible_reason` trong `catalog/views.py` chỉ trả về một chuỗi văn bản đơn lẻ, thiếu mảng đối tượng `eligibility.reasons[]` (`rule_type`, `required_value`, `actual_value`, `is_mandatory`) như đặc tả.
  * *Thiếu siêu dữ liệu AI*: `recommend.models.Recommendation` chỉ lưu điểm M1–M5; thiếu cờ `score_status` (phân biệt điểm sơ bộ M1–M4 với đủ M5), `weights_version` và nhãn nguồn fallback LLM. Khi người dùng chưa đăng nhập, hoàn toàn không có dữ liệu gợi ý.
* **Trang Kết quả phân công của SV (`allocate/student_result.html`)**:
  * Thiếu trường phân biệt nguồn gán `source` (xếp tự động ILP hay phân công tay của Khoa) và lý do chưa xếp chính thức từ hội đồng.
* **Trang Sinh viên đăng ký của GV (`catalog/lecturer_registrations.html`)**:
  * Thiếu cấu trúc Drawer/Modal chi tiết sinh viên: view chỉ truyền danh sách phẳng `rows` gồm `pref` và `rec`, thiếu lịch sử và phiên bản đánh giá tại thời điểm nộp.
* **Nút thông báo (Topbar `base.html`)**:
  * Backend hoàn toàn chưa có model hay context `notifications`. Cần loại bỏ hoàn toàn biểu tượng chuông giả theo đúng quy định ở Mục C - Lỗi 7.

---

### G2. Những điểm thông số còn thiếu số liệu cần Design Authority làm rõ
* **Q1 (Tương tác Drawer Phân công)**: Bấm vào dòng sinh viên trên bảng Khoa sẽ mở Offcanvas (420–480px bên phải) hay Modal căn giữa? Dữ liệu chi tiết nạp qua Fetch API bất đồng bộ hay render sẵn mã HTML ẩn trong từng dòng?
* **Q2 (Trạng thái Context Index)**: Nút thu gọn Context Index (224px) lưu trạng thái đóng/mở vào `localStorage` hay theo từng phiên? Khi đã thu gọn, vị trí nút bấm để mở lại nằm cố định ở Rail 68px hay đầu Main Canvas?
* **Q3 (Số liệu Metric Ledger Khoa)**: Yêu cầu giữ đúng "100 SV, 15 GV, 50 đề tài, 43%, 30%, 63.8...". Đây là số liệu giả định (mock) bắt buộc cho buổi bảo vệ hay phải tính động từ đợt thực tế của CSDL? Nếu đợt mới có quy mô khác thì hiển thị thế nào?
* **Q4 (Bottom Action Bar mobile)**: Khi màn hình vừa có Bottom Navigation (64px) vừa có Bottom Action Bar (72px) (ví dụ form Đăng ký nguyện vọng), Action Bar sẽ xếp chồng lên trên Bottom Nav hay tạm ẩn Bottom Nav?
* **Q5 (Cơ chế Theme 3 trạng thái)**: Thiết kế yêu cầu 3 tùy chọn: Sáng / Tối / Theo thiết bị. Tên khóa `localStorage` thống nhất là gì (chuyển từ `mosaic-theme` thành `atlas-theme`?) và cơ chế gán `data-bs-theme` khi người dùng đổi cài đặt OS?

---

### G3. Ánh xạ Bootstrap 5.3 và kiến trúc file CSS duy nhất (`static/css/atlas.css`)
* **Ánh xạ Bootstrap 5.3 Tokens**:
  * Ghi đè biến gốc tại `:root` và `[data-bs-theme="dark"]`:
    * `--bs-body-font-family: var(--at-font);`
    * `--bs-body-bg: var(--at-canvas);` | `--bs-body-color: var(--at-ink);`
    * `--bs-primary: var(--at-brand);` | `--bs-primary-rgb: 48, 95, 82;`
    * `--bs-border-color: var(--at-line);` | `--bs-border-radius: var(--at-radius-md);`
  * Đồng bộ các thành phần Bootstrap (`.btn`, `.form-control`, `.table`, `.badge`, `.modal-content`, `.offcanvas`) sang border 1px phẳng, bỏ gradient và shadow mặc định.
* **Cấu trúc 7 phần trong `atlas.css` (không viết CSS riêng lẻ)**:
  1. *Font Imports*: Định nghĩa `@font-face` nạp local Be Vietnam Pro từ `../vendor/fonts/`.
  2. *Design Tokens*: Hệ biến `--at-*` (màu sắc 2 theme, typography, spacing, radius, transitions).
  3. *Bootstrap Reset*: Ghi đè `--bs-*`, thiết lập chuẩn box-sizing, focus ring, heading, link.
  4. *App Shell Layout*: Topbar (60px), Navigation Rail (68px), Context Index (224px), Main Canvas (max 1480px / 880px), Mobile Bottom Nav (64px), Mobile Action Bar (72px).
  5. *Base UI Components*: Hệ nút `.at-btn`, Form controls, Data panel, Item card, Modal, Offcanvas, Toast.
  6. *Domain Components*: Metric Ledger, Evidence Strip M1–M5, Journey 4 bước, Data table phẳng, Empty state, Quy trình xác nhận 2 bước.
  7. *Motion & Accessibility*: Transition đồng bộ `cubic-bezier(.2, .7, .2, 1)`, xử lý `@media (prefers-reduced-motion: reduce)`.

---

### G4. Rủi ro trên màn hình 390px (Mobile) và giải pháp xử lý
* **Bảng dữ liệu nhiều cột (Phân công, Đề tài GV)**:
  * *Rủi ro*: Tràn ngang viewport, vỡ bố cục.
  * *Giải pháp*: Ẩn thẻ `table` (`d-none d-md-block`), thay bằng danh sách Card phẳng (`d-md-none`): mỗi thẻ 3 dòng (Tên/Mã SV → Đề tài & Điểm → Trạng thái & Nút thao tác).
* **Ngăn kéo chi tiết (Drawer 420–480px)**:
  * *Rủi ro*: Chiều rộng vượt quá 390px.
  * *Giải pháp*: Dưới 768px tự động chuyển thành Bottom Sheet trượt từ đáy (`height: 85vh`, bo góc đỉnh 16px) hoặc Offcanvas chiếm trọn 100% màn hình.
* **Thanh điều hướng đáy và Action Bar**:
  * *Rủi ro*: Chiếm gần 140px chiều cao, che lấp nội dung cuộn bên dưới.
  * *Giải pháp*: Gán `padding-bottom: calc(144px + env(safe-area-inset-bottom))` cho thẻ `main`; các trang có form ưu tiên hiển thị Action Bar và ẩn Bottom Nav.
* **Form dài (Hồ sơ SV, Đề tài GV)**:
  * *Rủi ro*: Bàn phím ảo che khuất nút gửi; ô nhập bị ép hẹp.
  * *Giải pháp*: Buộc form thành 1 cột duy nhất (`col-12`), khoảng cách trường tối thiểu 20px, touch target 44px, nút Lưu gắn cố định trên Action Bar.

---

### G5. Phân công 3 nhóm màn hình thi công song song (Zero-conflict)
* **Nhóm 1: Nền tảng Shell & Luồng Sinh viên** (7 trang):
  * *File đảm nhiệm*: `templates/base.html`, `templates/components/*`, `templates/registration/login.html`, `password_change_form.html`, `password_change_done.html`, `pages/home_student.html`, `catalog/student_profile.html`, `catalog/student_preferences.html`, `allocate/student_result.html`, `pages/missing_profile.html`, các trang lỗi `403/404/500`.
  * *Trọng tâm*: Dựng khung App Shell, Token `atlas.css`, Journey 4 bước, dải Top 5.
* **Nhóm 2: Danh mục Đề tài & Luồng Giảng viên** (7 trang):
  * *File đảm nhiệm*: `pages/home_lecturer.html`, `catalog/lecturer_topics.html`, `catalog/lecturer_topic_form.html`, `catalog/lecturer_registrations.html`, `catalog/lecturer_profile.html`, `catalog/topic_list.html`, `catalog/topic_detail.html`.
  * *Trọng tâm*: Bộ lọc Context Index, Evidence Strip M1–M5, form kỹ năng đa cấp, duyệt/từ chối sinh viên.
* **Nhóm 3: Workspace Khoa & Báo cáo số liệu** (4 trang):
  * *File đảm nhiệm*: `pages/home_admin.html`, `allocate/dashboard.html`, `reports/statistics.html`, `catalog/faculty_import.html`.
  * *Trọng tâm*: Metric Ledger, Phân trang server-side 20 dòng/trang, Drawer xếp tay pha 2, modal công bố 2 bước, biểu đồ Chart.js dark/light, nhập Excel.
* **Quy tắc phối hợp**: Nhóm 1 bàn giao bản khóa khung layout `base.html` và file token `atlas.css` ở mốc Sprint 0. Nhóm 2 và 3 kế thừa class hệ thống, chỉ làm việc độc lập trên template của nhóm mình.
