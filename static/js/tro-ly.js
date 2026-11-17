/* Trợ lý ảo Capstone AI: khung chat nổi. Lịch sử hiển thị giữ trong sessionStorage theo tab để đổi trang không mất;
   lịch sử dùng cho mô hình nằm ở phiên máy chủ. Câu trả lời được thoát HTML trước khi định dạng (chống XSS). */
(function () {
  var root = document.getElementById("tlRoot");
  if (!root) return;
  var KEY = "tro-ly:" + root.dataset.user, panel = document.getElementById("tlPanel"), fab = document.getElementById("tlFab");
  var log = document.getElementById("tlLog"), form = document.getElementById("tlForm"), input = document.getElementById("tlInput");
  var chips = document.getElementById("tlChips"), csrf = root.querySelector("[name=csrfmiddlewaretoken]").value;
  var state = load(), busy = false, warmed = false;

  function load() { try { return JSON.parse(sessionStorage.getItem(KEY)) || { open: false, msgs: [] }; } catch (e) { return { open: false, msgs: [] }; } }
  function save() { try { sessionStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }
  var KINDS = { guide: ["route", "Hướng dẫn", "mở trang"], topic: ["book-open", "Đề tài", "xem đề tài"],
    lecturer: ["user-round", "Giảng viên", "xem"], archived: ["archive", "Khoá trước", ""] };
  function icon(name, size) {
    var i = document.createElement("span"); i.className = "at-icon"; i.setAttribute("aria-hidden", "true");
    i.style.setProperty("--i", "url('" + root.dataset.icons + name + ".svg')"); i.style.setProperty("--s", size + "px");
    return i;
  }
  function esc(s) { return s.replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function inline(s) { return esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/\[((?:\d+|Bạn|Hệ thống)(?:\s*,\s*(?:\d+|Bạn|Hệ thống))*)\]/g, '<sup class="tl-ref">$1</sup>'); }
  function format(text) {
    var html = "", list = false;
    text.split(/\n+/).forEach(function (line) {
      var m = line.match(/^\s*[-•*]\s+(.*)/);
      if (m) { if (!list) { html += "<ul>"; list = true; } html += "<li>" + inline(m[1]) + "</li>"; return; }
      if (list) { html += "</ul>"; list = false; }
      if (line.trim()) html += "<p>" + inline(line) + "</p>";
    });
    return html + (list ? "</ul>" : "");
  }
  function render(m) {
    var div = document.createElement("div");
    div.className = "tl-msg " + (m.who === "me" ? "tl-me" : "tl-bot") + (m.err ? " tl-err" : "");
    if (m.who === "me") div.textContent = m.text; else div.innerHTML = format(m.text);
    if (m.sources && m.sources.length) {  // thẻ nguồn gọn: icon theo loại + tên 1 dòng; có đường dẫn thì bấm được
      var src = document.createElement("div"); src.className = "tl-src";
      m.sources.forEach(function (s) {
        var k = KINDS[s.kind] || KINDS.guide, el = document.createElement(s.url ? "a" : "div");
        el.className = "tl-thumb tl-thumb--" + (KINDS[s.kind] ? s.kind : "guide");
        if (s.url) el.href = s.url;
        el.title = s.title;
        var ic = document.createElement("span"); ic.className = "tl-thumb-ic";
        ic.appendChild(icon(k[0], 16));
        var num = document.createElement("b"); num.textContent = s.n; ic.appendChild(num);
        var tx = document.createElement("span"); tx.className = "tl-thumb-tx";
        var parts = s.title.replace(/^GV /, "").split(" · "), name = parts.pop();  // "DT-2026-316 · Tên" → mã lên dòng nhỏ
        var kd = document.createElement("small"); kd.textContent = (parts[0] || k[1]) + (s.url ? " · " + k[2] : "");
        var tt = document.createElement("span"); tt.textContent = name;
        tx.appendChild(kd); tx.appendChild(tt); el.appendChild(ic); el.appendChild(tx);
        if (s.url) el.appendChild(icon("chevron-right", 16));
        src.appendChild(el);
      });
      div.appendChild(src);
    }
    if (m.mode === "fallback") { var n = document.createElement("small"); n.className = "tl-mode"; n.textContent = "Chế độ dự phòng: chưa gọi được mô hình ngôn ngữ"; div.appendChild(n); }
    log.appendChild(div); log.scrollTop = log.scrollHeight;
  }
  function setOpen(open) {
    state.open = open; save(); panel.hidden = !open; fab.setAttribute("aria-expanded", open);
    root.classList.toggle("is-open", open);
    if (open) { input.focus(); log.scrollTop = log.scrollHeight; if (!warmed) { warmed = true; post({ warm: "1" }); } }
  }
  function post(data) {
    var body = new URLSearchParams(data);
    return fetch(root.dataset.url, { method: "POST", body: body, credentials: "same-origin", headers: { "X-CSRFToken": csrf } })
      .then(function (r) { return r.json().catch(function () { return { error: "Máy chủ trả lỗi " + r.status + "." }; }); });
  }
  function ask(q) {
    q = q.trim(); if (!q || busy) return;
    busy = true; chips.hidden = true;
    var me = { who: "me", text: q }; state.msgs.push(me); render(me); save();
    var wait = document.createElement("div"); wait.className = "tl-msg tl-bot tl-wait"; wait.textContent = "Đang tra dữ liệu…";
    log.appendChild(wait); log.scrollTop = log.scrollHeight;
    post({ q: q }).then(function (d) {
      var m = d.error ? { who: "bot", text: d.error, err: true } : { who: "bot", text: d.answer, sources: d.sources, mode: d.mode };
      wait.remove(); state.msgs.push(m); state.msgs = state.msgs.slice(-30); render(m); save();
    }).catch(function () {
      wait.remove(); render({ who: "bot", text: "Mất kết nối tới máy chủ, bạn thử lại nhé.", err: true });
    }).finally(function () { busy = false; input.focus(); });
  }

  state.msgs.forEach(render);
  chips.hidden = state.msgs.length > 0;
  setOpen(state.open);
  fab.addEventListener("click", function () { setOpen(!state.open); });
  document.getElementById("tlClose").addEventListener("click", function () { setOpen(false); fab.focus(); });
  document.getElementById("tlNew").addEventListener("click", function () {
    post({ reset: "1" }); state.msgs = []; save();
    Array.prototype.slice.call(log.querySelectorAll(".tl-msg:not(.tl-hello)")).forEach(function (n) { n.remove(); });
    chips.hidden = false; input.focus();
  });
  chips.addEventListener("click", function (e) { if (e.target.tagName === "BUTTON") ask(e.target.textContent); });
  form.addEventListener("submit", function (e) { e.preventDefault(); var q = input.value; input.value = ""; ask(q); });
  input.addEventListener("keydown", function (e) { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); } });
  panel.addEventListener("keydown", function (e) { if (e.key === "Escape") { setOpen(false); fab.focus(); } });
})();
