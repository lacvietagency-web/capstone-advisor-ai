# BÁO CÁO KIỂM TOÁN GIAO DIỆN HỆ THỐNG (UI/UX AUDIT REPORT)
**Dự án:** Hệ thống AI Tư vấn & Phân công Đề tài Tốt nghiệp (Capstone Advisor AI) — Khoa CNTT, EAUT  
**Chuyên gia đánh giá:** Giám đốc Nghệ thuật (Art Director) & Trưởng nhóm Thiết kế Trải nghiệm  
**Mục tiêu:** Đánh giá thẳng thắn, giải phẫu từng khuyết tật thị giác hiện hữu trên 16 trang màn hình (Desktop 1440px & Mobile 390px), bóc trần tư duy "Bootstrap mặc định lười biếng" và thiết lập danh mục lỗi cần thanh toán triệt để.

---

## I. BẢNG ĐIỂM ĐÁNH GIÁ 16 TRANG (DESKTOP & MOBILE)

*Thang điểm 1–10:*
- **TM:** Thẩm mỹ & Bản sắc (Aesthetics & Brand Personality)
- **PK:** Phân cấp thị giác (Visual Hierarchy)
- **KT:** Khoảng trắng & Nhịp điệu (Whitespace & Visual Rhythm)
- **NQ:** Tính nhất quán hệ thống (Systemic Consistency)
- **MB:** Khả năng đáp ứng & Công thái học Mobile (Mobile Responsiveness & Ergonomics)
- **ĐTB:** Điểm trung bình trọng số trang

| STT | Mã màn hình & Tên trang | Đường dẫn (URL) | TM | PK | KT | NQ | MB | ĐTB | Đánh giá tổng quan của Art Director |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| 01 | **00-dang-nhap**<br>(Anon: Đăng nhập) | `/dang-nhap/` | 3.5 | 4.0 | 3.0 | 5.0 | 4.5 | **4.0** | Trống hoác, vô hồn, như trang đăng nhập mẫu sinh viên năm 2 nộp bài tập. |
| 02 | **01-sv-trang-chu**<br>(SV: Trang chủ) | `/` | 4.0 | 4.5 | 4.0 | 4.5 | 3.5 | **4.1** | Ô nhiễm thẻ lồng thẻ, thanh tiến trình rác dán nhãn "—", đẩy nguyện vọng xuống đáy. |
| 03 | **02-sv-ho-so**<br>(SV: Hồ sơ năng lực) | `/ho-so/` | 3.0 | 3.5 | 3.5 | 4.0 | 2.5 | **3.3** | Bảng formset kỹ năng vỡ trận; mobile kéo dài 4.000px; nút Xóa đỏ rực báo động giả. |
| 04 | **03-sv-nguyen-vong**<br>(SV: Đăng ký nguyện vọng) | `/nguyen-vong/` | 3.0 | 3.5 | 2.5 | 4.0 | 3.5 | **3.3** | Empty state chết chóc, một icon lịch cô đơn trên bãi hoang 1440px. |
| 05 | **04-sv-danh-sach-de-tai**<br>(SV: Danh mục đề tài) | `/de-tai/` | 4.5 | 4.0 | 4.0 | 4.5 | 3.5 | **4.1** | Bộ lọc cồng kềnh, badge xám xịt không phân loại, nút "Chưa đủ điều kiện" dọa dẫm người dùng. |
| 06 | **05-sv-chi-tiet-de-tai**<br>(SV: Chi tiết đề tài) | `/de-tai/121/` | 3.5 | 3.0 | 3.5 | 4.0 | 2.5 | **3.3** | Cụm 5 vòng tròn M1–M5 toàn dấu gạch "—" nhìn như lỗi kết nối dữ liệu; alert vàng đục ngầu. |
| 07 | **06-sv-ket-qua**<br>(SV: Kết quả phân công) | `/ket-qua/` | 4.0 | 4.0 | 3.0 | 4.5 | 3.5 | **3.8** | Card lồng card nghiệp dư, 70% diện tích trang desktop bị bỏ hoang. |
| 08 | **07-sv-doi-mat-khau**<br>(SV: Đổi mật khẩu) | `/doi-mat-khau/` | 3.5 | 4.0 | 3.5 | 5.0 | 4.0 | **4.0** | Hộp form tẻ nhạt, bullet yêu cầu li ti khó đọc, thiếu thước đo độ mạnh mật khẩu. |
| 09 | **08-gv-trang-chu**<br>(GV: Bảng điều khiển) | `/` | 4.0 | 4.0 | 3.5 | 4.5 | 3.5 | **3.9** | 4 thẻ KPI như 4 ô Excel thô kệch; bảng 2 dòng kéo dãn 1440px vô duyên. |
| 10 | **09-gv-de-tai**<br>(GV: Đề tài của tôi) | `/giang-vien/de-tai/` | 4.0 | 4.0 | 4.0 | 4.5 | 3.5 | **4.0** | Rừng tag xám không phân cấp, nút hành động xem đăng ký bị dìm thành outline mờ nhạt. |
| 11 | **10-gv-de-tai-sua**<br>(GV: Chỉnh sửa đề tài) | `/giang-vien/de-tai/127/sua/` | 3.0 | 3.0 | 3.0 | 3.5 | 2.5 | **3.0** | Formset kỹ năng thô lậu với checkbox Xóa vô danh; chip lĩnh vực checkbox bọc pill kỳ quặc. |
| 12 | **11-gv-de-tai-dang-ky**<br>(GV: Duyệt sinh viên) | `/giang-vien/de-tai/127/dang-ky/` | 4.0 | 3.5 | 3.5 | 4.0 | 3.0 | **3.6** | Nút Đồng ý/Từ chối xanh-đỏ Bootstrap nguyên thủy sát nhau; điểm AI chỉ là số trần trụi. |
| 13 | **12-gv-ho-so**<br>(GV: Hồ sơ giảng viên) | `/giang-vien/ho-so/` | 3.5 | 3.5 | 3.0 | 4.0 | 2.5 | **3.3** | Banner khóa chỉ tiêu to quá khổ; 8 hộp chọn lĩnh vực chiếm dụng không gian vô ích. |
| 14 | **13-khoa-trang-chu**<br>(Khoa: Bảng điều khiển) | `/` | 3.5 | 3.5 | 2.5 | 4.5 | 3.5 | **3.5** | Trang trung tâm mà nghèo nàn như bản nháp; 1 dòng bảng dữ liệu bơ vơ giữa màn hình. |
| 15 | **14-khoa-phan-cong**<br>(Khoa: Quản lý phân công) | `/khoa/phan-cong/` | 2.5 | 2.0 | 2.0 | 3.0 | 1.5 | **2.2** | **THẢM HỌA LỚN NHẤT:** 57 dòng vàng chói chang như bãi rác dữ liệu; mobile tê liệt hoàn toàn! |
| 16 | **15-khoa-thong-ke**<br>(Khoa: Báo cáo thống kê) | `/khoa/thong-ke/` | 3.5 | 3.0 | 2.5 | 3.5 | 2.0 | **2.9** | Cột đỏ 21x dọa dẫm nhức mắt; trang mobile dài 12.000px gây kiệt sức thị giác. |

