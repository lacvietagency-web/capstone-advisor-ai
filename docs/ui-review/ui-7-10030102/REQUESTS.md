# Yêu cầu dữ liệu bổ sung từ Backend (Front-end UI Requests)

Tài liệu ghi nhận các yêu cầu dữ liệu hoặc cải tiến từ phía UI theo quy định của dự án (`docs/ui/DESIGN.md`), không tự ý sửa đổi code Python/Backend.

---

### 1. View `student_profile` (`catalog/views.py`)

- **Màn hình**: Trang Hồ sơ sinh viên (`/ho-so/` - `student_profile.html`)
- **Biến đề xuất thêm vào context**:
  - `profile_completeness`: Kiểu số nguyên (0 - 100), biểu thị tỷ lệ % hoàn thiện hồ sơ sinh viên.
  - `completion_tips`: Danh sách chuỗi (`list[str]`), chứa các gợi ý cụ thể để sinh viên hoàn thiện hồ sơ (ví dụ: `["Bổ sung phần tự giới thiệu", "Thêm ít nhất 1 lĩnh vực quan tâm"]`).
- **Lý do**:
  - Theo mục 10 của `docs/ui/DESIGN.md`, card "Mức độ hoàn thiện hồ sơ" cần thể hiện tiến độ thực tế của sinh viên.
  - Hiện tại, front-end đang tính toán động tại client-side (thông qua JavaScript kiểm tra độ dài văn bản giới thiệu, số kỹ năng và số lĩnh vực đã điền). Nếu backend chuẩn hóa công thức tính và truyền trực tiếp qua context thì dữ liệu này có thể được đồng bộ thống nhất giữa trang sinh viên và dashboard quản trị của Khoa.

---

### 2. Formset Widgets trong `catalog/forms.py` (Đề xuất tối ưu hóa UX)

- **Formset**: `StudentSkillFormSet` và `StudentInterestFormSet`
- **Đề xuất**:
  - Đối với `StudentSkill.level` (thang điểm 1–5): Cho phép cung cấp `choices` dạng dropdown (Select) với các nhãn tiếng Việt tương ứng:
    - `1`: 1 - Mới tiếp cận
    - `2`: 2 - Cơ bản
    - `3`: 3 - Khá
    - `4`: 4 - Tốt
    - `5`: 5 - Thành thạo chuyên sâu
  - Đối với `StudentInterest.level` (thang điểm 1–3):
    - `1`: 1 - Quan tâm
    - `2`: 2 - Yêu thích
    - `3`: 3 - Ưu tiên hàng đầu cho đồ án
- **Lý do**:
  - Hiện tại trường `level` đang được Django render mặc định thành `<input type="number">`. Front-end đã bổ sung nhãn huy hiệu (badge/pill) động bên cạnh ô nhập để người dùng nhận biết rõ ý nghĩa của từng mức điểm. Việc backend cấu hình `Select(choices=...)` tại form sẽ giúp hiển thị đồng nhất cả khi trình duyệt tắt JavaScript.
