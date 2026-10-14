HỢP ĐỒNG CÀI ĐẶT ATLAS V3.5 — NHÓM CHUNG

Trạng thái: DESIGN AUTHORITY APPROVED
Phạm vi: Khung giao diện chung và 5 nhóm màn hình 00a, 01, 02, 03, 04–06.
Nguồn chuẩn: Ảnh tham chiếu đã duyệt và các quyết định ATLAS V3.5.
Nguyên tắc: Chỉ bổ sung class bố cục khi cần. Không tạo lại những component đã có, không chỉnh backend để phục vụ yếu tố trang trí.

Khi có xung đột, thứ tự ưu tiên là: quy tắc nghiệp vụ đang hoạt động → quyết định sửa của chủ dự án/Claude → hợp đồng này → thông số V3.5 chung → ảnh tham chiếu.

0. KHUNG CHUNG — ÁP DỤNG MỌI MÀN HÌNH
0.1. App Shell desktop

Thành phần

	

Thông số bắt buộc




Breakpoint

	

Desktop ≥1200px; 992–1199px sidebar thu gọn; 768–991px offcanvas; mobile dưới 768px




Sidebar

	

Rộng 216px, cao 100dvh, fixed left




Sidebar thu gọn

	

60px




Nền sidebar

	

#17385B




Header

	

Cao 56px, bắt đầu sau sidebar, nền #142B4B




Canvas

	

#F2F5FB, rộng phần còn lại




Padding nội dung

	

24px tại ≥1200px; 20px tại 992–1199px




Giới hạn nội dung

	

Max-width 1600px, căn giữa




Grid

	

12 cột, gap 16px




Section gap

	

16px




Panel

	

Nền #FFFFFF, viền 1px #DDE4EF, radius 6px




Panel header

	

Cao tối thiểu 42px, nền #F5F8FE, padding ngang 16px




Chữ

	

Be Vietnam Pro; H1 24px, body 14px, bảng 13px




Icon

	

Lucide line, stroke 2px




Focus

	

Outline 2px, offset 2px; tương phản ≥3:1

Logo: dùng SVG chữ M dạng sách mở đã duyệt. Kích thước icon 32×32px desktop, 28×28px mobile. Chữ “Capstone AI” 18px/600; không dùng lại logo Open Path cũ.

0.2. Cấu trúc sidebar

Vùng logo cao 64px, padding ngang 16px. Menu bắt đầu cách vùng logo 12px; mỗi item cao 44px, padding ngang 14px, icon 18px và gap icon–chữ 12px. Item active nền #294E79, vạch trái 3px #F5BA6E, chữ trắng. Menu nhiều mục tự cuộn bên trong sidebar, không cuộn logo.

Menu phụ thuộc vai trò và route có thật:

Vai trò

	

Menu cấp 1




Sinh viên

	

Tổng quan, Hồ sơ năng lực, Đề tài, Nguyện vọng, Kết quả




Giảng viên

	

Tổng quan, Đề tài của tôi, Hồ sơ giảng viên




Khoa

	

Tổng quan, Phân công, Thống kê, Nhập Excel, Giảng viên, Quản trị

Chỉ hiển thị mục mà vai trò có quyền truy cập và hệ thống có route thực tế. Trang đổi mật khẩu không được thêm vào sidebar; vào bằng menu tài khoản.

0.3. Topbar, page header và breadcrumb

Thành phần

	

Thông số




Topbar

	

56px, padding ngang 20px, nội dung căn giữa theo chiều dọc




Tên đợt

	

14px/600, tối đa một dòng




Trạng thái đợt

	

Badge hoặc chấm trạng thái kèm chữ, không chỉ màu




Avatar

	

Hình tròn 32px, chữ viết tắt 12px/600




Tài khoản

	

Tên 13px/600, vai trò 12px/400




Page header

	

H1 24px/600, line-height 34px; mô tả 14px/23px




Khoảng cách page header → khối đầu

	

16px




Breadcrumb

	

12px/19px, gap 8px, dùng chevron-right

Topbar không có chuông thông báo. Các chức năng Sáng/Tối/Theo thiết bị, Đổi mật khẩu, Đăng xuất nằm trong menu tài khoản, không tạo thêm mục điều hướng chính.

