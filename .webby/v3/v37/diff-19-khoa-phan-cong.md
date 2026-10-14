KHÁC BIỆT

1. [Bố cục tổng thể — NGHIÊM TRỌNG NHẤT] hiện tại: trang có thêm banner “Kết quả đã công bố” chiếm một hàng riêng, biểu đồ quá cao khiến bảng sinh viên bị đẩy xuống dưới viewport 900px → phải thành: Header → Period tích hợp trạng thái công bố → Metric Ledger → hàng Biểu đồ + Chốt & công bố → Bảng sinh viên có tìm kiếm, lọc và phân trang | thông số: grid 12 cột; gap dọc 10px; padding canvas 16px; không tạo hàng banner toàn chiều rộng.

2. [Bảng sinh viên bị khuất] hiện tại: ở độ phân giải 1440×900 chỉ nhìn thấy tiêu đề “Danh sách sinh viên”, không thấy dữ liệu → phải thành: bảng bắt đầu đủ cao để nhìn thấy tối thiểu 8–10 hàng đầu tiên khi dữ liệu ngắn như ảnh duyệt | thông số: phần Header 68px; Period 64–72px; Ledger 58–64px; hàng biểu đồ 170–190px; toolbar bảng 44px; table header 30px; row 30–34px; không tạo min-height 300px cho biểu đồ.

3. [Banner đã công bố] hiện tại: khối nền xanh lá “Kết quả đã công bố” cao khoảng 70px nằm giữa Period và Ledger → phải thành: chuyển thông báo vào phần phải của Period, giống cấu trúc ảnh duyệt, giữ nguyên trạng thái PUBLISHED | thông số: Period grid 55% 45%; divider dọc 1px #DDE4EF; phần phải padding-left 16px; tiêu đề “Kết quả đã công bố” 12px/600; mô tả 11px/18px; nền trắng hoặc xanh rất nhạt, không tạo panel thứ hai.

4. [Dải Period] hiện tại: tên đợt, badge “Đã công bố”, khoảng ngày và câu mô tả nằm thành hai dòng thấp, không có phân vùng rõ → phải thành: trái có icon lịch, tên đợt, trạng thái, thời gian; phải là thông tin về kết quả công bố | thông số: min-height 68px; padding 8px 12px; icon calendar-days 18px trong ô 36×36px, background #EAF2FF; tên 12px/600; ngày 11px/17px.

5. [Trạng thái công bố] hiện tại: panel “Chốt & công bố” chỉ hiển thị badge “Đã công bố chính thức”, còn banner riêng phía trên lặp lại thông tin → phải thành: Period thông báo trạng thái; panel Chốt & công bố trình bày kết quả nghiệp vụ và các thao tác hợp lệ, không lặp thông báo nhiều lần | thông số: trong panel công bố, badge nhỏ height 22px; font 11px/600; không thêm banner xanh lớn.

6. [Page Header] hiện tại: tiêu đề “Phân công đề tài”, mô tả và cụm chọn đợt/nút hành động khá thấp, khiến header chiếm nhiều chiều cao → phải thành: tiêu đề bên trái, chọn đợt + Chạy Greedy + Chạy tối ưu ILP bên phải trên cùng một hàng, như ảnh duyệt | thông số: H1 24px/700, line-height 32px; mô tả 12px/19px; header min-height 60–68px; gap 12px.

7. [Breadcrumb] hiện tại: “Khoa › Phân công đề tài” chiếm một dòng riêng phía trên H1 → phải thành: nếu giữ breadcrumb theo shell đã khóa thì thu gọn, tránh tăng chiều cao Page Header | thông số: font 11px/18px; margin-bottom tối đa 4px; không thêm margin-top 16px.

8. [Vị trí cụm hành động] hiện tại: dropdown đợt và hai nút nằm ngang với phần mô tả thứ hai, khá thấp → phải thành: căn phải theo phần tiêu đề trang, không làm mô tả bị ngắt dòng sớm | thông số: toolbar display flex; align-items:center; gap 8px; không wrap khi viewport ≥1200px; dropdown width 190px; nút Greedy 100px; ILP 112px.

