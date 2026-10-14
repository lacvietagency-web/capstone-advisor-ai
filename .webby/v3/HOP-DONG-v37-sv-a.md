NHÓM sv-a — màn 11 Chi tiết đề tài (templates/catalog/topic_detail.html, lớp .pg-11), 12 Kết quả (templates/allocate/student_result.html, .pg-12);
bản điện thoại m07 (pages/home_student.html), m10 (catalog/topic_list.html), m11 theo bản desktop. CSS: static/css/pages/sv-a.css.
Màn 07 và 10 desktop ĐÃ ĐẠT — không đổi bố cục desktop của 2 trang này, chỉ sửa phần @media (max-width: 767.98px) nếu diff mobile cần.
Việc: làm hết .webby/v3/v37/diff-11-sv-chi-tiet-de-tai.md và diff-12-sv-ket-qua.md.
Biến mới (lõi đã có):
- topic_detail: checklist (list {label, state ok|warn|fail, value}) → khối "Kiểm tra điều kiện"; skills[].ratio (0,25…) cột Trọng số;
  ahp.criteria[i].ratio / .percent / .code / .label → cột "Trọng số (AHP)"; {% load atlas_tags %}: rec.reason|reason_points → "Lý do gợi ý" đánh số;
  topic.technologies|csv_items → thẻ từ khoá (không có thì bỏ nhóm). topic.code, topic.objectives giữ hiển thị gọn trong "Mô tả đề tài".
  Nút "Đăng ký nguyện vọng" chỉ khi đợt mở và SV đủ điều kiện (giữ điều kiện template đang dùng). Bỏ nút "Danh sách đề tài" ở đầu trang.
- student_result: journey (4 mục như trang chủ — dùng components/journey.html), recommendation (M1–M5 của đề tài được phân → components/evidence.html),
  published_at (có thì ghi "Công bố lúc H:i d/m/Y"), preferences (NV đã nộp; NV trúng ⇔ p.rank == preference_rank và topic khớp → "Đạt", còn lại "Không đạt"),
  allocation.get_source_display → badge "Phân công bằng …". Nút "Tải biên bản" = window.print() (LUẬT 0g); "Xem chi tiết đề tài" → topic_detail.
  Trường hợp chưa công bố / không được xếp giữ nguyên nội dung hiện có (banner + empty).
