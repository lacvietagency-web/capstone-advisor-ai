# Kịch bản kiểm thử toàn hệ thống — Capstone Advisor AI

Phạm vi: toàn bộ giao diện (frontend) và nghiệp vụ, dữ liệu, phân quyền (backend) của ba vai trò Sinh viên, Giảng viên, Khoa.
Mỗi ca ghi **Mã · Vai · Thao tác · Kết quả mong đợi**. Ca nào sai so với "Kết quả mong đợi" là lỗi; ghi lại kèm bước tái hiện,
đường dẫn, tài khoản và ảnh chụp (nếu là lỗi giao diện).

## 0. Môi trường

| Mục | Giá trị |
|---|---|
| Dữ liệu | `python manage.py seed_demo` — 100 SV (`sv001`…`sv100`), 15 GV (`gv001`…`gv015`), `khoa01`; mật khẩu `123456`; 50 đề tài; 1 đợt đang mở |
| Trạng thái đợt | Kiểm hai bộ dữ liệu: đợt **đang mở** (mặc định sau seed) và đợt **đã công bố** (Khoa: chạy ILP → Chốt & công bố) |
| Trình duyệt | Chrome mới nhất; bề rộng 1440, 768, 390 px; chế độ Sáng và Tối |
| Tắt AI nặng khi chạy máy yếu | `RECOMMEND_SEMANTIC=0 RECOMMEND_LLM=0` (M4/M5 hiện "Chưa đánh giá" là đúng) |
| Kiểm tự động có sẵn | `python manage.py test` (156 ca) · `ruff check .` |

Quy ước chung (áp dụng cho MỌI trang, vi phạm ở đâu ghi lỗi ở đó):
- **G1** Không lỗi 500, không lỗi JavaScript trên console, không gọi mạng lỗi (404 tài nguyên tĩnh).
- **G2** Không tràn ngang ở 390/768/1440 px; chữ không chồng, không bị cắt, không dính sát viền khối.
- **G3** Tiếng Việt đủ dấu; không chữ nhỏ hơn 12 px; chế độ Tối đọc rõ (không chữ tối trên nền tối).
- **G4** Mọi biểu mẫu POST có CSRF; bấm nút gửi hai lần nhanh không tạo bản ghi trùng.
- **G5** Mọi nút/liên kết hiển thị đều có chức năng thật (không `href="#"`, không nút "chết").
- **G6** Số liệu trên giao diện khớp CSDL (đếm, điểm, trạng thái).

## 1. Tài khoản và phân quyền

| Mã | Vai | Thao tác | Kết quả mong đợi |
|---|---|---|---|
| A01 | Khách | Mở `/trang-chu/`, `/ho-so/`, `/khoa/phan-cong/` khi chưa đăng nhập | Chuyển về `/dang-nhap/?next=…`; đăng nhập xong quay lại đúng trang |
| A02 | Khách | Đăng nhập sai mật khẩu; sai tên đăng nhập; để trống | Báo "Thông tin đăng nhập không chính xác…", không lộ tài khoản có tồn tại hay không; tên đăng nhập vẫn giữ trong ô |
| A03 | Khách | Bấm "Sử dụng" ở 3 tài khoản demo | Điền đúng `sv001`/`gv001`/`khoa01` vào ô tên, con trỏ sang ô mật khẩu; KHÔNG tự đăng nhập |
| A04 | Khách | Nút mắt ở ô mật khẩu | Hiện/ẩn mật khẩu, giữ nguyên giá trị, dùng được bằng bàn phím |
| A05 | SV/GV/Khoa | Đăng nhập đúng | Về trang chủ đúng vai (SV: hành trình + gợi ý; GV: tổng quan đề tài; Khoa: bảng điều khiển) |
| A06 | Mọi vai | Đổi mật khẩu: sai mật khẩu cũ; mật khẩu mới yếu (toàn số, < 8 ký tự, giống tên); hai ô không khớp; hợp lệ | 3 trường hợp đầu báo lỗi đúng ô; hợp lệ → trang "đã đổi", vẫn đăng nhập, mật khẩu cũ hết dùng được |
| A07 | Mọi vai | Đăng xuất | Hết phiên; bấm "Quay lại" trình duyệt không xem được trang cần đăng nhập |
| A08 | SV | Mở trực tiếp URL của GV/Khoa: `/de-tai/`, `/de-tai/them/`, `/de-tai/<id>/dang-ky/`, `/khoa/phan-cong/`, `/khoa/nhap-excel/`, `/khoa/thong-ke/`, `/ho-so-giang-vien/` | 403 hoặc chuyển hướng, không lộ dữ liệu |
| A09 | GV | Mở URL của SV và Khoa: `/ho-so/`, `/nguyen-vong/`, `/ket-qua/`, `/khoa/*` | 403/chuyển hướng |
| A10 | GV | Sửa/xem đăng ký đề tài của GV KHÁC: `/de-tai/<id của GV khác>/sua/`, `/de-tai/<id>/dang-ky/`; POST duyệt nguyện vọng của đề tài GV khác | 403/404; CSDL không đổi |
| A11 | Khoa | Mở trang SV/GV (`/ho-so/`, `/nguyen-vong/`, `/de-tai/`) | Báo thiếu hồ sơ hoặc 403 rõ ràng, không lỗi 500 |
| A12 | Mọi vai | URL không tồn tại `/abc/`, đề tài không tồn tại `/danh-sach-de-tai/999999/` | Trang 404 tiếng Việt, có nút về trang chủ |
| A13 | SV | Xem chi tiết đề tài đang ở trạng thái nháp; đề tài đã đóng | Nháp → 404. Đã đóng → xem được (SV cần mở lại đề tài được phân sau khi đợt đóng), không có nút đăng ký |
| A14 | Mọi vai | Menu tài khoản → Giao diện Sáng / Tối / Theo hệ thống → tải lại trang | Giữ lựa chọn; mọi trang đổi theo |

