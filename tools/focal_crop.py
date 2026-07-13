#!/usr/bin/env python3
"""focal_crop.py - face/subject-aware crop to a fixed card ratio, head fully kept.
Never blindly center-crops. Detects the largest face, then expands the crop box to
include full head + shoulders, clamps to image, and outputs exact card dimensions.

crop_card(src, dst, W=1200, H=675) -> dict(status, face, box)
"""
import os, sys, cv2, numpy as np
from PIL import Image

CASC = cv2.data.haarcascades
FACE = cv2.CascadeClassifier(os.path.join(CASC,'haarcascade_frontalface_default.xml'))
PROF = cv2.CascadeClassifier(os.path.join(CASC,'haarcascade_profileface.xml'))

def _faces(gray):
    out=[]
    for cc in (FACE,PROF):
        for (x,y,w,h) in cc.detectMultiScale(gray,1.1,5,minSize=(40,40)):
            out.append((x,y,w,h))
    # profile on mirror to catch right-facing
    flip=cv2.flip(gray,1); W=gray.shape[1]
    for (x,y,w,h) in PROF.detectMultiScale(flip,1.1,5,minSize=(40,40)):
        out.append((W-x-w,y,w,h))
    return out

def crop_card(src, dst, W=1200, H=675):
    im = Image.open(src).convert('RGB')
    iw,ih = im.size
    arr = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
    faces=_faces(gray)
    target = W/float(H)
    if faces:
        fx,fy,fw,fh = max(faces, key=lambda f:f[2]*f[3])
        cx = fx+fw/2.0
        # focal y: keep top of head -> anchor slightly above face center
        cy = fy+fh*0.45
        face=(int(fx),int(fy),int(fw),int(fh))
    else:
        cx, cy = iw/2.0, ih*0.42  # top-weighted default for standing athletes
        face=None
    # crop dims at source scale, largest box of target ratio that fits
    if iw/float(ih) > target:
        ch = ih; cw = ch*target
    else:
        cw = iw; ch = cw/target
    # if we have a face, ensure the whole head+shoulders fit vertically: min height ~ face*4.2
    if face:
        need_h = min(ih, fh*4.6)
        if ch < need_h:
            ch = need_h; cw = ch*target
            if cw> iw: cw=iw; ch=cw/target
    left = cx - cw/2.0
    # vertical: put face comfortably in upper third; top margin above head = ~0.9*fh
    if face:
        top = fy - fh*0.9
    else:
        top = cy - ch*0.42
    left = max(0, min(left, iw-cw))
    top  = max(0, min(top,  ih-ch))
    box=(int(left),int(top),int(left+cw),int(top+ch))
    card = im.crop(box).resize((W,H), Image.LANCZOS)
    card.save(dst, 'JPEG', quality=90)
    return dict(status='ok', face=face, box=box, src_size=(iw,ih))

if __name__=='__main__':
    r=crop_card(sys.argv[1], sys.argv[2])
    print(r)
