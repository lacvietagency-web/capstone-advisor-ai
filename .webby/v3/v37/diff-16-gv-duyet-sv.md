KHÁC BIỆT

1. [Bố cục tổng thể — NGHIÊM TRỌNG NHẤT] hiện tại: khi mở ngăn kéo Phân tích, toàn bộ trang phía sau bị phủ lớp đen bán trong suốt, nội dung trở nên khó đọc → phải thành: ngăn kéo mở bên phải nhưng trang phía sau vẫn sáng, đọc được bảng sinh viên, đúng ảnh duyệt; không sử dụng backdrop tối cho drawer phân tích | thông số: Bootstrap Offcanvas data-bs-backdrop="false"; drawer width 440px; background #FFFFFF; border-left 1px #DDE4EF; z-index 1050; không khóa cuộn toàn trang.

2. [Vùng bảng khi mở drawer] hiện tại: bảng sinh viên vẫn chiếm chiều rộng cũ và bị drawer che mất các cột bên phải → phải thành: vùng nội dung chính tự thu hẹp để nằm hoàn toàn bên trái drawer, không bị che cột Thao tác | thông số: desktop ≥1200px, khi drawer mở, vùng main có margin-right:440px hoặc chiều rộng khả dụng tương đương; transition 180ms cubic-bezier(.2,.7,.2,1); không tạo thanh cuộn ngang toàn viewport.

3. [Chiều rộng drawer] hiện tại: drawer khoảng 440px nhưng chiếm tỷ lệ lớn so với vùng nội dung còn lại, thông tin bên trong xếp dọc thiếu phân cấp → phải thành: drawer 440px cố định, chia rõ header, thông tin SV, đề tài, AI, điều kiện, giới thiệu, nhận xét và footer | thông số: width 440px; min-width 0; height 100dvh; display flex; flex-direction column; body overflow-y:auto; header 56px; footer min-height 72px.

4. [Thứ tự nội dung drawer] hiện tại: Header → thông tin SV nhỏ → điểm AI → textarea nhận xét → footer; thiếu các khối phân tích quan trọng → phải thành: Header → Tên SV/MSSV → Đề tài đăng ký/NV → Kết quả đánh giá AI → Kiểm tra điều kiện → Giới thiệu bản thân → Nhận xét giảng viên → Footer | thông số: gap giữa các section 12px; padding body 16px; không tạo khoảng trống lớn giữa các khối.

5. [Header drawer] hiện tại: tiêu đề “Phân tích hồ sơ sinh viên” nằm trên một vùng trắng, nút đóng nhỏ ở góc phải → phải thành: header cố định theo ảnh duyệt, tiêu đề căn trái rõ ràng, nút X bên phải | thông số: height 56px; padding 0 16px; border-bottom 1px #DDE4EF; title 16px/700, màu #172649; icon x 18px; nút đóng 36×36px.

6. [Thông tin nhận diện sinh viên] hiện tại: tên Nguyễn Thu Hùng chỉ là dòng phụ dưới tiêu đề drawer; MSSV, ngành, GPA và trạng thái nằm trong khối thông tin nhỏ riêng → phải thành: tên SV là heading lớn đầu drawer, ngay dưới có MSSV và Ngành, GPA chuyển sang phần kiểm tra điều kiện | thông số: tên 20px/700, line-height 28px; metadata 12px/19px; divider dọc 1px; khoảng cách tên–metadata 4px; padding-bottom 12px.

7. [Thẻ trạng thái SV] hiện tại: badge “Chờ duyệt” nằm trong nhóm thông tin đầu drawer → phải thành: trạng thái được thể hiện trong bảng chính và có thể giữ badge nhỏ cạnh thông tin đăng ký, không chiếm một hàng riêng dưới GPA | thông số: badge cao 22px; font 11px/600; background #FFF1D8; color #975600.

8. [Đề tài đăng ký] hiện tại: tên đề tài nằm trong một card thông tin cùng MSSV/GPA và nguyện vọng → phải thành: một dải riêng có nhãn “Đề tài đăng ký”, tên đề tài nổi bật bên trái và chip NV1/NV2/NV3 bên phải | thông số: min-height 76px; padding 12px 14px; border 1px #DDE4EF; radius 5px; grid minmax(0,1fr) 76px; gap 12px.

