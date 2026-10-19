/* ATLAS — hành vi dùng chung (không thư viện ngoài Bootstrap).
   data-at-theme="light|dark|system"   chọn giao diện, lưu localStorage "atlas-theme"
   data-at-busy (trên <form>)          nút gửi chuyển "Đang xử lý…", khoá bấm lặp
   data-at-autosubmit (trên <select>)  đổi là gửi form
   data-at-confirm-text="CÔNG BỐ"      (trên <input>) chỉ bật nút submit của form khi gõ đúng chữ
   data-at-fill='{"name": "giá trị"}'  (trên nút mở modal) điền input[name] và [data-at-slot=name] trong modal
   data-at-drawer-url="/..."           (trên nút mở offcanvas) tải mảnh HTML vào .offcanvas-body khi mở
   data-at-autoclose / data-at-dismiss thông báo tự đóng sau 5 giây / nút đóng
   data-at-chart='{...}'               (trên <canvas>) cấu hình Chart.js; màu "var(--at-chart-1)" được đổi thành mã màu thật */
(function () {
  "use strict";
  var KEY = "atlas-theme";
  var media = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

  function choice() { try { return localStorage.getItem(KEY) || "system"; } catch (e) { return "system"; } }
  function apply(c) {
    var dark = c === "dark" || (c === "system" && media && media.matches);
    document.documentElement.setAttribute("data-bs-theme", dark ? "dark" : "light");
    document.querySelectorAll("[data-at-theme]").forEach(function (b) {
      b.setAttribute("aria-checked", b.getAttribute("data-at-theme") === c ? "true" : "false");
    });
    document.dispatchEvent(new CustomEvent("atlas:theme"));
  }
  if (media && media.addEventListener) media.addEventListener("change", function () { if (choice() === "system") apply("system"); });

  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-at-theme]");
    if (t) { var c = t.getAttribute("data-at-theme"); try { localStorage.setItem(KEY, c); } catch (x) {} apply(c); }
    var d = e.target.closest("[data-at-dismiss]");
    if (d) d.closest(".at-toast").remove();
  });

  document.addEventListener("submit", function (e) {
    var f = e.target;
    if (!f.hasAttribute("data-at-busy")) return;
    if (f.dataset.atSubmitted) { e.preventDefault(); return; }
    f.dataset.atSubmitted = "1";
    var b = e.submitter || f.querySelector("[type=submit]");
    if (b) {
      b.style.width = b.offsetWidth + "px";
      b.setAttribute("aria-busy", "true");
      b.innerHTML = '<span class="at-spinner" aria-hidden="true"></span>Đang xử lý…';
      setTimeout(function () { b.disabled = true; }, 0);
    }
  });

  document.addEventListener("change", function (e) {
    if (e.target.matches("[data-at-autosubmit]")) e.target.form.submit();
  });

  document.addEventListener("input", function (e) {
    var i = e.target;
    if (!i.matches("[data-at-confirm-text]")) return;
    var ok = i.value.trim() === i.getAttribute("data-at-confirm-text");
    i.form.querySelectorAll("[type=submit]").forEach(function (b) { b.disabled = !ok; });
  });

  /* Modal: điền dữ liệu của dòng được bấm */
  document.addEventListener("show.bs.modal", function (e) {
    var src = e.relatedTarget, m = e.target;
    /* Hộp thoại mở từ trong ngăn kéo: đóng ngăn kéo trước, tránh hai bẫy focus giành nhau */
    document.querySelectorAll(".offcanvas.show").forEach(function (o) { bootstrap.Offcanvas.getOrCreateInstance(o).hide(); });
    if (!src || !src.dataset.atFill) return;
    var data = JSON.parse(src.dataset.atFill);
    Object.keys(data).forEach(function (k) {
      m.querySelectorAll('[name="' + k + '"]').forEach(function (el) { el.value = data[k]; });
      m.querySelectorAll('[data-at-slot="' + k + '"]').forEach(function (el) { el.textContent = data[k]; });
    });
    m.querySelectorAll("[data-at-confirm-text]").forEach(function (i) {
      i.value = ""; i.form.querySelectorAll("[type=submit]").forEach(function (b) { b.disabled = true; });
    });
  });

  /* Ngăn kéo: tải mảnh HTML khi mở */
  document.addEventListener("show.bs.offcanvas", function (e) {
    var src = e.relatedTarget, body = e.target.querySelector(".offcanvas-body");
    if (!src || !src.dataset.atDrawerUrl || !body) return;
    var title = e.target.querySelector(".offcanvas-title");
    if (title && src.dataset.atDrawerTitle) title.textContent = src.dataset.atDrawerTitle;
    body.innerHTML = '<p class="at-secondary at-row"><span class="at-spinner" aria-hidden="true"></span>Đang tải…</p>';
    fetch(src.dataset.atDrawerUrl, { headers: { "X-Requested-With": "fetch" }, credentials: "same-origin" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
      .then(function (html) { body.innerHTML = html; })
      .catch(function () { body.innerHTML = '<div class="at-banner at-banner--danger" role="alert"><div>Không tải được dữ liệu. Đóng ngăn kéo và thử lại.</div></div>'; });
  });

  /* Ngăn kéo mở không lớp phủ (data-bs-backdrop=false) thì Bootstrap không đưa focus vào trong, nên phím Esc
     (Bootstrap chỉ nghe khi focus nằm trong ngăn kéo) không đóng được — kiểm thử U03 ngày 20/10/2026.
     Mở xong: đưa focus vào nút Đóng (trình đọc màn hình đọc ngay tiêu đề); Esc ở bất kỳ đâu đóng ngăn kéo đang mở. */
  document.addEventListener("shown.bs.offcanvas", function (e) {
    var close = e.target.querySelector("[data-bs-dismiss=offcanvas]");
    if (close && !e.target.contains(document.activeElement)) close.focus();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape" || document.querySelector(".modal.show")) return;
    document.querySelectorAll(".offcanvas.show").forEach(function (o) { bootstrap.Offcanvas.getOrCreateInstance(o).hide(); });
  });

  /* Biểu đồ: đọc màu từ biến CSS, vẽ lại khi đổi sáng/tối */
  function cssVar(v) { return getComputedStyle(document.documentElement).getPropertyValue(v).trim(); }
  function resolve(x) {
    if (typeof x === "string") { var m = x.match(/^var\((--[\w-]+)\)$/); return m ? cssVar(m[1]) : x; }
    if (Array.isArray(x)) return x.map(resolve);
    if (x && typeof x === "object") { var o = {}; Object.keys(x).forEach(function (k) { o[k] = resolve(x[k]); }); return o; }
    return x;
  }
  var charts = [];
  function drawCharts() {
    if (!window.Chart) return;
    charts.forEach(function (c) { c.destroy(); }); charts = [];
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    Chart.defaults.font.family = '"Be Vietnam Pro", Arial, sans-serif';
    Chart.defaults.font.size = 12;
    Chart.defaults.color = cssVar("--at-ink-muted");
    Chart.defaults.borderColor = cssVar("--at-line");
    Chart.defaults.plugins.legend.position = "top";
    Chart.defaults.plugins.legend.labels.boxWidth = 10;
    Chart.defaults.plugins.legend.labels.boxHeight = 10;
    Chart.defaults.plugins.tooltip.backgroundColor = cssVar("--at-ink");
    Chart.defaults.plugins.tooltip.titleColor = cssVar("--at-surface");
    Chart.defaults.plugins.tooltip.bodyColor = cssVar("--at-surface");
    Chart.defaults.plugins.tooltip.padding = 10;
    Chart.defaults.animation = reduce ? false : { duration: 240, easing: "easeOutCubic" };
    Chart.defaults.maintainAspectRatio = false;
    Chart.defaults.datasets.bar.borderRadius = 4;
    Chart.defaults.datasets.bar.maxBarThickness = 38;
    document.querySelectorAll("canvas[data-at-chart]").forEach(function (cv) {
      charts.push(new Chart(cv, resolve(JSON.parse(cv.dataset.atChart))));
    });
  }
  document.addEventListener("atlas:theme", drawCharts);

  document.addEventListener("DOMContentLoaded", function () {
    apply(choice());
    document.querySelectorAll("[data-bs-toggle=tooltip]").forEach(function (el) { new bootstrap.Tooltip(el); });
    document.querySelectorAll("[data-at-autoclose]").forEach(function (t) { setTimeout(function () { t.remove(); }, 5000); });
  });
  window.addEventListener("load", drawCharts);
})();
