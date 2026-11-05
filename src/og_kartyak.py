"""Megosztási előnézeti képek (Open Graph, 1200×630) és ikonok generálása oldalanként. Futtatás: python3 src/og_kartyak.py (Playwright + Chromium kell)."""
import os, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
R, F, V = "assets/img/r2/", "assets/m/foto/", "assets/m/video/"
# oldal → (háttérkép, felirat, cím)
CARDS = {
    "index":       (R + "hero_evening.jpg",        "Méretre épített felső szekrény", "Ahol a szekrényed véget ér, <em>ott kezdődünk.</em>"),
    "zenit":       (F + "foto_003_hero.jpg",       "Kollekció",            "A hiányzó fél méter, <em>megoldva.</em>"),
    "anyagok":     (F + "foto_093.jpg",            "Anyagok és színek",    "Kasmír, tölgy, <em>fény és tükör.</em>"),
    "manufaktura": (V + "gyalu.jpg",               "Manufaktúra",          "Kéz, gép, terv – <em>magyar műhely.</em>"),
    "inspiracio":  (V + "inspiracio_loop.jpg",     "Inspiráció",           "Egy forma, <em>ezer otthon.</em>"),
    "keszites":    (V + "uzem.jpg",                "Így készül",           "Tervtől <em>a plafonig.</em>"),
    "garancia":    (R + "b_kasmir_evening.jpg",    "Örökgarancia",         "Egy életre <em>tervezve.</em>"),
    "tervezo":     (R + "b_open_led.jpg",          "Élő 3D tervező",       "Tervezd meg <em>a saját arányaidra.</em>"),
    "terv":        (F + "foto_109_hero.jpg",       "Az Ön terve",          "Mentett tervek, <em>ajánlat.</em>"),
    "szereles":    (V + "szereles_loop.jpg",       "Szerelési útmutató",   "Lépésről lépésre, <em>ábrákkal.</em>"),
    "kezikonyv":   (R + "kezikonyv_hero.jpg",      "Kézikönyv",            "Személyre szabott, <em>nyomtatható.</em>"),
    "concierge":   (F + "foto_112.jpg",            "Személyes konzultáció", "Tervezőnk <em>visszahív.</em>"),
    "projekt":     (V + "projekt_loop.jpg",        "AI-kihívás · projekt", "3D modell, videó, weboldal – <em>néhány nap alatt.</em>"),
    "letoltes":    (V + "furas.jpg",               "Letöltések",           "3D modellek, <em>gyártási dokumentáció.</em>"),
    "naplo":       (F + "foto_117_hero.jpg",       "Projektnapló",         "Eszközök, promptok, <em>elakadások.</em>"),
    "uzleti-terv": (R + "v_grafit_dio.jpg",        "Üzleti terv 2027–2029", "Piac, működés, <em>három év számokban.</em>"),
    "aszf":        ("assets/img/own/aszf_hero.jpg", "Jogi tudnivalók",     "Általános szerződési <em>feltételek.</em>"),
    "suti":        ("assets/img/own/suti_hero.jpg", "Adatkezelés",         "Sütik, <em>méretre szabva.</em>"),
}
FONT = "".join(f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};src:url({ROOT.as_uri()}/assets/fonts/{f}-latin-ext-{w}-{st}.woff2)}}'
               f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};src:url({ROOT.as_uri()}/assets/fonts/{f}-latin-{w}-{st}.woff2);unicode-range:U+0000-00FF}}'
               for fam, f, w, st in [("Cormorant", "cormorant-garamond", 300, "normal"), ("Cormorant", "cormorant-garamond", 300, "italic"), ("Inter", "inter", 400, "normal"), ("Inter", "inter", 500, "normal")])
CSS = FONT + """*{margin:0;box-sizing:border-box}body{width:1200px;height:630px;background:#14110E;overflow:hidden;font-family:Inter}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}
.sh{position:absolute;inset:0;background:linear-gradient(90deg,rgba(20,17,14,.94) 0%,rgba(20,17,14,.82) 38%,rgba(20,17,14,.25) 72%,rgba(20,17,14,.05) 100%),linear-gradient(0deg,rgba(20,17,14,.55),rgba(20,17,14,0) 40%)}
.c{position:absolute;left:84px;top:78px;bottom:70px;width:640px;display:flex;flex-direction:column;color:#EDE6DA}
.logo{display:flex;flex-direction:column;align-items:flex-start;gap:12px}.rule{width:138px;height:9px;border:1.6px solid #C2A274;border-bottom:0}
.word{font-family:Cormorant;font-weight:300;font-size:46px;letter-spacing:.32em;line-height:1}
.lab{margin-top:auto;font-size:17px;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:#C2A274}
h1{margin-top:18px;font-family:Cormorant;font-weight:300;font-size:64px;line-height:1.04;letter-spacing:-.005em}h1 em{font-style:italic;color:#D9C29B}
.url{margin-top:34px;font-size:16px;letter-spacing:.08em;color:rgba(237,230,218,.62)}.url b{display:inline-block;width:34px;height:1px;background:#A27D4A;vertical-align:middle;margin-right:14px}"""
ICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#14110E"/><rect x="10" y="12" width="44" height="1.6" fill="#C2A274"/><rect x="10" y="9" width="1.6" height="7" fill="#C2A274"/><rect x="52.4" y="9" width="1.6" height="7" fill="#C2A274"/><text x="32" y="51" font-family="Georgia,serif" font-size="34" fill="#EDE6DA" text-anchor="middle">Z</text></svg>"""

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 630})
    for k, (img, lab, title) in CARDS.items():
        tmp = ROOT / "_og_tmp.html"; tmp.write_text(f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><div class="bg" style="background-image:url({ROOT.as_uri()}/{img})"></div><div class="sh"></div>'
                       f'<div class="c"><div class="logo"><span class="rule"></span><span class="word">ZENIT</span></div><div class="lab">{lab}</div><h1>{title}</h1>'
                       f'<div class="url"><b></b>mbolgar11.github.io/zenit</div></div>', encoding="utf8")
        pg.goto(tmp.as_uri()); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150)
        pg.screenshot(path=str(ROOT / f"assets/img/og/{k}.jpg"), type="jpeg", quality=86); print("og", k)
    (ROOT / "_og_tmp.html").unlink()
    (ROOT / "assets/img/favicon.svg").write_text(ICON, encoding="utf8")
    for s, name in [(180, "apple-touch-icon.png"), (32, "favicon-32.png"), (512, "icon-512.png")]:
        q = b.new_page(viewport={"width": s, "height": s}); q.set_content(f'<style>*{{margin:0}}svg{{width:{s}px;height:{s}px;display:block}}</style>{ICON}')
        q.screenshot(path=str(ROOT / f"assets/img/{name}")); q.close(); print("ikon", name)
    b.close()
