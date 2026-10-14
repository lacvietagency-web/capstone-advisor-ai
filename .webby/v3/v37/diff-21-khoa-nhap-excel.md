KHÁC BIỆT

1. [Bố cục tổng thể] hiện tại: các khối Hướng dẫn, Tải mẫu, Tải lên, Kết quả kiểm tra xếp đúng thứ tự nhưng chiều cao lớn, khoảng trắng nhiều, chưa có khối Xác nhận nhập → phải thành: bố cục compact như ảnh duyệt, gồm hàng 1 Hướng dẫn + Tải mẫu, hàng 2 Tải lên, hàng 3 Kết quả kiểm tra, hàng 4 Xác nhận nhập | thông số: grid 12 cột; hàng 1 chia 8/12 + 4/12; các hàng sau 12/12; gap 12px; padding trang 16px; panel trắng #FFFFFF, viền #DDE4EF, bo góc 6px.

2. [Tiêu đề trang] hiện tại: “Nhập dữ liệu từ Excel”, bên dưới là mô tả và nút “Tải tệp mẫu (.xlsx)” ở góc phải → phải thành: tiêu đề “Nhập Excel” và mô tả ngắn như ảnh duyệt; chuyển chức năng tải mẫu vào panel Tải mẫu để tránh lặp | thông số: H1 24px/700, line-height 32px; mô tả 12px/19px; header cao khoảng 60–68px.

3. [Hướng dẫn nhập] hiện tại: các bước trình bày dạng bảng hai cột “Bước 1 / nội dung”, kèm dòng Định dạng ở cuối → phải thành: danh sách bốn bước đánh số tròn 1–4, nội dung ngắn gọn; vùng bên phải hiển thị định dạng được hỗ trợ | thông số: bốn hàng cao 26–30px; số thứ tự trong vòng tròn 20×20px, nền #EAF2FF, chữ #2454B8; nội dung 11–12px/18px; padding panel 12px.

4. [Định dạng hỗ trợ] hiện tại: thông tin “Microsoft Excel (.xlsx), dung lượng tối đa 5 MB” đặt thành hàng thứ năm trong phần Hướng dẫn → phải thành: nhóm thông tin bên phải của Hướng dẫn gồm tiêu đề “Định dạng tệp được hỗ trợ”, chip XLSX/CSV nếu backend thật sự hỗ trợ, và giới hạn dung lượng | thông số: trong panel Hướng dẫn chia 70%/30%; divider dọc 1px #DDE4EF; chip cao 22px; font 11px. Không quảng cáo CSV hoặc 10 MB nếu backend chỉ hỗ trợ XLSX và 5 MB.

5. [Panel Tải mẫu] hiện tại: chỉ có một nút “Tải tệp mẫu (.xlsx)” và đoạn mô tả cấu trúc bốn sheet → phải thành: nhóm nút tải mẫu theo từng loại dữ liệu như ảnh duyệt, nếu có đủ tệp mẫu thật | thông số: tối đa ba nút “Tải mẫu sinh viên”, “Tải mẫu giảng viên”, “Tải mẫu đề tài”; lưới hai cột; nút cao 32px; gap 8px; icon download 14px. Nếu backend chỉ có mẫu tổng hợp bốn sheet, giữ một nút tải mẫu thật, không tạo ba nút giả.

6. [Khu vực Tải lên] hiện tại: ô chọn tệp HTML mặc định “Choose File / No file chosen”, không đồng bộ với giao diện tiếng Việt → phải thành: vùng kéo thả tệp có viền nét đứt, icon tải lên, hướng dẫn “Kéo thả tệp Excel vào đây hoặc chọn tệp”, bên cạnh là thông tin tệp đã chọn và nút kiểm tra | thông số: panel body grid 7/12 + 5/12; dropzone min-height 96px; border 1px dashed #B7C5D8; radius 6px; icon cloud-upload hoặc upload 28px; chữ 12px/19px.

7. [Tệp đã chọn] hiện tại: chưa có vùng hiển thị tên, kích thước và nút loại bỏ tệp rõ ràng → phải thành: khối thông tin tệp bên phải dropzone như ảnh duyệt | thông số: tên tệp 12px/600, kích thước 11px/17px; icon file-spreadsheet 18px; nút bỏ tệp x 16px; chiều cao vùng thông tin tối thiểu 40px.

8. [Nút Tải lên & kiểm tra] hiện tại: nút nằm góc phải dưới form, tách xa vùng chọn tệp → phải thành: đặt ngay bên phải nút Chọn tệp trong khu vực thao tác tải lên | thông số: hai nút trên một hàng, gap 8px; secondary “Chọn tệp” và primary “Tải lên & kiểm tra”; cao 34px; font 12px/600.

