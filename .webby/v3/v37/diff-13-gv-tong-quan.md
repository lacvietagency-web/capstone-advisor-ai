KHÁC BIỆT

1. [Bảng sinh viên chờ duyệt — NGHIÊM TRỌNG NHẤT] hiện tại: bảng “Đề tài có sinh viên chờ duyệt” chỉ liệt kê đề tài, lĩnh vực, sức chứa, số chờ duyệt và nút “Duyệt ngay”; không thấy tên sinh viên, MSSV, điểm AI và thứ tự nguyện vọng → phải thành: bảng liệt kê trực tiếp từng lượt sinh viên đăng ký như ảnh duyệt; mỗi hàng tương ứng một lượt đăng ký của một sinh viên vào một đề tài thuộc GV | thông số: 7 cột theo thứ tự Đề tài / Sinh viên / MSSV / Điểm AI / NV / Trạng thái / Thao tác; độ rộng 23% / 19% / 13% / 10% / 8% / 15% / 12%; header 34px; mỗi hàng min-height 38px; font 11–12px; padding ô 6px 8px.

2. [Nguồn dữ liệu bảng] hiện tại: dữ liệu được tổng hợp theo từng đề tài nên một hàng có thể chứa 19 lượt chờ duyệt nhưng không xác định được từng sinh viên → phải thành: dữ liệu bảng lấy từ từng bản ghi đăng ký nguyện vọng, JOIN với Student, Topic và Recommendation tương ứng; chỉ hiển thị các bản ghi thuộc đề tài mà GV đăng nhập được phân quyền xét duyệt | thông số: một hàng = một bản ghi đăng ký; khóa định danh ổn định theo preference/registration ID; không nhân bản một sinh viên nếu cùng bản ghi được JOIN nhiều lần.

3. [Mục đích bảng] hiện tại: danh sách đề tài khiến GV phải đi thêm một bước mới biết sinh viên nào đăng ký → phải thành: bảng chờ duyệt cho phép GV nhìn ngay tên sinh viên, điểm AI, NV và trạng thái; nút “Phân tích” mở đúng hồ sơ đăng ký | thông số: mặc định sắp xếp lượt chờ duyệt theo thời điểm nộp tăng dần, sau đó ID tăng dần; tối đa 10 hàng ở trang Tổng quan; giữ đường dẫn tới trang duyệt theo từng đề tài.

4. [Tên panel] hiện tại: “Đề tài có sinh viên chờ duyệt” với mô tả “Danh sách đề tài có các nguyện vọng đang đăng ký cần xử lý” → phải thành: “Đề tài có sinh viên chờ duyệt” nhưng bảng bên trong là danh sách sinh viên, không phải thống kê đề tài | thông số: header panel 42px; tiêu đề 14px/600; vạch accent xanh #176BFF rộng 4px, cao 20px; bỏ dòng mô tả phụ để giảm chiều cao.

5. [Bộ lọc bảng] hiện tại: tìm theo tên đề tài và lọc “Tất cả trạng thái”; không hỗ trợ tìm sinh viên/MSSV ngay tại Tổng quan → phải thành: ô tìm kiếm “Tìm theo tên đề tài, sinh viên…” và dropdown trạng thái mặc định “Chờ duyệt” | thông số: toolbar grid 65% 35%; gap 12px; input/select cao 36px; padding toolbar 10px 12px; font 12px.

6. [Cột Sinh viên] hiện tại: hoàn toàn thiếu → phải thành: họ tên SV nằm ở cột thứ hai, ngay sau Đề tài, để GV nhận biết người đăng ký | thông số: tên font 12px/600, màu #172649; tối đa 2 dòng; tên đầy đủ trong drawer; không dùng mã thay cho họ tên.

7. [Cột MSSV] hiện tại: hoàn toàn thiếu → phải thành: MSSV dạng 2023xxxx, riêng từng lượt đăng ký | thông số: font 11px/500, tabular-nums, không ngắt dòng; độ rộng 13%.

8. [Cột Điểm AI] hiện tại: hoàn toàn thiếu → phải thành: điểm phù hợp ứng với chính cặp sinh viên–đề tài, căn phải hoặc căn giữa nhất quán | thông số: font 12px/600, màu #176B60; số thập phân một chữ số, ví dụ 82,4; nếu chưa có điểm thì hiển thị “Chưa đánh giá” hoặc trạng thái sơ bộ tương ứng, không thay bằng 0.

