// Az Ön terve: az utolsó mentett terv megjelenítése a tervezőből
(function(){try{
  const plans=JSON.parse(localStorage.getItem('zenitPlans')||'[]'); if(!plans.length) return;
  const p=plans[plans.length-1];
  const nm=v=>({oak:'Natúr tölgy',smoked:'Füstölt tölgy',walnut:'Dió',linen:'Len',concrete:'Beton','#F1EFEA':'Kréta','#CDBFAE':'Kasmír','#D8CBB3':'Homok','#A4AD98':'Zsálya','#A7735A':'Agyag','#4A4846':'Grafit','#273445':'Éjkék','#1B1A19':'Fekete'}[v]||v);
  const hn={edge:'Élfogantyú',bar:'Rúd',knob:'Gomb / bőrfül',push:'Nyomásra nyíló'}[p.handle]||'';
  const hc={'#C9C6C0':'alu elox','#1E1E1E':'matt fekete','#B08D57':'bronz','#7A4E2D':'bőr'}[p.hcol]||'';
  const fin={matt:'matt',satin:'selyemfény',gloss:'magasfény'}[p.fin];
  const ex=[p.led&&'Belső LED',p.trim&&'Plafonzáró léc',p.box&&'Tárolódobozok'].filter(Boolean).join(', ')||'–';
  const rows=[['Szélesség × magasság × mélység',`${p.w} × ${p.h} × ${p.d} cm`],['Ajtók',p.doors+' db'],['Ajtó / korpusz / belső',`${nm(p.ajto)} / ${nm(p.korpusz)} / ${nm(p.belso)}, ${fin}`],
    ['Fogantyú',hn+(p.handle!=='push'?', '+hc:'')],['Polc',(p.shelves||[]).map(s=>s+'.').join(', ')+' rekesz'],['Extrák',ex],['Pántok','Häfele, fékes']];
  const tb=document.querySelector('#planTable tbody');
  tb.innerHTML=rows.map(r=>`<tr><td>${r[0]}</td><td>${r[1]}</td></tr>`).join('')+`<tr><td><b style="font:300 24px var(--serif);color:var(--ink)">Becsült ár</b></td><td><b style="font:300 30px var(--serif)">${p.price}</b></td></tr>`;
  if(p.img){const im=document.querySelector('.plan-sum .frame img');im.src=p.img;im.nextElementSibling.textContent='Az Ön terve · élő 3D';}
}catch(e){}})();
