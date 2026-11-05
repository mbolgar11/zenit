/* ZENIT tervező v2 – élő 3D (three.js r147, klasszikus script). Mértékegység: méter.
   Újdonságok: ajtónkénti nyitásirány és tükör, ferde plafon + falkiegyenlítés (0–10 cm), plafon helyett szaggatott plafonvonal,
   szerelési animáció a saját tervből, és letölthető szerelési videó (WebM, feliratokkal). */
(function () {
  const $ = id => document.getElementById(id);
  const cv = $('cfg3d'); if (!cv || !window.THREE) return;
  const T = THREE;
  if (T.ColorManagement) T.ColorManagement.legacyMode = false;

  // ---------------- állapot
  const st = {
    w: 250, ceil: 259, baseH: 205, d: 60, baseD: 60, doors: 5, split: 'eq', slope: 0, wall: 0,
    ajto: '#CDBFAE', korpusz: '#CDBFAE', belso: '#F1EFEA', part: 'ajto',
    fin: 'matt', handle: 'edge', hcol: '#C9C6C0', shelves: new Set([3]),
    led: true, trim: false, box: false, env: 'room', open: false, baseCol: '#CDBFAF',
    hinge: [], mirror: []
  };
  const UNI = [['Kasmír', '#CDBFAE'], ['Kréta', '#F1EFEA'], ['Homok', '#D8CBB3'], ['Zsálya', '#A4AD98'],
               ['Agyag', '#A7735A'], ['Grafit', '#4A4846'], ['Éjkék', '#273445'], ['Fekete', '#1B1A19']];
  const WOOD = [['Natúr tölgy', 'oak'], ['Füstölt tölgy', 'smoked'], ['Dió', 'walnut']];
  const STONE = [['Beton', 'concrete'], ['Len', 'linen']];
  const ISTEX = { oak: 1, smoked: 1, walnut: 1, concrete: 1, linen: 1 };
  const TEXPREV = { oak: '#B48A57', smoked: '#4F3D2E', walnut: '#5E4130', concrete: '#9a958e', linen: '#d6cdbe' };

  const defHinge = n => Array.from({ length: n }, (_, i) => n === 1 ? 'L' : i < n / 2 ? 'L' : 'R');
  const PRESETS = {
    kasmir: {}, kreta: { ajto: '#F1EFEA', korpusz: '#F1EFEA' }, tolgy: { ajto: 'oak', korpusz: 'oak', hcol: '#1E1E1E' },
    grafit: { ajto: 'walnut', korpusz: '#4A4846', hcol: '#1E1E1E' }, zsalya: { ajto: '#A4AD98', korpusz: '#A4AD98', hcol: '#B08D57' },
    ejkek: { ajto: '#273445', korpusz: '#273445', hcol: '#B08D57' }, led: { open: true },
    referencia: { doors: 3, split: 'sym', hinge: ['L', 'R', 'R'], shelves: new Set([2]) }
  };
  const hm = location.hash.match(/preset=(\w+)/); if (hm && PRESETS[hm[1]]) Object.assign(st, PRESETS[hm[1]]);
  if (!st.hinge.length) st.hinge = defHinge(st.doors);
  if (!st.mirror.length) st.mirror = Array(st.doors).fill(false);

  // ---------------- procedurális textúrák
  function canvasTex(kind) {
    const c = document.createElement('canvas'); c.width = 512; c.height = 512; const g = c.getContext('2d');
    let seed = kind.length * 977; const rnd = (a, b) => { seed = (seed * 16807) % 2147483647; return a + (seed / 2147483647) * (b - a); };
    if (kind === 'concrete' || kind === 'linen') {
      g.fillStyle = TEXPREV[kind]; g.fillRect(0, 0, 512, 512);
      const id = g.getImageData(0, 0, 512, 512), px = id.data;
      for (let i = 0; i < px.length; i += 4) {
        const x = (i / 4) % 512, y = (i / 4 / 512) | 0;
        const n = kind === 'concrete' ? rnd(-16, 16) : ((x % 3 === 0) ^ (y % 3 === 0) ? -12 : 5) + rnd(-5, 5);
        px[i] += n; px[i + 1] += n; px[i + 2] += n;
      }
      g.putImageData(id, 0, 0);
    } else {
      const P = { oak: ['#B48A57', '#9C7444', '#C39B69'], smoked: ['#4F3D2E', '#3E2F23', '#604A38'], walnut: ['#5E4130', '#4A3122', '#73523A'] }[kind];
      g.fillStyle = P[0]; g.fillRect(0, 0, 512, 512);
      for (let k = 0; k < 180; k++) {
        let x = rnd(0, 512); g.strokeStyle = rnd(0, 1) < .5 ? P[1] : P[2];
        g.globalAlpha = rnd(.15, .55); g.lineWidth = rnd(0.6, 3.2); g.beginPath(); g.moveTo(x, 0);
        for (let y = 0; y <= 512; y += 16) { x += rnd(-1.6, 1.6) + Math.sin(y / 60 + k) * .6; g.lineTo(x, y); }
        g.stroke();
      }
      g.globalAlpha = 1;
    }
    const t = new T.CanvasTexture(c); t.wrapS = t.wrapT = T.RepeatWrapping; t.encoding = T.sRGBEncoding; t.anisotropy = 4;
    return t;
  }
  const TEX = {}; const tex = k => TEX[k] || (TEX[k] = canvasTex(k));
  const FIN = { matt: [0.72, 0.0], satin: [0.42, 0.25], gloss: [0.14, 0.9] };
  function surfMat(spec) {
    const [r, cc] = FIN[st.fin];
    const o = { roughness: r, metalness: 0, clearcoat: cc, clearcoatRoughness: 0.2, envMapIntensity: 0.55 };
    if (ISTEX[spec]) { o.map = tex(spec); o.color = new T.Color('#ffffff'); } else o.color = new T.Color(spec);
    return new T.MeshPhysicalMaterial(o);
  }

  // ---------------- renderer, jelenet
  const R = new T.WebGLRenderer({ canvas: cv, antialias: true, preserveDrawingBuffer: true });
  R.outputEncoding = T.sRGBEncoding; R.toneMapping = T.ACESFilmicToneMapping; R.toneMappingExposure = 0.65;
  R.shadowMap.enabled = true; R.shadowMap.type = T.PCFSoftShadowMap; R.setPixelRatio(Math.min(2, devicePixelRatio));
  const S = new T.Scene();
  if (T.RoomEnvironment) { const pm = new T.PMREMGenerator(R); S.environment = pm.fromScene(new T.RoomEnvironment(), 0.04).texture; }
  const cam = new T.PerspectiveCamera(32, 1, 0.05, 80);
  const ctl = new T.OrbitControls(cam, cv); ctl.enableDamping = true; ctl.dampingFactor = 0.08;
  ctl.minDistance = 1.2; ctl.maxDistance = 11; ctl.maxPolarAngle = Math.PI * 0.62;
  const hemi = new T.HemisphereLight('#fff8ee', '#8a8074', 0.22); S.add(hemi);
  const key = new T.DirectionalLight('#fff3e4', 0.95); key.position.set(-2.5, 4.5, 4.0); key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048); Object.assign(key.shadow.camera, { left: -4, right: 4, top: 4, bottom: -1, near: 0.5, far: 15 }); key.shadow.bias = -0.0004; S.add(key);
  const fill = new T.DirectionalLight('#e6ecf4', 0.22); fill.position.set(4, 2, 3); S.add(fill);
  const room = new T.Group(), model = new T.Group(); S.add(room, model);
  let doors = [], ledLights = [], asm = [];

  const box = (w, h, d, mat, x, y, z, shadow = true) => {
    const me = new T.Mesh(new T.BoxGeometry(w, h, d), mat); me.position.set(x, y, z);
    me.castShadow = shadow; me.receiveShadow = true; return me;
  };
  const clear = g => { while (g.children.length) { const c = g.children.pop(); c.traverse(o => { o.geometry && o.geometry.dispose(); }); } };
  const tag = (o, step, dir) => { o.userData.asm = { step, dir: dir || new T.Vector3(0, 0.6, 0), home: o.position.clone() }; asm.push(o); return o; };

  // ---------------- szoba: világos, plafonlap nélkül – helyette szaggatott plafonvonal
  function buildRoom() {
    clear(room);
    const W = st.w / 100, BH = st.baseH / 100, C = st.ceil / 100, D = Math.max(st.d, st.baseD) / 100, DB = st.baseD / 100, off = st.wall / 100, s = st.slope / 100;
    if (st.env === 'studio') {
      S.background = new T.Color('#E6DFD4'); hemi.intensity = 0.4;
      const fl = new T.Mesh(new T.CircleGeometry(7, 64), new T.MeshStandardMaterial({ color: '#E2D9CC', roughness: 0.95 }));
      fl.rotation.x = -Math.PI / 2; fl.position.set(W / 2, 0, 0); fl.receiveShadow = true; room.add(fl);
    } else {
      S.background = new T.Color('#A39582'); hemi.intensity = 0.22;
      const wall = new T.MeshStandardMaterial({ color: '#A69886', roughness: 0.95 });
      const floorT = tex('smoked'); floorT.repeat.set(4, 4);
      const floor = new T.MeshStandardMaterial({ color: '#efe6da', map: floorT, roughness: 0.6 });
      room.add(box(Math.max(9, W + 6), 0.02, 16, floor, W / 2, -0.01, 8 - D, false));
      room.add(box(Math.max(9, W + 6), C + 2.5, 0.1, wall, W / 2, (C + 2.5) / 2, -D - off - 0.05, false));
      room.add(box(0.1, C + 2.5, 16, wall, -1.3, (C + 2.5) / 2, 8 - D, false));
      room.add(box(Math.max(9, W + 6), 0.08, 0.014, new T.MeshStandardMaterial({ color: '#F6F2EC', roughness: 0.6 }), W / 2, 0.04, -D - off + 0.007, false));
    }
    // plafonvonal (bronz, szaggatott) – ferde plafonnál ferde
    const pts = [new T.Vector3(-1.25, C - s * 1.25 / Math.max(W, .6), -D - off + 0.002), new T.Vector3(W + 1.4, C + s * (W + 1.4) / Math.max(W, .6), -D - off + 0.002)];
    const lg = new T.BufferGeometry().setFromPoints(pts);
    const ln = new T.Line(lg, new T.LineDashedMaterial({ color: '#A27D4A', dashSize: 0.06, gapSize: 0.04 })); ln.computeLineDistances(); room.add(ln);
    const ln2 = new T.Line(new T.BufferGeometry().setFromPoints([new T.Vector3(W + 0.02, C + s, -D - off), new T.Vector3(W + 0.02, C + s, 0.4)]), new T.LineDashedMaterial({ color: '#A27D4A', dashSize: 0.05, gapSize: 0.04 })); ln2.computeLineDistances(); room.add(ln2);
    // meglévő szekrény (Bútorline ELIA jelleg: kasmír tolóajtók, középen tükör, alu csíkok)
    const bm = new T.MeshStandardMaterial({ color: st.baseCol, roughness: 0.55 });
    const mir = new T.MeshStandardMaterial({ color: '#dfe4e6', roughness: 0.04, metalness: 1 });
    const alu = new T.MeshStandardMaterial({ color: '#c4c6c8', metalness: 1, roughness: .3 });
    room.add(box(W, BH - 0.04, DB, bm, W / 2, BH / 2 + 0.02, -DB / 2));
    room.add(box(W, 0.04, DB - 0.02, new T.MeshStandardMaterial({ color: '#bfb2a2', roughness: .8 }), W / 2, 0.02, -D / 2 - 0.01));
    room.add(box(W / 3 - 0.004, BH - 0.07, 0.01, mir, W / 2, BH / 2 + 0.02, 0.006));
    [[W / 6], [W * 5 / 6]].forEach(([x]) => [0.4, 0.9, 1.4, 1.9].forEach(z => { if (z < BH - 0.05) room.add(box(W / 3 - 0.01, 0.008, 0.004, alu, x, z, 0.003, false)); }));
    room.add(box(W, 0.012, 0.03, alu, W / 2, BH - 0.01, -0.015, false));
    if (st.d < st.baseD - 0.5) room.add(box(W, 0.004, DB - st.d / 100, new T.MeshStandardMaterial({ color: '#cfc4b4', roughness: .9 }), W / 2, BH + 0.002, -st.d / 100 - (DB - st.d / 100) / 2, false));
  }

  function doorWidths(W, n) {
    if (st.split !== 'sym' || n < 3) return Array(n).fill(W / n);
    const f = Array.from({ length: n }, (_, i) => (n % 2 ? i === (n - 1) / 2 : (i === n / 2 - 1 || i === n / 2)) ? 1.25 : 1);
    const sum = f.reduce((a, b) => a + b, 0); return f.map(v => v / sum * W);
  }

  // ---------------- a ZENIT modellje
  function buildModel() {
    clear(model); doors = []; asm = []; ledLights.forEach(l => S.remove(l)); ledLights = [];
    const W = st.w / 100, BH = st.baseH / 100, H = (st.ceil - st.baseH) / 100 - 0.01, D = st.d / 100, t = 0.018, tb = 0.003, td = 0.018;
    const gv = 0.0045, dp = D - td - tb, n = st.doors, off = st.wall / 100, s = st.slope / 100;
    const mB = surfMat(st.korpusz), mD = surfMat(st.ajto), mI = surfMat(st.belso);
    const y0 = BH, zFront = 0, zBodyFront = -td, zBodyBack = zBodyFront - dp, zMid = (zBodyFront + zBodyBack) / 2;
    const UP = (k = .7) => new T.Vector3(0, k, 0);
    tag(model.add(box(W - 2 * t, t, dp, mB, W / 2, y0 + t / 2, zMid)) && model.children[model.children.length - 1], 0, new T.Vector3(0, 0.5, 0.4));
    tag(model.add(box(t, H, dp, mB, t / 2, y0 + H / 2, zMid)) && model.children[model.children.length - 1], 1, new T.Vector3(-0.7, 0, 0));
    tag(model.add(box(t, H, dp, mB, W - t / 2, y0 + H / 2, zMid)) && model.children[model.children.length - 1], 1, new T.Vector3(0.7, 0, 0));
    let ws = doorWidths(W, n), acc = 0; const edges = [0];
    ws.forEach(w => { acc += w; edges.push(acc); });
    for (let i = 1; i < n; i++) { const p = box(t, H - 2 * t, dp, mI, edges[i], y0 + H / 2, zMid); model.add(p); tag(p, 2, UP(.7)); }
    { const p = box(W - 2 * t, t, dp, mB, W / 2, y0 + H - t / 2, zMid); model.add(p); tag(p, 3, UP(.8)); }
    { const p = box(W, H, tb, mI, W / 2, y0 + H / 2, zBodyBack - tb / 2); model.add(p); tag(p, 4, new T.Vector3(0, 0, -0.9)); }
    // falkiegyenlítés: rejtett távtartók a hátfal mögött
    if (off > 0.001) [0.06, W / 2, W - 0.06].forEach(x => { const p = box(0.05, H - 0.04, off, new T.MeshStandardMaterial({ color: '#B08D57', roughness: .7 }), x, y0 + H / 2, zBodyBack - tb - off / 2); model.add(p); tag(p, 4, new T.Vector3(0, 0, -0.5)); });
    // polcok + dobozok
    for (let i = 0; i < n; i++) {
      if (!st.shelves.has(i + 1)) continue;
      const xa = i === 0 ? t : edges[i] + t / 2, xb = i === n - 1 ? W - t : edges[i + 1] - t / 2;
      const p = box(xb - xa - 0.002, t, dp - 0.02, mI, (xa + xb) / 2, y0 + H / 2, zMid + 0.01); model.add(p); tag(p, 5, new T.Vector3(0, 0, 0.8));
      if (st.box) { const b = box(Math.min(0.4, (xb - xa) * 0.7), 0.16, dp * 0.7, new T.MeshStandardMaterial({ color: '#cbbfae', map: tex('linen'), roughness: 1 }), (xa + xb) / 2, y0 + t + 0.08, zMid); model.add(b); tag(b, 5, new T.Vector3(0, 0, 0.8)); }
    }
    // élet a rekeszekben: bőrönd, összehajtott textil, lendoboz (csukott ajtónál nem látszik)
    const mSuit = new T.MeshStandardMaterial({ color: '#6B5240', roughness: 0.45 }), mAlu = new T.MeshStandardMaterial({ color: '#c4c6c8', metalness: 1, roughness: .3 });
    const TX = ['#EDE7DD', '#CDBFAE', '#B9A68E', '#E3D9CB'];
    for (let i = 0; i < n; i++) {
      const xa = i === 0 ? t : edges[i] + t / 2, xb = i === n - 1 ? W - t : edges[i + 1] - t / 2, cw = xb - xa, xc = (xa + xb) / 2, yb = y0 + t;
      const shelf = st.shelves.has(i + 1), hFree = (shelf ? H / 2 - t * 1.5 : H - 2 * t) - 0.02, zc = zMid + 0.02;
      if (cw < 0.3 || hFree < 0.12) continue;
      const kind = i % 3;
      if (kind === 0 || (n === 1)) {
        const sw = Math.min(0.62, cw - 0.08), sh = Math.min(0.23, hFree - 0.02);
        const s1 = box(sw, sh, Math.min(0.42, dp - 0.08), mSuit, xc, yb + sh / 2, zc); model.add(s1); tag(s1, 8, new T.Vector3(0, 0, 0.6));
        const hd = box(0.12, 0.02, 0.02, mAlu, xc, yb + sh + 0.01, zc + 0.12); model.add(hd); tag(hd, 8, new T.Vector3(0, 0, 0.6));
      } else {
        let yy = yb; const k = kind === 1 ? 3 : 2;
        for (let j = 0; j < k && yy < yb + hFree - 0.07; j++) {
          const th = 0.05 + (j % 2) * 0.015, tw = Math.min(0.38, cw * 0.45);
          const tx = box(tw, th, 0.3, new T.MeshStandardMaterial({ color: TX[(i + j) % 4], map: tex('linen'), roughness: 1 }), xc - (kind === 2 ? cw * 0.2 : 0), yy + th / 2, zc + 0.04);
          model.add(tx); tag(tx, 8, new T.Vector3(0, 0, 0.6)); yy += th;
        }
        if (kind === 2) { const bx = box(Math.min(0.3, cw * 0.38), Math.min(0.18, hFree - 0.02), 0.34, new T.MeshStandardMaterial({ color: '#C9BBA6', map: tex('linen'), roughness: 1 }), xc + cw * 0.22, yb + Math.min(0.18, hFree - 0.02) / 2, zc); model.add(bx); tag(bx, 8, new T.Vector3(0, 0, 0.6)); }
      }
      if (shelf) {  // a polcon is: összehajtott textil
        let yy = y0 + H / 2 + t / 2;
        for (let j = 0; j < 2; j++) { const th = 0.055; const tx = box(Math.min(0.36, cw * 0.42), th, 0.3, new T.MeshStandardMaterial({ color: TX[(i + j + 1) % 4], map: tex('linen'), roughness: 1 }), xc - cw * 0.18, yy + th / 2, zc + 0.04); model.add(tx); tag(tx, 8, new T.Vector3(0, 0, 0.6)); yy += th; }
      }
    }
    // LED
    if (st.led) for (let i = 0; i < n; i++) {
      const xa = i === 0 ? t : edges[i] + t / 2, xb = i === n - 1 ? W - t : edges[i + 1] - t / 2;
      const l = box(xb - xa - 0.04, 0.006, 0.012, new T.MeshBasicMaterial({ color: '#ffe0b0' }), (xa + xb) / 2, y0 + H - t - 0.006, zBodyFront - 0.03, false); model.add(l); tag(l, 8, UP(.2));
      const L = new T.PointLight('#ffcf94', 0, 0.9, 2); L.position.set((xa + xb) / 2, y0 + H - t - 0.05, zBodyFront - 0.08); S.add(L); ledLights.push(L);
    }
    // takaróléc a plafonig – ferde plafonnál ferdére szabva (automatikusan)
    if (st.trim || s > 0) {
      const g0 = 0.008, sh = new T.Shape();
      sh.moveTo(0, 0); sh.lineTo(W, 0); sh.lineTo(W, 0.01 + s - 0.002 + 0); sh.lineTo(0, 0.01 - 0.002); sh.lineTo(0, 0);
      const ge = new T.ExtrudeGeometry(sh, { depth: 0.018, bevelEnabled: false });
      const tr = new T.Mesh(ge, mB); tr.position.set(0, y0 + H, -0.018); tr.castShadow = true; model.add(tr); tag(tr, 8, UP(.3));
    }
    // ajtók – ajtónként nyitásirány és tükör
    const hmat = new T.MeshStandardMaterial({ color: st.hcol, metalness: st.hcol === '#7A4E2D' ? 0 : 0.9, roughness: st.hcol === '#7A4E2D' ? 0.7 : 0.3 });
    const mirM = new T.MeshStandardMaterial({ color: '#e3e8ea', roughness: 0.03, metalness: 1, envMapIntensity: 1.2 });
    for (let i = 0; i < n; i++) {
      const xa = edges[i] + 0.0015, xb = edges[i + 1] - 0.0015;
      const dw = xb - xa, dh = H - 2 * gv, left = (st.hinge[i] || 'L') === 'L';
      const piv = new T.Group(); piv.position.set(left ? xa : xb, y0 + gv, zFront - td); model.add(piv);
      const sx = left ? 1 : -1, cx = sx * dw / 2;
      const dr = box(dw, dh, td, mD, cx, dh / 2, td / 2); piv.add(dr);
      if (st.mirror[i]) { const mr = box(dw - 0.03, dh - 0.03, 0.004, mirM, cx, dh / 2, td + 0.002, false); piv.add(mr); mr.userData.pivot = piv; }
      if (st.handle === 'edge') {
        const L = Math.min(0.225, dw * 0.45);
        piv.add(box(L, 0.004, td + 0.014, hmat, cx, -0.002, td / 2 + 0.002));
        const lip = new T.Mesh(new T.CylinderGeometry(0.006, 0.006, L, 20), hmat); lip.rotation.z = Math.PI / 2; lip.position.set(cx, -0.006, td + 0.01); piv.add(lip);
      } else if (st.handle === 'bar') {
        const L = Math.min(0.32, dw * 0.6);
        const bar = new T.Mesh(new T.CylinderGeometry(0.006, 0.006, L, 20), hmat); bar.rotation.z = Math.PI / 2; bar.position.set(cx, 0.055, td + 0.03); bar.castShadow = true; piv.add(bar);
        [-1, 1].forEach(k => piv.add(box(0.008, 0.008, 0.03, hmat, cx + k * (L / 2 - 0.02), 0.055, td + 0.015)));
      } else if (st.handle === 'knob') {
        const k = new T.Mesh(new T.SphereGeometry(0.014, 24, 16), hmat); k.position.set(sx * (dw - 0.06), 0.06, td + 0.016); k.castShadow = true; piv.add(k);
      }
      piv.userData = Object.assign(piv.userData, { left, ang: 0 }); dr.userData.pivot = piv; doors.push(piv);
      tag(piv, 6, new T.Vector3(0, 0, 0.9));
    }
    applyOpen(true);
    $('dimW').textContent = st.w; $('dimH').textContent = Math.round((st.ceil - st.baseH) - 1); $('dimD').textContent = st.d;
    const nm = st.mirror.slice(0, n).filter(Boolean).length;
    const p = 89900 + st.w * 480 + n * 9000 + st.shelves.size * 6500 + (st.led ? 24900 : 0) + ((st.trim || s > 0) ? 14900 : 0) + (st.box ? 8900 * n : 0)
      + nm * 18900 + (off > 0 ? 6900 : 0)
      + (['oak', 'smoked', 'walnut'].some(k => st.ajto === k || st.korpusz === k) ? 64000 : 0) + (st.fin === 'gloss' ? 19000 : 0);
    $('price').textContent = (Math.round(p / 100) * 100).toLocaleString('hu-HU') + ' Ft';
    envTone(model);
  }
  // környezeti fény visszafogása a nem fémes felületeken – így a kasmír nem fakul ki
  function envTone(g) { g.traverse(o => { const m = o.material; if (m && m.envMapIntensity !== undefined && !m.metalness) m.envMapIntensity = 0.3; }); }

  function applyOpen(instant) {
    doors.forEach(d => { d.userData.target = st.open ? (d.userData.left ? -1 : 1) * 1.75 : 0; if (instant) d.rotation.y = d.userData.target; });
  }
  function frame() {
    const W = st.w / 100, C = st.ceil / 100, BH = st.baseH / 100;
    const ty = st.env === 'studio' ? (BH + C) / 2 - 0.15 : C * 0.6;
    ctl.target.set(W / 2, ty, -st.d / 200);
    const dist = st.env === 'studio' ? Math.max(4.4, W * 1.5 + 2.8) : Math.max(5.2, W * 1.5 + 3.2);
    cam.position.set(W / 2 + dist * 0.42, Math.min(C - 0.25, ty + 0.3), dist * 0.9); ctl.update();
  }
  function resize() {
    const r = cv.parentElement.getBoundingClientRect();
    R.setSize(r.width, r.height, false); cam.aspect = r.width / r.height; cam.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(cv.parentElement);

  // ---------------- ajtó kattintásra nyílik
  const ray = new T.Raycaster(), mp = new T.Vector2(); let down = null;
  cv.addEventListener('pointerdown', e => down = [e.clientX, e.clientY]);
  cv.addEventListener('pointerup', e => {
    if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 4) return;
    const r = cv.getBoundingClientRect(); mp.set((e.clientX - r.left) / r.width * 2 - 1, -(e.clientY - r.top) / r.height * 2 + 1);
    ray.setFromCamera(mp, cam); const hit = ray.intersectObjects(model.children, true).find(h => h.object.userData.pivot);
    if (hit) { const p = hit.object.userData.pivot; p.userData.target = p.userData.target ? 0 : (p.userData.left ? -1 : 1) * 1.75; }
  });

  // ---------------- szerelési animáció (a saját tervből) + videó
  const STEPS = [
    ['Fenéklap és tiplik', 'Tiplik a fenéklapba, gumikalapáccsal ütközésig.'],
    ['Oldallapok', 'Kötésenként két konfirmát 7×50, kívülről.'],
    ['Közfalak', 'A tiplikre ültetve, alulról konfirmáttal.'],
    ['Tetőlap', 'Az oldallapokon és a közfalakon át rögzítve.'],
    ['Hátfal', 'Beütős szeggel, kb. 15 cm-enként – előfúrás nélkül.'],
    ['Polc', 'Oldalanként három polctartó csapon.'],
    ['Ajtók', 'Rápattintva a Häfele szerelőtalpakra, hézag 3 mm.'],
    ['Ellenőrzés', 'Hézagok és záródás – a fékes pánt csendben húz be.'],
    ['Fény és befejezés', 'LED, takaróléc, védőfólia le. Kész. Csend.']];
  let asmT = -1, asmT0 = 0, rec = null, recChunks = [], comp = null, compG = null;
  const SPS = window.ZENIT_SPS || 1.9; // másodperc lépésenként
  function startAsm(record) {
    st.open = false; applyOpen(true); asmT = 0; asmT0 = performance.now();
    $('asmBox').classList.add('on');
    if (record) startRec();
  }
  const ease = k => k < 0 ? 0 : k > 1 ? 1 : 1 - Math.pow(1 - k, 3);
  function asmUpdate(now) {
    if (asmT < 0) return;
    const el = Math.max(0, (now - asmT0) / 1000), DU = window.ZENIT_DURS;
    if (DU) {  // lépésenként eltérő hossz (a narrált videóhoz): mozgás ~1,7 s, utána kitartás
      let c = 0, i = 0; while (i < DU.length && el >= c + DU[i]) { c += DU[i]; i++; }
      asmT = i >= DU.length ? DU.length + 0.6 + (el - c) : i + Math.min(0.999, (el - c) / Math.min(1.7, DU[i]));
    } else asmT = el / SPS;
    const N = STEPS.length;
    asm.forEach(o => {
      const a = o.userData.asm, k = ease(asmT - a.step);
      o.visible = asmT >= a.step;
      o.position.copy(a.home).addScaledVector(a.dir, 1 - k);
    });
    ledLights.forEach(l => l.intensity = asmT > 8 ? 2.6 : 0);
    const i = Math.max(0, Math.min(N - 1, Math.floor(asmT)));
    $('asmT').textContent = `${i + 1}/${N} · ${STEPS[i][0]}`; $('asmD').textContent = STEPS[i][1]; $('asmBar').style.width = Math.min(100, asmT / N * 100) + '%';
    // lassú kameraív
    const W = st.w / 100, C = st.ceil / 100, BH = st.baseH / 100, a0 = -0.24 + Math.min(1, asmT / N) * 0.48, dist = window.ZENIT_ASMDIST || Math.max(3.4, W * 1.2 + 2.0), ty = BH + (C - BH) / 2 - 0.02 + (window.ZENIT_ASMDY || 0);
    ctl.target.set(W / 2, ty, -st.d / 200); cam.position.set(W / 2 + Math.sin(a0) * dist, Math.min(C - 0.12, ty + 0.25), Math.cos(a0) * dist); cam.lookAt(ctl.target);
    if (asmT >= N + 0.6) {
      asmT = -1; asm.forEach(o => { o.visible = true; o.position.copy(o.userData.asm.home); });
      setTimeout(() => $('asmBox').classList.remove('on'), 1200); stopRec(); frame();
    }
  }
  function startRec() {
    const mime = ['video/webm;codecs=vp9', 'video/webm;codecs=vp8', 'video/webm', 'video/mp4'].find(m => window.MediaRecorder && MediaRecorder.isTypeSupported(m));
    if (!mime) { alert('Ez a böngésző nem támogatja a videórögzítést – a szerelési animáció megnézhető, de nem menthető.'); return; }
    comp = document.createElement('canvas'); comp.width = 1280; comp.height = 720; compG = comp.getContext('2d');
    rec = new MediaRecorder(comp.captureStream(30), { mimeType: mime, videoBitsPerSecond: 6e6 }); recChunks = [];
    rec.ondataavailable = e => e.data.size && recChunks.push(e.data);
    rec.onstop = () => {
      const b = new Blob(recChunks, { type: mime }), a = document.createElement('a');
      a.href = URL.createObjectURL(b); a.download = `ZENIT_szereles_${st.w}cm_${st.doors}ajto.${mime.includes('mp4') ? 'mp4' : 'webm'}`; a.click();
      comp = null; rec = null;
    };
    rec.start();
  }
  function stopRec() { if (rec && rec.state !== 'inactive') rec.stop(); }
  function drawComp() {
    if (!comp) return;
    const g = compG, W = comp.width, H = comp.height, s = Math.max(W / cv.width, H / cv.height);
    g.fillStyle = '#A39582'; g.fillRect(0, 0, W, H);
    g.drawImage(cv, (W - cv.width * s) / 2, (H - cv.height * s) / 2, cv.width * s, cv.height * s);
    const i = Math.max(0, Math.min(STEPS.length - 1, Math.floor(asmT)));
    g.fillStyle = 'rgba(20,17,14,.82)'; g.fillRect(0, H - 110, W, 110);
    g.fillStyle = '#C2A274'; g.font = '500 15px Inter, sans-serif'; g.fillText(`ZENIT · SZERELÉS · ${i + 1}/${STEPS.length}`, 40, H - 74);
    g.fillStyle = '#fff'; g.font = '300 30px Georgia, serif'; g.fillText(STEPS[i][0] + ' — ' + STEPS[i][1], 40, H - 34);
    g.fillStyle = '#C2A274'; g.fillRect(0, H - 110, W * Math.min(1, Math.max(0, asmT) / STEPS.length), 2);
  }

  // ---------------- render ciklus
  (function loop(now) {
    requestAnimationFrame(loop);
    let openAmt = 0;
    doors.forEach(d => { d.rotation.y += (d.userData.target - d.rotation.y) * 0.12; openAmt = Math.max(openAmt, Math.abs(d.rotation.y) / 1.75); });
    if (asmT < 0) ledLights.forEach(l => l.intensity = 2.8 * openAmt);
    asmUpdate(now || performance.now());
    if (asmT < 0) ctl.update();
    R.render(S, cam); drawComp();
  })();

  // ---------------- UI
  const rebuild = () => { buildRoom(); envTone(room); buildModel(); };
  const mk = (id, list, isTex) => {
    const g = $(id); list.forEach(it => {
      const b = document.createElement('button'); b.title = it[0]; b.style.background = isTex ? TEXPREV[it[1]] : it[1];
      if (isTex) b.style.backgroundImage = `url(${tex(it[1]).image.toDataURL('image/jpeg', .7)})`;
      b.onclick = () => pick(it[1], b); g.appendChild(b);
    });
  };
  mk('swUni', UNI); mk('swWood', WOOD, 1); mk('swStone', STONE, 1);
  function pick(spec, btn) {
    document.querySelectorAll('.sw button').forEach(x => x.classList.remove('on')); btn && btn.classList.add('on');
    st[st.part] = spec; syncHex(); buildModel();
  }
  function syncHex() {
    const v = st[st.part]; $('hexIn').value = ISTEX[v] ? '— textúra —' : v;
    $('hexPrev').style.background = ISTEX[v] ? TEXPREV[v] : v;
  }
  document.querySelectorAll('#partTabs button').forEach(b => b.onclick = () => {
    document.querySelectorAll('#partTabs button').forEach(x => x.classList.remove('on')); b.classList.add('on'); st.part = b.dataset.part; syncHex();
  });
  $('hexIn').oninput = () => { if (/^#[0-9a-f]{6}$/i.test($('hexIn').value)) pick($('hexIn').value); };
  const group = (id, fn) => document.querySelectorAll('#' + id + ' .opt').forEach(b => b.onclick = () => {
    document.querySelectorAll('#' + id + ' .opt').forEach(x => x.classList.remove('on')); b.classList.add('on'); fn(b); });
  const setD = v => { st.d = v; $('dVal').textContent = v; $('dRange').value = v; document.querySelectorAll('#depthOpts .opt').forEach(x => x.classList.toggle('on', +x.dataset.d === v)); rebuild(); };
  document.querySelectorAll('#depthOpts .opt').forEach(b => b.onclick = () => { setD(+b.dataset.d); frame(); });
  $('dRange').oninput = () => setD(+$('dRange').value);
  group('splitOpts', b => { st.split = b.dataset.s; buildModel(); });
  group('finOpts', b => { st.fin = b.dataset.f; buildModel(); });
  group('hcol', b => { st.hcol = b.dataset.c === '#222' ? '#1E1E1E' : b.dataset.c; buildModel(); });
  document.querySelectorAll('#handles .card2').forEach(b => b.onclick = () => {
    document.querySelectorAll('#handles .card2').forEach(x => x.classList.remove('on')); b.classList.add('on'); st.handle = b.dataset.h; buildModel(); });
  [['xLed', 'led'], ['xTrim', 'trim'], ['xBox', 'box']].forEach(([id, k]) => { const el = $(id); el.classList.toggle('on', st[k]); el.onclick = () => { st[k] = !st[k]; el.classList.toggle('on', st[k]); buildModel(); }; });
  document.querySelectorAll('#envSeg button').forEach(b => b.onclick = () => {
    document.querySelectorAll('#envSeg button').forEach(x => x.classList.remove('on')); b.classList.add('on'); st.env = b.dataset.env; buildRoom(); frame(); });
  $('btnOpen').onclick = () => { st.open = !st.open; applyOpen(false); $('btnOpen').classList.toggle('on', st.open); };
  $('btnReset').onclick = frame;
  $('btnFull').onclick = () => { const v = cv.parentElement; document.fullscreenElement ? document.exitFullscreen() : v.requestFullscreen && v.requestFullscreen(); };
  $('btnAsm').onclick = () => startAsm(false);
  $('lnkAsm').onclick = e => { e.preventDefault(); scrollTo({ top: 0, behavior: 'smooth' }); startAsm(false); };
  $('lnkRec').onclick = e => { e.preventDefault(); scrollTo({ top: 0, behavior: 'smooth' }); startAsm(true); };
  $('baseCol').onclick = e => { e.preventDefault(); const c = prompt('Az alatta lévő szekrény színe (HEX):', st.baseCol); if (c && /^#[0-9a-f]{6}$/i.test(c)) { st.baseCol = c; $('baseCol').textContent = c; buildRoom(); } };

  const rec_ = w => Math.max(1, Math.min(6, Math.ceil(w / 60)));
  function setDoors(k) {
    st.doors = k; st.hinge = defHinge(k); st.mirror = Array(k).fill(false); st.shelves = new Set([Math.ceil(k / 2)]);
  }
  function doorsUI() {
    const g = $('doorOpts'); g.innerHTML = ''; const r = rec_(st.w); $('doorRec').textContent = r;
    const lo = Math.max(1, Math.ceil(st.w / 90)), hi = Math.min(6, Math.max(lo, Math.floor(st.w / 35)));
    for (let k = lo; k <= hi; k++) {
      const b = document.createElement('button'); b.className = 'opt' + (k === st.doors ? ' on' : ''); b.textContent = k + (k === r ? ' · javasolt' : '');
      b.onclick = () => { setDoors(k); doorsUI(); buildModel(); }; g.appendChild(b);
    }
    // ajtónkénti beállítás
    const dg = $('doorGrid'); dg.innerHTML = '<span class="h">Ajtó</span><span class="h">Nyitás</span><span class="h">Front</span>';
    for (let i = 0; i < st.doors; i++) {
      const row = document.createElement('div'); row.style.display = 'contents';
      row.innerHTML = `<span>${i + 1}.</span><span class="mini"><button data-k="L" class="${st.hinge[i] === 'L' ? 'on' : ''}">◧ Bal</button><button data-k="R" class="${st.hinge[i] === 'R' ? 'on' : ''}">Jobb ◨</button></span><span class="mini"><button data-m="0" class="${!st.mirror[i] ? 'on' : ''}">Lap</button><button data-m="1" class="${st.mirror[i] ? 'on' : ''}">Tükör</button></span>`;
      row.querySelectorAll('[data-k]').forEach(b => b.onclick = () => { st.hinge[i] = b.dataset.k; doorsUI(); buildModel(); });
      row.querySelectorAll('[data-m]').forEach(b => b.onclick = () => { st.mirror[i] = b.dataset.m === '1'; doorsUI(); buildModel(); });
      dg.appendChild(row);
    }
    const s = $('shelfOpts'); s.innerHTML = '';
    for (let i = 1; i <= st.doors; i++) {
      const b = document.createElement('button'); b.className = 'opt' + (st.shelves.has(i) ? ' on' : ''); b.textContent = i + '. rekesz';
      b.onclick = () => { st.shelves.has(i) ? st.shelves.delete(i) : st.shelves.add(i); b.classList.toggle('on'); buildModel(); }; s.appendChild(b);
    }
  }
  $('w').oninput = () => {
    st.w = +$('w').value; $('wVal').textContent = st.w;
    const lo = Math.ceil(st.w / 90), hi = Math.floor(st.w / 35);
    if (st.doors < lo || st.doors > hi) setDoors(rec_(st.w));
    doorsUI(); rebuild(); frame();
  };
  $('ceil').oninput = () => { st.ceil = Math.max(+$('ceil').value, st.baseH + 30); $('ceilVal').textContent = st.ceil; rebuild(); };
  $('baseH').oninput = () => { st.baseH = Math.min(+$('baseH').value, st.ceil - 30); $('baseVal').textContent = st.baseH; rebuild(); frame(); };
  $('slope').oninput = () => { st.slope = +$('slope').value; $('slopeVal').textContent = String(st.slope).replace('.', ','); rebuild(); };
  $('wall').oninput = () => { st.wall = +$('wall').value; $('wallVal').textContent = String(st.wall).replace('.', ','); rebuild(); };

  // ---------------- terv mentése (kézikönyvhöz, ajánlathoz)
  document.querySelectorAll('[data-save]').forEach(a => a.addEventListener('click', () => {
    try {
      const plans = JSON.parse(localStorage.getItem('zenitPlans') || '[]');
      plans.push({ w: st.w, h: Math.round(st.ceil - st.baseH - 1), d: st.d, ceil: st.ceil, baseH: st.baseH, doors: st.doors, split: st.split,
        hinge: st.hinge.slice(0, st.doors), mirror: st.mirror.slice(0, st.doors), slope: st.slope, wall: st.wall,
        ajto: st.ajto, korpusz: st.korpusz, belso: st.belso, fin: st.fin, handle: st.handle, hcol: st.hcol, shelves: [...st.shelves],
        led: st.led, trim: st.trim || st.slope > 0, box: st.box, price: $('price').textContent, img: cv.toDataURL('image/jpeg', 0.72), t: Date.now(),
        serial: 'ZN-' + new Date().getFullYear() + '-' + String(Math.floor(1000 + Math.random() * 9000)) });
      localStorage.setItem('zenitPlans', JSON.stringify(plans.slice(-4)));
    } catch (e) { }
  }));

  // ---------------- kezdés
  if (st.open) applyOpen(false);
  syncHex(); doorsUI(); rebuild(); resize(); frame();
  // UI szinkron presetekhez
  document.querySelectorAll('#splitOpts .opt').forEach(b => b.classList.toggle('on', b.dataset.s === st.split));
  window.zenitCfg = { st, cam, ctl, frame, startAsm, rebuild, doorsUI, doors: () => doors, leds: () => ledLights, S, R, hemi, key, fill };
  if (/assemble/.test(location.hash)) setTimeout(() => startAsm(false), 600);
})();