9. [Cột Nguyện vọng] hiện tại: hoàn toàn thiếu → phải thành: chip NV1/NV2/NV3 theo thứ tự đăng ký thực | thông số: chip min-width 36px, height 22px; padding 2px 7px; radius 4px; font 11px/600; nền xanh nhạt cho NV1, xanh ngọc nhạt cho NV2, trung tính cho NV3.

10. [Cột Trạng thái] hiện tại: bảng dùng “Đang mở” của đề tài, không phải trạng thái duyệt đăng ký của sinh viên → phải thành: hiển thị “Chờ duyệt”, “Đồng ý”, “Từ chối” theo từng registration | thông số: badge height 22px; font 10–11px/600; Chờ duyệt nền #FFF1D8, chữ #975600; Đồng ý nền #E5F5EC, chữ #176B60; Từ chối nền #FCE8EB, chữ #B42335.

11. [Cột Thao tác] hiện tại: “Duyệt ngay” gắn với mỗi đề tài, dẫn GV sang trang khác → phải thành: nút “Phân tích” gắn với từng sinh viên, mở drawer hoặc trang duyệt SV của đúng đề tài | thông số: btn secondary cao 28–30px; padding ngang 10px; border #2454B8; chữ #2454B8, 11px/600; không có nút Đồng ý/Từ chối trực tiếp trong bảng Tổng quan.

12. [Mật độ bảng] hiện tại: mỗi dòng gồm tên đề tài, mô tả dài, các nhãn lĩnh vực và nút, khiến chiều cao hàng lớn → phải thành: bảng compact tương tự ảnh duyệt, chỉ giữ tên đề tài và các trường phục vụ quyết định duyệt | thông số: hàng tối thiểu 38px; tên đề tài tối đa 2 dòng; không hiển thị mô tả đề tài, thẻ lĩnh vực hoặc sức chứa trong bảng này; bảng 5 dòng khoảng 225–255px gồm header.

13. [Vị trí bảng] hiện tại: bảng bắt đầu quá thấp vì Metric Ledger và các panel phía trên chiếm nhiều chiều cao → phải thành: bảng bắt đầu ngay dưới Ledger và nhìn thấy các sinh viên trong viewport 900px | thông số: page header khoảng 72px; Period 72–88px; Ledger 110–124px; section gap 12px; không dùng min-height 184px cho Ledger.

14. [Bố cục tổng thể] hiện tại: cấu trúc Header → Period → Ledger → hai cột bảng và trạng thái đợt đã đúng, nhưng mật độ còn lỏng, bảng chỉ có vài dòng đề tài → phải thành: giữ cấu trúc đó, tái tổ chức nội dung thành dạng thông tin học vụ mật độ cao | thông số: grid 12 cột; hàng cuối trái 8/12, phải 4/12; gap 12px; padding trang 16px; panel nền #FFFFFF, border #DDE4EF, radius 5–6px.

15. [Page Header] hiện tại: “Xin chào, PGS.TS. Nguyễn Minh Bình”, dòng bộ môn bên dưới; thiếu mã GV trong metadata, có breadcrumb và nút bên phải → phải thành: lời chào, dòng “GVHD: [mã GV] | Bộ môn: [...] | Khoa [...]” theo dữ liệu thực, nút “Đề tài của tôi” bên phải | thông số: H1 24px/700, line-height 32px; metadata 12px/19px; nút cao 34px; header min-height 64–72px; chỉ hiển thị mã GV/Khoa khi backend có dữ liệu.

16. [Breadcrumb] hiện tại: “Tổng quan” nằm ở một dòng riêng trên tiêu đề → phải thành: ưu tiên header gọn như ảnh duyệt; nếu giữ breadcrumb do shell đã khóa, không cho nó làm tăng khoảng trống phía trên | thông số: font 11px/18px; margin-bottom tối đa 4px.

17. [Period] hiện tại: thẻ đợt gồm tên, trạng thái, thời gian và câu hướng dẫn xếp dọc, làm chiều cao tăng → phải thành: hai vùng ngang: thông tin đợt bên trái, hướng dẫn GV xét duyệt bên phải | thông số: grid 55% 45%; min-height 72px; divider dọc 1px #DDE4EF; padding 10px 14px; gap 12px.

18. [Icon Period] hiện tại: dùng icon nhỏ clipboard-list trước tên đợt → phải thành: icon lịch calendar-days trong nền xanh nhạt như ảnh duyệt | thông số: icon 18px; container 36×36px, background #EAF2FF, radius 50%; gap icon–nội dung 10px.

