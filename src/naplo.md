# Napló – Rátétszekrény AI kihívás

## 1. nap – kedd, nov. 3.

### Indítás
- Eszköz: Claude (Cowork, desktop app) – a gépemhez kötve, a „Szekrény” mappán dolgozik.
- Első prompt (lényeg): „Egy rátétszekrényt fogok csinálni egy meglévő szekrény tetejére… megtervezzük közösen koncepció/layout szinten, te lemodellezed 3D-ben Fusion 360-ban, csinálsz gyártási dokumentációt, hogy lapszabászaton vagy az OBI-ban meg tudjam rendelni… YouTube videó, promo videó, landing page… azt akarom, hogy mindent te csinálj.”

### GitHub
- Nem volt fiókom → „csinálj egyet” → Claude megnyitotta a regisztrációs oldalt a beépített böngészőben; a jelszót/ellenőrzést én csináltam (fiók: mbolgar11).
- **Elakadás:** Claude felhős munkaterületéről a GitHub nem volt elérhető (a proxy csak előre beállított repókat enged).
- **Megoldás:** GitHub „device flow” belépés az én gépemen keresztül: kaptam egy kódot, beírtam a github.com/login/device oldalon, és onnantól Claude a gépemről tud pusholni.

### YouTube
- Kérdés: kell-e API hozzáférés? **Tanulság:** a nem auditált YouTube API-alkalmazással feltöltött videók automatikusan privátok lesznek → nem ágyazhatók be. Megoldás: feltöltés a böngészőből, Claude kitölti a mezőket, publikálás előtt rákérdez.

### Méretek és koncepció
- Prompt: elküldtem a szekrényem termékoldalát (Bútorline ELIA D 250, kasmír). Claude kiolvasta: 250×205×60 cm, 16 mm lap, 3 tolóajtó (középső tükrös), és megnézte a méretrajzot.
- Belmagasság 260, de van ahol 259 → szabad hely 54 cm.
- Claude rajzolt egy elölnézeti vázlatot a chatbe; döntések kérdés-gombokkal:
  - „90-80-80-as osztás, szimmetrikusan, a középső a legszélesebb” → 80+90+80 cm
  - nyíló ajtó, nyomásra nyíló (TIP-ON), mind a 3 sima kasmír
  - középen polc, a széleken nincs (bőrönd)
  - „nem kell felső takaróléc és fent sem kell kirögzíteni, elég csak a szekrényhez”
- Claude felhívta a figyelmet: a dobozt fel kell emelni és hátratolni → 2 cm játék kell → 52 cm magas modul.

### 3D modell (v1)
- Claude tiszta Python geometriát írt (egy igazságforrás), ebből: CadQuery → STEP / GLB / STL, Blender (bpy) → renderek, Fusion 360 Python script, szabásjegyzék.
- **Elakadások a renderelésnél:**
  - az első render teljesen kiégett (túl erős fények) → fényerő ~1/6-ára
  - a nyitott ajtók befelé, a szekrénybe fordultak → forgatási előjel javítva
  - a kasmír fehérnek látszott → sötétebb, melegebb szín + zsályazöld hátfal a kontrasztért
- Prompt: „úgy tervezd meg, hogy legyen benne illesztő fa tipli, járatos csavarok, kekszek ha kell, könnyített szerelés, olcsó de jó” → 8×35 bükk tipli + konfirmát 7×50, keksz nem kell, 1:1 nyomtatható fúrósablon.

### Fusion 360 bekötése – a nap legnagyobb kalandja
- Prompt: „nem kell ehhez valami MCP vagy hasonló, hogy hatékonyan dolgozz a Fusionnel?” → Claude megtalálta a hivatalos **Autodesk Fusion MCP** connectort.
- Bekapcsoltam a Fusionben (Preferences → General → API → Fusion MCP Server), majd a connectort a Claude appban.
- **Elakadás 1:** Claude elérte a Fusion portját a beépített böngészőből, de a szerver biztonsági okból elutasította („Invalid Origin”) – helyesen.
- **Elakadás 2:** a connector eleinte nem jelent meg a felhős munkamenetben. Claude közben megkereste a külsős Fusion MCP-ket (faust-machines, prim-design, Misterbra), és írt egy **saját fájl alapú hidat** (ClaudeBridge add-in, a megosztott mappán keresztül).
- Aztán a hivatalos connector mégis megjelent → Claude **élőben építette a modellt a Fusionömben**.
- **Elakadások az élő modellezésnél (mind megoldva):**
  - az ékezetes „Szekrény” mappanév elromlott az átvitelben („SzekrÃ©ny”) → `chr(233)`-mal rakta össze
  - a Fusion nem enged „H” és „t” nevű paramétert, mert ezek mértékegységek (henry, tonna) → `Korpusz_magassag`, `Lapvastagsag`
  - az új Fusion „Part” dokumentuma csak egy komponenst enged → hibrid (összeállítás) módra váltás
  - a gépemre küldött fájl kétszer a régi változatot írta ki (gyorsítótár) → új fájlnévvel küldve, md5-tel ellenőrizve

