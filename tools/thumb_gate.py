#!/usr/bin/env python3
"""thumb_gate.py [--site] [page.html ...] - HARD publish gate for article card images.
Blocks (exit 2) unless every card on the checked pages passes:
  exists | min-resolution | ~16:9 ratio | unique file | no perceptual duplicate.
Default checks index.html. --site checks all root pages. Prints a pass/fail table.
"""
import os, re, sys, glob, hashlib
from PIL import Image
import imagehash

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MINW,MINH=600,338          # min rendered source; cards are 1200x675
RATIO=16/9.0; RTOL=0.12
PHASH_MIN=6                # Hamming distance below which two cards are "duplicates"

args=[a for a in sys.argv[1:] if not a.startswith('--')]
site='--site' in sys.argv
if site: pages=[os.path.basename(p) for p in glob.glob(os.path.join(ROOT,'*.html'))]
else: pages=args or ['index.html']

def imgpath(src):
    s=src.lstrip('./')
    while s.startswith('../'): s=s[3:]
    return os.path.join(ROOT,s)

cards=[]  # (page, href, src, alt)
seen=set()
for pg in pages:
    html=open(os.path.join(ROOT,pg),encoding='utf-8').read()
    # Scan anchor-bounded blocks: an <img> only counts as an article's card if it sits
    # INSIDE that anchor. Anchors with no image (text tiles, list items) are skipped
    # rather than silently adopting the next anchor's image.
    for a in re.finditer(r'<a\b[^>]*\bhref="((?:\.\./)?(?:articles/)?[^"]+\.html)"[^>]*>(.*?)</a>', html, re.S):
        href, block = a.group(1), a.group(2)
        if 'articles/' not in href: continue
        im=re.search(r'<img\s+src="([^"]+)"[^>]*\salt="([^"]*)"', block, re.S)
        if not im: continue
        src,alt=im.group(1),im.group(2)
        k=(pg,href,src)
        if k in seen: continue
        seen.add(k); cards.append((pg,href,src,alt))

fails=[]; info=[]
from collections import defaultdict
by_src=defaultdict(set); hashes={}
for pg,href,src,alt in cards:
    p=imgpath(src)
    row={'page':pg,'href':os.path.basename(href),'src':os.path.basename(src),'alt':alt,'ok':True,'why':[]}
    if not os.path.exists(p):
        row['ok']=False; row['why'].append('MISSING'); info.append(row); continue
    by_src[src].add(href)
    try:
        im=Image.open(p); w,h=im.size
        if w<MINW or h<MINH: row['ok']=False; row['why'].append('lowres %dx%d'%(w,h))
        r=w/float(h)
        if abs(r-RATIO)>RTOL: row['ok']=False; row['why'].append('ratio %.2f'%r)
        hashes[src]=imagehash.phash(im)
    except Exception as e:
        row['ok']=False; row['why'].append('imgerr')
    info.append(row)

# uniqueness: same file on >1 article
for src,arts in by_src.items():
    if len(arts)>1:
        for row in info:
            if row['src']==os.path.basename(src): row['ok']=False; row['why'].append('DUP-file(%d)'%len(arts))
# perceptual near-dup across distinct files
srcs=list(hashes.items())
for i in range(len(srcs)):
    for j in range(i+1,len(srcs)):
        if srcs[i][0]==srcs[j][0]: continue
        if srcs[i][1]-srcs[j][1] < PHASH_MIN:
            for row in info:
                if row['src'] in (os.path.basename(srcs[i][0]),os.path.basename(srcs[j][0])):
                    row['ok']=False; row['why'].append('PHASH-dup')

fails=[r for r in info if not r['ok']]
print("THUMB GATE  pages=%s  cards=%d  PASS=%d  FAIL=%d"%(','.join(pages),len(info),len(info)-len(fails),len(fails)))
for r in fails:
    print("  FAIL %-46s %-40s %s"%(r['href'][:46], r['src'][:40], ';'.join(sorted(set(r['why'])))))
if fails:
    print("\nGATE BLOCKED: fix the above before publishing."); sys.exit(2)
print("GATE PASSED."); sys.exit(0)
