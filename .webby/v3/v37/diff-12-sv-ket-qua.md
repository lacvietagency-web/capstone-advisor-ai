KHÁC BIỆT

1. [Bố cục tổng thể] hiện tại: trang chỉ có Period → Kết quả chính thức → Nguyện vọng đã nộp; khối kết quả chiếm chiều cao lớn, danh sách nguyện vọng bị đẩy xuống dưới viewport → phải thành: Header → Period → Hành trình đăng ký 4 bước → Kết quả phân công chính thức → Nguyện vọng đã nộp → Hành động cuối trang | thông số: grid 12 cột; tất cả khối rộng 12/12; gap dọc 10–12px; padding canvas 16px; panel nền #FFFFFF, viền #DDE4EF, radius 6px.

2. [Hành trình đăng ký — THIẾU] hiện tại: hoàn toàn không có thanh tiến trình 4 bước → phải thành: bổ sung panel “Hành trình đăng ký đề tài” nằm ngay sau Period, thể hiện đủ bốn bước đã hoàn thành | thông số: panel min-height 116px; header 36px; body padding 10px 14px; bốn bước chia đều 25%; vòng tròn hoàn thành 30×30px, nền #176BFF; đường nối 2px; gap 8px.

3. [Nội dung hành trình] hiện tại: người dùng không thấy tiến độ từ hồ sơ đến kết quả → phải thành: bốn bước đúng ảnh duyệt: “1. Hồ sơ năng lực”, “2. Gợi ý AI”, “3. Nguyện vọng”, “4. Kết quả phân công”; trạng thái lần lượt hoàn thành/hoàn thành/đã nộp/đã công bố | thông số: tiêu đề bước 12px/600, badge 10–11px/600, mô tả 10–11px/17px; mỗi bước có tối đa hai dòng mô tả; không thêm bước thứ năm.

4. [Page Header] hiện tại: tiêu đề “Kết quả phân công đề tài”, metadata bên dưới và một dòng mô tả dài → phải thành: tiêu đề cùng metadata như ảnh duyệt, loại bỏ mô tả phụ không cần thiết để tăng mật độ hiển thị | thông số: H1 24px/700, line-height 32px; metadata 12px/19px; khoảng cách 4px; header min-height khoảng 62px.

5. [Breadcrumb] hiện tại: “Trang chủ › Kết quả phân công” chiếm một dòng riêng trên H1 → phải thành: bố cục gọn; breadcrumb nếu thuộc shell chung vẫn giữ nhưng không tạo khoảng cách lớn trước tiêu đề | thông số: font 11px/18px, margin-bottom 4px; không thêm margin-top riêng.

6. [Period] hiện tại: dải trạng thái thấp, gồm tên đợt, ngày và câu mô tả trên cùng một hàng → phải thành: dải thông tin có chiều cao rõ, trái là tên/trạng thái/thời gian, phải là thông báo kết quả đã công bố | thông số: min-height 70px; grid 55%/45%; divider dọc 1px #DDE4EF; padding 10px 14px; label 12px/600; status 11px/600.

7. [Thông báo Period] hiện tại: câu “Kết quả phân công chính thức đã được công bố cho sinh viên” nằm nối tiếp sau ngày → phải thành: tách sang vùng phải như ảnh duyệt | thông số: text 12px/19px, padding-left 16px; căn giữa theo chiều dọc.

8. [Vị trí panel Kết quả] hiện tại: panel kết quả xuất hiện ngay sau Period → phải thành: đặt dưới Journey, chiếm 12 cột; không thay bằng nhiều KPI card nhỏ | thông số: margin-top theo section gap 10–12px; header panel 38–42px; body padding 12–14px.

9. [Header Kết quả chính thức] hiện tại: có tiêu đề, dòng mô tả phụ “Đợt đăng ký…”, ba badge “Đạt NV1”, “Chính thức”, “Tối ưu ILP” ở mép phải → phải thành: header chỉ có tiêu đề “Kết quả phân công chính thức”; badge chuyển xuống hàng nội dung đề tài, như ảnh duyệt | thông số: header 38–42px; title 14px/600; vạch accent 4×20px, màu #176BFF.

