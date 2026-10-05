BẢN THIẾT KẾ UI/UX — TRANG HỒ SƠ SINH VIÊN

Dự án: Capstone Advisor AI
Framework: Django Template + Bootstrap 5
Trang triển khai: /ho-so/
Template chính: templates/catalog/student_profile.html
Phạm vi chỉnh sửa: chỉ templates/ và static/
Đối tượng: Sinh viên — hồ sơ dùng làm dữ liệu đầu vào cho hệ thống gợi ý đề tài.

Nguyên tắc triển khai quan trọng: không đổi tên field, không bỏ management_form, không sửa luồng POST/backend hiện có. Chỉ thay đổi markup trình bày, class Bootstrap/CSS và JavaScript giao diện nếu cần.

1. Định hướng thiết kế

Trang /ho-so/ không nên mang cảm giác như một form quản trị Django. Đây phải giống một “Hồ sơ năng lực học thuật” để sinh viên hiểu rằng thông tin họ nhập sẽ ảnh hưởng tới việc AI tìm đề tài phù hợp.

Phong cách:

Hiện đại nhưng nghiêm túc, phù hợp môi trường đại học.
Tập trung vào nội dung, không dùng gradient/animation quá mức.
Card trắng, nền xám rất nhạt.
Màu xanh làm màu chức năng chính.
AI chỉ là công cụ hỗ trợ, không biến toàn bộ trang thành “AI futuristic”.
Desktop thoáng; mobile 390 px phải sử dụng được bằng một tay.
Không có card lồng card quá nhiều.
Không có sidebar cố định ở trang hồ sơ sinh viên.
2. Design Tokens
2.1. Font

Google Fonts:

CSS
font-family: "Be Vietnam Pro", system-ui, -apple-system, BlinkMacSystemFont,
             "Segoe UI", sans-serif;

Import:

XML
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">

Quy ước:

Thành phần	Size desktop	Mobile	Weight
H1	28px	24px	700
H2 / tiêu đề section	20px	18px	600
H3 nhỏ	16px	16px	600
Body	15px	15px	400
Form label	14px	14px	600
Helper text	13px	13px	400
Badge	12–13px	12px	600

Line-height body:

CSS
line-height: 1.55;

Không dùng font-weight 300 vì khả năng đọc tiếng Việt kém trên màn hình nhỏ.

3. Hệ màu
Primary
Plain text
Primary 700: #174EA6
Primary 600: #1D5DB8
Primary 500: #2563C4
Primary 100: #E8F0FE
Primary 50 : #F4F7FE

Nút chính:

CSS
background: #174EA6;
color: #FFFFFF;

Hover:

CSS
background: #123F88;
Neutral
Plain text
Text primary:   #172033
Text secondary: #5A6578
Text muted:     #6B7280

Border:         #D8DEE8
Border subtle:  #E8ECF2

Page bg:        #F6F8FB
Card bg:        #FFFFFF
Input bg:       #FFFFFF
Semantic
Plain text
Success:        #157347
Success bg:     #EAF7F0

Warning:        #946200
Warning bg:     #FFF6DD

Danger:         #B42318
Danger bg:      #FDECEC

Info:           #175CD3
Info bg:        #EFF5FF
Không dùng

Không sử dụng:

chữ xám nhạt hơn #6B7280 trên nền trắng cho nội dung quan trọng;
vàng sáng làm chữ;
xanh cyan nhạt;
text primary với opacity thấp.

Mục tiêu là duy trì WCAG AA, đặc biệt cho text thường.

4. Khoảng cách

Dùng hệ 4px:

Plain text
4px
8px
12px
16px
20px
24px
32px
40px
48px

Quy chuẩn:

Plain text
Khoảng cách giữa label và input:       8px
Các field cùng nhóm:                  16px
Giữa các nhóm trong card:             24px
Padding card desktop:                 24–28px
Padding card mobile:                  16px
Khoảng cách giữa card:                20px
Khoảng cách H1 → mô tả:                8px
Page top/bottom:                      32–48px

Không để các phần cách nhau 50–80px như landing page.