## 2. Sinh viên

| Mã | Thao tác | Kết quả mong đợi |
|---|---|---|
| S01 | Trang chủ | Hành trình 4 bước đúng trạng thái theo dữ liệu (hồ sơ / gợi ý / nguyện vọng / kết quả); thẻ đợt có "còn N ngày" khi đang mở; đề tài #1 có điểm + M1–M5 + lý do; #2–#5 dạng hàng gọn |
| S02 | Trang chủ của SV chưa có kỹ năng (xoá hết kỹ năng ở Hồ sơ) | Hiện khối "hồ sơ chưa hoàn tất" chỉ rõ mục còn thiếu, không có gợi ý rỗng/điểm 0 |
| S03 | Hồ sơ: sửa Email, Số điện thoại → Lưu hồ sơ | Lưu đúng; Họ tên, MSSV, Ngành, GPA chỉ đọc (sửa bằng công cụ trình duyệt rồi gửi cũng không đổi CSDL) |
| S04 | Hồ sơ: email sai định dạng; SĐT `12ab`, `0912 345 678`, `+84912345678` | Hai trường hợp đầu báo lỗi đúng ô; SĐT có dấu cách được chấp nhận và lưu dạng liền `0912345678` |
| S05 | Hồ sơ: thêm kỹ năng mới, đổi mức 1–5, xoá kỹ năng, chọn trùng một kỹ năng hai lần | Thêm/sửa/xoá đúng; trùng kỹ năng bị chặn kèm thông báo |
| S06 | Hồ sơ: tick 4 lĩnh vực quan tâm | Bị chặn "Chọn tối đa 3 lĩnh vực", không lưu gì |
| S07 | Hồ sơ: bỏ tick một lĩnh vực cũ, tick một lĩnh vực mới (≤ 3) | Lĩnh vực cũ giữ mức cũ, lĩnh vực mới mức 3; gợi ý được tính lại (điểm M3 đổi theo) |
| S08 | Hồ sơ: giới thiệu 500 ký tự; 501 ký tự (gửi thẳng); chèn `<script>alert(1)</script>` | 500 lưu được, bộ đếm đúng; 501 bị chặn ở cả giao diện và máy chủ; chuỗi script hiển thị dạng chữ (không chạy) |
| S09 | Danh sách đề tài: tab "Đủ điều kiện" / "Chưa đủ điều kiện" | Số đếm trên tab = số dòng; đề tài chưa đủ ghi rõ "cần …, bạn có …" / "bạn chưa có điểm"; nút Đăng ký bị khoá với đề tài chưa đủ |
| S10 | Danh sách: lọc lĩnh vực, giảng viên, độ khó, từ khoá; sắp xếp theo điểm/tên/độ khó/sức chứa/NV1; sang trang 2 | Kết quả đúng; bộ lọc giữ khi chuyển trang; không tìm thấy → minh hoạ "không tìm thấy" + nút Xoá bộ lọc |
| S11 | Từ khoá có dấu, có ký tự đặc biệt `%`, `'`, `"` | Không lỗi 500; tìm có dấu đúng |
| S12 | Chi tiết đề tài | Mã đề tài, GVHD + bộ môn, lĩnh vực, độ khó, chỉ tiêu "x/y — còn z chỗ", thẻ công nghệ, mô tả + mục tiêu, bảng kỹ năng (mức, trọng số dạng 0,xx, bắt buộc), điều kiện tiên quyết, điểm + M1–M5 có trọng số AHP, lý do đánh số, Kiểm tra điều kiện 4 mục |
| S13 | Chi tiết đề tài chưa đủ điều kiện | Không có nút "Đăng ký nguyện vọng"; khối Kiểm tra điều kiện có mục "fail" giải thích lý do |
| S14 | Nguyện vọng: chọn NV1–NV3 khác nhau → Lưu nháp | Báo "Đã lưu nháp…"; GV chưa thấy SV trong danh sách đăng ký; Khoa chạy phân công không tính bản nháp |
| S15 | Nguyện vọng: Nộp nguyện vọng | Báo "Đã lưu nguyện vọng và nộp chính thức"; trang ghi "Đã nộp lúc …"; GV thấy SV |
| S16 | Nguyện vọng: chọn trùng một đề tài ở 2 NV | Bị chặn, báo lỗi; không lưu |
| S17 | Nguyện vọng: Rút về nháp để sửa (khi đợt mở) | Trạng thái về nháp, ghi nhật ký; đề tài GV đã xét giữ trạng thái + nhận xét khi nộp lại |
| S18 | Bấm "Thêm vào nguyện vọng"/"Đăng ký" khi đã đủ 3 NV | Thông báo đã đủ 3 NV, gợi ý thay một ô; không mất NV cũ |
| S19 | Nguyện vọng khi đợt đã đóng/công bố | Chỉ xem; không còn nút lưu/nộp/rút; POST thẳng bị từ chối |
| S20 | Nguyện vọng: GV đã từ chối/đồng ý kèm nhận xét | SV thấy trạng thái, lý do từ chối, "Nhận xét của giảng viên" |
| S21 | Kết quả khi đợt đang mở / chưa có đợt / đã đóng chưa công bố | Câu trạng thái đúng từng trường hợp; KHÔNG lộ kết quả nháp |
| S22 | Kết quả khi đã công bố, SV được xếp | Đề tài, GVHD, NV đạt, nguồn phân công, điểm + M1–M5, thời điểm công bố, bảng NV đã nộp (Đạt/Không đạt), nút Xem chi tiết đề tài, nút In/Tải biên bản (hộp in của trình duyệt) |
| S23 | Kết quả khi đã công bố, SV không được xếp | Thông báo chưa được phân công, hướng dẫn liên hệ Khoa (pha 2) |
| S24 | SV sửa `?period_id=` trên URL kết quả sang đợt khác/không tồn tại | Không lỗi 500; không xem được kết quả nháp |

