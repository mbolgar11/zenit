"""ZENIT oldalgenerátor v2 (Atelier) – közös fejléc/lábléc, oldalanként tartalom. Futtatás: python3 src/build.py"""
import json, os, html as H
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = "assets/img/r2/"        # saját renderek (kasmír fő modell)
F = "assets/m/foto/"        # szűrt stock fotók (hangulat)
V = "assets/m/video/"       # szűrt stock videók
STEPS = json.load(open(os.path.join(ROOT, "assets/ill/szereles/steps.json"), encoding="utf8"))

FONTS = "".join(
    f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};font-display:swap;src:url(assets/fonts/{f}-latin-ext-{w}-{st}.woff2) format("woff2");unicode-range:U+0100-024F,U+2010-2027}}'
    f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};font-display:swap;src:url(assets/fonts/{f}-latin-{w}-{st}.woff2) format("woff2")}}'
    for fam, f, w, st in [("Cormorant", "cormorant-garamond", 300, "normal"), ("Cormorant", "cormorant-garamond", 400, "normal"),
                          ("Cormorant", "cormorant-garamond", 300, "italic"), ("Inter", "inter", 300, "normal"),
                          ("Inter", "inter", 400, "normal"), ("Inter", "inter", 500, "normal")])

FAV = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%2314110E'/%3E"
       "%3Crect x='10' y='12' width='44' height='1.6' fill='%23C2A274'/%3E%3Crect x='10' y='9' width='1.6' height='7' fill='%23C2A274'/%3E%3Crect x='52.4' y='9' width='1.6' height='7' fill='%23C2A274'/%3E"
       "%3Ctext x='32' y='51' font-family='Georgia,serif' font-size='34' fill='%23EDE6DA' text-anchor='middle'%3EZ%3C/text%3E%3C/svg%3E")

# ---------------------------------------------------------------- ikonok (vonalas, 1px, bronz/tinta)
def sym(i, body, vb="0 0 48 48"):
    return f'<symbol id="{i}" viewBox="{vb}" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">{body}</symbol>'
