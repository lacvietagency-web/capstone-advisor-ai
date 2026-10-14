NHÓM auth — màn 01 Đăng nhập. File: templates/registration/login.html + static/css/pages/auth.css (lớp trang .pg-01).
Việc: làm hết .webby/v3/v37/diff-01-dang-nhap.md. Ảnh: .webby/v3/v36/renders/01-dang-nhap.jpg, so sánh .webby/v3/v37/pairs/01-dang-nhap.jpg.
Asset hoạ tiết ChatGPT đã vẽ (SVG tĩnh, dùng làm background-image trong auth.css hoặc <img alt="" aria-hidden="true">):
  static/brand/ — xem các file login-*.svg có trong thư mục (chỉ dùng file có thật).
Giữ: form POST {% url 'login' %}, name="username"/"password", csrf, data-at-busy, nút data-at-demo="sv001|gv001|khoa01" (JS điền tên đăng nhập),
banner lỗi "Thông tin đăng nhập không chính xác". Thêm nút hiện/ẩn mật khẩu (icon eye / eye-off, aria-label, JS trong block extra_js).
Không thêm "Quên mật khẩu?" (chưa có chức năng). Phụ đề thương hiệu "Academic Decision Workspace" được dùng.
