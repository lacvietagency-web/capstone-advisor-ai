# Hợp đồng ngắn P1 — Các trang SINH VIÊN theo Mosaic AI (webbyLucifer GĐ8)
ĐẦU VÀO: .webby/DESIGN-SPEC-mosaic.md (PHẦN 1 phân rã trang SV, PHẦN 4 thành phần) · .webby/NGUYEN-LIEU-AP-DUNG.md ·
.webby/BIEN-BAN-HOP-GIAO-DIEN.html (mục 3: KHÔNG dải số liệu cấp Khoa ở màn SV; bảng chỉ hiện điểm tổng, bấm mới xem M1–M5) ·
NỀN MÓNG ĐÃ CÓ (P0): templates/base.html, templates/components/*.html (đọc templates/components/README.md), static/css/mosaic.css, static/js/mosaic.js.
BẮT BUỘC dùng thành phần P0; chỉ thêm CSS mới vào cuối static/css/mosaic.css trong khối /* P1 */ khi thực sự cần.
Ảnh tham chiếu (chỉ nhìn, không đo pixel): .webby/renders/03-sv-trangchu-mobile-sang.jpg, 04-…-toi.jpg, 05-sv-chitiet-detai-mobile.jpg,
06-sv-hoso-mobile.jpg, 07-sv-nguyenvong-mobile.jpg, 08-sv-danhsach-detai-desktop.jpg, 09-sv-ketqua-mobile.jpg, 20-trangthai-rong.jpg.

PHẠM VI (chỉ templates/ + static/): làm lại 6 trang, giữ NGUYÊN mọi biến Django, form field name, csrf, url name, logic điều kiện hiện có:
1. templates/pages/home_student.html — Trang chủ SV: thông tin SV + trạng thái đợt (tiến trình) + Top 5 gợi ý (score_block + reason_block) + nguyện vọng.
2. templates/catalog/student_profile.html — Hồ sơ năng lực (formset kỹ năng/lĩnh vực thêm–xoá dòng phải CHẠY ĐƯỢC; giữ management form).
3. templates/catalog/student_preferences.html — Nguyện vọng NV1–NV3; NV bị GV từ chối hiện nhãn "Từ chối" + LÝ DO (biến pref.reject_reason).
4. templates/catalog/topic_list.html — Danh sách đề tài (thanh lọc dính, điểm tổng, nhãn "Chưa đủ điều kiện" + lý do, phân trang).
5. templates/catalog/topic_detail.html — Chi tiết đề tài (điểm tổng + M1–M5 + lý do + điều kiện; không nút đăng ký khi chưa đủ điều kiện).
6. templates/allocate/student_result.html — Kết quả: phân biệt rõ "Chưa công bố" và "Chính thức".
Trạng thái rỗng dùng components/empty_state với minh hoạ static/mosaic/illus. Icon chỉ từ static/mosaic/icons.
KIỂM TRA: manage.py test xanh; ruff sạch; không tràn ngang ở 390px; sáng & tối đều đọc được.
BÁO CÁO: 3–5 dòng đầu ui-review/REQUESTS.md + bảng nguyên liệu đã dùng; NEED_ASSET/BLOCKED_SPEC nếu có.
PAGE sv001 /trang-chu/ · PAGE sv001 /ho-so/ · PAGE sv001 /nguyen-vong/ · PAGE sv001 /danh-sach-de-tai/ · PAGE sv001 /danh-sach-de-tai/1/ · PAGE sv001 /ket-qua/
