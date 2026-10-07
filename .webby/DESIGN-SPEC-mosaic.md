=== PHẦN 1: PHÂN RÃ GIAO DIỆN ===

Nguyên tắc chung của Mosaic AI: không xây dashboard bằng “một đống card giống nhau”. Mỗi màn chỉ có 1 vùng chính, các module còn lại được phân cấp bằng nền, đường chia, khoảng trắng và kích thước. Trên desktop dùng sidebar + workspace; trên điện thoại dùng topbar + bottom navigation. Chế độ sáng/tối dùng cùng một cấu trúc, không thay đổi bố cục.

1. Chung — Đăng nhập
Khu vực	Thành phần	Nội dung
Brand	Biểu tượng Mosaic + wordmark	Mosaic AI, tagline “Gợi ý đúng. Phân công tốt.”
Authentication	Form	Tên đăng nhập, mật khẩu, hiện/ẩn mật khẩu
Context	Dòng giới thiệu	“Hệ thống tư vấn và phân công đề tài tốt nghiệp”
Utility	Theme toggle	Sáng / tối / theo hệ thống
Feedback	Alert	Sai thông tin, tài khoản bị khóa, phiên hết hạn

Trạng thái: mặc định, đang đăng nhập, sai tài khoản, mật khẩu trống, server lỗi, màn hình 320–390px, bàn phím mobile mở.

2. Chung — Đổi mật khẩu

Sections:

Header: “Đổi mật khẩu”.
Form: mật khẩu hiện tại, mật khẩu mới, nhập lại.
Password rules: tối thiểu 8 ký tự, trạng thái từng điều kiện.
Actions: Cập nhật mật khẩu, Hủy.

Trạng thái: sai mật khẩu hiện tại, hai mật khẩu không khớp, mật khẩu yếu, đang lưu.

3. Chung — Đổi mật khẩu thành công
Success mark Mosaic.
Tiêu đề: “Mật khẩu đã được cập nhật”.
Nội dung: xác nhận phiên đăng nhập.
CTA: Quay lại trang chủ.
Không dùng minh họa lớn.
4. Chung — Thiếu hồ sơ
Progress header: Hồ sơ chưa hoàn tất.
Checklist:
Thông tin cơ bản.
Kỹ năng.
Lĩnh vực quan tâm.
Mô tả bản thân.
Giải thích: AI chưa thể gợi ý chính xác nếu thiếu dữ liệu.
CTA chính: Hoàn thiện hồ sơ.
CTA phụ: Để sau nếu route cho phép.

Trạng thái: thiếu một phần / thiếu nhiều phần / hồ sơ chưa từng tạo.

5. Chung — 403
Mã lớn 403.
“Bạn không có quyền truy cập trang này.”
Hiện vai trò hiện tại.
CTA Về trang chủ.

Không dùng ảnh hoạt hình vui nhộn.

6. Chung — 404
404 / Không tìm thấy.
Hiện URL rút gọn nếu phù hợp.
Quay lại + Trang chủ.
7. Chung — 500
500 / Hệ thống gặp sự cố.
Request ID nếu backend cung cấp.
Thử lại.
Về trang chủ.

Không hiển thị traceback Django.

SINH VIÊN
8. SV — Trang chủ / Top 5 gợi ý

A. Greeting strip

Tên SV.
Mã SV.
Ngành.
GPA.
Hồ sơ hoàn thành %.

B. Journey
Hồ sơ → Gợi ý → Nguyện vọng → Kết quả

C. Hero recommendation

Top 1.
Tên đề tài.
Giảng viên.
Lĩnh vực.
Tổng điểm AI.
M1–M5.
2–3 lý do phù hợp.
CTA Xem chi tiết.

D. Top 2–5

Compact recommendation rows/cards.
Tổng điểm.
M1–M5 dạng mini-strip.
1 dòng lý do.

E. Nguyện vọng hiện tại

NV1 / NV2 / NV3.
Trạng thái lưu.

Trạng thái:

Chưa hoàn thành hồ sơ.
Đang tính gợi ý.
Chưa có recommendation.
Chỉ có 1–4 đề tài hợp lệ.
Tên đề tài 2–4 dòng.
API M5 lỗi: hiển thị “Điểm LLM tạm thời chưa có”.
Mobile loading skeleton.
9. SV — Hồ sơ năng lực

A. Profile completion

% hoàn thành.
Dữ liệu được AI sử dụng.

B. Tự giới thiệu