ICONS = '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">' + "".join([
    sym("i-plafon", '<path d="M4 8h40"/><path d="M4 5v6M44 5v6"/><rect x="10" y="14" width="28" height="12"/><rect x="10" y="26" width="28" height="18"/><path d="M24 14v12"/>'),
    sym("i-nofuras", '<path d="M8 6v36"/><circle cx="26" cy="24" r="9"/><path d="M19.6 30.4l12.8-12.8"/>'),
    sym("i-pant", '<circle cx="16" cy="24" r="8"/><path d="M24 24h16M34 18v12"/><path d="M12 24h8" opacity=".5"/>'),
    sym("i-led", '<path d="M6 12h36"/><path d="M10 16l-3 6M18 16l-1 7M30 16l1 7M38 16l3 6M24 16v8"/><rect x="6" y="9" width="36" height="3"/>'),
    sym("i-tukor", '<rect x="12" y="6" width="24" height="36"/><path d="M17 14l8-5M17 22l14-9M22 30l9-6"/>'),
    sym("i-szint", '<path d="M4 10l40-4"/><path d="M8 18h32v24H8z"/><path d="M8 18l0-7M40 18v-12" stroke-dasharray="2 2"/><path d="M44 24v12M41 27l3-3 3 3M41 33l3 3 3-3"/>'),
    sym("i-csavarozo", '<path d="M8 18h20l4 4H8z"/><path d="M32 20h10"/><path d="M14 22l-2 16h8l2-16"/><path d="M28 16v4"/>'),
    sym("i-imbusz", '<path d="M14 8v26a6 6 0 0 0 6 6h16"/><path d="M10 8h8M36 36v8"/>'),
    sym("i-gumikalapacs", '<rect x="10" y="8" width="26" height="12" rx="5"/><path d="M23 20v22"/>'),
    sym("i-kalapacs", '<path d="M12 10h20l4 4-4 4H12z"/><path d="M22 18v24"/><path d="M12 10l-4 4 4 4"/>'),
    sym("i-meroszalag", '<rect x="6" y="12" width="24" height="24" rx="5"/><circle cx="18" cy="24" r="5"/><path d="M30 30h14v4H30"/><path d="M36 30v2M40 30v2"/>'),
    sym("i-letra", '<path d="M14 6l-6 38M34 6l6 38"/><path d="M12 16h24M11 26h26M9 36h30"/>'),
    sym("i-furo25", '<path d="M8 18h18l4 4H8z"/><path d="M30 20h4"/><path d="M34 20h10" stroke-dasharray="1.5 1.5"/><path d="M14 22l-2 16h8l2-16"/><text x="24" y="44" font-size="7" fill="currentColor" stroke="none" font-family="Inter">Ø2,5</text>'),
    sym("i-pz2", '<path d="M24 4v14"/><rect x="19" y="18" width="10" height="24" rx="3"/><path d="M21 4h6"/>'),
    sym("i-ket_fo", '<circle cx="16" cy="12" r="5"/><circle cx="32" cy="12" r="5"/><path d="M8 40v-10a8 8 0 0 1 16 0v10M24 40v-10a8 8 0 0 1 16 0v10"/>'),
    sym("i-vizmertek", '<rect x="4" y="18" width="40" height="12"/><rect x="19" y="21" width="10" height="6" rx="3"/><path d="M24 22v4"/>'),
    sym("i-kesztyu", '<path d="M16 42V22l-4-8M20 22V8M26 22V7M32 22V9M36 24V14l2 0M16 42h20V22"/>'),
    sym("i-laurel", '<path d="M14 40 A22 20 0 0 1 22 9"/><path d="M50 40 A22 20 0 0 0 42 9"/><ellipse cx="11.3" cy="32.2" rx="2.2" ry="5.2" transform="rotate(-110 11.3 32.2)"/><ellipse cx="10.1" cy="24.7" rx="2.2" ry="5.2" transform="rotate(-86 10.1 24.7)"/><ellipse cx="12.6" cy="17.5" rx="2.2" ry="5.2" transform="rotate(-62 12.6 17.5)"/><ellipse cx="18.5" cy="11.8" rx="2.2" ry="5.2" transform="rotate(-38 18.5 11.8)"/><ellipse cx="26.7" cy="8.5" rx="2.2" ry="5.2" transform="rotate(-14 26.7 8.5)"/><ellipse cx="35.8" cy="8.3" rx="2.2" ry="5.2" transform="rotate(10 35.8 8.3)"/><ellipse cx="52.7" cy="32.2" rx="2.2" ry="5.2" transform="rotate(-70 52.7 32.2)"/><ellipse cx="53.9" cy="24.7" rx="2.2" ry="5.2" transform="rotate(-94 53.9 24.7)"/><ellipse cx="51.4" cy="17.5" rx="2.2" ry="5.2" transform="rotate(-118 51.4 17.5)"/><ellipse cx="45.5" cy="11.8" rx="2.2" ry="5.2" transform="rotate(-142 45.5 11.8)"/><ellipse cx="37.3" cy="8.5" rx="2.2" ry="5.2" transform="rotate(-166 37.3 8.5)"/><ellipse cx="28.2" cy="8.3" rx="2.2" ry="5.2" transform="rotate(-190 28.2 8.3)"/><path d="M27 44h10"/>', "0 0 64 48"),
]) + '</svg>'
TOOLS = {"csavarozo": ("Akkus csavarozó", "PZ2 bittel"), "imbusz": ("Konfirmát kulcs", "4 mm imbusz, a csomagban"),
         "gumikalapacs": ("Gumikalapács", "tiplikhez"), "kalapacs": ("Kis kalapács", "hátfalszegekhez"), "meroszalag": ("Mérőszalag", "átlókhoz"),
         "letra": ("2 létra", "vagy stabil fellépő"), "furo25": ("Ø2,5 fúrószár", "a rögzítés előfuratához"), "pz2": ("PZ2 csavarhúzó", "pántállításhoz"),
         "ket_fo": ("Két ember", "az emeléshez"), "vizmertek": ("Vízmérték", "ellenőrzéshez")}
icon = lambda i, cls="ico": f'<svg class="{cls}"><use href="#i-{i}"/></svg>'

