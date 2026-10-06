DESIGN-v2 — Capstone Advisor AI
0. Mục tiêu thiết kế

DESIGN-v2 phải khiến hệ thống trông như một sản phẩm dữ liệu học thuật có AI, không còn giống “Bootstrap admin template”.

Không chạy theo phong cách AI neon/cyberpunk. Không dùng xanh dương Bootstrap làm thương hiệu chính. Không biến mọi thứ thành card. Không dùng màu trạng thái để trang trí.

Tinh thần tổng thể:

Academic Intelligence × Editorial Data × Calm Enterprise

Giao diện lấy chữ, số liệu và cấu trúc thông tin làm trung tâm. Nền sáng hơi ấm, chữ gần đen, xanh teal sâu tạo cảm giác học thuật + công nghệ, mint sáng chỉ xuất hiện ở điểm hành động/AI. Những khu vực quan trọng có thể dùng “dark island” teal đậm để tạo bản sắc thay vì toàn bộ trang trắng-xanh đồng dạng.

3 từ khóa cá tính: Điềm tĩnh — Sắc sảo — Học thuật

Web tham chiếu về tinh thần
Linear — hierarchy cực rõ, ít đường viền, typography mạnh.
Mercury — màu sắc trưởng thành, số liệu tài chính/data được trình bày có trọng lượng.
Vercel Dashboard — mật độ dữ liệu cao nhưng chrome UI rất tiết chế.

Không copy giao diện của họ. Chỉ học nguyên tắc: ít màu, nhiều phân cấp, khoảng trắng có chủ đích, dữ liệu là nhân vật chính.

Thẻ nguyên liệu áp dụng
color|cyber-deep-teal-and-slate-palette
color|teal-on-wordmark-and-buttons
Một phần tư duy layout từ layout|column-arithmetic-token-grid, nhưng không dùng full-bleed column arithmetic cho dashboard vì không phù hợp với app có navbar/container cố định.
1. Design Tokens
1.1 Font

Dùng Be Vietnam Pro toàn hệ thống.

Lý do:

hỗ trợ tiếng Việt tốt;
số rõ;
hiện đại nhưng không “startup quá đà”;
đủ weight cho dashboard;
giảm việc phối nhiều font.

Import duy nhất trong design-v2.css:

CSS
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');
1.2 :root hoàn chỉnh
CSS
:root {
  /* =========================================================
     CAPSTONE ADVISOR AI — DESIGN V2
     Academic Intelligence / Editorial Data
     ========================================================= */

  /* ---------- FONT ---------- */
  --font-sans: "Be Vietnam Pro", system-ui, -apple-system,
               BlinkMacSystemFont, "Segoe UI", sans-serif;

  /* ---------- BRAND ---------- */
  --brand-950: #052E2B;
  --brand-900: #073B37;
  --brand-800: #0A514B;
  --brand-700: #0C6860;
  --brand-600: #0F7F74;

  --accent-500: #18C5AD;
  --accent-400: #31D6BE;
  --accent-100: #DDF8F2;
  --accent-50:  #EFFBF8;

  /* ---------- NEUTRAL / PAPER ---------- */
  --bg-page:      #F4F5F2;
  --bg-subtle:    #ECEFEB;
  --surface-1:    #FFFFFF;
  --surface-2:    #F9FAF8;
  --surface-3:    #F0F2EF;
  --surface-dark: #073B37;

  --text-strong:  #17201E;
  --text:         #2B3532;
  --text-muted:   #66716D;
  --text-faint:   #88918E;
  --text-on-dark: #F5FBF9;

  --border:       #DCE2DE;
  --border-soft:  #E9ECE9;
  --border-strong:#B7C1BC;

  /* ---------- INTERACTION ---------- */
  --focus:        #18C5AD;
  --link:         #086B62;
  --link-hover:   #054D47;

  /* ---------- STATUS ---------- */
  --success:      #18794E;
  --success-bg:   #E8F5EE;
  --success-line: #B6DEC8;

  --warning:      #946200;
  --warning-bg:   #FFF6D8;
  --warning-line: #E8CF82;

  --danger:       #B42318;
  --danger-bg:    #FDECEA;
  --danger-line:  #F0B9B4;

  --info:         #35689A;
  --info-bg:      #EAF2FA;
  --info-line:    #BCD2E7;

  --neutral-status:    #58625E;
  --neutral-status-bg: #EEF0EF;

  /* ---------- DATA VISUALIZATION ---------- */
  --chart-1: #0F7F74;
  --chart-2: #4777A8;
  --chart-3: #7C67B5;
  --chart-4: #B4772A;
  --chart-5: #4E8C56;
  --chart-6: #A65C79;

  /* ---------- TYPOGRAPHY SCALE ---------- */
  --fs-11: 0.6875rem;
  --fs-12: 0.75rem;
  --fs-13: 0.8125rem;
  --fs-14: 0.875rem;
  --fs-16: 1rem;
  --fs-18: 1.125rem;
  --fs-20: 1.25rem;
  --fs-24: 1.5rem;
  --fs-28: 1.75rem;
  --fs-32: 2rem;
  --fs-40: 2.5rem;
  --fs-48: 3rem;

  /* ---------- LINE HEIGHT ---------- */
  --lh-tight: 1.2;
  --lh-heading: 1.32;
  --lh-body: 1.6;

  /* ---------- SPACING 4/8 SYSTEM ---------- */
  --sp-1: 4px;
  --sp-2: 8px;
  --sp-3: 12px;
  --sp-4: 16px;
  --sp-5: 20px;
  --sp-6: 24px;
  --sp-8: 32px;
  --sp-10: 40px;
  --sp-12: 48px;
  --sp-16: 64px;

  /* ---------- RADIUS ---------- */
  --radius-xs: 6px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 22px;
  --radius-pill: 999px;

  /* ---------- SHADOW ---------- */
  --shadow-xs:
    0 1px 2px rgba(16, 24, 20, .04);

  --shadow-sm:
    0 1px 2px rgba(16, 24, 20, .04),
    0 6px 20px rgba(16, 24, 20, .045);

  --shadow-md:
    0 2px 4px rgba(16, 24, 20, .05),
    0 14px 36px rgba(16, 24, 20, .07);

  /* ---------- LAYOUT ---------- */
  --content-max: 1360px;
  --reading-max: 820px;
  --sidebar-w: 296px;
  --nav-h: 64px;

  /* ---------- TRANSITIONS ---------- */
  --ease: cubic-bezier(.2, .8, .2, 1);
  --duration-fast: 140ms;
  --duration: 200ms;
}

