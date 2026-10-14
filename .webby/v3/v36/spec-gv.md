HỢP ĐỒNG CÀI ĐẶT ATLAS V3.5 — NHÓM GIẢNG VIÊN

Trạng thái: DESIGN AUTHORITY APPROVED
Phạm vi: 13–17 và m16-gv-duyet-sv.
Hiệu lực: Bổ sung hợp đồng nhóm Chung, ghi đè thông số cũ khi có xung đột.

Quy tắc chung nhóm GV

Shell: Sidebar 216px, topbar 56px, canvas #F2F5FB, panel trắng, header 42px. Logo chữ M đã duyệt.

Menu GV: Chỉ 3 mục: Tổng quan (house), Đề tài của tôi (file-text), Hồ sơ giảng viên (user-round). Màn duyệt SV nằm dưới Đề tài của tôi, không tạo menu cấp một mới.

Desktop: Grid 12 cột, gap 16px; content padding 24px tại ≥1200px.

Mobile: Dưới 768px, padding ngang 16px, một cột, gap 12px. Bottom Navigation gồm Tổng quan, Đề tài, Hồ sơ; khi drawer duyệt mở phải ẩn Bottom Navigation.

Dữ liệu: Lấy từ CSDL. Tên, điểm và số lượng trên ảnh chỉ dùng để kiểm tra hình thức, không hardcode.

M1–M5: Kỹ năng / Học lực / Lĩnh vực / Ngữ nghĩa / Đánh giá LLM. Trọng số AHP theo phiên bản dữ liệu; ví dụ ảnh là 25/20/15/20/20%.

Loại bỏ: Chuông, nút giả, nút sửa khi không được phép, trường không tồn tại hoặc chức năng backend chưa hỗ trợ.

Quyền: Chỉ cho giảng viên xem và xử lý đề tài, đăng ký và hồ sơ thuộc phạm vi được phân quyền.

13-gv-tong-quan — Trang chủ giảng viên
Lưới desktop

Hàng

	

Khối

	

Cột/12

	

Min-height




1

	

Page Header: lời chào, bộ môn, Khoa, nút Đề tài của tôi

	

12

	

72px




2

	

Đợt đăng ký + trạng thái

	

12

	

88px




3

	

Tổng quan đề tài hướng dẫn — Metric Ledger

	

12

	

184px




4

	

Đề tài có SV chờ duyệt

	

8

	

380px




4

	

Trạng thái đợt và việc cần xử lý

	

4

	

380px

Từng khối

Page Header — .at-page-heading

H1 “Xin chào, [học hàm/học vị + họ tên]”. Dòng phụ gồm mã GV, bộ môn, Khoa, phân tách bằng divider 14px. Một nút secondary “Đề tài của tôi”, căn phải.

Đợt đăng ký — .at-period

Tên đợt, trạng thái, ngày bắt đầu/kết thúc; phần hướng dẫn ở phải như ảnh. Nếu đợt đã đóng, thông điệp phải phản ánh đúng quyền xử lý còn lại của GV.

Tổng quan — .at-panel + .at-ledger

Bốn chỉ số trên một hàng, chia đều 25%:

Chỉ số

	

Nội dung




Đề tài

	

Tổng số đề tài GV phụ trách




SV đăng ký

	

Số đăng ký vào các đề tài thuộc GV




Chờ duyệt

	

Số đăng ký chưa được GV xử lý




Đã đồng ý

	

Số đăng ký được GV chấp thuận

Số lớn 36px/600, label 14px/600, chú thích 12px. Không dùng 4 KPI card riêng hoặc icon tròn. Các chỉ số đếm từ preference/registration thực, phân biệt số lượt đăng ký và số SV duy nhất khi cần.

Đề tài chờ duyệt — .at-panel + .at-table

Toolbar tìm kiếm 60% và trạng thái 40%, gap 12px.

Cột

	

Rộng




Đề tài

	

31%




Sinh viên

	

19%




MSSV

	

13%




Điểm AI

	

10%




NV

	

7%




Trạng thái

	

12%




Thao tác

	

8%

Mỗi dòng cao tối thiểu 48px, mặc định tối đa 10 dòng trong bảng tổng quan. “Phân tích” là hành động mở trang duyệt SV của đề tài tương ứng, không tạo route duyệt tổng giả.

Trạng thái đợt — .at-panel

