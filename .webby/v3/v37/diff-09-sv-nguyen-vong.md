KHÁC BIỆT

1. [Bố cục tổng thể] hiện tại: ba khối Đợt đăng ký, thông báo đã nộp, NV1 xếp dọc; cột Gợi ý AI bắt đầu ngang NV1 nhưng nội dung chính quá cao, chỉ nhìn thấy NV1 và phần đầu NV2 → phải thành: hàng thông tin đợt đăng ký nằm ngang với thông báo trạng thái; bên dưới là hai cột độc lập, NV1–NV3 bên trái và Gợi ý AI bên phải; cả ba nguyện vọng phải nhìn thấy trong vùng 900px khi nội dung ngắn như ảnh duyệt | thông số: grid 12 cột, trái 8/12, phải 4/12; gap 12px; padding trang 16px; gap panel dọc 12px; không tạo thêm hàng toàn chiều rộng cho banner trạng thái.

2. [Thanh trạng thái đã nộp] hiện tại: banner xanh “Đã nộp chính thức lúc…” chiếm một hàng riêng dưới Period → phải thành: thông báo trạng thái nằm bên phải bên trong cùng thẻ Đợt đăng ký, giữ nút “Rút về nháp để sửa” vì có chức năng thật | thông số: .at-period grid 52%/48%; divider 1px #DDE4EF; bên trái thông tin đợt, bên phải banner có icon trạng thái, tiêu đề, mô tả và nút; toàn thẻ min-height 88px, tự tăng chiều cao khi nội dung dài.

3. [Trạng thái banner] hiện tại: nền xanh nhạt phủ toàn chiều rộng và nút hành động ở mép phải → phải thành: chỉ phần trạng thái bên phải có nền phụ hoặc nền trắng, icon xanh/cảnh báo cạnh tiêu đề, nút rút nháp nằm trong vùng đó | thông số: padding 12px 16px; title 13px/600; mô tả 12px/19px; nút cao 32px, font 12px/600; màu xanh thành công #176B60; border-radius 4px.

4. [Page Header] hiện tại: tiêu đề “Nguyện vọng đăng ký đề tài”, bên dưới chỉ có câu mô tả và nút “Danh sách đề tài” bên phải → phải thành: giữ tiêu đề, thêm dòng MSSV, Ngành, GPA như ảnh duyệt, sau đó mới tới mô tả; bỏ nút “Danh sách đề tài” khỏi header nếu đã có menu Đề tài, trừ khi chủ xác nhận đây là shortcut thực sự cần thiết | thông số: H1 24px/700, line-height 32px; metadata 12px/19px; mô tả 12px/19px; khoảng cách các dòng 3–4px; tổng header khoảng 66–72px.

5. [Breadcrumb] hiện tại: dòng “Trang chủ › Nguyện vọng” chiếm một hàng phía trên tiêu đề → phải thành: ưu tiên header gọn như ảnh duyệt, không để breadcrumb làm giảm diện tích các nguyện vọng | thông số: nếu giữ do shell chung, breadcrumb cao tối đa 20px, margin-bottom 4px; không thêm padding hoặc margin-top riêng cho trang.

6. [Thứ tự nội dung] hiện tại: đợt đăng ký → banner đã nộp → NV1 → NV2 → NV3, Gợi ý AI chạy song song nhưng căn thấp → phải thành: Header → Period tích hợp trạng thái → hai cột song song: bên trái NV1 → NV2 → NV3 → thanh lưu; bên phải Gợi ý AI → Lưu ý khi nộp | thông số: grid 8:4, align-items:start; cột phải không bị đẩy xuống theo chiều cao của banner.

7. [Panel NV1] hiện tại: header, select, thẻ đề tài, điểm, checklist và lời giải thích xếp nhiều tầng khiến NV1 cao quá mức → phải thành: panel NV1 compact, phần chọn đề tài và điểm nằm cùng khu vực bên trái, checklist bên phải, lời giải thích ngắn ở cuối phần trái | thông số: panel min-height 174px; header 38–42px; body padding 10px 12px; chia nội dung 58%/42%, gap 12px.

8. [Panel NV2–NV3] hiện tại: NV2 bắt đầu gần cuối viewport, NV3 nằm ngoài màn hình → phải thành: ba panel có cấu trúc và mật độ giống nhau, không để NV2/NV3 cao hơn không cần thiết | thông số: mỗi panel mục tiêu 150–174px khi dữ liệu ngắn; gap 10–12px; không dùng min-height 260–300px.