Global baseline:

CSS
html {
  font-size: 16px;
}

body {
  margin: 0;
  font-family: var(--font-sans);
  font-size: var(--fs-14);
  line-height: var(--lh-body);
  color: var(--text);
  background: var(--bg-page);
  -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4, h5, h6 {
  color: var(--text-strong);
  line-height: var(--lh-heading);
  letter-spacing: -0.025em;
}

h1 {
  font-size: clamp(1.75rem, 3vw, 2.5rem);
  font-weight: 700;
}

h2 {
  font-size: var(--fs-24);
  font-weight: 700;
}

h3 {
  font-size: var(--fs-18);
  font-weight: 650;
}

a {
  color: var(--link);
  text-decoration-thickness: 1px;
  text-underline-offset: 3px;
}

a:hover {
  color: var(--link-hover);
}

:focus-visible {
  outline: 3px solid rgba(24, 197, 173, .38);
  outline-offset: 2px;
}
2. Luật hệ thống bắt buộc
2.1 Chống “hộp trong hộp”

Đây là lỗi lớn nhất của bản hiện tại.

Luật 1 — Một vùng chức năng chỉ có tối đa 1 surface

Sai:

Plain text
Card
 └─ Card
     └─ Alert
         └─ KPI box

Đúng:

Plain text
Section
 ├─ Heading
 ├─ Content
 └─ Divider

Hoặc:

Plain text
Surface
 ├─ Heading
 ├─ Data
 └─ Actions
Luật 2 — Không dùng card chỉ để tạo khoảng cách

Nếu nội dung chỉ cần phân nhóm:

CSS
.section-block {
  padding-block: var(--sp-8);
  border-bottom: 1px solid var(--border-soft);
}

Không:

XML
<div class="card">
  <div class="card">
Luật 3 — Trong một card không được có card khác

Ngoại lệ duy nhất:

preview kết quả;
modal;
expandable detail có ngữ nghĩa độc lập.
Luật 4 — Dùng divider trước khi dùng background

Ưu tiên:

whitespace;
typography;
divider;
đổi nền;
cuối cùng mới dùng border/card.
3. Màu trạng thái
3.1 Đỏ

Đỏ chỉ dùng cho:

thao tác phá hủy;
lỗi validation thực tế;
hệ thống thất bại;
quá hạn nghiêm trọng;
từ chối đã xác nhận.

Không dùng đỏ cho:

“chưa đủ điều kiện”;
điểm thấp;
nút Xóa lặp lại 10 lần;
cột chart vì giá trị cao;
dữ liệu chưa có.

Ví dụ Chưa đủ điều kiện:

Plain text
Không đủ điều kiện
Thiếu: GPA tối thiểu 3.0

Màu neutral hoặc warning, không phải danger.

3.2 Vàng

Vàng chỉ biểu thị:

cần chú ý;
sắp hết hạn;
thiếu một số dữ liệu;
cần người dùng xem xét;
chưa đạt điều kiện nhưng có thể khắc phục.

Không dùng vàng làm màu nền cả hàng bảng.

3.3 Xanh lá

Chỉ dùng cho trạng thái đã đạt:

Đủ điều kiện
Đã duyệt
Đã phân công
Hoàn thành
Published
3.4 Màu thương hiệu teal

Teal không phải màu trạng thái.

Teal dùng cho:

CTA chính;
tab active;
selected state;
điểm nhấn AI;
liên kết;
progress chủ đạo;
chart series chính.
4. Quy tắc số liệu lớn / KPI

Một KPI phải có đúng 4 tầng:

Plain text
NHÃN
48%
+6,2 điểm so với kỳ trước
Tỷ lệ Top 1

Không nhồi icon, badge, progress và mô tả vào cùng một thẻ.

CSS
CSS
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--sp-4);
}

.kpi {
  min-width: 0;
  padding: 20px 0;
  border-top: 1px solid var(--border);
}

.kpi__label {
  margin-bottom: 8px;
  color: var(--text-muted);
  font-size: var(--fs-12);
  font-weight: 600;
  letter-spacing: .06em;
  text-transform: uppercase;
}

.kpi__value {
  color: var(--text-strong);
  font-size: clamp(2rem, 3vw, 3rem);
  font-weight: 700;
  letter-spacing: -.05em;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.kpi__meta {
  margin-top: 10px;
  color: var(--text-muted);
  font-size: var(--fs-13);
}

@media (max-width: 767.98px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0 20px;
  }

  .kpi__value {
    font-size: 2rem;
  }
}

Không dùng 4 card Excel cạnh nhau nữa.

5. Thanh menu
Desktop

Navbar trở thành thanh application shell thực sự.

cao 64px;
nền gần trắng;
dưới có border;
logo nằm trái;
navigation ở giữa/trái;
account và logout phải;
active bằng chữ đậm + indicator 2px, không phải tab Bootstrap pill.
CSS
.app-navbar {
  min-height: var(--nav-h);
  background: rgba(249, 250, 248, .94);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(12px);
}

