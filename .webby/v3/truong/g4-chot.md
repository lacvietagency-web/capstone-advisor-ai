PHÁN QUYẾT DESIGN AUTHORITY — ATLAS V3.5 FINAL

Trạng thái: CHỐT THIẾT KẾ — SẴN SÀNG TRIỂN KHAI

Sau khi đối chiếu ý kiến Gemini, Grok, số đo mã nguồn web trường và hình ảnh ATLAS V3.4, em quyết định:

Học bố cục và mật độ thông tin của web trường, nhưng không sao chép nhận diện của trường. ATLAS V3.5 sử dụng navy riêng, xanh dương cho hành động và xanh ngọc cho bằng chứng AI.

I. PHÁN QUYẾT GEMINI
G1 — Những điểm đối chiếu web trường

G1.1 — Màu Navy: CHẤP NHẬN — Mã trường được báo cáo là #223771; hủy đề xuất #1D3E86. ATLAS dùng Navy độc lập #142B4B, khoảng cách RGB Euclid so với #1D3978 là 48,1 và so với #223771 là 44,6.

G1.2 — Gradient nền: BÁC — Không sao chép gradient #F0F3FD → #B2C2F0 và bo góc 30px của web trường. Canvas ATLAS dùng màu phẳng #F2F5FB, bán kính panel 6px.

G1.3 — Menu active màu cam: BÁC — Không dùng #F8843D làm nền active. Menu dùng nền #294E79, vạch trái 3px #F5BA6E, chữ trắng. Màu cam chỉ đánh dấu vị trí, không thay màu hành động.

G1.4 — Khung layout: CHẤP NHẬN — Sidebar chạy suốt viewport, header chỉ nằm trên vùng nội dung. Sidebar rộng 216px, thu gọn 60px; header cao 56px. Logo Open Path nằm ở đầu sidebar, cao 56px.

G1.5 — Phông: CHẤP NHẬN — Giữ duy nhất Be Vietnam Pro với weight 400/500/600/700; không chuyển sang Roboto hoặc Inter.

G2 — Triển khai CSS, shell và template

G2.1 — Biến màu và khung: CHẤP NHẬN CÓ SỬA — Navy #142B4B, action #2454B8, AI #176B60, canvas #F2F5FB, sidebar 216px thay vì 220px.

G2.2 — Section panel: CHẤP NHẬN — Nền #FFFFFF, viền trang trí #DDE4EF, radius 6px, header cao 42px nền #F5F8FE. Input và nút phụ phải dùng viền mạnh #747F93 để đạt tương phản.

G2.3 — Bảng dữ liệu: CHẤP NHẬN — Hàng cao tối thiểu 44px, cell padding 10px 12px, chữ 13px, tiêu đề cột 12px/600; khi nội dung xuống dòng, hàng tự tăng chiều cao.

G2.4 — base.html: CHẤP NHẬN CÓ SỬA — Thay rail bằng sidebar 216px; header Navy chỉ nằm trong Main Canvas. Logo Open Path không đổi. Tablet dùng offcanvas, mobile dùng Bottom Navigation.

G2.5 — Ba màn hình trọng tâm: CHẤP NHẬN — Ưu tiên Trang chủ SV, Phân công Khoa, Thống kê Khoa. Top 5 dùng 1 Evidence Panel + 4 hàng gọn; phân công dùng Metric Ledger phẳng; thống kê dùng lưới biểu đồ 7:5 và 6:6.

G2.6 — Các màn hình còn lại: BÁC phương án chỉ đổi class bao ngoài — Những trang có bố cục kém phải sắp xếp lại theo đặc tả từng màn hình. Không coi thay CSS là redesign hoàn tất.

G3 — Mobile 390px

G3.1 — Bảng mobile: CHẤP NHẬN — Dưới 768px đổi bảng nghiệp vụ thành danh sách card dọc; không đặt min-width:1000px làm tràn viewport. Bảng xem trước Excel được phép cuộn ngang trong vùng riêng.

G3.2 — Bottom Navigation: CHẤP NHẬN CÓ SỬA — Tối đa 4 mục, touch target tối thiểu 44×44px, nhãn “Nguyện vọng” dùng “NV” chỉ khi có aria-label đầy đủ; ưu tiên “Nguyện vọng” nếu hiển thị vừa trong một dòng. Không có nhãn gãy đè icon.

G3.3 — Evidence Strip mobile: CHẤP NHẬN — M1–M5 xếp dọc 5 hàng; mỗi hàng có tên, điểm, thanh ngang 7px. Không ép 5 thanh nhỏ trên một hàng.