Textarea.
Counter.

C. Kỹ năng
Mỗi dòng:

Skill select/search.
Mức 1–5.
Nhãn mức: Mới biết / Cơ bản / Khá / Tốt / Thành thạo.
Xóa.
Add row.

D. Lĩnh vực quan tâm

Field.
Mức 1–3.
Add/remove.

E. Thông tin học tập

GPA read-only.
Môn học / điểm liên quan read-only nếu dữ liệu chính thức.

F. Save bar
Sticky trên mobile.

Trạng thái:

0 kỹ năng.
20+ kỹ năng.
Skill duplicate.
Field duplicate.
Text dài.
Saving / saved / save failed.
10. SV — Đăng ký NV1–NV3

A. Period status

Đợt đăng ký.
Thời hạn.
OPEN/CLOSED.

B. Selected preferences
3 slot rõ ràng:

NV1.
NV2.
NV3.

Mỗi slot:

Tên đề tài.
Giảng viên.
AI score.
Drag không bắt buộc; dùng nút lên/xuống an toàn hơn cho mobile.

C. Candidate list

Đề tài đã lưu.
Tìm thêm đề tài.

D. Confirmation

Cảnh báo không trùng đề tài.
Lưu nguyện vọng.

Trạng thái:

0/3.
1/3.
2/3.
3/3.
Đề tài hết capacity.
Hết hạn.
Đang lưu.
Thay đổi chưa lưu.
11. SV — Danh sách đề tài

A. Search

Tên đề tài / GV / kỹ năng.

B. Filter

Lĩnh vực.
Giảng viên.
Difficulty.
GPA tối thiểu.
Có phù hợp hồ sơ.
Có chỗ.

C. Result toolbar

Số kết quả.
Sort: AI score / mới nhất / tên.

D. Desktop

Rows/table nhẹ.

E. Mobile

Topic list cards.

Mỗi item:

Tên.
GV.
field.
capacity.
min GPA.
AI score nếu đã có.
CTA.

Trạng thái:

0 kết quả.
1 kết quả.
50+.
filter quá chặt.
đề tài tên dài.
loading page.
pagination.
12. SV — Chi tiết đề tài

A. Topic header

Tên.
GV.
lĩnh vực.
difficulty.
capacity.
trạng thái.

B. Match summary

Tổng điểm.
M1–M5.

C. Why this topic

3–5 lý do.

D. Điều kiện

GPA.
prerequisite.
mandatory skill.
required skill level.

E. Mô tả

Mục tiêu.
nội dung.
công nghệ/phương pháp.

F. Preference action

Thêm NV1/NV2/NV3.

Trạng thái:

eligible.
ineligible.
thiếu M5.
capacity đầy.
đã có trong nguyện vọng.
đăng ký đóng.
13. SV — Kết quả phân công

A. Result hero

Đã phân công hoặc Chưa được phân công.

B. Topic

Tên.
GV.
preference rank.
match score.
source: ILP / Greedy / Manual.

C. Why result

Nếu NV1/NV2/NV3.
Nếu manual phase 2.

D. Timeline

Đăng ký.
tối ưu.
công bố.

Trạng thái:

chưa công bố.
assigned.
unassigned.
kết quả thay đổi trước khi official.
official locked.
GIẢNG VIÊN
14. GV — Trang chủ

Dải số liệu:

Đề tài đang mở.
Tổng SV đăng ký.
Chờ duyệt.
Đã đồng ý.
Chỉ tiêu còn lại.

Workspace

Danh sách đề tài.
SV chờ xử lý.
tải GV.
deadline.

Trạng thái:

chưa có đề tài.
không có SV đăng ký.
quota đầy.
nhiều request.
15. GV — Đề tài của tôi
Search/filter status.
Table/list:
tên.
lĩnh vực.
capacity.
số NV.
số được phân công.
status.
Actions:
xem.
sửa.
đóng/mở nếu backend cho phép.

Trạng thái:

0 đề tài.
draft.
open.
closed.
archived.
16. GV — Thêm / sửa đề tài

Sections:

Thông tin chung.
Lĩnh vực.
Mô tả.
Difficulty / min GPA / capacity.
Kỹ năng yêu cầu.
Môn tiên quyết.
Preview điều kiện.
Save actions.

Skill row:

skill.
required level 1–5.
weight.
mandatory checkbox.
remove.

Prerequisite row:

môn.
điểm tối thiểu.
remove.

Trạng thái:

new.
edit.
validation.
duplicate skill.
15+ skill.
unsaved changes.
publishing.
17. GV — Sinh viên đăng ký đề tài

A. Topic selector

B. Request summary

tổng.
pending.
accepted.
rejected.

C. Student list

SV.
GPA.
NV rank.
tổng match.
M1–M5.
lý do.
trạng thái.

D. Inspector
Click SV → mở side panel:

hồ sơ.
skills.
courses.
AI analysis.

Actions:

Đồng ý.
Từ chối.

Trạng thái:

no applicants.
pending.
accepted.
rejected.
quota full.
decision conflict.
18. GV — Hồ sơ giảng viên
Họ tên.
bộ môn.
học vị.
lĩnh vực chuyên môn.
mô tả.
max_students.
số đang hướng dẫn.
lĩnh vực add/remove.

Trạng thái:

thiếu profile.
quota 0.
quota full.
save success/error.
KHOA
19. Khoa — Trang chủ

Không dùng 6 card KPI.

A. Status strip
Một dải ngang:
100 sinh viên · 50 đề tài · 15 GV · 43 đã xếp · 57 chưa xếp

B. Current period

trạng thái.
deadline.
next action.

C. Operational bento

đăng ký SV.
đề tài.
tải GV.
readiness cho ILP.

D. Alert queue

thiếu preference.
thiếu topic capacity.
overloaded lecturer.

E. Quick actions

Nhập Excel.
Phân công.
Thống kê.
20. Khoa — Phân công

Đây là màn desktop quan trọng nhất.

A. Header

Đợt đăng ký.
trạng thái.
actions.

B. Metric strip — số thật
Một dải duy nhất:

100 SV | 43% đã xếp | 30% đạt NV1 | 43% đạt Top 3 | 63,8 điểm TB | 57 chưa xếp | 1,37s

Không icon tròn.

C. Distribution

histogram score.

D. Allocation health

assigned/unassigned.
constraints valid.
lecturer overload.

E. Algorithm control

ILP.
Greedy.
comparison result.

F. Student table

Mã SV.
tên.
GPA.
đề tài.
GV.
NV.
score.
source.
status.

G. Phase 2 manual assignment
Chỉ xuất hiện khi unassigned > 0.

chỉ SV chưa xếp.
eligible topics.
capacity remaining.
manual assign.

H. Finalize

Chốt kết quả.
Công bố.

Hai hành động tách biệt.

Trạng thái:

chưa chạy.
running ILP.
ILP success.
infeasible.
greedy result.
57 unassigned.
filter unassigned.
manual assignment.
draft finalized.
published.
rollback không khả dụng.
21. Khoa — Thống kê

Tabs/segments:

Tổng quan đăng ký.
Đề tài hot.
Lĩnh vực.
Tải giảng viên.
ILP vs Greedy.

Charts:

registration completion.
preference rank.
Top topics.
field distribution.
lecturer load.
algorithm comparison.

Trạng thái:

thiếu data.
1 period.
multiple periods.
chart no result.
export.
22. Khoa — Nhập Excel

A. Download template

B. Drop zone

chọn file.
drag/drop.

C. File validation

sheet.
rows.
valid.
warning.
errors.

D. Preview table

E. Import result

imported.
skipped.
failed.

Trạng thái:

no file.
parsing.
invalid extension.
missing columns.
100% valid.
partial invalid.
imported successfully.

=== PHẦN 2: KẾ HOẠCH TÀI NGUYÊN ===

1. LOGO / BRAND

Mosaic AI giữ đúng concept “5 ô ghép”.

Cần tạo:

Asset	Số lượng
Symbol light	1
Symbol dark	1
Wordmark ngang light	1
Wordmark ngang dark	1
Wordmark monochrome	2
Favicon SVG	1
favicon 32×32	1
app icon 192	1
app icon 512	1
Tổng	11

Tất cả tôi tự định nghĩa; không dùng logo trường.

2. ICON

Nguồn duy nhất: Lucide Icons, MIT License.

Phong cách:

stroke 1.75.
size UI: 16/18/20/24px.
Không trộn Font Awesome / Bootstrap Icons.
Chung — 19 icon

house, search, bell, sun, moon, monitor, user, log-out, lock-keyhole, eye, eye-off, chevron-down, chevron-right, arrow-left, check, x, triangle-alert, info, circle-help.

Sinh viên — 16 icon