Breadcrumb chỉ xuất hiện khi có cấp điều hướng hợp lệ. Không tự tạo breadcrumb giả chỉ để khớp ảnh.

0.4. Mobile dưới 768px

Header cao 56px, logo và avatar chữ viết tắt. Canvas padding ngang 16px ở viewport 390px; grid chuyển một cột, gap 12px. Các trang không có hành động cố định sử dụng bottom navigation cao 64px cộng env(safe-area-inset-bottom), tối đa bốn mục.

Sinh viên: Tổng quan, Đề tài, Nguyện vọng, Kết quả. Hồ sơ năng lực truy cập từ header/tài khoản hoặc shortcut có chức năng.

Giảng viên: Tổng quan, Đề tài, Hồ sơ. Duyệt sinh viên đi qua đề tài, không tạo tab riêng.

Khoa: Tổng quan, Phân công, Thống kê, Quản trị; Nhập Excel và Giảng viên đi từ điều hướng mở rộng có route thật.

Trang có Bottom Action Bar cao 72px cộng safe area phải ẩn Bottom Navigation. Không bao giờ chồng cả hai thanh.

0.5. Thành phần mới cấp Shell

Class đề xuất

	

Thông số




.at-shell

	

min-height:100dvh; chia sidebar và vùng làm việc




.at-sidebar-brand

	

Height 64px; padding 16px; gap 10px




.at-account-trigger

	

Height 44px; gap 10px; padding 0 8px




.at-page-heading

	

Margin-bottom 16px; gap 8px; H1 và mô tả




.at-breadcrumb

	

Min-height 24px; font 12px; gap 8px




.at-mobile-actionbar

	

Fixed bottom; min-height 72px; padding 12px 16px + safe area

Không tạo thêm class at-card hoặc at-widget để bọc chồng các panel hiện có.

00a-thanh-phan-sang — Thư viện thành phần giao diện sáng

Mục đích: Trang kiểm tra trực quan toàn bộ component của ATLAS V3.5. Đây là trang tham chiếu thiết kế, không đưa vào menu nghiệp vụ khi triển khai sản phẩm.

Lưới desktop

Hàng

	

Khối

	

Cột/12

	

Chiều cao tối thiểu




1

	

Metric Ledger

	

7

	

144px




1

	

AI Score Block M1–M5

	

5

	

144px




2–3

	

Buttons

	

3

	

316px




2–3

	

Form Controls

	

3

	

316px




2

	

Status Badges + Rank Chips

	

6, chia đôi

	

104px




3

	

Filter Chips + Tabs + Pagination

	

6

	

196px




4–5

	

Data Table

	

7

	

268px




4

	

Explanation Note

	

5

	

144px




5

	

Empty State

	

5

	

192px




6

	

Section Panel mẫu

	

7

	

124px




Phủ nổi

	

Drawer bên phải

	

440px cố định

	

100dvh




Phủ nổi

	

Confirm Modal

	

480px

	

Theo nội dung




Phủ nổi

	

Toast

	

320px

	

64px

Riêng trang 00a được phép hiển thị drawer, modal và toast đồng thời để kiểm tra thành phần. Các màn hình nghiệp vụ thực tế không được tự mở nhiều lớp phủ.

Từng khối

Metric Ledger — .at-ledger

Năm ô trên cùng một hàng; nội dung lần lượt: 100 SV, 43% đã xếp, 30% đạt NV1, 43% Top 3, 63,8 điểm TB. Số chính 28px/600; nhãn 12px/500; chú thích 12px. Phân cách bằng đường dọc 1px, không dùng icon tròn.

AI Score — .at-evidence + .at-score

Điểm 79,6/100, chữ số chính 36px/600, xanh #176B60. Năm thanh M1–M5 theo đúng tên và thứ tự: Kỹ năng, Học lực, Lĩnh vực, Ngữ nghĩa, Đánh giá LLM. Điểm mẫu 84/78/82/76/79; trọng số 25/20/15/20/20%. Mỗi thanh cao 7px, khoảng cách hàng 8px, có giá trị số ở cuối. Không dùng biểu đồ tròn.

Buttons

Hai cỡ chuẩn V3.5: lớn 38px desktop và nhỏ 30px. Bốn biến thể primary/secondary/danger/text, thể hiện normal, disabled. Khoảng cách 8px. Nút disabled không nhận tương tác; nút danger chỉ dùng với hành động phá hủy dữ liệu. Focus áp dụng chung V3.5.