9. [Tên đề tài trong drawer] hiện tại: chữ nhỏ, không có thứ bậc nổi bật → phải thành: tên đề tài 14px/600, tối đa ba dòng nếu dài; label ở trên | thông số: label 11px/17px; title 14px/21px; margin-top 4px.

10. [Chip NV] hiện tại: NV1 dạng viền xám nhỏ → phải thành: chip xanh nhạt có số thứ tự rõ, đặt trong vùng riêng bên phải đề tài như ảnh duyệt | thông số: chip 56×32px; background #E4F0FF; color #2454B8; font 13px/700; radius 4px; căn giữa.

11. [Panel đánh giá AI] hiện tại: panel có header và tổng điểm 67,0, năm hàng mô hình nhưng phần thông tin bị nén, các thanh điểm dài không đều → phải thành: panel “Kết quả đánh giá AI”, bên trái ô điểm lớn, bên phải năm hàng Evidence M1–M5, cùng hàng trên desktop drawer | thông số: panel header 38–42px; body grid 38% 62%; gap 10px; padding 10px; min-height 144px.

12. [Tên M5] hiện tại: đã ghi “Đánh giá LLM”, đúng quyết định → phải thành: giữ nguyên “M5 Đánh giá LLM”, không dùng “Mức phù hợp” hay “LLM” đơn lẻ | thông số: label 10–11px/17px.

13. [Điểm tổng AI] hiện tại: số 67,0 lớn nhưng không có vùng phân tách rõ, chú thích “Điểm sơ bộ M1–M4” nằm dưới → phải thành: ô điểm riêng như ảnh duyệt, nhấn mạnh tổng điểm | thông số: số 36–40px/700, màu #176B60; /100 14px; caption 11px/17px; border 1px #DDE4EF; radius 5px; padding 10px.

14. [M1–M5 Evidence] hiện tại: các hàng dùng thanh xanh dương, nhãn có trọng số phần trăm, M4/M5 chưa đánh giá → phải thành: năm thanh màu xanh AI, label M1–M5 và tên mô hình, điểm căn phải; trọng số AHP chuyển lên header của panel | thông số: mỗi hàng min-height 22px; thanh cao 7px; fill #176B60; track #E5EAF1; label 10–11px; điểm 11px/600.

15. [AHP] hiện tại: header AI có dòng “Trọng số AHP: expert-v0”, mang tính kỹ thuật và chiếm một hàng → phải thành: AHP hiển thị bằng bộ trọng số có dữ liệu thực, như ảnh duyệt | thông số: khi có weights thực, ghi “AHP: 25% / 20% / 15% / 20% / 20%” hoặc các giá trị phiên bản tương ứng; font 10px/16px; căn phải header; không hardcode từ ảnh.

16. [M4/M5 chưa đánh giá] hiện tại: ghi “Chưa đánh giá” là đúng dữ liệu máy kiểm → phải thành: giữ nguyên trạng thái, chỉ đồng bộ bố cục; không tạo thanh 0 hoặc điểm giả | thông số: text 10–11px, màu #596579; thanh nền #E5EAF1, không fill khi null.

17. [Ghi chú tính điểm] hiện tại: đoạn giải thích “Điểm tổng = tổng có trọng số…” nằm trong panel AI, chiếm nhiều chiều cao → phải thành: giữ thông tin cần thiết nhưng thu gọn thành chú thích nhỏ dưới điểm; không làm panel cao hơn 200px chỉ vì công thức | thông số: font 10px/16px; tối đa hai dòng tóm tắt, nội dung dài có thể xem đầy đủ bằng tooltip/chú giải có chức năng.

18. [Kiểm tra điều kiện — THIẾU] hiện tại: drawer không có panel kiểm tra điều kiện riêng, chỉ hiển thị điểm AI và nhận xét → phải thành: thêm panel “Kiểm tra điều kiện đăng ký” ngay sau AI, dùng các điều kiện thực tế của đề tài | thông số: header 38–42px; mỗi điều kiện min-height 32px; padding hàng 8px 10px; divider 1px #DDE4EF; body padding 0 10px.

19. [Nội dung kiểm tra điều kiện] hiện tại: không nhìn thấy GPA yêu cầu/thực tế, học phần bắt buộc hoặc kỹ năng thiếu → phải thành: checklist có từng tiêu chí, kết quả và giá trị so sánh; chỉ render điều kiện có dữ liệu thực | thông số: grid 20px minmax(0,1fr) auto; gap 8px; font 11px/18px; icon 14px; trạng thái đạt màu #176B60, chưa đạt màu cảnh báo.

