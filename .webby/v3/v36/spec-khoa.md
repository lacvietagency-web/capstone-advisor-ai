HỢP ĐỒNG CÀI ĐẶT ATLAS V3.5 — NHÓM KHOA

Trạng thái: DESIGN AUTHORITY APPROVED
Phạm vi: 18-khoa-tong-quan, 19-khoa-phan-cong, 20-khoa-thong-ke, 21-khoa-nhap-excel và m19-khoa-phan-cong.

Hiệu lực: Bổ sung hợp đồng nhóm Chung, Sinh viên và Giảng viên. Thông số trong hợp đồng này ghi đè V3.5 cũ khi có xung đột.

Quy tắc chung nhóm Khoa

Shell: Sidebar 216px, topbar 56px, canvas #F2F5FB, panel trắng, header panel 42px, logo chữ M đã duyệt.

Menu Khoa: Tổng quan (house), Phân công (users), Thống kê (chart-no-axes-column), Nhập Excel (file-spreadsheet), Giảng viên (graduation-cap), Quản trị (settings-2). Chỉ hiện các mục có route và quyền thực tế.

Desktop: Lưới 12 cột, gap 16px, padding nội dung 24px tại ≥1200px; nội dung max-width 1600px.

Mobile: Dưới 768px, padding ngang 16px, grid một cột, gap 12px. Bottom Navigation 64px + safe area, tối đa bốn mục: Tổng quan, Phân công, Thống kê, Quản trị.

Bảng dữ liệu: Server-side pagination mặc định 20 dòng/trang; hàng cao tối thiểu 44px; chữ 13px. Không render 100 sinh viên trong một trang.

Biểu đồ: Chart.js với sáu màu V3.5, không sử dụng donut/ring chart. Label và legend dùng --at-ink.

Nghiệp vụ: ILP, Greedy, xếp tay pha 2, xác nhận công bố hai bước; quyền, trạng thái và ràng buộc được kiểm tra phía backend.

Loại bỏ: Chuông, các nút giả, số liệu hardcode, biểu tượng KPI tròn, thông tin không tồn tại trong CSDL.

Các con số 100 SV, 50 đề tài, 43% đã xếp, 30% NV1, 43% Top 3, 63,8 điểm và 57 chờ pha 2 chỉ là dữ liệu đợt tham chiếu. Không đưa các giá trị này thành hằng số trong template.

18-khoa-tong-quan — Bảng điều khiển Khoa
Lưới desktop

Hàng

	

Khối

	

Cột/12

	

Min-height




1

	

Page Header: Bảng điều khiển Khoa + nút Mở trang phân công

	

12

	

72px




2

	

Đợt đăng ký + trạng thái

	

12

	

88px




3

	

Tổng quan số liệu — Metric Ledger

	

12

	

120px




4

	

Các đợt đăng ký

	

7

	

320px




4

	

Lối tắt thao tác

	

5

	

320px

Từng khối

Page Header — .at-page-heading

Tiêu đề “Bảng điều khiển Khoa”; mô tả “Tổng quan hệ thống phân công đề tài tốt nghiệp cho sinh viên”.

Nút “Mở trang phân công” kiểu primary, căn phải. Không hiển thị nút tạo đợt nếu backend chưa hỗ trợ.

Đợt đăng ký — .at-period

Tên đợt, trạng thái, ngày bắt đầu/kết thúc. Vùng trái chiếm 55%, vùng phải 45%, có divider đứng. Nội dung bên phải giải thích tình trạng đăng ký hoặc phân công hiện tại.

Metric Ledger — .at-ledger

Bốn chỉ số trên một hàng, mỗi ô 25%:

Chỉ số

	

Ví dụ tham chiếu

	

Nguồn dữ liệu




Sinh viên

	

100

	

Số SV thuộc đợt




Đề tài

	

50

	

Số đề tài hợp lệ thuộc đợt




Đợt đăng ký

	

1

	

Số đợt hiện có




Sinh viên có NV

	

100

	

Số SV duy nhất đã nộp/lưu NV theo quy tắc nghiệp vụ

Số lớn 32px/600, nhãn 13px, chú thích 12px. Dùng đường phân cách 1px, không chia thành bốn card độc lập.

Các đợt đăng ký — .at-panel + .at-table