### Teljes gyártási modell (v2)
- Prompt: „csináld meg, hogy benne legyenek a furatok is a modellben rendesen, az összes fúrási feature és tipli és csavar is, valamint a zsanérok és a nyitók, kilökők … ABS élzárással”
- Eredmény Fusionben: 19 lap (lapmag + **25 ABS élzáró csík** külön testként), **75 Hole feature / 258 furat** (konfirmát süllyesztéssel, tipli, Ø35 pántcsésze lapos fenékkel, pánttalp, TIP-ON, összekötő, rögzítő- és hátfalcsavar), **165 db vasalat** (42 konfirmát, 28 tipli, 6 pánt, 3 TIP-ON, 8 összekötő, 12 rögzítőcsavar, 66 hátfalcsavar).
- Claude programmal ellenőrizte: nincs egymásba futó vagy lapból kilógó furat; a Fusion, a STEP és az Excel furatszáma egyezik (258).
- Export a Fusionből: F3D + STEP.

### Gyártási dokumentáció
- Szabásjegyzék Excelben (képletekkel), 19 alkatrész, ABS élzárás élenként (H1/H2/R1/R2), „Furatok” lap: minden furat koordinátával.
- Táblaoptimalizálás (rectpack): 2 tábla 2800×2070 kasmír kell.
- v2 PDF (26 oldal): nézetrajz, szabásjegyzék, Fusion képek, **15 automatikusan generált alkatrészrajz furattáblával (A01–A15)**, szabásterv, vasalat (a modellből számolva), szerelés, 1:1 fúrósablon.
- **Elakadás:** a PDF lábléce kék lett szürke helyett – a ReportLab a 3-jegyű „#888” színkódot rosszul értelmezi → 6-jegyű kód.
- **Elakadás:** a polc fúrósablonjánál Claude saját maga vette észre, hogy a referenciaél nem a 260-as vonal, hanem a polc alja (251 mm) – javítva.
- **Elakadás:** a PDF nyitva volt nálam, nem lehetett felülírni → _v2 néven mentette.

### Rendrakás
- Prompt: „mentsd le ezeket verziózva, beszédes nevekkel a szekrény mappába, strukturáltan, követhetően”
- Új szerkezet: `00_Projekt`, `01_Koncepcio_es_latvany`, `02_3D_modell`, `03_Fusion360`, `04_Gyartasi_dokumentacio`, `05_Forraskod`; verziómappák (`v1_…`, `v2_…`), fájlnevek `Ratet_v<n>_<tartalom>` formában, README a gyökérben.