user-round, graduation-cap, sparkles, brain, bookmark, list-ordered, target, briefcase-business, book-open, layers-3, plus, trash-2, arrow-up, arrow-down, filter, sliders-horizontal.

Giảng viên — 13 icon

file-text, square-pen, users, user-check, user-x, badge-check, clipboard-list, circle-plus, save, archive, circle-dot, book-check, gauge.

Khoa — 22 icon

layout-dashboard, chart-no-axes-column, chart-pie, chart-line, table-2, play, square-stop, refresh-cw, settings-2, upload, download, file-spreadsheet, file-check-2, file-x-2, database, git-compare, wand-sparkles, route, users-round, circle-check-big, send, lock.

Sau loại bỏ icon trùng giữa vai trò: khoảng 57 icon distinct.

Không cần vẽ lại icon; lấy SVG trực tiếp từ Lucide.

3. MINH HỌA / EMPTY STATE

Tôi tự tạo bằng SVG line-art theo hình học Mosaic, tối đa 2 màu + neutral.

Chưa có gợi ý AI.
Chưa có đề tài.
Chưa có nguyện vọng.
Chưa có SV đăng ký.
Chưa có kết quả phân công.
Không tìm thấy khi search/filter.
Excel chưa tải lên.
Excel lỗi dữ liệu.
Hồ sơ chưa hoàn thành.

Tổng 12 minh họa SVG.

Không dùng stock illustration.

4. TỔNG TÀI NGUYÊN
Brand assets: 11
Distinct Lucide icons: ~57
Custom empty/error illustrations: 12
Custom chart artwork: 0 — Chart.js dựng runtime.
Stock/photo assets: 0

Tổng tài nguyên visual quản lý: khoảng 80.

=== PHẦN 3: THÔNG SỐ THIẾT KẾ ===

1. FONT

Google Fonts:

CSS
/* Google Fonts:
   Sora: 500, 600, 700
   Noto Sans: 400, 500, 600, 700
*/

--font-display: "Sora", "Noto Sans", sans-serif;
--font-ui: "Noto Sans", system-ui, sans-serif;

Sora:

logo.
heading.
KPI.
AI score.

Noto Sans:

body.
form.
table.
navigation.

Không dùng Inter.

2. CSS TOKENS
CSS
:root {
  color-scheme: light;

  /* Brand */
  --mz-teal-700: #005F73;
  --mz-teal-600: #087F8C;
  --mz-teal-500: #0A9396;
  --mz-teal-100: #D9F0EF;

  --mz-amber-600: #D68100;
  --mz-amber-500: #EE9B00;
  --mz-amber-100: #FFF1CC;

  --mz-olive-600: #6C7226;
  --mz-olive-500: #7A7D2D;
  --mz-olive-100: #ECEED8;

  --mz-red-700: #9B2226;
  --mz-red-600: #B33437;
  --mz-red-100: #F8E4E3;

  /* Background */
  --bg-canvas: #F3F4F1;
  --bg-page: #FAFAF8;
  --bg-surface: #FFFFFF;
  --bg-surface-subtle: #F6F7F4;
  --bg-surface-raised: #FFFFFF;

  /* Text */
  --text-strong: #181C1E;
  --text-default: #303638;
  --text-muted: #687174;
  --text-disabled: #9CA4A6;
  --text-on-accent: #FFFFFF;

  /* Border */
  --border-soft: #E4E7E3;
  --border-default: #D5DAD6;
  --border-strong: #B9C0BC;

  /* Accent */
  --accent: #005F73;
  --accent-hover: #004C5C;
  --accent-soft: #D9F0EF;
  --focus-ring: rgba(0, 95, 115, .28);

  /* States */
  --success: #287A52;
  --success-soft: #DFF1E7;

  --warning: #B66700;
  --warning-soft: #FFF0D0;

  --danger: #A33638;
  --danger-soft: #F8E2E2;

  --info: #31689C;
  --info-soft: #E2EEF8;

  /* AI score */
  --score-high: #16796F;
  --score-mid: #C37A00;
  --score-low: #B14245;

  /* Charts */
  --chart-1: #0A9396;
  --chart-2: #3E8FB0;
  --chart-3: #7A7D2D;
  --chart-4: #EE9B00;
  --chart-5: #BB5D48;
  --chart-6: #66717A;

  /* Geometry */
  --radius-xs: 6px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;

  /* Shadow */
  --shadow-xs: 0 1px 2px rgba(21, 30, 32, .05);
  --shadow-sm: 0 4px 14px rgba(21, 30, 32, .07);
  --shadow-md: 0 14px 36px rgba(21, 30, 32, .10);

  /* Bootstrap bridge */
  --bs-body-bg: var(--bg-page);
  --bs-body-color: var(--text-default);
  --bs-border-color: var(--border-default);
  --bs-primary: var(--accent);
  --bs-danger: var(--danger);
  --bs-warning: var(--warning);
  --bs-success: var(--success);
}

