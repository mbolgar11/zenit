"""v3 előzetes költségkalkuláció (Excel, képletekkel)."""
import json, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

d = json.load(open("cutlist.json"))
rows = d["rows"]
m2 = sum(r["terulet"] for r in rows if r["anyag"].startswith("Lam"))
e1 = sum(r["el_m_1"] for r in rows); e2 = sum(r["el_m_2"] for r in rows)
hw = {h[0]: h[1] for h in d["hardware"]}
def hwq(prefix):
    return next(v for k, v in hw.items() if k.startswith(prefix))

F = "Arial"; N = Font(name=F); B = Font(name=F, bold=True); BLUE = Font(name=F, color="0000FF")
H = Font(name=F, bold=True, color="FFFFFF"); HF = PatternFill("solid", fgColor="6B5E50")
SUB = PatternFill("solid", fgColor="EFE9E2"); YEL = PatternFill("solid", fgColor="FFF2CC")
thin = Side(style="thin", color="BFB5AA"); BR = Border(left=thin, right=thin, top=thin, bottom=thin)
LW = Alignment(horizontal="left", vertical="center", wrap_text=True); C = Alignment(horizontal="center", vertical="center", wrap_text=True)

S = {  # források
    "metalla": "https://butoralkatreszkft.hu/239-metalla-kivetopantok.html",
    "obi_lap": "https://www.obi.hu/search/lamin%C3%A1lt%20forg%C3%A1cslap%20feh%C3%A9r/",
    "obi_szabas": "https://www.obi.hu/aruhaz/services/lapszabaszat",
    "lapszabo": "https://www.lapszabo.hu/butorlap/egger/U702-ST9-kasmir-szurke",
    "fabuli": "https://fabuli.hu/butorlap-egger-uni-u702-st9-kasmir-szurke-2800x2070x18mm-7640",
    "fatelep": "https://www.fatelep.hu/adatlap/hdf-butor-hatlap-3x2800x2070-mm--festett-feher-/",
    "bszb": "https://butorszerelvenybolt.com/tablas-hatfallemez-kasta-hdf-feher-2800x2070x3-mm-raktarkeszletes",
    "lsz": "https://lapszabaszat.hu/munkadij/",
    "cegled": "https://butorlapszabascegled.hu/arlista/",
    "pant": "https://butorkellek.eu/blum-70t3550-clip-top-110-rautodo-kivetopant-rugo-nelkul-9302",
    "pant95": "https://szerelvenyek.indafabutorhaz.hu/termek/blum-clip-top-butorpant-110-95mm-hajlitott-rugo-nelkul-csavaros/",
    "pantb": "https://www.butor-vasalat.hu/clip-top-110-os-rautodo-beepitett-fekes-kivetopant",
    "szinkron": "https://szinkron.hu/butorvasalat/pantok/ob0169-kivetopant-felig-rautodo-pant-kompl-fekes-klippes-entry",
    "vasalatshop": "https://www.vasalatshop.eu/gtv-csillapitos-razarodo-kivetopant-5147",
    "hexa": "https://www.butorkellek.hu/index.php?kod=7709&modul=termek",
}