## 3. Giảng viên

| Mã | Thao tác | Kết quả mong đợi |
|---|---|---|
| L01 | Tổng quan | 4 số liệu (đề tài, SV đăng ký, chờ duyệt, đã đồng ý) khớp CSDL (chỉ tính NV đã nộp); bảng SV chờ duyệt có tên SV, MSSV, điểm AI, NV |
| L02 | Tổng quan: tìm theo MSSV / tên SV / tên đề tài; lọc Chờ duyệt / Đồng ý / Từ chối / Tất cả | Kết quả đúng; tối đa 10 dòng; giữ giá trị ô lọc sau khi tải lại |
| L03 | Tổng quan: bấm "Phân tích" của một SV | Mở trang đăng ký của đề tài đó và TỰ MỞ ngăn kéo đúng SV |
| L04 | Đề tài của tôi | Chỉ đề tài của mình; tìm kiếm + lọc trạng thái; số SV đăng ký đúng |
| L05 | Thêm đề tài: bỏ trống tên; sức chứa 0/âm; điểm sàn GPA > 4; kỹ năng trùng; môn tiên quyết trùng | Báo lỗi đúng ô, không lưu |
| L06 | Thêm đề tài hợp lệ (mục tiêu, công nghệ, ghi chú xét duyệt, kỹ năng, môn tiên quyết) | Lưu; mã `DT-<năm>-<số>` tự sinh, không sửa được; đề tài hiện với SV |
| L07 | Sửa mô tả đề tài | Phiên bản đề tài tăng (gợi ý được tính lại); các trường khác giữ nguyên |
| L08 | Duyệt SV: lọc trạng thái, tìm MSSV | Đúng; mặc định chỉ hiện "Chờ duyệt" |
| L09 | Mở ngăn kéo Phân tích | Điểm + M1–M5 + AHP, Kiểm tra điều kiện 4 mục, giới thiệu bản thân, ô Nhận xét giảng viên; trên 390 px ngăn kéo toàn màn, không tràn |
| L10 | Đồng ý kèm nhận xét | Trạng thái Đồng ý; nhận xét lưu (≤ 1000 ký tự); SV thấy nhận xét; ghi nhật ký |
| L11 | Từ chối: lý do < 5 ký tự; lý do hợp lệ | Lý do ngắn bị chặn; hợp lệ → trạng thái Từ chối, thông báo có lý do; NV bị từ chối không vào bài toán phân công |
| L12 | Hồ sơ giảng viên: sửa học hàm, bộ môn, SĐT, giới thiệu, từ khoá, lĩnh vực, chỉ tiêu | Lưu đúng; SĐT không xuất hiện ở bất kỳ trang nào của SV; khi đợt đã đóng thì chỉ tiêu bị khoá |
| L13 | Thống kê trong hồ sơ GV | Số đề tài, số SV hướng dẫn, phân bố theo lĩnh vực khớp CSDL |