10. [Tên đề tài được phân công] hiện tại: “Kho dữ liệu và báo cáo điểm danh” hiển thị như một tiêu đề nhỏ trong vùng thông tin nhãn–giá trị → phải thành: tên đề tài nổi bật ở đầu panel, cùng hàng với các badge trạng thái | thông số: tên 16px/700, line-height 24px; badge nhóm bên phải; gap 8px; tên được xuống tối đa 2 dòng ở desktop.

11. [Thông tin GVHD] hiện tại: GVHD, NV đạt, lĩnh vực và mô tả được trình bày theo nhiều dòng dạng biểu mẫu → phải thành: GVHD là dòng phụ ngay dưới tên đề tài, giống ảnh duyệt; lĩnh vực và mô tả chi tiết để trong trang Chi tiết đề tài | thông số: GVHD 12px/19px, màu #344563; margin-top 3px; không thêm panel con.

12. [Badge trạng thái] hiện tại: ba badge nằm ở header panel, bao gồm nhãn “Tối ưu ILP” → phải thành: cụm badge ngay bên phải tên đề tài: “Đạt NV1”, “Chính thức”, “Phân công bằng ILP” theo dữ liệu backend | thông số: badge min-height 22px; padding 3px 8px; gap 6px; font 10–11px/600; background tương ứng xanh nhạt, xanh dương nhạt và trung tính.

13. [Bố cục thân kết quả] hiện tại: thông tin đề tài nằm ở trái, điểm 67,0 nằm ở phải, dưới điểm là banner thông báo xanh → phải thành: phần thân kết quả chia ba vùng ngang: Điểm AI lớn bên trái, M1–M5 ở giữa, Nhận xét và thông báo chính thức bên phải | thông số: grid 25% 30% 45%; gap 12px; body min-height khoảng 156px khi đủ dữ liệu.

14. [Điểm phù hợp AI] hiện tại: 67,0/100 ở góc phải, kích thước vừa và không có khung nhấn → phải thành: điểm nằm trong ô nhấn riêng bên trái như ảnh duyệt | thông số: vùng điểm khoảng 180px rộng; số 40px/700, màu #176B60; hậu tố /100 15px; caption 11px/17px; background #F8FBFF; border 1px #DDE4EF; radius 5px; padding 12px.

15. [Phân tích M1–M5 — THIẾU] hiện tại: trang không có năm thanh điểm thành phần, chỉ hiển thị tổng điểm 67,0 → phải thành: bổ sung khối Evidence M1–M5 ngay bên phải điểm tổng, lấy từ recommendation thực | thông số: năm hàng; mỗi hàng 21–22px; nhãn M1–M5 10–11px; thanh cao 7px; track #E5EAF1; fill #176B60; giá trị số 11px/600; gap ngang 8px.

16. [Tên mô hình AI] hiện tại: không có nhãn M1–M5 → phải thành: M1 Kỹ năng, M2 Học lực, M3 Lĩnh vực, M4 Ngữ nghĩa, M5 Đánh giá LLM | thông số: tên 10–11px/17px; không dùng lại tên “Mức phù hợp” cho M5.

17. [Trọng số AHP] hiện tại: không thấy thông tin trọng số → phải thành: ghi chú AHP phía dưới năm thanh theo ảnh duyệt | thông số: font 10px/16px; margin-top 6px; dùng trọng số phiên bản thực, không mặc định 25/20/15/20/20% nếu CSDL lưu khác.

18. [M4/M5 chưa đánh giá] hiện tại: chỉ có điểm tổng, không cho biết thành phần nào chưa có → phải thành: hiển thị “Chưa đánh giá” ở mô hình thiếu; giữ nhãn điểm sơ bộ nếu điểm tổng chưa đủ 5 mô hình | thông số: font 10–11px, màu #596579; không vẽ thanh 0 giả; không tạo số M4/M5 theo ảnh duyệt.

19. [Nhận xét phù hợp] hiện tại: không có khối “Nhận xét phù hợp”, thay bằng mô tả đề tài và thông báo chính thức → phải thành: vùng bên phải có tiêu đề “Nhận xét phù hợp”, bên dưới là lý do gợi ý thực tế hoặc giải thích phù hợp từ backend | thông số: heading 12px/600; body 11px/18px; min-height 48px; divider dưới 1px #DDE4EF.

