"""Műszaki rajzok PNG-ben (matplotlib) a PDF dokumentációhoz."""
import json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry import PARAMS as P, parts, joint_positions, JOINT as J

plt.rcParams["font.family"] = "DejaVu Sans"
OUT = "doc/img"; os.makedirs(OUT, exist_ok=True)
LAP = "#F3F2EE"; EDGE = "#5E5850"; DIM = "#333333"; HOLE_C = "#B5462F"; HOLE_D = "#2F6DB5"


def dim(ax, x1, y1, x2, y2, txt, off=0, vertical=False, fs=8, ext=True):
    if vertical:
        xx = x1 + off
        if ext:
            ax.plot([x1, xx], [y1, y1], lw=0.4, color=DIM); ax.plot([x2, xx], [y2, y2], lw=0.4, color=DIM)
        ax.annotate("", (xx, y1), (xx, y2), arrowprops=dict(arrowstyle="<->", lw=0.6, color=DIM, shrinkA=0, shrinkB=0))
        ax.text(xx - 8 * (1 if off < 0 else -1) * 0 + (6 if off >= 0 else -6), (y1 + y2) / 2, txt, rotation=90,
                ha="left" if off >= 0 else "right", va="center", fontsize=fs, color=DIM)
    else:
        yy = y1 + off
        if ext:
            ax.plot([x1, x1], [y1, yy], lw=0.4, color=DIM); ax.plot([x2, x2], [y2, yy], lw=0.4, color=DIM)
        ax.annotate("", (x1, yy), (x2, yy), arrowprops=dict(arrowstyle="<->", lw=0.6, color=DIM, shrinkA=0, shrinkB=0))
        ax.text((x1 + x2) / 2, yy + (6 if off >= 0 else -6), txt, ha="center",
                va="bottom" if off >= 0 else "top", fontsize=fs, color=DIM)


def setup(w, h, figw=11.0):
    fig = plt.figure(figsize=(figw, figw * h / w))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def save(fig, name):
    fig.savefig(f"{OUT}/{name}.png", dpi=220); plt.close(fig)


# 1) Elölnézet + oldalnézet
def elevation():
    W = sum(P["module_widths"]); H = P["H"]; BH = P["base_H"]; C = P["ceiling"]
    fig, ax = setup(4050, 3050)
    ax.set_xlim(-350, 3700); ax.set_ylim(-250, 2800)
    # alsó szekrény
    ax.add_patch(Rectangle((0, 0), W, BH, fc="#F3EFEA", ec=EDGE, lw=0.8, hatch="", ls="--"))
    ax.text(W / 2, BH / 2, "Meglévő ELIA D 250\n2500 × 2050 × 600", ha="center", va="center", fontsize=10, color="#777")
    x = 0
    for i, w in enumerate(P["module_widths"]):
        ax.add_patch(Rectangle((x, BH), w, H, fc=LAP, ec=EDGE, lw=1.0))
        ax.add_patch(Rectangle((x + P["gap"] + 1, BH + 3), w - 6, H - 6, fc="none", ec=EDGE, lw=0.4))
        ax.text(x + w / 2, BH + H / 2, f"M{i+1}", ha="center", va="center", fontsize=12, color=EDGE, weight="bold")
        dim(ax, x, BH + H, x + w, BH + H, f"{w}", off=90)
        x += w
    ax.plot([-200, W + 200], [C, C], ls="-.", lw=0.8, color="#888")
    ax.text(-200, C + 20, "plafon (legalacsonyabb pont) 2590", fontsize=8, color="#666")
    ax.plot([-250, W + 250], [0, 0], lw=1.2, color="#444")
    dim(ax, W, BH, W, BH + H, f"{H}", off=90, vertical=True)
    dim(ax, W, BH + H, W, C, f"{C - BH - H} rés", off=90, vertical=True)
    dim(ax, W, 0, W, BH, f"{BH}", off=90, vertical=True)
    dim(ax, 0, 0, W, 0, f"{W}", off=-130)
    ax.text(0, -230, "ELÖLNÉZET (méretek mm-ben)", fontsize=10, weight="bold")
    # oldalnézet / metszet
    ox = 2850; D = P["D"]; s = 1
    ax.add_patch(Rectangle((ox, 0), D * s, BH, fc="#F3EFEA", ec=EDGE, lw=0.8, ls="--"))
    t, td, tb = P["t"], P["t_door"], P["t_back"]
    ax.add_patch(Rectangle((ox, BH + P["gap_v"]), td, H - 2 * P["gap_v"], fc="#E4E2DD", ec=EDGE, lw=0.6))  # ajtó
    ax.add_patch(Rectangle((ox + td, BH), D - td - tb, t, fc=LAP, ec=EDGE, lw=0.6))
    ax.add_patch(Rectangle((ox + td, BH + H - t), D - td - tb, t, fc=LAP, ec=EDGE, lw=0.6))
    ax.add_patch(Rectangle((ox + D - tb, BH + 1), tb, H - 2, fc="#FFF", ec=EDGE, lw=0.6))
    ax.plot([ox - 50, ox + D + 50], [C, C], ls="-.", lw=0.8, color="#888")
    ax.plot([ox + D + 60] * 2, [0, C + 50], lw=2, color="#999")
    ax.text(ox + D + 80, 1200, "fal", rotation=90, fontsize=8, color="#777")
    dim(ax, ox, BH + H, ox + D, BH + H, f"{D}", off=90)
    dim(ax, ox, BH, ox + td, BH, f"{td}", off=-70, fs=7)
    ax.text(ox, -230, "OLDALNÉZET", fontsize=10, weight="bold")
    save(fig, "elevation")


