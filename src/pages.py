# ZENIT oldalak (a build.py-ból fut). Szövegek: prémium, nyugodt, „csak a tiéd”.

# ======================================================================== KEZDŐLAP
HERO = f'''<section class="hero" id="top">
  <div class="media"><video data-bg muted loop playsinline autoplay preload="auto" poster="{R}hero_evening.jpg" src="assets/m/video/hero.mp4"></video></div>
  <div class="wrap content">
    <div>
      <div class="label reveal" style="color:var(--bronze2)">ZENIT Atelier · Budapest</div>
      <h1 class="h-display lines"><span class="ln"><span>Ahol a szekrényed véget ér,</span></span><span class="ln"><span><em>ott kezdődünk.</em></span></span></h1>
      <p class="lead reveal d2">Méretre épített felső szekrény a meglévő gardróbod tetejére – milliméterre a plafonig. Egyetlen otthonra tervezve: a tiédre.</p>
      <div class="acts reveal d3"><a href="zenit.html" class="btn fill">Ismerd meg <span class="arrow"></span></a><a href="tervezo.html" class="btn light">Tervezd meg a sajátod</a></div>
    </div>
    <div class="side reveal d3"><b>10 mm</b>ennyi marad a plafonig. A többi a tiéd.</div>
  </div>
  <span class="tag" style="left:auto;right:var(--pad);bottom:24px">Látványterv · kasmír</span>
  <div class="scrollcue"></div>
</section>'''

SCROLLY = f'''<section class="scrolly" data-theme="dark">
  <div class="stage">
    <figure class="on"><img src="{R}story_night.jpg" alt="Este: dobozok és bőrönd a gardrób tetején" loading="lazy"></figure>
    <figure><img src="{R}before_day.jpg" alt="Nappal: rendetlen sáv a szekrény fölött" loading="lazy"></figure>
    <figure><img src="{R}story_morning.jpg" alt="Reggel: a ZENIT a plafonig ér" loading="lazy"></figure>
    <figure><img src="{R}hero_evening.jpg" alt="Este: a ZENIT csendben, lámpafényben" loading="lazy"></figure>
    <div class="prog"><i class="on"></i><i></i><i></i><i></i></div>
    <span class="tag" style="left:auto;right:var(--pad)">Látványterv</span>
  </div>
  <div class="steps wrap">
    <div class="step"><div class="box"><div class="time">Este, tizenegy óra.</div><h2 class="h2">Lekapcsolod a villanyt. <em>Még egyszer látod.</em></h2><p>A bőröndöt a tavalyi nyaralásról. A dobozt, amit „majd elpakolsz”. Fél méter, ami minden este ugyanazt súgja: ez még nincs kész.</p></div></div>
    <div class="step"><div class="box"><div class="time">Ami fent van,</div><h2 class="h2">az fejben is <em>ott van.</em></h2><p>Egy szoba sosem lesz nyugodt, ha a legmagasabb pontja zajos. Rendet rakhatsz a polcokon – a szemed mindig felfelé téved.</p></div></div>
    <div class="step"><div class="box"><div class="time">Aztán egy reggel.</div><h2 class="h2">Egyetlen nyugodt felület. <em>Plafonig.</em></h2><p>A vonal ott fut tovább, ahol a szekrényed véget ért. A szoba magasabb lesz, a fal csendes, a bőrönd eltűnik egy ajtó mögött, ami puhán csukódik.</p></div></div>
    <div class="step"><div class="box"><div class="time">És este, megint.</div><h2 class="h2">Lekapcsolod a villanyt. <em>És csend van.</em></h2><p>Nem látsz semmit, ami dolgod lenne. Csak egy befejezett otthont – amit te terveztél.</p></div></div>
  </div>
</section>'''

FEATS = [("plafon", "Plafonig", "530 mm magas, 10 mm marad a plafonig. Nincs porfogó rés, nincs félbehagyott vonal."),
         ("nofuras", "Falfúrás nélkül", "Négy csavarral a szekrényedhez rögzül, belülről. Bérlakásban is – költözéskor viszed."),
         ("pant", "Csendes zárás", "Häfele Metalla 300SM pántok, felül fékes: az ajtó az utolsó centiken magától, puhán húz be."),
         ("led", "Belső fény", "Ajtónyitásra kigyúló, melegfehér LED – a legfelső polc is látható, este is."),
         ("tukor", "Tükör, ahová kéred", "Bármelyik ajtó lehet tükrös: a középső, a szélsők vagy mind. Egyesével választható."),
         ("szint", "Láthatatlan kiegyenlítés", "Ferde plafon vagy nem egyenes fal? Akár 10 cm eltérést is elnyelünk – egyedi takaróléccel.")]
FEATS_HTML = '<div class="feats reveal">' + "".join(f'<div class="feat">{icon(i)}<div class="no">{n + 1:02d}</div><b>{t}</b><span>{d}</span></div>' for n, (i, t, d) in enumerate(FEATS)) + '</div>'

PROCESS = [("alaprajz", "Tervezés", "Az élő 3D tervezőben vagy belsőépítészünkkel – a te méreteidre, a te színeidre."),
           ("cnc_kozel", "Precíziós gyártás", "CNC-vel vágott lapok, gépi élzárás, minden furat a 3D modellből – tizedmilliméterre."),
           ("veso2", "Kézi összeállítás", "Minden kötést, pántot és hézagot ember ellenőriz. A darab sorszámot és aláírást kap."),
           ("ruhak", "Szerelés és átadás", "Egy délután alatt, falfúrás nélkül. Mellé ábrás útmutató és a te tervedre szabott kézikönyv.")]
PROCESS_HTML = '<div class="process">' + "".join(f'<div class="pstep reveal{" d" + str(i) if i else ""}">{vid(v, "ar-34", tag="Hangulat")}<div class="no">{i + 1:02d}</div><b>{t}</b><span>{d}</span></div>' for i, (v, t, d) in enumerate(PROCESS)) + '</div>'

