/* ZENIT – görgetésre mozgó, stilizált ábrák (összeállás, színváltás, felemelkedés) */
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const el = (n, a = {}, p) => { const e = document.createElementNS(NS, n); for (const k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; };
  const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  const lerp = (a, b, t) => a + (b - a) * t;
  const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  const mix = (a, b, t) => { const x = hex(a), y = hex(b); return `rgb(${x.map((v, i) => Math.round(lerp(v, y[i], t))).join(',')})`; };
  const shade = (h, k) => `rgb(${hex(h).map(v => Math.round(v * k)).join(',')})`;
  const fmt = v => Math.round(v).toLocaleString('hu-HU');

  const stages = [];
  const progress = sec => { const r = sec.getBoundingClientRect(), H = innerHeight; return clamp(-r.top / Math.max(1, r.height - H)); };
  const steps = (sec, n, p) => {
    const li = sec.querySelectorAll('.sfx-steps li'), bar = sec.querySelector('.sfx-bar i');
    const k = Math.min(n - 1, Math.floor(p * n * 0.999)); li.forEach((x, i) => { x.classList.toggle('on', i === k); x.classList.toggle('done', i < k); });
    if (bar) bar.style.transform = `scaleX(${p})`;
  };

  // ------------------------------------------------------------ 1) összeállás (ferde axonometria)
  function assemble(sec) {
    const svg = sec.querySelector('svg'), W = 2464, H = 530, D = 560, t = 18, K = 0.5, A = 35 * Math.PI / 180;
    const P = (x, y, z) => [x + z * K * Math.cos(A), -y - z * K * Math.sin(A)];
    const pts = a => a.map(q => P(...q).map(v => v.toFixed(1)).join(',')).join(' ');
    const PAPER = { f: '#F7F2EA', t: '#ECE4D7', s: '#DED4C5' }, KAS = { f: '#CDBFAE', t: '#DCD0C1', s: '#B5A795' };
    const parts = {};
    const boxp = (id, x0, x1, y0, y1, z0, z1, col = PAPER) => {
      const g = el('g', { class: 'pt' }, svg);
      el('polygon', { points: pts([[x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]]), fill: col.t }, g);
      el('polygon', { points: pts([[x1, y0, z0], [x1, y0, z1], [x1, y1, z1], [x1, y1, z0]]), fill: col.s }, g);
      el('polygon', { points: pts([[x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0]]), fill: col.f }, g);
      parts[id] = g; return g;
    };
    // árnyék a padlón
    const sh = el('polygon', { points: pts([[-40, -4, -60], [W + 60, -4, -60], [W + 60, -4, D + 40], [-40, -4, D + 40]]), fill: 'rgba(30,24,18,.10)', filter: 'url(#sfxBlur)' }, svg);
    const defs = el('defs', {}, svg); const f = el('filter', { id: 'sfxBlur', x: '-20%', y: '-20%', width: '140%', height: '140%' }, defs); el('feGaussianBlur', { stdDeviation: 18 }, f);
    svg.insertBefore(defs, svg.firstChild);
    boxp('back', 0, W, 0, H, D - 3, D);
    boxp('bottom', t, W - t, 0, t, 0, D - 3);
    boxp('left', 0, t, 0, H - t, 0, D);
    boxp('shelf', W / 3 + t / 2, 2 * W / 3 - t / 2, H / 2 - t / 2, H / 2 + t / 2, 20, D - 3);
    boxp('div1', W / 3 - t / 2, W / 3 + t / 2, t, H - t, 0, D - 3);
    boxp('div2', 2 * W / 3 - t / 2, 2 * W / 3 + t / 2, t, H - t, 0, D - 3);
    boxp('right', W - t, W, 0, H - t, 0, D);
    boxp('top', 0, W, H - t, H, 0, D);
    // LED-csík (fény) a tetőlap alatt
    const led = el('g', { class: 'pt' }, svg);
    for (let i = 0; i < 3; i++) { const xa = i * W / 3 + 40, xb = (i + 1) * W / 3 - 40; el('polygon', { points: pts([[xa, H - t - 6, 30], [xb, H - t - 6, 30], [xb, H - t - 60, 30], [xa, H - t - 60, 30]]), fill: 'rgba(255,214,150,.55)' }, led); }
    parts.led = led;
    for (let i = 0; i < 3; i++) {
      const g = boxp('door' + i, i * W / 3 + 2, (i + 1) * W / 3 - 2, 0, H, -20, -2, KAS);
      const hx0 = (i + .5) * W / 3 - 96; el('polygon', { points: pts([[hx0, 8, -22], [hx0 + 192, 8, -22], [hx0 + 192, 30, -22], [hx0, 30, -22]]), fill: '#B9BDBF' }, g);
    }
    svg.querySelectorAll('polygon').forEach(p => { if (!p.getAttribute('filter')) { p.setAttribute('stroke', '#3A332C'); p.setAttribute('stroke-width', '1.25'); p.setAttribute('vector-effect', 'non-scaling-stroke'); p.setAttribute('stroke-linejoin', 'round'); } });
    // méretvonalak
    const dim = el('g', { class: 'dim', opacity: 0 }, svg);
    const [ax, ay] = P(0, -90, -20), [bx] = P(W, -90, -20);
    el('line', { x1: ax, y1: ay, x2: bx, y2: ay, stroke: '#A27D4A', 'stroke-width': 2.5 }, dim);
    [ax, bx].forEach(x => el('line', { x1: x, y1: ay - 22, x2: x, y2: ay + 22, stroke: '#A27D4A', 'stroke-width': 2.5 }, dim));
    const tw = el('text', { x: (ax + bx) / 2, y: ay + 72, 'text-anchor': 'middle', class: 'sfx-num' }, dim); tw.textContent = '2464 mm';
    const [cx, cy0] = P(-110, 0, -20), [, cy1] = P(-110, H, -20);
    el('line', { x1: cx, y1: cy0, x2: cx, y2: cy1, stroke: '#A27D4A', 'stroke-width': 2.5 }, dim);
    [cy0, cy1].forEach(y => el('line', { x1: cx - 22, y1: y, x2: cx + 22, y2: y, stroke: '#A27D4A', 'stroke-width': 2.5 }, dim));
    const th = el('text', { x: cx - 40, y: (cy0 + cy1) / 2 + 14, 'text-anchor': 'end', class: 'sfx-num' }, dim); th.textContent = '530 mm';
    const [vx0, vy1] = P(-420, H + 60, D), [vx1] = P(W + 120, 0, D), [, vy0] = P(0, -260, -60);
    svg.setAttribute('viewBox', `${vx0} ${vy1 - 40} ${vx1 - vx0 + 60} ${vy0 - vy1 + 60}`);
    // csoportok: [alkatrészek, beúszás iránya (mm)]
    const G = [[['bottom'], [0, -700, 0]], [['left', 'right'], [0, 0, 0], { left: [-900, 0, 0], right: [900, 0, 0] }], [['div1', 'div2'], [0, 800, 0]],
      [['top'], [0, 900, 0]], [['back', 'shelf'], [0, 0, 1400], { shelf: [0, 0, -900] }], [['led'], [0, 0, 0]], [['door0', 'door1', 'door2'], [0, 0, -1300]]];
    const cap = sec.querySelector('.sfx-cap');
    const CAPS = ['Fenéklap és tiplik', 'Oldallapok – konfirmáttal', 'Közfalak a tiplikre', 'Tetőlap', 'Hátfal és polc', 'Belső fény', 'Ajtók – csendes pántokon', 'Kész. 2464 × 530 mm, a plafonig.'];
    return p => {
      const a = 0.04, b = 0.86, n = G.length;
      G.forEach(([ids, dir, per], gi) => {
        const lp = ease(clamp(((p - a) / (b - a)) * n - gi));
        ids.forEach(id => { const d = (per && per[id]) || dir, [sx, sy] = P(d[0] * (1 - lp), d[1] * (1 - lp), d[2] * (1 - lp)), [ox, oy] = P(0, 0, 0);
          const g = parts[id]; g.setAttribute('transform', `translate(${(sx - ox).toFixed(1)} ${(sy - oy).toFixed(1)})`); g.style.opacity = clamp(lp * 1.6);
          g.classList.toggle('hl', lp > 0 && lp < 1); });
      });
      const k = clamp(((p - a) / (b - a)) * n, 0, n - .001);
      parts.led.style.opacity = clamp(((p - a) / (b - a)) * n - 5) * (1 - 0.65 * clamp(((p - a) / (b - a)) * n - 6));
      const dp = clamp((p - b) / 0.08); dim.setAttribute('opacity', dp); tw.textContent = fmt(2464 * ease(dp)) + ' mm'; th.textContent = fmt(530 * ease(dp)) + ' mm';
      sh.style.opacity = clamp(p * 3);
      const ci = p >= b ? 7 : Math.floor(k); if (cap && cap.dataset.i != ci) { cap.dataset.i = ci; cap.textContent = CAPS[ci]; }
      steps(sec, 8, p);
    };
  }

  // ------------------------------------------------------------ 2) színváltás (elölnézet a meglévő szekrénnyel)
  function palette(sec) {
    const svg = sec.querySelector('svg'), S = JSON.parse(sec.dataset.stops);
    const BW = 2500, BH = 2050, TH = 530, C = BH + TH + 10, X0 = 0;
    svg.setAttribute('viewBox', `-260 ${-C - 160} ${BW + 520} ${C + 360}`);
    const Y = y => -y;
    const wall = el('rect', { x: -260, y: -C - 160, width: BW + 520, height: C + 160, fill: '#E9E2D6' }, svg);
    el('rect', { x: -260, y: 0, width: BW + 520, height: 200, fill: '#8F7A64' }, svg);
    el('line', { x1: -260, y1: Y(C), x2: BW + 260, y2: Y(C), stroke: '#A27D4A', 'stroke-width': 5, 'stroke-dasharray': '26 18' }, svg);
    const pl = el('text', { x: -230, y: Y(C) - 26, class: 'sfx-lbl' }, svg); pl.textContent = 'PLAFON';
    // alsó szekrény (ELIA jelleg)
    const bc = '#CDBFAE';
    el('rect', { x: X0, y: Y(BH), width: BW, height: BH, fill: bc, stroke: '#3A332C', 'stroke-width': 4 }, svg);
    const mg = el('linearGradient', { id: 'sfxMir', x1: 0, y1: 0, x2: 0, y2: 1 }, el('defs', {}, svg));
    el('stop', { offset: 0, 'stop-color': '#9FA8AB' }, mg); el('stop', { offset: 1, 'stop-color': '#D5DADB' }, mg);
    el('rect', { x: BW * .36, y: Y(BH - 30), width: BW * .28, height: BH - 60, fill: 'url(#sfxMir)', stroke: '#3A332C', 'stroke-width': 3 }, svg);
    [.36, .64].forEach(k => el('line', { x1: BW * k, y1: Y(BH), x2: BW * k, y2: 0, stroke: '#3A332C', 'stroke-width': 3 }, svg));
    [.18, .4, .62, .84].forEach(k => { el('line', { x1: 0, y1: Y(BH * k), x2: BW * .36, y2: Y(BH * k), stroke: '#9A9C9C', 'stroke-width': 6 }, svg); el('line', { x1: BW * .64, y1: Y(BH * k), x2: BW, y2: Y(BH * k), stroke: '#9A9C9C', 'stroke-width': 6 }, svg); });
    // a ZENIT
    const doors = [], hs = [];
    for (let i = 0; i < 3; i++) {
      doors.push(el('rect', { x: i * BW / 3 + 4, y: Y(BH + TH), width: BW / 3 - 8, height: TH - 4, stroke: '#3A332C', 'stroke-width': 4 }, svg));
      hs.push(el('rect', { x: (i + .5) * BW / 3 - 96, y: Y(BH + 34), width: 192, height: 22, rx: 11 }, svg));
    }
    const grain = el('g', { opacity: 0 }, svg);
    for (let i = 0; i < 26; i++) { const y = BH + 20 + (i * 19.7) % (TH - 30); el('path', { d: `M 10 ${Y(y)} C ${BW * .3} ${Y(y + 8)}, ${BW * .6} ${Y(y - 8)}, ${BW - 10} ${Y(y + 3)}`, stroke: '#7A5A35', 'stroke-width': 2, fill: 'none', opacity: .35 }, grain); }
    const name = sec.querySelector('.sfx-cap');
    return p => {
      const n = S.length, f = clamp(p * 1.04) * (n - 1), i = Math.min(n - 2, Math.floor(f)), tt = ease(clamp((f - i - .2) / .6));
      const c = mix(S[i][1], S[i + 1][1], tt);
      doors.forEach(d => d.setAttribute('fill', c));
      const dark = (() => { const m = c.match(/\d+/g).map(Number); return m[0] * .3 + m[1] * .59 + m[2] * .11 < 110; })();
      hs.forEach(h => h.setAttribute('fill', dark ? '#B08D57' : '#AEB2B4'));
      const isOak = (k) => S[k][2] === 'oak';
      grain.setAttribute('opacity', (isOak(i) ? 1 - tt : 0) + (isOak(i + 1) ? tt : 0));
      wall.setAttribute('fill', mix('#E9E2D6', dark ? '#D9D0C2' : '#E9E2D6', .6));
      const cur = Math.round(f); if (name && name.dataset.i != cur) { name.dataset.i = cur; name.textContent = S[cur][0]; }
      steps(sec, n, p);
    };
  }

  // ------------------------------------------------------------ 3) felemelkedés: a hiányzó fél méter
  function rise(sec) {
    const svg = sec.querySelector('svg'), BW = 2500, BH = 2050, C = 2590, TH = 530;
    svg.setAttribute('viewBox', `-500 ${-C - 220} ${BW + 1700} ${C + 360}`);
    const Y = y => -y;
    el('rect', { x: -500, y: -C - 220, width: BW + 1700, height: C + 220, fill: '#E6DED1' }, svg);
    el('rect', { x: -500, y: 0, width: BW + 1700, height: 140, fill: '#7E6A55' }, svg);
    el('line', { x1: -500, y1: Y(C), x2: BW + 1200, y2: Y(C), stroke: '#A27D4A', 'stroke-width': 5, 'stroke-dasharray': '26 18' }, svg);
    const pl = el('text', { x: -460, y: Y(C) - 30, class: 'sfx-lbl' }, svg); pl.textContent = 'PLAFON';
    el('rect', { x: 0, y: Y(BH), width: BW, height: BH, fill: '#CDBFAE', stroke: '#3A332C', 'stroke-width': 4 }, svg);
    [1 / 3, 2 / 3].forEach(k => el('line', { x1: BW * k, y1: Y(BH), x2: BW * k, y2: 0, stroke: '#3A332C', 'stroke-width': 3 }, svg));
    // dobozok a tetején (eltűnnek)
    const clutter = el('g', {}, svg);
    [[120, 520, 300, '#B48A62'], [700, 420, 220, '#C9B79C'], [1180, 640, 360, '#8E6E52'], [1900, 460, 260, '#BCA88C']].forEach(([x, w, h, c]) => el('rect', { x, y: Y(BH + h), width: w, height: h, fill: c, stroke: '#3A332C', 'stroke-width': 3 }, clutter));
    const top = el('g', {}, svg);
    const body = el('rect', { x: 0, width: BW, fill: '#CDBFAE', stroke: '#3A332C', 'stroke-width': 4 }, top);
    const dl = [1, 2].map(i => el('line', { x1: i * BW / 3, x2: i * BW / 3, stroke: '#3A332C', 'stroke-width': 3 }, top));
    const hs = [0, 1, 2].map(i => el('rect', { x: (i + .5) * BW / 3 - 96, width: 192, height: 22, rx: 11, fill: '#AEB2B4' }, top));
    // mérés
    const g = el('g', {}, svg), mx = BW + 200;
    const ln = el('line', { x1: mx, x2: mx, stroke: '#A27D4A', 'stroke-width': 4 }, g);
    const t1 = el('line', { x1: mx - 26, x2: mx + 26, stroke: '#A27D4A', 'stroke-width': 4 }, g), t2 = el('line', { x1: mx - 26, x2: mx + 26, stroke: '#A27D4A', 'stroke-width': 4 }, g);
    const num = el('text', { x: mx + 60, class: 'sfx-num big' }, g), sub = el('text', { x: mx + 60, class: 'sfx-lbl' }, g);
    const cap = sec.querySelector('.sfx-cap');
    return p => {
      const c = ease(clamp(p / 0.3)); clutter.style.opacity = 1 - c; clutter.setAttribute('transform', `translate(0 ${(-c * 120).toFixed(1)})`);
      const r = ease(clamp((p - 0.3) / 0.5)), h = Math.max(1, (TH) * r);
      body.setAttribute('y', Y(BH + h)); body.setAttribute('height', h);
      dl.forEach(l => { l.setAttribute('y1', Y(BH + h)); l.setAttribute('y2', Y(BH)); l.style.opacity = clamp((r - .6) / .4); });
      hs.forEach(x => { x.setAttribute('y', Y(BH + 34)); x.style.opacity = clamp((r - .75) / .25); });
      top.style.opacity = clamp(r * 4);
      const gap = C - BH - h; ln.setAttribute('y1', Y(BH + h)); ln.setAttribute('y2', Y(C)); t1.setAttribute('y1', Y(C)); t1.setAttribute('y2', Y(C)); t2.setAttribute('y1', Y(BH + h)); t2.setAttribute('y2', Y(BH + h));
      num.setAttribute('y', Y(BH + h + gap / 2) + 30); num.textContent = fmt(gap) + ' mm'; sub.setAttribute('y', Y(BH + h + gap / 2) + 90);
      sub.textContent = gap > 20 ? 'RÉS A PLAFONIG' : 'ENNYI MARAD – PORFOGÓ NÉLKÜL';
      const ci = p < .3 ? 0 : p < .8 ? 1 : 2; if (cap && cap.dataset.i != ci) { cap.dataset.i = ci; cap.textContent = ['Ma: dobozok és por a szekrény tetején.', 'A ZENIT felnő a plafonig…', '…és 10 mm-re megáll.'][ci]; }
      steps(sec, 3, p);
    };
  }

  const KIND = { assemble, palette, rise };
  document.querySelectorAll('[data-sfx]').forEach(sec => { const f = KIND[sec.dataset.sfx]; if (f) stages.push([sec, f(sec)]); });
  if (!stages.length) return;
  let req = 0;
  const tick = () => { req = 0; stages.forEach(([sec, fn]) => { const r = sec.getBoundingClientRect(); if (r.bottom < -50 || r.top > innerHeight + 50) return; fn(progress(sec)); }); };
  addEventListener('scroll', () => { if (!req) req = requestAnimationFrame(tick); }, { passive: true });
  addEventListener('resize', tick); stages.forEach(([s, fn]) => fn(progress(s)));
})();
