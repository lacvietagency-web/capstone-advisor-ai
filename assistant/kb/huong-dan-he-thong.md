# Hướng dẫn và quy trình của hệ thống Capstone AI

Mỗi mục "##" là một đoạn tri thức của trợ lý ảo; {tên_url ...} cuối tiêu đề = trang mở khi bấm nguồn (trang đầu tiên người hỏi vào được). Nội dung lấy đúng theo luật đang chạy trong mã nguồn;
sửa luật trong code thì sửa cả mục tương ứng ở đây.

## Capstone AI là gì, ai dùng {home}
Capstone AI là hệ thống hỗ trợ tư vấn và phân công đề tài đồ án tốt nghiệp. Có 3 vai trò: Sinh viên (khai hồ sơ năng lực, xem gợi ý đề tài, nộp nguyện vọng, xem kết quả), Giảng viên (đăng đề tài, duyệt sinh viên đăng ký), Khoa (nhập dữ liệu, rà soát đề tài trùng, chạy phân công tối ưu, công bố kết quả, xem thống kê). Mỗi người đăng nhập bằng tài khoản Khoa cấp.

## Các bước đăng ký đề tài của sinh viên {home}
Sinh viên đi 4 bước, hiển thị ở "Hành trình" trên Trang chủ: (1) Hồ sơ năng lực: khai kỹ năng, lĩnh vực quan tâm, giới thiệu bản thân; (2) Gợi ý AI: hệ thống tính Top 5 đề tài phù hợp; (3) Nguyện vọng: chọn tối đa 3 đề tài (NV1, NV2, NV3) và nộp chính thức trong hạn của đợt; (4) Kết quả phân công: sau khi Khoa công bố, xem đề tài chính thức và giảng viên hướng dẫn ở mục "Kết quả".

## Hồ sơ năng lực của sinh viên {student_profile}
Mục "Hồ sơ" cho sinh viên khai: kỹ năng với mức 1–5; lĩnh vực quan tâm, chọn tối đa 3 lĩnh vực; phần tự giới thiệu, kinh nghiệm, định hướng nghề nghiệp, tối đa 500 ký tự; email và số điện thoại (10–11 chữ số, bắt đầu bằng 0 hoặc +84). GPA và điểm các môn do Khoa nhập, sinh viên không tự sửa. Mỗi lần sửa hồ sơ, hệ thống tính lại gợi ý đề tài. Chưa khai kỹ năng thì chưa có gợi ý.

## Gợi ý AI chọn Top 5 đề tài như thế nào {topic_list}
Gợi ý chạy hai giai đoạn. Giai đoạn 1 lọc cứng: bỏ đề tài sinh viên chưa đủ điều kiện (GPA tối thiểu, môn tiên quyết, kỹ năng bắt buộc), rồi chấm 3 tiêu chí: M1 kỹ năng (đáp ứng bao nhiêu phần kỹ năng đề tài cần, theo trọng số từng kỹ năng), M3 lĩnh vực (mức quan tâm của sinh viên với lĩnh vực của đề tài), M4 độ gần nghĩa (mô hình Sentence-BERT so phần tự giới thiệu với mô tả đề tài). Giai đoạn 2: 15 đề tài điểm cao nhất được mô hình ngôn ngữ chấm thêm M5 theo rubric 100 điểm (khả thi 35, định hướng nghề 30, tính chất đề tài 20, động lực 15). Điểm cuối là tổng có trọng số theo phương pháp AHP: kỹ năng 42,4%, gần nghĩa 22,7%, LLM 22,7%, lĩnh vực 12,2%. Khi mô hình ngôn ngữ lỗi, trọng số được chia lại cho M1, M3, M4. Gợi ý chỉ để tham khảo, sinh viên tự quyết nguyện vọng.

