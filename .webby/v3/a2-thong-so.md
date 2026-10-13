ATLAS — DESIGN SPECIFICATION V3.3
Design Authority: APPROVED

Dự án: Capstone Advisor AI · Django + Bootstrap 5.3 · Light/Dark

Nguyên tắc thực thi: Tài liệu này là nguồn thông số thiết kế duy nhất cho phiên bản ATLAS V3.3. Lập trình viên không tự thay màu, phông, khoảng cách, bán kính, layout hoặc trạng thái tương tác. Nếu thông số xung đột, ưu tiên quy tắc cụ thể của từng thành phần, sau đó đến quy tắc khung trang và cuối cùng là token toàn cục.

Phạm vi gồm 21 màn hình thực tế: 6 màn hình chung, 6 sinh viên, 5 giảng viên, 4 Khoa. Con số 18 trong hồ sơ ban đầu không khớp số màn hình được liệt kê.

=== PHẦN 1: BIẾN CSS ===

1.1. Hệ màu chính thức

Chốt hệ màu Academic Paper cho sáng và Graphite Study cho tối.

ATLAS · Light

84,2

Điểm phù hợp AI

ATLAS · Dark

84,2

Điểm phù hợp AI

CSS tokens — Light
CSS

:root,
[data-bs-theme="light"] {
  color-scheme: light;

  --at-canvas: #F6F4EE;
  --at-surface: #FFFEFA;
  --at-surface-2: #F0F1EB;
  --at-surface-hover: #E9EEE7;
  --at-ink: #222923;
  --at-ink-muted: #626D65;
  --at-ink-subtle: #626D65;
  --at-line: #D9DDD4;
  --at-line-strong: #AEB9AF;

  --at-brand: #305F52;
  --at-brand-hover: #244C41;
  --at-brand-pressed: #193B32;
  --at-on-brand: #FFFFFF;
  --at-brand-soft: #E5ECE5;
  --at-ai: #386D80;
  --at-ai-soft: #E5F0F3;

  --at-success: #246548;
  --at-success-soft: #E5F0E7;
  --at-warning: #925A31;
  --at-warning-soft: #F5EADC;
  --at-danger: #A23B35;
  --at-danger-hover: #842F2B;
  --at-danger-soft: #F7EAE7;
  --at-info: #2B617A;
  --at-info-soft: #E5F0F5;

  --at-chart-1: #305F52;
  --at-chart-2: #386D80;
  --at-chart-3: #94653E;
  --at-chart-4: #83699A;
  --at-chart-5: #4D7F78;
  --at-chart-6: #777B43;

  --at-focus: #386D80;
  --at-focus-ring: #386D804D;
  --at-overlay: #111A17A6;
  --at-shadow-color: 25, 37, 30;
}

CSS tokens — Dark
CSS

[data-bs-theme="dark"] {
  color-scheme: dark;

  --at-canvas: #151B19;
  --at-surface: #202724;
  --at-surface-2: #29322D;
  --at-surface-hover: #303D35;
  --at-ink: #ECEFE8;
  --at-ink-muted: #A8B4AB;
  --at-ink-subtle: #A8B4AB;
  --at-line: #39443E;
  --at-line-strong: #65776B;

  --at-brand: #8BB8A4;
  --at-brand-hover: #A6CDBB;
  --at-brand-pressed: #C0DBCE;
  --at-on-brand: #151B19;
  --at-brand-soft: #293F35;
  --at-ai: #8DBFD0;
  --at-ai-soft: #243F4A;

  --at-success: #A6D2B8;
  --at-success-soft: #233D30;
  --at-warning: #F0C58A;
  --at-warning-soft: #493827;
  --at-danger: #F4A9A2;
  --at-danger-hover: #FFC6BF;
  --at-danger-soft: #4C2C2B;
  --at-info: #8DBFD0;
  --at-info-soft: #243F4A;

  --at-chart-1: #8BB8A4;
  --at-chart-2: #8DBFD0;
  --at-chart-3: #E0AF80;
  --at-chart-4: #BEA4D2;
  --at-chart-5: #86B8AF;
  --at-chart-6: #BEC68A;

  --at-focus: #8DBFD0;
  --at-focus-ring: #8DBFD059;
  --at-overlay: #000000B8;
  --at-shadow-color: 0, 0, 0;
}

Typography, spacing, radius, shadow, motion

Dùng duy nhất Be Vietnam Pro, tự đóng gói các độ đậm 400, 500, 600, 700 và bảo đảm có bộ ký tự tiếng Việt. Không dùng Inter, Space Grotesk hoặc Noto Sans.

CSS

:root {
  --at-font: "Be Vietnam Pro", Arial, sans-serif;

  --at-h1-size: 32px;
  --at-h1-line: 42px;
  --at-h1-weight: 600;

  --at-h2-size: 24px;
  --at-h2-line: 34px;
  --at-h2-weight: 600;

  --at-h3-size: 19px;
  --at-h3-line: 28px;
  --at-h3-weight: 600;

  --at-body-size: 14px;
  --at-body-line: 23px;
  --at-body-weight: 400;

  --at-secondary-size: 13px;
  --at-secondary-line: 21px;
  --at-secondary-weight: 400;

  --at-label-size: 12px;
  --at-label-line: 19px;
  --at-label-weight: 600;

  --at-metric-size: 44px;
  --at-metric-line: 52px;
  --at-metric-weight: 600;

  --at-space-0: 0px;
  --at-space-1: 4px;
  --at-space-2: 8px;
  --at-space-3: 12px;
  --at-space-4: 16px;
  --at-space-5: 20px;
  --at-space-6: 24px;
  --at-space-8: 32px;
  --at-space-10: 40px;
  --at-space-12: 48px;
  --at-space-16: 64px;

  --at-radius-xs: 3px;
  --at-radius-sm: 5px;
  --at-radius-md: 8px;
  --at-radius-lg: 12px;
  --at-radius-xl: 16px;
  --at-radius-pill: 999px;

  --at-shadow-none: none;
  --at-shadow-sm:
    0 2px 8px rgba(var(--at-shadow-color), .06);
  --at-shadow-md:
    0 12px 32px rgba(var(--at-shadow-color), .14);

  --at-duration-fast: 120ms;
  --at-duration-normal: 180ms;
  --at-duration-overlay: 220ms;
  --at-duration-data: 240ms;
  --at-easing: cubic-bezier(.2, .7, .2, 1);
}


Mặc định: body dùng --at-body-size, nền --at-canvas, chữ --at-ink. Thẻ h1/h2/h3 dùng đúng biến tương ứng; letter-spacing: -0.015em chỉ áp dụng cho h1/h2 và số liệu lớn, không áp dụng cho thân bài. Phông chữ tuyệt đối không nhỏ hơn 12px ở nội dung nghiệp vụ.

Kiểm tra tương phản WCAG AA

Ngưỡng WCAG AA: tối thiểu 4,5:1 cho chữ thường, 3:1 cho chữ lớn. Các kết quả sau là độ tương phản tính theo sRGB cho các cặp màu đã chỉ định.

Cặp chữ / nền

	

Tỉ lệ

	

Kết quả




Light Ink / Canvas

	

13,55:1

	

Đạt AAA




Light Muted / Canvas

	

4,90:1

	

Đạt AA




Forest / Surface

	

7,21:1

	

Đạt AAA




Trắng / Forest

	

7,28:1

	

Đạt AAA




Warning / Surface

	

5,58:1

	

Đạt AA




Danger / Surface

	

6,48:1

	

Đạt AA




Success / Surface

	

6,87:1

	

Đạt AA




Info / Surface

	

6,73:1

	

Đạt AA




Dark Ink / Canvas

	

15,03:1

	

Đạt AAA




Dark Muted / Surface

	

7,10:1

	

Đạt AAA




Dark Brand / Surface

	

6,89:1

	

Đạt AAA




Dark AI / Surface

	

7,62:1

	

Đạt AAA

