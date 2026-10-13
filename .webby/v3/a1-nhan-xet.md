=== MỤC A: NHẬN XÉT ===

ĐIỂM THẨM ĐỊNH — NOVA V2

3,4

/10

Kết luận: REDESIGN TOÀN BỘ

Thẩm mỹ

3.8/10

Phân cấp

3/10

Dễ sử dụng

3.2/10

Luồng nghiệp vụ

2.6/10

Bản Nova không thất bại vì thiếu hiệu ứng hay màu sắc, mà vì không có hệ thống phân cấp thông tin và thứ tự hành động nhất quán. Nó trông giống một giao diện quản trị chưa hoàn thiện hơn là một sản phẩm hỗ trợ quyết định học thuật.

10 lỗi nghiêm trọng nhất

Mức

	

Lỗi quan sát

	

Quyết định




P0

	

1. Bố cục quá loãng. Các màn hình có vùng trống lớn, thông tin quan trọng lại bị ép nhỏ.

	

Thiết kế lại mật độ theo vai trò, không kéo giãn một kiểu layout cho mọi trang.




P0

	

2. Phân cấp thị giác yếu. Tiêu đề, mô tả, nút, bộ lọc và chỉ số thiếu sự phân biệt rõ ràng.

	

Mỗi trang chỉ có một tiêu đề chính, một hành động chính và một vùng nội dung trọng tâm.




P0

	

3. Khoảng cách không có quy luật. Chữ sát viền, nhiều vùng lại thừa khoảng trắng.

	

Áp dụng spacing scale 4/8/12/16/24/32/48px; khoảng đệm tối thiểu cho panel nội dung là 20px desktop, 16px mobile.




P0

	

4. Luồng nghiệp vụ và trạng thái sai. Kết quả đã công bố nhưng bước tiến trình vẫn ở gợi ý AI; trang cũ biến mất khi đợt đóng.

	

Backend quyết định trạng thái dựa trên dữ liệu thực, frontend không suy diễn từ trang hiện tại.




P0

	

5. Bảng Khoa mất khả năng kiểm soát. 100 dòng liên tục, không tìm kiếm, lọc hay phân trang.

	

Chuyển sang data workspace có bộ lọc, thanh hành động, phân trang và chi tiết theo dòng.




P1

	

6. Typography không nhất quán. Nhiều họ phông; chữ tiếng Việt và nhãn rất nhỏ, khó đọc khi chiếu.

	

Một họ font chính có dấu tiếng Việt chuẩn, hệ kích thước rõ ràng, không dùng chữ 10–11px cho thông tin nghiệp vụ.




P1

	

7. Màu tím chiếm quá nhiều vai trò. Điều hướng, hành động, trạng thái và điểm nhấn cùng tranh sự chú ý.

	

Tách rõ màu thương hiệu, màu tương tác, màu trạng thái và màu biểu diễn dữ liệu.




P1

	

8. Dữ liệu AI chưa trực quan. Top 5, điểm phù hợp và lý do đề xuất không tạo được cảm giác hệ thống thực sự có khả năng phân tích.

	

Điểm tổng hợp, 5 thành phần M1–M5, điều kiện và diễn giải AI phải có ngôn ngữ hiển thị thống nhất.




P1

	

9. Responsive chưa đúng bản chất. Ngăn kéo đè và tràn ngang; các thao tác duyệt sinh viên xếp chồng.

	

Mobile có bố cục riêng, thao tác theo từng sinh viên; không thu nhỏ bảng desktop.




P1

	

10. Các chi tiết tương tác thiếu hoàn thiện. Công tắc không nhãn, chuông vô dụng, phân trang Bootstrap lộ mặc định.

	

Không đưa vào giao diện những điều khiển chưa hoạt động; mọi trạng thái tương tác phải được thiết kế.

Quyết định: Không sử dụng Nova hoặc Mosaic làm cơ sở thị giác cho V3. Chỉ tái sử dụng logic nghiệp vụ, dữ liệu, biểu đồ và các SVG trạng thái rỗng đã có.

=== MỤC B: HƯỚNG MỚI ===

ATLAS — Academic Decision Workspace

Định hướng: Editorial × Research Instrument × Decision Workspace

