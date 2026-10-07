# Thư viện thành phần giao diện Mosaic AI (`templates/components/`)

Tất cả các thành phần giao diện của Mosaic AI đều tuân thủ Design Tokens (`static/css/mosaic.css`), bộ icon Lucide đóng băng (`static/mosaic/icons/`), minh họa hình học (`static/mosaic/illus/`), và các quy tắc từ `.webby/DESIGN-SPEC-mosaic.md` cùng 14 thẻ nguyên liệu trong `.webby/NGUYEN-LIEU-AP-DUNG.md`.

---

## 1. Icon (`components/icon.html`)
Nạp trực tiếp SVG từ `static/mosaic/icons/` thông qua kỹ thuật CSS mask-image để icon kế thừa màu chữ `currentColor`.

### Cú pháp
```django
{% include "components/icon.html" with name="house" size=18 class="text-primary" %}
```

### Tham số
- `name` (bắt buộc): Tên icon tương ứng với file trong `static/mosaic/icons/<name>.svg` (ví dụ: `house`, `bell`, `sparkles`, `user-check`, `badge-check`, `chevron-right`...).
- `size` (mặc định: `18`): Kích thước hiển thị (px), hỗ trợ `14`, `16`, `18`, `20`, `24`.
- `class` (tuỳ chọn): Các class CSS phụ trợ (ví dụ: `me-1`, `text-success`, `text-muted`).
- `aria_label` (tuỳ chọn): Nhãn cho screen reader khi icon mang ý nghĩa chức năng độc lập.

---

## 2. Dải số liệu (`components/metric_ribbon.html`)
Áp dụng thẻ `layout|fused-metric-ribbon-dock`: dải số liệu liền khối trên một surface chung, ngăn cách bằng đường kẻ dọc, không dùng các card KPI rời rạc hay icon bong bóng tròn.

### Cú pháp
```django
{% include "components/metric_ribbon.html" with items=kpi_metrics %}
```

### Cấu trúc dữ liệu `items`
```python
kpi_metrics = [
    {"label": "Tổng sinh viên", "value": "100 SV"},
    {"label": "Tỉ lệ đã xếp", "value": "43%", "secondary": "30% đạt NV1"},
    {"label": "Điểm trung bình", "value": "63.8", "secondary": "Toàn đợt"},
    {"label": "Chưa xếp", "value": "57 SV", "secondary": "Cần xếp bổ sung"},
]
```

---

## 3. Vỏ bọc bảng dữ liệu (`components/data_table.html`)
Cung cấp khung vỏ chuẩn Mosaic cho bảng dữ liệu: header sticky 40px, row hover nhẹ, căn lề số sang phải, hỗ trợ responsive.

### Cú pháp
```django
{% include "components/data_table.html" with title="Danh sách sinh viên" columns=table_cols rows=table_rows empty_text="Chưa có sinh viên đăng ký" %}
```

### Cấu trúc dữ liệu
- `columns`: Danh sách dict gồm `label` (tiêu đề cột), `align` (`left`, `center`, `right`).
- `rows`: Danh sách các mảng dữ liệu tương ứng theo từng hàng.

---

## 4. Nhãn trạng thái (`components/status_badge.html`)
Pill compact 24px, bo góc pill, bắt buộc đi kèm icon Lucide và nhãn chữ (không chỉ dùng màu đơn thuần).

### Cú pháp
```django
{% include "components/status_badge.html" with status="open" label="Đang mở" %}
{% include "components/status_badge.html" with status="assigned" label="Đã phân công" %}
{% include "components/status_badge.html" with status="rejected" label="Từ chối" %}
{% include "components/status_badge.html" with status="published" label="Chính thức" %}
```

### Ánh xạ trạng thái
- `draft` → Neutral (biểu tượng `circle-dot`)
- `open` → Info (biểu tượng `sparkles`)
- `pending` → Warning (biểu tượng `info`)
- `assigned` → Success (biểu tượng `badge-check`)
- `rejected` → Danger (biểu tượng `user-x`)
- `published` → Accent Teal (biểu tượng `circle-check-big`)

---

## 5. Nút bấm (`components/button.html`)
Hỗ trợ các biến thể thiết kế theo spec: `primary`, `secondary`, `ghost`, `danger`. Có hiệu ứng xúc giác nhẹ khi click (`motion|perceptual-spring-css-linear-easing`).

### Cú pháp
```django
{# Nút chính #}
{% include "components/button.html" with variant="primary" label="Lưu thay đổi" icon_name="save" type="submit" %}

{# Nút liên kết phụ #}
{% include "components/button.html" with variant="secondary" label="Quay lại" href="/danh-sach/" icon_name="arrow-left" %}

{# Nút thao tác nguy hiểm #}
{% include "components/button.html" with variant="danger" label="Từ chối yêu cầu" icon_name="user-x" %}
```

