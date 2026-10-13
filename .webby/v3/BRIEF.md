# Hồ sơ cho Design Authority (ChatGPT) — webbyLucifer v3.3, TASK = NEW_REDESIGN (lần 3)

## Dự án
- "Capstone AI" (tên đầy đủ: Capstone Advisor AI) — đồ án tốt nghiệp: hệ thống AI tư vấn đề tài cho sinh viên
  (5 mô hình M1 kỹ năng, M2 học lực, M3 lĩnh vực, M4 ngữ nghĩa, M5 LLM; trọng số AHP) + phân công tối ưu ILP cho Khoa.
- 3 vai: Sinh viên (hồ sơ năng lực → Top 5 đề tài phù hợp + lý do → đăng ký NV1–NV3 → xem kết quả), Giảng viên (đề tài của tôi,
  duyệt SV đăng ký kèm điểm phù hợp, hồ sơ/chỉ tiêu), Khoa (chạy phân công ILP/Greedy, xếp tay pha 2, chốt & công bố, thống kê, nhập Excel).
- Mục tiêu giao diện: thuyết phục hội đồng bảo vệ (chuyên nghiệp, đáng tin, thấy rõ "AI có giải thích") VÀ dùng được thật.
- Thiết bị: SV/GV chủ yếu điện thoại; Khoa máy tính; hội đồng xem trên máy chiếu/laptop.

## Lịch sử (để KHÔNG lặp lại)
- Bản 1 "Mosaic AI": menu trái, xanh ngọc (teal), logo 5 ô ghép. Chủ dự án yêu cầu đổi khác hẳn.
- Bản 2 "Nova" (ảnh đính kèm, đang chạy): thanh ngang, indigo/tím gradient, font Space Grotesk + Inter. Chủ dự án chê "ngáo ngơ".
- Bản 3 (việc này): phải KHÁC HẲN cả hai bản trên về bố cục, màu, chữ, cách trình bày số liệu.

## Lỗi thật của bản đang chạy (đã đo trên trang thật)
1. Thẻ mất lề trong: chữ dính sát viền thẻ ở hầu hết trang (trang chủ SV, kết quả, danh sách đề tài).
2. Ngăn kéo "Thông tin sinh viên" (trang GV duyệt) hiện đè lên trang và làm tràn ngang; 3 nút Chờ duyệt/Đồng ý/Từ chối xếp chồng dọc trong mỗi dòng.
3. Ba họ phông lẫn nhau (Space Grotesk, Inter, Noto Sans); dấu tiếng Việt ở tiêu đề lệch nét. Phân trang còn màu xanh Bootstrap mặc định.
4. Bảng phân công của Khoa: 100 dòng liền một trang (cao 6.500 px), không tìm kiếm, không phân trang; cả dòng "chưa xếp" tô hồng.
5. Luồng sai: đợt đã công bố kết quả nhưng thanh bước của SV vẫn báo đang ở bước 2 "Gợi ý AI"; khối "Top 5 đề tài phù hợp" trống
   dù SV đã có 3 nguyện vọng; trang Nguyện vọng khi đợt đã đóng chỉ hiện "chưa có đợt nào" (ngõ cụt) thay vì cho xem lại nguyện vọng đã nộp.
6. Danh sách đề tài: đa số đề tài ghi "Chưa đủ điều kiện" nhưng không nói thiếu gì; không thấy điểm phù hợp AI ngay trên danh sách.
7. Nút đổi sáng/tối là một công tắc trơn không nhãn; chuông thông báo không có chức năng.
8. Phụ thuộc CDN (Bootstrap, Chart.js, Google Fonts) — mạng yếu là vỡ giao diện. Sẽ đóng gói sẵn trong dự án (Claude làm).

## CẤM (chủ dự án đã chê nhiều lần)
- Kiểu template SaaS chung chung: font Inter khắp nơi, gradient tím–xanh, nút gradient, bóng màu tím, card lồng card, Bootstrap mặc định.
- Hàng thẻ số liệu mỗi thẻ một icon tròn màu. Ảnh người/stock. Emoji làm icon. Màu vàng/đỏ tô cả vùng lớn.
- Mỗi khối một hiệu ứng khác nhau (chỉ một ngôn ngữ chuyển động, kín đáo).

## Ràng buộc kỹ thuật (Claude giữ phần cơ chế)
- Django templates + Bootstrap 5.3 (đóng gói sẵn, dùng lưới/modal/dropdown/offcanvas) + MỘT file CSS mới (xoá 3 file CSS cũ) + Chart.js.
  Không React, không bước build. Breakpoint = Bootstrap (576/768/992/1200/1400). Có chế độ sáng + tối (data-bs-theme).
- Phông: tự lưu trong dự án, phải là Google Fonts CÓ tiếng Việt đầy đủ (subset vietnamese). Tối đa 2 họ phông.
- Icon: CHỈ dùng bộ Lucide đã có sẵn 68 icon (danh sách bên dưới). Minh hoạ trạng thái rỗng: đã có 12 SVG nét mảnh (dùng lại, đổi màu qua CSS).
- Tiếng Việt toàn bộ. Dữ liệu demo thật: 100 SV, 15 GV, 50 đề tài; phân công ILP: 43% đã xếp, 30% đạt NV1, 43% Top 3, điểm phù hợp TB 63,8, 57 SV chờ pha 2.

## Icon có sẵn (Lucide)
archive arrow-down arrow-left arrow-up badge-check bell book-check bookmark book-open brain briefcase-business chart-line chart-no-axes-column
chart-pie check chevron-down chevron-right circle-check-big circle-dot circle-help circle-plus clipboard-list database download eye-off eye
file-check-2 file-spreadsheet file-text file-x-2 filter gauge git-compare graduation-cap house info layers-3 layout-dashboard list-ordered
lock-keyhole lock log-out monitor moon play plus refresh-cw route save search send settings-2 sliders-horizontal sparkles square-pen
square-stop sun table-2 target trash-2 triangle-alert upload user-check user-round users-round users user user-x wand-sparkles

## Danh sách màn hình (18)
Chung: đăng nhập; đổi mật khẩu; thiếu hồ sơ; 403; 404; 500.
SV: trang chủ; hồ sơ năng lực (tự giới thiệu, kỹ năng mức 1–5 thêm/xoá, lĩnh vực quan tâm 1–3); đăng ký NV1–NV3; danh sách đề tài (lọc, tìm, phân trang);
chi tiết đề tài (điểm M1–M5, lý do, điều kiện, đăng ký); kết quả phân công.
GV: trang chủ; đề tài của tôi; thêm/sửa đề tài (lĩnh vực, kỹ năng yêu cầu: mức, trọng số, bắt buộc); SV đăng ký đề tài (duyệt Đồng ý / Từ chối có lý do, xem phân tích M1–M5); hồ sơ GV.
Khoa: trang chủ; phân công (chạy ILP/Greedy, chỉ số, phân bố điểm, bảng SV, xếp tay pha 2, chốt & công bố 2 bước); thống kê; nhập Excel.