## Điều kiện để được đăng ký một đề tài {topic_list}
Một đề tài có thể đặt 3 loại điều kiện bắt buộc: GPA tối thiểu (thang 4), môn tiên quyết với điểm tối thiểu, và kỹ năng bắt buộc với mức yêu cầu. Thiếu bất kỳ điều kiện nào thì không chọn đề tài đó làm nguyện vọng được; trang chi tiết đề tài ghi rõ điều kiện nào đạt, điều kiện nào còn thiếu. Trang đề tài cũng hiện số chỗ còn lại: đề tài hết chỗ khi giảng viên đã đồng ý đủ số sinh viên tối đa, lúc đó nên chọn thêm nguyện vọng khác.

## Nộp, sửa và rút nguyện vọng {student_preferences}
Ở mục "Nguyện vọng", sinh viên chọn tối đa 3 đề tài NV1–NV3 (bắt buộc có NV1), không được trùng nhau, danh sách chỉ hiện đề tài sinh viên đủ điều kiện. Có hai cách lưu: "Lưu nháp" (chỉ sinh viên thấy; giảng viên, thống kê và thuật toán phân công không thấy) và "Nộp nguyện vọng" (nộp chính thức). Đã nộp mà muốn sửa thì bấm "Rút về nháp để sửa", sửa xong nhớ nộp lại trước hạn. Chỉ nộp, sửa, rút được khi đợt đăng ký đang mở và chưa quá hạn chót; quá hạn chót thì chỉ xem. Đề tài giảng viên đã duyệt vẫn giữ nguyên trạng thái khi sinh viên sửa các nguyện vọng khác.

## Đợt đăng ký và hạn chót {home}
Mỗi đợt đăng ký có ngày bắt đầu, hạn chót và trạng thái: Đang mở đăng ký, Đã đóng đăng ký, Đã chạy phân công (nháp), Đã công bố. Thẻ đợt trên Trang chủ hiện số ngày còn lại. Quá hạn chót thì coi như đã đóng dù Khoa chưa đổi trạng thái.

## Giảng viên duyệt sinh viên đăng ký {lecturer_topics}
Ở mục "Đề tài" → "Đăng ký" của từng đề tài, giảng viên xem sinh viên đã nộp nguyện vọng và chọn Đồng ý hoặc Từ chối. Từ chối bắt buộc ghi lý do; có thể ghi nhận xét, sinh viên xem được sau khi duyệt. Hệ thống chặn: duyệt nguyện vọng còn là bản nháp; đồng ý quá số sinh viên tối đa của đề tài; đồng ý quá chỉ tiêu hướng dẫn của giảng viên trong đợt; đổi trạng thái sau khi Khoa đã công bố kết quả.

## Phân công tối ưu và công bố kết quả {allocation_dashboard student_allocation_result}
Sau khi đóng đăng ký, Khoa chạy phân công ở mục "Phân công". Thuật toán quy hoạch tuyến tính nguyên (ILP) xếp mỗi sinh viên tối đa 1 đề tài, không vượt số sinh viên tối đa của đề tài và chỉ tiêu của giảng viên. Mục tiêu: xếp được nhiều sinh viên nhất, rồi ưu tiên điểm phù hợp cao và nguyện vọng cao (NV1 hơn NV2, NV3). Nguyện vọng bị giảng viên từ chối hoặc không đủ điều kiện bị loại trước khi xếp. Sinh viên chưa được xếp thì Khoa xếp tay ở pha 2, hệ thống gợi ý các đề tài còn chỗ mà sinh viên đủ điều kiện. Khoa bấm "Công bố" thì sinh viên mới thấy kết quả; sau công bố, kết quả chỉ đọc.

## Xem kết quả phân công {student_allocation_result}
Sau khi Khoa công bố, sinh viên vào mục "Kết quả" để xem đề tài chính thức, giảng viên hướng dẫn, nguyện vọng đã đạt (NV1, NV2 hay NV3) và điểm phù hợp. Trước khi công bố, mục này ghi "Khoa đang xử lý" hoặc "Chưa có kết quả".

