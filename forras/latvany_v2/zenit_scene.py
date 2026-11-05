"""ZENIT látványtervek – Blender (bpy) jelenet-generátor.
Használat: python zenit_scene.py <kimenet.png> '<json beállítások>'
Beállítások (mind opcionális):
  cam: hero|front|before|open|top|macro_handle|macro_hinge|macro_edge|exploded|story_low
  mood: evening|morning|night|studio|day
  body/door/inner: "#hex" vagy textúra: oak|smoked|walnut|linen|concrete
  handle: alu|black|bronze ; finish: matt|satin|gloss
  topper: true/false ; clutter: true/false ; doors: szög fokban ; led: true/false
  wall: "#hex" ; floor: greyoak|oak|walnut ; props: true/false ; samples, w, h ; explode: 0..1
"""
import sys, os, math, json
import bpy, bmesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry import PARAMS, parts, base_cabinet, holes_and_hardware

OUT = sys.argv[1]
C = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
g = lambda k, d: C.get(k, d)
CAM, MOOD = g("cam", "hero"), g("mood", "evening")
BH = PARAMS["base_H"]; CEIL = PARAMS["ceiling"]


def srgb(h):
    h = h.lstrip("#"); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"
    sc.cycles.samples = g("samples", 40); sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 8; sc.cycles.glossy_bounces = 3; sc.cycles.transparent_max_bounces = 4
    sc.cycles.adaptive_threshold = 0.02; sc.render.film_transparent = False
    sc.render.resolution_x, sc.render.resolution_y = g("w", 1600), g("h", 1000)
    sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
    sc.view_settings.exposure = g("exposure", 0.0)
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    col, stren = {"evening": ("#2A3140", 0.08), "night": ("#1A2438", 0.03), "morning": ("#DDE6F2", 0.35),
                  "day": ("#E8EDF3", 0.45), "studio": ("#141210", 0.0)}[MOOD]
    bg.inputs[0].default_value = (*srgb(col), 1); bg.inputs[1].default_value = stren
    return sc


