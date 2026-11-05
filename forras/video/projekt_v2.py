"""ZENIT projektvideó v2 – valódi fotók és felvételek, alapító, weboldal, tervező, szerelés; férfi narráció (Piper/Imre), zenei alap, VTT felirat.
Használat: python3 projekt_v2.py overlays | render | audio | final"""
import sys, os, json, glob, subprocess, wave, pathlib
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
W, H, FPS = 1920, 1080, 25
D = "/home/claude/v3"; OV = D + "/ov"; os.makedirs(OV, exist_ok=True)
HANG = "/home/claude/hang_imre"; R = "/home/claude/zenit2/assets/img/r2/"; OWN = "/home/claude/zenit2/assets/img/own/"; WEB = D + "/web/"; SRC = D + "/src/"
FONTS = pathlib.Path('/home/claude/zenit2/assets/fonts').as_uri()
NARR = dict(json.load(open(D + "/narracio_v2.json", encoding="utf8"))["projekt"])
X = 12  # áttűnés kockában

def narr_len(k):
    with wave.open(f"{HANG}/{k}.wav") as w: return w.getnframes() / w.getframerate()

# ------------------------------------------------------------------ szakaszok
SEG = [("title", None, 4.6), ("portrait", "n01", None), ("clutter", "n02", None), ("ba", "n03", None), ("laptop", "n04", None), ("renders", "n05", None),
       ("web", "n06", None), ("cfg", "n07", None), ("asm", "n08", None), ("pal", "n09", None), ("close", "n10", None)]
DUR = []
for name, k, d in SEG:
    if d is None: d = narr_len(k) + (4.2 if name == "close" else 1.5)
    DUR.append(d)
NF = [int(round(d * FPS)) for d in DUR]
START = np.cumsum([0] + [n - X for n in NF[:-1]])          # kockában; a szakaszok X kockát átfednek
TOTAL = int(START[-1] + NF[-1])
CHAP = {"clutter": "01 · A probléma", "ba": "02 · Az ötlet", "laptop": "03 · A modell", "renders": "04 · A látvány", "web": "05 · A weboldal",
        "cfg": "06 · A tervező", "asm": "07 · A szerelés", "pal": "08 · Az anyagok"}
TAGS = {"close": "Látványterv · kasmír, esti fény", "clutter": "Valódi felvétel", "laptop": "Munka közben", "renders": "Látványterv · Blender", "web": "mbolgar11.github.io/zenit", "cfg": "Élő 3D tervező", "asm": "Szerelési animáció"}

