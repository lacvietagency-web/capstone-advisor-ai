NHÓM gv — V3.6. Ảnh duyệt: v36/renders/13-gv-tong-quan, 14-gv-de-tai, 15-gv-form-de-tai, 16-gv-duyet-sv, m16-gv-duyet-sv, 17-gv-ho-so. Hợp đồng số liệu: v36/spec-gv.md.
Trang: home_lecturer, lecturer_topics, lecturer_topic_form, lecturer_registrations, lecturer_profile.
Biến/trường MỚI có sẵn:
- topic.code (tự sinh, chỉ hiển thị), lecturer_topic_form: form có thêm objectives, technologies, review_note; prereq_formset (prefix "prereqs": course, min_score, DELETE) —
  PHẢI render đủ {{ prereq_formset.management_form }} + từng form (có nút thêm dòng như kỹ năng). KHÔNG có "Lưu nháp", "Nhận đăng ký NV1", "Cho phép chỉnh sửa sau công bố".
- lecturer_registrations: chân ngăn kéo có <textarea name="note"> "Nhận xét giảng viên" nằm TRONG form Đồng ý (gửi kèm); pref.lecturer_note hiển thị nếu đã có.
  Điện thoại: khi ngăn kéo mở, thanh nút nằm trong ngăn kéo, không chồng thanh đáy.
- lecturer_profile: form có academic_title, phone, bio, keywords (+ department, fields, max_students); n_topics, n_guided, field_stats [(lĩnh vực, số đề tài)] →
  khối "Chỉ tiêu hướng dẫn" (max_students sửa được trừ khi is_locked; n_topics, n_guided chỉ đọc) + "Thống kê theo lĩnh vực" (thanh ngang). SĐT chỉ hiện trên trang này.
- home_lecturer: hạn duyệt = current_period.end_at.
KHÔNG: chuông, ảnh người, mã "GVHD: 015".
PAGE gv001 /trang-chu/ · PAGE gv001 /de-tai/ · PAGE gv001 /de-tai/them/ · PAGE gv001 /ho-so-giang-vien/
