NHÓM gv — 5 trang Giảng viên. Ảnh: renders/05-gv-duyet-sv-desktop.png. Rail GV 3 mục (đã có trong base). Không tạo route mới.
1. templates/pages/home_lecturer.html — context: topics (annotate pending_count, .fields), n_topics, n_students, n_pending, n_accepted.
   Header (h1 "Tổng quan", nút primary "Thêm đề tài" → lecturer_topic_new) → at-ledger 4 mục (Đề tài, SV đăng ký, Chờ duyệt (warn nếu >0), Đã đồng ý) →
   panel "Đề tài cần duyệt" bảng/thẻ: tên, lĩnh vực, sức chứa, số chờ duyệt, nút "Duyệt" → lecturer_registrations. Rỗng: empty empty-topics "Bạn chưa có đề tài nào" + Thêm đề tài.
   Giữ chữ "Chưa có đề tài" (test kiểm).
2. templates/catalog/lecturer_topics.html — context: lecturer, topics. Bảng: tên (link sửa), lĩnh vực, độ khó, sức chứa, trạng thái (status OPEN/DRAFT/CLOSED), thao tác: "Sinh viên đăng ký", "Sửa" (btn-icon square-pen).
3. templates/catalog/lecturer_topic_form.html (at-canvas--read) — context: form (title, description, fields CheckboxSelectMultiple, difficulty, min_gpa, capacity, status), skill_formset (prefix skills: skill, required_level, weight, is_mandatory, DELETE), topic.
   Panel thông tin (field theo thứ tự, fields trong at-check-grid) → panel "Kỹ năng yêu cầu" (at-repeat-row--wide: kỹ năng, mức, trọng số, bắt buộc (checkbox), xoá) + thêm dòng → at-form-actions.
   GIỮ management_form và name field; JS thêm dòng viết gọn trong extra_js.
4. templates/catalog/lecturer_registrations.html — context: topic, rows [{pref (student.user, rank, status, reject_reason, created_at), rec (Recommendation|None), eligibility}].
   Header (breadcrumb Đề tài của tôi / tên; h1 "Sinh viên đăng ký"; meta trạng thái, sức chứa; nút secondary "Sửa đề tài") → at-ledger (Tổng hồ sơ, Chờ duyệt, Đồng ý, Từ chối — đếm trong template) →
   bảng: #, MSSV, họ tên, GPA, NV (at-rank), điểm (score sm), trạng thái (status), thao tác: "Phân tích" (mở offcanvas riêng của dòng) — KHÔNG đặt Đồng ý/Từ chối/Chờ duyệt xếp dọc trong ô.
   Mỗi dòng có offcanvas-end id="atStudent{{ pref.pk }}": thông tin SV, evidence detail=True, note lý do AI, at-steps điều kiện (eligibility), giới thiệu SV (pref.student.about);
   at-drawer-footer: form POST (csrf, preference_id, action=accept) nút primary "Đồng ý" + nút secondary "Từ chối" mở components/reject_modal.html (data-at-fill preference_id + student).
   Đã duyệt: hiện status + lý do từ chối, không hiện nút. Include reject_modal một lần (action_url = trang hiện tại). Rỗng: empty empty-registrations.
5. templates/catalog/lecturer_profile.html (at-canvas--read) — context: lecturer, form (department, fields, max_students), is_locked, is_faculty_admin, lecturers_list.
   Khoa: select chọn giảng viên (GET lecturer_id, autosubmit). is_locked: banner warning "Đợt đã đóng — chỉ tiêu bị khoá" + ô readonly.
PAGE gv001 /trang-chu/ · PAGE gv001 /de-tai/ · PAGE gv001 /de-tai/them/ · PAGE gv001 /ho-so-giang-vien/