20. [Giới thiệu bản thân — THIẾU] hiện tại: không có section “Giới thiệu bản thân” trong drawer → phải thành: panel riêng hiển thị nội dung SV khai báo, đứng dưới điều kiện | thông số: header 38–42px; body padding 10px 12px; text 12px/19px; không giới hạn chiều cao cố định, drawer body tự cuộn.

21. [Nhận xét giảng viên] hiện tại: textarea lớn có placeholder “Nhập nhận xét của giảng viên…” nằm trực tiếp dưới AI, không có panel tách rõ → phải thành: panel “Nhận xét giảng viên” sau Giới thiệu bản thân; textarea nằm trong panel và có trạng thái phù hợp | thông số: header 38–42px; textarea min-height 72px; padding 10px 12px; font 12px/19px; radius 4px; margin-top 0.

22. [Nhận xét và lưu dữ liệu] hiện tại: textarea có mô tả “Nhận xét sẽ được lưu và hiển thị cho sinh viên sau khi duyệt” → phải thành: giữ textarea nếu backend hỗ trợ nhận xét, nhưng không tự khẳng định SV nhìn thấy nhận xét nếu backend chưa có chức năng công bố nội dung này | thông số: mô tả phụ 10–11px/17px; chỉ hiện khi đúng nghiệp vụ; nếu không hỗ trợ lưu nhận xét thì bỏ textarea để tránh nút/trường giả.

23. [Footer drawer] hiện tại: hai nút Từ chối và Đồng ý nhỏ, nằm ở góc phải và không chiếm đủ chiều rộng → phải thành: footer có hai nút bằng nhau, mỗi nút chiếm 50% vùng khả dụng, như ảnh duyệt | thông số: footer min-height 72px; padding 12px 16px; gap 12px; mỗi nút flex:1; height 44px; border-radius 5px.

24. [Nút Từ chối] hiện tại: nút viền xám, chữ tối → phải thành: nút danger-outline với icon thùng rác hoặc từ chối, viền đỏ và chữ đỏ | thông số: border 1px #DC3545; color #DC3545; background #FFFFFF; icon user-x hoặc trash-2 16px; font 13px/600; không sử dụng nút xóa dữ liệu cho thao tác từ chối nếu muốn tránh hiểu nhầm.

25. [Nút Đồng ý] hiện tại: nút xanh nhỏ, nằm cạnh Từ chối ở góc phải → phải thành: primary xanh chiếm nửa footer, có icon check | thông số: background #2454B8; color #FFFFFF; icon check 16px; height 44px; font 13px/600.

26. [Backdrop khi mở drawer] hiện tại: backdrop tối che cả topbar và sidebar, khiến màn hình như đang mở một modal chặn toàn bộ → phải thành: không có backdrop trên desktop; drawer hoạt động dạng panel phân tích song song với danh sách | thông số: backdrop:false tại desktop; không làm tối main; không che topbar bằng overlay.

27. [Độ rộng vùng danh sách] hiện tại: vùng nội dung bên trái bị drawer che, phần bảng không đọc được cột trạng thái/thao tác → phải thành: vùng danh sách nằm hoàn toàn trong phần còn lại bên trái drawer; chấp nhận cuộn ngang nội bộ bảng khi viewport hẹp | thông số: wrapper min-width:0; overflow-x:auto; không để table đẩy page rộng hơn viewport.

28. [Tiêu đề trang] hiện tại: “Sinh viên đăng ký đề tài”, phía trên có breadcrumb, phía dưới có mô tả và thông tin đề tài → phải thành: tiêu đề cùng metadata GVHD/bộ môn/Khoa như ảnh duyệt, bớt các hàng mô tả thừa | thông số: H1 24px/700, line-height 32px; metadata 12px/19px; header tổng cao khoảng 68–72px.

29. [Breadcrumb] hiện tại: “Đề tài của tôi › Kho dữ liệu và báo cáo điểm danh” chiếm một hàng trên tiêu đề → phải thành: nếu giữ breadcrumb chung, rút gọn và không đẩy nội dung xuống nhiều | thông số: font 11px/18px; margin-bottom 4px; không tạo một vùng header cao 100px.

