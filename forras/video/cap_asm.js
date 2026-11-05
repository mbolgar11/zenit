const {chromium}=require('playwright');const fs=require('fs');
const T=JSON.parse(fs.readFileSync('/home/claude/video2/asm_timing.json'));const OUT='/home/claude/video2/asm';fs.mkdirSync(OUT,{recursive:true});
const FPS=25, N=Math.round((T.durs.reduce((a,b)=>a+b,0)+0.5)*FPS);
const INIT=`(()=>{let t=0;let q=[];window.requestAnimationFrame=cb=>{q.push(cb);return q.length};window.cancelAnimationFrame=()=>{};
performance.now=()=>t;window.__tick=(n=1)=>{for(let i=0;i<n;i++){t+=1000/${FPS};const c=q;q=[];c.forEach(f=>{try{f(t)}catch(e){console.error(e)}})}};window.__jump=(ms)=>{t+=ms;window.__tick(1)};window.ZENIT_DURS=${JSON.stringify(T.durs)};window.ZENIT_ASMDIST=3.9;window.ZENIT_ASMDY=0.06;})();`;
(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
const ctx=await b.newContext({viewport:{width:1280,height:720}});await ctx.addInitScript(INIT);const p=await ctx.newPage();
p.on('pageerror',e=>console.error('ERR',e.message));
await p.goto('http://localhost:8766/tervezo.html#preset=referencia');
await p.addStyleTag({content:'#hdr,.panel,.asm,.dims,.hint,.toolbar,.tools{display:none!important}.cfg-wrap{padding:0!important}.cfg-shell{grid-template-columns:1fr!important;height:100vh!important;border:0}.viewer{height:100vh}*{transition:none!important}'});
for(let i=0;i<60;i++){await p.evaluate(()=>window.__tick(1));if(await p.evaluate(()=>!!window.zenitCfg))break;await p.waitForTimeout(100)}
await p.evaluate(()=>window.__tick(5));
await p.evaluate(()=>zenitCfg.startAsm(false));
const t0=Date.now();
const SK=+(process.env.SKIP||0),NF=+(process.env.NF||N);if(SK)await p.evaluate(n=>window.__jump(n*1000/25),SK);
for(let f=SK;f<Math.min(N,SK+NF);f++){const d=await p.evaluate(()=>{window.__tick(1);return document.getElementById('cfg3d').toDataURL('image/jpeg',0.92)});
fs.writeFileSync(`${OUT}/${String(f).padStart(4,'0')}.jpg`,Buffer.from(d.split(',')[1],'base64'));if(f%50===0)console.log(f,'/',N,((Date.now()-t0)/(f+1)/1000).toFixed(2),'s/kocka')}
await b.close();console.log('kész')})();