19. [Metric Ledger] hiện tại: panel chứa bốn card số liệu có nhiều dòng nhãn và chú thích, tiêu đề khối có thêm subtitle → phải thành: một dải Metric Ledger phẳng, bốn chỉ số căn giữa, ngăn nhau bằng đường dọc, giữ tiêu đề “Tổng quan đề tài hướng dẫn” | thông số: header 38–42px; ledger body cao 96px; bốn cột 25%; divider #DDE4EF; không icon tròn.

20. [Tên các chỉ số] hiện tại: “Số đề tài”, “Tổng SV đăng ký”, “Số NV đang chờ duyệt”, “Số đã đồng ý” → phải thành: nhãn ngắn “Đề tài”, “SV đăng ký”, “Chờ duyệt”, “Đã đồng ý”, chú thích nhỏ phía dưới số như ảnh duyệt | thông số: label 12px/600; số lớn 30–34px/700; chú thích 10–11px/17px; gap dọc 4px.

21. [Màu các số liệu] hiện tại: các chỉ số số lớn chủ yếu dùng màu đen, chỉ một vài số có màu cam/xanh → phải thành: màu phân cấp như ảnh duyệt: Đề tài xanh dương, SV đăng ký xanh ngọc, Chờ duyệt cam, Đã đồng ý xanh lá | thông số: Đề tài #2454B8; SV đăng ký #176B60; Chờ duyệt #C47B11; Đã đồng ý #176B60; không tô nền toàn ô.

22. [Ý nghĩa số liệu] hiện tại: Tổng SV đăng ký 57, số NV chờ duyệt 64; có thể là hai đơn vị đếm khác nhau → phải thành: nhãn phân biệt rõ số sinh viên duy nhất và số lượt đăng ký, không để hội đồng hiểu 64 sinh viên đang chờ trong khi chỉ có 57 sinh viên | thông số: Nếu số 57 là số SV duy nhất, chú thích “57 sinh viên”; nếu 64 là lượt NV chờ duyệt, chú thích “64 lượt đăng ký”; không đổi giá trị thực.

23. [Panel Trạng thái đợt] hiện tại: nhiều card con có viền, khoảng cách lớn, mỗi card chứa trạng thái và giải thích; panel cao kéo dài → phải thành: một panel đơn với ba mục thông tin xếp dọc, phân tách bằng đường kẻ mảnh, không tạo card lồng card | thông số: header 42px; item min-height 78px; padding 10px 12px; gap 0; border-bottom 1px #DDE4EF; không có radius riêng từng item.

24. [Mục trạng thái đăng ký] hiện tại: trạng thái “Đang nhận đăng ký” trong một card trắng → phải thành: dải trạng thái xanh nhạt nhấn nhẹ, icon chấm xanh hoặc circle-check, tiêu đề và mô tả ngắn | thông số: background #EAF7F0; border-radius 4px; padding 10px 12px; title 12px/600; nội dung 11px/18px.

25. [Mục hạn duyệt GV] hiện tại: một card riêng hiển thị ngày hạn duyệt và mô tả → phải thành: hàng compact gồm icon clock, nhãn “Hạn duyệt của giảng viên”, ngày đậm và câu nhắc dưới | thông số: icon 16px; ngày 12px/600; mô tả 11px/18px; item min-height 74px; chỉ hiển thị ngày khi backend có dữ liệu.

26. [Mục kết quả phân công] hiện tại: mục thứ ba có thể nằm ngoài viewport, khiến nội dung Trạng thái đợt bị đẩy xuống → phải thành: ba mục của panel trạng thái có mặt trong màn hình đầu khi dữ liệu ngắn | thông số: item thứ ba min-height 74px; nhãn 12px/600; mô tả tối đa 3 dòng, không cắt dữ liệu quan trọng.

27. [Nút Xem tất cả] hiện tại: có link “Xem tất cả” trên header bảng, nhưng bảng không liệt kê SV như ảnh duyệt → phải thành: link này chỉ tồn tại nếu có trang danh sách SV đăng ký thực tế; khi bảng đổi sang từng SV, nút có thể dẫn tới danh sách đăng ký theo đề tài phù hợp | thông số: font 11px/600; icon chevron-right 14px; nếu chưa có route tổng, ẩn hẳn để tránh nút giả.