30. [Metadata giảng viên] hiện tại: trang không có dòng GVHD/Mã GV/Bộ môn/Khoa ngay dưới tiêu đề, mà hiển thị đề tài và trạng thái → phải thành: “GVHD: [GV đăng nhập] | Bộ môn: [...] | Khoa [...]” theo dữ liệu backend | thông số: font 12px/19px; divider đứng 1px; gap 12px; không tạo mã GV giả.

31. [Thông tin đề tài đang duyệt] hiện tại: có dòng “Đề tài: … Trạng thái… Sức chứa… GPA tối thiểu…” ngay dưới page header → phải thành: chuyển thành một dòng nhãn “Đề tài: [tên đề tài]” nằm trong panel Danh sách SV ngay trước toolbar, giống ảnh duyệt; các thông tin sức chứa/GPA nếu cần xem thì đưa vào chi tiết đề tài | thông số: min-height 36px; font 13px/600; padding 8px 12px; icon/vạch nhấn #176BFF 4×18px.

32. [Period] hiện tại: dải đợt thấp, nội dung xếp một dòng và chú thích ở dưới → phải thành: Period hai vùng: trái tên/trạng thái/thời gian, phải hướng dẫn GV xử lý đăng ký | thông số: grid 55%/45%; min-height 72px; padding 10px 14px; divider dọc 1px #DDE4EF.

33. [Chỉ số Tổng hồ sơ/Chờ duyệt/Đồng ý] hiện tại: có Metric Ledger ba ô nằm giữa Period và Danh sách SV; ảnh duyệt không có Ledger ở màn 16 → phải thành: bỏ Ledger khỏi trang duyệt SV để ưu tiên bảng, chuyển tổng số bản ghi vào header hoặc toolbar nếu cần | thông số: loại bỏ khối cao khoảng 100px; không tạo ba KPI card riêng; số hồ sơ có thể hiển thị font 11px ở bên phải header bảng.

34. [Vị trí bảng SV] hiện tại: bảng bắt đầu rất thấp vì có breadcrumb, mô tả đề tài, Period và Ledger → phải thành: bảng ngay dưới Period, header bảng và toolbar hiển thị cao hơn trong viewport để thấy tối thiểu 5 SV | thông số: section gap 10–12px; page header 68px; Period 72px; panel header 42px; toolbar 52px; table header 32px.

35. [Panel Danh sách SV] hiện tại: “Danh sách sinh viên đăng ký” có mô tả dài trong header, toolbar cách khá xa header → phải thành: panel compact, header chỉ “Danh sách sinh viên đăng ký”, bên dưới là tên đề tài và toolbar | thông số: header 42px; label đề tài min-height 36px; toolbar min-height 52px; body padding 10px 12px; vạch accent #176BFF.

36. [Toolbar tìm kiếm] hiện tại: search và select lọc trạng thái tương đối hẹp, mặc định “Tất cả trạng thái” → phải thành: search “Tìm theo tên sinh viên, MSSV…” chiếm phần lớn chiều ngang, filter “Chờ duyệt” ở phải | thông số: grid 65% 35%; gap 12px; input/select height 36px; icon search 16px; font 12px.

37. [Mặc định trạng thái] hiện tại: “Tất cả trạng thái” khiến nhiều SV đã xử lý trộn với SV chờ → phải thành: lọc mặc định Chờ duyệt giống ảnh duyệt, nếu backend hỗ trợ filter | thông số: query status pending; dropdown lựa chọn từ trạng thái thật; không đổi bản ghi chỉ để khớp ảnh.

38. [Bảng sinh viên] hiện tại: bảng vẫn hiển thị các cột MSSV, Sinh viên, GPA, NV, Điểm nhưng hai cột cuối bị drawer che và nội dung chữ nhỏ → phải thành: đủ bảy cột MSSV / Sinh viên / GPA / NV / Điểm AI / Trạng thái / Thao tác | thông số: tỷ lệ 14% / 19% / 9% / 9% / 12% / 19% / 18%; header 34px; mỗi hàng 44–48px; font 11–12px.

39. [Sinh viên đang chọn] hiện tại: không có dấu hiệu rõ hàng nào đang được xem trong drawer (do overlay tối) → phải thành: hàng tương ứng với drawer có nền xanh nhạt dễ nhận biết | thông số: selected background #EAF2FF; border-left 3px #176BFF; không đổi trạng thái dữ liệu.