9. [Header từng nguyện vọng] hiện tại: chip NV1 dạng viền xám, tiêu đề “Nguyện vọng 1 (NV1)”, dòng phụ “Ưu tiên cao nhất trong xét duyệt” và nút xóa ở xa → phải thành: số thứ tự trong ô xanh đặc bên trái, tiêu đề trực tiếp bên cạnh, trạng thái ở phải, icon xóa cuối header | thông số: chip thứ tự 24×24px, background #176BFF, chữ trắng 12px/700; title 13px/600; badge cao 22px; icon trash-2 16px; header padding 8px 12px.

10. [Trạng thái nguyện vọng] hiện tại: NV1 “Chờ duyệt”, NV2 “Từ chối” thể hiện trực tiếp trên header → phải thành: giữ nguyên trạng thái nghiệp vụ thật, nhưng bố cục badge nhỏ như ảnh duyệt; nếu đã nộp thì phân biệt trạng thái nộp và kết quả GV duyệt | thông số: badge 11px/600, height 22px; trạng thái Chờ duyệt dùng cam nhạt, Từ chối dùng đỏ nhạt, Đã lưu/Đã nộp dùng xanh nhạt; không đổi kết quả backend để giống dữ liệu tham chiếu.

11. [Select đề tài] hiện tại: select nằm toàn chiều rộng khối NV, nhãn trên một dòng riêng và nhiều padding → phải thành: select gọn nằm trong cột trái, cùng hàng với nhãn “Chọn đề tài” nếu đủ chỗ | thông số: label 12px/500; select cao 32–34px, font 12px; gap 8px; không tự mở dropdown hoặc dùng custom select nếu Bootstrap hiện tại đã đáp ứng.

12. [Thông tin đề tài đã chọn] hiện tại: thẻ lớn với nhiều vùng nền xanh, tên đề tài, GVHD, điểm và mô tả → phải thành: một dải thông tin phẳng, tên đề tài + GVHD bên trái, điểm AI bên phải, không thêm card lồng card | thông số: min-height 56px; padding 8px 10px; border 1px #DDE4EF; background #F8FBFF; radius 4px; tên 12px/600, GVHD 11px/17px.

13. [Điểm phù hợp AI] hiện tại: điểm 23,3/100 hoặc điểm sơ bộ M1–M4 đặt dưới tên đề tài, làm thẻ cao → phải thành: điểm nằm bên phải trong cùng dải đề tài như ảnh duyệt | thông số: vùng điểm rộng 102px; điểm 20px/700, màu #176B60; hậu tố /100 12px; chú thích “Điểm phù hợp (AI)” hoặc “Điểm sơ bộ M1–M4” 10–11px/15px.

14. [Nhận xét AI] hiện tại: lời giải thích nằm trong hộp nền xanh cao, có icon và nhiều dòng → phải thành: ghi chú ngắn một dòng dưới dải đề tài, có icon info, không chiếm phần lớn chiều cao panel | thông số: font 11px/17px; background #F0F5FC; padding 6px 8px; margin-top 6px; border-radius 3px; hiển thị tối đa 2 dòng ở trang NV, nội dung đầy đủ ở trang chi tiết.

15. [Kiểm tra điều kiện] hiện tại: chỉ có hai mục “GPA tối thiểu” và “Chỉ tiêu”, thiếu các mục đánh giá còn lại hoặc bị lược bớt → phải thành: checklist bên phải gồm GPA, kỹ năng phù hợp/bắt buộc, lĩnh vực quan tâm, chỉ tiêu còn chỗ, theo điều kiện backend thực tế | thông số: 4 hàng, min-height 24px/hàng; label 11px/17px; icon circle-check 14px; gap dọc 2px; kết quả căn phải.

16. [Bố cục checklist] hiện tại: checklist nằm dưới thông tin đề tài trong cùng chiều rộng nên gây kéo dài panel → phải thành: checklist là cột phải của mỗi panel NV như ảnh duyệt | thông số: nội dung panel grid 58%/42%, gap 12px; divider dọc 1px nếu cần, padding trái cột điều kiện 10px.

17. [Nội dung kiểm tra GPA] hiện tại: “GPA tối thiểu: Đạt (3,08)” → phải thành: có mức yêu cầu và giá trị hiện có để người dùng kiểm chứng | thông số: “GPA đạt yêu cầu (≥2,5)” và “Đạt (3,08)” hoặc cách viết tương đương từ backend; label 11px, giá trị 11px/600; không hardcode ngưỡng 2,5.

