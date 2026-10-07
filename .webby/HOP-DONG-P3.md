# Hợp đồng ngắn P3 — Các trang KHOA + đăng nhập + trang lỗi theo Mosaic AI (webbyLucifer GĐ8)
ĐẦU VÀO: giống P1/P2 (.webby/DESIGN-SPEC-mosaic.md, .webby/NGUYEN-LIEU-AP-DUNG.md, .webby/BIEN-BAN-HOP-GIAO-DIEN.html,
templates/components/README.md, static/css/mosaic.css, static/js/mosaic.js). BẮT BUỘC dùng thành phần P0; CSS mới thêm khối /* P3 */ cuối mosaic.css.
Ảnh tham chiếu (chỉ nhìn, KHÔNG đo pixel): .webby/renders/01-khoa-phancong-desktop-sang.jpg, 02-khoa-phancong-desktop-toi.jpg,
15-khoa-thongke-desktop.jpg, 16-khoa-trangchu-desktop.jpg, 17-khoa-phancong-mobile.jpg, 18-khoa-nhap-excel-desktop.jpg,
19-dangnhap-desktop.jpg, 21-trangthai-loi.jpg. Lỗi đã chốt trong biên bản (ảnh 17: không 4 thẻ icon màu; ảnh 12/17/18: không ảnh người thật,
không màu xanh Bootstrap — avatar = chữ cái viết tắt, màu = biến Mosaic).

PHẠM VI (chỉ templates/ + static/), giữ NGUYÊN biến Django, form field name, giá trị action (run_ilp, run_greedy, manual_assign, publish),
csrf, url name, logic:
1. templates/pages/home_admin.html — Tổng quan Khoa: dải số liệu + lối tắt (Phân công, Thống kê, Nhập Excel).
2. templates/allocate/dashboard.html — Phân công: MỘT nút chính "Chạy tối ưu (ILP)", Greedy là lựa chọn phụ "để so sánh";
   bảng nháp chỉ hiện điểm tổng; xếp tay Pha 2; nút Công bố dùng confirm_modal 2 bước; ghi rõ "Chưa công bố" khi chưa công bố.
   Mobile: chỉ phần xem nhanh + thao tác chính, bảng có cách hiển thị riêng (thẻ), không tràn ngang.
3. templates/reports/statistics.html — Thống kê (Chart.js giữ dữ liệu cũ, màu lấy từ biến CSS, đổi theo sáng/tối).
4. templates/catalog/faculty_import.html — TRANG MỚI (lõi đã có view, url 'faculty_import', 'faculty_import_sample'): giữ form multipart,
   input name="file" accept=".xlsx", csrf; nút tải tệp mẫu; ghi rõ "lỗi bất kỳ dòng nào thì không nhập gì"; kết quả: result.ok → bảng
   result.stats; lỗi → danh sách result.errors (mỗi lỗi là "Sheet X, dòng N: …"); max_mb. Thêm mục "Nhập Excel" vào menu Khoa trong base.html.
5. templates/registration/login.html (+ password_change_form/done) — đăng nhập theo ảnh 19, logo Mosaic từ static/mosaic/brand, KHÔNG logo trường.
6. templates/403.html, 404.html, 500.html — dùng minh hoạ static/mosaic/illus (500.html là HTML tĩnh, không extends, không thẻ template động).
KIỂM TRA: test xanh; ruff sạch; không tràn ngang 390px; sáng & tối. BÁO CÁO 3–5 dòng đầu ui-review/REQUESTS.md + nguyên liệu đã dùng.
PAGE khoa01 /trang-chu/ · PAGE khoa01 /khoa/phan-cong/ · PAGE khoa01 /khoa/thong-ke/ · PAGE khoa01 /khoa/nhap-excel/ · PAGE sv001 /khoa/phan-cong/