Quy định tương phản: Cặp màu trên là các cặp đã được kiểm tra, không phải bảo đảm cho mọi tổ hợp token. Màu biểu đồ và màu nền trạng thái không tự động hợp lệ để làm chữ. Badge phải dùng màu chữ trạng thái trên nền trạng thái tương ứng và được kiểm tra lại khi triển khai. Trạng thái disabled không dùng để truyền tải thông tin quan trọng duy nhất. Icon, viền focus và các chỉ dấu phi văn bản quan trọng cần đạt tương phản tối thiểu 3:1.

=== PHẦN 2: KHUNG TRANG ===

2.1. Desktop ≥ 992px

Hình học điều hướng ATLAS

Context Index

Bộ lọc / mục lục

Tất cả

Chưa xử lý

Main Canvas

Tiêu đề · Dữ liệu · Thao tác

Minh họa vai trò ba vùng; kích thước lập trình lấy theo bảng dưới.

Thuộc tính

	

Thông số




Topbar

	

Cao 60px; fixed/sticky top 0; z-index 1030




Navigation Rail

	

Rộng 68px; top 60px; bottom 0; fixed




Context Index

	

Rộng 224px; top 60px; bottom 0; độc lập cuộn




Main Canvas

	

Phần còn lại; có min-width: 0




Content max-width

	

1480px, tính trong Main Canvas




Content padding

	

32px ngang; 32px trên; 48px dưới




Khoảng cách section

	

32px




Khoảng cách trong section

	

20–24px




Desktop grid

	

12 cột; gutter 24px




Trang đọc hồ sơ/form

	

Nội dung chính max 880px




Trang bảng Khoa

	

Dùng 100% chiều rộng còn lại




Footer

	

Tối thiểu 56px, không cố định




Độ cao tối thiểu nội dung

	

calc(100dvh - 60px)

Rail gồm logo biểu tượng ở đầu, các điểm điều hướng theo vai trò, cài đặt ở cuối. Icon 20px, vùng nhấn 44×44px, khoảng cách giữa các vùng 6px. Mục đang chọn có nền --at-brand-soft trong chế độ sáng phù hợp với rail nền sáng hoặc màu sáng tương phản riêng nếu rail nền Forest; luôn có một vạch nhận biết rộng 3px.

Quyết định màu rail: nền --at-brand chỉ ở Light; trong Dark dùng --at-surface để tránh rail sáng chiếm ưu thế. Icon rail Light dùng màu trắng với độ tương phản hợp lệ, Dark dùng --at-ink. Không dùng trực tiếp màu chữ tối trên rail Forest.

Quy tắc Context Index

Context Index không phải menu cấp hai bắt buộc ở tất cả trang. Chỉ bật cho danh sách đề tài, danh sách đăng ký GV, phân công, thống kê và nhập Excel nhiều bước. Các trang chủ, hồ sơ, kết quả, form và lỗi tắt Context Index; Main Canvas tự mở rộng. Nút thu gọn Index nằm trong đầu vùng Index, kích thước 36px.

Bố cục theo độ rộng

Viewport

	

Rail

	

Context Index

	

Lề Canvas

	

Grid




≥ 1400px

	

68px

	

224px khi bật

	

40px

	

12 cột, gutter 24




1200–1399px

	

68px

	

224px khi bật

	

32px

	

12 cột, gutter 20




992–1199px

	

68px

	

Mặc định thu gọn

	

24px

	

12 cột, gutter 16




768–991px

	

Không

	

Offcanvas theo nhu cầu

	

24px

	

8 cột, gutter 16




576–767px

	

Không

	

Offcanvas

	

20px

	

4 cột, gutter 12




Dưới 576px

	

Không

	

Offcanvas

	

16px

	

4 cột, gutter 12

Ở 768–991px dùng topbar + menu mở bằng nút list-ordered hoặc layout-dashboard (ưu tiên layout-dashboard) cùng offcanvas, không thu nhỏ rail 68px. Đây là cấu hình chính thức cho khoảng breakpoint trung gian.

2.2. Mobile dưới 768px

Header: cao 56px, sticky top, viền dưới 1px, logo dạng chữ rút gọn và nút tài khoản.

Bottom navigation: cao 64px + env(safe-area-inset-bottom), fixed bottom, 4 mục, mỗi mục rộng 25%.

Nội dung: padding-top: 20px; padding-bottom: calc(96px + env(safe-area-inset-bottom)), tăng thêm khi có action bar cố định.

Main Canvas rộng 100%; không dùng 100vw cho phần tử có padding.

Grid: 4 cột với gutter 12px; khối lớn trải hết 4 cột; form một cột.

Bottom action bar: cao tối thiểu 72px, nằm phía trên bottom navigation, có viền trên và nền đặc, 1 hành động chính + tối đa 1 hành động phụ.

Touch target tối thiểu 44×44px; khoảng cách hai hành động tối thiểu 8px.

Bảng nhiều cột phải chuyển thành danh sách hoặc cuộn trong vùng bảng có chủ đích, không kéo ngang cả viewport.

Footer trên mobile là thông tin cuối nội dung, không lặp menu điều hướng.

2.3. Menu theo vai trò

Chỉ dùng icon Lucide có sẵn.

Vai trò

	

Mục

	

Icon




SV

	

Trang chủ

	

house




SV

	

Hồ sơ năng lực

	

user-round




SV

	

Danh sách đề tài

	

book-open




SV

	

Nguyện vọng

	

bookmark




SV

	

Kết quả

	

file-check-2




GV

	

Tổng quan

	

house




GV

	

Đề tài của tôi

	

book-open




GV

	

Sinh viên đăng ký

	

users-round




GV

	

Hồ sơ giảng viên

	

user-round




Khoa

	

Tổng quan

	

layout-dashboard




Khoa

	

Phân công

	

route




Khoa

	

Thống kê

	

chart-line




Khoa

	

Nhập Excel

	

file-spreadsheet




Khoa

	

Quản trị hệ thống nếu có route

	

settings-2

SV có 5 mục nên bottom nav chỉ giữ Trang chủ, Đề tài, Nguyện vọng, Kết quả; Hồ sơ vào header/tài khoản, đồng thời có lối vào rõ từ trang chủ. GV dùng đủ 4 mục. Khoa trên điện thoại dùng Trang chủ, Phân công, Thống kê, Thêm; mục Thêm mở sheet chứa Nhập Excel và Quản trị.

Không dùng menu có route chưa triển khai hoặc user không có quyền.

2.4. Tiêu đề trang và footer

Page header desktop: hàng đầu là breadcrumb 12px, cách tiêu đề 12px. Tiêu đề h1 32px; mô tả 14px, tối đa 2 dòng; hành động chính nằm góc phải, thẳng hàng với phần tiêu đề, cách ít nhất 24px. Chiều cao tự nhiên; margin-bottom 32px.

Page header mobile: breadcrumb chỉ giữ mục cha trực tiếp, h1 26px/36px; mô tả 13px; hành động chính xuống dưới hoặc đưa vào action bar. Khoảng cách sau header 24px. Không chèn nút dài bên cạnh h1.

Footer: đường viền trên 1px; chữ 12px; hiển thị “Capstone Advisor AI · Hệ thống hỗ trợ tư vấn và phân công đề tài tốt nghiệp” cùng thông tin phiên bản khi có. Nội dung căn hai bên desktop và xếp dọc mobile. Không thêm liên kết giả.

=== PHẦN 3: THÀNH PHẦN ===

3.1. Nguyên tắc chung

Tất cả thành phần dùng box-sizing: border-box. Không tự tạo shadow nếu không được chỉ định. Focus phải hiển thị rõ với người dùng bàn phím; hover không được là tín hiệu duy nhất. Trạng thái disabled và readonly phải phân biệt: disabled không tương tác, readonly vẫn có thể chọn và sao chép nội dung.

Không dùng nguyên màu Bootstrap mặc định cho btn, badge, pagination, form-control, alert, nav-tabs. Ánh xạ toàn bộ vào token ATLAS trong một file CSS.

3.2. Nút bấm

Chạy phân công

Xem chi tiết

Xóa dữ liệu

Chỉnh sửa thông tin

Thuộc tính

	

