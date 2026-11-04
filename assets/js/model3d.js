/* ZENIT – a gyártási modell (v10, GLB) interaktív nézegetője.
   three.js r147 + GLTFLoader + OrbitControls (klasszikus scriptek). */
(function () {
  const cv = document.getElementById('model3d');
  if (!cv || !window.THREE || !THREE.GLTFLoader) return;
  const wrap = cv.parentElement;
  if (THREE.ColorManagement) THREE.ColorManagement.legacyMode = false;
  const R = new THREE.WebGLRenderer({ canvas: cv, antialias: true, preserveDrawingBuffer: true });
  R.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
  R.outputEncoding = THREE.sRGBEncoding;
  R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = 0.72;
  R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap;
  const S = new THREE.Scene();
  S.background = new THREE.Color('#1b1815');
  if (THREE.RoomEnvironment) { const pm = new THREE.PMREMGenerator(R); S.environment = pm.fromScene(new THREE.RoomEnvironment(), 0.04).texture; }
  const cam = new THREE.PerspectiveCamera(32, 1, 0.05, 60);
  const ctl = new THREE.OrbitControls(cam, cv);
  ctl.enableDamping = true; ctl.dampingFactor = 0.08; ctl.minDistance = 1.2; ctl.maxDistance = 12;
  ctl.maxPolarAngle = Math.PI * 0.52;

  S.add(new THREE.HemisphereLight('#fff6ea', '#3a332c', 0.25));
  const key = new THREE.DirectionalLight('#fff3e2', 1.6);
  key.position.set(3.5, 5, 4); key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024);
  Object.assign(key.shadow.camera, { left: -3, right: 3, top: 4, bottom: -1, near: 0.5, far: 15 });
  key.shadow.bias = -0.0004; S.add(key);
  const rim = new THREE.DirectionalLight('#c9d6ff', 0.35); rim.position.set(-4, 3, -3); S.add(rim);
  const floor = new THREE.Mesh(new THREE.CircleGeometry(4.5, 64),
    new THREE.MeshStandardMaterial({ color: '#221e1a', roughness: 0.95, envMapIntensity: 0.3 }));
  floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; S.add(floor);

  const M = (c, o) => new THREE.MeshStandardMaterial(Object.assign({ color: c, roughness: 0.72, metalness: 0, envMapIntensity: 0.45 }, o || {}));
  const MAT = {
    korpusz: M('#CDBFAE'), ajto: M('#CDBFAE', { roughness: 0.6 }), el: M('#C2B3A1', { roughness: 0.5 }),
    hatfal: M('#ECE8E1'), belso: M('#EFEBE4'),
    vas: M('#bfbfbf', { metalness: 0.85, roughness: 0.32 }), fog: M('#B9B6B0', { metalness: 0.8, roughness: 0.38 }),
    elia: M('#CDBFAF', { roughness: 0.75 }), tukor: M('#d9dee2', { metalness: 1, roughness: 0.04, envMapIntensity: 1 }),
    sin: M('#9a9a96', { metalness: 0.7, roughness: 0.4 })
  };
  const fix = s => { try { return decodeURIComponent(escape(s)); } catch (e) { return s; } };

  const st = { explode: 0, target: 0, base: true, doors: true, hw: false, auto: true };
  const groups = []; let topper, elia, hwGroup, center = new THREE.Vector3(), size = new THREE.Vector3();
  const api = window.zenitModel = { ready: false };

  new THREE.GLTFLoader().load(cv.dataset.src, g => {
    const root = g.scene;
    // CadQuery mm → méter
    root.scale.setScalar(0.001);
    root.traverse(o => {
      const n = fix(o.name || ''), pn = fix((o.parent && o.parent.name) || '');
      if (o.isMesh) {
        o.castShadow = o.receiveShadow = true;
        let m = MAT.korpusz;
        const p = pn + '|' + n;
        if (/ELIA/.test(p)) m = /tükr|tukr|t.*krös/i.test(n) ? MAT.tukor : /sín|s.n/.test(n) ? MAT.sin : MAT.elia;
        else if (/HEXA|foganty/i.test(p)) m = MAT.fog;
        else if (/Metalla|konfirm|tipli|csap|csavar|szeg|vasalat/i.test(p)) m = MAT.vas;
        else if (/ajt/i.test(pn)) m = /^abs/.test(n) ? MAT.el : MAT.ajto;
        else if (/tfal/i.test(pn) && !/k.zfal/i.test(pn)) m = MAT.hatfal;
        else if (/polc|k.zfal/i.test(pn)) m = /^abs/.test(n) ? MAT.el : MAT.belso;
        else if (/^abs/.test(n)) m = MAT.el;
        o.material = m;
      }
      if (/^ELIA/.test(n) && !elia) elia = o;
      if (/^vasalat$/.test(n)) hwGroup = o;
      if (/^ratet_lapok$/.test(n)) topper = o;
    });
    S.add(root);
    // Y-fel tájolás: a CadQuery Z-fel modellt forgatjuk
    const bb0 = new THREE.Box3().setFromObject(root), sz0 = bb0.getSize(new THREE.Vector3());
    if (sz0.z > sz0.y * 1.2) root.rotation.x = -Math.PI / 2;
    root.updateMatrixWorld(true);
    const bb = new THREE.Box3().setFromObject(root);
    root.position.x -= (bb.min.x + bb.max.x) / 2; root.position.z -= (bb.min.z + bb.max.z) / 2; root.position.y -= bb.min.y;
    root.updateMatrixWorld(true);
    // robbantáshoz: a rátét lapjai a rátét középpontjától kifelé
    const tb = new THREE.Box3().setFromObject(topper || root); tb.getCenter(center); tb.getSize(size);
    const parts = (topper ? topper.children : []).concat(hwGroup ? hwGroup.children : []);
    parts.forEach(o => {
      const c = new THREE.Box3().setFromObject(o).getCenter(new THREE.Vector3());
      const d = c.clone().sub(center); const n = fix(o.name);
      d.x *= 0.45; d.y *= 1.15; d.z *= 1.4;
      if (/ajt/i.test(n)) d.z = Math.max(d.z, 0) + size.z * 1.05;
      if (/tfal/i.test(n) && !/k.zfal/i.test(n)) d.z -= size.z * 0.9;
      if (/vasalat|Metalla|HEXA/.test(n) || o.parent === hwGroup) d.z += size.z * 0.45;
      // lokális (forgatott, skálázott) térbe vissza
      const p0 = o.position.clone();
      const inv = new THREE.Matrix4().copy(o.parent.matrixWorld).invert();
      const w0 = o.parent.localToWorld(p0.clone());
      const local = w0.clone().add(d).applyMatrix4(inv);
      groups.push({ o, p0, p1: local, n });
    });
    frame(); api.ready = true; cv.closest('.m3d').classList.add('ready');
  }, undefined, e => { console.error(e); wrap.querySelector('.m3d-load').textContent = 'A 3D modell nem tölthető be.'; });

  function frame(az) {
    const H = topper ? new THREE.Box3().setFromObject(topper).max.y : 2.6;
    ctl.target.set(0, st.base ? H * 0.5 : center.y, 0);
    const r = st.base ? 6.4 : 5.4, a = az == null ? 0.62 : az;
    cam.position.set(Math.sin(a) * r, ctl.target.y + (st.base ? 0.6 : 1.1), Math.cos(a) * r);
    ctl.update();
  }
  function resize() {
    const w = wrap.clientWidth, h = wrap.clientHeight;
    if (cv.width !== Math.round(w * R.getPixelRatio()) || cv.height !== Math.round(h * R.getPixelRatio())) {
      R.setSize(w, h, false); cam.aspect = w / h; cam.updateProjectionMatrix();
    }
  }
  const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  function apply() {
    const e = ease(st.explode);
    groups.forEach(g => g.o.position.lerpVectors(g.p0, g.p1, e));
    if (elia) elia.visible = st.base;
    groups.forEach(g => { if (/ajt/i.test(g.n)) g.o.visible = st.doors; });
    if (hwGroup) hwGroup.visible = st.hw || st.explode > 0.02;
  }
  let last = performance.now();
  function loop(t) {
    const dt = Math.min(0.05, (t - last) / 1000); last = t;
    if (Math.abs(st.target - st.explode) > 1e-3) st.explode += Math.sign(st.target - st.explode) * Math.min(Math.abs(st.target - st.explode), dt / 1.4);
    if (st.auto && api.ready) { ctl.autoRotate = true; ctl.autoRotateSpeed = 0.6; } else ctl.autoRotate = false;
    resize(); apply(); ctl.update(); R.render(S, cam); requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
  ['pointerdown', 'wheel', 'touchstart'].forEach(ev => cv.addEventListener(ev, () => { st.auto = false; }, { passive: true }));

  // vezérlők
  const tg = (id, k, cb) => { const b = document.getElementById(id); if (!b) return; b.addEventListener('click', () => { st[k] = !st[k]; b.classList.toggle('on', st[k]); cb && cb(); }); };
  const ex = document.getElementById('mExplode');
  if (ex) ex.addEventListener('click', () => { st.target = st.target ? 0 : 1; ex.classList.toggle('on', !!st.target); });
  tg('mBase', 'base', () => frame());
  tg('mDoors', 'doors');
  tg('mHw', 'hw');
  const rs = document.getElementById('mReset'); if (rs) rs.addEventListener('click', () => { st.auto = true; frame(); });

  // filmezéshez / automatizáláshoz
  Object.assign(api, {
    set(o) { Object.assign(st, o); if ('explode' in o) st.target = o.explode; if ('base' in o) frame(); apply(); },
    orbit(az, opts) { st.auto = false; if (opts) Object.assign(st, opts); frame(az); apply(); ctl.update(); R.render(S, cam); },
    render() { resize(); apply(); ctl.update(); R.render(S, cam); }
  });
})();