def principled(name, rough=0.5, metal=0.0, spec=0.4, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    b.inputs["Specular IOR Level"].default_value = spec
    if coat: b.inputs["Coat Weight"].default_value = coat
    return m, b


FIN = {"matt": (0.62, 0.0), "satin": (0.32, 0.15), "gloss": (0.08, 0.6)}


def wood(name, c1, c2, c3, scale=6.0, rough=0.48, rot=True):
    """Procedurális fa: függőleges, finom erezet (sávos wave + zaj torzítás)."""
    m, b = principled(name, rough)
    nt = m.node_tree; N = nt.nodes; L = nt.links
    tc = N.new("ShaderNodeTexCoord"); mp = N.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (scale * 4.0, scale * 4.0, scale * 0.25)
    L.new(tc.outputs["Object"], mp.inputs["Vector"])
    wv = N.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "X"
    wv.inputs["Scale"].default_value = 1.0; wv.inputs["Distortion"].default_value = 7.0
    wv.inputs["Detail"].default_value = 4; wv.inputs["Detail Scale"].default_value = 1.5
    L.new(mp.outputs["Vector"], wv.inputs["Vector"])
    nz = N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 1.6; nz.inputs["Detail"].default_value = 6
    L.new(mp.outputs["Vector"], nz.inputs["Vector"])
    mx = N.new("ShaderNodeMix"); mx.data_type = "FLOAT"; mx.inputs["Factor"].default_value = 0.55
    L.new(wv.outputs["Fac"], mx.inputs[2]); L.new(nz.outputs["Fac"], mx.inputs[3])
    ramp = N.new("ShaderNodeValToRGB"); cr = ramp.color_ramp
    cr.elements[0].position = 0.2; cr.elements[0].color = (*srgb(c1), 1)
    cr.elements[1].position = 0.8; cr.elements[1].color = (*srgb(c3), 1)
    e = cr.elements.new(0.5); e.color = (*srgb(c2), 1)
    L.new(mx.outputs[0], ramp.inputs["Fac"]); L.new(ramp.outputs["Color"], b.inputs["Base Color"])
    bump = N.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.04
    L.new(wv.outputs["Fac"], bump.inputs["Height"]); L.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m


def linen(name, col="#D6CDBE", rough=0.85):
    m, b = principled(name, rough, spec=0.2)
    nt = m.node_tree; N = nt.nodes; L = nt.links
    tc = N.new("ShaderNodeTexCoord"); mp = N.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (300, 300, 300)
    L.new(tc.outputs["Object"], mp.inputs["Vector"])
    w1 = N.new("ShaderNodeTexWave"); w1.wave_type = "BANDS"; w1.bands_direction = "X"; w1.inputs["Scale"].default_value = 1
    w2 = N.new("ShaderNodeTexWave"); w2.wave_type = "BANDS"; w2.bands_direction = "Y"; w2.inputs["Scale"].default_value = 1
    for w_ in (w1, w2): L.new(mp.outputs["Vector"], w_.inputs["Vector"])
    mx = N.new("ShaderNodeMath"); mx.operation = "MULTIPLY"; L.new(w1.outputs["Fac"], mx.inputs[0]); L.new(w2.outputs["Fac"], mx.inputs[1])
    nz = N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 40
    L.new(mp.outputs["Vector"], nz.inputs["Vector"])
    mc = N.new("ShaderNodeMix"); mc.data_type = "RGBA"; mc.blend_type = "MULTIPLY"; mc.inputs["Factor"].default_value = 0.25
    mc.inputs[6].default_value = (*srgb(col), 1); L.new(nz.outputs["Color"], mc.inputs[7]); L.new(mc.outputs[2], b.inputs["Base Color"])
    bump = N.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.12
    L.new(mx.outputs[0], bump.inputs["Height"]); L.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m


def concrete(name):
    m, b = principled(name, 0.75)
    nt = m.node_tree; N = nt.nodes; L = nt.links
    nz = N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 18; nz.inputs["Detail"].default_value = 12; nz.inputs["Roughness"].default_value = 0.65
    ramp = N.new("ShaderNodeValToRGB"); cr = ramp.color_ramp
    cr.elements[0].color = (*srgb("#7F7A73"), 1); cr.elements[1].color = (*srgb("#B4AFA8"), 1)
    L.new(nz.outputs["Fac"], ramp.inputs["Fac"]); L.new(ramp.outputs["Color"], b.inputs["Base Color"])
    bump = N.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.08
    L.new(nz.outputs["Fac"], bump.inputs["Height"]); L.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m


TEX = {"oak": lambda n: wood(n, "#A9814F", "#C29A68", "#8E6A40"),
       "smoked": lambda n: wood(n, "#4A392B", "#5E4836", "#3A2C21"),
       "walnut": lambda n: wood(n, "#5A3D2A", "#73523A", "#47301F"),
       "greyoak": lambda n: wood(n, "#8F8A82", "#A39E96", "#7D7870", scale=3.0),
       "linen": lambda n: linen(n), "concrete": lambda n: concrete(n)}


def edge_soft(m, b, base_rgb=None, strength=0.16, radius=0.0035):
    """Extrém lágy élkiemelés: a Bevel-normál és a valódi normál eltéréséből élmaszk,
    amellyel az él egy árnyalattal sötétebb/melegebb lesz (ABS-él hatás) – nem fekete kontúr."""
    nt = m.node_tree; N = nt.nodes; L = nt.links
    bev = N.new("ShaderNodeBevel"); bev.inputs["Radius"].default_value = radius; bev.samples = 6
    geo = N.new("ShaderNodeNewGeometry")
    dot = N.new("ShaderNodeVectorMath"); dot.operation = "DOT_PRODUCT"
    L.new(bev.outputs["Normal"], dot.inputs[0]); L.new(geo.outputs["Normal"], dot.inputs[1])
    mr = N.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = 0.80; mr.inputs["From Max"].default_value = 0.995
    mr.inputs["To Min"].default_value = 1.0; mr.inputs["To Max"].default_value = 0.0
    L.new(dot.outputs["Value"], mr.inputs["Value"])
    if base_rgb is not None:
        mix = N.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "MULTIPLY"
        fac = N.new("ShaderNodeMath"); fac.operation = "MULTIPLY"; fac.inputs[1].default_value = strength
        L.new(mr.outputs["Result"], fac.inputs[0]); L.new(fac.outputs["Value"], mix.inputs["Factor"])
        mix.inputs[6].default_value = (*base_rgb, 1); mix.inputs[7].default_value = (0.70, 0.66, 0.62, 1)
        L.new(mix.outputs[2], b.inputs["Base Color"])
    if not b.inputs["Normal"].is_linked:
        L.new(bev.outputs["Normal"], b.inputs["Normal"])
    return m


def surface(name, spec):
    if spec in TEX:
        m = TEX[spec](name); return m
    r, ct = FIN[g("finish", "matt")]
    m, b = principled(name, r, coat=ct); b.inputs["Base Color"].default_value = (*srgb(spec), 1)
    b.inputs["Specular IOR Level"].default_value = 0.45
    return edge_soft(m, b, srgb(spec))


def plain(name, hexc, rough=0.6, metal=0.0, emit=None, estr=0.0):
    m, b = principled(name, rough, metal)
    b.inputs["Base Color"].default_value = (*srgb(hexc), 1)
    if emit:
        b.inputs["Emission Color"].default_value = (*srgb(emit), 1); b.inputs["Emission Strength"].default_value = estr
    return m


M = {}


def cube(name, b, m, bevel=0.0012, pivot=None, rot_z=0.0, parent=None):
    x, y, z, dx, dy, dz = [v / 1000.0 for v in b]
    bpy.ops.mesh.primitive_cube_add(size=1); o = bpy.context.object; o.name = name
    o.scale = (dx, dy, dz); o.location = (x + dx / 2, y + dy / 2, z + dz / 2)
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        bv = o.modifiers.new("bv", "BEVEL"); bv.width = bevel; bv.segments = 3
    o.data.materials.append(m)
    if pivot is not None and rot_z:
        bpy.context.scene.cursor.location = pivot
        bpy.ops.object.origin_set(type="ORIGIN_CURSOR"); o.rotation_euler[2] = math.radians(rot_z)
    if parent: o.parent = parent
    return o


def profile_handle(name, x0, L, y_back, z_bot, m, pivot=None, rot_z=0.0):
    """Lekerekített HEXA-szerű élfogantyú: hátsó talp + az ajtó alatt előre ívelő perem (mm)."""
    pts = [(y_back + 1.5, z_bot + 26), (y_back + 1.5, z_bot - 6), (y_back - 4, z_bot - 13), (y_back - 16, z_bot - 15),
           (y_back - 30, z_bot - 13), (y_back - 36, z_bot - 8), (y_back - 37.5, z_bot - 4),
           (y_back - 36, z_bot - 6.5), (y_back - 30, z_bot - 11.5), (y_back - 16, z_bot - 13.5), (y_back - 5, z_bot - 11.5),
           (y_back, z_bot - 5), (y_back, z_bot + 26)]
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    a = [bm.verts.new((x0 / 1000, y / 1000, z / 1000)) for y, z in pts]
    bpy_f = bm.faces.new(a)
    r = bmesh.ops.extrude_face_region(bm, geom=[bpy_f])
    bmesh.ops.translate(bm, vec=(L / 1000, 0, 0), verts=[v for v in r["geom"] if isinstance(v, bmesh.types.BMVert)])
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    o.data.materials.append(m)
    bv = o.modifiers.new("bv", "BEVEL"); bv.width = 0.0012; bv.segments = 3
    for p in o.data.polygons: p.use_smooth = True
    if pivot is not None and rot_z:
        bpy.context.view_layer.objects.active = o; o.select_set(True)
        bpy.context.scene.cursor.location = pivot
        bpy.ops.object.origin_set(type="ORIGIN_CURSOR"); o.rotation_euler[2] = math.radians(rot_z)
        o.select_set(False)
    return o


def olive(tag, PX, PY, pot, leafcol, top=1.5, n=320, seed=3):
    """olajfa-szerű szobanövény: törzs, ágak, sok apró levél (egy közös hálóval, gyorsan)"""
    import random
    rnd = random.Random(seed)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.17, depth=0.42, vertices=32, location=(PX, PY, 0.21)); bpy.context.object.data.materials.append(pot)
    bark = plain(tag + "_kereg", "#5B4B3B", 0.85)
    base = (PX, PY, 0.4); fork = (PX + 0.02, PY - 0.01, top - 0.55)
    cyl_between(tag + "_torzs", base, fork, 0.022, bark)
    tips = []
    for k in range(5):
        a = k * 1.26 + 0.3; r = 0.16 + 0.05 * (k % 2)
        tip = (PX + r * math.cos(a), PY + r * math.sin(a), top - 0.12 + 0.08 * ((k * 7) % 3) / 2)
        cyl_between(f"{tag}_ag{k}", fork, tip, 0.011, bark); tips.append(tip)
    leaf = plain(tag + "_level", leafcol, 0.5)
    from mathutils import Matrix, Euler
    bm = bmesh.new()
    for i in range(n):
        cx, cy, cz = tips[i % len(tips)]
        u, v, w = rnd.gauss(0, 0.11), rnd.gauss(0, 0.11), rnd.gauss(0, 0.09)
        M = (Matrix.Translation((cx + u, cy + v, cz + w)) @ Euler((rnd.uniform(-0.9, 0.9), rnd.uniform(-0.6, 0.6), rnd.uniform(0, 6.28))).to_matrix().to_4x4()
             @ Matrix.Diagonal((1.0, 0.36, 0.05, 1.0)))
        bmesh.ops.create_uvsphere(bm, u_segments=10, v_segments=6, radius=0.045, matrix=M)
    me = bpy.data.meshes.new(tag + "_lombok"); bm.to_mesh(me); bm.free()
    for pg in me.polygons: pg.use_smooth = True
    o = bpy.data.objects.new(tag + "_lombok", me); bpy.context.scene.collection.objects.link(o); me.materials.append(leaf)