### Költségcsökkentett változat (v3)
- Prompt: „csinálj egy olyan verziót is, költségcsökkentés miatt, hogy … négy függőleges tartó van … az alsó és felső lap egy-egy nagy elem … egy nagy téglatest váz lesz két osztással és 3 ajtóval. Oldd meg, hogy a 3 ajtó szépen záródjon … 18 mm-en kell megoldanod két ajtó zárását.”
- Megoldás: a közfal közepe pont az ajtóosztás vonalán (800 és 1700 mm) → mindkét ajtó 7,5 mm-t takar a 18 mm-es közfalból, köztük 3 mm hézag; a közfalon ülő pánt **félig ráütődő** (9,5 mm hajlítású) CLIP top, az oldallapokon maradt a ráütődő.
- Menet közbeni kérés: „a középső két függőleges osztófal mindkét oldalán legyen zsanér felfogató előfurat, hogy forgatható legyen a középső nyíló ajtó” → tartalék pánttalp- és TIP-ON-előfuratok a másik közfalon is; az ajtót fejjel lefelé fordítva a csészék a másik élre kerülnek (100 mm alul-felül, szimmetrikus).
- Fusion: 11 lap + 19 ABS él, 53 Hole feature / 196 furat, 125 vasalat; mentve „Rátétszekrény v3 - egy korpusz, költségcsökkentett” néven.
- Claude őszinte összevetése: 19 → 11 alkatrész, −9% lap, −62 furat, nincs összekötő csavar, 1 hátfal; DE a táblaszám marad 2 (5,8 m² épp nem fér egy táblára), a 2464 mm-es lapokhoz szállítás kell, és az egész korpusz ~56 kg (3 ember). Plusz: a tetőlapon felülről kell csavarozni → csak a földön szerelhető össze.
- **Elakadás:** a 2,5 m-es lapok rajzán összecsúsztak a feliratok → a rajzelemek mérete a lap hosszával skálázódik; a hátfal 54 soros furattáblája nem fért az oldalra → hosszú lapoknál a táblázat a rajz alá kerül.

### Részletek finomítása (v4–v5)
- Prompt (csak megbeszélés, még nincs modellezés): „az alsó nagy szekrényhez csak a két oldalán húzd le 2-2, szumma 4 forgácslapcsavarral … HDF ne menjen a polcba … polctartó furatok mindenhol … 2 konfirmát + 2 tipli … nyomásra nyitó helyett javasolj szép fogantyút”
- Claude javaslata: RIOS alu élfogantyú az ajtók alsó élének közepére; ehhez az ajtó 4,5 mm hézagot kap alul-felül (511 mm magas ajtó).
- „elég egy csillapított per ajtó, a másik legyen sima” → fent fékes, lent rugós pánt.
- Tanulság: „elég ha módosítod… előbb csak modell és árkalkuláció, a doksi a végén” – a dokumentációt csak a végleges változatra generáltattam, így nem ment el idő köztes PDF-ekre.
- v5: „nem kell a teljes furatsor, csak a pántok furatai és a polcnak pont középen, mind a 3 fakkban” → 48 Hole feature / 152 furat; a középső polc levehető, csapokon ül.

### Ár és anyag (v6)
- Prompt: „csekkold, hogy az OBI-ban valóban ingyenesen vágják-e … számold fehér lapból … 0,4-es ABS éllel”
- Claude utánanézett: az OBI szabási díja nem nyilvános (és nem ingyenes), élzárás csak 0,4 és 2 mm ABS; a kalkuláció ezért min–max sávval számol (szabás 0–300 Ft/vágás).
- Színvariációk renderelve az OBI 18 mm-es kínálatából (fehér 4 699 Ft/m², antracit 6 299, szürke 10 490, trüffel/szil 12 490); kasmír lapot olcsón a Lapp-Fánál talált (~28 e Ft/tábla). Döntés: **fehér** (fehér fal, fehér függöny mellé).

### Vasalat és végleges változat (v7)
- Prompt: „milyen kivetőpántok vannak? … GTV vagy Häfele a jobb?” → Claude összehasonlította (ráütődő / félig ráütődő, rugós / fékes / push); döntés: **Häfele Metalla 300SM** kombi, ajtónként 1 fékes (fent) + 1 rugós (lent).
- „amennyire lehet, egységesítsd a csavarhosszokat” → 3 csavarfajta maradt: konfirmát 7×50, forgácslapcsavar 3,5×16 (pánt, pánttalp, fogantyú, hátfal) és 3,5×30 (rögzítés az ELIA-hoz).
- Utolsó módosítás: „az ajtónak legyen inkább 2 mm-es élzárása, a bútor többi részének meg 0,4” → modell, kalkuláció, szabásjegyzék és Fusion frissítve (12 db 2 mm-es ABS csík az ajtókon).
- Fusion: „Rátétszekrény v7 - VÉGLEGES (OBI fehér, Häfele)”, 48 Hole feature / 152 furat; F3D + STEP export.
- Végleges gyártási dokumentáció (25 oldal): nézetrajz, szabásjegyzék élzárással, Fusion képek, 10 alkatrészrajz furattáblával (A01–A10), végleges döntések táblázata, szabásterv (2 tábla), vasalatlista, szerelési útmutató, 1:1 fúrósablon.
- Kalkuláció: kb. 83–139 e Ft, várhatóan ~111 e Ft (lap, HDF, szabás, élzárás, pántfúrás, Häfele pántok, RIOS fogantyú, kötőelemek, szállítás).
- **Elakadások:**
  - a Fusion MCP hívás 60 s után időtúllépést jelzett, de a modellépítés tovább futott → utána egy csak olvasó scripttel ellenőrizte az állapotot
  - a CadQuery összeállításban két vasalatcsoport ugyanazt a nevet kapta („pánt_2db”) → egyedi nevek a teljes megnevezésből
  - a rajzok még kasmír színnel készültek → a lapszín fehérre állítva, a polc mérete „880.0” helyett „880”
  - a belső vasalatkép a Fusionből: Claude scripttel elrejtette az ajtókat és a hátfalat, képet vett, majd visszakapcsolta őket