Form Controls

Thứ tự: Họ và tên → Mã sinh viên → Giảng viên hướng dẫn → Mô tả ngắn → checkbox. Trường nhập cao 38px, textarea tối thiểu 64px; label và lỗi theo chuẩn V3.5. Ví dụ lỗi “Trường này là bắt buộc” hiển thị ngay dưới textarea, không đẩy lên đầu form.

Badges, rank chips, filters, tabs

Badges gồm Chờ duyệt, Đồng ý, Từ chối, Đang mở, Đã công bố. Rank chips NV1, NV2, NV3 cao 28px, padding ngang 12px. Filter chips Tất cả, AI, Web, Đủ điều kiện, Chưa đủ điều kiện. Tabs Tất cả, Đã nộp, Chưa nộp. Active phải nhận biết bằng cả màu và vị trí/gạch chân.

Pagination

Chọn 10/trang, Trước, số 1–4, Sau; nút 32×32px, gap 4px. Phân trang trên ảnh mang tính trình diễn, không kết nối dữ liệu sản phẩm.

Data Table — .at-table

Cột

	

Rộng




#

	

5%




Mã SV

	

12%




Họ và tên

	

15%




Đề tài

	

25%




Giảng viên

	

16%




NV

	

7%




Điểm

	

7%




Trạng thái

	

8%




Thao tác

	

5%

Hiển thị 5 dòng minh họa, tên sinh viên Việt Nam và đề tài CNTT. Trường hợp tên dài cho xuống dòng trong cột. Các nút thao tác dùng text link “Xem chi tiết”, không tạo nhiều nút đặc màu trong mỗi hàng.

Explanation Note — .at-note

Tiêu đề “Vì sao đề tài này phù hợp?”, sau đó ba ý giải thích. Nội dung cỡ 13px, line-height 21px. Nếu lý do dài, hiển thị đầy đủ trong chi tiết, không cắt mất chứng cứ.

Empty State — .at-empty

Minh họa SVG 112×112px, tiêu đề “Chưa có dữ liệu”, mô tả một đến hai dòng. Nút CTA chỉ xuất hiện nếu route/hành động thực tế tồn tại. Loại bỏ nút “Thêm đề tài mới” ở ngữ cảnh sinh viên nếu không có quyền.

Drawer — Offcanvas 440px

Header 56px, avatar chữ viết tắt, thông tin sinh viên, tabs Thông tin chung/Đánh giá AI, M1–M5. Nội dung cuộn độc lập; không làm trang bên dưới tràn ngang. Không hiển thị tên giả trong một màn nghiệp vụ thật.

Confirm Modal

Rộng 480px, padding 20px, heading 18px/600. Nội dung nêu hậu quả công bố, trường nhập CÔNG BỐ, hai nút Hủy bỏ/Chốt & công bố cùng hàng. Quy tắc kiểm tra backend theo V3.4.

Toast

Góc trên phải, cách viewport 16px; rộng 320px, tối thiểu 64px cao; icon trạng thái 18px, tiêu đề 13px/600, mô tả 12px. Toast thành công tự đóng sau 5 giây; lỗi quan trọng không tự đóng trước khi người dùng đọc.

Trạng thái

Rỗng: từng component có empty state độc lập. Ít dữ liệu: giữ đúng số hàng/giá trị, không nhân bản. Chữ dài: tiêu đề và nội dung xuống dòng, không tràn panel. Chỉ xem: form control disabled/readonly đúng nghĩa, không mô phỏng bằng màu xám nhưng vẫn cho nhập.

Điện thoại dưới 768px

Trang trình diễn chỉ dùng một cột; thứ tự: Ledger → AI Score → Buttons → Form → Badges → Rank → Filters → Tabs → Pagination → Table (chuyển .at-list) → Explanation → Empty → Panel. Drawer và modal có nút mở riêng để kiểm tra, không phủ toàn bộ nội dung ngay khi tải.

Thành phần mới

Class

	

Thông số




.at-showcase-section

	

Margin-bottom 16px, min-width 0




.at-showcase-grid

	

12 cột, gap 12px, align-items:start




.at-showcase-overlay

	