9. [Panel Kết quả kiểm tra] hiện tại: mới thấy tiêu đề và mô tả, chưa có nội dung vì chưa chọn tệp → phải thành: sau khi kiểm tra hợp lệ, hiển thị dải thống kê và bảng lỗi giống ảnh duyệt | thông số: dải thống kê ba cột Tổng số dòng / Hợp lệ / Lỗi; mỗi ô cao 48px; số 20px/700; gap 6px; bên dưới là bảng lỗi.

10. [Bảng lỗi kiểm tra] hiện tại: không hiển thị trong trạng thái chưa tải tệp → phải thành: khi có lỗi thực, bảng gồm Dòng / Loại dữ liệu / Mức độ / Lỗi / Gợi ý sửa | thông số: độ rộng cột 8% / 16% / 12% / 34% / 30%; header 30px; hàng 30–34px; font 11px; bảng phân trang nếu lỗi nhiều, không tải toàn bộ hàng nghìn lỗi vào DOM.

11. [Phân biệt lỗi và cảnh báo] hiện tại: chưa có minh họa dữ liệu sau kiểm tra → phải thành: kết quả hiển thị badge Lỗi/Cảnh báo, thông điệp và hướng dẫn sửa cụ thể theo validation backend | thông số: badge Lỗi nền #FCE8EB, chữ #B42335; Cảnh báo nền #FFF1D8, chữ #975600; cao 20px; không tô đỏ toàn bộ hàng.

12. [Khối Xác nhận nhập — THIẾU] hiện tại: không có khu vực Xác nhận nhập ở cuối trang → phải thành: panel “Xác nhận nhập” dưới Kết quả kiểm tra, có ghi chú về dữ liệu hợp lệ, nút Hủy và Xác nhận nhập như ảnh duyệt | thông số: min-height 60px; padding 10px 12px; nút cao 34px; gap 8px; căn phải. Chỉ render hoặc kích hoạt khi backend thật sự có cơ chế kiểm tra trước và xác nhận ghi dữ liệu.

13. [Chiều cao các panel] hiện tại: Hướng dẫn và Tải mẫu cao, Tải lên chiếm khoảng 175px, các khối còn lại bị đẩy xuống → phải thành: nén mật độ để các bước nhập và kiểm tra hiện rõ hơn trong viewport | thông số: hàng Hướng dẫn/Tải mẫu khoảng 140–165px; Tải lên 120–145px; header panel 38–42px; gap 12px.

14. [Màu và hình thức] hiện tại: biểu mẫu dùng input trình duyệt mặc định, header panel rất nhạt, thiếu điểm nhấn trực quan của vùng tải tệp → phải thành: sử dụng đồng bộ ATLAS V3.5 với header xanh nhạt, vạch nhấn xanh và các nút viền xanh | thông số: canvas #F2F5FB; header #EAF4FF; accent #176BFF; primary #2454B8; AI/success #176B60; radius 6px; không dùng gradient.

15. [Thông số giới hạn tệp] hiện tại: web ghi chỉ hỗ trợ XLSX, tối đa 5 MB; ảnh duyệt ghi XLSX/CSV, tối đa 10 MB → phải thành: giữ đúng giới hạn backend hiện tại, không sửa thành 10 MB hay thêm CSV chỉ để giống ảnh; nếu chủ muốn hỗ trợ thêm thì Claude phải nâng cấp validator, parser và kiểm thử trước | thông số: cùng một giới hạn cho client/server; thông báo tiếng Việt thống nhất.

16. [Dữ liệu kiểm tra] hiện tại: chưa tải tệp nên không có kết quả, ảnh duyệt có 124 dòng, 118 hợp lệ, 6 lỗi → phải thành: giữ trạng thái rỗng trước tải tệp; chỉ hiển thị số liệu và bảng lỗi thật sau khi kiểm tra, không hardcode số liệu từ ảnh duyệt | thông số: các chỉ số lấy từ response backend; tổng lỗi phân biệt số dòng lỗi với số lỗi chi tiết nếu một dòng có nhiều lỗi.

17. [Shell] hiện tại: topbar, sidebar và avatar đã được chủ chấp nhận → phải thành: giữ nguyên shell V3.6; logo chữ M, không có “Open Path”, không có chuông; không đổi chiều rộng sidebar hay chiều cao topbar | thông số: chỉ sửa nội dung màn 21.

ASSET THÀNH PHẦN CÒN THIẾU

1. Lucide upload — Icon lớn ở vùng kéo thả tệp, 28px, màu #2454B8.

2. Lucide file-spreadsheet — Icon loại tệp Excel và tệp đã chọn, 18px.

