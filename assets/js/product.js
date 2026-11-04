// before/after
(()=>{const ba=document.getElementById('ba'),b=ba.querySelector('.before'),h=document.getElementById('baHandle');
 const set=x=>{const r=ba.getBoundingClientRect();let p=Math.min(1,Math.max(0,(x-r.left)/r.width))*100;b.style.clipPath=`inset(0 ${100-p}% 0 0)`;h.style.left=p+'%'};
 let d=false;ba.addEventListener('pointerdown',e=>{d=true;set(e.clientX)});addEventListener('pointerup',()=>d=false);addEventListener('pointermove',e=>d&&set(e.clientX));})();
// exploded placeholder
(()=>{const c=document.getElementById('exCanvas'),st=document.getElementById('explode');if(!c)return;
 const P=[[10,8,80,3,0,-60],[10,46,80,3,0,60],[10,8,3,41,-70,0],[87,8,3,41,70,0],[38,11,3,35,-20,0],[59,11,3,35,20,0],[10,11,27,35,-30,-10],[38,11,21,35,0,-40],[60,11,27,35,30,-10]];
 const els=P.map((p,i)=>{const d=document.createElement('div');d.className='part';Object.assign(d.style,{left:p[0]+'%',top:(p[1]+18)+'%',width:p[2]+'%',height:p[3]+'%',opacity:i>5?.55:1});c.appendChild(d);return d});
 addEventListener('scroll',()=>{const r=st.getBoundingClientRect(),t=Math.min(1,Math.max(0,-r.top/(r.height-innerHeight)));const k=Math.sin(t*Math.PI);
  els.forEach((d,i)=>d.style.transform=`translate(${P[i][4]*k*.6}px,${P[i][5]*k*.6}px)`)},{passive:true});})();
