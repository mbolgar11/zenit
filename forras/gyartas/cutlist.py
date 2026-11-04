"""Szabásjegyzék, élzárás, vasalat és táblaszükséglet a geometry.py-ból."""
import sys, os, json
from collections import OrderedDict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry import PARAMS, parts

SHEET = (2800, 2070)      # Egger/Kronospan szabvány tábla 18 mm
KERF = 4                  # fűrészlap vastagság
TRIM = 10                 # táblaszél-levágás
DENSITY_18 = 650 * 0.018  # kg/m² forgácslap
DENSITY_HDF = 850 * 0.003

POS_NAMES = {"oldal": "Oldallap", "közfal": "Közfal", "fenék": "Fenéklap", "tető": "Tetőlap", "polc": "Polc",
             "ajtó": "Ajtó", "hátfal": "Hátfal"}


def edge_spec(q):
    """Élzárás a lapszabászati logika szerint: H1,H2 = hosszú élek, R1,R2 = rövid élek."""
    L, W = max(q["L"], q["Wd"]), min(q["L"], q["Wd"])
    L = int(L) if L == int(L) else L; W = int(W) if W == int(W) else W
    k = q["kind"]
    if k == "ajtó":
        return L, W, dict(H1="2 mm", H2="2 mm", R1="2 mm", R2="2 mm"), "körbe 2 mm ABS"
    if k == "hátfal":
        return L, W, {}, "nincs"
    if k in ("oldal", "közfal"):
        # oldallap: 579 mély x 520 magas -> az elülső él a 520-as (rövid) él
        front_len = q["L"]  # H
        if front_len == L:
            return L, W, dict(H1="0,4 mm"), f"1 hosszú él ({L}) 0,4 mm ABS – elülső él"
        return L, W, dict(R1="0,4 mm"), f"1 rövid él ({W}) 0,4 mm ABS – elülső él"
    # fenék, tető, polc: elülső él = a szélesség irányú (L) él
    if q["L"] == L:
        return L, W, dict(H1="0,4 mm"), f"1 hosszú él ({L}) 0,4 mm ABS – elülső él"
    return L, W, dict(R1="0,4 mm"), f"1 rövid él ({W}) 0,4 mm ABS – elülső él"


def grouped():
    rows = OrderedDict()
    for q in parts():
        L, W, e, etxt = edge_spec(q)
        L, W = round(L, 1), round(W, 1)
        L = int(L) if L == int(L) else L; W = int(W) if W == int(W) else W
        mat = "Laminált forgácslap 18 mm, fehér (OBI 4160321)" if q["material"] == "lap18" else "HDF 3 mm, fehér"
        key = (mat, POS_NAMES[q["kind"]], L, W, etxt)
        r = rows.setdefault(key, dict(anyag=mat, nev=POS_NAMES[q["kind"]], L=L, W=W, db=0,
                                       el=e, eltxt=etxt, modulok=[], kind=q["kind"]))
        r["db"] += 1
        r["modulok"].append(q["module"])
    out = list(rows.values())
    order = {"ajtó": 0, "oldal": 1, "közfal": 2, "fenék": 3, "tető": 4, "polc": 5, "hátfal": 6}
    out.sort(key=lambda r: (r["anyag"].startswith("HDF"), order[r["kind"]], -r["L"]))
    for i, r in enumerate(out, 1):
        r["poz"] = i
        r["terulet"] = r["L"] * r["W"] * r["db"] / 1e6
        el_m = 0
        for k, v in r["el"].items():
            el_m += (r["L"] if k.startswith("H") else r["W"])
        r["el_m_1"] = el_m / 1000 * r["db"] if any(v == "0,4 mm" for v in r["el"].values()) else 0
        r["el_m_2"] = el_m / 1000 * r["db"] if any(v == "2 mm" for v in r["el"].values()) else 0
    return out


