=== PHẦN 8: NGUYÊN LIỆU ÁP DỤNG ===

Các nguyên liệu dưới đây chỉ nâng chất interaction, state, motion, data-viz, accessibility và dark mode. Không thay cấu trúc sidebar/topbar, logo 5 ô, Sora + Noto Sans hay bảng màu Mosaic đã duyệt. Vì dự án dùng Django + Bootstrap 5.3 + CSS/JS thuần, các kỹ thuật phụ thuộc React/Framer/Motion được chuyển thành CSS/WAAPI/vanilla JS tương đương.

Mã thẻ	Áp vào Mosaic AI	Điều chỉnh để hợp hệ Mosaic
component|shared-layout-tab-indicator	Tab Thống kê; tab Import Excel; filter trạng thái; switch nhóm dữ liệu	Không dùng Framer layoutId. Dùng indicator CSS màu --accent, cao 2px, transition 160ms var(--ease-standard). Tab active không đổi thành pill xanh Bootstrap. Không dùng cho navigation sidebar/bottom-nav.
component|tactile-bicolor-toggle-switch	Theme Light/Dark/System; các toggle “Bắt buộc”, “chỉ SV chưa xếp”	Track 44×24px, thumb 18px; active dùng --accent, inactive --border-strong; 140ms. Có aria-checked, focus ring. Không dùng để thay checkbox xác nhận hành động nguy hiểm.
motion|svg-path-drawing-toggle	Check hoàn tất hồ sơ, constraint hợp lệ, import Excel đạt, bước workflow hoàn tất	Lucide check path vẽ trong 180–220ms, stroke teal/success token. Chỉ chạy khi trạng thái thực sự đổi. Không chạy lại khi scroll/render bảng.
motion|crossfade-slide-transition	Wizard Hồ sơ → Gợi ý → Nguyện vọng → Kết quả; mobile filter panels; modal step 1 → step 2	opacity + translateY(6px), 180–220ms, không slide cả màn hình. Preserve focus và scroll. Không dùng khi đổi row/filter tức thời trong bảng.
component|responsive-omnichart-dataviz-system	Khoa Thống kê; Phân công; GV workload; ILP vs Greedy	Giữ Chart.js hiện tại, lấy nguyên lý responsive scale/tooltip/legend. 6 chart token Mosaic; cùng semantic color ở sáng/tối. Chart tự chuyển legend/axis theo breakpoint. Không thêm D3 chỉ để có hiệu ứng.
motion|perceptual-spring-css-linear-easing	Toggle, dropdown, toast, tooltip, button press	Không dùng Motion library. Chuẩn hóa thành CSS linear() spring nhẹ hoặc fallback cubic-bezier(.2,.8,.2,1). 120–180ms, không bounce rõ. Không dùng cho bảng/chart lớn.
motion|cubic-drawer-slide-transition	Inspector SV bên phải của GV; mobile offcanvas filter; mobile navigation drawer	Desktop inspector 360–400px, mobile min(92vw, 420px). 220ms cubic-bezier(.2,.8,.2,1). Có backdrop nhẹ, ESC close, focus trap. Không dùng cho dialog xác nhận ngắn.
motion|waapi-programmatic-reveal-hook	Empty state SVG; panel kết quả AI vừa tính xong; kết quả ILP mới trả về	Native WAAPI, opacity 0→1, translateY(8px→0), 220–280ms. Chỉ reveal một lần khi dữ liệu mới xuất hiện. Không scroll-animation liên tục.
color|chartreuse-text-safe-mix-system	Kiểm tra contrast của accent text/badge trên Light/Dark	Không lấy chartreuse. Chỉ áp dụng kỹ thuật sinh accessible foreground bằng color-mix() từ token Mosaic; fallback token cố định. Mục tiêu WCAG AA. Không thay màu thương hiệu gốc.
layout|fused-metric-ribbon-dock	Dải số liệu Khoa Phân công/Thống kê/Trang chủ; dải GV	Giữ đúng metric ribbon đã duyệt: một surface, separator dọc, không card con/icon bubble. Desktop 78–88px; mobile wrap/scroll. Không dùng trên Trang chủ SV vì đã chốt chỉ dữ liệu cá nhân.
component|flat-clean-accordion-list	Mobile advanced filters; giải thích M1–M5 chi tiết; điều kiện đề tài dài; lỗi import theo dòng	Không box lồng box. Chỉ separator --border-soft, chevron Lucide, 180ms expand. Không collapse nội dung cốt lõi như tổng điểm, eligibility hay CTA.
component|sticky-typewriter-filter-bar	Danh sách đề tài SV; danh sách SV Khoa/GV; bảng phân công dài	Bỏ “typewriter”. Chỉ lấy sticky filter bar: nền surface 96–98% opacity, top: 64px, border-bottom. Mobile sticky dưới topbar. Không sticky khi danh sách dưới ~8 item.
layout|floating-anchor-popover	Menu ..., tooltip M1–M5, chọn thao tác row, dropdown trong bảng có overflow	Vanilla JS getBoundingClientRect(), flip trên/dưới/trái/phải, viewport padding 8px. Shadow --shadow-sm, radius 8. Không dùng cho form dài hoặc confirmation critical.
interaction|inline-sentence-comparison-toggle	Khoa Thống kê: ILP ↔ Greedy, đặc biệt tablet/mobile	Desktop vẫn giữ bảng so sánh song song. Mobile có toggle ILP / Greedy để tiết kiệm ngang; active teal. Không dùng nếu cần nhìn hai thuật toán đồng thời để ra quyết định.
Cập nhật 3 quyết định nghiệp vụ bắt buộc vào component