---

## 6. Hộp thoại xác nhận (`components/confirm_modal.html`)
Hỗ trợ xác nhận 2 bước và biến thể Từ chối bắt buộc nhập lý do theo quyết định nghiệp vụ đã chốt.

### Biến thể 1: GV từ chối sinh viên đăng ký (Bắt buộc nhập lý do)
```django
{% include "components/confirm_modal.html" with modal_id="rejectStudentModal_12" variant="reject" title="Từ chối yêu cầu đăng ký" student_name="Nguyễn Văn A (SV001)" topic_title="Hệ thống gợi ý đề tài tốt nghiệp" action_url="/giang-vien/tu-choi/12/" %}
```
*Đặc tính bắt buộc:* Textarea có `name="reason"`, thuộc tính `required`, `minlength="5"`. Nút xác nhận bị vô hiệu hoá (disabled) cho tới khi người dùng nhập đủ tối thiểu 5 ký tự hợp lệ.

### Biến thể 2: Xác nhận 2 bước hoàn tất phân công
```django
{% include "components/confirm_modal.html" with modal_id="finalizeModal" variant="two_step" title="Chốt kết quả phân công" summary_info="43 đã xếp · 57 chưa xếp" step2_url="/khoa/cong-bo/" %}
```

---

## 7. Khối điểm AI (`components/score_block.html`)
Hiển thị điểm tổng (Sora 700) và dải mini-strip 5 mô hình M1–M5 (Kỹ năng, Học lực, Lĩnh vực, Ngữ nghĩa, LLM). Kèm thanh tiến độ và nút mở rộng chi tiết.

### Cú pháp
```django
{% include "components/score_block.html" with total_score=82 m1=85 m2=78 m3=90 m4=80 m5=75 score_id=topic.id details="Chi tiết phân tích độ phù hợp từ hệ thống..." %}
```
*Lưu ý:* Nếu `m5` để trống/None, hệ thống tự động ghi nhận chú thích `"Điểm LLM tạm thời chưa có"`.

---

## 8. Khối lý do gợi ý (`components/reason_block.html`)
Hiển thị tối đa 4 dòng giải thích vì sao đề tài phù hợp, mỗi dòng có dấu tích check xanh của Lucide.

### Cú pháp
```django
{% include "components/reason_block.html" with title="Vì sao đề tài này phù hợp?" reasons=reasons_list %}
```
Hoặc truyền các lý do trực tiếp:
```django
{% include "components/reason_block.html" with reason_1="Kỹ năng Java và SQL đáp ứng 4/5 yêu cầu." reason_2="Lĩnh vực AI ứng dụng trùng với mức quan tâm 3/3." %}
```

---

## 9. Minh hoạ trạng thái rỗng (`components/empty_state.html`)
Sử dụng bộ file SVG độc quyền trong `static/mosaic/illus/`.

### Cú pháp
```django
{% include "components/empty_state.html" with illustration="empty-topics" title="Chưa có đề tài nào" description="Hiện tại chưa có đề tài nào được phê duyệt cho đợt đăng ký này." primary_url="/de-tai/them/" primary_label="Tạo đề tài mới" %}
```

### Các mã minh hoạ khả dụng:
- `empty-recommendation`: Chưa có gợi ý AI
- `empty-topics`: Chưa có đề tài
- `empty-preferences`: Chưa có nguyện vọng
- `empty-registrations`: Chưa có sinh viên đăng ký
- `empty-result`: Chưa có kết quả phân công
- `empty-search`: Không tìm thấy kết quả tìm kiếm/lọc
- `empty-excel`: Chưa tải lên tệp Excel
- `excel-error`: Tệp Excel phát hiện lỗi dữ liệu
- `profile-incomplete`: Hồ sơ sinh viên chưa hoàn thành
- `error-403`: Không có quyền truy cập
- `error-404`: Trang không tồn tại
- `error-500`: Hệ thống gặp sự cố

---

## 10. Thông báo Alert & Toast (`components/alert.html`, `components/toast.html`)

### Alert nội dòng
```django
{% include "components/alert.html" with type="warning" title="Hạn chót sắp tới" message="Đợt đăng ký nguyện vọng sẽ kết thúc vào 23:59 ngày mai." dismissible=True %}
```

### Toast nổi góc màn hình
```django
{% include "components/toast.html" with type="success" title="Đã lưu thành công" message="Nguyện vọng của bạn đã được cập nhật." %}
```
