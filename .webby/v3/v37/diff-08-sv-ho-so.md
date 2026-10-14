KHÁC BIỆT

1. [Bố cục tổng thể] hiện tại: trang dùng vùng nội dung tương đối hẹp, các khối kéo dài theo chiều dọc; khu vực Kỹ năng bị đẩy xuống dưới khung nhìn 900px → phải thành: giao diện hồ sơ hai cột như ảnh duyệt, thông tin và biểu mẫu bên trái, tiến độ hoàn thiện bên phải; nhìn thấy ít nhất 4 nhóm chính gồm Thông tin SV, Giới thiệu, Kỹ năng, Lĩnh vực | thông số: grid 12 cột, trái 8/12, phải 4/12; gap 16px; padding nội dung 16px; khoảng cách panel 12px.

2. [Chiều rộng vùng nội dung] hiện tại: nhiều khoảng trống bên trái bị dùng cho shell và vùng nội dung bắt đầu quá xa → phải thành: tận dụng toàn bộ phần canvas sau sidebar, các panel nằm sát hàng và phủ hết chiều rộng khả dụng | thông số: sidebar giữ nguyên phiên bản chủ đã chấp nhận; page content width 100% phần còn lại; max-width 1600px; không thêm container max-width 960px.

3. [Thứ tự khối] hiện tại: Thông tin SV → Giới thiệu → Kỹ năng, trong khi panel mức độ hoàn thiện đặt bên phải và lĩnh vực nằm quá sâu → phải thành: cột trái lần lượt Thông tin SV → Giới thiệu bản thân → Kỹ năng → Lĩnh vực quan tâm; cột phải Mức độ hoàn thiện hồ sơ bắt đầu ngang với Thông tin SV | thông số: dùng hai column độc lập; không để chiều cao panel phải tạo khoảng trống giữa các panel trái.

4. [Page Header] hiện tại: tiêu đề “Hồ sơ năng lực”, có breadcrumb và nút “Về trang chủ” ở góc phải → phải thành: “Hồ sơ năng lực sinh viên”, bên dưới là dòng MSSV, Ngành, GPA rồi một dòng mô tả mục đích | thông số: H1 24px/700, line-height 32px; metadata 13px/20px; mô tả 12px/19px; margin-bottom 12px; bỏ nút “Về trang chủ” khỏi header vì đã có điều hướng Tổng quan. Breadcrumb có thể giữ theo shell chung nhưng phải tối đa 24px cao, không đẩy form xuống thêm một hàng lớn.

5. [Thông tin sinh viên] hiện tại: toàn bộ thông tin là văn bản nhãn–giá trị, không có ô để SV sửa email hoặc điện thoại → phải thành: form hai cột, trong đó họ tên, MSSV, ngành, GPA là readonly; Email và Số điện thoại là input có thể sửa | thông số: panel .at-panel, header 42px; form grid 2 cột, gap ngang 16px, gap dọc 8px; padding 12px 16px; input 34px cao, font 13px; trường readonly nền #EEF1F6, viền #DDE4EF; trường editable nền trắng, viền #B7C5D8.

6. [Trường thừa trong Thông tin SV] hiện tại: chưa có Lớp và GV cố vấn, nhưng bố cục hiện tại chỉ có 4 dữ liệu học vụ và một cụm điểm học phần liên quan → phải thành: sáu trường theo đúng quyết định: Họ và tên, MSSV, Ngành, GPA, Email, Số điện thoại; không tạo trường Lớp hoặc GV cố vấn | thông số: bố trí ba hàng × hai cột; hàng 1 Họ tên/GPA, hàng 2 MSSV/Email, hàng 3 Ngành/Số điện thoại; mỗi hàng min-height 34px; gap 8px.

7. [Thông tin học phần liên quan] hiện tại: hiển thị chuỗi mã học phần và điểm trong phần Thông tin SV → phải thành: bỏ chuỗi này khỏi panel thông tin cá nhân để khớp ảnh duyệt; dữ liệu học lực vẫn giữ trong backend và hiển thị ở nơi phân tích M2 phù hợp | thông số: không thêm block học phần vào panel 6 trường; không xóa dữ liệu học thuật.

8. [Header Thông tin SV] hiện tại: có badge “Đã đồng bộ” phía phải → phải thành: header gọn, chỉ nhãn “Thông tin sinh viên”, trạng thái đồng bộ nếu cần chuyển xuống dòng chú thích nhỏ riêng, không chiếm vị trí tiêu đề | thông số: header 42px, padding ngang 16px; vạch xanh 4×20px; tiêu đề 15px/600.

9. [Mật độ panel Thông tin SV] hiện tại: khoảng trắng lớn và nội dung mỗi hàng quá giãn → phải thành: sáu trường bố trí chặt nhưng vẫn đủ dễ đọc, tương tự ảnh duyệt | thông số: padding 12px 16px; row-gap 8px; label 12px/500; input 34px; tổng chiều cao panel mục tiêu khoảng 180–195px.

