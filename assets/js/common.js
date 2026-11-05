/* ZENIT – közös interakciók */
(() => {
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const hdr = document.getElementById('hdr');

  // --- fejléc: a mögötte lévő szakasz témája szerint vált (sötét/világos), lefelé görgetéskor elrejtődik
  let lastY = scrollY;
  function headerTheme() {
    const y = 40, x = innerWidth / 2;
    hdr.style.pointerEvents = 'none';
    let el = document.elementFromPoint(x, y + 39); hdr.style.pointerEvents = '';
    let theme = 'light';
    while (el && el !== document.body) {
      if (el.dataset && el.dataset.theme) { theme = el.dataset.theme === 'dark' ? 'dark' : 'light'; break; }
      if (el.classList && (el.classList.contains('hero') || el.classList.contains('band') || el.classList.contains('img'))) { theme = 'over'; break; }
      el = el.parentElement;
    }
    if (document.body.classList.contains('dark-body') && theme === 'light' && !el) theme = 'dark';
    hdr.classList.toggle('light', theme === 'light');
    hdr.classList.toggle('dark', theme === 'dark');
    const dy = scrollY - lastY;
    if (scrollY > 400 && dy > 6 && !document.body.dataset.nohide) hdr.classList.add('hide');
    else if (dy < -6 || scrollY < 400) hdr.classList.remove('hide');
    lastY = scrollY;
  }
  addEventListener('scroll', headerTheme, { passive: true }); addEventListener('resize', headerTheme); headerTheme();

  // --- mobil menü
  const mn = document.getElementById('mnav');
  $$('[data-menu]').forEach(b => b.onclick = () => mn.classList.toggle('open'));

  // --- megjelenés görgetéskor
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .14, rootMargin: '0px 0px -6% 0px' });
  $$('.reveal,.lines').forEach(el => io.observe(el));

  // --- háttérvideók: csak láthatóan játszanak
  const vio = new IntersectionObserver(es => es.forEach(e => {
    const v = e.target;
    if (e.isIntersecting) { if (v.dataset.src && !v.src) { v.src = v.dataset.src; } v.play().catch(() => {}); } else v.pause();
  }), { threshold: .05 });
  $$('video[data-bg]').forEach(v => { v.muted = true; v.loop = true; v.playsInline = true; vio.observe(v); });

  // --- számláló
  const cio = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return; cio.unobserve(e.target);
    const el = e.target, to = parseFloat(el.dataset.count), dec = (el.dataset.count.split('.')[1] || '').length, t0 = performance.now(), D = 1600;
    const fmt = v => v.toLocaleString('hu-HU', { minimumFractionDigits: dec, maximumFractionDigits: dec });
    (function f(t) { const k = Math.min(1, (t - t0) / D), e2 = 1 - Math.pow(1 - k, 3); el.textContent = fmt(to * e2); if (k < 1) requestAnimationFrame(f); })(t0);
  }), { threshold: .5 });
  $$('[data-count]').forEach(el => cio.observe(el));

  // --- parallax a média sávokban + dinamikus háttérszín
  const bands = $$('.band .media, [data-parallax]');
  const dyn = $$('[data-bgc]');
  const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  function onScroll() {
    const H = innerHeight;
    bands.forEach(m => { const r = m.parentElement.getBoundingClientRect(); if (r.bottom < 0 || r.top > H) return; const k = (r.top + r.height / 2 - H / 2) / H; m.style.transform = `translate3d(0,${(-k * 9).toFixed(2)}%,0)`; });
    if (dyn.length) {
      // a képernyő közepén lévő két szomszédos szakasz színe között interpolálunk
      let col = null;
      for (let i = 0; i < dyn.length; i++) {
        const r = dyn[i].getBoundingClientRect();
        if (r.top <= H * .55 && r.bottom > H * .55) {
          const a = hex(dyn[i].dataset.bgc), nx = dyn[i + 1], k = Math.max(0, Math.min(1, (H * .55 - r.top) / r.height));
          const b = nx ? hex(nx.dataset.bgc) : a, kk = Math.max(0, (k - .7) / .3);
          col = a.map((v, j) => Math.round(v + (b[j] - v) * kk));
          const dark = (col[0] * .3 + col[1] * .59 + col[2] * .11) < 110;
          document.body.style.setProperty('--dyn-fg', dark ? '#EDE6DA' : '#1E1A16');
          break;
        }
      }
      if (col) document.body.style.backgroundColor = `rgb(${col})`;
    }
  }
  if (bands.length || dyn.length) { addEventListener('scroll', onScroll, { passive: true }); onScroll(); }

  // --- scrollytelling (sticky képváltás)
  $$('.scrolly').forEach(sc => {
    const figs = $$('.stage figure', sc), steps = $$('.step', sc), prog = $$('.prog i', sc);
    const sio = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return; const i = steps.indexOf(e.target);
      figs.forEach((f, j) => f.classList.toggle('on', j === i)); prog.forEach((p, j) => p.classList.toggle('on', j === i));
    }), { threshold: .55 });
    steps.forEach(s => sio.observe(s));
  });

  // --- előtte / utána
  $$('.ba').forEach(ba => {
    const b = ba.querySelector('.before'), h = ba.querySelector('.handle');
    const set = x => { const r = ba.getBoundingClientRect(); const p = Math.min(1, Math.max(0, (x - r.left) / r.width)) * 100; b.style.clipPath = `inset(0 ${100 - p}% 0 0)`; h.style.left = p + '%'; };
    // első megjelenéskor egy lágy „lebbenés”, hogy látszódjon: húzható
    const setP = p => { b.style.clipPath = `inset(0 ${100 - p}% 0 0)`; h.style.left = p + '%'; };
    let touched = false;
    const hio = new IntersectionObserver(es => { if (!es[0].isIntersecting) return; hio.disconnect(); const t0 = performance.now();
      (function an(t) { if (touched) return; const k = (t - t0) / 2200; if (k > 1) return setP(50); setP(50 + Math.sin(k * Math.PI * 2) * 22 * (1 - k)); requestAnimationFrame(an); })(t0); }, { threshold: .6 });
    hio.observe(ba);
    let d = false; ba.addEventListener('pointerdown', e => { d = true; touched = true; set(e.clientX); }); addEventListener('pointerup', () => d = false); addEventListener('pointermove', e => d && set(e.clientX));
  });

  // --- galéria szűrő
  $$('.chips').forEach(ch => ch.addEventListener('click', e => {
    const b = e.target.closest('.chip'); if (!b) return;
    $$('.chip', ch).forEach(x => x.classList.toggle('on', x === b));
    const f = b.dataset.f; $$('.masonry figure').forEach(fg => fg.style.display = (f === '*' || fg.dataset.k === f) ? '' : 'none');
  }));

  // --- választógombok, kapcsolók
  $$('.slots button').forEach(b => b.addEventListener('click', () => { $$('button', b.parentNode).forEach(x => x.classList.remove('on')); b.classList.add('on'); }));

  // --- mentett tervek száma a fejlécben
  try { const n = JSON.parse(localStorage.getItem('zenitPlans') || '[]').length; $$('.plan i').forEach(i => { i.textContent = n; i.style.display = n ? '' : 'none'; }); } catch (e) { }
})();

