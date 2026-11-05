"""Szerelés oldal háttérvideója: a teljes szerelési felvétel gyorsítva (2,5×), néma, hurkolható, a végén áttűnéssel a kezdetbe."""
import glob, subprocess
from PIL import Image
fs = sorted(glob.glob("/home/claude/video2/asm/*.jpg"))
sel = fs[::5][:]  # 25 fps-ből minden 5. kocka, 10 fps-sel lejátszva = 2× gyorsítás
sel = [Image.open(f).convert("RGB") for f in sel]
X = 12  # áttűnés kockákban
out = sel[X:-X] + [Image.blend(sel[-X + i], sel[i], (i + 1) / (X + 1)) for i in range(X)]
V = "/home/claude/zenit2/assets/m/video/"
p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1280x720", "-r", "10", "-i", "-",
                      "-vf", "fps=25", "-c:v", "libx264", "-crf", "25", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", V + "szereles_loop.mp4"], stdin=subprocess.PIPE)
from PIL import ImageEnhance
out = [ImageEnhance.Brightness(im).enhance(0.66) for im in out]
for im in out: p.stdin.write(im.resize((1280, 720)).tobytes())
p.stdin.close(); p.wait()
out[len(out) * 3 // 5].save(V + "szereles_loop.jpg", quality=82, optimize=True)
print("ok", len(out) / 10, "s")
