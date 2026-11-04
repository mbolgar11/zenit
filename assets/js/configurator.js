/* ZENIT tervező – élő 3D (three.js r147, klasszikus script, file:// alatt is fut). Mértékegység: méter. */
(function () {
  const $ = id => document.getElementById(id);
  const cv = $('cfg3d'); if (!cv || !window.THREE) return;
  const T = THREE;

  // ---------------- állapot
  const st = {
    w: 250, ceil: 259, baseH: 205, d: 60, doors: 5, split: 'eq',
    ajto: '#CDBFAE', korpusz: '#CDBFAE', belso: '#F1EFEA', part: 'ajto',
    fin: 'matt', handle: 'edge', hcol: '#C9C6C0', shelves: new Set([3]),
    led: true, trim: false, box: false, env: 'room', open: false, baseCol: '#CDBFAF'
  };
  const UNI = [['Kréta', '#F1EFEA'], ['Kasmír', '#CDBFAE'], ['Homok', '#D8CBB3'], ['Zsálya', '#A4AD98'],
               ['Agyag', '#A7735A'], ['Grafit', '#4A4846'], ['Éjkék', '#273445'], ['Fekete', '#1B1A19']];
  const WOOD = [['Natúr tölgy', 'oak', '#B08757'], ['Füstölt tölgy', 'smoked', '#57432F'], ['Dió', 'walnut', '#664631']];
  const STONE = [['Beton', 'concrete', '#958F88'], ['Len', 'linen', '#D3CABB']];
  const TEXCSS = { oak: 'img-oak', smoked: 'img-smoked', walnut: 'img-walnut', concrete: 'img-concrete', linen: 'img-linen' };

  // presetek az inspirációs oldalról (#preset=...)
  const PRESETS = {
    kasmir: {}, kreta: { ajto: '#F1EFEA', korpusz: '#F1EFEA' }, tolgy: { ajto: 'oak', korpusz: 'oak', hcol: '#1E1E1E' },
    grafit: { ajto: 'walnut', korpusz: '#4A4846', hcol: '#1E1E1E' }, zsalya: { ajto: '#A4AD98', korpusz: '#A4AD98', hcol: '#B08D57' },
    ejkek: { ajto: '#273445', korpusz: '#273445', hcol: '#B08D57' }, led: { open: true }
  };
  const m = location.hash.match(/preset=(\w+)/); if (m && PRESETS[m[1]]) Object.assign(st, PRESETS[m[1]]);

  // ---------------- procedurális textúrák (canvas → nincs fájlbetöltés)
  function canvasTex(kind) {
    const c = document.createElement('canvas'); c.width = 512; c.height = 512; const g = c.getContext('2d');
    const rnd = (a, b) => a + Math.random() * (b - a);
    if (kind === 'concrete' || kind === 'linen') {
      g.fillStyle = kind === 'concrete' ? '#9a958e' : '#d6cdbe'; g.fillRect(0, 0, 512, 512);
      const id = g.getImageData(0, 0, 512, 512), px = id.data;
      for (let i = 0; i < px.length; i += 4) {
        const x = (i / 4) % 512, y = (i / 4 / 512) | 0;
        let n = kind === 'concrete' ? rnd(-18, 18) : ((x % 3 === 0) ^ (y % 3 === 0) ? -14 : 6) + rnd(-6, 6);
        px[i] += n; px[i + 1] += n; px[i + 2] += n;
      }
      g.putImageData(id, 0, 0);
    } else {
      const P = { oak: ['#B48A57', '#9C7444', '#C39B69'], smoked: ['#4F3D2E', '#3E2F23', '#604A38'], walnut: ['#5E4130', '#4A3122', '#73523A'] }[kind];
      g.fillStyle = P[0]; g.fillRect(0, 0, 512, 512);
      for (let k = 0; k < 180; k++) {
        let x = rnd(0, 512); const w = rnd(0.6, 3.2); g.strokeStyle = Math.random() < .5 ? P[1] : P[2];
        g.globalAlpha = rnd(.15, .55); g.lineWidth = w; g.beginPath(); g.moveTo(x, 0);
        for (let y = 0; y <= 512; y += 16) { x += rnd(-1.6, 1.6) + Math.sin(y / 60 + k) * .6; g.lineTo(x, y); }
        g.stroke();
      }
      g.globalAlpha = 1;
    }
    const t = new T.CanvasTexture(c); t.wrapS = t.wrapT = T.RepeatWrapping; t.encoding = T.sRGBEncoding; t.anisotropy = 4;
    return t;
  }
  const TEX = {}; const tex = k => TEX[k] || (TEX[k] = canvasTex(k));

  const FIN = { matt: [0.75, 0.0], satin: [0.42, 0.25], gloss: [0.14, 0.9] };
  function surfMat(spec) {
    const [r, cc] = FIN[st.fin];
    const o = { roughness: r, metalness: 0, clearcoat: cc, clearcoatRoughness: 0.2 };
    if (TEXCSS[spec]) { o.map = tex(spec); o.color = new T.Color('#ffffff'); }
    else o.color = new T.Color(spec);
    return new T.MeshPhysicalMaterial(o);
  }

  // ---------------- renderer, jelenet
  const R = new T.WebGLRenderer({ canvas: cv, antialias: true, preserveDrawingBuffer: true });
  R.outputEncoding = T.sRGBEncoding; R.toneMapping = T.ACESFilmicToneMapping; R.toneMappingExposure = 1.05;
  R.shadowMap.enabled = true; R.shadowMap.type = T.PCFSoftShadowMap; R.setPixelRatio(Math.min(2, devicePixelRatio));
  const S = new T.Scene();
  const cam = new T.PerspectiveCamera(32, 1, 0.05, 60);
  const ctl = new T.OrbitControls(cam, cv); ctl.enableDamping = true; ctl.dampingFactor = 0.08;
  ctl.minDistance = 1.2; ctl.maxDistance = 9; ctl.maxPolarAngle = Math.PI * 0.62;
  const hemi = new T.HemisphereLight('#fff6ea', '#3a332c', 0.55); S.add(hemi);
  const key = new T.DirectionalLight('#fff1e0', 1.25); key.position.set(-2.5, 4.5, 4.0); key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048); Object.assign(key.shadow.camera, { left: -4, right: 4, top: 4, bottom: -1, near: 0.5, far: 15 }); S.add(key);
  const fill = new T.DirectionalLight('#dfe7f2', 0.35); fill.position.set(4, 2, 3); S.add(fill);
  const room = new T.Group(), model = new T.Group(); S.add(room, model);
  let doors = [], ledLights = [];

  const box = (w, h, d, mat, x, y, z, shadow = true) => {
    const me = new T.Mesh(new T.BoxGeometry(w, h, d), mat); me.position.set(x, y, z);
    me.castShadow = shadow; me.receiveShadow = true; return me;
  };
  const clear = g => { while (g.children.length) { const c = g.children.pop(); c.traverse(o => { o.geometry && o.geometry.dispose(); }); } };

  function buildRoom() {
    clear(room);
    const W = st.w / 100, BH = st.baseH / 100, C = st.ceil / 100, D = st.d / 100;
    if (st.env === 'studio') {
      S.background = new T.Color('#151311'); hemi.intensity = 0.6;
      const fl = new T.Mesh(new T.CircleGeometry(6, 64), new T.MeshStandardMaterial({ color: '#0f0d0b', roughness: 0.95 }));
      fl.rotation.x = -Math.PI / 2; fl.position.y = BH - 0.002; fl.receiveShadow = true; room.add(fl);
      return;
    }
    S.background = new T.Color('#1a1714'); hemi.intensity = 0.55;
    const wall = new T.MeshStandardMaterial({ color: '#E9E4DC', roughness: 0.95 });
    const floorT = tex('oak'); floorT.repeat.set(3, 3);
    const floor = new T.MeshStandardMaterial({ color: '#9b958d', map: floorT, roughness: 0.6 });
    room.add(box(Math.max(8, W + 5), 0.02, 16, floor, W / 2, -0.01, 8 - D, false));
    room.add(box(Math.max(6, W + 3), C, 0.1, wall, W / 2, C / 2, -D - 0.05, false));
    room.add(box(0.1, C, 16, wall, -1.2, C / 2, 8 - D, false));
    const ceil = box(Math.max(8, W + 5), 0.03, 16, new T.MeshStandardMaterial({ color: '#F5F2EC', roughness: 1, emissive: '#7d766c', emissiveIntensity: 0.55 }), W / 2, C + 0.015, 8 - D, false);
    ceil.castShadow = false; room.add(ceil);
    // meglévő szekrény (alatta)
    const bm = new T.MeshStandardMaterial({ color: st.baseCol, roughness: 0.55 });
    const mir = new T.MeshStandardMaterial({ color: '#cfd6da', roughness: 0.05, metalness: 0.9 });
    room.add(box(W, BH - 0.04, D, bm, W / 2, BH / 2 + 0.02, -D / 2));
    room.add(box(W / 3 - 0.004, BH - 0.06, 0.01, mir, W / 2, BH / 2 + 0.02, 0.006));
    [[W / 6], [W * 5 / 6]].forEach(([x]) => [0.4, 0.9, 1.4, 1.9].forEach(z => { if (z < BH) room.add(box(W / 3 - 0.01, 0.008, 0.004, new T.MeshStandardMaterial({ color: '#c4c6c8', metalness: 1, roughness: .3 }), x, z, 0.003, false)); }));
  }

  function doorWidths(W, n) {
    if (st.split !== 'sym' || n < 3) return Array(n).fill(W / n);
    const f = Array.from({ length: n }, (_, i) => (n % 2 ? i === (n - 1) / 2 : (i === n / 2 - 1 || i === n / 2)) ? 1.25 : 1);
    const sum = f.reduce((a, b) => a + b, 0); return f.map(v => v / sum * W);
  }

  function buildModel() {
    clear(model); doors = []; ledLights.forEach(l => S.remove(l)); ledLights = [];
    const W = st.w / 100, BH = st.baseH / 100, H = (st.ceil - st.baseH) / 100 - 0.01, D = st.d / 100, t = 0.018, tb = 0.003, td = 0.018;
    const gv = 0.0045, dp = D - td - tb, n = st.doors;
    const mB = surfMat(st.korpusz), mD = surfMat(st.ajto), mI = surfMat(st.belso);
    const y0 = BH, zc = -D + tb;     // korpusz hátul a hátfalnál; elöl az ajtók síkja
    const zFront = 0;               // ajtó elülső síkja
    const zBodyFront = -td, zBodyBack = zBodyFront - dp;
    const zMid = (zBodyFront + zBodyBack) / 2;
    // oldalak, tető, fenék
    model.add(box(t, H, dp, mB, t / 2, y0 + H / 2, zMid));
    model.add(box(t, H, dp, mB, W - t / 2, y0 + H / 2, zMid));
    model.add(box(W - 2 * t, t, dp, mB, W / 2, y0 + t / 2, zMid));
    model.add(box(W - 2 * t, t, dp, mB, W / 2, y0 + H - t / 2, zMid));
    model.add(box(W, H, tb, mI, W / 2, y0 + H / 2, zBodyBack - tb / 2));
    // ajtóosztás → közfalak
    let ws = doorWidths(W, n), acc = 0; const edges = [0];
    ws.forEach(w => { acc += w; edges.push(acc); });
    for (let i = 1; i < n; i++) model.add(box(t, H - 2 * t, dp, mI, edges[i], y0 + H / 2, zMid));
    // polcok
    for (let i = 0; i < n; i++) {
      if (!st.shelves.has(i + 1)) continue;
      const xa = i === 0 ? t : edges[i] + t / 2, xb = i === n - 1 ? W - t : edges[i + 1] - t / 2;
      model.add(box(xb - xa - 0.002, t, dp - 0.02, mI, (xa + xb) / 2, y0 + H / 2, zMid + 0.01));
      if (st.box) model.add(box(Math.min(0.4, (xb - xa) * 0.7), 0.16, dp * 0.7, new T.MeshStandardMaterial({ color: '#cbbfae', map: tex('linen'), roughness: 1 }), (xa + xb) / 2, y0 + t + 0.08, zMid));
    }
    // LED
    if (st.led) for (let i = 0; i < n; i++) {
      const xa = i === 0 ? t : edges[i] + t / 2, xb = i === n - 1 ? W - t : edges[i + 1] - t / 2;
      model.add(box(xb - xa - 0.04, 0.006, 0.012, new T.MeshBasicMaterial({ color: '#ffe0b0' }), (xa + xb) / 2, y0 + H - t - 0.006, zBodyFront - 0.03, false));
      const L = new T.PointLight('#ffcf94', 0, 0.9, 2); L.position.set((xa + xb) / 2, y0 + H - t - 0.05, zBodyFront - 0.08); S.add(L); ledLights.push(L);
    }
    // plafonzáró léc
    if (st.trim) model.add(box(W, (st.ceil - st.baseH) / 100 - H, 0.018, mB, W / 2, y0 + H + ((st.ceil - st.baseH) / 100 - H) / 2, -0.009));
    // ajtók (zsanér: páratlan a bal, páros a jobb oldalon)
    const hm = new T.MeshStandardMaterial({ color: st.hcol, metalness: st.hcol === '#7A4E2D' ? 0 : 0.9, roughness: st.hcol === '#7A4E2D' ? 0.7 : 0.3 });
    for (let i = 0; i < n; i++) {
      const xa = edges[i] + (i === 0 ? 0.0015 : 0.0015), xb = edges[i + 1] - (i === n - 1 ? 0.0015 : 0.0015);
      const dw = xb - xa, dh = H - 2 * gv, left = i % 2 === 0;
      const piv = new T.Group(); piv.position.set(left ? xa : xb, y0 + gv, zFront - td); model.add(piv);
      const dr = box(dw, dh, td, mD, (left ? 1 : -1) * dw / 2, dh / 2, td / 2); piv.add(dr);
      const cx = (left ? 1 : -1) * dw / 2;
      if (st.handle === 'edge') {
        const L = Math.min(0.225, dw * 0.45);
        piv.add(box(L, 0.004, td + 0.014, hm, cx, -0.002, td / 2 + 0.002));
        const lip = new T.Mesh(new T.CylinderGeometry(0.006, 0.006, L, 20), hm); lip.rotation.z = Math.PI / 2; lip.position.set(cx, -0.006, td + 0.01); piv.add(lip);
      } else if (st.handle === 'bar') {
        const L = Math.min(0.32, dw * 0.6);
        const bar = new T.Mesh(new T.CylinderGeometry(0.006, 0.006, L, 20), hm); bar.rotation.z = Math.PI / 2; bar.position.set(cx, 0.06, td + 0.03); bar.castShadow = true; piv.add(bar);
        [-1, 1].forEach(s => piv.add(box(0.008, 0.008, 0.03, hm, cx + s * (L / 2 - 0.02), 0.06, td + 0.015)));
      } else if (st.handle === 'knob') {
        const k = new T.Mesh(new T.SphereGeometry(0.014, 24, 16), hm); k.position.set((left ? 1 : -1) * (dw - 0.06), 0.06, td + 0.016); k.castShadow = true; piv.add(k);
      }
      piv.userData = { left, ang: 0 }; dr.userData.pivot = piv; doors.push(piv);
    }
    applyOpen(true);
    // méretek kiírása
    $('dimW').textContent = st.w; $('dimH').textContent = Math.round((st.ceil - st.baseH) - 1); $('dimD').textContent = st.d;
    // ár (becslés)
    const p = 89900 + st.w * 480 + n * 9000 + st.shelves.size * 6500 + (st.led ? 24900 : 0) + (st.trim ? 14900 : 0) + (st.box ? 8900 * n : 0)
      + (['oak', 'smoked', 'walnut'].some(k => st.ajto === k || st.korpusz === k) ? 64000 : 0) + (st.fin === 'gloss' ? 19000 : 0);
    $('price').textContent = (Math.round(p / 100) * 100).toLocaleString('hu-HU') + ' Ft';
  }

  function applyOpen(instant) {
    doors.forEach(d => { d.userData.target = st.open ? (d.userData.left ? -1 : 1) * 1.75 : 0; if (instant) d.rotation.y = d.userData.target; });
  }

  function frame() {
    const W = st.w / 100, C = st.ceil / 100, BH = st.baseH / 100;
    const ty = st.env === 'studio' ? (BH + C) / 2 - 0.1 : C * 0.6;
    ctl.target.set(W / 2, ty, -st.d / 200);
    const dist = st.env === 'studio' ? Math.max(4.2, W * 1.5 + 2.6) : Math.max(5.2, W * 1.5 + 3.2);
    cam.position.set(W / 2 + dist * 0.42, Math.min(C - 0.25, ty + 0.3), dist * 0.9); ctl.update();
  }

  function resize() {
    const r = cv.parentElement.getBoundingClientRect();
    R.setSize(r.width, r.height, false); cam.aspect = r.width / r.height; cam.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(cv.parentElement);
  cv.style.width = '100%'; cv.style.height = '100%'; cv.style.display = 'block';

  // ajtó kattintásra nyílik
  const ray = new T.Raycaster(), mp = new T.Vector2(); let down = null;
  cv.addEventListener('pointerdown', e => down = [e.clientX, e.clientY]);
  cv.addEventListener('pointerup', e => {
    if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 4) return;
    const r = cv.getBoundingClientRect(); mp.set((e.clientX - r.left) / r.width * 2 - 1, -(e.clientY - r.top) / r.height * 2 + 1);
    ray.setFromCamera(mp, cam); const hit = ray.intersectObjects(model.children, true).find(h => h.object.userData.pivot);
    if (hit) { const p = hit.object.userData.pivot; p.userData.target = p.userData.target ? 0 : (p.userData.left ? -1 : 1) * 1.75; }
  });

  (function loop() {
    requestAnimationFrame(loop);
    let openAmt = 0;
    doors.forEach(d => { d.rotation.y += (d.userData.target - d.rotation.y) * 0.12; openAmt = Math.max(openAmt, Math.abs(d.rotation.y) / 1.75); });
    ledLights.forEach(l => l.intensity = 1.6 * openAmt);
    ctl.update(); R.render(S, cam);
  })();

  // ---------------- UI
  const rebuild = () => { buildRoom(); buildModel(); };
  const mk = (id, list, isTex) => {
    const g = $(id); list.forEach(it => {
      const b = document.createElement('button'); b.title = it[0];
      if (isTex) b.className = TEXCSS[it[1]]; else b.style.background = it[1];
      b.onclick = () => pick(isTex ? it[1] : it[1], b); g.appendChild(b);
    });
  };
  mk('swUni', UNI); mk('swWood', WOOD, 1); mk('swStone', STONE, 1);
  function pick(spec, btn) {
    document.querySelectorAll('.sw button').forEach(x => x.classList.remove('on')); btn && btn.classList.add('on');
    st[st.part] = spec; const hx = TEXCSS[spec] ? '' : spec; $('hexIn').value = hx || '— textúra —'; $('hexPrev').style.background = hx || '';
    $('hexPrev').className = TEXCSS[spec] || ''; buildModel();
  }
  document.querySelectorAll('#partTabs button').forEach(b => b.onclick = () => {
    document.querySelectorAll('#partTabs button').forEach(x => x.classList.remove('on')); b.classList.add('on'); st.part = b.dataset.part;
    const v = st[st.part]; $('hexIn').value = TEXCSS[v] ? '— textúra —' : v; $('hexPrev').style.background = TEXCSS[v] ? '' : v; $('hexPrev').className = TEXCSS[v] || '';
  });
  $('hexIn').oninput = () => { if (/^#[0-9a-f]{6}$/i.test($('hexIn').value)) pick($('hexIn').value); };
  const group = (id, fn) => document.querySelectorAll('#' + id + ' .opt').forEach(b => b.onclick = () => {
    document.querySelectorAll('#' + id + ' .opt').forEach(x => x.classList.remove('on')); b.classList.add('on'); fn(b); });
  group('depthOpts', b => { st.d = +b.dataset.d; rebuild(); frame(); });
  group('splitOpts', b => { st.split = b.dataset.s; buildModel(); });
  group('finOpts', b => { st.fin = b.dataset.f; buildModel(); });
  group('hcol', b => { st.hcol = b.dataset.c === '#222' ? '#1E1E1E' : b.dataset.c; buildModel(); });
  document.querySelectorAll('#handles .card').forEach(b => b.onclick = () => {
    document.querySelectorAll('#handles .card').forEach(x => x.classList.remove('on')); b.classList.add('on'); st.handle = b.dataset.h; buildModel(); });
  [['xLed', 'led'], ['xTrim', 'trim'], ['xBox', 'box']].forEach(([id, k]) => { const el = $(id); el.classList.toggle('on', st[k]); el.onclick = () => { st[k] = !st[k]; el.classList.toggle('on', st[k]); buildModel(); }; });
  document.querySelectorAll('#envSeg button').forEach(b => b.onclick = () => {
    document.querySelectorAll('#envSeg button').forEach(x => x.classList.remove('on')); b.classList.add('on'); st.env = b.dataset.env; buildRoom(); });
  $('btnOpen').onclick = () => { st.open = !st.open; applyOpen(false); };
  $('btnReset').onclick = frame;
  $('btnFull').onclick = () => { const v = cv.parentElement; document.fullscreenElement ? document.exitFullscreen() : v.requestFullscreen && v.requestFullscreen(); };
  $('btnAR').onclick = () => alert('Az AR-nézet a végleges oldalon érhető el mobilon.');
  $('baseCol').onclick = e => { e.preventDefault(); const c = prompt('Az alatta lévő szekrény színe (HEX):', st.baseCol); if (c && /^#[0-9a-f]{6}$/i.test(c)) { st.baseCol = c; $('baseCol').textContent = 'alatta lévő szekrény színe: ' + c; buildRoom(); } };

  const rec = w => Math.max(1, Math.min(6, Math.ceil(w / 60)));
  function doorsUI() {
    const g = $('doorOpts'); g.innerHTML = ''; const r = rec(st.w); $('doorRec').textContent = r;
    const lo = Math.max(1, Math.ceil(st.w / 75)), hi = Math.min(6, Math.max(lo, Math.floor(st.w / 35)));
    for (let k = lo; k <= hi; k++) {
      const b = document.createElement('button'); b.className = 'opt' + (k === st.doors ? ' on' : ''); b.textContent = k + (k === r ? ' · javasolt' : '');
      b.onclick = () => { st.doors = k; st.shelves = new Set([Math.ceil(k / 2)]); doorsUI(); buildModel(); }; g.appendChild(b);
    }
    const s = $('shelfOpts'); s.innerHTML = '';
    for (let i = 1; i <= st.doors; i++) {
      const b = document.createElement('button'); b.className = 'opt' + (st.shelves.has(i) ? ' on' : ''); b.textContent = i + '. rekesz';
      b.onclick = () => { st.shelves.has(i) ? st.shelves.delete(i) : st.shelves.add(i); b.classList.toggle('on'); buildModel(); }; s.appendChild(b);
    }
  }
  $('w').oninput = () => {
    st.w = +$('w').value; $('wVal').textContent = st.w;
    const lo = Math.ceil(st.w / 75), hi = Math.floor(st.w / 35);
    if (st.doors < lo || st.doors > hi) { st.doors = rec(st.w); st.shelves = new Set([Math.ceil(st.doors / 2)]); }
    doorsUI(); rebuild(); frame();
  };
  $('ceil').oninput = () => { st.ceil = Math.max(+$('ceil').value, st.baseH + 30); $('ceilVal').textContent = st.ceil; rebuild(); };
  $('baseH').oninput = () => { st.baseH = Math.min(+$('baseH').value, st.ceil - 30); $('baseVal').textContent = st.baseH; rebuild(); frame(); };

  // terv mentése
  document.querySelectorAll('[data-save]').forEach(a => a.addEventListener('click', () => {
    try {
      const plans = JSON.parse(localStorage.getItem('zenitPlans') || '[]');
      plans.push({ w: st.w, h: st.ceil - st.baseH - 1, d: st.d, doors: st.doors, ajto: st.ajto, korpusz: st.korpusz, belso: st.belso, fin: st.fin,
        handle: st.handle, hcol: st.hcol, shelves: [...st.shelves], led: st.led, trim: st.trim, box: st.box,
        price: $('price').textContent, img: cv.toDataURL('image/jpeg', 0.7), t: Date.now() });
      localStorage.setItem('zenitPlans', JSON.stringify(plans.slice(-4)));
    } catch (e) { }
  }));

  // kezdés
  if (st.open) applyOpen(false);
  $('hexIn').value = st.ajto; $('hexPrev').style.background = st.ajto;
  doorsUI(); rebuild(); resize(); frame();
  window.zenitCfg = { st, cam, ctl, frame };
})();