/* ZENIT – süti-hozzájárulás: „Nálunk a süti is méretre szabott.” */
(() => {
  const KEY = 'zenitConsent';
  const read = () => { try { const c = JSON.parse(localStorage.getItem(KEY) || 'null'); if (c && Date.now() - c.ts < 365 * 864e5) return c; } catch (e) { } return null; };
  const save = (stat, mkt) => { try { localStorage.setItem(KEY, JSON.stringify({ v: 1, stat, mkt, ts: Date.now() })); } catch (e) { } };
  const icon = '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 5a19 19 0 1 0 19 19 6 6 0 0 1-7.6-5.8A6 6 0 0 1 29 12.6 6 6 0 0 1 24 5z" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="17" cy="20" r="2" fill="currentColor"/><circle cx="27" cy="30" r="2" fill="currentColor"/><circle cx="16" cy="31" r="1.4" fill="currentColor"/><path d="M8 40h32" stroke="currentColor" stroke-width="1.2" opacity=".5"/></svg>';
  const el = document.createElement('div'); el.className = 'ck'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-live', 'polite'); el.setAttribute('aria-label', 'Süti-beállítások');
  el.innerHTML = `<div class="ck-in"><div class="ck-ic">${icon}</div><div class="ck-tx">
    <div class="ck-k">Süti, méretre szabva</div>
    <p>Csak azt tároljuk, ami a tervezőhöz kell – a mentett terveidet. Statisztikát és hirdetési sütit csak az engedélyeddel használnánk, és most egyáltalán nem használunk. <a href="suti.html">Részletek</a></p>
    <div class="ck-opts" hidden>
      <label class="ck-o"><span><b>Szükséges</b><small>Mentett tervek, a döntésed megjegyzése</small></span><input type="checkbox" checked disabled><i></i></label>
      <label class="ck-o"><span><b>Statisztika</b><small>Anonim látogatottság – jelenleg ki van kapcsolva</small></span><input type="checkbox" data-k="stat"><i></i></label>
      <label class="ck-o"><span><b>Marketing</b><small>Hirdetések mérése – jelenleg ki van kapcsolva</small></span><input type="checkbox" data-k="mkt"><i></i></label>
    </div>
    <div class="ck-acts"><button class="btn fill" data-a="all">Mindet engedem</button><button class="btn" data-a="nec">Csak a szükséges</button><button class="ck-link" data-a="set">Beállítások</button></div>
  </div></div>`;
  const show = full => {
    if (!el.isConnected) document.body.appendChild(el);
    const c = read(); el.querySelector('[data-k=stat]').checked = !!(c && c.stat); el.querySelector('[data-k=mkt]').checked = !!(c && c.mkt);
    el.querySelector('.ck-opts').hidden = !full; el.querySelector('[data-a=set]').textContent = full ? 'Mentés' : 'Beállítások';
    requestAnimationFrame(() => el.classList.add('on'));
  };
  const hide = () => { el.classList.remove('on'); };
  el.addEventListener('click', e => {
    const a = e.target.closest('[data-a]'); if (!a) return;
    if (a.dataset.a === 'all') { save(true, true); hide(); }
    else if (a.dataset.a === 'nec') { save(false, false); hide(); }
    else if (el.querySelector('.ck-opts').hidden) show(true);
    else { save(el.querySelector('[data-k=stat]').checked, el.querySelector('[data-k=mkt]').checked); hide(); }
  });
  document.addEventListener('click', e => { if (e.target.closest('[data-cookie-settings]')) { e.preventDefault(); show(true); } });
  if (!read() && !/[?&]nocookie/.test(location.search)) setTimeout(() => show(false), 1400);
})();

/* közösségi ikonok: a ZENIT kitalált márka, a fiókok látványelemek – kattintásra rövid jelzés, nem visz idegen profilra */
(function () {
  var names = { instagram: "Instagram", facebook: "Facebook", x: "X", youtube: "YouTube" }, box, tm;
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-social]"); if (!a) return;
    e.preventDefault();
    if (!box) { box = document.createElement("div"); box.className = "stoast"; box.setAttribute("role", "status"); document.body.appendChild(box); }
    box.innerHTML = "<b>@zenit.atelier · " + names[a.getAttribute("data-social")] + "</b><br>A ZENIT kitalált márka, ez a fiók csak a bemutató része. A projektvideó a weboldal „A projektről” oldalán nézhető meg.";
    box.classList.add("on"); clearTimeout(tm); tm = setTimeout(function () { box.classList.remove("on"); }, 4200);
  });
})();