Regular

	

Small




Height

	

44px

	

36px




Padding X

	

16px

	

12px




Padding Y

	

0, căn giữa

	

0, căn giữa




Font

	

14px / 600

	

13px / 600




Icon

	

18px

	

16px




Gap icon-chữ

	

8px

	

6px




Border

	

1px

	

1px




Radius

	

6px

	

6px




Min-width

	

88px

	

72px

Bốn biến thể:

Primary: nền --at-brand, chữ --at-on-brand, không viền tương phản; hover --at-brand-hover, pressed --at-brand-pressed.

Secondary: nền --at-surface, viền --at-line-strong, chữ --at-ink; hover --at-surface-hover.

Danger: nền --at-danger, chữ trắng ở Light và --at-canvas ở Dark; hover dùng --at-danger-hover. Chỉ xuất hiện cho hành động phá hủy thực sự.

Text: nền trong suốt, chữ --at-brand; hover nền --at-brand-soft; không viền. Dùng cho thao tác ít quan trọng.

Focus dùng outline 2px --at-focus, outline-offset: 2px; có thể dùng ring 3px bằng token --at-focus-ring nếu giữ đủ tương phản với nền. Disabled giảm nhấn bằng màu nền --at-surface-2, chữ --at-ink-muted, viền --at-line, cursor not-allowed, không hover. Không đặt opacity dưới 0,65 cho toàn nút.

Nút có loading phải khóa thao tác lặp, giữ nguyên chiều rộng, có biểu tượng tiến trình và văn bản “Đang xử lý…”. Không đổi nhãn thành một spinner không có chữ.

3.3. Form, input và validation

Thuộc tính

	

Giá trị




Label

	

13px / 600 / line-height 21px




Khoảng cách label-input

	

6px




Input regular

	

Cao 44px




Input small

	

Cao 36px




Padding input

	

0 12px




Font input

	

14px / 400




Border

	

1px --at-line-strong




Radius

	

6px




Background

	

--at-surface




Focus

	

Border --at-focus + ring 3px




Error text

	

12px / 19px / --at-danger




Helper text

	

12px / 19px / --at-ink-muted




Gap helper/error

	

6px




Gap giữa các field

	

20px




Textarea

	

Min-height 112px, padding 12px




Select

	

Cao 44px, icon chevron-down 16px




Checkbox

	

18×18px; vùng nhấn tối thiểu 44px

Placeholder dùng --at-ink-muted; không thay thế label. Trường bắt buộc đánh dấu bằng chữ “Bắt buộc” hoặc ký hiệu có giải thích. Validation chỉ hiện sau blur hoặc submit lần đầu, không báo lỗi ngay khi người dùng chưa nhập.

Trường lỗi đổi màu viền và thông điệp, không phủ đỏ toàn form. Khi submit thất bại, focus vào trường không hợp lệ đầu tiên; thông báo tổng hợp ở đầu form chỉ dùng khi nhiều lỗi.

Form có dữ liệu dài dùng giới hạn ký tự và đếm số ký tự nếu có ràng buộc thật. Kỹ năng 1–5 dùng select/radio có nhãn mức rõ ràng, không chỉ hiển thị 5 ngôi sao.

3.4. Surface và card

Loại

	

Padding

	

Border

	

Radius

	

Shadow




Page section phẳng

	

0–24px

	

Bottom 1px khi cần

	

0

	

Không




Data panel

	

24px

	

1px --at-line

	

8px

	

Không




Mobile content panel

	

16px

	

1px --at-line

	

8px

	

Không




Item card

	

20px

	

1px --at-line

	

8px

	

Không




Popover

	

12px

	

1px --at-line

	

8px

	

Shadow-sm




Modal

	

24px

	

1px --at-line

	

12px

	

Shadow-md

Panel hover chỉ đổi border --at-line-strong khi toàn panel có thể click. Không tạo hiệu ứng hover trên khu vực tĩnh. Không lồng panel trong panel vượt một cấp. Nếu nội dung cần phân tách bên trong, dùng divider hoặc nền --at-surface-2 không thêm viền bao mới.

3.5. Metric Ledger

Dải số liệu có chiều cao theo nội dung, không tạo card KPI riêng lẻ.

Thuộc tính

	

Desktop

	

Mobile




Cột

	

4–6 chỉ số/hàng

	

2 chỉ số/hàng




Padding

	

20px 24px

	

16px




Số lớn

	

36px/44px, weight 600

	

30px/38px




Nhãn

	

12px/19px

	

12px/19px




Phụ chú

	

12px/19px

	

12px/19px




Chia cột

	

Border-right 1px

	

Border-bottom 1px




Gap

	

24px

	

16px




Radius vùng bao

	

0 hoặc 8px

	

0 hoặc 8px

Mọi số lượng dùng tabular numerals. Có thể hiển thị tỷ lệ ngay dưới số, nhưng không dùng một icon tròn cho mỗi metric. Thay đổi số liệu sau thao tác có thể thông báo bằng text trạng thái, không nháy hoặc đếm số từ 0.

3.6. Bảng desktop và danh sách mobile
Bảng dữ liệu

Thành phần

	

Thông số




Header row

	

Min-height 44px




Data row

	

Min-height 56px




Cell padding

	

12px 16px




Header font

	

12px / 600




Cell font

	

13px / 21px




Viền

	

Chỉ border-bottom 1px




Hover

	

--at-surface-hover




Selected row

	

--at-brand-soft và chỉ dấu trái 3px




Sort icon

	

14px arrow-up/arrow-down




Checkbox column

	

48px




Action column

	

88–120px tùy hành động




Sticky header

	

Chỉ trong vùng bảng cuộn dọc có giới hạn




Empty row

	

Một hàng spanning toàn bộ cột

Không tô nền toàn hàng theo trạng thái chờ/xử lý/lỗi. Trạng thái nằm trong cột riêng. Điểm phải căn phải, tên căn trái; cột mã căn trái để tránh làm mất số 0 đầu.

Khoa: 20 bản ghi/trang mặc định, cho phép 10/20/50. Bảng không render toàn bộ 100 bản ghi cùng lúc. Không dùng cột chứa 3 nút xếp dọc.

Danh sách mobile

Mỗi bản ghi là một bề mặt có padding 16px, radius 8px, viền 1px. Header có tên/tiêu đề tối đa 3 dòng và trạng thái. Nội dung dưới là tối đa 3 cặp nhãn–giá trị quan trọng. Chân item chứa hành động chính và menu phụ nếu cần.

Khoảng cách item 12px; không dùng bảng thu nhỏ trên mobile. Tên dài được xuống dòng, không cắt nếu đó là dữ liệu cần nhận diện. Mã dài có thể wrap theo quy tắc hợp lý; email/URL dùng overflow-wrap:anywhere.

3.7. Badge trạng thái

Loại

	

Nền

	

Chữ

	

Viền




Thành công

	

--at-success-soft

	

--at-success

	

Transparent




Chờ/cảnh báo

	

--at-warning-soft

	

--at-warning

	

Transparent




Lỗi/từ chối

	

--at-danger-soft

	

--at-danger

	

Transparent




Thông tin

	

--at-info-soft

	

--at-info

	

Transparent




Trung tính

	

--at-surface-2

	

--at-ink

	

--at-line

Badge cao tối thiểu 26px, padding 4px 9px, font 12px/600, bo góc 5px. Không dùng chấm màu làm thông tin duy nhất; luôn có chữ như “Chưa xếp”, “Đủ điều kiện”, “Đã công bố”.

Badge không được tương tác trừ khi được thiết kế rõ là chip lọc. Chip lọc dùng thành phần riêng, không tận dụng badge trạng thái.

3.8. Phân trang

Chiều cao control 36px desktop, 40px mobile; nút số trang tối thiểu 36×36px; radius 5px; gap 4px. Trang hiện tại nền --at-brand, chữ --at-on-brand. Hover trang khác nền --at-surface-hover, focus rõ ràng.

