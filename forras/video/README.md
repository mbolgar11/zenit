# Videó – forráskód

Három narrált videó készült, mindhárom kódból: képkockák Pythonban (Pillow/NumPy), feliratok Chromiumban renderelt PNG-ként, vágás és kódolás ffmpeg-gel.

| Videó | Script | Hossz |
|---|---|---|
| Projektvideó v2 (valódi fotók, alapító, weboldal, tervező, szerelés, zárórender) | `projekt_v2.py`, `narracio_v2.json` | 1:31 |
| Szerelési videó (a tervező 3D szerelési animációjából) | `asm_video.py`, `cap_asm.js`, `szereles_szoveg.json`, `vttfix.py` | 1:03 |
| Promóvideó | `compose.py`, `overlays.py`, `capture.js`, `narracio.json` | 0:31 |

## Hang
- **Narráció:** Piper TTS, magyar férfi hang „Imre” (hu_HU-imre-medium), helyben futtatva, utána ffmpeg-lánc (highpass, EQ, kompresszor, finom visszhang):
  `echo "<szöveg>" | piper -m hu_HU-imre-medium.onnx -f n01.wav --length-scale 1.06 --sentence-silence 0.45`
- **Zene:** `zene.py` – saját, jogdíjmentes, kódból szintetizált zenei alap: zongora-arpeggio (additív felhangok, inharmonicitás, lecsengés), vonós pad, basszus, konvolúciós térhang; Dmaj9 – Bm9 – Gmaj7 – Asus4, 68–76 BPM. Próba: `python3 zene.py 30` → `zene_demo.wav`.
- **Keverés:** a zene beszéd alatt automatikusan halkul (ducking a beszéd burkolója alapján), lágy telítés, a webes változat -16 LUFS-re normalizálva (`loudnorm`).
- **Felirat:** WebVTT, a narráció időzítéséből generálva; a weboldalon `<track default>`, a promó MP4-ben beágyazott (mov_text) sáv.

## Futtatás
A scriptek az AI-munkakörnyezetben futottak; az elején lévő abszolút útvonalakat (`D`, `V`, `HANG`, `R`) a saját mappára kell átírni.
```
python3 projekt_v2.py overlays && python3 projekt_v2.py render && python3 projekt_v2.py audio && python3 projekt_v2.py final
python3 asm_video.py overlays && python3 asm_video.py render && python3 asm_video.py audio && python3 vttfix.py szereles.vtt && python3 asm_video.py final
python3 compose.py promo && python3 compose.py audio promo && python3 compose.py final promo ZENIT_promovideo.mp4
ffmpeg -i be.mp4 -c:v libx264 -crf 24 -af loudnorm=I=-16:TP=-1.5:LRA=9 -c:a aac -movflags +faststart ki.mp4
```
További fájlok: `loop.py`, `hero_loop.py` (a weboldal háttér-videóhurkai), `montage.py` (saját felvételek vágása, színkorrekció), `cap_open.js` (ajtónyitás-felvétel).