5. Bo góc và bóng
CSS
--radius-sm: 8px;
--radius-md: 12px;
--radius-lg: 16px;

Input:

CSS
border-radius: 10px;

Button:

CSS
border-radius: 10px;

Card:

CSS
border-radius: 14px;
border: 1px solid #E3E8EF;
box-shadow: 0 2px 8px rgba(16, 24, 40, 0.04);

Không dùng shadow lớn kiểu:

CSS
0 20px 50px rgba(...)

Trang học thuật không cần hiệu ứng nổi mạnh.

6. Container chung
CSS
.profile-page {
    max-width: 1120px;
    margin: 0 auto;
}

Bootstrap:

XML
<div class="container py-4 py-lg-5">

Không kéo form full chiều rộng màn hình desktop.

7. Navbar

Navbar dùng chung trong base.html.

Desktop

Chiều cao khoảng:

Plain text
64–68px

Bên trái:

Plain text
EAUT
Capstone Advisor AI

Có thể dùng logo trường hiện có nếu dự án đã có asset chính thức.

Giữa/phải đối với Sinh viên:

Plain text
Tổng quan
Hồ sơ năng lực
Đăng ký nguyện vọng

Phía cuối:

Plain text
sv001 / Tên sinh viên
Avatar initials
Dropdown
Active state

Khi ở /ho-so/:

Plain text
Hồ sơ năng lực

sử dụng:

CSS
color: #174EA6;
font-weight: 600;

và một đường active 2px ở dưới.

Không dùng tab xanh kín cả nền navbar.

Mobile

390px:

logo/tên hệ thống bên trái;
hamburger bên phải;
menu collapse Bootstrap;
mỗi item cao tối thiểu 44px;
Hồ sơ năng lực và Đăng ký nguyện vọng hiện rõ trong menu.

Không cố nhét tên tài khoản và toàn bộ nav vào một hàng.

8. Bố cục trang /ho-so/
8.1. Desktop

Cấu trúc:

Plain text
Breadcrumb nhỏ

Hồ sơ năng lực
Thông tin này giúp hệ thống hiểu năng lực và định hướng của bạn
để đề xuất các đề tài phù hợp hơn.

┌──────────────────────────────────────────────┐
│ Hoàn thiện hồ sơ                    80%       │
│ ████████████████████░░░                       │
│ Còn thiếu: 1 lĩnh vực quan tâm               │
└──────────────────────────────────────────────┘


┌──────────────────────────────────────────────┐
│ 01  Giới thiệu bản thân                      │
│     Mô tả ngắn về kinh nghiệm, thế mạnh...   │
│                                              │
│ [textarea                                  ] │
│ [                                          ] │
│                                              │
│                               180 / 500       │
└──────────────────────────────────────────────┘


┌──────────────────────────────────────────────┐
│ 02  Kỹ năng                                  │
│     Những kỹ năng bạn có thể sử dụng...      │
│                                              │
│ Kỹ năng             Mức độ                    │
│ [Python          ]  [Khá ▼]        [Xóa]     │
│ [Django          ]  [Tốt ▼]        [Xóa]     │
│                                              │
│ + Thêm kỹ năng                               │
└──────────────────────────────────────────────┘


┌──────────────────────────────────────────────┐
│ 03  Lĩnh vực quan tâm                        │
│                                              │
│ [Trí tuệ nhân tạo]                 [Xóa]     │
│ [Phát triển Web  ]                 [Xóa]     │
│                                              │
│ + Thêm lĩnh vực                              │
└──────────────────────────────────────────────┘


                           [Hủy] [Lưu hồ sơ]
Quan trọng

Không chia thành 2 cột form ở desktop chỉ để tận dụng không gian.

Form kỹ năng/lĩnh vực có thể rộng ~800–900px nhưng nên đọc theo chiều dọc.

9. Header trang

Phần trên:

Plain text
Hồ sơ năng lực

Subtitle:

Cập nhật kỹ năng, lĩnh vực quan tâm và phần giới thiệu để hệ thống có thêm dữ liệu khi đề xuất đề tài phù hợp với bạn.