Desktop hiển thị “1–20 trong 100 sinh viên”, chọn số bản ghi/trang, Previous / số trang / Next. Tối đa 5 nút trang hiển thị cùng lúc; dùng dấu “…” cho khoảng bị lược bỏ.

Mobile hiển thị “Trang 1/5”, hai nút Trước / Sau; không dàn đủ 5 số khiến tràn chiều ngang. Giữ tham số lọc và tìm kiếm khi chuyển trang.

3.9. Tabs, bộ lọc và tìm kiếm

Tabs desktop: chiều cao 44px, font 13px/600, gap 24px, active có đường gạch dưới 2px --at-brand, không tô toàn tab màu tím hay Forest. Mobile tab dài dùng cuộn ngang trong chính dải tab, có chỉ báo vùng cuộn; không tạo tràn toàn trang.

Chip lọc cao 32px, padding 0 12px, border 1px, radius pill chỉ dùng cho chip. Filter bar desktop gap 12px; tìm kiếm rộng 280–360px, bộ lọc dạng select 160–220px. Mobile dùng ô tìm kiếm full width + nút “Bộ lọc” mở sheet.

Filter cần hiển thị số điều kiện đang áp dụng; có “Xóa bộ lọc” khi khác mặc định. Không tự xoá query khi chuyển tab nếu bộ lọc đó vẫn có nghĩa.

3.10. Thanh tiến trình nghiệp vụ

Phân biệt hai thành phần:

Journey của sinh viên: 4 mốc Hồ sơ → Gợi ý → Nguyện vọng → Kết quả. Desktop nằm ngang nếu đủ không gian, mobile dùng vertical step list hoặc trạng thái hiện tại + menu xem lịch sử. Mỗi mốc có nhãn trạng thái “Hoàn thành”, “Đang thực hiện”, “Chưa thực hiện”, “Không thể thực hiện”, căn cứ trên dữ liệu thật.

Trạng thái đợt: một dải tách biệt, hiển thị tên đợt, OPEN/CLOSED/OPTIMIZED/PUBLISHED bằng tiếng Việt, khoảng thời gian và hành động được phép.

Không dùng step index đơn giản để giả định bước tiếp theo. Nếu đợt đã công bố nhưng sinh viên chưa nộp nguyện vọng, vẫn hiển thị kết quả “Chưa được phân công” (nếu đúng), đồng thời ghi rõ nguyện vọng chưa nộp.

Chiều cao step marker 24px, đường nối 1px, nhãn 13px; gap các bước desktop 24px, mobile 16px. Hoàn thành dùng icon check; hiện tại dùng circle-dot, chưa thực hiện dùng đường viền trung tính.

3.11. Khối điểm AI
Điểm tổng hợp

Desktop: số 48px/56px weight 600; mobile 40px/48px.

Đơn vị /100: 14px/22px muted.

Nhãn “Điểm phù hợp”: 13px/21px.

Khối điểm rộng 120–160px desktop, ở mobile nằm góc phải nếu đủ chỗ, nếu không chuyển dưới tiêu đề.

Không dùng vòng tròn progress khổng lồ. Điểm tổng lớn bằng typography, không bằng hiệu ứng.

Không tự phân loại “Xuất sắc/Tốt/Yếu” nếu backend chưa định nghĩa ngưỡng.

M1–M5

Mỗi hàng desktop gồm mã Mx 30px, nhãn 110px, thanh điểm linh hoạt, giá trị 40px. Khoảng cách hàng 12px; track cao 7px, radius 3px. Điểm phải hiển thị bằng chữ số để không phụ thuộc độ dài thanh.

M1–M4 dùng màu brand, M5 dùng AI Accent. Điểm chưa có dùng track trung tính rỗng và chữ “Chưa đánh giá”. Nếu M5 sử dụng fallback, thêm nhãn nguồn tính toán.

Mobile: nhãn và giá trị nằm trên một hàng, thanh ở hàng dưới; gap 6px, mỗi mô hình cách 14px. Mọi điểm đã tính theo thang 0–100; không suy ra M1 gốc 1–5 chính là phần trăm nếu công thức chuẩn hóa chưa được áp dụng.

Trọng số AHP

Trong vùng chi tiết mở rộng phải thể hiện trọng số w1–w5, tổng trọng số = 1, phiên bản trọng số, phiên bản mô hình, và phương pháp tính điểm đã áp dụng. Không hiển thị điểm kết quả giả khi thiếu thành phần hoặc fallback.

3.12. Khối giải thích AI

Tên: Evidence Note.

Nền --at-ai-soft, đường viền trái 3px --at-ai.

Padding 16px mobile, 20px desktop.

Radius 6px, không shadow.

Tiêu đề 14px/600, thân 13px/21px.

Icon info 18px, căn theo dòng tiêu đề.

Nội dung chia tối đa ba phần có nhãn: “Điểm phù hợp”, “Điểm cần lưu ý”, “Điều kiện bắt buộc”.

Nếu LLM tạo câu giải thích, phải thể hiện được nguồn (LLM/fallback) ở vùng mở rộng và giới hạn độ dài hiển thị mặc định khoảng 4 dòng; nút “Đọc đầy đủ” mở ra toàn bộ.

Nếu không có lý do hợp lệ, ghi “Chưa có giải thích cho kết quả này”, không sinh văn bản khẳng định chưa được backend xác nhận.

Không dùng icon sparkles lặp lại trong mỗi hàng để tạo cảm giác AI. AI là chứng cứ, không phải trang trí.

3.13. Ngăn kéo chi tiết

Desktop: rộng 440px, tối đa min(440px, 100vw), fixed right; trên trang nhiều biểu mẫu có thể mở rộng đến 520px nếu dùng biến thể form. Header cao tối thiểu 64px, padding 20–24px, title 19px/600; body cuộn độc lập; footer hành động cao tự nhiên, padding 16–24px, border-top.

Mobile: width 100%, height 100dvh cho nội dung phức tạp; ngăn kéo đơn giản từ dưới dùng tối đa 85dvh và có nút đóng. Header/footer sticky trong chính drawer, không vượt viewport.

Backdrop màu --at-overlay. Khi mở, khóa cuộn trang nền. Focus đi vào drawer, giữ bên trong, Esc đóng nếu không có thao tác phá hủy đang xác nhận. Khi đóng, trả focus về điều khiển đã mở drawer.

Trang GV duyệt sinh viên: không xếp ba nút “Chờ duyệt/Đồng ý/Từ chối” theo cột. Trạng thái “Chờ duyệt” là text/badge, không phải nút. Footer có “Đồng ý” primary và “Từ chối” secondary/danger tùy ngữ cảnh; mỗi hành động dẫn đến bước xác nhận phù hợp.

3.14. Hộp xác nhận hai bước

Bước 1 — Rà soát: trình bày tên hành động, đối tượng, tổng số bản ghi chịu tác động, ảnh hưởng đến trạng thái và những gì không thể hoàn tác. Chưa gọi endpoint thay đổi dữ liệu.

Bước 2 — Xác nhận: người dùng chủ động bấm xác nhận lần cuối; chỉ lúc này mới POST. Với hành động từ chối sinh viên, yêu cầu nhập lý do nếu nghiệp vụ bắt buộc. Lý do tối thiểu/tối đa ký tự do backend định nghĩa, UI phải nhận cùng validation.

Thông số modal: width 480px, max-width calc(100vw - 32px); padding 24px desktop/20px mobile; radius 12px; gap nội dung 16px; footer hai nút gap 8px, nút primary ở phải desktop, full-width hoặc chia hàng phù hợp trên mobile.

Với Công bố kết quả, bước 1 phải có tổng đã xếp, chưa xếp, phạm vi công bố và cảnh báo rõ; bước 2 yêu cầu xác nhận bằng văn bản cụ thể như “CÔNG BỐ” nếu muốn chống thao tác nhầm. Không dùng ô xác nhận chữ cho mọi hành động nhỏ.

Trong lúc submit, vô hiệu hóa cả nút submit và thao tác lặp; backend bắt buộc kiểm tra lại quyền, trạng thái đợt, điều kiện và tính idempotent. UI hai bước không thay thế kiểm tra backend.

