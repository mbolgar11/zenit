"""Rátétszekrény v8 – VÉGLEGES (egy korpusz, Häfele pántok, GTV HEXA élfogantyú, 3 polctartó csap oldalanként, szegezett hátfal) – Autodesk Fusion script – TELJES GYÁRTÁSI MODELL

Felépíti: 19 bútorlap (lapmag + ABS élzárás külön testként), minden fúrás valódi
Hole feature-ként (konfirmát, tipli, pántcsésze, pánttalp, TIP-ON, összekötő, rögzítő-
és hátfalcsavar), valamint a vasalatot (tiplik, csavarok, pántok, TIP-ON) külön komponensekben.

Futtatás: Fusion → Shift+S → Scripts → „+” → ez a mappa → Run.
A méretek a lenti PARAMS szótárban (mm) módosíthatók, utána újrafuttatás.
"""
import adsk.core, adsk.fusion, traceback, math

SHOW_BASE_CABINET = True

# ---------------------------------------------------------------------------
__GEOMETRY__
# ---------------------------------------------------------------------------

CM = 0.1
COLORS = {
    "lap18": (242, 241, 237), "door": (245, 244, 240), "hdf3": (237, 236, 232),
    "abs": (232, 231, 227), "cashmere": (201, 187, 170), "cashmere_body": (205, 191, 175),
    "mirror": (199, 211, 219), "alu": (180, 182, 186), "steel": (150, 152, 158),
    "zinc": (196, 198, 204), "beech": (214, 178, 128), "tipon": (90, 90, 95),
}


def P3(p):
    return adsk.core.Point3D.create(p[0] * CM, p[1] * CM, p[2] * CM)


def make_appearance(design, name, rgb):
    try:
        ex = design.appearances.itemByName(name)
        if ex:
            return ex
        app = adsk.core.Application.get()
        lib = None
        for ln in ("Fusion Appearance Library", "Fusion 360 Appearance Library"):
            lib = app.materialLibraries.itemByName(ln)
            if lib:
                break
        base = None
        for cand in ("Paint - Enamel Glossy (White)", "Plastic - Matte (White)", "Paint - Metal Flake (White)"):
            base = lib.appearances.itemByName(cand) if lib else None
            if base:
                break
        if not base:
            return None
        a = design.appearances.addByCopy(base, name)
        for i in range(a.appearanceProperties.count):
            prop = a.appearanceProperties.item(i)
            if prop.objectType == adsk.core.ColorProperty.classType():
                prop.value = adsk.core.Color.create(rgb[0], rgb[1], rgb[2], 255)
                break
        return a
    except Exception:
        return None