page("index.html", "ZENIT – Ahol a szekrényed véget ér, ott kezdődünk.",
     "ZENIT – méretre épített felső szekrény a meglévő gardróbod tetejére, milliméterre a plafonig. Egyedi, sorszámozott darab, magyar műhelyből.",
     HERO +
     S(AWARDS, "paper", "tight") +
     S(f'''<div class="reveal" style="text-align:center"><div class="label plain">A hiányzó fél méter</div></div>
<p class="big center reveal d1" style="margin-top:28px;max-width:22ch">Minden otthonban van fél méter, amit senki sem tervezett meg. <em>Mi megterveztük.</em></p>
<div class="split reveal d2" style="margin-top:clamp(50px,6vw,90px);align-items:start;gap:clamp(30px,5vw,80px)"><div class="prose"><p>A gardrób teteje és a plafon között ott a lakás legzajosabb csendje: dobozok, bőröndök, por. A ZENIT ezt a sávot az otthonod legelegánsabb részévé teszi – a te szekrényedre, a te plafonodra, a te színeidre szabva.</p></div>
<div class="prose"><p>Nem egy újabb bútor kerül a szobádba. A meglévő szekrényed kap befejezést – olyat, mintha mindig is így tervezték volna. Kasmírban, tölgyben, vagy abban az árnyalatban, amit csak te ismersz.</p></div></div>''') +
     SCROLLY +
     S(f'''<div class="split wide-r">
  <div class="reveal"><div class="label">Egyedi darab</div><h2 class="h2">Te rajzolod meg. <em>Mi megépítjük.</em></h2>
    <div class="prose"><p>A ZENIT nem raktárról érkezik. A te arányaidból, a te színeidből, a te plafonodból születik – és csak egyszer készül el. Te döntöd el, hány ajtó nyíljon és merre, hol legyen tükör, milyen fény gyúljon, amikor kinyitod.</p>
    <p>Benne van az alkotói kedved – és a mi műhelyünk nyugalma. Az izgalom, hogy valami a tiéd lesz. És a csend, amikor elkészül.</p></div>
    <div class="acts"><a class="btn fill" href="tervezo.html">Tervezd meg <span class="arrow"></span></a><a class="more" href="keszites.html">Így készül <span class="arrow"></span></a></div></div>
  <div class="overlap reveal d1">{img(R + "hero_day.jpg", "ZENIT kasmír felső szekrény világos hálószobában", "ar-43 a", "Látványterv")}{img(R + "macro_handle.jpg", "Lekerekített GTV HEXA alumínium élfogantyú közelről", "ar-11 b")}</div>
</div>''', "paper") +
     MARQUEE +
     band(V + "gyalu_kez.mp4", "Manufaktúra", "Kézzel épített. <em>Digitálisan megtervezve.</em>",
          "A magyar asztaloshagyomány türelme és a parametrikus 3D tervezés pontossága egyetlen bútorban. Minden furat helye a modellből jön – minden illesztést ember ellenőriz.",
          '<a class="btn light" href="manufaktura.html">A műhely <span class="arrow"></span></a>') +
     f'<section class="sec tex-linen"><div class="wrap">{head("Részletek", "Hat döntés, <em>amit sosem bánsz meg.</em>", "Mindegyik apróság. Együtt ezek adják azt a nyugalmat, amit nap mint nap érzel – akkor is, ha már észre sem veszed.")}{FEATS_HTML}</div></section>' +
     S(f'''<div class="split">
  <div class="reveal">{img(R + "b_open_led.jpg", "Nyitott kasmír ZENIT esti fényben, belső LED-del, bőrönddel és összehajtott textilekkel", "ar-45", "Látványterv · belső LED")}<p class="cap">Belső fény – ajtónyitásra, melegfehér 2700 K.</p></div>
  <div class="reveal d1" style="padding-top:12%">{img(R + "mirror_day.jpg", "ZENIT tükrös középső ajtóval nappali fényben", "ar-45", "Látványterv · tükrös ajtó")}<p class="cap">Tükör a középső ajtón – vagy bárhol, ahol kéred.</p>
    <h3 class="h3" style="margin-top:40px">Fény, ami <em>vár rád.</em> Tükör, ami <em>tágít.</em></h3>
    <p class="lead" style="margin-top:16px;font-size:16px">Kinyitod, és a legfelső polc is világos. Becsukod, és a szoba eggyel nagyobbnak látszik. Két apró döntés, ami minden nap ott van.</p></div>
</div>''', "paper", style="padding-top:0") +
     S(head("A ZENIT számokban", "Pontosság, <em>amit nem látsz.</em> Csak érzel.") + nums(NUMS), "dark") +
     S(head("Inspiráció", "Egy forma, <em>ezer otthon.</em>", "Kasmír az eredeti. De a ZENIT-et a te otthonod fejezi be – nézd meg, hogyan él különböző terekben.") +
       f'''<div class="cards">
  <a class="card reveal" href="inspiracio.html">{img(R + "v_tolgy_day.jpg", "Natúr tölgy ZENIT fekete élfogantyúval, nappali fényben", "ar-45", "Látványterv")}<b>Natúr tölgy</b><span>Japandi nyugalom, valódi erezettel.</span></a>
  <a class="card reveal d1" href="inspiracio.html">{img(F + "foto_131.jpg", "Meleg fényű, letisztult belső tér", "ar-45", "Hangulat")}<b>Esti fény</b><span>Len, függöny, lámpafény – és csend.</span></a>
  <a class="card reveal d2" href="inspiracio.html">{img(R + "b_ejkek_evening.jpg", "Éjkék ZENIT bronz fogantyúval, esti fényben, kárpitozott paddal", "ar-45", "Látványterv")}<b>Éjkék és bronz</b><span>Bátor, mély, elegáns.</span></a>
</div><div class="acts reveal" style="justify-content:center"><a class="more" href="inspiracio.html">Minden inspiráció <span class="arrow"></span></a></div>''', "ivory") +
     S(head("Tervtől a plafonig", "Négy lépés. <em>Nulla kompromisszum.</em>", "Három-négy hét a rendeléstől a csendes első zárásig. Közben végig tudod, hol tart a darabod.") + PROCESS_HTML, "paper") +
     S('<div class="quote reveal"><blockquote>„Egy szekrényt nem akkor fejezünk be, amikor összeáll, hanem amikor az ajtó először csendben becsukódik.”</blockquote><cite>ZENIT műhely · Budapest</cite></div>', "stone") +
     band(R + "story_morning.jpg", "Concierge", "Kezdjük el <em>a te ZENIT-edet.</em>",
          "Tervezd meg pár perc alatt az élő 3D tervezőben – vagy beszélj egy belsőépítésszel, aki visszahív.",
          '<a class="btn fill" href="tervezo.html">Tervező <span class="arrow"></span></a><a class="btn light" href="concierge.html">Tervező hív vissza</a>', center=True) +
     nxt("01", "zenit.html", "A ZENIT", "Felépítés, méretek, fény, tükör és kiegyenlítés – a hiányzó fél méter, részletesen."))

# ======================================================================== A ZENIT
ANAT = [("Egy korpusz, egybefüggő tetővel", "Nincsenek toldások, nincs látható illesztés – a vonal egyetlen mozdulat."),
        ("Tipli és konfirmát kötés", "Ragasztó nélkül szilárd, évtizedekre – és bármikor szétszedhető."),
        ("Häfele Metalla 300SM pántok", "110°-os nyitás, felül fékes, alul rugós; háromdimenziósan állítható."),
        ("2 mm-es, lekerekített ajtóél", "Kopásálló ABS, kézbe simuló – az ajtó minden érintésnél ugyanolyan."),
        ("GTV HEXA élfogantyú, 192 mm", "Lekerekített, eloxált alumínium; hátulról csavarozva, a fronton nincs csavarfej."),
        ("Polc három csapon oldalanként", "Nem billeg, nem hajlik; a szélső rekeszekbe később is bővíthető."),
        ("Szegezett HDF hátfal", "Merevít, zár, és kívülről sosem látszik.")]
OPTS = [(R + "mirror_day.jpg", "Tükör", "Ajtónként választható. Tágítja a teret, és a legfelső polcig minden látszik benne."),
        (R + "led_detail.jpg", "Belső LED", "Ajtónyitásra kigyúló, melegfehér fénycsík minden rekeszben."),
        (R + "macro_handle.jpg", "Élfogantyú", "GTV HEXA, 192 mm, lekerekített alumínium – vagy bronz, fekete, bőr."),
        (R + "hinge_in.jpg", "Fékes pánt", "Häfele Metalla 300SM: a zárás utolsó centijén magától, csendben húz be."),
        (R + "macro_edge.jpg", "Az él", "2 mm-es ABS az ajtókon, 0,4 mm a korpuszon – sorjamentesen, kézzel ellenőrizve."),
        (R + "exploded_light.jpg", "Tizenegy elem", "Előfúrva érkezik; a szerelés két emberrel kb. három óra.")]