.app-brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: var(--brand-900);
  font-weight: 700;
  letter-spacing: -.025em;
  text-decoration: none;
}

.app-brand__mark {
  display: grid;
  width: 30px;
  height: 30px;
  place-items: center;
  border-radius: 8px;
  background: var(--brand-900);
  color: var(--accent-400);
  font-size: 11px;
  font-weight: 800;
}

.app-nav-link {
  position: relative;
  padding: 22px 12px 20px;
  color: var(--text-muted);
  font-weight: 500;
  text-decoration: none;
}

.app-nav-link:hover,
.app-nav-link.is-active {
  color: var(--text-strong);
}

.app-nav-link.is-active::after {
  content: "";
  position: absolute;
  right: 12px;
  bottom: -1px;
  left: 12px;
  height: 2px;
  border-radius: 2px 2px 0 0;
  background: var(--brand-700);
}
Mobile

390px:

logo + tên rút gọn;
avatar;
menu button 44×44;
menu mở dạng offcanvas Bootstrap;
menu item cao tối thiểu 48px.

Không cố nhét 5 tab ngang vào 390px.

6. Nút
Quy tắc
Primary

Một màn hình chỉ nên có 1 primary action nổi bật.

CSS
.btn-v2 {
  min-height: 42px;
  padding: 9px 15px;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: var(--fs-14);
  transition:
    transform var(--duration-fast) var(--ease),
    background var(--duration-fast) var(--ease),
    border-color var(--duration-fast) var(--ease);
}

.btn-v2-primary {
  border: 1px solid var(--brand-900);
  background: var(--brand-900);
  color: #fff;
}

.btn-v2-primary:hover {
  border-color: var(--brand-800);
  background: var(--brand-800);
  color: #fff;
}

.btn-v2-secondary {
  border: 1px solid var(--border-strong);
  background: var(--surface-1);
  color: var(--text-strong);
}

.btn-v2-secondary:hover {
  background: var(--surface-3);
}

.btn-v2-danger {
  border: 1px solid var(--danger-line);
  background: var(--surface-1);
  color: var(--danger);
}

.btn-v2-danger:hover {
  background: var(--danger-bg);
}
Mobile
CSS
@media (max-width: 575.98px) {
  .btn-v2 {
    min-height: 46px;
  }
}

Không tự động width:100% cho mọi button.

7. Dangerous Action — xác nhận 2 bước

Không để 8 nút “Xóa” đỏ trên màn hình.

Ban đầu:

Plain text
⋯

Mở dropdown:

Plain text
Xóa kỹ năng

Sau đó modal:

Plain text
Xóa “Java”?

Kỹ năng này sẽ bị xóa khỏi hồ sơ.
Thao tác chỉ có hiệu lực sau khi anh lưu hồ sơ.

[Hủy] [Xóa kỹ năng]

Nút destructive chỉ đỏ ở bước cuối cùng.

8. Nhãn trạng thái

Không dùng .badge.bg-primary, .bg-danger, .bg-warning.

CSS
.status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 26px;
  padding: 4px 9px;
  border: 1px solid transparent;
  border-radius: var(--radius-pill);
  font-size: var(--fs-12);
  font-weight: 600;
  white-space: nowrap;
}

.status::before {
  content: "";
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.status-success {
  color: var(--success);
  background: var(--success-bg);
  border-color: var(--success-line);
}

.status-warning {
  color: var(--warning);
  background: var(--warning-bg);
  border-color: var(--warning-line);
}

.status-danger {
  color: var(--danger);
  background: var(--danger-bg);
  border-color: var(--danger-line);
}

.status-neutral {
  color: var(--neutral-status);
  background: var(--neutral-status-bg);
}
9. Bảng dữ liệu desktop

Bảng Khoa phải giống công cụ vận hành dữ liệu, không giống HTML table 2014.

CSS
.data-shell {
  overflow: hidden;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  background: var(--surface-1);
}

.data-table {
  margin: 0;
  font-size: var(--fs-13);
}

.data-table thead th {
  padding: 11px 14px;
  border-bottom: 1px solid var(--border);
  background: var(--surface-2);
  color: var(--text-muted);
  font-size: var(--fs-11);
  font-weight: 700;
  letter-spacing: .045em;
  text-transform: uppercase;
  white-space: nowrap;
}

.data-table tbody td {
  padding: 13px 14px;
  border-bottom: 1px solid var(--border-soft);
  vertical-align: middle;
}

.data-table tbody tr:last-child td {
  border-bottom: 0;
}

.data-table tbody tr:hover {
  background: #F7F9F7;
}

.data-table .number {
  font-variant-numeric: tabular-nums;
  text-align: right;
}

.data-table .primary-cell {
  color: var(--text-strong);
  font-weight: 600;
}
Quan trọng

Không tô vàng toàn bộ sinh viên chưa phân công.

Thay bằng:

XML
<span class="status status-warning">Chưa xếp</span>

Chỉ cell trạng thái có màu.

10. Mobile: bỏ table, chuyển sang record list

Ở ≤767px, không ép bảng desktop co lại.

CSS
.mobile-record-list {
  display: none;
}

@media (max-width: 767.98px) {
  .desktop-table {
    display: none;
  }

  .mobile-record-list {
    display: block;
  }
}

.record-item {
  padding: 16px 0;
  border-bottom: 1px solid var(--border);
}

.record-item__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.record-item__title {
  margin: 0;
  color: var(--text-strong);
  font-size: var(--fs-14);
  font-weight: 650;
}

.record-item__meta {
  margin-top: 4px;
  color: var(--text-muted);
  font-size: var(--fs-12);
}

.record-item__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px 16px;
  margin-top: 14px;
}