9. [Nút Chạy Greedy] hiện tại: nút secondary màu xám, có icon và chữ nhỏ → phải thành: nút viền xanh, nền trắng, giống ảnh duyệt | thông số: height 34px; padding 0 12px; border 1px #2454B8; color #2454B8; font 11–12px/600; radius 4px.

10. [Nút Chạy tối ưu ILP] hiện tại: nút xanh có icon play, gần đúng chức năng nhưng kích thước khác → phải thành: primary xanh gọn, có icon nếu icon tương ứng chức năng thật | thông số: height 34px; padding 0 14px; background #2454B8; color #FFFFFF; font 11–12px/600; radius 4px.

11. [Dropdown chọn đợt] hiện tại: nhãn dài “Đợt đăng ký ĐATN 2026 (Đã công bố)” làm dropdown rộng và chiếm không gian → phải thành: ưu tiên tên đợt trong select, trạng thái đã công bố thể hiện ở Period; không mất định danh đợt | thông số: width 190–210px; height 34px; font 11px; text-overflow:ellipsis; giá trị đầy đủ trong danh sách lựa chọn.

12. [Metric Ledger] hiện tại: một dải sáu chỉ số có chú thích dưới số, khiến khối cao khoảng 75px → phải thành: dải chỉ số phẳng gọn như ảnh duyệt, nhãn trên và số dưới, không có dòng giải thích phụ | thông số: body min-height 58–64px; sáu cột mỗi cột 16,667%; divider 1px #DDE4EF; padding 8px 6px.

13. [Nội dung Ledger] hiện tại: Sinh viên 100, Đã xếp 43%, Đạt NV1 30%, Top 3 43%, Điểm TB 63,8, Chờ pha 2 57 → phải thành: giữ nguyên sáu chỉ số và số liệu thực, đúng thứ tự ảnh duyệt | thông số: tên các ô lần lượt Sinh viên / Đã xếp / Đạt NV1 / Top 3 / Điểm TB / Chờ pha 2; không thêm KPI card riêng.

14. [Cỡ chữ Ledger] hiện tại: số liệu và chú thích khiến chiều cao dàn trải → phải thành: các số lớn vừa đủ nổi bật nhưng tiết kiệm chiều cao | thông số: label 11px/17px, weight 500; value 23–24px/700, line-height 30px; gap 2px; font-variant-numeric:tabular-nums.

15. [Màu Ledger] hiện tại: một số chỉ số đen, xanh dương, xanh lục, màu 57 nâu cam → phải thành: hệ màu theo ảnh duyệt, chỉ tô chữ số, không tô cả ô | thông số: Sinh viên #2454B8; Đã xếp #176B60; Đạt NV1 #2454B8; Top 3 #2454B8; Điểm TB #176B60; Chờ pha 2 #C47B11.

16. [Tỷ lệ hàng biểu đồ] hiện tại: biểu đồ chiếm khoảng 66–67% chiều ngang và panel công bố 33–34%, gần đúng → phải thành: giữ tỷ lệ nhưng giảm chiều cao tổng thể | thông số: trái 8/12, phải 4/12; gap 12px; align-items:stretch; min-height hàng khoảng 180px, không ép 300px.

17. [Chiều cao biểu đồ — SAI LỚN] hiện tại: biểu đồ có hệ trục từ 0–70, cao gần 230px và nhiều khoảng trắng bên trên/các cột → phải thành: biểu đồ cột compact, cao khoảng 135–145px như ảnh duyệt | thông số: panel header 38px; chart body 135px; tổng panel 175–185px; Chart.js maintainAspectRatio:false; chart container height 135px.

18. [Tên biểu đồ] hiện tại: “Kết quả theo nguyện vọng” đã đúng nhưng có dòng mô tả phụ làm header cao → phải thành: header chỉ có tên biểu đồ, không có subtitle | thông số: .at-panel-header height 38px; title 13px/600; accent 4×18px; background #EAF4FF.

19. [Phân bố cột biểu đồ] hiện tại: NV1=30, NV2=10, NV3=3, Ngoài NV=0, Chưa xếp=57, các cột khá hẹp và cách nhau nhiều → phải thành: năm cột vừa phải, khoảng cách giống ảnh duyệt, số nằm ngay trên cột | thông số: barThickness 42px hoặc maxBarThickness 48px; categoryPercentage 0,72; barPercentage 0,8; label trên cột 10px/600.

