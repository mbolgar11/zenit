# ======================================================================== ÜZLETI TERV (2027–2029) – oldal + nyomtatható PDF
import json as _json
BM = _json.load(open(os.path.join(ROOT, "src", "uzleti_modell.json"), encoding="utf8"))
O = BM["out"]; BASE = O["Alap"]
fmt = lambda v: f"{v:,.0f}".replace(",", " ")
M = lambda v: f"{v / 1000:,.1f}".replace(",", " ").replace(".", ",")          # eFt → M Ft, magyar tizedesvessző
BRZ, ESP, STN, SND, MUT = "#A27D4A", "#2B241D", "#CDBFAE", "#E3D6C2", "#8C7B66"

# ---------------------------------------------------------------- grafikonok (SVG)
def svg_years():
    w, h, pad = 720, 300, 46; mx = max(O["Optimista"]["years"][y]["rev"] for y in ("2029",)) * 1.08
    cols = [("Óvatos", "#D8CBB8"), ("Alap", BRZ), ("Optimista", ESP)]; out = []
    for yi, y in enumerate(("2027", "2028", "2029")):
        gx = pad + 30 + yi * 220
        for ci, (n, c) in enumerate(cols):
            v = O[n]["years"][y]["rev"]; bh = (h - 80) * v / mx; x = gx + ci * 52
            out.append(f'<rect class="bar bv" style="transition-delay:{(yi * 3 + ci) * 0.08:.2f}s" x="{x}" y="{h - 40 - bh:.1f}" width="40" height="{bh:.1f}" fill="{c}"/>')
            out.append(f'<text x="{x + 20}" y="{h - 46 - bh:.1f}" text-anchor="middle" class="v">{M(v)}</text>')
        out.append(f'<text x="{gx + 72}" y="{h - 14}" text-anchor="middle" class="y">{y}</text>')
    lg = "".join(f'<rect x="{pad + 30 + i * 150}" y="8" width="12" height="12" fill="{c}"/><text x="{pad + 48 + i * 150}" y="19" class="l">{n}</text>' for i, (n, c) in enumerate(cols))
    return (f'<svg class="bp-chart reveal" viewBox="0 0 {w} {h}" role="img" aria-label="Árbevétel évente, három forgatókönyv (M Ft)">{lg}'
            f'<line x1="{pad}" y1="{h - 40}" x2="{w - 10}" y2="{h - 40}" stroke="currentColor" stroke-opacity=".25"/>{"".join(out)}</svg>')

def svg_cash():
    w, h, l, r, t, b = 720, 300, 64, 20, 30, 40
    allv = [x["cash"] for n in O for x in O[n]["rows"]]; lo, hi = min(allv) * 1.1, max(allv) * 1.1
    X = lambda i: l + i * (w - l - r) / 11; Y = lambda v: t + (hi - v) / (hi - lo) * (h - t - b)
    g = [f'<line x1="{l}" y1="{Y(0):.1f}" x2="{w - r}" y2="{Y(0):.1f}" stroke="currentColor" stroke-opacity=".35" stroke-dasharray="4 4"/>',
         f'<text x="{l - 8}" y="{Y(0) + 4:.1f}" text-anchor="end" class="l">0</text>']
    for v in (-100000, -50000, 50000, 100000):
        if lo < v < hi: g.append(f'<text x="{l - 8}" y="{Y(v) + 4:.1f}" text-anchor="end" class="l">{v // 1000:+d}</text><line x1="{l}" y1="{Y(v):.1f}" x2="{w - r}" y2="{Y(v):.1f}" stroke="currentColor" stroke-opacity=".08"/>')
    for i, q in enumerate(BM["Q"]):
        if i % 4 == 0: g.append(f'<text x="{X(i):.1f}" y="{h - 12}" class="l">{q[:4]}</text>')
    for n, c, wd in (("Óvatos", "#C9B9A2", 2), ("Optimista", ESP, 2), ("Alap", BRZ, 3.5)):
        pts = " ".join(f"{X(i):.1f},{Y(x['cash']):.1f}" for i, x in enumerate(O[n]["rows"]))
        g.append(f'<polyline class="ln" pathLength="1" points="{pts}" fill="none" stroke="{c}" stroke-width="{wd}" stroke-linejoin="round"/>')
        lx = O[n]["rows"][-1]["cash"]; g.append(f'<text x="{w - r - 4}" y="{Y(lx) - 8:.1f}" text-anchor="end" class="l" fill="{c}">{n}</text>')
    mi = BASE["rows"].index(min(BASE["rows"], key=lambda x: x["cash"]))
    g.append(f'<circle cx="{X(mi):.1f}" cy="{Y(BASE["min_cash"]):.1f}" r="6" fill="{BRZ}"/><text x="{X(mi):.1f}" y="{Y(BASE["min_cash"]) + 24:.1f}" text-anchor="middle" class="v">legnagyobb tőkeigény: {M(-BASE["min_cash"])} M Ft</text>')
    return f'<svg class="bp-chart reveal" viewBox="0 0 {w} {h}" role="img" aria-label="Halmozott pénzforgalom negyedévente (M Ft)">{"".join(g)}</svg>'

