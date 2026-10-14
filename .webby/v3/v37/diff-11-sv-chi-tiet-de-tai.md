KHÁC BIỆT

1. [Bố cục tổng thể] hiện tại: trang có nhiều khoảng trống, các panel cao và nội dung kéo dài xuống dưới; phần Kỹ năng yêu cầu chưa hiển thị trọn vẹn trong viewport → phải thành: giao diện thông tin học thuật mật độ cao giống ảnh duyệt, với dải thông tin đề tài toàn chiều rộng, bên dưới là hai cột nội dung độc lập | thông số: grid 12 cột, trái 7/12, phải 5/12; gap ngang 12px; gap panel dọc 10–12px; padding canvas 16px; panel radius 5–6px.

2. [Thứ tự các khối] hiện tại: Header → Thông tin đề tài → Mô tả/Điểm AI → Kỹ năng/Lý do gợi ý → các khối còn lại nằm sâu phía dưới → phải thành: Header → Dải thông tin đề tài → hai cột: trái Mô tả đề tài → Kỹ năng yêu cầu → Điều kiện tiên quyết; phải Phân tích mức độ phù hợp → Lý do gợi ý → Kiểm tra điều kiện → Phiên bản đánh giá | thông số: hai cột at-col-7/at-col-5, mỗi cột xếp panel dọc gap 10px; không dùng các hàng grid bắt hai cột phải chờ chiều cao của nhau.

3. [Page Header] hiện tại: tên đề tài làm tiêu đề chính, dòng MSSV/ngành/GPA bên dưới, breadcrumb phía trên → phải thành: giữ tên đề tài là H1 nhưng tổ chức compact đúng ảnh duyệt, có breadcrumb, metadata và nút đăng ký bên phải cùng hàng tiêu đề | thông số: H1 22–24px/700, line-height 30px; metadata 12px/19px; breadcrumb 11px/18px; khoảng cách breadcrumb–H1 4px; header min-height 78px.

4. [Nút hành động header] hiện tại: có hai nút “Danh sách đề tài” và “Đăng ký nguyện vọng” cạnh nhau → phải thành: chỉ giữ nút primary “Đăng ký nguyện vọng” bên phải; bỏ nút “Danh sách đề tài” vì đã có breadcrumb và menu Đề tài | thông số: primary cao 36px, padding ngang 16px, font 12px/600; icon file-text 15px; điều hướng quay lại sử dụng breadcrumb hoạt động thật.

5. [Thanh thông tin đề tài] hiện tại: một panel có header “Thông tin đề tài”, bên dưới là các cột dữ liệu với nhiều dòng và badge “Đang mở” → phải thành: dải thông tin ngang không có header panel riêng, nằm trực tiếp dưới Page Header, tương tự ảnh duyệt | thông số: min-height 72px; background #FFFFFF; border 1px #DDE4EF; radius 5px; padding 10px 12px.

6. [Cấu trúc dải thông tin] hiện tại: chỉ có GVHD, Lĩnh vực, Độ khó, Sức chứa, Số người đăng ký NV1 → phải thành: năm nhóm trực quan gồm GVHD, Lĩnh vực, Độ khó, Chỉ tiêu, Thẻ từ khóa; chỉ hiển thị dữ liệu có thật, không tự sinh thẻ từ khóa | thông số: grid 30% 18% 12% 16% 24%; mỗi nhóm có thể có icon 16–18px; divider đứng 1px #DDE4EF; padding ngang mỗi nhóm 12px.

7. [Thông tin GVHD] hiện tại: tên GVHD hiển thị “Trần Thị Yến”, bộ môn nằm dưới trong ô văn bản đơn giản → phải thành: nhóm GVHD có icon người trong vòng nền xanh nhạt, tên và bộ môn rõ ràng như ảnh duyệt | thông số: icon user-round 18px; nền icon #EAF2FF; khung icon 36×36px; tên 13px/600, bộ môn 11px/17px; gap 10px.

8. [Lĩnh vực] hiện tại: “Phần mềm doanh nghiệp” là văn bản ngắn trong nhóm dữ liệu → phải thành: hiển thị icon lĩnh vực, label và tên giá trị theo cùng cấu trúc dải thông tin | thông số: icon layers-3 16px; label 11px/500, giá trị 12px/600; không ép tên lĩnh vực dài vào một dòng gây tràn.

9. [Độ khó] hiện tại: chữ “Dễ” là giá trị văn bản thông thường → phải thành: badge mức độ khó có màu nhẹ và được đặt ngay dưới label | thông số: badge height 22px; font 11px/600; radius 4px; mức Dễ dùng nền xanh nhạt, mức Trung bình dùng nền trung tính, mức Khó dùng màu cảnh báo có tương phản đạt chuẩn.