20. [Thứ tự biểu đồ] hiện tại: NV1 / NV2 / NV3 / Ngoài NV / Chưa xếp đã đúng → phải thành: giữ nguyên thứ tự; không đổi dữ liệu thực sang số trong ảnh duyệt | thông số: trục X gồm 5 nhãn, font 10px; trục Y số nguyên, chia bước 10 hoặc 20 theo miền dữ liệu; không làm tròn sai tổng.

21. [Màu biểu đồ] hiện tại: NV1 xanh dương, NV2 xanh lục, NV3 nâu, Ngoài NV xám, Chưa xếp xanh lam đậm → phải thành: bảng màu theo ảnh duyệt, trong đó Chưa xếp phải dùng màu cam để nổi bật nhóm cần xử lý pha 2 | thông số: NV1 #176BBD; NV2 #55A1EB; NV3 #7EB8F2; Ngoài NV #A67AE8; Chưa xếp #F59B4A; không gradient.

22. [Miền trục biểu đồ] hiện tại: trục Y tới 70 cho giá trị lớn nhất 57 tạo khoảng trống trên → phải thành: miền trục Y điều chỉnh theo max dữ liệu và nhãn, không tự cắt cột | thông số: suggestedMax là bội số 10 gần nhất lớn hơn giá trị lớn nhất một khoảng 5–10 đơn vị; ví dụ max=57 thì Y tối đa 60 hoặc 70 tùy khoảng nhãn; không dùng min khác 0.

23. [Lưới biểu đồ] hiện tại: nhiều đường kẻ ngang và dọc rõ, làm biểu đồ rối hơn ảnh duyệt → phải thành: chỉ giữ lưới ngang mảnh, hạn chế hoặc tắt lưới dọc | thông số: grid Y #DDE4EF, 1px; grid X display:false; tick font 10px, color #596579; border trục 1px.

24. [Panel Chốt & công bố] hiện tại: panel có tiêu đề, mô tả dài, badge trạng thái nằm một mình phía dưới tạo khoảng trắng → phải thành: phần giải thích ngắn ở trên, vùng hành động hoặc thông tin công bố ở dưới, đúng bố cục ảnh duyệt | thông số: header 38px; body padding 12px; font mô tả 11–12px/18px; không tạo card con lồng trong panel.

25. [Trạng thái Published] hiện tại: đã công bố nên nút Chốt & công bố không còn, chỉ có badge “Đã công bố chính thức” → phải thành: giữ đúng nghiệp vụ PUBLISHED; không hiển thị lại hai nút Chốt & công bố chỉ để khớp ảnh; thay bằng badge công bố và thông tin thời điểm nếu backend có | thông số: badge min-height 22px; nền #E5F5EC, chữ #176B60; không hiển thị ngày công bố giả.

26. [Nút Xem kiểm tra] hiện tại: không có nút này trong panel công bố → phải thành: chỉ bổ sung nếu backend có route hoặc modal kiểm tra trước công bố hoạt động thật; nếu không, không thêm nút giả | thông số khi có: btn secondary height 34px; width khoảng 48% vùng actions; icon file-check-2 15px.

27. [Nút Chốt & công bố] hiện tại: không xuất hiện vì PUBLISHED → phải thành: ở trạng thái hợp lệ trước công bố mới hiển thị nút chính như ảnh duyệt; sau công bố thay bằng thông báo hoàn tất | thông số: primary height 34px; width khoảng 48%; icon send hoặc badge-check 15px; POST qua modal xác nhận hai bước.

28. [Bảng sinh viên] hiện tại: bắt đầu dưới viewport 900px; ảnh duyệt nhìn thấy khoảng 10 dòng dữ liệu và phân trang → phải thành: bảng trở thành vùng chính ở nửa dưới màn hình, không bị biểu đồ và banner che mất | thông số: panel bắt đầu khoảng y=510–545px tính theo toàn viewport 1440×900; table toolbar 44px; header 30px; body row 29–33px.

