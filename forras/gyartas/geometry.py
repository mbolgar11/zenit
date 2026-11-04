"""Rátétszekrény v10 (v9 + GTV HEXA 192 élfogantyú, hátulról csavarozva) – v9 (v8 + Viefe CURVE lekerekített élfogantyú) – v8 (v7 + 3 polctartó csap oldalanként, beütős szeges hátfal előfurat nélkül) – v7 (v6 + Häfele Metalla 300SM pántok, egységes csavarok: 7×50, 3,5×16, 3,5×30) – v5 (egy korpusz, 2 közfal, csak pánttalp- és középső polctartó-furatok, élfogantyú, csillapított pánt) – egyetlen igazságforrás a geometriához.

Koordináták (mm):  X = szélesség (balról jobbra), Y = mélység (elöl 0 -> hátul),
Z = magasság (0 = az ELIA szekrény teteje).
Minden elem tengelyirányú téglatest: (x0, y0, z0, dx, dy, dz).
Tiszta Python, nincs függősége – a Fusion 360 script is ezt a logikát használja.
"""

PARAMS = {
    "variant": "v7",
    "shelf_clear": 1.0,                 # levehető polc: oldalanként 1 mm játék
    "gap_v": 4.5,                       # ajtó alatt/felett: hely az élfogantyú 1,5 mm-es talpának
    "module_widths": [800, 900, 800],  # AJTÓOSZTÁS (a közfalak közepe 800 és 1700 mm-nél)
    "H": 530, "D": 600, "t": 18, "t_door": 18, "t_back": 3, "gap": 1.5,
    "shelf_modules": [1], "shelf_setback": 20,
    "hinge_side": ["L", "R", "R"],     # bal ajtó: bal oldallapon; középső: 2. közfalon; jobb: jobb oldallapon
    "base_W": 2500, "base_H": 2050, "base_D": 600, "ceiling": 2590,
}


def layout(p=PARAMS):
    """Függőleges elemek x-helyzete: oldalak és közfalak (bal él x)."""
    t = p["t"]; W = sum(p["module_widths"])
    xs = [0.0]
    acc = 0.0
    for w in p["module_widths"][:-1]:
        acc += w
        xs.append(acc - t / 2)          # közfal középre a két ajtó illesztése alá
    xs.append(W - t)
    return xs                            # [bal oldal, 1. közfal, 2. közfal, jobb oldal]


def compartments(p=PARAMS):
    t = p["t"]; xs = layout(p)
    return [(xs[i] + t, xs[i + 1]) for i in range(len(xs) - 1)]


def parts(p=PARAMS):
    t, tb, H, D, g, td = p["t"], p["t_back"], p["H"], p["D"], p["gap"], p["t_door"]
    y_c = td; dp = D - td - tb; W = sum(p["module_widths"])
    xs = layout(p)
    out = []
    def add(name, kind, mat, box, L, Wd, **kw):
        out.append(dict(name=name, module="K", kind=kind, material=mat, box=box, L=L, Wd=Wd, **kw))
    add("K bal oldallap", "oldal", "lap18", (0, y_c, 0, t, dp, H), H, dp)
    add("K jobb oldallap", "oldal", "lap18", (W - t, y_c, 0, t, dp, H), H, dp)
    add("K fenéklap", "fenék", "lap18", (t, y_c, 0, W - 2 * t, dp, t), W - 2 * t, dp)
    add("K tetőlap", "tető", "lap18", (t, y_c, H - t, W - 2 * t, dp, t), W - 2 * t, dp)
    for i, x in enumerate(xs[1:-1], 1):
        add(f"K {i}. közfal", "közfal", "lap18", (x, y_c, t, t, dp, H - 2 * t), H - 2 * t, dp)
    comps = compartments(p)
    for ci in p["shelf_modules"]:
        x0, x1 = comps[ci]
        ih = H - 2 * t; z = t + (ih - t) / 2
        c_ = p["shelf_clear"]
        add("K polc", "polc", "lap18", (x0 + c_, y_c + p["shelf_setback"], z, x1 - x0 - 2 * c_, dp - p["shelf_setback"], t),
            x1 - x0 - 2 * c_, dp - p["shelf_setback"])
    add("K hátfal", "hátfal", "hdf3", (1, D - tb, 1, W - 2, tb, H - 2), W - 2, H - 2)
    names = ["bal", "középső", "jobb"] if len(p["module_widths"]) == 3 else [str(i + 1) for i in range(len(p["module_widths"]))]
    acc = 0.0
    for i, w in enumerate(p["module_widths"]):
        gv = p["gap_v"]
        add(f"K {names[i]} ajtó", "ajtó", "lap18", (acc + g, 0, gv, w - 2 * g, td, H - 2 * gv), w - 2 * g, H - 2 * gv,
            hinge=p["hinge_side"][i])
        acc += w
    return out


