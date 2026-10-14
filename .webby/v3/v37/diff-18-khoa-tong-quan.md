KHÁC BIỆT

1. [Metric Ledger — KHÁC BIỆT LỚN NHẤT] hiện tại: chỉ có 4 chỉ số “Sinh viên”, “Đề tài”, “Đợt đăng ký”, “Sinh viên có NV”, thiếu “Giảng viên” → phải thành: dải thống kê 5 chỉ số trên một hàng theo ảnh duyệt: Sinh viên, Đề tài, Đợt đăng ký, Sinh viên có NV, Giảng viên | thông số: mỗi chỉ số rộng 20%; ledger body cao 82px; divider dọc 1px #DDE4EF; không tách thành KPI card.

2. [Thứ bậc Metric Ledger] hiện tại: số liệu 100, 50, 1, 100 màu đen, cỡ chữ tương đối nhỏ và căn trái → phải thành: số lớn căn giữa, mỗi chỉ số có nhãn phía trên và giá trị phía dưới | thông số: nhãn 12px/500, line-height 18px; số 32px/700, line-height 40px; gap 4px; font-variant-numeric:tabular-nums.

3. [Màu số liệu] hiện tại: tất cả các số đều dùng cùng màu chữ đậm → phải thành: phân cấp màu theo ảnh duyệt, không dùng nền màu cho từng chỉ số | thông số: Sinh viên #2454B8; Đề tài #176B60; Đợt đăng ký #713CC0; Sinh viên có NV #176BFF; Giảng viên #344563; nền trắng.

4. [Panel Tổng quan số liệu — THIẾU HEADER] hiện tại: Metric Ledger hiển thị trực tiếp thành một dải chỉ số, không có tiêu đề khối → phải thành: panel “Tổng quan số liệu”, header xanh nhạt và vạch nhấn xanh, phía dưới mới là năm chỉ số | thông số: .at-panel-header cao 42px; background #EAF4FF; accent #176BFF, kích thước 4×20px; tiêu đề 14px/600; toàn panel cao khoảng 124px.

5. [Bố cục tổng thể] hiện tại: Page Header → Period → Metric Ledger không tiêu đề → hai panel cuối; bố cục bị kéo dài do panel bảng và lối tắt thao tác có padding lớn → phải thành: Header → Period → Panel Tổng quan số liệu → lưới 2 cột “Các đợt đăng ký” và “Lối tắt thao tác” | thông số: grid 12 cột; các khối đầu 12/12; hàng cuối trái 7/12, phải 5/12; gap ngang 12px; gap dọc 12px; padding trang 16px.

6. [Tỷ lệ hai panel cuối] hiện tại: “Các đợt đăng ký” chiếm khoảng 58%, “Lối tắt thao tác” khoảng 42%, tương đối gần ảnh duyệt nhưng panel thao tác có chiều cao quá lớn → phải thành: giữ tỷ lệ 7:5, tăng mật độ và thống nhất chiều cao các mục | thông số: panel min-height 310px; không đặt height:100vh; hai panel căn đỉnh trên cùng một hàng.

7. [Page Header] hiện tại: tiêu đề “Bảng điều khiển Khoa”, mô tả ngắn phía dưới, nút “Mở trang phân công” bên phải, breadcrumb phía trên → phải thành: header gọn như ảnh duyệt, tiêu đề rõ và mô tả đầy đủ vai trò quản lý Khoa | thông số: H1 24px/700, line-height 32px; mô tả 12px/19px; margin giữa tiêu đề và mô tả 4px; header min-height 64px.

8. [Nội dung mô tả trang] hiện tại: “Tổng quan hệ thống phân công đề tài tốt nghiệp cho sinh viên.” → phải thành: “Tổng quan về các đợt đăng ký khóa luận tốt nghiệp và hoạt động giảng viên trong khoa.” theo ảnh duyệt | thông số: font 12px/400; màu #596579; tối đa hai dòng tự nhiên.

9. [Breadcrumb] hiện tại: “Khoa › Tổng quan” nằm trên tiêu đề, tạo thêm một hàng thông tin → phải thành: ưu tiên Page Header compact như ảnh duyệt; nếu breadcrumb là thành phần shell chung đã khóa thì giữ nhưng giảm khoảng cách | thông số: breadcrumb 11px/18px; margin-bottom tối đa 4px; không thêm padding-top riêng.