40. [Cột GPA] hiện tại: GPA hiển thị đúng nhưng nhỏ, ít khoảng cách → phải thành: căn giữa, hiển thị 2 chữ số thập phân, không ngắt dòng | thông số: font 12px/500, tabular-nums; width 9%.

41. [Cột NV] hiện tại: badge viền xám nhỏ → phải thành: chip NV1/NV2/NV3 theo hệ màu của ảnh duyệt | thông số: 36×22px; NV1 nền #E4F0FF chữ #2454B8; NV2 nền #E5F5EC chữ #176B60; NV3 nền trung tính.

42. [Cột Điểm AI] hiện tại: điểm có một chữ số thập phân nhưng màu trung tính → phải thành: điểm nổi bật bằng xanh AI | thông số: font 12px/600; color #176B60; text-align:center; nếu chưa có điểm, ghi “Chưa đánh giá” hoặc trạng thái sơ bộ đúng backend.

43. [Cột Trạng thái] hiện tại: khi drawer mở, trạng thái bị che; các badge khó nhận biết → phải thành: hiển thị đầy đủ Chờ duyệt/Đồng ý/Từ chối ngay trong bảng | thông số: badge height 22px; font 10–11px/600; nền cam nhạt cho pending, xanh nhạt cho approved, đỏ nhạt cho rejected.

44. [Cột Thao tác] hiện tại: bị drawer che khuất, người dùng không thao tác được ở các hàng phía sau → phải thành: nút “Phân tích” hiển thị trọn vẹn tại mọi hàng ngay cả khi drawer mở | thông số: btn secondary min-width 68px, height 28–30px; padding ngang 10px; font 11px/600.

45. [Khoảng trắng dưới bảng] hiện tại: bảng dài phía sau nhưng phần đọc được ít, drawer che → phải thành: vùng bảng có min-height đủ rộng và danh sách cuộn bình thường, không dùng bảng kéo toàn trang dưới overlay | thông số: panel min-height 540px ở desktop; bảng 20 dòng/trang; overflow-x:auto nếu vùng còn lại nhỏ.

46. [Panel và viền] hiện tại: drawer và trang có nhiều vùng trắng, header mờ, khoảng cách lớn → phải thành: panel trắng, header xanh nhạt, vạch accent trái rõ, nhất quán ảnh duyệt | thông số: panel background #FFFFFF; header #EAF4FF; accent #176BFF; border #DDE4EF; radius 5–6px.

47. [Typography] hiện tại: cỡ chữ trong bảng, drawer và form nhận xét có nhiều mức khác nhau → phải thành: thống nhất Be Vietnam Pro, tập trung vào tên SV, điểm, điều kiện và nút quyết định | thông số: Page H1 24px/700; drawer title 16px/700; tên SV 20px/700; panel title 13–14px/600; body 12px/19px; caption 11px/17px.

48. [Dữ liệu demo] hiện tại: GV Nguyễn Minh Bình, SV Nguyễn Thu Hùng, đề tài Kho dữ liệu và báo cáo điểm danh, điểm 67,0 khác ảnh duyệt → phải thành: giữ nguyên dữ liệu thật; không đổi thành GV Phạm Hồng Quân, SV Nguyễn Minh Đức hay điểm 82,4 chỉ để giống ảnh | thông số: query theo lecturer/topic/preference thực; không hardcode tên, điểm hoặc trạng thái.

49. [Shell] hiện tại: sidebar và topbar đã được chủ chấp nhận → phải thành: giữ shell V3.6; logo chữ M, không dùng chữ phụ “Open Path”, không có chuông; không đổi width sidebar/topbar | thông số: chỉ chỉnh nội dung màn 16 và hành vi drawer.

ASSET THÀNH PHẦN CÒN THIẾU

1. Lucide x — Nút đóng drawer, icon 18px, button 36×36px.

2. Lucide search — Ô tìm kiếm sinh viên/MSSV, icon 16px.

3. Lucide circle-check — Điều kiện đạt và trạng thái được đồng ý, icon 14–16px, màu #176B60.

4. Lucide circle-minus — Điều kiện chưa xác định/chưa rõ, icon 14px, màu #596579; có thể dùng circle-help nếu bộ Lucide hiện tại chưa có circle-minus.

