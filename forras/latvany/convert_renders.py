"""Renderek → web JPG (enyhe színkorrekció). python3 src/convert_renders.py"""
import os
from PIL import Image, ImageEnhance
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.environ.get("ZENIT_RENDERS", "renders_v1"); DST = os.path.join(ROOT, "assets/img/r")
os.makedirs(DST, exist_ok=True)
for f in sorted(os.listdir(SRC)):
    if not f.endswith(".png"): continue
    im = Image.open(os.path.join(SRC, f)).convert("RGB")
    n = f[:-4]
    if "evening" in n or n in ("open_led", "insp_grafit_dio", "insp_ejkek"):
        im = ImageEnhance.Color(im).enhance(0.78)          # kevésbé narancs esti fény
        r, g, b = im.split(); b = b.point(lambda v: min(255, int(v * 1.05 + 4))); im = Image.merge("RGB", (r, g, b))
    if n.startswith(("after", "before", "story_morning", "insp_zsalya", "insp_kreta", "insp_tolgy")):
        im = ImageEnhance.Contrast(im).enhance(1.06)
    if n.startswith("tex_"):
        im = ImageEnhance.Contrast(im).enhance(1.1)
    im.save(os.path.join(DST, n + ".jpg"), quality=84, optimize=True, progressive=True)
    print(n, im.size)