10. [Nút Mở trang phân công] hiện tại: nút nền xanh đặc với icon phân công → phải thành: nút viền xanh, nền trắng như ảnh duyệt; giữ chức năng chuyển tới trang phân công | thông số: height 34px; padding 0 12px; border 1px #2454B8; background #FFFFFF; chữ #2454B8, 12px/600; radius 4px; icon external-link 14px.

11. [Dải thông tin đợt đăng ký] hiện tại: thông tin đợt, ngày, trạng thái và mô tả trải ngang trên một dải thấp, chưa có phân vùng rõ → phải thành: dải Period hai phần, bên trái nhận diện đợt, bên phải giải thích tình hình nghiệp vụ | thông số: grid 55% 45%; min-height 72px; padding 10px 14px; divider đứng 1px #DDE4EF; gap 12px.

12. [Icon Period] hiện tại: icon tài liệu nhỏ trước tên đợt → phải thành: icon lịch lớn trong nền xanh nhạt, nằm đầu vùng trái | thông số: Lucide calendar-days 18px; container 36×36px; background #EAF2FF; radius 50%; gap 10px.

13. [Thông tin Period] hiện tại: tên đợt, trạng thái và thời gian cùng một hàng nhỏ → phải thành: hàng đầu tên đợt + badge, hàng dưới ngày bắt đầu/kết thúc; không ép tất cả thành một dòng | thông số: tên 13px/600; badge 11px/600, height 22px; ngày 11px/18px; gap dọc 3px.

14. [Mô tả bên phải Period] hiện tại: câu giải thích nằm cùng dòng với ngày trong dải Period → phải thành: đoạn giải thích riêng bên phải, căn giữa dọc, tương tự ảnh duyệt | thông số: font 12px/19px, màu #344563; padding-left 16px; tối đa ba dòng ở desktop nếu nội dung ngắn.

15. [Trạng thái đợt] hiện tại: “Đang mở đăng ký” là badge dài → phải thành: nhãn trạng thái ngắn “Đang mở” nếu không gây sai nghĩa nghiệp vụ; chỉ thay cách đặt nhãn hiển thị, không thay status backend | thông số: badge min-height 22px; background #E5F5EC; color #176B60; font 11px/600.

16. [Panel Các đợt đăng ký] hiện tại: header có tiêu đề và dòng mô tả phụ, làm khối header cao và bảng bị đẩy xuống → phải thành: header chỉ có tiêu đề “Các đợt đăng ký” và vạch xanh như ảnh duyệt | thông số: header 42px; background #EAF4FF; tiêu đề 14px/600; vạch accent 4×20px; bỏ subtitle trong header.

17. [Cột bảng đợt đăng ký] hiện tại: có bốn cột “Đợt đăng ký”, “Thời gian”, “Sinh viên”, “Trạng thái”, nút Phân công nằm ghép trong cột trạng thái hoặc cuối hàng → phải thành: bảng 5 cột riêng biệt gồm Đợt đăng ký / Thời gian / Sinh viên / Trạng thái / Thao tác | thông số: độ rộng 34% / 26% / 12% / 16% / 12%; header cao 34px; body row tối thiểu 44px; padding 8px.

18. [Tên đợt trong bảng] hiện tại: “Đợt đăng ký ĐATN 2026” hiển thị nhỏ và gần đường viền → phải thành: tên đợt có độ đậm rõ, nằm trong ô có padding đúng chuẩn | thông số: font 12px/600, line-height 19px; padding 8px 10px; max 2 dòng.

19. [Cột Thời gian] hiện tại: thời gian hiển thị hai dòng, tỷ lệ cột hơi hẹp → phải thành: khoảng ngày được ưu tiên đủ không gian, chỉ xuống dòng khi viewport thực sự hẹp | thông số: font 11px/18px; width 26%; không dùng white-space:nowrap nếu gây tràn.

20. [Cột Sinh viên] hiện tại: 100 hiển thị căn giữa, tương đối đúng → phải thành: giữ giá trị và căn giữa, dùng số liệu thuộc chính đợt đăng ký | thông số: font 12px/600; width 12%; tabular-nums.

21. [Cột Trạng thái] hiện tại: badge “Đang mở đăng ký” dài làm cột chật → phải thành: badge compact “Đang mở” hoặc trạng thái ngắn hợp lệ khác | thông số: height 22px; padding 3px 8px; font 10–11px/600; width 16%.

22. [Cột Thao tác] hiện tại: nút “Phân công” nằm sát badge trạng thái, khiến hai chức năng nhìn như cùng một ô → phải thành: nút Phân công nằm riêng trong cột cuối, căn giữa | thông số: btn secondary min-width 72px; height 28px; font 11px/600; border #2454B8; chữ #2454B8; chỉ hiển thị khi route và quyền hợp lệ.