OFFSET_SVG = '''<svg viewBox="0 0 520 300" width="100%" style="max-width:560px" fill="none" stroke="currentColor" stroke-width="1.2" font-family="Inter" font-size="12">
  <path d="M20 40 L500 18" stroke="#A27D4A" stroke-width="1.6"/><text x="380" y="14" fill="#A27D4A" stroke="none">ferde plafon</text>
  <rect x="80" y="62" width="360" height="90" fill="#E9E1D4"/><path d="M80 62 L80 50 L440 34 L440 62 Z" fill="#D8BF97" stroke="#A27D4A"/>
  <text x="160" y="56" fill="#5A5148" stroke="none" font-size="11">egyedi, ferdére szabott takaróléc</text>
  <rect x="80" y="152" width="360" height="130" stroke-dasharray="5 4" opacity=".6"/><text x="200" y="225" fill="#8A8176" stroke="none">meglévő szekrény</text>
  <path d="M470 62v-28M465 40l5-6 5 6M465 56l5 6 5-6" stroke="#A27D4A"/><text x="478" y="52" fill="#A27D4A" stroke="none">0–10 cm</text>
  <path d="M60 62v220" stroke-dasharray="2 3"/><path d="M40 62v220" stroke="#5A5148"/><text x="2" y="170" fill="#5A5148" stroke="none" transform="rotate(-90 12 170)">fal</text>
  <path d="M44 100h34M50 95l-6 5 6 5M72 95l6 5-6 5" stroke="#A27D4A"/><text x="40" y="118" fill="#A27D4A" stroke="none" font-size="11">falkiegyenlítés 0–10 cm</text>
</svg>'''
page("zenit.html", "A ZENIT – felső szekrény a plafonig", "A ZENIT felépítése, opciói (tükör, LED, fogantyú), kiegyenlítés, méretek és számok.",
     page_hero("Kollekció · 01", "A hiányzó fél méter, <em>megoldva.</em>",
               "Egy korpusz, egybefüggő tető, csendes ajtók. Méretre tervezve a meglévő szekrényedhez – a plafonig.",
               [("index.html", "ZENIT"), ("", "Kollekció"), ("", "A ZENIT")], R + "after_day.jpg", tag="Látványterv · kasmír") +
     S(head("Előtte, utána", "Ugyanaz a szoba. <em>Más nyugalom.</em>", "Húzd a csúszkát: a dobozok és a por helyén egyetlen, csendes felület – a plafonig.") +
       f'''<div class="ba reveal"><img src="{R}after_day.jpg" alt="Utána: a gardrób a ZENIT felső szekrénnyel">
  <div class="before"><img src="{R}before_day.jpg" alt="Előtte: dobozok a szekrény fölött"></div><div class="handle"></div>
  <span class="lbl" style="left:18px">Előtte</span><span class="lbl" style="right:18px">Utána</span><span class="tag">Látványterv</span></div>''', "paper") +
     S(head("Nyisd ki", "Kinyitod, <em>és fény gyúl.</em>", "Fékes pántok, melegfehér LED minden rekeszben – és hely mindannak, ami eddig a szekrény tetején porosodott. Valós idejű 3D-felvétel a tervezőből.")
       + vid("nyitas", "ar-169", "Élő 3D · a tervezőből") + '<div class="acts reveal" style="justify-content:center;margin-top:34px"><a class="btn light" href="tervezo.html#preset=led">Nyisd ki a tervezőben <span class="arrow"></span></a></div>', "dark") +
     S(f'''<div class="split wide-l">
  <div class="reveal">{img(R + "exploded_light.jpg", "A ZENIT robbantott nézete", "ar-32", "Látványterv · robbantott nézet")}</div>
  <div class="reveal d1"><div class="label">Felépítés</div><h2 class="h2">Egy bútor. <em>Harminc gondos részlet.</em></h2>
  <ol style="list-style:none;padding:0;margin:0;counter-reset:a">''' + "".join(
           f'<li style="display:grid;grid-template-columns:44px 1fr;padding:14px 0;border-bottom:1px solid var(--ln)"><span style="font:300 22px var(--serif);color:var(--bronze)">{i + 1:02d}</span><span><b style="font-weight:500">{t}.</b> <span style="color:var(--fg2)">{d}</span></span></li>'
           for i, (t, d) in enumerate(ANAT)) + '</ol></div></div>') +
     S(head("Opciók", "A te döntéseid. <em>A mi pontosságunk.</em>", "Minden opció a tervezőben, élőben kipróbálható – és pontosan úgy készül el, ahogy látod.") +
       '<div class="cards">' + "".join(f'<div class="card reveal{" d" + str(i % 3) if i % 3 else ""}">{img(s, t, "ar-45", "Látványterv")}<b>{t}</b><span>{d}</span></div>' for i, (s, t, d) in enumerate(OPTS)) + '</div>', "paper") +
     S(f'''<div class="split"><div class="reveal"><div class="label">Kiegyenlítés</div><h2 class="h2">Ha a ház nem tökéletes, <em>a ZENIT az.</em></h2>
  <div class="prose"><p>A régi lakások plafonja ritkán vízszintes, a falak ritkán egyenesek. A tervezőben megadhatod a bal és jobb oldali plafonmagasság közti különbséget és a fal felé szükséges kiegyenlítést – mindkettőt 10 cm-ig.</p>
  <p>A korpusz mindig vízszintes és derékszögű marad; az eltérést egyedire szabott, a szekrénnyel azonos színű takaróléc és rejtett távtartó veszi fel. Kívülről csak annyi látszik, hogy a ZENIT pontosan odaér.</p></div>
  <div class="acts"><a class="btn" href="tervezo.html">Kipróbálom a tervezőben <span class="arrow"></span></a></div></div>
  <div class="reveal d1" style="color:var(--ink)">{OFFSET_SVG}</div></div>''', "stone") +
     S(head("Méretek", "Méretre szabva, <em>nem méretre vágva.</em>") + '''<dl class="specs reveal">
  <div><dt>Szélesség</dt><dd>60 – 280 cm</dd></div><div><dt>Ajtók</dt><dd>1 – 6, ajtónként max. 90 cm, nyitásiránnyal</dd></div><div><dt>Magasság</dt><dd>a plafonodhoz, −10 mm</dd></div>
  <div><dt>Mélység</dt><dd>30 – 70 cm (javasolt: az alsó szekrényé)</dd></div><div><dt>Kiegyenlítés</dt><dd>plafon és fal, 0 – 10 cm</dd></div><div><dt>Pántok</dt><dd>Häfele Metalla 300SM, 110°</dd></div>
  <div><dt>Fogantyú</dt><dd>GTV HEXA 192, lekerekített</dd></div><div><dt>Rögzítés</dt><dd>a szekrényhez, falfúrás nélkül</dd></div><div><dt>Elkészülés</dt><dd>3 – 4 hét</dd></div>
</dl>''', "paper") +
     S(head("A referencia-darab számokban", "Bútorline ELIA 250 fölé, <em>kasmírban.</em>", "A bemutatott ZENIT egy valódi szekrényre készült: 250 × 205 × 60 cm, belmagasság a legalacsonyabb ponton 259 cm.") + nums(NUMS), "dark") +
     nxt("02", "anyagok.html", "Anyagok és színek", "Kasmír, natúr tölgy, éjkék – és a részlet, amit minden nap megérintesz."))

# ======================================================================== ANYAGOK
UNI = [("Kasmír", "#CDBFAE", "a ZENIT alapszíne"), ("Kréta", "#F1EFEA", ""), ("Homok", "#D8CBB3", ""), ("Zsálya", "#A4AD98", ""),
       ("Agyag", "#A7735A", ""), ("Grafit", "#4A4846", ""), ("Éjkék", "#273445", ""), ("Fekete", "#1B1A19", "")]
pal = "".join(f'<div class="reveal" style="text-align:center"><div style="aspect-ratio:1;border-radius:50%;background:{c};box-shadow:inset 0 0 0 1px rgba(0,0,0,.08),0 18px 30px -18px rgba(20,17,14,.4)"></div><b style="display:block;font:300 22px var(--serif);margin-top:16px">{n}</b><span class="small">{c}{" · " + d if d else ""}</span></div>' for n, c, d in UNI)
page("anyagok.html", "Anyagok és színek – ZENIT", "A ZENIT színpalettája, textúrái, fogantyúi, fénye és tükre.",
     page_hero("Kollekció · 02", "Amit érintesz, <em>annak súlya van.</em>",
               "Kurált színek, valódi fa hatású textúrák, lekerekített alumínium, meleg fény. Minden anyag azért van itt, mert évekig jó érinteni.",
               [("index.html", "ZENIT"), ("", "Kollekció"), ("", "Anyagok és színek")], F + "foto_093.jpg") +
     S(f'''<div class="split wide-l"><div class="reveal">{img(R + "hero_evening.jpg", "Kasmír ZENIT esti fényben", "ar-43", "Látványterv · kasmír")}</div>
  <div class="reveal d1"><div class="label">Kasmír</div><h2 class="h2">Az eredeti. <em>Meleg, csendes, időtlen.</em></h2>
  <div class="prose"><p>A kasmír a ZENIT alapszíne: meleg szürkésbézs, ami reggel krémesnek, este mézszínűnek látszik. A Bútorline ELIA kasmír szekrényekhez hangolva – a két bútor egyetlen tömbbé olvad.</p></div></div></div>''', "paper") +
     S(head("Uni paletta", "Nyolc szín. <em>És a tiéd.</em>", "Matt, selyemfényű vagy magasfényű felülettel. Ha a te árnyalatod nincs köztük, add meg a pontos HEX-kódját – mi kikeverjük.") +
       f'<div style="display:grid;grid-template-columns:repeat(8,1fr);gap:clamp(12px,2vw,28px)" class="palgrid">{pal}</div>', "ivory") +
     f'<section class="sec tex-oak"><div class="wrap">' + head("ZENIT Natúr", "Fa, kő, <em>len.</em>", "Valódi erezetű tölgy és dió, nyugodt beton, puha len. Az ajtók erezetét egyenként párosítjuk.") +
     '<div class="cards">' + "".join(f'<div class="card reveal{" d" + str(i) if i else ""}">{img(s, t, "ar-11", tg)}<b>{t}</b><span>{d}</span></div>' for i, (s, t, d, tg) in enumerate([
         ("assets/img/r/tex_oak.jpg", "Natúr tölgy", "Világos, nyugodt erezet – japandi és skandináv terekhez.", "Textúra"),
         ("assets/img/r/tex_walnut.jpg", "Dió", "Mély, meleg barna – esti fényben a legszebb.", "Textúra"),
         (F + "foto_146.jpg", "Len", "Puha, mátt textúra – a belső térben és a tárolódobozokon.", "Hangulat")])) + '</div></div></section>' +
     S(f'''<div class="split wide-r"><div class="overlap reveal">{img(R + "macro_handle.jpg", "GTV HEXA élfogantyú kasmír ajtón", "ar-43 a", "Látványterv")}{img(R + "hinge_in_detail.jpg", "Häfele fékes pánt közelről", "ar-11 b")}</div>
  <div class="reveal d1"><div class="label">Vasalat</div><h2 class="h2">A részlet, <em>amit minden nap megérintesz.</em></h2>
  <div class="prose"><p>Alapfelszereltség a GTV HEXA lekerekített alumínium élfogantyú, 192 mm-es furattávval: hátulról csavarozzuk, így a fronton nincs csavarfej. Kérhető matt fekete, szálcsiszolt bronz vagy bőr kivitelben, illetve rúd, gomb vagy nyomásra nyíló változatban.</p>
  <p>A pántok Häfele Metalla 300SM, 110°-os pántok: felül fékes, alul rugós. Az ajtó az utolsó centiken magától, hangtalanul húz be.</p></div></div></div>''', "paper") +
     S(f'''<div class="split"><div class="reveal"><div class="label">Fény és tükör</div><h2 class="h2">Meleg fény. <em>Tágabb tér.</em></h2>
  <div class="prose"><p>A belső LED ajtónyitásra gyullad fel: 2700 K-es, melegfehér fény, ami a textileket és a fát is a valódi színükben mutatja. A tükör bármelyik ajtóra kérhető – 4 mm-es, biztonsági fóliával, keskeny kasmír kerettel.</p></div></div>
  <div class="reveal d1">{img(R + "open_led.jpg", "Nyitott ZENIT belső LED-fénnyel", "ar-43", "Látványterv · belső LED")}</div></div>''', "stone") +
     nxt("03", "manufaktura.html", "Manufaktúra", "Kéz, gép, terv – és a díjak, amelyekre büszkék vagyunk."))