3.15. Thông báo

Toast cao tối thiểu 48px, rộng 320–400px desktop, mobile calc(100vw - 32px), radius 8px, padding 12px 16px, border-left 3px theo trạng thái. Icon 18px, tiêu đề 13px/600, mô tả 12px/19px.

Success tự đóng sau 5 giây, trừ khi cần đọc nội dung dài.

Info sau 6 giây.

Warning/Error quan trọng giữ đến khi người dùng đóng hoặc thực hiện hành động.

Có nút x nhưng icon này không nằm trong danh sách Lucide đã cấp: dùng button đóng với ký tự × CSS/text hoặc mở rộng bộ icon khi được phê duyệt, không tự import bộ icon khác.

Có vùng aria-live="polite" cho kết quả thường, role="alert" cho lỗi cần phản hồi ngay.

Không hiện cùng một lỗi bằng cả toast, banner và modal khi không cần thiết.

Banner trong trang dùng khi thông tin có hiệu lực lâu dài như “Đợt đã đóng” hoặc “Kết quả chưa công bố”. Đặt gần đầu nội dung, không dùng toast cho thông tin cần tồn tại.

3.16. Trạng thái rỗng

Tái sử dụng 12 SVG line-art hiện có, đổi màu qua CSS. Không thêm ảnh stock.

Vùng rỗng thường: min-height 240px desktop, 200px mobile.

SVG: 160×107px desktop, 128×85px mobile, tỉ lệ gốc bảo toàn.

Tiêu đề: 16px/24px weight 600.

Mô tả: 13px/21px, max-width 380px.

Khoảng cách minh họa–tiêu đề 16px, tiêu đề–mô tả 8px, mô tả–nút 20px.

Tối đa một CTA chính và một liên kết phụ.

Bắt buộc phân biệt empty-first-use, empty-search, empty-filter, no-permission, closed-period, loading, error, no-data-yet. Không dùng “Không có dữ liệu” cho tất cả các trường hợp.

Nếu SVG hiện có hardcode màu không đổi được qua CSS, Claude phải chỉnh fill/stroke theo token hoặc currentColor, giữ nguyên hình học và nội dung minh họa.

3.17. Biểu đồ Chart.js

Phân bố kết quả phân công

Minh họa tỉ lệ tổng hợp đã cung cấp, không phải biểu đồ phân bố từng khoảng điểm.
0
15
30
45
60
Đã xếp
Chờ pha 2
Đã xếp: Số sinh viên 43
Chờ pha 2: Số sinh viên 57

Thông số chuẩn:

Thuộc tính

	

Giá trị




Font toàn chart

	

Be Vietnam Pro




Tick label

	

12px/400, màu --at-ink-muted




Axis title

	

12px/600, màu --at-ink




Legend

	

12px/500, đặt phía trên




Grid

	

--at-line, độ rộng 1px




Dataset border

	

0 đối với bar; 2px với line




Border radius bar

	

4px




Bar thickness

	

Max 38px




Point radius

	

3px, hover 5px




Tooltip

	

Nền --at-ink, chữ --at-surface, padding 10px




Animation

	

240ms, easing easeOutCubic, hoặc tắt




Chart container

	

Desktop 280–320px; mobile 220–260px




Legend gap

	

16px




Resize

	

Responsive true, maintainAspectRatio false

Với biểu đồ bar xếp chồng phân bố điểm NV1/NV2/NV3, dùng chart-1/2/3, legend có chữ đầy đủ, tooltip hiển thị số lượng và phần trăm đúng mẫu số. Chart-4/5/6 dành cho chuỗi dữ liệu bổ sung; không dùng nhiều hơn 6 chuỗi trên một biểu đồ. Trường hợp nhiều dữ liệu hơn phải lọc, nhóm hoặc đổi cách biểu diễn.

Dữ liệu thiếu dùng null; không biến null thành 0. Chart ẩn phải được resize khi panel/tab trở nên visible. Dark mode phải cập nhật toàn bộ màu biểu đồ và tooltip, không chỉ đổi CSS bên ngoài canvas. Bên dưới biểu đồ thống kê quan trọng cần có bảng dữ liệu thay thế để phục vụ tiếp cận và kiểm chứng.

=== PHẦN 4: TỪNG MÀN HÌNH ===

4.1. Quy tắc chung của mọi màn hình

Desktop dùng page header → trạng thái nghiệp vụ (nếu có) → nội dung chính → hành động phụ → footer. Mobile ưu tiên thứ tự đọc và thao tác, không cố bảo toàn vị trí hai cột của desktop.

Trạng thái toàn cục bắt buộc xử lý: loading, success, empty, error, forbidden, readonly khi phù hợp. Nếu một khối chưa có dữ liệu thì chỉ thay khối đó bằng empty state, không tự động xóa toàn bộ nội dung trang.

Khi văn bản dài, không sử dụng text-overflow: ellipsis cho tên đề tài, tên sinh viên, tên giảng viên, lý do từ chối và giải thích AI ở vùng chi tiết. Có thể giới hạn 2–3 dòng trong danh sách nếu có đường dẫn xem đầy đủ. Dữ liệu ít phải được căn theo đầu vùng nội dung, không phóng to card để lấp chỗ trống.

A. Sáu màn hình chung

#

	

Màn hình

	

Desktop: bố cục và thứ tự

	

Mobile: bố cục và thứ tự




01

	

Đăng nhập

	

Khung chia 2 vùng theo tỉ lệ 5:7; trái nền Forest có thương hiệu, mô tả hệ thống và họa tiết logo; phải form rộng 400px gồm tiêu đề, tài khoản, mật khẩu, đăng nhập. Không stock image.

	

Một cột full width, logo trên đầu, form bên dưới. Padding 24px, max-width 440px, không hiện mảng nền thương hiệu lớn.




02

	

Đổi mật khẩu

	

Page header → form rộng 520px gồm mật khẩu hiện tại, mới, xác nhận → yêu cầu mật khẩu → nút cập nhật.

	

Một cột, field cách nhau 20px, nút lưu full-width ở cuối form.




03

	

Thiếu hồ sơ

	

Header → dải tiến độ hoàn thiện → danh sách mục còn thiếu → nút hoàn thiện hồ sơ; nội dung rộng 720px.

	

Nêu điều cần bổ sung trước, rồi checklist và CTA. Không làm người dùng phải đọc một màn hình cảnh báo dài.




04

	

403

	

Centered illustration + tiêu đề “Bạn không có quyền truy cập” + lý do tổng quát + về trang chủ. Không tiết lộ dữ liệu hoặc quyền nội bộ.

	

Minh họa 128px, một cột, CTA rõ.




05

	

404

	

Centered layout tương tự 403; tiêu đề “Không tìm thấy trang”; có quay về trang chủ.

	

Tương tự, giữ header tối giản.




06

	

500

	

Minh họa lỗi hệ thống, thông báo trung tính, mã tham chiếu lỗi nếu backend cung cấp, nút thử lại và về trang chủ.

	

Không hiện traceback, không hiển thị chi tiết kỹ thuật.

Trạng thái đặc biệt:

Đăng nhập: sai mật khẩu chỉ hiện lỗi chung “Thông tin đăng nhập không chính xác”; submit loading không mất dữ liệu đã nhập ngoại trừ mật khẩu khi chính sách bảo mật yêu cầu.

Đổi mật khẩu: có hướng dẫn độ dài, kiểm tra khớp hai mật khẩu và xác nhận thành công; không cho xem mật khẩu hiện tại sau khi hoàn tất.

Thiếu hồ sơ: chỉ liệt kê dữ liệu thực sự cần bổ sung. Nếu backend tạm lỗi, hiển thị lỗi tải thông tin chứ không kết luận sinh viên thiếu hồ sơ.

403/404/500: xử lý cả khi chưa đăng nhập; không phụ thuộc dữ liệu nghiệp vụ. Không tự chuyển hướng liên tục.

Nội dung dài: ngắt dòng, tối đa 640px vùng đọc; thông báo lỗi kỹ thuật chỉ hiện mã tham chiếu an toàn.

