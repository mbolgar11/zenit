(() => {
  const p = ZPlan.last(), tb = document.querySelector('#planTable tbody'); if (!tb) return;
  if (p.ref) return;
  tb.innerHTML = ZPlan.rows(p).map(([a, b]) => `<tr><td>${a}</td><td>${b}</td></tr>`).join('') +
    `<tr><td><b style="font:300 24px var(--serif);color:var(--fg)">Becsült ár</b></td><td><b style="font:300 30px var(--serif)">${p.price}</b></td></tr>`;
  if (p.img) document.getElementById('planImg').src = p.img;
})();
