import json, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.comments import Comment

d = json.load(open("cutlist.json"))
rows, P = d["rows"], d["params"]
out = sys.argv[1]

F = "Arial"
H = Font(name=F, bold=True, color="FFFFFF")
B = Font(name=F, bold=True)
N = Font(name=F)
BLUE = Font(name=F, color="0000FF")
HF = PatternFill("solid", fgColor="6B5E50")
SUB = PatternFill("solid", fgColor="EFE9E2")
thin = Side(style="thin", color="BFB5AA")
BR = Border(left=thin, right=thin, top=thin, bottom=thin)
C = Alignment(horizontal="center", vertical="center", wrap_text=True)
LW = Alignment(horizontal="left", vertical="center", wrap_text=True)

wb = Workbook()
ws = wb.active
ws.title = "Szabásjegyzék"
ws["A1"] = "Rátétszekrény ELIA D 250 tetejére – szabásjegyzék"
ws["A1"].font = Font(name=F, bold=True, size=14)
ws["A2"] = ("Minden méret KÉSZMÉRET mm-ben, élzárással együtt. Dekor: fehér (OBI 4160321), uni (nincs szálirány, a lapok forgathatók). "
            f"v8 (végleges): EGY korpusz, 2 közfallal, élfogantyúval; ajtók 2 mm, minden más 0,4 mm ABS; ajtóosztás {' + '.join(str(w) for w in P['module_widths'])} = {sum(P['module_widths'])} mm, magasság {P['H']} mm, mélység {P['D']} mm.")
ws["A2"].font = N
ws.merge_cells("A2:P2"); ws["A2"].alignment = LW; ws.row_dimensions[2].height = 32

hdr = ["Poz.", "Megnevezés", "Anyag", "Hossz (mm)", "Szélesség (mm)", "Vast. (mm)", "Db",
       "Élzárás H1", "Élzárás H2", "Élzárás R1", "Élzárás R2", "Modul", "Terület (m²)",
       "Él 0,4 mm (fm)", "Él 2 mm (fm)", "Megjegyzés"]
R0 = 4
for c, h in enumerate(hdr, 1):
    x = ws.cell(R0, c, h); x.font = H; x.fill = HF; x.alignment = C; x.border = BR
from geometry import PARAMS as _P
_zh = (_P["gap_v"] + 95.5, _P["H"] - _P["gap_v"] - 95.5)
_w = json.load(open("cutlist.json"))["weights"]["K"]["no_door"]
notes = {
    "Ajtó": "Pántcsésze furat Ø35×13 mm, a pántoldali élétől 21,5 mm-re (csészeközép), az ajtó aljától és tetejétől 95,5 mm-re",
    "Oldallap": f"A {_P['H']}-as él az elülső (látszó) él",
    "Polc": "Levehető polc, 6 db Ø5 polctartó csapon (oldalanként 3); 20 mm-rel hátrébb az ajtótól; furat nincs benne",
    "Hátfal": "Rátétesen a korpusz hátára, beütős hátfalszeggel (előfúrás nem kell)",
}
r = R0
for q in rows:
    r += 1
    thick = 18 if q["anyag"].startswith("Lam") else 3
    e = q["el"]
    vals = [q["poz"], q["nev"], q["anyag"], q["L"], q["W"], thick, q["db"],
            e.get("H1", ""), e.get("H2", ""), e.get("R1", ""), e.get("R2", ""),
            ", ".join(sorted(set(q["modulok"])))]
    for c, v in enumerate(vals, 1):
        x = ws.cell(r, c, v); x.font = N; x.border = BR
        x.alignment = C if c != 2 and c != 3 else LW
    ws.cell(r, 13, f"=D{r}*E{r}*G{r}/1000000")
    ws.cell(r, 14, f'=((H{r}="0,4 mm")*D{r}+(I{r}="0,4 mm")*D{r}+(J{r}="0,4 mm")*E{r}+(K{r}="0,4 mm")*E{r})*G{r}/1000')
    ws.cell(r, 15, f'=((H{r}="2 mm")*D{r}+(I{r}="2 mm")*D{r}+(J{r}="2 mm")*E{r}+(K{r}="2 mm")*E{r})*G{r}/1000')
    ws.cell(r, 16, notes.get(q["nev"], ""))
    for c in (13, 14, 15):
        ws.cell(r, c).number_format = "0.00"; ws.cell(r, c).font = N; ws.cell(r, c).border = BR
        ws.cell(r, c).alignment = C
    ws.cell(r, 16).font = N; ws.cell(r, 16).border = BR; ws.cell(r, 16).alignment = LW
last = r
r += 1
ws.cell(r, 2, "Összesen").font = B
ws.cell(r, 7, f"=SUM(G{R0+1}:G{last})").font = B
for c in (13, 14, 15):
    col = get_column_letter(c)
    x = ws.cell(r, c, f"=SUM({col}{R0+1}:{col}{last})"); x.font = B; x.number_format = "0.00"; x.alignment = C
