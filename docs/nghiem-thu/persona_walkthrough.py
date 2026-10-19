"""Nghiệm thu P1 #12 (thay thế có ghi rõ hạn chế) — ĐÁNH GIÁ KHẢ DỤNG THEO KỊCH BẢN DO AI ĐÓNG VAI.

KHÔNG phải khảo sát người dùng thật. Cách làm:
 1. Playwright làm THẬT từng nhiệm vụ của 6 nhân vật trên bản sao CSDL demo → nhiệm vụ có hoàn thành không, bao nhiêu
    thao tác, ảnh chụp từng bước;
 2. ghép ảnh mỗi nhân vật thành 1 tấm, ChatGPT đóng vai nhân vật đó: chấm độ khó từng nhiệm vụ, chỉ chỗ khó hiểu theo
    10 nguyên tắc Nielsen, trả lời 10 câu SUS (Brooke 1996) — điểm SUS ghi là "mô phỏng".

  python docs/nghiem-thu/persona_walkthrough.py <thư mục kết quả>
"""

import json
import re
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
import browser_checks as bc  # noqa: E402  (dùng chung máy chủ thử + đăng nhập)

sys.path.insert(0, "/opt/lucifer-agent/runtime/demo_kit")
import pipeline as P  # noqa: E402  (cầu nối ChatGPT của Hermes)

OUT = Path(sys.argv[1]).resolve()
bc.OUT = OUT
OUT.mkdir(parents=True, exist_ok=True)

PERSONAS = [
    ("sv-gioi", "sv001", "Minh, SV năm 4 ngành CNTT, dùng máy tính thành thạo, muốn chọn nhanh đề tài AI phù hợp",
     ["Xem 5 đề tài được gợi ý trên trang chủ", "Mở chi tiết đề tài gợi ý số 1", "Đăng ký đề tài đó làm NV1 rồi nộp"]),
    ("sv-it-ranh", "sv002", "Lan, SV năm 4, ít dùng web ngoài Facebook, lo sợ bấm nhầm, đọc chậm",
     ["Cập nhật số điện thoại trong Hồ sơ", "Tìm đề tài có chữ 'web' trong danh sách", "Xem trang Kết quả phân công"]),
    ("gv-tre", "gv001", "Anh Tuấn, GV trẻ, quen công nghệ, muốn duyệt nhanh SV đăng ký",
     ["Xem SV đang chờ duyệt trên trang chủ", "Mở trang duyệt đăng ký của một đề tài", "Thêm một đề tài mới"]),
    ("gv-lon-tuoi", "gv002", "Cô Hạnh, GV 58 tuổi, ít dùng web, cần chữ to rõ, sợ thao tác sai",
     ["Xem đề tài của mình", "Sửa giới thiệu trong hồ sơ giảng viên"]),
    ("giao-vu", "khoa01", "Chị Hoa, giáo vụ Khoa, làm việc với Excel hằng ngày, cần chạy phân công đúng quy trình",
     ["Tải tệp Excel mẫu", "Chạy phân công tối ưu ILP", "Xem bảng kết quả phân công"]),
    ("truong-khoa", "khoa01", "Thầy Bình, trưởng khoa, chỉ xem số liệu tổng hợp để ra quyết định",
     ["Xem bảng điều khiển Khoa", "Xem trang Thống kê và biểu đồ so sánh ILP/Greedy"]),
]


def shot(p, name, i, label, shots):
    path = OUT / f"{name}-{i:02d}.png"
    p.screenshot(path=str(path), full_page=False)
    shots.append((label, path))


def do_tasks(p, base, name, user, shots, log):
    """Thực hiện thật; mỗi bước ghi (nhiệm vụ, hoàn thành?, số thao tác)."""
    def step(task, fn, clicks):
        try:
            fn()
            log.append({"nhiem_vu": task, "hoan_thanh": True, "thao_tac": clicks})
        except Exception as e:  # nhiệm vụ không làm được = phát hiện quan trọng, ghi lại, không che
            log.append({"nhiem_vu": task, "hoan_thanh": False, "loi": str(e).splitlines()[0][:150]})
        shot(p, name, len(shots) + 1, task, shots)

    bc.login(p, base, user)
    if name == "sv-gioi":
        step("Xem gợi ý", lambda: p.wait_for_selector("text=/gợi ý|Gợi ý/"), 1)
        def open_top1():
            link = p.locator("a[href*='/danh-sach-de-tai/']").first
            link.click()
            p.wait_for_url(re.compile(r".*/danh-sach-de-tai/\d+/"))
        step("Mở chi tiết đề tài số 1", open_top1, 1)
        def register():
            p.locator("a:has-text('Đăng ký')").first.click()
            p.wait_for_url(re.compile(r".*/nguyen-vong/.*"))
            p.locator("button[value=submit], button:has-text('Nộp')").first.click()
            p.wait_for_load_state("networkidle")
        step("Đăng ký NV1 và nộp", register, 3)
    elif name == "sv-it-ranh":
        def phone():
            p.goto(base + "/ho-so/")
            p.fill("input[name=phone]", "0912345678")
            p.locator("button[type=submit]").first.click()
            p.wait_for_load_state("networkidle")
        step("Cập nhật SĐT trong Hồ sơ", phone, 3)
        def search():
            p.goto(base + "/danh-sach-de-tai/")
            p.fill("input[name=q]", "web")
            p.keyboard.press("Enter")
            p.wait_for_load_state("networkidle")
        step("Tìm đề tài chữ 'web'", search, 3)
        step("Xem Kết quả phân công", lambda: p.goto(base + "/ket-qua/"), 1)
    elif name == "gv-tre":
        step("Xem SV chờ duyệt", lambda: p.goto(base + "/trang-chu/"), 1)
        def review():
            p.goto(base + "/de-tai/")
            p.locator("a[href*='/dang-ky/']").first.click()
            p.wait_for_load_state("networkidle")
        step("Mở trang duyệt đăng ký", review, 2)
        step("Mở form thêm đề tài", lambda: p.goto(base + "/de-tai/them/"), 2)
    elif name == "gv-lon-tuoi":
        step("Xem đề tài của mình", lambda: p.goto(base + "/de-tai/"), 1)
        def bio():
            p.goto(base + "/ho-so-giang-vien/")
            p.fill("textarea[name=bio]", "Hướng dẫn đề tài hệ thống thông tin quản lý.")
            p.locator("button[type=submit]").first.click()
            p.wait_for_load_state("networkidle")
        step("Sửa giới thiệu hồ sơ GV", bio, 3)
    elif name == "giao-vu":
        def sample():
            p.goto(base + "/khoa/nhap-excel/")
            with p.expect_download() as d:
                p.locator("a[href*='mau.xlsx']").first.click()
            d.value.save_as(str(OUT / "mau.xlsx"))
        step("Tải tệp Excel mẫu", sample, 2)
        def run_ilp():
            p.goto(base + "/khoa/phan-cong/")
            p.locator("button[name=action][value=run_ilp], button:has-text('ILP')").first.click()
            p.wait_for_load_state("networkidle")
        step("Chạy phân công ILP", run_ilp, 2)
        step("Xem bảng kết quả", lambda: p.mouse.wheel(0, 900), 1)
    elif name == "truong-khoa":
        step("Xem bảng điều khiển", lambda: p.goto(base + "/trang-chu/"), 1)
        step("Xem Thống kê", lambda: (p.goto(base + "/khoa/thong-ke/"), p.wait_for_timeout(1500)), 1)