Header “Các đợt đăng ký”, chiều cao 42px.

Cột

	

Rộng




Đợt đăng ký

	

38%




Thời gian

	

27%




Sinh viên

	

13%




Trạng thái

	

22%

Hàng min-height 48px. Tên đợt dùng 14px/600; thời gian và trạng thái dùng 13px. Nếu có nhiều hơn 10 đợt, phân trang server-side; không hiển thị danh sách không giới hạn.

Lối tắt thao tác — .at-panel + .at-list

Bốn hàng, mỗi hàng min-height 64px, padding 12px 16px:

Phân công đề tài → route phân công.

Thống kê & Báo cáo → route thống kê.

Nhập dữ liệu Excel → route nhập Excel.

Quản trị hệ thống → route quản trị, nếu tồn tại.

Mỗi hàng có Lucide 18px, tên 14px/600, mô tả 12px và chevron-right. Không dùng nút lớn khác màu cho từng lối tắt.

Trạng thái

Rỗng: chưa có đợt → .at-empty “Chưa có đợt đăng ký”; không hiển thị ngày/đợt giả.

Ít dữ liệu: một đợt → một hàng bảng; không nhân bản.

Chữ dài: tên đợt xuống tối đa hai dòng; tooltip hoặc chi tiết cho nội dung đầy đủ.

Chỉ xem: cán bộ thiếu quyền vận hành chỉ xem ledger và danh sách, ẩn các hành động bị cấm.

Điện thoại dưới 768px

Thứ tự: Header → Period → Metric Ledger 2×2 → Các đợt đăng ký dạng .at-list → Lối tắt thao tác → Bottom Navigation.

Bảng chuyển thành danh sách, mỗi item min-height 88px, gồm tên đợt, thời gian, số SV và trạng thái.

Thành phần mới

Class

	

Thông số




.at-faculty-overview-ledger

	

4 cột desktop; 2 cột mobile; gap 0; padding 16px




.at-faculty-period-item

	

Min-height 88px; padding 12px 16px; gap 8px




.at-faculty-quicklink

	

Min-height 64px; padding 12px 16px; display grid; grid-template-columns 20px minmax(0,1fr) 20px; gap 12px

19-khoa-phan-cong — Phân công đề tài tốt nghiệp
Lưới desktop

Hàng

	

Khối

	

Cột/12

	

Min-height




1

	

Page Header + chọn đợt + Chạy Greedy / Chạy tối ưu ILP

	

12

	

72px




2

	

Đợt đăng ký + trạng thái

	

12

	

88px




3

	

Metric Ledger 6 chỉ số

	

12

	

74px




4

	

Kết quả theo nguyện vọng — biểu đồ cột

	

8

	

200px




4

	

Chốt & công bố

	

4

	

200px




5

	

Danh sách sinh viên + toolbar + bảng

	

12

	

Theo số hàng




6

	

Phân trang

	

12

	

52px




Phủ khi mở

	

Drawer chi tiết/xếp tay

	

440px

	

100dvh




Phủ khi xác nhận

	

Modal công bố hai bước

	

480px

	

Theo nội dung

Từng khối

Page Header — .at-page-heading

Tiêu đề “Phân công đề tài”, mô tả một dòng. Nhóm thao tác bên phải:

Select đợt đăng ký: width 228px, height 38px.

Chạy Greedy: secondary, cao 38px.

Chạy tối ưu ILP: primary, cao 38px.

Gap giữa các nút 8px. Khi thiếu quyền hoặc trạng thái không cho chạy thuật toán, ẩn/khóa đúng theo backend. Không để thao tác chạy tối ưu kích hoạt hai lần khi request đang xử lý.

Period — .at-period

Vùng trái tên đợt/trạng thái/thời gian 55%; vùng phải giải thích tình hình phân công 45%.

Metric Ledger — .at-ledger

Sáu chỉ số một hàng, mỗi ô 16,667%:

Thứ tự

	

Chỉ số

	

Giá trị tham chiếu




1

	

Sinh viên

	

100




2

	

Đã xếp

	

43%




3

	

Đạt NV1

	

30%




4

	

Top 3

	

43%




5

	

Điểm TB

	

63,8




6

	

Chờ pha 2

	