Chính xác
Điềm tĩnh
Có chiều sâu học thuật
Ý tưởng thiết kế — 3 câu

ATLAS là không gian làm việc học thuật được thiết kế như một hồ sơ nghiên cứu kết hợp bàn điều khiển quyết định, thay vì một dashboard SaaS thông thường. Giao diện dùng nền giấy ngà, chữ mực than, đường phân cách tinh tế và các khối nội dung phẳng để tạo cảm giác nghiêm túc, đáng tin nhưng không cũ kỹ. AI không được thể hiện bằng hiệu ứng phát sáng hay biểu tượng trang trí, mà bằng điểm số có thể kiểm chứng, lý do có cấu trúc và minh bạch về những gì hệ thống đã tính toán.

Bảng cảm hứng thị giác

1. Editorial hierarchy

Tiêu đề lớn, chữ có độ tương phản mạnh, nhiều khoảng nghỉ có chủ đích.

2. Data workspace

Thông tin có cấu trúc, đường phân cách rõ, ưu tiên mật độ sử dụng.

Hình chỉ minh họa ngôn ngữ thị giác, không phải giao diện để sao chép.

1. Bố cục khung
Desktop ≥ 992px

Thay thanh điều hướng ngang Nova và sidebar Mosaic bằng Navigation Rail + Context Index + Main Canvas.

ATLAS / Capstone AI

Đợt ĐATN 2026 · Khoa CNTT

Phân công

Tổng quan

Chưa xếp · 57

Đã xếp · 43

Cần rà soát

Đợt ĐATN 2026

Bản nháp phân công

KHOA / PHÂN CÔNG

Phân công đề tài
43/100

Sinh viên đã phân công

43%

Sinh viên

Đề tài / Trạng thái

Hoàng Quang Phúc

Đã xếp

Nguyễn Thu Hằng

Chưa xếp

Bùi Thị Hạnh

Đã xếp

Minh họa cấu trúc, không phải bản mockup hoàn chỉnh.

Quy tắc kích thước:

Rail cố định 68px, chỉ dùng icon Lucide có tooltip và aria-label. Cho phép thu gọn hoàn toàn phần Context Index.

Context Index rộng 224px, chỉ hiện ở những trang cần điều hướng hoặc bộ lọc nhiều cấp; không biến thành sidebar menu toàn hệ thống.

Main Canvas rộng tối đa 1480px; padding 32–40px. Trang Khoa ưu tiên chiều rộng bảng; các trang hồ sơ có giới hạn chiều rộng vùng đọc 760–880px.

Header sản phẩm cao 60px, không lặp menu trong header. Chỉ chứa ngữ cảnh đợt, tìm kiếm khi phù hợp, tài khoản và thiết lập.

Khác biệt mấu chốt: Rail điều hướng theo nhóm chức năng, Context Index điều hướng theo công việc đang làm, nội dung chính là một bề mặt thống nhất. Không dựng 3 lớp card.

Mobile dưới 768px

Dùng Mobile Reading Canvas + Bottom Navigation, không giữ rail desktop.

ATLAS.

ĐỀ XUẤT PHÙ HỢP

Đề tài dành cho bạn

Xem mức phù hợp và lý do hệ thống đề xuất.

86,4

/100 điểm

Ứng dụng di động quản lý sự kiện

Đề tài minh họa · NV1

M1

M2

M3

M4

M5

Xem phân tích

Các đề tài tiếp theo

Hệ thống giám sát ký túc xá

Quản lý đặt phòng khách sạn

Trang chủ

Đề tài

Nguyện vọng

Hồ sơ

Các điểm số và đề tài trong khung điện thoại chỉ minh họa cách bố trí.

Mobile rules: thanh điều hướng đáy tối đa 4 mục, cao 64–72px cộng safe area; không nằm đè nội dung. Nút hành động chính tại các bước nhập/nguyện vọng có thể cố định phía trên thanh điều hướng, với khoảng đệm tương ứng. Bộ lọc mở bằng bottom sheet hoặc offcanvas toàn chiều rộng, không tự tạo một trang tràn ngang.

2. Bảng màu

Light — Academic Paper

Canvas

