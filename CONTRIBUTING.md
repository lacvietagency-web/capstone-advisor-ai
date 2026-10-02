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