57

Số 28px/600, nhãn 12px. Ledger cao 74px, padding dọc 10px. Phân cách bằng divider 1px.

Quy tắc tính: Các tỷ lệ phải có mẫu số và phạm vi đợt thống nhất. Đã xếp là số SV có allocation hợp lệ chia tổng SV xét phân công; Top 3 dựa trên preference_rank 1–3; Điểm TB dựa trên match_score của những assignment được tính. Hiển thị chú thích/mẫu số khi cần để tránh hiểu sai.

Biểu đồ — .at-panel + Chart.js

Header “Kết quả theo nguyện vọng”, chart canvas cao 140px nằm trong panel min-height 200px. Biểu đồ cột dọc, năm nhãn NV1, NV2, NV3, Ngoài NV, Chưa xếp.

Cần lưu ý: nếu quy tắc ILP cấm phân công ngoài nguyện vọng, “Ngoài NV” không phải một loại phân công ILP hợp lệ; chỉ hiển thị khi có bản ghi Manual được phép và nguồn dữ liệu xác nhận. Nếu không có, giá trị là 0 hoặc loại bỏ nhóm này theo báo cáo nghiệp vụ.

Chart có nhãn số phía trên cột, lưới ngang 1px và chú giải khi cần. Không dùng donut/ring.

Chốt & công bố — .at-panel

Header 42px, nội dung mô tả tối đa 3 dòng. Hai nút trên một hàng:

“Xem kiểm tra” secondary nếu có trang hoặc modal kiểm tra thực tế.

“Chốt & công bố” primary nếu backend cho phép.

Nút công bố mở quy trình xác nhận hai bước, không POST ngay từ click đầu.

Danh sách sinh viên — .at-panel + .at-table

Header “Danh sách sinh viên” và toolbar cùng vùng section; desktop một hàng công cụ.

Toolbar:

Thành phần

	

Phần chiều rộng




Tìm kiếm MSSV/họ tên

	

25%




Trạng thái

	

16%




Nguyện vọng

	

16%




Giảng viên

	

20%




Lĩnh vực / khoảng điểm nếu backend hỗ trợ

	

15%




Số kết quả

	

8%

Gap 8px, input/select 38px.

Thứ tự và độ rộng cột bảng:

Cột

	

Rộng




Mã SV

	

9%




Họ và tên

	

13%




Đề tài phân công

	

25%




Giảng viên

	

14%




NV đạt

	

7%




Điểm tổng

	

8%




Nguồn

	

8%




Trạng thái

	

9%




Thao tác

	

7%

Hàng min-height 44px; tên đề tài dài cho xuống tối đa hai dòng, hàng tự tăng chiều cao. Dòng chưa xếp không tô đỏ/hồng toàn hàng; chỉ có badge “Chờ pha 2”.

Trường hợp chưa xếp không được hiển thị tên đề tài hay giảng viên giả trong cột allocation. Nếu muốn xem NV1–NV3 của SV chưa xếp, mở drawer.

Hành động “Xem” mở drawer; “Xếp tay” chỉ hiện với SV đủ điều kiện pha 2 và người dùng có quyền.

Phân trang

Server-side 20 dòng/trang mặc định, chọn 10/20/50 nếu backend hỗ trợ. Giữ query khi chuyển trang: đợt, q, status, rank, lecturer_id, field_id, score_min, score_max, sort.

Drawer và xác nhận

Drawer 440px: Header 56px; thông tin SV; ba NV đã nộp; kết quả kiểm tra điều kiện; các đề tài còn chỉ tiêu phù hợp; hành động xếp tay. GET bất đồng bộ dữ liệu một SV khi mở.

Xếp tay chỉ được chọn đề tài thuộc nguyện vọng hợp lệ, đáp ứng điều kiện, capacity và quota. Backend phải kiểm lại trước khi ghi.

Modal công bố: Rộng 480px, hai bước. Bước 1 xác nhận số đã xếp/chưa xếp, trạng thái đợt và các cảnh báo. Bước 2 nhập chính xác CÔNG BỐ, sau đó gửi POST. Client khóa nút sai chuỗi; backend kiểm quyền, trạng thái và tính hợp lệ. Không coi kiểm tra chuỗi ở UI là biện pháp bảo vệ duy nhất.

