LUẬT CHUNG ĐỘI GIAO DIỆN — ATLAS V3.4 (máy kiểm sẽ chặn mọi vi phạm)
1. Thông số có hiệu lực (mới nhất thắng): .webby/v3/truong/g4-chot.md (V3.5, học bố cục web trường) > .webby/v3/b2-chot.md (V3.4) > .webby/v3/a2-thong-so.md (V3.3).
   Ảnh web trường để học bố cục: .webby/v3/truong/truong-sheet.jpg (KHÔNG chép logo/tên trường, không chép code). Ảnh .webby/v3/renders/*.png chỉ để nhìn bố cục;
   số liệu trong ảnh là ví dụ — KHÔNG gõ cứng vào template, mọi con số lấy từ biến context.
2. CHỈ dùng class có trong static/css/atlas.css và mã HTML mẫu trong templates/styleguide.html (xem trang /mau-giao-dien/).
   Không thêm <style>, không file CSS mới, không sửa atlas.css/base.html/components (thuộc Claude). style="" chỉ được dùng cho giá trị động
   từ dữ liệu (VD style="--v:{{ x }}%"). Thiếu thành phần → ghi BLOCKED_SPEC vào ui-review/REQUESTS-<nhóm>.md.
3. Không dùng class cũ mz-*, nova-*, app-card, bi bi-*, emoji, ảnh ngoài. Icon CHỈ qua {% include "components/icon.html" with name="<tên>" %}
   với tên file có trong static/icons/. Không include các component cũ: alert, button, confirm_modal, data_table, empty_state, metric_ribbon,
   reason_block, score_block, status_badge, toast (sẽ bị xoá). Dùng: status, score, evidence, note, banner, empty, journey, period, pagination, reject_modal.
4. Khung mỗi trang: {% extends "base.html" %} → block title → (block canvas_class: at-canvas--read cho trang form/hồ sơ) → block content:
   <header class="at-page-header"> (breadcrumb, h1, at-page-desc, at-page-actions) → các <section class="at-panel"> trong <div class="at-stack">.
   MỖI khối nghiệp vụ = <section class="at-panel"> có <div class="at-panel-header"><div><h2>Tên khối</h2><p>mô tả ngắn</p></div>[nút]</div> là CON ĐẦU TIÊN (CSS tự vẽ thanh đầu đề 42px).
   Mỗi trang đúng MỘT h1 và tối đa MỘT nút btn-primary nổi bật ở đầu trang.
5. Bảng: <table class="at-table d-none d-md-table"> + danh sách thẻ <div class="at-list d-md-none"> dùng CÙNG dữ liệu (cùng page_obj).
   Không tô nền cả dòng theo trạng thái; trạng thái nằm ở cột riêng bằng components/status.html. Điểm căn phải (at-td-num).
6. Điểm AI: components/score.html (điểm tổng, chữ số lớn) + components/evidence.html (M1–M5) + components/note.html (lý do từ rec.reason).
   Không có điểm → để component tự ghi "Chưa có điểm"/"Chưa đánh giá"; KHÔNG hiện 0 hay "—" thay điểm. Không icon sparkles trang trí.
7. Trạng thái rỗng: components/empty.html với tiêu đề nói ĐÚNG lý do (VD "Chưa có sinh viên đăng ký đề tài này"), không "Không có dữ liệu".
8. Giữ NGUYÊN mọi: name="" của input, csrf_token, action/method form, url name, biến context đang dùng, chữ mà tests đang kiểm
   (chạy `grep -n assertContains */tests*.py` để biết chữ nào phải giữ). Không sửa file .py.
9. Chữ tiếng Việt có dấu, câu ngắn, không thuật ngữ tiếng Anh khi có từ Việt. Không chữ nhỏ hơn 12px (đã lo bởi atlas.css nếu không tự đặt cỡ chữ).
10. Kiểm trước khi nộp: `RECOMMEND_SEMANTIC=0 RECOMMEND_LLM=0 .venv/bin/python manage.py test` phải OK.
