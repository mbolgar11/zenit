# Videó – forráskód

- `narracio.json` – a narráció szövege jelenetenként (projekt + promó).
- Hang: Piper TTS, magyar „Anna” hang (hu_HU-anna-medium), helyben futtatva:
  `echo "<szöveg>" | piper -m hu_HU-anna-medium.onnx -f s1.wav --length-scale 1.06 --sentence-silence 0.45`
- `capture.js` – determinisztikus képkocka-felvétel a weboldalról (Playwright, 30 fps; a requestAnimationFrame és a performance.now kézzel léptetve).
- `overlays.py` – feliratok HTML-ből, átlátszó PNG-ként (a weboldal betűtípusaival).
- `compose.py` – jelenetek (Ken Burns, áttűnések, feliratok) → MP4 jelenetenként, concat, szintetizált zenei alap + narráció keverése, ducking.

```
node capture.js frames            # 3D-nézegető, oldalgörgetés, tervező
python3 overlays.py
python3 compose.py projekt && python3 compose.py audio projekt && python3 compose.py final projekt ZENIT_projektvideo.mp4
python3 compose.py promo   && python3 compose.py audio promo   && python3 compose.py final promo   ZENIT_promovideo.mp4
```
