import re
"""CadQuery – teljes gyártási modell (furatok, ABS él, vasalat) → STEP + GLB."""
import sys, os, math
import cadquery as cq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry import parts, base_cabinet, split_banding, holes_and_hardware

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
WITH_BASE = "--nobase" not in sys.argv
os.makedirs(OUT, exist_ok=True)
C = lambda r, g, b: cq.Color(r / 255, g / 255, b / 255)
COL = {"lap18": C(241, 240, 236), "door": C(244, 243, 239), "hdf3": C(232, 231, 226), "abs": C(236, 235, 230),
       "cashmere": C(201, 187, 170), "cashmere_body": C(205, 191, 175), "mirror": C(199, 211, 219),
       "alu": C(180, 182, 186), "beech": C(214, 178, 128), "zinc": C(196, 198, 204), "steel": C(150, 152, 158),
       "tipon": C(90, 90, 95)}


def box(b):
    x, y, z, dx, dy, dz = b
    return cq.Workplane("XY").box(dx, dy, dz, centered=False).translate((x, y, z))


def cyl(a, b, d):
    v = cq.Vector(*b) - cq.Vector(*a)
    return cq.Solid.makeCylinder(d / 2, v.Length, cq.Vector(*a), v.normalized())


def cone(a, b, d1, d2):
    v = cq.Vector(*b) - cq.Vector(*a)
    return cq.Solid.makeCone(d1 / 2, d2 / 2, v.Length, cq.Vector(*a), v.normalized())


def hole_tool(h, pt):
    n = cq.Vector(*h["normal"])
    a = cq.Vector(*pt) + n * 0.5
    b = cq.Vector(*pt) - n * h["depth"]
    tool = cyl(a.toTuple(), b.toTuple(), h["d"])
    if h.get("cs_d"):
        csl = (h["cs_d"] - h["d"]) / 2
        c2 = cq.Vector(*pt) - n * csl
        tool = tool.fuse(cone(cq.Vector(*pt).toTuple(), c2.toTuple(), h["cs_d"], h["d"]))
    return tool


def hw_solids(h):
    s = h["shape"]
    if s == "cyl":
        return cyl(h["p1"], h["p2"], h["d"])
    if s == "screw":
        a, b = h["p1"], h["p2"]
        L = math.dist(a, b); u = [(b[i] - a[i]) / L for i in range(3)]
        hb = tuple(a[i] + u[i] * h["head_l"] for i in range(3))
        return cone(a, hb, h["head_d"], h["d"]).fuse(cyl(hb, b, h["d"] * 0.85))
    if s == "hinge":
        cx, cy, cz = h["cup"]
        cup = cyl((cx, cy - 12.5, cz), (cx, cy + 0.5, cz), 35)
        xin, sg, yp = h["inner_x"], h["sgn"], h["y_plate"]
        ax0, ax1 = sorted((cx, xin + sg * 12))
        arm = box((ax0, cy, cz - 7, ax1 - ax0, yp + 22 - cy, 14)).val()
        plate = box((min(xin, xin + sg * 10), yp - 10, cz - 25, 10, 20, 50)).val()
        return cup.fuse(arm).fuse(plate)
    if s == "edgepull":
        cx, z, L, D, lip, t, yb = h["cx"], h["z"], h["L"], h["depth"], h["lip"], h["t"], h["y_back"]
        leg = box((cx - L / 2, yb - D, z - t, L, D, t)).val()
        lp = box((cx - L / 2, yb - D, z - t, L, t, lip)).val()
        return leg.fuse(lp)
    if s == "tipon":
        x, z, y0, L, d = h["x"], h["z"], h["y0"], h["L"], h["d"]
        house = cyl((x, y0 + 2, z - 3 - d / 2), (x, y0 + L, z - 3 - d / 2), d)
        plate = box((x - 12, y0 + 15, z - 3, 24, 60, 3)).val()
        return house.fuse(plate)


HWC = {"RIOS": "alu", "Viefe": "alu", "GTV HEXA": "alu", "tipli": "beech", "konfirmát": "zinc", "pánt": "steel", "TIP-ON": "tipon",
       "forgácslapcsavar": "zinc", "szekrényösszekötő": "steel", "hátfalcsavar": "zinc", "hátfalszeg": "zinc"}

holes, hw = holes_and_hardware()
by_part = {}
for h in holes:
    by_part.setdefault(h["part"], []).append(h)

assy = cq.Assembly(name="ratet_szekreny")
lap = cq.Assembly(name="ratet_lapok")
nh = 0
for q in parts():
    core, strips = split_banding(q)
    solid = box(core).val()
    tools = [hole_tool(h, pt) for h in by_part.get(q["name"], []) for pt in h["pts"]]
    if tools:
        comp = cq.Compound.makeCompound(tools)
        solid = solid.cut(comp)
        nh += len(tools)
    key = "door" if q["kind"] == "ajtó" else q["material"]
    sub = cq.Assembly(name=q["name"].replace(" ", "_"))
    sub.add(solid, name="mag", color=COL[key])
    for i, (sn, sb, th) in enumerate(strips):
        sub.add(box(sb).val(), name=f"abs{i}", color=COL["abs"])
    lap.add(sub)
assy.add(lap)

vas = cq.Assembly(name="vasalat")
groups = {}
for h in hw:
    groups.setdefault(h["kind"], []).append(h)
for kind, items in groups.items():
    ck = next((v for k, v in HWC.items() if kind.startswith(k)), "steel")
    comp = cq.Compound.makeCompound([hw_solids(h) for h in items])
    vas.add(comp, name=re.sub(r"[^0-9A-Za-z_]+","_",kind)[:60] + f"_{len(items)}db", color=COL[ck])
assy.add(vas)

if WITH_BASE:
    base = cq.Assembly(name="ELIA_D250")
    for b in base_cabinet():
        base.add(box(b["box"]), name=b["name"].replace(" ", "_"), color=COL[b["color"]])
    assy.add(base)

tag = "" if WITH_BASE else "_csak_ratet"
assy.export(os.path.join(OUT, f"ratet_szekreny_teljes{tag}.step"))
assy.export(os.path.join(OUT, f"ratet_szekreny_teljes{tag}.glb"), tolerance=0.3, angularTolerance=0.3)
print("furatok kivágva:", nh, "| vasalat:", len(hw))