JOINT = {
    # a tető/fenék/polc és az oldallap kötése, a lap elejétől mérve (mm)
    "confirmat": [50, -50],          # v4: kötésenként 2 konfirmát + 2 tipli (negatív = hátulról mérve)
    "dowel": [170, -170],
    "dowel_d": 8, "dowel_len": 35, "dowel_face_depth": 12, "dowel_edge_depth": 25,
    "conf_face_d": 7, "conf_edge_d": 5, "conf_edge_depth": 50,
    "hinge_from_door_edge": 100, "hinge_plate_from_front": 37,
    "cup_d": 35, "cup_depth": 13, "cup_center_from_edge": 21.5,
}


def joint_positions(depth, j=JOINT):
    """Konfirmát és tipli pozíciók egy adott mélységű lap elejétől mérve."""
    def res(v):
        return depth / 2 if v is None else (depth + v if v < 0 else v)
    return dict(confirmat=[res(v) for v in j["confirmat"]], dowel=[res(v) for v in j["dowel"]])


# ---------------------------------------------------------------------------
# ÉLZÁRÁS (ABS) – a méretek készméretek, a lapmag ennyivel kisebb
# ---------------------------------------------------------------------------
ABS_THIN, ABS_THICK = 0.4, 2.0          # v7: ajtók körbe 2 mm ABS, minden más 0,4 mm ABS (OBI gépi élzárás)


def banding(q):
    """Élzárt élek: list of (irány, vastagság). Irány: '-y' = elülső él, '+x','-x','+z','-z'."""
    if q["kind"] == "ajtó":
        return [("-x", ABS_THICK), ("+x", ABS_THICK), ("-z", ABS_THICK), ("+z", ABS_THICK)]
    if q["kind"] in ("oldal", "közfal", "fenék", "tető", "polc"):
        return [("-y", ABS_THIN)]
    return []


def split_banding(q):
    """Lapmag + ABS csíkok tengelyirányú dobozai. Visszaad: (mag_box, [(név, box, vastagság)])."""
    x, y, z, dx, dy, dz = q["box"]
    strips = []
    b = dict(banding(q))
    cx0, cy0, cz0, cx1, cy1, cz1 = x, y, z, x + dx, y + dy, z + dz
    if "-x" in b: cx0 += b["-x"]
    if "+x" in b: cx1 -= b["+x"]
    if "-y" in b: cy0 += b["-y"]
    if "-z" in b: cz0 += b["-z"]
    if "+z" in b: cz1 -= b["+z"]
    core = (cx0, cy0, cz0, cx1 - cx0, cy1 - cy0, cz1 - cz0)
    if "-x" in b: strips.append(("ABS bal él", (x, y, z, b["-x"], dy, dz), b["-x"]))
    if "+x" in b: strips.append(("ABS jobb él", (x + dx - b["+x"], y, z, b["+x"], dy, dz), b["+x"]))
    if "-z" in b: strips.append(("ABS alsó él", (cx0, y, z, cx1 - cx0, dy, b["-z"]), b["-z"]))
    if "+z" in b: strips.append(("ABS felső él", (cx0, y, z + dz - b["+z"], cx1 - cx0, dy, b["+z"]), b["+z"]))
    if "-y" in b: strips.append(("ABS elülső él", (x, y, z, dx, b["-y"], dz), b["-y"]))
    return core, strips