def svg_mix():
    w, h = 720, 250; chans = list(BM["UNITS"]); cols = [BRZ, "#C9A877", STN, ESP]; out = []
    mx = max(BASE["years"][y]["units"] for y in ("2029",))
    for yi, y in enumerate(("2027", "2028", "2029")):
        rows = [x for x in BASE["rows"] if x["q"].startswith(y)]; x0 = 110; yy = 30 + yi * 66
        out.append(f'<text x="0" y="{yy + 24}" class="y">{y}</text>')
        for ci, c in enumerate(chans):
            n = sum(r["u"][c] for r in rows); ww = 500 * n / mx
            if n: out.append(f'<rect class="bar bh" style="transition-delay:{(yi * 4 + ci) * 0.07:.2f}s" x="{x0:.1f}" y="{yy}" width="{ww:.1f}" height="34" fill="{cols[ci]}"/>' + (f'<text x="{x0 + ww / 2:.1f}" y="{yy + 22}" text-anchor="middle" class="in">{n}</text>' if ww > 34 else ""))
            x0 += ww
        out.append(f'<text x="{x0 + 10:.1f}" y="{yy + 23}" class="v">{BASE["years"][y]["units"]} db</text>')
    leg = '<div class="bp-leg">' + "".join(f'<span><i style="background:{cols[i]}"></i>{c}</span>' for i, c in enumerate(chans)) + '</div>'
    return f'<svg class="bp-chart reveal" viewBox="0 0 {w} 230" role="img" aria-label="Eladott darabszám csatornánként (alap forgatókönyv)">{"".join(out)}</svg>' + leg

def bars(items, unit="M Ft", color=BRZ):
    mx = max(v for _, v in items)
    return '<div class="bp-bars reveal">' + "".join(f'<div class="r"><span>{n}</span><b><i style="width:{100 * v / mx:.1f}%;background:{color}"></i></b><em>{M(v)} {unit}</em></div>' for n, v in items) + '</div>'

# ---------------------------------------------------------------- táblázatok
def pl_table(name):
    o = O[name]["years"]; rows = [("Eladott darab", "units", False), ("Nettó árbevétel", "rev", True), ("Közvetlen költség (gyártás, szerelés, szállítás)", "cogs", True),
                                  ("Fedezet", "gm", True), ("Működési költség", "opex", True), ("EBITDA", "ebitda", True), ("Halmozott pénzállás (év végén)", "cash_end", True)]
    body = "".join(f'<tr class="{"hl" if k in ("gm", "ebitda") else ""}"><td>{t}</td>' + "".join(f'<td>{M(o[y][k]) if m else fmt(o[y][k])}</td>' for y in ("2027", "2028", "2029")) + '</tr>' for t, k, m in rows)
    return f'<table class="bp-t"><thead><tr><td>{name} forgatókönyv · M Ft</td><td>2027</td><td>2028</td><td>2029</td></tr></thead><tbody>{body}</tbody></table>'

Y1 = {k: sum(v[:4]) for k, v in BM["OPEX"].items()}; Y1_CAPEX = sum(BM["CAPEX"][:4])
UNIT = [(c, BM["PRICE"][c], BM["COGS"][c]) for c in BM["UNITS"]]
unit_t = ('<table class="bp-t"><thead><tr><td>Csatorna</td><td>Nettó ár / db</td><td>Közvetlen költség / db</td><td>Fedezet</td></tr></thead><tbody>' +
          "".join(f'<tr><td>{c}</td><td>{fmt(p)} eFt</td><td>{fmt(k)} eFt</td><td>{round(100 * (p - k) / p)}%</td></tr>' for c, p, k in UNIT) + '</tbody></table>')

# ---------------------------------------------------------------- idővonal
TL = [("Alapítás", "Kft., védjegy, gyártópartner, ÁSZF, webshop", 0, 2), ("Budapesti pilot", "20 alapító ügyfél, tartalomgyártás, első vélemények", 1, 3),
      ("Construma · Budapest Design Week", "április: szakmai debütálás · október: design-közönség", 2, 7), ("Belsőépítész-program", "jutalékos partnerprogram, mintadobozok", 3, 12),
      ("Bécs · Pozsony · Prága", "lokalizált web, helyi szerelőpartnerek, pop-up", 5, 9), ("Fuorisalone · Milánó", "2028 április: pop-up a design héten", 5, 6),
      ("DACH és Észak-Olaszország", "bemutatótermi partnerek, nagykereskedelmi ár", 7, 12), ("Salone del Mobile", "2029 április: kiállítás vagy SaloneSatellite", 9, 10),
      ("Licenc és white label", "gyártói partnerség – a tervező szoftverrel együtt", 10, 12)]