#F6F4EE

Surface

#FFFEFA

Ink

#222923

Forest

#305F52

Muted

#69736C

Line

#D9DDD4

AI Accent

#386D80

Warm

#A66D40

Dark — Graphite Study

Canvas

#151B19

Surface

#202724

Ink

#ECEFE8

Forest

#8BB8A4

Muted

#A8B4AB

Line

#39443E

AI Accent

#8DBFD0

Warm

#E0AF80

Quy tắc: Forest dùng cho hành động chính, AI Accent dành riêng cho phân tích mô hình và điểm số. Trạng thái lỗi dùng chữ đỏ sẫm trên nền trung tính, không tô đỏ cả thẻ hay dòng bảng. Không dùng gradient. Không dùng bóng màu; phần lớn khối sử dụng đường viền 1px hoặc khoảng trắng để phân tách.

3. Typography

Chốt một họ duy nhất: Be Vietnam Pro. Đây là phông được phát triển với trọng tâm hỗ trợ tiếng Việt, có các kiểu dấu phù hợp. 
GitHub
+1

Tiêu đề chính desktop 30–34px, mobile 25–28px, weight 600.

Tiêu đề khu vực 19–22px, weight 600.

Nội dung thường 14–15px, line-height 1.55.

Bảng dữ liệu 13–14px; nhãn 12–13px; số liệu lớn 36–48px.

Không sử dụng ALL CAPS kéo dài cho tiếng Việt. Chỉ dùng chữ hoa với nhãn rất ngắn.

Dùng font theo dạng self-hosted .woff2, tải đầy đủ vietnamese và latin, dùng font-display: swap, không gọi Google Fonts CDN lúc chạy. Giữ font chữ số tabular cho bảng và KPI.

4. Hệ thống trình bày số liệu

Thay hàng 6–8 KPI card bằng Metric Ledger: một hàng số liệu phẳng, có đường phân cách dọc, nhãn phía trên hoặc phía dưới, thay đổi màu chỉ khi cần diễn đạt trạng thái.

Đợt ĐATN 2026

Đang xử lý pha 2
100

Sinh viên

43

Đã phân công

57

Chờ pha 2

63,8

Điểm phù hợp TB

30% đạt NV1 · 43% đạt Top 3

Số liệu thật cần giữ đúng: 100 SV, 15 GV, 50 đề tài, 43% đã xếp, 30% đạt NV1, 43% Top 3, điểm phù hợp trung bình 63,8, còn 57 SV chờ pha 2. Không sử dụng số demo khác để thay các con số này trong trang Khoa.

Điểm AI M1–M5: Evidence Strip

Không dùng biểu đồ radar làm thành phần chính: người xem khó đọc giá trị chính xác, còn hội đồng cần biết hệ thống tính ra sao.

Mỗi đề tài hiển thị điểm tổng hợp, năm thước đo song song, trạng thái đủ điều kiện và lời giải thích ngay trong cùng một vùng.

Ví dụ minh họa
Ứng dụng quản lý sự kiện

Phân tích mức độ phù hợp của sinh viên

84,2

/100

M1

Kỹ năng

88

M2

Học lực

78

M3

Lĩnh vực

95

M4

Ngữ nghĩa

82

M5

Đánh giá LLM

75

Vì sao đề tài này phù hợp?

Ví dụ: lĩnh vực quan tâm trùng khớp, kỹ năng đạt yêu cầu; cần xem xét thêm mức độ sẵn sàng triển khai.

Quy định bắt buộc cho M1–M5:

Điểm tổng hợp phải là kết quả tính từ trọng số AHP đang có hiệu lực, không lấy trung bình cộng năm điểm minh họa.

Hiển thị trọng số AHP và phiên bản cấu hình khi mở chi tiết phân tích.

Điều kiện bắt buộc (kỹ năng, học phần, GPA) hiển thị độc lập với điểm mềm; điểm cao không được tự động vượt qua hard filter.

M5 chưa tính thì ghi "Chưa đánh giá", không gán 0. M5 dự phòng phải nêu rõ phương pháp fallback; không giả làm điểm do LLM sinh ra.