# ---------------------------------------------------------------------------
# FURATOK ÉS VASALAT
# ---------------------------------------------------------------------------
HW = {
    "confirmat": dict(d_face=7.0, cs_d=10.5, d_edge=5.0, depth_edge=50.0, L=50.0),
    "dowel": dict(d=8.0, L=35.0, depth_face=12.0, depth_edge=25.0),
    "hinge": dict(cup_d=35.0, cup_depth=13.0, cup_from_edge=21.5, from_door_edge=95.5,
                  plate_from_front=37.0, plate_hole_d=5.0, plate_hole_depth=13.0, plate_pitch=32.0),
    "tipon": dict(hole_d=2.5, hole_depth=10.0, L=76.0, d=15.0),
    "connector": dict(d=5.0, positions_y=(90.0, 490.0), positions_z=(120.0, 400.0)),
    "mount": dict(d=4.0, cs_d=8.0, L=30.0, inset_side=40.0, from_front=80.0, from_back=80.0),
    "grid": dict(d=5.0, depth_side=12.0, from_front=37.0, from_back=37.0, z0=84.0, pitch=32.0, n=12),
    "handle": dict(name="GTV HEXA élfogantyú, alu elox, 192/225 mm (UA-HEXA-192-05)", L=225.0, pitch=192.0, depth=40.0, lip=17.0, t=1.5,
                   hole_from_edge=10.0, pilot_d=2.5, pilot_depth=12.0),
    "back": dict(nail_d=1.6, L=25.0, max_pitch=150.0, end=40.0),
}


def _hole(part, normal, pts, d, depth, kind, cs_d=None):
    return dict(part=part, normal=normal, pts=[tuple(round(v, 3) for v in p) for p in pts],
                d=d, depth=depth, kind=kind, cs_d=cs_d)


def _spread(a, b, max_pitch):
    """Egyenletes pontok a..b között (a végpontokkal), max_pitch távolsággal."""
    import math
    n = max(1, math.ceil((b - a) / max_pitch))
    return [a + (b - a) * i / n for i in range(n + 1)]