Có thể thêm breadcrumb:

Plain text
Sinh viên / Hồ sơ năng lực

Breadcrumb rất nhỏ, không cần card.

10. Card “Hoàn thiện hồ sơ”

Đây là phần giúp sinh viên hiểu việc cần làm.

Ví dụ:

Plain text
Hoàn thiện hồ sơ                                      75%

██████████████████────────

Bạn đã bổ sung phần giới thiệu và kỹ năng.
Thêm ít nhất một lĩnh vực quan tâm để hồ sơ đầy đủ hơn.

Không gọi:

AI Profile Score

vì đây không phải điểm AI.

Mà gọi:

Mức độ hoàn thiện hồ sơ

Nếu backend không cung cấp % hoàn thiện thì không giả lập số %. Có thể bỏ toàn bộ card này trong implementation đầu tiên.

11. Card “Giới thiệu bản thân”

Header:

Plain text
01
Giới thiệu bản thân

Mô tả ngắn về kinh nghiệm, định hướng và loại đồ án bạn muốn thực hiện.

Textarea:

Plain text
Ví dụ: Tôi quan tâm đến phát triển web và AI, đã làm việc với
Python, Django và MySQL...

Chiều cao:

CSS
min-height: 140px;

Nếu backend có maxlength:

Plain text
180 / 500 ký tự

Nếu không có maxlength thì không tự đặt giới hạn làm ảnh hưởng dữ liệu.

Helper text

Nên viết 2–4 câu về thế mạnh, công nghệ đã học hoặc định hướng đồ án.

Không viết thuật ngữ:

Dữ liệu này được embedding vector hóa...

Sinh viên không cần biết ở bước nhập liệu.

12. Formset Kỹ năng

Đây là phần phải cẩn thận nhất vì backend đã hoàn thành.

Phải giữ nguyên:

django
{{ skill_formset.management_form }}

và field names Django sinh ra.

Không được chuyển thành input mới tự đặt name=.

Ví dụ logic template:

django
{{ skill_formset.management_form }}

{% for form in skill_formset %}
    ...
    {{ form.id }}
    {{ form.skill }}
    {{ form.level }}
    {{ form.DELETE }}
{% endfor %}

Tên thực tế phải theo source đang có, không tự suy đoán tên field.

Hiển thị desktop

Header row:

Plain text
Kỹ năng                           Mức độ

Mỗi row:

Plain text
[ Python / Django / SQL... ]      [ Mức độ ▼ ]    [Xóa]

Nếu field thực tế chỉ có tên kỹ năng mà không có level thì chỉ hiển thị field backend cung cấp.

Không thêm field backend chưa tồn tại.

13. Mobile cho kỹ năng

Không dùng bảng.

390 px:

Plain text
Kỹ năng 1

Kỹ năng
[ Python                         ]

Mức độ
[ Khá                          ▼ ]

                              Xóa

Sau đó border separator nhẹ.

Nút:

Plain text
+ Thêm kỹ năng

chiếm full width hoặc ít nhất cao 44px.

14. Xóa một dòng formset

Nếu Django formset sử dụng:

django
{{ form.DELETE }}

có thể style bằng CSS/JS thành nút:

Plain text
Xóa

nhưng checkbox DELETE thật vẫn phải tồn tại.

Không xóa DOM rồi làm backend mất index management form một cách tùy tiện.

Nếu dùng JS:

Plain text
Nhấn Xóa
→ tick DELETE
→ row chuyển trạng thái "Đã đánh dấu xóa"

hoặc ẩn visually nhưng không phá management data.

15. Lĩnh vực quan tâm

Phần này nên khác kỹ năng một chút về mặt nhận thức.

Header:

Plain text
03
Lĩnh vực quan tâm

Chọn những lĩnh vực bạn muốn ưu tiên khi tìm đề tài.

Nếu field hiện tại là select:

Plain text
[ Trí tuệ nhân tạo                      ▼ ]
[ Phát triển phần mềm                   ▼ ]

Nếu backend sử dụng text input, giữ nguyên.