28. [Thanh tìm kiếm] hiện tại: search input ngắn và còn nhiều khoảng trắng trong toolbar → phải thành: ô tìm kiếm chiếm khoảng 65%, select trạng thái 35%, cùng một hàng và căn giữa | thông số: toolbar padding 10px 12px; gap 12px; height control 34–36px; border #B7C5D8; radius 4px.

29. [Trạng thái mặc định bảng] hiện tại: “Tất cả trạng thái” → phải thành: mặc định “Chờ duyệt” để GV thấy ngay các lượt cần xử lý; vẫn hỗ trợ chọn Tất cả, Đồng ý, Từ chối khi có backend filter | thông số: select font 12px; height 36px; query status=pending hoặc giá trị tương đương model hiện có; không tự đặt filter mà backend không hỗ trợ.

30. [Tên đề tài trong bảng] hiện tại: tên đề tài có màu xanh dạng link, mô tả dưới tên chiếm 2–3 dòng → phải thành: tên đề tài màu chữ chính, ngắn gọn, không thêm mô tả; chỉ link nếu route dẫn đúng trang duyệt | thông số: font 11–12px/600; color #172649; max 2 dòng; không tạo hover link nếu không thể mở.

31. [Nguồn và luồng duyệt] hiện tại: nút “Duyệt ngay” trên từng đề tài là hành động cấp đề tài → phải thành: “Phân tích” từng SV, đi tới đúng catalog/lecturer_registrations với topic_id và preference_id hoặc mở drawer của màn 16 | thông số: nút 28–30px; không thực hiện Đồng ý/Từ chối trực tiếp từ trang Tổng quan nếu chưa kiểm tra eligibility.

32. [Khoảng cách panel] hiện tại: Period, Ledger, bảng và Trạng thái dùng các khoảng cách lớn, nhiều padding → phải thành: nhịp compact nhất quán ảnh duyệt | thông số: section gap 10–12px; panel body padding 10–12px; header 42px; không thêm margin-top 24px nội bộ.

33. [Màu panel và header] hiện tại: header panel xanh xám rất nhạt và vùng nền nhiều mức trắng/xám → phải thành: panel trắng, header xanh nhạt rõ ràng, vạch accent xanh trái | thông số: panel #FFFFFF; header #EAF4FF; vạch #176BFF, 4×20px; border #DDE4EF; radius 6px; shadow tối thiểu.

34. [Mật độ chữ] hiện tại: bảng và mô tả có nhiều chữ 10–11px, độ đậm không đồng đều → phải thành: dùng Be Vietnam Pro, ưu tiên tên sinh viên, điểm AI và trạng thái | thông số: H1 24px/700; panel title 14px/600; table header 11px/600; table body 11–12px/19px; chú thích 11px/17px; không dùng chữ 9px.

35. [Dữ liệu khác ảnh] hiện tại: GV Nguyễn Minh Bình, 4 đề tài, 57 SV, 64 lượt NV chờ, khác GV Phạm Hồng Quân và số 6/18/5/9 trong ảnh duyệt → phải thành: giữ nguyên dữ liệu demo thực, không thay tên, số lượng hoặc ngày cho giống ảnh | thông số: mọi metric/query phụ thuộc GV đang đăng nhập, đợt đăng ký và permission; không hardcode số.

36. [Shell] hiện tại: sidebar và topbar V3.6 đã được chủ chấp nhận → phải thành: giữ nguyên bố cục shell, logo chữ M đã chọn, không có phụ đề “Open Path”, không có chuông | thông số: không sửa width sidebar, height topbar hoặc breakpoint để khớp riêng trang 13.

ASSET THÀNH PHẦN CÒN THIẾU

1. Lucide search — Ô tìm tên sinh viên/MSSV/đề tài, icon 16px, màu #596579, padding-left input 36px.

2. Lucide circle-check — Trạng thái đã đồng ý và đang nhận đăng ký, icon 14–16px, màu #176B60.

3. Lucide clock — Trạng thái chờ duyệt và hạn duyệt giảng viên, icon 14–16px, màu #C47B11 hoặc trung tính theo ngữ cảnh.

4. Lucide calendar-days — Icon Period trong nền xanh nhạt 36×36px, icon 18px.

5. Lucide file-text — Nút “Đề tài của tôi” ở Header, 15px.

6. Lucide chevron-down — Dropdown lọc trạng thái, 14px.