18. [Kỹ năng và lĩnh vực] hiện tại: không hiện đủ lý do đủ/chưa đủ điều kiện trong NV đang xem → phải thành: mỗi tiêu chí có kết quả “Phù hợp”, “Thiếu kỹ năng…” hoặc “Chưa đạt” cụ thể | thông số: một hàng 24px, nội dung dài cho xuống tối đa 2 dòng; trường hợp cần giải thích sâu có liên kết Chi tiết đề tài thật.

19. [Chỉ tiêu đề tài] hiện tại: chỉ ghi “Còn 1 chỗ” trong checklist nhỏ → phải thành: thông tin tương tự ảnh “Còn 3/5”, nếu backend cung cấp capacity và số đã sử dụng | thông số: label 11px, số liệu 11px/600; không dùng số còn chỗ ước lượng.

20. [Panel Gợi ý AI] hiện tại: chỉ hiển thị một đề tài nổi bật trong viewport, có thẻ lớn, điểm và ghi chú dài → phải thành: danh sách Top 5 gợi ý compact theo ảnh duyệt, mỗi đề tài một hàng, xếp thứ hạng #1–#5 | thông số: panel cột phải rộng 4/12, header 42px; mỗi item min-height 62–66px; gap 0; divider giữa các item 1px #DDE4EF.

21. [Cấu trúc từng gợi ý] hiện tại: số thứ tự dạng ô viền, tên, GVHD, tag, điểm, lời giải thích chiếm khoảng 200px → phải thành: số thứ tự nhỏ bên trái, tên đề tài và GVHD ở giữa, điểm bên phải, tối đa hai chip lĩnh vực phía dưới tên | thông số: grid 28px minmax(0,1fr) 56px; gap 8px; tên 12px/600, GVHD 10–11px, điểm 16px/700.

22. [Độ phủ Top 5] hiện tại: nội dung gợi ý chưa hiển thị đủ Top 5 trong màn đầu vì card quá cao → phải thành: Top 5 hiển thị thành năm hàng với tổng chiều cao khoảng 330–360px | thông số: 5×64px + header 42px; panel cao khoảng 362px; nếu chỉ có K đề tài hợp lệ, hiển thị đúng K, không sinh thêm hàng giả.

23. [Nút xem thêm] hiện tại: “Xem thêm đề tài” nằm dưới mô tả panel và chiếm dòng riêng → phải thành: nút/link “Xem thêm đề tài” nằm phía phải header Gợi ý AI như ảnh duyệt | thông số: font 11px/600; icon arrow-right 14px; height 28px; không chiếm thêm hàng.

24. [Lưu ý khi nộp] hiện tại: chưa thấy panel riêng dưới Top 5 do Gợi ý AI quá dài → phải thành: panel “Lưu ý khi nộp” nằm ngay dưới Gợi ý AI, gồm ba ý ngắn, có số thứ tự và icon info | thông số: header 42px; body padding 12px 16px; ba hàng min-height 30px; font 11px/18px; tổng cao khoảng 130–150px.

25. [Nội dung lưu ý] hiện tại: banner xác nhận nộp chứa giải thích, nhưng không có đủ phần lưu ý như ảnh → phải thành: thể hiện các quy tắc thực tế: không chọn trùng đề tài, thứ tự NV ảnh hưởng ưu tiên, chỉnh sửa/nộp theo quy định đợt | thông số: mỗi ý 1–2 dòng; số thứ tự 18px tròn; không ghi “không thể sửa sau nộp” nếu hệ thống có chức năng rút về nháp.

26. [Thanh lưu đáy trang] hiện tại: không thấy trong viewport vì khối NV quá cao → phải thành: thanh hành động nằm cuối vùng nội dung bên trái và luôn truy cập được khi chỉnh sửa | thông số: desktop sticky bottom 0; height 52–56px; background #FFFFFF; border-top 1px #DDE4EF; padding 8px 12px; z-index 20.

27. [Nội dung thanh lưu] hiện tại: không hiển thị “Đã cập nhật lúc…” như ảnh duyệt → phải thành: phía trái là thời gian cập nhật/lưu thật, bên phải là các thao tác hợp lệ theo trạng thái | thông số: timestamp 11px/18px; icon info 14px; nút cao 34px; gap 8px; không tự tạo thời gian nếu backend không lưu.

