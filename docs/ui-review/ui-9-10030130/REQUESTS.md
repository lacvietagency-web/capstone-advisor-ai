# UI Review & Backend Feature Requests

Tài liệu ghi nhận các yêu cầu dữ liệu / tối ưu hóa từ Front-end gửi tới Backend theo quy định trong quy trình phát triển giao diện.

---

## 1. Màn hình `/de-tai/` (`catalog.views.lecturer_topics`)

- **Biến context cần thêm**: `total_registrations` (int)
  - **Mục đích**: Hiển thị tổng số lượt sinh viên đã đăng ký vào tất cả các đề tài của giảng viên trên thanh tóm tắt thông tin: `X đề tài · Y lượt đăng ký` theo đặc tả `docs/ui/DESIGN.md` (Mục 9.1).
  - **Hiện trạng**: Template đang dùng `{{ topics|length }} đề tài` và fallback nếu `total_registrations` chưa có trong context.
  - **Gợi ý backend**:
    ```python
    total_registrations = Preference.objects.filter(topic__lecturer=lec).count()
    return render(request, "catalog/lecturer_topics.html", {
        "lecturer": lec,
        "topics": topics,
        "total_registrations": total_registrations,
    })
    ```

- **Tối ưu truy vấn (N+1)**:
  - **Mục đích**: Trên mỗi thẻ đề tài có hiển thị `{{ t.preference_set.count }} sinh viên đăng ký`.
  - **Gợi ý backend**: Thêm `annotate(reg_count=Count('preference'))` vào queryset `topics` để tối ưu performance khi giảng viên có nhiều đề tài.

---

## 2. Màn hình `/de-tai/<id>/dang-ky/` (`catalog.views.lecturer_registrations`)

- **Tối ưu prefetch**:
  - **Mục đích**: Hiển thị tên chuyên ngành của sinh viên (`{{ row.pref.student.major.name }}`).
  - **Gợi ý backend**: Bổ sung `'student__major'` vào `select_related`:
    ```python
    prefs = (
        Preference.objects.filter(topic=topic)
        .select_related("student__user", "student__major", "period")
        .order_by("rank", "created_at")
    )
    ```
