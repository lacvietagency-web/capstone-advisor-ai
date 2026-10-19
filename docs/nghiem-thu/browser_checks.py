"""Nghiệm thu — các ca chỉ kiểm được trên trình duyệt thật (Playwright) + quét khả năng truy cập axe-core.

  python docs/nghiem-thu/browser_checks.py <thư mục kết quả> [chromium,firefox,webkit] [đường dẫn axe.min.js]

Tự dựng máy chủ riêng trên BẢN SAO CSDL demo (webby-v3/db/open.sqlite3) — không đụng máy chạy thật.
Ghi <out>/ket-qua.json (mỗi ca: mã, trình duyệt, đạt/không đạt/chưa kiểm chứng, chi tiết) + ảnh chụp.
Ca: A03 A04 A14 K10 K13 U01 U02 U03 U04 U05 U06 U07 + AXE (#10) + ĐA TRÌNH DUYỆT (#11).
"""

import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[2]
OUT = Path(sys.argv[1]).resolve()
BROWSERS = (sys.argv[2] if len(sys.argv) > 2 else "chromium").split(",")
AXE = Path(sys.argv[3]) if len(sys.argv) > 3 else None
PY = os.environ.get("QA_PYTHON", sys.executable)
OUT.mkdir(parents=True, exist_ok=True)
RESULTS = []


def record(code, browser, status, detail="", shot=None):
    RESULTS.append({"ma": code, "trinh_duyet": browser, "ket_qua": status, "chi_tiet": detail, "anh": shot})
    print(f"[{browser:8}] {code:6} {status:16} {detail[:110]}", flush=True)


