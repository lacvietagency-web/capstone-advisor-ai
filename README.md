# Capstone Advisor AI

Hệ thống thông minh hỗ trợ tư vấn và tối ưu hóa quy trình đăng ký đồ án tốt nghiệp.
Đồ án tốt nghiệp — SV Trịnh Hoàng Thành · GVHD ThS. Đặng Khánh Trung · Khoa CNTT, Trường Đại học Công nghệ Đông Á (EAUT).

## Chức năng
- **Sinh viên:** hồ sơ năng lực, nhận Top 5 đề tài gợi ý kèm lý do, đăng ký 3 nguyện vọng.
- **Giảng viên:** đăng đề tài (kỹ năng yêu cầu, môn tiên quyết, sức chứa), xem sinh viên đăng ký.
- **Khoa:** quản lý dữ liệu, mở/đóng đợt, chạy phân công tối ưu, duyệt và công bố, thống kê.

## Công nghệ
Python · Django 5 · MySQL (hoặc SQLite khi chạy thử) · Bootstrap 5 · sentence-transformers · PuLP (ILP) · LLM qua API miễn phí / Ollama.

## Cài đặt và chạy (Windows / Linux)
```bash
git clone <địa chỉ repo>
cd capstone-advisor
python -m venv .venv
.venv\Scripts\activate            # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env            # Linux/macOS: cp .env.example .env
python manage.py migrate
python manage.py seed_demo        # tạo dữ liệu mô phỏng: 100 SV, 15 GV, 50 đề tài
python manage.py createsuperuser  # tài khoản Khoa
python manage.py runserver
```
Mở http://127.0.0.1:8000 — tài khoản demo: `sv001` / `gv001` mật khẩu `123456`.

## Cấu trúc
| Thư mục | Nội dung |
|---|---|
| `accounts/` | Tài khoản, 3 vai trò, trang chủ theo vai trò |
| `catalog/` | Dữ liệu nghiệp vụ: SV, GV, đề tài, kỹ năng, đợt đăng ký, nguyện vọng; lệnh `seed_demo` |
| `recommend/` | **AI gợi ý** — mô hình kết hợp M1–M5 (kỹ năng, học lực, lĩnh vực, ngữ nghĩa, LLM) |
| `allocate/` | **Phân công tối ưu** — ILP (PuLP) và Greedy |
| `reports/` | Thống kê cho Khoa |
| `templates/` | Giao diện |
| `docs/` | Giải thích dễ hiểu từng phần + sổ tay bảo vệ |

## Kiểm thử
```bash
python manage.py test
```

Giấy phép: Apache-2.0.