.record-kv dt {
  color: var(--text-faint);
  font-size: var(--fs-11);
}

.record-kv dd {
  margin: 2px 0 0;
  color: var(--text);
  font-size: var(--fs-13);
}

Một sinh viên mobile chỉ khoảng 120–170px, không phải card 400px.

11. Form
Input
CSS
.form-label {
  margin-bottom: 7px;
  color: var(--text-strong);
  font-size: var(--fs-13);
  font-weight: 600;
}

.form-control,
.form-select {
  min-height: 44px;
  border-color: var(--border-strong);
  border-radius: var(--radius-sm);
  background-color: var(--surface-1);
  color: var(--text);
  font-size: var(--fs-14);
  box-shadow: none !important;
}

.form-control:hover,
.form-select:hover {
  border-color: #909C97;
}

.form-control:focus,
.form-select:focus {
  border-color: var(--brand-700);
  box-shadow: 0 0 0 3px rgba(15, 127, 116, .12) !important;
}

.form-text {
  margin-top: 6px;
  color: var(--text-muted);
  font-size: var(--fs-12);
}
12. Formset kỹ năng — thiết kế mới

Formset không còn là “table Django”.

Desktop
Plain text
KỸ NĂNG                          MỨC ĐỘ           HÀNH ĐỘNG
Java                             ●●●●○  4/5      ⋯
MySQL                            ●●●○○  3/5      ⋯
UML                              ●●●○○  3/5      ⋯
────────────────────────────────────────────────────
+ Thêm kỹ năng

Select kỹ năng và mức độ chỉ chuyển sang input khi user bấm Edit.

CSS
CSS
.formset-row {
  display: grid;
  grid-template-columns: minmax(220px, 1fr) 220px 44px;
  gap: 16px;
  align-items: center;
  min-height: 58px;
  border-bottom: 1px solid var(--border-soft);
}

.level-picker {
  display: flex;
  align-items: center;
  gap: 5px;
}

.level-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--border-strong);
}

.level-dot.is-filled {
  background: var(--brand-700);
}
Mobile

Không lặp label 8 lần thành form card dài.

Mỗi item:

Plain text
Java                                  ⋯
Khá · 4/5

Tap item → mở Bootstrap collapse/editor.

13. Empty state

Empty state phải trả lời 3 câu:

Chuyện gì đang xảy ra?
Vì sao?
Tôi làm gì tiếp?
CSS
.empty-state {
  max-width: 620px;
  margin: 72px auto;
  text-align: center;
}

.empty-state__icon {
  display: grid;
  width: 56px;
  height: 56px;
  margin: 0 auto 20px;
  place-items: center;
  border-radius: 14px;
  background: var(--surface-3);
  color: var(--brand-800);
}

.empty-state h2 {
  margin-bottom: 8px;
}

.empty-state p {
  max-width: 520px;
  margin-inline: auto;
  color: var(--text-muted);
}

Không tạo card 1000px chỉ để đặt icon ở giữa.

14. Chart.js — nguyên tắc
Tuyệt đối cấm
cột đỏ mặc định;
rainbow chart;
gridline dày;
chart title lặp lại H2;
legend nếu chart chỉ có 1 series;
donut có 9 segment màu.
Mẫu options
JavaScript
const chartText = '#66716D';
const chartGrid = '#E9ECE9';

const baseChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  animation: {
    duration: 450
  },
  interaction: {
    mode: 'index',
    intersect: false
  },
  plugins: {
    legend: {
      display: false,
      labels: {
        color: chartText,
        usePointStyle: true,
        boxWidth: 8,
        boxHeight: 8,
        font: {
          family: "'Be Vietnam Pro', sans-serif",
          size: 12,
          weight: '500'
        }
      }
    },
    tooltip: {
      backgroundColor: '#17201E',
      titleColor: '#FFFFFF',
      bodyColor: '#E7ECE9',
      padding: 12,
      cornerRadius: 8,
      displayColors: false,
      titleFont: {
        family: "'Be Vietnam Pro', sans-serif",
        weight: '600'
      },
      bodyFont: {
        family: "'Be Vietnam Pro', sans-serif"
      }
    }
  },
  scales: {
    x: {
      border: {
        display: false
      },
      grid: {
        display: false
      },
      ticks: {
        color: chartText,
        maxRotation: 0,
        font: {
          family: "'Be Vietnam Pro', sans-serif",
          size: 11
        }
      }
    },
    y: {
      beginAtZero: true,
      border: {
        display: false
      },
      grid: {
        color: chartGrid
      },
      ticks: {
        color: chartText,
        font: {
          family: "'Be Vietnam Pro', sans-serif",
          size: 11
        }
      }
    }
  }
};

Dataset:

JavaScript
{
  label: 'Sinh viên',
  data: values,
  backgroundColor: '#0F7F74',
  borderRadius: 5,
  borderSkipped: false,
  maxBarThickness: 34
}

Nếu highlight một cột:

JavaScript
backgroundColor: values.map((_, i) =>
  i === activeIndex ? '#0F7F74' : '#DCE7E3'
)

Không dùng đỏ để nói “21 sinh viên”.

15. Trang đăng nhập
Desktop

Không còn một card bé trôi giữa 1440px.