tl_html = ('<div class="bp-tl reveal"><div class="hd"><span></span>' + "".join(f'<b>{y}</b>' for y in ("2027", "2028", "2029")) + '</div>' +
           "".join(f'<div class="row"><span><b>{t}</b><small>{d}</small></span><div class="tr"><i style="left:{a / 12 * 100:.2f}%;width:{max(1, b - a) / 12 * 100:.2f}%;transition-delay:{0.15 + a * 0.06:.2f}s"></i></div></div>' for t, d, a, b in TL) + '</div>')

# ---------------------------------------------------------------- szöveges blokkok
def cards(items, cls="bp-cards", imgs=None):
    im = lambda i: (f'<div class="ci"><img src="{imgs[i]}" alt="" loading="lazy"></div>' if imgs else "")
    return f'<div class="{cls}">' + "".join(f'<div class="c reveal d{i % 3}">{im(i)}<div class="k">{k}</div><h4>{t}</h4><p>{d}</p></div>' for i, (k, t, d) in enumerate(items)) + '</div>'

KEY = [("Indulás", "2027. március", "pilot Budapesten, 20 alapító ügyféllel"), ("Tőkeigény (alap)", f"{M(-BASE['min_cash'] * 1.08)} M Ft", "a legmélyebb pont + 8% tartalék, 2029 Q2"),
       ("Pozitív EBITDA", "2028 Q4", "a 22. hónaptól; óvatosan 2029 Q3"), ("Eladás 3 év alatt", f"{fmt(sum(BASE['years'][y]['units'] for y in ('2027', '2028', '2029')))} db", "alap forgatókönyv, 4 csatorna"),
       ("Árbevétel 2029", f"{M(BASE['years']['2029']['rev'])} M Ft", f"≈ {round(BASE['years']['2029']['rev'] * 1000 / BM['EUR'] / 1e6, 2)} M €, 7 országban"), ("Fedezet", "≈ 50%", "közvetlen költségek után, csatornától függően")]

MODELS = [("01 · D2C", "Közvetlen online eladás", "Tervező → mentett terv → videós konzultáció → felmérés → 50% előleg. A legmagasabb árrés, a márka itt épül."),
          ("02 · B2B2C", "Belsőépítészek és stúdiók", "10% jutalék, mintadoboz, saját tervezői hozzáférés. Bizalmi ajánlás, nagyobb kosárérték."),
          ("03 · B2B", "Ingatlanfejlesztők", "„Plafonig” felárcsomag prémium új lakásokhoz – sorozatgyártási ár, egy szerződés sok lakásra."),
          ("04 · Retail", "Bemutatótermi partnerek", "Shop-in-shop sarok gardróbstúdiókban: mintadarab, QR-kód a tervezőhöz, nagykereskedelmi ár (−35%)."),
          ("05 · Licenc", "White label és licenc", "Szekrénygyártóknak: a ZENIT-rendszer (tervező + gyártási modell) licencdíjért vagy darabdíjért."),
          ("06 · Szolgáltatás", "Örökgarancia és bővítés", "Pót- és bővítőelemek, költözési átszerelés, LED-utólag – visszatérő bevétel a meglévő vevőktől.")]

SALES = [("Az első 10", "Ismeretségi kör és alapító ügyfelek", "Kedvezményes ár cserébe előtte–utána fotókért, videóért és véleményért. Mindegyik ügyfél egy referencia-otthon."),
         ("Az első 100", "Tartalom + hirdetés + belsőépítészek", "Előtte–utána reels, „milyen magas a szekrényed?” kampány, 15 belsőépítész partner, Construma és Budapest Design Week."),
         ("Az első 1000", "Partnerek és nemzetközi jelenlét", "Bemutatótermi partnerek Bécsben, Pozsonyban, Prágában és Münchenben, fejlesztői keretszerződések, Fuorisalone és Salone del Mobile.")]

FUNNEL = [("Hirdetés / tartalom elérés", "100 000"), ("Látogató a tervezőben", "2 500 (2,5%)"), ("Mentett terv", "500 (20%)"), ("Konzultáció / felmérés", "125 (25%)"),
          ("Rendelés", "45 (36%)")]

ONLINE = [("SEO és tartalom", "„szekrény fölötti tér”, „gardrób magasítás”, „plafonig érő szekrény” kulcsszavak; útmutatók, mérési segédlet, előtte–utána galéria."),
          ("Meta és Pinterest", "Előtte–utána reels, carousel a tervezőből, retargeting a mentett tervekre; Pinterest-táblák lakberendezőknek."),
          ("Google Search", "Magas szándékú keresések (egyedi gardrób, szekrény plafonig, beépített szekrény ár) – a tervezőre irányítva."),
          ("YouTube és TikTok", "Szerelési videó, „3 óra alatt plafonig” time-lapse, belsőépítész-interjúk, a műhely kulisszái."),
          ("Influencerek", "8–12 lakberendezési mikroinfluenszer (10–80 ezer követő) – valódi beépítéssel, nem fizetett képpel."),
          ("CRM és hírlevél", "Mentett terv → emlékeztető, mintadoboz-ajánlat, ünnepi kampány; ajánlói program: 25 000 Ft kupon mindkét félnek.")]