for c in range(1, 17):
    ws.cell(r, c).fill = SUB; ws.cell(r, c).border = BR
ws.cell(R0, 8).comment = Comment("H1, H2 = a két hosszú él; R1, R2 = a két rövid él. Üres = nincs élzárás.", "Claude")
widths = [6, 14, 30, 11, 13, 9, 6, 11, 11, 11, 11, 12, 12, 12, 12, 58]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.freeze_panes = ws.cell(R0 + 1, 1)
TOT = r

# --- Összesítő
s = wb.create_sheet("Összesítő")
s["A1"] = "Anyagszükséglet és rendelési összesítő"; s["A1"].font = Font(name=F, bold=True, size=14)
SZ = "Szabásjegyzék"
items = [
    ("Tábla hossza (mm)", 2800, "Szabvány Egger/Kronospan tábla – ellenőrizd a boltban", True),
    ("Tábla szélessége (mm)", 2070, "", True),
    ("Ráhagyás a vágásra és hulladékra", 0.15, "Becslés", True),
    ("18 mm fehér lap – nettó (m²)", f"=SUMIFS({SZ}!M{R0+1}:M{last},{SZ}!F{R0+1}:F{last},18)", "", False),
    ("18 mm fehér lap – bruttó (m²)", "=B6*(1+B5)", "", False),
    ("Egy tábla területe (m²)", "=B3*B4/1000000", "", False),
    ("Szükséges 18 mm tábla (db, felfelé kerekítve)", "=ROUNDUP(B7/B8,0)",
     f"A szabásterv-optimalizáló szerint: {d['sheets']} tábla", False),
    ("3 mm HDF hátfal (m²)", f"=SUMIFS({SZ}!M{R0+1}:M{last},{SZ}!F{R0+1}:F{last},3)", "1 tábla bőven elég", False),
    ("Élzáró 0,4 mm ABS, fehér (fm)", f"={SZ}!N{TOT}", "Korpusz elülső élek és polc", False),
    ("Élzáró 2 mm ABS, fehér (fm) – ajtók", f"={SZ}!O{TOT}", "", False),
    ("Alkatrészek száma (db)", f"={SZ}!G{TOT}", "", False),
]
s["A2"] = "Kék = bemenő adat, átírható"; s["A2"].font = Font(name=F, italic=True, color="0000FF")
for i, (k, v, note, inp) in enumerate(items, 3):
    s.cell(i, 1, k).font = N
    x = s.cell(i, 2, v); x.font = BLUE if inp else N
    x.number_format = "0%" if "Ráhagyás" in k else ("0.00" if isinstance(v, str) else "0")
    s.cell(i, 3, note).font = Font(name=F, italic=True, color="666666")
s["B9"].font = B
w = d["weights"]
s["A16"] = "Tömeg (becslés, 650 kg/m³ forgácslap)"; s["A16"].font = B
for i, (m, v) in enumerate(w.items(), 17):
    s.cell(i, 1, "Korpusz (egyben)" if m == "K" else m).font = N
    s.cell(i, 2, f"{v['total']} kg összesen").font = N
    s.cell(i, 3, f"{v['no_door']} kg ajtó nélkül – így emeld fel").font = N
s.column_dimensions["A"].width = 46; s.column_dimensions["B"].width = 18; s.column_dimensions["C"].width = 50

# --- Vasalat
v = wb.create_sheet("Vasalat")
v["A1"] = "Vasalat- és kellékjegyzék"; v["A1"].font = Font(name=F, bold=True, size=14)
for c, h in enumerate(["Tétel", "Mennyiség", "Egység", "Hova / megjegyzés"], 1):
    x = v.cell(3, c, h); x.font = H; x.fill = HF; x.alignment = C; x.border = BR
for i, (name, qty, unit, note) in enumerate(d["hardware"], 4):
    for c, val in enumerate([name, qty, unit, note], 1):
        x = v.cell(i, c, val); x.font = N; x.border = BR; x.alignment = LW if c in (1, 4) else C
v.column_dimensions["A"].width = 70; v.column_dimensions["B"].width = 11
v.column_dimensions["C"].width = 8; v.column_dimensions["D"].width = 70