# ======================================================================== MANUFAKTÚRA
page("manufaktura.html", "Manufaktúra – ZENIT", "Magyar kézművesség és digitális pontosság: így készül a ZENIT. Díjak, kiállítások, műhely.",
     page_hero("Kollekció · 03", "Nem gyártjuk. <em>Megépítjük.</em>",
               "Minden ZENIT egyetlen otthonra készül – a magyar asztalosműhelyek generációkon át csiszolt tudására és a mai legpontosabb technológiára építve.",
               [("index.html", "ZENIT"), ("", "Kollekció"), ("", "Manufaktúra")], V + "gyalu.mp4", tag="Hangulat") +
     S(f'''<div class="split wide-r"><div class="overlap reveal">{img(F + "foto_046.jpg", "Asztalosműhely munkapaddal, ablakfényben", "ar-43 a", "Hangulat")}{img(F + "foto_086.jpg", "Régi gyaluk a műhely falán", "ar-11 b", "Hangulat")}</div>
  <div class="reveal d1"><div class="label">Örökség</div><h2 class="h2">A magyar asztaloshagyomány <em>csendes pontossága.</em></h2>
  <div class="prose"><p>A jó asztalos mindig is arról volt híres, hogy az ajtaja évtizedek múlva is ugyanazzal a halk mozdulattal záródik. A ZENIT ebből a tudásból született: a tipli és a derékszög tiszteletéből, a hézag türelméből.</p>
  <p>Ma ugyanezt a gondosságot egy parametrikus 3D modell és tizedmilliméteres gépek viszik tovább – de minden darabot ember fejez be.</p></div></div></div>''', "paper") +
     MARQUEE +
     S(head("Részletek a műhelyből", "A kéz, az él <em>és a fa.</em>") + f'''<div class="cards">
  <div class="card reveal">{vid("veso_v", "ar-23", "Hangulat")}<b>A kéz</b><span>Véső, gyalu, türelem. Minden illesztést kézzel ellenőrzünk.</span></div>
  <div class="card reveal d1">{vid("csiszolo_v", "ar-23", "Hangulat")}<b>Az él</b><span>Gépi élzárás, kézi utánmunka: sorjamentes, kézbe simuló élek.</span></div>
  <div class="card reveal d2">{vid("forgacs_v", "ar-23", "Hangulat")}<b>A fa</b><span>Ahol forgács van, ott valaki gondosan dolgozott.</span></div></div>''', "ivory") +
     band(V + "cnc.mp4", "Digitális pontosság", "Tizedmilliméterre. <em>Minden alkalommal.</em>",
          "A te ZENIT-ed egy parametrikus 3D modellből születik: a szélességed, a plafonod és a választásaid minden lapot, furatot és pántot újraszámolnak. A CNC pontosan azt vágja, amit a terv mond.") +
     S(f'''<div class="split"><div class="reveal"><div class="label">Tervezés</div><h2 class="h2">Algoritmus <em>és ceruza.</em></h2>
  <div class="prose"><p>A ZENIT-et belsőépítészek, asztalosok és mérnökök közösen rajzolták – mesterséges intelligenciával gyorsítva, de emberi ízléssel eldöntve. Minden változat 3D-ben, Autodesk Fusionben készül, a gyártási dokumentáció automatikusan generálódik belőle.</p></div>
  <div class="acts"><a class="btn" href="keszites.html">Így készül <span class="arrow"></span></a></div></div>
  <div class="reveal d1">{vid("tervezes", "ar-43", "Hangulat")}</div></div>''', "paper") +
     S(head("Elismerések", "Díjak, <em>amelyekre büszkék vagyunk.</em>", "A ZENIT, a tervezőcsapat és a műhely munkája – itthon és külföldön.") + AWARDS +
       '''<div class="specs reveal" style="margin-top:50px">
  <div><dt>2026 · Milánó</dt><dd>Aurum Interior Award – arany, bútor kategória</dd></div>
  <div><dt>2026 · Milánó</dt><dd>Atelier Week – a ZENIT nemzetközi bemutatója</dd></div>
  <div><dt>2026 · Bécs</dt><dd>Atelier Europa Prize – Craft &amp; Technology</dd></div>
  <div><dt>2025 · Budapest</dt><dd>Pannon Mesterség Díj – az év bútora</dd></div>
  <div><dt>2025 · Budapest</dt><dd>Az év fiatal tervezőcsapata – Pannon Mesterség</dd></div>
  <div><dt>2026 · Koppenhága</dt><dd>Lumen Design Prize – fény a bútorban</dd></div>
</div>''', "stone") +
     S(f'''<div class="split"><div class="reveal" style="text-align:center"><img src="assets/ill/seal.svg" alt="ZENIT sorszám-pecsét" style="width:min(320px,70%);margin:0 auto;border-radius:50%"></div>
  <div class="reveal d1"><div class="label">Sorszámozva</div><h2 class="h2">Egyetlen darab. <em>Egyetlen otthon.</em></h2>
  <div class="prose"><p>Minden ZENIT egyedi sorszámot és a készítő aláírását kapja a tetőlap belső oldalán. Nincs raktárkészlet, nincs két egyforma: a te méreteidből, a te színeidből születik, és csak a tiéd lesz.</p></div>
  <dl class="specs" style="grid-template-columns:1fr 1fr;margin-top:30px"><div><dt>Készítés</dt><dd>Megrendelésre</dd></div><div><dt>Ellenőrzés</dt><dd>Kézzel, darabonként</dd></div><div><dt>Kötés</dt><dd>Ragasztó nélkül</dd></div><div><dt>Származás</dt><dd>Magyarország</dd></div></dl></div></div>''', "paper") +
     S('<div class="quote reveal"><blockquote>„A legjobb bútor az, amelyik úgy néz ki, mintha mindig is ott lett volna.”</blockquote><cite>A ZENIT tervezőcsapata</cite></div>', "ivory") +
     nxt("04", "inspiracio.html", "Inspiráció", "Nézd meg, hogyan él a ZENIT különböző otthonokban – és nyisd meg bármelyiket a tervezőben."))

# ======================================================================== INSPIRÁCIÓ
G = [("zenit", R + "hero_evening.jpg", "Kasmír · az eredeti", "Esti hálószoba", "kasmir", "ar-32"),
     ("hangulat", F + "foto_121.jpg", "Reggeli fény", "Hangulat", "", "ar-32"),
     ("zenit", R + "insp_tolgy.jpg", "Natúr tölgy · japandi", "Nappali fény", "tolgy", "ar-32"),
     ("hangulat", F + "foto_015.jpg", "Rend, ami nyugtat", "Hangulat", "", "ar-23"),
     ("zenit", R + "led_detail.jpg", "Belső fény", "Kasmír, LED", "led", "ar-45"),
     ("zenit", R + "insp_ejkek.jpg", "Éjkék + bronz", "Esti hálószoba", "ejkek", "ar-32"),
     ("hangulat", F + "foto_041.jpg", "Meleg minimalizmus", "Hangulat", "", "ar-45"),
     ("zenit", R + "mirror_day.jpg", "Tükrös középső ajtó", "Kasmír", "kasmir", "ar-32"),
     ("zenit", R + "b_kasmir_evening.jpg", "Kasmír · dióbútorokkal", "Esti fény", "kasmir", "ar-32"),
     ("zenit", R + "b_open_led.jpg", "Nyitva, belső fénnyel", "Kasmír, LED", "led", "ar-32"),
     ("anyag", F + "foto_135.jpg", "Len, összehajtva", "Anyag", "", "ar-23"),
     ("zenit", R + "insp_zsalya.jpg", "Zsálya · nyugodt nappal", "Nappali fény", "zsalya", "ar-32"),
     ("zenit", R + "b_zsalya_day.jpg", "Zsálya · oldalnézet", "Nappali fény", "zsalya", "ar-32"),
     ("hangulat", F + "foto_009.jpg", "Gardrób, tölgy polcok", "Hangulat", "", "ar-43"),
     ("zenit", R + "insp_grafit_dio.jpg", "Grafit + dió · városi loft", "Esti fény", "grafit", "ar-32"),
     ("zenit", R + "v_grafit_dio.jpg", "Grafit + dió · alulnézet", "Esti fény", "grafit", "ar-32"),
     ("zenit", R + "b_ejkek_evening.jpg", "Éjkék · dióbútorokkal", "Esti fény", "ejkek", "ar-32"),
     ("anyag", F + "foto_093.jpg", "Natúr tölgy", "Anyag", "", "ar-32"),
     ("zenit", R + "insp_kreta.jpg", "Krétafehér · skandináv reggel", "Reggeli fény", "kreta", "ar-32"),
     ("hangulat", F + "foto_128.jpg", "Esti csend", "Hangulat", "", "ar-23"),
     ("zenit", R + "story_morning.jpg", "Kasmír reggel", "Reggeli fény", "kasmir", "ar-32"),
     ("hangulat", F + "foto_037.jpg", "Napfény a hálóban", "Hangulat", "", "ar-43"),
     ("anyag", R + "macro_edge.jpg", "Az él", "Kasmír, 2 mm ABS", "", "ar-32")]
gal = "".join(
    f'<figure class="reveal" data-k="{k}">' + (f'<a href="tervezo.html#preset={p}">' if p else "") + img(s, t, ar, "Látványterv" if k == "zenit" else ("Hangulat" if k == "hangulat" else "Anyag")) + (f'</a>' if p else "")
    + f'<figcaption><b>{t}</b><span>{("Megnyitom a tervezőben →" if p else c)}</span></figcaption></figure>' for k, s, t, c, p, ar in G)
