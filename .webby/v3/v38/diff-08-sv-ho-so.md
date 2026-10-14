KHÁC BIỆT

1. [Bố cục tổng thể] hiện tại: cột trái chứa nhiều form dài, phần Kỹ năng chiếm gần hết chiều cao, không nhìn thấy Lĩnh vực quan tâm → phải thành: hai cột rõ ràng, bên trái gồm Thông tin sinh viên → Giới thiệu bản thân → Kỹ năng → Lĩnh vực quan tâm; bên phải là Mức độ hoàn thiện hồ sơ | thông số: grid 12 cột, trái 9/12, phải 3/12; gap 12px; padding trang 16px; khoảng cách panel 10px; nền #F2F5FB, panel #FFFFFF, bo góc 6px.

2. [Kỹ năng — NGHIÊM TRỌNG NHẤT] hiện tại: 6 dòng kỹ năng với radio và nhãn mức độ sát nhau, tạo cảm giác rối; dòng cuối chưa chọn kỹ năng vẫn hiện đủ 5 radio → phải thành: mỗi kỹ năng một hàng gọn, có select bên trái, năm mức đánh giá chia đều, nút xóa bên phải; chỉ hiển thị dòng đã có kỹ năng, thêm dòng khi người dùng bấm Thêm kỹ năng | thông số: mỗi hàng cao 36px; gap dọc 4px; select rộng 28%, cao 32px; năm mức chiếm 62%; nút xóa chiếm 6%; gap ngang 8px.

3. [Nhãn mức độ kỹ năng] hiện tại: số 1–5 và mô tả đặt quá gần nhau, nhiều nhãn bị ngắt dòng không đều → phải thành: năm lựa chọn có bố cục thống nhất, số ở trên và mô tả dưới, radio căn giữa theo từng lựa chọn | thông số: mỗi lựa chọn rộng 20% vùng đánh giá; radio 14×14px; số 12px/600; nhãn 12px/16px; căn giữa; không dùng chữ nhỏ hơn 12px.

4. [Chiều cao Kỹ năng] hiện tại: panel kéo dài tới sát thanh lưu, che mất lĩnh vực quan tâm → phải thành: giới hạn chiều cao phần hiển thị kỹ năng, khi số lượng lớn cho phép cuộn bên trong hoặc cuộn trang; tuyệt đối không bỏ bớt kỹ năng thật để khớp ảnh | thông số: header 36px; hàng kỹ năng 36px; 5 hàng chiếm khoảng 196px; trường hợp nhiều hơn 5 hàng cho phép mở rộng/thu gọn danh sách, không che thanh lưu.

5. [Nút Thêm kỹ năng — THIẾU] hiện tại: không thấy nút thêm, chỉ có một dòng select trống → phải thành: nút “+ Thêm kỹ năng” đặt ngay dưới danh sách, không sử dụng dòng kỹ năng trống làm nút thay thế | thông số: nút secondary cao 30px; rộng 125px; border #2454B8; chữ 12px/600; icon plus 14px; margin-top 6px.

6. [Lĩnh vực quan tâm — THIẾU TRONG VIEWPORT] hiện tại: phần chọn lĩnh vực bị đẩy xuống dưới → phải thành: panel Lĩnh vực quan tâm xuất hiện ngay sau Kỹ năng, có các ô tick như ảnh duyệt và dòng “Chọn tối đa 3 lĩnh vực” | thông số: grid 3 cột; gap 6px; mỗi ô cao 32px; checkbox 16×16px; nhãn 12px/500; nền được chọn #EAF2FF; border #DDE4EF; radius 4px.

7. [Thông tin sinh viên] hiện tại: sáu trường đã chia hai nhóm nhưng nhãn và ô nhập không thẳng hàng hoàn toàn, các trường chỉ đọc và chỉnh sửa gần giống nhau → phải thành: bảng thông tin 2 cột cân đối, mỗi hàng gồm nhãn + ô giá trị, phân biệt rõ trường chính thức và trường được sửa | thông số: mỗi nửa 50%; trong mỗi nửa label 32%, input 68%; 3 hàng cao 32px; gap dọc 6px; input cao 30px; nhãn 12px/500; giá trị 12px.