3. Lucide download — Nút tải tệp mẫu, 14px.

4. Lucide x — Xóa tệp đã chọn khỏi form, 16px.

5. Lucide info — Ghi chú định dạng và hướng dẫn xác nhận nhập, 14px.

6. Lucide triangle-alert — Trạng thái lỗi kiểm tra, 14px.

7. Lucide circle-check — Dữ liệu hợp lệ, 14px.

8. Số thứ tự bước 1–4 — Dùng HTML/CSS tạo vòng tròn 20×20px, không cần SVG mới.

9. Dropzone viền nét đứt — Dựng bằng CSS với border:1px dashed, không cần hình minh họa bitmap.

Không có hoạ tiết hay minh họa đặc biệt cần GPT render thành ảnh. Các asset còn thiếu đều triển khai được bằng Lucide và CSS, không nên tạo ảnh riêng vì sẽ làm giảm tính đồng bộ và khả năng tương tác.

TRẠNG THÁI / HÀNH VI

1. Tải mẫu: Giữ nút tải tệp mẫu XLSX có chức năng thật. Chỉ thêm mẫu riêng từng loại dữ liệu nếu server cung cấp các tệp tương ứng.

2. Chọn tệp: Hỗ trợ chọn XLSX; kéo thả chỉ bật khi đã có xử lý drag-and-drop thật. Hiển thị tên, kích thước, nút xóa lựa chọn.

3. Kiểm tra định dạng: Kiểm tra phần mở rộng, MIME khi phù hợp và kích thước; backend vẫn phải xác thực nội dung tệp, không tin tên file.

4. Giới hạn dung lượng: Giữ tối đa 5 MB theo web hiện tại, trừ khi backend đã được nâng cấp. Nếu vượt giới hạn, hiển thị lỗi tiếng Việt và không gửi request kiểm tra.

5. Tải lên & kiểm tra: Nút disabled khi chưa chọn tệp; khi gửi hiển thị “Đang kiểm tra…”, khóa bấm lặp; POST kèm CSRF và hiển thị kết quả từ server.

6. Kết quả hợp lệ: Nếu server trả số dòng kiểm tra, số hợp lệ và số lỗi, hiển thị Metric Ledger ba cột và bảng vấn đề; không tạo dữ liệu giả trước khi upload.

7. Bảng lỗi: Hiển thị số dòng, loại dữ liệu, mô tả và cách sửa khi có; không tự suy luận thông báo lỗi nếu backend không trả chi tiết.

8. Xác nhận nhập: Chỉ có nút “Xác nhận nhập” nếu backend hỗ trợ luồng kiểm tra trước rồi mới commit. Nếu upload hiện tại ghi trực tiếp vào CSDL, không dựng nút xác nhận giả; cần Claude bổ sung cơ chế staging/preview trước khi áp dụng giao diện ảnh duyệt.

9. Chống nhập trùng: Server xử lý ID trùng, liên kết GV–đề tài, MSSV, khóa ngoại và chính sách cập nhật/ghi đè; giao diện không tự quyết định bỏ qua lỗi.

10. Hủy nhập: Nếu có dữ liệu staging, nút Hủy xóa phiên kiểm tra chưa commit theo nghiệp vụ. Nếu không có staging, chỉ cho xóa tệp đã chọn hoặc quay lại, không gọi là hủy dữ liệu đã nhập.

11. Trạng thái rỗng: Khi chưa upload, panel Kết quả kiểm tra hiển thị “Chưa có tệp nào được kiểm tra”; không hiển thị bảng giả 124/118/6.

12. Trạng thái lỗi mạng: Nếu upload thất bại, giữ tệp đã chọn khi trình duyệt cho phép, hiện lỗi rõ ràng và cho thử lại; không báo thành công khi chưa có response.

13. Mobile dưới 768px: Thứ tự Header → Hướng dẫn → Tải mẫu → Tải lên → Kết quả kiểm tra → Xác nhận nhập; tất cả panel 12/12; bảng lỗi chuyển danh sách; nút chính rộng 100%, touch target ≥44px.

14. Dark mode: Dùng token tối của V3.6, đảm bảo dropzone, input file, table và badge đủ tương phản; không dùng nền trắng cố định trong theme tối.

15. QA: Kiểm thử tại 1440×900 và 390px, Light/Dark; tệp hợp lệ, sai định dạng, vượt 5 MB, thiếu cột, trùng mã, lỗi liên kết, không có dữ liệu và lỗi mạng. Xác nhận đúng số dòng hợp lệ/lỗi, không nhập dữ liệu hai lần và không có lỗi JavaScript/CSRF/HTTP 500.