## 4. Khoa

| Mã | Thao tác | Kết quả mong đợi |
|---|---|---|
| K01 | Bảng điều khiển | 5 số liệu (SV, đề tài, đợt, SV có NV, GV) khớp CSDL; bảng đợt; 4 lối tắt đi đúng trang |
| K02 | Nhập Excel: tải tệp mẫu `mau.xlsx` | Tải được, mở bằng Excel, đúng các sheet/cột |
| K03 | Nhập Excel: tệp không phải .xlsx; .xlsx hỏng; .xlsx thiếu cột; dòng sai kiểu dữ liệu | Báo lỗi rõ theo số dòng; KHÔNG ghi gì vào CSDL |
| K04 | Nhập Excel hợp lệ: "Tải lên & kiểm tra" | Hiện số bản ghi sẽ tạo; CSDL CHƯA đổi |
| K05 | Bấm "Xác nhận nhập" | Ghi đúng số bản ghi đã báo; bấm lại lần hai không nhân đôi |
| K06 | Phân công (đợt đang mở/đã đóng): Chạy tối ưu ILP; Chạy Greedy | Bảng + số liệu (đã xếp %, NV1 %, Top 3, điểm TB, chờ pha 2) cập nhật; biểu đồ vẽ được |
| K07 | Kiểm tra ràng buộc ILP trên kết quả | Mỗi SV tối đa 1 đề tài; số SV mỗi đề tài ≤ sức chứa; số SV mỗi GV ≤ chỉ tiêu; không xếp vào NV bị từ chối |
| K08 | Bộ lọc bảng: trạng thái, NV, GV, lĩnh vực, khoảng điểm, từ khoá, sắp xếp, số dòng/trang; sang trang | Kết quả đúng; bộ lọc giữ khi phân trang |
| K09 | Xem chi tiết SV chưa xếp → Xếp tay vào đề tài còn chỗ → Lưu | Cập nhật, nguồn "Khoa xếp"; thông báo thành công |
| K10 | Chốt & công bố: nút xác nhận khi chưa gõ / gõ sai / gõ đúng "CÔNG BỐ" | Khoá đến khi gõ đúng; sau đó đợt "Đã công bố", SV xem được kết quả |
| K11 | Đợt đã công bố: thử Chạy ILP / Greedy / Xếp tay (cả bằng POST trực tiếp) | Bị từ chối "đã công bố — kết quả chính thức không được thay đổi"; kết quả chính thức không đổi; giao diện không còn các nút đó |
| K12 | Công bố lần hai; công bố khi chưa chạy phân công | Bị từ chối kèm thông báo |
| K13 | Thống kê | Các biểu đồ vẽ được, đổi màu theo Sáng/Tối, dưới mỗi biểu đồ có bảng số liệu khớp |
| K14 | Trang quản trị `/quan-tri/` | Chỉ Khoa/siêu người dùng vào được |