[data-bs-theme="dark"] {
  color-scheme: dark;

  --bg-canvas: #090C0D;
  --bg-page: #111315;
  --bg-surface: #171A1C;
  --bg-surface-subtle: #1D2123;
  --bg-surface-raised: #202527;

  --text-strong: #F4F4F0;
  --text-default: #DEE2DE;
  --text-muted: #9BA4A2;
  --text-disabled: #68716F;
  --text-on-accent: #071011;

  --border-soft: #23292A;
  --border-default: #303739;
  --border-strong: #465052;

  --accent: #0A9396;
  --accent-hover: #22AAAC;
  --accent-soft: #12383A;
  --focus-ring: rgba(34, 211, 213, .30);

  --success: #59B785;
  --success-soft: #173628;

  --warning: #E9B949;
  --warning-soft: #3A301A;

  --danger: #E76F51;
  --danger-soft: #40241E;

  --info: #72A9D4;
  --info-soft: #1C3041;

  --score-high: #48BFAF;
  --score-mid: #E9B949;
  --score-low: #E76F51;

  --chart-1: #22B3AD;
  --chart-2: #66A9D3;
  --chart-3: #B4B84A;
  --chart-4: #E9B949;
  --chart-5: #E76F51;
  --chart-6: #899493;

  --shadow-xs: 0 1px 2px rgba(0, 0, 0, .24);
  --shadow-sm: 0 5px 18px rgba(0, 0, 0, .24);
  --shadow-md: 0 18px 46px rgba(0, 0, 0, .34);

  --bs-body-bg: var(--bg-page);
  --bs-body-color: var(--text-default);
  --bs-border-color: var(--border-default);
  --bs-primary: var(--accent);
}
3. TYPOGRAPHY SCALE
Token	px	Line-height	Weight	Dùng
Display	32	40	700	Login / special
H1	26	34	700	Page title
H2	21	29	700	Section major
H3	17	24	600	Module title
Body L	16	25	400/500	intro
Body	14	22	400	default
Body S	13	19	400/500	table/mobile
Label	12	17	600	form/metadata
Caption	11	16	500	helper
Metric XL	30	34	700	primary KPI
Metric	22	28	700	secondary KPI

Mobile H1: 22/29px.

Không xuống dưới 12px với nội dung chức năng.

4. SPACING

Base unit: 4px.

Plain text
4   micro
8   compact
12  control gap
16  component
20  section compact
24  default section
32  major section
40  page rhythm
48  large separation
64  hero
5. BO GÓC
Buttons: 8px.
Inputs: 8px.
Small module: 10px.
Functional bento: 12px.
Dialog: 16px.
Không sử dụng pill cho mọi thứ.
Pill chỉ dành status/filter chip.
6. DESKTOP GEOMETRY
≥1400px
Plain text
Sidebar:           240px
Topbar:             64px
Page padding:       28px 32px 40px
Content Khoa:      max 1560px
Content SV/GV:     max 1280px
Grid:               12 cột
Grid gap:           16px
Module vertical:    16–24px
1200–1399px
Plain text
Sidebar:        224px
Page padding:    24px
Grid gap:        16px
992–1199px

Sidebar chuyển compact:

Plain text
Sidebar:       72px
Icon:          20px
Label:         tooltip / hidden
Page padding:  20px
7. TABLET 768–991px
Sidebar → offcanvas.
Topbar 60px.
Bento từ 3 cột → 2 cột.
Khoa allocation table có horizontal scroll.
Inspector chuyển offcanvas-right.
8. MOBILE <768px
Plain text
Topbar:              56px
Bottom nav:          64px + safe area
Page padding:        16px
Grid:                1 cột
Gap:                 12px
Card/list padding:   14px
Form height:         44px minimum
Primary action:      48px

Ở <576px:

Không sidebar.
Không desktop table nếu có thể thay bằng stacked list.
Bottom nav tối đa 5 mục.
Sticky action bar ở đáy cho form quan trọng.

=== PHẦN 4: THÀNH PHẦN ===

1. MENU TRÁI

