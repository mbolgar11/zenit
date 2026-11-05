/* ZENIT – személyre szabott, nyomtatható kézikönyv a mentett tervből */
(() => {
  const root = document.getElementById('manual'); if (!root) return;
  const p = ZPlan.last(), S = window.ZSTEPS || [], n = p.doors || 3;
  const today = new Date().toLocaleDateString('hu-HU', { year: 'numeric', month: 'long', day: 'numeric' });
  const logo = '<span class="mlogo"><span class="rule"><i></i></span><span class="word">ZENIT</span></span>';
  const head = (t, no) => `<div class="mh">${logo}<span>${t}</span><span>${p.serial} · ${no}</span></div>`;
  const foot = '<div class="mf"><span>ZENIT Atelier · Budapest · hello@zenit.example</span><span>Koncepció – AI-kihívás projekt</span></div>';
  // vasalat a tervhez számolva
  const shelves = (p.shelves || []).length, handles = p.handle === 'push' ? 0 : n;
  const HW = [['Fatipli 8×35', 4 * (n + 1)], ['Konfirmát 7×50 + takarósapka', 4 * (n + 1)], ['Häfele Metalla 300SM pánt (fékes + rugós)', 2 * n], ['Häfele szerelőtalp', 2 * n],
    ['Csavar 3,5×16', 8 * n + 2 * handles], ['Csavar 3,5×30 (rögzítés a szekrényhez)', 4], ['Polctartó csap Ø5', 6 * shelves], ['Hátfalszeg 1,6×25', Math.round(50 * p.w / 250)]];
  if (handles) HW.push([p.handle === 'edge' ? 'GTV HEXA 192 élfogantyú' : 'Fogantyú', handles]);
  if (p.handle === 'push') HW.push(['Nyomásra nyitó (TIP-ON)', n]);
  if (p.wall) HW.push([`Rejtett távtartó léc (${String(p.wall).replace('.', ',')} cm)`, 3]);
  if (p.trim) HW.push(['Takaróléc a plafonhoz' + (p.slope ? ' (ferdére szabva)' : ''), 1]);
  if (p.led) HW.push(['LED-szalag + ajtókapcsoló', n]);
  const mirrors = (p.mirror || []).filter(Boolean).length; if (mirrors) HW.push(['Tükör 4 mm, biztonsági fóliával (gyárilag felragasztva)', mirrors]);
  const TOOLS = ['Akkus csavarozó, PZ2 bit', 'Konfirmát kulcs (4 mm, a csomagban)', 'Gumikalapács', 'Kis kalapács', 'Mérőszalag', 'Két létra', 'Ø2,5 fúrószár', 'PZ2 csavarhúzó', 'Vízmérték', 'Két ember'];
  const hingeTxt = (p.hinge || []).map((h, i) => `${i + 1}. ajtó ${h === 'L' ? 'balra' : 'jobbra'}${p.mirror && p.mirror[i] ? ' (tükrös)' : ''}`).join(', ');
  const extra = {
    8: (p.wall ? ` Felemelés előtt csavarozd a három rejtett távtartót (${String(p.wall).replace('.', ',')} cm) a hátfal mögé, a jelölt helyekre – így a ZENIT a falhoz simul, a korpusz derékszögű marad.` : ''),
    10: ` Az Ön terve szerint: ${hingeTxt}.` + (mirrors ? ' A tükrös ajtókat mindig két kézzel, az élüknél fogd meg.' : ''),
    12: (p.trim ? ` Végül pattintsd fel a takarólécet a tetőlap elejére${p.slope ? ' – ferdére szabva, a magasabb vége a jobb oldalra kerül' : ''}.` : '') + (p.led ? ' A LED-et a csomagban lévő dugós csatlakozóval kösd össze, és tedd a konnektorba.' : '')
  };
  const sheets = [];
  // 1. borító
  sheets.push(`<div class="sheet cover">${head('Használati és szerelési kézikönyv', '1')}
    <div class="cv"><div class="label">Az Ön ZENIT-je</div><h2 class="h1" style="margin:18px 0 10px">Ahol a szekrényed véget ér, <em>ott kezdődünk.</em></h2>
    <p class="lead">Ez a kézikönyv az Ön tervéből készült ${today}-án. ${p.ref ? '(Mentett terv híján a 250 cm-es referencia-darabot mutatjuk.)' : ''}</p></div>
    <div class="cvimg"><img src="${p.img}" alt="Az Ön terve"></div>
    <table class="mt">${ZPlan.rows(p).map(([a, b]) => `<tr><td>${a}</td><td>${b}</td></tr>`).join('')}${p.ref ? '' : `<tr><td>Becsült ár</td><td>${p.price}</td></tr>`}</table>${foot}</div>`);
  // 2. előkészület
  sheets.push(`<div class="sheet">${head('Mielőtt elkezdené', '2')}
    <h3 class="h3">Három szabály, <em>és minden sikerül.</em></h3>
    <ol class="ml"><li>Puha takarón dolgozzon – a lapok éle és felülete hálás lesz érte.</li><li>A konfirmátot ütközésig húzza, utána csak negyed fordulatot.</li><li>Emelni mindig ketten kell: a korpusz ajtók nélkül kb. ${Math.round(56 * p.w / 250)} kg.</li></ol>
    <div class="cols"><div><h4>Szerszámok</h4><ul class="ml">${TOOLS.map(t => `<li>${t}</li>`).join('')}</ul></div>
    <div><h4>Vasalat az Ön tervéhez</h4><table class="mt small">${HW.map(([a, b]) => `<tr><td>${a}</td><td>${b} db</td></tr>`).join('')}</table></div></div>
    <p class="note">Az ábrák a 250 cm-es, három ajtós referencia-darabot mutatják. Az Ön ${n} ajtós ZENIT-je pontosan ugyanígy, ugyanebben a sorrendben áll össze – csak a közfalak és az ajtók száma más.</p>${foot}</div>`);
  // 3+. lépések (két lépés / oldal)
  for (let i = 0; i < S.length; i += 2) {
    sheets.push(`<div class="sheet">${head('Szerelés', 3 + i / 2)}${S.slice(i, i + 2).map(s => `
      <div class="ms"><div class="no">${String(s.no).padStart(2, '0')}</div><div><h4>${s.title}</h4><p>${s.text}${extra[s.no] || ''}</p>
      ${s.need && s.need.length ? `<div class="need">${s.need.map(([a, b]) => `<span><b>${b}×</b> ${a}</span>`).join('')}</div>` : ''}
      ${s.warn ? `<div class="warn">${s.warn}</div>` : ''}</div><img src="assets/ill/szereles/${s.svg}" alt="${s.title}"></div>`).join('')}${foot}</div>`);
  }
  // ápolás + garancia
  sheets.push(`<div class="sheet">${head('Ápolás és Örökgarancia', 3 + Math.ceil(S.length / 2))}
    <div class="cols"><div><h4>Ápolás</h4><ul class="ml"><li>Puha, enyhén nedves pamutkendő; utána szárazra törölni.</li><li>Ne használjon súrolószert, alkoholt vagy oldószert.</li><li>A tükröt üvegtisztítóval, a kendőre fújva tisztítsa – ne közvetlenül a tükörre.</li>
    <li>Évente egyszer ellenőrizze a pántokat; a hézagot a pánt három csavarjával állíthatja.</li><li>Polconként legfeljebb 25 kg, egyenletesen elosztva.</li></ul></div>
    <div class="cert"><img src="assets/ill/seal.svg" alt="ZENIT pecsét"><div class="label plain">ZENIT Örökgarancia <span class="demo">Demó</span></div>
    <p>Amíg a lap, a szín és a vasalat kapható, a ZENIT minden eleme pótolható, cserélhető vagy bővíthető.</p>
    <dl><dt>Sorszám</dt><dd>${p.serial}</dd><dt>Méret</dt><dd>${p.w} × ${p.h} × ${p.d} cm</dd><dt>Dátum</dt><dd>${today}</dd></dl>
    <div class="sig"><span>Készítette</span><span>Ellenőrizte</span></div></div></div>${foot}</div>`);
  root.innerHTML = sheets.join('');
})();