items = [
    ("Lapanyag", "OBI laminált forgácslap fehér 18 mm, 280×207 (4160321) – 4 699 Ft/m²", d["sheets"], "tábla", 27236, 38248,
     f"Nettó szükséglet {m2:.2f} m² → {d['sheets']} tábla. Min: 4 699 Ft/m² × 5,796 m²; max: a másik fehér 18 mm-es OBI-lap 6 599 Ft/m². Online nem rendelhető, áruházi átvétel", "obi_lap"),
    ("Lapanyag", "HDF hátfal 3 mm fehér, 2800×2070", 1, "tábla", 5696, 10764, "Az obi.hu HDF-oldala nem volt elérhető – más boltok ára", "fatelep / bszb"),
    ("Megmunkálás", "OBI szabás (méretre vágás)", 30, "vágás", 0, 300,
     "Az obi.hu nem közöl árat, és nem írja, hogy ingyenes; egy 2025-ös vásárlói válasz szerint „nem ingyen”. Kb. 30 vágás. Áruházban kérdezd meg!", "obi_szabas (becslés)"),
    ("Megmunkálás", "OBI élzárás ABS 0,4 mm (korpusz elülső élek, polc)", round(e1, 2), "fm", 350, 600,
     "Ár nincs online – piaci árszint (lapszabaszat.hu: 350 Ft/fm)", "obi_szabas (becslés)"),
    ("Megmunkálás", "OBI élzárás ABS 2 mm (ajtók körbe)", round(e2, 2), "fm", 650, 1000, "Ár nincs online – piaci árszint (lapszabaszat.hu: 650 Ft/fm)", "obi_szabas (becslés)"),
    ("Megmunkálás", "OBI pántfúrás Ø35 (ajtók)", 6, "db", 300, 600, "Az OBI kínál pántfuratfúrást; ár nincs online", "obi_szabas (becslés)"),
    ("Vasalat", "Häfele Metalla 300SM kombi ráütődő, fékes 110° (311.60.525)", 2, "db", 659, 750, "Bal és jobb ajtó felső pántja", "metalla"),
    ("Vasalat", "Häfele Metalla 300SM kombi ráütődő, rugós 110° (311.60.620)", 2, "db", 519, 600, "Bal és jobb ajtó alsó pántja", "metalla"),
    ("Vasalat", "Häfele Metalla 300SM kombi félig ráütődő, fékes 110° (311.60.526)", 1, "db", 663, 750, "Középső ajtó felső pántja", "metalla"),
    ("Vasalat", "Häfele Metalla 300SM kombi félig ráütődő, rugós 110° (311.60.621)", 1, "db", 528, 600, "Középső ajtó alsó pántja", "metalla"),
    ("Vasalat", "Häfele Metalla 300SM kombi szerelőtalp D0 (311.71.540)", 6, "db", 109, 130, "Mind a 6 pánthoz ugyanaz a talp", "metalla"),
    ("Vasalat", "Polctartó csap Ø5 fém (a középső polchoz, oldalanként 3)", 6, "db", 20, 60, "Becslés; a szélső rekeszekbe későbbi polchoz +6-6 db", "becslés"),
    ("Vasalat", "GTV HEXA élfogantyú, alu, 192/225 mm (UA-HEXA-192-05, „Fogantyú 1342”)", 3, "db", 805, 805, "butorkellek.hu, 2026. 11. 04.: 805 Ft/db, raktáron", "hexa"),
    ("Kötőelem", "Konfirmát 7×50 (1. csavarfajta)", 20, "db", 20, 45, "Modellben 16 db + tartalék", "becslés"),
    ("Kötőelem", "Konfirmát takarósapka", 20, "db", 10, 25, "Becslés", "becslés"),
    ("Kötőelem", "Bükk tipli 8×35", 20, "db", 6, 15, "Modellben 16 db + tartalék", "becslés"),
    ("Kötőelem", "Forgácslapcsavar 3,5×16, süllyesztett, PZ2 (2. csavarfajta)", 50, "db", 4, 10,
     "Pántcsészék (12), pánttalpak (12), élfogantyúk (6) = 30 db + tartalék", "becslés"),
    ("Kötőelem", "Hátfalszeg 1,6×25, horganyzott (beütős)", 100, "db", 3, 8, "Hátfal: 50 db + tartalék; előfúrás nem kell", "becslés"),
    ("Kötőelem", "Forgácslapcsavar 3,5×30, süllyesztett, PZ2 (3. csavarfajta)", 10, "db", 6, 15, "Rögzítés az ELIA tetejéhez: 4 db + tartalék", "becslés"),
    ("Szállítás", "OBI fuvar (2464 mm-es lapok – autóba nem fér)", 1, "alkalom", 5990, 15000, "Az OBI fuvardíja 5 990 Ft-tól (terméklap szerint), a végleges összeg a távolságtól függ", "obi_lap"),
]

