"""Blender (bpy) jelenet a rátétszekrényről. Használat:
python render_bl.py <kimenet.png> <nézet> [minta] [szélesség] [magasság] [ajtószög]
nézet: front | three | open | low | top
"""
import sys, os, math
import bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry import PARAMS, parts, base_cabinet

out = sys.argv[1]
view = sys.argv[2] if len(sys.argv) > 2 else "three"
samples = int(sys.argv[3]) if len(sys.argv) > 3 else 64
RW = int(sys.argv[4]) if len(sys.argv) > 4 else 1600
RH = int(sys.argv[5]) if len(sys.argv) > 5 else 1000
door_deg = float(sys.argv[6]) if len(sys.argv) > 6 else (100.0 if view == "open" else 0.0)

BASE_Z = PARAMS["base_H"] / 1000.0
CEIL = PARAMS["ceiling"] / 1000.0


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = RW, RH
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    w = bpy.data.worlds.new("w"); sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.92, 0.94, 1.0, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.35
    return sc


def mat(name, rgb, rough=0.55, metal=0.0, spec=0.4):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Specular IOR Level"].default_value = spec
    return m


def srgb(h):
    h = h.lstrip("#"); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)


def make_mats():
  return {
    "cashmere": mat("kasmir", srgb("#CDBFAF"), 0.5),
    "cashmere_door": mat("kasmir_ajto", srgb("#C9BBAA"), 0.45),
    "hdf": mat("hdf", srgb("#EDECE8"), 0.7),
    "mirror": mat("tukor", (0.9, 0.92, 0.93), 0.03, 1.0),
    "alu": mat("alu", (0.75, 0.76, 0.78), 0.3, 1.0),
    "wall": mat("fal", srgb("#F3F2EF"), 0.9),
    "accent": mat("hatfal", srgb("#F3F2EF"), 0.9),
    "top_body": mat("ratet_korpusz", srgb(os.environ.get("TOPPER", "#CDBFAF")), 0.5),
    "top_door": mat("ratet_ajto", srgb(os.environ.get("TOPPER_DOOR", os.environ.get("TOPPER", "#C9BBAA"))), 0.45),
    "handle": mat("fogantyu", (0.78, 0.79, 0.80), 0.35, 1.0),
    "floor": mat("padlo", srgb("#9C968E"), 0.5),
    "ceiling": mat("plafon", srgb("#FAFAF8"), 0.95),
    "edge": mat("el", srgb("#CFC5B9"), 0.4),
  }
M = {}


def cube(name, b, m, bevel=0.0012, pivot=None, rot_z=0.0):
    x, y, z, dx, dy, dz = [v / 1000.0 for v in b]
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.object; o.name = name
    o.scale = (dx, dy, dz)
    o.location = (x + dx / 2, y + dy / 2, z + dz / 2)
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        bv = o.modifiers.new("bv", "BEVEL"); bv.width = bevel; bv.segments = 2
    o.data.materials.append(m)
    if pivot is not None and rot_z:
        # forgatás a pánt tengelye körül
        bpy.context.scene.cursor.location = pivot
        bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
        o.rotation_euler[2] = math.radians(rot_z)
    return o


def build():
    for q in parts():
        x, y, z, dx, dy, dz = q["box"]
        b = (x, y, z + PARAMS["base_H"], dx, dy, dz)
        if q["kind"] == "ajtó":
            hx = x if q["hinge"] == "L" else x + dx
            ang = -door_deg if q["hinge"] == "L" else door_deg
            cube(q["name"], b, M["top_door"], 0.0015,
                 pivot=(hx / 1000, 0.0, 0), rot_z=ang)
        elif q["material"] == "hdf3":
            cube(q["name"], b, M["hdf"], 0)
        else:
            cube(q["name"], b, M["top_body"])
    for e in base_cabinet():
        x, y, z, dx, dy, dz = e["box"]
        b = (x, y, z + PARAMS["base_H"], dx, dy, dz)
        key = {"cashmere_body": "cashmere", "cashmere": "cashmere_door",
               "mirror": "mirror", "alu": "alu"}[e["color"]]
        cube(e["name"], b, M[key])
    from geometry import holes_and_hardware
    for h in holes_and_hardware()[1]:
        if h["shape"] == "edgepull":
            cx, z, L, Dd, lip, tt, yb = h["cx"], h["z"] + PARAMS["base_H"], h["L"], h["depth"], h["lip"], h["t"], h["y_back"]
            cube("fogantyu_talp", (cx - L / 2, yb - Dd, z - tt, L, Dd, tt), M["handle"], 0)
            cube("fogantyu_perem", (cx - L / 2, yb - Dd, z - tt, L, tt, lip), M["handle"], 0)
    # ezüst díszcsíkok a szélső tolóajtókon
    for x0, w in ((2, 798), (1702, 796)):
        for zz in (400, 900, 1400, 1900):
            cube("csik", (x0, -1.5, zz - 4, w, 2, 8), M["alu"], 0)
    # lábazat
    cube("labazat", (0, 10, 0, 2500, 590, 40), M["cashmere"], 0)
    # szoba
    cube("padlo", (-2500, -4000, -20, 7500, 4700, 20), M["floor"], 0)
    cube("hatfal", (-2500, 600, 0, 7500, 100, CEIL * 1000), M["accent"], 0)
    cube("balfal", (-900, -4000, 0, 100, 4700, CEIL * 1000), M["wall"], 0)
    cube("elofal", (-2500, -4100, 0, 7500, 100, CEIL * 1000), M["wall"], 0)
    cube("plafon", (-2500, -4000, CEIL * 1000, 7500, 4700, 30), M["ceiling"], 0)
    cube("szegely", (-800, 590, 0, 7000, 12, 70), M["ceiling"], 0)


def lights():
    bpy.ops.object.light_add(type="AREA", location=(0.6, -3.2, 2.4))
    a = bpy.context.object; a.data.energy = 160; a.data.size = 3.0
    a.rotation_euler = (math.radians(70), 0, math.radians(-15))
    bpy.ops.object.light_add(type="AREA", location=(3.8, -2.0, 1.8))
    b = bpy.context.object; b.data.energy = 60; b.data.size = 2.0
    b.rotation_euler = (math.radians(75), 0, math.radians(50))
    bpy.ops.object.light_add(type="POINT", location=(1.25, -1.5, 2.45))
    c = bpy.context.object; c.data.energy = 12; c.data.shadow_soft_size = 0.5


def camera(kind):
    cams = {
        "front": ((1.25, -3.9, 1.45), (1.25, 0.3, 1.40), 26),
        "three": ((3.9, -3.6, 1.55), (1.15, 0.3, 1.55), 28),
        "open":  ((3.3, -2.9, 1.75), (1.2, 0.3, 2.25), 30),
        "low":   ((2.2, -1.6, 1.05), (1.25, 0.3, 2.3), 22),
        "top":   ((1.25, -2.4, 2.25), (1.25, 0.3, 2.3), 30),
    }
    loc, tgt, lens = cams[kind]
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    bpy.ops.object.empty_add(location=tgt); t = bpy.context.object
    tc = cam.constraints.new("TRACK_TO"); tc.target = t
    tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
    cam.data.lens = lens / 1.0 * 1.0
    cam.data.sensor_width = 36
    bpy.context.scene.camera = cam
    return cam


if __name__ == "__main__":
    sc = reset(); M.update(make_mats()); build(); lights(); camera(view)
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    print("render:", out)