## Giảng viên đăng và sửa đề tài {lecturer_topic_new}
Ở mục "Đề tài" → "Thêm đề tài", giảng viên nhập: tên, mô tả, mục tiêu, công nghệ gợi ý, lĩnh vực, độ khó (Dễ, Trung bình, Khó), GPA tối thiểu, số sinh viên tối đa, kỹ năng yêu cầu (mức 1–5, trọng số, có bắt buộc hay không), môn tiên quyết và ghi chú xét duyệt. Mã đề tài dạng DT-năm-số được tạo tự động. Mỗi lần sửa đề tài, gợi ý của sinh viên được tính lại.

## Kiểm tra đề tài trùng và đề tài khoá trước {faculty_duplicates lecturer_topics}
Khi giảng viên soạn hoặc sửa đề tài, hệ thống đo độ giống bằng Sentence-BERT. Giống từ 70% trở lên với đề tài đang mở khác thì cảnh báo trùng và gợi ý cách làm cho khác. Giống từ 62,5% trở lên với đề tài khoá trước thì tư vấn điểm cải tiến, ưu tiên các hướng phát triển mà chính khoá trước đã đề xuất. Hai ngưỡng được hiệu chỉnh trên kho 449 đồ án thật của các khoá trước. Hệ thống chỉ cảnh báo, không tự chặn; giảng viên và Khoa quyết định. Khoa xem toàn bộ cặp trùng ở mục "Rà soát trùng lặp".

## Việc của Khoa trong hệ thống {home}
Khoa: nhập danh sách sinh viên, giảng viên, đề tài, điểm bằng Excel theo 2 bước (kiểm tra lỗi trước, xác nhận mới ghi; có lỗi thì không ghi dòng nào); rà soát đề tài trùng toàn khoa; chạy phân công tối ưu và xếp tay sinh viên chưa được xếp; công bố kết quả; xem thống kê đăng ký, tải giảng viên, so sánh thuật toán.

## Tài khoản và mật khẩu {password_change}
Đổi mật khẩu ở menu tài khoản (góc trên bên phải) → "Đổi mật khẩu". Hệ thống chưa có chức năng tự lấy lại mật khẩu; quên mật khẩu thì liên hệ Khoa để được cấp lại.

## Quy chế chính thức của trường
Hệ thống chưa nạp văn bản quy chế đào tạo và quy định đồ án tốt nghiệp chính thức của trường. Các câu hỏi về thang điểm, hội đồng bảo vệ, định dạng quyển báo cáo, thời lượng, học phí, điều kiện được làm đồ án theo quy chế thì trợ lý chưa có căn cứ để trả lời: hãy liên hệ giáo vụ Khoa hoặc giảng viên hướng dẫn. Khi Khoa cung cấp văn bản, trợ lý sẽ trả lời kèm trích dẫn điều, khoản.

## Xem Top 5 đề tài gợi ý ở đâu {home}
Top 5 đề tài AI gợi ý hiện ở Trang chủ, khối "Đề tài phù hợp nhất" (kèm điểm phù hợp và điểm từng tiêu chí M1, M3, M4, M5). Trang "Nguyện vọng" cũng hiện Top 5 để chọn nhanh. Ở mục "Đề tài" xem được mọi đề tài kèm điểm phù hợp với mình, sắp xếp được theo điểm phù hợp. Muốn gợi ý sát hơn thì cập nhật kỹ năng, lĩnh vực quan tâm và phần tự giới thiệu ở mục "Hồ sơ".

## Được giảng viên đồng ý một nguyện vọng thì các nguyện vọng khác thế nào {student_preferences}
Khi giảng viên đồng ý một nguyện vọng, các nguyện vọng còn lại không tự huỷ. Lúc Khoa chạy phân công, thuật toán xét mọi nguyện vọng đã nộp chính thức và chưa bị từ chối, rồi xếp mỗi sinh viên vào tối đa 1 đề tài. Kết quả cuối cùng là kết quả Khoa công bố ở mục "Kết quả".