page("inspiracio.html", "Inspiráció – ZENIT", "ZENIT különböző otthonokban, színekben és fényekben – hangulatok és anyagok.",
     page_hero("Kollekció · 04", "Egy forma, <em>ezer otthon.</em>", "Válassz egy hangulatot, és nyisd meg a tervezőben – a színek és arányok már be lesznek állítva.",
               [("index.html", "ZENIT"), ("", "Kollekció"), ("", "Inspiráció")], V + "inspiracio_loop.mp4", tag="Látványtervek · hat szín, két berendezés") +
     S('<div class="chips reveal"><button class="chip on" data-f="*">Mind</button><button class="chip" data-f="zenit">ZENIT látványtervek</button><button class="chip" data-f="hangulat">Hangulatok</button><button class="chip" data-f="anyag">Anyagok</button></div>'
       f'<div class="masonry">{gal}</div>') +
     S('<div class="quote reveal"><blockquote>„Nem egy újabb doboz kerül a szekrényedre. A szekrényed kap befejezést.”</blockquote><cite>Tervezői jegyzet</cite></div>', "stone") +
     nxt("05", "keszites.html", "Így készül", "Tervtől a plafonig: a gyártás, a minőség és a részletek – és minden kérdésre válasz."))

# ======================================================================== ÍGY KÉSZÜL
TL = [("alaprajz", "Felmérés és terv", "A te méreteidből – vagy belsőépítészünk helyszíni felméréséből – parametrikus 3D modell készül. Minden lap, furat és pánt ebből számolódik."),
      ("cnc_tag", "Lapszabászat", "18 mm-es bútorlap, tizedmilliméteres CNC-vágás. A szabásterv két táblából hozza ki a teljes korpuszt."),
      ("el", "Élzárás", "Gépi élzárás: 2 mm-es ABS az ajtókon, 0,4 mm a korpusz látható élein – majd kézi sorjázás."),
      ("pantcsesze", "Fúrás", "108 furat a modell szerint: pántcsészék Ø35-tel, tiplik, konfirmátok, polctartó csapok, fogantyúfuratok."),
      ("veso2", "Kézi próbaszerelés", "A műhelyben összeállítjuk, beállítjuk a hézagokat, ellenőrizzük a záródást – majd lapra szedve csomagoljuk."),
      ("ruhak", "Szerelés nálad", "Mi szereljük, vagy te – ábrás útmutatóval és a te tervedre szabott kézikönyvvel, kb. három óra alatt.")]
tl = "".join(f'''<div class="split reveal" style="padding:clamp(30px,4vw,50px) 0;border-top:1px solid var(--ln);gap:clamp(30px,5vw,80px);{"direction:rtl" if i % 2 else ""}">
  <div style="direction:ltr">{vid(v, "ar-169", "Hangulat")}</div>
  <div style="direction:ltr"><div style="font:300 64px/1 var(--serif);color:var(--bronze)">{i + 1:02d}</div><h3 class="h3" style="margin:12px 0 14px">{t}</h3><p class="lead" style="font-size:16px">{d}</p></div></div>''' for i, (v, t, d) in enumerate(TL))
page("keszites.html", "Így készül – ZENIT", "A ZENIT gyártása lépésről lépésre: felmérés, lapszabászat, élzárás, fúrás, próbaszerelés, szerelés. GYIK.",
     page_hero("Kollekció · 05", "Tervtől a plafonig, <em>hat lépésben.</em>", "Nincs dobozos kompromisszum: minden ZENIT a te méreteidre készül, a műhelyben próbaszerelve érkezik.",
               [("index.html", "ZENIT"), ("", "Kollekció"), ("", "Így készül")], V + "uzem.mp4", tag="Hangulat") +
     S(tl, "paper") +
     S(f'''<div class="split"><div class="reveal">{img("assets/img/fusion_inside.png", "A ZENIT belső felépítése az Autodesk Fusion modellben", "ar-43", "3D gyártási modell · Fusion")}</div>
  <div class="reveal d1"><div class="label">A részletekben</div><h2 class="h2">Előfúrva, <em>előre gondolva.</em></h2>
  <div class="prose"><p>Minden furat helyét a 3D gyártási modell határozza meg: tipli és konfirmát kötés, pántcsésze, polctartó csap, fogantyú. A modellből automatikusan születik a szabásjegyzék, a furattábla, a rajzok – és a te szerelési útmutatód is.</p></div>
  <div class="acts"><a class="btn" href="szereles.html">Szerelési útmutató <span class="arrow"></span></a></div></div></div>''', "stone") +
     S(faq(FAQ), "ivory") +
     nxt("06", "szereles.html", "Szerelés", "Három óra, két ember, egy csendes szekrény – lépésről lépésre, ábrákkal."))

# ======================================================================== SZERELÉS
tools_needed = ["csavarozo", "imbusz", "gumikalapacs", "kalapacs", "meroszalag", "letra", "furo25", "pz2", "ket_fo", "vizmertek"]
TOOLSET = '<div class="toolset reveal">' + "".join(f'<div class="tl">{icon(t, "")}<b>{TOOLS[t][0]}</b><span>{TOOLS[t][1]}</span></div>' for t in tools_needed) + '</div>'
PARTS = '<div class="partsgrid reveal">' + "".join(f'<figure><img src="assets/ill/szereles/{p["file"]}" alt="{p["letter"]} – {p["name"]}" loading="lazy"><figcaption><b>{p["letter"]} · {p["name"]}</b>{p["dim"]}</figcaption></figure>' for p in STEPS["parts"]) + '</div>'
HWLIST = [("Fatipli 8×35", 16), ("Konfirmát 7×50 + sapka", 16), ("Häfele pánt (fékes/rugós)", 6), ("Häfele szerelőtalp", 6), ("Csavar 3,5×16", 30),
          ("Csavar 3,5×30", 4), ("Polctartó csap Ø5", 6), ("Hátfalszeg 1,6×25", 50), ("GTV HEXA 192 élfogantyú", 3)]
HW = '<div class="specs reveal" style="grid-template-columns:repeat(3,1fr)">' + "".join(f'<div><dt>{n}</dt><dd>{c} db</dd></div>' for n, c in HWLIST) + '</div>'
ST = "".join(f'''<div class="asmstep reveal"><div class="no">{s["no"]:02d}</div>
  <div class="ill"><img src="assets/ill/szereles/{s["svg"]}" alt="{s["no"]}. lépés: {s["title"]} – ábra" loading="lazy"></div>
  <div><h3>{s["title"]}</h3><p>{s["text"]}</p>
  {('<div class="need">' + "".join(f'<span><b>{c}×</b>{n}</span>' for n, c in s["need"]) + '</div>') if s["need"] else ""}
  <div class="meta"><span>~{s["minutes"]} perc</span><span>{s["people"]} fő</span>{"".join(f'<span>{TOOLS[t][0]}</span>' for t in s["tools"] if t != "ket_fo")}</div>
  {f'<div class="warn">{s["warn"]}</div>' if s.get("warn") else ""}</div></div>''' for s in STEPS["steps"])
page("szereles.html", "Szerelési útmutató – ZENIT", "A ZENIT szerelése lépésről lépésre: szerszámok, alkatrészek, 12 ábrás lépés, szerelési videó és nyomtatható kézikönyv.",
     page_hero("Concierge · Szerelés", "Három óra. Két ember. <em>Egy csendes szekrény.</em>",
               "Minden alkatrész előfúrva, betűvel jelölve érkezik. Kövesd a 12 lépést – vagy nézd meg a saját tervedre készült szerelési animációt.",
               [("index.html", "ZENIT"), ("", "Concierge"), ("", "Szerelés")], V + "szereles_loop.mp4", tag="Szerelési animáció · a tervezőből") +
     S(f'''<div class="split wide-l"><div class="reveal"><div class="video"><video controls preload="metadata" playsinline poster="assets/video/zenit_szereles_poster.jpg" src="assets/video/zenit_szereles.mp4"></video></div>
  <p class="vid-note">Szerelési videó · a referencia-darab (250 cm, 3 ajtó, kasmír). <a href="tervezo.html#assemble">A saját tervedhez: lejátszás a tervezőben ›</a></p></div>
  <div class="reveal d1"><div class="label">Mielőtt elkezded</div><h3 class="h3" style="margin:18px 0 16px">Három szabály, <em>és minden sikerül.</em></h3>
  <ol style="margin:0;padding-left:18px;color:var(--fg2)"><li>Egy puha takarón dolgozz – a lapok éle és felülete hálás lesz érte.</li><li>A konfirmátot ütközésig húzd, utána csak negyed fordulatot.</li><li>Emelni mindig ketten kell: a korpusz ajtók nélkül kb. 56 kg.</li></ol>
  <div class="acts"><a class="btn fill" href="kezikonyv.html">A te kézikönyved <span class="arrow"></span></a><a class="btn" href="letoltes/ZENIT_kezikonyv_referencia.pdf">PDF letöltése</a></div></div></div>''', "paper") +
     S(head("Szerszámok", "Ami kell. <em>És semmi több.</em>", "A konfirmát kulcsot és a csavarokat a csomagban találod.") + TOOLSET, "dark") +
     soft(F + "foto_077.jpg", "Előfúrva, betűvel jelölve", "Minden furat a helyén van. <em>Neked csak össze kell illesztened.</em>") +
     S(head("Alkatrészek", "Tizenegy elem, <em>betűvel jelölve.</em>", "Minden lap címkéjén ott a betű – az ábrákon is ezekkel hivatkozunk rájuk.") + PARTS +
       '<div style="margin-top:50px">' + HW + '</div>', "stone") +
     S(head("Lépésről lépésre", 'Tizenkét lépés, <em>nyugodt tempóban.</em>', "A lépések együtt kb. két és fél óra, kicsomagolással és takarítással együtt nagyjából három. Az ábrák a valódi gyártási modellből készültek – minden furat ott van, ahol a rajzon látod.") + ST, "paper") +
     nxt("", "garancia.html", "Örökgarancia", "Nem évekre adunk garanciát. Ígéretet adunk.", alt=False))

