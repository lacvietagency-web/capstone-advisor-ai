# Kế hoạch kiểm thử nghiệm thu — Capstone Advisor AI

Lập ngày 20/10/2026 từ cuộc họp đội AI (Gemini: nghiệp vụ–thuật toán, bảo mật–hiệu năng; ChatGPT: giao diện–người dùng, chuẩn hồ sơ),
Claude tổng hợp và kiểm chứng. Biên bản các đội: `workspace/research/capstone-test-plan-20261020/`.
Mục tiêu: trước buổi bảo vệ có **bằng chứng đo được** cho chương 4.5, theo cấu trúc hồ sơ của ISO/IEC/IEEE 29119-3
(kế hoạch → đặc tả ca → nhật ký thực thi → báo cáo tổng kết).

## 1. Hiện trạng (đo ngày 20/10/2026, commit d15fc51 / ui/v3 1bff0a0)

| Hạng mục | Kết quả |
|---|---|
| Test tự động (Django) | 179/179 đạt, ruff sạch |
| Độ phủ mã (câu lệnh) | **91%** (2.976 câu, 274 chưa chạy). Thấp nhất: `recommend/llm.py` 65% (M5 tắt), `allocate/solver.py` 81%, `recommend/ahp.py` 82% |
| E2E Playwright | 19/19 bước đạt |
| Đã dò lỗi | 3 vòng, 33 lỗi đã sửa (`webby-v3/qa/LOI-DA-SUA.md`) |
| Kịch bản thủ công 84 ca | Đã viết, **chưa có biên bản Đạt/Không đạt** |
| Tải đồng thời, người dùng thật, quét bảo mật tự động | **Chưa làm** |

## 2. Hạng mục theo ưu tiên

P0 = bắt buộc trước bảo vệ · P1 = nên có · P2 = nếu kịp.

| # | Ưu tiên | Hạng mục | Cách làm | Tiêu chí đạt | Bằng chứng |
|---|---|---|---|---|---|
| 1 | P0 | Ma trận phân quyền tự động | Test lặp mọi URL × {khách, SV, GV, Khoa} × {GET, POST}, cả đổi id trên URL (IDOR) | Mọi ô đúng bảng mong đợi; 0 lỗi 500 | Bảng ma trận + log test |
| 2 | P0 | Kiểm thử thuộc tính (Hypothesis) | Bất biến ILP/Greedy: mỗi SV ≤ 1 đề tài, không vượt sức chứa, không vượt chỉ tiêu GV, chỉ xếp vào đề tài SV đủ điều kiện; số SV xếp được ILP ≥ Greedy; AHP: trọng số tổng 1, CR ≥ 0,1 bị từ chối; M1–M3 trong [0, 100] | 0 phản ví dụ sau ≥ 200 lần sinh/bất biến | File test + số lần sinh |
| 3 | P0 | ILP so với nghiệm tối ưu vét cạn | Dữ liệu ngẫu nhiên ≤ 8 SV: so mục tiêu ILP với brute-force | Bằng nhau ở mọi mẫu | Bảng so sánh |
| 4 | P0 | Biên dữ liệu | 0 SV; 1 GV; đề tài sức chứa 0; 100% SV chọn cùng 1 đề tài; 1.000 SV | Không lỗi, kết quả hợp lệ, ILP 1.000 SV < 5 s | Bảng thời gian |
| 5 | P0 | Bảo mật tĩnh và cấu hình | `pip-audit`, `bandit -r`, `manage.py check --deploy` với cấu hình DEBUG=0 | 0 lỗ hổng mức Cao chưa giải trình | 3 báo cáo |
| 6 | P0 | Tệp Excel độc | Thêm gói `defusedxml` (hiện `openpyxl.DEFUSEDXML=False`), thử tệp XML bomb và zip bomb ≤ 5 MB | Từ chối hoặc báo lỗi, không treo, không ghi CSDL | Log + test |
| 7 | P0 | Tải đồng thời (Locust) | 50 và 100 người dùng ảo, kịch bản trộn SV/GV/Khoa | p95 < 2 s trang đọc, < 5 s thao tác nặng; lỗi < 1% | Báo cáo Locust (số đo thật) |
| 8 | P0 | Chạy 84 ca thủ công | Playwright tự động phần chạy được, người làm phần còn lại; mỗi ca ghi Đạt/Không đạt/Chưa kiểm | 100% ca có kết quả; 0 lỗi Nghiêm trọng/Cao còn mở | Biên bản 84 ca |
| 9 | P0 | Ma trận truy vết | UC01–UC23 ↔ mã ca ↔ kết quả | Mỗi use case có ≥ 1 ca đạt | Bảng truy vết |
| 10 | P1 | Khả năng truy cập | axe-core trong Playwright trên mọi trang, Sáng/Tối; bàn phím thủ công | 0 vi phạm mức serious/critical; mọi việc chính làm được bằng bàn phím | Báo cáo axe |
| 11 | P1 | Đa trình duyệt | Chạy lại e2e trên Firefox và WebKit | 19/19 trên cả 3 | Log |
| 12 | P1 | Người dùng thật + SUS | 6 người (2 SV, 2 GV, 2 người đóng vai Khoa), nhiệm vụ theo vai, bảng SUS 10 câu (Brooke) | Ghi tỉ lệ hoàn thành, thời gian, điểm SUS; mốc tham chiếu 68 (không phải ngưỡng bắt buộc) | Phiếu ẩn danh P01–P06 |
| 13 | P1 | Độ phủ nhánh | `coverage run --branch` | Ghi số, giải trình phần M5 tắt | Báo cáo coverage |
| 14 | P2 | OWASP ZAP baseline | Quét động trên bản chạy thử | 0 cảnh báo High | Báo cáo ZAP |
| 15 | P2 | Tối ưu lưu phân công | Đổi vòng `update_or_create` sang `bulk_create/bulk_update` | Thời gian lưu 1.000 SV giảm | Số đo trước/sau |