Desktop:

240px.
Logo zone 64px.
Item 40px.
Icon 18px.
gap 10px.
active: nền accent-soft, text accent, thanh Mosaic 3px bên trái.
Không dùng shadow.

Section label:

11px.
uppercase.
letter spacing .06em.

Mobile: offcanvas, không cố nhồi sidebar vào 390px.

2. TOPBAR

Desktop 64px.

Bao gồm:

breadcrumb/page context.
search optional.
notification.
theme switch.
avatar/menu.

Mobile 56px:

logo symbol + tên page.
notification.
avatar/menu.
3. DẢI SỐ LIỆU

Thay hoàn toàn hàng 6 KPI cards.

Desktop:

Plain text
height: 78–88px
display: grid
background: surface
border-block: 1px

Mỗi metric:

chia bằng border dọc.
label 12px.
value 22–28px.
secondary 11–12px.

Ví dụ Khoa:

100 SV | 43% đã xếp | 30% NV1 | 43% Top 3 | 63,8 điểm TB | 57 chưa xếp

Không icon tròn.

Mobile:

scroll ngang snap hoặc grid 2 × N.
không tạo mỗi metric thành một card riêng.
4. BẢNG

Desktop:

Header 40px.
Row 44–48px.
Header sticky với bảng dài.
Zebra rất nhẹ hoặc không zebra.
Hover đổi surface 1 cấp.
numeric right aligned.
name/text left aligned.

Không dùng quá nhiều badge.

Mobile:

các bảng nghiệp vụ SV/GV chuyển sang stacked rows.
bảng Khoa phức tạp được phép scroll ngang.
5. DANH SÁCH THẺ MOBILE

Topic recommendation:

Plain text
padding: 14px
radius: 12px
border: 1px solid
gap: 10px

Header:

rank 24×24.
title.
score.

Meta:

GV.
field.

AI strip.

Reason.

Actions.

Không card trong card; M1–M5 chỉ là hàng con phẳng.

6. NHÃN TRẠNG THÁI

Pill compact:

height 24px.
padding 4×8px.
font 11/16 600.

Mapping:

Draft → neutral.
OPEN → info.
Pending → warning.
Assigned → success.
Rejected → danger.
Published → teal strong.

Không dùng đỏ/vàng làm trang trí.

7. BUTTON
Primary
bg accent.
height 40 desktop / 44 mobile.
radius 8.
font 13–14 / 600.
Secondary
transparent.
border.
text strong.
Ghost
no border.
hover subtle.
Danger
chỉ cho delete/reject/destructive publish rollback.
Large critical action
44–48px.
8. FORM

Input desktop 40px.
Mobile 44px.

Label:

ở trên.
không placeholder thay label.

Helper/error:

dưới input.

Focus:

border accent.
box-shadow: 0 0 0 3px var(--focus-ring).
9. DANH SÁCH KỸ NĂNG

Không dùng hàng card.

Desktop row:

Skill | Level | Weight/Mandatory | Remove

Height 48px.

Mobile:

skill line.
level phía dưới.
remove icon top-right.

+ Thêm kỹ năng dùng secondary button.

Duplicate → inline error ngay row.

10. KHỐI ĐIỂM M1–M5

Không radar chart.

Desktop
Plain text
M1      M2      M3      M4      M5
82      78      85      76      80
━━━     ━━━     ━━━     ━━━     ━━━

Mỗi model:

label.
descriptor:
M1 Kỹ năng.
M2 Học lực.
M3 Lĩnh vực.
M4 Ngữ nghĩa.
M5 LLM.
score.
bar.
Mobile

5 cột vẫn giữ được nếu width ≥360px.

Màu:

≥75 high.
50–74 medium.
<50 low.

Không tô 5 màu khác nhau chỉ để trang trí.

11. KHỐI LÝ DO GỢI Ý

Header:
Vì sao đề tài này phù hợp?

Tối đa 4 dòng.

Mỗi dòng:

check icon 16.
câu cụ thể.

Ví dụ:

“Kỹ năng Java và SQL đáp ứng 4/5 yêu cầu.”
“Lĩnh vực AI ứng dụng trùng với mức quan tâm 3/3.”
“Điểm môn Cơ sở dữ liệu đạt yêu cầu tiên quyết.”

Không để LLM tạo prose dài hàng đoạn.