# ======================================================================== GARANCIA
page("garancia.html", "ZENIT Örökgarancia", "Egy életre tervezve – a ZENIT Örökgarancia.",
     page_hero("Kollekció · 06", "Egy életre <em>tervezve.</em>", "A ZENIT Örökgarancia nem határidő, hanem ígéret.", [("index.html", "ZENIT"), ("", "Kollekció"), ("", "Örökgarancia")],
               R + "b_kasmir_evening.jpg", tag="Látványterv · kasmír, esti fény") +
     S('''<div class="guar reveal"><img class="seal" src="assets/ill/seal.svg" alt="ZENIT pecsét" style="border-radius:50%">
  <div class="label plain">ZENIT Örökgarancia <span class="demo">Demó</span></div>
  <p style="margin-top:26px">Nem évekre adunk garanciát, hanem a szekrényed egész életére. Amíg a lap, a szín és a vasalat kapható, a ZENIT minden eleme pótolható: ha megsérül, elkopik, vagy megváltozik az életed, elemenként pótoljuk, cseréljük vagy bővítjük.</p>
  <p class="big center" style="margin-top:34px;font-size:clamp(26px,2.6vw,38px)">Amíg létezik, pótoljuk. <em>A ZENIT veled marad.</em></p></div>''', "paper") +
     soft(F + "foto_020.jpg", "Költözéskor is", "Ragasztó nélkül, csavarral épül. <em>Szétszeded, viszed, újra összerakod.</em>") +
     S(head("Amit vállalunk", "Négy ígéret, <em>aláírva.</em>", "Minden ZENIT sorszámot kap; a tanúsítványt a kézikönyv utolsó oldalán találod.") + '''<div class="trust reveal" style="margin-top:0"><div><b>Örökgarancia</b><span>Elemenként pótolható, amíg az anyag kapható.</span></div><div><b>Szétszedhető</b><span>Ragasztó nélküli kötések – költözéskor viszed.</span></div><div><b>Sorszámozva</b><span>Minden darab nyilvántartva, aláírva.</span></div><div><b>Szerviz</b><span>Pántbeállítás, csere, bővítés – kérésre helyszínen.</span></div></div>''', "dark") +
     nxt("07", "tervezo.html", "Tervezd meg a sajátod", "Minden változtatás azonnal megjelenik – méret, ajtók, tükör, színek, fény, fogantyú.", alt=False))

# ======================================================================== TERVEZŐ
CFG = f'''<section class="cfg-wrap">
<div class="cfg-shell">
  <div class="viewer" id="viewer">
    <div class="toolbar"><div class="seg" id="envSeg"><button class="on" data-env="room">Szobában</button><button data-env="studio">Stúdió</button></div></div>
    <div class="tools">
      <button class="icon-btn txt" id="btnAsm" title="Szerelési animáció a te tervedhez">▶ Szerelés</button>
      <button class="icon-btn" id="btnOpen" title="Ajtók nyitása / zárása">◫</button>
      <button class="icon-btn" id="btnReset" title="Nézet alaphelyzetbe">⟲</button>
      <button class="icon-btn" id="btnFull" title="Teljes képernyő">⤢</button>
    </div>
    <div class="asm" id="asmBox"><b id="asmT">Szerelés</b><span id="asmD"></span><div class="bar"><i id="asmBar"></i></div></div>
    <canvas id="cfg3d" aria-label="A ZENIT élő 3D modellje"></canvas>
    <div class="dims"><b id="dimW">250</b> cm × <b id="dimH">53</b> cm × <b id="dimD">60</b> cm</div>
    <div class="hint">Forgasd · nagyíts · kattints egy ajtóra</div>
  </div>
  <aside class="panel">
    <div class="scroll">
      <div class="step"><h4>Méret <small>1 / 7</small></h4>
        <div class="val">A meglévő szekrényed: <a href="#" id="baseCol" style="border-bottom:1px solid var(--line)">kasmír</a></div>
        <div class="row"><label>Szélesség <b><span id="wVal">250</span> cm</b></label><input type="range" id="w" min="60" max="280" value="250"></div>
        <div class="row"><label>Belmagasság (legalacsonyabb pont) <b><span id="ceilVal">259</span> cm</b></label><input type="range" id="ceil" min="220" max="320" value="259"></div>
        <div class="row"><label>Meglévő szekrény magassága <b><span id="baseVal">205</span> cm</b></label><input type="range" id="baseH" min="150" max="260" value="205"></div>
        <div class="row"><label>Mélység <b><span id="dVal">60</span> cm</b></label>
          <div class="opts" id="depthOpts"><button class="opt" data-d="35">35</button><button class="opt" data-d="45">45</button><button class="opt on rec" data-d="60">60 · javasolt</button></div>
          <input type="range" id="dRange" min="30" max="70" value="60" aria-label="Egyedi mélység">
          <div class="val" style="margin:8px 0 0">Javasolt: <b>60 cm</b> – a meglévő szekrényed mélysége, így a front egy síkban fut. Egyedi mélység 30–70 cm között.</div></div>
      </div>
      <div class="step"><h4>Illesztés <small>2 / 7</small></h4>
        <div class="val">Ha a plafon nem vízszintes vagy a fal nem egyenes – max. 10 cm.</div>
        <div class="row"><label>Plafon jobb oldalon magasabb <b><span id="slopeVal">0</span> cm</b></label><input type="range" id="slope" min="0" max="10" value="0" step="0.5"></div>
        <div class="row"><label>Falkiegyenlítés (távtartó) <b><span id="wallVal">0</span> cm</b></label><input type="range" id="wall" min="0" max="10" value="0" step="0.5"></div>
      </div>
      <div class="step"><h4>Ajtók <small>3 / 7</small></h4>
        <div class="val">Javasolt: <span id="doorRec">5</span> ajtó · ajtónként max. 90 cm, ideálisan 60 cm alatt</div>
        <div class="opts" id="doorOpts"></div>
        <div class="opts" id="splitOpts"><button class="opt on" data-s="eq">Egyenlő osztás</button><button class="opt" data-s="sym">Középen szélesebb</button></div>
        <div class="doorgrid" id="doorGrid" style="margin-top:14px"></div>
      </div>
      <div class="step"><h4>Szín és textúra <small>4 / 7</small></h4>
        <div class="tabs" id="partTabs"><button class="on" data-part="ajto">Ajtók</button><button data-part="korpusz">Korpusz</button><button data-part="belso">Belső</button></div>
        <div class="sw-group">Uni színek</div><div class="sw" id="swUni"></div>
        <div class="sw-group">ZENIT Natúr</div><div class="sw" id="swWood"></div>
        <div class="sw-group">Kő és len</div><div class="sw" id="swStone"></div>
        <div class="hex"><i id="hexPrev" style="background:#CDBFAE"></i><input id="hexIn" value="#CDBFAE" maxlength="7" aria-label="Egyedi HEX színkód"></div>
        <div class="opts" id="finOpts" style="margin-top:14px"><button class="opt on" data-f="matt">Matt</button><button class="opt" data-f="satin">Selyemfény</button><button class="opt" data-f="gloss">Magasfény</button></div>
      </div>
      <div class="step"><h4>Fogantyú <small>5 / 7</small></h4>
        <div class="cards2" id="handles">
          <button class="card2 on" data-h="edge"><div class="pic"><svg width="70" height="20"><path d="M2 4h66v6a6 6 0 0 1-6 6H8a6 6 0 0 1-6-6z" fill="none" stroke="currentColor"/></svg></div><b>GTV HEXA élfogantyú</b><span>lekerekített, 192 mm</span></button>
          <button class="card2" data-h="bar"><div class="pic"><svg width="70" height="20"><path d="M6 10h58" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg></div><b>Rúd</b><span>vízszintes, alul · 320 mm</span></button>
          <button class="card2" data-h="knob"><div class="pic"><svg width="70" height="20"><circle cx="35" cy="10" r="7" fill="none" stroke="currentColor"/></svg></div><b>Gomb / bőrfül</b><span>diszkrét részlet</span></button>
          <button class="card2" data-h="push"><div class="pic"><svg width="70" height="20"><path d="M10 10h50" stroke="currentColor" stroke-dasharray="3 3"/></svg></div><b>Nyomásra nyíló</b><span>fogantyú nélkül</span></button>
        </div>
        <div class="opts" id="hcol" style="margin-top:10px"><button class="opt on" data-c="#C9C6C0">Alu elox</button><button class="opt" data-c="#222">Matt fekete</button><button class="opt" data-c="#B08D57">Bronz</button><button class="opt" data-c="#7A4E2D">Bőr</button></div>
      </div>
      <div class="step"><h4>Belső <small>6 / 7</small></h4><div class="val">Polc rekeszenként</div><div class="opts" id="shelfOpts"></div></div>
      <div class="step" style="border:0"><h4>Extrák <small>7 / 7</small></h4>
        <div class="toggle"><span>Belső LED-világítás<small>ajtónyitásra, melegfehér 2700 K</small></span><button class="sw-t on" id="xLed"></button></div>
        <div class="toggle"><span>Plafonzáró takaróléc<small>beépített hatás – ferde plafonnál automatikus</small></span><button class="sw-t" id="xTrim"></button></div>
        <div class="toggle"><span>Tárolódobozok<small>lenvászon, rekeszre méretezve</small></span><button class="sw-t" id="xBox"></button></div>
        <div class="toggle"><span>Fékes Häfele pántok<small>alapfelszereltség</small></span><button class="sw-t on" disabled></button></div>
      </div>
    </div>
    <div class="summary">
      <div class="price"><b id="price">229 900 Ft</b><span>Becsült ár</span></div>
      <div class="meta">Elkészül 3–4 hét alatt · szállítás és szerelés országosan · ZENIT Örökgarancia</div>
      <div class="acts"><a class="btn fill full" href="terv.html" data-save>Ajánlatot kérek <span class="arrow"></span></a>
        <a class="btn" href="concierge.html" data-save>Tervező hív vissza</a><a class="btn" href="terv.html#rendeles" data-save>Megrendelem <span class="demo" style="margin-left:4px">Demó</span></a></div>
      <div class="ftiles">
        <a href="#" id="lnkAsm"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9.5"/><path d="M10 8.5l5.5 3.5-5.5 3.5z" fill="currentColor"/></svg><b>Szerelés lejátszása</b><span>3D animáció a te tervedből</span></a>
        <a href="#" id="lnkRec"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6" width="13" height="12" rx="1.5"/><path d="M16 10l5-3v10l-5-3"/><path d="M9.5 9v6M7 12.5l2.5 2.5 2.5-2.5"/></svg><b>Szerelési videó</b><span>letöltés, feliratokkal</span></a>
        <a href="kezikonyv.html" data-save><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/><path d="M8 7h8M8 10.5h6"/></svg><b>Kézikönyv</b><span>személyre szabott, PDF</span></a>
        <a href="terv.html" data-save><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12v18l-6-4.5L6 21z"/><path d="M9.5 9l2 2 3.5-3.5"/></svg><b>Terv mentése</b><span>ajánlathoz, később is</span></a>
      </div>
    </div>
  </aside>
</div></section>'''
page("tervezo.html", "Tervező – ZENIT", "Tervezd meg a saját ZENIT felső szekrényed élő 3D-ben: méret, illesztés, ajtók és nyitásirány, tükör, színek, fény, fogantyú.",
     CFG, scripts=["vendor/three.min.js", "vendor/OrbitControls.js", "vendor/RoomEnvironment.js", "configurator.js"], body_cls="cfg-page")