Thứ tự: trạng thái nhận đăng ký → thời hạn duyệt nếu backend có → trạng thái phân công. Mỗi mục là một hàng thông tin min-height 64px, không dùng ba card lồng nhau. Không tự tạo ngày hạn duyệt.

Trạng thái

Rỗng: chưa có đề tài → .at-empty “Bạn chưa có đề tài hướng dẫn”; CTA thêm đề tài chỉ khi route và quyền cho phép.

Ít dữ liệu: 1–9 đăng ký hiển thị đúng số dòng; ẩn phân trang.

Chữ dài: tên đề tài tối đa 2 dòng ở bảng tổng quan, đầy đủ trong trang Đề tài của tôi.

Chỉ xem: GV không được sửa/duyệt thì chỉ hiện danh sách và trạng thái, ẩn nút xử lý; chỉ số vẫn hiển thị.

Điện thoại dưới 768px

Thứ tự: Header → Period → Metric Ledger dạng 2×2 → Danh sách cần duyệt → Trạng thái đợt → Bottom Navigation.

Bảng chuyển thành .at-list; mỗi item gồm tên đề tài, SV/MSSV, điểm, NV, trạng thái và link Phân tích. Không hiển thị bảy cột dạng bảng thu nhỏ.

Thành phần mới

Class

	

Thông số




.at-lecturer-ledger

	

4 cột desktop; 2 cột mobile; divider 1px; padding 16px




.at-review-summary-item

	

Min-height 76px; padding 12px 16px; gap 8px




.at-period-task

	

Min-height 64px; padding 12px 16px; divider dưới 1px

14-gv-de-tai — Đề tài của tôi
Lưới desktop

Hàng

	

Khối

	

Cột/12

	

Min-height




1

	

Page Header

	

12

	

72px




2

	

Đợt đăng ký

	

12

	

88px




3

	

Danh sách đề tài: toolbar + bảng

	

12

	

480px




4

	

Phân trang

	

12

	

52px

Từng khối

Header — .at-page-heading

Tiêu đề “Đề tài của tôi”, thông tin GV. Nút “Thêm đề tài” đặt bên phải toolbar bảng, chỉ xuất hiện khi backend hỗ trợ tạo đề tài và đợt cho phép.

Toolbar

Tìm kiếm theo tên đề tài chiếm 60%; trạng thái 25%; hành động thêm chiếm 15%. Input/select cao 38px, gap 12px.

Bảng — .at-table

Cột

	

Rộng




#

	

5%




Đề tài

	

29%




Lĩnh vực

	

18%




Chỉ tiêu

	

8%




SV đăng ký

	

10%




Trạng thái

	

13%




Thao tác

	

17%

Hàng cao tối thiểu 52px. Tên đề tài 14px/600. Trạng thái lấy từ topic: Đang mở, Đủ chỉ tiêu, Tạm khóa hoặc tên trạng thái thực trong backend.

Thao tác: Xem, Sửa, menu bổ sung chỉ khi có chức năng thật; nút Sửa ẩn nếu đề tài bị khóa/chưa được phép chỉnh sửa. Tránh hiện ba nút primary cùng hàng.

Phân trang server-side 20 đề tài/trang, giữ q, status, sort.

Trạng thái

Rỗng: chưa có đề tài → .at-empty “Bạn chưa tạo đề tài nào”.

Ít dữ liệu: 1–20 đề tài → bảng co theo nội dung, không tạo hàng giả.

Chữ dài: tên đề tài tối đa 2 dòng; lĩnh vực tự xuống dòng, không tràn.

Chỉ xem: đợt đóng/đã công bố → giữ nút Xem và thông tin đăng ký, ẩn Sửa/Thêm khi backend không cho phép.

Điện thoại dưới 768px

Header → Period → Tìm kiếm → Bộ lọc trạng thái → Danh sách đề tài → Phân trang → Bottom Navigation.

Mỗi .at-item có tên đề tài, lĩnh vực, chỉ tiêu/SV đăng ký, trạng thái và hành động Xem; nút Sửa xuất hiện nếu được phép. Không ép bảng ngang.

Thành phần mới

Class

	

Thông số




.at-lecturer-topic-toolbar

	

Grid minmax(0,3fr) minmax(160px,1.25fr) auto; gap 12px; mobile một cột




.at-topic-capacity

	

Font 13px/21px; số dạng “2/3”; tabular-nums




.at-lecturer-topic-item

	

Padding 16px; min-height 112px; gap 10px; border-bottom 1px --at-line

