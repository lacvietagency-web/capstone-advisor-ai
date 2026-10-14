HỢP ĐỒNG CÀI ĐẶT ATLAS V3.5 — NHÓM SINH VIÊN

Trạng thái: DESIGN AUTHORITY APPROVED
Phạm vi: 07–12 và các bản mobile m07, m09, m10, m11.
Hiệu lực: Bổ sung hợp đồng nhóm Chung; ghi đè thông số V3.5 cũ nếu có xung đột.

Quy tắc chung cho 6 màn SV

Shell: sidebar 216px, topbar 56px, canvas #F2F5FB, panel trắng, header panel tối thiểu 42px. Logo chữ M. Menu SV đúng 5 mục.

Desktop: grid 12 cột, gap 16px, section gap 16px, content padding 24px tại ≥1200px.

Mobile: dưới 768px một cột, padding ngang 16px, gap 12px; bottom navigation 64px + safe area, tối đa 4 mục: Tổng quan, Đề tài, Nguyện vọng, Kết quả.

Điểm AI: xanh #176B60; M1 Kỹ năng, M2 Học lực, M3 Lĩnh vực, M4 Ngữ nghĩa, M5 Đánh giá LLM; trọng số AHP 25%/20%/15%/20%/20%. M5 chưa có phải hiển thị điểm sơ bộ M1–M4, không tự giả lập M5.

Dữ liệu: lấy từ CSDL theo sinh viên đăng nhập và đợt đang chọn. Các số trong ảnh chỉ là dữ liệu tham chiếu trực quan.

Loại bỏ: chuông thông báo, logo cũ, nút không có chức năng, liên kết không có route. Không tự sinh nội dung AI, điểm, thời hạn hoặc trạng thái duyệt.

07-sv-trang-chu — Trang chủ sinh viên
Lưới desktop

Hàng

	

Khối

	

Cột/12

	

Min-height




1

	

Page Header: lời chào, MSSV, ngành, GPA, nút Hồ sơ năng lực

	

12

	

72px




2

	

Đợt đăng ký + trạng thái

	

12

	

88px




3

	

Hành trình đăng ký 4 bước

	

12

	

192px




4

	

Đề tài phù hợp nhất + Top 5

	

8

	

440px




4

	

Nguyện vọng đã nộp NV1–NV3

	

4

	

440px

Các khối hàng 4 căn đỉnh; min-height không có nghĩa phải kéo dài khi nội dung rỗng.

Từng khối

Page Header — .at-page-heading

H1 “Xin chào, [họ tên]”, bên dưới MSSV, ngành, GPA trên một hàng, ngăn cách bằng divider đứng cao 14px. Nút Hồ sơ năng lực kiểu secondary, căn phải, chỉ một nút.

Đợt đăng ký — .at-period

Bên trái chiếm 55%, bên phải 45%, ngăn bằng divider đứng. Hiển thị tên đợt, trạng thái, ngày bắt đầu/kết thúc, thông điệp hướng dẫn. Không dùng số ngày còn lại tính từ dữ liệu mẫu.

Hành trình — .at-journey

Bốn bước chia đều 25% chiều rộng. Mỗi bước gồm icon số/check 40×40px, tiêu đề 14px/600, badge trạng thái 24px và mô tả tối đa 2 dòng. Đường nối 2px; hoàn thành xanh dương, chưa tới bước dùng nét đứt. Trạng thái phải suy ra từ dữ liệu hồ sơ, gợi ý, nguyện vọng và công bố.

Top 5 — .at-panel + .at-evidence + .at-score + .at-list

Header “Đề tài phù hợp nhất”, hành động “Xem chi tiết đề tài” nếu có route.

Đề tài #1 dùng một Evidence Panel riêng, bố cục nội bộ: thông tin đề tài 60%, điểm AI và M1–M5 40%. Thứ tự: rank #1 → tên đề tài → GVHD → điểm lớn → lý do → 5 thanh mô hình. Điểm chính 40px/600. Evidence bar 7px, năm hàng cách nhau 8px.