OFFLINE = [("Kiállítások", "Construma (Hungexpo, 2027. ápr. 8–11.), Budapest Design Week (október), Vienna Design Week, Designblok Prága."),
           ("Milánó", "2027: látogatás és kapcsolatépítés · 2028: Fuorisalone pop-up · 2029: Salone del Mobile vagy SaloneSatellite (35 év alatti tervezőknek)."),
           ("Bemutatóterem", "Budapesti „atelier” időponttal – mintafal 3 színnel, élő tervezővel; később shop-in-shop partnereknél."),
           ("Sajtó és díjak", "Lakáskultúra, Elle Decoration, Otthon; nemzetközileg Dezeen, Designboom. Valódi nevezés: Magyar Formatervezési Díj, German Design Award, Red Dot."),
           ("Partnerprogram", "Belsőépítészeknek mintadoboz, tervezői belépés, 10% jutalék és közös referenciafotózás."),
           ("Fejlesztők", "Mintalakás-beépítés prémium projektekben, „Plafonig” felárcsomag a vevői menüben.")]

BRAND = [("Kategória", "Nem szekrényt adunk el, hanem egy új kategóriát: a felső szekrényt, ami befejezi a meglévőt. A név a jelenség neve legyen: „ZENIT-elni” a szekrényt."),
         ("Ígéret", "Ahol a szekrényed véget ér, ott kezdődünk. Méretre, 10 mm-re a plafontól, falfúrás nélkül, három óra alatt."),
         ("Jelek", "Bronz vonal, 10 mm-es rés, sorszámozott tetőlap, aláírt tanúsítvány, Örökgarancia – minden érintési ponton ugyanaz."),
         ("Hang", "Nyugodt, pontos, meleg. Nem kiabál akciót – megmutatja az előtte–utánát, és hagyja, hogy a csend beszéljen.")]

OPS = [("Cégforma", "Kft., 3 M Ft törzstőke; alapítás ügyvéddel, egyszerűsített eljárásban."),
       ("Védjegy", "Előzetes névkutatás (ZENIT/Zenith ütközés!), majd HU és EUIPO bejelentés – EU-ban 1 osztály 850 €, 2 osztály 900 €."),
       ("Gyártás", "Partner asztalosüzem CNC-vel és élzáróval; a 3D modellből gépi fájl; Häfele vasalat keretszerződéssel; minőségellenőrzés nálunk."),
       ("Szerelés", "Saját kétfős csapat Budapesten, alvállalkozó szerelők vidéken és külföldön, egységes szerelési protokoll és kézikönyv."),
       ("Jog és pénzügy", "ÁSZF (egyedi gyártás – elállási kivétel), 3 év kötelező jótállás 250 e Ft felett, termékfelelősség-biztosítás, online könyvelés."),
       ("Rendszerek", "Saját tervező + webshop, Barion/Stripe fizetés, HubSpot vagy Pipedrive CRM, felmérő app, gyártási ütemező tábla.")]

TEAM = [("2027", "2 alapító (értékesítés és termék) + 1 szerelő (H2-től), külsős marketing és könyvelés."),
        ("2028", "+ ügyfélkapcsolati vezető, + szerelő, + DACH/CEE partnermenedzser (részmunkaidő)."),
        ("2029", "+ marketingvezető, + 2 szerelő, + gyártáskoordinátor; országonkénti partnerhálózat.")]

RISKS = [("Rejtett igény", "Kevesen keresnek rá a „szekrény fölötti térre”.", "Problémát mutató tartalom (előtte–utána), és a tervező mint játékos belépő."),
         ("Ár-érzékenység itthon", "Helyi asztalos olcsóbb.", "Sebesség, garantált illeszkedés, design, Örökgarancia; részletfizetés."),
         ("Gyártói kapacitás", "Partnernél csúszás.", "Két gyártópartner, sorozatba rendezett gyártási napok, 2029-től saját CNC-cella."),
         ("Utánzás", "Nagy szereplők lemásolják.", "Márka, közösség, partnerhálózat, a tervező és a szerelési protokoll mint előny; formatervezési minta oltalom."),
         ("Export-logisztika", "Szállítás és szerelés drága.", "Lapra szerelt csomag, helyi szerelőpartnerek, régiónkénti gyűjtőszállítás."),
         ("Finanszírozás", "Lassabb növekedés.", "Óvatos forgatókönyv karcsú költségekkel; mérföldkőhöz kötött befektetési részletek.")]