15-gv-form-de-tai — Thêm / chỉnh sửa đề tài
Lưới desktop

Hàng

	

Khối

	

Cột/12

	

Min-height




1

	

Page Header

	

12

	

72px




2

	

Đợt đăng ký

	

12

	

88px




3

	

Thông tin chung

	

7

	

420px




3

	

Lĩnh vực

	

5

	

136px




4, cùng cột phải hàng 3

	

Kỹ năng yêu cầu

	

5

	

284px




5

	

Điều kiện

	

7

	

206px




5

	

Chỉ tiêu & trạng thái

	

5

	

206px




6

	

Hành động Hủy / Lưu

	

12

	

56px

Đây là lưới hai cột theo ảnh. Cột phải có hai panel xếp dọc, tổng chiều cao phụ thuộc số kỹ năng.

Từng khối

Thông tin chung — .at-panel

Form 2 cột, gap 16px:

Tên đề tài 65% và Mã đề tài 35%.

Lĩnh vực chính 50% và Độ khó 50%.

Mô tả ngắn 50% và Mục tiêu 50%, textarea min-height 96px.

Công nghệ gợi ý 100%, nếu model/view có dữ liệu này.

Các trường bắt buộc phải theo Django form, không bắt buộc Mã đề tài nhập tay nếu backend tự sinh.

Lĩnh vực — .at-panel + .at-chip

Tìm kiếm lĩnh vực nếu có danh mục; các chip được chọn tự wrap, gap 8px. Lĩnh vực chính phải rõ; không tạo đa lĩnh vực nếu backend chỉ hỗ trợ một field_id.

Kỹ năng yêu cầu — .at-panel + .at-table

Cột

	

Rộng




Kỹ năng

	

30%




Mức yêu cầu

	

27%




Trọng số

	

17%




Bắt buộc

	

16%




Xóa

	

10%

Hàng min-height 42px; select mức 1–5. Trọng số kỹ năng là trọng số nội bộ của topic_skills, không phải AHP M1–M5. Hệ thống validate mức, trọng số, lựa chọn bắt buộc và các dòng trùng trên server. Nút Thêm kỹ năng ở header panel, chỉ khi có quyền.

Điều kiện — .at-panel

GPA tối thiểu + học phần tiên quyết. Với từng học phần, phải có mã/tên và điểm tối thiểu nếu backend hỗ trợ. Ghi chú xét duyệt là tùy chọn nếu tồn tại trong model/form.

Chỉ tiêu & trạng thái — .at-panel

Trường chỉ tiêu sinh viên, trạng thái đề tài và các thuộc tính mà backend thực sự hỗ trợ. Không thêm “Cho phép chỉnh sửa sau công bố” hay “Nhận đăng ký NV1” nếu không có field/logic tương ứng.

Hành động gồm Hủy và Lưu đề tài. Nút “Lưu nháp” chỉ hiển thị khi có trạng thái nháp và xử lý tương ứng.

Trạng thái

Tạo mới: form trống hoặc default hợp lệ do backend cung cấp; không tự điền tên đề tài.

Sửa: điền toàn bộ dữ liệu hiện tại, gồm các formset kỹ năng/tiên quyết; xóa dòng phải tuân thủ cơ chế formset.

Ít dữ liệu: không có kỹ năng/học phần → một empty row hoặc hướng dẫn thêm, không tạo nội dung giả.

Chữ dài: textarea phát triển chiều cao, label xuống dòng; không tràn cột.

Chỉ xem: đề tài khóa hoặc thiếu quyền → trường readonly/disabled, không có nút Lưu; giữ xem đầy đủ dữ liệu.

Điện thoại dưới 768px

Header → Period → Thông tin chung → Lĩnh vực → Kỹ năng → Điều kiện → Chỉ tiêu/trạng thái → Action Bar.

Form một cột. Kỹ năng trở thành từng item với select kỹ năng, select mức, input trọng số, checkbox bắt buộc và nút xóa. Field gap 20px, touch target ≥44px. Action Bar 72px + safe area thay Bottom Navigation.

Thành phần mới

Class

	

Thông số




.at-topic-form-grid

	

Grid 7fr 5fr; gap 16px; mobile một cột




.at-topic-form-fields

	

Grid 2 cột; gap 16px; mobile một cột, gap 20px




.at-topic-skill-row

	

Min-height 42px desktop; mobile padding 12px, gap 12px




.at-topic-form-actions

	

Min-height 56px desktop; padding 8px 16px; gap 8px; mobile fixed bottom min-height 72px + safe area