Bốn đề tài #2–#5 hiển thị thành danh sách gọn, mỗi hàng min-height 46px: thứ hạng 36px, tên đề tài co giãn, GVHD, điểm AI 14px/600 và chevron-right. Không lặp 5 Evidence Panel lớn.

Nguyện vọng — .at-panel + .at-list + .at-chip

Ba hàng NV1/NV2/NV3, mỗi hàng min-height 116px, padding 16px. Bố cục chip NV 48px → tên đề tài + GVHD → trạng thái; thời điểm nộp nằm dưới nội dung chính.

Trạng thái “Đã nộp” là trạng thái của nguyện vọng, không được thay bằng “Chờ duyệt” chỉ vì giảng viên chưa phản hồi. Nếu cần hiển thị cả hai, dùng hai thông tin có nhãn riêng.

Trạng thái

Rỗng: chưa có gợi ý → dùng .at-empty với CTA hoàn thiện hồ sơ nếu thực sự thiếu; chưa nộp NV → hiện “Bạn chưa nộp nguyện vọng”, CTA chọn đề tài khi đợt đang mở.

Ít dữ liệu: có 1–4 gợi ý → hiển thị đúng số lượng, không thêm hàng giả.

Chữ dài: tên đề tài tối đa 2 dòng trong hàng gọn; có link xem toàn bộ. Phần tên đề tài nổi bật được xuống dòng đầy đủ.

Chỉ xem: đợt CLOSED/PUBLISHED vẫn hiển thị Top 5 và NV lịch sử; ẩn thao tác chỉnh sửa nếu không được phép. Journey vẫn giữ đúng trạng thái đã hoàn thành.

Điện thoại dưới 768px — m07

Thứ tự: Header → shortcut Hồ sơ năng lực → Period → Journey → Đề tài nổi bật → danh sách #2–#5 → Nguyện vọng → Bottom Navigation.

Journey hiển thị bốn bước nằm ngang với icon 32px, nhãn ngắn tối đa 2 dòng; bỏ mô tả dài của từng bước. Evidence Panel chuyển một cột, 5 hàng M1–M5 dọc. Nguyện vọng dùng ba hàng, min-height 76px/hàng, không dùng ba card lồng riêng biệt.

Thành phần mới

Class

	

Thông số




.at-student-identity

	

Display flex; gap 12px; min-height 72px; responsive wrap




.at-featured-topic

	

Padding 16px; border 1px solid --at-line; radius 6px; grid 3fr 2fr; gap 16px; mobile 1fr




.at-topic-compact

	

Min-height 46px; padding 10px 12px; grid 36px minmax(0,1fr) auto 20px; gap 10px




.at-preference-summary

	

Min-height 116px; padding 16px; gap 12px; mobile min-height 76px

08-sv-ho-so — Hồ sơ năng lực
Lưới desktop

Hàng

	

Khối

	

Cột/12

	

Min-height




1

	

Page Header + trạng thái hoàn thiện

	

12

	

72px




2

	

Thông tin sinh viên

	

8

	

152px




2

	

Tình trạng hồ sơ

	

4

	

152px




3

	

Giới thiệu bản thân

	

12

	

160px




4

	

Kỹ năng chuyên môn

	

12

	

Theo số hàng




5

	

Lĩnh vực quan tâm

	

12

	

132px




6

	

Thanh hành động lưu

	

12

	

72px

Từng khối

Thông tin SV — .at-panel

Dữ liệu readonly: họ tên, MSSV, ngành, GPA; desktop bố trí 2 cột, gap 16px. Không cho sửa dữ liệu học vụ thuộc quyền quản lý của Khoa.

Tình trạng hồ sơ — .at-panel

Hiển thị đã đủ/chưa đủ điều kiện tạo gợi ý, số kỹ năng khai báo và số lĩnh vực quan tâm. Không sử dụng biểu đồ tròn phần trăm hoàn thiện nếu backend không có tiêu chí tính rõ ràng.

