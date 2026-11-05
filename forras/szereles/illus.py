"""ZENIT – szerelési ábrák a gyártási geometriából (ferde axonometria, vonalas, prémium stílus).
Kimenet: SVG lépésenként + steps.json (cím, leírás, kellékek, szerszámok) a weboldalhoz, a kézikönyvhöz és a PDF-hez.
Használat: python3 illus.py <kimeneti mappa>"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry import parts, holes_and_hardware, PARAMS

OUT = sys.argv[1] if len(sys.argv) > 1 else "szereles"
os.makedirs(OUT, exist_ok=True)

# ---- színek (ZENIT papír)
INK, LINE, DONE, DONE_T, DONE_S = "#2B2622", "#2B2622", "#F3EEE6", "#FAF7F2", "#E4DDD2"
ACT, ACT_T, ACT_S = "#D8BF97", "#E9D7B8", "#C4A577"
BRONZE, MUTED = "#A8834F", "#8C8378"
GHOST = "#D9D2C7"

# ---- ferde (kabinet-) axonometria: a front valós alakban, a mélység 30°-ban, fele léptékben
CA, SA, K = math.cos(math.radians(35)), math.sin(math.radians(35)), 0.62
S = 0.42  # mm → rajzegység


def P(x, y, z):
    return (S * (x + y * K * CA), S * (-z - y * K * SA))


def box_faces(b):
    x, y, z, dx, dy, dz = b
    X, Y, Z = x + dx, y + dy, z + dz
    front = [P(x, y, z), P(X, y, z), P(X, y, Z), P(x, y, Z)]
    top = [P(x, y, Z), P(X, y, Z), P(X, Y, Z), P(x, Y, Z)]
    right = [P(X, y, z), P(X, Y, z), P(X, Y, Z), P(X, y, Z)]
    return front, top, right


def poly(pts, fill, stroke=LINE, sw=1.1, op=1.0, dash=None):
    d = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    return (f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"'
            + (f' fill-opacity="{op}" stroke-opacity="{min(1, op + .25)}"' if op < 1 else "")
            + (f' stroke-dasharray="{dash}"' if dash else "") + "/>")


def draw_box(b, style):
    f, t, r = box_faces(b)
    if style == "act":
        cols = (ACT, ACT_T, ACT_S); sw = 1.4; op = 1
    elif style == "ghost":
        return "".join(poly(p, "none", "#B9AFA2", 1.1, 1, "7 5") for p in (f, t, r))
    elif style == "fade":
        cols = (DONE, DONE_T, DONE_S); sw = 0.8; op = 0.55
    else:
        cols = (DONE, DONE_T, DONE_S); sw = 1.0; op = 1
    return poly(r, cols[2], sw=sw, op=op) + poly(t, cols[1], sw=sw, op=op) + poly(f, cols[0], sw=sw, op=op)


def arrow(p1, p2, col=BRONZE, sw=2.6):
    (x1, y1), (x2, y2) = P(*p1), P(*p2)
    a = math.atan2(y2 - y1, x2 - x1); L = 14
    h1 = (x2 - L * math.cos(a - 0.42), y2 - L * math.sin(a - 0.42)); h2 = (x2 - L * math.cos(a + 0.42), y2 - L * math.sin(a + 0.42))
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>'
            f'<polygon points="{x2:.1f},{y2:.1f} {h1[0]:.1f},{h1[1]:.1f} {h2[0]:.1f},{h2[1]:.1f}" fill="{col}"/>')


def dot(p, r=4, col=BRONZE, ring=False):
    x, y = P(*p)
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{"none" if ring else col}" stroke="{col}" stroke-width="1.6"/>')


def label(p, txt, dx=0, dy=0, size=26, col=INK, anchor="middle", weight=500):
    x, y = P(*p)
    return (f'<text x="{x + dx:.1f}" y="{y + dy:.1f}" font-family="Inter, Helvetica, Arial, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" fill="{col}" text-anchor="{anchor}">{txt}</text>')


def letter(p, ch, dx=0, dy=0):
    x, y = P(*p); x += dx; y += dy
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="19" fill="#FBF8F3" stroke="{INK}" stroke-width="1.3"/>'
            f'<text x="{x:.1f}" y="{y + 8:.1f}" font-family="Cormorant Garamond, Georgia, serif" font-size="24" fill="{INK}" text-anchor="middle">{ch}</text>')


# ---- alkatrészek
PS = parts()
by = {q["name"]: q for q in PS}
L = {"K bal oldallap": "A", "K jobb oldallap": "B", "K fenéklap": "C", "K tetőlap": "D", "K 1. közfal": "E",
     "K 2. közfal": "F", "K polc": "G", "K hátfal": "H", "K bal ajtó": "J", "K középső ajtó": "K", "K jobb ajtó": "L"}
holes, hw = holes_and_hardware()


def B(name, off=(0, 0, 0)):
    x, y, z, dx, dy, dz = by[name]["box"]
    return (x + off[0], y + off[1], z + off[2], dx, dy, dz)


def scene(items, extras="", pad=70, base=False):
    """items: [(név, stílus, eltolás)] – festő-algoritmus: hátulról előre, alulról felfelé."""
    boxes = []
    if base:  # a meglévő szekrény csonkja szaggatottan
        boxes.append(((0, 0, -360, 2500, 600, 360), "ghost"))
    for n, st, off in items:
        boxes.append((B(n, off), st))
    boxes.sort(key=lambda bs: (-(bs[0][1] + bs[0][4] / 2) // 60, bs[0][2] + bs[0][5] / 2, bs[0][0]))
    body = "".join(draw_box(b, s) for b, s in boxes) + extras
    # befoglaló doboz
    xs, ys = [], []
    for b, _ in boxes:
        for f in box_faces(b):
            for a, c in f:
                xs.append(a); ys.append(c)
    x0, y0, x1, y1 = min(xs) - pad, min(ys) - pad - 30, max(xs) + pad, max(ys) + pad
    return x0, y0, x1, y1, body


def svg(fn, sc, w=1200):
    x0, y0, x1, y1, body = sc
    h = round(w * (y1 - y0) / (x1 - x0))
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.0f} {y0:.0f} {x1 - x0:.0f} {y1 - y0:.0f}" width="{w}" height="{h}">'
         f'{body}</svg>')
    open(os.path.join(OUT, fn), "w", encoding="utf8").write(s)
    return fn


ALL = list(L)
SIDES, BOT, TOP, P1, P2 = "K bal oldallap", "K fenéklap", "K tetőlap", "K 1. közfal", "K 2. közfal"
SHELF, BACK, DOORS = "K polc", "K hátfal", ["K bal ajtó", "K középső ajtó", "K jobb ajtó"]
RIGHT = "K jobb oldallap"


def hw_pts(kind_sub, part=None):
    out = []
    for h in holes:
        if kind_sub in h["kind"] and (part is None or h["part"] == part):
            out += h["pts"]
    return out


steps = []


def step(no, title, text, items, extras="", base=False, need=(), tools=(), people=1, minutes=10, warn=None):
    fn = svg(f"lepes_{no:02d}.svg", scene(items, extras, base=base))
    steps.append(dict(no=no, title=title, text=text, svg=fn, need=list(need), tools=list(tools), people=people, minutes=minutes, warn=warn))


# 1. tiplik a fenéklapba és a tetőlapba
ex = "".join(dot(p, 5) for p in hw_pts("tipli (lapél)", BOT) + hw_pts("tipli (fenéklap felső lapja)", BOT))
ex += letter((1250, 300, 18), "C", 0, -60)
step(1, "Tiplik a helyükre", "Fektesd a fenéklapot (C) egy puha takaróra. Üsd be a 8×35-ös fatipliket a jelölt furatokba – gumikalapáccsal, ütközésig. Ugyanígy a tetőlapba (D).",
     [(BOT, "act", (0, 0, 0))], ex, need=[("Fatipli 8×35", 16)], tools=["gumikalapacs"], minutes=10)

# 2. oldallapok
ex = arrow((-260, 300, 265), (-40, 300, 265)) + arrow((2760, 300, 265), (2540, 300, 265))
ex += letter((-150, 0, 560), "A") + letter((2650, 0, 560), "B")
step(2, "Oldallapok", "Illeszd az oldallapokat (A, B) a fenéklap tiplijeire. Kötésenként két konfirmát 7×50 csavarral húzd össze – kívülről, a süllyesztett furatokon át. Ne húzd túl: ütközésig, majd negyed fordulat.",
     [(BOT, "done", (0, 0, 0)), (SIDES, "act", (-220, 0, 0)), (RIGHT, "act", (220, 0, 0))], ex,
     need=[("Konfirmát 7×50", 4)], tools=["csavarozo", "imbusz"], minutes=15)

# 3. közfalak
ex = arrow((800, 300, 760), (800, 300, 560)) + arrow((1700, 300, 760), (1700, 300, 560))
ex += letter((800, 0, 840), "E", 0, 0) + letter((1700, 0, 840), "F", 0, 0)
step(3, "Közfalak", "A két közfalat (E, F) a fenéklap tiplijeire ültesd, majd alulról, a fenéklapon át két-két konfirmáttal rögzítsd. A közfal pántfuratai a rekesz felé néznek – az ábrán jelölt oldalra.",
     [(BOT, "done", (0, 0, 0)), (SIDES, "done", (0, 0, 0)), (RIGHT, "done", (0, 0, 0)), (P1, "act", (0, 0, 220)), (P2, "act", (0, 0, 220))], ex,
     need=[("Konfirmát 7×50", 4)], tools=["csavarozo", "imbusz"], minutes=15)

# 4. tetőlap
ex = arrow((1250, 300, 1080), (1250, 300, 760))
ex += letter((1250, 0, 1000), "D", -60, 0)
step(4, "Tetőlap", "Tedd fel a tetőlapot (D) a tiplikre, és rögzítsd: az oldallapokon át kívülről, a közfalakba felülről – mindenhol két-két konfirmát.",
     [(BOT, "done", (0, 0, 0)), (SIDES, "done", (0, 0, 0)), (RIGHT, "done", (0, 0, 0)), (P1, "done", (0, 0, 0)), (P2, "done", (0, 0, 0)), (TOP, "act", (0, 0, 320))], ex,
     need=[("Konfirmát 7×50", 8), ("Takarósapka", 8)], tools=["csavarozo", "imbusz"], minutes=15)

# 5. derékszög – átlók
x0, x1, z0, z1 = 0, 2500, 0, 530
ex = (f'<line x1="{P(x0,0,z0)[0]:.1f}" y1="{P(x0,0,z0)[1]:.1f}" x2="{P(x1,0,z1)[0]:.1f}" y2="{P(x1,0,z1)[1]:.1f}" stroke="{BRONZE}" stroke-width="2" stroke-dasharray="10 7"/>'
      f'<line x1="{P(x0,0,z1)[0]:.1f}" y1="{P(x0,0,z1)[1]:.1f}" x2="{P(x1,0,z0)[0]:.1f}" y2="{P(x1,0,z0)[1]:.1f}" stroke="{BRONZE}" stroke-width="2" stroke-dasharray="10 7"/>')
ex += label((1250, 0, 265), "a₁ = a₂", 0, -14, 24, BRONZE)
step(5, "Derékszög", "Mérd meg a korpusz két átlóját. Ha egyformák (±2 mm), a szekrény derékszögű – ez a záródó ajtók titka. Ha eltérnek, a hosszabb átló sarkait finoman nyomd össze.",
     [(n, "done", (0, 0, 0)) for n in (BOT, SIDES, RIGHT, P1, P2, TOP)], ex, tools=["meroszalag"], minutes=5)

# 6. hátfal
nails = [h["p1"] for h in hw if "hátfalszeg" in h["kind"]][::3]
ex = "".join(dot((p[0], 600, p[2]), 4.5) for p in nails)
ex += arrow((1250, 1150, 265), (1250, 700, 265)) + letter((2200, 640, 470), "H")
step(6, "Hátfal", "Fordítsd a korpuszt elejével lefelé. Fektesd rá a hátfalat (H), igazítsd a sarkokhoz, és ~15 cm-enként üsd be a hátfalszegeket – körbe és a közfalakba is. Előfúrni nem kell.",
     [(n, "done", (0, 0, 0)) for n in (BOT, SIDES, RIGHT, P1, P2, TOP)] + [(BACK, "act", (0, 380, 0))], ex,
     need=[("Hátfalszeg 1,6×25", 50)], tools=["kalapacs"], minutes=20)

# 7. pánttalpak
plates = hw_pts("pánttalp")
ex = "".join(dot(p, 5.5) for p in plates)
step(7, "Pánttalpak", "Csavarozd fel a hat Häfele szerelőtalpat az előfúrt helyekre: az oldallapokra és a 2. közfalra, két-két 3,5×16 csavarral.",
     [(n, "done", (0, 0, 0)) for n in (BOT, SIDES, RIGHT, P1, P2, TOP, BACK)], ex,
     need=[("Häfele szerelőtalp", 6), ("Csavar 3,5×16", 12)], tools=["csavarozo"], minutes=10)

# 8. feltétel a szekrényre
ex = arrow((1250, -300, 760), (1250, -300, 560)) + arrow((1250, -330, 300), (1250, -120, 300))
ex += label((1250, -300, 860), "2 fő", 0, 0, 24, BRONZE, weight=600)
fix = [(250, 300, 0), (550, 300, 0), (1950, 300, 0), (2250, 300, 0)]
ex += "".join(dot(p, 5.5) for p in fix)
ex += (f'<line x1="{P(-150,0,540)[0]:.1f}" y1="{P(-150,0,540)[1]:.1f}" x2="{P(2650,0,540)[0]:.1f}" y2="{P(2650,0,540)[1]:.1f}" stroke="{BRONZE}" stroke-width="1.6" stroke-dasharray="12 6"/>'
       + label((2650, 0, 540), "plafon · ~10 mm", 10, 5, 15, BRONZE, anchor="start"))
step(8, "Fel a szekrényre", "Ketten emeljétek fel a korpuszt a meglévő szekrény tetejére – vízszintesen, és toljátok hátra. A plafonig ~10 mm marad, ezért billenteni nem lehet. Belülről, a két szélső rekeszben 2-2 csavarral rögzítsd a szekrény tetejéhez (Ø2,5 előfurat).",
     [(n, "done", (0, 0, 0)) for n in (BOT, SIDES, RIGHT, P1, P2, TOP, BACK)], ex, base=True,
     need=[("Csavar 3,5×30", 4)], tools=["letra", "csavarozo", "furo25", "ket_fo"], people=2, minutes=20,
     warn="Emeléskor mindig ketten! A korpusz kb. 56 kg ajtók nélkül.")

# 9. polc
pins = hw_pts("polctartó")
ex = "".join(dot(p, 5) for p in pins) + arrow((1250, -350, 274), (1250, -60, 274)) + letter((1250, -300, 274), "G", 0, -40)
step(9, "Polc", "Nyomd a polctartó csapokat a középső rekesz furataiba – oldalanként hármat. Csúsztasd be a polcot (G).",
     [(n, "done", (0, 0, 0)) for n in (BOT, SIDES, RIGHT, P1, P2, TOP, BACK)] + [(SHELF, "act", (0, -320, 0))], ex, base=True,
     need=[("Polctartó csap Ø5", 6)], minutes=5)

# 10. ajtók
ex = arrow((400, -500, 265), (400, -120, 265)) + arrow((1250, -500, 265), (1250, -120, 265)) + arrow((2100, -500, 265), (2100, -120, 265))
ex += letter((400, -420, 560), "J") + letter((1250, -420, 560), "K") + letter((2100, -420, 560), "L")
step(10, "Ajtók", "Pattintsd az ajtókat (J, K, L) a szerelőtalpakra – szerszám nélkül, egy kattanásig. A pántok három csavarjával állítsd be a hézagokat: 3 mm az ajtók között, egyenes vonal alul és felül.",
     [(n, "done", (0, 0, 0)) for n in (BOT, SIDES, RIGHT, P1, P2, TOP, BACK, SHELF)] + [(d, "act", (0, -260, 0)) for d in DOORS], ex, base=True,
     tools=["pz2"], minutes=20)

# 11. fogantyúk
hs = [h for h in hw if "foganty" in h["kind"].lower()]
ex = ""
for d in DOORS:
    x, y, z, dx, dy, dz = by[d]["box"]
    cx = x + dx / 2
    ex += poly([P(cx - 112, -2, z - 2), P(cx + 112, -2, z - 2), P(cx + 112, -2, z - 16), P(cx - 112, -2, z - 16)], "#C9C6C0", INK, 1.2)
    ex += dot((cx - 96, 0, z + 10), 4.5) + dot((cx + 96, 0, z + 10), 4.5)
ex += label((1250, 0, -60), "furattáv 192 mm", 0, 0, 16, MUTED)
step(11, "Fogantyúk", "Nyisd ki az ajtót, és belülről, két-két 3,5×16 csavarral rögzítsd a GTV HEXA élfogantyút az alsó él közepére. A furatok előre elkészültek, 192 mm-re egymástól.",
     [(n, "done", (0, 0, 0)) for n in (BOT, SIDES, RIGHT, P1, P2, TOP, BACK, SHELF)] + [(d, "done", (0, 0, 0)) for d in DOORS], ex, base=True,
     need=[("GTV HEXA 192 élfogantyú", 3), ("Csavar 3,5×16", 6)], tools=["csavarozo"], minutes=10)

# 12. kész
ex = label((1250, 0, 640), "Z E N I T", 0, 0, 30, INK, weight=300)
step(12, "Kész. Csend.", "Húzd le a védőfóliát, töröld át a felületeket puha, száraz kendővel. Csukd be az ajtókat – és hallgasd, ahogy a fékes pántok csendben behúzzák őket.",
     [(n, "done", (0, 0, 0)) for n in (BOT, SIDES, RIGHT, P1, P2, TOP, BACK, SHELF)] + [(d, "done", (0, 0, 0)) for d in DOORS], ex, base=True, minutes=5)

# ---- alkatrész-áttekintő (A–L)
def parts_sheet():
    items, ex, x = [], "", 0
    order = [SIDES, RIGHT, BOT, TOP, P1, P2, SHELF, BACK] + DOORS
    # külön rajz minden alkatrészről: egymás mellé rakott dobozok (kis méretben a valós arányokkal)
    out = []
    for n in order:
        q = by[n]; b = q["box"]
        sc = scene([(n, "done", (-b[0], -b[1], -b[2]))], letter((b[3] / 2, 0, b[5] + 60), L[n]), pad=50)
        fn = svg(f"alkatresz_{L[n]}.svg", sc, w=360)
        out.append(dict(letter=L[n], name=n.replace("K ", "").capitalize(), file=fn, dim=f"{round(max(b[3], b[4], b[5]))} × {round(sorted([b[3], b[4], b[5]])[1])} mm", db=1))
    return out


meta = dict(steps=steps, parts=parts_sheet(), total_minutes=sum(s["minutes"] for s in steps))
json.dump(meta, open(os.path.join(OUT, "steps.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(len(steps), "lépés,", meta["total_minutes"], "perc")
