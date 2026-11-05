import numpy as np
from PIL import Image, ImageEnhance
def grade(im, sat=0.82, gamma=1.08, warm=(1.035,1.0,0.94), vig=0.14, grain=2.0, seed=1):
    a=np.asarray(im.convert('RGB')).astype(np.float32)/255
    a=a*np.array(warm); a=np.clip(a,0,1)**gamma
    a=0.025+a*0.965                                   # enyhén emelt feketék (filmes)
    h,w=a.shape[:2]; y,x=np.ogrid[:h,:w]; r=np.sqrt(((x-w/2)/(w/2))**2+((y-h/2)/(h/2))**2)
    a=a*(1-vig*np.clip((r-0.5)/0.9,0,1)**1.5)[...,None]
    a+=np.random.default_rng(seed).normal(0,grain/255,(h,w,1))
    out=Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8))
    return ImageEnhance.Color(out).enhance(sat)
if __name__=="__main__":
    for src,dst in [('before_clean_full.jpg','before_real.jpg'),('after_full.jpg','after_real.jpg')]:
        im=Image.open(src).crop((660,0,3009,1468)).resize((1920,1200),Image.LANCZOS)
        grade(im).save('/home/claude/zenit2/assets/img/own/'+dst,quality=86,optimize=True,progressive=True)