def cyl_between(name, p1, p2, r, m):
    from mathutils import Vector
    a, b = Vector(p1), Vector(p2); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=20)
    o = bpy.context.object; o.name = name; o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized()); o.data.materials.append(m)
    for pg in o.data.polygons: pg.use_smooth = True
    return o


def hinge(hx, left, ang, zc, m):
    """Häfele Metalla-szerű pánt: csésze az ajtó belső lapján, kar, szerelőtalp a korpusz belső oldalán (mm)."""
    sg = 1 if left else -1; a = math.radians(ang)
    def rot(x, y):  # az ajtó forgatása a (hx, 0) tengely körül
        dx, dy = x - hx, y
        return (hx + dx * math.cos(a) - dy * math.sin(a), dx * math.sin(a) + dy * math.cos(a))
    cx = hx + sg * (21.5 + 17.5)
    c1 = rot(cx, 18.5); c2 = rot(cx, 4)
    cyl_between("pant_csesze", (c1[0] / 1000, c1[1] / 1000, zc / 1000), (c2[0] / 1000, c2[1] / 1000, zc / 1000), 0.0175, m)
    f1 = rot(cx, 18.0); f2 = rot(cx, 20.0)
    cyl_between("pant_perem", (f1[0] / 1000, f1[1] / 1000, zc / 1000), (f2[0] / 1000, f2[1] / 1000, zc / 1000), 0.024, m)
    px = hx + sg * 22
    cube("pant_talp", (px - (0 if left else 12), 30, zc - 20, 12, 40, 40) if left else (px - 12, 30, zc - 20, 12, 40, 40), m, 0.002)
    k1 = (px / 1000 + sg * 0.012, 0.050, zc / 1000); c3 = rot(cx, 30)
    cyl_between("pant_kar", k1, (c3[0] / 1000, c3[1] / 1000, zc / 1000), 0.0065, m)