### Utolsó finomítások (v8 – végleges)
- Prompt: „a polctartó legyen oldalanként 3 csap, ne csak kettő, valamint a hátfal nem csavaros, hanem beütős szeges, nem kell előfúrni/jelölni … és a doksit rövidre csináld, ha lehet, ne csússzon át tartalom több oldalra”
- Menet közben: „és legyen még 1 cm-rel magasabb a teljes magasság” → 520 → **530 mm**, ajtók 521 mm; a plafonig 10 mm marad, ezért a korpuszt vízszintesen kell feltolni, billenteni nem lehet.
- Polctartó: oldalanként 3 csap (37 / 289,5 / 542 mm elölről), mindhárom rekeszben; a hátfal 50 db 1,6×25-ös beütős hátfalszeggel kerül fel, így 48 hátfalfurat kiesett (108 furat / 47 feature).
- Fusion: „Rátétszekrény v8 - VÉGLEGES (530 mm, 3 polccsap, szegezett hátfal)”. A 28 kB-os scriptet nem a chatbe másolta Claude: a gépemre mentette, és egy rövid Fusion-script onnan futtatta (gyorsabb, olcsóbb).
- Dokumentáció 25 → **12 oldal**: minden fejezet egy oldal, egy blokkban (KeepTogether), az alkatrészrajzok csoportosítva (3 rajz/oldal), a furat nélküli lapoknak (polc, hátfal) nincs külön rajza. Minden szöveges méret a modellből számolódik, így a magasságváltozás mindenhol egyszerre frissült.
- **Elakadás:** a fúrósablon „B” csíkja még a régi, konfirmátos polcot mutatta (v5 óta csapokon ül) → kicserélve 3 csapos polctartó-sablonra.

### Fogantyúcsere és nagyobb rajzok (v9)
- Prompt: „olyan kéne, ami ilyen kivitel, de le van kicsit kerekítve, nem ilyen sarkos, kb. ilyen alu elox szürke színben”
- Claude a beépített böngészőben végignézte a fogantyushop.hu élre szerelhető kínálatát (képek alapján): a GTV HEXA, Furnipart EDGE STRAIGHT, Viefe WAY és Rujz 658.35 szögletes; a Furnipart EDGE ROUND csak 40/200 mm-ben van. Választás: **Viefe CURVE**, lekerekített, íves profil, alu szálcsiszolt (L24), 128 mm furattáv / 200 mm hossz, 3 020 Ft/db, raktáron. Eloxált matt szürke változatot a boltban nem talált.
- Kalkuláció: ~90–145 e Ft, várhatóan ~118 e Ft (a drágább fogantyú miatt +7 e Ft).
- Prompt: „a PDF-nél, ahol 3 rajz van egy lapon, azt szedd szét külön, a többin meg a rajzokon annyit nagyíts, amíg csak lehet, hogy ne kelljen oldalszámot növelni”
- Megoldás: minden alkatrésznek külön oldal; egy kis „illesztő” függvény minden oldalon milliméterenként csökkenti a rajz méretét, amíg az egész oldal egy lapra fér, így minden rajz a lehető legnagyobb. 16 oldal.
- **Elakadás:** az első próbánál 20 oldal lett, mert a ReportLab keret 6 pt-os belső margóját nem számolta bele → javítva, 16 oldal, semmi nem csúszik át.

