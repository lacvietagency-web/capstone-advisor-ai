NHÓM khoa — màn 18 Bảng điều khiển Khoa (templates/pages/home_admin.html, .pg-18), 19 Phân công (templates/allocate/dashboard.html, .pg-19);
điện thoại m19. CSS: static/css/pages/khoa.css. Màn 20, 21 đã đạt — không động.
Việc: làm hết .webby/v3/v37/diff-18-khoa-tong-quan.md và diff-19-khoa-phan-cong.md (+ .webby/v3/v37/asset-khoa.md nếu có SVG).
Biến mới: home_admin có thêm n_lecturers, n_with_pref (SV có NV) cho khối "Tổng quan số liệu" 5 ô (số to căn giữa, mỗi ô 1 màu như diff).
Lối tắt: icon Lucide trong ô nền nhạt (chỉ icon có trong static/icons/; thiếu → ghi NEED_ASSET).
dashboard: giữ NGUYÊN mọi name/param GET của bộ lọc đang có (status, rank, lecturer, field, score_min, score_max, q, sort, per_page, page) và form POST
(chạy ILP/Greedy, xếp tay, chốt & công bố + gõ "CÔNG BỐ"). Bố cục bộ lọc theo ảnh: hàng ngang gọn có nhãn; bộ lọc ảnh không có thì gom vào cuối hàng
(không xoá chức năng). Bảng dòng gọn 1 dòng; thao tác dạng liên kết chữ "Xem" / "Xếp tay" mở đúng ngăn kéo hiện có.
Biểu đồ "Kết quả theo nguyện vọng": cấu hình JSON trong data-at-chart; màu ghi dạng "var(--pg19-nv1)" (atlas.js tự đổi var() thành màu, đọc ở :root).
Ngoại lệ luật tiền tố: khoa.css được khai báo biến màu biểu đồ trên :root (và bản tối) với tên bắt đầu --pg19-. Màu từng cột như diff.
