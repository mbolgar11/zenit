"""ZENIT – saját, generált zenei alap (jogdíjmentes): meleg zongora-arpeggio, vonós pad, lágy basszus, finom térhang.
Hangnem: D-dúr / h-moll környéke, ~72 BPM. Használat: from zene import zene; y = zene(masodperc)"""
import numpy as np
SR = 48000
def hz(m): return 440 * 2 ** ((m - 69) / 12)
CH = [  # akkordok (MIDI): Dmaj9 – Bm9 – Gmaj7(#11) – Asus4/A
    [50, 57, 62, 66, 69, 76], [47, 54, 62, 66, 69, 73], [43, 55, 62, 66, 71, 73], [45, 52, 62, 64, 69, 71]]
def env_adsr(n, a, d, s, r, sr=SR):
    t = np.arange(n) / sr; e = np.ones(n) * s
    ia, idd = int(a * sr), int((a + d) * sr); e[:ia] = np.linspace(0, 1, max(1, ia)); e[ia:idd] = np.linspace(1, s, max(1, idd - ia))
    ir = int(r * sr); e[-ir:] *= np.linspace(1, 0, ir); return e
def piano(f, dur, vel, rng):
    n = int(dur * SR); t = np.arange(n) / SR; y = np.zeros(n)
    for k, (amp, dec) in enumerate([(1, 2.2), (.42, 3.0), (.22, 4.0), (.12, 5.2), (.06, 6.5)], start=1):
        inh = 1 + 0.0004 * k * k
        y += amp * np.sin(2 * np.pi * f * k * inh * t + rng.uniform(0, 6.28)) * np.exp(-t * dec * (0.6 + f / 900))
    y *= (1 - np.exp(-t * 400)) * vel; return y
def pad(f, dur, rng):
    n = int(dur * SR); t = np.arange(n) / SR; y = np.zeros(n)
    for det in (-0.004, 0, 0.0035):
        for k, a in ((1, 1), (2, .35), (3, .18), (4, .08)):
            y += a * np.sin(2 * np.pi * f * (1 + det) * k * t + rng.uniform(0, 6.28))
    y *= (1 + 0.12 * np.sin(2 * np.pi * 0.17 * t + rng.uniform(0, 6))) * env_adsr(n, 1.8, 0.6, .85, 1.8); return y / 6
def reverb(x, sec=2.6, mix=0.28, seed=7):
    rng = np.random.default_rng(seed); n = int(sec * SR); t = np.arange(n) / SR
    ir = rng.normal(0, 1, n) * np.exp(-t * 3.2); ir[:int(.012 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum())
    from numpy.fft import rfft, irfft
    L = len(x) + n; N = 1 << (L - 1).bit_length(); w = irfft(rfft(x, N) * rfft(ir, N), N)[:len(x)]
    return x * (1 - mix) + w * mix * 3.5
def _add(buf, a, y):
    if a >= len(buf) or a < 0: return
    m = min(len(y), len(buf) - a); buf[a:a + m] += y[:m]
def zene(total, bpm=72, seed=3, intro=2.0):
    rng = np.random.default_rng(seed); n = int(total * SR); out_p = np.zeros(n + SR * 6); out_s = np.zeros_like(out_p); out_b = np.zeros_like(out_p)
    beat = 60 / bpm; bar = 4 * beat
    pat = [0, 2, 3, 5, 4, 3, 2, 1]              # arpeggio-lépések az akkord hangjain
    k = 0; t0 = 0.0
    while t0 < total + bar:
        ch = CH[k % 4]; i0 = int(t0 * SR)
        p = pad(hz(ch[1] + 12), bar + 1.6, rng) + pad(hz(ch[3]), bar + 1.6, rng) * .8 + pad(hz(ch[4]), bar + 1.6, rng) * .6
        _add(out_s, i0, p)
        b = pad(hz(ch[0] - 12), bar, rng) * 1.4; _add(out_b, i0, b)
        if t0 >= intro:
            for j in range(8):
                note = ch[2 + pat[j] % 4] + (12 if pat[j] >= 4 else 0)
                st = t0 + j * beat / 2 + rng.normal(0, .008); vel = (0.55 if j % 2 else 0.8) * (0.85 + 0.3 * rng.random())
                if j in (3, 7) and rng.random() < .35: continue      # lélegző szünetek
                y = piano(hz(note), 3.2, vel, rng); _add(out_p, int(st * SR), y)
        k += 1; t0 += bar
    mix = reverb(out_p * 0.16, 2.8, 0.32) + reverb(out_s * 0.12, 3.5, 0.45, 9) + out_b * 0.10
    mix = mix[:n]; fi, fo = int(2.0 * SR), int(3.0 * SR)
    mix[:fi] *= np.linspace(0, 1, fi); mix[-fo:] *= np.linspace(1, 0, fo)
    return mix / (np.abs(mix).max() + 1e-9) * 0.5
if __name__ == "__main__":
    import wave, sys
    y = zene(float(sys.argv[1]) if len(sys.argv) > 1 else 30)
    st = (np.stack([y, y], 1) * 32767).astype(np.int16)
    with wave.open("zene_demo.wav", "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
    print("ok", len(y) / SR)
