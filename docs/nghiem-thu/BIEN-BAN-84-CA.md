# Biên bản thực hiện 84 ca kiểm thử — Capstone Advisor AI

Ngày chạy: 20/10/2026 03:50. Nguồn: chạy lại 116 test tự động được ánh xạ (lỗi: 0) + kết quả trình duyệt (26 mục). Tổng hợp: Đạt 84.

| Mã | Ca | Kết quả | Bằng chứng |
|---|---|---|---|
| A01 | Mở `/trang-chu/`, `/ho-so/`, `/khoa/phan-cong/` khi chưa đăng nhập | Đạt | 2 test tự động |
| A02 | Đăng nhập sai mật khẩu; sai tên đăng nhập; để trống | Đạt | 1 test tự động |
| A03 | Bấm "Sử dụng" ở 3 tài khoản demo | Đạt | Trình duyệt: chromium ĐẠT; firefox ĐẠT |
| A04 | Nút mắt ở ô mật khẩu | Đạt | Trình duyệt: chromium ĐẠT; firefox ĐẠT |
| A05 | Đăng nhập đúng | Đạt | 3 test tự động |
| A06 | Đổi mật khẩu: sai mật khẩu cũ; mật khẩu mới yếu (toàn số, < 8 ký tự, giống tên); hai ô khô | Đạt | 5 test tự động |
| A07 | Đăng xuất | Đạt | 1 test tự động |
| A08 | Mở trực tiếp URL của GV/Khoa: `/de-tai/`, `/de-tai/them/`, `/de-tai/<id>/dang-ky/`, `/khoa | Đạt | 2 test tự động |
| A09 | Mở URL của SV và Khoa: `/ho-so/`, `/nguyen-vong/`, `/ket-qua/`, `/khoa/*` | Đạt | 1 test tự động |
| A10 | Sửa/xem đăng ký đề tài của GV KHÁC: `/de-tai/<id của GV khác>/sua/`, `/de-tai/<id>/dang-ky | Đạt | 3 test tự động |
| A11 | Mở trang SV/GV (`/ho-so/`, `/nguyen-vong/`, `/de-tai/`) | Đạt | 1 test tự động |
| A12 | URL không tồn tại `/abc/`, đề tài không tồn tại `/danh-sach-de-tai/999999/` | Đạt | 1 test tự động |
| A13 | Xem chi tiết đề tài đang ở trạng thái nháp; đề tài đã đóng | Đạt | 2 test tự động |
| A14 | Menu tài khoản → Giao diện Sáng / Tối / Theo hệ thống → tải lại trang | Đạt | Trình duyệt: chromium ĐẠT; firefox ĐẠT |
| S01 | Trang chủ | Đạt | 1 test tự động |
| S02 | Trang chủ của SV chưa có kỹ năng (xoá hết kỹ năng ở Hồ sơ) | Đạt | 1 test tự động |
| S03 | Hồ sơ: sửa Email, Số điện thoại → Lưu hồ sơ | Đạt | 2 test tự động |
| S04 | Hồ sơ: email sai định dạng; SĐT `12ab`, `0912 345 678`, `+84912345678` | Đạt | 2 test tự động |
| S05 | Hồ sơ: thêm kỹ năng mới, đổi mức 1–5, xoá kỹ năng, chọn trùng một kỹ năng hai lần | Đạt | 2 test tự động |
| S06 | Hồ sơ: tick 4 lĩnh vực quan tâm | Đạt | 1 test tự động |
| S07 | Hồ sơ: bỏ tick một lĩnh vực cũ, tick một lĩnh vực mới (≤ 3) | Đạt | 2 test tự động |
| S08 | Hồ sơ: giới thiệu 500 ký tự; 501 ký tự (gửi thẳng); chèn `<script>alert(1)</script>` | Đạt | 1 test tự động |
| S09 | Danh sách đề tài: tab "Đủ điều kiện" / "Chưa đủ điều kiện" | Đạt | 1 test tự động |
| S10 | Danh sách: lọc lĩnh vực, giảng viên, độ khó, từ khoá; sắp xếp theo điểm/tên/độ khó/sức chứ | Đạt | 7 test tự động |
| S11 | Từ khoá có dấu, có ký tự đặc biệt `%`, `'`, `"` | Đạt | 2 test tự động |
| S12 | Chi tiết đề tài | Đạt | 2 test tự động |
| S13 | Chi tiết đề tài chưa đủ điều kiện | Đạt | 1 test tự động |
| S14 | Nguyện vọng: chọn NV1–NV3 khác nhau → Lưu nháp | Đạt | 1 test tự động |
| S15 | Nguyện vọng: Nộp nguyện vọng | Đạt | 1 test tự động |
| S16 | Nguyện vọng: chọn trùng một đề tài ở 2 NV | Đạt | 1 test tự động |
| S17 | Nguyện vọng: Rút về nháp để sửa (khi đợt mở) | Đạt | 2 test tự động |
| S18 | Bấm "Thêm vào nguyện vọng"/"Đăng ký" khi đã đủ 3 NV | Đạt | 1 test tự động |
| S19 | Nguyện vọng khi đợt đã đóng/công bố | Đạt | 2 test tự động |
| S20 | Nguyện vọng: GV đã từ chối/đồng ý kèm nhận xét | Đạt | 1 test tự động |
| S21 | Kết quả khi đợt đang mở / chưa có đợt / đã đóng chưa công bố | Đạt | 2 test tự động |
| S22 | Kết quả khi đã công bố, SV được xếp | Đạt | 2 test tự động |
| S23 | Kết quả khi đã công bố, SV không được xếp | Đạt | 1 test tự động |
| S24 | SV sửa `?period_id=` trên URL kết quả sang đợt khác/không tồn tại | Đạt | 2 test tự động |
| L01 | Tổng quan | Đạt | 2 test tự động |
| L02 | Tổng quan: tìm theo MSSV / tên SV / tên đề tài; lọc Chờ duyệt / Đồng ý / Từ chối / Tất cả | Đạt | 1 test tự động |
| L03 | Tổng quan: bấm "Phân tích" của một SV | Đạt | 1 test tự động |
| L04 | Đề tài của tôi | Đạt | 1 test tự động |
| L05 | Thêm đề tài: bỏ trống tên; sức chứa 0/âm; điểm sàn GPA > 4; kỹ năng trùng; môn tiên quyết  | Đạt | 2 test tự động |
| L06 | Thêm đề tài hợp lệ (mục tiêu, công nghệ, ghi chú xét duyệt, kỹ năng, môn tiên quyết) | Đạt | 2 test tự động |
| L07 | Sửa mô tả đề tài | Đạt | 1 test tự động |
| L08 | Duyệt SV: lọc trạng thái, tìm MSSV | Đạt | 1 test tự động |
| L09 | Mở ngăn kéo Phân tích | Đạt | 1 test tự động |
| L10 | Đồng ý kèm nhận xét | Đạt | 2 test tự động |
| L11 | Từ chối: lý do < 5 ký tự; lý do hợp lệ | Đạt | 3 test tự động |
| L12 | Hồ sơ giảng viên: sửa học hàm, bộ môn, SĐT, giới thiệu, từ khoá, lĩnh vực, chỉ tiêu | Đạt | 3 test tự động |
| L13 | Thống kê trong hồ sơ GV | Đạt | 1 test tự động |
| K01 | Bảng điều khiển | Đạt | 2 test tự động |
| K02 | Nhập Excel: tải tệp mẫu `mau.xlsx` | Đạt | 2 test tự động |
| K03 | Nhập Excel: tệp không phải .xlsx; .xlsx hỏng; .xlsx thiếu cột; dòng sai kiểu dữ liệu | Đạt | 6 test tự động |
| K04 | Nhập Excel hợp lệ: "Tải lên & kiểm tra" | Đạt | 1 test tự động |
| K05 | Bấm "Xác nhận nhập" | Đạt | 2 test tự động |
| K06 | Phân công (đợt đang mở/đã đóng): Chạy tối ưu ILP; Chạy Greedy | Đạt | 2 test tự động |
| K07 | Kiểm tra ràng buộc ILP trên kết quả | Đạt | 4 test tự động |
| K08 | Bộ lọc bảng: trạng thái, NV, GV, lĩnh vực, khoảng điểm, từ khoá, sắp xếp, số dòng/trang; s | Đạt | 1 test tự động |
| K09 | Xem chi tiết SV chưa xếp → Xếp tay vào đề tài còn chỗ → Lưu | Đạt | 2 test tự động |
| K10 | Chốt & công bố: nút xác nhận khi chưa gõ / gõ sai / gõ đúng "CÔNG BỐ" | Đạt | 1 test tự động |
| K11 | Đợt đã công bố: thử Chạy ILP / Greedy / Xếp tay (cả bằng POST trực tiếp) | Đạt | 2 test tự động |
| K12 | Công bố lần hai; công bố khi chưa chạy phân công | Đạt | 1 test tự động |
| K13 | Thống kê | Đạt | 1 test tự động |
| K14 | Trang quản trị `/quan-tri/` | Đạt | 1 test tự động |
| B01 | Lọc cứng | Đạt | 2 test tự động |
| B02 | M1 kỹ năng | Đạt | 2 test tự động |
| B03 | M3 lĩnh vực | Đạt | 2 test tự động |
| B04 | Điểm tổng | Đạt | 2 test tự động |
| B05 | AHP | Đạt | 4 test tự động |
| B06 | Lưu hồ sơ | Đạt | 1 test tự động |
| B07 | Chỗ còn lại | Đạt | 2 test tự động |
| B08 | Mã đề tài | Đạt | 1 test tự động |
| B09 | Giao dịch | Đạt | 2 test tự động |
| B10 | Nhật ký | Đạt | 1 test tự động |
| B11 | Hiệu năng | Đạt | 1 người: mọi trang 6–110 ms (Thống kê lần đầu 1,03 s, có bộ đệm 21 ms); Locust 50 người p95 390 ms (runserver), 100 người p95 110 ms, 28,4 yêu cầu/s (gunicorn 8 tiến trình); 0 lỗi — docs/nghiem-thu/locust/ |
| B12 | Lệnh quản trị | Đạt | 2 test tự động |
| U01 | Mọi trang ở 390/768/1440 px, Sáng/Tối | Đạt | Trình duyệt: chromium ĐẠT; chromium ĐẠT; firefox ĐẠT; firefox ĐẠT |
| U02 | Điện thoại 390 px | Đạt | Trình duyệt: chromium ĐẠT; firefox ĐẠT |
| U03 | Bàn phím | Đạt | Trình duyệt: chromium ĐẠT; firefox ĐẠT |
| U04 | Nhãn | Đạt | Trình duyệt: chromium ĐẠT |
| U05 | Trạng thái rỗng | Đạt | Trình duyệt: chromium ĐẠT; firefox ĐẠT |
| U06 | Không có Internet (`ASSETS_FROM_CDN=0` hoặc chặn CDN) | Đạt | Trình duyệt: chromium ĐẠT; firefox ĐẠT |
| U07 | Trang lỗi 403/404/500 | Đạt | Trình duyệt: chromium ĐẠT; firefox ĐẠT |

## Ma trận truy vết use case ↔ ca kiểm thử

Use case đạt khi MỌI ca ánh xạ đều đạt. Mã `UCxx` là test riêng cho thao tác qua trang quản trị `/quan-tri/`.

| Use case | Tên | Ca kiểm thử | Kết quả |
|---|---|---|---|
| UC01 | Đăng nhập hệ thống & Phân quyền | A01, A02, A03, A05, A08, A09, A10, A11, K14 | Đạt |
| UC02 | Đăng xuất hệ thống | A07 | Đạt |
| UC03 | Đổi mật khẩu cá nhân | A06 | Đạt |
| UC04 | Cập nhật hồ sơ năng lực sinh viên | S03, S04, S05, S06, S07, S08, B06 | Đạt |
| UC05 | Xem danh sách đề tài gợi ý AI (Top 5) | S01, S02, B01, B02, B03, B04 | Đạt |
| UC06 | Tra cứu danh mục & xem chi tiết đề tài | S09, S10, S11, S12, S13, A12, A13 | Đạt |
| UC07 | Đăng ký & sắp xếp nguyện vọng (NV1–NV3) | S14, S15, S16, S17, S18, S19, S20 | Đạt |
| UC08 | Xem kết quả phân công đồ án cá nhân | S21, S22, S23, S24 | Đạt |
| UC09 | Cập nhật hồ sơ chuyên môn & chỉ tiêu GV | L12, L13 | Đạt |
| UC10 | Đăng ký đề xuất đề tài tốt nghiệp mới | L05, L06, B08 | Đạt |
| UC11 | Quản lý & chỉnh sửa thông tin đề tài | L04, L07 | Đạt |
| UC12 | Phê duyệt / Từ chối SV đăng ký đề tài | L09, L10, L11, B07, B09 | Đạt |
| UC13 | Theo dõi danh sách SV đăng ký đề tài | L01, L02, L03, L08 | Đạt |
| UC14 | Quản lý đợt đăng ký đồ án tốt nghiệp | UC14, S19, S21, K11 | Đạt |
| UC15 | Nhập liệu hàng loạt từ file Excel | K02, K03, K04, K05 | Đạt |
| UC16 | Kiểm duyệt danh mục đề tài toàn Khoa | UC16, K14 | Đạt |
| UC17 | Xem báo cáo thống kê tình hình đăng ký | K01, K13 | Đạt |
| UC18 | Chạy phân công tối ưu tự động (Pha 1) | K06, K07 | Đạt |
| UC19 | Điều phối thủ công & Gợi ý vét chỗ (Pha 2) | K08, K09 | Đạt |
| UC20 | Chốt bảng phân công & Công bố kết quả | K10, K11, K12 | Đạt |
| UC21 | Xem báo cáo so sánh thuật toán & Tải GV | K13 | Đạt |
| UC22 | Tra cứu nhật ký kiểm toán (Audit Log) | UC22, B10 | Đạt |
| UC23 | Cấu hình trọng số đánh giá đa tiêu chí AHP | UC23, B05 | Đạt |
