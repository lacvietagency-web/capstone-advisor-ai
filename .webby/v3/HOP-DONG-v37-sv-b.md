NHÓM sv-b — màn 08 Hồ sơ năng lực (templates/catalog/student_profile.html, .pg-08), 09 Nguyện vọng (templates/catalog/student_preferences.html
+ templates/catalog/_pref_actions.html, .pg-09); điện thoại m09. CSS: static/css/pages/sv-b.css.
Việc: làm hết .webby/v3/v37/diff-08-sv-ho-so.md và diff-09-sv-nguyen-vong.md. BỎ {% block canvas_class %}at-canvas--read{% endblock %} ở cả 2 trang
(trang phải rộng toàn vùng nội dung như ảnh duyệt).
Biến/luật mới (lõi đã có):
- student_profile: contact_form (email, phone — SV sửa được; name="email", name="phone"); Họ tên/MSSV/Ngành/GPA = ô readonly KHÔNG có name.
  interest_form: ô tick lĩnh vực — field picked (name="interest-picked", CheckboxSelectMultiple, tối đa 3; lỗi ở interest_form.picked.errors).
  BẮT BUỘC có <input type="hidden" name="interest-shown" value="1"> trong form (thiếu thì lĩnh vực không được lưu). interest_formset đã BỎ.
  skill_formset giữ nguyên (prefix skills). Thanh lưu dính đáy: chỉ nút "Lưu hồ sơ" (không có Lưu nháp hồ sơ). completeness / completeness_items như cũ.
- student_preferences: pref_rows[].checklist (4 mục GPA / kỹ năng / lĩnh vực / chỉ tiêu) cho khối "Kiểm tra điều kiện" mỗi NV; pref_rows[].rec, .remaining;
  top5 (Gợi ý AI, hàng gọn #1–#5); is_submitted, submitted_at. Banner "đã nộp / chưa nộp" + nút "Rút về nháp để sửa" đặt bên phải thẻ đợt:
  {% include "components/period.html" with period=period aside=<nội dung> %} không truyền được HTML → tự viết khối bên phải trong .pg-09
  (thẻ đợt bên trái + ô cảnh báo bên phải như ảnh). Giữ nguyên các nút POST action=draft|submit|withdraw và name="nv1|nv2|nv3".
