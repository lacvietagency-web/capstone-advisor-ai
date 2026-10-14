KHÁC BIỆT

1. [Bố cục tổng thể] hiện tại: cấu trúc Header → Period → Danh sách đề tài đã đúng, nhưng bảng quá ngắn, nhiều khoảng trắng, thiếu mật độ thông tin như ảnh duyệt → phải thành: giao diện quản lý đề tài tập trung vào bảng dữ liệu, chiếm phần lớn vùng nội dung; giữ đúng ba khối chính nhưng thay đổi kích thước, khoảng cách và cách trình bày | thông số: grid 12 cột; các khối rộng 12/12; padding canvas 16px; gap giữa các khối 12px; panel #FFFFFF, viền #DDE4EF, radius 6px.

2. [Page Header] hiện tại: tiêu đề “Đề tài của tôi” có dòng phụ chỉ ghi Bộ môn và Khoa, thiếu tên GVHD; breadcrumb chiếm một dòng riêng → phải thành: tiêu đề “Đề tài của tôi”, ngay dưới là “GVHD: [học hàm/học vị + họ tên] | Bộ môn: [...] | Khoa [...]” như ảnh duyệt | thông số: H1 24px/700, line-height 32px; metadata 12px/19px; divider đứng 1px, cao 14px; khoảng cách giữa các nhóm metadata 12px.

3. [Breadcrumb] hiện tại: “Tổng quan › Đề tài của tôi” nằm trên H1, tạo khoảng trống và đẩy bảng xuống → phải thành: ưu tiên Page Header compact như ảnh duyệt; nếu breadcrumb là thành phần chung đã được khóa thì giữ nhưng giảm khoảng cách | thông số: breadcrumb 11px/18px; margin-bottom tối đa 4px; không thêm padding-top riêng.

4. [Chiều cao Page Header] hiện tại: phần tiêu đề và metadata chiếm chiều cao lớn hơn cần thiết → phải thành: header hai dòng, không có đoạn mô tả bổ sung | thông số: min-height 62–68px; margin-bottom 12px; không đặt min-height 96px.

5. [Dải thông tin đợt đăng ký] hiện tại: Period là một dải thấp, thông tin tên đợt, trạng thái, ngày và mô tả nằm liên tiếp theo chiều ngang → phải thành: Period chia hai vùng rõ ràng; trái có icon lịch, tên đợt, badge và thời gian; phải có hướng dẫn quản lý đề tài | thông số: grid 55% 45%; min-height 72px; padding 10px 14px; divider dọc 1px #DDE4EF; gap 12px.

6. [Icon Period] hiện tại: icon nhỏ trước tên đợt, không có vùng nhận diện nổi bật → phải thành: icon lịch trong ô nền xanh nhạt, giống ảnh duyệt | thông số: icon Lucide calendar-days 18px, container 36×36px, background #EAF2FF, radius 50%; gap icon–text 10px.

7. [Nội dung Period] hiện tại: câu hướng dẫn “Trong thời gian này, giảng viên có thể thêm, chỉnh sửa…” nằm phía dưới thông tin đợt → phải thành: chuyển câu hướng dẫn sang cột phải, căn giữa theo chiều dọc | thông số: font 12px/19px, màu #344563; padding-left 16px; không làm tăng chiều cao nếu chỉ có hai dòng.

8. [Tên panel danh sách] hiện tại: “Danh sách đề tài hướng dẫn” và dòng mô tả phụ “Quản lý các đề tài tốt nghiệp do bạn phụ trách” → phải thành: giữ tên panel, bỏ dòng mô tả phụ để giảm chiều cao và khớp ảnh duyệt | thông số: .at-panel-header cao 42px; tiêu đề 14px/600; padding ngang 12px; vạch nhấn #176BFF kích thước 4×20px.

9. [Khoảng cách giữa header panel và toolbar] hiện tại: header panel có mô tả phụ nên vùng toolbar bị đẩy xuống → phải thành: toolbar nằm ngay dưới header, không có khoảng trống trung gian lớn | thông số: padding toolbar 10px 12px; gap giữa header và toolbar 0px; border-bottom 1px #DDE4EF.