MARKET = [("330 Mrd Ft", "a hazai háztartások bútor- és világításköltése 2020-ban (GVH / Pénzcentrum)"),
          ("~98 Mrd Ft", "az IKEA magyarországi árbevétele egy évben (2019/20)"),
          ("3,2 Mrd $", "az európai beépített gardróbpiac becsült mérete (DataHorizzon)"),
          ("300 000+", "vevő 28 országban a lengyel Tylko méretre szabott bútoraira – az online konfigurátoros modell működik")]

SOURCES = [("Salone del Mobile 2027 időpont", "https://www.salonemilano.it/en/articles/salone-del-mobile-2027-dates"),
           ("CONSTRUMA 2027 kiállítói anyag (időpont, m²-ár)", "https://hungexpo.hu/wp-content/uploads/CONSTRUMA2027_kiallitoi_prezi_EN.pdf"),
           ("Budapest Design Week 2025 (Time Out)", "https://www.timeout.com/hu/budapest/hirek/hamarosan-kezdodik-a-budapest-design-week-2025-100725"),
           ("EU védjegy díjak 2026", "https://tmarkmetric.com/insights/eu-trademark-cost"),
           ("Fitted wardrobe market (DataHorizzon)", "https://datahorizzonresearch.com/fitted-wardrobe-market-38623"),
           ("Bútorpiac, IKEA és XXXLutz számok (Pénzcentrum)", "https://www.penzcentrum.hu/vallalkozas/20210606/folytatodik-a-magyar-butorhaboru-lenyomhatja-az-ikea-t-a-tronkovetelo-xxxlutz-1115167/amp"),
           ("Tylko – vélemények, 28 ország", "https://tylko.com/en-dk/review-list"),
           ("deinSchrank.de felvásárlása (2023)", "https://www.unternehmeredition.de/rheinische-moebelwerke-kauft-deinschrank-de/"),
           ("Kft. alapítás költségei", "https://financera.hu/befektetes/cegalapitas-menete/"),
           ("Facebook hirdetési benchmarkok 2026", "https://influee.co/hu/blog/facebook-ads-benchmarks")]


# ---------------------------------------------------------------- mozgó elemek: számláló, Európa-térkép, telefonos tartalom-makettek
import re as _re
def numwrap(v):
    if not _re.search(r"(M Ft|db|Mrd|\$|\+|%)", v): return v
    m = _re.search(r"(\d+(?:[  ]\d{3})*(?:,\d+)?)", v)
    if not m: return v
    raw = m.group(1).replace(" ", "").replace(" ", ""); num = raw.replace(",", ".")
    return v[:m.start()] + f'<span data-count="{num}">{m.group(1)}</span>' + v[m.end():]

CITIES = [("Budapest", 19.04, 47.50, 0), ("Győr", 17.64, 47.69, 0), ("Debrecen", 21.63, 47.53, 0), ("Bécs", 16.37, 48.21, 1), ("Pozsony", 17.11, 48.15, 1),
          ("Prága", 14.42, 50.08, 1), ("München", 11.58, 48.14, 2), ("Zürich", 8.54, 47.37, 2), ("Milánó", 9.19, 45.46, 2), ("Varsó", 21.01, 52.23, 3), ("Amszterdam", 4.90, 52.37, 3)]