Trạng thái

Rỗng: chưa chạy phân công → ledger và trạng thái đúng dữ liệu, bảng/biểu đồ hiện hướng dẫn, không tạo kết quả giả.

Ít dữ liệu: 1–19 SV → bảng co theo số dòng, không thêm hàng giả.

Chữ dài: đề tài xuống tối đa hai dòng ở bảng; đầy đủ trong drawer.

Chỉ xem: PUBLISHED hiển thị kết quả chính thức; ẩn Chạy ILP/Greedy, Xếp tay, Chốt & công bố nếu backend không cho phép thao tác nữa.

Chạy lâu: nút “Đang tối ưu…” khóa bấm lặp; không dùng skeleton toàn trang.

Lỗi solver: hiển thị lỗi thực tế ở banner, không tự thay ILP bằng Greedy mà không thông báo.

Điện thoại dưới 768px — m19

Thứ tự: Header → Period → hai nút Chạy tối ưu ILP/Chạy Greedy → Metric Ledger 2 cột × 3 hàng → Biểu đồ → Danh sách SV → Phân trang → Chốt & công bố (chỉ khi được phép) → Bottom Navigation.

Metric Ledger giữ dải số liệu phẳng, chia bằng divider; không biến thành sáu KPI card có icon.

Bảng chuyển sang .at-list: mỗi sinh viên một item có tên, MSSV, đề tài, GVHD, NV đạt, điểm, nguồn, trạng thái và Chi tiết.

Bộ lọc dùng bottom sheet tối đa 85dvh.

Khi drawer xếp tay mở: full-screen 100dvh, ẩn Bottom Navigation, footer hành động 72px + safe area.

Các nút ILP/Greedy cao 44px, hiển thị cùng hàng khi đủ rộng; không chồng lên nhau.

Thành phần mới

Class

	

Thông số




.at-allocation-actions

	

Display flex; align-items:center; gap 8px; select width 228px; mobile grid 2 cột




.at-allocation-ledger

	

6 cột desktop, 2 cột mobile; min-height 74px desktop; divider 1px




.at-allocation-chart

	

Height 140px desktop; 180px mobile; position relative




.at-allocation-toolbar

	

Display grid; gap 8px; align-items:end; mobile thay bằng search + filter trigger




.at-allocation-student-item

	

Padding 12px 16px; min-height 112px; gap 8px; radius 6px




.at-manual-assign-footer

	

Min-height 72px; padding 12px 16px; gap 12px; mobile thêm safe area




.at-publish-summary

	

Grid 2 cột; gap 12px; padding 16px; mobile 1 cột

20-khoa-thong-ke — Thống kê Khoa
Lưới desktop

Hàng

	

Khối

	

Cột/12

	

Min-height




1

	

Page Header: Thống kê Khoa

	

12

	

72px




2

	

Đợt đăng ký + trạng thái

	

12

	

88px




3

	

Tổng quan đăng ký và phân công — Ledger

	

12

	

104px




4

	

Kết quả theo nguyện vọng

	

7

	

316px




4

	

Phân bố lĩnh vực

	

5

	

316px




5

	

Tải GV so với chỉ tiêu

	

6

	

316px




5

	

So sánh ILP và Greedy

	

6

	

316px




6

	

Bảng kiểm chứng chi tiết, nếu cần

	

12

	

Theo số hàng

Từng khối

Page Header — .at-page-heading

H1 “Thống kê Khoa”, mô tả tình hình đăng ký và phân công. Không thêm nút Xuất báo cáo nếu backend chưa có chức năng.

Đợt đăng ký — .at-period

Tên đợt, trạng thái và thời gian lấy từ CSDL. Phần phải trình bày phạm vi số liệu.

Ledger — .at-ledger

Sáu chỉ số, mỗi ô chiếm 16,667%:

Sinh viên 100; Đề tài 50; Đã xếp 43; Chờ pha 2 là 57; Giảng viên 15; Đạt NV1 30%.

Dữ liệu lấy động theo đợt. Số lớn 28px/600, nhãn 12px. Không có icon tròn.

Kết quả theo nguyện vọng — .at-panel + Chart.js + .at-table

Biểu đồ cột, cao 150px. Bảng ngay dưới biểu đồ, min-height 108px.