Giới thiệu — .at-panel

Textarea min-height 112px; mô tả mục tiêu, năng lực, kinh nghiệm. Không ép số từ hoặc tạo giới hạn ký tự không có trong backend.

Kỹ năng — .at-panel + .at-table

Cột

	

Rộng




Kỹ năng

	

46%




Mức năng lực 1–5

	

38%




Xóa

	

16%

Mỗi hàng min-height 52px. Mức kỹ năng hiển thị tên mức cùng số: 1 — Mới bắt đầu; 2 — Cơ bản; 3 — Khá; 4 — Tốt; 5 — Thành thạo. Nút Thêm kỹ năng đặt trong header panel. Không thêm hai kỹ năng trùng.

Lĩnh vực quan tâm — .at-panel

Chọn 1–3 lĩnh vực theo quy tắc backend. Chip được chọn có checkbox hoặc dấu check; tên lĩnh vực dài được xuống dòng. Hiển thị bộ đếm “2/3 lĩnh vực” nếu phù hợp.

Thanh lưu

Nút Lưu hồ sơ là primary; trạng thái xử lý “Đang lưu…”. Sau khi lưu thành công, hệ thống cập nhật trạng thái và chỉ tính lại gợi ý bằng cơ chế backend hiện có.

Trạng thái

Rỗng: skills/interests chưa có → hướng dẫn thêm; không điền giả.

Ít dữ liệu: một kỹ năng hoặc một lĩnh vực vẫn hiển thị bình thường, thiếu tiêu chí nào thì báo đúng tiêu chí đó.

Chữ dài: tên kỹ năng/lĩnh vực xuống dòng; textarea tăng chiều cao.

Chỉ xem: khóa trường khi backend không cho chỉnh sửa, giữ hiển thị đầy đủ hồ sơ; ẩn nút lưu và nút xóa.

Điện thoại dưới 768px

Thứ tự: Header → Tình trạng hồ sơ → Thông tin SV → Giới thiệu → Kỹ năng → Lĩnh vực → Action Bar.

Thông tin SV một cột; bảng kỹ năng chuyển thành danh sách: tên kỹ năng → select mức → nút xóa. Action Bar cao 72px, ẩn Bottom Navigation khi chỉnh sửa, tránh che ô nhập bởi bàn phím.

Thành phần mới

Class

	

Thông số




.at-skill-row

	

Desktop min-height 52px; mobile padding 12px; gap 12px




.at-skill-level

	

Min-width 220px desktop; mobile width 100%




.at-interest-picker

	

Display flex; flex-wrap:wrap; gap 8px




.at-profile-savebar

	

Min-height 72px; padding 12px 16px; border-top 1px --at-line; mobile fixed bottom + safe area

09-sv-nguyen-vong — Đăng ký NV1, NV2, NV3
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

	

Trạng thái đợt + thông báo lưu/nộp

	

12

	

88px




3

	

NV1

	

8

	

186px




3–5

	

Gợi ý AI Top 5

	

4

	

Theo nội dung




4

	

NV2

	

8

	

186px




5

	

NV3

	

8

	

186px




6

	

Lưu ý và kiểm tra trước khi nộp

	

12

	

88px




7

	

Thanh hành động

	

12

	

72px

Từng khối

Đợt đăng ký — .at-period + .at-banner

Tên đợt, thời hạn và trạng thái OPEN/CLOSED. Thông báo phân biệt: “Chưa lưu”, “Đã lưu nháp”, “Đã nộp chính thức”. Không đồng nhất trạng thái giảng viên duyệt với trạng thái nộp nguyện vọng.

NV1–NV3 — .at-panel + .at-chip + .at-evidence

Ba khối có cấu trúc giống nhau. Header cao 42px: chip NV 40×28px, tiêu đề “Nguyện vọng 1 (NV1)”, badge lưu/nộp ở phải.

