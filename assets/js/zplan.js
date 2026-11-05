/* ZENIT – közös: a mentett terv olvasása és szöveges leírása */
window.ZPlan = (function () {
  const NAMES = { '#CDBFAE': 'Kasmír', '#F1EFEA': 'Kréta', '#D8CBB3': 'Homok', '#A4AD98': 'Zsálya', '#A7735A': 'Agyag', '#4A4846': 'Grafit', '#273445': 'Éjkék', '#1B1A19': 'Fekete',
    oak: 'Natúr tölgy', smoked: 'Füstölt tölgy', walnut: 'Dió', concrete: 'Beton', linen: 'Len' };
  const HN = { edge: 'GTV HEXA élfogantyú, 192 mm', bar: 'Rúd, 320 mm', knob: 'Gomb / bőrfül', push: 'Nyomásra nyíló' };
  const HC = { '#C9C6C0': 'alu elox', '#1E1E1E': 'matt fekete', '#B08D57': 'bronz', '#7A4E2D': 'bőr' };
  const FN = { matt: 'matt', satin: 'selyemfényű', gloss: 'magasfényű' };
  const col = c => NAMES[c] || NAMES[(c || '').toUpperCase()] || (c || '').toUpperCase();
  const DEF = { w: 250, h: 53, d: 60, ceil: 259, baseH: 205, doors: 3, split: 'sym', hinge: ['L', 'R', 'R'], mirror: [false, false, false], slope: 0, wall: 0,
    ajto: '#CDBFAE', korpusz: '#CDBFAE', belso: '#F1EFEA', fin: 'matt', handle: 'edge', hcol: '#C9C6C0', shelves: [2], led: true, trim: false, box: false,
    price: '—', img: 'assets/img/r2/after_day.jpg', serial: 'ZN-2026-0001', ref: true };
  function last() {
    try { const p = JSON.parse(localStorage.getItem('zenitPlans') || '[]'); if (p.length) return Object.assign({}, DEF, p[p.length - 1], { ref: false }); } catch (e) { }
    return DEF;
  }
  function rows(p) {
    const hinge = (p.hinge || []).map((h, i) => `${i + 1}. ${h === 'L' ? 'balra' : 'jobbra'}${p.mirror && p.mirror[i] ? ' · tükör' : ''}`).join(', ');
    return [
      ['Méret (sz × m × mé)', `${p.w} × ${p.h} × ${p.d} cm`],
      ['Belmagasság / alatta lévő szekrény', `${p.ceil} cm / ${p.baseH} cm`],
      ['Illesztés', (p.slope ? `ferde plafon: jobb oldalon +${String(p.slope).replace('.', ',')} cm` : 'vízszintes plafon') + ' · ' + (p.wall ? `falkiegyenlítés ${String(p.wall).replace('.', ',')} cm` : 'falhoz illesztve')],
      ['Ajtók', `${p.doors} db, ${p.split === 'sym' ? 'középen szélesebb' : 'egyenlő'} osztás`],
      ['Nyitásirány és front', hinge],
      ['Ajtó / korpusz / belső', `${col(p.ajto)} / ${col(p.korpusz)} / ${col(p.belso)}, ${FN[p.fin] || p.fin}`],
      ['Fogantyú', `${HN[p.handle] || p.handle}, ${HC[p.hcol] || p.hcol}`],
      ['Polc', (p.shelves || []).sort().map(s => s + '. rekesz').join(', ') || '—'],
      ['Extrák', [p.led && 'belső LED', p.trim && 'takaróléc', p.box && 'tárolódobozok'].filter(Boolean).join(', ') || '—'],
      ['Pántok', 'Häfele Metalla 300SM, felül fékes'],
      ['Sorszám', p.serial]];
  }
  return { last, rows, col };
})();