PH = [("2027 · Magyarország", BRZ), ("2028 · szomszédok", "#C9A877"), ("2029 · DACH és Észak-Olaszország", ESP), ("Licencpartnerek", "#8C7B66")]
LBL = {"Bécs": (-10, -10), "Pozsony": (6, -14), "Győr": (-8, 20), "Budapest": (12, 18), "Debrecen": (10, -10), "München": (-10, -10), "Zürich": (-10, -10), "Milánó": (10, 18)}
def svg_map():
    W_, H_ = 760, 440; X = lambda lo: 30 + (lo - 4.0) * 36.5; Y = lambda la: 30 + (53.2 - la) * 48
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="1.6"/>' for x in range(12, W_, 22) for y in range(12, H_, 22))
    bx, by = X(19.04), Y(47.50); arcs, pins = [], []
    for i, (n, lo, la, ph) in enumerate(CITIES):
        x, y = X(lo), Y(la); c = PH[ph][1]
        if n != "Budapest":
            mx_, my_ = (bx + x) / 2, min(by, y) - 40 - abs(bx - x) * 0.12
            arcs.append(f'<path class="arc" pathLength="1" style="transition-delay:{0.3 + ph * 0.5 + i * 0.05:.2f}s" d="M{bx:.0f},{by:.0f} Q{mx_:.0f},{my_:.0f} {x:.0f},{y:.0f}" stroke="{c}"/>')
        pins.append(f'<g class="pin" style="transition-delay:{0.2 + ph * 0.5 + i * 0.05:.2f}s"><circle class="pulse" cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{c}" style="animation-delay:{i * 0.37:.2f}s"/>'
                    f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{7 if n == "Budapest" else 5}" fill="{c}"/><text x="{x + LBL.get(n, (10, -9))[0]:.0f}" y="{y + LBL.get(n, (10, -9))[1]:.0f}" text-anchor="{"end" if LBL.get(n, (10, 0))[0] < 0 else "start"}">{n}</text></g>')
    leg = "".join(f'<span><i style="background:{c}"></i>{t}</span>' for t, c in PH)
    return (f'<div class="bp-map reveal"><svg viewBox="0 0 {W_} {H_}" role="img" aria-label="Terjeszkedési térkép: Budapesttől Európáig"><g class="grid">{dots}</g>{"".join(arcs)}{"".join(pins)}</svg>'
            f'<div class="bp-leg">{leg}</div></div>')

def phones():
    ph = lambda inner, cap, d: f'<figure class="phone reveal d{d}"><div class="scr">{inner}<span class="ui"><b>zenit.atelier</b><i>♥ 2,4 E · ↻ 318</i></span></div><figcaption>{cap}</figcaption></figure>'
    ba = f'<div class="ba-fade"><img src="assets/img/own/before_real.jpg" alt=""><img class="b" src="assets/img/own/after_real.jpg" alt=""></div><span class="lbl">előtte · utána</span>'
    v = lambda n: f'<video data-bg muted loop playsinline preload="none" poster="{V}{n}.jpg" data-src="{V}{n}.mp4"></video>'
    return ('<div class="bp-phones">' + ph(ba, "Reels · előtte–utána – a tartalom motorja", 0) + ph(v("nyitas"), "Story · „kinyitod, és fény gyúl”", 1) +
            ph(v("el_erintes"), "Pinterest / TikTok · anyag és érintés", 2) + '</div>')

BP_HERO = page_hero("Üzleti terv · 2027–2029", "A műhelytől <em>Európáig.</em>",
                    "Hogyan lesz a ZENIT-ből márka: cégalapítás, értékesítés, marketing, kiállítások, terjeszkedés és egy három évre szóló, három forgatókönyves pénzügyi terv.",
                    [("index.html", "ZENIT"), ("projekt.html", "A projektről"), ("", "Üzleti terv")], R + "v_grafit_dio.jpg", tag="Látványterv · grafit és dió")

BP = (BP_HERO +
  S('<div class="bp-note noprint-hide"><b>Koncepció.</b> Ez a terv az AI-kihívás része: a piaci adatok forrásoltak, a darabszámok, árak és költségek tervezői becslések (guesswork), egy induló prémium bútormárka szokásos arányaival. '
    '<a class="btn fill" href="letoltes/ZENIT_uzleti_terv.pdf" style="margin-left:auto">PDF letöltése <span class="arrow"></span></a></div>' +
    head("Összefoglaló", "Egy új kategória, <em>prémium áron, nyugodt tempóban.</em>",
         "A ZENIT a meglévő gardrób fölötti fél métert alakítja egyetlen, méretre gyártott felső szekrénnyé. Budapesten indulunk, 2028-ban Bécs, Pozsony és Prága, 2029-ben a német nyelvterület és Észak-Olaszország következik. Az alap forgatókönyvben a működés 2028 végére nyereséges, a legmagasabb finanszírozási igény kb. 60 M Ft.") +
    '<div class="bp-key">' + "".join(f'<div class="reveal"><span>{k}</span><b>{numwrap(v)}</b><small>{d}</small></div>' for k, v, d in KEY) + '</div>', "paper") +
  band(V + "inspiracio_loop.mp4", "A kiindulópont", "A termék kész. <em>Most jön a márka.</em>", "Működő 3D tervező, méretpontos gyártási modell, kézikönyv, videók – a ZENIT nem ötlettel, hanem kész termékkel indul.", center=True) +
  S(head("01 · Piac és realitás", "Van piaca? <em>Igen – ha megmutatjuk.</em>",
         "A szekrény fölötti üres sáv szinte minden otthonban ott van, de ritkán keresnek rá: ez rejtett igény. A feladat ezért nem a kereslet kiszolgálása, hanem a probléma láthatóvá tétele.") +
    '<div class="bp-market">' + "".join(f'<div class="reveal"><b>{numwrap(v)}</b><span>{d}</span></div>' for v, d in MARKET) + '</div>' +
    '<div class="bp-two"><div><h4>Kinek szól?</h4><ul><li>30–55 éves, jól kereső városi párok és családok</li><li>új lakásba költözők és felújítók</li><li>meglévő gardróbbal: IKEA PAX, Bútorline, XXXLutz, asztalosmunka</li><li>belsőépítészek, akiknek „befejezett” megoldás kell</li></ul></div>'
    '<div><h4>Becslés a piac méretére</h4><ul><li>Magyarországon kb. 4,5 millió lakás; nagyjából minden harmadikban van beépített vagy álló gardrób</li><li>prémium szegmens (vásárlóerő + igény): kb. 3–4%, azaz 45–60 ezer háztartás</li><li>a 3 éves terv ebből kb. 0,8 ezer magyar vevővel számol – a prémium szegmens 1,5–2%-a</li><li>Európában a beépített gardróbpiac kb. 3,2 Mrd $, évi 5% körüli növekedéssel</li></ul></div></div>'
    '<p class="bp-verdict"><b>Ítélet:</b> a piac létezik, de kicsi és rejtett – ezért a ZENIT prémium rés-márkaként működik: magas árrés, kevés, de büszke vevő, erős tartalom. A tanulság a német deinSchrank.de-től (2010, kb. 80 fő, 2023-ban fizetésképtelenség, majd felvásárlás): a méretre gyártás online is eladható, de a túl korai saját gyár és a tőkeigényes növekedés veszélyes. Ezért gyártunk partnerrel, és csak 2029-ben lépünk saját CNC-cella felé.</p>', "stone") +
  S(head("02 · Márka", "A szekrény, amit <em>befejeztek.</em>", "A ZENIT nem újabb szekrény, hanem egy hiányzó gesztus: a meglévő bútor befejezése a plafonig. Erről kell, hogy beszéljenek.") +
    cards([(f"0{i + 1}", t, d) for i, (t, d) in enumerate(BRAND)], "bp-cards c2"), "paper") +
  soft(R + "b_kasmir_evening.jpg", "Márkaígéret", "Ahol a szekrényed véget ér, <em>ott kezdődünk.</em>") +
  S(head("03 · Üzleti modellek", "Hat út <em>ugyanahhoz a vevőhöz.</em>", "Az első év a közvetlen eladásé és a belsőépítészeké, a második a partnereké, a harmadik a licencé és a visszatérő bevételé.") + cards(MODELS, imgs=[R + "b_open_led.jpg", F + "foto_109.jpg", R + "hero_day.jpg", F + "foto_002.jpg", R + "exploded_light.jpg", R + "hinge_in_detail.jpg"]), "ivory") +
  S(head("04 · Ütemterv", "Harminchat hónap, <em>kilenc mérföldkő.</em>", "Negyedéves tervezés, havonta mérve. A kiállítási időpontok a szervezők közzétett dátumai.") + tl_html, "paper") +
  S(head("05 · Értékesítés", "Az első tíz, száz <em>és ezer vevő.</em>", "Más módszer kell mindhárom lépcsőhöz – és a tervező mindháromban a belépő.") +
    cards([(k, t, d) for k, t, d in SALES]) +
    '<div class="bp-funnel"><h4>Egy átlagos negyedév tölcsére (alap forgatókönyv, 2028)</h4>' +
    "".join(f'<div style="width:{100 - i * 14}%"><span>{t}</span><b>{v}</b></div>' for i, (t, v) in enumerate(FUNNEL)) + '</div>', "stone") +
  S(head("06 · Marketing és PR", "Online és fizikai térben – <em>ugyanazzal a csenddel.</em>", "A tartalom motorja az előtte–utána: minden beépítésből fotó, rövid videó és vélemény lesz.") +
    phones() + '<div class="bp-two"><div><h4>Online</h4>' + "".join(f'<p><b>{t}.</b> {d}</p>' for t, d in ONLINE) + '</div><div><h4>Fizikai jelenlét</h4>' + "".join(f'<p><b>{t}.</b> {d}</p>' for t, d in OFFLINE) + '</div></div>', "paper") +
  S(head("07 · Terjeszkedés", "Három kör <em>Európában.</em>", "Budapestről indulva, partnerekkel – a térképen a belépés sorrendje.") + svg_map() +
    cards([("2027", "Magyarország", "Budapest és agglomeráció, majd Győr, Debrecen, Szeged, Pécs – szerelőpartnerekkel."),
           ("2028", "Szomszédok", "Ausztria, Szlovákia, Csehország: lokalizált web és tervező, helyi szerelők, pop-up a design heteken."),
           ("2029", "DACH és Észak-Olaszország", "Bemutatótermi partnerek Münchenben, Zürichben és Milánóban; licencpartner keresése Lengyelországban és a Benelux-államokban.")]), "ivory") +
  band(V + "szereles_loop.mp4", "Skálázható folyamat", "Egy modell. <em>Bármelyik szekrényre.</em>", "A paraméteres 3D modell minden méretre legenerálja a szabásjegyzéket, a furattáblát és a szerelési animációt – ettől skálázható a gyártás partnerekkel is.") +
  S(head("08 · Működés és csapat", "Kicsi csapat, <em>erős partnerek.</em>") + cards([(f"0{i + 1}", t, d) for i, (t, d) in enumerate(OPS)]) +
    '<div class="bp-two" style="margin-top:40px"><div><h4>Csapat évente</h4>' + "".join(f'<p><b>{y}.</b> {d}</p>' for y, d in TEAM) + '</div>'
    '<div><h4>Az első 90 nap</h4><ol class="bp-ol"><li>Névkutatás és védjegybejelentés</li><li>Kft. alapítása, bankszámla, könyvelő</li><li>Két gyártópartner ajánlata, próbagyártás</li><li>ÁSZF, jótállási jegy, biztosítás</li><li>Webshop és fizetés élesítése</li><li>20 alapító ügyfél kiválasztása</li><li>Construma-stand foglalása (korai ár)</li></ol></div></div>', "paper") +
  S(head("09 · Pénzügyi terv", "Három év, <em>három forgatókönyv.</em>",
         f"Nettó, ezer forintos negyedéves modell; árfolyam {BM['EUR']} Ft/€. Az óvatos forgatókönyv 60%-os darabszámmal és karcsúbb költségekkel, az optimista 140%-kal számol.") +
    '<div class="bp-two"><div><h4>Árbevétel évente · M Ft</h4>' + svg_years() + '</div><div><h4>Halmozott pénzállás negyedévente · M Ft</h4>' + svg_cash() + '</div></div>' +
    '<h4 style="margin-top:50px">Eladott darabszám csatornánként · alap forgatókönyv</h4>' + svg_mix() +
    '<div class="bp-tables">' + pl_table("Alap") + pl_table("Óvatos") + pl_table("Optimista") + '</div>' +
    '<div class="bp-two"><div><h4>Egységgazdaságtan</h4>' + unit_t + '<p class="bp-small">A közvetlen költség tartalmazza a lapot, a megmunkálást, a Häfele-vasalatot, a fogantyút, a csomagolást, a szállítást és a szerelést. LED és tükör felár külön fedezetet hoz.</p></div>'
    '<div><h4>Az első év költségvetése</h4>' + bars(sorted(list(Y1.items()) + [("Beruházás (minták, eszközök)", Y1_CAPEX)], key=lambda x: -x[1])) +
    f'<p class="bp-small">Összesen kb. {M(sum(Y1.values()) + Y1_CAPEX)} M Ft. A Construma-stand 24 m²-en a korai árral (170–195 €/m²) és építéssel kb. 4 M Ft.</p></div></div>' +
    '<div class="bp-two"><div><h4>Megtérülés</h4><ul><li><b>Alap:</b> pozitív EBITDA 2028 Q4-től, a legmélyebb pénzállás 2029 Q2-ben kb. ' + M(-BASE["min_cash"]) + ' M Ft, a halmozott megtérülés 2030 elején.</li>'
    f'<li><b>Óvatos:</b> pozitív EBITDA 2029 Q3-tól, kb. {M(-O["Óvatos"]["min_cash"])} M Ft tőkeigény, megtérülés 2031 körül.</li>'
    f'<li><b>Optimista:</b> pozitív EBITDA 2028 Q3-tól, kb. {M(-O["Optimista"]["min_cash"])} M Ft tőkeigény, a halmozott megtérülés 2029 Q2-ben.</li></ul></div>'
    '<div><h4>Finanszírozás (alap)</h4><ul><li>8 M Ft alapítói saját forrás</li><li>20–25 M Ft kedvezményes vállalkozói hitel (pl. Széchenyi Kártya Program)</li><li>30 M Ft angyalbefektető, két mérföldkőhöz kötve (100. és 400. eladás)</li><li>2028-tól exportpiaci és innovációs pályázatok figyelése</li></ul></div></div>', "stone") +
  S(head("10 · Kockázatok", "Ami elsőre <em>nem fog menni.</em>") +
    '<table class="bp-t risks"><thead><tr><td>Kockázat</td><td>Mi történhet?</td><td>Válasz</td></tr></thead><tbody>' + "".join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>' for a, b, c in RISKS) + '</tbody></table>', "paper") +
  band(R + "hero_evening.jpg", "2029 és tovább", "Egy szekrény, <em>ami befejezi a többit.</em>", "A cél nem a legtöbb eladott darab, hanem az, hogy a „ZENIT-elni” ige legyen.", center=True) +
  S(head("Források", "Amire <em>a számok épülnek.</em>") + '<ol class="bp-src">' + "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in SOURCES) + '</ol>' +
    '<p class="bp-small">Minden más szám – darabszám, ár, költség, konverzió – tervezői becslés. A ZENIT márka, a díjak és az események a látványprojekt részeként kitaláltak.</p>', "ivory") +
  nxt("", "projekt.html", "A projektről", "Négy nap, egy ötlet, egy mesterséges intelligencia – a teljes folyamat.", alt=False))

page("uzleti-terv.html", "Üzleti terv 2027–2029 – ZENIT", "A ZENIT üzleti és operatív stratégiája: piac, márka, értékesítés, marketing, kiállítások, terjeszkedés és háromforgatókönyves pénzügyi terv.", BP)
