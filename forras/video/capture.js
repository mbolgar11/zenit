// Determinisztikus képkocka-felvétel a ZENIT oldalról (30 fps, 1920×1080, JPEG q92).
// rAF és performance.now kézi léptetése → sima, egyenletes mozgás lassú (szoftveres) WebGL mellett is.
const { chromium } = require('playwright');
const fs = require('fs');
const OUT = process.argv[2] || '/home/claude/video/frames';
const ONLY = (process.argv[3] || '').split(',').filter(Boolean);
const BASE = 'http://localhost:8765/';
const INIT = `(()=>{let t=0;let q=[];window.requestAnimationFrame=cb=>{q.push(cb);return q.length};window.cancelAnimationFrame=()=>{};
performance.now=()=>t;window.__tick=(n=1)=>{for(let i=0;i<n;i++){t+=1000/30;const c=q;q=[];c.forEach(f=>{try{f(t)}catch(e){console.error(e)}})}};})();`;
const NOANIM = '*{transition:none!important;animation:none!important;scroll-behavior:auto!important}';
const ease = t => t <= 0 ? 0 : t >= 1 ? 1 : (t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const lerp = (a, b, t) => a + (b - a) * t;

async function shot(page, dir, n, perFrame, canvasSel, uiFrames) {
  fs.mkdirSync(dir, { recursive: true });
  const t0 = Date.now();
  for (let f = 0; f < n; f++) {
    const ui = await perFrame(f);
    const name = `${dir}/${String(f).padStart(4, '0')}`;
    if (!canvasSel) {
      await page.evaluate(() => window.__tick(1));
      await page.screenshot({ path: name + '.jpg', type: 'jpeg', quality: 92 });
      continue;
    }
    const data = await page.evaluate(sel => { window.__tick(1); const c = document.querySelector(sel); return c.toDataURL('image/jpeg', 0.93); }, canvasSel);
    fs.writeFileSync(name + '.c.jpg', Buffer.from(data.split(',')[1], 'base64'));
    if (uiFrames && (f === 0 || ui)) {
      await page.screenshot({ path: name + '.ui.jpg', type: 'jpeg', quality: 92 });
      if (f === 0) { const r = await page.evaluate(sel => { const b = document.querySelector(sel).getBoundingClientRect(); return [b.left, b.top, b.width, b.height]; }, canvasSel); fs.writeFileSync(dir + '/rect.json', JSON.stringify(r)); }
    }
    if (f % 30 === 0) console.log(dir, f, ((Date.now() - t0) / (f + 1) / 1000).toFixed(2) + ' s/kocka');
  }
  console.log('kész', dir, n);
}

(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'] });
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await ctx.addInitScript(INIT);
  const want = k => !ONLY.length || ONLY.includes(k);

  // ---------- 3D modell (GLB nézegető, teljes képernyő)
  if (want('model') || want('modelb')) {
    const p = await ctx.newPage(); p.on('pageerror', e => console.error('ERR', e.message));
    await p.goto(BASE + 'projekt.html');
    await p.addStyleTag({ content: NOANIM + '.m3d{position:fixed!important;inset:0!important;z-index:999;aspect-ratio:auto!important;border:0!important}.m3d-bar,.m3d-hint,.m3d-load{display:none!important}' });
    for (let i = 0; i < 400; i++) { await p.evaluate(() => window.__tick(1)); if (await p.evaluate(() => window.zenitModel && window.zenitModel.ready)) break; await p.waitForTimeout(100); }
    await p.evaluate(() => window.__tick(3));
    if (!ONLY.includes('modelb')) await shot(p, OUT + '/model_a', 210, f => p.evaluate(([az]) => { zenitModel.set({ explode: 0, base: true, doors: true, hw: false }); zenitModel.orbit(az); }, [lerp(0.18, 1.0, f / 209)]), '#model3d');
    await shot(p, OUT + '/model_b', 240, f => p.evaluate(([az, e]) => { zenitModel.set({ explode: e, base: false, doors: true }); zenitModel.orbit(az); },
      [lerp(0.55, 1.25, f / 239), ease((f - 25) / 110)]), '#model3d');
    await p.close();
  }

  // ---------- Weboldal görgetés (kezdőlap)
  if (want('site')) {
    const p = await ctx.newPage();
    await p.goto(BASE + 'index.html'); await p.waitForTimeout(800);
    await p.addStyleTag({ content: NOANIM });
    await p.evaluate(() => document.querySelectorAll('.reveal').forEach(e => e.classList.add('in')));
    const H = await p.evaluate(() => document.documentElement.scrollHeight - innerHeight);
    const end = Math.min(H, 5200);
    await shot(p, OUT + '/site', 270, f => p.evaluate(y => window.scrollTo(0, y), Math.round(lerp(0, end, ease(f / 269)))));
    await p.close();
  }

  // ---------- 3D tervező: interakciók
  if (want('cfg') || want('cfg2')) {
    const p = await ctx.newPage(); p.on('pageerror', e => console.error('ERR', e.message));
    await p.goto(BASE + 'tervezo.html' + (want('cfg') ? '' : ''));
    await p.addStyleTag({ content: NOANIM });
    for (let i = 0; i < 100; i++) { await p.evaluate(() => window.__tick(1)); if (await p.evaluate(() => !!window.zenitCfg)) break; await p.waitForTimeout(100); }
    // a tervezőt a képernyő tetejére görgetjük (fejléc + nézet + panel)
    await p.evaluate(() => { const v = document.querySelector('.cfg-shell'); window.scrollTo(0, v.getBoundingClientRect().top + scrollY - 70); });
    const cam = az => p.evaluate(a => { const c = zenitCfg; c.frame(); const off = c.cam.position.clone().sub(c.ctl.target); off.applyAxisAngle(new THREE.Vector3(0, 1, 0), a); c.cam.position.copy(c.ctl.target).add(off); c.ctl.update(); }, az);
    const panelTo = (sel, t) => p.evaluate(([s, t]) => { const sc = document.querySelector('.panel .scroll'); const el = document.querySelector(s).closest('.step');
      sc.__from = sc.__from == null || t === 0 ? sc.scrollTop : sc.__from; sc.scrollTop = sc.__from + (el.offsetTop - 8 - sc.__from) * t; if (t >= 1) sc.__from = null; }, [sel, t]);
    const click = sel => p.evaluate(s => document.querySelector(s).click(), sel);

    if (want('cfg')) {
      await shot(p, OUT + '/cfg', 390, async f => {
        const ui = (f >= 30 && f <= 45) || (f >= 50 && f <= 110 && f % 2 === 0) || (f >= 120 && f <= 135) || f === 145 || (f >= 175 && f <= 190) || f === 198 || (f >= 228 && f <= 243) || f === 250 || f === 290;
        if (f >= 30 && f <= 45) await panelTo('#w', ease((f - 30) / 15));
        if (f >= 50 && f <= 110 && f % 2 === 0) await p.evaluate(v => { const w = document.getElementById('w'); w.value = v; w.oninput(); }, Math.round(lerp(250, 190, ease((f - 50) / 60))));
        if (f >= 120 && f <= 135) await panelTo('#swWood', ease((f - 120) / 15));
        if (f === 145) await click('#swWood button:nth-child(1)');
        if (f >= 175 && f <= 190) await panelTo('#doorOpts', ease((f - 175) / 15));
        if (f === 198) await p.evaluate(() => [...document.querySelectorAll('#doorOpts .opt')].find(b => b.textContent.trim().startsWith('3')).click());
        if (f >= 228 && f <= 243) await panelTo('#hcol', ease((f - 228) / 15));
        if (f === 250) await click('#hcol .opt[data-c="#B08D57"]');
        if (f === 290) await click('#btnOpen');
        await cam(lerp(-0.22, 0.22, f / 389));
        return ui;
      }, '#cfg3d', true);
    }
    if (want('cfg2')) {
      await p.evaluate(() => { const w = document.getElementById('w'); w.value = 250; w.oninput(); if (zenitCfg.st.open) document.getElementById('btnOpen').click(); });
      await p.evaluate(() => window.__tick(40));
      const seq = [['#swUni button:nth-child(2)', 0], ['#swUni button:nth-child(4)', 30], ['#swUni button:nth-child(7)', 60], ['#swWood button:nth-child(1)', 90], ['#swWood button:nth-child(3)', 120], ['#swUni button:nth-child(1)', 150]];
      await p.evaluate(() => { const sc = document.querySelector('.panel .scroll'); sc.scrollTop = document.getElementById('swUni').closest('.step').offsetTop - 8; });
      await shot(p, OUT + '/cfg2', 180, async f => {
        let ui = false; for (const [s, t] of seq) if (f === t) { await click(s); ui = true; }
        await cam(lerp(0.25, -0.15, f / 179));
        return ui;
      }, '#cfg3d', true);
    }
    await p.close();
  }
  await b.close();
})();