23. [Màu header bảng] hiện tại: header bảng gần trắng, chưa tạo khác biệt với body → phải thành: nền header xanh nhạt, cột tách nhau bằng viền mỏng như ảnh duyệt | thông số: header background #EDF5FE; border #DDE4EF; chữ #344563, 11px/600; không dùng border đậm.

24. [Chiều rộng và padding bảng] hiện tại: bảng kéo tới sát viền panel, một số ô có padding hẹp → phải thành: bảng nằm trong vùng body có lề đều, header và dữ liệu canh thẳng hàng | thông số: panel body padding 12px; table width 100%; wrapper radius 4px; overflow-x:auto chỉ khi thực sự cần.

25. [Số dòng dữ liệu] hiện tại: có một đợt đăng ký nên bảng chỉ một dòng, bên dưới trống → phải thành: giữ đúng một dòng vì dữ liệu thực; không thêm đợt giả để lấp khoảng trắng | thông số: min-height panel 310px theo layout nếu cần cân cột; không sinh hàng rỗng có đường viền.

26. [Panel Lối tắt thao tác] hiện tại: có 5 mục, gồm Phân công đề tài, Thống kê & Báo cáo, Nhập dữ liệu Excel, Giảng viên, Quản trị hệ thống → phải thành: 4 mục theo ảnh duyệt, gồm Phân công đề tài, Thống kê & Báo cáo, Nhập dữ liệu Excel, Giảng viên; mục Quản trị hệ thống vẫn ở sidebar nếu đã có route thật, không cần lặp trong lối tắt | thông số: bốn hàng, mỗi hàng min-height 64px; tổng chiều cao khoảng 256px + header 42px.

27. [Lối tắt dạng card lồng — SAI] hiện tại: mỗi mục thao tác là một card có border và radius riêng, tạo cảm giác năm hộp lồng trong panel lớn → phải thành: danh sách phẳng bốn hàng, ngăn bằng divider, không border riêng từng mục | thông số: .at-list + .at-item; item padding 10px 12px; min-height 64px; border-bottom 1px #DDE4EF; background trắng; radius 0px.

28. [Icon lối tắt] hiện tại: icon nhỏ đen/xám đặt trực tiếp trong mỗi card → phải thành: icon xanh trong ô nền xanh rất nhạt, cùng một kích thước và vị trí như ảnh duyệt | thông số: container 36×36px; background #EAF2FF; radius 6px; icon 18px, màu #2454B8; gap icon–text 12px.

29. [Cấu trúc một lối tắt] hiện tại: tên, mô tả và chevron nằm trong card có nhiều khoảng cách → phải thành: mỗi hàng gồm icon 36px bên trái, cụm tiêu đề + mô tả ở giữa, chevron bên phải | thông số: display grid; grid-template-columns:36px minmax(0,1fr) 16px; gap 12px; căn giữa theo chiều dọc.

30. [Nhãn lối tắt] hiện tại: mô tả các mục có thể xuống hai đến ba dòng, làm item cao bất thường → phải thành: tiêu đề ngắn và mô tả gọn, giữ đúng chức năng thực của route | thông số: tiêu đề 12px/600, line-height 19px; mô tả 11px/17px, tối đa hai dòng ở desktop; không ghi tính năng xuất báo cáo nếu hệ thống chưa hỗ trợ.

31. [Thứ tự lối tắt] hiện tại: Phân công → Thống kê → Nhập Excel → Giảng viên → Quản trị → phải thành: Phân công → Thống kê → Nhập Excel → Giảng viên; thứ tự cố định đúng ảnh duyệt | thông số: bốn .at-item, không chèn mục khác giữa danh sách.

32. [Chiều cao lối tắt] hiện tại: card cao, gap giữa card khoảng 10–12px, khiến cả panel dài quá viewport → phải thành: danh sách liên tục, không có gap ngoài item, tận dụng chiều cao để vừa bốn mục | thông số: item 64px; divider 1px; panel header 42px; panel body padding 0–8px.

33. [Hover lối tắt] hiện tại: hover có thể đổi toàn bộ nền card riêng → phải thành: chỉ thay nền item nhạt và đổi màu chevron, không dùng shadow nổi | thông số: hover background #F5F9FF; transition 160ms ease; focus outline 2px #2454B8.