8. [Trường chỉ đọc] hiện tại: Họ tên, MSSV, Ngành, GPA đều là ô nền xám nhưng vẫn giống input vô hiệu hóa → phải thành: hiển thị dạng trường read-only rõ ràng, chữ dễ đọc, không cho chỉnh sửa | thông số: nền #F1F4F8; border #DDE4EF; chữ #344563; cao 30px; padding ngang 10px; không dùng trạng thái disabled gây khó đọc.

9. [Email và Số điện thoại] hiện tại: ô sửa được chưa phân biệt rõ với ô chính thức, số điện thoại đang trống → phải thành: hai input nền trắng, viền rõ, có focus khi nhập; dữ liệu trống được phép nếu backend không bắt buộc | thông số: mỗi input cao 30px; width 100% phần giá trị; border #AEBED2; focus ring 2px #2454B8; radius 4px; font 12px.

10. [Giới thiệu bản thân] hiện tại: textarea có khoảng trắng đáng kể vì nội dung ngắn, panel cao hơn cần thiết → phải thành: textarea gọn như ảnh duyệt, bộ đếm ký tự căn góc dưới phải | thông số: textarea width 100%; height 76–82px; padding 8px 10px; font 12px/18px; panel header 36px; bộ đếm 12px; margin-top 4px.

11. [Thanh mức độ hoàn thiện] hiện tại: số 100% và thanh tiến độ chiếm chiều ngang gần hết panel, các checklist hơi sát nhau → phải thành: tỷ lệ hoàn thiện lớn, thanh tiến độ bên dưới, bốn tiêu chí phân cấp rõ như ảnh duyệt | thông số: số 32px/700 màu #176B60; progress height 8px; margin-top 8px; checklist mỗi hàng 30px; icon 16px; badge cao 22px; gap 6px.

12. [Nội dung checklist] hiện tại: bốn trạng thái hoàn thành đúng nhưng nhãn và badge nhỏ, khó đọc → phải thành: căn trái nhãn, căn phải badge, chiều cao bằng nhau | thông số: nhãn 12px/18px; badge 12px/600, height 22px; gap 8px; không xuống dòng không cần thiết.

13. [Ghi chú bên phải] hiện tại: thông báo “Hoàn thiện hồ sơ để tăng độ chính xác của gợi ý AI” xuất hiện ngay cả khi hồ sơ đạt 100% → phải thành: thông báo phù hợp với tỷ lệ hoàn thiện thực, ví dụ khi 100% dùng “Hồ sơ đã đầy đủ. Bạn có thể cập nhật để cải thiện gợi ý.” | thông số: nền #EAF2FF; padding 10px; icon info 16px; chữ 12px/18px; radius 4px.

14. [Thanh lưu hồ sơ] hiện tại: chỉ có nút “Lưu hồ sơ” ở góc trái của thanh đáy, khác ảnh duyệt → phải thành: thông báo thay đổi chưa lưu bên trái, nút Lưu hồ sơ nằm góc phải; không thêm nút Lưu nháp nếu chưa có chức năng | thông số: thanh cao 48px; position sticky bottom 0; padding 8px 12px; border-top 1px #DDE4EF; nút primary cao 34px, rộng 112px; chữ 12px/600.

15. [Header và khoảng cách panel] hiện tại: các panel có chiều cao header và khoảng cách chưa thống nhất, làm trang phân mảnh → phải thành: một hệ panel đồng đều, vạch xanh nhận diện ở đầu tiêu đề, không lồng thêm khung không cần thiết | thông số: header 36px; padding body 10px 12px; gap 10px; vạch accent 4×18px màu #176BFF; panel border #DDE4EF, radius 6px.