28. [Nút Lưu nháp / Nộp nguyện vọng] hiện tại: trang đã nộp nên nút không xuất hiện, thay bằng “Rút về nháp để sửa” → phải thành: giữ đúng nghiệp vụ: khi đã nộp, không hiển thị Lưu nháp/Nộp lại; chỉ cho rút về nháp qua chức năng thật. Sau khi rút thành công mới hiện các nút Lưu nháp/Nộp theo backend | thông số: secondary “Lưu nháp” cao 34px; primary “Nộp nguyện vọng” cao 34px; khoảng cách 8px.

29. [Màu panel và độ tương phản] hiện tại: NV có nhiều nền xám/xanh nhạt lồng nhau, nhìn như các card nhỏ trong card lớn → phải thành: panel trắng phẳng, chỉ phần dải đề tài và ghi chú AI có nền xanh rất nhạt, đúng tinh thần ảnh duyệt | thông số: panel #FFFFFF; header #EAF4FF; border #DDE4EF; surface phụ #F8FBFF; radius 5–6px; không đổ bóng màu.

30. [Màu số thứ tự NV] hiện tại: NV chip viền xám, chưa đủ nổi bật → phải thành: chip xanh đặc, chữ trắng và số thứ tự rõ | thông số: #176BFF; chữ #FFFFFF; kích thước 24×24px, radius 4px.

31. [Màu điểm AI] hiện tại: điểm xanh lục đậm nhưng nhỏ và phân tán → phải thành: dùng một màu #176B60 cho toàn bộ điểm AI; kích thước 20px trong NV và 16px trong list Top 5 | thông số: font-weight 700; tabular-nums; không dùng xanh CTA #2454B8 cho điểm.

32. [Mật độ chữ] hiện tại: nhiều dòng chú thích 10–12px khiến khu vực NV có chữ nhỏ nhưng vẫn rất cao → phải thành: tinh giản số dòng, giữ thông tin quan trọng, không giảm chữ quá nhỏ để ép vừa | thông số: tiêu đề panel 13px/600; body 12px/19px; caption 11px/17px; font Be Vietnam Pro; các giá trị số 13–20px tùy vai trò.

33. [Đường viền và khoảng cách] hiện tại: khối NV, gợi ý và banner có padding lớn, khoảng cách giữa các lớp khác nhau → phải thành: cùng hệ spacing compact như ảnh duyệt | thông số: panel gap 10–12px; body padding 10px 12px; divider #DDE4EF; radius 5px; tránh margin-top 20–24px bên trong mỗi NV.

34. [Vùng trống và độ cân đối] hiện tại: bên phải có nhiều vùng trắng dưới card gợi ý, bên trái kéo dài quá mức → phải thành: bên phải có Top 5 + Lưu ý khi nộp, tạo chiều cao cân đối với ba panel nguyện vọng ở trái | thông số: Top 5 khoảng 360px, Lưu ý 140px; cột NV gồm 3×160–174px + gap 12px; cả hai cột căn từ cùng một hàng.

35. [Dữ liệu khác ảnh] hiện tại: điểm 23,3, trạng thái chính thức, tên và thời gian khác dữ liệu mẫu → phải thành: giữ nguyên dữ liệu demo thật, không ép thành 79,6 hay trạng thái Đã lưu; chỉ điều chỉnh cách hiển thị và thông tin đầy đủ | thông số: số liệu và status lấy từ backend; giá trị null M4/M5 hiển thị “Chưa đánh giá”, điểm tổng ghi rõ sơ bộ M1–M4 khi phù hợp.

36. [Shell] hiện tại: topbar và menu trái khác đôi chút về kích thước so với ảnh duyệt → phải thành: giữ shell V3.6 đã được chủ chấp nhận; chỉ đồng bộ logo chữ M, không có phụ đề Open Path và không có chuông | thông số: không thay width sidebar, topbar height hoặc breakpoint chỉ để khớp ảnh này.

ASSET THÀNH PHẦN CÒN THIẾU

1. Lucide circle-check — Checklist điều kiện GPA, kỹ năng, lĩnh vực, chỉ tiêu. Icon 14–16px, màu #176B60, dùng cho điều kiện đạt.

2. Lucide triangle-alert — Cảnh báo chưa nộp, thiếu điều kiện, hoặc cần lưu ý. Icon 16px, màu #C47B11.

3. Lucide info — Ghi chú giải thích mức phù hợp và panel “Lưu ý khi nộp”. Icon 14–16px, màu #2454B8.

4. Lucide trash-2 — Xóa lựa chọn NV, icon 16px; nút 32×32px desktop, 44×44px mobile.

5. Lucide send — Nút “Nộp nguyện vọng” trong trạng thái có thể nộp; icon 16px.