5. Lucide triangle-alert — Điều kiện bắt buộc chưa đạt, icon 14px, màu cảnh báo.

6. Lucide check — Nút Đồng ý, icon 16px.

7. Lucide user-x — Nút Từ chối, icon 16px.

8. Lucide chevron-down — Select trạng thái, icon 14px.

9. Lucide info — Ghi chú điểm sơ bộ hoặc hướng dẫn xét duyệt, icon 14px.

10. Evidence bars M1–M5 — Dùng .at-evidence hiện có, không cần render SVG mới.

11. Chip NV1/NV2/NV3 — Dùng .at-chip, không cần asset riêng.

12. Badge Chờ duyệt/Đồng ý/Từ chối — Dùng .at-badge, không cần SVG riêng.

Không thiếu minh họa hình học hoặc ảnh trang trí. Cần thay đổi cấu trúc drawer và bảng, không cần tạo asset hình ảnh mới.

TRẠNG THÁI / HÀNH VI

1. Mở drawer: Click “Phân tích” ở một SV → mở drawer 440px bên phải, không backdrop tối, bảng vẫn đọc được. Ở desktop đủ rộng, main thu lại để không bị che cột; không mở modal căn giữa.

2. Đóng drawer: Nút X, phím Escape; sau khi đóng, trả focus về nút Phân tích đã mở, giữ bộ lọc, trang và vị trí cuộn bảng.

3. Dữ liệu theo SV: Drawer nạp đúng cặp preference_id/student_id/topic_id; không dùng dữ liệu của SV trước đó khi đổi hàng. Backend kiểm quyền GV cho từng request.

4. Điểm AI: Hiển thị M1–M5 đúng dữ liệu; M4/M5 null là “Chưa đánh giá”; tổng điểm sơ bộ có nhãn đúng. M5 gọi là “Đánh giá LLM”.

5. Kiểm tra điều kiện: Hiển thị GPA, kỹ năng bắt buộc, học phần tiên quyết và các quy tắc áp dụng thực tế; kết quả từ backend, không tự suy ra tất cả đều đạt vì AI score cao.

6. Giới thiệu SV: Render nguyên văn giới thiệu đã lưu; nếu trống hiện “Sinh viên chưa cung cấp giới thiệu”.

7. Nhận xét GV: Nếu backend hỗ trợ, textarea cho nhập/sửa theo quyền; nội dung không được tự công bố cho SV nếu chưa có chức năng. Nếu không hỗ trợ thì không render field giả.

8. Đồng ý: Chỉ bật khi quyền, trạng thái đăng ký và điều kiện nghiệp vụ cho phép; POST có CSRF, khóa bấm lặp, cập nhật trạng thái sau phản hồi server.

9. Từ chối: Mở modal nhập lý do 5–500 ký tự, validate cả client/server; không đổi trạng thái nếu chưa xác nhận hoặc POST lỗi.

10. Đã xử lý: Với đăng ký đã Đồng ý/Từ chối, drawer chỉ xem hoặc cho sửa theo đúng backend; không hiển thị hai nút xử lý khi không còn quyền.

11. Tìm kiếm/lọc: Search theo tên/MSSV, default Chờ duyệt; server-side và phân trang 20 dòng, giữ query khi mở/đóng drawer.

12. Màn mobile dưới 768px: Drawer thành full-screen 100dvh; ẩn Bottom Navigation; footer 72px + safe area; body cuộn riêng, không để bàn phím ảo che nút.

13. Tương tác mobile: Danh sách SV chuyển thành .at-list; mỗi item có tên, MSSV, GPA, điểm, NV, trạng thái và nút Phân tích; touch target ≥44px.

14. Accessibility: Drawer có role dialog và nhãn, focus quản lý hợp lý, tất cả nút có accessible name, các thanh điểm có số, trạng thái không chỉ dựa vào màu; đáp ứng WCAG AA.

15. QA: Nghiệm thu 1440×900 với drawer mở phải đồng thời nhìn thấy các cột MSSV, Sinh viên, GPA, NV, Điểm, Trạng thái, Phân tích; không backdrop, không tràn ngang. Kiểm thử 390px Light/Dark, null M4/M5, điều kiện thiếu, từ chối có lý do, phân quyền và lỗi request.