def build_topper():
    door_deg = g("doors", 0.0); ex = g("explode", 0.0)
    led = g("led", False)
    for q in parts():
        x, y, z, dx, dy, dz = q["box"]
        b = [x, y, z + BH, dx, dy, dz]
        k = q["kind"]
        if ex:
            off = {"tető": (0, 0, 260), "fenék": (0, 0, -260), "oldal": (-260 if x < 100 else 260, 0, 0),
                   "ajtó": (0, -520, 0), "hátfal": (0, 380, 0), "polc": (0, -180, 60), "közfal": (0, -90, 0)}.get(k, (0, 0, 0))
            b = [b[0] + off[0] * ex, b[1] + off[1] * ex, b[2] + off[2] * ex, dx, dy, dz]
        if k == "ajtó":
            build_topper.di = getattr(build_topper, "di", -1) + 1
            hx = x if q["hinge"] == "L" else x + dx
            ang = -door_deg if q["hinge"] == "L" else door_deg
            dm = M["mirror_door"] if build_topper.di in g("mirror_doors", []) else M["door"]
            cube(q["name"], b, dm, 0.002, pivot=(hx / 1000, 0.0, 0), rot_z=ang)
            if dm is M["mirror_door"]:  # keskeny kasmír keret a tükör körül
                for fb in ((x, y - 0.6, z + BH, dx, 0.5, 14), (x, y - 0.6, z + BH + dz - 14, dx, 0.5, 14), (x, y - 0.6, z + BH, 14, 0.5, dz), (x + dx - 14, y - 0.6, z + BH, 14, 0.5, dz)):
                    cube("tukorkeret", list(fb), M["door"], 0, pivot=(hx / 1000, 0.0, 0), rot_z=ang)
            if door_deg or g("hinges", False):
                for zc in (b[2] + dz - 95.5, b[2] + 95.5):
                    hinge(hx, q["hinge"] == "L", ang, zc, M["nickel"])
            if g("handle", "alu") != "none":
                cx = x + dx / 2
                profile_handle("fog", cx - 112.5, 225, PARAMS["t_door"] + b[1], b[2], M["handle"],
                               pivot=(hx / 1000, 0.0, 0), rot_z=ang)
        elif q["material"] == "hdf3":
            cube(q["name"], b, M["inner"], 0)
        elif k in ("polc", "közfal"):
            cube(q["name"], b, M["inner"])
        else:
            cube(q["name"], b, M["body"])
    if led and not ex:
        for xa, xb in ((18, 791), (809, 1691), (1709, 2482)):
            cube("led", (xa + 10, 40, BH + PARAMS["H"] - 18 - 6, xb - xa - 20, 10, 5), M["led"], 0)
            bpy.ops.object.light_add(type="AREA", location=((xa + xb) / 2000, 0.12, (BH + PARAMS["H"] - 30) / 1000))
            l = bpy.context.object; l.data.shape = "RECTANGLE"; l.data.size = (xb - xa) / 1000 * 0.9; l.data.size_y = 0.02
            l.data.energy = 25; l.data.color = srgb("#FFD9A8"); l.rotation_euler = (math.radians(180), 0, 0)


def build_base():
    for e in base_cabinet():
        x, y, z, dx, dy, dz = e["box"]
        key = {"cashmere_body": "base", "cashmere": "base_door", "mirror": "mirror", "alu": "alu"}[e["color"]]
        cube(e["name"], (x, y, z + BH, dx, dy, dz), M[key])
    for x0, w in ((2, 798), (1702, 796)):
        for zz in (400, 900, 1400, 1900):
            cube("csik", (x0, -1.5, zz - 4, w, 2, 8), M["alu"], 0)
    cube("labazat", (0, 10, 0, 2500, 590, 40), M["base"], 0)


def build_inside():
    """Élet a rekeszekben: összehajtott textil, len dobozok, bőrönd – ha nyitva vannak az ajtók."""
    z0 = BH + 18
    tex = [("#E9E3D8", 70), ("#CDBFAE", 55), ("#B9A68E", 60)]
    for xa in (60, 1730):
        cube("borond", (xa, 120, z0, 640, 420, 230), plain("borond", "#6B5240", 0.45), 0.012)
        cube("borond_fogo", (xa + 260, 110, z0 + 230, 120, 20, 22), M["alu"], 0.004)
    zz = z0
    for i, (c, h) in enumerate(tex):
        cube(f"textil{i}", (880 + i * 6, 90, zz, 360, 300, h), linen(f"textil{i}", c), 0.02); zz += h
    cube("doboz_len", (1300, 80, z0, 340, 380, 200), linen("doboz_len", "#CDBFAE"), 0.01)
    zz = BH + 256 + 18
    for i, (c, h) in enumerate([("#F1ECE4", 60), ("#D9CCBB", 50)]):
        cube(f"textil_p{i}", (900, 90, zz, 420, 300, h), linen(f"textil_p{i}", c), 0.02); zz += h
    cube("doboz_p", (1380, 80, BH + 256 + 18, 280, 360, 170), linen("doboz_p", "#B9A68E"), 0.01)


def build_clutter():
    top = BH
    items = [((180, 60, top, 620, 420, 240), "#2F3A4A"), ((900, 120, top, 420, 380, 300), "#B79C7A"),
             ((1340, 90, top, 360, 330, 220), "#C7AF8E"), ((1730, 40, top, 560, 470, 180), "#6E6A64"),
             ((1760, 80, top + 180, 380, 300, 160), "#A58B6A"), ((60, 380, top, 300, 200, 90), "#D9D2C6")]
    for i, (b, c) in enumerate(items):
        cube(f"doboz{i}", b, plain(f"doboz{i}", c, 0.8), 0.006)