6. Lucide save — Nút “Lưu nháp” nếu nút này có chức năng backend độc lập; icon 16px.

7. Lucide arrow-right — Liên kết “Xem thêm đề tài”, icon 14px.

8. Lucide refresh-cw — Nút “Rút về nháp để sửa” có chức năng thật; icon 14–16px.

9. Rank chip #1–#5 và NV1–NV3 — Không cần SVG riêng; tạo bằng HTML/CSS, có nền, viền và màu đúng trạng thái.

10. Không có minh họa đặc biệt cần render thêm. Khác biệt chủ yếu là bố cục component, spacing, mật độ danh sách và trạng thái form.

TRẠNG THÁI / HÀNH VI

1. Đã nộp chính thức: Banner thông báo và nút “Rút về nháp để sửa” nằm trong phần phải của .at-period, không tạo hàng toàn chiều rộng. Phải phản ánh timestamp và trạng thái thật nếu backend cung cấp.

2. Rút về nháp: Nhấn nút mở xác nhận theo nghiệp vụ, sau đó POST với CSRF; chỉ cập nhật giao diện sau khi server xác nhận. Không tự chuyển trạng thái khi request thất bại.

3. Sau khi rút nháp: Cho phép thay đổi NV1–NV3, xóa/chọn đề tài, lưu nháp và nộp lại theo quyền và thời hạn. Không mất dữ liệu NV đã lưu.

4. Chọn đề tài: Ba select lấy danh mục thật, không cho trùng đề tài. Khi đổi lựa chọn, cập nhật điểm AI, GVHD, điều kiện và lý do theo đúng cặp SV–đề tài; không giữ dữ liệu của đề tài cũ.

5. Kiểm tra điều kiện: GPA, kỹ năng bắt buộc, học phần tiên quyết nếu có và chỉ tiêu phải được backend kiểm tra. Không cho nộp đề tài thiếu điều kiện bắt buộc, trừ trường hợp quy tắc nghiệp vụ cho phép và có giải thích rõ.

6. Top 5 AI: Danh sách lấy kết quả recommendation hiện tại, sắp xếp theo điểm. Hiển thị đúng số kết quả, không lặp đề tài đã chọn thành bản sao giả, không tự tạo điểm M5 khi chưa có.

7. Trạng thái AI sơ bộ: Nếu chưa có M5, hiện “Điểm sơ bộ M1–M4”; M4 hoặc M5 chưa đánh giá hiển thị thiếu dữ liệu đúng thực tế, không quy về 0. Sau khi hoàn tất đánh giá mới dùng nhãn điểm đầy đủ.

8. Lưu nháp: Nút chỉ bật khi form thay đổi hợp lệ; POST một lần, chống bấm lặp, cập nhật timestamp lưu và trạng thái theo phản hồi server.

9. Nộp nguyện vọng: Kiểm tra các NV được chọn, thứ tự, tính duy nhất và điều kiện hợp lệ; xác nhận trước POST nếu luồng backend có bước xác nhận. Không báo “Đã nộp” trước khi server trả thành công.

10. Đợt đóng/công bố: Trang chuyển chế độ chỉ xem, vẫn hiển thị ba NV và Top 5 lịch sử khi dữ liệu có sẵn; không xuất hiện ngõ cụt “Chưa có đợt nào”. Nút rút nháp, xóa, lưu và nộp phải tuân thủ quyền và trạng thái.

11. Thanh lưu: Khi chỉnh sửa, save bar sticky cuối vùng nội dung; không che NV3 hoặc phần lưu ý. Khi đã nộp, thay hành động bằng trạng thái lưu/nộp phù hợp, không đưa nút vô hiệu trang trí.

12. Mobile dưới 768px: Thứ tự Header → Period tích hợp banner → NV1 → NV2 → NV3 → Gợi ý AI Top 5 → Lưu ý → Action Bar. Ba panel NV chuyển một cột; checklist dọc; action bar 72px + safe area thay Bottom Navigation khi có thao tác chỉnh sửa.

13. Accessibility: Input/select có label, nút xóa có tên truy cập, trạng thái không chỉ phân biệt bằng màu, focus ≥2px; touch target mobile ≥44px.

14. QA: Tại 1440×900 phải kiểm tra cả ba NV hiển thị khi dữ liệu ngắn, Top 5 compact, banner nằm cạnh Period, không tràn ngang; kiểm tra thêm 390px, Light/Dark, tình huống draft/submitted/closed/published và lỗi validation.