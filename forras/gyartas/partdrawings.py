"""Alkatrészrajzok + furattáblázat automatikusan a geometry.py furatlistájából."""
import os, sys, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry import PARAMS as P, parts, holes_and_hardware, banding

plt.rcParams["font.family"] = "DejaVu Sans"
OUT = "doc/img/parts"; os.makedirs(OUT, exist_ok=True)
LAP = "#F3F2EE"; EDGE = "#5E5850"; DIM = "#333333"
KCOL = {"pánttalp": "#2E8B57", "polctartó": "#C28A00", "élfogantyú": "#8A4FBF", "konfirmát": "#B5462F", "tipli": "#2F6DB5", "pánt": "#2E8B57", "TIP-ON": "#8A4FBF",
        "modulösszekötő": "#C28A00", "rögzítő": "#555555", "hátfal": "#777777"}
SHORT = {"konfirmát (oldallap, átmenő, süllyesztett)": "K", "konfirmát előfurat (lapél)": "K",
         "tipli (oldallap)": "T", "tipli (lapél)": "T", "pántcsésze Ø35": "P", "pánttalp (euro csavar)": "PT",
         "TIP-ON adapterlap": "TO", "modulösszekötő": "Ö", "rögzítőcsavar a szekrényhez (süllyesztett)": "R",
         "hátfal csavar": "H", "konfirmát (tetőlap, átmenő, süllyesztett)": "K", "konfirmát (fenéklap alulról, átmenő, süllyesztett)": "K", "konfirmát (közfal, átmenő, süllyesztett)": "K", "tipli (tetőlap alsó lapja)": "T", "tipli (fenéklap felső lapja)": "T", "tipli (közfal)": "T", "polctartó / pánttalp furat (System 32)": "S", "polctartó / pánttalp furat (System 32, átmenő)": "S", "élfogantyú csavar előfurat": "F", "pánttalp előfurat (3,5×16 csavar)": "PT", "polctartó csap furat": "C", "polctartó csap furat (átmenő)": "C", "pánttalp – tartalék (megfordítható ajtó)": "PT*", "TIP-ON adapterlap – tartalék (megfordítható ajtó)": "TO*"}


def kcol(kind):
    for k, v in KCOL.items():
        if kind.startswith(k) or k in kind:
            return v
    return "#000"


def face_label(q, n):
    k = q["kind"]
    if k == "oldal":
        x0 = q["box"][0]
        side_left = q["name"].split()[1] == "bal"
        outward = -1 if side_left else 1
        return "külső lap" if n[0] == outward else "belső lap"
    if k == "közfal":
        if n[0] == -1: return "bal lap"
        if n[0] == 1: return "jobb lap"
        return "felső él" if n[2] == 1 else "alsó él"
    if k in ("fenék", "tető", "polc"):
        if n[0] == -1: return "bal él"
        if n[0] == 1: return "jobb él"
        return "felső lap" if n[2] == 1 else "alsó lap"
    if k == "ajtó":
        return "belső (hátsó) lap"
    if k == "hátfal":
        return "hátsó lap"
    return "?"


def local(q, pt):
    """Lokális 2D koordináta a rajz síkjában (mm), és a rajz tengelyneve."""
    x, y, z, dx, dy, dz = q["box"]
    k = q["kind"]
    if k in ("oldal", "közfal"):
        return (pt[1] - y, pt[2] - z)          # u = elölről, v = alulról
    if k in ("fenék", "tető", "polc"):
        return (pt[0] - x, pt[1] - y)          # u = balról, v = elölről
    return (x + dx - pt[0], pt[2] - z)         # ajtó, hátfal: hátulról nézve (a fúrt oldal), u = balról


def part_view(q):
    x, y, z, dx, dy, dz = q["box"]
    k = q["kind"]
    if k == "közfal": return dy, dz, "u = az elülső (élzárt) éltől, v = az alsó éltől", "nézet: bal lap felől, az élzárt elülső él balra"
    if k == "oldal": return dy, dz, "u = az elülső (élzárt) éltől, v = az alsó éltől", "nézet: belső lap, az élzárt elülső él balra"
    if k in ("fenék", "tető", "polc"): return dx, dy, "balról mért (u) × elölről mért (v)", "nézet: felülről"
    if k == "ajtó": return dx, dz, "u = balról, v = alulról", "nézet: HÁTULRÓL, a fúrt belső lap"
    return dx, dz, "u = balról, v = alulról", "nézet: HÁTULRÓL, a fúrt lap"


def table_rows(q, hl):
    rows = []
    for h in hl:
        for pt in h["pts"]:
            u, v = local(q, pt)
            rows.append(dict(jel=SHORT.get(h["kind"], "?"), kind=h["kind"], d=h["d"], depth=h["depth"],
                             cs=h.get("cs_d"), face=face_label(q, h["normal"]), u=round(u, 1), v=round(v, 1),
                             normal=h["normal"]))
    rows.sort(key=lambda r: (r["face"], r["jel"], r["v"], r["u"]))
    return rows