1. GV từ chối SV bắt buộc nhập lý do

Ở màn GV — Sinh viên đăng ký:

Nút Từ chối không cập nhật ngay.
Mở confirmation dialog:
Sinh viên.
Mã SV.
Đề tài.
Điểm phù hợp.
textarea **“Lý do từ chối *”**.
CTA Xác nhận từ chối disabled khi textarea rỗng.
Lỗi validation nằm ngay dưới textarea.
Esc/Hủy không thay đổi trạng thái.
Sau thành công: row → Từ chối, toast xác nhận, lý do có thể xem lại trong inspector/audit.

Không sử dụng danger cho toàn modal; chỉ CTA destructive dùng --danger.

2. Trọng số kỹ năng không bắt buộc tổng bằng 100%

Form GV — Thêm/sửa đề tài đổi logic trình bày:

Plain text
Kỹ năng           Mức       Trọng số      Bắt buộc
Java              4/5          20%            ON
SQL               4/5          20%            ON
Phân tích dữ liệu 3/5          15%            OFF

Helper text:

“Trọng số thể hiện mức độ quan trọng tương đối của từng kỹ năng. Không yêu cầu tổng bằng 100%.”

Bỏ hoàn toàn:

progress “Tổng trọng số”.
validation ≠ 100%.
cảnh báo đỏ khi tổng không đủ 100.

Bắt buộc vẫn kèm chú thích “Là điều kiện loại” và giữ semantic hard-filter riêng với weight.

3. SV được sửa NV đến khi đợt đóng; NV đã được GV duyệt giữ trạng thái

Màn SV — Nguyện vọng:

Khi đợt OPEN:

đổi NV1/NV2/NV3;
đổi thứ tự;
thêm/xóa theo rule backend;
Lưu nguyện vọng.

Preference đã GV duyệt hiển thị:

Đã GV duyệt

và khi đổi thứ hạng:

NV2 → NV1

thì trạng thái duyệt không reset.

Khi đợt CLOSED:

toàn bộ controls sắp xếp/thêm/xóa disabled;
màn chuyển read-only;
banner: Đợt đăng ký đã đóng — nguyện vọng không thể chỉnh sửa.

Không dùng màu warning cho NV đã duyệt; dùng --success.

