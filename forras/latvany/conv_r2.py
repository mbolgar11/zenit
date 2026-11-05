"""Renderek → web (JPEG). Ha az új (v2) render még nincs kész, a régi (v1) helyettesíti."""
import os, sys
from PIL import Image, ImageEnhance
import numpy as np
DAY = {"hero_day", "after_day", "before_day", "story_morning", "mirror_day", "b_zsalya_day", "v_tolgy_day", "insp_kreta", "insp_zsalya", "insp_tolgy"}
def grade(im, n):
    """egységes fotós utómunka: nappali képeken lágy vállas görbe, mindenhol finom vignetta"""
    a = np.asarray(im).astype(np.float32) / 255
    if n in DAY: a = a ** 1.15
    if n.startswith("macro"): a = a ** 1.22
    if n == "exploded_light": a = a ** 1.7
    h, w = a.shape[:2]; y, x = np.ogrid[:h, :w]; r = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2)
    a = a * (1 - 0.13 * np.clip((r - 0.55) / 0.85, 0, 1) ** 1.6)[..., None]
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype("uint8"))
    return ImageEnhance.Color(im).enhance(1.08) if n in DAY else im

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC2 = os.environ.get("ZENIT_RENDERS_V2", "renders_v2")   # Blender PNG-k (render_v3.py kimenete)
OLD, DST = os.path.join(ROOT, "assets/img/r"), os.path.join(ROOT, "assets/img/r2")
NAMES = ["hero_evening", "hero_day", "led_detail", "open_led", "after_day", "before_day", "story_morning", "story_night", "mirror_day",
         "macro_handle", "macro_edge", "macro_hinge", "exploded_light", "exploded", "insp_kreta", "insp_zsalya", "insp_ejkek", "insp_tolgy", "insp_grafit_dio",
         "hinge_in", "b_kasmir_evening", "b_open_led", "b_zsalya_day", "v_tolgy_day", "b_ejkek_evening", "v_grafit_dio"]
FALLBACK = {"hero_day": "after_day", "led_detail": "open_led", "mirror_day": "after_day", "macro_hinge": "macro_edge", "exploded_light": "exploded", "hinge_in": "macro_hinge", "b_kasmir_evening": "hero_evening", "b_open_led": "open_led",
            "b_zsalya_day": "insp_zsalya", "v_tolgy_day": "insp_tolgy", "b_ejkek_evening": "insp_ejkek", "v_grafit_dio": "insp_grafit_dio"}
for n in NAMES:
    p = os.path.join(SRC2, n + ".png")
    if os.path.exists(p):
        im = Image.open(p).convert("RGB"); src = "v2"
    else:
        q = os.path.join(OLD, n + ".jpg")
        if not os.path.exists(q): q = os.path.join(OLD, FALLBACK.get(n, "after_day") + ".jpg")
        im = Image.open(q).convert("RGB"); src = "v1"
    if im.width > 1600: im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
    if src == "v2" and n != "exploded": im = grade(im, n)
    im.save(os.path.join(DST, n + ".jpg"), quality=84, optimize=True, progressive=True)
    print(n, src)
# második kivágás a pántról (az Anyagok oldalra), hogy ne ugyanaz a kép ismétlődjön
_h = os.path.join(DST, "hinge_in.jpg")
if os.path.exists(_h):
    Image.open(_h).crop((300, 110, 1100, 710)).save(os.path.join(DST, "hinge_in_detail.jpg"), quality=86, optimize=True, progressive=True)
