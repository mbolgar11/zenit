"""Rövid gyártási dokumentáció PDF (A4 fekvő) + 1:1 fúrósablon – v8. Minden szám a geometry.py / cutlist.json-ból."""
import json, os, sys, datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image,
                                Table, TableStyle, PageBreak, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus.flowables import Flowable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry import PARAMS as P, joint_positions, JOINT as J

pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("DV", normal="DV", bold="DVB", italic="DV", boldItalic="DVB")

d = json.load(open("cutlist.json"))
OUT = sys.argv[1]
PAGE = landscape(A4)
BROWN = colors.HexColor("#6B5E50"); SAND = colors.HexColor("#EFE9E2"); RED = colors.HexColor("#B5462F")
BLUE = colors.HexColor("#2F6DB5")

S = {
    "h1": ParagraphStyle("h1", fontName="DVB", fontSize=22, leading=27, textColor=BROWN, spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName="DVB", fontSize=14, leading=18, textColor=BROWN, spaceAfter=6, spaceBefore=2),
    "b": ParagraphStyle("b", fontName="DV", fontSize=9.5, leading=13.5),
    "s": ParagraphStyle("s", fontName="DV", fontSize=8, leading=10.5, textColor=colors.HexColor("#555555")),
    "c": ParagraphStyle("c", fontName="DV", fontSize=8.5, leading=10.5),
}


def footer(cv, doc):
    cv.saveState()
    cv.setFont("DV", 7.5); cv.setFillColor(colors.HexColor("#888888"))
    cv.drawString(15 * mm, 8 * mm, "Rátétszekrény ELIA D 250-re · v10 végleges · gyártási dokumentáció · Bolgár Milán, 2026")
    cv.drawRightString(PAGE[0] - 15 * mm, 8 * mm, f"{doc.page}. oldal")
    cv.restoreState()


def img(path, w_mm, max_h_mm=None):
    from PIL import Image as PI
    iw, ih = PI.open(path).size
    w = w_mm * mm; h = w * ih / iw
    if max_h_mm and h > max_h_mm * mm:
        h = max_h_mm * mm; w = h * iw / ih
    return Image(path, width=w, height=h)