def holes_and_hardware(p=PARAMS):
    """v3: egy korpusz. Visszaad: (holes, hardware) modellkoordinátákban (mm)."""
    t, H, D, g, td, tb = p["t"], p["H"], p["D"], p["gap"], p["t_door"], p["t_back"]
    y_c = td; dp = D - td - tb; W = sum(p["module_widths"])
    C, Dw, Hg, Tp, Mt, Bk = (HW[k] for k in ("confirmat", "dowel", "hinge", "tipon", "mount", "back"))
    xs = layout(p); comps = compartments(p)
    holes, hw = [], []
    M = "K"

    def conf_hw(p1, p2):
        hw.append(dict(kind="konfirmát 7×50", module=M, shape="screw", p1=p1, p2=p2, d=7.0, head_d=10.0, head_l=3.0))

    def dowel_hw(p1, p2):
        hw.append(dict(kind="tipli 8×35", module=M, shape="cyl", p1=p1, p2=p2, d=Dw["d"]))

    jp = joint_positions(dp)
    cy = [y_c + v for v in jp["confirmat"]]; dy_ = [y_c + v for v in jp["dowel"]]
    # 1) oldallapok <-> tető/fenék (mint v2): konfirmát az oldallap külső lapján át a vízszintes lap végébe
    for side, outer, inner, sgn in (("bal", 0.0, t, -1), ("jobb", W, W - t, 1)):
        sp = f"K {side} oldallap"
        for hp, z in (("K fenéklap", t / 2), ("K tetőlap", H - t / 2)):
            holes.append(_hole(sp, (sgn, 0, 0), [(outer, y, z) for y in cy], C["d_face"], t, "konfirmát (oldallap, átmenő, süllyesztett)", C["cs_d"]))
            holes.append(_hole(hp, (sgn, 0, 0), [(inner, y, z) for y in cy], C["d_edge"], C["depth_edge"], "konfirmát előfurat (lapél)"))
            holes.append(_hole(sp, (-sgn, 0, 0), [(inner, y, z) for y in dy_], Dw["d"], Dw["depth_face"], "tipli (oldallap)"))
            holes.append(_hole(hp, (sgn, 0, 0), [(inner, y, z) for y in dy_], Dw["d"], Dw["depth_edge"], "tipli (lapél)"))
            for y in cy:
                conf_hw((outer, y, z), (outer - sgn * C["L"], y, z))
            for y in dy_:
                a = inner + sgn * Dw["depth_face"]
                dowel_hw((a, y, z), (a - sgn * Dw["L"], y, z))
    # 2) közfalak <-> tető/fenék: konfirmát a tető felső / a fenék alsó lapján át a közfal élébe
    for i, x in enumerate(xs[1:-1], 1):
        cx = x + t / 2; kp = f"K {i}. közfal"
        # tető
        holes.append(_hole("K tetőlap", (0, 0, 1), [(cx, y, H) for y in cy], C["d_face"], t, "konfirmát (tetőlap, átmenő, süllyesztett)", C["cs_d"]))
        holes.append(_hole(kp, (0, 0, 1), [(cx, y, H - t) for y in cy], C["d_edge"], C["depth_edge"], "konfirmát előfurat (lapél)"))
        holes.append(_hole("K tetőlap", (0, 0, -1), [(cx, y, H - t) for y in dy_], Dw["d"], Dw["depth_face"], "tipli (tetőlap alsó lapja)"))
        holes.append(_hole(kp, (0, 0, 1), [(cx, y, H - t) for y in dy_], Dw["d"], Dw["depth_edge"], "tipli (lapél)"))
        for y in cy:
            conf_hw((cx, y, H), (cx, y, H - C["L"]))
        for y in dy_:
            dowel_hw((cx, y, H - t + Dw["depth_face"]), (cx, y, H - t + Dw["depth_face"] - Dw["L"]))
        # fenék
        holes.append(_hole("K fenéklap", (0, 0, -1), [(cx, y, 0) for y in cy], C["d_face"], t, "konfirmát (fenéklap alulról, átmenő, süllyesztett)", C["cs_d"]))
        holes.append(_hole(kp, (0, 0, -1), [(cx, y, t) for y in cy], C["d_edge"], C["depth_edge"], "konfirmát előfurat (lapél)"))
        holes.append(_hole("K fenéklap", (0, 0, 1), [(cx, y, t) for y in dy_], Dw["d"], Dw["depth_face"], "tipli (fenéklap felső lapja)"))
        holes.append(_hole(kp, (0, 0, -1), [(cx, y, t) for y in dy_], Dw["d"], Dw["depth_edge"], "tipli (lapél)"))
        for y in cy:
            conf_hw((cx, y, 0), (cx, y, C["L"]))
        for y in dy_:
            dowel_hw((cx, y, t - Dw["depth_face"]), (cx, y, t - Dw["depth_face"] + Dw["L"]))
    # 3) a polc levehető, polctartó csapokon ül (lásd 4b) – nincs konfirmát/tipli
    # 4) pántok: ajtónként 1 csillapított (BLUMOTION) + 1 sima rugós; a talp a polctartó-furatsor furataiba csavarozva
    Gd = HW["grid"]; Hd = HW["handle"]
    gv = p["gap_v"]
    acc = 0.0
    doors = [q for q in parts(p) if q["kind"] == "ajtó"]
    for i, (w, q) in enumerate(zip(p["module_widths"], doors)):
        hs = p["hinge_side"][i]
        dx0, dx1 = acc + g, acc + w - g
        v_idx = i if hs == "L" else i + 1
        vx = xs[v_idx]
        inner_x, sgn = (vx + t, 1) if hs == "L" else (vx, -1)
        overlay = "ráütődő" if v_idx in (0, len(xs) - 1) else "félig ráütődő"
        cup_x = dx0 + Hg["cup_from_edge"] if hs == "L" else dx1 - Hg["cup_from_edge"]
        zhs = [gv + Hg["from_door_edge"], H - gv - Hg["from_door_edge"]]          # 100 és 420 mm – a furatsorban
        holes.append(_hole(q["name"], (0, 1, 0), [(cup_x, td, zh) for zh in zhs], Hg["cup_d"], Hg["cup_depth"], "pántcsésze Ø35"))
        for zh, kind in zip(zhs, ("sima, rugós", "csillapított (fékes)")):
            hw.append(dict(kind=f"pánt Häfele Metalla 300SM kombi 110° {overlay}, {kind}", module=M, shape="hinge",
                           cup=(cup_x, td, zh), inner_x=inner_x, sgn=sgn, y_plate=y_c + Hg["plate_from_front"]))
        # élfogantyú az ajtó alsó élének közepén
        cx = (dx0 + dx1) / 2
        zh_ = gv + Hd["hole_from_edge"]            # hátulról, az ajtó belső lapjába csavarozva, 10 mm-re az alsó éltől
        holes.append(_hole(q["name"], (0, 1, 0), [(cx - Hd["pitch"] / 2, td, zh_), (cx + Hd["pitch"] / 2, td, zh_)],
                           Hd["pilot_d"], Hd["pilot_depth"], "élfogantyú csavar előfurat"))
        hw.append(dict(kind=Hd["name"], module=M, shape="edgepull", cx=cx, z=gv, L=Hd["L"], depth=Hd["depth"],
                       lip=Hd["lip"], t=Hd["t"], y_back=td))
        acc += w
    # 4b) csak a szükséges furatok: pánttalp (a pántoldali lapon + tartalék a középső ajtó megfordításához)
    #     és polctartó csapfuratok a polc magasságában mindhárom rekeszben
    Gd = HW["grid"]
    gy = [y_c + Gd["from_front"], y_c + dp - Gd["from_back"]]
    zh_list = [gv + Hg["from_door_edge"], H - gv - Hg["from_door_edge"]]
    plate_faces = []   # (alkatrész, normál, x)
    for i in range(len(p["module_widths"])):
        hs = p["hinge_side"][i]
        v_idx = i if hs == "L" else i + 1
        vx = xs[v_idx]
        plate_faces.append((v_idx, (1, 0, 0) if hs == "L" else (-1, 0, 0), vx + t if hs == "L" else vx))
        if 0 < i < len(p["module_widths"]) - 1:          # tartalék a másik közfalon
            a_idx = i + 1 if hs == "L" else i
            ax_ = xs[a_idx]
            plate_faces.append((a_idx, (-1, 0, 0) if hs == "L" else (1, 0, 0), ax_ if hs == "L" else ax_ + t))
    vname = lambda k: "K bal oldallap" if k == 0 else ("K jobb oldallap" if k == len(xs) - 1 else f"K {k}. közfal")
    for k, nrm, x in plate_faces:
        pts = [(x, gy[0], zh + dz) for zh in zh_list for dz in (-Hg["plate_pitch"] / 2, Hg["plate_pitch"] / 2)]
        holes.append(_hole(vname(k), nrm, pts, 2.5, 10.0, "pánttalp előfurat (3,5×16 csavar)"))
    gp = [gy[0], y_c + dp / 2, gy[1]]                          # polctartó: oldalanként 3 csap (elöl, középen, hátul)
    ih = H - 2 * t
    z_shelf_bottom = t + (ih - t) / 2
    zp = z_shelf_bottom - 2.5                                  # Ø5 csap teteje = a polc alja
    for ci, (x0, x1) in enumerate(comps):
        for x, nrm, k in ((x0, (1, 0, 0), ci), (x1, (-1, 0, 0), ci + 1)):
            is_mid = 0 < k < len(xs) - 1
            if is_mid and nrm == (-1, 0, 0):
                continue                                       # közfalon egy átmenő furat szolgál ki két rekeszt
            depth = t if is_mid else Gd["depth_side"]
            kind = "polctartó csap furat (átmenő)" if is_mid else "polctartó csap furat"
            holes.append(_hole(vname(k), nrm, [(x, yy, zp) for yy in gp], Gd["d"], depth, kind))
    for ci, (x0, x1) in enumerate(comps):
        if ci in p["shelf_modules"]:
            for x in (x0, x1):
                for yy in gp:
                    hw.append(dict(kind="polctartó csap Ø5", module=M, shape="cyl", p1=(x - 6, yy, zp), p2=(x + 6, yy, zp), d=5.0))
    # 5) rögzítés a szekrényhez: összesen 4 csavar, a két szélső rekeszben 2-2
    mpts = [(xx, yy, t) for xx in (t + Mt["inset_side"], W - t - Mt["inset_side"])
            for yy in (y_c + Mt["from_front"], y_c + dp - Mt["from_back"])]
    holes.append(_hole("K fenéklap", (0, 0, 1), mpts, Mt["d"], t, "rögzítőcsavar a szekrényhez (süllyesztett)", Mt["cs_d"]))
    for pt in mpts:
        hw.append(dict(kind="forgácslapcsavar 3,5×30", module=M, shape="screw", p1=pt, p2=(pt[0], pt[1], pt[2] - Mt["L"]), d=3.5, head_d=7.0, head_l=2.0))
    # 6) hátfal: beütős hátfalszeggel körbe és a 4 függőleges elembe (a polcba nem) – nincs előfurat, nincs jelölés
    vlines = [x + t / 2 for x in xs]
    zs = _spread(Bk["end"], H - Bk["end"], Bk["max_pitch"])
    xsr = _spread(t + Bk["end"], W - t - Bk["end"], Bk["max_pitch"])
    bpts = [(vx, D, zz) for vx in vlines for zz in zs] + [(xx, D, zz) for zz in (t / 2, H - t / 2) for xx in xsr]
    for pt in bpts:
        hw.append(dict(kind="hátfalszeg 1,6×25", module=M, shape="screw", p1=pt, p2=(pt[0], pt[1] - Bk["L"], pt[2]), d=1.6, head_d=3.2, head_l=0.8))
    return holes, hw


def hardware_counts(p=PARAMS):
    from collections import Counter
    _, hw = holes_and_hardware(p)
    return Counter(h["kind"] for h in hw)


def base_cabinet(p=PARAMS):
    """A meglévő ELIA D 250 egyszerűsített tömbje a jelenethez (Z negatív = lefelé)."""
    W, H, D = p["base_W"], p["base_H"], p["base_D"]
    return [
        dict(name="ELIA korpusz", box=(0, 20, -H, W, D - 20, H), color="cashmere_body"),
        dict(name="ELIA bal ajtó", box=(2, 0, -H + 40, 798, 22, H - 60), color="cashmere"),
        dict(name="ELIA tükrös ajtó", box=(801, 2, -H + 40, 898, 18, H - 60), color="mirror"),
        dict(name="ELIA jobb ajtó", box=(1702, 0, -H + 40, 796, 22, H - 60), color="cashmere"),
        dict(name="ELIA felső sín", box=(0, 0, -20, W, 20, 20), color="alu"),
    ]


if __name__ == "__main__":
    for q in parts():
        print(q["name"], q["L"], "x", q["Wd"], q["material"])
