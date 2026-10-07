# Hợp đồng ngắn P0 — Nền móng giao diện Mosaic AI (webbyLucifer GĐ8)
TRẠNG THÁI: IMPLEMENTATION_READY_UI cho phần nền móng.

ĐẦU VÀO (chỉ dùng những thứ này, không tự sáng tác):
- Thông số: .webby/DESIGN-SPEC-mosaic.md (PHẦN 3 thông số, PHẦN 4 thành phần, PHẦN 5 chuyển động)
- Nguyên liệu áp dụng: .webby/NGUYEN-LIEU-AP-DUNG.md (14 thẻ: mỗi thẻ áp vào thành phần nào)
- Ảnh tham chiếu: .webby/renders/*.jpg — CHỈ ĐỂ NHÌN bố cục/cảm giác, KHÔNG đo pixel; số liệu lấy từ thông số.
- Biên bản sửa lỗi: .webby/BIEN-BAN-HOP-GIAO-DIEN.html mục 3–4 (không ảnh người, không xanh Bootstrap, logo 5 ô, không thẻ số liệu icon màu).
- Tài nguyên đã đóng băng: static/mosaic/brand/*.svg, static/mosaic/illus/*.svg, static/mosaic/icons/*.svg (Lucide) — .webby/ASSET_MANIFEST.json.
  Icon CHỈ được dùng file trong static/mosaic/icons/ (không Bootstrap Icons, không emoji, không icon khác). Thiếu icon → ghi NEED_ASSET vào REQUESTS.md.

PHẠM VI (chỉ templates/ và static/):
1. static/css/mosaic.css: biến màu :root (sáng) + [data-bs-theme="dark"] (tối) đúng PHẦN 3, nối sang biến --bs-* của Bootstrap
   (primary, body-bg, body-color, border-color, link…); thang chữ, khoảng cách, bo góc, bóng; tôn trọng prefers-reduced-motion.
2. templates/base.html làm lại thành khung Mosaic: menu trái theo vai trò (SV/GV/Khoa) với logo 5 ô, topbar (breadcrumb, đợt, chuông, nút sáng/tối,
   avatar = chữ cái viết tắt), thanh điều hướng dưới trên điện thoại cho SV; nút sáng/tối lưu localStorage (bọc try/catch) và đặt data-bs-theme
   trước khi vẽ trang (tránh nháy). Giữ NGUYÊN mọi url name, block, csrf, messages.
3. templates/components/*.html — thư viện thành phần dùng {% include %}: metric_ribbon, data_table (vỏ), status_badge, button variants,
   confirm_modal (2 bước; biến thể có ô lý do bắt buộc cho Từ chối — field name="reason", required, minlength=5), score_block (điểm tổng + M1–M5 gọn,
   mở rộng xem chi tiết), reason_block (lý do gợi ý dạng gạch đầu dòng có dấu tích), empty_state (dùng static/mosaic/illus), toast/alert, icon (include
   nạp SVG theo tên từ static/mosaic/icons).
4. static/js/mosaic.js: chuyển sáng/tối, đóng/mở ngăn kéo, tab có vạch trượt, hiện dần (WAAPI) — đúng 14 thẻ nguyên liệu, có reduced-motion.
5. templates/components/_demo.html + URL không cần — thay vào đó tạo templates/components/README.md mô tả cách include từng thành phần.

KHÔNG làm ở P0: không sửa các trang nghiệp vụ (P1–P3 làm sau), không sửa .py.
KIỂM TRA: manage.py test xanh; ruff sạch; trang hiện có vẫn mở được (không lỗi template). Ghi các trang/biến cần thêm vào ui-review/REQUESTS.md.
BÁO CÁO: 3–5 dòng ở đầu REQUESTS.md: đã làm gì, NEED_ASSET/BLOCKED_SPEC nếu có.
PAGE sv001 /trang-chu/ · PAGE gv001 /trang-chu/ · PAGE khoa01 /trang-chu/