def planks(m, scale=(0.9, 5.5)):
    """Fa padló deszkaosztással (Brick textúra fugái finoman sötétítenek)."""
    nt = m.node_tree; N = nt.nodes; L = nt.links
    b = N["Principled BSDF"]; src = b.inputs["Base Color"].links[0].from_socket
    tc = N.new("ShaderNodeTexCoord"); br = N.new("ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = 1.0; br.inputs["Mortar Size"].default_value = 0.0035
    br.inputs["Brick Width"].default_value = 1.8; br.inputs["Row Height"].default_value = 0.19; br.offset = 0.37
    br.inputs["Color1"].default_value = (1, 1, 1, 1); br.inputs["Color2"].default_value = (0.93, 0.93, 0.93, 1)
    br.inputs["Mortar"].default_value = (0.55, 0.55, 0.55, 1)
    L.new(tc.outputs["Object"], br.inputs["Vector"])
    mix = N.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "MULTIPLY"; mix.inputs["Factor"].default_value = 1.0
    L.new(src, mix.inputs[6]); L.new(br.outputs["Color"], mix.inputs[7]); L.new(mix.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.38
    return m


def art(name, cols):
    """Absztrakt, meleg tónusú festmény (procedurális)."""
    m, b = principled(name, 0.8, spec=0.2)
    nt = m.node_tree; N = nt.nodes; L = nt.links
    tc = N.new("ShaderNodeTexCoord"); nz = N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 0.9
    nz.inputs["Detail"].default_value = 2.5; nz.inputs["Distortion"].default_value = 0.25
    L.new(tc.outputs["Generated"], nz.inputs["Vector"])
    ramp = N.new("ShaderNodeValToRGB"); cr = ramp.color_ramp
    cr.elements[0].position = 0.35; cr.elements[0].color = (*srgb(cols[0]), 1)
    cr.elements[1].position = 0.62; cr.elements[1].color = (*srgb(cols[2]), 1)
    e = cr.elements.new(0.5); e.color = (*srgb(cols[1]), 1)
    L.new(nz.outputs["Fac"], ramp.inputs["Fac"]); L.new(ramp.outputs["Color"], b.inputs["Base Color"])
    return m


def build_room():
    W = g("wall", "#ECE8E2")
    wall = plain("fal", W, 0.92); ceil = plain("plafon", "#F6F4F0", 0.95)
    floor = planks(TEX[g("floor", "greyoak")]("padlo"))
    cube("padlo", (-2600, -4200, -20, 7800, 4900, 20), floor, 0)
    cube("hatfal", (-2600, 600, 0, 7800, 100, CEIL), wall, 0)
    cube("plafon", (-2600, -4200, CEIL, 7800, 4900, 30), ceil, 0)
    cube("szegely", (-900, 588, 0, 7000, 14, 80), plain("szegely", "#F4F1EC", 0.6), 0)
    # bal fal ablakkal
    cube("balfal_a", (-1000, -4200, 0, 100, 1700, CEIL), wall, 0)
    cube("balfal_b", (-1000, -1300, 0, 100, 1900, CEIL), wall, 0)
    cube("balfal_c", (-1000, -2500, 0, 100, 1200, 700), wall, 0)
    cube("balfal_d", (-1000, -2500, 2350, 100, 1200, CEIL - 2350), wall, 0)
    cube("ablakkeret", (-960, -2500, 700, 30, 1200, 40), plain("keret", "#F4F1EC", 0.4), 0)
    sky = {"evening": ("#6E7C9A", 1.6), "night": ("#1E2A44", 0.6), "morning": ("#EAF1F8", 4.0), "day": ("#EEF3F8", 4.0)}.get(MOOD, ("#888888", 1.0))
    cube("kint", (-1500, -2700, 0, 20, 1600, CEIL), plain("kint", sky[0], 1.0, emit=sky[0], estr=sky[1]), 0)
    cube("elofal", (-2600, -4300, 0, 7800, 100, CEIL), wall, 0)
    cube("jobbfal", (4200, -4200, 0, 100, 4900, CEIL), wall, 0)
    if not g("props", True):
        return
    if g("layout", "A") == "B":
        build_props_b(); return
    lin = linen("agynemu", "#E9E3D8"); lin2 = linen("takaro", "#BFAF98")
    # ágy a szekrénnyel szemben, jobbra
    cube("agykeret", (2900, -3300, 0, 1300, 2050, 320), TEX["oak"]("agykeret"), 0.01)
    cube("matrac", (2930, -3270, 320, 1240, 1990, 200), lin, 0.04)
    cube("takaro", (2910, -3100, 470, 1280, 1500, 70), lin2, 0.03)
    cube("parna1", (2980, -1500, 520, 520, 300, 130), lin, 0.05)
    cube("parna2", (3620, -1500, 520, 520, 300, 130), lin, 0.05)
    cube("tamla", (2880, -1260, 0, 1340, 70, 1050), linen("tamla", "#8B8073"), 0.02)
    # éjjeliszekrény + lámpa
    cube("ejjeli", (2560, -520, 0, 420, 380, 520), TEX["walnut"]("ejjeli"), 0.006)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=0.22, location=(2.77, -0.33, 0.68))
    sh = bpy.context.object; sh.data.materials.append(plain("bura", "#F3E6CF", 0.7, emit="#FFC98A",
                                                           estr={"evening": 6, "night": 0.0}.get(MOOD, 0.0)))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.16, location=(2.77, -0.33, 0.58))
    bpy.context.object.data.materials.append(M["alu"])
    if MOOD == "evening":
        bpy.ops.object.light_add(type="POINT", location=(2.77, -0.33, 0.70))
        l = bpy.context.object; l.data.energy = 48; l.data.color = srgb("#FFC48A"); l.data.shadow_soft_size = 0.12
    # szőnyeg (kétszínű, szegéllyel)
    cube("szonyeg", (900, -3000, 0, 2300, 1700, 8), linen("szonyeg", "#B9AC99"), 0.002)
    cube("szonyeg_bel", (1000, -2900, 0, 2100, 1500, 10), linen("szonyeg_b", "#D4C9B8"), 0.002)
    # festmény a hátsó falon, a szekrénytől jobbra
    fr = plain("keret_fa", "#6B4E36", 0.45)
    cube("kep_keret", (2930, 560, 1050, 1000, 40, 1250), fr, 0.004)
    cube("kep", (2960, 548, 1080, 940, 14, 1190), plain("vaszon", "#E9E2D6", 0.85), 0)
    cube("kep_mezo1", (3040, 540, 1160, 780, 6, 520), plain("mezo1", "#B98D69", 0.9), 0)
    cube("kep_mezo2", (3040, 540, 1720, 780, 6, 330), plain("mezo2", "#D7C6AE", 0.9), 0)
    cube("kep_vonal", (3040, 536, 1700, 780, 4, 6), plain("vonal", "#2E2925", 0.6), 0)
    # éjjeliszekrényen könyvek + váza
    for i, (c, hh) in enumerate((("#3F4A57", 34), ("#B59C7C", 28), ("#E2DACD", 40))):
        cube(f"konyv{i}", (2600, -470 + i * 6, 520 + sum(x[1] for x in ((0, 34), (0, 28), (0, 40))[:i]), 260 - i * 20, 190, hh), plain(f"konyv{i}", c, 0.7), 0.003)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.26, location=(2.88, -0.24, 0.65))
    v = bpy.context.object; v.data.materials.append(plain("vaza", "#D8D0C4", 0.25))
    for k in range(5):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.003, depth=0.42, location=(2.88 + 0.02 * math.cos(k), -0.24 + 0.02 * math.sin(k), 0.92))
        o = bpy.context.object; o.rotation_euler = (0.25 * math.sin(k * 2), 0.25 * math.cos(k * 2), 0); o.data.materials.append(plain("ag", "#6E5A43", 0.8))
    # olvasófotel + állólámpa az ablak mellett
    lc = linen("fotel", "#A89A86"); ft = TEX["walnut"]("fotel_lab")
    cube("fotel_ules", (-760, -2300, 380, 760, 720, 140), lc, 0.05)
    cube("fotel_hat", (-780, -2300, 450, 160, 720, 520), lc, 0.05)
    cube("fotel_k1", (-760, -2330, 380, 760, 90, 260), lc, 0.04)
    cube("fotel_k2", (-760, -1640, 380, 760, 90, 260), lc, 0.04)
    for xx, yy in ((-720, -2290), (-60, -2290), (-720, -1600), (-60, -1600)):
        cube("fotel_lab", (xx, yy, 0, 34, 34, 380), ft, 0.004)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.006, depth=1.55, location=(0.25, -2.55, 0.78))
    bpy.context.object.data.materials.append(plain("lampa_rud", "#2B2622", 0.35, 0.8))
    bpy.ops.mesh.primitive_cone_add(radius1=0.2, radius2=0.12, depth=0.26, location=(0.25, -2.55, 1.6))
    bpy.context.object.data.materials.append(plain("lampa_bura", "#EFE6D6", 0.8, emit="#FFC98A", estr={"evening": 3.5, "night": 0.6}.get(MOOD, 0.0)))
    if MOOD in ("evening", "night"):
        bpy.ops.object.light_add(type="POINT", location=(0.25, -2.55, 1.52))
        l = bpy.context.object; l.data.energy = 55 if MOOD == "evening" else 14; l.data.color = srgb("#FFC48A"); l.data.shadow_soft_size = 0.15
    # növény
    olive("na", -0.55, -0.35, plain("kaspo", "#8E6F5A", 0.7), "#55634A", top=1.45, seed=5)
    # függöny az ablaknál
    cur = linen("fuggony", "#F2EEE6", 0.9)
    for i in range(7):
        cube(f"fugg{i}", (-880, -2650 + i * 70, 0, 25 + (i % 2) * 20, 60, CEIL - 30), cur, 0.01)