Nội dung chia hai cột 58%/42%, cách 16px:

Trái: select chọn đề tài 100% chiều rộng; tên đề tài 15px/600, GVHD 13px; điểm phù hợp .at-score 32px; lý do ngắn tối đa 2 dòng.

Phải: checklist bốn điều kiện gồm GPA, kỹ năng bắt buộc, lĩnh vực quan tâm, chỉ tiêu. Mỗi hàng min-height 30px; dùng chữ “Cần ... / Hiện có ...” với điều kiện chưa đạt.

Điểm AI đầy đủ/sơ bộ phải lấy đúng bản đánh giá của SV–đề tài.

Không cho chọn trùng đề tài giữa NV1–NV3. Đổi nguyện vọng phải cập nhật giá trị có kiểm soát, không thay đổi ngầm thứ tự các NV khác.

Gợi ý AI — .at-panel + .at-list

Top 5 sắp xếp theo điểm phù hợp giảm dần. Mỗi hàng min-height 68px, gồm thứ hạng 32px, tên đề tài tối đa 2 dòng, GVHD một dòng và điểm AI 16px/600. Đề tài đang nằm trong NV được đánh dấu “Đã chọn NV1/NV2/NV3”.

Thanh hành động

“Lưu nháp” secondary và “Nộp nguyện vọng” primary; chỉ hiển thị hành động có backend hỗ trợ. Nếu hệ thống chỉ có một POST lưu, không tạo nút Nộp riêng giả.

Trạng thái

Rỗng: chưa chọn NV nào → ba slot trống có hướng dẫn; không tự điền Top 3.

Ít dữ liệu: có một hoặc hai NV → giữ slot chưa chọn nếu đợt mở và cho phép nộp thiếu NV theo quy tắc backend.

Chữ dài: tên đề tài tối đa 3 dòng trong khối NV; lý do dài xem ở chi tiết.

Chỉ xem: CLOSED/PUBLISHED hiển thị lại NV đã lưu/nộp theo thứ tự, điểm và trạng thái tương ứng; ẩn select, xóa, lưu và nộp. Không hiển thị “Chưa có đợt nào” nếu có dữ liệu lịch sử.

Điện thoại dưới 768px — m09

Thứ tự: Header → Period → Journey thu gọn → NV1 → NV2 → NV3 → Gợi ý AI → Action Bar.

Ba khối NV thành một cột; tên đề tài trên cùng, điểm 32px phía dưới, checklist dọc; không để nội dung cuộn ngang. Action Bar chỉ có “Lưu nguyện vọng” nếu đó là thao tác backend thực. Thanh này thay Bottom Navigation, không xếp chồng.

Thành phần mới

Class

	

Thông số




.at-preference-slot

	

Min-height 186px; padding 16px; grid minmax(0,1.4fr) minmax(0,1fr); gap 16px




.at-preference-eligibility

	

Display grid; gap 6px; row min-height 30px




.at-preference-actionbar

	

Min-height 72px; padding 12px 16px; mobile fixed bottom, safe-area; desktop theo luồng




.at-suggestion-row

	

Min-height 68px; padding 12px; gap 10px

10-sv-danh-sach-de-tai — Danh sách đề tài tốt nghiệp
Lưới desktop

Hàng

	

Khối

	

Cột/12

	

Min-height




1

	

Page Header + số đề tài

	

12

	

72px




2

	

Period

	

12

	

88px




3

	

Toolbar tìm kiếm và lọc

	

12

	

106px




4

	

Tabs Tất cả/Đủ điều kiện/Chưa đủ điều kiện

	

12

	

48px




5

	

Bảng đề tài

	

12

	

Theo số hàng




6

	

Phân trang

	

12

	

52px

Từng khối

Toolbar — .at-panel + .form-control + .form-select

Tìm kiếm chiếm 34% chiều rộng; Lĩnh vực 22%, Giảng viên 22%, Độ khó 22%. Input/select cao 38px. Filter theo GET backend, có khả năng kết hợp; thay đổi filter reset page=1.

