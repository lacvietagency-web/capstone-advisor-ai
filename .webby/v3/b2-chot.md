PHÁN QUYẾT DESIGN AUTHORITY — ATLAS V3.4

Trạng thái: CHỐT TRIỂN KHAI
Hiệu lực: Ghi đè các thông số ATLAS V3.3 có xung đột.

Nguyên tắc: ưu tiên giao diện dễ hiểu, vận hành đúng hệ thống hiện có, không phát triển tính năng backend chỉ để phục vụ trang trí. Giữ nguyên nhận diện ATLAS, màu sắc, typography, logo Open Path và ngôn ngữ chuyển động Quiet Precision.

I. PHÁN QUYẾT GEMINI
G1 — Thiếu dữ liệu và cấu trúc backend

G1.1 — Bộ lọc phân công: CHẤP NHẬN — Giữ status, rank, q, sort hiện có; bổ sung lọc lecturer_id, field_id, score_min, score_max bằng truy vấn backend. Tất cả bộ lọc phải kết hợp được, phân trang 20 dòng/trang và giữ query khi chuyển trang.

G1.2 — Chi tiết sinh viên chưa xếp: CHẤP NHẬN — Drawer phải hiển thị NV1–NV3 gốc, điểm từng nguyện vọng, trạng thái điều kiện và đề tài có thể xếp tay. unassigned_reason được tính từ dữ liệu phân công/điều kiện thực; không tạo một lý do chung kiểu “Chưa đủ điểm” khi chưa xác định được nguyên nhân.

G1.3 — Điều kiện đề tài: CHẤP NHẬN — Chuẩn hóa _ineligible_reason thành eligibility.reasons[] gồm rule_type, required_value, actual_value, is_mandatory. Thông tin trả về phải phản ánh đúng từng điều kiện; không tách chuỗi văn bản bằng quy tắc đoán.

G1.4 — Siêu dữ liệu điểm AI: CHẤP NHẬN MỘT PHẦN — score_status được suy ra từ các thành phần đã có; M5 null hiển thị “Điểm sơ bộ M1–M4”. Dùng weights_version, model_version nếu có. Không bổ sung trường lưu nguồn fallback trong Sprint này; không gắn nhãn “LLM đánh giá” khi không xác minh được nguồn.

G1.5 — Người chưa đăng nhập: CHẤP NHẬN — Danh sách đề tài công khai (nếu được phép) không hiển thị điểm phù hợp cá nhân. Hiện “Đăng nhập để xem mức phù hợp”, tuyệt đối không sử dụng điểm AI mẫu của một sinh viên khác.

G1.6 — Kết quả phân công: CHẤP NHẬN MỘT PHẦN — Chỉ hiển thị nguồn ILP/Greedy/Manual nếu dữ liệu source tồn tại; không suy luận từ thứ tự nguyện vọng. Lý do chưa xếp chính thức chỉ xuất hiện nếu được backend cung cấp và được phép công khai.

G1.7 — Drawer duyệt SV của GV: CHẤP NHẬN — Bổ sung context chi tiết student, preference, recommendation, eligibility; hiển thị phiên bản đánh giá nếu đã lưu. Không tự tạo lịch sử đánh giá khi CSDL không lưu snapshot.

G1.8 — Chuông thông báo: CHẤP NHẬN — Xóa hoàn toàn khỏi base.html, desktop và mobile. Không để nút ẩn có thể focus hoặc một badge giả.

G2 — Trả lời 5 câu hỏi kỹ thuật

G2.Q1 — Drawer Phân công: CHẤP NHẬN — Dùng Bootstrap Offcanvas bên phải, rộng 440px, max-width:100vw; dưới 768px chuyển thành offcanvas toàn màn hình. Dữ liệu chi tiết lấy qua GET bất đồng bộ khi bấm “Xem chi tiết”, trả HTML fragment Django; không nhúng HTML của 100 sinh viên vào bảng. Click toàn dòng không mở drawer.

G2.Q2 — Context Index: BÁC — Loại bỏ Context Index 224px hoàn toàn. Không có trạng thái thu gọn, không dùng localStorage cho Context Index và không cần nút mở lại.

G2.Q3 — Metric Ledger: CHẤP NHẬN — Tất cả chỉ số lấy động từ CSDL của đợt đang chọn. Các số 100 SV, 15 GV, 50 đề tài, 43% đã xếp, 30% NV1, 43% Top 3, 63,8 điểm, 57 chờ pha 2 là dữ liệu đợt thử nghiệm đã cung cấp, không hardcode. Đợt khác hiển thị số liệu riêng; không có dữ liệu thì hiển thị 0 hoặc “Chưa có dữ liệu” đúng ngữ nghĩa.