Chỉ sử dụng ở trang 00a; backdrop 40% đen khi chủ động kiểm tra modal




.at-rank-chip

	

Height 28px, min-width 44px, radius 4px, padding ngang 12px, font 12px/600

01-dang-nhap — Đăng nhập
Lưới desktop

Hàng

	

Khối

	

Cột/12

	

Chiều cao tối thiểu




1

	

Brand Identity

	

5

	

100dvh




1

	

Login Form

	

7

	

100dvh

Trang đăng nhập không sử dụng sidebar, topbar hoặc bottom navigation.

Từng khối

Brand Identity

Nền #142B4B, padding 64px. Logo chữ M sáng 48×48px, “Capstone AI” 28px/600. Tên đầy đủ “Hệ thống tư vấn và phân công đề tài tốt nghiệp bằng AI” tối đa 3 dòng, 24px/34px.

Một câu giá trị: “Gợi ý đúng năng lực, phân công minh bạch.” Bên dưới ba lợi ích ngắn: Gợi ý phù hợp hồ sơ, Giải thích bằng 5 mô hình AI, Phân công tối ưu theo nguyện vọng. Mỗi lợi ích icon Lucide 20px, gap 12px. Không dùng ảnh sinh viên, stock, gradient.

Login Form

Khối form rộng 400px, căn giữa vùng 7/12. Thứ tự: tiêu đề “Đăng nhập” → mô tả → tên đăng nhập → mật khẩu → nút Đăng nhập → tài khoản demo.

Tên đăng nhập và mật khẩu cao 44px; cách nhau 20px. Nút Đăng nhập cao 44px, full-width. Không tạo liên kết “Quên mật khẩu” nếu backend không có route xử lý.

Ba tài khoản demo: sv001, gv001, khoa01, trình bày ba hàng văn bản trong một section nền phụ, tiêu đề “Tài khoản dùng thử”. Không hiển thị mật khẩu thật trong HTML ở môi trường production.

Trạng thái

Sai thông tin: thông báo lỗi chung ngay trên nút, giữ tên đăng nhập, không tiết lộ tài khoản có tồn tại hay không. Đang xử lý: khóa nút và hiển thị “Đang đăng nhập…”. Không có tài khoản demo: ẩn toàn bộ section demo, không để khối trắng.

Chữ dài: câu giới thiệu xuống tối đa ba dòng. Chỉ xem: không áp dụng cho đăng nhập.

Điện thoại dưới 768px

Ẩn vùng Brand Identity lớn; logo và tên sản phẩm ở đầu, tiếp đến tiêu đề, hai trường, CTA, tài khoản demo. Form max-width 440px, padding ngang 24px; không có bottom navigation.

Thành phần mới

Class

	

Thông số




.at-login-layout

	

Grid 5fr 7fr; min-height 100dvh; mobile 1 cột




.at-login-brand

	

Padding 64px; nền Navy; mobile ẩn




.at-login-form-wrap

	

Max-width 400px; margin auto; padding 32px 0




.at-demo-accounts

	

Padding 16px; margin-top 24px; radius 6px; background --at-surface-2; row gap 8px

02-doi-mat-khau — Đổi mật khẩu
Lưới desktop

Hàng

	

Khối

	

Cột/12

	

Chiều cao tối thiểu




1

	

Page Header

	

12

	

Không cố định




2

	

Form bảo mật

	

5

	

Theo nội dung




2

	

Vùng trống còn lại

	

7

	

Không tạo panel

Form rộng tối đa 480px, căn trái, không căn giữa toàn Canvas.

Từng khối

Page Header

Tiêu đề “Đổi mật khẩu”; mô tả “Cập nhật mật khẩu để bảo vệ tài khoản của bạn.”

Form — .at-panel

Header “Thông tin bảo mật”, sau đó: Mật khẩu hiện tại → Mật khẩu mới → Yêu cầu mật khẩu → Nhập lại mật khẩu mới → hành động.

Padding nội dung 20px, field gap 20px. Mỗi ô cao 44px. Nút Hủy và Cập nhật mật khẩu nằm cuối form, căn phải, gap 8px.

Yêu cầu mật khẩu phải lấy theo validation thực của Django, không tự áp dụng quy tắc giả khác backend. Không hiển thị “Mật khẩu cập nhật lần cuối” nếu hệ thống không lưu hoặc không cung cấp dữ liệu đó.