# ---------------------------------------------------------------- navigáció
KOLL = [("zenit.html", "A ZENIT", "A hiányzó fél méter, megoldva"), ("anyagok.html", "Anyagok és színek", "Kasmír, tölgy, fény és tükör"),
        ("manufaktura.html", "Manufaktúra", "Kéz, gép, terv – és díjak"), ("inspiracio.html", "Inspiráció", "Egy forma, ezer otthon"),
        ("keszites.html", "Így készül", "Tervtől a plafonig"), ("garancia.html", "Örökgarancia", "Egy életre tervezve")]
CONC = [("tervezo.html", "Tervező", "Élő 3D – a te arányaidra"), ("terv.html", "Az Ön terve", "Mentett tervek, ajánlat"),
        ("szereles.html", "Szerelés", "Lépésről lépésre, ábrákkal"), ("kezikonyv.html", "Kézikönyv", "Személyre szabott, nyomtatható"),
        ("concierge.html", "Személyes konzultáció", "Tervezőnk visszahív")]


def header(cur):
    def drop(items, feat):
        return '<div class="drop">' + feat + "".join(f'<a href="{h}"><b>{t}</b><span>{d}</span></a>' for h, t, d in items) + "</div>"
    kc = "cur" if cur in [h for h, *_ in KOLL] else ""
    cc = "cur" if cur in [h for h, *_ in CONC] else ""
    return f'''<header id="hdr"><div class="wrap nav">
  <a href="index.html" class="logo" aria-label="ZENIT – kezdőlap"><span class="rule"><i></i></span><span class="word">ZENIT</span></a>
  <ul class="main">
    <li class="{kc}"><a href="zenit.html">Kollekció</a>{drop(KOLL, f'<a class="feat" href="zenit.html" style="background-image:url({R}hero_evening.jpg)"><b>A ZENIT</b><span>Ahol a szekrényed véget ér</span></a>')}</li>
    <li class="{cc}"><a href="tervezo.html">Concierge</a>{drop(CONC, f'<a class="feat" href="tervezo.html" style="background-image:url({R}led_detail.jpg)"><b>Tervező</b><span>Élő 3D, a te méreteidre</span></a>')}</li>
  </ul>
  <div class="right">
    <span class="lang"><b>HU</b> / EN</span>
    <a href="terv.html" class="plan" title="Az Ön terve"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1"><path d="M2 3.5h12M2.5 3.5v9h11v-9M8 3.5v9"/></svg><i style="display:none">0</i></a>
    <a href="tervezo.html" class="btn">Tervezd meg</a>
    <button class="burger" data-menu aria-label="Menü"></button>
  </div></div></header>
<nav class="mnav" id="mnav"><button class="x" data-menu aria-label="Bezárás">×</button>
  <div><h6>Kollekció</h6>{"".join(f'<a href="{h}">{t}</a>' for h, t, _ in KOLL)}</div>
  <div><h6>Concierge</h6>{"".join(f'<a href="{h}">{t}</a>' for h, t, _ in CONC)}</div>
  <div><h6>A projekt</h6><a href="projekt.html">A projektről</a><a href="naplo.html">Napló</a></div></nav>'''


FOOTER = f'''<footer><div class="wrap">
  <div class="top">
    <div><a class="logo" href="index.html"><span class="rule"><i></i></span><span class="word">ZENIT</span></a>
      <p class="claim">Ahol a szekrényed véget ér, ott kezdődünk.</p>
      <form class="news" onsubmit="return false"><input placeholder="Hírlevél – e-mail címed" aria-label="E-mail"><button class="more" style="border:0">Feliratkozom</button></form></div>
    <div><h5>Kollekció</h5><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t, _ in KOLL)}</ul></div>
    <div><h5>Concierge</h5><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t, _ in CONC)}</ul></div>
    <div><h5>Atelier</h5><ul><li>ZENIT Atelier · Budapest</li><li>hello@zenit.example</li><li>H–P 10–18 · bejelentkezéssel</li><li><a href="projekt.html">A projektről</a></li><li><a href="naplo.html">Projektnapló</a></li></ul></div>
  </div>
  <div class="legal"><span>© 2026 ZENIT · Koncepció – AI-kihívás projekt, nem valós webáruház. A márka, a díjak és az események kitaláltak.</span><span>A termékképek saját látványtervek; a hangulatképek Unsplash/Pexels licenc alatt, szűrve.</span></div>
</div></footer>'''


def crumb(*items):
    return '<div class="crumb">' + '<i>/</i>'.join(f'<a href="{h}">{t}</a>' if h else f"<span>{t}</span>" for h, t in items) + '</div>'


