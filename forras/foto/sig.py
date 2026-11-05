from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
f=TTFont('MrsSaintDelafield-Regular.ttf'); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
def path(text,x0=0,y0=0,size=1.0,track=0):
    out=[]; x=x0
    for ch in text:
        g=cmap.get(ord(ch)); 
        if g is None: continue
        pen=SVGPathPen(gs); tp=TransformPen(pen,(size,0,0,-size,x,y0)); gs[g].draw(tp); out.append(pen.getCommands()); x+=gs[g].width*size+track
    return ' '.join(out), x
d,xe=path('Zenthe Milán',40,330,0.30)
# lendületes aláhúzás
flour=f'M 60 360 C 240 330, 520 400, {xe+40:.0f} 340'
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {xe+90:.0f} 420" fill="none"><path d="{d}" fill="#2B241D"/><path d="{flour}" stroke="#2B241D" stroke-width="5" stroke-linecap="round"/></svg>'''
open('/home/claude/zenit2/assets/ill/alairas.svg','w').write(svg); print(xe)
