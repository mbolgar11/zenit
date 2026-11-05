import json, subprocess, os, time
K = {"body": "#CABCAB", "door": "#C8BAA9"}
B = {"layout": "B", "floor": "walnut"}
J = [
 ("b_kasmir_evening", dict(K, **B, cam="left", mood="evening", wall="#B9AEA1")),
 ("b_open_led", dict(K, **B, cam="open", mood="evening", doors=100, led=True, inside=True, wall="#B9AEA1")),
 ("b_zsalya_day", dict(B, cam="side", mood="day", body="#A4AD98", handle_col="bronze", wall="#D4CBBE", **{"floor": "oak"}, exposure=-0.85, art="#8C7A62")),
]
for name, o in J:
    out = f"/home/claude/zr2/{name}.png"
    o = dict({"samples": 26, "w": 1600, "h": 1000}, **o)
    t = time.time()
    subprocess.run(["python", "zenit_scene.py", out + ".tmp.png", json.dumps(o)], stdout=open(f"/home/claude/zr2/log/{name}_b.log", "w"), stderr=subprocess.STDOUT)
    if os.path.exists(out + ".tmp.png"): os.replace(out + ".tmp.png", out)
    open("/home/claude/zr2/progress.txt", "a").write(f"{name} (v3b) {time.time()-t:.0f}s\n")