16-gv-duyet-sv — Sinh viên đăng ký đề tài
Lưới desktop

Hàng

	

Khối

	

Cột/12

	

Min-height




1

	

Page Header + thông tin GV

	

12

	

72px




2

	

Đợt đăng ký

	

12

	

88px




3

	

Danh sách sinh viên đăng ký

	

12

	

540px




Phủ bên phải

	

Drawer phân tích hồ sơ

	

440px

	

100dvh

Drawer mở theo nút Phân tích, không phải một cột nằm sẵn trong grid. Khi đóng, bảng chiếm toàn bộ Main Canvas.

Từng khối

Danh sách SV — .at-panel + .at-table

Header “Danh sách sinh viên đăng ký”, bên dưới tên đề tài đang xét. Tên đề tài 15px/600; toolbar tìm kiếm chiếm 65%, trạng thái 35%; gap 12px.

Khi drawer 440px mở, vùng bảng còn lại có min-width:0, không tràn viewport. Nếu không đủ chiều rộng, bảng được cuộn ngang trong chính panel; không đẩy cả trang.

Cột

	

Rộng




MSSV

	

14%




Sinh viên

	

19%




GPA

	

9%




NV

	

9%




Điểm AI

	

12%




Trạng thái

	

19%




Thao tác

	

18%

Hàng min-height 48px. Sinh viên đang chọn có nền --at-surface-hover; trạng thái là Chờ duyệt/Đồng ý/Từ chối theo dữ liệu thực. Thao tác duy nhất trong bảng là “Phân tích” hoặc “Xem” khi chỉ có quyền xem.

Phân trang server-side 20 dòng/trang, giữ q, status và page. Không nạp trước 100 drawer.

Drawer phân tích — Offcanvas 440px

Cấu trúc cố định:

Vùng

	

Kích thước




Drawer header

	

56px




Student identity

	

Min-height 80px; padding 16px




Đề tài đăng ký + NV

	

Min-height 76px; padding 12px 16px




Kết quả AI

	

Min-height 184px




Điều kiện đăng ký

	

Theo số điều kiện, mỗi hàng 38px




Giới thiệu bản thân

	

Theo nội dung, padding 16px




Nhận xét giảng viên

	

Theo dữ liệu/form thực




Footer hành động

	

72px + safe area

Drawer body tự cuộn, padding 16px, gap section 12px. Header và footer không cuộn theo body.

AI — .at-evidence + .at-score

Điểm tổng 40px/600, M1–M5 theo tên đã khóa, thanh 7px. Trọng số AHP hiển thị ở header nếu có weights_version. Không giả định M5 có dữ liệu.

Điều kiện — .at-list

Mỗi hàng gồm icon, nhãn, giá trị thực và kết quả. Ví dụ “GPA yêu cầu 2,80 — thực tế 3,42”. Khi không đạt, thể hiện rõ thiếu bao nhiêu và loại điều kiện; không chỉ ghi “Chưa rõ”.

Giới thiệu

Hiển thị văn bản SV đã khai báo, 13px/21px; không viết hộ SV. Nếu trống: “Sinh viên chưa cung cấp giới thiệu.”

Nhận xét GV

Nếu backend có trường nhận xét thì render; nếu không có, không hiển thị textarea giả hoặc tự lưu nhận xét.

Footer

Hai nút cùng hàng: Từ chối secondary-danger và Đồng ý primary, flex mỗi nút 1:1, gap 12px; min-height 44px. Từ chối mở modal yêu cầu lý do 5–500 ký tự, validate ở client và server. Đồng ý có xác nhận theo luồng nghiệp vụ thực nếu backend yêu cầu.

Quy tắc nghiệp vụ quan trọng: Nếu sinh viên không đạt điều kiện bắt buộc, không được suy luận rằng điểm AI cao là đủ để chấp thuận. Nút Đồng ý phải tuân thủ quyền và kiểm tra eligibility phía backend.

Trạng thái

Rỗng: chưa có SV đăng ký → .at-empty trong panel; không mở drawer.

Ít dữ liệu: 1–19 SV → hiển thị đúng số hàng, ẩn pagination nhiều trang.

Chữ dài: tên SV xuống tối đa 2 dòng; giới thiệu trong drawer đầy đủ, cuộn body.

Chỉ xem: GV không còn quyền duyệt → drawer vẫn cho xem dữ liệu hợp lệ, ẩn cả hai nút quyết định. Đăng ký đã xử lý → hiển thị trạng thái và lý do nếu có, không cho duyệt lại trái phép.