B. Sáu màn hình sinh viên
7. Trang chủ sinh viên
Ưu tiên cao

SƠ ĐỒ BỐ CỤC DESKTOP

Lời chào + trạng thái đợt

Đề xuất Top 5

Danh sách chính · 8 cột grid

Nguyện vọng & hành động

Cột phụ · 4 cột grid

Journey + các thông tin cần chú ý

Desktop: header trang → trạng thái đợt → khối gợi ý Top 5 (8/12 cột) cùng khối nguyện vọng (4/12) → hành trình học thuật → cập nhật liên quan. Không có Top 5 thì dùng empty state đúng nguyên nhân.

Mobile: lời chào → trạng thái đợt → hành động cần làm tiếp → đề tài phù hợp nhất → 4 đề tài còn lại → 3 nguyện vọng → journey dạng dọc. Không dùng khối trống cao 300px khi chưa có đề xuất.

Dữ liệu ít: nếu chỉ có 1–4 đề tài hợp lệ, hiển thị đúng số đó và giải thích vì sao không đủ 5. Khi công bố kết quả, ưu tiên một khối kết quả chính thức ở đầu trang, không giữ CTA “Đăng ký ngay”.

08. Hồ sơ năng lực

Desktop: header → thông tin cá nhân và trạng thái hoàn thiện → tự giới thiệu (8 cột) + hướng dẫn hoàn thiện (4 cột) → kỹ năng → lĩnh vực quan tâm → nút lưu.

Mobile: thông tin cá nhân → tự giới thiệu → kỹ năng từng dòng (tên, mức 1–5, nút xóa) → thêm kỹ năng → lĩnh vực quan tâm dạng checkbox/chip lựa chọn, có giới hạn 1–3 → nút lưu cố định theo mẫu action bar nếu form dài.

Kỹ năng hiển thị tên đầy đủ, không rút gọn khi chỉnh sửa.

Mức kỹ năng 1–5 có giải thích ngắn gọn; không dùng progress bar thay input.

Khi chưa có kỹ năng, hiện empty state nhỏ và nút “Thêm kỹ năng”.

Trường tự giới thiệu dài giữ tối đa theo backend; textarea tự tăng chiều cao đến ngưỡng 240px rồi cuộn trong.

Có trạng thái chưa lưu, lưu thành công, lưu thất bại.

Khi cập nhật hồ sơ, cảnh báo gợi ý AI cũ có thể cần tính lại nếu quy trình backend yêu cầu; không tự động xóa nguyện vọng đã nộp.

09. Đăng ký nguyện vọng NV1–NV3

Desktop: header + trạng thái đợt → ba vùng NV1/NV2/NV3 xếp dọc (vùng đọc tối đa 880px) → tổng quan kiểm tra điều kiện → nút lưu/nộp. Mỗi nguyện vọng có vị trí, tên đề tài, giảng viên, điểm và trạng thái đủ điều kiện.

Mobile: ba nguyện vọng xếp dọc toàn chiều rộng, điều khiển chọn/đổi đề tài rõ ràng, thao tác cuối trong action bar.

Cấm chọn trùng cùng đề tài ở các nguyện vọng.

NV đã lưu hiển thị được kể cả khi đợt đóng.

Đợt đóng/chưa mở/đã công bố: readonly, có thời điểm nộp và thông báo không thể chỉnh sửa.

Nếu chỉ có NV1, không tự vẽ dữ liệu NV2/NV3; hiển thị “Chưa chọn”.

Nếu đề tài bị thay đổi điều kiện sau khi SV nộp, hiển thị trạng thái cập nhật; cách xử lý nguyện vọng đã nộp do backend quyết định.

Trước khi nộp/chốt phải có xác nhận và phản hồi backend.

10. Danh sách đề tài

Desktop: header → search/filter bar → tóm tắt số kết quả → danh sách đề tài (dòng phẳng, mỗi dòng có tên, lĩnh vực, giảng viên, điểm sơ bộ/cuối cùng, điều kiện, hành động) → phân trang. Context Index chứa bộ lọc nâng cao: lĩnh vực, giảng viên, đủ điều kiện, mức phù hợp nếu có điểm.

Mobile: header → tìm kiếm → nút Bộ lọc → danh sách card dọc → phân trang đơn giản.

10 mục/trang mobile và 20 mục/trang desktop mặc định; backend cho phép điều chỉnh theo cấu hình thống nhất.

Empty search phải hiện “Không tìm thấy đề tài phù hợp với bộ lọc” và nút xóa bộ lọc.

Đề tài không đủ điều kiện vẫn được xem, phải nêu lý do.

Điểm chưa tính hiển thị “Chưa đánh giá”; không hiện 0.

Tên dài tối đa 3 dòng ở danh sách, xem đủ tại chi tiết.

Không bao mỗi đề tài trong 3 card lồng nhau.

11. Chi tiết đề tài

Desktop: breadcrumb → tên đề tài + giảng viên + tình trạng → mô tả đề tài (8 cột) / bảng điểm tổng hợp và đăng ký (4 cột) → M1–M5 → lý do gợi ý → yêu cầu kỹ năng/học phần/GPA → thông tin còn lại.

Mobile: tên đề tài → trạng thái đủ điều kiện → điểm tổng → CTA nếu hợp lệ → diễn giải AI → M1–M5 → điều kiện → mô tả đầy đủ. Không bắt buộc cuộn qua mô tả dài mới thấy điểm AI.

Nếu không đủ điều kiện, lý do hiện ngay dưới điểm.

Nếu chưa tính M5, hiển thị M1–M4 và nhãn chờ đánh giá.

Mô tả dài có đề mục phân đoạn và line-height 1.6, không giới hạn bằng chiều cao cố định.

Đề tài không còn chỗ: trạng thái độc lập với “không đủ điều kiện học thuật”.

Nếu đăng ký làm NV1/NV2/NV3, cần kiểm tra trạng thái đợt và trùng nguyện vọng.

12. Kết quả phân công

Desktop: header → thông báo kết quả chính thức → thông tin đề tài được phân công, giảng viên, nguyện vọng trúng, điểm phù hợp → tóm tắt 3 nguyện vọng đã nộp → thông tin bước tiếp theo nếu có.

Mobile: kết luận kết quả ở đầu, tên đề tài rõ, giảng viên, thứ tự NV, điểm; hành động xem chi tiết. Thông tin bổ sung bên dưới.

Chưa công bố: trạng thái chờ, không thấy dữ liệu phân công nháp.

Đã công bố nhưng chưa xếp: thông báo trung tính và nguyên nhân hợp lệ nếu backend cung cấp.

Được xếp tay: thể hiện nguồn phân công theo cách dễ hiểu, không suy diễn “NV1”.

Nếu có thay đổi sau công bố, hiển thị phiên bản/ghi chú điều chỉnh khi backend có lịch sử.

Nếu thiếu dữ liệu giảng viên hoặc đề tài, thông báo lỗi dữ liệu rõ ràng, không trình bày kết quả rỗng như đã xếp thành công.

C. Năm màn hình giảng viên

#

	

Màn hình

	

Desktop

	

Mobile




13

	

Trang chủ GV

	

Header → Metric Ledger (tổng đề tài, SV đăng ký, chờ duyệt, chỉ tiêu) → danh sách cần xử lý 8 cột / lịch hoặc trạng thái đợt 4 cột → đề tài gần đây.

	

Việc cần xử lý trước → số liệu hai cột → đăng ký mới nhất → đề tài.




14

	

Đề tài của tôi

	

Header + thêm đề tài → tabs trạng thái → bộ lọc → bảng các đề tài: tên, lĩnh vực, số SV, capacity, trạng thái, hành động.

	

Card từng đề tài, số SV/capacity và hành động xem/sửa.




15

	

Thêm/sửa đề tài

	

Form max 880px: thông tin chính → mô tả → lĩnh vực → kỹ năng yêu cầu → học phần tiên quyết/GPA nếu có → capacity → lưu. Dùng 2 cột chỉ với field ngắn.

	