### Végleges fogantyú (v10)
- Prompt: elküldtem egy linket (butorkellek.hu, „Fogantyú 1342, alu”): „ehhez hasonlókat nézz, olyat is, amit hátulról csavarozok, nem élben … előbb keress, és válasszuk ki, utána csináld csak meg a módosítást”
- Claude végignézte a butorkellek.hu élfogantyúit (képek és adatlapok). Kiderült, hogy a linkelt darab a **GTV HEXA (UA-HEXA-…-05)**, és hogy korábban tévesen soroltam a szögletesek közé – valójában lekerekített, ráhajló profil. Ez hátulról, az ajtó belső lapjába csavarozható.
- Kérdés: „jobb a hosszabb?” → Claude: igen, mert a szekrény fejmagasság felett van, vakon nyúlsz érte; a 192 mm-es furattávú (225 mm hosszú) arányos a 797/897 mm-es ajtókhoz.
- Döntés: **GTV HEXA 192, alu**, 805 Ft/db, raktáron (butorkellek.hu). A furatok átkerültek az ajtó élébe fúrtról az ajtó belső lapjára (Ø2,5×12, 10 mm-re az alsó éltől, 192 mm-re egymástól), 3,5×16 csavarral (nem fut át a 18 mm-es ajtón).
- Kalkuláció: ~84–138 e Ft, várhatóan ~111 e Ft.
- Fusion: „Rátétszekrény v10 - VÉGLEGES (GTV HEXA 192 fogantyú, 530 mm)”, 47 feature / 108 furat, mind ép.

## 2. nap – szerda, nov. 4.

### Márka, weboldal, látványtervek (ZENIT)
- Ötletelés sok kérdéssel (AskUserQuestion-gombokkal):
  - név: **ZENIT**;
  - szlogen: „Ahol a szekrényed véget ér, ott kezdődünk.”, mellé „A hiányzó fél méter.”;
  - méretvonalas logó, 6 változatból;
  - a „ZENIT Örökgarancia” szövege négy javaslat összefésüléséből;
  - sötét-meleg prémium arculat: Cormorant Garamond és Inter betűtípus, bronz kiemelőszín.
- Prompt: „ne egy landing oldalra, hanem aloldalakra, egy-két fő menüponttal … vezessük végig a vevőt”
  - Eredmény: 11 oldal, fő menü: Kollekció + Concierge.
  - Minden oldal alján „Következő fejezet” vezet tovább.
  - A közös fejlécet és láblécet egy Python-generátor írja (src/build.py).
- Prompt: „legyen benne … hogy ez egy luxus, egyedi termék, magyar felhalmozott tudással és szakértelemmel … legyen sztori is, és érzés eladva”
  - Manufaktúra oldal.
  - Négy jelenetes történet: este a bőrönd → reggel plafonig → este csend.
  - „Öt érzés” blokk.
  - A márka kitalált, ezt a lábléc jelzi. Kitalált vásárlói vélemény nincs az oldalon.
- **Képek:** stock fotót (Unsplash/Pexels) és AI-képgenerálást a munkamenet hálózati beállítása nem engedett. Helyettük **saját Blender-jelenetgenerátor** készült (zenit_scene.py):
  - szoba ággyal, lámpával, növénnyel, függönnyel;
  - este, reggel, éjszaka és stúdió hangulat;
  - procedurális fa-, len- és betontextúrák;
  - 21 kép: előtte–utána pár, nyitott LED-es belső, 6 színvariáció, makrók, robbantott nézet;
  - mellé saját vonalas SVG-illusztrációk.
- Kérés közben: „ne fehér legyen a rátétszekrény, hanem kasmír … csak amit bemutatok” → a bemutató képeken kasmír lett.
- **Elakadások:**
  - Az első fa-shader márványszerű lett → sávos, függőleges erezetre cseréltük.
  - A gépen csak 2 CPU van, egy kép ~3,5 perc → a renderek háttérben futó sorban készültek.
  - file:// alatt nem jelentek meg a külső SVG-ikonok → az ikonkészletet beágyaztuk az oldalakba.

### Élő 3D tervező
- Prompt (a kérdésre, hogy jöhet-e a valódi 3D): „igen, mehet”
- three.js-alapú tervező a tervező oldalon, valós idejű látvánnyal:
  - szélesség 60–280 cm;
  - 1–6 ajtó, javasolt és felülírható osztás;
  - külön szín a korpusznak, az ajtóknak és a belsőnek: palettából, HEX-kóddal vagy textúrával (tölgy, füstölt tölgy, dió, beton, len);
  - matt, selyemfényű vagy magasfényű felület;
  - 4 fogantyútípus és 4 szín;
  - polcok rekeszenként;
  - LED, takaróléc, tárolódobozok;
  - szoba- vagy stúdiónézet.