29. [Tên panel danh sách] hiện tại: “Danh sách sinh viên”, bên dưới có dòng mô tả “Chi tiết phân công từng sinh viên…” → phải thành: header chỉ “Danh sách sinh viên”, bộ lọc nằm cùng hàng hoặc ngay bên dưới theo ảnh duyệt | thông số: title 13px/600; header/toolbar kết hợp min-height 44px; không thêm mô tả phụ.

30. [Bố cục toolbar bảng] hiện tại: bảng dùng bộ lọc ở phần dưới chưa thấy rõ trong screenshot → phải thành: toolbar compact nằm cùng khu vực tiêu đề bảng: tìm kiếm → Trạng thái → Nguyện vọng → Giảng viên → tổng số sinh viên | thông số: flex nowrap ≥1200px; gap 8px; search 190px; select trạng thái 95px; select NV 100px; select GV 100px; count căn phải.

31. [Ô tìm kiếm] hiện tại: chưa xuất hiện trong vùng nhìn thấy → phải thành: “Tìm mã SV, họ tên…” có icon kính lúp | thông số: height 32px; width 190px; icon search 14px; padding-left 30px; font 11px; border #B7C5D8; radius 4px.

32. [Bộ lọc trạng thái] hiện tại: chưa thấy trong viewport → phải thành: lọc Tất cả / Đã xếp / Chờ pha 2 và trạng thái backend thực | thông số: select height 32px; width 95px; font 11px; không tạo filter không có backend.

33. [Bộ lọc nguyện vọng] hiện tại: chưa nhìn thấy → phải thành: select Tất cả / NV1 / NV2 / NV3, phân biệt sinh viên chưa xếp | thông số: width 100px; height 32px; font 11px; các giá trị phải khớp kiểu preference_rank hoặc logic backend.

34. [Bộ lọc giảng viên] hiện tại: chưa nhìn thấy → phải thành: select GV dựa trên danh sách giảng viên thực, không hardcode tên | thông số: width 100–120px; height 32px; text-overflow:ellipsis; font 11px; mặc định “Tất cả”.

35. [Bảng phân công] hiện tại: chưa nhìn thấy dữ liệu trong viewport → phải thành: bảng bảy đến chín cột theo ảnh duyệt, dữ liệu đủ để Khoa đánh giá phân công và tìm sinh viên | thông số: thứ tự Mã SV / Họ và tên / Đề tài phân công / Giảng viên / NV đạt / Điểm tổng / Nguồn / Trạng thái / Thao tác; header 30px; mỗi hàng 30–34px.

36. [Tỷ lệ cột bảng] hiện tại: chưa thể so sánh trực tiếp vì bảng nằm dưới viewport → phải thành: bố trí cân đối để không cần cuộn ngang ở 1440px | thông số: độ rộng 9% / 13% / 24% / 15% / 7% / 8% / 7% / 10% / 7%; tổng 100%; font 10–11px; cell padding 5px 6px.

37. [Tên sinh viên] hiện tại: nằm dưới viewport → phải thành: cột họ tên dễ đọc, không thay bằng MSSV hoặc viết tắt | thông số: font 11px/500; màu #172649; tên tối đa 2 dòng; không tự đổi danh tính demo.

38. [Đề tài phân công] hiện tại: nằm dưới viewport → phải thành: tên đề tài hiển thị trực tiếp, không yêu cầu mở drawer mới biết đề tài | thông số: font 10–11px/17px; max 2 dòng; không hiển thị mô tả đề tài dài trong bảng.

39. [Giảng viên] hiện tại: nằm dưới viewport → phải thành: GVHD tương ứng allocation được hiển thị ở cột riêng | thông số: 10–11px/17px; tên dài tối đa 2 dòng; không lấy GV từ NV1 nếu allocation thuộc NV2/NV3.

40. [NV đạt] hiện tại: chưa nhìn thấy → phải thành: chip NV1/NV2/NV3 theo preference_rank; chưa xếp hiển thị “—” | thông số: chip height 20px; font 10px/600; NV1 nền #E4F0FF, NV2 nền #E5F5EC, NV3 nền trung tính.

41. [Điểm tổng] hiện tại: chưa nhìn thấy → phải thành: điểm phù hợp một chữ số thập phân, có nhãn hoặc tooltip giải thích | thông số: font 11px/600; tabular-nums; màu #176B60 khi có điểm; null là “—”, không hiển thị 0 giả.