G2.Q4 — Bottom Action Bar: CHẤP NHẬN — Trên màn hình có hành động chính cố định, ẩn Bottom Navigation. Action Bar cao tối thiểu 72px + safe area, neo đáy; Main có padding-bottom 96px + safe area. Các trang không có Action Bar giữ Bottom Navigation 64px + safe area.

G2.Q5 — Theme: CHẤP NHẬN — Khóa localStorage là atlas-theme, giá trị hợp lệ light, dark, system; mặc định system. Khi hệ điều hành đổi theme, chỉ cập nhật data-bs-theme tự động nếu người dùng chọn system. Áp dụng theme trước khi hiển thị giao diện để tránh nháy sáng/tối. Không giữ song song mosaic-theme.

G3 — CSS và Bootstrap

G3.1 — Ánh xạ Bootstrap: CHẤP NHẬN CÓ SỬA — Dùng đúng các biến Bootstrap đã đề xuất, nhưng --bs-primary-rgb phải đổi theo theme: Light 48,95,82, Dark 139,184,164. Đồng bộ cả --bs-btn-*, --bs-pagination-*, --bs-form-*, --bs-table-* theo ATLAS; chỉ đổi --bs-primary không đủ để loại màu Bootstrap.

G3.2 — Một file CSS: CHẤP NHẬN — Chỉ một CSS ứng dụng static/css/atlas.css, gồm đúng 7 nhóm: Fonts, Tokens, Bootstrap Reset, Shell, Base Components, Domain Components, Motion & Accessibility. Bootstrap CSS đóng gói local không tính là CSS ứng dụng. Xóa tham chiếu ba CSS cũ khỏi template.

G3.3 — Font local: CHẤP NHẬN — Be Vietnam Pro, các weight 400/500/600/700, subset Vietnamese + Latin, dùng WOFF2 local, font-display:swap. Không gọi CDN.

G4 — Mobile 390px

G4.1 — Bảng desktop/mobile: CHẤP NHẬN CÓ SỬA — Chuyển bảng thành danh sách card dưới 768px; dùng d-none d-md-table cho bảng và d-md-none cho danh sách, không dùng d-md-block trực tiếp trên thẻ table. Phân trang dùng chung backend, tránh hai tập kết quả khác nhau.

G4.2 — Drawer mobile: CHẤP NHẬN MỘT PHẦN — Các drawer có form, duyệt SV, xếp tay hoặc Evidence Strip M1–M5 phải mở toàn màn hình 100dvh, không dùng sheet cao 85vh. Sheet 85dvh chỉ dành cho bộ lọc/tuỳ chọn ngắn.

G4.3 — Khoảng đệm đáy: BÁC phương án cố định 144px cho mọi trang — Trang có Bottom Nav dùng padding-bottom calc(96px + env(safe-area-inset-bottom)); trang có Action Bar dùng cùng khoảng đệm 96px nhưng ẩn Bottom Nav. Không bao giờ xếp cả hai thanh để chiếm 144px.

G4.4 — Form dài và bàn phím: CHẤP NHẬN — Form mobile một cột, gap field 20px, touch target tối thiểu 44px. Khi bàn phím ảo mở, Action Bar không được che trường đang nhập: ưu tiên đưa nút vào cuối luồng cuộn nếu việc neo cố định không tương thích với visual viewport.

G5 — Phân công triển khai

G5.1 — Chia ba nhóm: CHẤP NHẬN — Nhóm 1 Shell/SV, nhóm 2 Đề tài/GV, nhóm 3 Khoa/Thống kê; phân chia theo file đã đề xuất.

G5.2 — Sprint 0: CHẤP NHẬN — Nhóm 1 bàn giao base.html, token atlas.css, các component mẫu và quy ước class trước khi nhóm 2/3 chỉnh template nghiệp vụ.

G5.3 — Zero-conflict: CHẤP NHẬN CÓ ĐIỀU KIỆN — Chỉ một nhóm được quyền sửa base.html, atlas.css và components dùng chung; hai nhóm còn lại đề xuất thay đổi qua nhóm sở hữu. Không ghi đè CSS bằng style inline hoặc file CSS riêng.

II. PHÁN QUYẾT GROK

X1 — Báo cáo phản biện: CHẤP NHẬN việc Grok chỉ đọc và đối chiếu mã nguồn, nhưng chưa có ý kiến X1/X2 cụ thể để phán quyết. Không suy diễn thêm bất kỳ yêu cầu nào từ phần báo cáo chưa được cung cấp.

III. PHÁN QUYẾT CLAUDE

C1 — Menu Giảng viên: CHẤP NHẬN — Rail GV chỉ còn 3 mục: Tổng quan (house), Đề tài của tôi (book-open), Hồ sơ giảng viên (user-round). Luồng duyệt SV truy cập từ Tổng quan (danh sách đề tài có số chờ duyệt) hoặc từng dòng “Đề tài của tôi”. Không tạo trang tổng đăng ký mới nếu backend không có route tương ứng.