# 2) Alkatrész-rajzok furatokkal
def part_side(name, with_shelf):
    H = P["H"]; t = P["t"]; dp = P["D"] - P["t_door"] - P["t_back"]
    fig, ax = setup(1000, 800, 8)
    ax.set_xlim(-180, 820); ax.set_ylim(-170, 630)
    ax.add_patch(Rectangle((0, 0), dp, H, fc=LAP, ec=EDGE, lw=1))
    ax.plot([0, 0], [0, H], lw=4, color="#8E8A84", solid_capstyle="butt")  # élzárt elülső él
    ax.text(-12, H / 2, "ELÖL (élzárt, 1 mm)", rotation=90, ha="right", va="center", fontsize=8, color=EDGE)
    rows = [("fenék", t / 2, 0, dp), ("tető", H - t / 2, 0, dp)]
    if with_shelf:
        ih = H - 2 * t; zc = t + (ih - t) / 2 + t / 2
        rows.append(("polc", zc, P["shelf_setback"], dp - P["shelf_setback"]))
    for lbl, z, yo, depth in rows:
        jp = joint_positions(depth)
        for y in jp["confirmat"]:
            ax.add_patch(Circle((yo + y, z), 7, fc="white", ec=HOLE_C, lw=1.2))
        for y in jp["dowel"]:
            ax.add_patch(Circle((yo + y, z), 5, fc=HOLE_D, ec=HOLE_D, lw=0.8))
    # méretezés (fenék sor)
    jp = joint_positions(dp)
    ys = sorted(jp["confirmat"] + jp["dowel"])
    prev = 0
    for y in ys:
        dim(ax, prev, 0, y, 0, f"{y - prev:g}", off=-45 if prev == 0 else -45, fs=7)
        prev = y
    dim(ax, 0, 0, dp, 0, f"{dp}", off=-110)
    dim(ax, dp, 0, dp, H, f"{H}", off=60, vertical=True)
    dim(ax, dp, H - t / 2, dp, H, f"{t/2:g}", off=25, vertical=True, fs=7)
    dim(ax, dp, 0, dp, t / 2, f"{t/2:g}", off=25, vertical=True, fs=7)
    if with_shelf:
        ih = H - 2 * t; zc = t + (ih - t) / 2 + t / 2
        dim(ax, dp, 0, dp, zc, f"{zc:g}", off=110, vertical=True, fs=7)
        ax.add_patch(Rectangle((P["shelf_setback"], zc - t / 2), dp - P["shelf_setback"], t, fc="none", ec="#999", ls=":", lw=0.8))
    # pánttalp furatok (csak a pántoldali oldallapon)
    for zh in (P["gap"] + J["hinge_from_door_edge"], H - P["gap"] - J["hinge_from_door_edge"]):
        for dz in (-16, 16):
            ax.add_patch(Circle((J["hinge_plate_from_front"], zh + dz), 3, fc="#555", ec="#555"))
    ax.text(J["hinge_plate_from_front"] + 14, P["gap"] + J["hinge_from_door_edge"], "pánttalp\n(csak pántoldalon)",
            fontsize=7, va="center", color="#555")
    ax.text(0, 600, name, fontsize=11, weight="bold")
    ax.text(0, 575, "belső oldal nézete · ○ konfirmát Ø7 átmenő (süllyesztve kívül) · ● tipli Ø8, 12 mm mély · ▪ pánttalp Ø3 előfúrás",
            fontsize=7.5, color="#444")
    save(fig, name.split()[0].lower())