Không tự chuyển sang multi-select thư viện bên ngoài nếu backend chưa hỗ trợ.

Nút:

Plain text
+ Thêm lĩnh vực
16. Nút hành động
Primary
Plain text
Lưu hồ sơ

Style:

CSS
.btn-primary-custom {
    min-height: 44px;
    padding: 10px 18px;
    background: #174EA6;
    border-color: #174EA6;
    font-weight: 600;
}
Secondary
Plain text
Hủy

hoặc quay lại:

Plain text
Quay lại

Nếu không tồn tại behavior “Hủy” rõ ràng, nên dùng:

Plain text
Về trang tổng quan

Không tạo nút không có chức năng.

Desktop

Cuối form:

Plain text
                           [Về tổng quan] [Lưu hồ sơ]
Mobile
Plain text
[Lưu hồ sơ                   ]
[Về trang tổng quan          ]

Primary đứng trước.

17. Sticky action trên mobile

Không cần sticky footer ở phiên bản đầu.

Một form hồ sơ ngắn không cần thanh nút dính đáy vì:

chiếm diện tích 390 px;
dễ che form;
làm giao diện giống app thương mại hơn hệ thống học thuật.
18. Input

Chiều cao:

CSS
min-height: 44px;

Style:

CSS
.form-control,
.form-select {
    border: 1px solid #C9D1DC;
    border-radius: 10px;
    color: #172033;
    background: #FFFFFF;
}

Focus:

CSS
border-color: #2563C4;
box-shadow: 0 0 0 3px rgba(37, 99, 196, 0.16);

Placeholder:

CSS
color: #7A8494;

Không remove focus outline mà không thay thế bằng trạng thái focus khác.

19. Validation

Error đặt ngay dưới field.

Ví dụ:

Plain text
Kỹ năng
[                              ]
Vui lòng nhập tên kỹ năng.

CSS:

Plain text
#B42318

Border lỗi:

Plain text
#D92D20

Không chỉ thể hiện lỗi bằng border đỏ vì người mù màu có thể khó nhận biết.

20. Thông báo
Thành công

Sau POST thành công:

Plain text
✓ Hồ sơ đã được cập nhật.
Thông tin mới sẽ được sử dụng trong các lần gợi ý tiếp theo.

Màu nhẹ:

Plain text
bg #EAF7F0
text #157347
border #B7E2C8

Không dùng popup modal cho save success.

Lỗi
Plain text
Không thể lưu hồ sơ.
Vui lòng kiểm tra các trường được đánh dấu bên dưới.

Alert đầu form + lỗi cụ thể từng field.

21. Trạng thái trống

Ví dụ sinh viên chưa có kỹ năng:

Không hiển thị một bảng rỗng.

Hiển thị:

Plain text
Bạn chưa thêm kỹ năng nào.

Hãy bổ sung những công nghệ hoặc kỹ năng bạn đã học,
ví dụ Python, Java, thiết kế cơ sở dữ liệu...

[+ Thêm kỹ năng]

Không cần illustration lớn.

Có thể sử dụng Bootstrap Icon:

Plain text
person-check
tools
lightbulb

nhưng tối đa 1 icon nhỏ/empty state.

22. Badge

Badge chỉ sử dụng cho dữ liệu trạng thái ngắn.

Ví dụ:

Plain text
Đã hoàn thiện
Chưa đầy đủ
Bắt buộc
Tùy chọn

Không biến tất cả kỹ năng thành hàng chục badge màu khác nhau nếu người dùng đang sửa form.

Badge phù hợp hơn ở chế độ xem.

23. Responsive 390px

Breakpoint quan trọng:

CSS
@media (max-width: 576px)

Page padding:

CSS
.container {
    padding-left: 16px;
    padding-right: 16px;
}

Card:

CSS
.profile-card {
    padding: 16px;
    border-radius: 12px;
}

Header:

Plain text
Hồ sơ năng lực

không được xuống thành 3 dòng.

Mọi input:

CSS
width: 100%;

Các row kỹ năng chuyển từ:

Plain text
input | select | delete

thành:

Plain text
input
select
delete

Khoảng cách ít nhất 12px.

