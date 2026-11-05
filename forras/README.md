# Forrásfájlok

Minden, amiből a ZENIT anyagai készültek. A scriptek az AI-munkakörnyezetben futottak; ahol abszolút útvonal maradt bennük, azt a script elején kell átírni.

| Mappa | Mi ez | Fő fájlok |
|---|---|---|
| `gyartas/` | Paraméteres geometria – az egyetlen igazságforrás. Ebből készül a Fusion 360 script, a CadQuery STEP/GLB, a szabásjegyzék, a furattábla, a rajzok és a gyártási PDF | `geometry.py`, `fusion_template2.py`, `build_cq2.py`, `cutlist.py`, `drawings.py`, `build_pdf.py` |
| `latvany/` | Blender (bpy) jelenetgenerátor az első látványtervekhez, textúrák; render → web konverzió | `zenit_scene.py`, `render_bl.py`, `conv_r2.py` |
| `latvany_v2/` | A második látványterv-sorozat: élkiemelés, két berendezés, színváltozatok, fékes pánt belülről | `zenit_scene.py`, `render_v3.py` |
| `szereles/` | Szerelési ábrák (SVG) a gyártási modellből | `illus.py` |
| `video/` | Projektvideó, promó, szerelési videó, háttérhurkok, felirat (VTT), saját generált zene | `projekt_v2.py`, `asm_video.py`, `compose.py`, `zene.py`, `montage.py` |
| `foto/` | Saját fotók retusálása, előtte–utána fotómontázs, alapítói portré kompozit, egységes színszűrő | `retouch.py`, `montage_after.py`, `portre_kompozit.py`, `grade.py` |
| `MEDIA_FORRASOK_es_LICENC.md` | A felhasznált stock fotók és videók forrásai, licence | – |

A weboldal generátora a gyökér `src/` mappájában van (`python3 src/build.py`), az üzleti terv pénzügyi modellje: `src/uzleti_modell.py`.