Có thể xem lý do ở ba lớp: kết luận dễ hiểu → chứng cứ chi tiết → thông tin mô hình và phiên bản để phục vụ bảo vệ.

5. Ngôn ngữ chuyển động

Chọn duy nhất Quiet Precision.

Thành phần

	

Cảm giác & thông số




Hover nút / hàng

	

Đổi màu nền hoặc đường viền nhẹ, 120ms




Chuyển vùng / tab

	

Fade 160–180ms; không bay/zoom




Dialog / sheet

	

Fade + translate 8px, 180–220ms




Điểm số / biểu đồ

	

Hiện dần tối đa 240ms khi dữ liệu sẵn sàng, không giả lập AI đang suy nghĩ




Loading

	

Skeleton trung tính ở vùng dữ liệu; hành động xử lý dài có spinner và trạng thái rõ




Reduced motion

	

Tắt dịch chuyển và hiệu ứng không thiết yếu với prefers-reduced-motion: reduce

Tất cả chuyển động dùng cùng một easing cubic-bezier(.2, .7, .2, 1). Không hiệu ứng neon, không stagger hàng loạt, không đếm KPI giả.

=== MỤC C: SỬA LUỒNG ===

Các quy định dưới đây là hợp đồng giữa Design Authority và đội triển khai. Backend cung cấp trạng thái thật; frontend chỉ hiển thị theo trạng thái đó.

Lỗi 4 — Bảng phân công 100 dòng
Giao diện thay thế: Assignment Workspace
Danh sách phân công

100 sinh viên · 57 chưa xếp

Đang xử lý
Tất cả
Chưa xếp
Đã xếp

Sinh viên

	

Trạng thái

	

Điểm




Hoàng Quang Phúc

SV001

	

Đã xếp

NV1

	

78,5




Nguyễn Thu Hằng

SV002

	

Chưa xếp

—

	

—




Bùi Thị Hạnh

SV003

	

Đã xếp

NV2

	

67,0

Bản minh họa tương tác bằng dữ liệu mẫu. Triển khai thật phải truy vấn dữ liệu và phân trang phía server.

Yêu cầu hiển thị: lọc theo trạng thái, NV1/NV2/NV3, giảng viên, ngành/lĩnh vực, điểm phù hợp; tìm theo mã/tên; sắp xếp tăng/giảm; 20 dòng/trang mặc định, tùy chọn 10/20/50. Thanh công cụ luôn cho biết đang xem bao nhiêu trên tổng số bản ghi. Dòng chưa xếp giữ nền bình thường, chỉ dùng nhãn hoặc ký hiệu trạng thái.

Khi chọn sinh viên, mở chi tiết có giới hạn chiều rộng 420–480px trên desktop, toàn màn hình trên mobile. Nếu có nguy cơ tràn ngang, modal căn giữa là phương án thay thế được phép. Chi tiết hiển thị ba nguyện vọng, điểm và điều kiện, nguyên nhân chưa xếp, danh sách đề tài còn chỗ. Nút Xếp tay chỉ xuất hiện khi đợt ở pha cho phép xếp tay.

Backend Claude cần bổ sung:

GET /allocations với tham số page, page_size, q, status, rank, lecturer_id, field_id, sort.

Tổng số bản ghi, tổng sau lọc và số trang; truy vấn phân trang thực ở database, không render đủ 100 dòng rồi ẩn bằng JavaScript.

student_id, student_code, name, GPA, preference_rank, topic_id, lecturer_id, match_score, source, allocation_status, unassigned_reason.

Danh sách lựa chọn xếp tay từ đề tài hợp lệ, còn capacity và thỏa ràng buộc; kiểm tra lại bằng transaction khi lưu.

Kết quả xử lý ILP/Greedy và trạng thái đợt để khóa đúng các hành động.

Lỗi 5 — Trạng thái sinh viên sai khi đợt đóng / công bố
Thay progress bar tuyến tính bằng Period Status + Journey

Thanh bốn bước cũ đang gộp nhầm tiến độ cá nhân với trạng thái nghiệp vụ toàn đợt. ATLAS tách hai khái niệm.

Đợt ĐATN 2026

Trạng thái theo kỳ đăng ký

Đã công bố

Hồ sơ năng lực