Không có horizontal scroll ở 390px.

24. Mobile hierarchy

Thứ tự nội dung:

Plain text
Navbar
↓
Breadcrumb
↓
H1
↓
Mô tả
↓
Mức hoàn thiện
↓
Giới thiệu
↓
Kỹ năng
↓
Lĩnh vực
↓
Lưu

Đây cũng là thứ tự tab keyboard.

Không dùng CSS order đảo thứ tự thị giác khác DOM.

25. Accessibility

Bắt buộc:

XML
<label for="...">

tương ứng input.

Không dùng placeholder thay cho label.

Button icon phải có tên truy cập:

XML
<button aria-label="Xóa kỹ năng">

Thông báo lỗi:

XML
aria-describedby

Focus visible rõ.

Tap target:

Plain text
>= 44 × 44px

Không dùng màu là tín hiệu duy nhất cho:

lỗi;
thành công;
mức điểm;
trạng thái.
26. Card component dùng chung
XML
<section class="profile-section-card">
    <div class="section-heading">
        ...
    </div>

    <div class="section-content">
        ...
    </div>
</section>

CSS gợi ý:

CSS
.profile-section-card {
    background: #fff;
    border: 1px solid #E3E8EF;
    border-radius: 14px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(16, 24, 40, .04);
}

Mobile:

CSS
@media (max-width: 576px) {
    .profile-section-card {
        padding: 16px;
        border-radius: 12px;
    }
}
27. Number indicator cho section

Có thể dùng:

Plain text
01
02
03

dạng ô nhỏ:

CSS
.section-number {
    width: 32px;
    height: 32px;
    background: #E8F0FE;
    color: #174EA6;
    border-radius: 8px;
}

Mục đích là tăng hierarchy chứ không trang trí.

Không cần icon khác nhau cho cả ba section nếu đã dùng số.

28. Trang Hồ sơ — desktop wireframe hoàn chỉnh
Plain text
┌────────────────────────────────────────────────────────────────────────────┐
│ EAUT  Capstone Advisor AI       Tổng quan  Hồ sơ năng lực  Nguyện vọng   ▼│
└────────────────────────────────────────────────────────────────────────────┘


        Sinh viên / Hồ sơ năng lực

        Hồ sơ năng lực
        Cập nhật thông tin để hệ thống hiểu năng lực và định hướng
        của bạn khi đề xuất đề tài.


        ┌───────────────────────────────────────────────────────────────┐
        │ Mức độ hoàn thiện hồ sơ                              75%      │
        │ ██████████████████████████────────────                        │
        │ Bổ sung lĩnh vực quan tâm để hoàn thiện hồ sơ.                │
        └───────────────────────────────────────────────────────────────┘


        ┌───────────────────────────────────────────────────────────────┐
        │ 01   Giới thiệu bản thân                                      │
        │      Chia sẻ ngắn về kinh nghiệm và định hướng của bạn.       │
        │                                                               │
        │ Giới thiệu                                                    │
        │ ┌───────────────────────────────────────────────────────────┐ │
        │ │ Tôi quan tâm đến...                                       │ │
        │ │                                                           │ │
        │ └───────────────────────────────────────────────────────────┘ │
        │ Gợi ý: 2–4 câu về thế mạnh, công nghệ và hướng đồ án.        │
        └───────────────────────────────────────────────────────────────┘


        ┌───────────────────────────────────────────────────────────────┐
        │ 02   Kỹ năng                                                  │
        │      Bổ sung công nghệ và kỹ năng bạn đã sử dụng.             │
        │                                                               │
        │ Kỹ năng                           Mức độ                       │
        │ [ Python                      ]   [ Khá                    ▼ ] │
        │ [ Django                      ]   [ Tốt                    ▼ ] │
        │                                                               │
        │ [+ Thêm kỹ năng]                                              │
        └───────────────────────────────────────────────────────────────┘


        ┌───────────────────────────────────────────────────────────────┐
        │ 03   Lĩnh vực quan tâm                                        │
        │      Những hướng bạn muốn ưu tiên khi lựa chọn đề tài.        │
        │                                                               │
        │ [ Trí tuệ nhân tạo                                      ▼ ]  │
        │ [ Phát triển phần mềm                                   ▼ ]  │
        │                                                               │
        │ [+ Thêm lĩnh vực]                                             │
        └───────────────────────────────────────────────────────────────┘


                                      [Về tổng quan]   [Lưu hồ sơ]