Cột bảng

	

Rộng




Chỉ số

	

19%




NV1

	

13,5%




NV2

	

13,5%




NV3

	

13,5%




Ngoài NV

	

13,5%




Chưa xếp

	

13,5%




Tổng

	

13,5%

Phân nhóm phải loại trừ lẫn nhau. 43 SV đã xếp và 57 chưa xếp phải cộng thành 100 SV. Số liệu minh họa mâu thuẫn giữa các ảnh không được sao chép nguyên vào biểu đồ.

Nếu backend cấm xếp ngoài nguyện vọng, cột Ngoài NV chỉ có thể xuất hiện khi tồn tại nguồn phân công khác hợp lệ; không tự tạo số lượng.

Phân bố lĩnh vực — .at-panel

Biểu đồ thanh ngang cao 150px, tối đa 5 lĩnh vực hiển thị đầu tiên; bên dưới bảng 3 cột:

Lĩnh vực

	

Số đề tài

	

Tỷ lệ




58%

	

21%

	

21%

Tỷ lệ dùng mẫu số là số đề tài thuộc phạm vi thống kê. Nếu mỗi đề tài có một lĩnh vực chính, tổng tỷ lệ bằng 100%; nếu có nhiều lĩnh vực, ghi rõ cách đếm.

Tải GV so với chỉ tiêu — .at-panel

Biểu đồ cột nhóm, cao 150px, hai series “Đã nhận” và “Chỉ tiêu”. Hiển thị tối đa 5 giảng viên đầu tiên theo thứ tự tải thực tế.

Bảng dưới biểu đồ:

Giảng viên

	

Đã nhận

	

Chỉ tiêu

	

Tỷ lệ




40%

	

20%

	

20%

	

20%

Không nhầm chỉ tiêu sinh viên của GV với capacity của từng đề tài.

So sánh ILP và Greedy — .at-panel

Biểu đồ cột nhóm cao 150px, hai series ILP/Greedy. Bốn chỉ số: Đã xếp, Đạt NV1, Top 3, Điểm TB.

Bảng phía dưới:

Chỉ số

	

ILP

	

Greedy




50%

	

25%

	

25%

Dữ liệu so sánh phải thuộc cùng bộ đầu vào, cùng ràng buộc và cùng phạm vi thực nghiệm. Nếu chỉ lưu kết quả của thuật toán được chạy cuối, không tự suy ra kết quả thuật toán còn lại.

Lưu ý: Không vẽ chỉ số điểm trung bình thang 100 cạnh tỷ lệ phần trăm mà không có nhãn đơn vị hoặc chú giải thang đo.

Trạng thái

Rỗng: chưa có kết quả tối ưu → vẫn hiển thị số liệu đăng ký; các biểu đồ phân công dùng .at-empty.

Ít dữ liệu: một lĩnh vực/GV → hiển thị đúng một thanh, không thêm thanh mẫu.

Chữ dài: nhãn biểu đồ rút gọn khi cần; tên đầy đủ có trong bảng bên dưới.

Chỉ xem: thống kê vẫn được truy cập theo quyền; không có nút chạy thuật toán hoặc chỉnh sửa trực tiếp.

Thiếu dữ liệu so sánh: hiển thị “Chưa có đủ kết quả ILP và Greedy để so sánh”, không dùng số liệu mẫu.

Điện thoại dưới 768px

Thứ tự: Header → Period → Ledger 2×3 → Kết quả NV → Phân bố lĩnh vực → Tải GV → ILP/Greedy → Bảng kiểm chứng nếu có → Bottom Navigation.

Biểu đồ thanh dọc cao tối thiểu 220px; biểu đồ thanh ngang cao tối thiểu 200px. Các bảng được chuyển thành danh sách số liệu hoặc cuộn ngang trong panel khi cần giữ đối chiếu cột.

Không đặt hai biểu đồ cạnh nhau trên viewport 390px.

Thành phần mới

Class

	

Thông số




.at-statistics-ledger

	

6 cột desktop, 2 cột mobile; padding 16px; divider 1px




.at-stat-chart

	

Height 150px desktop; min-height 200px mobile; position relative




.at-stat-chart-scroll

	

Width 100%; overflow-x:auto; bảng không kéo giãn viewport