Trạng thái

Sai mật khẩu hiện tại: lỗi ngay dưới trường. Mật khẩu mới không hợp lệ: hiển thị từng lỗi do validator trả về. Không khớp xác nhận: báo ngay dưới trường xác nhận. Thành công: hiển thị xác nhận và không giữ giá trị mật khẩu.

Đang xử lý: khóa nút tránh submit hai lần. Chỉ xem: không áp dụng; nếu không có quyền, trả trang 403.

Điện thoại dưới 768px

Một cột: Header → Form. Form full-width; nút cập nhật full-width và nút hủy dạng secondary ở dưới. Không dùng action bar cố định, vì form ngắn. Giữ Bottom Navigation nếu người dùng đang đăng nhập và đây là trang thuộc shell, nhưng không để thanh đáy che nút.

Thành phần mới

Không cần class mới ngoài .at-page-heading đã khóa.

03-thieu-ho-so — Hồ sơ năng lực chưa hoàn tất
Lưới desktop

Hàng

	

Khối

	

Cột/12

	

Chiều cao tối thiểu




1

	

Page Header

	

12

	

Không cố định




2

	

Period Status

	

12

	

88px




3

	

Thông tin còn thiếu

	

8

	

400px




3

	

Việc cần làm tiếp theo

	

4

	

400px




4

	

Lưu ý về đánh giá AI

	

12

	

88px

Từng khối

Period Status — .at-period

Tên đợt, trạng thái và ngày bắt đầu/kết thúc từ backend. Mô tả ngắn giải thích hồ sơ năng lực cần hoàn thành trước khi hệ thống tạo gợi ý.

Thông tin còn thiếu — .at-panel + .at-list

Header “Thông tin còn thiếu”. Các dòng có tên mục, mô tả và trạng thái “Chưa có”; min-height 64px/dòng, padding 12px 16px, gap 8px.

Các mục được hiển thị theo dữ liệu thiếu thực tế, không mặc định tất cả đều thiếu. Ví dụ: Giới thiệu bản thân, Kỹ năng mức 1–5, Lĩnh vực quan tâm, học phần liên quan nếu bắt buộc theo cấu hình.

Việc cần làm tiếp theo

Ba bước hướng dẫn: hoàn thiện hồ sơ → nhận gợi ý AI → nộp nguyện vọng. CTA “Đi đến Hồ sơ năng lực” full-width, cao 44px. Không có nút “Xem hướng dẫn” khi route/tài liệu chưa tồn tại.

Lưu ý về AI — .at-note

Giải thích hệ thống sử dụng M1–M5 và trọng số AHP 25/20/15/20/20%. Font 13px/21px; không tự khẳng định M5 đã được chấm khi hồ sơ chưa hoàn chỉnh.

Trạng thái

Không có hồ sơ: hiển thị toàn bộ các trường bắt buộc cần tạo. Thiếu một trường: chỉ hiển thị đúng một dòng. Hồ sơ đã đủ: redirect hợp lệ sang Trang chủ hoặc Hồ sơ, không giữ trang cảnh báo.

Lỗi tải dữ liệu: “Không thể kiểm tra trạng thái hồ sơ”, có nút thử lại nếu chức năng tải lại tồn tại. Không kết luận người dùng thiếu hồ sơ chỉ vì truy vấn lỗi.

Chữ dài: mô tả xuống dòng, không giới hạn chiều cao item. Chỉ xem: nếu đợt đóng và không thể chỉnh sửa, CTA phải ẩn/disabled theo quyền backend, kèm giải thích.

Điện thoại dưới 768px

Header → Period → Thông tin còn thiếu → Việc cần làm → Lưu ý AI. Tất cả một cột; checklist dạng danh sách dọc. CTA full-width. Không dùng các biểu tượng tròn lớn trong từng mục.

Thành phần mới

Class

	

Thông số




.at-missing-item

	

Min-height 64px; padding 12px 16px; display flex; gap 12px




.at-next-steps

	

Padding 16px; bước dọc; khoảng cách 20px




.at-next-step-number

	

32×32px; radius 50%; font 14px/600; nền --at-info-soft

04-06-trang-loi — 403, 404, 500