Layout
Plain text
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   LEFT 56%                         RIGHT 44%                  │
│                                                              │
│   CAPSTONE ADVISOR AI              Đăng nhập                 │
│                                                              │
│   Phân công đề tài tốt nghiệp      Tài khoản                 │
│   dựa trên dữ liệu, năng lực       [________________]        │
│   và tối ưu hóa.                   Mật khẩu                  │
│                                    [________________]        │
│   ┌─────────────────────────┐      [ Đăng nhập → ]           │
│   │ dark data visual island │                              │
│   │ M1  M2  M3  M4  M5      │      Demo                     │
│   │ → Recommendation         │      SV · GV · Khoa           │
│   └─────────────────────────┘                                │
│                                                              │
│   Khoa CNTT · EAUT                                          │
└──────────────────────────────────────────────────────────────┘

Left panel brand-950.

Không cần illustration cầu kỳ. Dùng data motif hình học đơn giản:

Plain text
M1 → M2 → M3 → M4 → M5
            ↓
        TOP MATCH

để nói lên bản chất sản phẩm.

CSS
CSS
.login-shell {
  min-height: 100dvh;
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(420px, .85fr);
}

.login-brand {
  position: relative;
  overflow: hidden;
  padding: clamp(48px, 6vw, 92px);
  background: var(--brand-950);
  color: var(--text-on-dark);
}

.login-brand h1 {
  max-width: 680px;
  color: white;
  font-size: clamp(2.5rem, 5vw, 4.75rem);
}

.login-panel {
  display: grid;
  align-items: center;
  padding: 48px clamp(32px, 7vw, 100px);
  background: var(--surface-1);
}

.login-form {
  width: 100%;
  max-width: 440px;
}
Mobile 390px

Bỏ split screen.

Plain text
Dark brand header ~190px
CAPSTONE ADVISOR AI
Tư vấn & phân công ĐATN bằng AI

White form
Đăng nhập
[...]
[...]
[Đăng nhập →]

Tài khoản demo
Sinh viên / Giảng viên / Khoa

Không căn card giữa viewport.

16. Trang Phân công Khoa — redesign triệt để

Đây là trang ưu tiên số 1.

Desktop

Không còn:

6 KPI card;
hàng vàng;
toolbar dày;
bảng dài không hierarchy.
Layout mới
Plain text
Phân công đề tài tốt nghiệp
Đợt ĐATN 2026 · 100 sinh viên

[Báo cáo thống kê]      [Chạy lại phân công]

────────────────────────────────────────────

43%        30%        43%        5
NV1        NV2        Top 3      Chưa xếp

98/100 SV đã xử lý                    Cập nhật 10:42
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Tất cả 100] [Chưa xếp 5] [Có cảnh báo 7]

Tìm sinh viên...   Nguyện vọng ▾   Giảng viên ▾   Sắp xếp ▾

┌─────────────────────────────────────────────────────────────┐
│ SV           GPA   NGUYỆN VỌNG   ĐỀ TÀI      GV   TRẠNG THÁI│
│ Hoàng...     3.08  NV1            ...          ...  Đã xếp   │
│ Nguyễn...    2.81  NV1            ...          ...  Đã xếp   │
│ ...                                                         │
└─────────────────────────────────────────────────────────────┘
“Chưa xếp”

Không tô vàng hàng.

Plain text
Trần Ngọc Thịnh       GPA 2.73       —       Chưa xếp

Chỉ badge trạng thái vàng.

Chi tiết một record

Không nhồi vào row.

Click row → Bootstrap Offcanvas bên phải:

Plain text
Trần Ngọc Thịnh
20230004 · GPA 2.73

NGUYỆN VỌNG
1. Hệ thống A
2. Hệ thống B
3. Hệ thống C

ĐIỂM PHÙ HỢP
M1 82
M2 67
M3 91
M4 76
M5 84

Phân công hiện tại
Chưa xếp

[Điều chỉnh thủ công]
Mobile 390px

Thứ tự phải là:

Plain text
Phân công
ĐATN 2026

43% NV1   30% NV2
43% Top3  5 chưa xếp

[Tất cả] [Chưa xếp] [Cảnh báo]

[Tìm kiếm................]

Hoàng Quang Phúc          Đã xếp
20230001 · GPA 3.08
NV1 · 63,8 điểm
Giảng viên: Nguyễn Minh Bình
────────────────────────────────

Nguyễn Thu Hằng           Đã xếp
...

Không render <table>.

17. Trang Thống kê Khoa
Desktop

Hiện tại có quá nhiều container ngang nhau.

Chuyển thành kiểu data editorial report.

Plain text
Thống kê & Báo cáo Khoa
ĐATN 2026                     [Xuất báo cáo]

48%          43%          30%          5
Top 3        NV1          NV2          Chưa xếp

────────────────────────────────────────────

TÌNH HÌNH ĐĂNG KÝ
100 / 100 sinh viên
━━━━━━━━━━━━━━━━━━━━━━━

────────────────────────────────────────────

PHÂN BỔ NGUYỆN VỌNG THEO LĨNH VỰC

[ BAR CHART 8 categories                     ]

AI                       33
Dữ liệu                  28
Web                      22
...

────────────────────────────────────────────

ĐỀ TÀI CÓ NHU CẦU CAO

01  Khoe dữ liệu & báo cáo điểm        21 / 5
    Nguyễn Minh Bình
    Cạnh tranh cao

02  Ứng dụng ...                       18 / 5
Thay donut

Chart “100 đăng ký / 0 chưa đăng ký” không cần donut lớn.

Dùng progress + text:

Plain text
Đã đăng ký
100 / 100                               100%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Top đề tài

Không dựng 10 cột đỏ.

Dùng horizontal ranking list vì người dùng cần đọc tên + so sánh lượng, không cần chiêm ngưỡng chart.

CSS
.rank-row {
  display: grid;
  grid-template-columns: 28px minmax(0, 1fr) auto;
  gap: 12px;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--border-soft);
}
Mobile

Không đưa tất cả chart desktop xuống một cột dài 12.000px.