# ------------------------------------------------------------------ feliratok (Chromium → PNG)
def overlays():
    ff = lambda fam, f, w, st: (f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};src:url({FONTS}/{f}-latin-ext-{w}-{st}.woff2);unicode-range:U+0100-024F,U+2010-2027}}'
                                f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};src:url({FONTS}/{f}-latin-{w}-{st}.woff2)}}')
    css = ff('CG', 'cormorant-garamond', 300, 'normal') + ff('CG', 'cormorant-garamond', 300, 'italic') + ff('In', 'inter', 400, 'normal') + ff('In', 'inter', 500, 'normal') + '''
html,body{margin:0;background:transparent}.o{display:inline-block;color:#fff}
.k{font:500 15px In;letter-spacing:.32em;text-transform:uppercase;color:#C2A274}
.ch{display:flex;align-items:center;gap:16px;padding:12px 18px;background:rgba(20,17,14,.5)}.ch i{display:block;width:46px;height:1px;background:#C2A274}
.tag{font:500 13px In;letter-spacing:.24em;text-transform:uppercase;color:#fff;background:rgba(20,17,14,.55);padding:10px 14px}
.ml{display:flex;align-items:center}.ml i{display:block;width:2px;height:24px;background:#C2A274}.ml b{display:block;flex:1;height:2px;background:#C2A274}
.wm{font:300 150px/1 CG;letter-spacing:.42em;margin-right:-.42em;color:#fff}
.title{text-align:center;padding:40px}.t{font:300 58px/1.15 CG}.t em{font-style:italic;color:#E3CBA4}.s{font:400 20px In;color:#D9CFC0;margin-top:22px;letter-spacing:.04em}
.lt{padding:30px 10px}.lt .n{font:300 96px/1 CG;color:#fff}.lt .r{font:500 14px In;letter-spacing:.32em;text-transform:uppercase;color:#C2A274;margin-top:18px}
.url{font:400 26px In;letter-spacing:.14em;color:#C2A274;margin-top:34px}'''
    logo = '<div style="display:inline-block"><div class="ml" style="margin-bottom:34px"><i></i><b></b><i></i></div><div class="wm">ZENIT</div></div>'
    items = {"title": f'<div class="title">{logo}<div class="k" style="margin-top:46px">Egy AI-kihívás története · 2026</div><div class="t" style="margin-top:20px">Fél méter, <em>a plafonig.</em></div></div>',
             "lt": '<div class="lt"><div class="ml" style="width:120px;margin-bottom:26px"><i></i><b></b></div><div class="n">Milán</div><div class="r">a ZENIT ötletgazdája</div></div>',
             "close": f'<div class="title">{logo}<div class="t" style="margin-top:44px;font-size:52px"><em>Ahol a szekrényed véget ér, ott kezdődünk.</em></div><div class="url">mbolgar11.github.io/zenit</div></div>',
             "tag_foto": '<div class="tag">Valódi fotó</div>', "tag_mont": '<div class="tag">Fotómontázs · méretpontos modell</div>'}
    for k, v in CHAP.items(): items["ch_" + k] = f'<div class="ch"><i></i><span class="k">{v}</span></div>'
    for k, v in TAGS.items(): items["tag_" + k] = f'<div class="tag">{v}</div>'
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>' + "".join(f'<div id="{k}" class="o">{v}</div><br>' for k, v in items.items()) + '</body></html>'
    open(D + "/ov.html", "w", encoding="utf8").write(html)
    js = ('const {chromium}=require("playwright");(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});'
          f'await p.goto("file://{D}/ov.html");await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);'
          f'for(const id of {json.dumps(list(items))})await p.locator("#"+id).screenshot({{path:"{OV}/"+id+".png",omitBackground:true}});await b.close()}})();')
    open(D + "/ov.js", "w").write(js); subprocess.run(["node", D + "/ov.js"], check=True, cwd="/tmp"); print("ok overlays", len(items))

