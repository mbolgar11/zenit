import numpy as np, cv2
from PIL import Image, ImageFilter, ImageEnhance
from grade import grade
W,H=1600,2000
bg=Image.open('/home/claude/zenit2/assets/m/foto/foto_046.jpg').convert('RGB')
s=H/bg.height*1.12; bg=bg.resize((int(bg.width*s),int(bg.height*s)),Image.LANCZOS)
ox=int((bg.width-W)*0.75); oy=int((bg.height-H)*0.35)
bg=bg.crop((ox,oy,ox+W,oy+H)).filter(ImageFilter.GaussianBlur(2.2)); bg=ImageEnhance.Brightness(bg).enhance(1.1); bg=ImageEnhance.Color(bg).enhance(0.9)
B=np.asarray(bg).astype(np.float32)/255
cut=Image.open('cut.png'); cut=cut.crop(cut.getbbox()); sc=0.84
cut=cut.resize((int(cut.width*sc*0.96),int(cut.height*sc)),Image.LANCZOS)
C=np.asarray(cut).astype(np.float32)/255; rgb=C[...,:3]; A=C[...,3]
A=cv2.erode(A,np.ones((3,3),np.uint8),iterations=2); A=cv2.GaussianBlur(A,(0,0),1.6)
px=int(W*0.585-(1050-325)*sc*0.96); py=H-cut.height+10
# a figura beillesztése egy vászon méretű rétegre
F=np.zeros((H,W,3),np.float32); M=np.zeros((H,W),np.float32)
x0,y0=max(px,0),max(py,0); x1,y1=min(px+cut.width,W),min(py+cut.height,H)
F[y0:y1,x0:x1]=rgb[y0-py:y1-py,x0-px:x1-px]; M[y0:y1,x0:x1]=A[y0-py:y1-py,x0-px:x1-px]
# 1) tónusillesztés: fekete pont, expozíció és színhőmérséklet a háttérhez
lum=lambda X: X[...,0]*.3+X[...,1]*.59+X[...,2]*.11
mask=M>0.9; bl=np.percentile(lum(B),2); fl=np.percentile(lum(F)[mask],2)
F=np.clip((F-fl)*1.0+bl,0,1)
bgm=B[int(H*.25):int(H*.75)].reshape(-1,3).mean(0); F=F*(0.85+0.15*bgm/bgm.mean())       # a környezet színe
# 2) fény: az ablak (jobb fent) felől meleg főfény, bal oldalon lágy árnyék
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); xs=(xx-px)/cut.width; ys=(yy-py)/cut.height
key=np.clip(0.80+0.34*xs-0.10*ys,0.72,1.12)[...,None]
F=F*key*np.array([1.05,1.0,0.90])*(1-(1-key)*np.array([0.0,0.05,0.12]))
# 3) fényátölelés (light wrap): a háttér fénye befolyik a peremekre
inner=cv2.GaussianBlur(M,(0,0),9); band=np.clip(M-inner*0.85,0,1)*(M>0.02)
Bb=cv2.GaussianBlur(B,(0,0),18); F=1-(1-F)*(1-Bb*band[...,None]*0.55)
# 4) peremfény a hajon és a vállon az ablak felől
edge=np.clip(M-cv2.GaussianBlur(M,(0,0),6),0,1)*np.clip((xs-0.35)/0.65,0,1)*np.clip(1-ys*1.3,0,1)
F=np.clip(F+edge[...,None]*np.array([1.0,0.88,0.66])*0.55,0,1)
# 5) kontaktárnyék a háttéren
sh=cv2.GaussianBlur(np.roll(np.roll(M,30,0),-45,1),(0,0),40)*0.30
B2=B*(1-sh[...,None]*np.array([1,1.05,1.12]))
out=B2*(1-M[...,None])+F*M[...,None]
img=Image.fromarray((np.clip(out,0,1)*255).astype(np.uint8))
img=grade(img,sat=0.86,gamma=1.02,warm=(1.03,1.0,0.95),vig=0.2,grain=3.0,seed=4)
img.save('alapito_v5.jpg',quality=87,optimize=True,progressive=True); img.resize((480,600)).save('v5.jpg')
img.crop((650,400,1550,1100)).resize((540,420)).save('v5_head.jpg')