Đây là một sheet tham chiếu ba biến thể. Khi ứng dụng chạy thật, mỗi mã lỗi là một màn độc lập, không hiển thị cả ba cùng lúc.

Lưới màn tham chiếu desktop

Hàng

	

Khối

	

Cột/12

	

Chiều cao tối thiểu




1

	

Tiêu đề “Trạng thái lỗi hệ thống”

	

12

	

Không cố định




2

	

403 — Không có quyền truy cập

	

4

	

560px




2

	

404 — Không tìm thấy trang

	

4

	

560px




2

	

500 — Lỗi hệ thống

	

4

	

560px

Từng khối

Mỗi biến thể sử dụng .at-panel, header 42px, nội dung căn giữa. Minh họa SVG 112×112px; mã lỗi 64px/700; tiêu đề 18px/600; mô tả 14px/23px, tối đa 3–4 dòng; nút quay về trang chủ cao 44px.

Mã

	

Icon/minh họa

	

Nội dung

	

Hành động




403

	

lock-keyhole

	

Bạn không có quyền xem trang này.

	

Quay về trang chủ




404

	

file-search hoặc SVG trạng thái rỗng

	

Trang bạn tìm kiếm không tồn tại hoặc đã được chuyển.

	

Quay về trang chủ




500

	

settings-2 + triangle-alert trong SVG có sẵn

	

Đã xảy ra lỗi khi xử lý yêu cầu.

	

Thử lại / Quay về trang chủ

403 không hiển thị chi tiết phân quyền nội bộ. 404 không tự đoán trang thay thế. 500 không lộ traceback, đường dẫn hệ thống, câu truy vấn hay thông tin nhạy cảm.

Trạng thái

Rỗng/ít dữ liệu: không áp dụng, vì mỗi trang có nội dung tĩnh theo mã lỗi. Chữ dài: mô tả tự xuống dòng, max-width 360px. Chỉ xem: toàn bộ trang; chỉ các hành động điều hướng được phép tương tác.

Trang lỗi phải render được khi người dùng chưa đăng nhập. Trong trường hợp đó dùng shell tối giản có logo Capstone AI và không hiển thị sidebar, topbar đợt hoặc thông tin tài khoản.

Điện thoại dưới 768px

Màn sheet tham chiếu chuyển ba panel thành ba khối dọc. Màn lỗi thực tế chỉ hiển thị một panel: minh họa 96×96px, mã lỗi 48px, mô tả tối đa chiều rộng 320px và CTA full-width tối đa 280px. Không cần Bottom Navigation nếu không xác thực.

Thành phần mới

Class

	

Thông số




.at-error-layout

	

Min-height calc(100dvh - 56px); display flex; align-items:center; justify-content:center; padding 24px




.at-error-panel

	

Width 100%; max-width 560px; padding 32px; text-align:center




.at-error-illustration

	

Width/height 112px; margin 0 auto 20px




.at-error-code

	

Font 64px; line-height 72px; weight 700




.at-error-copy

	

Max-width 360px; margin 16px auto 24px

QUY TẮC KHÓA KHI TRIỂN KHAI

Hệ class mới chỉ được bổ sung vào static/css/atlas.css. Không tạo CSS riêng cho từng trang, không dùng inline style để chữa bố cục.

Các ảnh đã duyệt là chuẩn về cấu trúc, mật độ, phân cấp và nhận diện; không phải nguồn dữ liệu nghiệp vụ. Tên, điểm, thời hạn, trạng thái và các con số trong ảnh không được hardcode vào sản phẩm.

Bắt buộc loại bỏ khỏi ảnh khi triển khai: chuông thông báo chưa có backend, nút không có chức năng, nhãn M5 cũ “Mức phù hợp”, logo không đúng chữ M và mọi mục menu không có route hoặc không đúng quyền.

Nghiệm thu nhóm chung khi shell thống nhất ở 390/768/992/1200/1440px; các thành phần không tràn, không chồng; tương phản WCAG AA đạt; form/validation, trạng thái lỗi và điều hướng thực tế hoạt động. Trang 00a là công cụ kiểm tra component và không được lộ trong menu người dùng thông thường.

Hiệu lực: Hợp đồng này khóa phần khung chung cùng các màn 00a, 01, 02, 03, 04–06 của ATLAS V3.5.