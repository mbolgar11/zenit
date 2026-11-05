"""Renderek → web (JPEG). Ha az új (v2) render még nincs kész, a régi (v1) helyettesíti."""
import os, sys
from PIL import Image, ImageEnhance
SRC2, OLD, DST = "/home/claude/zr2", "/home/claude/zenit-site/assets/img/r", "/home/claude/zenit2/assets/img/r2"
NAMES = ["hero_evening", "hero_day", "led_detail", "open_led", "after_day", "before_day", "story_morning", "story_night", "mirror_day",
         "macro_handle", "macro_edge", "macro_hinge", "exploded_light", "exploded", "insp_kreta", "insp_zsalya", "insp_ejkek", "insp_tolgy", "insp_grafit_dio"]
FALLBACK = {"hero_day": "after_day", "led_detail": "open_led", "mirror_day": "after_day", "macro_hinge": "macro_edge", "exploded_light": "exploded"}
for n in NAMES:
    p = os.path.join(SRC2, n + ".png")
    if os.path.exists(p):
        im = Image.open(p).convert("RGB"); src = "v2"
    else:
        q = os.path.join(OLD, n + ".jpg")
        if not os.path.exists(q): q = os.path.join(OLD, FALLBACK.get(n, "after_day") + ".jpg")
        im = Image.open(q).convert("RGB"); src = "v1"
    if im.width > 1600: im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
    im.save(os.path.join(DST, n + ".jpg"), quality=84, optimize=True, progressive=True)
    print(n, src)
