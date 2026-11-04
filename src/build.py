"""ZENIT oldalgenerátor – közös fejléc/lábléc, oldalanként tartalom. Futtatás: python3 src/build.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(os.path.join(ROOT, "src", "parts.json")))

FONTS = "".join(
    f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};font-display:swap;src:url(../fonts/{f}-latin-ext-{w}-{st}.woff2) format("woff2");unicode-range:U+0100-024F,U+2010-2027}}'
    f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};font-display:swap;src:url(../fonts/{f}-latin-{w}-{st}.woff2) format("woff2")}}'
    for fam, f, w, st in [("Cormorant", "cormorant-garamond", 300, "normal"), ("Cormorant", "cormorant-garamond", 400, "normal"),
                          ("Cormorant", "cormorant-garamond", 300, "italic"), ("Inter", "inter", 300, "normal"),
                          ("Inter", "inter", 400, "normal"), ("Inter", "inter", 500, "normal")])

FAV = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23141210'/%3E"
       "%3Crect x='8' y='8' width='48' height='2' fill='%23B08D57'/%3E%3Crect x='8' y='5' width='2' height='8' fill='%23B08D57'/%3E%3Crect x='54' y='5' width='2' height='8' fill='%23B08D57'/%3E"
       "%3Ctext x='32' y='52' font-family='Georgia,serif' font-size='38' fill='%23EDE6DA' text-anchor='middle'%3EZ%3C/text%3E%3C/svg%3E")

KOLL = [("zenit.html", "A ZENIT", "A hiányzó fél méter, megoldva"),
        ("anyagok.html", "Anyagok és színek", "Paletta, textúrák, ZENIT Natúr"),
        ("manufaktura.html", "Manufaktúra", "Magyar kézművesség, egyedi darabok"),
        ("inspiracio.html", "Inspiráció", "Egy forma, ezer otthon"),
        ("keszites.html", "Hogyan készül", "Tervtől a plafonig"),
        ("garancia.html", "Örökgarancia", "Egy életre tervezve")]
CONC = [("tervezo.html", "Tervező", "Állítsd össze a sajátod"),
        ("terv.html", "Az Ön terve", "Mentett tervek, ajánlat, rendelés"),
        ("concierge.html", "Személyes konzultáció", "Tervezőnk visszahív"),
        ("projekt.html", "A projektről", "AI kihívás: videó, 3D, napló")]


def header(cur):
    def drop(items, feat):
        return ('<div class="drop">' + feat + "".join(f'<a href="{h}"><b>{t}</b><span>{d}</span></a>' for h, t, d in items) + "</div>")
    kc = "cur" if cur in [h for h, *_ in KOLL] else ""
    cc = "cur" if cur in [h for h, *_ in CONC] else ""
    return f'''<header id="hdr">
  <div class="wrap nav">
    <a href="index.html" class="logo" aria-label="ZENIT – kezdőlap"><span class="rule"></span><span class="word">ZENIT</span></a>
    <ul class="main">
      <li class="{kc}"><a href="zenit.html">Kollekció</a>{drop(KOLL, '<a class="feat" href="zenit.html"><b>A ZENIT</b><span>Ahol a szekrényed véget ér</span></a>')}</li>
      <li class="{cc}"><a href="concierge.html">Concierge</a>{drop(CONC, '<a class="feat" href="tervezo.html" style="background-image:url(assets/img/r/open_led.jpg)"><b>Tervező</b><span>Élő 3D, a te méreteidre</span></a>')}</li>
    </ul>
    <div class="right">
      <span class="lang"><b>HU</b> / EN</span>
      <a href="terv.html" class="plan" title="Az Ön terve"><svg viewBox="0 0 16 16" fill="none" stroke="#EDE6DA" stroke-width="1"><path d="M2 3.5h12M2.5 3.5v9h11v-9M8 3.5v9"/><path d="M1 1.5h3M12 1.5h3" stroke="#B08D57"/></svg><i style="display:none">0</i></a>
      <a href="tervezo.html" class="btn">Tervezd meg</a>
      <button class="burger" data-menu aria-label="Menü"></button>
    </div>
  </div>
</header>
<nav class="mnav" id="mnav"><button class="x" data-menu aria-label="Bezárás">×</button>
  <div><h6>Kollekció</h6>{"".join(f'<a href="{h}">{t}</a>' for h, t, _ in KOLL)}</div>
  <div><h6>Concierge</h6>{"".join(f'<a href="{h}">{t}</a>' for h, t, _ in CONC)}</div>
</nav>'''


FOOTER = '''<footer>
  <div class="wrap">
    <div class="foot">
      <div><a class="logo" href="index.html"><span class="rule"></span><span class="word">ZENIT</span></a><p style="margin-top:20px;max-width:32ch">Ahol a szekrényed véget ér, ott kezdődünk.</p></div>
      <div><h5>Kollekció</h5><ul>''' + "".join(f'<li><a href="{h}">{t}</a></li>' for h, t, _ in KOLL) + '''</ul></div>
      <div><h5>Concierge</h5><ul>''' + "".join(f'<li><a href="{h}">{t}</a></li>' for h, t, _ in CONC) + '''</ul></div>
      <div><h5>Kapcsolat</h5><ul><li>hello@zenit.example</li><li>Budapest</li><li><a href="projekt.html">A projektről</a></li></ul></div>
    </div>
    <div class="legal"><span>© 2026 ZENIT · Koncepció – AI kihívás projekt, nem valós webáruház.</span><span>Minden kép látványterv.</span></div>
  </div>
</footer>'''


def chapter(no, href, title, text, alts=""):
    return f'''<section class="chapter"><div class="wrap">
  <a href="{href}"><div><div class="kicker">Következő fejezet · {no}</div><div class="t">{title}</div><p>{text}</p></div><span class="circle"><span class="arrow"></span></span></a>
  {f'<div class="alt">{alts}</div>' if alts else ''}
</div></section>'''


ALT_CTA = '<span>Vagy:</span><a href="tervezo.html">Ugrás a tervezőbe</a><a href="concierge.html">Beszélek egy tervezővel</a>'


def crumb(*items):
    return '<div class="crumb">' + '<i>/</i>'.join(f'<a href="{h}">{t}</a>' if h else t for h, t in items) + '</div>'


def page_hero(kicker, title, lead, bg=None, cls="", cr=None):
    bgdiv = f'<div class="bg" style="background-image:url({bg})"></div>' if bg else ""
    return f'''<section class="page-hero {cls}">{bgdiv}<div class="wrap">
  {crumb(*cr) if cr else ''}<div class="kicker">{kicker}</div><h1 class="h1">{title}</h1><p class="lead">{lead}</p></div></section>'''


ICONS = open(os.path.join(ROOT, "assets/ill/icons.svg")).read()


def page(fname, title, desc, body, scripts=(), solid=False):
    html = f'''<!doctype html>
<html lang="hu">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="icon" href="{FAV}">
<style>{FONTS}</style>
<link rel="stylesheet" href="assets/css/zenit.css">
</head>
<body{' data-solid="1"' if solid else ''}>
{ICONS}
{header(fname)}
<main>
{body}
</main>
{FOOTER}
<script src="assets/js/common.js"></script>
{"".join(f'<script src="assets/js/{s}"></script>' for s in scripts)}
</body>
</html>
'''
    open(os.path.join(ROOT, fname), "w").write(html)
    print("ok", fname)


SEC = lambda inner, cls="", style="": f'<section class="sec {cls}" style="{style}"><div class="wrap">{inner}</div></section>'
HEAD = lambda k, t, lead="": f'<div class="sec-head reveal"><div><div class="kicker">{k}</div><h2 class="h2">{t}</h2></div>{f"<p class=lead>{lead}</p>" if lead else ""}</div>'

STORY = '''<section class="story" id="tortenet"><div class="wrap">
  <div class="sec-head reveal" style="margin:clamp(80px,10vw,140px) 0 0"><div><div class="kicker">Egy történet</div><h2 class="h2">Nem több helyet adunk. <em>Több nyugalmat.</em></h2></div><p class="lead">Mert ami a fejünk fölött van, az a fejünkben is ott van.</p></div>
  <div class="scene dim reveal"><div class="frame"><img src="assets/img/r/story_night.jpg" alt="Este: dobozok és bőrönd a gardrób tetején"><span class="render-tag">Látványterv</span></div>
    <div><div class="time">Este, tizenegy óra.</div><h3>Lekapcsolod a villanyt. <em>Még egyszer látod.</em></h3><p>A bőröndöt a tavalyi nyaralásról. A dobozt, amit „majd elpakolsz”. A vékony porréteget, amit csak oldalfényben veszel észre. Fél méter, ami minden este ugyanazt mondja: ez még nincs kész.</p></div></div>
  <div class="scene dim reveal"><div class="frame"><img src="assets/img/r/before_day.jpg" alt="Nappal: a rendetlen gardróbtető"><span class="render-tag">Látványterv</span></div>
    <div><div class="time">Ami fent van,</div><h3>az fejben is <em>ott van.</em></h3><p>Egy szoba sosem lesz nyugodt, ha a legmagasabb pontja zajos. Rendet rakhatsz a polcokon, kivasalhatod az ágyneműt – a szemed mindig felfelé téved.</p></div></div>
  <div class="scene reveal"><div class="frame"><img src="assets/img/r/story_morning.jpg" alt="Reggel: a ZENIT a plafonig ér"><span class="render-tag">Látványterv</span></div>
    <div><div class="time">Aztán egy reggel.</div><h3>A fal egyetlen <em>nyugodt felület.</em> Plafonig.</h3><p>A vonal ott fut, ahol a szekrényed véget ért – és nem áll meg. A szoba hirtelen magasabb lesz. A bőrönd, a téli takaró, az emlékek doboza eltűnik egy ajtó mögött, ami csendben, puhán csukódik be.</p></div></div>
  <div class="scene reveal"><div class="frame"><img src="assets/img/r/hero_evening.jpg" alt="Este: a ZENIT csendben, lámpafényben" style="object-position:30% 50%"><span class="render-tag">Látványterv</span></div>
    <div><div class="time">És este, megint.</div><h3>Lekapcsolod a villanyt. <em>És csend van.</em></h3><p>Nem látsz semmit, ami dolgod lenne. Csak egy befejezett szobát. Ezt adja a ZENIT: nem egy újabb bútort – hanem azt az érzést, hogy az otthonod végre <em>kész</em>.</p></div></div>
  <div style="padding:clamp(80px,10vw,140px) 0" class="reveal"><p class="big-quote">„Az otthon akkor kész, amikor már nem keresel <em>rajta semmit.</em>”</p></div>
</div></section>'''

FEEL = SEC(HEAD("Amit valójában kapsz", "Öt érzés, <em>egy bútorban.</em>") + '''<div class="feel reveal">
  <div><svg class="ico"><use href="#i-nyugalom"/></svg><b><i>01</i>Nyugalom</b><span>Vizuális csend a szoba legmagasabb pontján. Semmi, ami a szemed sarkában kiabál.</span></div>
  <div><svg class="ico"><use href="#i-tagassag"/></svg><b><i>02</i>Tágasság</b><span>A plafonig futó vonal optikailag megemeli a teret – a szoba magasabbnak, nagyobbnak hat.</span></div>
  <div><svg class="ico"><use href="#i-rend"/></svg><b><i>03</i>Rend</b><span>Mindennek megvan a helye: bőrönd, téli takaró, emlékek. Egy ajtó mögött.</span></div>
  <div><svg class="ico"><use href="#i-buszkeseg"/></svg><b><i>04</i>Büszkeség</b><span>Egyedi, sorszámozott darab, ami csak a te otthonodra készült.</span></div>
  <div><svg class="ico"><use href="#i-szabadsag"/></svg><b><i>05</i>Szabadság</b><span>Falfúrás nélkül, bérlakásban is. Ha költözöl, viszed magaddal.</span></div>
</div>''', style="padding-top:0")

CRAFT_HOME = SEC('''<div class="split rev reveal">
  <div><div class="kicker">Manufaktúra</div><h2 class="h2" style="margin-top:18px">Magyar kézművesség. <em>Egyetlen otthonra.</em></h2>
  <div class="prose" style="margin-top:24px"><p>Minden ZENIT megrendelésre, a te méreteidre készül – hazai műhelyben, a magyar asztaloshagyomány felhalmozott tudására építve. Kézzel állítjuk össze, kézzel ellenőrizzük, és minden darab egyedi sorszámot kap.</p></div>
  <a class="btn" href="manufaktura.html" style="margin-top:30px">A műhely története <span class="arrow"></span></a></div>
  <div class="frame" style="aspect-ratio:4/5"><img src="assets/img/r/macro_handle_oak.jpg" alt="Natúr tölgy ajtó lekerekített fogantyúval"><span class="render-tag">Látványterv</span></div>
</div>''', style="padding-top:0")

# ---------------------------------------------------------------- KEZDŐLAP
page("index.html", "ZENIT – Ahol a szekrényed véget ér, ott kezdődünk.",
     "ZENIT – méretre tervezett felső szekrény a meglévő gardróbod tetejére, milliméterre a plafonig.",
     '''<section class="hero" id="top">
  <div class="media" role="img" aria-label="ZENIT felső szekrény egy hálószobában – látványterv"></div>
  <div class="wrap content">
    <div class="kicker">A hiányzó fél méter</div>
    <h1 class="h1">Ahol a szekrényed véget ér, <em>ott kezdődünk.</em></h1>
    <p class="lead">Méretre tervezett felső szekrény a meglévő gardróbod tetejére – milliméterre a plafonig, falfúrás nélkül, prémium vasalattal.</p>
    <div class="cta"><a href="zenit.html" class="btn fill">Ismerd meg a ZENIT-et <span class="arrow"></span></a><a href="tervezo.html" class="btn ghost">Tervezd meg</a></div>
  </div>
  <div class="scroll"></div><div class="video-note">Látványterv · a végleges oldalon háttérvideó</div>
</section>''' +
     SEC('''<div class="split reveal"><div><div class="kicker">ZENIT</div><h2 class="h2" style="margin-top:18px">Nem egy újabb doboz. <em>A szekrényed befejezése.</em></h2></div>
  <div class="prose"><p>Minden lakásban ott van: fél méter csend a gardrób teteje és a plafon között. Porfogó, bőröndtemető, félbehagyott mondat.</p>
  <p>A ZENIT ezt a mondatot fejezi be. Milliméterre a te plafonodhoz méretezzük, a te színeidben készül, és úgy simul a meglévő szekrényedre, mintha mindig is ott lett volna.</p></div></div>''') +
     STORY + FEEL +
     CRAFT_HOME +
     SEC(HEAD("Fedezd fel", "Három fejezet <em>a tökéletes befejezésig.</em>") + '''<div class="teasers reveal">
  <a class="teaser" href="zenit.html"><div class="bg" style="background-image:url(assets/img/r/after_day.jpg)"></div><div><div class="kicker">01</div><b>A ZENIT</b><span>Felépítés, méretek, a hiányzó fél méter.</span></div></a>
  <a class="teaser" href="anyagok.html"><div class="bg" style="background-image:url(assets/img/r/macro_handle_oak.jpg)"></div><div><div class="kicker">02</div><b>Anyagok és színek</b><span>Kurált paletta, valódi furnér, kézbe simuló vasalat.</span></div></a>
  <a class="teaser" href="inspiracio.html"><div class="bg" style="background-image:url(assets/img/r/insp_ejkek.jpg)"></div><div><div class="kicker">03</div><b>Inspiráció</b><span>Egy forma, ezer otthon.</span></div></a>
</div>''', style="padding-top:0") +
     SEC('<div class="reveal">' + P["stats"] + '</div>', style="padding-top:0") +
     chapter("01", "zenit.html", "A ZENIT", "Ismerd meg, hogyan lesz a kihasználatlan sávból a lakás legelegánsabb tárhelye.", ALT_CTA))

# ---------------------------------------------------------------- A ZENIT
page("zenit.html", "A ZENIT – felső szekrény a plafonig", "A ZENIT felépítése, méretei és előnyei.",
     page_hero("Kollekció · 01", "A hiányzó fél méter, <em>megoldva.</em>",
               "Egy korpusz, egybefüggő tető, csendes ajtók. Méretre tervezve a meglévő szekrényedhez – a plafonig.",
               "assets/img/r/after_day.jpg", cr=[("index.html", "ZENIT"), ("", "Kollekció"), ("", "A ZENIT")]) +
     SEC(HEAD("A probléma", "Minden lakásban ott van. <em>Fél méter csend</em> a szekrény fölött.",
              "A gardrób teteje és a plafon közötti sáv a lakás legkihasználatlanabb tere. A ZENIT ezt a sávot a bútorod szerves, elegáns részévé teszi.") +
         P["ba"] + P["stats"] + "</div>") +
     P["explode"] +
     SEC(HEAD("Méretek", "Méretre szabva, <em>nem méretre vágva.</em>", "Minden ZENIT egyedi darab: a te szekrényed szélességéhez, a te plafonod magasságához tervezzük.") + '''<dl class="specs reveal">
  <div><dt>Szélesség</dt><dd>60 – 280 cm</dd></div><div><dt>Ajtók</dt><dd>1 – 6, arányos osztással</dd></div><div><dt>Magasság</dt><dd>a plafonodhoz, −10 mm</dd></div>
  <div><dt>Mélység</dt><dd>35 / 45 / 60 cm vagy egyedi</dd></div><div><dt>Pántok</dt><dd>Häfele, fékes, 110°</dd></div><div><dt>Rögzítés</dt><dd>a szekrényhez, falfúrás nélkül</dd></div>
</dl>''') +
     chapter("02", "anyagok.html", "Anyagok és színek", "Kurált paletta, egyedi színkód, valódi furnér és kézbe simuló vasalat.", ALT_CTA),
     scripts=["product.js"])

# ---------------------------------------------------------------- ANYAGOK
UNI = [("Kréta", "#F1EFEA"), ("Kasmír", "#CDBFAE"), ("Homok", "#D8CBB3"), ("Zsálya", "#A4AD98"),
       ("Agyag", "#A7735A"), ("Grafit", "#4A4846"), ("Éjkék", "#273445"), ("Fekete", "#1B1A19")]
pal = "".join(f'<div class="pal"><i style="background:{c}"></i><div><b>{n}</b><span>{c}</span></div></div>' for n, c in UNI)
tex = "".join(f'<div class="pal"><i class="{c}"></i><div><b>{n}</b><span>{t}</span></div></div>' for n, c, t in
              [("Natúr tölgy", "img-oak", "ZENIT Natúr"), ("Füstölt tölgy", "img-smoked", "ZENIT Natúr"), ("Dió", "img-walnut", "ZENIT Natúr"), ("Beton", "img-concrete", "Kő és len"), ("Len", "img-linen", "Kő és len")])
page("anyagok.html", "Anyagok és színek – ZENIT", "A ZENIT színpalettája, textúrái és vasalata.",
     page_hero("Kollekció · 02", "Amit érintesz, <em>annak súlya van.</em>",
               "Fa alapú lapanyag kurált színekben és textúrákban – vagy a ZENIT Natúr valódi tölgy- és diófurnérja.",
               None, "plain", cr=[("index.html", "ZENIT"), ("", "Kollekció"), ("", "Anyagok és színek")]) +
     SEC(P["matgrid"], style="padding-top:60px") +
     SEC(HEAD("Uni paletta", "Nyolc szín, <em>végtelen árnyalat.</em>", "Matt, selyemfényű vagy magasfényű felülettel – és ha a tiéd nincs köztük, add meg a pontos HEX kódját.") + f'<div class="palette reveal">{pal}</div>', style="padding-top:0") +
     SEC(HEAD("Textúrák", "Fa, kő, <em>len.</em>", "A ZENIT Natúr valódi furnért kap: minden ajtó erezete egyedi. A kő- és lenfelületek a merészebb belsőkhöz.") + f'<div class="palette reveal">{tex}</div>', style="padding-top:0") +
     SEC(HEAD("Fogantyúk", "A részlet, <em>amit minden nap megérintesz.</em>") + '''<div class="handles reveal">
  <div class="hcard"><div class="pic"><svg width="90" height="24"><path d="M2 5h86v7a7 7 0 0 1-7 7H9a7 7 0 0 1-7-7z" fill="none" stroke="#EDE6DA"/></svg></div><b>Élfogantyú</b><span>Lekerekített, az ajtó alsó élén, hátulról rögzítve. 192 vagy 320 mm.</span></div>
  <div class="hcard"><div class="pic"><svg width="90" height="24"><path d="M8 12h74" stroke="#EDE6DA" stroke-width="3" stroke-linecap="round"/></svg></div><b>Rúd</b><span>Vékony, hosszú vonal – a modern klasszikus.</span></div>
  <div class="hcard"><div class="pic"><svg width="90" height="24"><circle cx="45" cy="12" r="8" fill="none" stroke="#EDE6DA"/></svg></div><b>Gomb / bőrfül</b><span>Diszkrét, kézműves részlet.</span></div>
  <div class="hcard"><div class="pic"><svg width="90" height="24"><path d="M10 12h70" stroke="#857B70" stroke-dasharray="3 3"/></svg></div><b>Nyomásra nyíló</b><span>Fogantyú nélkül, tiszta front.</span></div>
</div><p class="lead reveal" style="margin-top:30px">Minden fogantyú elérhető eloxált alumínium, matt fekete, szálcsiszolt bronz vagy bőr kivitelben.</p>''', style="padding-top:0") +
     chapter("03", "manufaktura.html", "Manufaktúra", "Akik készítik: magyar műhelyhagyomány, kézzel ellenőrzött részletek, sorszámozott darabok.", ALT_CTA))

# ---------------------------------------------------------------- MANUFAKTÚRA
page("manufaktura.html", "Manufaktúra – ZENIT", "Magyar kézművesség, egyedi, sorszámozott ZENIT darabok.",
     page_hero("Kollekció · 03", "Nem gyártjuk. <em>Megépítjük.</em>",
               "Minden ZENIT egyetlen otthonra készül. Magyar asztalosműhelyek generációkon át csiszolt tudására építünk – a vágástól az utolsó pántbeállításig.",
               "assets/img/r/exploded.jpg", cr=[("index.html", "ZENIT"), ("", "Kollekció"), ("", "Manufaktúra")]) +
     SEC('''<div class="split reveal"><div><div class="kicker">Örökség</div><h2 class="h2" style="margin-top:18px">A magyar asztalos­hagyomány <em>csendes pontossága.</em></h2></div>
  <div class="prose"><p>A magyar bútorkészítés mindig is a pontosságról szólt: arról, hogy egy ajtó évtizedek múlva is ugyanazzal a halk mozdulattal záródjon. A ZENIT ebből a felhalmozott tudásból született – és a mai technológiával emeli új szintre.</p>
  <p>Hazai lapszabászatban, milliméterre vágva, gépi élzárással készül, és kézzel áll össze. Minden kötést, minden pántot, minden hézagot ember ellenőriz, nem szalag.</p></div></div>''') +
     SEC('''<div class="mat-grid reveal">
  <div class="tile big"><img class="fill" src="assets/ill/workshop.svg" alt="Műhely: gyalu, derékszög, tiplik – illusztráció"><div class="cap"><div class="h3">Kézzel összeállítva</div><p>Tipli és konfirmát kötés, ragasztó nélkül – évtizedekre.</p></div></div>
  <div class="tile"><img class="fill" src="assets/img/r/open_led.jpg" alt="Nyitott ajtók, beállított hézagok" style="object-position:60% 30%"><div class="cap"><div class="h3">Hézagra állítva</div><p>1,5 mm oldalt, 3 mm az ajtók között. Mindig.</p></div></div>
  <div class="tile"><img class="fill" src="assets/ill/seal.svg" alt="ZENIT sorszám-bélyeg – illusztráció"><div class="cap"><div class="h3">Sorszámozva</div><p>Minden ZENIT egyedi sorszámot és készítői aláírást kap.</p></div></div>
  <div class="tile"><img class="fill" src="assets/img/r/tex_walnut.jpg" alt="Diófurnér textúra"><div class="cap"><div class="h3">Válogatott furnér</div><p>A ZENIT Natúr ajtóinak erezetét egyenként párosítjuk.</p></div></div>
  <div class="tile"><img class="fill" src="assets/img/r/macro_edge.jpg" alt="Az ajtó lekerekített 2 mm-es éle"><div class="cap"><div class="h3">Az él, amit megfogsz</div><p>Kézzel ellenőrzött, sorjamentes élzárás.</p></div></div>
</div>''', style="padding-top:0") +
     SEC(HEAD("Az egyedi darab", "Egyetlen otthonra <em>tervezve.</em>", "Nincs raktárkészlet, nincs két egyforma ZENIT. A te méreteidből, a te színeidből és a te plafonodból születik – és csak a tiéd lesz.") + '''<dl class="specs reveal">
  <div><dt>Készítés</dt><dd>Megrendelésre, egyedi méretben</dd></div><div><dt>Ellenőrzés</dt><dd>Kézzel, darabonként</dd></div><div><dt>Jelölés</dt><dd>Sorszám és készítői aláírás</dd></div>
  <div><dt>Származás</dt><dd>Magyarországon tervezve és gyártva</dd></div><div><dt>Kötés</dt><dd>Ragasztó nélkül, szétszedhető</dd></div><div><dt>Élettartam</dt><dd>Örökgarancia <span class="demo">Demó</span></dd></div>
</dl>''', style="padding-top:0") +
     SEC('''<div class="note reveal"><div class="kicker">A műhelyből</div><div><blockquote>„Egy szekrényt nem akkor fejezünk be, amikor összeáll, hanem amikor az ajtó először csendben becsukódik. Azt a pillanatot mi is ott akarjuk hallani.”</blockquote><cite>ZENIT műhely · Budapest</cite></div></div>''', style="padding-top:0") +
     chapter("04", "inspiracio.html", "Inspiráció", "Nézd meg, hogyan él a ZENIT különböző otthonokban – és nyisd meg bármelyiket a tervezőben.", ALT_CTA))

# ---------------------------------------------------------------- INSPIRÁCIÓ
INS = [("Kasmír · az eredeti", "kasmir", "assets/img/r/hero_evening.jpg", ""), ("Natúr tölgy · japandi", "tolgy", "assets/img/r/insp_tolgy.jpg", ""),
       ("Grafit + dió · városi loft", "grafit", "assets/img/r/insp_grafit_dio.jpg", ""), ("Zsálya · nyugodt nappali fény", "zsalya", "assets/img/r/insp_zsalya.jpg", ""),
       ("Éjkék + bronz · esti hálószoba", "ejkek", "assets/img/r/insp_ejkek.jpg", ""), ("Krétafehér · skandináv reggel", "kreta", "assets/img/r/insp_kreta.jpg", "")]
ins = "".join(f'<a class="teaser" href="tervezo.html#preset={k}"><div class="bg {c}" style="{f"background-image:url({img})" if img else ""}"></div>'
              f'<div><div class="kicker">Látványterv</div><b>{t}</b><span class="go">Megnyitom a tervezőben →</span></div></a>' for t, k, img, c in INS)
page("inspiracio.html", "Inspiráció – ZENIT", "ZENIT különböző otthonokban és stílusokban.",
     page_hero("Kollekció · 04", "Egy forma, <em>ezer otthon.</em>", "Válassz egy hangulatot, és nyisd meg a tervezőben – a színek és arányok már be lesznek állítva.",
               None, "plain", cr=[("index.html", "ZENIT"), ("", "Kollekció"), ("", "Inspiráció")]) +
     SEC(f'<div class="insp reveal">{ins}</div>', style="padding-top:60px") +
     SEC('''<div class="note reveal"><div class="kicker">Tervezői jegyzet</div><div><blockquote>„A legjobb bútor az, amelyik úgy néz ki, mintha mindig is ott lett volna. A ZENIT-et úgy rajzoltuk meg, hogy a szekrényed <em>befejezése</em> legyen – ne egy újabb doboz rajta.”</blockquote><cite>A ZENIT tervezőcsapata</cite></div></div>''', style="padding-top:0") +
     chapter("05", "keszites.html", "Hogyan készül", "Tervtől a plafonig, négy lépésben – és minden kérdésre válasz.", ALT_CTA))

# ---------------------------------------------------------------- HOGYAN KÉSZÜL
page("keszites.html", "Hogyan készül – ZENIT", "A ZENIT gyártása, szállítása, szerelése és GYIK.",
     page_hero("Kollekció · 05", "Tervtől a plafonig, <em>négy lépésben.</em>", "Nincs dobozos kompromisszum: minden ZENIT a te méreteidre, a te színeidben készül, és mi szereljük fel.",
               "assets/img/r/exploded.jpg", "short", cr=[("index.html", "ZENIT"), ("", "Kollekció"), ("", "Hogyan készül")]) +
     SEC(P["howgrid"] + "</div>") +
     SEC('''<div class="split reveal"><div class="frame" style="aspect-ratio:4/3"><img src="assets/img/fusion_inside.png" alt="A ZENIT belső felépítése – 3D modell"><span class="render-tag">3D gyártási modell</span></div>
  <div><div class="kicker">A részletekben</div><h2 class="h2" style="margin-top:18px">Előfúrva, <em>előre gondolva.</em></h2>
  <div class="prose" style="margin-top:24px"><p>Minden furat helyét a 3D gyártási modell határozza meg: tipli és konfirmát kötés, pántcsésze, polctartó csap. A lapszabászat milliméterre vág és élt zár, mi pedig egy nap alatt összeállítjuk.</p>
  <p>A hátfal beütős szeggel kerül fel, a ZENIT négy csavarral rögzül a szekrényed tetejéhez. A falat nem fúrjuk.</p></div></div></div>''', style="padding-top:0") +
     SEC('<div class="faq"><div class="reveal"><div class="kicker">GYIK</div><h2 class="h2" style="margin-top:18px">Kérdések, <em>röviden.</em></h2></div><div class="reveal">' + P["faq"] + "</div></div>", style="padding-top:0") +
     chapter("06", "garancia.html", "Örökgarancia", "Nem évekre adunk garanciát. Ígéretet adunk.", ALT_CTA))

# ---------------------------------------------------------------- GARANCIA
page("garancia.html", "ZENIT Örökgarancia", "Egy életre tervezve – a ZENIT Örökgarancia.",
     page_hero("Kollekció · 06", "Egy életre <em>tervezve.</em>", "A ZENIT Örökgarancia nem határidő, hanem ígéret.", None, "plain",
               cr=[("index.html", "ZENIT"), ("", "Kollekció"), ("", "Örökgarancia")]) +
     '''<section class="sec guar"><div class="wrap reveal">
    <img src="assets/ill/seal.svg" alt="ZENIT pecsét" style="width:170px;margin:0 auto 34px;border-radius:50%">
    <div class="kicker">ZENIT Örökgarancia <span class="demo">Demó</span></div>
    <p>Nem évekre adunk garanciát, hanem a szekrényed egész életére. Amíg a lap, a szín és a vasalat kapható, a ZENIT minden darabja pótolható: ha megsérül, elkopik, vagy megváltozik az életed, elemenként pótoljuk, cseréljük vagy bővítjük.</p>
    <div class="closing">Amíg létezik, pótoljuk. A ZENIT nem avul el – veled marad.</div>
    ''' + P["trust"] + '''</div></section>''' +
     chapter("07", "tervezo.html", "Tervezd meg a sajátod", "Minden változtatás azonnal megjelenik – méret, ajtók, színek, fogantyú, polcok.",
             '<span>Vagy:</span><a href="concierge.html">Inkább egy tervező segítsen</a>'))

# ---------------------------------------------------------------- TERVEZŐ
cfg = P["cfgshell"].replace('<a class="btn fill full" href="#">Ajánlatot kérek', '<a class="btn fill full" href="terv.html" data-save>Ajánlatot kérek') \
    .replace('<a class="btn" href="#">Tervező hív vissza</a>', '<a class="btn" href="concierge.html" data-save>Tervező hív vissza</a>') \
    .replace('<a class="btn" href="#">Megrendelem', '<a class="btn" href="terv.html#rendeles" data-save>Megrendelem') \
    .replace('<a href="#">Terv mentése</a>', '<a href="terv.html" data-save>Terv mentése</a>')
page("tervezo.html", "Tervező – ZENIT", "Tervezd meg a saját ZENIT felső szekrényed élő 3D-ben.",
     '<section class="cfg" style="padding-top:78px"><div class="wrap" style="padding-top:34px;padding-bottom:26px">' +
     crumb(("index.html", "ZENIT"), ("", "Concierge"), ("", "Tervező")) +
     '<div class="sec-head" style="margin-bottom:0"><div><h1 class="h2">Tervezd meg <em>a sajátod.</em></h1></div><p class="lead">Minden változtatás azonnal megjelenik. Ha elkészültél, kérj ajánlatot, beszélj egy tervezővel – vagy rendeld meg.</p></div></div>' +
     cfg + '</section>',
     scripts=["vendor/three.min.js", "vendor/OrbitControls.js", "configurator.js"], solid=True)

# ---------------------------------------------------------------- AZ ÖN TERVE
page("terv.html", "Az Ön terve – ZENIT", "A mentett ZENIT terv összesítője, ajánlatkérés és rendelés.",
     page_hero("Concierge", "Az Ön <em>terve.</em>", "Nézze át, mentse el, kérjen rá ajánlatot – vagy rendelje meg.", None, "plain",
               cr=[("index.html", "ZENIT"), ("", "Concierge"), ("", "Az Ön terve")]) +
     SEC('''<div class="plan-sum">
  <div class="reveal"><div class="frame" style="aspect-ratio:16/10"><img src="assets/img/r/after_day.jpg" alt="A terv látványa"><span class="render-tag">Látványterv</span></div>
    <table id="planTable" style="margin-top:26px"><tbody>
      <tr><td>Szélesség × magasság × mélység</td><td>250 × 53 × 60 cm</td></tr><tr><td>Ajtók</td><td>5, egyenlő osztás</td></tr>
      <tr><td>Ajtó / korpusz / belső</td><td>Kréta / Kréta / Kréta, matt</td></tr><tr><td>Fogantyú</td><td>Élfogantyú, alu elox</td></tr>
      <tr><td>Polc</td><td>3. rekesz</td></tr><tr><td>Extrák</td><td>Belső LED</td></tr><tr><td>Pántok</td><td>Häfele, fékes</td></tr>
      <tr><td><b style="font:300 24px var(--serif);color:var(--ink)">Becsült ár</b></td><td><b style="font:300 30px var(--serif)" id="planPrice">254 900 Ft</b></td></tr>
    </tbody></table>
    <div class="links" style="display:flex;gap:26px;margin-top:20px;font:400 10px var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--muted)"><a href="tervezo.html">Módosítás</a><a href="#">Link másolása</a><a href="#">PDF összesítő</a></div>
  </div>
  <div class="choice reveal" id="rendeles">
    <div class="hi"><div class="kicker">Ajánlat</div><b>Ajánlatot kérek</b><p>Pontos ár szállítással és szereléssel, 24 órán belül e-mailben.</p>
      <form class="form"><div><label>Név</label><input></div><div><label>Telefon</label><input></div><div class="full"><label>E-mail</label><input type="email"></div>
      <div class="full"><label>Település</label><input></div><div class="full"><a class="btn fill" href="#">Ajánlatot kérek <span class="arrow"></span></a></div></form></div>
    <div><div class="kicker">Concierge</div><b>Egy tervező hív vissza</b><p>Belsőépítészünk átbeszéli a tervet, és segít a színekben, arányokban.</p><a class="btn" href="concierge.html">Időpontot választok</a></div>
    <div><div class="kicker">Rendelés <span class="demo">Demó</span></div><b>Megrendelem most</b><p>Biztonságos online fizetés. Ez a projektben bemutató lépés – valódi fizetés nem történik.</p><a class="btn ghost" href="#">Tovább a fizetéshez</a></div>
  </div>
</div>''', style="padding-top:60px"), scripts=["plan.js"])

# ---------------------------------------------------------------- CONCIERGE
page("concierge.html", "Concierge – személyes konzultáció – ZENIT", "Tervező vagy lakberendező hív vissza a ZENIT tervedről.",
     page_hero("Concierge", "Beszéljünk <em>a terved­ről.</em>", "Belsőépítészünk visszahív, átbeszéli a méreteket, színeket és arányokat – és ha kéri, személyesen is felmér.",
               "assets/img/r/open_led.jpg", "short", cr=[("index.html", "ZENIT"), ("", "Concierge"), ("", "Személyes konzultáció")]) +
     SEC('''<div class="split reveal" style="align-items:start">
  <div><div class="kicker">Hogyan működik</div><h2 class="h2" style="margin-top:18px">Húsz perc, <em>és minden a helyére kerül.</em></h2>
    <div class="prose" style="margin-top:24px"><p>Válasszon időpontot, és tervezőnk a megadott számon hívja. Ha már van mentett terve, azt is átnézzük – ha nincs, a beszélgetés végére lesz.</p>
    <p>Budapesten és környékén díjmentes helyszíni felmérést is kérhet.</p></div>
    <div class="specs" style="grid-template-columns:1fr 1fr;margin-top:40px"><div><dt>Telefon</dt><dd>+36 1 000 0000</dd></div><div><dt>E-mail</dt><dd>hello@zenit.example</dd></div><div><dt>Showroom</dt><dd>Budapest</dd></div><div><dt>Nyitva</dt><dd>H–P 9–18</dd></div></div></div>
  <form class="form" style="border:1px solid var(--line);padding:34px">
    <div class="full"><div class="kicker">Visszahívás kérése</div></div>
    <div><label>Név</label><input></div><div><label>Telefon</label><input></div><div class="full"><label>E-mail</label><input type="email"></div>
    <div class="full"><label>Kivel beszélne?</label><div class="slots"><button type="button" class="on">Tervező</button><button type="button">Lakberendező</button><button type="button">Mindegy</button></div></div>
    <div class="full"><label>Nap</label><div class="slots"><button type="button" class="on">Holnap</button><button type="button">Csütörtök</button><button type="button">Péntek</button><button type="button">Jövő hét</button></div></div>
    <div class="full"><label>Időpont</label><div class="slots"><button type="button">9:00</button><button type="button" class="on">11:00</button><button type="button">14:00</button><button type="button">16:30</button></div></div>
    <div class="full"><label>Megjegyzés</label><textarea rows="3" placeholder="Pl. belmagasság, szekrény típusa, stílus…"></textarea></div>
    <div class="full"><a class="btn fill" href="#">Kérem a visszahívást <span class="arrow"></span></a></div>
  </form></div>''') +
     chapter("", "tervezo.html", "Vagy tervezze meg most", "Az élő 3D tervezőben pár perc alatt összeállíthatja a sajátját."))

# ---------------------------------------------------------------- A PROJEKTRŐL
page("projekt.html", "A projektről – ZENIT AI kihívás", "A ZENIT AI kihívás projekt: videó, 3D modell, napló, forrásfájlok.",
     page_hero("A projektről", "Négy nap, egy ötlet, <em>egy mesterséges intelligencia.</em>",
               "A ZENIT egy AI kihívásra készült: a 3D modellt, a gyártási dokumentációt, a látványterveket, a videót és ezt az oldalt Claude-dal együtt terveztük – mindent dokumentálva.",
               None, "plain", cr=[("index.html", "ZENIT"), ("", "A projektről")]) +
     SEC('<div class="video reveal"><div class="play">▶</div><span class="render-tag">Projektvideó – hamarosan (YouTube)</span></div>', style="padding-top:60px") +
     SEC(HEAD("3D modell", "Forgasd meg <em>a gyártási modellt.</em>", "Autodesk Fusion-ben épült, 47 furat-feature, 108 furat, 101 vasalatelem – minden a helyén.") +
         '<div class="video reveal" style="aspect-ratio:16/8"><span class="kicker">Interaktív 3D nézegető – hamarosan</span></div>', style="padding-top:0") +
     SEC(HEAD("Letöltések és napló", "Minden, <em>ami mögötte van.</em>") + '''<div class="proj-grid reveal">
  <a href="#"><div class="kicker">Napló</div><b>Projektnapló</b><span>Eszközök, promptok, elakadások és megoldások.</span></a>
  <a href="#"><div class="kicker">GitHub</div><b>Forráskód</b><span>Weboldal, paraméteres geometria, generátorok.</span></a>
  <a href="#"><div class="kicker">3D</div><b>Fusion F3D / STEP</b><span>A teljes gyártási modell.</span></a>
  <a href="#"><div class="kicker">PDF</div><b>Gyártási dokumentáció</b><span>16 oldal: szabásjegyzék, rajzok, fúrósablon.</span></a>
  <a href="#"><div class="kicker">Excel</div><b>Szabásjegyzék és kalkuláció</b><span>Rendeléshez és árazáshoz.</span></a>
  <a href="#"><div class="kicker">Videó</div><b>YouTube</b><span>A projekt 2–3 percben.</span></a>
</div>''', style="padding-top:0"))