- Kattintásra nyíló ajtók, élő becsült ár. A „Terv mentése” képpel együtt elmenti a tervet.
- **Elakadás:** a böngésző file:// alatt nem enged képet tölteni a WebGL-be → a fa- és kőtextúrákat a kód rajzolja canvasra.

### Publikálás – GitHub Pages
- A repót (mbolgar11/zenit) Claude a gépemről hozta létre és pusholta, mert a felhős munkaterületről a GitHub nem érhető el. A Pages-t is ő kapcsolta be.
- **Elakadás:** a GitHub API a gépemről időnként HTTP/2-hibát adott, és a github.io sem volt elérhető onnan → az élő oldalt Claude a beépített böngészőben ellenőrizte.
- **Elakadás:** élesben a betűtípusok 404-et adtak. A CSS-ben a font útvonala az oldalhoz volt relatív (assets/fonts/…), nem a CSS-fájlhoz (../fonts/…) → javítva és újra pusholva.
- Projekt oldal:
  - **interaktív 3D nézegető** a GLB-modellből: robbantott nézet, az ELIA szekrény ki-be kapcsolása, ajtók, vasalatok;
  - letöltések (F3D, STEP, GLB, PDF, Excel);
  - ez a napló, a videók és a GitHub-link.

### Videó narrációval + promóvideó
- **Narráció:**
  - A szokásos hangforrások (HuggingFace, online TTS) nem voltak elérhetők.
  - Claude megtalálta ugyanazokat a magyar **Piper**-hangokat a sherpa-onnx GitHub-kiadásai között.
  - A Piper TTS a gépemen fut, teljesen helyben. Három hangmintát kaptam (Anna, Berta, Imre); a videóhoz Anna hangja készült.
  - **Elakadás:** a sherpa-onnx 2.0 nem tudta a magyar szöveget hangokra bontani → a piper-tts csomag ugyanazzal a modellel működött.
- **3D felvételek:**
  - Este a Fusion MCP nem válaszolt → a forgó és robbantott 3D felvételek a GLB-ből készültek, a weboldal nézegetőjével (ugyanaz a v10 geometria).
  - **Trükk:** a requestAnimationFrame-et és az időt kézzel léptettük, így a lassú szoftveres WebGL ellenére is egyenletes 30 fps lett.
  - A teljes képernyőkép kockánként 4 s volt → helyette a WebGL-vásznat mentjük közvetlenül, és a felületet csak akkor fényképezzük, ha változik.
- **Feliratok:**
  - A Pillow nem tudta összefűzni a betűtípus ékezetes (latin-ext) részhalmazait.
  - Ezért a feliratok HTML-ben készülnek, a weboldal betűivel, és átlátszó PNG-ként kerülnek a képre.
- **Vágás:**
  - Jelenetenként egy MP4 (1920×1080, 30 fps), Ken Burns-mozgás, áttűnések, felirat-animáció.
  - A jeleneteket az ffmpeg veszteség nélkül fűzi össze.
  - Alá egy numpy-val szintetizált lágy akkordpad, amely beszéd alatt automatikusan halkul.
- **Ellenőrzés a teljes render előtt:** a legzsúfoltabb pillanatokról állóképek készültek.
  - Az ár a fehér rajzon olvashatatlan volt → sötét dobozba került.
  - A felirat rálógott a Fusion-képre → átrendeztük.
- **Eredmény:**
  - projektvideó ~2:12, 9 fejezet: kiindulópont, 3D modell, részletek, gyártás, márka, weboldal és tervező, AI-munkamódszer;
  - promóvideó ~0:31.

## 3. nap – csütörtök, nov. 5.