G3.4 — Safe Area: CHẤP NHẬN — Bottom Nav 64px + safe area; Bottom Action Bar 72px + safe area. Hai thanh không đồng thời xuất hiện.

G4 — Kế hoạch thi công

G4.1 — FE Lead: CHẤP NHẬN — Một người sở hữu atlas.css, token, Bootstrap overrides và section panel.

G4.2 — App Shell: CHẤP NHẬN — Một người sở hữu base.html, nav_links.html, sidebar, mobile navigation.

G4.3 — Sinh viên: CHẤP NHẬN — Tái cấu trúc Trang chủ, Nguyện vọng, Danh sách đề tài; đồng bộ các trang SV còn lại.

G4.4 — Khoa/GV: CHẤP NHẬN — Tái cấu trúc Phân công, Thống kê và GV Tổng quan; các trang GV khác cũng phải được rà soát.

G4.5 — QA: CHẤP NHẬN — Test 390px và 1440px cho Light/Dark, bổ sung kiểm tra breakpoint 768px, 992px, 1200px và WCAG AA.

II. PHÁN QUYẾT GROK
X1 — Nguy cơ mất bản sắc

X1.1: CHẤP NHẬN — Không sao chép nguyên khung và màu trường; ATLAS có Navy #142B4B, Open Path, AI teal #176B60 và sidebar riêng.

X1.2: CHẤP NHẬN — Hủy #1D3E86; header chính thức #142B4B, đáp ứng khoảng cách RGB tối thiểu 40 so với hai navy tham chiếu.

X1.3: CHẤP NHẬN — Tách --at-brand: #2454B8, --at-ai: #176B60, --at-info: #315D91; cả ba phải khác nhau ở Light/Dark.

X1.4: CHẤP NHẬN — Không tên/logo trường, không ảnh stock. Evidence Panel là điểm nhận diện chính của Capstone AI sau logo.

X2 — Tương phản WCAG

X2.1: CHẤP NHẬN — #DDE4EF chỉ dùng đường phân khu vực trang trí, không dùng làm ranh giới control cần nhận biết.

X2.2: CHẤP NHẬN — Viền nút phụ chuyển thành #747F93 ở Light, #90A1B9 ở Dark.

X2.3: CHẤP NHẬN — Input/select phải có viền mạnh và focus ring; không dựa vào chênh lệch nền panel/canvas 1,09:1 để nhận diện.

X2.4: CHẤP NHẬN — Viền control Dark #90A1B9, tương phản 5,45:1 trên Surface. #344564 chỉ dùng divider trang trí.

X2.5: CHẤP NHẬN — Menu active Light có vạch #F5BA6E rộng 3px, tương phản 6,92:1 trên sidebar #17385B.

X2.6: CHẤP NHẬN — Dark cũng sử dụng vạch #F5BA6E; không dựa riêng vào nền active.

X2.7: CHẤP NHẬN — Màu biểu đồ không dùng làm nhãn chữ nhỏ. Label/legend luôn dùng --at-ink; màu chart-5/6 chỉ dùng cho nét và vùng biểu diễn.

X3 — Những điểm không nên học web trường

X3.1: CHẤP NHẬN — Sidebar cấp một tối đa 8 mục; không sao chép cấu trúc 33 mục của trường.

X3.2: CHẤP NHẬN — Một màu action chính, một màu AI, bộ màu trạng thái riêng; không trộn nhiều màu xanh làm CTA.

X3.3: CHẤP NHẬN — Một họ Be Vietnam Pro; table cell tối thiểu 13px, chữ phụ tối thiểu 12px.

X3.4: CHẤP NHẬN — Không bảng lồng bảng, không cảnh báo chồng cảnh báo; tối đa một banner trạng thái nghiệp vụ chính tại đầu một section.

X3.5: CHẤP NHẬN — Đăng nhập không sử dụng ảnh đám đông hoặc ảnh sinh viên. Vùng nhận diện dùng Open Path và hình học trừu tượng tĩnh.

X3.6: CHẤP NHẬN — Phân biệt viền trang trí với viền điều khiển: --at-line nhạt được phép, --at-control-border phải đạt tối thiểu 3:1.

X4 — Tiêu chí đo được

X4.1: CHẤP NHẬN — 100% màn hình đã đăng nhập có Open Path và Capstone AI, 0 logo/tên trường trong chrome, 0 ảnh stock; khoảng cách RGB header tối thiểu 40.

