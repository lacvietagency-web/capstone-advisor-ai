# UI Review — Yêu cầu dữ liệu & Phản hồi Backend

## 1. Màn hình Sinh viên — Đăng ký nguyện vọng (`/nguyen-vong/`)
- **Template:** `templates/catalog/student_preferences.html`
- **View:** `catalog.views.student_preferences`
- **Đánh giá hợp đồng dữ liệu hiện tại:**
  - `period`: Cung cấp thông tin đợt đăng ký (`name`, `start_at`, `end_at`, `status`). Đầy đủ.
  - `form`: `PreferenceForm` chứa `nv1`, `nv2`, `nv3` với danh sách đề tài đang mở (`status=OPEN`). Đầy đủ.
  - `top5`: QuerySet `Recommendation` lấy 5 đề tài xếp hạng cao nhất của sinh viên (`topic`, `final_score`, `m1_skill`, `m2_academic`, `m3_field`, `m4_semantic`, `m5_llm`, `reason`, `rank`). Đầy đủ.
  - `scores`: Dictionary `{topic_id: Recommendation}` chứa điểm chi tiết của tất cả đề tài đã đánh giá cho sinh viên. Đầy đủ để hiển thị điểm phù hợp compact ngay khi chọn đề tài bất kỳ.
- **Biến cần thêm:** Không có. Dữ liệu từ PR #11 đã đầy đủ để hiện thực toàn bộ các mục P0 & P1 theo đặc tả `docs/ui/DESIGN.md`.
- **Góp ý cải thiện trong tương lai (P2/P3 - không bắt buộc sprint này):**
  - Có thể bổ sung trường `reason` phong phú hơn từ LLM cho các đề tài ngoài Top-5 nếu có tài nguyên LLM.
  - Hỗ trợ API endpoint `/api/nguyen-vong/` nếu sau này muốn chuyển sang lưu realtime không cần reload trang.