12. CHART.JS
Style chung
responsive: true
maintainAspectRatio: false
animation 500ms.
grid line dùng border-soft.
tick text-muted.
no 3D.
no shadow/glow.
legend 12px.
Histogram
bar radius 4.
bar percentage .72.
category percentage .82.
không dùng gradient.
Donut
cutout 72%.
border width 0.
tối đa 4 segments.
Horizontal lecturer load
indexAxis y.
barThickness 14.
quota line nếu cần.
Tooltip
background surface-raised.
text strong.
border 1px.
radius 8.
padding 10.
13. CONFIRM 2 BƯỚC
Bước 1 — Chốt kết quả

Modal:

số SV assigned.
unassigned.
overload.
invalid constraints.
note: “Sau khi chốt, thuật toán không tự chạy lại.”

CTA:
Chốt bản phân công.

Bước 2 — Công bố

Modal khác hoàn toàn.

Hiển thị:

thời điểm.
số SV nhận kết quả.
cảnh báo đây là hành động official.

Yêu cầu nhập:

CONG BO

hoặc checkbox xác nhận tùy scope.

CTA danger/strong:
Công bố kết quả chính thức.

Không gộp Chốt + Công bố thành một nút.

14. EMPTY STATE

Kích thước minh họa:

desktop 112–144px.
mobile 88–112px.

Cấu trúc:

SVG.
heading.
mô tả ≤2 dòng.
tối đa 1 CTA chính + 1 phụ.
15. THÔNG BÁO
Inline alert

Form/process issue.

Toast

Save success.
Update success.
Import completed.

Placement:

desktop top-right.
mobile top-center.

Toast 4–5 giây.

Không dùng toast cho lỗi nghiêm trọng cần người dùng xử lý.

=== PHẦN 5: CHUYỂN ĐỘNG ===

Mosaic AI phải có cảm giác nhanh, chính xác, bình tĩnh, không “AI neon”.

Micro interaction
Hover: 120ms.
Button press: 80ms.
Menu/item: 140ms.
Drawer/offcanvas: 220ms.
Modal: 180ms.
Chart reveal: 450–550ms.
Page content entrance: tối đa 240ms.

Easing chuẩn:

CSS
--ease-standard: cubic-bezier(.2, .8, .2, 1);
--ease-enter: cubic-bezier(.16, 1, .3, 1);
--ease-exit: cubic-bezier(.4, 0, 1, 1);

Khoảng dịch:

section: 8px.
modal: 12px.
drawer: theo chiều mở.
Không dịch 30–50px.

Stagger:

tối đa 40ms giữa các module.
tối đa 4 phần tử.
bảng không animate từng row.
AI score

Khi vừa nhận recommendation:

bar M1–M5 grow 0 → score.
400ms.
stagger 35ms.

Không chạy lại animation mỗi lần scroll.

ILP running

Không spinner khổng lồ.

Hiện process line:
Chuẩn bị dữ liệu → Kiểm tra ràng buộc → Tối ưu → Lưu bản nháp

Active step pulse rất nhẹ.

Reduce motion
CSS
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    scroll-behavior: auto !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

=== PHẦN 6: LOGO SVG ===

Bản sáng

Dùng trên nền sáng.

<svg
  width="48"
  height="48"
  viewBox="0 0 48 48"
  fill="none"
  xmlns="http://www.w3.org/2000/svg"
  role="img"
  aria-labelledby="mosaic-ai-light-title"
>
  <title id="mosaic-ai-light-title">Mosaic AI</title>

  <!-- Tile 1 -->
  <rect
    x="4"
    y="4"
    width="18"
    height="18"
    rx="4"
    fill="#005F73"
  />

  <!-- Tile 2 -->
  <rect
    x="26"
    y="4"
    width="18"
    height="12"
    rx="4"
    fill="#EE9B00"
  />

  <!-- Tile 3 -->
  <rect
    x="26"
    y="20"
    width="18"
    height="24"
    rx="4"
    fill="#0A9396"
  />

  <!-- Tile 4 -->
  <rect
    x="4"
    y="26"
    width="10"
    height="18"
    rx="4"
    fill="#7A7D2D"
  />

  <!-- Tile 5 -->
  <rect
    x="18"
    y="26"
    width="4"
    height="18"
    rx="2"
    fill="#9B2226"
  />
</svg>
Bản tối

Dùng trên #111315 hoặc bề mặt tối.

<svg
  width="48"
  height="48"
  viewBox="0 0 48 48"
  fill="none"
  xmlns="http://www.w3.org/2000/svg"
  role="img"
  aria-labelledby="mosaic-ai-dark-title"