### Prémium újratervezés (v6)
- **A kérés (20 pontban):**
  - tükör bárhová;
  - hülyebiztos szerelési útmutató szerszámlistával, szerelési videó a vevő saját tervéhez, brandelt kézikönyv;
  - plafon- és falkiegyenlítés 10 cm-ig;
  - kevesebb sötét felület, stock fotók és videók, görgetésre változó háttér;
  - kitalált díjak és kiállítások;
  - élethűbb képek, látható (de lágy) élek, belső LED-kép;
  - ajtónként állítható nyitásirány, plafon nélküli szobanézet a tervezőben;
  - „projekt számokban”, high-end ügynökségi hatás.
- **Inspiráció:** Claude a megadott oldalak felépítését elemezte (Octagon Works, Prodomo, Mondini, BFP, Rossato). Átvett elemek:
  - kis angol címkék magyar főcímek fölött;
  - folyamatlépések, anyagpaletta, GYIK, visszatérő konzultációs CTA.
- **Stock anyagok:**
  - A felhős munkaterület és a gépem virtuális gépe nem éri el a képoldalakat, a beépített böngésző viszont igen. 31 Unsplash-fotó és 20 Pexels-videó a böngészőből töltődött le, majd átkerült a `08_Media` mappába, licencnyilvántartással együtt.
  - **Elakadás:** minden letöltés külön engedélyablakot dobott. Tanulság: egyszerre, csomagban kell letölteni.
- **Egységes színvilág:**
  - Saját fotószűrő (Pillow): meleg árnyékok, krémes csúcsfények, visszafogott telítettség.
  - Videószűrő (ffmpeg, a gépemen): eq + colorbalance + finom filmszemcse.
  - A klipek 6–8 másodperces, néma, hurkolható háttérvideók, 0,2–1,4 MB-osak.
- **Dizájnrendszer v2:**
  - elefántcsont, kő és espresso felületek váltakozva;
  - a fejléc a mögötte lévő szakasz színéhez igazodik;
  - scrollytelling (görgetésre váltó, „ragadós” képek), parallax videósávok, len- és tölgytextúrás szakaszok;
  - egymásra csúsztatott képek, futó szalag, számláló, masonry galéria szűrővel, díjsáv.
  - A díjak és kiállítások a látványprojekt részeként kitaláltak – ezt a díjsáv alatt és a láblécben is jelezzük.
- **Pontosítás:** a „~1 m³ extra tárhely” túlzás volt; a valós belső térfogat 2464 × 579 × 494 mm ≈ 0,7 m³, ez került az oldalra.

### Szerelési útmutató, kézikönyv, szerelési videó
- **Ábrák:**
  - Az ábrák a gyártási geometriából generálódnak (illus.py): ferde axonometria, vonalas stílus, az aktuális alkatrész bronz kiemeléssel.
  - A furat- és vasalatpozíciók is a modellből jönnek.
  - 12 lépés és 11 alkatrészrajz (A–L).
- **Szerelés oldal:** szerszámok ikonokkal, alkatrészek, vasalatlista, lépések időigénnyel és figyelmeztetésekkel.
- **Személyre szabott kézikönyv:**
  - A mentett tervből készül: méret, ajtók és nyitásirány, tükör, kiegyenlítés, a tervhez számolt vasalatlista.
  - A lépések szövege is a tervhez igazodik: távtartó, ferde takaróléc, nyitásirányok.
  - A végén ápolás és garancialap sorszámmal. Nyomtatható és PDF-be menthető (A4).
- **Referencia-kézikönyv PDF:** ugyanebből a nézetből, Chromiummal nyomtatva.
- **Szerelési animáció a tervezőben:** a vevő saját tervéből; a lépéseket feliratok kísérik, a kamera lassú ívben mozog. „Szerelési videó letöltése”: a böngésző WebM-videót rögzít (MediaRecorder), feliratokkal.
- **Narrált szerelési MP4:**
  - ugyanez az animáció, a gépemen generált narrációval (Piper, Anna hangja);
  - a lépések hossza a narrációhoz igazodik.
  - **Elakadás:** az első képkockán negatív időbélyeg miatt összeomlott az animáció → értékhatár-ellenőrzés került bele.
  - **Elakadás:** a kamera irányát nem frissítette (`lookAt` hiányzott) → javítva.