def build_props_b():
    """B elrendezés: öltözőszoba-hangulat – diókomód lámpával és könyvekkel, kárpitozott pad, nagy álló kép, kerek tükör, szőnyeg."""
    wal = TEX["walnut"]("komod"); lin = linen("pad", g("bench", "#8F8476"))
    cube("komod", (2750, 130, 0, 1350, 440, 720), wal, 0.006)
    for i in range(3):
        cube(f"komod_fiok{i}", (2770 + i * 445, 126, 60, 420, 6, 600), plain(f"fiokrés{i}", "#3E2B1E", 0.6), 0)
    cube("komod_lab", (2760, 140, -10, 1330, 420, 12), plain("lab", "#2B211A", 0.5), 0)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.28, location=(3.85, 0.33, 0.86)); bpy.context.object.data.materials.append(plain("lampatest", "#D8CBB8", 0.3))
    bpy.ops.mesh.primitive_cone_add(radius1=0.19, radius2=0.13, depth=0.24, location=(3.85, 0.33, 1.1))
    bpy.context.object.data.materials.append(plain("lampabura", "#EFE6D6", 0.85, emit="#FFC98A", estr={"evening": 4, "night": 0.8}.get(MOOD, 0.0)))
    if MOOD in ("evening", "night"):
        bpy.ops.object.light_add(type="POINT", location=(3.85, 0.33, 1.05)); l = bpy.context.object; l.data.energy = 60 if MOOD == "evening" else 16; l.data.color = srgb("#FFC48A"); l.data.shadow_soft_size = 0.15
    for i, (c, hh) in enumerate((("#2F3A33", 40), ("#C9B79C", 30), ("#E8E1D5", 36))):
        cube(f"konyvb{i}", (2950, 220 + i * 4, 720 + sum((40, 30, 36)[:i]), 300 - i * 18, 210, hh), plain(f"konyvb{i}", c, 0.7), 0.003)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.09, location=(3.35, 0.35, 0.81)); o = bpy.context.object; o.scale = (1, 1, 1.1); o.data.materials.append(plain("vazab", "#B08D6A", 0.35))
    # nagy álló kép a komódon a falnak döntve
    cube("allo_keret", (3050, 480, 720, 760, 30, 980), plain("allokeret", "#E9E2D6", 0.6), 0.004)
    cube("allo_kep", (3080, 470, 750, 700, 12, 920), plain("allokep", "#D6C7B1", 0.9), 0)
    cube("allo_folt", (3140, 466, 830, 420, 6, 520), plain("allofolt", g("art", "#7C6A57"), 0.9), 0)
    # kerek tükör a jobb falon
    bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=0.02, location=(4.19, -1.2, 1.55), rotation=(0, math.radians(90), 0))
    bpy.context.object.data.materials.append(M["mirror"])
    bpy.ops.mesh.primitive_torus_add(major_radius=0.42, minor_radius=0.012, location=(4.18, -1.2, 1.55), rotation=(0, math.radians(90), 0))
    bpy.context.object.data.materials.append(plain("tukorkeret_b", "#A07A45", 0.3, 1.0))
    # kárpitozott pad a szekrény előtt, rajta összehajtott pléd
    cube("pad", (650, -1650, 0, 1200, 420, 440), lin, 0.04)
    cube("pled", (1150, -1660, 440, 520, 400, 40), linen("pled", "#D9CDBB"), 0.02)
    # szőnyeg, növény, függöny
    cube("szonyeg_b", (300, -2700, 0, 2600, 1800, 8), linen("szonyegb", "#C2B49F"), 0.002)
    PX, PY = g("plant", (-0.72, -0.28))
    olive("nb", PX, PY, plain("kaspob", "#D8CFC2", 0.6), "#5E6C4F", top=1.6, seed=9)
    cur = linen("fuggonyb", "#EEE8DE", 0.9)
    for i in range(8):
        cube(f"fuggb{i}", (-880, -2700 + i * 70, 0, 25 + (i % 2) * 22, 60, CEIL - 30), cur, 0.01)