10. [Thanh công cụ] hiện tại: ô tìm kiếm và dropdown nằm bên trái, nút Thêm đề tài nằm bên phải nhưng khoảng cách và tỷ lệ chưa giống ảnh → phải thành: ba vùng rõ: tìm kiếm rộng, trạng thái ở giữa, nút Thêm đề tài căn phải | thông số: layout flex; search width 43%; status width 22%; action margin-left:auto; gap 12px; toolbar min-height 56px.

11. [Ô tìm kiếm] hiện tại: chiều rộng tương đối nhỏ, placeholder “Tìm theo tên đề tài…” → phải thành: ô tìm kiếm rộng hơn, có icon kính lúp bên trái như ảnh duyệt | thông số: width 100% vùng search; height 36px; icon search 16px; padding-left 36px; border #B7C5D8; radius 4px; font 12px.

12. [Bộ lọc trạng thái] hiện tại: select “Tất cả trạng thái”, hình thức gần đúng nhưng đặt quá sát ô tìm kiếm → phải thành: select độc lập, căn cùng baseline với input | thông số: width 100% vùng status; height 36px; padding 0 12px; icon chevron-down 14px; font 12px; gap với search 12px.

13. [Nút Thêm đề tài] hiện tại: nút xanh nhỏ với dấu cộng, nằm phía phải toolbar → phải thành: giữ vị trí và chức năng, tăng chiều cao/độ rõ vừa đủ giống ảnh duyệt | thông số: height 36px; padding ngang 14px; background #2454B8; chữ trắng 12px/600; icon plus 15px; gap 6px; radius 5px.

14. [Mật độ bảng] hiện tại: mỗi dòng chứa tên đề tài, mô tả phụ 2 dòng, nhiều chip lĩnh vực và hai nút lớn; dữ liệu bị dàn theo chiều ngang và chiều cao không đồng nhất → phải thành: bảng một dòng thông tin chính cho mỗi đề tài, không hiển thị mô tả dài, sử dụng mật độ quản lý học vụ như ảnh duyệt | thông số: table header 34px; body row min-height 48px; padding ô 8px 10px; font body 12px/19px.

15. [Thứ tự cột] hiện tại: # / Đề tài / Lĩnh vực / Chỉ tiêu / SV đăng ký / Trạng thái / Thao tác đã đúng → phải thành: giữ nguyên thứ tự bảy cột, chỉ thay đổi chiều rộng và nội dung từng ô | thông số: tỷ lệ cột 5% / 29% / 18% / 8% / 10% / 13% / 17%.

16. [Cột số thứ tự] hiện tại: số thứ tự sát đường viền và không có khoảng trắng như ảnh → phải thành: số thứ tự căn giữa, font trung tính | thông số: width 5%; text-align:center; font 11px/500; padding 8px 6px.

17. [Cột Đề tài] hiện tại: tên đề tài màu xanh, gạch chân dạng liên kết; bên dưới có đoạn mô tả ngắn → phải thành: tên đề tài màu chữ chính, một dòng hoặc tối đa hai dòng; bỏ mô tả khỏi bảng để tập trung vào tên | thông số: font 12px/600; color #172649; line-height 19px; tối đa 2 dòng; overflow-wrap:anywhere; link chỉ giữ nếu route hoạt động thật.

18. [Đề tài dài] hiện tại: một số tên dài bị xuống dòng nhưng mô tả cũng xuống dòng, làm hàng cao không đều → phải thành: chỉ tên được phép xuống tối đa hai dòng; tên đầy đủ xem trong trang chi tiết | thông số: max-lines 2; min-height hàng 48px; khi tên 2 dòng, row tự tăng tới khoảng 54px; không cắt mất dữ liệu ở trang chi tiết.

19. [Cột Lĩnh vực] hiện tại: hiển thị nhiều chip cạnh nhau như “IoT”, “Phần mềm doanh nghiệp”, khiến cột chật → phải thành: ưu tiên hiển thị tên lĩnh vực chính như văn bản, theo ảnh duyệt; nếu một đề tài có nhiều lĩnh vực hợp lệ, trình bày tên chính trước, nhãn phụ không được phá bố cục | thông số: font 12px/19px; text color #344563; không có nền chip mặc định; max 2 dòng.

20. [Cột Chỉ tiêu] hiện tại: chỉ hiển thị một số như 2 hoặc 1 → phải thành: giữ dữ liệu chỉ tiêu thật, căn giữa và không trộn với số lượt NV1 | thông số: font 12px/600, text-align:center, tabular-nums; width 8%.

