"""ZENIT szerelési videó: bevezető + valós 3D szerelési animáció (a tervezőből) feliratokkal + zárókép, narráció + zenei alap.
Használat: python3 asm_video.py overlays | render | audio | final"""
import sys, os, json, glob, subprocess, wave, pathlib
import numpy as np
from PIL import Image, ImageFilter
W, H, FPS = 1920, 1080, 25
D = "/home/claude/video2"; FR = D + "/asm"; OV = D + "/ov"; os.makedirs(OV, exist_ok=True)
HANG = "/mnt/user-data/uploads/Szekrény/07_Video/_hang_szereles"
R2 = "/home/claude/zenit2/assets/img/r2/"
T = json.load(open(D + "/asm_timing.json")); DURS = T["durs"]
STEPS = [("Fenéklap és tiplik", "16 db 8×35 fatipli · gumikalapács"), ("Oldallapok", "kötésenként 2 konfirmát 7×50 · kívülről"),
         ("Közfalak", "a tiplikre ültetve · alulról rögzítve"), ("Tetőlap", "oldallapokon és közfalakon át"),
         ("Hátfal, majd fel a szekrényre", "50 hátfalszeg · 2 fő emel · 4 csavar 3,5×30 belülről"), ("Polc", "oldalanként 3 polctartó csap"),
         ("Ajtók", "rápattintva a Häfele talpakra · hézag 3 mm"), ("Ellenőrzés", "egyenes vonalak · csendes, fékes zárás"),
         ("Fény és befejezés", "LED · takaróléc · védőfólia le")]
INTRO, OUTRO = 6.4, 5.4
ASM = sum(DURS) + 0.5
FONTS = pathlib.Path('/home/claude/zenit2/assets/fonts').as_uri()

def overlays():
    ff = lambda fam, f, w, st: (f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};src:url({FONTS}/{f}-latin-ext-{w}-{st}.woff2);unicode-range:U+0100-024F,U+2010-2027}}'
                                f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};src:url({FONTS}/{f}-latin-{w}-{st}.woff2)}}')
    css = ff('CG', 'cormorant-garamond', 300, 'normal') + ff('CG', 'cormorant-garamond', 300, 'italic') + ff('In', 'inter', 400, 'normal') + ff('In', 'inter', 500, 'normal') + '''
html,body{margin:0;background:transparent}.o{display:inline-block}
.cap{width:1920px;height:190px;box-sizing:border-box;padding:34px 120px;background:linear-gradient(0deg,rgba(20,17,14,.9),rgba(20,17,14,.72));color:#fff;display:flex;align-items:center;gap:40px}
.no{font:300 86px/1 CG;color:#C2A274;font-variant-numeric:lining-nums;min-width:120px}
.k{font:500 15px In;letter-spacing:.3em;text-transform:uppercase;color:#C2A274}
.t{font:300 50px/1.1 CG;margin-top:8px}.s{font:400 20px In;color:#D9CFC0;margin-top:8px;font-variant-numeric:lining-nums}
.ml{display:flex;align-items:center}.ml i{display:block;width:2px;height:24px;background:#C2A274}.ml b{display:block;flex:1;height:2px;background:#C2A274}
.wm{font:300 150px/1 CG;letter-spacing:.42em;margin-right:-.42em;color:#fff}
.title{text-align:center;color:#fff}.title .t{font-size:84px}.title em{font-style:italic;color:#E3CBA4}
.url{font:400 28px In;letter-spacing:.12em;color:#C2A274;margin-top:34px}'''
    logo = '<div style="display:inline-block"><div class="ml" style="margin-bottom:34px"><i></i><b></b><i></i></div><div class="wm">ZENIT</div></div>'
    items = {f"cap{i}": f'<div class="cap"><div class="no">{i + 1:02d}</div><div><div class="k">Szerelés · {i + 1} / 9</div><div class="t">{t}</div><div class="s">{s}</div></div></div>' for i, (t, s) in enumerate(STEPS)}
    items["intro"] = f'<div class="title" style="padding:40px">{logo}<div class="k" style="margin-top:46px">Szerelési útmutató</div><div class="t" style="margin-top:18px">Három óra. Két ember. <em>Egy csendes szekrény.</em></div><div class="s" style="margin-top:22px">Referencia-darab · 250 × 53 × 60 cm · 3 ajtó · kasmír</div></div>'
    items["outro"] = f'<div class="title" style="padding:40px">{logo}<div class="t" style="margin-top:44px;font-size:56px"><em>Ahol a szekrényed véget ér, ott kezdődünk.</em></div><div class="url">mbolgar11.github.io/zenit</div></div>'
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>' + "".join(f'<div id="{k}" class="o">{v}</div><br>' for k, v in items.items()) + '</body></html>'
    open(D + "/ov.html", "w", encoding="utf8").write(html)
    js = ('const {chromium}=require("playwright");(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});'
          f'await p.goto("file://{D}/ov.html");await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);'
          f'for(const id of {json.dumps(list(items))})await p.locator("#"+id).screenshot({{path:"{OV}/"+id+".png",omitBackground:true}});await b.close()}})();')
    open(D + "/ov.js", "w").write(js)
    subprocess.run(["node", D + "/ov.js"], check=True, cwd="/tmp/claude-0/-home-claude/d203fd6a-2896-55a0-bc1b-23668e704c22/scratchpad"); print("ok overlays")

