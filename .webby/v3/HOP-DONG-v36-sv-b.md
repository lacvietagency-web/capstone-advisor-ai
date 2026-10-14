NHÓM sv-b — V3.6. Ảnh duyệt: v36/renders/08-sv-ho-so, 09-sv-nguyen-vong, m09-sv-nguyen-vong. Hợp đồng số liệu: v36/spec-sv.md (màn 08, 09). Trang: student_profile, student_preferences, _pref_actions.
Biến MỚI có sẵn:
- student_profile: completeness, completeness_items → khối "Mức độ hoàn thiện hồ sơ" (cột phải). Thông tin SV chỉ xem: họ tên, MSSV, ngành, GPA (KHÔNG email/SĐT/lớp/GV cố vấn).
  Mức kỹ năng: nút tròn có nhãn chữ 1 Cơ bản … 5 Thành thạo — nhưng PHẢI giữ input name="skills-N-level" (radio cùng name, value 1–5). Lĩnh vực: giữ select mức 1–3 (M3 cần mức).
- student_preferences (đợt mở): pref_rows [{rank, pref (submitted, status, reject_reason, lecturer_note), rec, eligibility, remaining}], is_submitted, submitted_at, top5, scores, form (nv1–nv3).
  HAI NÚT submit trong cùng form: name="action" value="draft" ("Lưu nháp") và value="submit" ("Nộp nguyện vọng"); khi is_submitted: banner "Đã nộp chính thức lúc …" + form riêng
  POST action=withdraw ("Rút về nháp để sửa"). Nhận xét GV (pref.lecturer_note) chỉ hiện khi status khác PENDING. Kiểm tra điều kiện từ eligibility; "Còn N chỗ" từ remaining.
  Điện thoại: hai nút nằm trong <div class="at-actionbar">.
- Chế độ chỉ xem (period None): giữ như hiện tại.
KHÔNG: chuông, năm 2025.
PAGE sv001 /ho-so/ · PAGE sv001 /nguyen-vong/
