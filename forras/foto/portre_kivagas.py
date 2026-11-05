import numpy as np, cv2
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from rembg import remove, new_session
im=ImageOps.exif_transpose(Image.open('IMG_20261105_071929490.jpg')).convert('RGB')   # 1740x2320
a=np.asarray(im).copy(); h,w,_=a.shape
m=np.zeros((h,w),np.uint8); m[h-110:h-20,w-560:w-10]=255   # dátum
a=cv2.inpaint(a,m,7,cv2.INPAINT_TELEA); im=Image.fromarray(a)
cut=remove(im,session=new_session('u2net_human_seg'),alpha_matting=True,alpha_matting_foreground_threshold=235,alpha_matting_background_threshold=20,alpha_matting_erode_size=8)
cut.save('me_cut.png'); print(cut.size)