Loading: click Phân tích → GET HTML fragment cho đúng SV; hiển thị “Đang tải hồ sơ…” trong drawer; lỗi GET có thông báo và nút Thử lại.

Bảo mật: kiểm quyền cho từng yêu cầu drawer, không chỉ kiểm ở trang danh sách.

Điện thoại dưới 768px — m16

Thứ tự trang nền: Header → Period → Tên đề tài + số đăng ký → Tìm kiếm/lọc → Danh sách SV.

Khi mở hồ sơ: Drawer chiếm 100dvh, có header 56px và footer 72px + safe area. Thứ tự nội dung: thông tin SV → đề tài/NV → giới thiệu → điểm AI → M1–M5 → điều kiện → nhận xét → footer. Không hiển thị Bottom Navigation trong trạng thái này.

Các thanh M1–M5 xếp dọc 5 hàng; nút Từ chối/Đồng ý cùng một hàng, mỗi nút tối thiểu 44px cao. Nội dung cuộn độc lập, không bị footer che.

Ảnh tham chiếu có Bottom Navigation đồng thời với footer duyệt; triển khai phải sửa lỗi này theo quyết định V3.5: chỉ giữ footer hành động.

Thành phần mới

Class

	

Thông số




.at-registration-toolbar

	

Grid 65% 35%; gap 12px; padding 16px; mobile một cột




.at-registration-selected

	

Background --at-surface-hover; không thay trạng thái dữ liệu




.at-review-drawer-body

	

Height calc(100dvh - 128px - env(safe-area-inset-bottom)); overflow-y:auto; padding 16px; gap 12px




.at-review-drawer-footer

	

Height 72px + safe area; padding 12px 16px; display flex; gap 12px; border-top 1px




.at-review-student-meta

	

Display flex; flex-wrap:wrap; gap 8px; font 13px/21px




.at-eligibility-row

	

Min-height 38px; grid 20px minmax(0,1fr) auto; gap 10px; align-items:center




.at-mobile-review-drawer

	

Dưới 768px width 100vw; height 100dvh; border-radius 0

17-gv-ho-so — Hồ sơ giảng viên
Lưới desktop

Hàng

	

Khối

	

Cột/12

	

Min-height




1

	

Page Header + Chỉnh sửa hồ sơ

	

12

	

72px




2

	

Thông tin giảng viên

	

7

	

360px




2

	

Chỉ tiêu hướng dẫn

	

5

	

360px




3

	

Chuyên môn và lĩnh vực hướng dẫn

	

7

	

260px




3

	

Thống kê theo lĩnh vực

	

5

	

260px

Từng khối

Thông tin GV — .at-panel

Header “Thông tin giảng viên”. Phần đầu gồm avatar chữ viết tắt 64px, họ tên 18px/600, vai trò 13px, mã GV 12px.

Form hiển thị dạng lưới hai hoặc ba cột tùy chiều rộng: học hàm/học vị, email, điện thoại, bộ môn, Khoa, trạng thái. Các trường chỉ đọc từ dữ liệu quản lý phải khóa. Giới thiệu bản thân textarea min-height 80px.

Chỉ tiêu hướng dẫn — .at-panel

Các giá trị: chỉ tiêu GV, số đề tài đang phụ trách, số SV đang hướng dẫn, chỉ tiêu theo đề tài nếu model hỗ trợ. Mỗi chỉ tiêu một hàng 56px với nhãn bên trái, giá trị bên phải.

Không tự tạo trường “Số lượng tối đa đề tài” nếu backend chỉ lưu max_students. Trường nào không có dữ liệu thì không hiện như một input giả.

Khi đợt đóng và backend khóa chỉ tiêu: .at-banner “Không thể chỉnh sửa chỉ tiêu trong trạng thái hiện tại”. Không tự suy luận CLOSED luôn khóa mọi thông tin hồ sơ.

Chuyên môn — .at-panel + .at-chip

Danh sách lĩnh vực chuyên môn dưới dạng checkbox/chip; wrap nhiều dòng, gap 8px. Từ khóa nghiên cứu chỉ xuất hiện nếu hệ thống lưu và cho sửa. Không tạo danh mục lĩnh vực mới ngoài dữ liệu của Khoa.

Thống kê lĩnh vực — .at-panel