42. [Nguồn phân công] hiện tại: chưa nhìn thấy → phải thành: hiển thị nguồn thực ILP, Greedy hoặc Manual, không tự suy luận theo NV | thông số: font 10px/17px; text màu #344563; width 7%; giá trị không có là “—”.

43. [Trạng thái hàng] hiện tại: chưa nhìn thấy → phải thành: badge Đã xếp/Chờ pha 2 nhỏ, không tô màu toàn bộ hàng | thông số: badge height 20–22px; font 10px/600; Đã xếp nền #E5F5EC; Chờ pha 2 nền #FFF1D8; không tô toàn dòng hồng/vàng.

44. [Thao tác trong bảng] hiện tại: chưa nhìn thấy → phải thành: “Xem” với SV đã xếp, “Xếp tay” với SV chưa xếp và có quyền, theo ảnh duyệt | thông số: text button height 26px; font 10–11px/600; màu #2454B8; không tạo hành động giả khi PUBLISHED.

45. [Trạng thái PUBLISHED và Xếp tay] hiện tại: đợt đang PUBLISHED nên không được thao tác phân công nữa → phải thành: ẩn hoặc khóa nút Chạy ILP, Chạy Greedy, Xếp tay và Chốt & công bố khi backend không cho phép sửa, dù ảnh duyệt thể hiện trạng thái đang chuẩn bị | thông số: chế độ chỉ xem; action “Xem” được giữ; nếu cần hiển thị thông tin pha 2, dùng nhãn “Chưa được phân công” thay CTA xếp tay.

46. [Đếm sinh viên trong toolbar] hiện tại: không nhìn thấy → phải thành: hiển thị tổng sinh viên đang xét theo filter hoặc tổng đợt một cách rõ ràng | thông số: font 11px/500; màu #596579; căn phải; ví dụ “100 sinh viên”; phân biệt filtered total và overall total.

47. [Phân trang — THIẾU TRONG VIEWPORT] hiện tại: không thấy vì bảng nằm quá thấp → phải thành: footer phân trang nằm dưới bảng, bao gồm số dòng từ–đến, chọn 20/trang và Previous/Next + các trang | thông số: footer height 40–44px; page button 28×28px; gap 6px; font 11px; active background #2454B8.

48. [Số dòng một trang] hiện tại: không kiểm tra được qua ảnh → phải thành: server-side pagination mặc định 20 dòng/trang; ảnh duyệt hiển thị 10 hàng trong viewport đầu nhưng không có nghĩa backend chỉ trả 10 | thông số: per_page=20; dữ liệu 100 SV có 5 trang; không tải 100 hàng liền.

49. [Drawer chi tiết phân công] hiện tại: không mở trong ảnh chụp nên chưa đánh giá được → phải thành: click Xem mở chi tiết allocation, click Xếp tay (khi hợp lệ) mở drawer 440px có NV1–NV3, điều kiện, gợi ý và phương án xếp hợp lệ | thông số: desktop drawer width 440px; không backdrop tối nếu dùng kiểu phân tích song song; mobile full-screen 100dvh; không che thao tác bảng.

50. [Nội dung Chốt & công bố] hiện tại: chỉ có badge và câu giải thích, panel trống phần còn lại → phải thành: trong trạng thái đã công bố, thể hiện thông tin thực tế gồm trạng thái PUBLISHED, số đã xếp/chưa xếp và thời gian công bố nếu có; không tạo số liệu hoặc ngày giả | thông số: các dòng 11–12px/18px; gap 6px; background panel trắng; không thêm KPI card con.

51. [Panel và viền] hiện tại: header panel xanh xám nhạt, một số vùng có subtitle → phải thành: panel trắng, header xanh nhạt có vạch xanh trái, nhất quán ảnh duyệt | thông số: panel #FFFFFF; panel header #EAF4FF; accent #176BFF, 4×18px; border #DDE4EF; radius 5–6px.

