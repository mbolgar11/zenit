"""ZENIT videó – feliratok és grafikai elemek HTML-ből, átlátszó PNG-ként (Playwright).
Így a magyar ékezetek és a márka-tipográfia pontosan olyan, mint a weboldalon."""
import json, subprocess, pathlib
FONTS = pathlib.Path('/home/claude/zenit-site/assets/fonts').as_uri()
OUT = pathlib.Path('/home/claude/video/ov'); OUT.mkdir(exist_ok=True)

def ff(fam, f, w, st):
    return (f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};src:url({FONTS}/{f}-latin-ext-{w}-{st}.woff2);unicode-range:U+0100-024F,U+2010-2027}}'
            f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};src:url({FONTS}/{f}-latin-{w}-{st}.woff2)}}')
CSS = ''.join([ff('CG', 'cormorant-garamond', 300, 'normal'), ff('CG', 'cormorant-garamond', 300, 'italic'),
               ff('CG', 'cormorant-garamond', 400, 'normal'), ff('In', 'inter', 300, 'normal'), ff('In', 'inter', 400, 'normal'), ff('In', 'inter', 500, 'normal')])
CSS += '''
html,body{margin:0;background:transparent}
body{width:1920px;color:#EDE6DA;font-family:In;-webkit-font-smoothing:antialiased}
.o{display:inline-block;padding:24px}
.k{font:400 17px In;letter-spacing:.34em;text-transform:uppercase;color:#B08D57}
.t{font:300 64px/1.08 CG;letter-spacing:.005em;font-variant-numeric:lining-nums;text-shadow:0 2px 24px rgba(0,0,0,.35)}
.t em{font-style:italic}
.s{font:300 22px/1.5 In;color:#D9D1C4;letter-spacing:.02em;text-shadow:0 1px 12px rgba(0,0,0,.5)}
.wm{font:300 150px/1 CG;letter-spacing:.42em;margin-right:-.42em}
.ml{display:flex;align-items:center}.ml i{display:block;width:1.5px;height:22px;background:#B08D57}.ml b{display:block;flex:1;height:1.5px;background:#B08D57}
.slog{font:300 italic 46px CG;color:#E4DCCF}
.chip{display:inline-flex;align-items:center;gap:16px;padding:16px 26px;border:1px solid rgba(176,141,87,.55);background:rgba(20,18,16,.72);font:300 25px In;color:#EDE6DA;letter-spacing:.01em}
.chip b{font:400 15px In;letter-spacing:.24em;color:#B08D57;text-transform:uppercase}
.card{width:1060px;padding:44px 52px;background:rgba(20,18,16,.86);border:1px solid #3a342d}
.tool{display:grid;grid-template-columns:330px 1fr;gap:6px 26px;font:300 25px/1.55 In;color:#D9D1C4}
.tool b{font:400 25px In;color:#EDE6DA}
.pr{width:900px;padding:30px 36px;background:#211d19;border:1px solid #3a342d;border-left:2px solid #B08D57;font:300 26px/1.5 In;color:#EDE6DA}
.pr small{display:block;font:400 14px In;letter-spacing:.24em;text-transform:uppercase;color:#8C8378;margin-bottom:10px}
.price{font:300 92px/1 CG;font-variant-numeric:lining-nums}
.url{font:300 30px In;letter-spacing:.12em;color:#B08D57}
'''

def logo(scale=1.0, sub=''):
    return (f'<div class="o" style="text-align:center;transform-origin:top left"><div style="display:inline-block">'
            f'<div class="ml" style="margin-bottom:34px"><i></i><b></b><i></i></div><div class="wm">ZENIT</div></div>{sub}</div>')

def cap(k, t, s=''):
    return f'<div class="o" style="max-width:1300px"><div class="k">{k}</div><div class="t" style="margin-top:18px">{t}</div>' + (f'<div class="s" style="margin-top:16px">{s}</div>' if s else '') + '</div>'