def sm(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def cover(im, z=1.0):
    sw, sh = im.size; s = max(W / sw, H / sh) * z; vw, vh = W / s, H / s
    return im.transform((W, H), Image.AFFINE, (1 / s, 0, (sw - vw) / 2, 0, 1 / s, (sh - vh) / 2), resample=Image.BICUBIC)
def ovl(base, name, a, pos="bottom", dy=0):
    o = Image.open(f"{OV}/{name}.png").convert("RGBA")
    if a < 1: o.putalpha(o.getchannel("A").point(lambda v: int(v * a)))
    x = (W - o.width) // 2; y = H - o.height if pos == "bottom" else (H - o.height) // 2 + dy
    base.paste(o, (x, y), o); return base
def black(im, k): return Image.blend(Image.new("RGB", (W, H)), im, k) if k < 1 else im

def frames():
    fs = sorted(glob.glob(FR + "/*.jpg")); hero = Image.open(R2 + "hero_evening.jpg").convert("RGB")
    nI, nA, nO = int(INTRO * FPS), int(ASM * FPS), int(OUTRO * FPS)
    for f in range(nI):  # bevezető: lassú közelítés a renderen, sötétített, cím
        t = f / FPS; im = Image.blend(cover(hero, 1.0 + 0.05 * t / INTRO), Image.new("RGB", (W, H), (14, 12, 10)), 0.55)
        im = ovl(im, "intro", sm((t - .3) / .8) * sm((INTRO - t) / .6), "center")
        yield black(im, min(sm(t / .5), sm((INTRO - t) / .4) + .0))
    starts = np.cumsum([0] + DURS)
    for f in range(nA):
        t = f / FPS; im = Image.open(fs[min(f, len(fs) - 1)]).convert("RGB").resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.0, 35, 2))
        i = int(np.searchsorted(starts, t, side="right") - 1); i = max(0, min(8, i)); lt = t - starts[i]
        a = min(sm(lt / .45), sm((DURS[i] - lt) / .35)) if i < 8 else sm(lt / .45) * sm((ASM - t) / .5)
        im = ovl(im, f"cap{i}", a)
        yield black(im, min(sm(t / .4), sm((ASM - t) / .4)))
    for f in range(nO):
        t = f / FPS; im = Image.new("RGB", (W, H), (20, 17, 14)); im = ovl(im, "outro", sm((t - .2) / .8), "center")
        yield black(im, sm((OUTRO - t) / .8))

def render():
    out = D + "/szereles_video.mp4"; tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    n = 0
    for im in frames(): p.stdin.write(im.tobytes()); n += 1
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out); print("ok video", n, "kocka")

SR = 48000
def rd(path):
    with wave.open(path) as w: sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return np.interp(np.arange(int(len(x) * SR / sr)) / SR * sr, np.arange(len(x)), x)

def audio():
    sys.path.insert(0, "/home/claude/video"); from compose import pad
    total = INTRO + ASM + OUTRO; vo = np.zeros(int(total * SR) + SR)
    starts = [0.5] + [INTRO + s + 0.35 for s in np.cumsum([0] + DURS[:-1])] + [INTRO + ASM + 0.6]
    for i, s in enumerate(starts):
        x = rd(f"{HANG}/a{i:02d}.wav"); j = int(s * SR); vo[j:j + len(x)] += x * 0.92
    mus = pad(len(vo) / SR, level=0.06, bpm_chord=5.0)
    env = np.convolve(np.abs(vo), np.ones(4800) / 4800, "same"); duck = np.convolve(1 - 0.55 * np.clip(env / 0.03, 0, 1), np.ones(9600) / 9600, "same")
    mix = np.tanh((vo + mus * duck)[:int(total * SR)] * 1.1) / np.tanh(1.1)
    st = (np.stack([mix, mix], 1) * 32767).astype(np.int16)
    with wave.open(D + "/szereles_hang.wav", "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
    print("ok audio", round(total, 2))

def final():
    out = D + "/ZENIT_szerelesi_video.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", D + "/szereles_video.mp4", "-i", D + "/szereles_hang.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out + ".tmp.mp4"], check=True)
    os.replace(out + ".tmp.mp4", out)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "20", "-i", out, "-frames:v", "1", "-q:v", "3", D + "/ZENIT_szerelesi_video_poster.jpg"], check=True)
    print("ok", out)

if __name__ == "__main__":
    {"overlays": overlays, "render": render, "audio": audio, "final": final}[sys.argv[1]]()