34. [Bố cục khi ít dữ liệu] hiện tại: panel Các đợt chỉ có một dòng nhưng kéo dài vì lối tắt quá cao → phải thành: hai panel có thể cân chiều cao theo grid, nhưng bảng một dòng vẫn giữ chiều cao thực, phần trống không được lấp bằng hàng giả | thông số: align-items:stretch cho hai panel; min-height khoảng 310px; bảng bên trái height:auto.

35. [Footer ứng dụng] hiện tại: dòng “Capstone Advisor AI…” xuất hiện ở đáy sidebar; trong ảnh duyệt không gây chú ý → phải thành: footer nhỏ, không cạnh tranh với nội dung dashboard | thông số: font 10px/16px; màu #B8CBE3 trên sidebar; padding 12px; chỉ giữ nội dung footer nếu là thành phần shell thật.

36. [Mật độ chữ] hiện tại: nhiều chữ 10–11px và các panel dùng subtitle làm giao diện loãng → phải thành: thứ bậc H1 → panel heading → chỉ số → bảng → mô tả rõ như ảnh duyệt | thông số: Be Vietnam Pro; H1 24px/700; panel title 14px/600; metric number 32px/700; table body 12px/19px; caption 11px/17px.

37. [Màu sắc vùng nội dung] hiện tại: canvas xanh-xám, nhưng nền header panel quá nhạt, màu số liệu không đúng ảnh → phải thành: giữ shell và đồng bộ màu nội dung theo ATLAS đã duyệt | thông số: canvas #F2F5FB; panel #FFFFFF; header panel #EAF4FF; accent #176BFF; brand #2454B8; AI #176B60; border #DDE4EF.

38. [Viền và bo góc] hiện tại: lối tắt có nhiều viền card lồng nhau, bảng và panel chưa cùng một hệ hình học → phải thành: panel ngoài radius 6px, phần trong chủ yếu dùng divider, không thêm card con | thông số: border ngoài 1px #DDE4EF; radius 6px; divider 1px; shadow tối thiểu 0 1px 3px rgba(20,43,75,.04).

39. [Khoảng cách toàn trang] hiện tại: có khoảng trống và nhiều khoảng cách chưa thống nhất giữa header, Period, Ledger và panel cuối → phải thành: dùng thang spacing 4/8/12/16px, không phát sinh margin 20–24px tùy tiện | thông số: page padding 16px; vertical section gap 12px; panel body padding 12px; header height 42px.

40. [Độ rộng vùng nội dung] hiện tại: sidebar chiếm diện tích như bản V3.6 đã được duyệt, canvas còn lại tương đối rộng → phải thành: giữ nguyên shell, sử dụng hết chiều ngang nội dung khả dụng cho grid và ledger, không bó dashboard vào container nhỏ | thông số: main width 100% phần sau sidebar; max-width 1600px; grid gap 12px.

41. [Dữ liệu khác ảnh] hiện tại: 100 SV, 50 đề tài, 1 đợt, 100 SV có NV; ảnh duyệt có thêm 15 GV → phải thành: giữ bốn giá trị thật và bổ sung chỉ số Giảng viên tính từ CSDL; không hardcode 15 nếu DB thay đổi | thông số: count theo tập giảng viên hợp lệ của phạm vi Khoa; không lấy số 15 từ ảnh.

42. [Nút và quyền truy cập] hiện tại: Phân công, Thống kê, Nhập Excel, Giảng viên, Quản trị đều là mục có route → phải thành: giữ route thật ở sidebar; vùng lối tắt chỉ hiển thị bốn mục giống ảnh, không thêm shortcut chỉ để lấp chỗ | thông số: mỗi .at-item là một link hoạt động, min-height 64px; nếu thiếu quyền, ẩn hoặc disabled kèm giải thích theo quy tắc backend.

43. [Shell] hiện tại: topbar, sidebar và avatar đã được chủ chấp nhận → phải thành: giữ nguyên cấu trúc shell V3.6, chỉ đảm bảo logo chữ M không kèm “Open Path” và không có chuông | thông số: không thay sidebar width, topbar height, menu/breakpoint hoặc avatar trong lần sửa màn 18.

ASSET THÀNH PHẦN CÒN THIẾU

1. Lucide calendar-days — Icon Period cần đặt trong ô nền xanh nhạt 36×36px, icon 18px, stroke-width 1,8px.

2. Lucide external-link — Nút “Mở trang phân công”, icon 14px, stroke-width 1,8px.

3. Lucide users-round — Lối tắt Phân công đề tài, icon 18px, đặt trong container 36×36px.