Tabs — .at-tabs

Tất cả (50), Đủ điều kiện (32), Chưa đủ điều kiện (18) trong dữ liệu ảnh tham chiếu; số đếm thực tế phải tính từ CSDL cho sinh viên hiện tại. Tab cao 44px, active gạch dưới 2px hoặc bề mặt active thống nhất V3.5.

Bảng — .at-table

Cột

	

Rộng




Đề tài + nhãn lĩnh vực

	

24%




Giảng viên hướng dẫn

	

15%




Độ khó

	

9%




Chỉ tiêu / số NV1

	

11%




Điểm AI

	

12%




Điều kiện

	

18%




Thao tác

	

11%

Table header 12px/600, body 13px/21px, min-height mỗi dòng 60px để chứa tên đề tài hai dòng và nhãn lĩnh vực. Tên đề tài 14px/600; nhãn lĩnh vực 12px.

Cột AI dùng điểm số 16px/600 xanh #176B60 và hậu tố /100, không có biểu đồ tròn.

Cột điều kiện: đạt → badge “Đủ điều kiện”; không đạt → diễn giải cụ thể “Cần Python mức 4, bạn có 3”. Nhiều lý do thì hiện lý do đầu tiên và số lượng còn lại; chi tiết hiển thị đầy đủ.

Cột hành động ưu tiên một nút “Chi tiết”. Đăng ký chỉ khả dụng nếu đúng điều kiện và đợt đang mở. Không cho thao tác đăng ký khi không đạt điều kiện bắt buộc.

Phân trang

20 đề tài/trang mặc định, giữ q, field_id, lecturer_id, difficulty, eligibility, sort trong URL khi chuyển trang.

Trạng thái

Rỗng: không có đề tài → .at-empty “Chưa có đề tài trong đợt”.

Ít dữ liệu: ít hơn 20 kết quả → ẩn pagination nhiều trang, không thêm hàng giả.

Chữ dài: tên đề tài tối đa 2 dòng trong bảng, tooltip/title hoặc trang chi tiết cung cấp tên đầy đủ; lý do điều kiện không được cắt mất giá trị bắt buộc và thực tế.

Chỉ xem: CLOSED/PUBLISHED vẫn xem được danh mục khi được phép; ẩn hoặc khóa đăng ký. Chưa có hồ sơ hoàn chỉnh → không tạo điểm AI, hiển thị hướng dẫn cập nhật.

Điện thoại dưới 768px — m10

Thứ tự: Header → Period → Tìm kiếm → nút mở bộ lọc → danh sách đề tài → Phân trang → Bottom Navigation.

Ẩn bảng desktop, thay bằng .at-list với mỗi đề tài một item có viền, padding 16px:

Hàng tên đề tài + điểm AI nổi bật.

GVHD và nhãn lĩnh vực.

Checklist điều kiện 2 cột nếu đủ rộng; tự chuyển một cột khi nội dung dài.

Link “Chi tiết”.

Bộ lọc mở bottom sheet tối đa 85dvh. Không đặt bốn select liên tiếp chiếm toàn bộ chiều cao trước danh sách.

Thành phần mới

Class

	

Thông số




.at-topic-toolbar

	

Grid 34% 22% 22% 22%; gap 12px; padding 16px; mobile 1fr




.at-topic-mobile-item

	

Padding 16px; gap 12px; border 1px solid --at-line; radius 6px




.at-topic-tags

	

Display flex; flex-wrap:wrap; gap 6px




.at-eligibility-summary

	

Font 12px/19px; max 3 dòng trong card mobile; đầy đủ trong chi tiết




.at-mobile-filter-sheet

	

Max-height 85dvh; padding 20px 16px + safe area; radius đỉnh 16px

11-sv-chi-tiet-de-tai — Chi tiết đề tài và phân tích AI
Lưới desktop

Hàng

	

Khối

	

Cột/12

	