# ======================================================================== AZ ÖN TERVE
page("terv.html", "Az Ön terve – ZENIT", "A mentett ZENIT terv összesítője, kézikönyv, szerelési animáció, ajánlatkérés és rendelés.",
     page_hero("Concierge", "Az Ön <em>terve.</em>", "Nézze át, mentse el, töltse le a kézikönyvét – kérjen ajánlatot, vagy rendelje meg.", [("index.html", "ZENIT"), ("", "Concierge"), ("", "Az Ön terve")], F + "foto_109_hero.jpg", tag="Hangulat") +
     S(f'''<div class="plan-sum">
  <div class="reveal"><div class="frame ar-1610" style="aspect-ratio:16/10"><img id="planImg" src="{R}after_day.jpg" alt="A terv látványa"><span class="tag">Látványterv</span></div>
    <table id="planTable" style="margin-top:26px"><tbody><tr><td>Még nincs mentett terv</td><td><a class="more" href="tervezo.html">Tervezőbe <span class="arrow"></span></a></td></tr></tbody></table>
    <div class="acts"><a class="btn" href="tervezo.html">Módosítás</a><a class="btn" href="kezikonyv.html">Kézikönyv a tervhez</a><a class="btn" href="tervezo.html#assemble">Szerelési animáció</a></div>
  </div>
  <div class="choice reveal d1" id="rendeles">
    <div class="hi"><div class="label">Ajánlat</div><b>Ajánlatot kérek</b><p>Pontos ár szállítással és szereléssel, 24 órán belül e-mailben.</p>
      <form class="form" onsubmit="return false"><div><label>Név</label><input></div><div><label>Telefon</label><input></div><div class="full"><label>E-mail</label><input type="email"></div>
      <div class="full"><label>Település</label><input></div><div class="full"><a class="btn fill" href="#">Ajánlatot kérek <span class="arrow"></span></a></div></form></div>
    <div><div class="label">Concierge</div><b>Egy tervező hív vissza</b><p>Belsőépítészünk átbeszéli a tervet, segít a színekben, arányokban.</p><a class="btn" href="concierge.html">Időpontot választok</a></div>
    <div><div class="label">Rendelés <span class="demo">Demó</span></div><b>Megrendelem most</b><p>Biztonságos online fizetés. A projektben bemutató lépés – valódi fizetés nem történik.</p><a class="btn" href="#">Tovább a fizetéshez</a></div>
  </div></div>''', "paper"), scripts=["zplan.js", "plan.js"])

# ======================================================================== KÉZIKÖNYV (személyre szabott, nyomtatható)
steps_js = json.dumps([dict(no=s["no"], title=s["title"], text=s["text"], svg=s["svg"], need=s["need"], minutes=s["minutes"], people=s["people"], warn=s.get("warn")) for s in STEPS["steps"]], ensure_ascii=False)
page("kezikonyv.html", "Kézikönyv – ZENIT", "Személyre szabott, nyomtatható ZENIT használati és szerelési kézikönyv a mentett tervhez.",
     f'''<section class="page-hero img noprint"><div class="media"><picture><source media="(max-width:760px)" srcset="{R}kezikonyv_hero_m.jpg"><img src="{R}kezikonyv_hero.jpg" alt="A ZENIT kézikönyv nyomtatott oldalai"></picture></div><div class="wrap">{crumb(("index.html", "ZENIT"), ("", "Concierge"), ("", "Kézikönyv"))}
  <div class="label" style="color:var(--bronze2)">Az Ön kézikönyve</div><h1 class="h1 lines"><span class="ln"><span>Az Ön ZENIT-je, <em>papíron is.</em></span></span></h1>
  <p class="lead">A mentett tervéből készül: méretek, ajtók és nyitásirányok, tükör, fény, alkatrészek, szerelés és ápolás. Nyomtassa ki, vagy mentse PDF-be.</p>
  <div class="acts"><button class="btn fill" onclick="print()">Nyomtatás / PDF <span class="arrow"></span></button><a class="btn light" href="tervezo.html">Terv módosítása</a><a class="btn light" href="letoltes/ZENIT_kezikonyv_referencia.pdf">Referencia PDF</a></div></div><span class="tag" style="left:auto;right:var(--pad);bottom:24px">Brandelt kézikönyv · A4</span></section>
<section class="sec" data-theme="stone"><div class="wrap" id="manual"></div></section>
<script>window.ZSTEPS={steps_js};</script>''', scripts=["zplan.js", "manual.js"])

