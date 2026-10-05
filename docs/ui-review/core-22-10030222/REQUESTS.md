# Yêu cầu bổ sung giao diện (UI Requests) — UC09

Ghi nhận các yêu cầu điều chỉnh giao diện ngoài phạm vi cho phép (`catalog/`, `templates/catalog/`, `config/urls.py`):

---

## 1. Điều hướng và Menu người dùng: Liên kết đến Hồ sơ Giảng viên (`/ho-so-giang-vien/`)

- **Vị trí 1: Thanh điều hướng chung (`templates/base.html`)**:
  - *Mô tả*: Khi người dùng đăng nhập với vai trò Giảng viên (`user.is_lecturer`), hiển thị liên kết nhanh hoặc mục trong menu tới trang hồ sơ cá nhân:
    ```html
    <a class="btn btn-sm btn-outline-primary" href="{% url 'lecturer_profile' %}">
      <i class="bi bi-person-badge me-1"></i>Hồ sơ chuyên môn
    </a>
    ```
- **Vị trí 2: Trang chủ Giảng viên (`templates/pages/home_lecturer.html`)**:
  - *Mô tả*: Thêm nút hoặc thẻ liên kết đưa giảng viên đến trang cập nhật hồ sơ chuyên môn và chỉ tiêu hướng dẫn (`{% url 'lecturer_profile' %}`).
  - *Dữ liệu sẵn sàng*: URL pattern `lecturer_profile` (`/ho-so-giang-vien/`) đã được cấu hình và hoạt động.
