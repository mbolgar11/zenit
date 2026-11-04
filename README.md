# ZENIT – felső szekrény a meglévő gardróbod tetejére

> „Ahol a szekrényed véget ér, ott kezdődünk.”

AI kihívás projekt (2026. november): egy valós rátétszekrény (Bútorline ELIA D 250 tetejére, 250 × 53 × 60 cm) teljes megtervezése
Claude (Anthropic) segítségével – 3D gyártási modell, gyártási dokumentáció, látványtervek, videó és egy kitalált prémium márka weboldala.

**Weboldal:** https://mbolgar11.github.io/zenit/

## Mi van a repóban
| Mappa | Tartalom |
|---|---|
| `/` (`*.html`, `assets/`) | A ZENIT weboldal (statikus, GitHub Pages) – 11 oldal, élő 3D tervező (three.js) |
| `src/` | Az oldalgenerátor (`build.py`) és a renderek web-konverziója |
| `forras/gyartas/` | Paraméteres geometria (egy igazságforrás) → Fusion 360 script, CadQuery STEP/GLB, szabásjegyzék, furattábla, PDF dokumentáció, kalkuláció |
| `forras/latvany/` | Blender (bpy) jelenetgenerátor a látványtervekhez és a textúrákhoz |

## A termék (v10, végleges)
- 250 × 53 × 60 cm, egy korpusz, 3 ajtó (80 + 90 + 80 cm osztás), 18 mm laminált lap, ajtók 2 mm ABS éllel
- Häfele Metalla 300SM pántok (fent fékes, lent rugós), GTV HEXA lekerekített alu élfogantyú
- tipli + konfirmát kötés, 3 polctartó csap oldalanként, beütős szeges hátfal, falfúrás nélküli rögzítés

## Megjegyzés
A ZENIT márka, a garancia és a fizetés kitalált / demó – nem valós webáruház. Minden kép látványterv (saját Blender-render vagy illusztráció).