Min-height




1

	

Breadcrumb + Page Header + Đăng ký NV

	

12

	

96px




2

	

Thông tin đề tài: GVHD, lĩnh vực, độ khó, chỉ tiêu

	

12

	

88px




3

	

Mô tả đề tài

	

7

	

180px




3

	

Phân tích M1–M5

	

5

	

300px




4

	

Kỹ năng yêu cầu

	

7

	

Theo số hàng




4

	

Lý do gợi ý AI

	

5

	

144px




5

	

Điều kiện tiên quyết

	

7

	

Theo số hàng




5

	

Kiểm tra đủ điều kiện

	

5

	

Theo số hàng

Cột trái/phải căn đỉnh, không ép các khối cùng chiều cao nếu nội dung khác nhau.

Từng khối

Page Header

Breadcrumb “Đề tài / Chi tiết đề tài”, tên đề tài H1 24px/600, thông tin ngắn; nút “Đăng ký nguyện vọng” ở phải khi được phép.

Thông tin đề tài — .at-panel

Một dải bốn nhóm: GVHD 30%, lĩnh vực 25%, độ khó 15%, chỉ tiêu 15%, từ khóa 15%. Chiều cao tối thiểu 88px. Dữ liệu đầy đủ từ topic và lecturer; không tạo thông tin khoa/bộ môn không tồn tại trong CSDL.

Mô tả — .at-panel

Header “Mô tả đề tài”; mô tả, mục tiêu và công nghệ nếu dữ liệu nguồn có. Text 14px/23px; padding 16px. Không tự viết mô tả thay giảng viên.

Kỹ năng yêu cầu — .at-table

Cột

	

Rộng




Kỹ năng

	

35%




Mức yêu cầu 1–5

	

20%




Trọng số kỹ năng

	

20%




Bắt buộc

	

25%

Hàng min-height 44px, tối đa 20 hàng/trang nếu dữ liệu thực vượt quá giới hạn hiển thị hợp lý. Giá trị bắt buộc dùng Có/Không; không chỉ thể hiện bằng màu.

Điều kiện tiên quyết — .at-table

Cột Học phần 45%, Điểm yêu cầu 25%, Kết quả của SV 30%. Các tiêu chí không có trong dữ liệu không được thêm vào bảng.

Phân tích AI — .at-evidence + .at-score

Điểm tổng 40px/600, màu AI. Năm hàng M1–M5 theo thứ tự đã khóa, tên đầy đủ, điểm 0–100; thanh cao 7px, chiều rộng linh hoạt. Trọng số AHP 25/20/15/20/20% trình bày trong hàng chú thích dưới khối.

Nếu m5=null, hiển thị “Điểm sơ bộ M1–M4” theo cơ chế tính hiện có, M5 “Chưa đánh giá”. Không được biến null thành 0.

Lý do gợi ý — .at-note

Tối đa ba luận điểm ở phần tóm tắt; nếu backend có nhiều hơn, hiển thị mở rộng bằng văn bản. Không suy diễn rằng một kỹ năng đạt chỉ dựa trên điểm tổng cao.

Kiểm tra điều kiện — .at-list

Các điều kiện GPA, kỹ năng bắt buộc, học phần tiên quyết, chỉ tiêu; chỉ hiển thị tiêu chí áp dụng thực tế. Mỗi hàng min-height 36px, có biểu tượng, nội dung, kết quả thực và yêu cầu tương ứng khi chưa đạt.

Trạng thái

Rỗng: đề tài không tồn tại → 404; không có recommendation → “Chưa có điểm phù hợp”, không tự tạo 79,6.

Ít dữ liệu: không yêu cầu kỹ năng/học phần → hiện “Đề tài không quy định điều kiện này” trong đúng section, không ẩn các điều kiện khác.

Chữ dài: tên đề tài xuống tối đa 3 dòng ở header; nội dung mô tả hiển thị đầy đủ và giữ ngắt đoạn.