52. [Typography] hiện tại: chữ body và nhãn biểu đồ có nhiều kích thước, chưa đủ mật độ compact → phải thành: thống nhất Be Vietnam Pro, ưu tiên tiêu đề, chỉ số và bảng phân công | thông số: H1 24px/700; panel title 13px/600; ledger value 24px/700; table header 10–11px/600; body 10–11px/17px; không dùng chữ 8–9px.

53. [Nền canvas] hiện tại: xanh xám hơi tím, ảnh duyệt có nền xanh rất nhạt → phải thành: giữ palette ATLAS đã khóa trong vùng nội dung | thông số: canvas #F2F5FB; panel #FFFFFF; line #DDE4EF; ink #172649; brand #2454B8; AI #176B60.

54. [Khoảng cách tổng thể] hiện tại: các panel và banner dùng nhiều padding khiến trang bị kéo dài → phải thành: nhịp dọc compact theo ảnh duyệt | thông số: page padding 16px; section gap 10px; panel header 38px; body padding 10–12px; không có margin-top 24px giữa các panel.

55. [Chiều cao biểu đồ và bảng] hiện tại: biểu đồ chiếm nhiều diện tích hơn bảng trong vùng nhìn thấy → phải thành: vùng biểu đồ chỉ là phần phân tích tóm tắt, bảng là thành phần chính cần ưu tiên | thông số: chart height 135px; bảng panel chiếm phần lớn chiều cao còn lại; không đặt chart canvas height:300px.

56. [Dữ liệu khác ảnh] hiện tại: NV2=10, NV3=3, Ngoài NV=0, Chưa xếp=57; ảnh duyệt có NV2=13, NV3=7, Ngoài NV=7, Chưa xếp=43 → phải thành: giữ nguyên số liệu thực và yêu cầu kiểm tra sự nhất quán giữa các chỉ số với biểu đồ, không sửa số để khớp ảnh | thông số: tổng các nhóm loại trừ nhau phải bằng tổng SV của đợt nếu tất cả thuộc phạm vi phân công; với 100 SV, 30+10+3+0+57=100.

57. [Điểm TB] hiện tại: 63,8, tương ứng ảnh duyệt → phải thành: giữ cách tính từ CSDL theo cùng phạm vi đã xếp, không tính sinh viên chưa có điểm vào mẫu số | thông số: định dạng một chữ số thập phân và dấu phẩy tiếng Việt; nhãn “Điểm TB”.

58. [Shell] hiện tại: menu trái, topbar và avatar đã được chủ duyệt → phải thành: giữ nguyên shell V3.6; chỉ bảo đảm logo chữ M, không có “Open Path” và không có chuông thông báo | thông số: không thay sidebar width, topbar height, thứ tự menu hoặc breakpoint.

ASSET THÀNH PHẦN CÒN THIẾU

1. Lucide calendar-days — Icon nhận diện Period, 18px, container 36×36px nền #EAF2FF.

2. Lucide search — Icon tìm kiếm mã SV/họ tên, 14–16px.

3. Lucide chevron-down — Select chọn đợt, trạng thái, NV và giảng viên, 14px.

4. Lucide play — Nút Chạy tối ưu ILP khi được phép, 14px.

5. Lucide git-compare — Nút Chạy Greedy nếu quy ước icon đã có, 14px.

6. Lucide file-check-2 — Nút Xem kiểm tra trước công bố khi có chức năng thật, 15px.

7. Lucide send — Nút Chốt & công bố trong trạng thái được phép, 15px.

8. Lucide badge-check — Trạng thái PUBLISHED, icon 14px.

9. Lucide circle-check — Badge Đã xếp, icon 12–14px.

10. Lucide clock — Badge Chờ pha 2 hoặc chưa phân công, 12–14px.

11. Lucide chevron-left / chevron-right — Phân trang bảng, icon 14px.

12. Lucide sliders-horizontal — Bộ lọc bảng trên mobile, 16px.

13. Lucide user-check — Ngăn kéo chi tiết/xếp tay, 16px nếu phù hợp chức năng thật.

14. Chart.js bar chart — Không cần render asset bitmap; dùng biểu đồ thực có dữ liệu từ backend, cấu hình màu và chiều cao đúng thông số.

15. Vạch xanh ở panel header — Tạo bằng CSS pseudo-element 4×18px, không cần SVG.