Hoàn thành

Gợi ý AI

Đã tạo danh sách phù hợp

Nguyện vọng

Đã nộp · chỉ xem

Kết quả phân công

Đã công bố · xem kết quả

Đây không phải thanh tiến trình cố định. Ví dụ sinh viên chưa nộp nguyện vọng nhưng đợt đã đóng phải nhìn thấy "Chưa nộp trong đợt này", không được đánh dấu hoàn thành.

Tình huống

	

Giao diện bắt buộc




Đợt đang mở, SV chưa nộp

	

Hiện gợi ý, hướng dẫn hoàn thiện hồ sơ và CTA đăng ký.




SV đã nộp NV1–NV3

	

Hiện đầy đủ 3 nguyện vọng và thời điểm nộp; khả năng sửa tùy quy định của đợt.




Đợt đóng

	

Giữ nguyên danh sách nguyện vọng đã nộp trong chế độ chỉ xem.




Đang tối ưu/chờ công bố

	

Hiện thông báo đang xử lý, không công khai phân công nháp.




Đã công bố, SV được phân công

	

Hiện tên đề tài, giảng viên, thứ tự nguyện vọng trúng, điểm phù hợp và trạng thái chính thức.




Đã công bố, SV chưa được phân công

	

Hiện "Chưa được phân công trong đợt này"; chỉ nêu phương án tiếp theo khi có thông tin thực.




Top 5 hiện trống

	

Nếu có bản gợi ý thì render; nếu chưa có, phân biệt chưa tạo, dữ liệu đã lỗi thời, hoặc lỗi tính toán. Không nói "chưa có đề tài" một cách chung chung.

Backend Claude cần bổ sung:

period.status, published_at, registration_open_at, registration_closed_at và quyền thao tác tương ứng.

student_profile_complete, recommendation_status, recommendation_generated_at, recommendation_profile_version, recommendation_weights_version.

submitted_preferences từ database, không chỉ query những nguyện vọng thuộc đợt OPEN.

allocation.status và allocation.published_at; chỉ kết quả OFFICIAL thuộc đợt đã công bố mới hiển thị cho sinh viên.

Bản ghi Top 5 hoặc trạng thái gợi ý bị lỗi thời; khi kết quả đã công bố vẫn giữ quyền xem lịch sử gợi ý và nguyện vọng đã nộp nếu dữ liệu còn được lưu.

Bảo đảm mỗi màn hình cùng đọc một trạng thái đợt thống nhất, tránh dashboard nói đã công bố nhưng trang khác nói chưa có đợt.

Lỗi 6 — Danh sách đề tài không giải thích điều kiện và điểm AI
Giao diện thay thế: Topic Evidence List

Mỗi dòng hoặc khối đề tài có 4 lớp thông tin: tên đề tài, trạng thái điều kiện, điểm phù hợp, hành động.

ĐỀ TÀI · MINH HỌA

Chatbot hỗ trợ học tập trực tuyến

Lĩnh vực: Trí tuệ nhân tạo

82

/100

Đủ điều kiện đăng ký

Xem 5 yếu tố đánh giá

ĐỀ TÀI · MINH HỌA

Hệ thống phân tích dữ liệu học tập

76/100

Chưa đủ điều kiện

Ví dụ: yêu cầu kỹ năng Python mức 4, hiện tại mức 2; chưa đạt điều kiện học phần tiên quyết.

Xem điều kiện chi tiết

Quy tắc xử lý:

Đủ điều kiện: được đăng ký khi đợt mở và đề tài còn chỗ.

Không đủ điều kiện: vẫn xem được thông tin và điểm phân tích nếu đã có; nút đăng ký bị khóa, lý do phải cụ thể.

Chưa có điểm AI: hiển thị "Chưa đánh giá", không dùng dấu gạch ngang gây nhầm với điểm 0.

M1–M4 có thể là kết quả sơ bộ; M5 bổ sung khi đề tài nằm trong Top 15 hoặc được chọn làm nguyện vọng theo logic hai giai đoạn.

Không tính M5 cho toàn bộ 50 đề tài chỉ để lấp chỗ trống giao diện.