Danh sách thanh ngang theo số đề tài từng lĩnh vực, tối đa 5 lĩnh vực hiển thị đầu tiên theo số lượng giảm dần; thanh cao 8px, mỗi hàng min-height 36px, có tên lĩnh vực và số đếm.

Không hiển thị phân bố giả khi thiếu dữ liệu hoặc khi một đề tài thuộc nhiều lĩnh vực mà backend chưa có quy tắc đếm.

Trạng thái

Rỗng: chưa có chuyên môn/giới thiệu → hiển thị văn bản “Chưa cập nhật”, CTA sửa nếu cho phép.

Ít dữ liệu: một lĩnh vực → một thanh; không tạo bốn thanh còn lại.

Chữ dài: email, từ khóa và lĩnh vực tự xuống dòng, không cắt nội dung dữ liệu.

Chỉ xem: khi backend khóa sửa, giữ đầy đủ thông tin; ẩn nút Chỉnh sửa và thao tác thêm/xóa.

Lỗi dữ liệu: không hiển thị số 0 thay cho các chỉ tiêu không được cung cấp; phân biệt “0” và “Chưa có dữ liệu”.

Điện thoại dưới 768px

Thứ tự: Header → Thông tin GV → Chuyên môn → Chỉ tiêu hướng dẫn → Thống kê lĩnh vực → Bottom Navigation.

Form một cột, avatar 56px. Checkbox lĩnh vực chia tối đa 2 cột nếu nhãn ngắn; tự xuống một cột khi nhãn dài. Thanh thống kê hiển thị đủ tên và giá trị.

Khi vào chế độ chỉnh sửa form dài, Action Bar lưu thay Bottom Navigation, tuân thủ safe area.

Thành phần mới

Class

	

Thông số




.at-lecturer-profile-head

	

Display flex; align-items:center; gap 16px; padding 16px




.at-lecturer-avatar

	

64×64px desktop, 56×56px mobile; radius 50%; font 20px/600




.at-lecturer-fields

	

Grid 3 cột desktop; gap 16px; mobile 1 cột




.at-supervision-quota-row

	

Min-height 56px; display grid; grid-template-columns minmax(0,1fr) 120px; gap 12px




.at-expertise-picker

	

Display flex; flex-wrap:wrap; gap 8px; padding 16px




.at-field-stat-row

	

Min-height 36px; grid minmax(120px,1fr) minmax(80px,1.2fr) 52px; gap 12px; progress height 8px

TIÊU CHÍ NGHIỆM THU — NHÓM GV

#

	

Điều kiện đo được




1

	

Đủ 5 màn desktop và m16 mobile; đúng menu 3 mục, logo M, không có chuông và nút giả.




2

	

Screenshot 1440×900 và 390px không tràn ngang, không chồng nội dung; các breakpoint 768/992/1200 hoạt động.




3

	

Trang GV Tổng quan có Ledger 4 chỉ số và chỉ đếm dữ liệu thuộc GV đăng nhập.




4

	

Trang Đề tài có tìm kiếm/lọc, phân trang server-side 20 dòng, giữ query; Thêm/Sửa theo quyền.




5

	

Form đề tài lưu đúng kỹ năng 1–5, trọng số, cờ bắt buộc, GPA, tiên quyết và chỉ tiêu; không mất dữ liệu khi validation lỗi.




6

	

Drawer desktop đúng 440px; mobile 100dvh; body cuộn riêng, footer hai nút cùng hàng và không có Bottom Navigation phía dưới.




7

	

M1–M5 đúng nhãn; điểm và trọng số từ backend; M5 null không biến thành 0; điều kiện học thuật hiển thị rõ.




8

	

Từ chối yêu cầu lý do 5–500 ký tự, validation server-side; chấp thuận/từ chối kiểm quyền và trạng thái backend.




9

	

CLOSED/PUBLISHED và các trường hợp chỉ xem không hiển thị thao tác bị cấm; không có route hoặc dữ liệu tự tạo.




10

	

QA có screenshot Light/Dark, kiểm tra WCAG AA, kiểm thử form/drawer/duyệt; không lỗi JavaScript, CSRF hoặc HTTP 500 trong các luồng chính.

KẾT LUẬN: Hợp đồng này khóa thiết kế cho nhóm Giảng viên ATLAS V3.5. Lập trình viên sử dụng component sẵn có, chỉ bổ sung các class bố cục đã liệt kê; không được tự thay đổi kích thước, thứ tự khối hay trạng thái nghiệp vụ.