21. [Cột SV đăng ký] hiện tại: số đăng ký 1, 20, 43 được hiển thị, nhưng đơn vị chưa rõ → phải thành: giữ số lượt đăng ký thực tế theo đề tài, cột “SV đăng ký” hoặc “Lượt đăng ký” tùy nguồn đếm | thông số: font 12px/600; text-align:center; width 10%; không giới hạn số lượt bằng capacity vì một đề tài có thể nhận nhiều NV đăng ký.

22. [Cột Trạng thái] hiện tại: tất cả hàng có badge xanh “Đang mở” → phải thành: badge nhỏ, nhất quán, có thể phân biệt “Đang mở”, “Đủ chỉ tiêu”, “Tạm khóa” theo trạng thái thật của từng đề tài | thông số: height 22px; font 10–11px/600; padding 3px 8px; radius 4px; không thay trạng thái backend chỉ để khớp ảnh.

23. [Trạng thái Đủ chỉ tiêu] hiện tại: không có badge “Đủ chỉ tiêu” trong dữ liệu đang chụp → phải thành: hỗ trợ hiển thị đúng trạng thái hoặc trạng thái suy ra hợp lệ từ capacity và số sinh viên được nhận, nếu backend có quy tắc này | thông số: nền #EAF2FF, chữ #2454B8; chiều cao 22px; không lấy số lượt đăng ký làm căn cứ duy nhất kết luận đủ chỉ tiêu.

24. [Trạng thái Tạm khóa] hiện tại: không thấy trường hợp tạm khóa trên ảnh thật → phải thành: trạng thái này phải có kiểu hiển thị riêng nếu model hỗ trợ | thông số: background #FFF1D8, color #975600; badge 22px; không tạo dữ liệu tạm khóa giả.

25. [Cột Thao tác] hiện tại: có hai nút “Xem” và “Sửa” với viền xám đậm, kích thước nhỏ và sát nhau → phải thành: hai nút viền xanh mảnh “Xem” và “Sửa” như ảnh duyệt; dấu ba chấm chỉ xuất hiện khi có menu hành động thực | thông số: mỗi nút cao 28px, min-width 44px; gap 6px; border #B7C5D8 hoặc #2454B8; chữ xanh #2454B8, font 11px/600; radius 4px.

26. [Menu dấu ba chấm] hiện tại: không có icon ba chấm cuối hàng, trong ảnh duyệt có → phải thành: chỉ thêm dropdown ellipsis-vertical nếu có hành động nghiệp vụ thật ngoài Xem/Sửa; nếu không có thì không thêm icon, vì chủ cấm nút giả | thông số khi có: button 28×28px, icon 16px; menu width tối thiểu 160px; keyboard accessible.

27. [Màu nền bảng] hiện tại: table header gần như trắng, đường chia cột đậm, một số vùng trắng xám chồng nhau → phải thành: header bảng xanh cực nhạt như ảnh duyệt, đường kẻ mảnh, không kẻ viền dày quanh từng ô | thông số: header background #EDF5FE; body #FFFFFF; border #DDE4EF 1px; không zebra màu mạnh; hover #F5F9FF.

28. [Căn lề bảng] hiện tại: bảng sát mép panel, toolbar và bảng không đồng trục padding → phải thành: bảng nằm trong nội dung panel, canh thẳng hàng với toolbar và pagination | thông số: padding wrapper 12px; table width 100%; không thêm margin âm; radius 4px cho khung bảng.

29. [Chiều cao panel danh sách] hiện tại: panel kết thúc ngay sau bốn đề tài, bên dưới là footer ứng dụng và khoảng trắng canvas lớn → phải thành: panel có cấu trúc rõ header → toolbar → table → pagination; chiều cao theo dữ liệu, không cần kéo dài giả đến đáy viewport | thông số: min-height phần danh sách 340px khi desktop và có dữ liệu; không đặt height cố định 600px; panel body gap 0.

30. [Phân trang — THIẾU] hiện tại: chỉ có dòng “Hiển thị 4 / 4 đề tài”, không có điều hướng trang → phải thành: footer phân trang bên dưới bảng, gồm dòng “Hiển thị 1–4 / 4 đề tài” bên trái, cụm trang trước/số trang/sau bên phải như ảnh duyệt | thông số: footer min-height 48px; padding 10px 12px; font 11px; button page 28×28px; active background #2454B8, chữ trắng; disabled khi không có trang trước/sau.