>
  <title id="mosaic-ai-dark-title">Mosaic AI</title>

  <!-- Tile 1 -->
  <rect
    x="4"
    y="4"
    width="18"
    height="18"
    rx="4"
    fill="#22B3AD"
  />

  <!-- Tile 2 -->
  <rect
    x="26"
    y="4"
    width="18"
    height="12"
    rx="4"
    fill="#E9B949"
  />

  <!-- Tile 3 -->
  <rect
    x="26"
    y="20"
    width="18"
    height="24"
    rx="4"
    fill="#48BFAF"
  />

  <!-- Tile 4 -->
  <rect
    x="4"
    y="26"
    width="10"
    height="18"
    rx="4"
    fill="#B4B84A"
  />

  <!-- Tile 5 -->
  <rect
    x="18"
    y="26"
    width="4"
    height="18"
    rx="2"
    fill="#E76F51"
  />
</svg>
Wordmark
Plain text
[Mosaic symbol] Mosaic AI
Mosaic: Sora 700.
AI: Sora 600.
Không gradient.
Không tagline nằm trong logo chính.
Khoảng symbol → chữ: 10px.

=== PHẦN 7: THỨ TỰ VẼ & DUYỆT ===

Không cho Claude redesign toàn bộ 22 màn cùng lúc. Vẽ và duyệt theo các “anchor screens” trước; khi 3 vai trò đã ổn mới nhân design system.

Vòng 1 — Khóa ngôn ngữ sản phẩm

1. Khoa — Phân công / Desktop 1440px, light

Quan trọng nhất vì chứa:

metric strip mới.
bento.
chart.
table.
filter.
ILP.
phase 2.
finalize.

Nếu trang này chưa premium thì chưa làm tiếp.

2. Cùng trang Khoa — Dark mode 1440px

Kiểm tra dark mode là một theme thật, không phải đảo màu.

3. SV — Trang chủ / 390px light

Khóa:

mobile shell.
recommendation card.
M1–M5.
reason block.
bottom nav.

4. SV — Trang chủ / 390px dark

Khóa hệ màu mobile tối.

Vòng 2 — Khóa luồng AI

5. SV — Chi tiết đề tài / 390px

Điểm tổng + M1–M5 + eligibility + explanation + nguyện vọng.

6. SV — Hồ sơ năng lực / 390px

Kiểm tra form động skill/field thực sự dùng được.

7. SV — Nguyện vọng NV1–NV3 / 390px

Khóa flow đăng ký.

Vòng 3 — Khóa workflow giảng viên

8. GV — Trang chủ / 1280–1440px

9. GV — Sinh viên đăng ký / desktop

Đặc biệt side inspector + AI score + Đồng ý/Từ chối.

10. GV — Form thêm/sửa đề tài

Kiểm tra dynamic skill/prerequisite rows.

Vòng 4 — Khoa nâng cao

11. Khoa — Thống kê

Khóa toàn bộ chart language.

12. Khoa — Nhập Excel

Khóa upload / validation / error presentation.

13. Khoa — Phase 2 manual assignment

Có thể vẽ state riêng từ trang Phân công.

14. Khoa — Chốt & Công bố

Vẽ hai modal state để kiểm tra workflow nguy hiểm.

Vòng 5 — Danh mục và trạng thái

15. SV — Danh sách đề tài desktop + 390px.

16. GV — Đề tài của tôi.

17. Khoa — Trang chủ.

18. SV — Kết quả phân công.

Vòng 6 — System pages

19. Login light/dark.

20. Thiếu hồ sơ.

21. Đổi mật khẩu + success.

22. 403 / 404 / 500 family.

Điều kiện để Design Authority duyệt implementation

Mỗi anchor screen phải được QA tối thiểu ở:

Plain text
390px
768px
992px
1440px

Với các màn quan trọng phải có cả:

Plain text
Light
Dark
Loading
Empty / zero
Long text
Realistic populated data

Riêng Khoa / Phân công bắt buộc QA thêm:

100 SV.
43 đã xếp.
57 chưa xếp.
30% NV1.
43% Top 3.
63,8 điểm trung bình.
trạng thái trước chạy ILP.
đang chạy.
sau chạy.
phase 2.
đã chốt.
đã công bố.

Sau khi 4 ảnh anchor đầu tiên được chủ dự án duyệt, Claude mới được phép triển khai global shell + CSS tokens + component primitives và nhân ra toàn bộ màn hình.