7. Lucide chevron-right — Link chuyển tới trang duyệt chi tiết hoặc Xem tất cả nếu route tồn tại, 14px.

8. Lucide user-round — Nhận diện sinh viên trong drawer nếu cần; không đặt icon ở từng hàng bảng gây tăng chiều cao.

9. Chip NV1/NV2/NV3 — Không cần asset riêng; tạo bằng .at-chip có màu theo rank, kích thước 36×22px.

10. Badge Chờ duyệt/Đồng ý/Từ chối — Dùng .at-badge hiện có; không cần SVG mới.

Không thiếu asset hình học hoặc minh họa đặc biệt. Cần sửa trọng tâm là cấu trúc bảng từ đề tài sang từng sinh viên đăng ký.

TRẠNG THÁI / HÀNH VI

1. Danh sách SV chờ duyệt: Mặc định liệt kê từng lượt đăng ký đang chờ thuộc các đề tài do GV đăng nhập hướng dẫn. Hiển thị đầy đủ tên SV, MSSV, điểm AI, NV và trạng thái.

2. Tìm kiếm: Tìm theo tên sinh viên, MSSV hoặc tên đề tài; không chỉ tìm tên đề tài. Tìm kiếm xử lý server-side, giữ filter và phân trang.

3. Bộ lọc: Mặc định “Chờ duyệt”; các lựa chọn khác phải dùng trạng thái thật trong model. Không tự gán tất cả là Chờ duyệt để khớp ảnh.

4. Điểm AI: Lấy từ Recommendation đúng cặp SV–đề tài, đúng phiên bản khi có; nếu M5 hoặc M4 chưa được đánh giá, hiển thị sơ bộ theo nghiệp vụ, không thay bằng 0. M5 luôn gọi là “Đánh giá LLM”.

5. Phân tích SV: Nút Phân tích mở đúng hồ sơ sinh viên thuộc lượt đăng ký, với nội dung M1–M5, GPA, kỹ năng, điều kiện, NV và quyền duyệt. Có thể dẫn tới màn 16 nếu backend hiện chỉ hỗ trợ URL theo đề tài.

6. Duyệt/Từ chối: Không thêm nút duyệt/từ chối trực tiếp vào bảng Tổng quan. Hành động quyết định được thực hiện trong màn 16 hoặc drawer sau khi GV xem điều kiện; Từ chối yêu cầu lý do theo validation backend.

7. Metric Ledger: Đề tài, SV đăng ký, Chờ duyệt, Đã đồng ý tính theo phạm vi GV và đợt. Nếu chỉ số đếm lượt preference chứ không phải SV duy nhất, nhãn phải nói rõ.

8. Trạng thái đợt: Ngày mở/đóng, hạn duyệt và phân công chỉ lấy từ backend. Nếu không có hạn duyệt, ẩn mục hạn thay vì tạo ngày giả.

9. Đợt đóng/đã công bố: Trang vẫn cho xem lịch sử đăng ký nhưng các thao tác duyệt phải khóa theo quyền và trạng thái thực. Không ẩn toàn bộ bảng khi đợt đóng.

10. Dữ liệu ít/rỗng: Nếu chưa có SV chờ duyệt, hiện .at-empty “Chưa có sinh viên chờ duyệt”; các đăng ký đã xử lý vẫn có thể xem bằng filter nếu backend hỗ trợ.

11. Phân trang: Tối đa 10 lượt đăng ký trên Trang chủ GV; nếu nhiều hơn, hiển thị điều hướng tới danh sách có chức năng thật hoặc phân trang server-side. Không load toàn bộ hàng trăm lượt.

12. Mobile dưới 768px: Thứ tự Header → Period → Ledger 2×2 → Danh sách SV dạng .at-list → Trạng thái đợt. Mỗi item tối thiểu 96px gồm tên SV, MSSV, đề tài, điểm, NV, trạng thái và nút Phân tích; không dùng bảng rộng.

13. Accessibility: Tên SV và MSSV không bị che, badge có chữ, điểm AI có nhãn, focus rõ; touch target mobile ≥44px; đạt WCAG AA.

14. QA: Nghiệm thu 1440×900 phải nhìn thấy ít nhất 5 sinh viên trong bảng khi dữ liệu có đủ; test 390px, Light/Dark, lọc pending/approved/rejected, dữ liệu thiếu điểm AI, quyền của GV và đường dẫn tới màn 16. Không lỗi template, JavaScript hoặc HTTP 500.