.at-stat-data-table

	

Width 100%; font 12px/19px ở header, 13px/21px ở body; margin-top 12px




.at-stat-empty

	

Min-height 150px; display flex; align-items:center; justify-content:center; padding 20px

21-khoa-nhap-excel — Nhập dữ liệu Excel
Lưới desktop

Hàng

	

Khối

	

Cột/12

	

Min-height




1

	

Page Header: Nhập Excel

	

12

	

72px




2

	

Hướng dẫn

	

8

	

190px




2

	

Tải mẫu

	

4

	

190px




3

	

Tải lên

	

12

	

178px




4

	

Kết quả kiểm tra + bảng lỗi

	

12

	

288px




5

	

Xác nhận nhập

	

12

	

72px

Không thêm wizard nhiều trang. Toàn bộ quy trình trên một trang, tuần tự từ trên xuống.

Từng khối

Page Header

H1 “Nhập Excel”, mô tả “Nhận dữ liệu sinh viên, giảng viên, đề tài từ tệp Excel”.

Hướng dẫn — .at-panel

Bốn bước, mỗi hàng min-height 34px, số thứ tự 28×28px:

Tải đúng tệp mẫu.

Điền dữ liệu theo cấu trúc yêu cầu.

Tải tệp và kiểm tra lỗi.

Xác nhận nhập dữ liệu hợp lệ.

Vùng phải trong panel dành cho định dạng hỗ trợ và dung lượng tối đa, lấy từ backend/config thực. Không mặc định hỗ trợ CSV hoặc giới hạn 10MB chỉ vì ảnh thể hiện như vậy.

Tải mẫu — .at-panel

Các hành động tải mẫu Sinh viên, Giảng viên, Đề tài; sắp xếp hai cột khi đủ rộng, gap 12px, nút cao 38px. Chỉ xuất hiện tệp mẫu có endpoint hoặc file tĩnh thực tế.

Tải lên — .at-panel

Chia hai vùng 60%/40%:

Trái: drop zone min-height 114px, viền nét đứt 2px, icon upload 28px, hướng dẫn chọn tệp.

Phải: tên tệp đã chọn, dung lượng, nút Chọn tệp và “Tải lên & kiểm tra”.

Các loại tệp hợp lệ, giới hạn dung lượng và cách đọc file phải theo chức năng backend đang hỗ trợ.

Kết quả kiểm tra — .at-panel

Dải chỉ số phẳng 3 ô: Tổng dòng, Hợp lệ, Có lỗi. Min-height 72px, chữ số 24px/600, không dùng ba KPI card icon tròn.

Bảng lỗi:

Cột

	

Rộng




Dòng

	

8%




Loại dữ liệu

	

16%




Mức độ

	

12%




Lỗi

	

39%




Gợi ý sửa

	

25%

Hàng min-height 44px. Mã lỗi/mô tả phải lấy từ kết quả validator thực, không tự tạo lý do. Lỗi có thể dài nên cell được xuống dòng và chiều cao hàng tự tăng.

Mặc định hiển thị 20 lỗi/trang khi backend hỗ trợ phân trang kết quả kiểm tra.

Xác nhận nhập — .at-panel

Thông tin “Dữ liệu hợp lệ sẽ được ghi vào đợt đang chọn”, nút Hủy secondary và Xác nhận nhập primary ở bên phải.

Không cho xác nhận khi chưa kiểm tra file, kiểm tra thất bại hoặc không có dữ liệu hợp lệ. Việc nhập một phần file lỗi hay buộc sửa toàn bộ phải theo chính sách backend; UI không tự bỏ qua hàng lỗi.

Trạng thái

Rỗng: chưa chọn file → drop zone hướng dẫn; chưa có bảng kết quả.

Đã chọn tệp: hiển thị tên, dung lượng và hành động xóa lựa chọn.

Đang kiểm tra: khóa nút, hiện “Đang kiểm tra dữ liệu…”.

Có lỗi: hiển thị tổng số lỗi, số dòng, vị trí lỗi và cách sửa nếu backend cung cấp.

Hợp lệ: cho phép xác nhận nhập; số lượng cập nhật theo dữ liệu kiểm tra.