29. Trang Hồ sơ — mobile 390px
Plain text
┌──────────────────────────────┐
│ EAUT  Capstone Advisor   ☰   │
└──────────────────────────────┘

Sinh viên / Hồ sơ

Hồ sơ năng lực
Cập nhật thông tin để hệ thống
đề xuất đề tài phù hợp hơn.

┌──────────────────────────────┐
│ Hoàn thiện hồ sơ        75%  │
│ █████████████████░░░░        │
│ Còn thiếu lĩnh vực quan tâm. │
└──────────────────────────────┘

┌──────────────────────────────┐
│ 01  Giới thiệu bản thân      │
│                              │
│ Giới thiệu                   │
│ [                          ] │
│ [                          ] │
│ [                          ] │
│                              │
│ Gợi ý: viết 2–4 câu...       │
└──────────────────────────────┘

┌──────────────────────────────┐
│ 02  Kỹ năng                  │
│                              │
│ Kỹ năng                      │
│ [ Python                   ] │
│                              │
│ Mức độ                       │
│ [ Khá                    ▼ ] │
│                         Xóa │
│ ───────────────────────────  │
│                              │
│ Kỹ năng                      │
│ [ Django                   ] │
│                              │
│ Mức độ                       │
│ [ Tốt                    ▼ ] │
│                         Xóa │
│                              │
│ [+ Thêm kỹ năng            ] │
└──────────────────────────────┘

┌──────────────────────────────┐
│ 03  Lĩnh vực quan tâm        │
│                              │
│ [ Trí tuệ nhân tạo       ▼ ] │
│                         Xóa │
│                              │
│ [+ Thêm lĩnh vực           ] │
└──────────────────────────────┘

[Lưu hồ sơ                  ]
[Về trang tổng quan         ]
30. Thành phần điểm AI dùng chung cho các trang sau

Trang hồ sơ chủ yếu cung cấp dữ liệu đầu vào, không cần ép M1–M5 vào trang này.

Tuy nhiên design system phải chuẩn hóa ngay cách hiển thị M1–M5 cho các trang:

gợi ý đề tài;
danh sách đề tài phù hợp;
chi tiết giải thích kết quả;
nguyện vọng.

Không nên chỉ hiện:

Plain text
M1 = 0.82
M2 = 0.67
M3 = 0.91
M4 = 0.76
M5 = 0.88

Người không chuyên sẽ không hiểu.

31. Quy tắc trình bày M1–M5

Theo kiến trúc Capstone Advisor AI, UI nên dùng tên dễ hiểu trước, mã mô hình sau.

Ví dụ:

Code	Tên hiển thị
M1	Phù hợp kỹ năng
M2	Phù hợp học lực
M3	Phù hợp lĩnh vực
M4	Tương đồng nội dung
M5	Đánh giá hỗ trợ từ AI

Hiển thị:

Plain text
Phù hợp kỹ năng
M1

chứ không phải:

Plain text
M1 SKILL MATCHING MODEL
32. Điểm tổng

Ví dụ:

Plain text
Mức độ phù hợp
86 / 100
Rất phù hợp

Nhưng chỉ hiển thị nhãn như “Rất phù hợp” nếu hệ thống đã định nghĩa ngưỡng chính thức.

Nếu backend chỉ trả score:

Plain text
Mức độ phù hợp
86 / 100

là đủ.

Không tự suy luận:

Plain text
AI khuyên bạn nên chọn đề tài này.

Nên dùng:

Hệ thống đánh giá đề tài này có mức độ phù hợp 86/100 dựa trên hồ sơ hiện tại.

33. Điểm thành phần M1–M5

Thiết kế:

Plain text
Chi tiết mức độ phù hợp