Chỉ xem: CLOSED/PUBLISHED ẩn nút đăng ký, vẫn hiển thị đề tài, M1–M5 nếu người dùng được phép xem. Không dùng điểm AI để vượt qua điều kiện bắt buộc.

Điện thoại dưới 768px — m11

Thứ tự: Header → Period → Tên đề tài + GVHD/tags → CTA đăng ký nếu hợp lệ → Thông tin đề tài → Phân tích AI → Kiểm tra điều kiện → Lý do AI → Mô tả → Kỹ năng → Học phần tiên quyết → Bottom Navigation.

Ưu tiên điểm AI và điều kiện trong viewport đầu sau thông tin cơ bản. Điều này có hiệu lực cao hơn thứ tự desktop nếu cần tối ưu chiều dài cuộn.

M1–M5 xếp 5 hàng dọc, mỗi hàng tên + thanh 7px + điểm; bảng kỹ năng và học phần chuyển sang danh sách có nhãn, không thu nhỏ chữ.

Thành phần mới

Class

	

Thông số




.at-topic-meta

	

Grid 30% 25% 15% 15% 15%; padding 16px; gap 0; mobile 2 cột, gap 12px




.at-topic-description

	

Padding 16px; font 14px/23px; paragraph gap 12px




.at-evidence-summary

	

Grid minmax(150px,0.85fr) minmax(0,1.15fr); gap 16px; mobile một cột




.at-prerequisite-item

	

Min-height 52px; padding 12px 16px; border-bottom 1px --at-line

12-sv-ket-qua — Kết quả phân công đề tài
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

	

Đợt đăng ký — trạng thái công bố

	

12

	

88px




3

	

Hành trình 4 bước

	

12

	

156px




4

	

Kết quả phân công chính thức

	

12

	

310px




5

	

Nguyện vọng đã nộp

	

12

	

150px




6

	

Hành động xem chi tiết

	

12

	

48px

Màn này không dùng Metric Ledger hoặc nhiều card KPI. Chỉ có một panel kết quả chính, đúng ảnh được duyệt.

Từng khối

Period — .at-period

Trạng thái PUBLISHED hiển thị “Đã công bố”. Thời gian công bố chỉ hiện khi backend cung cấp timestamp có thể xác minh; không tự tạo published_at.

Journey — .at-journey

Bốn bước hoàn thành: Hồ sơ năng lực, Gợi ý AI, Nguyện vọng, Kết quả phân công. Bước 4 dùng nhãn “Đã công bố” khi PUBLISHED. Journey hiển thị theo dữ liệu thực, không dựa vào việc người dùng đang xem route /ket-qua.

Kết quả chính thức — .at-panel

Header “Kết quả phân công chính thức”. Bên dưới là thông tin đề tài được xếp, GVHD và các badge:

“Đạt NV1/NV2/NV3” nếu đề tài được phân công đúng nguyện vọng đã nộp.

“Chính thức” nếu kết quả đã được công bố.

Nguồn ILP/Greedy/Manual chỉ khi backend có source.

Panel chia ba vùng desktop: điểm AI 25%, Evidence M1–M5 30%, kết quả + lý do/thông tin chính thức 45%, gap 16px.

Điểm tổng 40px/600; M1–M5 năm hàng 7px. Ngày công bố không được suy luận từ thời điểm truy cập.

Nguyện vọng đã nộp — .at-list

Ba hàng NV1/NV2/NV3, mỗi hàng min-height 40px; chip NV 44px, tên đề tài, GVHD và trạng thái. Với NV được xếp: “Đạt”; các NV khác không được gắn “Không đạt” nếu hệ thống không thực hiện đánh giá/từ chối riêng. Ưu tiên ghi “Không được phân công” khi cần giải thích kết quả.

Hành động

Nút “Xem chi tiết đề tài” nếu route tồn tại. Nút “Tải biên bản” chỉ được hiển thị khi có chức năng xuất/tải thật. Không tạo PDF giả hoặc nút trang trí.