Nếu kết quả chỉ là điểm sơ bộ, hiển thị nhãn "Điểm sơ bộ M1–M4", không trình bày như điểm tổng hợp đủ M1–M5.

Nếu không thể tính một điểm hợp lệ thì hiển thị "Chưa có điểm", không tự tính lại bằng công thức không được backend phê duyệt.

Backend Claude cần bổ sung:

eligibility.is_eligible, eligibility.reasons[] với rule_type, required_value, actual_value, is_mandatory; score_status, preliminary_score, final_score, m1..m5, weights_version, model_version, llm_score_source, is_top15, topic_capacity, remaining_capacity, can_register, register_disabled_reason.

API phải lọc đủ điều kiện bằng các quy tắc nghiệp vụ thực. Không suy diễn is_eligible chỉ từ điểm tổng hợp.

Lỗi 7 — Công tắc sáng/tối không nhãn và chuông vô dụng
Thay bằng Preferences & Activity

Đổi giao diện: bỏ công tắc trơn trên header. Đưa vào menu tài khoản mục "Giao diện" với 3 lựa chọn Sáng / Tối / Theo thiết bị, có icon sun, moon, monitor. Người dùng phải biết lựa chọn hiện tại. Áp dụng data-bs-theme cho toàn hệ thống, lưu lựa chọn cá nhân ở localStorage, tùy chọn đồng bộ tài khoản nếu backend hỗ trợ; chế độ mặc định là theo thiết bị.

Thông báo: ở V3 chỉ có hai phương án hợp lệ:

Nếu triển khai đầy đủ: chuông có số thông báo chưa đọc, danh sách sự kiện thật, thời gian, trạng thái đã đọc và liên kết đến trang tương ứng.

Nếu chưa có hệ thống thông báo: loại bỏ hoàn toàn chuông. Không giữ nút trang trí giả chức năng.

Thông báo nên phát sinh từ các sự kiện thật như giảng viên duyệt/từ chối nguyện vọng, đợt đăng ký đóng, công bố kết quả hoặc cập nhật liên quan trực tiếp tới người nhận. Với hoạt động xếp nháp nội bộ, không gửi thông báo phân công chính thức tới sinh viên.

Backend Claude cần bổ sung nếu triển khai chuông: notifications(id, recipient_id, event_type, title, body, target_url, created_at, read_at), bộ đếm chưa đọc, đánh dấu đã đọc có kiểm tra quyền và lọc thông báo theo người nhận. Không bắt buộc WebSocket; có thể dùng polling hợp lý nếu cần.

Quyết định nghiệm thu cuối cùng

ATLAS V3 chỉ được thông qua khi đạt đồng thời các điều kiện sau:

Cả 18 màn hình sử dụng cùng hệ màu, chữ, spacing, trạng thái và tương tác; không còn Bootstrap mặc định lộ ra ở phân trang, form và modal.

Test giao diện tại 390px, 768px, 1440px và kích thước trình chiếu laptop; không có tràn ngang, chữ dính viền hay điều khiển chồng lên nhau.

Trang Khoa quản lý được toàn bộ 100 SV mà không tải 100 dòng liên tục, có tìm kiếm, lọc, phân trang và xếp tay đúng quyền.

Sinh viên vẫn xem được nguyện vọng sau khi đợt đóng, xem được kết quả chính thức sau công bố, và không bị dẫn vào trạng thái rỗng giả.

Giảng viên có thể xem chứng cứ M1–M5 và duyệt/từ chối theo một luồng rõ ràng; hành động từ chối yêu cầu lý do và xác nhận.

Hệ thống có thể trình bày và giải thích đúng các kết quả 43%, 30%, 63,8 và 57 SV chờ pha 2 trên máy chiếu; không sử dụng dữ liệu dựng để che chỗ trống.

Phán quyết Design Authority: Chọn duy nhất ATLAS — Academic Decision Workspace. Gemini và Grok được triển khai theo đặc tả này, Claude chịu trách nhiệm đảm bảo dữ liệu, quyền hạn, trạng thái và thao tác đúng nghiệp vụ. Không quay lại giao diện sidebar đầy đủ Mosaic, thanh điều hướng ngang Nova, gradient tím hay dashboard KPI dạng card trang trí.