31. [Dữ liệu một trang] hiện tại: bốn đề tài đều nằm trên một trang, nên backend có thể không render pagination → phải thành: hiển thị thông tin phân trang và số trang hiện tại; các nút trước/sau disabled nếu chỉ có một trang; không tạo page 2 giả | thông số: current page button 28×28px; tổng số trang tính ceil(total/per_page); per_page mặc định 20.

32. [Dòng kết quả] hiện tại: “Hiển thị 4 / 4 đề tài” đặt riêng ở góc dưới trái, không có khoảng chỉ số từ–đến → phải thành: format thống nhất “Hiển thị 1–4 / 4 đề tài”, căn trái footer | thông số: font 11px/18px; màu #596579; padding-left 0 trong vùng footer.

33. [Panel header và màu nhấn] hiện tại: header rất nhạt, gần như hòa với nền canvas → phải thành: header panel rõ hơn, có vạch dọc xanh tại tiêu đề | thông số: header background #EAF4FF; accent #176BFF, width 4px, height 20px; title 14px/600; border-bottom 1px #DDE4EF.

34. [Kiểu chữ] hiện tại: chữ trong bảng có nhiều cỡ nhỏ và tên đề tài link màu xanh, làm phân cấp rối → phải thành: thống nhất Be Vietnam Pro; tiêu đề trang và panel rõ, bảng tập trung dữ liệu, link không lấn át trạng thái | thông số: H1 24px/700; panel title 14px/600; body 12px/19px; table header 11px/600; table body 12px/19px; caption 11px/17px.

35. [Màu sắc tổng thể] hiện tại: xanh navy shell, nền canvas hơi tím-xám, panel gần trắng, khác độ tương phản so với ảnh duyệt → phải thành: giữ shell đã khóa, đồng bộ phần nội dung theo palette ATLAS đã duyệt | thông số: canvas #F2F5FB; panel #FFFFFF; header #EAF4FF; brand #2454B8; AI #176B60; border #DDE4EF; text #172649.

36. [Khoảng cách tổng thể] hiện tại: từ header đến Period rồi đến bảng có những khoảng lớn, toolbar/table hơi rời nhau → phải thành: một nhịp dọc thống nhất, tập trung thông tin | thông số: page padding 16px; section gap 12px; panel header 42px; toolbar min-height 56px; body padding 12px; không thêm margin 24px giữa các section.

37. [Footer ứng dụng] hiện tại: có dòng “Capstone Advisor AI…” và “Điểm phù hợp tính theo trọng số AHP-expert-v0” ở đáy màn → phải thành: không để footer kỹ thuật nổi bật cạnh bảng, nhất là thông tin version không đúng bản dữ liệu | thông số: footer nếu giữ thì font 10–11px, màu #73809A, padding 8px 16px; chỉ hiện model/weights version khi backend cung cấp; không hardcode AHP-expert-v0.

38. [Dữ liệu khác ảnh] hiện tại: GV Nguyễn Minh Bình có 4 đề tài, còn ảnh duyệt GV Phạm Hồng Quân có 6 đề tài → phải thành: giữ nguyên dữ liệu demo thật của GV đăng nhập; không thêm hai đề tài giả, không đổi tên giảng viên để khớp ảnh | thông số: query theo lecturer_id thực và quyền; số lượng tổng từ CSDL.

39. [Shell] hiện tại: sidebar và topbar đã được chủ chấp nhận → phải thành: giữ nguyên shell V3.6; logo chữ M, không có phụ đề “Open Path”, không chuông; không thay đổi chiều rộng sidebar hoặc chiều cao topbar | thông số: chỉ chỉnh vùng nội dung màn 14, không sửa component điều hướng chung.

ASSET THÀNH PHẦN CÒN THIẾU

1. Lucide calendar-days — Icon dải đợt đăng ký, 18px, container 36×36px nền #EAF2FF.

2. Lucide search — Ô tìm kiếm, icon 16px, màu #596579.

3. Lucide chevron-down — Dropdown trạng thái, icon 14px.

4. Lucide plus — Nút Thêm đề tài, icon 15px, màu trắng.