10. [Chỉ tiêu] hiện tại: “1 sinh viên (còn 1 chỗ)” và 5 NV1 hiển thị tách riêng → phải thành: nhóm “Chỉ tiêu” thể hiện sức chứa và số còn chỗ theo định dạng đã nhận / tối đa, như ảnh duyệt | thông số: số chính 13px/600; chú thích 11px/17px; ví dụ từ dữ liệu thực “0/1 — còn 1 chỗ”; nếu có số lượt NV1 thì giữ trong tooltip/chi tiết bổ sung, không thay chỉ tiêu bằng lượt đăng ký.

11. [Thẻ từ khóa] hiện tại: không có nhóm từ khóa trong dải thông tin → phải thành: nhóm chip lĩnh vực/công nghệ khi backend có dữ liệu; nếu không có, bỏ nhóm và phân phối lại chiều rộng các nhóm còn lại | thông số: chip min-height 20px, padding 3px 7px, gap 4px; font 10–11px; nền #EAF2FF, chữ #2454B8; tối đa 3 chip trong dải compact.

12. [Panel Mô tả đề tài] hiện tại: header có tiêu đề, mô tả phụ và mã đề tài ở góc phải; nội dung phân thành Mô tả, Mục tiêu, Công nghệ đề xuất với nhiều khoảng trống → phải thành: panel gọn giống ảnh duyệt, header chỉ “Mô tả đề tài”; body bắt đầu trực tiếp bằng mô tả thực tế, dòng Công nghệ đề xuất cuối phần | thông số: header 38–42px; body padding 12px 14px; font 12px/19px; gap đoạn 8px; min-height theo nội dung, không cố định 250px.

13. [Mã đề tài] hiện tại: “Mã: ĐT-2026-026” nằm trên header Mô tả → phải thành: bỏ khỏi header để giữ sự gọn gàng; nếu cần kiểm tra, hiển thị trong tooltip hoặc chi tiết bổ sung không chiếm thêm hàng | thông số: mã đề tài font 11px, màu #596579; không tự tạo ID khác với CSDL.

14. [Mục tiêu đề tài] hiện tại: một mục dài nằm giữa Mô tả và Công nghệ, khiến panel tăng chiều cao → phải thành: giữ nguyên dữ liệu thật nhưng trình bày compact hơn; không xóa trường Mục tiêu nếu đó là nội dung giảng viên đã khai báo | thông số: tiêu đề mục 12px/600, margin-top 8px; nội dung 12px/19px; không tạo panel con.

15. [Công nghệ đề xuất] hiện tại: trình bày thành một đoạn riêng khá dài → phải thành: dòng nhãn đậm và giá trị ngay sau nhãn khi nội dung ngắn, như ảnh duyệt | thông số: nhãn 11px/600; giá trị 11–12px/18px; margin-top 8px; nội dung dài được xuống dòng đầy đủ.

16. [Panel Kỹ năng yêu cầu] hiện tại: nằm thấp dưới Mô tả, chỉ thấy một phần bảng trong viewport → phải thành: panel bảng compact nằm ngay sau Mô tả, hiển thị được nhiều dòng kỹ năng | thông số: header 38–42px; bảng header 28px; hàng min-height 30–34px; font body 11–12px; padding ô 6px 8px.

17. [Thứ tự cột kỹ năng] hiện tại: # / Kỹ năng / Mức yêu cầu / Trọng số / Bắt buộc đã gần đúng → phải thành: giữ chính xác năm cột theo thứ tự ảnh duyệt, căn số liệu và badge nhất quán | thông số: độ rộng 6% / 39% / 20% / 17% / 18%; kỹ năng căn trái, mức/trọng số căn giữa; cột Bắt buộc dùng badge “Có/Không”.

18. [Dòng giải thích kỹ năng] hiện tại: ghi “3 kỹ năng được thiết lập cho đề tài này” trong header, tạo thêm dòng phụ → phải thành: ưu tiên bảng, bỏ dòng mô tả phụ không cần thiết để giảm chiều cao | thông số: chỉ header 42px; nếu cần số kỹ năng, hiển thị 3 kỹ năng cỡ 11px ở mép phải header.

19. [Trọng số kỹ năng] hiện tại: trọng số biểu diễn bằng phần trăm, ảnh duyệt là các giá trị 0,25 / 0,20 / 0,15 → phải thành: trình bày thống nhất một định dạng và phân biệt với trọng số AHP của M1–M5; để khớp ảnh, ưu tiên số thập phân hai chữ số | thông số: 0,25, 0,20...; font 11px/500, tabular-nums; giá trị tính từ backend, không đổi trọng số thật.