def build_studio():
    bg = plain("hatter", g("studio_bg", "#1B1815"), 0.9)
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, BH / 1000 - 0.75)); bpy.context.object.data.materials.append(bg)
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 4, 0), rotation=(math.radians(90), 0, 0)); bpy.context.object.data.materials.append(bg)


def lights():
    if MOOD == "studio":
        for loc, rot, e, s in (((-1.5, -3.0, 4.2), (55, 0, -25), 900, 2.5), ((4.5, -2.5, 3.6), (60, 0, 50), 420, 2.0), ((1.2, 2.5, 4.5), (-50, 0, 180), 300, 3.0)):
            bpy.ops.object.light_add(type="AREA", location=loc); l = bpy.context.object
            l.data.energy = e; l.data.size = s; l.rotation_euler = tuple(math.radians(a) for a in rot); l.data.color = srgb("#FFF3E4")
        return
    if MOOD in ("morning", "day"):
        bpy.ops.object.light_add(type="SUN", location=(-3, -2, 4)); s = bpy.context.object
        s.data.energy = 4.5 if MOOD == "morning" else 3.0; s.data.angle = math.radians(3)
        s.data.color = srgb("#FFE7C8" if MOOD == "morning" else "#FFF6EC")
        s.rotation_euler = (math.radians(62), 0, math.radians(-62))
        bpy.ops.object.light_add(type="AREA", location=(-0.9, -1.9, 1.5)); a = bpy.context.object
        a.data.energy = 260; a.data.size = 1.2; a.rotation_euler = (0, math.radians(-90), 0); a.data.color = srgb("#E9F0FA")
        bpy.ops.object.light_add(type="AREA", location=(1.3, -3.5, 2.4)); f = bpy.context.object
        f.data.energy = 90 if MOOD == "morning" else 140; f.data.size = 3.0; f.rotation_euler = (math.radians(72), 0, 0)
    elif MOOD == "evening":
        bpy.ops.object.light_add(type="AREA", location=(1.3, -3.6, 2.5)); f = bpy.context.object
        f.data.energy = 46; f.data.size = 3.5; f.rotation_euler = (math.radians(70), 0, 0); f.data.color = srgb("#E9E7E4")
        bpy.ops.object.light_add(type="AREA", location=(-0.9, -1.9, 1.5)); mo = bpy.context.object
        mo.data.energy = 25; mo.data.size = 1.2; mo.rotation_euler = (0, math.radians(-90), 0); mo.data.color = srgb("#9FB2D8")
        bpy.ops.object.light_add(type="AREA", location=(1.25, -0.6, 2.56)); c = bpy.context.object
        c.data.energy = 14; c.data.size = 0.6; c.data.color = srgb("#FFD2A3")
    elif MOOD == "night":
        bpy.ops.object.light_add(type="AREA", location=(-0.9, -1.9, 1.5)); a = bpy.context.object
        a.data.energy = 70; a.data.size = 1.2; a.rotation_euler = (0, math.radians(-90), 0); a.data.color = srgb("#8FA6D6")
        bpy.ops.object.light_add(type="AREA", location=(1.3, -3.6, 2.4)); f = bpy.context.object
        f.data.energy = 8; f.data.size = 3.5; f.rotation_euler = (math.radians(70), 0, 0); f.data.color = srgb("#9DB0D8")


