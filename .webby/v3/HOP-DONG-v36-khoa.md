NHÓM khoa — V3.6. Ảnh duyệt: v36/renders/18-khoa-tong-quan, 19-khoa-phan-cong, m19-khoa-phan-cong, 20-khoa-thong-ke, 21-khoa-nhap-excel. Hợp đồng số liệu: v36/spec-khoa.md.
Trang: home_admin, dashboard (phân công), statistics, faculty_import.
- dashboard: như ảnh 19 — ô "Chốt & công bố" đặt cạnh biểu đồ (giữ modal 2 bước + data-at-confirm-text); số trên đầu cột (Chart.js: vẽ nhãn bằng plugin nội tuyến nhỏ trong extra_js);
  bảng giữ MỌI bộ lọc hiện có (q, status, rank, lecturer, field, score_min, sort, per_page) và ngăn kéo data-at-drawer-url; dòng chưa xếp có link "Xếp tay" mở cùng ngăn kéo.
- statistics: "Điểm TB" theo thang 100.
- faculty_import (MỚI 2 bước): form tải lên gửi action=check (input name="file"); khi result.pending: hiện kết quả kiểm tra + form POST action=confirm "Xác nhận nhập" và nút "Huỷ" (link về trang).
  result: ok, errors (danh sách chuỗi lỗi theo dòng), rows [(nhãn, số)], filename, pending. Một file mẫu 4 sheet (faculty_import_sample), chỉ .xlsx, tối đa {{ max_mb }} MB (KHÔNG CSV, KHÔNG 3 file mẫu).
- home_admin: số liệu cùng một màu.
KHÔNG: vai "Giảng viên" ở góc phải, năm 2025.
PAGE khoa01 /trang-chu/ · PAGE khoa01 /khoa/phan-cong/ · PAGE khoa01 /khoa/thong-ke/ · PAGE khoa01 /khoa/nhap-excel/
