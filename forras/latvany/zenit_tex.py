"""Textúra-csempék (felülnézet, puha stúdiófény). python zenit_tex.py <out.png> <tex>"""
import sys, math, bpy, json
sys.argv = [sys.argv[0], "/dev/null", json.dumps({"mood": "studio"})] + sys.argv[1:]
import zenit_scene as Z
out, tex = sys.argv[3], sys.argv[4]
sc = Z.reset(); sc.render.resolution_x = sc.render.resolution_y = 900; sc.cycles.samples = 16
m = Z.TEX[tex]("t")
bpy.ops.mesh.primitive_plane_add(size=0.6, location=(0, 0, 0)); p = bpy.context.object; p.data.materials.append(m)
bpy.ops.object.light_add(type="AREA", location=(-0.6, -0.5, 1.0)); l = bpy.context.object
l.data.energy = 45; l.data.size = 1.2; l.rotation_euler = (math.radians(35), math.radians(-30), 0); l.data.color = Z.srgb("#FFF1DE")
bpy.ops.object.camera_add(location=(0, 0, 0.9)); c = bpy.context.object; c.data.lens = 85; sc.camera = c
sc.render.filepath = out; bpy.ops.render.render(write_still=True); print("render:", out)
