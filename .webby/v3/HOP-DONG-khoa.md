NHÓM khoa — 4 trang Khoa. Ảnh: renders/06-khoa-thongke-desktop-toi.png (+ thông số PHẦN 4 mục 18–21). Canvas rộng (mặc định).
1. templates/pages/home_admin.html — context: n_topics, n_students, n_periods, periods (annotate student_count). Header (h1 "Tổng quan Khoa", primary "Mở trang phân công")
   → period.html (current_period) → at-ledger (SV, đề tài, đợt) → panel "Các đợt đăng ký" bảng (tên, thời gian, SV, trạng thái, nút Phân công ?period_id=) → panel lối tắt (at-list at-item link: Phân công, Thống kê, Nhập Excel, Giảng viên, Quản trị).
   Giữ chữ "Bảng điều khiển Khoa" (test kiểm) — dùng làm h1.
2. templates/allocate/dashboard.html — context: periods, period, page_obj (Allocation: student.user, student.gpa, topic.lecturer, preference_rank, match_score, source, status), total_count, allocations (đã lọc),
   metrics (assigned_rate, nv1_rate, top3_rate, avg_match, unassigned_count, elapsed_time — có thể None), status, rank, sort, q, per_page, per_page_choices, querystring, lecturers, fields, lecturer_id, field_id, open_topics.
   Header (h1 "Phân công đề tài"; select đợt GET period_id autosubmit; 2 form POST data-at-busy: action=run_ilp (primary "Chạy tối ưu ILP"), action=run_greedy (secondary)) →
   period.html → (chưa có kết quả) empty "Chưa chạy phân công cho đợt này" → at-ledger: SV (total_count), Đã xếp %, Đạt NV1 %, Đạt Top 3 %, Điểm TB (ai), Chờ pha 2 (warn), Thời gian giải →
   panel biểu đồ (canvas data-at-chart: bar "Kết quả theo nguyện vọng": NV1/NV2/NV3/ngoài NV/chưa xếp — đếm từ allocations bằng template) →
   panel bảng (at-panel--flush): chip status (Tất cả/Chưa xếp/Đã xếp, giữ tham số khác), toolbar (q, rank, lecturer, field, sort) → bảng 20 dòng/trang từ page_obj:
   MSSV, sinh viên+GPA, đề tài+GVHD, NV, điểm, nguồn, trạng thái, nút "Chi tiết" mở MỘT offcanvas-end chung id="atAllocDrawer" bằng
   data-at-drawer-url="{% url 'allocation_student_detail' period.pk a.student.pk %}" data-at-drawer-title="<tên SV>" (mảnh HTML có sẵn: templates/allocate/_student_drawer.html — KHÔNG sửa)
   → pagination.html (unit "sinh viên", per_page, per_page_choices) → panel "Chốt và công bố" (chỉ khi period.status != PUBLISHED và có kết quả): nút mở modal 2 bước
   (bước 1 tóm tắt đã xếp/chưa xếp; bước 2 input data-at-confirm-text="CÔNG BỐ"; form POST action=publish data-at-busy). Đã công bố: banner success.
   KHÔNG còn: bảng 100 dòng, gợi ý pha 2 dạng ?suggest_student_id trong trang, select xếp tay trong từng dòng (đã chuyển vào ngăn kéo).
3. templates/reports/statistics.html — context: periods, period, reg_stats, topic_nv1_list, field_list, lecturer_load, load_source, comparison, chart_data (dict, xuất bằng {{ chart_data|json_script:"atStats" }}).
   Header + select đợt → at-ledger từ reg_stats → at-grid các panel biểu đồ (đăng ký, đề tài NV1 nhiều nhất, lĩnh vực, tải GV so chỉ tiêu, so sánh ILP vs Greedy):
   mỗi biểu đồ canvas data-at-chart (màu "var(--at-chart-N)"), dưới mỗi biểu đồ có bảng số liệu (at-table) để kiểm chứng. Giữ mọi chữ test đang kiểm trong reports/tests.py.
   Viết JS dựng cấu hình biểu đồ từ #atStats trong extra_js (nạp vendor/chart.umd.min.js bằng {% static %}), gán vào canvas.dataset.atChart TRƯỚC sự kiện load.
4. templates/catalog/faculty_import.html — context: result (ok, errors [dòng/lỗi], stats, rows [(nhãn, số)], filename), max_mb. Bước 1 tải mẫu (link faculty_import_sample) → bước 2 form upload
   (enctype multipart, input name="file" accept .xlsx, data-at-busy) → kết quả: ok → banner success + bảng rows; lỗi → banner danger + bảng lỗi theo dòng. Giữ name="file".
PAGE khoa01 /trang-chu/ · PAGE khoa01 /khoa/phan-cong/ · PAGE khoa01 /khoa/thong-ke/ · PAGE khoa01 /khoa/nhap-excel/