def pack(rows):
    import rectpack
    rects = []
    for r in rows:
        if not r["anyag"].startswith("Laminált"):
            continue
        for n in range(r["db"]):
            rects.append((r["L"] + KERF, r["W"] + KERF, f'{r["poz"]}'))
    best = None
    for algo in (rectpack.MaxRectsBssf, rectpack.MaxRectsBaf, rectpack.GuillotineBssfSas,
                 rectpack.GuillotineBafSas, rectpack.SkylineBl):
        pk = rectpack.newPacker(rotation=True, pack_algo=algo)  # uni dekor: forgatható
        for w, h, rid in rects:
            pk.add_rect(w, h, rid)
        for _ in range(4):
            pk.add_bin(SHEET[0] - 2 * TRIM, SHEET[1] - 2 * TRIM)
        pk.pack()
        res = pk.rect_list()
        if len(res) != len(rects):
            continue
        nb = len({b for b, *_ in res})
        if best is None or nb < best[0]:
            best = (nb, res, algo.__name__)
    return best


def hardware(p=PARAMS):
    """v8 vasalat- és kötőelemlista a 3D modellből + vásárlási tartalék. 3 csavarfajta + hátfalszeg."""
    import math
    from geometry import hardware_counts, holes_and_hardware
    cnt = hardware_counts(p)
    holes, _ = holes_and_hardware(p)
    caps = sum(len(h["pts"]) for h in holes if h["kind"].startswith("konfirmát (") and h["part"] in ("K bal oldallap", "K jobb oldallap"))
    buy = lambda n, pack: int(math.ceil(n / pack) * pack)
    g = lambda pre: sum(v for k, v in cnt.items() if k.startswith(pre))
    n_hinge = g("pánt")
    n_handle = g("GTV HEXA")
    n_back = cnt["hátfalszeg 1,6×25"]
    s16 = 2 * n_hinge + 2 * n_hinge + 2 * n_handle
    return [
        ("Pánt: Häfele Metalla 300SM kombi 110°, RÁÜTŐDŐ, FÉKES (311.60.525)", g("pánt Häfele Metalla 300SM kombi 110° ráütődő, csill"), "db",
         "Bal és jobb ajtó FELSŐ pántja. Csésze Ø35×13, 21,5 mm-re a pántoldali éltől, 95,5 mm-re az ajtó tetejétől"),
        ("Pánt: Häfele Metalla 300SM kombi 110°, RÁÜTŐDŐ, rugós (311.60.620)", g("pánt Häfele Metalla 300SM kombi 110° ráütődő, sima"), "db",
         "Bal és jobb ajtó ALSÓ pántja, 95,5 mm-re az ajtó aljától"),
        ("Pánt: Häfele Metalla 300SM kombi 110°, FÉLIG RÁÜTŐDŐ, FÉKES (311.60.526)", g("pánt Häfele Metalla 300SM kombi 110° félig ráütődő, csill"), "db",
         "Középső ajtó FELSŐ pántja (a 2. közfalon)"),
        ("Pánt: Häfele Metalla 300SM kombi 110°, FÉLIG RÁÜTŐDŐ, rugós (311.60.621)", g("pánt Häfele Metalla 300SM kombi 110° félig ráütődő, sima"), "db",
         "Középső ajtó ALSÓ pántja"),
        ("Szerelőtalp: Häfele Metalla 300SM kombi D0 (311.71.540)", n_hinge, "db", "Mind a 6 pánthoz ugyanaz; 2 db 3,5×16 csavarral, Ø2,5×10 előfuratba"),
        ("Élfogantyú: GTV HEXA, alu elox, 192 mm furattáv / 225 mm hossz (UA-HEXA-192-05, butorkellek.hu 1342)", n_handle, "db",
         "Ajtónként 1 db az alsó él közepén, lekerekített profil; hátulról, az ajtó belső lapjába 2 db 3,5×16 csavarral, Ø2,5×12 előfurat, 192 mm-re egymástól, 10 mm-re az alsó éltől"),
        ("Polctartó csap Ø5, fém", cnt.get("polctartó csap Ø5", 0), "db", "A középső levehető polchoz, oldalanként 3 db (elöl, középen, hátul); szélső rekeszekbe későbbi polchoz +6-6 db"),
        ("1. csavar: konfirmát 7×50 + takarósapka", buy(cnt["konfirmát 7×50"] + 4, 10), "db",
         f"Modellben {cnt['konfirmát 7×50']} db (kötésenként 2); takarósapka {caps} db kell (a két külső oldallapra)"),
        ("Bükk fatipli 8×35 mm, hornyolt", buy(cnt["tipli 8×35"] + 4, 10), "db", f"Modellben {cnt['tipli 8×35']} db (kötésenként 2)"),
        ("2. csavar: forgácslapcsavar 3,5×16, süllyesztett, PZ2", buy(s16 + 10, 50), "db",
         f"Pántcsészék {2*n_hinge}, pánttalpak {2*n_hinge}, élfogantyúk {2*n_handle} = {s16} db"),
        ("3. csavar: forgácslapcsavar 3,5×30, süllyesztett, PZ2", buy(cnt["forgácslapcsavar 3,5×30"] + 2, 10), "db",
         f"Rögzítés az ELIA tetejéhez: {cnt['forgácslapcsavar 3,5×30']} db, a két szélső rekeszben 2-2 (az ELIA tetejét Ø2,5-tel előfúrni)"),
        ("Hátfalszeg 1,6×25, horganyzott (beütős)", buy(n_back + 15, 50), "db",
         f"Hátfal: {n_back} db, kb. 15 cm-enként körbe és a 4 függőleges elembe; előfúrás és jelölés nem kell, kalapáccsal beütni"),
    ]