def contact_sheet(shots, path):
    imgs = [Image.open(s).convert("RGB") for _, s in shots]
    w = 1000
    imgs = [im.resize((w, int(im.height * w / im.width))) for im in imgs]
    sheet = Image.new("RGB", (w, sum(im.height for im in imgs) + 10 * len(imgs)), "white")
    y = 0
    for im in imgs:
        sheet.paste(im, (0, y))
        y += im.height + 10
    sheet.save(path, quality=80)


PROMPT = """Bạn đóng vai NGƯỜI DÙNG sau, lần đầu dùng hệ thống "Capstone Advisor AI" (hệ thống gợi ý và phân công đề tài
đồ án tốt nghiệp của một khoa). Nhân vật: {who}.
Ảnh đính kèm là các màn hình theo thứ tự trên xuống, ứng với các nhiệm vụ: {tasks}.
Máy đã làm thử các nhiệm vụ này: {log}.
Hãy trả lời ĐÚNG GIỌNG nhân vật, tiếng Việt, ngắn gọn, theo đúng 4 phần:
1. Mỗi nhiệm vụ: độ khó 1 (rất dễ) – 5 (rất khó) và 1 câu lý do, dựa vào những gì thấy trên màn hình.
2. Tối đa 5 chỗ làm nhân vật bối rối hoặc dễ bấm nhầm; mỗi chỗ ghi màn hình số mấy và nguyên tắc Nielsen bị vi phạm.
3. Trả lời 10 câu SUS (thang 1–5) theo cảm nhận của nhân vật, dạng: SUS: 4,2,5,1,4,2,5,1,4,2
4. Một câu: nhân vật có muốn dùng lại hệ thống không.
Đây là ĐÁNH GIÁ MÔ PHỎNG phục vụ kiểm thử, không phải ý kiến người thật — đừng khen chung chung, hãy chỉ ra vấn đề cụ thể."""


def sus_score(answers):
    """Brooke (1996): câu lẻ (x−1), câu chẵn (5−x), tổng × 2,5."""
    return 2.5 * sum((a - 1) if i % 2 == 0 else (5 - a) for i, a in enumerate(answers))


def main():
    proc, base, env = bc.start_server()
    results = []
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            for name, user, who, tasks in PERSONAS:
                ctx = br.new_context(viewport={"width": 1366, "height": 768})
                p = ctx.new_page()
                shots, log = [], []
                do_tasks(p, base, name, user, shots, log)
                ctx.close()
                sheet = OUT / f"{name}-tong.jpg"
                contact_sheet(shots, sheet)
                res = P.chatgpt(OUT, f"persona-{name}", PROMPT.format(who=who, tasks="; ".join(tasks),
                                log=json.dumps(log, ensure_ascii=False)), image=sheet, new_chat=True, timeout=600)
                text = res.get("text", "")
                m = re.search(r"SUS[^0-9]*((?:[1-5]\s*,\s*){9}[1-5])", text)
                answers = [int(x) for x in re.findall(r"[1-5]", m.group(1))] if m else []
                results.append({"nhan_vat": name, "mo_ta": who, "nhiem_vu": log, "sus_mo_phong": sus_score(answers) if len(answers) == 10 else None,
                                "danh_gia": text})
                print(f"{name}: {sum(t['hoan_thanh'] for t in log)}/{len(log)} nhiệm vụ, SUS mô phỏng = {results[-1]['sus_mo_phong']}", flush=True)
            br.close()
    finally:
        proc.terminate()
    (OUT / "danh-gia-dong-vai.json").write_text(json.dumps(results, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
