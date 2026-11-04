"""ZENIT videók összeállítása: jelenetenként egy MP4 (1920×1080, 30 fps, x264 CRF 18), majd concat + hang.
Használat: python3 compose.py projekt [s1 s2 …] | promo [p1 …] | audio | final"""
import sys, os, json, glob, math, subprocess, functools, wave
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

W, H, FPS = 1920, 1080, 30
V = '/home/claude/video'; R = '/home/claude/zenit_renders'; FR = V + '/frames'; OV = V + '/ov'
D10 = '/mnt/attach/outputs/v10final'
HANG = '/mnt/user-data/uploads/Szekrény/07_Video/_hang_anna'
BG = (20, 18, 16)

def sm(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)

@functools.lru_cache(maxsize=64)
def load(path, mode='RGB'):
    return Image.open(path).convert(mode)

def cover(im, z=1.0, cx=0.5, cy=0.5):
    """Ken Burns: im kitölti a képkockát, z-szeres nagyítással, (cx,cy) középpont körül."""
    sw, sh = im.size; s = max(W / sw, H / sh) * z
    vw, vh = W / s, H / s  # látható forrásterület
    x0 = min(max(cx * sw - vw / 2, 0), sw - vw); y0 = min(max(cy * sh - vh / 2, 0), sh - vh)
    return im.transform((W, H), Image.AFFINE, (1 / s, 0, x0, 0, 1 / s, y0), resample=Image.BICUBIC)

@functools.lru_cache(maxsize=32)
def paper(path, hmax=900, wmax=1700):
    """Rajz/képernyőkép 'kártyaként' sötét háttéren, árnyékkal (nagyobb vásznon a Ken Burnshoz)."""
    im = load(path); s = min(hmax / im.height, wmax / im.width); im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    return im