Trạng thái

Chưa công bố: hiện .at-banner “Kết quả chưa được công bố”; không lộ allocations DRAFT, không hiện điểm/đề tài phân công nháp. Vẫn xem được NV đã nộp.

Đã công bố và được xếp: hiển thị đề tài, GVHD, NV đạt, điểm và trạng thái chính thức.

Đã công bố nhưng chưa xếp: hiện “Chưa được phân công đề tài”, lý do chính thức nếu backend cung cấp, cùng ba NV đã nộp; không tự quy kết do học lực hoặc năng lực.

Không có nguyện vọng: hiển thị thông báo tương ứng, không tạo NV1–NV3 giả.

Chữ dài: tên đề tài được xuống dòng đầy đủ trong panel chính.

Chỉ xem: toàn bộ kết quả PUBLISHED chỉ đọc; không có nút thay đổi nguyện vọng, chấp thuận hoặc từ chối.

Điện thoại dưới 768px

Thứ tự: Header → Period → Journey thu gọn → Kết quả chính thức → Điểm AI → M1–M5 → Thông tin/lý do phân công → NV đã nộp → Xem chi tiết → Bottom Navigation.

Panel chính một cột; điểm số đặt phía trên năm thanh evidence. NV chuyển thành danh sách ba hàng. Không hiển thị nút tải nếu chưa có backend.

Thành phần mới

Class

	

Thông số




.at-allocation-result

	

Padding 16px; grid minmax(0,1fr) minmax(0,1.2fr) minmax(0,1.8fr); gap 16px; mobile một cột




.at-result-topic

	

Font 18px/28px/600; margin-bottom 8px; không truncate




.at-result-facts

	

Display flex; flex-wrap:wrap; gap 8px; margin-bottom 12px




.at-submitted-preference

	

Min-height 40px; padding 8px 12px; grid 44px minmax(0,1fr) auto; gap 12px; mobile tự wrap




.at-result-actions

	

Display flex; justify-content:flex-end; gap 8px; mobile nút full-width

KHÓA NGHIỆM THU NHÓM SV

#

	

Điều kiện nghiệm thu đo được




1

	

Đủ 6 màn desktop và 4 bản mobile, giữ logo M, đúng menu theo vai trò; không có chuông hoặc nút giả.




2

	

Screenshot 1440×900 và viewport 390px không tràn ngang; mobile không có bảng nghiệp vụ rộng vượt viewport.




3

	

Hành trình 4 bước chính xác theo dữ liệu; sau PUBLISHED không báo đang ở bước Gợi ý AI.




4

	

Top 5 hiển thị đúng số đề tài backend trả về, không sinh điểm, tên hoặc lý do giả.




5

	

M1–M5 đúng tên; M5 null hiển thị chưa đánh giá; trọng số theo đúng phiên bản được lưu, không hardcode nếu phiên bản thay đổi.




6

	

NV1–NV3 không trùng đề tài; chỉ sửa khi backend cho phép; CLOSED/PUBLISHED vẫn xem được NV đã nộp.




7

	

Danh sách đề tài lọc/tìm kiếm/phân trang server-side 20 dòng mặc định; điều kiện không đạt có giá trị yêu cầu và thực tế.




8

	

Trang kết quả không lộ DRAFT; trường hợp chưa xếp, chưa công bố và đã xếp đều hiển thị đúng.




9

	

Mobile Action Bar và Bottom Navigation không xuất hiện đồng thời; touch target tối thiểu 44px, safe area không che nút.




10

	

Không có lỗi JavaScript, Django template hoặc HTTP 500 trong các luồng chính; form và link thực hiện đúng quyền, CSRF và backend validation.

Kết luận: Các thông số trên là hợp đồng cài đặt có hiệu lực cho nhóm Sinh viên ATLAS V3.5. Các lớp component chung giữ nguyên; chỉ thêm class bố cục đã chỉ định, không phát sinh design system khác.