20. [Thông báo chính thức] hiện tại: một banner màu xanh có tiêu đề “Thông báo chính thức”, chiếm chiều cao lớn trong vùng điểm bên phải → phải thành: thông báo gọn trong vùng phải của panel kết quả, nằm dưới Nhận xét phù hợp, có tiêu đề và thông điệp từ Khoa | thông số: heading 12px/600; text 11px/18px; padding 8px 0; nền trắng hoặc xanh rất nhạt, không có banner lớn lồng trong card.

21. [Nội dung thông báo] hiện tại: “Khoa đã công bố kết quả phân công chính thức. Sinh viên chủ động liên hệ GVHD qua email…” → phải thành: giữ nội dung hướng dẫn chính thức có thật, trình bày gọn giống ảnh duyệt, không tự tạo thời hạn hoặc nghĩa vụ mới | thông số: tối đa 3 dòng tại cột phải nếu nội dung ngắn; dài hơn tự xuống dòng, không cắt mất thông tin quan trọng.

22. [Thời điểm công bố] hiện tại: không hiển thị thời điểm công bố riêng trong panel → phải thành: hiển thị dòng “Công bố lúc…” khi backend có timestamp thực | thông số: icon calendar-days 13px; font 10px/17px; màu #596579; không tạo published_at giả khi CSDL không lưu.

23. [Mật độ phần kết quả] hiện tại: các nhóm thông tin cách nhau nhiều, panel cao hơn cần thiết → phải thành: kết quả trong một panel gọn, không tạo bảng thông tin dài phía trên điểm AI | thông số: panel mục tiêu 190–220px gồm header và nội dung nếu dữ liệu ngắn; padding 12px; gap 10px; không đặt min-height:300px cố định.

24. [Mô tả đề tài] hiện tại: nguyên đoạn mô tả “Xây dựng kho dữ liệu…” nằm trong panel kết quả → phải thành: không hiển thị mô tả dài trong kết quả; chỉ giữ tên, GVHD, NV đạt, điểm, lý do phù hợp và thông báo công bố; mô tả đầy đủ thuộc màn 11 | thông số: link “Xem chi tiết đề tài” dẫn tới route có thật, không cần tạo modal mới.

25. [Nguyện vọng đã nộp] hiện tại: danh sách NV1/NV2 hiển thị dưới dạng các card lớn, mỗi NV có tên và GVHD, NV3 bị đẩy ra ngoài viewport → phải thành: bảng/danh sách ba hàng compact giống ảnh duyệt, tất cả NV1–NV3 nằm trong cùng một panel | thông số: panel header 38–42px; mỗi hàng min-height 34–38px; divider 1px #DDE4EF; padding ngang 12px.

26. [Bố cục một hàng NV] hiện tại: chip NV, tên, GVHD và badge trạng thái nằm trong một card dày → phải thành: mỗi hàng gồm chip NV → tên đề tài → GVHD → trạng thái | thông số: grid 52px minmax(0,1.3fr) minmax(0,1fr) 100px; gap 10px; chip 36×22px; title 11–12px/600; GVHD 11px; status 10–11px/600.

27. [Trạng thái NV khác NV đạt] hiện tại: NV2 ghi “Không được phân công”, ảnh duyệt ghi “Không đạt” → phải thành: giữ cách diễn đạt đúng nghiệp vụ “Không được phân công”, không được biến thành “Không đủ điều kiện” hoặc “Bị từ chối” chỉ để giống ảnh | thông số: badge trung tính hoặc cảnh báo nhẹ, min-height 22px; trạng thái NV1 đạt dùng xanh lá; các NV khác dùng nhãn không được phân công nếu backend xác nhận.

28. [Panel NV] hiện tại: header có thêm dòng mô tả “Các nguyện vọng bạn đã đăng ký trong đợt này” → phải thành: chỉ giữ title “Nguyện vọng đã nộp” để giảm chiều cao, như ảnh duyệt | thông số: header 42px, không có subtitle; số lượng NV có thể hiển thị nhỏ bên phải nếu cần.