def card_frame(items, z, align='c', dy=0):
    """items: [(path, hmax, wmax)] egymás mellett középre; z: lassú nagyítás."""
    can = Image.new('RGB', (W, H), BG)
    ims = [paper(*it) for it in items]; gap = 60
    tw = sum(i.width for i in ims) + gap * (len(ims) - 1); x0 = (W - tw) // 2 if align == 'c' else W - 120 - tw; x = x0
    sh = Image.new('L', (W, H), 0)
    for im in ims:
        y = (H - im.height) // 2 + dy
        sh.paste(255, (x + 10, y + 18, x + im.width + 10, y + im.height + 18)); x += im.width + gap
    sh = sh.filter(ImageFilter.GaussianBlur(26)); can.paste((0, 0, 0), (0, 0), sh.point(lambda v: int(v * 0.6)))
    x = x0
    for im in ims:
        can.paste(im, (x, (H - im.height) // 2 + dy)); x += im.width + gap
    if z != 1.0: can = cover(can, z)
    return can

# ---------------------------------------------------------------- klipek (t: jeleneten belüli idő)
def still(path, z0=1.0, z1=1.06, c0=(.5, .5), c1=(.5, .5), dim=0.0, sat=1.0):
    def f(t, a, b):
        u = (t - a) / max(1e-6, b - a); e = sm(u) * 0.5 + u * 0.5
        im = cover(load(path), z0 + (z1 - z0) * e, c0[0] + (c1[0] - c0[0]) * e, c0[1] + (c1[1] - c0[1]) * e)
        if sat != 1.0: im = ImageEnhance.Color(im).enhance(sat)
        if dim: im = Image.blend(im, Image.new('RGB', (W, H), BG), dim)
        return im
    return f

def cards(items, z0=1.0, z1=1.05, align='c', dy=0):
    def f(t, a, b):
        u = (t - a) / max(1e-6, b - a); return card_frame(tuple(items), z0 + (z1 - z0) * u, align, dy)
    return f

def seq(name, speed=1.0, kind='plain', dim=0.0, offset=0):
    """Képkocka-sorozat. kind: plain (.jpg) | canvas (.c.jpg) | ui (canvas a legutóbbi UI-képre illesztve)."""
    d = f'{FR}/{name}'
    def f(t, a, b):
        i = offset + int(round((t - a) * FPS * speed))
        if kind == 'plain':
            fs = sorted(glob.glob(d + '/*[0-9].jpg')); im = load(fs[min(i, len(fs) - 1)])
        else:
            fs = sorted(glob.glob(d + '/*.c.jpg')); i = min(i, len(fs) - 1); can = Image.open(fs[i]).convert('RGB')
            if kind == 'canvas': im = can if can.size == (W, H) else can.resize((W, H), Image.LANCZOS)
            else:
                uis = sorted(glob.glob(d + '/*.ui.jpg')); idx = [int(os.path.basename(u)[:4]) for u in uis]
                k = max(j for j, n in enumerate(idx) if n <= i); im = load(uis[k]).copy()
                x, y, w, h = [int(round(v)) for v in json.load(open(d + '/rect.json'))]
                if can.size != (w, h): can = can.resize((w, h), Image.LANCZOS)
                im.paste(can, (x, y))
        if dim: im = Image.blend(im, Image.new('RGB', (W, H), BG), dim)
        return im
    return f

def solid(t, a, b): return Image.new('RGB', (W, H), BG)

# ---------------------------------------------------------------- jelenetek
def ov(name, a, b, pos, fade=0.6, rise=14):
    return dict(img=OV + '/' + name + '.png', a=a, b=b, pos=pos, fade=fade, rise=rise)
BL = ('l', 120, 'b', 110)   # bal alsó felirat-pozíció
SC = {
 # ------------------------------ PROJEKTVIDEÓ
 's1': dict(dur=11.3, voice=('s1', 1.6), base=[(0, 11.3, still(f'{R}/hero_evening.png', 1.14, 1.0, dim=0.38), 0)],
            ov=[ov('logo_slogan', 1.0, 10.7, ('c', 0, 'c', -40), 1.2, 18), ov('intro_sub', 2.6, 10.7, ('c', 0, 'b', 90)), ov('demo', 0.4, 11.3, ('r', 70, 'b', 40), 0.8, 0)]),
 's2': dict(dur=16.4, voice=('s2', 0.6), scrim=True,
            base=[(0, 8.3, still(f'{R}/before_day.png', 1.0, 1.07, (.5, .45), (.5, .4)), 0), (7.7, 16.4, still(f'{R}/after_day.png', 1.07, 1.0, (.5, .4), (.5, .45)), 0.6)],
            ov=[ov('c2a', 0.8, 7.5, BL), ov('c2b', 8.4, 15.8, BL), ov('demo', 0, 16.4, ('r', 70, 'b', 40), 0.3, 0)]),
 's3': dict(dur=18.4, voice=('s3', 0.6), scrim=True,
            base=[(0, 4.6, cards([(f'{D10}/render/Ratet_v10_Fusion_osszeallitas.png', 720, 900), (f'{D10}/render/Ratet_v10_Fusion_belso_vasalat.png', 590, 900)], 1.0, 1.04, 'c', 85), 0),
                  (4.0, 11.0, seq('model_a', kind='canvas'), 0.6), (10.4, 18.4, seq('model_b', kind='canvas'), 0.6)],
            ov=[ov('c3a', 0.6, 4.5, ('l', 120, 't', 80), 0.5), ov('c3b', 5.4, 17.8, BL)]),
 's4': dict(dur=15.5, voice=('s4', 0.6),
            base=[(0, 5.4, cards([(f'{D10}/render/Ratet_v10_Fusion_belso_vasalat.png', 960, 1500)], 1.0, 1.08), 0),
                  (4.8, 10.4, still(f'{R}/exploded.png', 1.0, 1.08), 0.6), (9.8, 15.5, still(f'{R}/macro_handle.png', 1.08, 1.0, (.5, .5), (.5, .55)), 0.6)],
            ov=[ov('c4', 0.4, 15.0, ('l', 120, 't', 90)), ov('chip_pant', 0.9, 5.2, ('l', 120, 'b', 110)), ov('chip_csap', 5.6, 10.0, ('l', 120, 'b', 110)), ov('chip_fog', 10.4, 15.0, ('l', 120, 'b', 110))]),
 's5': dict(dur=14.7, voice=('s5', 0.6),
            base=[(0, 5.4, cards([(f'{D10}/rajz/Ratet_v10_nezetrajz.png', 760, 1500)], 1.0, 1.06, 'r', 0), 0),
                  (4.8, 10.0, cards([(f'{D10}/rajz/Ratet_v10_szabasterv_1.png', 760, 1500)], 1.04, 1.0, 'r', 0), 0.6),
                  (9.4, 14.7, cards([(f'{D10}/rajz/Ratet_v10_alkatresz_A01.png', 800, 1100), (f'{D10}/rajz/Ratet_v10_alkatresz_A05.png', 800, 1100)], 1.0, 1.04, 'l', -60), 0.6)],
            ov=[ov('c5', 0.6, 8.8, ('l', 120, 'c', 0)), ov('price', 9.8, 14.3, ('r', 120, 'b', 110))]),
 's6': dict(dur=12.7, voice=('s6', 0.6), scrim=True,
            base=[(0, 2.8, solid, 0), (2.2, 5.4, still(f'{R}/story_morning.png', 1.0, 1.06), 0.6), (4.8, 8.0, still(f'{R}/story_night.png', 1.06, 1.0), 0.6),
                  (7.4, 10.4, still(f'{R}/insp_grafit_dio.png', 1.0, 1.06), 0.6), (9.8, 12.7, still(f'{R}/open_led.png', 1.06, 1.0), 0.6)],
            ov=[ov('logo', 0.2, 2.6, ('c', 0, 'c', 0), 0.6, 10), ov('c6', 3.0, 12.2, BL), ov('demo', 2.4, 12.7, ('r', 70, 'b', 40), 0.3, 0)]),
 's7': dict(dur=18.4, voice=('s7', 0.6), scrim=True,
            base=[(0, 6.3, seq('site', speed=1.5), 0), (5.7, 18.4, seq('cfg', kind='ui'), 0.6)],
            ov=[ov('c7a', 0.6, 5.6, BL), ov('c7b', 6.6, 11.8, BL)]),
 's8': dict(dur=18.7, voice=('s8', 0.6),
            base=[(0, 18.7, still(f'{R}/story_night.png', 1.0, 1.1, dim=0.62, sat=0.6), 0)],
            ov=[ov('c8', 0.6, 18.1, ('l', 120, 't', 110)), ov('tools', 2.2, 9.9, ('r', 120, 'c', 40)), ov('pr1', 10.1, 14.5, ('r', 170, 'c', 40)), ov('pr2', 14.3, 18.2, ('r', 170, 'c', 40))]),
 's9': dict(dur=5.7, voice=('s9', 0.8), base=[(0, 5.7, solid, 0)], ov=[ov('end', 0.3, 5.7, ('c', 0, 'c', 0), 0.9, 12)], fade_out=1.0),
 # ------------------------------ PROMÓVIDEÓ (zene-vezérelt)
 'p1': dict(dur=7.5, voice=('p1', 1.0), scrim=True, base=[(0, 7.5, still(f'{R}/story_night.png', 1.12, 1.0), 0)], ov=[ov('p_t1', 1.2, 7.0, ('l', 120, 'b', 120), 1.0)]),
 'p2': dict(dur=7.5, voice=('p2', 0.8), scrim=True,
            base=[(0, 3.2, still(f'{R}/before_day.png', 1.0, 1.04), 0), (2.6, 7.5, still(f'{R}/after_day.png', 1.04, 1.0), 0.6)], ov=[ov('p_t2', 3.0, 7.0, ('l', 120, 'b', 120), 0.9)]),
 'p3': dict(dur=9.0, voice=('p3', 0.8), scrim=True,
            base=[(0, 6.0, seq('cfg2', kind='ui'), 0), (5.4, 9.0, still(f'{R}/macro_handle.png', 1.0, 1.08), 0.6)], ov=[ov('p_t3', 5.8, 8.6, ('l', 120, 'b', 120), 0.8)]),
 'p4': dict(dur=7.5, voice=('p4', 1.0), base=[(0, 7.5, still(f'{R}/hero_evening.png', 1.0, 1.1, dim=0.45), 0)], ov=[ov('end_promo', 0.6, 7.5, ('c', 0, 'c', 0), 1.2, 16)], fade_out=1.2),
}
ORDER = {'projekt': ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9'], 'promo': ['p1', 'p2', 'p3', 'p4']}

@functools.lru_cache(maxsize=1)
def scrim():
    a = np.zeros((H, W), np.float32)
    yy = np.linspace(0, 1, H)[:, None]; xx = np.linspace(0, 1, W)[None, :]
    a = np.clip((yy - 0.38) / 0.62, 0, 1) ** 1.3 * np.clip(1.35 - xx * 0.95, 0, 1) * 0.9
    return Image.fromarray((a * 255).astype(np.uint8))

def place(o, img):
    hx, dx, vy, dy = o['pos']; w, h = img.size
    x = {'l': dx, 'r': W - dx - w, 'c': (W - w) // 2 + dx}[hx]
    y = {'t': dy, 'b': H - dy - h, 'c': (H - h) // 2 + dy}[vy]
    return x, y

def frame(sc, t):
    base = None
    for a, b, clip, xf in sc['base']:
        if a - 1e-6 <= t < b + 1e-6 or (b >= sc['dur'] - 1e-6 and t >= a):
            im = clip(t, a, b)
            if base is None: base = im
            else:
                al = sm((t - a) / xf) if xf else 1.0
                base = Image.blend(base, im, al) if al < 1 else im
    base = base or solid(t, 0, 1)
    if sc.get('scrim') and any(o['a'] - 0.6 <= t <= o['b'] + 0.6 for o in sc['ov'] if o['pos'][0] == 'l' or o['pos'][0] == 'r'):
        k = max([min(sm((t - o['a'] + 0.6) / 0.8), sm((o['b'] + 0.6 - t) / 0.8)) for o in sc['ov']] + [0])
        if k > 0: base.paste((8, 7, 6), (0, 0), scrim().point(lambda v: int(v * k)))
    for o in sc['ov']:
        if not (o['a'] <= t <= o['b']): continue
        al = min(sm((t - o['a']) / o['fade']), sm((o['b'] - t) / o['fade'])) if o['fade'] else 1
        img = load(o['img'], 'RGBA'); x, y = place(o, img); y += int(round((1 - sm((t - o['a']) / (o['fade'] * 1.6 or 1))) * o['rise']))
        if al < 1: img = img.copy(); img.putalpha(img.getchannel('A').point(lambda v: int(v * al)))
        base.paste(img, (x, y), img)
    # bemenő / kimenő sötétítés
    fi, fo = sc.get('fade_in', 0.35), sc.get('fade_out', 0.35)
    k = min(sm(t / fi) if fi else 1, sm((sc['dur'] - t) / fo) if fo else 1)
    if k < 1: base = Image.blend(Image.new('RGB', (W, H), (0, 0, 0)), base, k)
    return base

ENC = ['-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-g', '60']
def render(key, outdir):
    sc = SC[key]; n = int(round(sc['dur'] * FPS)); os.makedirs(outdir, exist_ok=True)
    tmp = f'{outdir}/{key}.tmp.mp4'; out = f'{outdir}/{key}.mp4'
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-'] + ENC + [tmp], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(sc, i / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, out); print('ok', key, n)
    else: print('HIBA', key)

def still_at(key, t, path):
    frame(SC[key], t).save(path, quality=88)

# ---------------------------------------------------------------- hang
SR = 48000
def readwav(path):
    with wave.open(path) as w:
        sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    if sr != SR: x = np.interp(np.arange(int(len(x) * SR / sr)) / SR * sr, np.arange(len(x)), x)
    return x

def pad(total, seed=3, level=0.06, bpm_chord=6.0):
    """Lágy, lassú akkordpad (szinuszok + enyhe felharmonikusok, lassú burkoló, egyszerű visszhang)."""
    t = np.arange(int(total * SR)) / SR; y = np.zeros_like(t)
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    chords = [[45, 52, 57, 60, 64, 71], [41, 48, 57, 60, 64, 69], [36, 43, 52, 59, 64, 67], [43, 50, 55, 59, 62, 69]]  # Am9, Fmaj7, Cmaj7, G6
    L = bpm_chord; rng = np.random.default_rng(seed)
    for k in range(int(total / L) + 2):
        ch = chords[k % 4]; a = k * L - 1.5; b = a + L + 3.0
        i0, i1 = max(0, int(a * SR)), min(len(t), int(b * SR))
        if i1 <= i0: continue
        tt = t[i0:i1]; env = np.sin(np.clip((tt - a) / (b - a), 0, 1) * np.pi) ** 1.4
        for j, m in enumerate(ch):
            f0 = hz(m); ph = rng.uniform(0, 6.28); det = 1 + rng.uniform(-0.0015, 0.0015)
            v = np.sin(2 * np.pi * f0 * det * tt + ph) + 0.25 * np.sin(4 * np.pi * f0 * tt + ph) + 0.08 * np.sin(6 * np.pi * f0 * tt)
            y[i0:i1] += v * env * (0.9 if j == 0 else 0.55) * (1 + 0.15 * np.sin(2 * np.pi * 0.11 * tt + j))
    # egyszerű visszhang
    for d, g in [(0.29, .35), (0.53, .22), (0.97, .14)]:
        n = int(d * SR); y[n:] += y[:-n] * g
    y = y / (np.abs(y).max() + 1e-9) * level
    fade = np.clip(np.minimum(t / 3.0, (total - t) / 4.0), 0, 1); return y * fade

def audio(kind):
    keys = ORDER[kind]; total = sum(SC[k]['dur'] for k in keys)
    vo = np.zeros(int(total * SR) + SR); t0 = 0.0
    for k in keys:
        name, off = SC[k]['voice']; x = readwav(f'{HANG}/{name}.wav'); i = int((t0 + off) * SR)
        vo[i:i + len(x)] += x * 0.92; t0 += SC[k]['dur']
    mus = pad(len(vo) / SR, level=0.05 if kind == 'projekt' else 0.11, bpm_chord=6.0 if kind == 'projekt' else 4.0)
    # ducking: a zene halkul, ha beszéd szól
    env = np.convolve(np.abs(vo), np.ones(4800) / 4800, 'same'); duck = 1 - 0.55 * np.clip(env / 0.03, 0, 1)
    duck = np.convolve(duck, np.ones(9600) / 9600, 'same')
    mix = vo + mus * duck; mix = mix[:int(total * SR)]
    mix = np.tanh(mix * 1.1) / np.tanh(1.1)
    st = (np.stack([mix, mix], 1) * 32767).astype(np.int16)
    path = f'{V}/{kind}_hang.wav'
    with wave.open(path, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
    print('hang', path, round(total, 2), 's')

def final(kind, out):
    d = f'{V}/out_{kind}'; lst = f'{d}/list.txt'
    open(lst, 'w').write(''.join(f"file '{d}/{k}.mp4'\n" for k in ORDER[kind]))
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', f'{d}/video_only.mp4'], check=True)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{d}/video_only.mp4', '-i', f'{V}/{kind}_hang.wav', '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out + '.tmp.mp4'], check=True)
    os.replace(out + '.tmp.mp4', out); print('kész', out)

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd in ORDER:
        for k in (sys.argv[2:] or ORDER[cmd]): render(k, f'{V}/out_{cmd}')
    elif cmd == 'still': still_at(sys.argv[2], float(sys.argv[3]), sys.argv[4])
    elif cmd == 'audio': audio(sys.argv[2])
    elif cmd == 'final': final(sys.argv[2], sys.argv[3])
