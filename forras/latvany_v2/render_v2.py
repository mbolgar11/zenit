import json, subprocess, os, time
K = {"body": "#CABCAB", "door": "#C8BAA9"}
J = [
 ("hero_evening", dict(K, cam="hero", mood="evening")),
 ("hero_day", dict(K, cam="hero_wide", mood="day", exposure=-0.5)),
 ("led_detail", dict(K, cam="led", mood="evening", doors=105, led=True, inside=True, exposure=0.2)),
 ("open_led", dict(K, cam="open", mood="evening", doors=100, led=True, inside=True)),
 ("after_day", dict(K, cam="before", mood="day", exposure=-0.5)),
 ("before_day", dict(K, cam="before", mood="day", topper=False, clutter=True, exposure=-0.5)),
 ("story_morning", dict(K, cam="front", mood="morning", exposure=-0.35)),
 ("story_night", dict(K, cam="story_low", mood="night", topper=False, clutter=True)),
 ("mirror_day", dict(K, cam="mirror", mood="day", mirror_doors=[1], exposure=-0.5)),
 ("macro_handle", dict(K, cam="macro_handle", mood="day", props=False, exposure=-0.3, w=1440, h=900)),
 ("macro_edge", dict(K, cam="macro_edge", mood="day", props=False, exposure=-0.3, w=1440, h=900)),
 ("macro_hinge", dict(K, cam="macro_hinge", mood="day", props=False, doors=80, exposure=-0.3, w=1440, h=900)),
 ("exploded_light", dict(K, cam="exploded", mood="studio", explode=1, studio_bg="#E9E3DA", exposure=0.35)),
 ("exploded", dict(K, cam="exploded", mood="studio", explode=1)),
 ("insp_kreta", dict(cam="hero", mood="morning", body="#F1EFEA", exposure=-0.4)),
 ("insp_zsalya", dict(cam="hero", mood="day", body="#A4AD98", handle_col="bronze", wall="#EEE9E1", exposure=-0.45)),
 ("insp_ejkek", dict(cam="hero", mood="evening", body="#273445", handle_col="bronze", wall="#E2DCD3")),
 ("insp_tolgy", dict(cam="hero", mood="day", body="oak", door="oak", floor="oak", handle_col="black", wall="#E8E1D6", exposure=-0.45)),
 ("insp_grafit_dio", dict(cam="hero", mood="evening", body="#4A4846", door="walnut", handle_col="black", wall="#D6D0C7")),
]
os.makedirs("/home/claude/zr2/log", exist_ok=True)
for name, o in J:
    out = f"/home/claude/zr2/{name}.png"
    if os.path.exists(out): continue
    o = dict({"samples": 26, "w": 1600, "h": 1000}, **o)
    t = time.time()
    subprocess.run(["python", "zenit_scene.py", out, json.dumps(o)], stdout=open(f"/home/claude/zr2/log/{name}.log", "w"), stderr=subprocess.STDOUT)
    open("/home/claude/zr2/progress.txt", "a").write(f"{name} {time.time()-t:.0f}s\n")