def part_panel(name, L, Wd, holes_depth, fname):
    fig, ax = setup(1100, 860, 8)
    ax.set_xlim(-120, 980); ax.set_ylim(-120, 740)
    ax.add_patch(Rectangle((0, 0), L, Wd, fc=LAP, ec=EDGE, lw=1))
    ax.plot([0, L], [0, 0], lw=4, color="#8E8A84", solid_capstyle="butt")
    ax.text(L / 2, 12, "ELÖL (élzárt, 1 mm)", ha="center", fontsize=8, color=EDGE)
    jp = joint_positions(holes_depth)
    for xe in (0, L):
        for y in jp["confirmat"]:
            ax.add_patch(Rectangle((xe - 50 if xe else 0, y - 2.5), 50, 5, fc="none", ec=HOLE_C, lw=0.8))
        for y in jp["dowel"]:
            ax.add_patch(Rectangle((xe - 25 if xe else 0, y - 4), 25, 8, fc=HOLE_D, ec=HOLE_D, lw=0.6))
    prev = 0
    for y in sorted(jp["confirmat"] + jp["dowel"]):
        dim(ax, L, prev, L, y, f"{y - prev:g}", off=40, vertical=True, fs=7)
        prev = y
    dim(ax, 0, Wd, L, Wd, f"{L}", off=40)
    dim(ax, 0, 0, 0, Wd, f"{Wd}", off=-60, vertical=True)
    ax.text(0, 712, name, fontsize=11, weight="bold")
    ax.text(0, 688, "felülnézet · a két rövid élbe (oldalak felé): konfirmát Ø5 × 50 mm, tipli Ø8 × 25 mm, mindkettő az él közepén (9 mm)",
            fontsize=7.5, color="#444")
    save(fig, fname)


def part_door(name, L, Wd, hinge, fname):
    fig, ax = setup(1100, 780, 8)
    ax.set_xlim(-120, 980); ax.set_ylim(-120, 660)
    ax.add_patch(Rectangle((0, 0), L, Wd, fc="#D9CDBF", ec=EDGE, lw=2.2))
    cx = J["cup_center_from_edge"] if hinge == "L" else L - J["cup_center_from_edge"]
    for z in (J["hinge_from_door_edge"], Wd - J["hinge_from_door_edge"]):
        ax.add_patch(Circle((cx, z), J["cup_d"] / 2, fc="white", ec=HOLE_C, lw=1.2))
    tip_x = L - 40 if hinge == "L" else 40
    ax.add_patch(Rectangle((tip_x - 15, Wd - 40), 30, 25, fc="none", ec="#555", ls="--"))
    ax.text(tip_x, Wd - 55, "TIP-ON ütköző\nhelye", ha="center", va="top", fontsize=7, color="#555")
    dim(ax, 0, Wd, L, Wd, f"{L:g}", off=40)
    dim(ax, 0, 0, 0, Wd, f"{Wd:g}", off=-60, vertical=True)
    xe = 0 if hinge == "L" else L
    dim(ax, xe, 0, cx, 0, f"{J['cup_center_from_edge']}", off=-40, fs=7)
    dim(ax, L if hinge == "L" else 0, 0, L if hinge == "L" else 0, J["hinge_from_door_edge"],
        f"{J['hinge_from_door_edge']}", off=40 if hinge == "L" else -40, vertical=True, fs=7)
    ax.text(0, 632, name, fontsize=11, weight="bold")
    ax.text(0, 608, f"belső oldal nézete · pántoldal: {'BAL' if hinge == 'L' else 'JOBB'} · pántcsésze Ø35 × 13 mm · körbe 2 mm ABS élzárás",
            fontsize=7.5, color="#444")
    save(fig, fname)