THẺ BỊ LOẠI
interaction|form-wrapped-slider — Form Mosaic là form nghiệp vụ dài/dynamic row, không phải onboarding slider.
component|interactive-credit-card-form — Không có thanh toán/thẻ tín dụng.
color|white-ink-shell-hsl-mats — Thay đổi hệ màu đã duyệt.
component|near-black-map-stat-band — Thiên về brand/marketing section, không phù hợp dashboard.
color|teal-on-wordmark-and-buttons — Mosaic đã có teal token riêng; không cần thay hệ brand.
interaction|circular-toggle-minimal-faq-accordion — Trùng chức năng với flat-clean-accordion-list, phiên bản tròn dễ tăng tính “template”.
color|cyber-deep-teal-and-slate-palette — Làm sản phẩm cyber/fintech, lệch tone học thuật.
component|floating-card-menu-panel — Phá kiến trúc sidebar/topbar đã duyệt.
motion|css-variable-scroll-progress — Không có scrollytelling dài cần progress theo scroll.
interaction|focus-trap-motion-pause — Không có carousel/ticker autoplay cần pause khi focus.
color|safety-orange-signal-accent — Cam chỉ là semantic secondary của Mosaic, không được chiếm vai trò CTA chính.
interaction|morphing-page-refresh — Phụ thuộc Turbo và không cần thiết với Django hiện tại.
layout|high-contrast-bipolar-theming — Phá hệ Light/Dark token Mosaic.
layout|undistorted-border-radius-layout-projection — Không cần shared-card expansion và Motion library.
typography|manrope-display-tracking-scale — Font đã khóa Sora + Noto Sans.
color|black-pink-white-phase-system — Sai hoàn toàn palette.
component|pow-checkbox-widget — Không có yêu cầu CAPTCHA/anti-bot.
component|circular-metric-process-cluster — Trái quyết định bỏ KPI card/circle kiểu SaaS.
color|deep-forest-contrast-palette — Thay palette đã khóa.
motion|scroll-built-card-cascade — Hiệu ứng landing/roadmap, gây cản trở thao tác.
motion|css-draw-fade-quartet — Bộ animation rộng hơn mức cần thiết; WAAPI reveal đã đủ.
layout|fullscreen-single-scene-stage — Dành cho landing/portfolio, không phù hợp app.
component|corner-sticker-product-cell — Ecommerce/marketing.
color|stark-monochrome-with-subtle-warmth — Xóa đặc trưng Mosaic.
component|accessible-audio-visual-code-challenge — Không có CAPTCHA challenge.
component|turbo-frame-scoped-lazy-loader — Phụ thuộc Turbo; Django page architecture hiện tại không cần.
component|index-pill-square-card — Không cần thêm một card language khác.
typography|dual-contrast-font-pairing — Thay typography đã duyệt và dùng font không thuộc stack hiện tại.
component|split-column-faq-matrix — Marketing FAQ, không phải nghiệp vụ.
typography|grotesque-display-typewriter-roles — Thay hệ font và làm dashboard quá editorial.
motion|electric-spark-lightning-flash — Quá trình diễn, phá cảm giác bình tĩnh/chính xác.
color|emerald-lime-contrast-system — Lime không thuộc palette Mosaic.
component|sticker-split-footer — Không cần footer marketing.
component|visionos-spatial-glass-card — Glass/blur phá bề mặt phẳng và accessibility.
typography|geometric-display-tight-tracking — Font/scale headline quá lớn cho application UI.
color|monochrome-chrome-photo-hue — Hệ photo/monochrome không liên quan.
motion|lottie-offscreen-worker-renderer — Không có animation Lottie phức tạp; tăng chi phí runtime.
component|fixed-acid-info-strip — Acid bar quá xâm lấn và không thuộc palette.
motion|waapi-compositor-ticker — Không có ticker.
interaction|pointer-trail-emitter — Decoration kiểu creative-tech, gây nhiễu và hại accessibility.
motion|root-transform-page-transition — Transition 650ms toàn trang quá nặng cho phần mềm thao tác thường xuyên.
motion|pinned-scrubbed-story-timeline — Scrollytelling marketing.
motion|segmented-white-panel-wipe — Transition chiến dịch/landing.
motion|progressive-copy-reveal-by-occlusion — Headline reveal không phục vụ nghiệp vụ.
interaction|draggable-inertia-snap — NV cần thao tác deterministic, keyboard/mobile accessible; giữ nút lên/xuống.
component|dual-layer-rolling-text-button — Nút nghiệp vụ phải ổn định, không rolling text.
motion|compositor-thread-scroll-reveal — Trùng WAAPI reveal; không duy trì hai cơ chế reveal.
color|high-contrast-neon-mint-accent-system — Neon/cyber trái direction.
motion|alternating-corner-scale-reveal — Experimental typography, không phù hợp.
motion|dom-interactive-box-choreography — Theatre.js quá mức cần thiết.
motion|float-bobbing-illustration-keyframes — Empty state không nên bob vô hạn.
component|micro-stacked-risk-histogram — Histogram hiện tại của phân bố điểm rõ hơn; không cần 30 cột siêu nhỏ.
component|badge-pill-scale-pop — Hệ thống đã chủ động giảm lạm dụng badge/pill.
interaction|prefers-reduced-motion-video-controller — Mosaic không có autoplay video; prefers-reduced-motion đã xử lý trực tiếp ở design system.
Tóm tắt tác động
Mosaic AI không đổi hình dáng, nhưng thao tác giờ có phản hồi rõ hơn: tab, drawer, state change, modal và AI result đều có motion ngắn, thống nhất và có reduced-motion.
Dashboard trở nên giống sản phẩm dữ liệu trưởng thành hơn: metric ribbon nhất quán, chart responsive, sticky filter, popover không bị cắt và ILP/Greedy đọc tốt cả desktop lẫn mobile.
Light/Dark và accessibility được nâng thành hành vi hệ thống, không chỉ đổi màu: contrast token an toàn, focus/keyboard rõ ràng, trạng thái loading/empty/error/destructive đều có quy tắc cụ thể.