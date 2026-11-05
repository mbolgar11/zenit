# ZENIT – felső szekrény a meglévő gardróbod tetejére

> „Ahol a szekrényed véget ér, ott kezdődünk.”

**AI-kihívás, 2026. november.** Egy valós rátétszekrény (a Bútorline ELIA D 250 tetejére, 250 × 53 × 60 cm) teljes megtervezése Claude-dal (Anthropic): 3D gyártási modell, gyártási dokumentáció, látványtervek, videók, egy kitalált prémium márka weboldala élő 3D tervezővel, kézikönyv és üzleti terv.

## Leadandók egy helyen

| | Link |
|---|---|
| 🌐 **Weboldal** | https://mbolgar11.github.io/zenit/ |
| 🎬 **Projektvideó** (1:30, narráció + kikapcsolható felirat) | [a weboldalon](https://mbolgar11.github.io/zenit/projekt.html) · [MP4](assets/video/zenit_projekt.mp4) · [felirat](assets/video/zenit_projekt.vtt) |
| 🧊 **3D modell** | [élő nézegető](https://mbolgar11.github.io/zenit/projekt.html) · [Fusion F3D](letoltes/Ratet_v10_Fusion.f3d) · [STEP (Fusion)](letoltes/Ratet_v10_Fusion_export.step) · [STEP (CadQuery, vasalatokkal)](letoltes/Ratet_v10_CadQuery_teljes.step) · [GLB](assets/model/zenit_v10.glb) |
| 🛠 **Élő 3D tervező** | https://mbolgar11.github.io/zenit/tervezo.html |
| 📝 **Napló** (eszközök, promptok, elakadások) | [NAPLO.md](NAPLO.md) · [a weboldalon](https://mbolgar11.github.io/zenit/naplo.html) |
| 📄 **Dokumentumok** | [gyártási dokumentáció](letoltes/Ratet_v10_gyartasi_dokumentacio.pdf) · [kézikönyv](letoltes/ZENIT_kezikonyv_referencia.pdf) · [üzleti terv 2027–2029](letoltes/ZENIT_uzleti_terv.pdf) · [szabásjegyzék](letoltes/Ratet_v10_szabasjegyzek_furattabla.xlsx) · [kalkuláció](letoltes/Ratet_v10_kalkulacio.xlsx) |
| 🎞 **További videók** | [szerelési videó](assets/video/zenit_szereles.mp4) · [promóvideó](assets/video/zenit_promo.mp4) |

## A termék (v10)
- 250 × 53 × 60 cm, egy korpusz, 3 ajtó, 18 mm laminált lap, az ajtókon 2 mm ABS él
- Häfele Metalla 300SM pántok (fent fékes, lent rugós), GTV HEXA 192 lekerekített alumínium élfogantyú
- tipli + konfirmát kötés, polctartó csapok, beütős szeges hátfal, falfúrás nélküli rögzítés a meglévő szekrényhez
- opciók a tervezőben: méret (szélesség, plafon, mélység 30–70 cm), 1–6 ajtó (max. 90 cm), ajtónként nyitásirány és tükör, ferde plafon és falkiegyenlítés 10 cm-ig, belső LED, színek, fogantyúk

## A repó felépítése
| Útvonal | Tartalom |
|---|---|
| `*.html`, `assets/` | A statikus weboldal (GitHub Pages): 18 oldal, three.js tervező, görgetésre mozgó ábrák (`assets/js/scrollfx.js`), saját betűkészletek, képek, videók |
| `assets/js/` | `common.js` (közös interakciók, süti-ablak), `configurator.js` (élő 3D tervező), `model3d.js` (GLB-nézegető), `manual.js` (személyre szabott kézikönyv), `scrollfx.js` |
| `src/` | Oldalgenerátor: `python3 src/build.py` újraírja az összes HTML-t (`pages.py`, `legal_pages.py`, `uzleti_terv.py`); napló forrása; üzleti modell (`uzleti_modell.py`) |
| `letoltes/` | Letölthető fájlok: F3D, STEP, GLB, PDF-ek, Excel |
| `forras/` | Gyártási geometria, Blender-jelenetek, szerelési ábrák, videó- és fotóscriptek – lásd [forras/README.md](forras/README.md) |

## Futtatás helyben
```bash
python3 src/build.py          # HTML-ek újragenerálása (Python 3.10+, markdown csomag a naplóhoz)
python3 -m http.server 8000   # majd: http://localhost:8000
```

## Eszközök
Claude (Anthropic) · Autodesk Fusion · CadQuery · Blender (bpy, Cycles) · three.js · Python (Pillow, NumPy, OpenCV, ReportLab) · Playwright/Chromium · ffmpeg · Piper TTS (magyar férfi hang) · rembg (U²-Net) · GitHub Pages

## Megjegyzés
A ZENIT márka, a díjak, az események, a cégadatok és a fizetés kitaláltak – ez látványprojekt, nem valós webáruház. A termékképek saját Blender-renderek vagy fotómontázsok; a hangulatképek és -videók Unsplash/Pexels licenc alatt, szűrve ([forrásjegyzék](forras/MEDIA_FORRASOK_es_LICENC.md)).
