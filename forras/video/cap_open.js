const {chromium}=require('playwright');const fs=require('fs');
const OUT='/home/claude/video2/open';fs.mkdirSync(OUT,{recursive:true});const FPS=25,N=250,NF=+(process.env.NF||250);
const INIT=`(()=>{let t=0;let q=[];window.requestAnimationFrame=cb=>{q.push(cb);return q.length};window.cancelAnimationFrame=()=>{};
performance.now=()=>t;window.__tick=(n=1)=>{for(let i=0;i<n;i++){t+=1000/${FPS};const c=q;q=[];c.forEach(f=>{try{f(t)}catch(e){console.error(e)}})}};})();`;
(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
const ctx=await b.newContext({viewport:{width:1280,height:720}});await ctx.addInitScript(INIT);const p=await ctx.newPage();p.on('pageerror',e=>console.error('ERR',e.message));
await p.goto('http://localhost:8766/tervezo.html#preset=referencia');
await p.addStyleTag({content:'#hdr,.panel,.asm,.dims,.hint,.toolbar,.tools{display:none!important}.cfg-wrap{padding:0!important}.cfg-shell{grid-template-columns:1fr!important;height:100vh!important;border:0}.viewer{height:100vh}*{transition:none!important}'});
for(let i=0;i<60;i++){await p.evaluate(()=>window.__tick(1));if(await p.evaluate(()=>!!window.zenitCfg))break;await p.waitForTimeout(100)}
await p.evaluate(()=>window.__tick(5));
const sk=+(process.env.SKIP||0);
for(let f=0;f<Math.min(N,(+(process.env.SKIP||0))+NF);f++){
  const d=await p.evaluate(([f,N,grab])=>{const c=zenitCfg,st=c.st,W=st.w/100,C=st.ceil/100,BH=st.baseH/100,H=C-BH;
    const ds=c.doors();const open=(i,o)=>{ds[i].userData.target=o?(ds[i].userData.left?-1:1)*1.75:0};
    ds.forEach((d,i)=>{if(f===28+i*14)open(i,true);if(f===N-70+i*8)open(i,false)});
    const k=Math.sin(Math.PI*f/N); const az=0.36-0.2*k, dist=6.2-2.0*k, ty=BH*0.55+(BH+H*0.5-BH*0.55)*k;
    c.ctl.target.set(W/2,ty,-st.d/200); c.cam.position.set(W/2+Math.sin(az)*dist, ty+0.18+0.1*k, Math.cos(az)*dist); c.cam.lookAt(c.ctl.target);
    c.ctl.enabled=false; window.__tick(1); return grab?document.getElementById('cfg3d').toDataURL('image/jpeg',0.92):null},[f,N,f>=sk]);
  if(d)fs.writeFileSync(`${OUT}/${String(f).padStart(4,'0')}.jpg`,Buffer.from(d.split(',')[1],'base64'));if(f%50===0)console.log(f)}
await b.close();console.log('kész')})();