Không có hoạ tiết hoặc minh họa riêng phải render bằng AI. Màn Phân công Khoa thiếu chủ yếu bố cục compact, hiển thị bảng trong viewport và điều chỉnh trạng thái công bố.

TRẠNG THÁI / HÀNH VI

1. Chọn đợt: Dropdown chuyển toàn bộ metric, biểu đồ, bảng, trạng thái và quyền theo đúng period_id. Không trộn số liệu các đợt.

2. Trạng thái PUBLISHED: Kết quả đã công bố phải được hiển thị, không để CTA tối ưu/xếp tay/chốt xuất hiện như còn khả dụng. Nếu backend hỗ trợ thao tác đặc biệt sau công bố thì phải có quyền rõ ràng và luồng riêng.

3. Chạy ILP/Greedy: Chỉ khả dụng khi trạng thái và quyền hợp lệ; POST có CSRF; nút hiển thị “Đang xử lý…” và ngăn submit lặp. Không chạy thuật toán từ nút giả.

4. Kiểm tra trước công bố: Chỉ hiển thị “Xem kiểm tra” khi thực sự có trang hoặc modal tổng hợp cảnh báo, số SV chưa xếp, quota và điều kiện ràng buộc.

5. Công bố: Modal xác nhận hai bước; backend kiểm quyền, trạng thái và dữ liệu hợp lệ; không chỉ dựa vào kiểm tra chuỗi xác nhận ở giao diện.

6. Biểu đồ: Các nhóm NV1/NV2/NV3/Ngoài NV/Chưa xếp lấy từ allocation thực; các cột loại trừ nhau, không đếm trùng.

7. Bảng sinh viên: Hiển thị đầy đủ 9 cột; phân trang server-side mặc định 20/trang; không đổ 100 dòng vào một trang.

8. Tìm kiếm: Tìm theo MSSV, họ tên; giữ filter và pagination khi điều hướng; đổi filter reset về trang 1.

9. Bộ lọc: Trạng thái, NV đạt, GVHD dùng dữ liệu thật. “Chưa xếp” phải hiển thị kể cả khi topic null, không làm mất bản ghi khi JOIN.

10. Chi tiết SV: Click Xem mở đúng allocation và NV lịch sử, có giải thích điểm nếu recommendation tương ứng; không dùng dữ liệu của sinh viên khác.

11. Xếp tay pha 2: Chỉ được thao tác khi backend cho phép, chọn đề tài hợp lệ, kiểm quota GV và capacity; không phân công ngoài NV nếu chính sách hiện tại cấm.

12. Chưa xếp sau công bố: Hiển thị “Chưa được phân công”, không đưa nút Xếp tay trong bảng chỉ xem. Nếu có pha xử lý bổ sung chính thức, phải biểu diễn theo trạng thái nghiệp vụ riêng.

13. Số liệu thống kê: Đã xếp + Chưa xếp = Tổng SV trong phạm vi; %NV1 và %Top3 có mẫu số rõ ràng. Không hardcode 100/43/30/63,8/57.

14. Phân trang: Hiển thị khoảng dòng từ–đến, tổng kết quả sau lọc, số dòng/trang và điều hướng; không tạo trang giả.

15. Responsive dưới 768px: Header → Period → Ledger 2 cột → Biểu đồ → Công bố → Danh sách SV dạng .at-list → phân trang → Bottom Navigation. Mobile toolbar dùng nút Bộ lọc mở sheet; không có bảng tràn ngang toàn viewport.

16. Dark mode: Giữ data-bs-theme và token tối V3.6; màu bar Chart.js, grid, text và tooltip thay theo theme, không hardcode chữ đen trên nền tối.

17. Accessibility: Badge có chữ, chart có bảng dữ liệu thay thế, nút icon có nhãn truy cập, focus rõ; mobile touch target ≥44px, đáp ứng WCAG AA.

18. QA: Screenshot 1440×900 phải thấy Ledger, biểu đồ compact, panel công bố và ít nhất 8–10 SV đầu bảng khi dữ liệu đủ; kiểm tra 390px, Light/Dark, PUBLISHED/DRAFT, 0/100 SV, lọc, phân trang, drawer, chạy thuật toán và công bố. Không lỗi JS/CSRF/HTTP 500.