X4.2: CHẤP NHẬN — Chữ thường tối thiểu 4,5:1; ranh giới control và focus tối thiểu 3:1. Màu mới phải được kiểm tra tự động trên Light/Dark.

X4.3: CHẤP NHẬN — Brand, AI, Info là ba mã riêng; ở viewport 1280×800, điểm AI và ít nhất một lý do phù hợp phải thấy trong viewport đầu tại Trang chủ SV và Chi tiết đề tài.

X4.4: CHẤP NHẬN — Sidebar tối đa 8 mục; một nút primary đặc màu brand trong mỗi nhóm hành động. Không dùng bốn nút trạng thái khác màu trên cùng header.

X4.5: CHẤP NHẬN — Chữ bảng tối thiểu 13px, chữ phụ 12px; focus outline 2px đạt 3:1; Bottom Navigation dưới 768px tối đa 4 mục.

=== SỬA ĐỔI V3.5 ===

Mọi giá trị dưới đây ghi đè V3.4 nếu có xung đột.

1. Hệ màu chính thức
Light theme

Token

	

Giá trị




--at-canvas

	

#F2F5FB




--at-surface

	

#FFFFFF




--at-surface-2

	

#F5F8FE




--at-surface-hover

	

#EAF1FF




--at-header

	

#142B4B




--at-sidebar

	

#17385B




--at-sidebar-active

	

#294E79




--at-active-indicator

	

#F5BA6E




--at-brand

	

#2454B8




--at-brand-hover

	

#1D4496




--at-on-brand

	

#FFFFFF




--at-ai

	

#176B60




--at-ai-soft

	

#E6F4F0




--at-info

	

#315D91




--at-info-soft

	

#EAF1FF




--at-ink

	

#212529




--at-ink-muted

	

#596579




--at-line

	

#DDE4EF




--at-control-border

	

#747F93




--at-focus

	

#2454B8




--at-success

	

#176B50




--at-success-soft

	

#E7F5ED




--at-warning

	

#925A31




--at-warning-soft

	

#FFF4E5




--at-danger

	

#B42332




--at-danger-soft

	

#FFF1F2

Dark theme

Token

	

Giá trị




--at-canvas

	

#121D32




--at-surface

	

#1B2A45




--at-surface-2

	

#243653




--at-surface-hover

	

#30466B




--at-header

	

#101C31




--at-sidebar

	

#15223A




--at-sidebar-active

	

#213C81




--at-active-indicator

	

#F5BA6E




--at-brand

	

#B5D4FF




--at-brand-hover

	

#D2E4FF




--at-on-brand

	

#121D32




--at-ai

	

#84D0BD




--at-ai-soft

	

#233D3B




--at-info

	

#A9C7ED




--at-info-soft

	

#243B61




--at-ink

	

#EAF1FF




--at-ink-muted

	

#CAD4E4




--at-line

	

#344564




--at-control-border

	

#90A1B9




--at-focus

	

#B5D4FF




--at-success

	

#A6D2B8




--at-success-soft

	

#233D30




--at-warning

	

#F0C58A




--at-warning-soft

	

#493827




--at-danger

	

#F4A9A2




--at-danger-soft

	

#4C2C2B

Màu biểu đồ

Series

	

Light

	

Dark




Chart 1 / NV1

	

#2454B8

	

#8AB4FF




Chart 2 / NV2

	

#176B50

	

#86CDAE




Chart 3 / NV3

	

#91603A

	

#E0AF80




Chart 4 / Ngoài NV

	

#77539C

	

#C4A5E0




Chart 5

	

#357A92

	

#8DC8DB




Chart 6

	

#777B43

	

#C4C987

Legend luôn dùng --at-ink, không dùng màu chart làm chữ.

Một số cặp tương phản quan trọng

Cặp màu

	

Tỉ lệ

	

Kết quả




Trắng / Header Light

	

14,22:1

	

AAA




Trắng / Sidebar Light

	

11,98:1

	

AAA




Trắng / Brand Light

	

6,92:1

	

AA




AI Light / Trắng

	

6,35:1

	

AA




Info Light / Trắng

	

6,76:1

	

AA




Control border Light / Trắng

	

4,04:1

	

Đạt yêu cầu 3:1




Control border Dark / Surface

	

5,45:1

	

Đạt yêu cầu 3:1




Active indicator / Sidebar Light

	

6,92:1

	

Đạt yêu cầu 3:1




AI Dark / Surface

	

8,02:1

	

