NHÓM sv-a — 4 trang Sinh viên (đọc kết quả). Ảnh tham chiếu: renders/02-sv-trangchu-desktop.png, 03-sv-trangchu-mobile.png, 04-sv-danhsach-detai-desktop.png.
1. templates/pages/home_student.html — context: student, preferences (Preference, có .topic.lecturer), recommendations (≤5 Recommendation có rank, .topic),
   allocation_result (dict: period, is_published, topic, lecturer, preference_rank, match_score, unassigned, status_text), journey.
   Thứ tự: page-header (h1 "Xin chào, <tên>", meta MSSV/ngành/GPA; nút phụ "Hồ sơ năng lực") → components/period.html (allocation_result.period)
   → panel hành trình components/journey.html → nếu đã công bố: panel kết quả (đề tài, GVHD, NV đạt, score) hoặc banner warning "Chưa được phân công trong đợt này";
   chưa công bố: banner neutral status_text → lưới: at-col-8 "Top 5 đề tài phù hợp" (mỗi đề tài = at-item dạng .at-topic: hạng, tên link topic_detail, GVHD,
   score size md, evidence gọn (không detail), note lý do rút gọn at-clamp-3) / at-col-4 "Nguyện vọng đã nộp" (NV1–NV3 + status của từng Preference, nút sửa nếu đợt mở).
   Rỗng: không có recommendations → empty "Chưa có gợi ý vì hồ sơ chưa có kỹ năng" + nút Cập nhật hồ sơ; không preferences → empty empty-preferences.
2. templates/allocate/student_result.html — context: student, period, periods, is_published, status_text, allocation, topic, lecturer, preference_rank, match_score, unassigned.
   Header + (nếu >1 đợt) select đợt GET period_id data-at-autosubmit → period.html → đã công bố & có topic: panel lớn: tên đề tài, GVHD (tên, bộ môn, email),
   NV đạt (at-rank) hoặc "Xếp bổ sung", score lớn, nhãn "Chính thức"; unassigned: empty empty-result "Chưa được phân công trong đợt này"; chưa công bố: empty "Khoa đang xử lý phân công".
3. templates/catalog/topic_list.html — context: page_obj/topics (mỗi topic có .recommendation, .match_score, .ineligible_reason, .eligibility [rule dict: label, required, actual, ok], .nv1_count),
   fields, lecturers, difficulties, selected_*, search_query, querystring, is_student, open_period.
   Header → at-toolbar (form GET: ô q, select field/lecturer/difficulty data-at-autosubmit, at-count "N đề tài", Xoá bộ lọc khi có lọc) → at-list các at-item .at-topic:
   tag lĩnh vực + độ khó, tên (at-clamp-3), GVHD, mô tả at-clamp-3, meta (sức chứa, số NV1, GPA tối thiểu); bên phải score sm (SV) hoặc "Đăng nhập để xem mức phù hợp" (khách);
   chân: nếu ineligible → note warning liệt kê các điều kiện ok=False ("cần X, có Y"); nút "Chi tiết" (secondary) + "Đăng ký nguyện vọng" (primary, chỉ khi SV, đủ điều kiện, open_period).
   → components/pagination.html (unit "đề tài"). Rỗng sau lọc: empty empty-search "Không có đề tài khớp bộ lọc" + Xoá bộ lọc.
4. templates/catalog/topic_detail.html — context: topic, nv1_count, is_student, student, recommendation, skills (TopicSkill), prerequisites, eligibility, ineligible_reason, open_period.
   Header (breadcrumb Đề tài / tên; h1 tên đầy đủ; meta GVHD, lĩnh vực, độ khó, trạng thái; nút primary Đăng ký nguyện vọng nếu đủ điều kiện + open_period) →
   at-grid: at-col-8 [panel Mô tả (at-pre) · panel Kỹ năng yêu cầu (bảng: kỹ năng, mức yêu cầu, trọng số %, bắt buộc) · panel Môn tiên quyết]
   / at-col-4 [SV: panel "Mức độ phù hợp với hồ sơ của bạn": score + evidence detail=True + note lý do; panel Điều kiện đăng ký: at-steps từ eligibility; panel Thông số: sức chứa, NV1, GPA tối thiểu].
   Giữ chữ "Mức độ phù hợp với hồ sơ của bạn", "Đăng ký nguyện vọng".
PAGE sv001 /trang-chu/ · PAGE sv001 /ket-qua/ · PAGE sv001 /danh-sach-de-tai/