20. [Panel Điều kiện tiên quyết] hiện tại: nằm dưới phần Kỹ năng và không thấy trong viewport → phải thành: panel bảng ngay dưới Kỹ năng, hiển thị GPA và học phần tiên quyết như ảnh duyệt | thông số: header 42px; body padding 8px 12px; bảng có header 28px, mỗi hàng min-height 32px.

21. [Bảng điều kiện tiên quyết] hiện tại: dữ liệu điều kiện nằm rải rác trong khối mô tả hoặc kiểm tra AI → phải thành: bảng có bốn cột # / Điều kiện / Yêu cầu / Trạng thái của bạn | thông số: độ rộng 6% / 44% / 22% / 28%; chữ 11–12px; icon circle-check 14px khi đạt; trường hợp chưa đạt phải có giá trị yêu cầu và thực tế.

22. [Panel Phân tích mức độ phù hợp] hiện tại: header “Mức độ phù hợp với hồ sơ của bạn”, bên dưới điểm lớn và năm thanh AI xếp dọc, thêm đoạn giải thích điểm sơ bộ khá dài → phải thành: panel phân tích compact, điểm lớn bên trái, năm thanh M1–M5 ở bên phải như ảnh duyệt | thông số: panel cột phải 5/12; body grid 30% 70%; gap 12px; padding 12px; min-height khoảng 170–185px khi đủ dữ liệu.

23. [Tên panel AI] hiện tại: “Mức độ phù hợp với hồ sơ của bạn” → phải thành: “Phân tích mức độ phù hợp” | thông số: header 42px; tiêu đề 14px/600; vạch nhấn xanh 4×20px.

24. [Điểm tổng AI] hiện tại: 79,6/100 cỡ tương đối nhỏ, bên dưới ghi “Điểm sơ bộ M1–M4” → phải thành: điểm tổng lớn, là trọng tâm panel | thông số: số 40px/700, màu #176B60; /100 14px; caption 11px/17px; vùng điểm width khoảng 155px trên desktop. Nếu điểm sơ bộ, caption phải ghi đúng “Điểm sơ bộ M1–M4”.

25. [Thanh M1–M5] hiện tại: mỗi hàng kèm trọng số ngay trong nhãn, thanh màu xanh dương, các hàng giãn rộng → phải thành: năm hàng compact, nhãn M1–M5 ở trái, thanh xanh AI ở giữa, điểm ở phải; trọng số chuyển thành một cột riêng nếu có đủ không gian | thông số: mỗi hàng 22px; nhãn 11px; bar height 7px; track #E5EAF1; fill #176B60; điểm 11px/600; gap hàng 3px.

26. [Trọng số AHP] hiện tại: M1 25%, M2 20%, M3 15%, M4 20%, M5 20% đặt ngay cạnh tên mô hình → phải thành: nhóm cột “Trọng số (AHP)” ở phải như ảnh duyệt, hoặc hiển thị đủ trong footer nếu màn hẹp | thông số: nhãn 10–11px; số 0,25 / 0,20 / 0,15 / 0,20 / 0,20; cột weight 40px; không hardcode nếu backend lưu phiên bản khác.

27. [Màu thanh AI] hiện tại: progress M1–M3 màu xanh dương #2454B8 → phải thành: màu xanh lục AI riêng, không trùng màu nút CTA | thông số: fill #176B60, track #E5EAF1; radius 3px; height 7px.

28. [M4 và M5 chưa đánh giá] hiện tại: hai hàng hiện “Chưa đánh giá” thay vì thanh số → phải thành: giữ đúng trạng thái này, không tạo điểm giả để khớp ảnh duyệt; chỉ chỉnh hình học hàng và nhãn M5 đầy đủ | thông số: M4 “Ngữ nghĩa”, M5 “Đánh giá LLM”; “Chưa đánh giá” font 11px, màu #596579; track để trống, không fill 0%.

29. [Lời giải thích điểm sơ bộ] hiện tại: có đoạn dài giải thích công thức tính lại điểm khi thiếu M4/M5 trong panel AI → phải thành: ghi chú compact không quá hai dòng, có liên kết/chi tiết nếu backend có cơ chế giải thích | thông số: font 10–11px/17px; padding-top 8px; border-top 1px #DDE4EF; không xóa thông tin quan trọng về điểm sơ bộ.

