import numpy as np
from PIL import Image, ImageDraw, ImageFilter
rng=np.random.default_rng(7)
base=Image.open('before_clean_full.jpg').convert('RGB'); A=np.asarray(base).astype(np.float32); H,W,_=A.shape
TL,TR,BL,BR=(672,156),(3002,185),(672,623),(3002,650)
def lerp(p,q,t): return (p[0]+(q[0]-p[0])*t, p[1]+(q[1]-p[1])*t)
# kasmír szín az alsó szekrény ajtóiról, oszloponként
cols=np.zeros((W,3),np.float32)
L=A[760:1000,760:1560].mean(axis=0); R=A[760:1000,2440:2960].mean(axis=0)
lm=L.mean(axis=0); rm=R.mean(axis=0)
for x in range(W):
    t=np.clip((x-1160)/(2700-1160),0,1); cols[x]=lm*(1-t)+rm*t
# finom oszloponkénti árnyalat a bal ajtóról (természetes egyenetlenség)
face=np.zeros_like(A)
yy=np.arange(H)[:,None]; xx=np.arange(W)[None,:]
ytop=TL[1]+(xx-TL[0])*(TR[1]-TL[1])/(TR[0]-TL[0]); ybot=BL[1]+(xx-BL[0])*(BR[1]-BL[1])/(BR[0]-BL[0])
v=np.clip((yy-ytop)/(ybot-ytop),0,1)
shade=0.90+0.10*v**0.8                       # felül kicsit sötétebb (plafon árnyéka)
face=cols[None,:,:]*shade[...,None]*0.985*np.array([1.025,1.0,0.955],np.float32)
# ajtóosztások (harmadok) – sötét rés + világos él
mask=Image.new('L',(W,H),0); d=ImageDraw.Draw(mask); d.polygon([TL,TR,BR,BL],fill=255)
lines=Image.new('L',(W,H),0); dl=ImageDraw.Draw(lines); hl=Image.new('L',(W,H),0); dh=ImageDraw.Draw(hl)
for k in (1/3,2/3):
    p=lerp(TL,TR,k); q=lerp(BL,BR,k)
    dl.line([p,q],fill=255,width=5); dh.line([(p[0]+5,p[1]),(q[0]+5,q[1])],fill=255,width=2)
dl.line([TL,TR],fill=255,width=7)            # rés a plafonig (10 mm)
dl.line([(BL[0],BL[1]-2),(BR[0],BR[1]-2)],fill=200,width=4)   # illesztés az alsó szekrényre
# élfogantyúk (GTV HEXA 192) az ajtók alsó élén
hd=Image.new('L',(W,H),0); dd=ImageDraw.Draw(hd)
for i in range(3):
    c=lerp(lerp(BL,BR,(i+.5)/3),lerp(TL,TR,(i+.5)/3),0.0)
    dd.rounded_rectangle([c[0]-88,c[1]-17,c[0]+88,c[1]-7],radius=5,fill=255)
lines=np.asarray(lines.filter(ImageFilter.GaussianBlur(1.1)))[...,None]/255
hl=np.asarray(hl.filter(ImageFilter.GaussianBlur(1)))[...,None]/255
hd=np.asarray(hd.filter(ImageFilter.GaussianBlur(.8)))[...,None]/255
face=face*(1-0.55*lines)+np.array([238,234,228])*hl*0.25+face*0*hl
alu=np.array([172,170,166],np.float32)
face=face*(1-hd)+alu*hd*(0.92+0.08*v[...,None])
face+=rng.normal(0,2.4,(H,W,1))
m=np.asarray(mask.filter(ImageFilter.GaussianBlur(1.2)))[...,None]/255
out=A*(1-m)+face*m
# enyhe kontaktárnyék a plafonon a ZENIT fölött
sh=Image.new('L',(W,H),0); ds=ImageDraw.Draw(sh); ds.polygon([(TL[0],TL[1]-22),(TR[0],TR[1]-22),TR,TL],fill=70)
sh=np.asarray(sh.filter(ImageFilter.GaussianBlur(14)))[...,None]/255
out=out*(1-0.35*sh*(1-m))
img=Image.fromarray(np.clip(out,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.35))
img.save('after_full.jpg',quality=95)
img.resize((1088,489)).save('v_after.jpg')