OV = {
  'logo': logo(),
  'logo_slogan': logo(sub='<div class="slog" style="margin-top:46px">Ahol a szekrényed véget ér, ott kezdődünk.</div>'),
  'intro_sub': '<div class="o"><div class="k" style="letter-spacing:.42em">AI-kihívás · rátétszekrény · 2026</div></div>',
  'c2a': cap('01 · A kiindulópont', 'Bútorline ELIA · 250 × 205 × 60 cm', 'Belmagasság a legalacsonyabb ponton: 259 cm'),
  'c2b': cap('01 · A kiindulópont', '54 cm, <em>amit senki sem használ.</em>', 'A rátét 530 mm magas – a plafonig 10 mm marad.'),
  'c3a': cap('02 · A 3D modell', 'Egy fájl, <em>minden méret.</em>', 'geometry.py → Autodesk Fusion · STEP · GLB'),
  'c3b': cap('02 · A 3D modell', '530 mm · 18 mm bútorlap · <em>három ajtó</em>', '10 alkatrész · 47 furat-feature · 108 furat'),
  'chip_pant': '<div class="o"><div class="chip"><b>Pánt</b>Häfele Metalla 300SM – fékes csukódás</div></div>',
  'chip_csap': '<div class="o"><div class="chip"><b>Polc</b>3 polctartó csap oldalanként · szeges hátfal</div></div>',
  'chip_fog': '<div class="o"><div class="chip"><b>Fogantyú</b>GTV HEXA 192 · alu elox · hátulról csavarozva</div></div>',
  'c4': '<div class="o"><div class="k">03 · Részletek</div></div>',
  'c5': cap('04 · Gyártás', 'Szabásjegyzék, rajzok,<br><em>fúrósablon.</em>', '16 oldalas gyártási PDF<br>Excel szabásjegyzék és furattábla'),
  'price': '<div class="o"><div style="padding:34px 44px;background:rgba(20,18,16,.92);border:1px solid #3a342d;text-align:right"><div class="k">Anyagköltség (OBI fehér, becslés)</div><div class="price" style="margin-top:14px">≈ 111 000 Ft</div></div></div>',
  'c6': cap('05 · A márka', 'ZENIT – <em>a hiányzó fél méter.</em>', 'Kitalált prémium márka · Blenderben, Python-szkripttel renderelt látványtervek'),
  'c7a': cap('06 · Weboldal', 'Fejezetekben, <em>mint egy könyv.</em>', '11 oldal · GitHub Pages'),
  'c7b': cap('06 · 3D tervező', 'Valós időben, <em>a böngészőben.</em>', 'Szélesség · ajtók · színek és textúrák · fogantyú · polcok'),
  'c8': '<div class="o"><div class="k">07 · Hogyan dolgoztam az AI-jal</div><div class="t" style="margin-top:18px">Claude <em>mint munkatárs.</em></div></div>',
  'tools': '''<div class="o"><div class="card"><div class="tool">
     <b>Claude (Cowork)</b><span>tervezés, kód, döntés-előkészítés</span>
     <b>Autodesk Fusion</b><span>MCP-n át, közvetlenül vezérelve</span>
     <b>Python</b><span>CadQuery · ReportLab · openpyxl</span>
     <b>Blender</b><span>szkriptelt látványtervek</span>
     <b>three.js</b><span>élő 3D tervező a weboldalon</span>
     <b>Piper TTS</b><span>helyben generált magyar narráció</span>
     <b>GitHub Pages</b><span>publikálás, verziókezelés</span></div></div></div>''',
  'pr1': '<div class="o"><div class="pr"><small>Prompt</small>„a polctartó legyen oldalanként 3 csap, ne csak kettő, a hátfal pedig ne csavaros, hanem beütős szeges … ez alapján frissíts mindent”</div></div>',
  'pr2': '<div class="o"><div class="pr"><small>Prompt</small>„az egész terméket úgy akarom bemutatni, mint egy luxus, felső kategóriás elit bútort … a user választhasson színeket, textúrákat, és valós időben változzon a látványterv”</div></div>',
  'end': logo(sub='<div class="slog" style="margin-top:46px">A hiányzó fél méter.</div><div class="url" style="margin-top:40px">mbolgar11.github.io/zenit</div>'),
  'end_promo': logo(sub='<div class="slog" style="margin-top:46px">Ahol a szekrényed véget ér, ott kezdődünk.</div><div class="url" style="margin-top:40px">mbolgar11.github.io/zenit</div>'),
  'demo': '<div class="o"><div class="k" style="color:#8C8378;font-size:13px">Látványterv · koncepció – AI-kihívás projekt</div></div>',
  'p_t1': '<div class="o"><div class="t" style="font-size:78px">Van egy fél méter <em>az otthonodban.</em></div></div>',
  'p_t2': '<div class="o"><div class="t" style="font-size:78px">Pontosan <em>a plafonig.</em></div></div>',
  'p_t3': '<div class="o"><div class="t" style="font-size:78px">A te színeid. <em>A te tered.</em></div></div>',
}

html = '<!doctype html><html><head><meta charset="utf-8"><style>' + CSS + '</style></head><body>' + ''.join(f'<div id="{k}" style="width:max-content">{v}</div>' for k, v in OV.items()) + '</body></html>'
pathlib.Path('/home/claude/video/ov.html').write_text(html, encoding='utf8')
js = '''const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file:///home/claude/video/ov.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
for(const id of %s){await p.locator('#'+id+' > .o').screenshot({path:'/home/claude/video/ov/'+id+'.png',omitBackground:true});}
await b.close();console.log('ok');})();''' % json.dumps(list(OV))
pathlib.Path('/tmp/claude-0/-home-claude/d203fd6a-2896-55a0-bc1b-23668e704c22/scratchpad/v/ov.js').write_text(js)
print(subprocess.run(['node', 'ov.js'], cwd='/tmp/claude-0/-home-claude/d203fd6a-2896-55a0-bc1b-23668e704c22/scratchpad/v', capture_output=True, text=True))