30. [Lý do gợi ý] hiện tại: panel “Lý do gợi ý” ở dưới khối AI, nội dung chủ yếu là note dài trong vùng xanh → phải thành: danh sách tối đa ba luận điểm đánh số như ảnh duyệt, không phải một hộp văn bản dài duy nhất | thông số: header 42px; item min-height 28px; số thứ tự hình tròn 18px, nền #176BFF, chữ trắng; nội dung 11px/18px; gap 7px.

31. [Nguồn lý do AI] hiện tại: lý do dựa trên dữ liệu thực hoặc fallback → phải thành: giữ nguyên nội dung từ backend, chỉ chuyển thành tối đa ba luận điểm nếu dữ liệu có cấu trúc rõ; không tự sáng tác ba nguyên nhân | thông số: nếu chỉ có một đoạn, hiển thị một đoạn trong .at-note, không tự tách sai ý để đủ ba dòng.

32. [Kiểm tra điều kiện] hiện tại: không nằm trực tiếp ngay dưới phần AI trong viewport → phải thành: panel “Kiểm tra điều kiện” đứng ngay sau Lý do gợi ý ở cột phải | thông số: header 42px; body padding 8px 12px; mỗi điều kiện min-height 30px; gap 0; divider giữa các hàng 1px.

33. [Bố cục checklist điều kiện] hiện tại: một số điều kiện hiện trong các section dữ liệu khác nhau → phải thành: danh sách tập trung, có icon loại điều kiện bên trái, tên ở giữa, kết quả căn phải | thông số: grid 20px minmax(0,1fr) 100px; gap 8px; icon 14px; font 11px/18px; kết quả 11px/600.

34. [Bốn nhóm điều kiện] hiện tại: đủ GPA, kỹ năng, học phần và chỉ tiêu đang được biểu diễn chưa nhất quán → phải thành: kiểm tra GPA, kỹ năng bắt buộc, lĩnh vực quan tâm nếu có ràng buộc, học phần tiên quyết và chỉ tiêu theo dữ liệu thật; chỉ gộp thành bốn hàng nếu backend cho phép tổng hợp chính xác | thông số: kết quả có “Đạt”, “Phù hợp”, “Còn X/Y” hoặc “Cần... hiện có...”; không bỏ điều kiện cứng để khớp số dòng ảnh.

35. [Thông tin phiên bản AI] hiện tại: chưa thấy footer nhỏ như ảnh duyệt, hoặc nằm sâu phía dưới → phải thành: dải footer chứa weights_version và model_version ở cuối cột phải, ngay sau Kiểm tra điều kiện | thông số: min-height 32px; background #F5F8FE; border 1px #DDE4EF; radius 4px; padding 7px 10px; font 10px/16px; icon settings-2 và database 13px.

36. [Khoảng cách panel] hiện tại: panel có padding lớn, header kèm mô tả phụ nên cao → phải thành: toàn bộ panel tuân thủ mật độ compact như ảnh duyệt | thông số: panel header 38–42px; body padding 10–14px; gap giữa panel 10px; border #DDE4EF; radius 5–6px.

37. [Nền section] hiện tại: header panel có sắc xanh xám rất nhẹ nhưng chưa đồng bộ hoàn toàn → phải thành: nền header xanh nhạt, vạch xanh trái rõ, cùng một hệ với ảnh duyệt | thông số: header background #EAF4FF; accent #176BFF, width 4px, height 20px; panel background #FFFFFF; canvas #F2F5FB.

38. [Mật độ chữ] hiện tại: label có cỡ nhỏ, nhiều chú thích và khoảng trắng gây phân tán → phải thành: chữ gọn nhưng rõ thứ bậc, ưu tiên dữ liệu đề tài/điểm/điều kiện | thông số: H1 22–24px/700; tiêu đề panel 13–14px/600; body 12px/19px; nhãn bảng 11px/17px; font Be Vietnam Pro.

39. [Nội dung khác ảnh] hiện tại: đề tài “Phần mềm quản lý bãi đỗ xe cho doanh nghiệp”, điểm 79,6, GVHD Trần Thị Yến khác ảnh duyệt → phải thành: giữ nguyên dữ liệu demo thật, không đổi sang đề tài “Ứng dụng di động quản lý sự kiện” hoặc sửa điểm thành 78,4 chỉ để khớp ảnh | thông số: toàn bộ dữ liệu từ backend; không hardcode tên, số liệu, mô hình hay mô tả.

40. [Shell] hiện tại: topbar và sidebar đã được chủ chấp nhận → phải thành: giữ nguyên shell V3.6 đang chạy, không chỉnh width/sidebar/topbar chỉ vì ảnh duyệt có tỷ lệ khác; đảm bảo logo chữ M, không phụ đề “Open Path” và bỏ chuông nếu còn | thông số: áp dụng shell đã khóa, chỉ chỉnh nội dung trang 11.

