NHÓM gv — màn 13 Tổng quan GV (templates/pages/home_lecturer.html, .pg-13), 14 Đề tài của tôi (templates/catalog/lecturer_topics.html, .pg-14),
16 Duyệt SV (templates/catalog/lecturer_registrations.html, .pg-16); điện thoại m16. CSS: static/css/pages/gv.css.
Việc: làm hết .webby/v3/v37/diff-13-gv-tong-quan.md, diff-14-gv-de-tai.md, diff-16-gv-duyet-sv.md. Chủ: "chưa nhìn thấy được tên sinh viên".
Biến mới (lõi đã có):
- home_lecturer: review_rows (mỗi dòng 1 NV: r.pref.topic, r.pref.student.user.get_full_name, r.pref.student.student_code, r.score (điểm AI, có thể None),
  r.pref.rank, r.pref.status/get_status_display), review_total, review_q, review_tt. Bộ lọc = <form method="get"> với input name="q" và
  select name="tt" (cho = Chờ duyệt, dong-y = Đồng ý, tu-choi = Từ chối, tat-ca = Tất cả). Nút "Phân tích" →
  {% url 'lecturer_registrations' r.pref.topic_id %}?mo={{ r.pref.pk }} (trang đích tự mở ngăn kéo của SV đó).
  n_topics, n_students, n_pending, n_accepted cho khối "Tổng quan đề tài hướng dẫn" (số to căn giữa, màu như diff). topics vẫn có nếu cần.
- lecturer_registrations: rows[].checklist cho khối "Kiểm tra điều kiện đăng ký" trong ngăn kéo; giữ id ngăn kéo atStudent{{ row.pref.pk }}, form duyệt/từ chối,
  ô "Nhận xét giảng viên" (name giữ nguyên), reject_modal. Script ?mo= ở cuối trang PHẢI giữ.
- lecturer_topics: chỉ hiển thị trạng thái có thật của đề tài (không bịa "Tạm khoá" nếu không có); bỏ nút "⋮" nếu không có chức năng.