Ưu tiên:

4 KPI.
Đăng ký.
Top lĩnh vực.
Top 5 đề tài.
Nút “Xem toàn bộ báo cáo” để mở dữ liệu phụ.

Mobile không cần hiển thị Top 10 mặc định.

18. Hồ sơ sinh viên
Desktop

Chuyển từ “các card giống nhau” thành profile workspace.

Plain text
Hồ sơ năng lực                            Đã lưu 14:32
Thông tin được dùng để AI đánh giá...

Hoàn thiện hồ sơ 100%
Giới thiệu ✓  Kỹ năng ✓  Lĩnh vực ✓

──────────────────────────────────────────────────

01 / GIỚI THIỆU BẢN THÂN

[ textarea ...................................... ]
                                             103/500

──────────────────────────────────────────────────

02 / KỸ NĂNG                              + Thêm

Java                        ●●●●○ 4/5       ⋯
UML                         ●●●○○ 3/5       ⋯
MySQL                       ●●●○○ 3/5       ⋯
SQL                         ●●●●○ 4/5       ⋯

──────────────────────────────────────────────────

03 / LĨNH VỰC QUAN TÂM

Trí tuệ nhân tạo
Quan tâm cao            ●●●

Backend
Quan tâm vừa            ●●○

Data Engineering
Quan tâm cao            ●●●

                                       [Lưu thay đổi]

Không dùng progress full-width 100%.

Thang kỹ năng

Bắt buộc ghi nghĩa ngay một lần:

Plain text
1 Mới học · 2 Cơ bản · 3 Khá · 4 Tốt · 5 Thành thạo
Thang lĩnh vực

Không giả vờ giống kỹ năng:

Plain text
Mức quan tâm
○ Thấp
○ Vừa
● Cao

Hai mental model tách biệt hoàn toàn.

Mobile

Top:

Plain text
Hồ sơ năng lực
100% hoàn thiện

[Giới thiệu] [Kỹ năng] [Lĩnh vực]

Có thể dùng Bootstrap accordion/anchor section.

Mỗi kỹ năng compact 60–72px, không 300–400px.

CTA save dùng sticky bottom action:

CSS
@media (max-width: 767.98px) {
  .mobile-save-bar {
    position: sticky;
    bottom: 0;
    z-index: 20;
    margin-inline: -16px;
    padding: 10px 16px calc(10px + env(safe-area-inset-bottom));
    border-top: 1px solid var(--border);
    background: rgba(255,255,255,.96);
    backdrop-filter: blur(10px);
  }
}
19. Chi tiết đề tài

Phải bỏ cụm 5 vòng tròn M1–M5.

M1–M5 là cấu trúc thuật toán nội bộ, không nên biến thành “5 cái đồng hồ lỗi”.

Desktop
Plain text
← Danh sách đề tài

Hệ thống gợi ý và dự báo điểm sinh viên
Trí tuệ nhân tạo · Khó                          Đang mở

Nguyễn Minh Bình
5 vị trí · 21 nguyện vọng

────────────────────────────────────────────────────────

ĐÁNH GIÁ PHÙ HỢP CỦA BẠN

82 / 100
Phù hợp cao

Kỹ năng         86
Học lực         74
Lĩnh vực        91
Ngữ nghĩa       Đang tính
AI đánh giá     Chưa có

Hệ thống có đủ dữ liệu để đưa ra điểm tổng.
Một số thành phần nâng cao sẽ được bổ sung khi chạy gợi ý.

────────────────────────────────────────────────────────

Vì sao phù hợp

✓ Có Java ở mức 4/5, cao hơn yêu cầu 3/5
✓ Điểm Cơ sở dữ liệu đáp ứng điều kiện
✓ Quan tâm mạnh đến lĩnh vực AI

────────────────────────────────────────────────────────

Kỹ năng yêu cầu

Java               Yêu cầu 3/5        Bạn 4/5        Đạt
Python             Yêu cầu 2/5        Bạn 1/5        Cần cải thiện

────────────────────────────────────────────────────────

Mô tả đề tài
...
Sidebar desktop
Plain text
THÔNG TIN

Giảng viên
Nguyễn Minh Bình

Số lượng
5 sinh viên

Đã chọn NV1
21 sinh viên

Điểm GPA tối thiểu
2.5

[Đặt làm NV1]

Sidebar sticky:

CSS
.topic-sidebar {
  position: sticky;
  top: calc(var(--nav-h) + 24px);
}
Khi chưa có M4/M5

Không:

Plain text
— / 100

Dùng:

Plain text
Ngữ nghĩa
Đang tính

hoặc:

Plain text
Chưa chấm

với neutral status.

Mobile

Thứ tự:

title;
status;
CTA;
điểm tổng;
“Vì sao phù hợp”;
yêu cầu;
mô tả;
metadata.

Không đưa sidebar xuống cuối một cách máy móc.

CTA có thể sticky bottom.

20. Trang Khoa — chi tiết điểm AI

Ở các màn hình GV/Khoa, điểm AI không được hiển thị kiểu:

Plain text
67.0

Mà:

Plain text
67
Khá phù hợp

Hoặc cell:

Plain text
67 / 100

Có tooltip:

Plain text
Điểm tổng từ M1–M5 theo trọng số của phiên bản mô hình hiện tại.

Không dùng progress bar cho từng số chỉ vì có số phần trăm.

21. Recommended Topic Card

Trang sinh viên hiện tại nhồi 5 progress bar/card.

DESIGN-v2:

Plain text
#01
Phần mềm quản lý bãi đỗ xe doanh nghiệp          80

Nguyễn Minh Bình · Hệ thống thông tin

Phù hợp cao
Java 4/5 · CSDL 4/5 · AI vừa