# --- Rendelés
o = wb.create_sheet("Rendelési tudnivalók")
lines = [
    "Rendelés a lapszabászaton / OBI-ban",
    "1. Anyag: OBI fehér laminált forgácslap 18 mm, 280×207 (cikkszám 4160321), 2 tábla – áruházban rendelhető.",
    "2. A méretek készméretek, ABS élzárással együtt. Mondd ki: „a méretek élzárással együtt értendők”.",
    "3. Élzárás: ajtók körbe 2 mm ABS; oldallapok, közfalak, tető, fenék, polc: csak az elülső él 0,4 mm ABS (H1/H2/R1/R2 oszlop).",
    "4. FIGYELEM: a tető- és fenéklap 2464 mm hosszú – személyautóba nem fér be, kérj szállítást (vagy furgont).",
    "5. Pántcsésze-fúrás az ajtókon: Ø35 × 13 mm, csészeközép 21,5 mm-re a pántoldali éltől, 95,5 mm-re az ajtó aljától és tetejétől. Pántoldal: bal ajtó bal, középső ajtó jobb, jobb ajtó jobb.",
    "6. Ha vállalják a konfirmát-, tipli-, csap- és előfuratokat is: add oda az A-rajzokat és a „Furatok” lapot.",
    f"7. Hátfal: 1 db 3 mm HDF, 2498 × {_P['H'] - 2} mm.",
    "",
    "Szerelés röviden (v8)",
    "a) A korpuszt a FÖLDÖN szereld össze (a tetőlapon felülről kell konfirmátot hajtani, a plafon alatt erre nincs hely).",
    "b) Fenéklapra a tiplik → oldallapok és közfalak rá → konfirmátok alulról a fenéklapon át, oldalról az oldallapokon át. Polc a középső rekeszbe.",
    "c) Tetőlap rá a tiplikre → konfirmátok felülről a közfalakba, oldalról az oldallapokba.",
    "d) Hátfal felszegelése (beütős hátfalszeg 1,6×25, kb. 15 cm-enként, előfúrás nélkül) – derékszögbe állítja a korpuszt (átlók egyenlők!).",
    f"e) Pánttalpak az előfuratokba ({_zh[0]:g} és {_zh[1]:g} mm magasan, felül fékes, alul rugós pánt), élfogantyúk az ajtók alsó élére; ajtók NÉLKÜL emeljétek fel: kb. {_w} kg, 2,5 m – 3 ember.",
    "f) Rögzítés: 4 db 3,5×30 csavar a két szélső rekeszben a fenéklapon át (az ELIA tetejét Ø2,5-tel előfúrni). Ajtók felakasztása (CLIP), hézag: 3 mm az ajtók között, 1,5 mm oldalt, 4,5 mm fent/lent.",
]
for i, t in enumerate(lines, 1):
    x = o.cell(i, 1, t); x.alignment = LW
    x.font = Font(name=F, bold=True, size=13) if t and not t[0].isdigit() and not t.startswith(tuple("abcdef")) else N
o.column_dimensions["A"].width = 130


# --- Furatok (a 3D modellből)
import os
if os.path.exists("doc/parts.json"):
    pj = json.load(open("doc/parts.json"))
    f = wb.create_sheet("Furatok", 1)
    f["A1"] = "Furattáblázat – alkatrészenként (a Fusion / CadQuery modellből generálva)"
    f["A1"].font = Font(name=F, bold=True, size=14)
    f["A2"] = ("u, v = a rajz szerinti koordináta mm-ben (lásd a PDF alkatrészrajzát). Oldallap: u az élzárt elülső éltől, v az alsó éltől. "
               "Fenék/tető/polc: u balról, v elölről (felülnézet). Ajtó, hátfal: hátulról nézve, u balról, v alulról. "
               "Lapél-furat: u = 0, v = távolság az elülső éltől, az él közepén (9 mm).")
    f["A2"].font = N; f.merge_cells("A2:K2"); f["A2"].alignment = LW; f.row_dimensions[2].height = 45
    hdr = ["Rajzszám", "Alkatrész(ek)", "Jel", "Furat", "Felület", "u (mm)", "v (mm)", "Ø (mm)", "Mélység (mm)", "Süllyesztés Ø", "Db alkatrész"]
    for c, h in enumerate(hdr, 1):
        x = f.cell(4, c, h); x.font = H; x.fill = HF; x.alignment = C; x.border = BR
    r = 4
    for part in pj:
        for row in part["rows"]:
            r += 1
            u = 0 if row["face"] in ("bal él", "jobb él") else row["u"]
            vals = [part["code"], ", ".join(part["names"]), row["jel"], row["kind"], row["face"], u, row["v"],
                    row["d"], row["depth"], row["cs"] or "", len(part["names"])]
            for c, v in enumerate(vals, 1):
                x = f.cell(r, c, v); x.font = N; x.border = BR; x.alignment = LW if c in (2, 4) else C
    r += 2
    f.cell(r, 1, "Furatok összesen (alkatrész-darabszámmal szorozva):").font = B
    f.cell(r, 9, f"=SUM(K5:K{r-2})").font = B
    for i, w in enumerate([10, 34, 6, 40, 14, 9, 9, 8, 12, 12, 12], 1):
        f.column_dimensions[get_column_letter(i)].width = w
    f.freeze_panes = "A5"
wb.save(out)
print("saved+furatok", out)