AAA

2. Khung trang

Thành phần

	

Thông số V3.5




Sidebar desktop

	

216px, fixed left, cao 100dvh




Sidebar thu gọn

	

60px




Header

	

56px, nằm bên phải sidebar




Logo vùng sidebar

	

Open Path 32px + tên Capstone AI




Sidebar item

	

Cao 44px; icon 18px; nhãn 13px/500




Active

	

Nền --at-sidebar-active, vạch trái 3px




Content ≥1200px

	

Padding ngang 24px




Content 992–1199px

	

Padding ngang 20px




Content max-width

	

1600px




Grid

	

12 cột, gutter 16px




Khoảng cách section

	

16px




Tablet 768–991px

	

Header + navigation offcanvas




Mobile dưới 768px

	

Header 56px + Bottom Nav 64px




Bottom Action Bar

	

72px; khi hiện phải ẩn Bottom Nav




Drawer desktop

	

440px




Drawer nghiệp vụ mobile

	

Full-screen 100dvh




Footer

	

Min-height 40px, theo luồng nội dung

Header và sidebar cố định độc lập; vùng nội dung có min-width:0, không được gây tràn ngang.

3. Typography và thành phần

Thành phần

	

Thông số V3.5




Font

	

Be Vietnam Pro 400/500/600/700




H1 desktop

	

24px / 34px / 600




H1 mobile

	

22px / 32px / 600




H2

	

18px / 28px / 600




H3

	

16px / 25px / 600




Body

	

14px / 23px / 400




Table body

	

13px / 21px / 400




Table header

	

12px / 19px / 600




Nhãn form

	

13px / 21px / 600




Chữ phụ

	

12px / 19px / 400




Metric lớn

	

32px / 40px / 600




Điểm AI nổi bật

	

40px / 48px / 600




Section header

	

Cao 42px, padding ngang 16px




Section panel

	

Radius 6px, viền 1px trang trí




Input/select

	

Cao 38px desktop, 44px mobile




Button

	

Cao 38px desktop, 44px mobile




Table row

	

Min-height 44px, tự mở rộng nếu chữ dài




Table cell

	

Padding 10px 12px




Badge

	

Cao 24px, radius 4px




Tab active

	

Gạch dưới 2px




Focus

	

Outline 2px, offset 2px




Evidence M1–M5 mobile

	

5 hàng dọc




Empty state

	

Minh họa 112–144px, không tạo khoảng trắng quá lớn

Mỗi khu vực nghiệp vụ có một section header riêng. Không lồng nhiều panel, không dùng gradient, không thay thế độ tương phản bằng bóng đổ.

4. Thay đổi theo màn hình

Màn hình

	

Thay đổi bắt buộc




01. Đăng nhập

	

Hai vùng 5:7; nhận diện Navy + Open Path, form 400px, 3 tài khoản demo. Không ảnh stock.




02. Đổi mật khẩu

	

Form 480px trong một section trắng.




03. Thiếu hồ sơ

	

Banner nghiệp vụ + checklist trường còn thiếu + CTA.




04–06. 403/404/500

	

Giữ cấu trúc lỗi, cập nhật theme, giảm minh họa và khoảng trắng.




07. Trang chủ SV

	

Header SV + trạng thái đợt → Journey → Top 5 8/12 cột + NV 4/12. Đề tài tốt nhất có Evidence Panel; bốn đề tài khác là hàng gọn.




08. Hồ sơ năng lực

	

Tách section Thông tin / Giới thiệu / Kỹ năng / Lĩnh vực; bỏ các card kỹ năng rời rạc.




09. Nguyện vọng

	

Ba section NV1–NV3, mỗi section có tên đề tài, GV, điểm, điều kiện và đổi đề tài.




10. Danh sách đề tài

	

Toolbar → tabs trạng thái → bảng desktop / card mobile → phân trang.




11. Chi tiết đề tài

	

Thông tin đề tài trên đầu; mô tả 7/12 cột, AI Evidence 5/12 cột.




12. Kết quả SV

	

Một panel kết quả chính; phân biệt chưa công bố, đã xếp, chưa xếp.




13. Trang chủ GV

	

Ledger gọn → đề tài có SV chờ duyệt → trạng thái đợt.




14. Đề tài GV

	

Bảng với toolbar lọc, chỉ tiêu, số đăng ký, hành động.




15. Thêm/sửa đề tài

	

Section form theo nhóm thông tin, kỹ năng, điều kiện, chỉ tiêu.




