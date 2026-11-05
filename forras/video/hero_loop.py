"""Kezdőlap háttérvideó a renderekből: lassú Ken Burns + áttűnés, hurkolható (az eleje és vége ugyanaz a kép)."""
import subprocess, sys
from PIL import Image
W, H, FPS = 1920, 1080, 25
R = "/home/claude/zenit2/assets/img/r2/"
SHOTS = [("hero_evening", 1.10, 1.0, (.5, .5), (.46, .5)), ("led_detail", 1.0, 1.08, (.5, .55), (.55, .45)), ("hero_day", 1.08, 1.0, (.55, .5), (.5, .5))]
DUR, XF = 6.0, 1.2
def cover(im, z, cx, cy):
    sw, sh = im.size; s = max(W / sw, H / sh) * z; vw, vh = W / s, H / s
    x0 = min(max(cx * sw - vw / 2, 0), sw - vw); y0 = min(max(cy * sh - vh / 2, 0), sh - vh)
    return im.transform((W, H), Image.AFFINE, (1 / s, 0, x0, 0, 1 / s, y0), resample=Image.BICUBIC)
ims = {n: Image.open(R + n + ".jpg").convert("RGB") for n, *_ in SHOTS}
def shot(i, t):
    n, z0, z1, c0, c1 = SHOTS[i % len(SHOTS)]; u = max(0, min(1, t / DUR))
    return cover(ims[n], z0 + (z1 - z0) * u, c0[0] + (c1[0] - c0[0]) * u, c0[1] + (c1[1] - c0[1]) * u)
total = len(SHOTS) * (DUR - XF)
out = sys.argv[1]
p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-c:v", "libx264", "-crf", "26", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", out], stdin=subprocess.PIPE)
for f in range(int(total * FPS)):
    t = f / FPS; i = int(t // (DUR - XF)); lt = t - i * (DUR - XF)
    fr = shot(i, lt)
    if lt > DUR - XF - XF:  # áttűnés a következőbe (az utolsó után az elsőbe → hurok)
        k = (lt - (DUR - 2 * XF)) / XF
        fr = Image.blend(fr, shot(i + 1, lt - (DUR - XF)), max(0, min(1, k)))
    p.stdin.write(fr.tobytes())
p.stdin.close(); p.wait(); print("kész", out)