## Đăng ký theo nhóm, nhiều sinh viên cùng một đề tài {student_preferences}
Hệ thống không có đăng ký theo nhóm: mỗi sinh viên tự nộp nguyện vọng của mình. Đề tài có số sinh viên tối đa lớn hơn 1 thì nhiều sinh viên cùng chọn được, giảng viên duyệt từng người. Muốn làm chung với bạn thì mỗi người nộp cùng đề tài đó và hỏi ý giảng viên ra đề.

## Không thấy nút nộp nguyện vọng {student_preferences}
Các lý do thường gặp: đợt đăng ký chưa mở hoặc đã quá hạn chót (lúc đó trang Nguyện vọng chỉ cho xem); đã nộp rồi (nút đổi thành "Rút về nháp để sửa"); chưa chọn NV1 (NV1 bắt buộc); đề tài muốn chọn không có trong danh sách vì chưa đủ điều kiện (xem trang chi tiết đề tài để biết thiếu gì). Vẫn lỗi thì liên hệ Khoa.

## Chỉ tiêu hướng dẫn và số đề tài của giảng viên {lecturer_profile}
Hệ thống không giới hạn số đề tài một giảng viên được đăng. Giới hạn là chỉ tiêu hướng dẫn: số sinh viên tối đa giảng viên nhận trong một đợt (mặc định 5). Giảng viên tự sửa chỉ tiêu ở mục "Hồ sơ" khi đợt đang mở; đợt đã đóng thì chỉ tiêu bị khoá, chỉ Khoa điều chỉnh được. Hệ thống chặn giảng viên đồng ý vượt chỉ tiêu.

## Hạn duyệt sinh viên của giảng viên {lecturer_topics}
Giảng viên duyệt (đồng ý, từ chối) được tới khi Khoa công bố kết quả phân công; sau công bố thì không đổi được. Nên duyệt trước khi Khoa chạy phân công, vì thuật toán chỉ loại những nguyện vọng đã bị từ chối tại thời điểm chạy.

## Cấu hình trước khi chạy phân công {allocation_dashboard}
Thuật toán phân công không cần chỉnh tham số. Những gì ảnh hưởng kết quả: số sinh viên tối đa của từng đề tài (giảng viên đặt khi đăng đề tài), chỉ tiêu hướng dẫn của từng giảng viên (ở hồ sơ giảng viên), và trọng số tính điểm phù hợp theo AHP (quản trị hệ thống đặt ở trang Quản trị → Bộ trọng số).

## Công bố kết quả làm gì {allocation_dashboard student_allocation_result}
Bấm "Công bố" sẽ chuyển toàn bộ kết quả phân công nháp thành chính thức, chuyển đợt sang trạng thái "Đã công bố" và khoá chỉnh sửa (không đổi duyệt, không xếp lại). Sinh viên xem kết quả ở mục "Kết quả". Hiện hệ thống chưa gửi email hay thông báo tự động; Khoa thông báo cho sinh viên theo kênh thường dùng.

## Mẫu Excel để nhập dữ liệu {faculty_import}
Ở trang "Nhập Excel" của Khoa có nút "Tải tệp mẫu (.xlsx)". Tệp mẫu có 4 sheet: SinhVien (Mã sinh viên, Họ đệm, Tên, GPA, Email, Chuyên ngành, Ghi chú), GiangVien (Mã giảng viên, Họ đệm, Tên, Email, Bộ môn, Chỉ tiêu, Lĩnh vực), DeTai (Tên đề tài, Mã giảng viên, Mô tả, Lĩnh vực, Độ khó, GPA tối thiểu, Số lượng) và KyNang. Nhập theo 2 bước: kiểm tra lỗi, rồi xác nhận mới ghi; có lỗi ở bất kỳ dòng nào thì không ghi dòng nào.
