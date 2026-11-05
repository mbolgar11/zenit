import numpy as np, cv2
from PIL import Image, ImageOps
from scipy.ndimage import gaussian_filter1d
rng=np.random.default_rng(3)
orig=np.asarray(ImageOps.exif_transpose(Image.open('IMG_20261105_084110076.jpg')).convert('RGB')).astype(np.float32)
im=orig.copy(); H,W,_=im.shape
x0,x1,ys=1628,2416,900
band=orig[760:900,x0:x1]
col=np.median(band,axis=0)                        # oszloponkénti szín
col=gaussian_filter1d(col,6,axis=0)               # csíkmentesítés (a sarokvonal megmarad)
fill=np.empty((H-ys,x1-x0,3),np.float32)
for i,y in enumerate(range(ys,H)):
    k=i/(H-ys)
    fill[i]=col*(1-0.13*k)
# lágy, átlós tükörfény
yy,xx=np.mgrid[0:H-ys,0:x1-x0]
sheen=np.exp(-((xx*0.55+yy-260)/180.0)**2)*7
fill+=sheen[...,None]
fill+=rng.normal(0,1.6,fill.shape[:2])[...,None]
# átúsztatás 50 sorban
L=50
for i in range(H-ys):
    a=min(1,i/L)
    im[ys+i,x0:x1]=orig[ys+i,x0:x1]*(1-a)+fill[i]*a
img8=np.clip(im,0,255).astype(np.uint8)
mask=np.zeros((H,W),np.uint8)
mask[915:1030,1612:1690]=255          # kéz-maradék a tükör bal szélén
mask[1385:1452,2950:3264]=255         # dátum
img8=cv2.inpaint(img8,mask,9,cv2.INPAINT_TELEA)
# klónozás felülről: tükörkeret-szél (kéz) és a bal oldali apró tárgy
def clone(x0,x1,y0,y1,dy):
    best=None
    for dx in range(-14,15):
        a=img8[y0-1,x0+20:x1-20].astype(np.float32); b=img8[y0-dy-1,x0+20+dx:x1-20+dx].astype(np.float32)
        a2=img8[y1,x0+20:x1-20].astype(np.float32); b2=img8[y1-dy,x0+20+dx:x1-20+dx].astype(np.float32)
        e=np.abs(a-b).mean()+np.abs(a2-b2).mean()
        if best is None or e<best[0]: best=(e,dx)
    dx=best[1]
    src=img8[y0-dy:y1-dy,x0+dx:x1+dx].astype(np.float32); dst=img8[y0:y1,x0:x1].astype(np.float32)
    h=y1-y0; w=np.ones((h,1,1),np.float32)
    f=12
    for i in range(f): w[i]=w[-1-i]=(i+1)/(f+1)
    img8[y0:y1,x0:x1]=np.clip(dst*(1-w)+src*w,0,255).astype(np.uint8)
clone(1606,1700,905,1040,140)
clone(700,800,900,1045,150)
Image.fromarray(img8).save('before_clean_full.jpg',quality=95)
