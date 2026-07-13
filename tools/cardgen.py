#!/usr/bin/env python3
"""cardgen.py - premium editorial card graphic (1200x675) for an article.
Correct team palette + subject name + angle. Unique, safe (no logos/likeness),
perfectly composed. Used when no verified correct-team photo exists.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

F="C:/Windows/Fonts/"
def font(name,size):
    for f in (name,'arialbd.ttf'):
        p=F+f
        if os.path.exists(p): return ImageFont.truetype(p,size)
    return ImageFont.load_default()
BLACK=lambda s: font('ariblk.ttf',s)
BOLD =lambda s: font('arialbd.ttf',s)
REG  =lambda s: font('arial.ttf',s)

# team -> (c1 deep, c2 mid, accent, accent2 light, kicker, monogram)
TEAMS={
 'giants':   ('#120a03','#7a3410','#fd5a1e','#ffd9b0','SAN FRANCISCO GIANTS','SF'),
 '49ers':    ('#2a0308','#7a0d17','#c9302c','#efd08a','SAN FRANCISCO 49ERS','49'),
 'warriors': ('#050f26','#1d428a','#ffc72c','#bcd0ff','GOLDEN STATE WARRIORS','GS'),
 'athletics':('#03201a','#0a4130','#1e9e6a','#f0c23a','ATHLETICS','A'),
 'sharks':   ('#021d1c','#064a4a','#00a3b0','#d7eaea','SAN JOSE SHARKS','SJ'),
 'bay':      ('#12151d','#2a1030','#e11d2a','#f5a623','BAY AREA SPORTS','BA'),
}
def hx(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))

def wrap(draw,text,fnt,maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if draw.textlength(t,font=fnt)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def _seed(s):
    h=0
    for ch in s: h=(h*131+ord(ch))&0xffffffff
    return h

def make(team, name, subhead, out, W=1200, H=675, seed=None):
    c1,c2,acc,acc2,kicker,mono = TEAMS.get(team, TEAMS['bay'])
    C1,C2,ACC,ACC2=hx(c1),hx(c2),hx(acc),hx(acc2)
    sd=_seed(seed if seed is not None else name+subhead)
    motif=sd%6; ang=(sd>>3)%2   # gradient direction variant
    # gradient (direction varies by seed so same-team cards differ structurally)
    base=Image.new('RGB',(W,H),C1); px=base.load()
    for y in range(H):
        for x in range(0,W,2):
            t=((x/W)*0.6+(y/H)*0.4) if ang==0 else ((1-x/W)*0.5+(y/H)*0.5)
            r=int(C1[0]+(C2[0]-C1[0])*t); g=int(C1[1]+(C2[1]-C1[1])*t); b=int(C1[2]+(C2[2]-C1[2])*t)
            f=max(0,(t-0.55)/0.45)
            r=int(r*(1-f)+11*f); g=int(g*(1-f)+13*f); b=int(b*(1-f)+17*f)
            px[x,y]=(r,g,b)
            if x+1<W: px[x+1,y]=(r,g,b)
    d=ImageDraw.Draw(base,'RGBA')
    # --- background motif (structural variation -> distinct perceptual hash) ---
    if motif==0:                       # diagonal accent wedge, right
        d.polygon([(W*0.66,0),(W,0),(W,H),(W*0.5,H)], fill=ACC+(22,))
    elif motif==1:                     # vertical panel + stripes, right third
        d.rectangle([W*0.70,0,W,H], fill=ACC+(16,))
        for i in range(0,H,54): d.line([(W*0.70,i),(W,i-40)], fill=(255,255,255,12), width=4)
    elif motif==2:                     # big radial rings, lower-right
        for rr in range(520,120,-70):
            d.ellipse([W-rr-30,H-rr-10,W-30+rr*0.1,H-10+rr*0.1], outline=ACC+(30,), width=6)
    elif motif==3:                     # chevron band across middle
        for k in range(-1,14):
            x0=k*100
            d.polygon([(x0,H*0.42),(x0+50,H*0.5),(x0,H*0.58),(x0-14,H*0.5)], fill=ACC2+(10,))
    elif motif==4:                     # halftone dot field, right
        for gy in range(40,H,46):
            for gx in range(int(W*0.60),W,46):
                d.ellipse([gx,gy,gx+10,gy+10], fill=ACC+(26,))
    else:                              # corner triangle + top bar
        d.polygon([(W,0),(W,H*0.6),(W*0.62,0)], fill=ACC+(20,))
        d.rectangle([0,0,W,10], fill=ACC+(120,))
    # continuous seed-positioned sweep band -> guarantees structural (phash) spread
    off=(sd>>11)%W; sw=170+(sd>>13)%120; skew=((sd>>9)%200)-100
    d.polygon([(off,0),(off+sw,0),(off+sw+skew,H),(off+skew,H)], fill=(255,255,255,14))
    d.line([(off,0),(off+skew,H)], fill=ACC+(60,), width=4)
    # seed-positioned horizontal accent rule (strong phash separator between same-team cards)
    hy=470+(sd>>17)%150
    d.rectangle([0,hy,W,hy+7], fill=ACC+(150,))
    d.rectangle([0,hy+7,W,hy+11], fill=ACC2+(50,))
    # huge ghosted monogram; corner varies by seed
    msz=300+ (sd>>7)%90
    mf=BLACK(msz); tw=d.textlength(mono,font=mf)
    if (sd>>5)%2==0: mpos=(W-tw-24, H-msz*0.92)      # lower-right
    else:            mpos=(W-tw-30, -msz*0.12)        # upper-right
    d.text(mpos, mono, font=mf, fill=ACC2+(24,))
    # left text column, constrained so it never runs under the monogram
    LX=84; MAXW=W*0.60
    # accent underline bar
    d.rounded_rectangle([LX,140,LX+92,154],7,fill=ACC)
    # kicker
    d.text((LX+4,168), kicker, font=BOLD(26), fill=ACC2)
    # name (big, wrapped) - measure block height first
    nf=BLACK(88); lines=wrap(d,name.upper(),nf,MAXW)[:3]
    lh=90; y=214
    for ln in lines:
        d.text((LX,y), ln, font=nf, fill=(255,255,255)); y+=lh
    # subhead below the name block with a clear gap
    y+=18
    sf=REG(29); sub=wrap(d,subhead,sf,MAXW+40)[:2]
    for ln in sub:
        d.text((LX+2,y), ln, font=sf, fill=(224,228,236)); y+=38
    # bottom scrim for footer legibility
    d.rectangle([0,H-70,W,H], fill=(6,8,12,150))
    d.text((LX+2,H-50), "BAY AREA SPORTS BLOG", font=BOLD(22), fill=ACC)
    base.save(out,'JPEG',quality=92)
    return out

if __name__=='__main__':
    import sys
    make(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    print('wrote',sys.argv[4])