# ======================================================================== CONCIERGE
page("concierge.html", "Concierge – személyes konzultáció – ZENIT", "Tervező vagy lakberendező hív vissza a ZENIT tervedről, helyszíni felméréssel.",
     page_hero("Concierge", "Beszéljünk <em>a tervedről.</em>", "Belsőépítészünk visszahív, átbeszéli a méreteket, színeket és arányokat – és ha kéred, személyesen is felmér.",
               [("index.html", "ZENIT"), ("", "Concierge"), ("", "Személyes konzultáció")], F + "foto_112.jpg", tag="Hangulat") +
     S(f'''<div class="split" style="align-items:start">
  <div class="reveal"><div class="label">Hogyan működik</div><h2 class="h2">Húsz perc, <em>és minden a helyére kerül.</em></h2>
    <div class="prose"><p>Válassz időpontot, és tervezőnk a megadott számon hív. Ha már van mentett terved, azt is átnézzük – ha nincs, a beszélgetés végére lesz.</p>
    <p>Budapesten és környékén díjmentes helyszíni felmérést is kérhetsz: lézeres méréssel a ferde plafont és a falat is pontosan felvesszük.</p></div>
    <dl class="specs" style="grid-template-columns:1fr 1fr;margin-top:40px"><div><dt>Telefon</dt><dd>+36 1 000 0000</dd></div><div><dt>E-mail</dt><dd>hello@zenit.example</dd></div><div><dt>Atelier</dt><dd>Budapest</dd></div><div><dt>Nyitva</dt><dd>H–P 10–18</dd></div></dl>
    <div style="margin-top:40px">{vid("tervezes", "ar-169", "Hangulat")}</div></div>
  <form class="form reveal d1" style="border:1px solid var(--ln);padding:34px;background:var(--paper)" onsubmit="return false">
    <div class="full"><div class="label">Visszahívás kérése</div></div>
    <div><label>Név</label><input></div><div><label>Telefon</label><input></div><div class="full"><label>E-mail</label><input type="email"></div>
    <div class="full"><label>Kivel beszélnél?</label><div class="slots"><button type="button" class="on">Tervező</button><button type="button">Lakberendező</button><button type="button">Mindegy</button></div></div>
    <div class="full"><label>Nap</label><div class="slots"><button type="button" class="on">Holnap</button><button type="button">Csütörtök</button><button type="button">Péntek</button><button type="button">Jövő hét</button></div></div>
    <div class="full"><label>Időpont</label><div class="slots"><button type="button">9:00</button><button type="button" class="on">11:00</button><button type="button">14:00</button><button type="button">16:30</button></div></div>
    <div class="full"><label>Megjegyzés</label><textarea rows="3" placeholder="Pl. belmagasság, ferde plafon, stílus…"></textarea></div>
    <div class="full"><a class="btn fill" href="#">Kérem a visszahívást <span class="arrow"></span></a></div>
  </form></div>''', "paper") +
     nxt("", "tervezo.html", "Vagy tervezd meg most", "Az élő 3D tervezőben pár perc alatt összeállíthatod a sajátodat.", alt=False))

# ======================================================================== A PROJEKTRŐL
PNUMS = [("4", "nap", "a kihívás hossza – keddtől péntekig"), ("10", "", "tervváltozat (v1–v10) a végleges modellig"), ("108", "", "furat a Fusion-modellben, 47 furat-feature"),
         ("101", "", "vasalatelem 3D-ben modellezve"), ("16", "oldal", "gyártási dokumentáció, automatikusan generálva"), ("40", "", "saját Blender-látványterv"),
         ("3", "", "videó: projekt, promó, szerelés"), ("17", "", "weboldal, élő 3D tervezővel")]
page("projekt.html", "A projektről – ZENIT AI-kihívás", "A ZENIT AI-kihívás projekt: videók, 3D modell, számok, napló, forrásfájlok.",
     page_hero("A projektről", "Négy nap, egy ötlet, <em>egy mesterséges intelligencia.</em>",
               "A ZENIT egy AI-kihívásra készült: a 3D modellt, a gyártási dokumentációt, a látványterveket, a videókat és ezt az oldalt Claude-dal együtt terveztük – mindent dokumentálva.",
               [("index.html", "ZENIT"), ("", "A projektről")], V + "projekt_loop.mp4", tag="Modell · render · élő 3D") +
     S('<div class="video reveal"><video controls preload="metadata" playsinline poster="assets/video/zenit_projekt_poster.jpg" src="assets/video/zenit_projekt.mp4"></video></div>'
       '<p class="vid-note">Projektvideó · magyar narráció (helyben generált gépi beszéd, Piper TTS). <a href="assets/video/zenit_promo.mp4">Promóvideó ›</a> &nbsp; <a href="assets/video/zenit_szereles.mp4">Szerelési videó ›</a></p>', "paper", style="padding-top:40px") +
     S(head("A projekt számokban", "Négy nap, <em>tizedmilliméterre.</em>") + nums(PNUMS), "dark") +
     S(head("3D modell", "Forgasd meg <em>a gyártási modellt.</em>", "A paraméteres geometriából készült GLB: ugyanaz, mint a Fusion-modell és a gyártási dokumentáció (v10).") +
       '''<div class="m3d reveal"><canvas id="model3d" data-src="assets/model/zenit_v10.glb" aria-label="A ZENIT rátétszekrény gyártási 3D modellje"></canvas>
  <div class="m3d-load">3D modell betöltése…</div>
  <div class="m3d-bar"><button class="opt" id="mExplode">Robbantott nézet</button><button class="opt on" id="mBase">Alatta a meglévő szekrény</button><button class="opt on" id="mDoors">Ajtók</button><button class="opt" id="mHw">Vasalatok</button><button class="opt" id="mReset">⟲</button></div>
  <div class="m3d-hint">Forgasd egérrel / ujjal · görgess a nagyításhoz</div></div>''', "ivory") +
     S(head("Letöltések és napló", "Minden, <em>ami mögötte van.</em>") + '''<div class="proj-grid reveal">
  <a href="naplo.html"><div class="label plain">Napló</div><b>Projektnapló</b><span>Eszközök, promptok, elakadások és megoldások.</span></a>
  <a href="https://github.com/mbolgar11/zenit"><div class="label plain">GitHub</div><b>Forráskód</b><span>Weboldal, paraméteres geometria, generátorok.</span></a>
  <a href="letoltes.html"><div class="label plain">3D</div><b>Fusion F3D · STEP · GLB</b><span>A teljes gyártási modell, három formátumban.</span></a>
  <a href="letoltes/Ratet_v10_gyartasi_dokumentacio.pdf"><div class="label plain">PDF</div><b>Gyártási dokumentáció</b><span>16 oldal: szabásjegyzék, rajzok, fúrósablon.</span></a>
  <a href="letoltes/ZENIT_kezikonyv_referencia.pdf"><div class="label plain">PDF</div><b>Használati és szerelési kézikönyv</b><span>Brandelt, ábrás – a referencia-darabhoz.</span></a>
  <a href="szereles.html"><div class="label plain">Szerelés</div><b>Útmutató és videó</b><span>12 ábrás lépés a gyártási modellből.</span></a>
</div>''', "paper"),
     scripts=["vendor/three.min.js", "vendor/OrbitControls.js", "vendor/GLTFLoader.js", "vendor/RoomEnvironment.js", "model3d.js"])

# ======================================================================== LETÖLTÉSEK
DL = [("3D modell", [("Ratet_v10_Fusion.f3d", "Autodesk Fusion archívum (F3D) – a teljes, furatolt gyártási modell"),
                     ("Ratet_v10_Fusion_export.step", "STEP – a Fusion-modell exportja"),
                     ("Ratet_v10_CadQuery_teljes.step", "STEP – a paraméteres geometriából, vasalatokkal és az ELIA szekrénnyel"),
                     ("Ratet_v10_CadQuery_teljes.glb", "GLB – webes 3D (ezt mutatja a nézegető)")]),
      ("Gyártás és használat", [("Ratet_v10_gyartasi_dokumentacio.pdf", "Gyártási dokumentáció, 16 oldal"),
                   ("ZENIT_kezikonyv_referencia.pdf", "Használati és szerelési kézikönyv – brandelt, ábrás"),
                   ("Ratet_v10_szabasjegyzek_furattabla.xlsx", "Szabásjegyzék és furattábla (Excel)"),
                   ("Ratet_v10_kalkulacio.xlsx", "Anyag- és árkalkuláció (Excel)")]),
      ("Videó", [("../assets/video/zenit_projekt.mp4", "Projektvideó, narrációval (MP4)"), ("../assets/video/zenit_promo.mp4", "Promóvideó (MP4)"),
                 ("../assets/video/zenit_szereles.mp4", "Szerelési videó (MP4)")])]
rows = ''.join(f'<div class="dl-group reveal"><div class="label">{g}</div>' + ''.join(
    f'<a class="dl" href="letoltes/{f}" download><b>{f.split("/")[-1]}</b><span>{d}</span></a>' for f, d in items) + '</div>' for g, items in DL)
page("letoltes.html", "Letöltések – ZENIT AI-kihívás", "A ZENIT 3D modelljei, gyártási dokumentációja, kézikönyve és videói.",
     page_hero("Letöltések", "Minden fájl, <em>ami mögötte van.</em>", "Fusion- és STEP-modell, gyártási PDF, kézikönyv, szabásjegyzék, kalkuláció és a videók. A forráskód a GitHubon.",
               [("index.html", "ZENIT"), ("projekt.html", "A projektről"), ("", "Letöltések")], V + "furas.mp4", tag="Hangulat") +
     S(rows + '<p class="vid-note" style="margin-top:30px"><a href="naplo.html">Projektnapló ›</a> &nbsp; <a href="https://github.com/mbolgar11/zenit">GitHub-repó ›</a></p>', "paper"))

# ======================================================================== NAPLÓ
import markdown as _md, pathlib as _pl
_np = _pl.Path(ROOT) / "src" / "naplo.md"
if _np.exists():
    _src = _np.read_text(encoding='utf8').split('\n', 1)[1]
    _html = _md.markdown(_src, extensions=['extra', 'sane_lists'])
    page("naplo.html", "Projektnapló – ZENIT AI-kihívás", "Eszközök, promptok, elakadások és megoldások – a ZENIT AI-kihívás naplója.",
         page_hero("Projektnapló", "Hogyan készült – <em>lépésről lépésre.</em>", "Eszközök, példapromptok, elakadások és megoldások, ahogy a munka közben történt.",
                   [("index.html", "ZENIT"), ("projekt.html", "A projektről"), ("", "Napló")], F + "foto_117_hero.jpg", tag="Hangulat") +
         S(f'<article class="naplo">{_html}</article>', "paper"))