29. [Thanh hành động cuối] hiện tại: nút “Xem chi tiết đề tài” nằm trong footer panel Kết quả chính thức → phải thành: hai nút hành động ở cuối panel Nguyện vọng như ảnh duyệt | thông số: nút cao 34px, gap 8px; căn phải; primary “Xem chi tiết đề tài”; secondary “Tải biên bản” chỉ khi có endpoint tạo/tải thật.

30. [Nút Tải biên bản] hiện tại: không có nút này → phải thành: chỉ hiển thị khi hệ thống thực sự hỗ trợ xuất biên bản; nếu chưa có chức năng, không tạo nút giả | thông số khi có: icon download 14px; font 11px/600; height 34px.

31. [Khoảng trắng bên dưới] hiện tại: một phần lớn chiều cao bị tiêu tốn cho chi tiết kết quả, kéo danh sách NV xuống → phải thành: nén khối kết quả, Journey và NV để các nhóm thông tin chính hiện trong màn đầu 900px | thông số: Header khoảng 62px; Period 70px; Journey 116px; Result 200px; NV 170–190px; tổng gap khoảng 48px; không cắt dữ liệu thật nếu dài.

32. [Nền và viền panel] hiện tại: panel hơi xám, nhiều khu vực nền lồng nhau → phải thành: panel trắng, header xanh rất nhạt và vạch accent trái đúng ảnh duyệt | thông số: panel #FFFFFF; header #EAF4FF; accent #176BFF, 4×20px; border #DDE4EF; radius 5–6px; shadow tối thiểu.

33. [Kiểu chữ] hiện tại: trang dùng nhiều cỡ nhỏ khác nhau, điểm và trạng thái chưa có thứ bậc nổi bật → phải thành: ưu tiên tiêu đề trang, tên đề tài, điểm AI và kết quả NV | thông số: Be Vietnam Pro; H1 24px/700; tên đề tài 16px/700; panel heading 14px/600; body 12px/19px; caption 11px/17px; điểm 40px/700.

34. [Màu thành phần] hiện tại: điểm 67,0 và thông báo dùng xanh cùng tông, không tách rõ AI và hành động → phải thành: điểm/AI dùng xanh #176B60, CTA dùng xanh #2454B8, trạng thái đạt dùng xanh lá nhạt, trạng thái không đạt dùng trung tính/cảnh báo nhẹ | thông số: track thanh #E5EAF1; badge nền #E7F5EE hoặc #F1F4F8; không tô nguyên vùng lớn đỏ/vàng.

35. [Dữ liệu demo] hiện tại: sinh viên Nguyễn Thu Hùng, đề tài Kho dữ liệu và báo cáo điểm danh, điểm 67,0 khác ảnh duyệt → phải thành: giữ nguyên dữ liệu thật, không thay tên hoặc điểm thành 79,6 chỉ để giống ảnh | thông số: mọi trường lấy từ backend; kiểm tra bằng trường hợp SV có allocation PUBLISHED hợp lệ.

36. [Nguồn phân công] hiện tại: badge “Tối ưu ILP” hiển thị trong header → phải thành: hiển thị “Phân công bằng ILP” hoặc tên nguồn hợp lệ cạnh badge chính thức trong phần tên đề tài; nếu nguồn không có thì ẩn | thông số: badge 10–11px; không suy luận nguồn từ điểm số hoặc trạng thái.

37. [Shell] hiện tại: sidebar, topbar và avatar khác ảnh duyệt nhưng đã được chủ chấp nhận → phải thành: giữ shell V3.6; chỉ bảo đảm logo chữ M, không có “Open Path” và không có chuông | thông số: không thay sidebar width, topbar height hoặc menu chỉ để khớp ảnh này.

ASSET THÀNH PHẦN CÒN THIẾU

1. Lucide circle-check — Icon hoàn thành của Journey; 18px màu trắng trong vòng nền xanh 30×30px.

2. Lucide badge-check — Trạng thái kết quả chính thức; icon 14px, màu #2454B8.

3. Lucide graduation-cap — Nhóm nguyện vọng đạt hoặc thông tin học thuật khi cần; icon 14–16px.

4. Lucide git-compare — Nhãn nguồn phân công ILP/Greedy/Manual; icon 13–14px.

5. Lucide calendar-days — Thời điểm công bố nếu backend cung cấp; icon 13px.

