"""ZENIT – 3 éves pénzügyi modell (2027–2029), negyedéves bontás, három forgatókönyv. Minden összeg ezer Ft-ban (eFt), nettó (ÁFA nélkül)."""
import json
EUR = 390  # Ft/€ – tervezési árfolyam
Q = [f"{y} Q{q}" for y in (2027, 2028, 2029) for q in (1, 2, 3, 4)]
# darabszám csatornánként, alap forgatókönyv
UNITS = {
  "HU közvetlen (D2C)":        [10, 25, 38, 52,   60, 72, 80, 88,   95, 110, 120, 130],
  "Belsőépítészek, fejlesztők": [0, 2, 6, 10,     15, 20, 25, 30,   35, 40, 45, 50],
  "CEE közvetlen (AT·SK·CZ)":  [0, 0, 0, 0,       8, 20, 32, 45,    60, 72, 82, 90],
  "DACH·IT partnerek":         [0, 0, 0, 0,       0, 0, 8, 15,      40, 70, 100, 130],
}
# nettó egységár (eFt) és közvetlen költség (gyártás + vasalat + szállítás + szerelés + díjak), eFt/db
PRICE = {"HU közvetlen (D2C)": 265, "Belsőépítészek, fejlesztők": 225, "CEE közvetlen (AT·SK·CZ)": round(1150 * EUR / 1000), "DACH·IT partnerek": round(1000 * EUR / 1000)}
COGS = {"HU közvetlen (D2C)": 140, "Belsőépítészek, fejlesztők": 130, "CEE közvetlen (AT·SK·CZ)": 205, "DACH·IT partnerek": 195}
# működési költség negyedévente (eFt)
OPEX = {
  "Csapat (bér + járulék)":            [1500, 2600, 4200, 4200,  7800, 7800, 9800, 9800,   13500, 13500, 15500, 15500],
  "Marketing és hirdetés":             [1500, 2500, 3000, 3000,  5000, 6000, 7000, 7000,   11000, 12000, 13000, 14000],
  "Kiállítás, design hét, pop-up":     [600, 4500, 500, 2200,    1500, 6500, 1000, 4500,   2500, 14000, 2000, 6000],
  "Bemutatóterem, minták":             [2500, 1200, 1200, 1200,  1800, 1800, 2400, 2400,   3600, 3600, 3600, 3600],
  "Szoftver, web, tervező":            [900, 600, 450, 450,      900, 900, 900, 900,       1500, 1500, 1500, 1500],
  "Jog, könyvelés, védjegy, biztosítás": [1600, 500, 450, 450,   900, 600, 600, 600,       1200, 900, 900, 900],
  "Egyéb, utazás, tartalék":           [500, 500, 600, 600,      900, 900, 1100, 1100,     1600, 1600, 1600, 1600],
}
CAPEX = [3000, 1000, 0, 0,  2500, 0, 2000, 0,  6000, 2000, 0, 0]   # minták, bemutató sarkok, szerszámok, szerelőautó (Y3: saját CNC-cella előleg)
SCEN = {"Óvatos": 0.6, "Alap": 1.0, "Optimista": 1.4}

def run(k):
    rows = []; cash = 0; first_pos = None
    for i, q in enumerate(Q):
        u = {c: round(v[i] * k) for c, v in UNITS.items()}
        rev = sum(u[c] * PRICE[c] for c in u); cogs = sum(u[c] * COGS[c] for c in u)
        # óvatos forgatókönyv: karcsúbb működés (lassabb felvétel, kevesebb hirdetés és kiállítás)
        sc = {"Csapat (bér + járulék)": 0.72, "Marketing és hirdetés": 0.7, "Kiállítás, design hét, pop-up": 0.55, "Bemutatóterem, minták": 0.8} if k < 1 else {}
        opex = sum(v[i] * sc.get(n, 1) for n, v in OPEX.items())
        ebitda = rev - cogs - opex; cash += ebitda - CAPEX[i]
        if ebitda > 0 and first_pos is None: first_pos = q
        rows.append(dict(q=q, units=sum(u.values()), u=u, rev=rev, cogs=cogs, gm=rev - cogs, opex=round(opex), ebitda=round(ebitda), cash=round(cash)))
    return rows, first_pos

out = {}
for name, k in SCEN.items():
    rows, fp = run(k)
    yrs = {}
    for y in (2027, 2028, 2029):
        r = [x for x in rows if x["q"].startswith(str(y))]
        yrs[y] = {key: sum(x[key] for x in r) for key in ("units", "rev", "cogs", "gm", "opex", "ebitda")}
        yrs[y]["cash_end"] = r[-1]["cash"]
    out[name] = dict(rows=rows, years=yrs, first_profitable_q=fp, min_cash=min(x["cash"] for x in rows),
                     min_cash_q=min(rows, key=lambda x: x["cash"])["q"], payback_q=next((x["q"] for x in rows if x["cash"] > 0 and rows.index(x) > 2), None))
json.dump(dict(Q=Q, UNITS=UNITS, PRICE=PRICE, COGS=COGS, OPEX=OPEX, CAPEX=CAPEX, EUR=EUR, out=out), open(__file__.replace(".py", ".json"), "w"), ensure_ascii=False, indent=1)
for n, o in out.items():
    print(n, "| 1. negyedév pozitív EBITDA:", o["first_profitable_q"], "| legmélyebb pénzállás:", o["min_cash"], o["min_cash_q"], "| kumulált megtérülés:", o["payback_q"])
    for y, v in o["years"].items(): print("  ", y, {k: (round(v[k] / 1000, 1) if k != "units" else v[k]) for k in v}, "(M Ft)")