Kỹ năng                         82/100
████████████████░░░░

Học lực                         74/100
███████████████░░░░░

Lĩnh vực quan tâm               91/100
██████████████████░░

Tương đồng nội dung             86/100
█████████████████░░░

Đánh giá hỗ trợ từ AI           80/100
████████████████░░░░

Mã M1–M5 có thể nằm dạng muted:

Plain text
Kỹ năng · M1
34. Không dùng năm màu cho M1–M5

Sai:

Plain text
M1 = xanh
M2 = tím
M3 = vàng
M4 = hồng
M5 = cyan

Người dùng phải học màu vô ích.

Nên dùng cùng một màu primary cho progress bar.

Chỉ dùng màu semantic khi score cần truyền trạng thái đã được hệ thống định nghĩa.

35. Giải thích dưới mỗi M

Có thể mở bằng:

Plain text
Xem cách tính

Collapse Bootstrap:

Plain text
Kỹ năng · M1                   82/100
████████████████░░░░

Dựa trên mức độ tương đồng giữa kỹ năng trong hồ sơ
của bạn và kỹ năng yêu cầu của đề tài.

M2:

So sánh kết quả học tập liên quan với yêu cầu của đề tài.

M3:

Đánh giá mức độ trùng khớp giữa lĩnh vực bạn quan tâm và lĩnh vực của đề tài.

M4:

Đo mức độ tương đồng về nội dung giữa hồ sơ của bạn và mô tả đề tài.

M5:

AI đọc hồ sơ và yêu cầu đề tài theo một bộ tiêu chí cố định để cung cấp thêm một góc đánh giá.

Đặc biệt với M5, không viết:

AI xác nhận bạn phù hợp.

36. Disclosure về AI

Ở khu vực kết quả:

Plain text
Điểm phù hợp là dữ liệu hỗ trợ tham khảo, không thay thế quyết định
của sinh viên, giảng viên hoặc khoa.

Màu muted, icon info-circle.

Điều này giúp hệ thống mang tính học thuật và đáng tin hơn.

37. Badge điểm

Nếu có badge:

Plain text
86/100

thì badge nên:

CSS
background: #E8F0FE;
color: #174EA6;

Không dùng:

Plain text
AI: 98%

vì có thể khiến người dùng hiểu sai đây là xác suất chắc chắn.

Dùng thuật ngữ:

Plain text
Điểm phù hợp

thay cho:

Plain text
Độ chính xác AI
Xác suất phù hợp
AI confidence

trừ khi mô hình thực sự xuất probability/calibrated confidence.

38. Progress bar accessibility

HTML nên có:

XML
<div
  class="progress"
  role="progressbar"
  aria-label="Mức độ phù hợp kỹ năng"
  aria-valuenow="82"
  aria-valuemin="0"
  aria-valuemax="100">

Điểm số phải được viết bằng text bên cạnh.

Không bắt người dùng suy ra giá trị từ chiều dài thanh.

39. Bảng

Trang profile hiện tại không cần bảng.

Nhưng các trang danh sách sau này:

Desktop:

Plain text
Tên đề tài | Giảng viên | Lĩnh vực | Điểm phù hợp | Trạng thái | Hành động

Mobile không ép <table> 6 cột.

Chuyển mỗi row thành card:

Plain text
Xây dựng hệ thống gợi ý...
Nguyễn Văn A

Lĩnh vực
Trí tuệ nhân tạo

Điểm phù hợp
86/100

[Xem chi tiết]
40. Mẫu CSS architecture

Nên tạo file riêng:

Plain text
static/css/capstone-ui.css

hoặc:

Plain text
static/css/student-profile.css

Không nhét hàng trăm dòng CSS trực tiếp vào template.

Naming:

CSS
.profile-page
.profile-header
.profile-section-card
.profile-section-heading
.profile-section-number
.profile-help-text
.formset-row
.profile-actions
.ai-score
.ai-score-bar
.empty-state

Tránh class kiểu:

Plain text
.blue-card2
.box-new
.test-style
41. Bootstrap ưu tiên trước CSS tự viết

Tận dụng:

Plain text
container
row
col-*
d-flex
gap-*
mb-*
py-*
form-control
form-select
btn
alert
collapse
navbar

CSS riêng dùng cho:

màu thương hiệu;
typography;
radius;
card;
formset responsive;
score component.

Không viết lại grid system.

42. Quy tắc template Django

Đặc biệt với student_profile.html:

Phải giữ
django
{% csrf_token %}

và:

django
{{ ...management_form }}

của cả hai formset.

Phải giữ:

hidden ID;
hidden management values;
form prefix;
tên field;
validation errors;
DELETE field nếu backend sử dụng.
Không làm
XML
<input name="skill_name">

nếu Django hiện tại không dùng tên này.

Thiết kế phải bọc field Django có sẵn, không thay đổi contract backend.

43. Trạng thái loading

Submit form:

Plain text
Lưu hồ sơ

khi đã click có thể đổi thành:

Plain text
Đang lưu...

và disable button để tránh submit 2 lần.

Không cần spinner toàn màn hình.

44. Navbar sinh viên cần bổ sung

Theo yêu cầu nghiệp vụ, navbar role Sinh viên phải có:

Plain text
Tổng quan
Hồ sơ năng lực
Đăng ký nguyện vọng

Hồ sơ năng lực:

Plain text
/ho-so/

Đăng ký nguyện vọng phải dùng URL Django hiện có; không hard-code đường dẫn đoán.

Ưu tiên:

django
{% url '...' %}

theo tên route thực tế của project.

45. Không nên làm

Lập trình viên/Gemini không nên thêm:

glassmorphism;
gradient tím-xanh kiểu AI;
glow;
background mesh;
animated blobs;
card 3D;
icon quá lớn;
avatar minh họa AI;
dashboard chart vào trang hồ sơ;
sidebar chỉ để chứa 3 menu;
tooltip cho mọi label;
modal khi thêm kỹ năng;
modal khi thêm lĩnh vực;
5 màu khác nhau cho M1–M5;
text tiếng Anh không cần thiết như Profile Completeness, Skill Matching, AI Insights.

Đây là hệ thống quản lý đồ án đại học, không phải landing page SaaS.

46. Acceptance Criteria cho PR UI

PR có thể coi là đạt khi:

/ho-so/ không làm thay đổi logic POST hiện tại.
Cả hai Django formset vẫn có management_form.
Field names/backend contract không thay đổi.
Có đủ ba khu vực: Giới thiệu – Kỹ năng – Lĩnh vực quan tâm.
Navbar sinh viên có Hồ sơ năng lực và Đăng ký nguyện vọng.
Desktop không rộng quá khoảng 1120px.
Ở viewport 390px không xuất hiện horizontal scrollbar.
Input/button có chiều cao tối thiểu khoảng 44px.
Validation error vẫn xuất hiện cạnh field tương ứng.
Keyboard focus có trạng thái nhìn thấy rõ.
Text quan trọng đạt tương phản WCAG AA.
Không dùng placeholder thay label.
Không thêm field giả mà backend không có.
Không hard-code điểm/profile completeness nếu backend chưa cung cấp.
M1–M5 ở các màn hình kết quả sau này luôn có tên tiếng Việt + điểm số + mô tả ngắn, không chỉ hiện mã kỹ thuật.
M5 phải được mô tả là đánh giá hỗ trợ từ AI, không phải quyết định cuối cùng.
Giao diện phải dùng tốt bằng touch ở 390px.
Toàn bộ text giao diện là tiếng Việt tự nhiên, thống nhất thuật ngữ.
Kết quả hình ảnh mong muốn

Tổng thể nên tạo cảm giác giống một cổng học thuật hiện đại của trường đại học: nền #F6F8FB, card trắng, chữ xanh đen, primary xanh EAUT/corporate, nhiều khoảng trắng vừa phải, typography rõ ràng và form là trọng tâm. Không cần cố thể hiện “AI” bằng hiệu ứng thị giác; giá trị của AI nên xuất hiện ở cách giải thích kết quả M1–M5 rõ ràng và minh bạch.
