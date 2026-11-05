"""Lassú közelítéses, áttűnéses hurokvideó állóképekből (aloldal-fejlécekhez)."""
import sys, subprocess
from PIL import Image, ImageEnhance
W, H, FPS = 1600, 900, 25
def cover(im, z, px, py):
    sw, sh = im.size; s = max(W / sw, H / sh) * z; vw, vh = W / s, H / s
    x0 = (sw - vw) * (0.5 + px); y0 = (sh - vh) * (0.5 + py)
    return im.transform((W, H), Image.AFFINE, (1 / s, 0, x0, 0, 1 / s, y0), resample=Image.BICUBIC)
def run(out, files, seg=3.4, xf=0.9, dark=1.0):
    ims = [Image.open(f).convert("RGB") for f in files]
    n = len(ims); per = int(seg * FPS); X = int(xf * FPS); total = n * per
    def shot(i, f):  # i. kép, f: kocka a saját szakaszán belül (0..per+X)
        k = f / (per + X); d = 1 if i % 2 == 0 else -1
        return cover(ims[i], 1.02 + 0.07 * (k if d > 0 else 1 - k), 0.12 * d * (k - .5), 0)
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-crf", "24", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", out + ".mp4"], stdin=subprocess.PIPE)
    poster = None
    for t in range(total):
        i, f = divmod(t, per)
        im = shot(i, f + X)
        if f < X:  # áttűnés az előző képből (az elsőnél az utolsóból → hurok)
            j = (i - 1) % n; im = Image.blend(shot(j, per + f), im, (f + 1) / (X + 1))
        if dark < 1: im = ImageEnhance.Brightness(im).enhance(dark)
        if t == per // 2: poster = im
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait(); poster.resize((1280, 720)).save(out + ".jpg", quality=82, optimize=True)
    print("ok", out, total / FPS, "s")
if __name__ == "__main__":
    R = "/home/claude/zenit2/assets/img/r2/"; O = "/home/claude/zenit2/assets/m/video/"
    if sys.argv[1] == "insp":
        run(O + "inspiracio_loop", [R + f + ".jpg" for f in ["b_kasmir_evening", "b_zsalya_day", "b_ejkek_evening", "v_tolgy_day", "v_grafit_dio", "insp_kreta"]], dark=0.92)
    if sys.argv[1] == "proj":
        run(O + "projekt_loop", [R + "exploded_light.jpg", "/home/claude/video2/asm/0640.jpg", "/home/claude/video2/open/0120.jpg", R + "hinge_in.jpg", R + "hero_evening.jpg", R + "macro_handle.jpg"], dark=0.68)