wb = Workbook(); ws = wb.active; ws.title = "Kalkuláció"
ws["A1"] = "Rátétszekrény v10 – OBI fehér lap, ABS 0,4 mm + ajtók 2 mm, Häfele Metalla pántok, 3 csavarfajta + hátfalszeg, OBI szabással és élzárással – előzetes kalkuláció"; ws["A1"].font = Font(name=F, bold=True, size=14)
ws["A2"] = ("Bruttó árak Ft-ban, 2026. november 3-i webes árak alapján. Kék = egységár (átírható), sárga = becslés, "
            "ahol nem találtam konkrét árat. A végleges árat a kiválasztott lapszabászat árajánlata adja.")
ws["A2"].font = N; ws.merge_cells("A2:I2"); ws["A2"].alignment = LW; ws.row_dimensions[2].height = 32
hdr = ["Csoport", "Tétel", "Menny.", "Egység", "Egységár min", "Egységár max", "Összeg min", "Összeg max", "Megjegyzés / forrás"]
R0 = 4
for c, h in enumerate(hdr, 1):
    x = ws.cell(R0, c, h); x.font = H; x.fill = HF; x.alignment = C; x.border = BR
r = R0
for grp, name, q, unit, lo, hi, note, src in items:
    r += 1
    vals = [grp, name, q, unit, lo, hi, f"=C{r}*E{r}", f"=C{r}*F{r}", f"{note} [{src}]" if note else f"[{src}]"]
    for c, v in enumerate(vals, 1):
        x = ws.cell(r, c, v); x.border = BR
        x.font = BLUE if c in (5, 6) else N
        x.alignment = LW if c in (1, 2, 9) else C
        if c in (5, 6, 7, 8): x.number_format = '#,##0 "Ft"'
    if "becslés" in src:
        for c in (5, 6): ws.cell(r, c).fill = YEL
last = r
r += 1
ws.cell(r, 2, "Összesen (bruttó)").font = B
for c, col in ((7, "G"), (8, "H")):
    x = ws.cell(r, c, f"=SUM({col}{R0+1}:{col}{last})"); x.font = B; x.number_format = '#,##0 "Ft"'; x.alignment = C
for c in range(1, 10): ws.cell(r, c).fill = SUB; ws.cell(r, c).border = BR
TOT = r
r += 1
ws.cell(r, 2, "Várható érték (a két határ átlaga)").font = B
x = ws.cell(r, 7, f"=ROUND(AVERAGE(G{TOT},H{TOT}),-3)"); x.font = B; x.number_format = '#,##0 "Ft"'; x.alignment = C
r += 2
ws.cell(r, 2, "Opcionális szerszámok (ha nincs otthon)").font = B
r += 1
for name, lo, hi in (("Konfirmát lépcsős fúrószár Ø5/Ø7", 1500, 2500), ("Ø8 fafúró + mélységütköző", 1000, 2000)):
    ws.cell(r, 2, name).font = N
    for c, v in ((5, lo), (6, hi)):
        x = ws.cell(r, c, v); x.font = BLUE; x.number_format = '#,##0 "Ft"'; x.fill = YEL
    r += 1
r += 1
ws.cell(r, 2, "Csoportösszesítő").font = B
r += 1
for g in ("Lapanyag", "Megmunkálás", "Vasalat", "Kötőelem", "Szállítás"):
    ws.cell(r, 2, g).font = N
    for c, col in ((7, "G"), (8, "H")):
        x = ws.cell(r, c, f'=SUMIF($A${R0+1}:$A${last},"{g}",{col}{R0+1}:{col}{last})'); x.font = N; x.number_format = '#,##0 "Ft"'
    r += 1
for i, w in enumerate([13, 52, 9, 8, 13, 13, 14, 14, 70], 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.freeze_panes = ws.cell(R0 + 1, 1)

s2 = wb.create_sheet("Források")
s2["A1"] = "Források (2026. 11. 03.)"; s2["A1"].font = Font(name=F, bold=True, size=13)
for i, (k, u) in enumerate(S.items(), 3):
    s2.cell(i, 1, k).font = B; s2.cell(i, 2, u).font = N
s2.column_dimensions["A"].width = 12; s2.column_dimensions["B"].width = 110
wb.save(sys.argv[1]); print("ok")