## 5. Thuật toán và dữ liệu (backend)

| Mã | Kiểm | Kết quả mong đợi |
|---|---|---|
| B01 | Lọc cứng | Đề tài có điểm sàn GPA > GPA SV, thiếu môn tiên quyết, thiếu kỹ năng bắt buộc → không vào Top 5, nằm ở tab "Chưa đủ" |
| B02 | M1 kỹ năng | = 100·Σ wₖ·min(mức SV/mức yêu cầu, 1)/Σ wₖ; đề tài không yêu cầu kỹ năng → 100 |
| B03 | M3 lĩnh vực | = 100·trung bình (mức quan tâm/3) trên các lĩnh vực của đề tài |
| B04 | Điểm tổng | Tổng có trọng số AHP của các thành phần đã có điểm, chia lại trọng số khi M4/M5 chưa có; trong [0, 100] |
| B05 | AHP | Ma trận 5×5 → vector trọng số tổng = 1; CR ≥ 0,1 bị từ chối; chỉ 1 bộ đang dùng |
| B06 | Lưu hồ sơ | `profile_version` tăng; gợi ý cũ bị xoá và tính lại |
| B07 | Chỗ còn lại | = sức chứa − số NV đã nộp được đồng ý; không âm |
| B08 | Mã đề tài | Duy nhất, dạng `DT-YYYY-NNN`, đề tài cũ đã được điền mã |
| B09 | Giao dịch | Lỗi giữa chừng khi phân công / nhập Excel → CSDL không bị ghi dở |
| B10 | Nhật ký | Duyệt/từ chối, nộp/rút NV, chạy phân công, công bố, sửa hồ sơ đều có dòng AuditLog đúng người, đúng thực thể |
| B11 | Hiệu năng | Mỗi trang chính trả về < 1 giây với dữ liệu demo (không tính lần đầu tải mô hình M4); không truy vấn lặp N+1 rõ rệt |
| B12 | Lệnh quản trị | `seed_demo`, `ahp_weights`, `allocate_period` chạy được; `allocate_period` với đợt đã công bố báo lỗi rõ, không ghi đè |

## 6. Giao diện và khả năng truy cập

| Mã | Kiểm | Kết quả mong đợi |
|---|---|---|
| U01 | Mọi trang ở 390/768/1440 px, Sáng/Tối | Đạt G1–G3 |
| U02 | Điện thoại 390 px | Thanh điều hướng đáy; trang Nguyện vọng khi đang sửa thì thanh Lưu/Nộp thay thanh đáy (không chồng hai thanh); bảng lớn chuyển thành thẻ |
| U03 | Bàn phím | Tab đi hết các nút/ô theo thứ tự hợp lý, có viền focus rõ; Esc đóng ngăn kéo/hộp thoại |
| U04 | Nhãn | Mọi ô nhập có nhãn; nút chỉ có icon có `aria-label` |
| U05 | Trạng thái rỗng | Đề tài chưa có SV đăng ký, SV chưa có NV, chưa có đợt… đều có minh hoạ + câu nói đúng lý do |
| U06 | Không có Internet (`ASSETS_FROM_CDN=0` hoặc chặn CDN) | Giao diện vẫn đủ kiểu, biểu đồ vẫn vẽ (dùng bản lưu sẵn) |
| U07 | Trang lỗi 403/404/500 | Đúng bố cục, tiếng Việt, có đường quay về |

## 7. Ghi nhận lỗi

Mỗi lỗi một mục: **Mã ca · Mức (Nghiêm trọng / Cao / Trung bình / Thấp) · Vai + tài khoản · URL · Bước tái hiện · Kết quả thực tế · Kết quả mong đợi ·
Ảnh/nhật ký**. Nghiêm trọng = mất/sai dữ liệu, lộ dữ liệu, vượt quyền, lỗi 500 ở luồng chính.