16. GV duyệt SV

	

Bảng trái + drawer 440px phải, M1–M5 và Đồng ý/Từ chối cùng hàng.




17. Hồ sơ GV

	

Các section thông tin/chuyên môn/chỉ tiêu, không dùng card lồng.




18. Trang chủ Khoa

	

Trạng thái đợt → Ledger → danh sách đợt 7/12 + tác vụ 5/12.




19. Phân công Khoa

	

6 chỉ số trong một Ledger → biểu đồ → bảng 20 dòng/trang → drawer xếp tay.




20. Thống kê Khoa

	

Tình hình đăng ký → biểu đồ kết quả/lĩnh vực 7:5 → tải GV/ILP–Greedy 6:6 → bảng kiểm chứng.




21. Nhập Excel

	

Hướng dẫn → tải mẫu → upload → preview → lỗi → xác nhận nhập.

=== GIỮ NGUYÊN ===

Những quyết định sau từ V3.4 không được thay đổi:

Thương hiệu: Capstone AI, logo Open Path, SVG light/dark/favicon; không dùng logo hoặc tên trường.

Công nghệ: Django templates + Bootstrap 5.3 + Chart.js, một CSS ứng dụng static/css/atlas.css, tài nguyên đóng gói local.

AI: M1 kỹ năng, M2 học lực, M3 lĩnh vực, M4 ngữ nghĩa, M5 LLM; trọng số AHP, điểm sơ bộ và cách xử lý M5 chưa đánh giá.

Luồng SV: Hồ sơ → Gợi ý → Nguyện vọng → Kết quả, dựa trên trạng thái backend thật.

Kết quả và nguyện vọng: Sau CLOSED/PUBLISHED vẫn xem được dữ liệu lịch sử hợp lệ; không hiện phân công nháp cho SV.

Phân công: ILP/Greedy, xếp tay pha 2, kiểm capacity/quota, xác nhận công bố hai bước.

Bảng: Tìm kiếm, lọc, sắp xếp, phân trang server-side; không render 100 dòng liên tục.

Drawer: 440px desktop, full-screen mobile; dữ liệu chi tiết GET khi mở.

Theme: atlas-theme với light/dark/system, cập nhật khi OS đổi ở chế độ system.

Accessibility: WCAG AA, focus rõ, reduced-motion, quản lý focus modal/drawer, mobile touch target tối thiểu 44px.

Thông báo: Không có chuông giả; không tạo nút hay route chưa có chức năng.

Dữ liệu: Không hardcode kết quả 100 SV, 43%, 30%, 63,8; lấy động từ CSDL theo đợt.

=== TIÊU CHÍ NGHIỆM THU ===

Nhận diện: 100% màn hình đã đăng nhập có Open Path + Capstone AI; 0 logo/tên trường trong chrome; 0 ảnh stock.

Khung: Sidebar 216px hoặc 60px khi thu gọn; header vùng nội dung 56px; không còn rail 88px và Context Index.

Responsive: Screenshot 390, 768, 992, 1200 và 1440px không tràn ngang viewport, không chồng nút, không che nội dung.

WCAG: 0 cặp chữ thường dưới 4,5:1; 0 viền control/focus quan trọng dưới 3:1, đo trên cả Light/Dark.

Typography: Chỉ Be Vietnam Pro; bảng ≥13px, chữ phụ ≥12px; không có chữ nghiệp vụ 11px.

AI: Brand/AI/Info khác mã màu; tại 1280×800, điểm và lý do AI của đề tài nổi bật nhìn thấy trong viewport đầu.

Nghiệp vụ: 100% trạng thái OPEN/CLOSED/OPTIMIZED/PUBLISHED và thao tác theo quyền hoạt động đúng; không có dữ liệu giả.

Bảng: Phân trang server-side 20 dòng mặc định; tìm kiếm/lọc không mất điều kiện khi chuyển trang; không tải toàn bộ 100 SV.

Tương tác: Drawer, xác nhận hai bước, modal từ chối 5–500 ký tự, theme và Bottom Nav hoạt động; không có thành phần bấm giả.

QA: Có ảnh trước/sau Light/Dark tại 390px và 1440px; lint/test đạt, không lỗi JavaScript hoặc HTTP 500 trong luồng chính.

KẾT LUẬN: ATLAS V3.5 ĐƯỢC PHÊ DUYỆT TRIỂN KHAI. Các thông số trên thay thế phần xung đột của V3.4; không cần thêm vòng thảo luận thị giác trước khi lập trình.