Chữ dài: tên file tối đa hai dòng, bảng lỗi xuống dòng đầy đủ.

Chỉ xem: không đủ quyền nhập → chỉ hiển thị hướng dẫn và tệp mẫu nếu được phép; ẩn khu vực upload/xác nhận.

Lỗi server: thông báo thất bại; không kết luận file đã được nhập khi chưa có xác nhận backend.

Điện thoại dưới 768px

Thứ tự: Header → Hướng dẫn → Tải mẫu → Tải lên → Kết quả kiểm tra → Danh sách lỗi → Xác nhận nhập → Bottom Navigation.

Drop zone và thông tin file xếp dọc. Các nút tải mẫu một cột; bảng lỗi chuyển thành .at-list, mỗi lỗi hiển thị số dòng, loại, mức độ, nội dung và gợi ý sửa.

Khi xác nhận nhập bằng Action Bar cố định, ẩn Bottom Navigation. Với màn hình nhập nhiều lỗi, không neo nút xác nhận cho đến khi có kết quả kiểm tra hợp lệ.

Thành phần mới

Class

	

Thông số




.at-import-instructions

	

Grid minmax(0,1.5fr) minmax(0,1fr); gap 16px; mobile một cột




.at-import-step

	

Min-height 34px; gap 12px; padding 4px 0




.at-import-step-number

	

Width/height 28px; radius 50%; font 13px/600




.at-import-templates

	

Grid 2 cột; gap 12px; mobile một cột




.at-import-upload

	

Grid 3fr 2fr; gap 16px; mobile một cột




.at-import-dropzone

	

Min-height 114px; border 2px dashed --at-control-border; radius 6px; padding 20px; text-align:center




.at-import-file-summary

	

Display flex; flex-direction:column; gap 12px; min-width 0




.at-import-validation-ledger

	

Grid 3 cột; min-height 72px; padding 12px; mobile giữ 3 cột nếu chữ vừa




.at-import-error-item

	

Padding 12px 16px; gap 8px; min-height 88px




.at-import-confirm

	

Min-height 72px; padding 12px 16px; display flex; justify-content:space-between; gap 12px

TIÊU CHÍ NGHIỆM THU — NHÓM KHOA

#

	

Điều kiện đo được




1

	

Đủ bốn màn desktop 18–21 và mobile m19; logo M và menu Khoa đúng; không có chuông hoặc hành động giả.




2

	

Screenshot 1440×900 và viewport 390px không tràn ngang, chồng nút hay che nội dung; kiểm tra thêm 768/992/1200px.




3

	

Trang Tổng quan hiển thị đúng dữ liệu đợt đang chọn; Ledger và bảng đợt không hardcode.




4

	

Trang Phân công hiển thị 6 chỉ số đúng CSDL; số đã xếp + chưa xếp nhất quán với tổng SV xét phân công.




5

	

Bảng phân công có tìm kiếm, lọc, phân trang server-side mặc định 20 dòng; giữ query khi chuyển trang.




6

	

Chạy ILP/Greedy xử lý đúng trạng thái, khóa submit lặp; không tạo kết quả giả hoặc âm thầm thay thuật toán.




7

	

Drawer xếp tay desktop 440px, mobile 100dvh; kiểm tra NV, eligibility, capacity, quota và quyền ở backend.




8

	

Công bố phải qua hai bước xác nhận; dữ liệu DRAFT không lộ cho SV; PUBLISHED khóa thao tác trái phép.




9

	

Thống kê có bốn biểu đồ đúng nguồn dữ liệu và bảng kiểm chứng; so sánh ILP/Greedy chỉ xuất hiện khi đủ kết quả thực.




10

	

Nhập Excel kiểm tra loại file, lỗi dòng, quyền và kết quả nhập; QA Light/Dark, WCAG AA, không lỗi JS/CSRF/HTTP 500 trong luồng chính.

KẾT LUẬN: HỢP ĐỒNG NHÓM KHOA ATLAS V3.5 ĐƯỢC KHÓA.

Lập trình viên phải dùng các component ATLAS hiện có, chỉ bổ sung class bố cục đã chỉ định trong static/css/atlas.css. Không thay đổi kiến trúc backend, không tạo trang mới để khớp ảnh, không sao chép số liệu minh họa thành dữ liệu thật.