CAMS = {
    "hero": ((3.25, -3.1, 1.40), (1.10, 0.3, 1.95), 24),
    "front": ((1.25, -4.05, 1.35), (1.25, 0.3, 1.45), 24),
    "before": ((2.55, -3.9, 1.30), (1.15, 0.3, 1.80), 24),
    "open": ((2.9, -2.6, 1.65), (1.15, 0.3, 2.30), 26),
    "story_low": ((1.9, -1.9, 0.95), (1.05, 0.3, 2.25), 22),
    "top": ((1.25, -1.7, 2.5), (1.25, 0.3, 2.28), 24),
    "macro_handle": ((0.62, -0.42, 1.88), (0.40, 0.0, 2.055), 60),
    "macro_hinge": ((0.30, -0.70, 2.38), (0.03, 0.03, 2.40), 55),
    "macro_edge": ((2.70, -0.30, 2.555), (2.485, 0.0, 2.545), 55),
    "exploded": ((3.3, -3.0, 3.05), (1.25, 0.1, 2.30), 30),
    "led": ((1.62, -1.25, 1.78), (1.20, 0.30, 2.27), 28),
    "left": ((-0.55, -3.45, 1.45), (1.55, 0.3, 1.85), 24),
    "side": ((3.95, -1.75, 1.55), (1.05, 0.3, 2.0), 26),
    "front_wide": ((1.25, -4.15, 1.42), (1.25, 0.3, 1.62), 22),
    "hinge_in": ((0.78, -0.80, 2.08), (0.08, 0.10, 2.38), 38),
    "low_up": ((2.05, -1.55, 0.95), (1.30, 0.30, 2.20), 22),
    "mirror": ((2.35, -3.4, 1.45), (1.25, 0.3, 2.05), 26),
    "hero_wide": ((3.6, -3.9, 1.30), (1.05, 0.3, 1.55), 22),
}


def camera():
    loc, tgt, lens = CAMS[CAM]
    loc = tuple(C.get("cam_loc", loc)); tgt = tuple(C.get("cam_tgt", tgt)); lens = C.get("lens", lens)
    bpy.ops.object.camera_add(location=loc); cam = bpy.context.object
    bpy.ops.object.empty_add(location=tgt); t = bpy.context.object
    tc = cam.constraints.new("TRACK_TO"); tc.target = t; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
    cam.data.lens = lens; cam.data.sensor_width = 36
    if CAM.startswith("macro"):
        cam.data.dof.use_dof = True; cam.data.dof.focus_object = t; cam.data.dof.aperture_fstop = C.get("fstop", 2.8)
    bpy.context.scene.camera = cam


if __name__ == "__main__":
    sc = reset()
    M.update({
        "body": surface("korpusz", g("body", "#F1EFEA")),
        "door": surface("ajto", g("door", g("body", "#F1EFEA"))),
        "inner": surface("belso", g("inner", "#F1EFEA")),
        "handle": plain("fogantyu", {"alu": "#BFC1C3", "black": "#1C1C1C", "bronze": "#A07A45"}[g("handle_col", "alu")],
                        0.28, 1.0 if g("handle_col", "alu") != "black" else 0.0),
        "base": plain("kasmir", "#CDBFAF", 0.5), "base_door": plain("kasmir_ajto", "#C9BBAA", 0.45),
        "mirror": plain("tukor", "#E4E8EA", 0.03, 1.0), "alu": plain("alu", "#C4C6C8", 0.3, 1.0),
        "mirror_door": plain("tukorajto", "#E9ECEE", 0.02, 1.0),
        "nickel": plain("nikkel", "#C9CCCF", 0.28, 1.0),
        "led": plain("led", "#FFE2B8", 0.5, emit="#FFD39A", estr=12),
    })
    if MOOD == "studio":
        build_studio()
    else:
        build_room(); build_base()
    if g("topper", True):
        build_topper()
    if g("clutter", False):
        build_clutter()
    if g("inside", False):
        build_inside()
    lights(); camera()
    sc.render.filepath = OUT
    bpy.ops.render.render(write_still=True)
    print("render:", OUT)