def draw(q, rows, fname, title):
    W, Hh, axes_txt, view_txt = part_view(q)
    k = q["kind"]
    nl = len({(r["jel"], r["kind"]) for r in rows})
    sf = max(1.0, (W + 260) / 1100.0)
    fig = plt.figure(figsize=(9 * min(sf, 1.6), 9 * min(sf, 1.6) * (Hh + sf * (200 + 24 * nl)) / (W + 260)))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_aspect("equal"); ax.axis("off")
    nleg = len({(r["jel"], r["kind"]) for r in rows})
    ax.set_xlim(-150 * sf, W + 110 * sf); ax.set_ylim(sf * (-80 - 24 * nleg), Hh + 120 * sf)
    ax.add_patch(Rectangle((0, 0), W, Hh, fc=LAP if k != "hátfal" else "#F5F4F0", ec=EDGE, lw=1.2))
    # élzárás jelölése
    for d_, th in banding(q):
        lw = 4 if th >= 2 else 2.5
        if k in ("oldal", "közfal") and d_ == "-y": ax.plot([0, 0], [0, Hh], lw=lw, color="#8E8A84", solid_capstyle="butt")
        if k in ("fenék", "tető", "polc") and d_ == "-y": ax.plot([0, W], [0, 0], lw=lw, color="#8E8A84", solid_capstyle="butt")
        if k == "ajtó":
            ax.add_patch(Rectangle((0, 0), W, Hh, fc="none", ec="#8E8A84", lw=lw))
    for r in rows:
        u, v, c = r["u"], r["v"], kcol(r["kind"])
        if r["face"] in ("felső él", "alsó él"):
            L = r["depth"]
            y0_ = Hh - L if r["face"] == "felső él" else 0
            ax.add_patch(Rectangle((u - r["d"] / 2, y0_), r["d"], L, fc=c, ec=c, alpha=0.75, lw=0.5))
        elif r["face"] in ("bal él", "jobb él"):
            L = r["depth"]
            x0 = 0 if r["face"] == "bal él" else W - L
            ax.add_patch(Rectangle((x0, v - r["d"] / 2), L, r["d"], fc=c, ec=c, alpha=0.75, lw=0.5))
        else:
            dashed = r["face"] in ("külső lap", "alsó lap", "jobb lap")
            ax.add_patch(Circle((u, v), max(r["d"] / 2, 2.2), fc="white" if dashed else c, ec=c, lw=1.0,
                                ls="--" if dashed else "-", alpha=0.95))
    # befoglaló méretek
    ax.annotate("", (0, Hh + 40 * sf), (W, Hh + 40 * sf), arrowprops=dict(arrowstyle="<->", lw=0.7, color=DIM))
    ax.text(W / 2, Hh + 48 * sf, f"{W:g}", ha="center", fontsize=9)
    ax.annotate("", (-45 * sf, 0), (-45 * sf, Hh), arrowprops=dict(arrowstyle="<->", lw=0.7, color=DIM))
    ax.text(-55 * sf, Hh / 2, f"{Hh:g}", ha="right", va="center", fontsize=9, rotation=90)
    ax.plot([0], [0], marker="o", color="k", ms=4); ax.text(-8, -22, "0,0", fontsize=7, ha="right")
    ax.text(0, Hh + 95 * sf, title, fontsize=12, weight="bold")
    ax.text(0, Hh + 75 * sf, view_txt + " · koordináták: " + axes_txt, fontsize=7.5, color="#444")
    lg = sorted({(r["jel"], r["kind"]) for r in rows})
    for i, (j, kd) in enumerate(lg):
        ax.text(0, sf * (-55 - i * 24), f"■ {j} = {kd}", fontsize=7.5, color=kcol(kd))
    if k in ("oldal", "közfal", "fenék", "tető", "polc"):
        ax.text(W, -55 * sf, "szaggatott kör = a túloldali lapról fúrva", fontsize=7, ha="right", color="#666")
    fig.savefig(f"{OUT}/{fname}.png", dpi=200); plt.close(fig)


def main():
    holes, _ = holes_and_hardware()
    byp = {}
    for h in holes:
        byp.setdefault(h["part"], []).append(h)
    groups = {}
    for q in parts():
        rows = table_rows(q, byp.get(q["name"], []))
        sig = (q["kind"], round(q["L"], 1), round(q["Wd"], 1),
               tuple((r["jel"], r["face"], r["d"], r["depth"], r["u"], r["v"]) for r in rows))
        g = groups.setdefault(sig, dict(names=[], q=q, rows=rows))
        g["names"].append(q["name"])
    out = []
    for i, (sig, g) in enumerate(groups.items(), 1):
        q = g["q"]
        code = f"A{i:02d}"
        nm = q['name'].split(' ', 1)[1]
        title = f"{code} · {nm[0].upper() + nm[1:]} ({len(g['names'])} db)" if len(g['names']) == 1 else f"{code} · {', '.join(n.split(' ', 1)[1] for n in g['names'])} ({len(g['names'])} db)"
        draw(q, g["rows"], code, title)
        out.append(dict(code=code, names=g["names"], kind=q["kind"], L=q["L"], W=q["Wd"],
                        material=q["material"], rows=g["rows"], title=title, img=f"{OUT}/{code}.png"))
    json.dump(out, open("doc/parts.json", "w"), ensure_ascii=False, indent=1)
    print(len(out), "egyedi alkatrész-rajz;", sum(len(o["rows"]) for o in out), "sor a furattáblákban")


if __name__ == "__main__":
    main()