10. [Giới thiệu bản thân] hiện tại: textarea lớn, nội dung ít, mô tả phụ phía trên làm panel cao → phải thành: textarea gọn, nằm ngay dưới header; nếu có giới hạn ký tự backend thì hiện bộ đếm góc dưới phải | thông số: panel header 42px; textarea min-height 104px, padding 10px 12px; font 13px/20px; panel padding 12px 16px; không hardcode giới hạn 500 ký tự nếu backend không có.

11. [Giới thiệu — nhãn phụ] hiện tại: có dòng “Nội dung giới thiệu” đứng riêng trước textarea và câu mô tả dài trong header → phải thành: header chỉ “Giới thiệu bản thân”, textarea nằm trực tiếp dưới header; mô tả trợ giúp chỉ giữ nếu cần và không chiếm thêm chiều cao đáng kể | thông số: nhãn phụ 12px/18px, margin-bottom tối đa 6px.

12. [Kỹ năng chuyên môn] hiện tại: khu vực chỉ mới xuất hiện phần header ở đáy khung nhìn, chưa thấy dữ liệu kỹ năng → phải thành: bảng chỉnh sửa kỹ năng dạng hàng ngang, hiển thị nhiều kỹ năng ngay trong viewport đầu | thông số: panel header 42px; padding 12px 16px; tối thiểu 5 hàng tham chiếu nếu CSDL có đủ; mỗi hàng 36px cao, gap dọc 4px.

13. [Bố cục từng kỹ năng] hiện tại: dự kiến dùng form chiếm chiều cao lớn → phải thành: mỗi hàng gồm select kỹ năng trái 28%, thang mức độ 1–5 ở giữa 65%, nút xóa phải 7% | thông số: grid 28% 65% 7%; gap 8px; mỗi radio target ≥32px trong hàng desktop, click label cũng chọn được; toàn hàng min-height 36px.

14. [Thang mức độ 1–5] hiện tại: không nhìn thấy các mức đánh giá trong viewport → phải thành: năm lựa chọn ngang có radio và nhãn số/mức như ảnh duyệt: 1 Cơ bản, 2 Biết làm, 3 Khá, 4 Tốt, 5 Thành thạo | thông số: mỗi lựa chọn chiếm 20% vùng mức độ; số 12px/600, mô tả 10–11px/15px; radio 14–16px; mức được chọn màu #2454B8. Nếu nhãn mức backend đã khóa khác, không tự đổi ý nghĩa điểm.

15. [Thêm/xóa kỹ năng] hiện tại: khu vực tương tác chưa xuất hiện rõ trên màn 900px → phải thành: nút “+ Thêm kỹ năng” bên dưới các hàng và icon trash-2 cuối từng hàng | thông số: nút thêm 30px cao, font 12px; icon xóa 16px; button hit-area tối thiểu 32×32px desktop, 44×44px mobile.

16. [Lĩnh vực quan tâm] hiện tại: không nhìn thấy trong khung ảnh thật → phải thành: panel ngay sau kỹ năng, chứa các checkbox lĩnh vực dạng lưới | thông số: header 42px; checkbox items 2–4 cột tùy chiều rộng; gap 8px; chip có nền #F1F6FC, viền #DDE4EF, cao tối thiểu 30px; tối đa ba lĩnh vực theo quy tắc dự án.

17. [Lựa chọn lĩnh vực] hiện tại: thiếu trạng thái được chọn rõ trong phần nhìn thấy → phải thành: checkbox xanh bên trái tên lĩnh vực; các lĩnh vực đã chọn nền xanh nhạt và viền rõ | thông số: checkbox 16px; font 12px/18px; chip padding 6px 10px; selected background #E7F0FF, border #8BB2EF.

18. [Panel hoàn thiện hồ sơ] hiện tại: hiển thị “100%” và danh sách hoàn thành bên phải nhưng panel gọn hơn về cấu trúc, thiếu nhịp thị giác ảnh duyệt → phải thành: panel tiến độ rộng đủ 4 cột grid, thể hiện tỷ lệ lớn, thanh tiến độ và checklist trạng thái | thông số: header 42px; padding 16px; phần trăm 36px/700, màu #176B60; progress height 8px, radius 4px; margin-top 12px; checklist gap 10px.

19. [Danh sách hoàn thiện] hiện tại: “Giới thiệu bản thân”, “Kỹ năng và mức độ”, “Lĩnh vực quan tâm”, “Điểm các môn đã học” và trạng thái hoàn thành → phải thành: các bước rõ theo những thành phần thực sự dùng để xác định hồ sơ đủ điều kiện: Thông tin cá nhân, Giới thiệu, Kỹ năng, Lĩnh vực quan tâm; kết quả học tập có thể hiển thị thêm chỉ khi backend tính vào completeness | thông số: mỗi hàng min-height 32px; icon circle-check 16px; label 12px/18px; badge 11px/600.