## 3. Lịch 7 ngày

| Ngày | Việc | Ai làm |
|---|---|---|
| 1 | #1 ma trận phân quyền, #2 Hypothesis, #3 vét cạn | Gemini viết test, Claude đọc và gộp |
| 2 | #5 quét bảo mật, #6 defusedxml + tệp độc, #4 biên dữ liệu | Claude + Gemini |
| 3 | #7 Locust, đo ILP theo quy mô | Claude chạy, Grok soi kết quả |
| 4 | #8 chạy 84 ca, sửa lỗi phát sinh | Đội AI chạy Playwright, Claude sửa lõi |
| 5 | #10 axe, #11 đa trình duyệt, #13 coverage nhánh | Gemini + Claude |
| 6 | #12 người dùng thật + SUS | **Anh** mời 6 người; em chuẩn bị phiếu và kịch bản |
| 7 | #9 truy vết, viết lại mục 4.5, dựng lại .docx, khoá phiên bản | Claude, ChatGPT soát văn |

## 4. Quy tắc trung thực của hồ sơ

- Chỉ ghi số đo thật. Ca chưa chạy ghi "Chưa kiểm chứng", không ghi "Đạt".
- Không tự điền điểm SUS hay số Locust. Bảng mẫu trong biên bản của đội AI là ví dụ, không phải kết quả.
- Không ghi "đạt WCAG 2.2 AA" nếu chỉ có điểm Lighthouse hoặc axe; phải kèm kiểm tra thủ công.
- Lỗi Nghiêm trọng còn mở thì không che bằng tỉ lệ đạt chung.

## 5. Nguồn đã kiểm chứng (DOI tra trên Crossref ngày 20/10/2026)

- Abraham, Irving, Manlove (2007). Two algorithms for the Student-Project Allocation problem. doi:10.1016/j.jda.2006.03.006
- Anwar, Bahaj (2003). Student project allocation using integer programming. IEEE Trans. Education. doi:10.1109/te.2003.811038
- Manlove, Milne, Olaosebikan (2022). Student-project allocation with preferences over projects: algorithmic and experimental results. Discrete Applied Mathematics. doi:10.1016/j.dam.2020.08.015
- Saaty (1977). A scaling method for priorities in hierarchical structures. doi:10.1016/0022-2496(77)90033-5
- MacIver và cộng sự (2019). Hypothesis: A new approach to property-based testing. JOSS. doi:10.21105/joss.01891
- Brooke (1996). SUS: A quick and dirty usability scale. · W3C WCAG 2.2 (Recommendation). · ISO/IEC/IEEE 29119-3:2021. · OWASP ASVS 4.0, OWASP Top 10:2021.

Đội AI đã ghi sai 3 DOI (Anwar & Bahaj, Manlove 2022, Hypothesis); danh sách trên là bản đã sửa.

## 6. Cần quyết trước khi chạy

1. Thêm gói `defusedxml` vào requirements (hạng mục 6).
2. Ai tham gia kiểm thử người dùng thật (hạng mục 12) và lịch ngày 6.
3. Câu hỏi ILP "bắt buộc xếp SV vào đề tài GV đã đồng ý" vẫn chờ ý kiến thầy; kế hoạch giữ mô hình 3 ràng buộc.
4. Gemini (agy) đang bị đăng xuất: cần đăng nhập lại để đội AI viết test.