C2 — Rail 68px hay 88px: CHẤP NHẬN đề xuất 88px có nhãn. Mỗi mục cao 60px, icon Lucide 20px, nhãn Be Vietnam Pro 12px/600, tối đa 2 dòng; active dùng nền riêng và vạch trái 3px. Tooltip chỉ bổ sung, không thay thế nhãn. Mobile dưới 768px vẫn dùng bottom navigation.

C3 — Context Index: CHẤP NHẬN — Loại bỏ hoàn toàn 224px Context Index. Desktop dùng toolbar ngay trên bảng gồm tìm kiếm, bộ lọc và chip trạng thái; dưới 768px chuyển bộ lọc vào bottom sheet, giới hạn 85dvh. Main Canvas tận dụng chiều rộng còn lại sau rail 88px.

C4 — Skeleton: CHẤP NHẬN — Không dùng skeleton trên các trang Django render hoàn toàn server-side. Chuyển trang hiển thị bình thường; các POST chạy lâu dùng nút “Đang xử lý…” khóa thao tác lặp. Riêng drawer tải qua GET bất đồng bộ được dùng một trạng thái tải nội bộ nhỏ, không skeleton toàn trang.

C5 — Xác nhận và lý do từ chối: CHẤP NHẬN CÓ ĐIỀU KIỆN — Modal công bố vẫn có hai bước. UI yêu cầu nhập chính xác CÔNG BỐ (so khớp sau trim, phân biệt dấu và chữ hoa); backend phải kiểm quyền, trạng thái đợt, phạm vi công bố và tính hợp lệ trước khi ghi. Lý do từ chối minlength=5, maxlength=500, đồng thời validate phía server từ 5–500 ký tự. Không được dựa duy nhất vào khóa nút ở frontend để bảo vệ thao tác.

C6 — Metadata M5: CHẤP NHẬN — Không thêm cột CSDL cho m5_source, published_at, recommendation_generated_at trong V3.4. M5 null → “Chưa đánh giá”; chưa đủ M5 → “Điểm sơ bộ M1–M4”; phiên bản trọng số/mô hình hiện khi đã lưu. Không ghi rằng điểm do LLM chấm nếu nguồn không được lưu/xác nhận.

C7 — SVG logo: CHẤP NHẬN — Giữ chính xác hình học Open Path đã khóa, viewBox 0 0 64 64, nét 4.5px, stroke-linecap=round, stroke-linejoin=round. Dùng lại ba tệp capstone-symbol-light.svg, capstone-symbol-dark.svg, favicon.svg đã gửi ở dạng văn bản thay [[/]]; không thiết kế logo mới. Khi lưu file phải chuyển [[ thành <escape><</escape> và ]] thành > để SVG hợp lệ.

C8 — Màu minh họa trạng thái rỗng: BÁC bộ ba màu đề xuất vì chưa bảo đảm đủ tương phản trên cả hai theme — Chốt SVG sử dụng currentColor ở đường nét chính và hai biến CSS riêng. Light: nét chính #305F52, nhấn #386D80, phụ #69736C; Dark: nét chính #8BB8A4, nhấn #8DBFD0, phụ #A8B4AB. Nếu nhúng bằng <img>, dùng hai phiên bản SVG tĩnh Light/Dark hoặc CSS filter chỉ khi kiểm tra màu đầu ra, không dùng một bộ màu cố định cho cả hai theme.

C9 — Chuông và theme: CHẤP NHẬN — Xóa chuông hoàn toàn; chuyển Sáng/Tối/Theo thiết bị vào menu tài khoản, dùng khóa atlas-theme và cơ chế ở G2.Q5.

=== SỬA ĐỔI THÔNG SỐ ===

Các thay đổi sau có hiệu lực ngay, ghi đè ATLAS V3.3. Thông số cũ không được áp dụng nếu trái với bảng này.

Mục

	

V3.3

	

V3.4 — Đã khóa




Navigation Rail desktop

	

68px, icon-only

	

88px, icon + nhãn 12px/600; item cao 60px




Context Index

	

224px tùy trang

	

Bỏ hoàn toàn




Main Canvas

	

Sau Rail + Context Index

	

Sau Rail 88px; max-width 1480px




Bộ lọc desktop

	

Context Index hoặc toolbar

	

Toolbar ngang trên bảng/danh sách




Bộ lọc mobile

	

Offcanvas tùy nội dung

	

Bottom sheet tối đa 85dvh




Drawer desktop

	

420–480px

	

440px cố định, max-width 100vw




Drawer nghiệp vụ mobile

	