**ĐIỂM TRUNG BÌNH TOÀN HỆ THỐNG: 3.48 / 10**  
*Kết luận của Art Director:* Hệ thống hiện tại hoàn toàn thất bại trong việc truyền tải tinh thần "AI phân công thông minh". Toàn bộ trải nghiệm mang nặng tính kỹ trị, thô thiển, lạm dụng các thành phần dựng sẵn của Bootstrap 5 và bỏ rơi hoàn toàn bài toán công thái học dữ liệu (data ergonomics).

---

## II. CHI TIẾT LỖI XẤU NHẤT TRÊN TỪNG TRANG (16 TRANG)

---

### TRANG 01: Anon — Đăng nhập (`/dang-nhap/`)
*Ảnh tham chiếu: `shots/d-00-anon-dang-nhap.png` (Desktop) & `shots/m-00-anon-dang-nhap.png` (Mobile)*

1. **Card form trôi nổi vô định giữa sa mạc khoảng trắng chết (Desktop - Chính giữa viewport):**  
   Một chiếc hộp chữ nhật màu trắng bo góc 14px nhỏ thó (~420px) đặt trơ trọi giữa vùng xám `#F6F8FB`. Không có bất kỳ hình ảnh thương hiệu nào của Khoa CNTT - Đại học Công nghệ Đông Á (EAUT), không có đồ họa nhận diện thuật toán AI, không có phân vùng nền (Split Screen). 80% không gian màn hình 1440px bị bỏ hoang một cách lãng phí và lười biếng.
2. **Khối Header thương hiệu nghiệp dư (Desktop & Mobile - Đỉnh card):**  
   Cụm nhãn `AI` đóng trong khung bo góc xám xanh nhạt đặt cạnh dòng chữ `Capstone Advisor AI` màu xanh tím đậm `#174EA6`. Tỷ lệ giữa icon và wordmark vụng về, không có cấu trúc typographic chặt chẽ. Dòng phụ đề "Tư vấn và phân công đồ án tốt nghiệp bằng AI" dùng font xám mờ `#5A6578` tạo cảm giác thiếu năng lượng, thiếu tính học thuật danh giá.
3. **Nút "Đăng nhập" thô kệch và thiếu phản hồi trạng thái (Desktop & Mobile - Đáy form):**  
   Nút bấm xanh đậm nguyên khối (`#174EA6`) chiếm toàn bộ bề ngang card, không có hiệu ứng vi mô, không có icon mũi tên tiến bước, không có cơ chế chuyển đổi tài khoản mẫu (Demo Switcher cho SV/GV/Khoa). Đây là nguyên nhân khiến ban giám khảo hoặc người dùng thử nghiệm phải gõ tay thông tin đăng nhập mà không hiểu rõ hệ thống có những vai trò nào.
4. **Mobile lơ lửng, chân trang dính sát mép (Mobile - Toàn màn hình):**  
   Trên màn hình 390px, card đăng nhập nằm lơ lửng ở 1/3 trên của màn hình, để lại một khoảng trống xám vô nghĩa ở đáy trước khi chạm dòng chữ "Đồ án tốt nghiệp · Khoa CNTT – EAUT". Không tạo được cảm giác vững chãi của một ứng dụng di động chuyên nghiệp.

---

### TRANG 02: Sinh viên — Trang chủ (`/`)
*Ảnh tham chiếu: `shots/d-01-sv001-trang-chu.png` (Desktop) & `shots/m-01-sv001-trang-chu.png` (Mobile)*