### Tervező v2
- Világos szoba és világos stúdió.
- A plafonlap helyett bronz, szaggatott plafonvonal, így felülről is látszik minden.
- Ajtónként állítható nyitásirány (bal/jobb) és front (lap/tükör).
- **Ferde plafon (0–10 cm):** a takaróléc automatikusan ferdére szabva készül.
- **Falkiegyenlítés (0–10 cm):** rejtett távtartók.
- Az ár a tükörrel és a kiegyenlítéssel együtt számolódik.
- Pontos színkezelés (sRGB): a kasmír valóban kasmírnak látszik.
- **Elakadás:** a tervező „szobában” nézetben a kamera a szoba falán kívül állt → a szoba előre meghosszabbítva, a keretezés újrahangolva.

### Látványtervek v2 (Blender)
- Lágy élkiemelés a lapokon (bevel-normál alapú élmaszk), így a bútor körvonala kirajzolódik, de nem fekete.
- Deszkás padló, modern absztrakt festmény, könyvek, váza, olvasófotel, állólámpa, szürkületi ég az ablakban.
- Új képek:
  - belső LED közelről, a polcokon összehajtott textilekkel és bőrönddel;
  - tükrös középső ajtó;
  - fékes pánt közelről;
  - világos robbantott nézet.
- **Elakadás:** a nappali képek kiégtek → levett expozíció.
- **Elakadás:** a várakozó szkript a saját parancssorát találta meg (`pgrep`) → közvetlen indítás.
- **Elakadás:** a környezet újraindult, a háttérfolyamatok leálltak → újraindítás onnan, ahol tartottak (a kész képek megmaradtak).

### Rendrakás
- A tegnapi ZENIT- és Ratet-fájlok a Letöltések mappából: amelyik már megvolt a munkamappában, az törölve, a többi áthelyezve.

### Finomhangolás (v7): láthatóság, változatosság, mozgókép
- **Visszajelzés:** több szín és szögből készült kép, más-más berendezéssel; nagy kép/videó a Szerelés és a Garancia oldal tetejére; néhány sötétebb és elmosott képsáv; kevesebb ismétlődő kép; a fékes pánt belülről; ajtónyitás-animáció LED-del és tárgyakkal; sötétebb falak, hogy a kasmír kiemelkedjen.
- **Tervező:**
  - Mélység 30–70 cm csúszkával, a javasolt érték (az alsó szekrény mélysége) külön kiemelve.
  - Ajtónként max. 90 cm.
  - A rúdfogantyú vízszintesen, az ajtó alján.
  - A négy fő funkció (szerelés lejátszása, videó letöltése, kézikönyv, terv mentése) ikonos csempékre került.
- **Színek és fények a tervezőben:**
  - A kasmír kifakult, mert a környezeti fény (RoomEnvironment) és a félgömbfény összeadódott.
  - Javítás: a környezeti visszaverődés 0,3-re visszafogva a nem fémes felületeken, gyengébb fények, melegszürke fal és háttér, füstölt tölgy padló.
  - Így a kasmír ajtó tisztán elválik a faltól.
- **Előtte/utána csúszka:** vastagabb, árnyékolt vonal, sötét fogó „Húzd” felirattal, és az első megjelenéskor egy rövid „lebbenés”, ami jelzi, hogy húzható.
- **Új látványtervek (Blender):**
  - második berendezés: diófa komód, lámpa, kerek tükör, kárpitozott pad pléddel, függöny, olajfa;
  - kasmír esti fényben, nyitva belső LED-del, zsálya, éjkék, natúr tölgy, grafit + dió alulnézetből;
  - a fékes pánt belülről.
  - **Elakadás:** a növény levelei pálcikának látszottak, egyenként másolt objektumként pedig nem jelentek meg a renderen. Megoldás: a levelek (bmesh) egyetlen hálóba épülnek, olajfa-szerű ágakkal.
- **Egységes fotós utómunka:** nappali képeken lágy, vállas tónusgörbe, minden képen finom vignetta.
- **Mozgókép a tervezőből:**
  - Determinisztikus felvétel (Playwright, rögzített időléptetés): ajtónyitás belső fénnyel és tárgyakkal; új szerelési felvétel a sötétebb szobával.
  - Ebből készült a szerelési oldal háttérvideója és a narrált szerelési videó új változata.
- **Oldalak:**
  - Szerelés: háttérvideós fejléc, sötét szerszámszakasz, elmosott műhelyképsáv.
  - Garancia: esti render a fejlécben, elmosott képsáv, sötét „Amit vállalunk” blokk.
  - A ZENIT oldalon „Nyisd ki” videóblokk.