Sheet/full-screen tùy tình huống

	

Full-screen 100dvh




Nạp drawer

	

Chưa thống nhất

	

GET HTML fragment bất đồng bộ theo yêu cầu




Bottom Nav + Action Bar

	

Có thể đồng thời

	

Loại trừ nhau: Action Bar hiện thì Bottom Nav ẩn




Padding dưới mobile

	

Phụ thuộc cả hai thanh

	

96px + safe area, chỉ tính thanh đang hiện




Metric Ledger

	

Các số demo cố định trong ảnh

	

Tính động từ đợt được chọn, không hardcode




Menu GV

	

4 mục

	

3 mục, duyệt SV qua trang đề tài




Skeleton

	

Có ở vùng dữ liệu

	

Bỏ ở trang server-rendered, chỉ hiện tải cục bộ khi fetch drawer




Theme storage

	

Chưa có khóa

	

atlas-theme: light/dark/system




Thông báo

	

Có thể triển khai chuông

	

Không hiển thị chuông




M5 chưa có

	

Có thể dùng fallback

	

“Chưa đánh giá”, ghi điểm sơ bộ M1–M4 khi hợp lệ




Metadata M5

	

Yêu cầu thêm trường nguồn

	

Không thêm CSDL trong V3.4




Lý do từ chối

	

Theo backend

	

5–500 ký tự, validate cả client/server




Công bố

	

Modal hai bước

	

Hai bước + nhập CÔNG BỐ ở UI + kiểm quyền/trạng thái backend




Màu SVG rỗng

	

Có thể cố định một bộ

	

Hai bộ màu Light/Dark hoặc CSS currentColor




Bootstrap primary RGB

	

Giá trị Light

	

Light 48,95,82; Dark 139,184,164




File CSS

	

Một CSS mới

	

static/css/atlas.css, đúng 7 phần, không CSS ứng dụng thứ hai

Quy tắc bổ sung có hiệu lực:

Mọi số liệu trong ảnh tham chiếu chỉ được dùng để kiểm tra thiết kế, không được đưa vào template như dữ liệu thật.

Dữ liệu có thể thiếu thì giao diện phải biểu đạt trạng thái thiếu, không suy luận hoặc tự tạo kết quả AI.

Không thêm trang hay route không tồn tại chỉ để khớp menu.

Frontend không được tự thực hiện logic phân công hoặc quyết định điều kiện học thuật.

Mọi thao tác thay đổi dữ liệu phải được backend kiểm tra quyền, trạng thái và ràng buộc.

Mọi xung đột giữa ảnh mockup và thông số V3.4: V3.4 thắng.

=== TIÊU CHÍ NGHIỆM THU ===

21 màn hình đúng theme, font, logo, spacing; không còn CSS cũ, Bootstrap mặc định hoặc CDN thiết yếu.

Rail desktop rộng đúng 88px, có icon + nhãn; không còn Context Index 224px.

390px, 768px, 992px, 1440px: không tràn ngang viewport, không nút bị che, không chữ dính viền.

Mobile: Bottom Nav và Action Bar không đồng thời xuất hiện; padding đáy đúng 96px + safe area.

Bảng Khoa: phân trang server-side 20 dòng mặc định, tìm kiếm và bộ lọc giữ đúng kết quả khi đổi trang.

Drawer: rộng 440px desktop, toàn màn hình mobile; chỉ nạp dữ liệu một SV khi mở, không render sẵn 100 drawer.

Điểm AI: M1–M5, trạng thái sơ bộ/chưa đánh giá và điều kiện bắt buộc đúng backend; không có điểm hoặc lý do giả.

Luồng SV: OPEN/CLOSED/OPTIMIZED/PUBLISHED hiển thị nhất quán; CLOSED vẫn xem được nguyện vọng đã nộp.

Công bố/duyệt: xác nhận hai bước; từ chối 5–500 ký tự; mọi POST được kiểm quyền và trạng thái ở backend.

Theme: light/dark/system lưu bằng atlas-theme, theo OS đúng khi chọn system; không nháy sai theme lúc tải.

Accessibility: chữ đạt WCAG AA, keyboard focus rõ, drawer/modal quản lý focus, reduced-motion hoạt động.

QA bằng chứng: screenshot trước/sau tại 390px và 1440px, lint/test chạy đạt, không có lỗi JavaScript hoặc lỗi 500 trong các luồng chính.

PHÁN QUYẾT CUỐI: ATLAS V3.4 APPROVED FOR IMPLEMENTATION.

Claude giữ quyền quyết định cơ chế backend; Gemini triển khai giao diện; Grok kiểm tra độc lập theo 12 tiêu chí. Không tự mở lại các quyết định đã khóa khi chưa có bằng chứng lỗi kỹ thuật hoặc nghiệp vụ.