20. [Logic mức độ hoàn thiện] hiện tại: 100%, trong khi ảnh duyệt 82% → không bắt buộc đổi thành 82%, vì dữ liệu khác là hợp lệ; phải thành: phần trăm tính đúng từ tiêu chí hiện có, không hardcode 82% hoặc 100% | thông số: giá trị động, thang 0–100%, thanh fill theo phần trăm.

21. [Ghi chú trong panel tiến độ] hiện tại: khối nhắc nhở khá dài và đặt gần đáy panel → phải thành: note nhỏ gọn, một khối thông tin về độ chính xác gợi ý AI như ảnh duyệt | thông số: padding 10px 12px; background #EFF5FC; border-radius 4px; font 12px/19px; icon info 16px.

22. [Thanh lưu cuối trang] hiện tại: không nhìn thấy thanh hành động trong khung 900px → phải thành: save bar nằm cố định ở đáy vùng nội dung như ảnh duyệt, gồm cảnh báo thay đổi chưa lưu bên trái và nút hành động bên phải | thông số: height 56px desktop; background #FFFFFF; border-top 1px #DDE4EF; padding 8px 16px; position:sticky; bottom:0; z-index 20; vùng main có padding-bottom tối thiểu 64px.

23. [Nút lưu] hiện tại: không thấy nút Lưu nháp/Lưu hồ sơ trong viewport → phải thành: một nút primary “Lưu hồ sơ”, và nút secondary “Lưu nháp” chỉ khi backend hỗ trợ hai hành động độc lập; nếu không, chỉ hiển thị Lưu hồ sơ | thông số: height 36px desktop; padding 0 18px; gap 8px; primary #2454B8, chữ trắng 13px/600.

24. [Cảnh báo thay đổi chưa lưu] hiện tại: chưa thấy cơ chế nhận biết thay đổi → phải thành: khi form dirty, hiển thị thông báo “Thay đổi chưa được lưu” và icon cảnh báo; khi sạch, không hiện cảnh báo | thông số: font 12px/500, màu #9A5B15, icon triangle-alert 16px; căn trái thanh lưu.

25. [Màu các phần] hiện tại: tiêu đề khối, header và thanh tiến độ dùng cùng hệ xanh nhưng các panel có độ phân tách chưa đủ giống ảnh duyệt → phải thành: section header xanh nhạt, vạch accent xanh rõ, nền panel trắng | thông số: panel #FFFFFF, header #EAF4FF, accent #176BFF, border #DDE4EF; radius 6px; không gradient.

26. [Khoảng cách giữa panel] hiện tại: các khối Thông tin, Giới thiệu, Kỹ năng có margin khá lớn → phải thành: các panel xếp sát, thống nhất mật độ của ảnh duyệt để thấy Lĩnh vực trong màn đầu | thông số: vertical gap 12px; panel body padding 12px 16px; không tự thêm margin-bottom:24px.

27. [Mật độ chữ] hiện tại: phần thông tin học vụ và chú giải có nhiều chữ nhỏ, các label chưa đồng nhất → phải thành: thống nhất Be Vietnam Pro, chữ dữ liệu tối thiểu 12px, nhãn 12px/500, tiêu đề panel 15px/600 | thông số: H1 24px/700, body 13px/21px, caption 12px/18px, weight 400/500/600/700.

28. [Viền input] hiện tại: dữ liệu học vụ là văn bản nên chưa phân biệt trực quan readonly và editable → phải thành: input readonly nền xám xanh có border nhẹ; input Email/SĐT trắng và trạng thái focus rõ | thông số: readonly background #EEF1F6, color #344563; editable border #B7C5D8, focus outline 2px #2454B8, offset 2px; disabled không được dùng thay readonly nếu cần copy giá trị.

29. [Thông báo trạng thái] hiện tại: badge “Đã đồng bộ” có thể khiến người dùng hiểu thông tin đã được lưu dù Email/SĐT chưa sửa → phải thành: trạng thái học vụ và trạng thái lưu form tách riêng; “Dữ liệu học vụ” chỉ đọc, “Thay đổi chưa lưu” hoặc “Đã lưu” phản ánh form thật | thông số: badge trạng thái 11px/600, min-height 22px; không hiển thị success trước phản hồi backend.

