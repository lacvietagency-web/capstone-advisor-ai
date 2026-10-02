# Cách đội làm việc trên repo này

Đội: **Claude** (phần lõi: CSDL, AI gợi ý, ILP phân công, thực nghiệm; review và merge) · **ChatGPT** (thiết kế UI/UX) ·
**Gemini** (code giao diện) · **Groq/OpenRouter** (dữ liệu mô phỏng, phản biện) · **Hermes** (điều phối) · chủ đồ án **Trịnh Hoàng Thành**.

## Giao việc và trao đổi
- **Mỗi việc là một Issue.** Nhãn: `core` (Claude), `ui` (ChatGPT + Gemini), `docs`, `research`, `review`.
- Bàn bạc, hỏi đáp, phản biện: comment ngay trong Issue hoặc Pull Request. Ghi rõ ai nói (`[Gemini]`, `[ChatGPT]`, `[Claude]`).
- Phần UI cần thêm dữ liệu từ backend: comment trong Issue với nhãn `core`, không tự sửa file `.py`.

## Nhánh và Pull Request
- Không ai đẩy thẳng lên `main`. Mỗi việc một nhánh: `core/<việc>`, `ui/<số issue>-<việc>`, `docs/<việc>`.
- PR ghi `Closes #<số issue>`, kèm ảnh chụp (UI) hoặc kết quả kiểm thử (core).
- Đội UI chỉ sửa `templates/` và `static/`. Máy kiểm tự hoàn tác mọi thay đổi ngoài khu vực đó.
- Claude review rồi merge. `python manage.py test` phải đạt (CI chạy tự động).

## Quy ước
- Giao diện, comment code, tài liệu: tiếng Việt. Tên biến/hàm: tiếng Anh.
- Không đưa file `.env`, mật khẩu, API key lên repo.

## Code sạch (bắt buộc, CI tự kiểm)
Học theo cách GVHD tổ chức OpenCPS (chia tầng, CI tự động, review PR):
- **`ruff check .` và `ruff format --check .` phải sạch** — chạy `ruff check . --fix && ruff format .` trước khi commit.
- **Chia tầng:** view chỉ nhận request → gọi service → trả template. Logic nghiệp vụ/AI nằm trong `services.py`, `engine.py`,
  `solver.py`; model chỉ khai báo dữ liệu. Không viết truy vấn phức tạp trong template.
- **Hàm ngắn, một việc:** độ phức tạp ≤ 10 (ruff C901); hàm dài thì tách.
- **Mỗi model có `__str__`** (trang quản trị đọc được), mỗi công thức có docstring tiếng Việt kèm công thức toán.
- **Có kiểm thử** cho mọi công thức và luồng nghiệp vụ; kiểm thử nghiệm thu do Claude viết trước, code phải đạt.
- **Commit nhỏ, message rõ** (tiếng Việt, nói được *làm gì* và *vì sao*); không commit file sinh ra (db, .env, .venv).