def tools():
    return [
        ("Akkus fúró-csavarozó", "Mindenhez"),
        ("Konfirmát lépcsős fúrószár Ø5/Ø7", "Konfirmát furatok egy mozdulattal (~1500–2500 Ft)"),
        ("Ø8 mm fafúró + mélységütköző gyűrű", "Tiplifuratok: 12 mm (lapfelület) és 25 mm (lapél)"),
        ("Ø35 mm Forstner fúró", "Csak ha a lapszabászat nem fúrja ki a pántcsészéket"),
        ("Ø5 mm fafúró + mélységütköző (12 mm)", "Polctartó csapfuratok: oldallapon 12 mm mély, közfalon átmenő"),
        ("Ø2,5 mm fafúró", "Előfuratok: pánttalp, élfogantyú, ELIA teteje"),
        ("Mérőszalag, derékszög, ceruza, kinyomtatott fúrósablon", "A sablon 1:1-ben a dokumentáció végén"),
        ("Gumikalapács + kis kalapács", "Tiplis kötések összeütése; hátfalszegek"),
    ]


def weights(p=PARAMS):
    w = {}
    for q in parts():
        a = q["L"] * q["Wd"] / 1e6
        dens = DENSITY_18 if q["material"] == "lap18" else DENSITY_HDF
        d = w.setdefault(q["module"], dict(total=0, door=0))
        d["total"] += a * dens
        if q["kind"] == "ajtó":
            d["door"] += a * dens
    return {m: dict(total=round(v["total"], 1), door=round(v["door"], 1),
                    no_door=round(v["total"] - v["door"], 1)) for m, v in w.items()}


if __name__ == "__main__":
    rows = grouped()
    for r in rows:
        print(r["poz"], r["nev"], r["L"], "x", r["W"], r["db"], "db", r["eltxt"], r["modulok"])
    tot18 = sum(r["terulet"] for r in rows if r["anyag"].startswith("Lam"))
    print("18mm m2:", round(tot18, 2), " 1mm él m:", round(sum(r["el_m_1"] for r in rows), 2),
          " 2mm él m:", round(sum(r["el_m_2"] for r in rows), 2))
    nb, res, algo = pack(rows)
    print("táblák:", nb, algo)
    print(weights())
    json.dump(dict(rows=rows, sheets=nb, layout=res, algo=algo, weights=weights(),
                   hardware=hardware(), tools=tools(), params=PARAMS), open("cutlist.json", "w"),
              ensure_ascii=False, indent=1, default=str)