4. Lucide chart-no-axes-column — Lối tắt Thống kê & Báo cáo, icon 18px.

5. Lucide file-spreadsheet — Lối tắt Nhập dữ liệu Excel, icon 18px.

6. Lucide graduation-cap — Lối tắt Giảng viên, icon 18px.

7. Lucide chevron-right — Mũi tên cuối từng lối tắt, icon 16px.

8. Lucide circle-check — Trạng thái “Đang mở” khi phù hợp với trạng thái nghiệp vụ, icon 13–14px.

9. Metric Ledger 5 ô — Không cần SVG riêng; dùng .at-ledger và divider CSS, hiển thị số liệu theo đúng token màu.

10. Vạch xanh tiêu đề panel — Không cần asset; dùng pseudo-element CSS ::before, kích thước 4×20px, màu #176BFF.

Không thiếu asset minh họa hoặc hoạ tiết đặc biệt phải render bằng AI. Màn Tổng quan Khoa chỉ sử dụng icon Lucide, số liệu, bảng và các component CSS có sẵn. Không cần tạo ảnh trang trí mới.

TRẠNG THÁI / HÀNH VI

1. Metric Ledger: Bổ sung chỉ số Giảng viên từ CSDL; toàn bộ năm chỉ số tính theo phạm vi Khoa và đợt phù hợp. Không hardcode số liệu tham chiếu.

2. Đợt đăng ký: Hiển thị trạng thái, thời gian và số sinh viên đúng backend. Nếu có nhiều đợt, bảng phải hiển thị từng đợt và hỗ trợ phân trang khi số lượng vượt giới hạn.

3. Nút Mở trang phân công: Điều hướng tới đúng màn 19, giữ ngữ cảnh đợt đang chọn nếu có. Không mở route không tồn tại.

4. Nút Phân công trong bảng: Mỗi hàng đợt dẫn tới trang phân công của chính đợt đó, không luôn dùng đợt mới nhất.

5. Lối tắt thao tác: Bốn hàng Phân công, Thống kê, Nhập Excel, Giảng viên đều phải điều hướng thật; không dùng href="#", click giả hoặc nút chỉ để trang trí.

6. Quản trị hệ thống: Giữ trong sidebar đã duyệt; bỏ khỏi panel Lối tắt thao tác để khớp ảnh, không xóa route hoặc quyền quản trị.

7. Quyền truy cập: Ẩn hoặc khóa thao tác khi người dùng không có quyền; backend phải kiểm tra quyền trên từng route và POST, không chỉ kiểm tra trong template.

8. Trạng thái đợt: Không đổi trạng thái nghiệp vụ từ “Đang mở đăng ký” sang trạng thái khác chỉ để giống ảnh. Cho phép dùng nhãn ngắn “Đang mở” khi không gây hiểu lầm.

9. Dữ liệu rỗng: Không có đợt → panel bảng hiển thị .at-empty “Chưa có đợt đăng ký”; Ledger hiển thị 0 hoặc dấu “—” tùy ý nghĩa chỉ số, không hiển thị số giả.

10. Dữ liệu ít: Một đợt → đúng một dòng; không thêm dữ liệu mẫu để cân panel. Danh sách lối tắt không phụ thuộc số lượng đợt.

11. Responsive dưới 768px: Thứ tự Page Header → Period → Ledger 2 cột → Các đợt đăng ký dạng .at-list → Lối tắt thao tác → Bottom Navigation. Chỉ số thứ năm chiếm hàng cuối phù hợp, không bị kéo giãn bất thường.

12. Mobile lối tắt: Mỗi item min-height 64px, icon 36×36px, mô tả tối đa hai dòng; toàn hàng là vùng click, touch target ≥44px.

13. Dark mode: Giữ theme V3.6, dùng biến tương ứng; không hardcode màu nền sáng khiến ledger/panel bị trắng trong dark mode. Màu chữ và viền đạt WCAG AA theo vai trò.

14. Accessibility: H1 duy nhất, bảng có header semantic, nút/link có nhãn, icon trang trí aria-hidden, focus rõ 2px; màu metric luôn kèm nhãn và số.

15. QA: Nghiệm thu screenshot 1440×900 phải thấy đầy đủ 5 chỉ số, bảng đợt và 4 lối tắt trong viewport đầu; kiểm tra 390px, Light/Dark, 0/1/nhiều đợt, permission, route, không tràn ngang hoặc lỗi JavaScript/HTTP 500.