def extrude_box(comp, design, b, name, color_key):
    x, y, z, dx, dy, dz = b
    planes = comp.constructionPlanes
    if abs(z) > 1e-6:
        pin = planes.createInput()
        pin.setByOffset(comp.xYConstructionPlane, adsk.core.ValueInput.createByReal(z * CM))
        plane = planes.add(pin)
        plane.isLightBulbOn = False
    else:
        plane = comp.xYConstructionPlane
    sk = comp.sketches.add(plane)
    sk.name = name
    sk.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(x * CM, y * CM, 0), adsk.core.Point3D.create((x + dx) * CM, (y + dy) * CM, 0))
    sk.isVisible = False
    ext = comp.features.extrudeFeatures.addSimple(
        sk.profiles.item(0), adsk.core.ValueInput.createByReal(dz * CM),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext.name = name
    body = ext.bodies.item(0)
    body.name = name
    ap = make_appearance(design, "Ratet_" + color_key, COLORS[color_key])
    if ap:
        body.appearance = ap
    return body


def find_face(body, normal, pt):
    n = adsk.core.Vector3D.create(*normal)
    P = P3(pt)
    best = None
    for f in body.faces:
        if f.geometry.objectType != adsk.core.Plane.classType():
            continue
        ok, fn = f.evaluator.getNormalAtPoint(f.pointOnFace)
        if not ok or fn.dotProduct(n) < 0.999:
            continue
        if abs(f.pointOnFace.vectorTo(P).dotProduct(fn)) < 1e-4:
            best = f
            break
    return best


def add_holes(comp, body, hdef, idx):
    VI = adsk.core.ValueInput
    face = find_face(body, hdef["normal"], hdef["pts"][0])
    if face is None:
        raise RuntimeError(f"Nincs lap a furathoz: {hdef['part']} {hdef['kind']} {hdef['normal']}")
    sk = comp.sketches.add(face)
    sk.name = f"F{idx:02d} {hdef['kind']}"
    coll = adsk.core.ObjectCollection.create()
    for pt in hdef["pts"]:
        coll.add(sk.sketchPoints.add(sk.modelToSketchSpace(P3(pt))))
    sk.isVisible = False
    hf = comp.features.holeFeatures
    if hdef.get("cs_d"):
        hi = hf.createCountersinkInput(VI.createByReal(hdef["d"] * CM), VI.createByReal(hdef["cs_d"] * CM),
                                       VI.createByString("90 deg"))
    else:
        hi = hf.createSimpleInput(VI.createByReal(hdef["d"] * CM))
    if "pántcsésze" in hdef["kind"]:
        hi.tipAngle = VI.createByString("180 deg")   # Forstner: lapos fenék
    hi.setPositionBySketchPoints(coll)
    hi.setDistanceExtent(VI.createByReal(hdef["depth"] * CM))
    try:
        hi.participantBodies = [body]
    except Exception:
        pass
    feat = hf.add(hi)
    feat.name = f"F{idx:02d} Ø{hdef['d']:g}×{hdef['depth']:g} {hdef['kind']}"
    return len(hdef["pts"])


# --- vasalat ideiglenes B-rep testekből ---------------------------------------
def _cyl(tbm, a, b, d):
    return tbm.createCylinderOrCone(P3(a), d / 2 * CM, P3(b), d / 2 * CM)


def _cone(tbm, a, b, d1, d2):
    return tbm.createCylinderOrCone(P3(a), d1 / 2 * CM, P3(b), d2 / 2 * CM)


def _box(tbm, c, size):
    obb = adsk.core.OrientedBoundingBox3D.create(P3(c), adsk.core.Vector3D.create(1, 0, 0),
                                                 adsk.core.Vector3D.create(0, 1, 0),
                                                 size[0] * CM, size[1] * CM, size[2] * CM)
    return tbm.createBox(obb)


def _union(tbm, bodies):
    base = bodies[0]
    for b in bodies[1:]:
        tbm.booleanOperation(base, b, adsk.fusion.BooleanTypes.UnionBooleanType)
    return base


def hw_bodies(tbm, h):
    s = h["shape"]
    if s == "cyl":
        return [_cyl(tbm, h["p1"], h["p2"], h["d"])]
    if s == "screw":
        a, b = h["p1"], h["p2"]
        L = math.dist(a, b)
        u = [(b[i] - a[i]) / L for i in range(3)]
        hb = [a[i] + u[i] * h["head_l"] for i in range(3)]
        return [_union(tbm, [_cone(tbm, a, hb, h["head_d"], h["d"]), _cyl(tbm, hb, b, h["d"] * 0.85)])]
    if s == "hinge":
        cx, cy, cz = h["cup"]
        cup = _cyl(tbm, (cx, cy - 12.5, cz), (cx, cy + 0.5, cz), 35)
        xin, sg, yp = h["inner_x"], h["sgn"], h["y_plate"]
        arm_x0, arm_x1 = sorted((cx, xin + sg * 12))
        arm = _box(tbm, ((arm_x0 + arm_x1) / 2, (cy + yp + 22) / 2, cz), (arm_x1 - arm_x0, yp + 22 - cy, 14))
        plate = _box(tbm, (xin + sg * 5, yp, cz), (10, 20, 50))
        return [_union(tbm, [cup, arm, plate])]
    if s == "edgepull":
        cx, z, L, D, lip, th, yb = h["cx"], h["z"], h["L"], h["depth"], h["lip"], h["t"], h["y_back"]
        leg = _box(tbm, (cx, yb - D / 2, z - th / 2), (L, D, th))
        lp = _box(tbm, (cx, yb - D + th / 2, z - th + lip / 2), (L, th, lip))
        return [_union(tbm, [leg, lp])]
    if s == "tipon":
        x, z, y0, L, d = h["x"], h["z"], h["y0"], h["L"], h["d"]
        house = _cyl(tbm, (x, y0 + 2, z - 3 - d / 2), (x, y0 + L, z - 3 - d / 2), d)
        plate = _box(tbm, (x, y0 + 45, z - 1.5), (24, 60, 3))
        return [_union(tbm, [house, plate])]
    return []


HW_COLOR = {"pánt": "steel", "RIOS": "alu", "Viefe": "alu", "GTV HEXA": "alu", "tipli": "beech", "konfirmát": "zinc", "pánt": "steel", "TIP-ON": "tipon",
            "forgácslapcsavar": "zinc", "szekrényösszekötő": "steel", "hátfalcsavar": "zinc", "hátfalszeg": "zinc"}


def build(design, status=print):
    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
    try:
        if design.designIntent != adsk.fusion.DesignIntentTypes.HybridDesignIntentType:
            design.designIntent = adsk.fusion.DesignIntentTypes.HybridDesignIntentType
    except Exception:
        pass
    design.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
    root = design.rootComponent
    up = design.userParameters
    for pname, key, comment in (("Korpusz_magassag", "H", "Korpusz magasság"), ("Teljes_melyseg", "D", "Teljes mélység ajtóval"),
                                ("Lapvastagsag", "t", "Bútorlap vastagság"), ("Ajtohezag", "gap", "Ajtó körbe hézag")):
        if not up.itemByName(pname):
            up.add(pname, adsk.core.ValueInput.createByString(f"{PARAMS[key]} mm"), "mm", comment)
    for i, w in enumerate(PARAMS["module_widths"]):
        if not up.itemByName(f"Ajtoosztas{i+1}"):
            up.add(f"Ajtoosztas{i+1}", adsk.core.ValueInput.createByString(f"{w} mm"), "mm", f"Ajtóosztás {i+1}")

    stats = dict(panels=0, abs=0, hole_features=0, holes=0, hardware=0)
    modules, bodies = {}, {}
    for q in parts():
        m = q["module"]
        if m not in modules:
            mocc = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            mocc.component.name = "Korpusz (v10, egyben)" if m == "K" else f"{m} modul"
            modules[m] = mocc.component
        pocc = modules[m].occurrences.addNewComponent(adsk.core.Matrix3D.create())
        comp = pocc.component
        comp.name = q["name"]
        core, strips = split_banding(q)
        key = "door" if q["kind"] == "ajtó" else q["material"]
        bodies[q["name"]] = (comp, extrude_box(comp, design, core, q["name"], key))
        stats["panels"] += 1
        for sname, sbox, th in strips:
            extrude_box(comp, design, sbox, f"{sname} {th:g} mm", "abs")
            stats["abs"] += 1
    status("lapok kész")

    holes, hw = holes_and_hardware()
    for idx, h in enumerate(holes, 1):
        comp, body = bodies[h["part"]]
        stats["holes"] += add_holes(comp, body, h, idx)
        stats["hole_features"] += 1
    status("furatok kész")

    tbm = adsk.fusion.TemporaryBRepManager.get()
    vocc = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    vas = vocc.component
    vas.name = "Vasalat"
    groups = {}
    for h in hw:
        groups.setdefault(h["kind"], []).append(h)
    for kind, items in groups.items():
        kocc = vas.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        kc = kocc.component
        kc.name = f"{kind} ({len(items)} db)"
        bf = kc.features.baseFeatures.add()
        bf.startEdit()
        ckey = next((v for k, v in HW_COLOR.items() if kind.startswith(k)), "steel")
        ap = make_appearance(design, "Ratet_" + ckey, COLORS[ckey])
        for n, h in enumerate(items, 1):
            for tb in hw_bodies(tbm, h):
                b = kc.bRepBodies.add(tb, bf)
                b.name = f"{kind.split()[0]} {n:02d}"
                if ap:
                    b.appearance = ap
                stats["hardware"] += 1
        bf.finishEdit()
        bf.name = kind
    status("vasalat kész")

    if SHOW_BASE_CABINET:
        bocc = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        bocc.component.name = "ELIA D 250 (meglévő)"
        for e in base_cabinet():
            cocc = bocc.component.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            cocc.component.name = e["name"]
            extrude_box(cocc.component, design, e["box"], e["name"], e["color"])
    return stats


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = adsk.fusion.Design.cast(app.activeProduct)
        st = build(design, status=lambda s: None)
        app.activeViewport.fit()
        ui.messageBox(f"Kész: {st['panels']} lap, {st['abs']} ABS él, {st['hole_features']} furat-feature "
                      f"({st['holes']} furat), {st['hardware']} vasalat.", "Rátétszekrény")
    except Exception:
        if ui:
            ui.messageBox("Hiba:\n{}".format(traceback.format_exc()))