def tstyle(header_rows=1):
    return TableStyle([
        ("FONT", (0, 0), (-1, -1), "DV", 8.5),
        ("FONT", (0, 0), (-1, header_rows - 1), "DVB", 8.5),
        ("BACKGROUND", (0, 0), (-1, header_rows - 1), BROWN),
        ("TEXTCOLOR", (0, 0), (-1, header_rows - 1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFB5AA")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, header_rows), (-1, -1), [colors.white, SAND]),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ])



ORANGE = colors.HexColor("#C28A00")
from geometry import holes_and_hardware, hardware_counts, layout
_h, _hw = holes_and_hardware()
NH = sum(len(h["pts"]) for h in _h)
H = P["H"]; t = P["t"]; gv = P["gap_v"]; DOOR_H = H - 2 * gv
ZH = (gv + 95.5, H - gv - 95.5)
DP = P["D"] - P["t_door"] - P["t_back"]
PIN_Y = (37.0, DP / 2, DP - 37.0)
Z_PIN = [h for h in _h if h["kind"] == "polctartó csap furat"][0]["pts"][0][2]
GAP_TOP = P["ceiling"] - P["base_H"] - H
W = d["weights"]["K"]
el1 = sum(r["el_m_1"] for r in d["rows"]); el2 = sum(r["el_m_2"] for r in d["rows"])
tot18 = sum(r["terulet"] for r in d["rows"] if r["anyag"].startswith("Lam"))
N_NAIL = hardware_counts()["hátfalszeg 1,6×25"]


def small_table(rows, widths, fs=8, header=True):
    tt = Table([[Paragraph(str(c), ParagraphStyle("x", fontName="DV", fontSize=fs, leading=fs + 2)) if isinstance(c, str) and len(c) > 25 else c
                 for c in r] for r in rows], colWidths=[w * mm for w in widths], repeatRows=1 if header else 0)
    if header:
        st = tstyle(1); st.add("FONT", (0, 0), (-1, -1), "DV", fs); st.add("FONT", (0, 0), (-1, 0), "DVB", fs)
    else:
        st = TableStyle([("FONT", (0, 0), (-1, -1), "DV", fs), ("FONT", (0, 0), (0, -1), "DVB", fs),
                         ("TEXTCOLOR", (0, 0), (0, -1), BROWN), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFB5AA")),
                         ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, SAND])])
    st.add("TOPPADDING", (0, 0), (-1, -1), 1.5); st.add("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)
    tt.setStyle(st); return tt


def page(title, *flow):
    return [KeepTogether([Paragraph(title, S["h2"])] + list(flow)), PageBreak()]


FW, FH = PAGE[0] - 30 * mm - 12, PAGE[1] - 26 * mm - 12 - 3 * mm   # keret (6 pt belső margó, tartalék)


def fit_page(title, build, hi, lo, step=1.0):
    """A legnagyobb x (mm), amelynél az oldal tartalma egy oldalra fér – a rajzok így a lehető legnagyobbak."""
    x = hi
    while x >= lo:
        flow = [Paragraph(title, S["h2"])] + build(x)
        h = 0; ok = True
        for f in flow:
            w_, h_ = f.wrap(FW, FH)
            h += h_ + f.getSpaceBefore() + f.getSpaceAfter()
            if w_ > FW + 0.5: ok = False
        if ok and h <= FH:
            print(f"  {title[:40]}: x = {x:.0f} mm")
            return [KeepTogether([Paragraph(title, S["h2"])] + build(x)), PageBreak()]
        x -= step
    raise SystemExit("nem fér el: " + title)


story = []
# ===== 1. Borító + végleges döntések
spec = [
    ["Méret", f"{sum(P['module_widths'])} × {H} × {P['D']} mm (sz × m × mé) · {GAP_TOP} mm hely marad a plafonig (2590 mm)"],
    ["Felépítés", f"Egy korpusz: 2 oldallap + 2 közfal, egybefüggő 2464 mm-es tető/fenék, 1 HDF hátfal · ajtóosztás {' + '.join(map(str, P['module_widths']))} mm"],
    ["Ajtók", f"797 / 897 / 797 × {DOOR_H:g} mm, körbe 2 mm ABS · hézag 1,5 mm oldalt, 3 mm az ajtók közt, {gv:g} mm fent/lent · a középső megfordítható"],
    ["Pántok", "Häfele Metalla 300SM kombi 110° – ajtónként fent FÉKES, lent rugós; a közfalon félig ráütődő"],
    ["Fogantyú", "GTV HEXA lekerekített alu élfogantyú (elox), 192/225 mm, az ajtók alsó élének közepén, hátulról csavarozva"],
    ["Anyag", "OBI fehér 18 mm laminált forgácslap (4160321) · ajtók 2 mm ABS, minden más elülső él 0,4 mm ABS · 3 mm fehér HDF"],
    ["Kötés", "Élenként 2 konfirmát 7×50 + 2 bükk tipli 8×35 – szétszedhető"],
    ["Polc", "Középen levehető polc 3 + 3 Ø5 csapon; csapfuratok mindhárom rekeszben (később a szélsőkbe is tehető polc)"],
    ["Hátfal", f"Beütős hátfalszeg 1,6×25, kb. 15 cm-enként körbe és a 4 függőleges elembe ({N_NAIL} db) – előfúrás, jelölés nem kell"],
    ["Rögzítés", "4 db 3,5×30 a két szélső rekeszben, a fenéklapon át az ELIA tetejébe; falhoz/plafonhoz nem"],
    ["Kötőelemek", "3 csavarfajta (7×50 · 3,5×16 · 3,5×30) + hátfalszeg"],
    ["Tömeg", f"korpusz ajtó nélkül ~{W['no_door']} kg, ajtókkal ~{W['total']} kg (3 ember emelje)"],
]
right = [Paragraph("Rátétszekrény – v10 (végleges)", S["h1"]),
         Paragraph("az ELIA D 250 tolóajtós szekrény tetejére", S["h2"]),
         small_table(spec, [24, 104], fs=7.5, header=False), Spacer(1, 6),
         Paragraph(f"Tartalom: 1 Áttekintés · 2 Nézetrajz és 3D modell · 3 Szabásjegyzék és szabásterv · 4 Vasalat · 5 Szerelés · "
                   f"6–13 Alkatrészrajzok furattáblával · 14–16 Fúrósablon 1:1. Készült {datetime.date.today():%Y. %m. %d.} – "
                   "Claude (Anthropic) + Bolgár Milán; paraméteres modell: Python → Fusion 360 / CadQuery.", S["s"])]
story += [Table([[img("renders/koncepcio_three.png", 132), right]], colWidths=[136 * mm, 132 * mm],
                style=[("VALIGN", (0, 0), (-1, -1), "TOP")]), PageBreak()]

# ===== 2. Nézetrajz + Fusion
TXT2 = (f"Magasság: 2590 (plafon legalacsonyabb pontja) − 2050 (ELIA) − {GAP_TOP} mm beemelési játék = {H} mm. "
        f"A Fusion modellben minden lap külön komponens, az ABS él külön test; {len(_h)} furat-feature / {NH} furat, {len(_hw)} db vasalat a helyén. "
        "Jobb alsó kép: ajtók és hátfal elrejtve. A korpuszt a földön szereld össze, ajtó nélkül emeld fel és told hátra.")


def _ar(p):
    from PIL import Image as _I
    w_, h_ = _I.open(p).size
    return h_ / w_


def b2(x):
    eh = x * _ar("doc/img/elevation.png")
    fw = min(FW / mm - x - 8, (eh - 3) / (_ar("doc/img/fusion/osszeallitas.png") + _ar("doc/img/fusion/belso_vasalat.png")))
    return [Table([[img("doc/img/elevation.png", x), [img("doc/img/fusion/osszeallitas.png", fw), Spacer(1, 3),
                                                       img("doc/img/fusion/belso_vasalat.png", fw)]]],
                  colWidths=[(x + 4) * mm, (fw + 4) * mm], style=[("VALIGN", (0, 0), (-1, -1), "TOP")]),
            Paragraph(TXT2, S["s"])]


story += fit_page("Nézetrajz és 3D modell (Autodesk Fusion)", b2, FW / mm - 75, 100)

# ===== 3. Szabásjegyzék + szabásterv
codes = {}
for p_ in json.load(open("doc/parts.json")):
    for n in p_["names"]: codes[n] = p_["code"]
rows = [["Poz.", "Megnevezés", "Hossz", "Szél.", "Vast.", "Db", "Élzárás", "Rajz"]]
for r in d["rows"]:
    rows.append([r["poz"], r["nev"], f'{r["L"]:g}', f'{r["W"]:g}', 18 if r["anyag"].startswith("Lam") else 3, r["db"], r["eltxt"],
                 {"Ajtó": "A08–A10", "Oldallap": "A01", "Közfal": "A04–A05", "Fenéklap": "A02", "Tetőlap": "A03"}.get(r["nev"], "nincs furat")])
rows.append(["", "Összesen", "", "", "", sum(r["db"] for r in d["rows"]), "", ""])
st_ = small_table(rows, [11, 24, 15, 15, 12, 10, 64, 20], fs=8)
def b3(x):
    return [Table([[[st_, Spacer(1, 5),
             Paragraph(f"<b>Készméretek mm-ben, élzárással együtt.</b> Fehér uni: nincs szálirány. HDF hátfal 3 mm. "
                       f"<b>Anyag:</b> 18 mm lap nettó {tot18:.2f} m² → <b>{d['sheets']} tábla</b> 2800×2070 · HDF 1 tábla · "
                       f"élzáró 0,4 mm {el1:.1f} fm · 2 mm {el2:.1f} fm.", S["c"]), Spacer(1, 4),
             Paragraph("<b>Rendeléskor kérd:</b> pántcsésze-fúrás az ajtókon – Ø35×13 mm, csészeközép 21,5 mm-re a pántoldali éltől, "
                       "95,5 mm-re az ajtó aljától és tetejétől; pántoldal: bal ajtó bal, középső jobb, jobb ajtó jobb. "
                       "<b>A 2464 mm-es lapok autóba nem férnek – szállítás kell.</b> Ha a többi furatot is vállalják, add oda a 6–13. oldalt "
                       "és az Excel „Furatok” lapját.", S["c"])],
            [img("doc/img/sheet1.png", x), Spacer(1, 2), img("doc/img/sheet2.png", x)]]],
          colWidths=[175 * mm, (x + 4) * mm], style=[("VALIGN", (0, 0), (-1, -1), "TOP")])]


story += fit_page("Szabásjegyzék és szabásterv – rendeléshez (OBI / lapszabászat)", b3, FW / mm - 179, 50)


# ===== 4. Vasalat + szerszám
vr = [["Tétel", "Menny.", "Hova / megjegyzés"]] + [[n, f"{q} {u}", note] for n, q, u, note in d["hardware"]]
tr = [["Szerszám", "Mire kell"]] + [[a, b] for a, b in d["tools"]]
story += page("Vasalat, kötőelem, szerszám",
    small_table(vr, [95, 18, 152], fs=7.5), Spacer(1, 6), small_table(tr, [95, 170], fs=7.5))

# ===== 5. Szerelés
steps = [
    ["1. Előkészítés", "Fúrósablon nyomtatása 100%-on (ellenőrizd a 100 mm-es vonalzót). Tető- és fenéklapon a közfalak középvonala: 800 és 1700 mm balról."],
    ["2. Fúrás", f"A 6–13. oldal szerint: konfirmát Ø7 átmenő + süllyesztés, Ø5×50 a lapélben; tipli Ø8×12 / Ø8×25; polccsap Ø5 – oldallapon 12 mm mély, "
                 f"közfalon átmenő, oldalanként 3 db ({PIN_Y[0]:g} / {PIN_Y[1]:g} / {PIN_Y[2]:g} mm elölről, oldallapon {Z_PIN:g}, közfalon {Z_PIN - t:g} mm magasan); "
                 f"pánttalp Ø2,5×10 ({ZH[0]:g} és {ZH[1]:g} mm magasan, 37 mm elölről); élfogantyú Ø2,5×12 az ajtók belső lapján, 10 mm-re az alsó éltől, 192 mm-re egymástól."],
    ["3. Korpusz a FÖLDÖN", "Fenéklapra tiplik → oldallapok és közfalak rá → konfirmátok alulról a fenéklapon át és oldalról az oldallapokon át."],
    ["4. Tetőlap", "Tetőlap a tiplikre → konfirmátok felülről a közfalakba, oldalról az oldallapokon át."],
    ["5. Hátfal", f"Átlómérés (egyformák legyenek), majd a {sum(P['module_widths']) - 2}×{H - 2} HDF beütős hátfalszeggel, kb. 15 cm-enként körbe és a 4 függőleges elembe – előfúrás, jelölés nélkül, a lapok közepére célozva. A polcba nem."],
    ["6. Vasalat", "Pánttalpak 2-2 db 3,5×16 csavarral (bal oldallap, 2. közfal bal lapja, jobb oldallap). Fent a FÉKES, lent a rugós pánt. "
                   "Élfogantyúk az ajtók alsó élének közepére, hátulról a belső lapba, 2-2 db 3,5×16. Polccsapok (3 + 3) és polc a középső rekeszbe."],
    ["7. Felemelés", f"Ajtó nélkül ~{W['no_door']} kg, 2,5 m hosszú – 3 ember. A plafonig csak {GAP_TOP} mm marad: a korpuszt elölről, vízszintesen told fel az ELIA tetejére, "
                     "ne billentsd. Rögzítés: 4 db 3,5×30 a fenéklapon át (az ELIA tetejét Ø2,5-tel előfúrni)."],
    ["8. Ajtók", f"Rákattintás a pántokra, beállítás: 1,5 mm oldalt, 3 mm az ajtók között, {gv:g} mm fent/lent. A középső ajtó fejjel lefelé fordítva a másik közfalra is felrakható (tartalék előfuratok)."],
]
stp = Table([[Paragraph(f"<b>{a}</b>", S["c"]), Paragraph(b, S["c"])] for a, b in steps], colWidths=[34 * mm, 140 * mm])
stp.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFB5AA")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                         ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, SAND]),
                         ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
story += fit_page("Szerelési útmutató", lambda x: [Table([[stp, img("renders/koncepcio_open.png", x)]], colWidths=[178 * mm, (x + 4) * mm],
                                                          style=[("VALIGN", (0, 0), (-1, -1), "TOP")])], FW / mm - 182, 40)

# ===== 6–9. Alkatrészrajzok
parts_doc = {p_["code"]: p_ for p_ in json.load(open("doc/parts.json"))}


def hole_table(p_, fs=6.5):
    rows = [["Jel", "Felület", "u", "v", "Ø", "Mély.", "Süll."]]
    for r in p_["rows"]:
        u = "él" if r["face"] in ("bal él", "jobb él") else f'{r["u"]:g}'
        rows.append([r["jel"], r["face"], u, f'{r["v"]:g}', f'{r["d"]:g}', f'{r["depth"]:g}', f'{r["cs"]:g}' if r["cs"] else ""])
    tt = small_table(rows, [8, 23, 11, 11, 8, 10, 9], fs=fs)
    tt.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    return tt


LEG = ("Jelek: K konfirmát · T tipli · P pántcsésze · PT pánttalp-előfurat (* tartalék a megfordítható középső ajtóhoz) · C polctartó csap · "
       "F élfogantyú-előfurat · R rögzítőcsavar. Lapél-furatnál a „v” az elülső éltől mért távolság, a furat az él közepén (9 mm) van. "
       "A polc (880×559) és a hátfal furat nélküli.")


def single(code, title, fs=7):
    def bld(x):
        return [Table([[img(parts_doc[code]["img"], x), hole_table(parts_doc[code], fs)]],
                      colWidths=[(x + 4) * mm, 82 * mm], style=[("VALIGN", (0, 0), (-1, -1), "TOP")]),
                Spacer(1, 3), Paragraph(LEG, S["s"])]
    return fit_page(title, bld, FW / mm - 87, 60)


for code, title in (("A01", "A01 – bal és jobb oldallap (2 db)"), ("A02", "A02 – fenéklap"), ("A03", "A03 – tetőlap"),
                    ("A04", "A04 – 1. közfal"), ("A05", "A05 – 2. közfal"), ("A08", "A08 – bal ajtó, hátulról nézve"),
                    ("A09", "A09 – középső ajtó, hátulról nézve"), ("A10", "A10 – jobb ajtó, hátulról nézve")):
    story += single(code, "Alkatrészrajz " + title)

# ---- 10-12. fúrósablon 1:1
class Template(Flowable):
    def __init__(self, seg, idx, total):
        super().__init__(); self.seg, self.idx, self.total = seg, idx, total
        self.width, self.height = PAGE[0] - 34 * mm, 172 * mm

    def strip(self, c, y0, label, positions, zero_marks, s0, s1):
        x0 = 20 * mm
        X = lambda p: x0 + (p - s0) * mm
        c.setStrokeColor(colors.black); c.setLineWidth(0.6)
        c.rect(X(s0), y0, (s1 - s0) * mm, 30 * mm)
        c.setLineWidth(1.4); c.line(X(s0), y0, X(s1), y0)          # referencia él
        c.setFont("DV", 7); c.drawString(X(s0) + 1 * mm, y0 - 4 * mm, "◄ EZT AZ ÉLT A LAP SZÉLÉHEZ ILLESZD (felső / alsó él, vagy a lapél felülete)")
        c.setDash(2, 2); c.setLineWidth(0.4); c.line(X(s0), y0 + 9 * mm, X(s1), y0 + 9 * mm); c.setDash()
        c.setFont("DVB", 9); c.drawString(X(s0) + 1 * mm, y0 + 31.5 * mm, label)
        for zp, zl in zero_marks:
            if s0 <= zp <= s1:
                c.setLineWidth(1.2); c.setStrokeColor(colors.black); c.line(X(zp), y0, X(zp), y0 + 30 * mm)
                c.setFont("DVB", 7); c.drawString(X(zp) + 1 * mm, y0 + (25 if zp == 0 else 3) * mm, zl)
        for p, kind in positions:
            if not (s0 - 0.01 <= p <= s1 + 0.01):
                continue
            r = {"C": J["conf_face_d"], "D": J["dowel_d"], "S": 5}[kind] / 2 * mm
            col = {"C": RED, "D": BLUE, "S": ORANGE}[kind]
            c.setStrokeColor(col); c.setLineWidth(0.6)
            c.circle(X(p), y0 + 9 * mm, r)
            c.line(X(p) - 6 * mm, y0 + 9 * mm, X(p) + 6 * mm, y0 + 9 * mm)
            c.line(X(p), y0 + 2 * mm, X(p), y0 + 16 * mm)
            c.setFillColor(col); c.setFont("DV", 7)
            c.drawCentredString(X(p), y0 + 18 * mm, {"C": "konfirmát", "D": "tipli", "S": "polccsap Ø5"}[kind])
            c.drawCentredString(X(p), y0 + 21.5 * mm, f"{p:g}")
            c.setFillColor(colors.black)
        c.setStrokeColor(colors.black)
        # illesztő jelek
        for edge in (s0, s1):
            if (edge == s0 and self.idx > 0) or (edge == s1 and self.idx < self.total - 1):
                c.setFont("DV", 6.5)
                c.drawCentredString(X(edge), y0 - 8 * mm, "▲ illesztés")

    def draw(self):
        c = self.canv
        s0, s1 = self.seg
        c.setFont("DVB", 12)
        c.drawString(20 * mm, self.height - 2 * mm, f"Fúrósablon 1:1 – {self.idx+1}/{self.total}. lap  ({s0:g}–{s1:g} mm)")
        c.setFont("DV", 8)
        c.drawString(20 * mm, self.height - 7 * mm, "Nyomtatás: 100% / „Tényleges méret” – NE „Oldalhoz igazítva”. Ellenőrizd a lenti 100 mm-es vonalzót. "
                     "Vágd ki a csíkokat, és ragaszd össze a lapokat az illesztésnél.")
        dp = P["D"] - P["t_door"] - P["t_back"]
        jp = joint_positions(dp)
        A = [(p, "C") for p in jp["confirmat"]] + [(p, "D") for p in jp["dowel"]]
        B = [(v, "S") for v in PIN_Y]
        self.strip(c, 95 * mm, "A sablon – oldallap/tető/fenék kötés; a közfal kötéséhez a tető/fenék lapján a szaggatott vonalat a közfal középvonalára (800 / 1700 mm) illeszd",
                   A, [(0, "0 = ELÖL")], s0, s1)
        self.strip(c, 35 * mm, f"B sablon – polctartó csap (3 db) · az élt a ceruzavonalhoz illeszd: oldallapon {Z_PIN:g} mm, közfalon {Z_PIN - P['t']:g} mm a lap aljától",
                   B, [(0, "0 = ELÖL")], s0, s1)
        # 100 mm vonalzó
        c.setLineWidth(0.8); c.line(20 * mm, 15 * mm, 120 * mm, 15 * mm)
        for i in range(11):
            h = 3 * mm if i % 5 else 5 * mm
            c.line((20 + i * 10) * mm, 15 * mm, (20 + i * 10) * mm, 15 * mm + h)
        c.setFont("DV", 7); c.drawString(122 * mm, 14 * mm, "100 mm – ha nem pontosan ennyi, rossz a nyomtatási méretezés")



segs = [(0, 200), (190, 400), (390, 579)]
for i, sg in enumerate(segs):
    story.append(Template(sg, i, len(segs)))
    if i < len(segs) - 1:
        story.append(PageBreak())

doc = BaseDocTemplate(OUT, pagesize=PAGE, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=12 * mm, bottomMargin=14 * mm,
                      title="Rátétszekrény v10 – gyártási dokumentáció", author="Bolgár Milán + Claude")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=footer)])
doc.build(story)
print("ok", OUT)