16. [Kiểu chữ và mật độ] hiện tại: một số nhãn trường, mô tả radio và badge rất nhỏ → phải thành: toàn bộ chữ từ 12px trở lên, ưu tiên sự rõ ràng hơn việc nhồi nhiều thông tin vào một hàng | thông số: Be Vietnam Pro; H1 24px/700; panel title 14px/600; nhãn 12px/500; body 12px/18px; số thống kê 32px/700.

17. [Căn lề và độ rộng ô] hiện tại: select kỹ năng, radio, ô giá trị và các nút thiếu một hệ căn chỉnh, tạo cảm giác lệch hàng → phải thành: các thành phần cùng loại có chiều cao cố định, không thay đổi kích thước theo nội dung | thông số: input/select nhỏ 30–32px; nút nhỏ 30px; các hàng kỹ năng 36px; gap 8px; label căn giữa theo trục dọc; toàn bộ trường dùng box-sizing:border-box.

18. [Khoảng trắng] hiện tại: khu vực dưới Mức độ hoàn thiện trống nhiều trong khi Kỹ năng bên trái dày đặc → phải thành: không kéo dài panel phải để bằng cột trái; giữ chiều cao tự nhiên, ưu tiên khoảng trắng có chủ đích và khối form đọc dễ dàng | thông số: align-items:start; không dùng height:100% cho panel tiến độ; gap dọc 10px.

TRẠNG THÁI / HÀNH VI

1. Thông tin chính thức: Họ tên, MSSV, Ngành, GPA lấy từ dữ liệu đào tạo và chỉ đọc. Email, Số điện thoại có thể chỉnh sửa và lưu thật vào backend.

2. Kỹ năng: Thêm, xóa, thay đổi tên và chọn mức 1–5; lưu theo dữ liệu thực. Không hiển thị dòng kỹ năng trống khi chưa yêu cầu thêm; không tự xóa kỹ năng đã có chỉ để giảm chiều cao.

3. Giới hạn kỹ năng: Không được chọn trùng một kỹ năng hai lần; khi xóa cần cập nhật dữ liệu sau khi lưu.

4. Lĩnh vực quan tâm: Dùng checkbox, tối đa 3 lĩnh vực; khi đã chọn 3, không cho chọn thêm cho đến khi bỏ một lựa chọn. Hiển thị rõ các lựa chọn đang được lưu.

5. Giới thiệu bản thân: Cập nhật bộ đếm ký tự trực tiếp; áp dụng giới hạn 500 ký tự nếu đúng quy định backend.

6. Mức độ hoàn thiện: Tính động theo dữ liệu thực, không hardcode 100%; checklist phản ánh đúng các mục đã hoàn thành.

7. Thanh lưu: Khi có thay đổi chưa lưu, hiển thị cảnh báo; khi lưu thành công, cập nhật trạng thái và tỷ lệ hoàn thiện. Khóa nút khi đang gửi để tránh lưu lặp.

8. Dữ liệu thiếu: Email/SĐT trống hiển thị ô nhập trống; kỹ năng/lĩnh vực trống hiển thị hướng dẫn thêm/chọn, không chèn thông tin demo giả.

9. Chế độ chỉ xem: Nếu đợt đã khóa sửa hồ sơ theo nghiệp vụ, không cho chỉnh sửa nhưng vẫn hiển thị dữ liệu và lý do khóa.

10. Responsive: Dưới 768px chuyển form sang một cột; radio kỹ năng có đủ không gian; checkbox lĩnh vực chia 1–2 cột; thanh lưu cố định an toàn phía dưới, không che nội dung hoặc bàn phím.

11. Kiểm thử: Tại 1440×900 phải nhìn thấy Thông tin, Giới thiệu, Kỹ năng, Lĩnh vực quan tâm và thanh lưu khi số kỹ năng ở mức thông thường; tại 390px không tràn ngang, không cắt chữ, mọi thao tác thực hiện được.