30. [Chiều cao tổng thể] hiện tại: phần Kỹ năng bị đẩy xuống quá xa → phải thành: ưu tiên mật độ desktop đủ để panel Kỹ năng có tối thiểu các hàng đầu trong vùng 900px; Lĩnh vực quan tâm bắt đầu xuất hiện ở cuối khung nếu dữ liệu không quá dài | thông số: page header khoảng 72px; Thông tin SV khoảng 190px; Giới thiệu khoảng 152px; Kỹ năng 240–275px với 5 hàng; gap mỗi panel 12px. Không cắt hoặc ẩn nội dung để ép vừa chiều cao.

31. [Shell khác ảnh duyệt] hiện tại: một số menu icon và nhãn khác nhưng shell đã được chủ chấp nhận → phải thành: giữ nguyên shell hiện tại, chỉ bỏ chuông nếu còn tồn tại, dùng logo chữ M không có chữ phụ “Open Path”; không làm lại sidebar, topbar hay breakpoint | thông số: giữ token và kích thước shell V3.6 đã nghiệm thu.

ASSET THÀNH PHẦN CÒN THIẾU

Lucide trash-2 — Nút xóa từng dòng kỹ năng; icon 16px, màu đỏ trạng thái, button hit-area tối thiểu 32×32px desktop / 44×44px mobile.

Lucide plus — Nút “Thêm kỹ năng”, icon 14–16px, đặt trước nhãn.

Lucide circle-check — Checklist hoàn thiện hồ sơ, icon 16px màu #176B60.

Lucide info — Note tiến độ/giải thích AI, icon 16px màu #2454B8.

Lucide triangle-alert — Cảnh báo thay đổi chưa lưu trong save bar, icon 16px.

Lucide save — Nút Lưu hồ sơ nếu ảnh/thiết kế chung yêu cầu icon; icon 16px, không bắt buộc nếu nút chỉ chữ đã khớp.

Thang mức kỹ năng dạng radio 1–5 — Không cần asset ảnh riêng; phải xây component dùng HTML radio thật, nhãn hai dòng và trạng thái selected.

Chip checkbox lĩnh vực — Không cần SVG riêng; tạo bằng input checkbox thực, nền/viền CSS và trạng thái selected.

Không cần render minh họa mới hoặc trang trí hình học cho màn này.

TRẠNG THÁI / HÀNH VI

1. Thông tin sinh viên: Họ tên, MSSV, Ngành và GPA là readonly, SV không thể chỉnh sửa; Email và Số điện thoại được phép sửa và lưu về đúng trường dữ liệu. Backend kiểm quyền sở hữu hồ sơ, validate Email/SĐT, không cho POST thay đổi dữ liệu học vụ.

2. Điền form: Giá trị học vụ lấy từ dữ liệu chính thức; Email và SĐT lấy từ hồ sơ SV. Không thêm trường Lớp và GV cố vấn khi chưa có dữ liệu.

3. Lưu hồ sơ: Thay đổi Email, SĐT, giới thiệu, kỹ năng hoặc lĩnh vực phải được đánh dấu dirty; thanh lưu xuất hiện/hoạt động tương ứng. Submit có CSRF, validation server-side và chống bấm lặp.

4. Kỹ năng: Chọn kỹ năng từ danh mục, mức 1–5 bằng radio; thêm/xóa hàng hoạt động thật; không cho trùng kỹ năng; cập nhật formset và xử lý các hàng đánh dấu xóa đúng Django.

5. Lĩnh vực: Chọn tối đa ba lĩnh vực; nếu vượt giới hạn thì chặn và báo ngay gần nhóm checkbox, đồng thời backend kiểm tra.

6. Tiến độ hoàn thiện: Tỷ lệ phần trăm và checklist cập nhật dựa trên dữ liệu đã lưu; không tăng tiến độ chỉ vì người dùng thao tác trên form chưa submit. Nếu chưa đủ hồ sơ, mô tả rõ tiêu chí còn thiếu.

7. Tính lại gợi ý AI: Sau lưu hồ sơ, gọi đúng cơ chế đã có để cập nhật profile_version, cache và gợi ý nếu backend cho phép. Không tự tuyên bố M4/M5 đã chấm. M5 phải mang nhãn “Đánh giá LLM”.

8. Đợt đóng/khóa: Thông tin vẫn xem được; chỉ khóa những trường bị hạn chế theo trạng thái backend. Không mặc định CLOSED khiến Email/SĐT không thể sửa nếu hệ thống cho phép cập nhật thông tin liên hệ.

9. Responsive: Dưới 768px, thứ tự Thông tin SV → Mức độ hoàn thiện → Giới thiệu → Kỹ năng → Lĩnh vực. Form một cột; skill row chuyển dọc; lưu bằng Bottom Action Bar 72px + safe area và ẩn Bottom Navigation trong chế độ sửa.

10. Accessibility và QA: Nhãn liên kết đúng input, radio group có tên nhóm, keyboard thao tác được, focus rõ; thông báo lỗi ngay dưới trường; dữ liệu dài không tràn; không có lỗi JS/CSRF/HTTP 500.