Toàn bộ form một cột, kỹ năng yêu cầu dạng item thêm/xóa; action bar lưu.




16

	

SV đăng ký đề tài

	

Context Index chọn đề tài → danh sách SV → ngăn kéo chi tiết điểm AI và hồ sơ → duyệt/từ chối.

	

Chọn đề tài → card SV → toàn màn hình chi tiết → hành động xác nhận.




17

	

Hồ sơ GV

	

Header → thông tin GV → chuyên môn/lĩnh vực → chỉ tiêu → danh sách đề tài liên quan → thao tác chỉnh sửa trường được phép.

	

Thông tin cá nhân → chuyên môn → chỉ tiêu → đề tài; một cột.

Quy tắc đặc biệt trang GV

Trang 14: Không có đề tài phải có CTA “Tạo đề tài” nếu người dùng có quyền. Chỉ tiêu đầy không đồng nghĩa không được xem đề tài. Tên đề tài dài xuống dòng; trạng thái đề tài độc lập với trạng thái đợt.

Trang 15: Kỹ năng yêu cầu gồm tên kỹ năng, mức bắt buộc (1–5), trọng số, cờ bắt buộc. Hiển thị lỗi tại từng dòng, không chỉ lỗi toàn form. Khi xóa kỹ năng phải cập nhật validation. Nếu đề tài đã có SV đăng ký, backend phải quyết định field nào được sửa; UI không cho sửa lén ràng buộc đang có hiệu lực.

Trang 16: Duyệt dùng nhãn trạng thái chờ, không tạo ba nút lựa chọn như hiện tại. Điểm M1–M5 trong drawer phải gắn với đúng sinh viên–đề tài, có thời điểm/phiên bản đánh giá. Từ chối có lý do; khi hành động thành công cập nhật trạng thái dòng mà không thay toàn bộ viewport.

Trang 17: Thiếu thông tin GV dùng dấu “Chưa cập nhật” và lời nhắc hợp lệ; không dùng dữ liệu mẫu trong hồ sơ thật. Chỉ tiêu phải phân biệt quota tối đa với số đã được phân công.

D. Bốn màn hình Khoa

18. Trang chủ Khoa

Desktop: header + chọn đợt → Period Status → Metric Ledger (100 SV, 50 đề tài, các chỉ số đăng ký/phân công) → tiến độ đợt và các việc cần xử lý (chia 7/5 cột) → danh sách đợt → lối tắt Phân công/Thống kê/Nhập Excel.

Mobile: chọn đợt → trạng thái → 4 số liệu ưu tiên → việc cần làm → đợt gần đây → lối tắt.

Không có đợt phải hiển thị trạng thái trống và hướng dẫn xử lý tùy quyền. Nếu đang có một đợt được chọn, mọi số liệu phải thuộc cùng đợt. Không trộn 100 SV toàn hệ thống với 43 SV của một đợt khác.

19. Phân công đề tài — màn hình trung tâm

BỐ CỤC DESKTOP — THỨ TỰ BẮT BUỘC

01. Header + chọn đợt + hành động

02. Dải trạng thái và cảnh báo

03. Metric Ledger

43

Đã xếp

30%

NV1

43%

Top 3

57

Chờ pha 2

04. Phân bố điểm / kết quả tối ưu

05. Bộ lọc + bảng phân công

20 bản ghi/trang · drawer chi tiết · xếp tay pha 2

06. Chốt và công bố: quy trình xác nhận hai bước

Desktop: đầu trang có chọn đợt và hành động chạy ILP/Greedy (khi được phép), dải tiến độ, chỉ số, biểu đồ, bảng phân công. Context Index cho phép chuyển nhanh giữa Tất cả / Chưa xếp / Cần rà soát. Xếp tay mở drawer, không chèn form dài vào bảng.

Mobile: trạng thái đợt → chỉ số chính → nút xem SV chưa xếp → danh sách SV → chi tiết full-screen → xếp tay. Biểu đồ và số liệu nâng cao nằm sau phần hành động chính. Nếu chạy ILP/Greedy trên mobile, vẫn cần dialog xác nhận và phản hồi thời gian xử lý.

Đặc biệt: Không chuyển kết quả ILP nháp thành công bố chỉ vì đã xếp 43 người. Không tự động công bố khi còn 57 SV chưa xếp. Quy tắc cho phép chốt/công bố phải do backend xác định, có hiển thị phạm vi công bố và hệ quả rõ ràng.

20. Thống kê Khoa

Desktop: header + chọn đợt/bộ lọc → Metric Ledger → biểu đồ phân công theo nguyện vọng → phân bố điểm phù hợp → phân bố theo giảng viên/chỉ tiêu → bảng chi tiết và xuất báo cáo nếu có.

Mobile: chỉ số → biểu đồ từng khối dọc → bảng tóm tắt → bộ lọc bằng sheet. Biểu đồ có khả năng chuyển sang bảng số liệu để đọc chính xác.

Không có dữ liệu: hiển thị “Chưa có kết quả thống kê cho đợt này”.

Ít dữ liệu: trục biểu đồ vẫn đúng, không kéo cột thành 100%.

Chart dài: giới hạn legend và cho cuộn danh sách chú giải khi cần.

Nếu số liệu giữa dashboard và thống kê khác nhau, phải thể hiện bộ lọc/phạm vi; không tự sửa bằng frontend.

21. Nhập Excel

Desktop: header → hướng dẫn định dạng và tải mẫu → vùng chọn file → kiểm tra cấu trúc → preview dữ liệu → danh sách lỗi/cảnh báo → xác nhận nhập → kết quả nhập.

Mobile: hướng dẫn → chọn file → trạng thái upload → tóm tắt kiểm tra → danh sách lỗi → xác nhận. Preview bảng nhiều cột có thể dùng vùng cuộn ngang riêng, nhưng phải có danh sách lỗi đọc được ở mobile.

Các trạng thái bắt buộc:

Chưa chọn file.

Đang tải file.

Đang kiểm tra.

File sai định dạng.

File có lỗi nhưng có thể sửa.

File hợp lệ, sẵn sàng nhập.

Đang ghi dữ liệu.

Nhập thành công / nhập một phần / thất bại.

Backend trả số dòng hợp lệ, lỗi, trùng dữ liệu, thông tin dòng/cột lỗi và lý do; frontend không tự đánh dấu file hợp lệ chỉ vì phần mở rộng .xlsx. Nếu file lớn, preview chỉ tải một tập con có phân trang, không render toàn bộ workbook.

4.2. Quy tắc dữ liệu dài và ít dữ liệu

Áp dụng cho cả 21 màn hình:

Loại dữ liệu

	

Quy tắc




Tên người

	

Không cắt trong chi tiết; danh sách giới hạn 2 dòng khi cần




Tên đề tài

	

Danh sách tối đa 3 dòng; trang chi tiết hiển thị đầy đủ




Đoạn mô tả

	

Line-height tối thiểu 1.55; cho phép nhiều đoạn




Điểm AI

	

Không làm tròn đến số nguyên nếu backend trả 1 chữ số thập phân có ý nghĩa




Mã SV

	

Giữ nguyên dạng chuỗi, bảo toàn số 0 đầu




Lý do từ chối

	

Không cắt trong lịch sử/chi tiết




Lý do AI

	

Có thể thu gọn trong list, bắt buộc xem đầy đủ




Ngày giờ

	

Theo giờ Việt Nam, định dạng ngày dd/MM/yyyy, giờ HH:mm khi cần




Giá trị null

	

“Chưa có dữ liệu”, “Chưa đánh giá”, “Chưa cập nhật” tùy nghĩa




Danh sách 1 item

	

Căn trên, không phóng item chiếm toàn trang




Danh sách 0 item

	

Empty state đúng ngữ cảnh, có hành động phù hợp




Lỗi server

	

Giữ bố cục và dữ liệu cũ an toàn nếu hợp lệ; hiển thị lỗi tải lại

=== PHẦN 5: CHUYỂN ĐỘNG ===

5.1. Một ngôn ngữ: Quiet Precision