5. Lucide ellipsis-vertical — Menu hành động thêm cuối hàng, chỉ hiển thị nếu có chức năng thật.

6. Lucide chevron-left / chevron-right — Điều hướng phân trang, icon 14px.

7. Lucide circle-check — Badge trạng thái Đang mở/Đã duyệt nếu phù hợp với trạng thái backend.

8. Lucide clock — Badge trạng thái chờ hoặc khóa tạm thời nếu có trạng thái thật.

9. Chip trạng thái Đang mở/Đủ chỉ tiêu/Tạm khóa — Dùng .at-badge sẵn có, không cần SVG riêng.

Không thiếu asset minh họa đặc biệt. Các điểm cần sửa chủ yếu thuộc bố cục bảng, mật độ dữ liệu, Period, toolbar và phân trang.

TRẠNG THÁI / HÀNH VI

1. Danh sách đề tài: Query chỉ lấy đề tài thuộc giảng viên đăng nhập, giữ đúng tên, lĩnh vực, chỉ tiêu, số lượt SV đăng ký và trạng thái thực.

2. Tìm kiếm: Tìm theo tên đề tài, không phân biệt hoa/thường; kết quả server-side. Khi đổi từ khóa, reset về trang 1 và giữ bộ lọc trạng thái.

3. Lọc trạng thái: “Tất cả trạng thái”, “Đang mở”, “Đủ chỉ tiêu”, “Tạm khóa” chỉ xuất hiện nếu backend có trạng thái tương ứng. Không gán trạng thái giả từ CSS.

4. Thêm đề tài: Nút Thêm đề tài dẫn đến form màn 15 có chức năng thật; chỉ hiện khi quyền và trạng thái đợt cho phép.

5. Xem đề tài: Nút Xem dẫn đến đúng trang chi tiết của topic; nếu GV cần xem sinh viên đăng ký, route phải cung cấp lối vào thật, không đặt nút giả.

6. Sửa đề tài: Nút Sửa mở đúng form edit cùng topic_id; chỉ hiện khi backend cho phép. Nếu không được sửa, ẩn nút hoặc disabled kèm lý do rõ ràng.

7. Duyệt SV: Từ danh sách đề tài, GV phải có lối vào xem sinh viên đăng ký của từng đề tài, theo route hiện có /de-tai/<id>/dang-ky/. Không tạo trang tổng duyệt SV không tồn tại.

8. Phân trang: Mặc định 20 đề tài/trang, server-side; hiển thị số bản ghi từ–đến và tổng. Chỉ một trang thì nút Previous/Next disabled; không tạo trang giả.

9. Trạng thái đề tài: Capacity và số SV đăng ký là hai chỉ số khác nhau; không dùng số NV đăng ký lớn hơn chỉ tiêu để tự chuyển thành “Đủ chỉ tiêu”.

10. Đợt đóng/công bố: Danh sách vẫn xem được, nhưng các hành động Thêm/Sửa phải tuân thủ permission và trạng thái. Không cho ghi dữ liệu khi backend khóa.

11. Trạng thái rỗng: Không có đề tài → .at-empty “Bạn chưa có đề tài hướng dẫn”, CTA Thêm đề tài chỉ khi được phép. Không dùng bảng trắng không giải thích.

12. Dữ liệu ít: Một đến bốn đề tài → bảng co theo dữ liệu, pagination một trang, không tạo hàng mẫu để lấp khoảng trống.

13. Responsive dưới 768px: Thứ tự Header → Period → Tìm kiếm → Lọc trạng thái → Danh sách đề tài dạng .at-list → Phân trang → Bottom Navigation. Mỗi item có tên, lĩnh vực, chỉ tiêu, SV đăng ký, trạng thái và hành động hợp lệ.

14. Accessibility: Input có label, nút icon có aria-label, badge không chỉ thể hiện bằng màu, focus rõ; touch target mobile ≥44px; tương phản WCAG AA.

15. QA: Nghiệm thu 1440×900 phải có header, Period, toolbar, bảng và footer phân trang cùng hiện; thử 390px Light/Dark, tìm kiếm, lọc, thêm/sửa/xem, đề tài khóa, một trang/nhiều trang, dữ liệu rỗng; không lỗi template, JavaScript, CSRF hoặc HTTP 500.