1. **Card lồng card và ô nhiễm dữ liệu giả "—" trong thẻ đề tài gợi ý (Desktop - Cột trái):**  
   Ở mỗi card đề tài (từ #1 đến #5), hệ thống nhồi nhét một ma trận 5 thanh tiến trình con: Kỹ năng, Học lực, Lĩnh vực, Ngữ nghĩa, Đánh giá AI. Trong đó, hai cột "Ngữ nghĩa" và "Đánh giá AI" đều hiển thị dấu gạch ngang "—". Việc phơi bày các trường dữ liệu rỗng liên tục 5 lần trên cùng một màn hình là một lỗi sơ đẳng trong thiết kế giao diện dữ liệu, làm rác mắt sinh viên và tạo cảm giác hệ thống bị lỗi backend.
2. **Hộp "Vì sao đề tài này phù hợp?" vụng về (Desktop - Đáy mỗi card đề tài):**  
   Khối giải thích dùng một dải viền xanh dương 3px bên trái, đặt trên nền xám xanh nhạt dán đè vào trong card cha. Đoạn văn bản dài dòng không được định dạng dạng bullet points, không bôi đậm các từ khóa kỹ năng (ví dụ: "Kiểm thử phần mềm", "Deep Learning"), khiến sinh viên không thể quét nhanh thông tin trong 3 giây.
3. **Thẻ điểm tổng "80/100 Phù hợp cao" màu sắc phản logic (Desktop - Góc trên phải card):**  
   Con số 80/100 và nhãn "Phù hợp cao" được đóng trong một ô vuông xanh dương nhạt. Tuy nhiên, khi nhìn xuống đề tài #3 (32/100 Cần cân nhắc) và #4 (23/100 Cần cân nhắc), màu nền của ô điểm VẪN LÀ MÀU XANH LƠ NHẠT ĐÓ! Hoàn toàn triệt tiêu phản xạ thị giác về mức độ rủi ro (đáng lẽ phải dùng màu vàng hổ phách hoặc xám dịu cho mức điểm thấp).
4. **Banner thẩm định phân công đụng độ màu sắc gay gắt (Desktop & Mobile - Dưới header):**  
   Badge xanh ngọc "Chờ công bố", icon đồng hồ cát trong vòng tròn xanh lơ `#E0F2FE`, tiêu đề xanh dương đậm `#174EA6`, và nút viền mỏng "Xem trạng thái /ket-qua/". 4 sắc độ xanh khác nhau nằm chen chúc trong một khung viền bo cong tạo nên sự xung đột bảng màu luộm thuộm.
5. **Thảm họa trật tự thị giác trên di động (Mobile - Toàn màn hình):**  
   Trên màn hình 390px, cột "Nguyện vọng của bạn" bị đẩy tụt xuống đáy cùng, nằm sau 5 card đề tài gợi ý dài dằng dặc. Sinh viên mở điện thoại lên không thể nhìn thấy trạng thái 3 nguyện vọng sống còn của mình nếu không cuộn qua hơn 3.000px chiều dọc!

---

### TRANG 03: Sinh viên — Hồ sơ năng lực (`/ho-so/`)
*Ảnh tham chiếu: `shots/d-02-sv001-ho-so.png` (Desktop) & `shots/m-02-sv001-ho-so.png` (Mobile)*

1. **Thanh tiến độ 100% lãng phí diện tích (Desktop - Đầu trang):**  
   Một thanh ngang màu xanh dương đậm đặc chạy dài 100% chiếm hẳn một khối card riêng biệt chỉ để báo một con số tĩnh "100%". Không có tính năng tương tác, không có phân rã xem 100% đó bao gồm những cấu phần nào (Ví dụ: Giới thiệu 30%, Kỹ năng 40%, Lĩnh vực 30%).
2. **Formset Kỹ năng thô ráp và dữ liệu rác hiển thị công khai (Desktop - Section 02):**  
   Cột "MỨC ĐỘ (1–5)" bị chia chẻ vụn vặt: vừa có ô nhập số (4, 3, 1), vừa có badge bên cạnh ("4 - Tốt", "1 - Mới học"). Hai hàng cuối cùng hiển thị dropdown chưa chọn `---------` và ô số ghi `1-!` với badge `Mức 1-5`. Đây là sự cẩu thả của việc render nguyên xi formset Django mà không có lớp bọc UI xử lý giao diện người dùng.
3. **Ô nhiễm nút Xóa màu đỏ báo động giả (Desktop - Cột Hành động):**  
   Cột hành động lặp đi lặp lại 8 nút viền đỏ rực chữ đỏ kèm icon thùng rác `[Xóa]`. Việc rải thảm màu đỏ nguy hiểm lên một trang nhập liệu bình thường tạo ra tâm lý căng thẳng không đáng có và biến bảng kỹ năng thành một danh sách lỗi hệ thống.
4. **Vỡ trận công thái học trên màn hình di động (Mobile - Toàn màn hình):**  
   Ở màn hình 390px, mỗi dòng kỹ năng bị phân mảnh thành một thẻ con riêng biệt với 3 tầng nút bấm và dropdown xếp chồng. Người dùng phải cuộn qua gần 4.000px màn hình chỉ để xem 8 kỹ năng. Chiều cao vùng chạm ngón tay bị xô lệch, các nút Xóa nằm lơ lửng sát mép phải rất dễ chạm nhầm khi đang cuộn trang.
5. **Đồng dạng gây nhầm lẫn giữa Mục 02 và Mục 03 (Desktop & Mobile):**  
   Phần "03 Lĩnh vực quan tâm" có cấu trúc thị giác sao chép 100% phần Kỹ năng, nhưng thang đo lại âm thầm đổi thành (1–3) thay vì (1–5). Sự thiếu nhất quán về mô hình tâm lý (mental model) này khiến sinh viên nhập nhầm mức độ ưu tiên mà không hề hay biết.

---

### TRANG 04: Sinh viên — Đăng ký nguyện vọng (`/nguyen-vong/`)
*Ảnh tham chiếu: `shots/d-03-sv001-nguyen-vong.png` (Desktop) & `shots/m-03-sv001-nguyen-vong.png` (Mobile)*

1. **Trạng thái rỗng (Empty State) tàn nhẫn và vô cảm (Desktop - Chính giữa viewport):**  
   Một chiếc icon lịch màu xám tro gạch chéo đặt đơn độc trong card trắng khổng lồ. Dòng tiêu đề "Hiện chưa có đợt đăng ký nào đang mở" như một cánh cửa sắt đóng sập vào mặt sinh viên. Không có mốc thời gian đếm ngược đến đợt mở tiếp theo, không có danh sách lịch trình dự kiến, không có liên kết xem các đề tài đã lưu.
2. **Nút "Về trang chủ" nhỏ thó và lệch phân cấp (Desktop & Mobile - Trong card):**  
   Nút điều hướng chính dùng kiểu viền xám mảnh chữ xanh nhạt (`btn-outline`), kích thước bé hạt tiêu, nằm lọt thỏm giữa khoảng trắng mênh mông, thiếu hoàn toàn sức nặng thị giác của một Call-to-Action định hướng người dùng.
3. **Liên kết chân trang lệch trục thô thiển (Desktop - Dưới card):**  
   Dòng liên kết `← Xem danh sách đề tài để tìm kiếm và tra cứu chi tiết` nằm trơ trọi sát lề trái màn hình, trong khi card thông báo bên trên lại căn giữa trang. Sự đứt gãy về trục gióng (alignment axis) này tố cáo bố cục chắp vá, thiếu lưới thiết kế cơ sở.
4. **Chênh lệch tỷ lệ khung nhìn trên Mobile (Mobile - Màn hình 390px):**  
   Trên điện thoại, card rỗng bị ép ngắn cũn cỡn ở nửa trên màn hình, dòng liên kết chân trang bị ngắt dòng luộm thuộm, tạo cảm giác một trang web đang bảo trì dở dang hơn là một hệ thống chính quy của trường đại học.

---

### TRANG 05: Sinh viên — Danh sách đề tài (`/de-tai/`)
*Ảnh tham chiếu: `shots/d-04-sv001-danh-sach-de-tai.png` (Desktop) & `shots/m-04-sv001-danh-sach-de-tai.png` (Mobile)*

1. **Hộp bộ lọc xơ cứng kiểu form hành chính (Desktop - Đầu trang):**  
   4 trường nhập liệu và chọn lựa đóng trong một card viền xám phẳng lì. Các ô select chiếm diện tích quá lớn nhưng nội dung bên trong chỉ là các dòng mặc định `-- Tất cả lĩnh vực --`. Nút "Lọc đề tài" màu xanh navy đặc và nút "Xóa bộ lọc" màu xám nằm dính sát nhau thiếu nhịp thở; dòng text "Tìm thấy 50 đề tài" bị dồn về góc phải bên dưới một cách tạm bợ.
2. **Rừng badge xám đồng dạng gây mù thông tin (Desktop & Mobile - Đầu mỗi card đề tài):**  
   Mỗi đề tài trưng ra 3 badge nằm ngang: `Đang mở` (xanh lá), `Khó` (xám), `Trí tuệ nhân tạo` (xám). Việc dùng cùng một kiểu dáng bo góc và nền xám cho cả "Độ khó" lẫn "Chuyên ngành" làm mất khả năng phân loại bằng mắt thường. Sinh viên phải đọc từng chữ thay vì nhận diện được qua màu sắc và icon đặc trưng.
3. **Nút cảnh báo "Chưa đủ điều kiện" mang tính trừng phạt (Desktop - Góc phải card):**  
   Hệ thống dùng một nút màu hồng nhạt viền đỏ, chữ đỏ kèm icon chấm tròn đỏ và ổ khóa `[● 🔒 Chưa đủ điều kiện]` to ngang ngửa nút "Chi tiết". Thiết kế này tạo cảm giác sinh viên đang phạm lỗi nghiêm trọng hoặc bị cấm cửa, thay vì một thông báo trạng thái hướng dẫn mang tính hỗ trợ.
4. **Phân trang cổ lỗ sỹ của Bootstrap 3 (Desktop & Mobile - Cuối trang):**  
   Cụm phân trang với các ô vuông viền xanh dương `« Trang trước` `1` `2` `3` `4` `Trang sau »` trông như bê nguyên xi từ giao diện web năm 2012. Không hiển thị tổng số trang, không hiển thị số bản ghi trên mỗi trang, hoàn toàn lạc lõng với thẩm mỹ hiện đại.
5. **Cơn ác mộng cuộn trang trên di động (Mobile - Toàn màn hình):**  
   Trên mobile 390px, mỗi card đề tài dài tới gần 500px do các nút "Chi tiết" và "Chưa đủ điều kiện" bị bẻ thành 2 hàng nút full-width khổng lồ. Danh sách 10 đề tài trên trang biến thành một dải cuộn vô tận dài hơn 5.000px, triệt tiêu hoàn toàn khả năng so sánh lướt giữa các đề tài.

---

### TRANG 06: Sinh viên — Chi tiết đề tài (`/de-tai/121/`)
*Ảnh tham chiếu: `shots/d-05-sv001-danh-sach-de-tai_121.png` (Desktop) & `shots/m-05-sv001-danh-sach-de-tai_121.png` (Mobile)*

1. **Thảm họa 5 vòng tròn M1–M5 toàn dấu gạch ngang (Desktop - Khối trung tâm):**  
   Cụm 5 hình tròn viền xanh lơ với mũi tên điều hướng ở giữa mô phỏng một quy trình 5 bước: M1 Kỹ năng, M2 Học lực, M3 Lĩnh vực, M4 Ngữ nghĩa, M5 Hỗ trợ AI. Nhưng bên trong cả 5 vòng tròn đều hiển thị con số chết `— / 100`! Thiết kế này không chỉ làm xấu giao diện mà còn gây hoang mang tột độ cho sinh viên vì tưởng hệ thống chấm điểm AI bị sập.
2. **Khối cảnh báo vàng đục và nút đỏ chói lọi (Desktop - Dưới tiêu đề):**  
   Dải thông báo màu vàng nhạt `#FEF3C7` chiếm trọn chiều ngang, bên phải cắm một chiếc nút nền hồng cam chữ đỏ `[? Vì sao chưa đủ điều kiện?]`. Hai gam màu cảnh báo cấp 1 (Vàng) và cấp 2 (Đỏ) đặt cạnh nhau tạo nên một mớ hỗn độn về tín hiệu màu sắc (color screaming).
3. **Bảng kỹ năng lai căng giữa tiến trình và text (Desktop - Nửa dưới trang):**  
   Bảng "Kỹ năng yêu cầu" cố gắng nhét các thanh progress bar màu xanh dương vào cột "Mức yêu cầu" (Mức 3/5, Mức 2/5), đứng cạnh badge "Bắt buộc" màu hồng nhạt và "Tùy chọn" màu xám. Sự chênh lệch về độ dày nét và phong cách thị giác giữa các cột khiến bảng dữ liệu trông lem nhem, thiếu quy chuẩn.
4. **Cột thông số đề tài bên phải bị cô lập và nghèo nàn (Desktop - Sidebar phải):**  
   Card "Thông số đề tài" bên phải chỉ chứa 5 dòng chữ ngắn ngủn với các icon người, bookmark, mũ tốt nghiệp màu xanh lơ chói chang. Chiều cao card chỉ bằng 1/3 cột nội dung bên trái, để lại một khoảng trống to lớn bên dưới sidebar làm mất cân bằng bố cục 2 cột.
5. **Cụm vòng tròn M1–M5 vỡ vụn trên Mobile (Mobile - Khối trung tâm):**  
   Trên màn hình 390px, 5 vòng tròn bị bẻ thành 3 hàng lộn xộn (2 trên, 2 giữa, 1 dưới), các mũi tên liên kết biến mất hoàn toàn. Cụm này ngốn đứt 2 màn hình cuộn chỉ để hiển thị 5 dấu gạch ngang, tạo nên trải nghiệm người dùng tệ hại nhất trên thiết bị di động.

---

### TRANG 07: Sinh viên — Kết quả phân công (`/ket-qua/`)
*Ảnh tham chiếu: `shots/d-06-sv001-ket-qua.png` (Desktop) & `shots/m-06-sv001-ket-qua.png` (Mobile)*

1. **Card lồng trong card thô kệch (Desktop - Khung nội dung chính):**  
   Toàn bộ trang chỉ có một khung viền lớn màu xanh nhạt. Bên trong khung đó, bên phải lại lồng thêm một card con nền trắng viền xám mang tên "QUY TRÌNH PHÂN CÔNG". Sự lồng ghép hộp trong hộp này thể hiện rõ sự bế tắc trong tư duy bố cục không gian của lập trình viên khi không biết dùng khoảng trắng để phân tách nội dung.
2. **Icon đồng hồ cát và badge xanh lơ đụng độ (Desktop & Mobile - Cột trái):**  
   Biểu tượng đồng hồ cát to đùng màu xanh ngọc đặt trong đĩa tròn xanh lơ nhạt, đứng dưới một badge "Đang thẩm định" màu xanh cyan gắt gỏng. Bảng màu này hoàn toàn không ăn nhập với sắc xanh navy chủ đạo của thanh điều hướng phía trên.
3. **Không gian chết chiếm 70% trang Desktop (Desktop - Nửa dưới màn hình):**  
   Sau khối thông báo thẩm định, toàn bộ nửa dưới của màn hình 1440px là một bãi đất trống mênh mông, chỉ có duy nhất một nút quay lại nhỏ bé dạt sang lề trái. Hệ thống hoàn toàn không cung cấp thông tin phụ trợ nào: danh sách giảng viên hội đồng, hướng dẫn chuẩn bị báo cáo, hoặc kênh liên hệ hỗ trợ khi cần khiếu nại.
4. **Mobile co cụm nghẹt thở (Mobile - Khung chính):**  
   Trên điện thoại, khối quy trình phân công bị ép tụt xuống dưới khối thông báo, tạo thành 2 tầng hộp viền xám dính chặt vào nhau. Các bước 1, 2, 3 với icon check xanh lá và mũi tên xanh dương trông vụn vặt và mất cân đối với độ rộng màn hình.

---

### TRANG 08: Sinh viên — Đổi mật khẩu (`/doi-mat-khau/`)
*Ảnh tham chiếu: `shots/d-07-sv001-doi-mat-khau.png` (Desktop) & `shots/m-07-sv001-doi-mat-khau.png` (Mobile)*

1. **Card form đơn điệu như bài tập thực hành (Desktop - Giữa màn hình):**  
   Khung đổi mật khẩu kích thước ~540px đặt trơ trọi giữa trang web. Không có biểu tượng bảo mật trang nhã (Shield / Security Key), không có thông tin thời gian đổi mật khẩu lần cuối, không có chỉ dẫn bảo vệ tài khoản của Khoa CNTT.
2. **Quy tắc mật khẩu dạng danh sách chết (Desktop & Mobile - Dưới ô mật khẩu mới):**  
   4 gạch đầu dòng quy định độ dài và ký tự hiển thị bằng chữ xám li ti dính sát đáy ô input. Không có thanh đo độ mạnh mật khẩu theo thời gian thực (Password Strength Meter), không có phản hồi đổi màu xanh/đỏ khi người dùng gõ đạt yêu cầu. Đây là chuẩn mực tối thiểu của UX hiện đại nhưng hệ thống hoàn toàn thiếu vắng.
3. **Cặp nút hành động khập khiễng (Desktop & Mobile - Đáy card):**  
   Nút "← Hủy" màu trắng viền xám mảnh khảnh đứng cạnh nút "✓ Đổi mật khẩu" màu xanh navy đậm đặc. Sự chênh lệch trọng lượng thị giác quá lớn khiến nút Hủy trông như một nút bị vô hiệu hóa (disabled).
4. **Mobile thiếu an toàn khi gõ (Mobile - Khung form):**  
   Trên màn hình 390px, các ô nhập mật khẩu không có nút bật/tắt ẩn hiện mật khẩu (Eye icon toggle). Trong môi trường trường học hoặc nơi công cộng, việc không thể kiểm tra ký tự vừa gõ trên bàn phím ảo di động là một khiếm khuyết bảo mật và công thái học nghiêm trọng.

---

### TRANG 09: Giảng viên — Trang chủ (`/`)
*Ảnh tham chiếu: `shots/d-08-gv001-trang-chu.png` (Desktop) & `shots/m-08-gv001-trang-chu.png` (Mobile)*

1. **4 thẻ số liệu KPI như 4 ô Excel phóng to (Desktop - Hàng trên cùng):**  
   4 hộp chữ nhật màu trắng bo góc 14px chứa các con số `2`, `16`, `16`, `0`. Các con số màu đen trần trụi, kích thước font to nhưng không có điểm nhấn typography, không có icon minh họa chủ đề, không có tỷ lệ phần trăm tiến độ (ví dụ: Đã duyệt 0/16 - 0%). Trông vô hồn và nghèo nàn y như bảng tính văn phòng.
2. **Bảng "Đề tài của tôi" kéo dãn vô duyên (Desktop - Khối dưới):**  
   Chỉ có đúng 2 dòng đề tài nhưng bảng dữ liệu lại bị ép kéo dài hết bề ngang 1440px. Khoảng cách giữa tên đề tài, độ khó, chỉ tiêu và nút "Duyệt ngay" xa nhau hàng trăm pixel, buộc mắt giảng viên phải đảo liên tục từ mép trái sang mép phải màn hình để đọc một dòng thông tin.
3. **Badge số chờ duyệt (4, 12) màu vàng nhờ nhờ (Desktop & Mobile - Trong bảng đề tài):**  
   Con số sinh viên đang chờ duyệt (4 và 12) được đóng trong một badge màu vàng nhạt viền vàng nhờ nhờ `#FFF6DD`. Đối với giảng viên, đây là chỉ số khẩn cấp cần hành động ngay, nhưng màu sắc thiết kế lại mang tính thụ động, nhạt nhòa, không kích thích hành vi xử lý công việc.
4. **Mobile 2x2 gây nghẽn màn hình đầu (Mobile - 4 thẻ KPI):**  
   Trên màn hình 390px, 4 thẻ số liệu chia lưới 2x2 nuốt trọn toàn bộ màn hình đầu tiên (above the fold). Các dòng phụ đề bên dưới con số bị bẻ dòng gãy khúc vụn vặt ("sinh viên đăng ký", "nguyện vọng Đã đồng ý"). Giảng viên không hề thấy danh sách đề tài cần duyệt nếu không cuộn xuống dưới.

---

### TRANG 10: Giảng viên — Đề tài của tôi (`/giang-vien/de-tai/`)
*Ảnh tham chiếu: `shots/d-09-gv001-de-tai.png` (Desktop) & `shots/m-09-gv001-de-tai.png` (Mobile)*

1. **Nút "+ Thêm đề tài" cô đơn ở góc trời (Desktop - Đầu trang):**  
   Một chiếc nút màu xanh navy đậm nằm lẻ loi ở góc trên cùng bên phải màn hình 1440px, cách tiêu đề trang cả mét khoảng trắng. Không có thanh công cụ tìm kiếm, không có bộ lọc trạng thái đề tài (Đang mở / Đã đóng / Đủ chỉ tiêu).
2. **Rừng tag xám đơn điệu không phân biệt ngữ nghĩa (Desktop & Mobile - Trong mỗi card):**  
   Trong mỗi card đề tài, hệ thống rải ra 4 chiếc pill màu xám nhạt: `🏷 Trí tuệ nhân tạo`, `📊 Độ khó: Trung bình`, `🔧 3 kỹ năng yêu cầu`, `👥 Chỉ tiêu: 1 SV`. Tất cả đều dùng chung một màu xám tro, triệt tiêu hoàn toàn khả năng phân biệt đâu là phân loại chuyên môn, đâu là ràng buộc kỹ thuật.
3. **Phân cấp nút hành động bị đảo lộn (Desktop - Góc dưới phải card):**  
   Hành động quan trọng nhất của giảng viên ở trang này là "Xem đăng ký" (để duyệt sinh viên), nhưng nút này lại được vẽ bằng dạng viền mảnh mờ nhạt (`btn-outline`), đứng ngang hàng với nút phụ "Chỉnh sửa". Trong khi đó, dòng chữ "4 sinh viên đăng ký" ở bên trái lại dùng màu xanh lam đậm có icon to đùng, tạo nên sự tranh chấp chú ý vô lý.
4. **Mobile chồng chất nút bấm (Mobile - Cuối mỗi card đề tài):**  
   Trên màn hình 390px, hai nút "Xem đăng ký" và "Chỉnh sửa" bị kéo dãn 100% chiều rộng thành 2 thanh chữ nhật xếp chồng lên nhau. Mỗi card đề tài biến thành một khối dày đặc nút bấm, làm gia tăng chiều dài trang một cách không cần thiết.

---

### TRANG 11: Giảng viên — Chỉnh sửa đề tài (`/giang-vien/de-tai/127/sua/`)
*Ảnh tham chiếu: `shots/d-10-gv001-de-tai_127_sua.png` (Desktop) & `shots/m-10-gv001-de-tai_127_sua.png` (Mobile)*

1. **Khối chọn lĩnh vực chuyên môn lai căng dị hợm (Desktop & Mobile - Section 1):**  
   Các lựa chọn lĩnh vực (Web, Trí tuệ nhân tạo, Dữ liệu...) được thiết kế dưới dạng pill bo tròn viền xám, nhưng BÊN TRONG LẠI NHÉT MỘT Ô CHECKBOX VUÔNG VẮN! Khi được chọn, cả khối biến thành viền xanh đậm chữ xanh. Sự kết hợp giữa checkbox cổ điển và pill hiện đại tạo nên một thành phần giao diện quái dị, nghiệp dư.
2. **Formset kỹ năng thô lậu với checkbox Xóa vô danh (Desktop - Section Kỹ năng):**  
   Bảng kỹ năng yêu cầu có cột "Bắt buộc" là một checkbox trần trụi, và cột "Xóa" lại là MỘT CHECKBOX RỖNG KHÔNG CÓ CHỮ! Giảng viên nhìn vào cột "Xóa" chỉ thấy một ô vuông nhỏ xíu, hoàn toàn không biết tick vào đó là xóa hay không xóa. Hai hàng cuối cùng hiển thị dropdown `---------` rác rưởi của Django formset.
3. **3 ô thông số số học chia cột mất cân đối (Desktop - Cuối Section 1):**  
   Ba trường "Độ khó", "GPA tối thiểu", "Số sinh viên tối đa" được dàn đều 3 cột bằng nhau. Tuy nhiên, ô GPA và ô Số sinh viên chỉ cần nhập 1-2 chữ số nhưng lại bị kéo dãn rộng mênh mông, trong khi phần chú thích bên dưới "Thang điểm 4.0..." và "Chỉ tiêu sinh viên hướng dẫn" dính sát vào đáy input trông rất bí bách.
4. **Thảm họa nhập liệu kỹ năng trên di động (Mobile - Section Kỹ năng):**  
   Trên mobile 390px, bảng kỹ năng biến thành một chuỗi 5 card con xếp dọc mang tên "Kỹ năng 1", "Kỹ năng 2"... Mỗi card lại chứa 4 trường thông tin chen chúc. Giảng viên muốn thêm hoặc bớt 1 kỹ năng trên điện thoại phải vật lộn với hàng chục thao tác cuộn và chạm vô cùng mệt mỏi.

---

### TRANG 12: Giảng viên — Sinh viên đăng ký (`/giang-vien/de-tai/127/dang-ky/`)
*Ảnh tham chiếu: `shots/d-11-gv001-de-tai_127_dang-ky.png` (Desktop) & `shots/m-11-gv001-de-tai_127_dang-ky.png` (Mobile)*

1. **Nút "Đồng ý" và "Từ chối" màu sắc thô thiển, rủi ro cao (Desktop & Mobile - Cột Duyệt):**  
   Nút "Đồng ý" dùng màu xanh lá cây đặc (`#157347`) và nút "Từ chối" dùng viền đỏ chữ đỏ (`#B42318`). Hai nút này đặt sát sạt nhau mà không có khoảng đệm an toàn, không có hộp thoại xác nhận (modal confirmation), tiềm ẩn nguy cơ giảng viên bấm nhầm nút "Từ chối" sinh viên bằng một cú click vô tình.
2. **Cột "ĐIỂM AI" nghèo nàn, thiếu giải thích trực quan (Desktop - Cột giữa bảng):**  
   Điểm AI chỉ hiển thị dạng con số thô `66 /100`, `67 /100`, `76 /100` đặt cạnh badge xơ cứng "Khá phù hợp" hoặc "Cần xem thêm". Không có thanh tiến độ mini, không có biểu đồ radar so sánh thế mạnh, không giải thích vì sao sinh viên này lại được 76 điểm còn sinh viên kia chỉ được 60 điểm.
3. **Nút "Xem phân tích ⌵" dạng textlink chìm nghỉm (Desktop & Mobile - Đáy mỗi hàng):**  
   Đây là tính năng cốt lõi nơi AI cung cấp ma trận đối sánh kỹ năng chi tiết của sinh viên với đề tài, nhưng nó lại bị dìm xuống thành một dòng chữ nhỏ viền xám lơ lửng ở đáy hàng, khiến hầu hết giảng viên sẽ bỏ qua mà không bấm vào xem.
4. **Mobile nguy hiểm cho ngón tay cái (Mobile - Thẻ sinh viên):**  
   Trên điện thoại 390px, hai nút "Đồng ý" và "Từ chối" chiếm trọn một hàng ngang. Khi người dùng cầm điện thoại bằng tay phải, ngón tay cái tự nhiên rơi đúng vào vị trí của nút "Từ chối", cực kỳ dễ xảy ra thao tác nhầm lẫn gây hậu quả nghiêm trọng cho sinh viên.

---

### TRANG 13: Giảng viên — Hồ sơ giảng viên (`/giang-vien/ho-so/`)
*Ảnh tham chiếu: `shots/d-12-gv001-ho-so-giang-vien.png` (Desktop) & `shots/m-12-gv001-ho-so-giang-vien.png` (Mobile)*

1. **Avatar chữ "L" và khung chỉ tiêu như vé xem phim (Desktop - Đầu trang):**  
   Vòng tròn avatar chữ cái "L" màu xanh nhạt to tướng bên trái đặt đối diện với một khung viền xám đóng khung dòng chữ `5 CHỈ TIÊU TỐI ĐA`. Hai thành phần này rời rạc, tỷ lệ vụng về, không tạo nên phong thái trang trọng của một nhà khoa học/giảng viên đại học.
2. **Banner khóa chỉ tiêu khổng lồ gây ức chế thị giác (Desktop & Mobile - Dưới avatar):**  
   Một khối viền vàng cam dày đặc chiếm trọn chiều ngang màn hình với icon ổ khóa to tướng và hàng loạt đoạn văn lặp đi lặp lại thông báo "Đợt đăng ký đã đóng...". Nó chiếm tới 25% chiều cao màn hình chỉ để thông báo một trạng thái tĩnh đã rồi.
3. **8 ô chọn lĩnh vực dàn trải lãng phí không gian (Desktop - Section 02):**  
   8 lĩnh vực nghiên cứu được chia làm 2 cột với các hộp chữ nhật trắng viền xám to đùng (Web, Trí tuệ nhân tạo, Dữ liệu...). Không gian bên trong hộp hầu như trống rỗng, chỉ có một dòng chữ nhỏ và một ô checkbox thụt bên trái, tạo cảm giác giao diện bị loãng và thô.
4. **Văn bản giải thích thuật toán ILP như một bài luận văn (Desktop & Mobile - Section 03):**  
   Khối giải thích "Mục đích và quy tắc tính chỉ tiêu" ở cuối form là một bức tường chữ xám xịt với 4 gạch đầu dòng kỹ thuật khô khan (Thuật toán ILP, Nguyện vọng, Cơ chế khoá...). Hoàn toàn thiếu các sơ đồ trực quan hoặc biểu đồ dòng chảy để giảng viên hiểu nhanh cơ chế phân bổ.
5. **Mobile cuộn vô tận chỉ để xem 8 checkbox (Mobile - Toàn màn hình):**  
   Trên màn hình 390px, 8 hộp lĩnh vực xếp chồng thành 8 tầng màn hình. Giảng viên phải cuộn mỏi tay qua 4 màn hình mới thấy được nút "Lưu thông tin" nằm khuất tận đáy.

---

### TRANG 14: Khoa — Bảng điều khiển / Trang chủ (`/`)
*Ảnh tham chiếu: `shots/d-13-khoa01-trang-chu.png` (Desktop) & `shots/m-13-khoa01-trang-chu.png` (Mobile)*

1. **Trang đầu não nhưng trống rỗng như bãi đất hoang (Desktop - Toàn màn hình):**  
   Đây là trang chủ của Cán bộ Quản trị Khoa — nơi cần nắm bắt toàn cảnh tiến độ làm đồ án của hàng trăm sinh viên và hàng chục giảng viên. Nhưng màn hình chỉ có vỏn vẹn 3 thẻ số và 1 dòng bảng dữ liệu! Hơn 75% diện tích màn hình 1440px là khoảng xám chết `#F6F8FB` vô nghĩa.
2. **3 thẻ KPI nghèo nàn thông tin (Desktop & Mobile - Đầu trang):**  
   Các thẻ `50 Đề tài`, `100 Sinh viên`, `1 Đợt đăng ký` chỉ hiển thị con số trần trụi. Không có thông tin phân tích đi kèm: Bao nhiêu đề tài đã có SV đăng ký? Bao nhiêu SV chưa nộp hồ sơ? Tỷ lệ đáp ứng chỉ tiêu là bao nhiêu %? Đây là sự lãng phí nghiêm trọng về năng lực hiển thị của một dashboard quản trị.
3. **Bảng dữ liệu chỉ có 1 dòng trải dài 1440px (Desktop - Khối dưới):**  
   Bảng "Danh sách đợt đăng ký" chỉ chứa đúng 1 bản ghi duy nhất nhưng lại được kẻ khung full-width. Khoảng cách giữa tên đợt, thời gian, số lượng sinh viên xa cách nhau mù mịt, tạo cảm giác hệ thống chưa được hoàn thiện.
4. **Nút "Vào trang quản trị" và liên kết ngoài lệch pha (Desktop - Góc trên và góc dưới):**  
   Nút "Vào trang quản trị" màu xanh navy đặc ở góc trên bên phải, trong khi ở dưới bảng lại có thêm nút "Vào trang quản trị dữ liệu" viền mỏng có icon mở tab mới `↗`. Sự trùng lặp chức năng với hai phong cách thiết kế đá nhau chan chát gây bối rối cho cán bộ khoa.

---

### TRANG 15: Khoa — Quản lý phân công (`/khoa/phan-cong/`)
*Ảnh tham chiếu: `shots/d-14-khoa01-khoa_phan-cong.png` (Desktop) & `shots/m-14-khoa01-khoa_phan-cong.png` (Mobile)*

1. **THẢM HỌA THỊ GIÁC LỚN NHẤT: Bãi rác dữ liệu màu vàng chanh "Chưa xếp" (Desktop - Bảng dữ liệu):**  
   Hơn 50 dòng sinh viên chưa được xếp đề tài bị phủ kín toàn bộ nền bằng một màu vàng chanh nhạt `#FFF3CD` / `#FEF3C7` chói lọi, xen kẽ với các dòng màu trắng. Cột "ĐỀ TÀI PHÂN CÔNG" lặp đi lặp lại 57 lần chiếc badge đỏ gạch `[! Chưa xếp]`. Màn hình trông như một trang tính Excel bị đổ mực vàng lem nhem, gây nhức mắt, hoảng loạn thị giác và khiến cán bộ Khoa không thể tập trung đối soát dữ liệu.
2. **Biểu đồ cột CSS nghiệp dư không có trục tọa độ (Desktop - Dưới KPI):**  
   Khối "Phân bố điểm phù hợp sau phân công" vẽ 5 cột màu xanh ngọc và xanh dương lơ lửng giữa trời. Phía trên cột ghi các con số sinh viên `8, 9, 11, 9, 6, 0`, bên dưới là nhãn `< 50, 50-64...`. Không hề có trục tung Y, không có vạch lưới ngang (grid lines), tỷ lệ chiều cao giữa các cột không chuẩn xác toán học. Trông như sản phẩm cắt ghép vụng về của người mới học CSS Flexbox.
3. **Dải 7 ô metric KPI xếp hàng ngang nghẹt thở (Desktop - Đầu trang):**  
   7 hộp số liệu (Tỉ lệ phân công: 43%, Đạt NV1: 30%, Đạt Top 3: 43%, Thứ hạng TB: 1.37, Điểm TB: 63.8, Vi phạm chỉ tiêu: 0, Thời gian: 0.018s) bị nhồi chung vào một hàng ngang. Các con số có kích thước quá nhỏ, nhãn phụ lí nhí, không có phân cấp đâu là KPI cốt lõi sinh tử (Tỉ lệ phân công, Vi phạm chỉ tiêu) và đâu là thông số kỹ thuật phụ trợ (Thời gian giải ILP).
4. **Cụm nút điều khiển thuật toán nguy hiểm và cẩu thả (Desktop - Góc trên phải):**  
   Ba nút "Chạy tối ưu ILP" (xanh đậm), "Chạy Greedy" (trắng viền xám), và "Chốt & Công bố" (xanh lá cây) đặt san sát nhau ở góc trên. Nút "Chốt & Công bố" là hành động tối hậu mang tính pháp lý của Khoa, nhưng lại không có màu cảnh báo đặc biệt, không có khoảng cách an toàn với các nút chạy thử nghiệm thuật toán.
5. **Mobile hoàn toàn tê liệt và vô dụng (Mobile - Toàn màn hình):**  
   Trên màn hình 390px, bảng dữ liệu 10 cột bị cắt đứt ngang xương, chỉ hiện trơ trọi 3 cột: Mã SV, Họ tên, GPA. Toàn bộ các cột quan trọng nhất gồm: Đề tài phân công, Giảng viên hướng dẫn, Điểm phù hợp, Nút điều chỉnh... bị giấu kín sau thanh cuộn ngang. Cán bộ Khoa hoàn toàn không thể thực hiện bất kỳ thao tác nghiệp vụ nào trên điện thoại.

---

### TRANG 16: Khoa — Thống kê & Báo cáo (`/khoa/thong-ke/`)
*Ảnh tham chiếu: `shots/d-15-khoa01-khoa_thong-ke.png` (Desktop) & `shots/m-15-khoa01-khoa_thong-ke.png` (Mobile)*

1. **Biểu đồ cột đỏ rực "Top đề tài cạnh tranh" dọa dẫm nhức mắt (Desktop - Giữa trang):**  
   Khối biểu đồ Top đề tài nhận nhiều NV1 nhất sử dụng các cột dọc màu đỏ cờ đậm đặc `#DC2626` với các con số giật gân `21,0x`, `19,0x`, `6,0x`... Màu đỏ rực này chiếm lĩnh toàn bộ thị giác trang web, tạo cảm giác như hệ thống đang gặp sự cố báo động đỏ nguy cấp thay vì chỉ là dữ liệu thống kê sự quan tâm của sinh viên.
2. **Biểu đồ Donut đơn điệu và xoay nhãn 45 độ phản công thái học (Desktop - Khối biểu đồ trên):**  
   Biểu đồ Donut bên trái là một vòng tròn màu xanh lá cây 100% trơ trọi, lãng phí một nửa diện tích card. Biểu đồ cột bên phải có các nhãn lĩnh vực (Trí tuệ nhân tạo, Phần mềm doanh nghiệp...) bị xoay nghiêng 45 độ chen chúc, chữ nọ đè lên chữ kia, buộc người dùng phải nghiêng đầu mới đọc được.
3. **Bảng so sánh ILP vs Greedy dài lê thê và màu sắc rối loạn (Desktop - Nửa dưới trang):**  
   Bảng so sánh hai thuật toán nhồi nhét dày đặc các con số với 4 hệ màu khác nhau: Xanh lam (ILP), Đỏ (`57 SV` chưa xếp), Xanh lá (`+9,0%`, `+2,0%`), và Xám (Greedy). Sự nhảy múa của màu sắc trên từng dòng khiến người đọc bị phân tâm, không nắm bắt được ưu thế thực sự của mô hình tối ưu.
4. **Biểu đồ tải giảng viên lệch trục với bảng số liệu bên dưới (Desktop - Đáy trang):**  
   Biểu đồ cột thể hiện tải giảng viên bên trên có số lượng cột và vị trí không hề gióng hàng (misaligned) với bảng danh sách giảng viên chi tiết bên dưới. Người dùng không thể đối chiếu trực quan giữa cột biểu đồ và dòng dữ liệu tương ứng.
5. **Trang Mobile dài kỷ lục 12.000 pixel gây kiệt sức (Mobile - Toàn màn hình):**  
   Trên màn hình 390px, trang thống kê bị kéo dài thành một dải cuộn vô tận hơn 12.000px! Tất cả các biểu đồ, bảng dữ liệu, khối so sánh bị xếp chồng máy móc. Biểu đồ Donut và Bar chart bị bóp méo, bảng ILP bị cắt dòng chữ nọ đè chữ kia. Đây là ví dụ kinh điển của việc "đem nguyên xi desktop nhét vào mobile" mà không hề có tư duy thiết kế trải nghiệm di động.

---

## III. TOP 10 VẤN ĐỀ LẶP LẠI TOÀN HỆ THỐNG (XẾP THEO MỨC NGHIÊM TRỌNG)

1. **Hội chứng "Bệnh viện Bootstrap" — Vô hồn và Thiếu bản sắc thương hiệu (Brand Anemia):**  
   *Mức độ: TỐI KHẨN CẤP.*  
   Toàn bộ hệ thống bị dìm trong sắc xanh blue rẻ tiền `#174EA6` trên nền xám chết `#F6F8FB`. Không có một chi tiết nào thể hiện đây là một sản phẩm công nghệ cao của Khoa CNTT trường đại học danh tiếng. Giao diện nhạt nhòa đến mức nếu thay logo, nó có thể là bất kỳ phần mềm quản lý kho hay quản lý nhân sự lỗi thời nào từ thập niên trước.

2. **Khủng hoảng màu sắc ngữ nghĩa và Ô nhiễm thị giác (Color Semantics Crisis):**  
   *Mức độ: TỐI KHẨN CẤP.*  
   Lạm dụng màu vàng chanh `#FFF3CD` bôi kín 57 dòng sinh viên chưa xếp tại trang phân công; rải thảm màu đỏ rực cho các cảnh báo không nguy hiểm (nút Xóa, nút Chưa đủ điều kiện, cột biểu đồ 21x). Ngược lại, những chỉ số thực sự cần cảnh báo khẩn cấp (như số NV chờ duyệt của giảng viên) lại dùng màu vàng mờ nhạt. Hệ thống tín hiệu thị giác bị đảo lộn hoàn toàn.

3. **Cơn nghiện "Hộp trong hộp" (Card-in-Card Nesting Addiction):**  
   *Mức độ: NGHIÊM TRỌNG.*  
   Tư duy đóng khung mọi thứ vào thẻ chữ nhật bo góc 14px viền xám 1px. Càng chia nhỏ nội dung thì lại càng lồng card con vào card cha (Trang chủ SV, Trang Kết quả, Trang Hồ sơ, Trang Sửa đề tài). Điều này làm nát vụn nhịp điệu thị giác, lãng phí diện tích viền/đệm (padding) và khiến trang web trông như một đống hộp carton xếp chồng lộn xộn.

4. **Trải nghiệm Mobile chỉ là "Co ép Desktop" chứ không phải Mobile-First (Mobile Degradation):**  
   *Mức độ: NGHIÊM TRỌNG.*  
   Giao diện trên điện thoại 390px hoàn toàn không được thiết kế cho ngón tay cái. Bảng dữ liệu 10 cột bị cắt cụt; trang thống kê dài dằng dặc 12.000px; form kỹ năng kéo dài 4.000px; các nút bấm nguy hiểm (Từ chối, Xóa) nằm ngay vị trí chạm tự nhiên của ngón tay. Khả năng sử dụng trên di động thực tế gần như bằng không.

5. **Phân cấp Typography phẳng lì và nghiệp dư (Flat & Amateur Typography):**  
   *Mức độ: NGHIÊM TRỌNG.*  
   Font Be Vietnam Pro bị dùng một cách cơ học. Tiêu đề H1, H2, H3 thiếu sự chênh lệch rõ ràng về kích thước, line-height và letter-spacing âm. Các con số dữ liệu lớn (KPI metrics) bị đối xử như text thông thường, không dùng font mono chuyên dụng, không có số liệu dạng tabular lining, làm mất đi tính trang trọng của một bảng điều khiển khoa học.

6. **Phơi bày dữ liệu rác và Lỗi Formset nguyên thủy của Django (Raw Data Leakage):**  
   *Mức độ: TRUNG BÌNH CAO.*  
   Hệ thống liên tục để lộ các giá trị mặc định thô sơ của backend: các hàng dropdown chưa chọn `---------`, ô số lỗi cú pháp `1-!`, các trường rỗng hiển thị dấu gạch ngang `— / 100`, checkbox Xóa không có nhãn. Đây là bằng chứng của việc thiếu lớp thiết kế giao diện trung gian (UI Presentation Layer) để xử lý dữ liệu trước khi trình bày cho người dùng.

7. **Trạng thái rỗng (Empty States) tàn nhẫn và Bế tắc hành động (Brutal Empty States):**  
   *Mức độ: TRUNG BÌNH CAO.*  
   Khi không có dữ liệu (chưa mở đợt đăng ký, chưa có kết quả chính thức), hệ thống chỉ vứt ra một icon xám tro và một câu từ chối cộc lốc giữa bãi đất trống 1440px. Hoàn toàn không có hướng dẫn hành động tiếp theo, không có đồ họa giải thích quy trình, triệt tiêu tính tương tác và gây cảm giác ứng dụng bị đóng băng.

8. **Trực quan hóa dữ liệu (Dataviz) phi khoa học và cẩu thả:**  
   *Mức độ: TRUNG BÌNH.*  
   Biểu đồ cột dựng bằng CSS không có hệ trục tọa độ chuẩn; biểu đồ Donut lãng phí không gian; biểu đồ thanh xoay nhãn 45 độ phản công thái học; biểu đồ tải giảng viên lệch trục hoàn toàn với bảng dữ liệu bên dưới. Biểu đồ không giúp người dùng hiểu nhanh dữ liệu mà trái lại còn tạo thêm gánh nặng nhận thức (cognitive load).

9. **Hệ thống nút bấm (Buttons & Actions) lộn xộn, thiếu quy chuẩn bảo vệ:**  
   *Mức độ: TRUNG BÌNH.*  
   Nút chính, nút phụ, nút nguy hiểm dùng màu sắc và kích thước tùy tiện. Các hành động mang tính hủy hoại hoặc chốt pháp lý (Chốt công bố, Từ chối sinh viên) không có cơ chế bảo vệ hai bước (Two-step confirmation modal), biến các thao tác quản trị thành một trò chơi may rủi dễ bấm nhầm.

10. **Khoảng trắng chết và Mất cân bằng trục gióng bố cục (Dead Space & Alignment Fractures):**  
    *Mức độ: TRUNG BÌNH.*  
    Rất nhiều trang trên màn hình 1440px bị bỏ hoang tới 60–80% diện tích (Trang Đăng nhập, Trang Đổi mật khẩu, Trang Nguyện vọng, Trang Chủ Khoa). Các thành phần nội dung không bám theo hệ thống lưới (12-column grid) chặt chẽ, tạo ra những khoảng hở vô duyên và cảm giác thiếu hoàn thiện ở mọi góc nhìn.

---
*Bản kiểm toán kết thúc tại đây. Hệ thống thiết kế thay thế toàn diện được trình bày chi tiết tại tài liệu `DESIGN-v2.md`.*