Không dùng hiệu ứng để gây ấn tượng. Chuyển động chỉ có hai mục đích: xác nhận thay đổi trạng thái và giúp người dùng định hướng khi một lớp nội dung xuất hiện hoặc biến mất.

Tình huống

	

Kích hoạt

	

Thời lượng

	

Dịch chuyển




Hover button

	

Pointer enter/leave

	

120ms

	

0




Hover row

	

Pointer enter/leave

	

120ms

	

0




Tab content

	

Sau khi chọn tab và có dữ liệu

	

180ms

	

0




Drawer mở

	

Click xem chi tiết

	

220ms

	

8px theo hướng xuất hiện




Drawer đóng

	

Click đóng/Esc

	

180ms

	

8px




Modal mở

	

Click hành động cần xác nhận

	

220ms

	

translateY(8px) → 0




Toast xuất hiện

	

Có thông báo mới

	

180ms

	

translateY(8px) → 0




Empty → loaded

	

Dữ liệu hoàn tất

	

180ms

	

0




Biểu đồ lần đầu

	

Sau khi dữ liệu được nhận và vùng hiển thị

	

240ms

	

Không dịch container




Expand lý do AI

	

Click “Đọc đầy đủ”

	

180ms

	

Không dịch toàn trang

Tất cả CSS transition dùng cubic-bezier(.2, .7, .2, 1), trừ Chart.js sử dụng easeOutCubic gần tương đương do thư viện hỗ trợ. Không tự chọn easing khác ở từng màn hình.

5.2. Thứ tự và quy tắc kích hoạt

Khi trang xuất hiện, header và nội dung đã sẵn có phải hiển thị ngay, không chạy animation vào trang. Dữ liệu bất đồng bộ có skeleton tại đúng vùng dự kiến; khi nhận dữ liệu, crossfade một lần 180ms, không xuất hiện từng card nối tiếp.

Drawer: backdrop và drawer bắt đầu cùng lúc; backdrop fade 180ms, panel transform 220ms. Focus chỉ chuyển vào nội dung sau khi drawer sẵn sàng tương tác; khi đóng trả focus đúng nút mở.

Modal: backdrop 180ms, modal 220ms, không dùng scale/bounce.

Thông báo: fade + translateY(8px), 180ms; khi nhiều toast, giới hạn tối đa 3 toast hiển thị, không chạy stagger. Các thông báo trùng sự kiện được hợp nhất.

Biểu đồ: animation chỉ một lần khi dữ liệu có hiệu lực. Thay đổi bộ lọc cập nhật hình học tối đa 240ms, không reset toàn bộ hiệu ứng từ 0 nếu điều đó gây hiểu nhầm.

5.3. Tuyệt đối không chuyển động

Logo, nền và các họa tiết nhận diện.

Giá trị KPI bằng bộ đếm từ 0.

Dấu hiệu sai điều kiện học thuật.

Chữ, label, tooltip giải thích điều kiện.

Dòng bảng khi phân trang hay sắp xếp.

Thanh tiến độ giả mô phỏng quá trình AI suy nghĩ.

Gradient, glow, pulse, blinking.

Cả màn hình khi người dùng chỉ thay một bộ lọc.

Nút xác nhận giao dịch theo kiểu rung/lắc/bounce.

Các thông tin quan trọng khi đang cần đọc.

Loading dài dùng spinner đơn giản trong nút hoặc thanh tiến độ thực nếu có phần trăm từ backend. Không dựng phần trăm ảo.

5.4. Giảm chuyển động
CSS

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}


Với Chart.js, kiểm tra prefers-reduced-motion và đặt animation: false. Không dùng JavaScript để buộc hiệu ứng bất chấp thiết lập hệ điều hành.

=== PHẦN 6: LOGO ===

6.1. Quyết định biểu tượng

Tên thương hiệu giao diện: ATLAS
Tên sản phẩm đầy đủ: Capstone Advisor AI
Biểu tượng: Open Path — Con đường tri thức.

Logo mới được xây dựng từ một nét gấp hình học liên tục gợi liên tưởng đến cuốn sách mở và hai hướng hội tụ về một đích chung. Phần trống ở trung tâm tạo cảm giác lựa chọn, đánh giá và kết nối giữa sinh viên với đề tài. Không dùng 5 ô Mosaic, 4 ô Nova, ngôi sao AI hay họa tiết gradient.

Các đặc tính được khóa:

Artboard gốc 64×64, viewBox 0 0 64 64.

Dùng nét stroke-width="4.5", đầu nét tròn, nối nét tròn.

Không dùng filter, mask, gradient, shadow, animation.

Ở kích thước nhỏ dùng biểu tượng thuần, không đặt chữ trong biểu tượng.

Logo đầy đủ gồm biểu tượng bên trái và chữ Capstone AI bên phải; chữ viết bằng font của ứng dụng, không ép tên ATLAS thay thế tên dự án trong các tiêu đề nghiệp vụ.

6.2. Bản sáng
Capstone AI

Academic Decision Workspace

File: capstone-symbol-light.svg

XML
6.3. Bản tối
Capstone AI

Academic Decision Workspace

File: capstone-symbol-dark.svg

XML
6.4. Favicon

Favicon nền Forest, biểu tượng sách và đường tri thức màu trắng/kem. Dùng SVG vuông, không bo góc nền bằng CSS. Nếu trình duyệt tự áp dụng kiểu icon khác, không thay đổi hình học gốc.

Capstone AI Favicon

Thiết kế ở lưới 64×64; kiểm tra raster tại 16, 32 và 48px.

File: favicon.svg

XML
6.5. Quy tắc sử dụng logo

Ngữ cảnh

	

Biến thể

	

Kích thước




Desktop header

	

Symbol + wordmark HTML

	

Symbol 32px, chữ 18px




Mobile header

	

Symbol + tên ngắn

	

Symbol 28px, chữ 16px




Navigation Rail

	

Symbol-only

	

32px




Login desktop

	

Symbol + tên sản phẩm

	

Symbol 48px, chữ 24px




Login mobile

	

Symbol + tên sản phẩm

	

Symbol 40px, chữ 21px




Favicon

	

favicon.svg

	

Browser tự scale




Dark mode

	

capstone-symbol-dark.svg

	

Cùng kích thước

SVG light/dark phải được giữ ở dạng file riêng để dùng trong thẻ img; không dùng CSS filter đảo màu. Nếu embed inline, được phép ánh xạ stroke sang token tương đương nhưng không sửa tọa độ path.

Các kích thước chỉ áp dụng cho biểu tượng. Chữ thương hiệu được render bằng HTML với Be Vietnam Pro, không nhúng font, chuyển chữ thành path hoặc phụ thuộc Google Fonts CDN.

6.6. Checklist bàn giao để nghiệm thu

Kiểm tra hoàn thành

0/10

Một file CSS ATLAS thay thế ba CSS cũ; không còn style Bootstrap lộ rõ

Hai theme dùng đúng token, kiểm tra tương phản cả trạng thái hover/focus

Đủ 21 màn hình và bốn mức kiểm tra 390 / 768 / 992 / 1440px

Điều hướng và bảng Khoa không tràn ngang, có phân trang thật

M1–M5 và điều kiện học thuật hiển thị đúng nguồn điểm, không bịa dữ liệu

Đợt CLOSED/PUBLISHED vẫn cho xem dữ liệu lịch sử có quyền

Drawer, modal hai bước, form error, keyboard navigation hoạt động

Be Vietnam Pro và tài nguyên thiết yếu self-host; không phụ thuộc CDN

Logo light/dark/favicon đúng SVG và kích thước

Screenshot đối chiếu, kiểm tra WCAG, test nghiệp vụ và không lỗi console

Sao chép checklist

Kết luận Design Authority: ATLAS V3.3 được khóa theo sáu phần trên. Đội triển khai phải giữ nguyên token, bố cục, thứ tự nghiệp vụ và các quy tắc trạng thái. Thay đổi thiết kế ngoài thông số phải được thẩm định lại; không được coi hoàn thành chỉ vì giao diện chạy được hoặc build thành công.