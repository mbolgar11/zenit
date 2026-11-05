import json, subprocess, os, time
K = {"body": "#CABCAB", "door": "#C8BAA9"}
B = {"layout": "B", "floor": "walnut"}
J = [
 ("hinge_in", dict(K, cam="hinge_in", mood="day", doors=85, props=False, inside=True, exposure=-0.2, w=1440, h=900)),
 ("b_kasmir_evening", dict(K, **B, cam="left", mood="evening", wall="#B9AEA1")),
 ("b_open_led", dict(K, **B, cam="open", mood="evening", doors=100, led=True, inside=True, wall="#B9AEA1")),
 ("b_zsalya_day", dict(B, cam="side", mood="day", body="#A4AD98", handle_col="bronze", wall="#E2DCD2", **{"floor": "oak"}, exposure=-0.45, art="#8C7A62")),
 ("v_tolgy_day", dict(cam="front_wide", mood="day", body="oak", door="oak", handle_col="black", wall="#D9D0C4", exposure=-0.45)),
 ("b_ejkek_evening", dict(B, cam="hero", mood="evening", body="#273445", handle_col="bronze", wall="#CFC5B8", bench="#B9A88F")),
 ("v_grafit_dio", dict(cam="low_up", mood="evening", body="#4A4846", door="walnut", handle_col="black", wall="#C9BFB3")),
 ("story_night", dict(K, cam="story_low", mood="night", topper=False, clutter=True)),
 ("mirror_day", dict(K, cam="mirror", mood="day", mirror_doors=[1], exposure=-0.5)),
 ("macro_handle", dict(K, cam="macro_handle", mood="day", props=False, exposure=-0.3, w=1440, h=900)),
 ("macro_edge", dict(K, cam="macro_edge", mood="day", props=False, exposure=-0.3, w=1440, h=900)),
 ("exploded_light", dict(K, cam="exploded", mood="studio", explode=1, studio_bg="#E9E3DA", exposure=0.35)),
]
os.makedirs("/home/claude/zr2/log", exist_ok=True)
for name, o in J:
    out = f"/home/claude/zr2/{name}.png"
    if os.path.exists(out): continue
    o = dict({"samples": 26, "w": 1600, "h": 1000}, **o)
    t = time.time()
    subprocess.run(["python", "zenit_scene.py", out, json.dumps(o)], stdout=open(f"/home/claude/zr2/log/{name}.log", "w"), stderr=subprocess.STDOUT)
    open("/home/claude/zr2/progress.txt", "a").write(f"{name} {time.time()-t:.0f}s\n")