VÌ SAO PHÙ HỢP
• Kỹ năng backend đáp ứng đầy đủ yêu cầu.
• Điểm học phần CSDL tốt.
• Phù hợp định hướng Backend Developer.

[Xem đề tài]                         [Chọn NV1]

Không hiển thị M1–M5 ở card browse.

M1–M5 chỉ xuất hiện trong màn hình explanation/detail.

22. Toolbar / filter

Filter list đề tài hiện quá nặng.

Desktop:

Plain text
[Tìm theo tên đề tài............................]

Lĩnh vực ▾     Độ khó ▾     Giảng viên ▾     Điều kiện ▾

50 đề tài                                      Xóa bộ lọc

Không cần card bao quanh.

CSS
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  padding-block: 16px;
  border-block: 1px solid var(--border-soft);
}

Mobile:

Plain text
[Tìm kiếm...]

[Bộ lọc 2]

Bấm → Bootstrap Offcanvas bottom/full-height.

Không hiển thị 4 select liên tục trên đầu màn hình.

23. Pagination

Bỏ style Bootstrap mặc định.

Plain text
1–10 / 50 đề tài

← Trước          1  2  3  4  5          Sau →

Mobile:

Plain text
1–10 / 50

[← Trước]       [Sau →]

Không cần 5 số trang trên điện thoại.

24. App shell

Desktop max-width:

CSS
.app-container {
  width: min(calc(100% - 48px), var(--content-max));
  margin-inline: auto;
}

.page-header {
  padding: 36px 0 24px;
}

.page-eyebrow {
  margin-bottom: 6px;
  color: var(--text-muted);
  font-size: var(--fs-12);
  font-weight: 600;
}

.page-title {
  margin: 0;
  font-size: clamp(1.75rem, 3vw, 2.5rem);
}

.page-subtitle {
  max-width: 720px;
  margin-top: 8px;
  color: var(--text-muted);
}

Mobile:

CSS
@media (max-width: 575.98px) {
  .app-container {
    width: auto;
    margin-inline: 16px;
  }

  .page-header {
    padding: 24px 0 18px;
  }
}
25. Surface system

Chỉ 3 kiểu.

CSS
.surface {
  background: var(--surface-1);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
}

.surface-soft {
  background: var(--surface-2);
  border-radius: var(--radius-lg);
}

.surface-dark {
  background: var(--brand-950);
  color: var(--text-on-dark);
  border-radius: var(--radius-xl);
}

Không tạo thêm 10 biến thể .card-primary, .card-info, .card-warning...

26. Section heading
CSS
.section-heading {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 18px;
}

.section-heading__eyebrow {
  margin-bottom: 4px;
  color: var(--text-muted);
  font-size: var(--fs-11);
  font-weight: 700;
  letter-spacing: .08em;
  text-transform: uppercase;
}

.section-heading h2 {
  margin: 0;
}

Dùng numbering khi có ích:

Plain text
01 / Giới thiệu
02 / Kỹ năng
03 / Lĩnh vực quan tâm

Đây là một phần tạo chất editorial/học thuật riêng cho hệ thống.

27. Responsive chuẩn

Không chỉ có desktop → mobile.

CSS
/* Mobile first */

@media (min-width: 576px) {
  /* small tablet */
}

@media (min-width: 768px) {
  /* tablet / table appears */
}

@media (min-width: 992px) {
  /* desktop two-column */
}

@media (min-width: 1200px) {
  /* full dashboard */
}
390px là viewport QA bắt buộc

Kiểm tra:

không horizontal scroll;
touch target ≥44px;
title không vỡ khó đọc;
không có nút action sát nhau;
không bảng desktop;
không card hơn ~300px nếu chỉ chứa metadata;
CTA quan trọng nhìn thấy trong khoảng 1–1.5 viewport đầu.
28. Phân cấp chữ
Vai trò	Size
Page title	28–40px
KPI number	32–48px
Section H2	24px
Card/list title	16–18px
Body	14px
Metadata	12–13px
Table header	11px

Không dùng chữ 10px cho thông tin người dùng cần đọc.

29. Icons

Một bộ icon duy nhất.

Nếu dự án đang có Bootstrap Icons thì giữ Bootstrap Icons, nhưng:

stroke/visual weight đồng nhất;
icon decorative aria-hidden="true";
icon không thay thế text ở action quan trọng;
không dùng icon màu xanh ngẫu nhiên từng hàng.

Icon default:

CSS
.ui-icon {
  color: var(--text-muted);
}

Brand icon chỉ dùng trong điểm nhấn AI.

30. AI visual language

Bản cũ muốn thể hiện AI bằng:

vòng tròn;
progress;
màu xanh;
hàng loạt số.

Sai.

DESIGN-v2 thể hiện AI bằng explainability.

Ba component đặc trưng:

1. Match Score
Plain text
82
Phù hợp cao
2. Reason List
Plain text
Vì sao phù hợp
✓ Kỹ năng Java vượt yêu cầu
✓ GPA đáp ứng
✓ Quan tâm đúng lĩnh vực
3. Evidence breakdown
Plain text
Kỹ năng       86
Học lực       74
Lĩnh vực      91
Ngữ nghĩa     79
AI đánh giá   82

Như vậy hệ thống nhìn thông minh thật, không cần graphic AI giả.

31. Accessibility

Bắt buộc:

CSS
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    scroll-behavior: auto !important;
    transition-duration: .01ms !important;
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
  }
}

Ngoài ra:

màu không bao giờ là dấu hiệu duy nhất;
mọi status có text;
label thật cho form;
error có aria-describedby;
modal focus trap của Bootstrap;
offcanvas có title;
<th scope="col">;
<caption> cho bảng quan trọng;
chart phải có summary text hoặc bảng dữ liệu tương đương.
32. Bố cục 5 trang cần cứu đầu tiên
A. /khoa/phan-cong/
Desktop
Plain text
Page header + 2 actions
KPI strip
Allocation progress
Filter/status tabs
Toolbar
Dense data table
Right offcanvas detail
Mobile
Plain text
Header
2x2 KPI
Tabs ngang scroll
Search
Record list
Bottom-sheet/offcanvas detail

Bỏ tuyệt đối: row vàng, table responsive kéo ngang, nút trên từng cell.

B. /khoa/thong-ke/
Desktop
Plain text
Header
KPI strip
Registration completion
2-column:
  Left 8/12: lĩnh vực
  Right 4/12: quality summary
Top topic ranking full width
Allocation quality
Mobile
Plain text
Header
2x2 KPI
Registration
Top lĩnh vực 5
Top đề tài 5
Allocation summary

Ẩn dữ liệu phụ dưới “Xem thêm”.

C. /ho-so/
Desktop
Plain text
Header + saved state
Compact completion summary
01 Giới thiệu
02 Kỹ năng
03 Lĩnh vực
Footer save action
Mobile
Plain text
Header
Completion
Section anchors
Compact skill list
Compact interest list
Sticky save bar

Không table formset.

D. /de-tai/<id>/
Desktop
Plain text
Breadcrumb
Title / status
Main 8 columns + sidebar 4 columns
Match score
Reason list
Requirements
Description
Sidebar sticky metadata / CTA
Mobile
Plain text
Title
Status
CTA
Match score
Reasons
Requirements
Description
Metadata
Sticky CTA

Không 5 circles.

E. /dang-nhap/
Desktop
Plain text
56% dark brand/data storytelling
44% clean login form
Mobile
Plain text
Dark identity header
White form below
Demo role switcher

Không card floating.

33. Thứ tự làm lại 16 trang

Không redesign từng trang độc lập. Làm theo dependency.

Phase 0 — Foundation

Làm trước mọi page:

design-v2.css
app shell/navbar
typography
buttons
statuses
surfaces
form controls
data table
mobile records
Chart.js theme
empty state
Phase 1 — 5 màn hình phá hình ảnh sản phẩm nhất
14-khoa-phan-cong /khoa/phan-cong/
15-khoa-thong-ke /khoa/thong-ke/
02-sv-ho-so /ho-so/
05-sv-chi-tiet-de-tai /de-tai/<id>/
00-dang-nhap /dang-nhap/

Đây là 5 màn hình phải dùng để xác nhận DESIGN-v2 trước khi triển khai toàn hệ thống.

Phase 2 — Core Student Journey
01-sv-trang-chu
04-sv-danh-sach-de-tai
03-sv-nguyen-vong
06-sv-ket-qua
07-sv-doi-mat-khau
Phase 3 — Lecturer
08-gv-trang-chu
09-gv-de-tai
10-gv-de-tai-sua
11-gv-de-tai-dang-ky
12-gv-ho-so
Phase 4 — Khoa Dashboard
13-khoa-trang-chu

Trang dashboard Khoa làm sau khi pattern KPI/data/table/chart của hai trang Khoa lớn đã ổn định, để nó dùng đúng component đã chuẩn hóa thay vì thiết kế lần thứ ba.

34. Quy tắc QA trước khi DESIGN-v2 được coi là đạt

Mỗi trang phải chụp:

desktop 1440×900;
mobile 390×844.

Và kiểm tra tối thiểu:

Tiêu chí	Điều kiện đạt
Horizontal scroll 390px	Không
Table desktop xuất hiện 390px	Không
Card lồng card	Không
Danger color dùng sai ngữ nghĩa	Không
Empty — lặp lại	Không
Primary CTA	≤1 nhóm chính/màn hình
Touch target	≥44px
KPI đọc trong 2 giây	Có
Nội dung sống còn nằm sau >3.000px scroll	Không
Bootstrap blue mặc định	Không
Màu chart đỏ không có nghĩa	Không
Focus-visible	Có
Text/background chính	WCAG AA
35. Một số class nên cấm trong template mới

Dev không được dùng trực tiếp các class này để quyết định visual semantics:

Plain text
bg-primary
bg-danger
bg-warning
text-primary
text-danger
alert-warning
alert-danger
btn-primary
btn-danger
badge
card
shadow

Bootstrap vẫn được dùng cho:

Plain text
container
row
col-*
d-flex
gap-*
offcanvas
modal
collapse
dropdown
utilities responsive

Nhưng visual language phải đi qua class DESIGN-v2:

Plain text
btn-v2-primary
status-warning
surface
data-shell
record-item
kpi
section-heading

Như vậy Bootstrap chỉ là layout/runtime framework, không còn là art direction.

36. Kết luận thiết kế

Bản hiện tại không xấu chủ yếu vì “màu chưa đẹp”; nó xấu vì mọi dữ liệu đều được biến thành hộp, mọi trạng thái đều biến thành badge, mọi con số đều biến thành progress bar và desktop component bị ép nguyên xuống mobile.

DESIGN-v2 đảo ngược cách làm đó:

Typography tạo hierarchy. Whitespace tạo nhóm. Divider tạo cấu trúc. Màu chỉ mang nghĩa. Card chỉ xuất hiện khi thật sự là một object độc lập.

Nếu triển khai đúng bộ này, Capstone Advisor AI sẽ chuyển từ cảm giác “bài tập Django + Bootstrap” sang “hệ thống phân tích và ra quyết định học thuật” mà không cần React, không cần framework UI mới và vẫn chỉ cần Bootstrap 5 + một design-v2.css.