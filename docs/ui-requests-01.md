# Yêu cầu bổ sung dữ liệu từ Backend (Frontend Requests)

Tài liệu này ghi nhận các biến và cấu hình backend cần bổ sung cho các giao diện theo đặc tả `docs/ui/DESIGN.md`.

---

## 1. View `accounts.views.home` — Bảng điều khiển Khoa (`pages/home_admin.html`)

Theo thiết kế mục 38 & 40 trong `docs/ui/DESIGN.md`, Bảng điều khiển Khoa cần 3 thẻ số liệu KPI và thông tin chi tiết các đợt đăng ký:

- **Biến `n_students`**:
  - *Mục đích*: Hiển thị tổng số sinh viên đủ điều kiện trong thẻ KPI "Sinh viên".
  - *Gợi ý backend*: `n_students = Student.objects.count()` (hoặc lọc theo điều kiện GPA/tín chỉ nếu có).
  - *Hiện trạng*: View `home` hiện chỉ truyền `n_topics` và `periods`, chưa có `n_students` (template đang fallback hiển thị `—`).

- **Biến `n_periods`**:
  - *Mục đích*: Hiển thị tổng số đợt đăng ký trong năm học trong thẻ KPI "Đợt đăng ký".
  - *Gợi ý backend*: `n_periods = RegistrationPeriod.objects.count()`.
  - *Hiện trạng*: View `home` hiện chỉ truyền 5 đợt gần nhất (`[:5]`), chưa có biến đếm tổng số đợt.

- **Số sinh viên đăng ký theo đợt (`period.student_count`)**:
  - *Mục đích*: Hiển thị số lượng sinh viên đã gửi nguyện vọng cho từng đợt đăng ký tại bảng `Danh sách đợt đăng ký`.
  - *Gợi ý backend*: Sử dụng `annotate(student_count=Count('preference__student', distinct=True))` khi truy vấn `periods`.

---

## 2. Cấu hình Static Files trong `config/settings.py`

- **Cấu hình `STATICFILES_DIRS`**:
  - *Mục đích*: Cho phép Django `runserver` (chế độ phát triển) và lệnh `findstatic`/`collectstatic` nhận diện và phục vụ các tệp tĩnh dùng chung tại thư mục root `static/` (bao gồm `static/css/app.css`).
  - *Gợi ý cấu hình bổ sung trong `config/settings.py`*:
    ```python
    STATICFILES_DIRS = [
        BASE_DIR / "static",
    ]
    ```
  - *Hiện trạng*: Hiện `settings.py` có `STATIC_URL = 'static/'` và `STATIC_ROOT = BASE_DIR / 'staticfiles'`, nhưng chưa khai báo `STATICFILES_DIRS`.