def start_server():
    db = OUT / "browser.sqlite3"
    shutil.copy(REPO.parent / "webby-v3" / "db" / "open.sqlite3", db)
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    env = {**os.environ, "SQLITE_PATH": str(db), "DJANGO_DEBUG": "0", "ASSETS_FROM_CDN": "0",
           "RECOMMEND_SEMANTIC": "0", "RECOMMEND_LLM": "0"}
    subprocess.run([PY, "manage.py", "migrate", "-v", "0"], cwd=REPO, env=env, check=True)
    proc = subprocess.Popen([PY, "manage.py", "runserver", f"127.0.0.1:{port}", "--noreload", "--insecure"],
                            cwd=REPO, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    base = f"http://127.0.0.1:{port}"
    for _ in range(60):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                break
        except OSError:
            time.sleep(0.5)
    return proc, base, env


def django(env, code):
    out = subprocess.run([PY, "manage.py", "shell", "-c", code], cwd=REPO, env=env, capture_output=True, text=True).stdout
    return (out.strip().splitlines() or [""])[-1]  # bỏ các dòng log, lấy dòng in cuối


def login(page, base, user):
    page.goto(base + "/dang-nhap/")
    page.fill("#id_username", user)
    page.fill("#id_password", "123456")
    page.click("button[type=submit]")
    page.wait_for_url(re.compile(r".*/trang-chu/.*|.*/$"), timeout=15000)


OVERFLOW_JS = "() => document.documentElement.scrollWidth - document.documentElement.clientWidth"
SMALL_TEXT_JS = """() => { const out = []; for (const e of document.querySelectorAll('body *')) {
  if (!e.childNodes.length || ![...e.childNodes].some(c => c.nodeType === 3 && c.textContent.trim())) continue;
  const r = e.getBoundingClientRect(); if (!r.width || !r.height) continue;
  const fs = parseFloat(getComputedStyle(e).fontSize);
  if (fs < 12) out.push(e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).split(' ').join('.') : '') + '=' + fs + 'px "' + e.textContent.trim().slice(0, 20) + '"'); }
  return out; }"""


def page_set(base, env):
    t = django(env, "from catalog.models import Topic;print(Topic.objects.filter(status='OPEN').first().pk)")
    own = django(env, "from catalog.models import Topic;print(Topic.objects.filter(lecturer__user__username='gv001').first().pk)")
    return {
        None: ["/dang-nhap/", "/abc-khong-ton-tai/"],
        "sv001": ["/trang-chu/", "/ho-so/", "/danh-sach-de-tai/", f"/danh-sach-de-tai/{t}/", "/nguyen-vong/",
                  "/ket-qua/", "/doi-mat-khau/"],
        "gv001": ["/trang-chu/", "/de-tai/", "/de-tai/them/", f"/de-tai/{own}/sua/", f"/de-tai/{own}/dang-ky/",
                  "/ho-so-giang-vien/"],
        "khoa01": ["/trang-chu/", "/khoa/phan-cong/", "/khoa/nhap-excel/", "/khoa/thong-ke/"],
    }


def new_context(br, theme="light", width=1440, mobile=False):
    ctx = br.new_context(viewport={"width": width, "height": 900 if width > 500 else 844}, is_mobile=mobile and width < 500,
                         color_scheme="dark" if theme == "dark" else "light")
    ctx.add_init_script(f"try {{ localStorage.setItem('atlas-theme', '{theme}') }} catch (e) {{}}")
    return ctx


def check_login_page(br, base, name):
    ctx = new_context(br)
    p = ctx.new_page()
    p.goto(base + "/dang-nhap/")
    # A03 — nút "Sử dụng" điền tên, đưa con trỏ sang ô mật khẩu, KHÔNG tự đăng nhập
    ok, det = True, []
    for user in ("sv001", "gv001", "khoa01"):
        p.click(f"[data-at-demo='{user}']")
        val = p.input_value("#id_username")
        focus = p.evaluate("() => document.activeElement && document.activeElement.id")
        if val != user or focus != "id_password" or "/dang-nhap/" not in p.url:
            ok = False
            det.append(f"{user}: ô={val} focus={focus} url={p.url}")
    shot = str(OUT / f"{name}-A03.png")
    p.screenshot(path=shot)
    record("A03", name, "ĐẠT" if ok else "KHÔNG ĐẠT", "; ".join(det) or "3 nút điền đúng, focus ô mật khẩu, không tự đăng nhập", shot)
    # A04 — nút mắt: đổi kiểu ô, giữ giá trị, dùng được bằng bàn phím
    p.fill("#id_password", "abc123")
    p.click("#btnTogglePassword")
    t1 = p.get_attribute("#id_password", "type")
    p.focus("#btnTogglePassword")
    p.keyboard.press("Enter")
    t2 = p.get_attribute("#id_password", "type")
    ok = t1 == "text" and t2 == "password" and p.input_value("#id_password") == "abc123"
    record("A04", name, "ĐẠT" if ok else "KHÔNG ĐẠT", f"bấm chuột → {t1}; Enter → {t2}; giá trị giữ nguyên")
    ctx.close()


def check_theme(br, base, name):
    # A14 — chọn Tối, tải lại, sang trang khác vẫn giữ
    ctx = br.new_context(viewport={"width": 1440, "height": 900})
    p = ctx.new_page()
    login(p, base, "sv001")
    p.evaluate("() => localStorage.setItem('atlas-theme', 'dark')")
    p.reload()
    dark1 = p.evaluate("() => document.documentElement.getAttribute('data-bs-theme')")
    p.goto(base + "/danh-sach-de-tai/")
    dark2 = p.evaluate("() => document.documentElement.getAttribute('data-bs-theme')")
    ok = "dark" in str(dark1) and "dark" in str(dark2)
    shot = str(OUT / f"{name}-A14-toi.png")
    p.screenshot(path=shot)
    record("A14", name, "ĐẠT" if ok else "KHÔNG ĐẠT", f"sau tải lại: {dark1}; trang khác: {dark2}", shot)
    ctx.close()


def check_publish_and_charts(br, base, env, name):
    ctx = new_context(br)
    p = ctx.new_page()
    login(p, base, "khoa01")
    p.goto(base + "/khoa/phan-cong/")
    run = p.locator("button[name=action][value=run_ilp], button:has-text('ILP')").first
    if run.count():
        run.click()
        p.wait_for_load_state("networkidle")
    opener = p.locator("[data-bs-target]:has-text('ông bố'), button:has-text('Chốt')").first
    if not opener.count():
        record("K10", name, "CHƯA KIỂM CHỨNG", "không thấy nút mở hộp Chốt & công bố")
    else:
        opener.click()
        p.wait_for_selector("#atConfirmInput", state="visible")
        submit = p.locator("form:has(#atConfirmInput) button[type=submit]")
        s0 = submit.is_disabled()
        p.fill("#atConfirmInput", "cong bo")
        s1 = submit.is_disabled()
        p.fill("#atConfirmInput", "CÔNG BỐ")
        s2 = submit.is_disabled()
        shot = str(OUT / f"{name}-K10.png")
        p.screenshot(path=shot)
        ok = s0 and s1 and not s2
        record("K10", name, "ĐẠT" if ok else "KHÔNG ĐẠT", f"trống→khoá={s0}, gõ sai→khoá={s1}, gõ đúng→mở={not s2}", shot)
    # K13 — biểu đồ vẽ được ở Sáng và Tối, có bảng số liệu
    det, ok = [], True
    for theme in ("light", "dark"):
        c2 = new_context(br, theme)
        q = c2.new_page()
        login(q, base, "khoa01")
        q.goto(base + "/khoa/thong-ke/")
        q.wait_for_timeout(1500)
        charts = q.evaluate("() => document.querySelectorAll('canvas, svg.chart, [data-chart] svg, .at-chart svg').length")
        tables = q.evaluate("() => document.querySelectorAll('table').length")
        q.screenshot(path=str(OUT / f"{name}-K13-{theme}.png"), full_page=True)
        det.append(f"{theme}: {charts} biểu đồ, {tables} bảng")
        ok = ok and charts > 0 and tables > 0
        c2.close()
    record("K13", name, "ĐẠT" if ok else "KHÔNG ĐẠT", "; ".join(det), str(OUT / f"{name}-K13-dark.png"))
    ctx.close()


def check_pages(br, base, env, name, axe_src):
    pages = page_set(base, env)
    overflow, small, console_err, http_err, external, axe_bad, axe_all = [], [], [], [], [], [], {}
    for theme in ("light", "dark"):
        for width in (390, 768, 1440):
            for user, urls in pages.items():
                ctx = new_context(br, theme, width, mobile=True)
                p = ctx.new_page()
                p.on("console", lambda m, u=None: console_err.append(m.text) if m.type == "error" else None)
                p.on("response", lambda r: http_err.append(f"{r.status} {r.url}") if r.status >= 400 and "abc-khong" not in r.url else None)
                p.on("request", lambda r: external.append(r.url) if not r.url.startswith(base) and r.url.startswith("http") else None)
                if user:
                    login(p, base, user)
                for url in urls:
                    p.goto(base + url)
                    p.wait_for_load_state("networkidle")
                    tag = f"{user or 'khach'} {url} {width}px {theme}"
                    if p.evaluate(OVERFLOW_JS) > 1:
                        overflow.append(tag)
                    tiny = p.evaluate(SMALL_TEXT_JS)
                    if tiny:
                        small.append(f"{tag}: {len(tiny)} ({'; '.join(sorted(set(tiny))[:3])})")
                    if axe_src and width == 1440:
                        p.add_script_tag(content=axe_src)
                        res = p.evaluate("async () => (await axe.run(document, {runOnly: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']})).violations.map(v => [v.id, v.impact, v.nodes.length])")
                        for vid, impact, n in res:
                            axe_all.setdefault((vid, impact), []).append(f"{tag} ×{n}")
                            if impact in ("serious", "critical"):
                                axe_bad.append(f"{vid} ({impact}) {tag} ×{n}")
                    if width == 390 and theme == "light":
                        p.screenshot(path=str(OUT / f"{name}-390-{(user or 'khach')}-{url.strip('/').replace('/', '_') or 'root'}.png"))
                ctx.close()
    record("U01", name, "ĐẠT" if not overflow and not small else "KHÔNG ĐẠT",
           f"{len(overflow)} trang tràn ngang; {len(small)} trang có chữ < 12px. " + "; ".join((overflow + small)[:6]))
    record("G1", name, "ĐẠT" if not console_err and not http_err else "KHÔNG ĐẠT",
           f"{len(console_err)} lỗi console, {len(http_err)} tài nguyên lỗi. " + "; ".join(sorted(set(http_err))[:6] + sorted(set(console_err))[:3]))
    record("U06", name, "ĐẠT" if not external else "KHÔNG ĐẠT",
           f"{len(set(external))} địa chỉ ngoài máy được gọi khi ASSETS_FROM_CDN=0. " + "; ".join(sorted(set(external))[:4]))
    if axe_src:
        summary = "; ".join(f"{vid}/{imp}: {len(v)} trang" for (vid, imp), v in sorted(axe_all.items()))
        record("AXE", name, "ĐẠT" if not axe_bad else "KHÔNG ĐẠT",
               f"{len(axe_bad)} vi phạm serious/critical. Tất cả: {summary or 'không có'}")
        (OUT / f"axe-{name}.json").write_text(json.dumps({f"{k[0]}|{k[1]}": v for k, v in axe_all.items()}, ensure_ascii=False, indent=1))


def check_mobile_keyboard_labels(br, base, env, name):
    # U02 — 390 px: có thanh điều hướng đáy; khi sửa nguyện vọng không chồng hai thanh
    ctx = new_context(br, "light", 390, mobile=True)
    p = ctx.new_page()
    login(p, base, "sv001")
    p.goto(base + "/nguyen-vong/")
    bars = p.evaluate("""() => [...document.querySelectorAll('nav, [class*=bottom], [class*=sticky], [class*=action-bar]')]
        .filter(e => { const s = getComputedStyle(e), r = e.getBoundingClientRect();
                       return (s.position === 'fixed' || s.position === 'sticky') && r.bottom >= innerHeight - 2 && r.height > 0
                              && s.display !== 'none' && s.visibility !== 'hidden'; }).length""")
    shot = str(OUT / f"{name}-U02.png")
    p.screenshot(path=shot)
    record("U02", name, "ĐẠT" if bars <= 1 else "KHÔNG ĐẠT", f"{bars} thanh cố định ở đáy màn hình trang Nguyện vọng 390 px", shot)
    ctx.close()
    # U03 — Tab đi qua các phần tử có viền focus; Esc đóng ngăn kéo
    ctx = new_context(br)
    p = ctx.new_page()
    login(p, base, "gv001")
    p.goto(base + "/trang-chu/")
    no_ring, seen = [], 0
    for _ in range(25):
        p.keyboard.press("Tab")
        info = p.evaluate("""() => { const e = document.activeElement; if (!e || e === document.body) return null;
            const s = getComputedStyle(e); return [e.tagName + (e.className ? '.' + String(e.className).split(' ')[0] : ''),
            s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0 || s.boxShadow !== 'none'] }""")
        if info:
            seen += 1
            if not info[1]:
                no_ring.append(info[0])
    own = django(env, "from catalog.models import Preference;p=Preference.objects.filter(topic__lecturer__user__username='gv001',submitted=True).first();print(f'{p.topic_id} {p.pk}' if p else '')")
    esc = "không có NV để mở ngăn kéo"
    if own:
        tid, pid = own.split()
        p.goto(base + f"/de-tai/{tid}/dang-ky/?mo={pid}")
        p.wait_for_timeout(800)
        vis = lambda: p.evaluate("() => [...document.querySelectorAll('[role=dialog], .offcanvas, [class*=drawer]')].some(e => { const r = e.getBoundingClientRect(); return r.width > 0 && getComputedStyle(e).visibility !== 'hidden' && e.classList.contains('show') || e.getAttribute('aria-hidden') === 'false' || e.open })")
        before = vis()
        p.keyboard.press("Escape")
        p.wait_for_timeout(500)
        esc = f"ngăn kéo mở={before}, sau Esc còn mở={vis()}"
    ok = seen >= 10 and not no_ring and "còn mở=False" in esc
    record("U03", name, "ĐẠT" if ok else "KHÔNG ĐẠT",
           f"Tab qua {seen} phần tử, {len(no_ring)} không có viền focus ({', '.join(sorted(set(no_ring))[:5])}); {esc}")
    ctx.close()
    # U05 — trạng thái rỗng: SV chưa có nguyện vọng
    django(env, "from catalog.models import Preference;Preference.objects.filter(student__user__username='sv100').delete()")
    ctx = new_context(br)
    p = ctx.new_page()
    login(p, base, "sv100")
    p.goto(base + "/nguyen-vong/")
    has_empty = p.evaluate("() => !!document.querySelector('.at-empty, [class*=empty], svg[class*=empty], img[alt]')")
    record("U05", name, "ĐẠT" if has_empty else "KHÔNG ĐẠT", f"trang Nguyện vọng của SV chưa có NV có khối trạng thái rỗng: {has_empty}")
    ctx.close()
    # U07 — trang 404 tiếng Việt, có đường về
    ctx = new_context(br)
    p = ctx.new_page()
    r = p.goto(base + "/abc-khong-ton-tai/")
    txt = p.inner_text("body")
    home = p.locator("a[href='/'], a[href='/trang-chu/'], a[href*='trang-chu']").count()
    ok = r.status == 404 and home > 0 and re.search(r"[ơưđạảấầẩẫậắằẳẵặ]", txt.lower())
    shot = str(OUT / f"{name}-U07.png")
    p.screenshot(path=shot)
    record("U07", name, "ĐẠT" if ok else "KHÔNG ĐẠT", f"mã {r.status}, {home} liên kết về trang chủ, tiếng Việt có dấu", shot)
    ctx.close()


def main():
    proc, base, env = start_server()
    axe_src = AXE.read_text() if AXE and AXE.exists() else None
    try:
        with sync_playwright() as pw:
            for name in BROWSERS:
                try:
                    br = getattr(pw, name).launch()
                except Exception as e:  # thiếu thư viện hệ thống → không giả vờ đạt
                    record("BROWSER", name, "CHƯA KIỂM CHỨNG", f"không mở được trình duyệt: {str(e).splitlines()[0][:150]}")
                    continue
                for fn in (check_login_page, check_theme):
                    try:
                        fn(br, base, name)
                    except Exception as e:
                        record(fn.__name__, name, "LỖI KỊCH BẢN", str(e).splitlines()[0][:150])
                for fn in (check_publish_and_charts, check_mobile_keyboard_labels):
                    try:
                        fn(br, base, env, name)
                    except Exception as e:
                        record(fn.__name__, name, "LỖI KỊCH BẢN", str(e).splitlines()[0][:150])
                try:
                    check_pages(br, base, env, name, axe_src if name == "chromium" else None)
                except Exception as e:
                    record("check_pages", name, "LỖI KỊCH BẢN", str(e).splitlines()[0][:150])
                br.close()
    finally:
        proc.terminate()
    (OUT / "ket-qua.json").write_text(json.dumps(RESULTS, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
