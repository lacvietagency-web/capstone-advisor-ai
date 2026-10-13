NHÓM sv-b — Sinh viên nhập liệu. Ảnh: renders/07-sv-nguyenvong-mobile.png.
1. templates/catalog/student_profile.html (canvas at-canvas--read) — context: student, about_form, skill_formset (prefix skills: skill, level 1–5, DELETE),
   interest_formset (prefix interests: field, level 1–3, DELETE). GIỮ NGUYÊN management_form, tên field, nút thêm dòng JS hiện có (viết lại JS gọn trong {% block extra_js %} nếu cần, không thư viện).
   Header (h1 "Hồ sơ năng lực", mô tả: AI dùng hồ sơ để tính M1–M5) → form data-at-busy: panel "Giới thiệu" (textarea + help) → panel "Kỹ năng" (mỗi dòng at-repeat-row:
   select kỹ năng, select mức có nhãn chữ "1 — Mới biết … 5 — Chuyên sâu", nút xoá btn-icon) + nút "Thêm kỹ năng" btn-secondary → panel "Lĩnh vực quan tâm" (tương tự, mức 1–3)
   → at-form-actions: Huỷ + "Lưu và tính lại gợi ý" (primary). Lỗi formset: non_form_errors bằng components/banner.html kind danger.
2. templates/catalog/student_preferences.html — context A (đợt mở): period, form (nv1, nv2, nv3: ModelChoiceField; chỉ đề tài đủ điều kiện), top5 (Recommendation), scores {topic_id: Recommendation}.
   Header (h1 "Nguyện vọng", period.html) → form data-at-busy: 3 khối NV1/NV2/NV3 (at-panel, mỗi khối: nhãn at-rank, select, nếu đã chọn hiện score sm từ scores) →
   panel "Gợi ý cho bạn" từ top5 (tên, score sm, nút "Chọn làm NV trống tiếp theo" dùng link ?topic=<id>) → at-form-actions "Lưu nguyện vọng".
   Trên điện thoại nút lưu nằm trong <div class="at-actionbar"> (thanh hành động thay thanh đáy).
   context B (không có đợt mở): period=None, last_period, submitted [{pref, rec}] → banner neutral "Đợt <last_period.name> đã đóng — nguyện vọng chỉ xem" →
   danh sách NV đã nộp (at-rank, tên đề tài, GVHD, status Preference (PENDING/ACCEPTED/REJECTED) + lý do từ chối nếu có (note kind danger), score sm);
   last_period=None → empty empty-preferences "Chưa có đợt đăng ký nào" + link Xem danh sách đề tài.
3. templates/catalog/_pref_actions.html — giữ chức năng hiện có, đổi sang class ATLAS.
PAGE sv001 /ho-so/ · PAGE sv001 /nguyen-vong/