# ------------------------------------------------------------------ segédek
def sm(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
_cache = {}
def load(p, mode="RGB"):
    if p not in _cache:
        if len(_cache) > 40: _cache.clear()
        _cache[p] = Image.open(p).convert(mode)
    return _cache[p]
def cover(im, z=1.0, px=0.0, py=0.0, w=W, h=H):
    sw, sh = im.size; s = max(w / sw, h / sh) * z; vw, vh = w / s, h / s
    x0 = (sw - vw) * (0.5 + px); y0 = (sh - vh) * (0.5 + py)
    return im.transform((w, h), Image.AFFINE, (1 / s, 0, x0, 0, 1 / s, y0), resample=Image.BICUBIC)
def ov(base, name, a=1.0, xy=None, anchor="bl", pad=90):
    if a <= 0.01: return base
    o = load(f"{OV}/{name}.png", "RGBA")
    if a < 1: o = o.copy(); o.putalpha(o.getchannel("A").point(lambda v: int(v * a)))
    if xy is None:
        xy = {"bl": (pad, H - o.height - pad), "tl": (pad - 4, pad - 30), "br": (W - o.width - pad + 30, H - o.height - pad + 40), "c": ((W - o.width) // 2, (H - o.height) // 2)}[anchor]
    base.paste(o, (int(xy[0]), int(xy[1])), o); return base
def dark(im, k): return ImageEnhance.Brightness(im).enhance(k)
def frames_of(folder): return sorted(glob.glob(folder + "/*.jpg"))
def pick(lst, u): return lst[min(len(lst) - 1, int(u * len(lst)))]
ESP = (20, 17, 14)

# ------------------------------------------------------------------ szakaszok képe (u: 0..1 a szakaszon belül)
def seg_frame(name, u, d):
    if name == "title":
        im = dark(cover(load(R + "hero_evening.jpg"), 1.04 + 0.05 * u), 0.42)
        return ov(im, "title", sm((u * d - .4) / .9) * sm((d - u * d) / .7), anchor="c")
    if name == "portrait":
        # 1. snitt: valódi portré az irodában (lassú kihúzás a festménytől az arcig) – 2. snitt: műhelyportré, a szerszámfaltól lefelé az arcra
        def office(v):
            p = load(OWN + "portre_iroda.jpg"); bg = load(OWN + "portre_iroda_bg.jpg")
            im = bg.copy(); fh = H; fw = int(p.width * fh / p.height); fg = cover(p, 1.0 + 0.06 * v, -0.02 * v, 0, fw, fh)
            m = Image.new("L", (fw, fh), 255); dm = ImageDraw.Draw(m)
            for x in range(160): dm.line([(x, 0), (x, fh)], fill=int(255 * x / 160))
            im.paste(fg, (W - fw, 0), m); return im
        def shop(v): return cover(load(OWN + "alapito.jpg"), 1.04 - 0.04 * sm(v), 0.04, -0.30 + 0.39 * sm(v))
        if u < 0.5: im = office(u / 0.56)
        elif u > 0.62: im = shop((u - 0.56) / 0.44)
        else: im = Image.blend(office(u / 0.56), shop((u - 0.56) / 0.44), sm((u - 0.5) / 0.12))
        g = Image.new("L", (W, H), 0); ImageDraw.Draw(g).rectangle([0, 0, 900, H], fill=150); g = g.filter(ImageFilter.GaussianBlur(220))
        im.paste(Image.new("RGB", (W, H), ESP), (0, 0), g)
        return ov(im, "lt", sm((u * d - .7) / .8) * sm((d * 0.53 - u * d) / .5), xy=(150, H - 430))
    if name == "clutter":
        lst = frames_of(SRC + "CA") + frames_of(SRC + "CB")[:26]; im = cover(load(pick(lst, u)), 1.0 + 0.04 * u)
        return im
    if name == "ba":
        b = cover(load(OWN + "before_real.jpg"), 1.02 + 0.03 * u); a = cover(load(OWN + "after_real.jpg"), 1.02 + 0.03 * u)
        w = sm((u - 0.33) / 0.3); xcut = int(W * w)
        im = b.copy()
        if xcut > 0: im.paste(a.crop((0, 0, xcut, H)), (0, 0))
        if 0 < w < 1: ImageDraw.Draw(im).rectangle([xcut - 2, 0, xcut + 1, H], fill=(194, 162, 116))
        im = ov(im, "tag_foto", 1 - sm((u - .3) / .1), anchor="br"); im = ov(im, "tag_mont", sm((u - .62) / .1), anchor="br")
        return im
    if name == "laptop":
        segs = [("L1", 0.36), ("L2", 0.30), ("L4", 0.34)]; acc = 0
        for k, f in segs:
            if u < acc + f or k == "L4":
                v = (u - acc) / f; break
            acc += f
        bg = load(pick(frames_of(SRC + k + "bg"), v)).copy(); card = load(pick(frames_of(SRC + k), v))
        sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).rounded_rectangle([W // 2 - 340, 130, W // 2 + 380, 1010], 24, fill=110)
        bg.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), sh.filter(ImageFilter.GaussianBlur(55)))
        m = Image.new("L", card.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, card.width - 1, card.height - 1], 18, fill=255)
        bg.paste(card, (W // 2 - 360, 90), m); return bg
    if name == "renders":
        L = ["SIDE", "hinge_in", "macro_handle", "b_open_led"]; n = len(L); f = u * n; i = min(n - 1, int(f)); v = f - i
        def shot(j, vv):
            if L[j] == "SIDE": return cover(load(pick(frames_of(SRC + "SIDE"), vv)), 1.0 + 0.04 * vv)
            return cover(load(R + L[j] + ".jpg"), 1.03 + 0.06 * vv, 0.04 * (vv - .5) * (1 if j % 2 else -1), 0)
        im = shot(i, v)
        if v > 0.82 and i < n - 1: im = Image.blend(im, shot(i + 1, 0), sm((v - .82) / .18))
        return im
    if name == "web":
        if u < 0.45:
            v = sm(u / 0.45); top = load(WEB + "idx_top.jpg"); y = int(v * (top.height - H) * 0.75)
            return top.crop((0, y, W, y + H))
        return load(pick(sorted(glob.glob(WEB + "asm_*.jpg")), (u - .45) / .55))
    if name == "cfg":
        if u < 0.3: return cover(load(WEB + "cfg.jpg"), 1.0 + 0.06 * u / 0.3, 0.1 * u, 0)
        return cover(load(pick(frames_of("/home/claude/video2/open"), (u - .3) / .7)))
    if name == "asm":
        if u < 0.74: return cover(load(pick(frames_of("/home/claude/video2/asm"), 0.04 + u / 0.74 * 0.92)))
        return cover(load(WEB + "manual.jpg"), 1.02 + 0.08 * (u - .74) / .26, 0, -0.1 * (u - .74) / .26)
    if name == "pal":
        return load(pick(sorted(glob.glob(WEB + "pal_*.jpg")), 0.05 + u * 0.95))
    if name == "close":
        # zárósnitt: a legszebb, élethű render, lassú ráközelítés; a logó alatt is látszik
        im = cover(load(R + "hero_evening.jpg"), 1.02 + 0.09 * sm(u), -0.03 * u, 0)
        k = sm((u * d - (d - 3.8)) / 1.4); im = Image.blend(im, Image.new("RGB", (W, H), ESP), k * 0.58)
        return ov(im, "close", sm((u * d - (d - 3.0)) / 0.9), anchor="c")

def decorate(name, u, d, im):
    t = u * d
    if name in CHAP: im = ov(im, "ch_" + name, sm((t - .3) / .6) * sm((d - t - .4) / .6), anchor="tl")
    if name in TAGS:
        end = 4.2 if name == "close" else 0.4
        im = ov(im, "tag_" + name, sm((t - .5) / .6) * sm((d - t - end) / .5), anchor="br")
    return im

def frame(g):
    out = None
    for i, (name, k, _) in enumerate(SEG):
        s, n = START[i], NF[i]
        if s <= g < s + n:
            u = (g - s) / max(1, n - 1); im = decorate(name, u, DUR[i], seg_frame(name, u, DUR[i]).convert("RGB"))
            if out is None: out = im
            else: out = Image.blend(out, im, sm((g - s + 1) / (X + 1)))
    if g < 12: out = Image.blend(Image.new("RGB", (W, H)), out, g / 12)
    if g > TOTAL - 18: out = Image.blend(Image.new("RGB", (W, H)), out, max(0, (TOTAL - g) / 18))
    return out

def render():
    out = D + "/projekt_v2_kep.mp4"
    vf = "colorbalance=rs=0.025:gs=0:bs=-0.03:rh=0.01:bh=-0.02,eq=saturation=0.92:gamma=0.98,vignette=angle=PI/5.2,noise=alls=3:allf=t"
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-vf", vf, "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for g in range(TOTAL):
        p.stdin.write(frame(g).tobytes())
        if g % 250 == 0: print(g, "/", TOTAL, flush=True)
    p.stdin.close(); assert p.wait() == 0; print("ok video", TOTAL / FPS)

SR = 48000
def rd(path):
    with wave.open(path) as w: sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return np.interp(np.arange(int(len(x) * SR / sr)) / SR * sr, np.arange(len(x)), x)

def music(total):
    sys.path.insert(0, "/home/claude/video"); from compose import pad
    y = pad(total, level=0.05, bpm_chord=6.0)
    t = np.arange(len(y)) / SR; rng = np.random.default_rng(11); hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    seq = [69, 72, 76, 79, 77, 72, 74, 76, 67, 71, 74, 79]           # lágy zongora-arpeggio
    for k, st in enumerate(np.arange(3.0, total - 4, 1.5)):
        m = seq[k % len(seq)] - 12; i0 = int(st * SR); n = int(3.2 * SR); tt = np.arange(n) / SR
        v = (np.sin(2 * np.pi * hz(m) * tt) + 0.35 * np.sin(4 * np.pi * hz(m) * tt * 1.0007) + 0.12 * np.sin(6 * np.pi * hz(m) * tt)) * np.exp(-tt * 1.9) * (1 - np.exp(-tt * 180))
        y[i0:i0 + n] += v[:max(0, len(y) - i0)] * 0.018 * (0.8 + 0.4 * rng.random())
    return y

def audio():
    total = TOTAL / FPS; vo = np.zeros(int(total * SR) + SR); cues = []
    for i, (name, k, _) in enumerate(SEG):
        if not k: continue
        s0 = START[i] / FPS + 0.55; x = rd(f"{HANG}/{k}.wav"); j = int(s0 * SR); vo[j:j + len(x)] += x * 0.95
        cues.append((s0, s0 + len(x) / SR, NARR[k]))
    mus = music(len(vo) / SR)
    env = np.convolve(np.abs(vo), np.ones(4800) / 4800, "same"); duck = np.convolve(1 - 0.5 * np.clip(env / 0.03, 0, 1), np.ones(9600) / 9600, "same")
    mix = np.tanh((vo + mus * duck)[:int(total * SR)] * 1.15) / np.tanh(1.15)
    fade = np.ones_like(mix); nf = int(1.2 * SR); fade[-nf:] = np.linspace(1, 0, nf); mix *= fade
    st = (np.stack([mix, mix], 1) * 32767).astype(np.int16)
    with wave.open(D + "/projekt_v2_hang.wav", "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
    # VTT: hosszú mondatok két részre bontva
    def ts(t): return f"{int(t//3600):02d}:{int(t%3600//60):02d}:{t%60:06.3f}"
    out = []; n = 1
    for a, b, txt in cues:
        parts = [txt]
        if len(txt) > 84:
            cut = max((i for i, c in enumerate(txt) if c in ".:–" and 20 < i < len(txt) - 15), key=lambda i: -abs(i - len(txt) / 2), default=None)
            if cut: parts = [txt[:cut + 1].strip(), txt[cut + 1:].strip()]
        L = sum(len(p) for p in parts); t0 = a
        for p in parts:
            t1 = t0 + (b - a) * len(p) / L; out.append(f"{n}\n{ts(t0)} --> {ts(t1 + 0.2)}\n{p}\n"); n += 1; t0 = t1
    open(D + "/projekt.vtt", "w", encoding="utf8").write("WEBVTT\n\n" + "\n".join(out)); print("ok audio", round(total, 2))

def final():
    out = D + "/ZENIT_projektvideo_v2.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", D + "/projekt_v2_kep.mp4", "-i", D + "/projekt_v2_hang.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(START[3] / FPS + DUR[3] * 0.85), "-i", out, "-frames:v", "1", "-q:v", "3", D + "/ZENIT_projektvideo_v2_poster.jpg"], check=True)
    print("ok", out)

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        for g in [int(x) for x in sys.argv[2:]]: frame(g).resize((960, 540)).save(f"{D}/pv_{g}.jpg")
    else: {"overlays": overlays, "render": render, "audio": audio, "final": final}[sys.argv[1]]()