# 3) Szabásterv
def sheets(layout, rows):
    names = {str(r["poz"]): f'{r["poz"]}. {r["nev"]}' for r in rows}
    bins = sorted({b for b, *_ in layout})
    for b in bins:
        fig, ax = setup(3000, 2300, 10)
        ax.set_xlim(-100, 2900); ax.set_ylim(-150, 2150)
        ax.add_patch(Rectangle((0, 0), 2800, 2070, fc="#F7F4F0", ec="#444", lw=1))
        for bb, x, y, w, h, rid in layout:
            if bb != b:
                continue
            ax.add_patch(Rectangle((x + 10, y + 10), w - 4, h - 4, fc=LAP, ec=EDGE, lw=0.8))
            ax.text(x + 10 + w / 2, y + 10 + h / 2, f"{names[rid]}\n{int(max(w, h) - 4)} × {int(min(w, h) - 4)}",
                    ha="center", va="center", fontsize=8)
        ax.text(0, -100, f"{b+1}. tábla – 2800 × 2070 × 18 mm, kasmír · fűrészlap 4 mm, szélezés 10 mm", fontsize=10, weight="bold")
        save(fig, f"sheet{b+1}")


def elevation_v3():
    from geometry import layout, parts as P3
    W = sum(P["module_widths"]); H = P["H"]; BH = P["base_H"]; C = P["ceiling"]; t = P["t"]
    fig, ax = setup(4050, 3050)
    ax.set_xlim(-350, 3700); ax.set_ylim(-250, 2800)
    ax.add_patch(Rectangle((0, 0), W, BH, fc="#F3EFEA", ec=EDGE, lw=0.8, ls="--"))
    ax.text(W / 2, BH / 2, "Meglévő ELIA D 250\n2500 × 2050 × 600", ha="center", va="center", fontsize=10, color="#777")
    ax.add_patch(Rectangle((0, BH), W, H, fc=LAP, ec=EDGE, lw=1.0))
    for x in layout()[1:-1]:
        ax.add_patch(Rectangle((x, BH + t), t, H - 2 * t, fc="none", ec=EDGE, lw=0.6, ls=":"))
    for q in P3():
        if q["kind"] == "ajtó":
            x, y, z, dx, dy, dz = q["box"]
            ax.add_patch(Rectangle((x, BH + z), dx, dz, fc="none", ec=EDGE, lw=0.5))
            ax.text(x + dx / 2, BH + H / 2, f"{dx:g}", ha="center", va="center", fontsize=9, color=EDGE)
    acc = 0
    for w in P["module_widths"]:
        dim(ax, acc, BH + H, acc + w, BH + H, f"{w}", off=90); acc += w
    ax.plot([-200, W + 200], [C, C], ls="-.", lw=0.8, color="#888")
    ax.text(-200, C + 20, "plafon (legalacsonyabb pont) 2590", fontsize=8, color="#666")
    ax.plot([-250, W + 250], [0, 0], lw=1.2, color="#444")
    dim(ax, W, BH, W, BH + H, f"{H}", off=90, vertical=True)
    dim(ax, W, BH + H, W, C, f"{C - BH - H} rés", off=90, vertical=True)
    dim(ax, W, 0, W, BH, f"{BH}", off=90, vertical=True)
    dim(ax, 0, 0, W, 0, f"{W}", off=-130)
    ax.text(0, -230, "ELÖLNÉZET (méretek mm-ben) – pontozott: közfalak, a számok az ajtószélességek", fontsize=10, weight="bold")
    ox = 2850; D = P["D"]; td, tb = P["t_door"], P["t_back"]
    ax.add_patch(Rectangle((ox, 0), D, BH, fc="#F3EFEA", ec=EDGE, lw=0.8, ls="--"))
    ax.add_patch(Rectangle((ox, BH + P["gap_v"]), td, H - 2 * P["gap_v"], fc="#E4E2DD", ec=EDGE, lw=0.6))
    ax.add_patch(Rectangle((ox + td, BH), D - td - tb, t, fc=LAP, ec=EDGE, lw=0.6))
    ax.add_patch(Rectangle((ox + td, BH + H - t), D - td - tb, t, fc=LAP, ec=EDGE, lw=0.6))
    ax.add_patch(Rectangle((ox + D - tb, BH + 1), tb, H - 2, fc="#FFF", ec=EDGE, lw=0.6))
    ax.plot([ox - 50, ox + D + 50], [C, C], ls="-.", lw=0.8, color="#888")
    dim(ax, ox, BH + H, ox + D, BH + H, f"{D}", off=90)
    ax.text(ox, -230, "OLDALNÉZET", fontsize=10, weight="bold")
    save(fig, "elevation")


if __name__ == "__main__":
    d = json.load(open("cutlist.json"))
    elevation_v3()
    sheets(d["layout"], d["rows"])
    print(sorted(os.listdir(OUT)))
