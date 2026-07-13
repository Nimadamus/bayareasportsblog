#!/usr/bin/env python3
"""contact_sheet.py [page.html ...] - render every article card on the given pages
(default index.html) into a labeled grid PNG at true card ratio, so duplicates and
bad crops are obvious before deploy. Output: tools/contact_sheet.png"""
import os, re, sys, glob
from PIL import Image, ImageDraw, ImageFont
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages=sys.argv[1:] or ['index.html']
def font(s):
    try: return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf",s)
    except: return ImageFont.load_default()
items=[]
seen=set()
for pg in pages:
    html=open(os.path.join(ROOT,pg),encoding='utf-8').read()
    for m in re.finditer(r'href="((?:\.\./)?(?:articles/)?[^"]+\.html)"[^>]*>.*?<img src="([^"]+)"[^>]*alt="([^"]*)"', html, re.S):
        href,src,alt=m.group(1),m.group(2),m.group(3)
        if 'articles/' not in href: continue
        key=(href,src)
        if key in seen: continue
        seen.add(key)
        items.append((src,alt))
cw,ch=320,180; pad=26; cols=4
rows=(len(items)+cols-1)//cols
W=cols*(cw+8)+8; H=rows*(ch+pad+8)+8
sheet=Image.new('RGB',(W,H),(17,18,22)); d=ImageDraw.Draw(sheet)
from collections import Counter
cnt=Counter(s for s,_ in items)
for i,(src,alt) in enumerate(items):
    p=os.path.join(ROOT, src.lstrip('./').replace('../',''))
    try:
        im=Image.open(p).convert('RGB').resize((cw,ch))
    except Exception:
        im=Image.new('RGB',(cw,ch),(90,0,0))
    x=8+(i%cols)*(cw+8); y=8+(i//cols)*(ch+pad+8)
    sheet.paste(im,(x,y))
    dup = cnt[src]>1
    d.rectangle([x,y,x+cw,y+ch],outline=(200,40,40) if dup else (60,60,70), width=3 if dup else 1)
    lbl=os.path.basename(src)[:40]+('  DUP!' if dup else '')
    d.text((x+3,y+ch+4), lbl, fill=(255,120,120) if dup else (200,204,212), font=font(13))
sheet.save(os.path.join(os.path.dirname(__file__),'contact_sheet.png'))
print("cards:",len(items),"dupes:",sum(1 for s in cnt if cnt[s]>1))
