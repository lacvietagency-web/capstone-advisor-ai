# Hợp đồng ngắn P2 — Các trang GIẢNG VIÊN theo Mosaic AI + sửa lỗi P1 (webbyLucifer GĐ8)
ĐẦU VÀO: giống P1 (.webby/DESIGN-SPEC-mosaic.md, .webby/NGUYEN-LIEU-AP-DUNG.md, .webby/BIEN-BAN-HOP-GIAO-DIEN.html,
templates/components/README.md, static/css/mosaic.css, static/js/mosaic.js). BẮT BUỘC dùng thành phần P0; CSS mới thêm khối /* P2 */ cuối mosaic.css.
Ảnh tham chiếu (chỉ nhìn): .webby/renders/10-gv-trangchu-desktop.jpg, 11-gv-duyet-sv-desktop.jpg, 12-gv-form-detai-desktop.jpg,
13-gv-detai-cuatoi-desktop.jpg, 14-gv-hoso-desktop.jpg.

PHẠM VI (chỉ templates/ + static/), giữ NGUYÊN biến Django, form field name, csrf, url name, logic:
1. templates/pages/home_lecturer.html — dải số liệu (n_topics, n_students, n_pending, n_accepted) + đề tài có số chờ duyệt + "Duyệt ngay".
2. templates/catalog/lecturer_topics.html — Đề tài của tôi.
3. templates/catalog/lecturer_topic_form.html — Thêm/sửa đề tài: lĩnh vực dạng chip; formset kỹ năng thêm/xoá dòng PHẢI chạy (giữ management form,
   empty_form/__prefix__); công tắc "Bắt buộc" có chú thích "là điều kiện loại"; HIỂN THỊ tỉ lệ % trọng số từng kỹ năng (tính bằng JS từ các ô trọng số,
   KHÔNG ép tổng 100%); môn tiên quyết.
4. templates/catalog/lecturer_registrations.html + templates/catalog/_pref_actions.html — danh sách SV đăng ký: bảng chỉ hiện ĐIỂM TỔNG, bấm để mở
   ngăn kéo phân tích M1–M5 bên phải; Đồng ý = nút; Từ chối = confirm_modal có Ô LÝ DO BẮT BUỘC (name="reason", required, minlength=5);
   hiện lý do đã từ chối (pref.reject_reason).
5. templates/catalog/lecturer_profile.html — Hồ sơ GV (avatar chữ cái, chip lĩnh vực, chỉ tiêu + trạng thái khoá).
SỬA LỖI P1 (bug fix, không mở rộng phạm vi):
 B1 templates/base.html: chân trang và mọi chỗ ghi "EAUT"/"Khoa CNTT – EAUT" → thay bằng "Mosaic AI" (sản phẩm riêng, KHÔNG thương hiệu trường).
 B2 templates/catalog/topic_detail.html: khi đề tài CHƯA ĐỦ ĐIỀU KIỆN, bỏ câu "bạn vẫn có thể đăng ký…" (mâu thuẫn); khi chưa có điểm thì chỉ nói chưa có điểm.
 B3 templates/catalog/student_profile.html: hiển thị lỗi của formset (non_form_errors + lỗi từng dòng, VD kỹ năng trùng) ngay tại dòng lỗi.
 B4 breadcrumb trang chi tiết đề tài = "Sinh viên / Danh sách đề tài / <tên đề tài>".
KIỂM TRA: test xanh; ruff sạch; không tràn ngang 390px; sáng & tối. BÁO CÁO 3–5 dòng đầu ui-review/REQUESTS.md + nguyên liệu đã dùng.
PAGE gv001 /trang-chu/ · PAGE gv001 /de-tai/ · PAGE gv001 /de-tai/them/ · PAGE gv001 /ho-so-giang-vien/ · PAGE sv001 /ho-so/