6. Lucide arrow-right — Nút Xem chi tiết đề tài; icon 14px.

7. Lucide download — Nút Tải biên bản nếu có chức năng thực; icon 14px.

8. Lucide info — Ghi chú điểm sơ bộ và hướng dẫn kết quả; icon 14px.

9. Evidence bar M1–M5 — Không cần SVG riêng; dùng .at-evidence sẵn có với thanh ngang 7px, nhãn và số điểm.

10. Journey connector — Đường nối bốn bước dùng CSS, không cần asset riêng; nét liền 2px với các bước đã hoàn thành.

Không thiếu minh họa đặc biệt cần render mới. Khác biệt lớn nhất là thiếu Journey và khối phân tích điểm M1–M5, cùng cách tổ chức panel kết quả.

TRẠNG THÁI / HÀNH VI

1. Kết quả được phân công: Khi đợt PUBLISHED và SV có allocation chính thức, trang phải hiển thị đề tài, GVHD, NV đạt, điểm AI, nguồn phân công và thông báo chính thức theo dữ liệu thực.

2. Journey bốn bước: Trạng thái lấy từ hồ sơ, gợi ý, nguyện vọng và công bố. Khi có kết quả PUBLISHED, bước 4 phải là “Đã công bố”, không dừng ở bước 2 hoặc 3.

3. Điểm M1–M5: Lấy từ recommendation tương ứng với cặp SV–đề tài đã phân công, theo phiên bản lưu. Nếu chưa có đủ điểm, hiển thị thành phần thiếu “Chưa đánh giá”; không tạo lại điểm giả hoặc gán 0.

4. Điểm tổng: Dùng match_score/final_score đúng ý nghĩa dữ liệu hệ thống. Nếu điểm allocation và điểm recommendation khác nhau, phải ghi rõ nguồn hiển thị, không đánh đồng hai giá trị.

5. Đã công bố nhưng chưa được xếp: Thay panel kết quả bằng trạng thái “Chưa được phân công đề tài”, hiển thị lý do chính thức nếu backend có; vẫn giữ Journey và các NV đã nộp.

6. Chưa công bố: Không để SV xem dữ liệu DRAFT hoặc đề tài phân công nội bộ; hiện banner “Kết quả chưa được công bố”.

7. Nguyện vọng đã nộp: Luôn hiển thị lại NV1–NV3 nếu dữ liệu tồn tại, kể cả đợt đã đóng/công bố. Không báo “Chưa có đợt nào” khi vẫn có lịch sử.

8. Trạng thái NV: Đề tài được phân công xác định NV đạt; các NV còn lại ghi “Không được phân công” nếu phù hợp. Không tự chuyển thành “Từ chối” hoặc “Không đủ điều kiện”.

9. Xem chi tiết đề tài: Điều hướng đến đúng topic thuộc allocation chính thức; không dẫn sang NV khác hoặc đề tài không tồn tại.

10. Tải biên bản: Chỉ cho phép tải khi có chức năng thật và file/dữ liệu thuộc SV có quyền; nếu chưa có thì ẩn nút.

11. Công bố và trạng thái: Không hiển thị timestamp công bố nếu CSDL chưa lưu; không lấy ngày hiện tại thay ngày công bố. Không cho SV chỉnh sửa, hủy hoặc thay đổi allocation sau PUBLISHED.

12. Responsive dưới 768px: Thứ tự Header → Period → Journey → Kết quả → Điểm AI → M1–M5 → Nhận xét/Thông báo → Nguyện vọng → Hành động → Bottom Navigation. Nội dung một cột, không tràn ngang, các thanh M1–M5 xếp dọc.

13. Accessibility: Journey có text trạng thái, badge không chỉ dựa vào màu, Evidence bar có nhãn và số; CTA mobile touch target ≥44px, focus rõ, WCAG AA.

14. QA: Chụp và kiểm thử tối thiểu bốn trạng thái: chưa công bố, đã công bố–đã xếp, đã công bố–chưa xếp, thiếu điểm M4/M5. Nghiệm thu 1440×900 và 390px Light/Dark; không hardcode số, không lỗi template/JavaScript/CSRF/HTTP 500.