NHÓM sv-a — V3.6. Ảnh duyệt: v36/renders/07-sv-trang-chu, m07-sv-trang-chu, 10-sv-danh-sach-de-tai, m10-sv-danh-sach-de-tai, 11-sv-chi-tiet-de-tai, m11-sv-chi-tiet-de-tai, 12-sv-ket-qua.
Hợp đồng số liệu: v36/spec-sv.md (màn 07, 10, 11, 12). Trang: home_student, topic_list, topic_detail, student_result.
Biến MỚI có sẵn:
- home_student: completeness (0–100), completeness_items [(nhãn, đã có?)] — nếu SV chưa có gợi ý vì thiếu hồ sơ: dùng {% include "components/profile_missing.html" %} (màn 03).
- topic_list: tab ("" | "1" | "0"), tab_counts {"all","ok","no"} → tabs "Tất cả (N)", "Đủ điều kiện (N)", "Chưa đủ điều kiện (N)" là link ?dk=1/0 GIỮ các tham số lọc khác;
  sort ("score"|"title"|"difficulty"|"capacity"|"nv1") → tiêu đề cột bảng là link ?sort=...; mỗi topic có .code, .remaining (chỗ còn), .technologies, .eligibility, .match_score.
  Nút "Đăng ký" CHỈ khi SV đủ điều kiện và có open_period; còn lại hiện lý do "cần … có …".
- topic_detail: topic.code, topic.objectives, topic.technologies, remaining (chỗ còn / topic.capacity), eligibility, recommendation, skills (mỗi skill có .share %), prerequisites.
- student_result: giữ nguyên biến cũ.
KHÔNG: chuông, "Tải biên bản", năm 2025, số mẫu trong ảnh.
PAGE sv001 /trang-chu/ · PAGE sv001 /danh-sach-de-tai/ · PAGE sv001 /ket-qua/