def page(fname, title, desc, body, scripts=(), body_cls=""):
    html = f'''<!doctype html>
<html lang="hu">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="{R}hero_evening.jpg">
<link rel="icon" href="{FAV}">
<style>{FONTS}</style>
<link rel="stylesheet" href="assets/css/zenit.css">
</head>
<body class="{body_cls}">
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
    open(os.path.join(ROOT, fname), "w", encoding="utf8").write(html)
    print("ok", fname)


# ---------------------------------------------------------------- építőelemek
def S(inner, theme="", cls="", style="", attrs=""):
    t = f' data-theme="{theme}"' if theme else ""
    return f'<section class="sec {cls}"{t} style="{style}"{attrs}><div class="wrap">{inner}</div></section>'


def head(label, title, lead="", center=False, cls=""):
    return (f'<div class="sec-head{" center" if center else ""} {cls}"><div class="reveal"><div class="label">{label}</div><h2 class="h2">{title}</h2></div>'
            + (f'<p class="lead reveal d1">{lead}</p>' if lead else "<div></div>") + '</div>')


def img(src, alt, ar="ar-45", tag="", cls="", style=""):
    return f'<div class="frame {ar} {cls}" style="{style}"><img src="{src}" alt="{H.escape(alt)}" loading="lazy">' + (f'<span class="tag">{tag}</span>' if tag else "") + '</div>'


def vid(name, ar="ar-169", tag="", cls="", style=""):
    return (f'<div class="frame {ar} {cls}" style="{style}"><video data-bg muted loop playsinline preload="none" poster="{V}{name}.jpg" data-src="{V}{name}.mp4"></video>'
            + (f'<span class="tag">{tag}</span>' if tag else "") + '</div>')


def band(media, label, title, lead="", acts="", center=False, theme_dark=True, cls=""):
    if media.endswith(".mp4"):
        m = f'<video data-bg muted loop playsinline preload="none" poster="{media[:-4]}.jpg" data-src="{media}"></video>'
    else:
        m = f'<img src="{media}" alt="" loading="lazy">'
    return (f'<section class="band{" center" if center else ""}{" " + cls if cls else ""}"><div class="media">{m}</div><div class="wrap">'
            f'<div class="label reveal" style="color:var(--bronze2)">{label}</div><h2 class="h1 reveal d1">{title}</h2>'
            + (f'<p class="lead reveal d2">{lead}</p>' if lead else "") + (f'<div class="acts reveal d3">{acts}</div>' if acts else "") + '</div></section>')


def page_hero(label, title, lead, cr, media=None, theme="ivory", tag=""):
    if media:
        m = (f'<video data-bg muted loop playsinline autoplay preload="auto" poster="{media[:-4]}.jpg" src="{media}"></video>' if media.endswith(".mp4")
             else f'<img src="{media}" alt="">')
        return (f'<section class="page-hero img"><div class="media">{m}</div><div class="wrap">{crumb(*cr)}'
                f'<div class="label reveal" style="color:var(--bronze2)">{label}</div><h1 class="h1 lines"><span class="ln"><span>{title}</span></span></h1>'
                f'<p class="lead reveal d2">{lead}</p></div>' + (f'<span class="tag" style="left:auto;right:var(--pad);bottom:24px">{tag}</span>' if tag else "") + '</section>')
    t = f' data-theme="{theme}"' if theme != "ivory" else ""
    return (f'<section class="page-hero"{t}><div class="wrap">{crumb(*cr)}<div class="label reveal">{label}</div>'
            f'<h1 class="h1 lines"><span class="ln"><span>{title}</span></span></h1><p class="lead reveal d2">{lead}</p></div></section>')


def soft(media, label, quote):
    """elmosott, szűrt képsáv egy idézettel"""
    m = (f'<video data-bg muted loop playsinline preload="none" poster="{media[:-4]}.jpg" data-src="{media}"></video>' if media.endswith(".mp4") else f'<img src="{media}" alt="" loading="lazy">')
    return (f'<section class="band center soft"><div class="media">{m}</div><div class="wrap"><div class="label reveal" style="color:var(--bronze2)">{label}</div>'
            f'<p class="quote reveal d1">{quote}</p></div></section>')


def nxt(no, href, title, text, alt=True):
    alts = '<div class="alt"><span>Vagy:</span><a href="tervezo.html">Ugrás a tervezőbe</a><a href="concierge.html">Beszélek egy tervezővel</a></div>' if alt else ""
    return (f'<section class="next"><div class="wrap"><a href="{href}"><div><div class="label">Következő fejezet{" · " + no if no else ""}</div>'
            f'<div class="t">{title}</div><p>{text}</p></div><span class="circ"><span class="arrow"></span></span></a>{alts}</div></section>')


AW = [("Aurum Interior Award", "Bútor · Arany · Milánó 2026"), ("Pannon Mesterség Díj", "Az év bútora · 2025"),
      ("Atelier Europa Prize", "Craft &amp; Technology · 2026"), ("Lumen Design Prize", "Fény a bútorban · 2026"),
      ("Atelier Week Milano", "Kiállító · 2026")]
AWARDS = ('<div class="awards reveal">' + "".join(f'<div class="award">{icon("laurel", "")}<b>{a}</b><span>{b}</span></div>' for a, b in AW)
          + '</div><p class="fine">A díjak és kiállítások a látványprojekt részeként kitaláltak.</p>')

NUMS = [("530", "mm", "magasság – a te plafonodhoz méretezve"), ("10", "mm", "marad a plafonig, sehol nincs porfogó rés"),
        ("0.7", "m³", "zárt tárhely egy 250 cm-es szekrény fölött"), ("108", "", "előfúrt furat, a 3D modellből számolva"),
        ("6", "", "Häfele pánt – felül fékes, alul rugós"), ("0", "", "furat a falban – a szekrényedhez rögzül"),
        ("3", "óra", "szerelés két emberrel, ábrás útmutatóval"), ("16", "m", "élzárás – az ajtókon 2 mm-es ABS")]


def nums(items):
    return '<div class="nums reveal">' + "".join(f'<div class="num"><b><span data-count="{v}">0</span><small>{u}</small></b><span>{t}</span></div>' for v, u, t in items) + '</div>'


FAQ = [("Mennyi idő alatt készül el?", "A rendeléstől számítva 3–4 hét: tervellenőrzés, lapszabászat és élzárás, kézi összeállítás és próbaszerelés, majd kiszállítás."),
       ("Kell-e fúrni a falba?", "Nem. A ZENIT négy csavarral a meglévő szekrényed tetejéhez rögzül, belülről – bérlakásban is nyugodtan választhatod."),
       ("Mi van, ha nem egyenes a plafon vagy a fal?", "A tervezőben megadhatod a bal–jobb plafoneltérést és a falkiegyenlítést, mindkettőt 10 cm-ig. A különbséget egyedire szabott, láthatatlan takaróléc és távtartó veszi fel."),
       ("Bármelyik ajtó lehet tükrös?", "Igen. Ajtónként választhatod a tükröt – a középsőt, a szélsőket vagy akár mindet. A tükör 4 mm-es, biztonsági fóliával."),
       ("Én is össze tudom szerelni?", "Igen, két emberrel kb. három óra. Minden ZENIT mellé ábrás, lépésről lépésre útmutató, a te tervedre szabott kézikönyv és szerelési animáció jár. Kérésre mi szereljük."),
       ("Milyen pántokat használtok?", "Häfele Metalla 300SM, 110°-os pántokat: ajtónként egy fékes (felül) és egy rugós (alul). Háromdimenziósan állíthatók, szerszám nélkül pattinthatók.")]


def faq(items):
    return '<div class="faq"><div class="reveal"><div class="label">GYIK</div><h2 class="h2" style="margin-top:20px">Kérdések, <em>röviden.</em></h2></div><div class="reveal d1">' + "".join(
        f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + '</div></div>'


MARQ = ["Kasmír", "Natúr tölgy", "Häfele", "Plafonig", "Csendes zárás", "Belső fény", "Tükör", "Kézzel összeállítva", "Sorszámozva", "Magyar műhely"]
MARQUEE = '<div class="marquee" aria-hidden="true"><div class="track">' + "".join(f"<span>{w}</span>" for w in MARQ * 2) + '</div></div>'

# folytatás: oldalak
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages.py"), encoding="utf8").read())