ASSET THÀNH PHẦN CÒN THIẾU

1. Lucide user-round — Nhóm GVHD trong dải thông tin, 18px, đặt trong ô nền xanh nhạt 36×36px.

2. Lucide layers-3 — Lĩnh vực đề tài, 16px, màu #596579.

3. Lucide gauge — Độ khó, 16px; đi cùng badge mức độ.

4. Lucide users — Chỉ tiêu sinh viên, 16px.

5. Lucide tag — Từ khóa/nhãn công nghệ, 16px, chỉ khi backend có dữ liệu từ khóa.

6. Lucide circle-check — Các điều kiện đạt, 14–16px màu #176B60.

7. Lucide triangle-alert — Điều kiện thiếu hoặc chưa đáp ứng, 14–16px màu cảnh báo.

8. Lucide info — Giải thích AI và điểm sơ bộ, 14px màu #2454B8.

9. Lucide settings-2 — Phiên bản trọng số AHP, 13px.

10. Lucide database — Phiên bản mô hình đánh giá, 13px.

11. Lucide file-text — Nút Đăng ký nguyện vọng, 15px.

12. Số thứ tự luận điểm AI — Vòng tròn CSS 18×18px, không cần tạo SVG riêng.

13. Chip từ khóa — HTML/CSS, không cần render icon hay hình nền riêng.

Không thiếu asset minh họa đặc biệt. Màn này cần tái cấu trúc bố cục, bảng, thanh AI và checklist; không cần tạo ảnh trang trí mới.

TRẠNG THÁI / HÀNH VI

1. Đăng ký nguyện vọng: Nút primary mở luồng chọn NV hợp lệ cho đề tài hiện tại; không đăng ký âm thầm. Chỉ hiện khi đợt mở và backend cho phép.

2. Điều kiện bắt buộc: Backend quyết định khả năng đăng ký dựa trên GPA, kỹ năng, học phần, chỉ tiêu và các ràng buộc hiện có. Điểm AI cao không được vượt điều kiện cứng.

3. Dữ liệu AI: Điểm tổng, M1–M5 và trọng số lấy từ recommendation thực. M4/M5 chưa đánh giá giữ null, nhãn “Chưa đánh giá”, không vẽ thanh giả 0%.

4. Điểm sơ bộ: Khi chưa đủ mô hình, hiển thị rõ “Điểm sơ bộ M1–M4” hoặc nhãn phạm vi điểm chính xác theo backend. Không gắn “Điểm phù hợp AI đầy đủ” nếu chưa tính đủ.

5. Lý do gợi ý: Hiển thị nội dung có thật. Nếu backend có danh sách luận điểm, render tối đa ba ý nổi bật; nếu chỉ có một đoạn, giữ đoạn văn, không tạo lý do giả.

6. Điều kiện tiên quyết: Bảng dùng dữ liệu thật; yêu cầu và kết quả của SV phải đối chiếu đúng. Điều kiện không áp dụng không được hiển thị như đã đạt giả.

7. Chỉ tiêu: Hiển thị capacity và số còn chỗ từ backend, không lấy số lượng NV1 làm số sinh viên đã nhận. Nếu hết chỉ tiêu, hành động đăng ký phải phản ánh đúng quy tắc nghiệp vụ.

8. Phiên bản đánh giá: Chỉ hiện weights_version, model_version khi dữ liệu có; không điền tên phiên bản mẫu từ ảnh duyệt.

9. Đợt đóng/đã công bố: Trang chuyển chỉ xem. Người dùng vẫn đọc đề tài, M1–M5, lý do và điều kiện; không hiển thị nút đăng ký trái phép.

10. Responsive dưới 768px: Thứ tự Header → Dải thông tin đề tài → Phân tích AI → Lý do AI → Kiểm tra điều kiện → Mô tả → Kỹ năng → Tiên quyết → Bottom Navigation. Các panel một cột; bảng chuyển danh sách, không có cuộn ngang toàn trang.

11. Accessibility: Các thanh điểm có giá trị số và label, không phụ thuộc vào màu; badge điều kiện có chữ; nút đạt touch target ≥44px trên mobile; tương phản WCAG AA.

12. Nghiệm thu: Screenshot 1440×900 phải thấy header, dải thông tin, panel Mô tả, Kỹ năng, Phân tích AI, Lý do và phần Kiểm tra điều kiện trong viewport đầu khi nội dung ngắn; kiểm tra 390px, Light/Dark, đủ/chưa đủ điều kiện, điểm đầy đủ/sơ bộ và lỗi backend.