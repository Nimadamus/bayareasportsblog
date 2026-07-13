#!/usr/bin/env python3
"""Audit every article card thumbnail across all live pages of Bay Area Sports Blog.
Reports: page, article, image, team-from-slug, exact-dup, perceptual-dup, crop risk."""
import os, re, glob, hashlib, json, sys
from PIL import Image
import imagehash

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = [f for f in glob.glob(os.path.join(ROOT,'*.html'))]
IMGDIR = os.path.join(ROOT,'assets','img')

CARD_RE = re.compile(r'<a[^>]*class="(?:ncard|post|mini)"[^>]*href="([^"]+)".*?<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"', re.S)
# also capture nearby h3 title
BLOCK_RE = re.compile(r'<a[^>]*href="(articles/[^"]+)"[^>]*>(.*?)</a>', re.S)
IMG_RE = re.compile(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"')
H3_RE = re.compile(r'<h3>(.*?)</h3>', re.S)

TEAMS = ['giants','49ers','niners','athletics','warriors','sharks','bay','stanford','cal']
def team_of(text):
    t=text.lower()
    for k in ['giants','athletics','warriors','sharks']:
        if k in t: return k
    if '49ers' in t or 'niners' in t or 'purdy' in t or 'aiyuk' in t or 'montana' in t or 'rice' in t or 'kaepernick' in t: return '49ers'
    return '?'

def imgpath(src):
    src = src.lstrip('./')
    while src.startswith('../'): src=src[3:]
    return os.path.join(ROOT, src)

rows=[]
for page in PAGES:
    html=open(page,encoding='utf-8').read()
    pname=os.path.basename(page)
    for m in BLOCK_RE.finditer(html):
        href, inner = m.group(1), m.group(2)
        im = IMG_RE.search(inner)
        if not im: continue
        src, alt = im.group(1), im.group(2)
        h3 = H3_RE.search(inner)
        title = re.sub('<[^>]+>','',h3.group(1)).strip() if h3 else alt
        rows.append(dict(page=pname, href=href, src=src, alt=alt, title=title))

# hash images
hashes={}
for r in rows:
    p=imgpath(r['src'])
    if not os.path.exists(p):
        r['sha']='MISSING'; r['phash']=None; r['size']=None; continue
    data=open(p,'rb').read()
    r['sha']=hashlib.sha256(data).hexdigest()[:12]
    try:
        im=Image.open(p); r['size']=im.size
        r['phash']=str(imagehash.phash(im))
    except Exception as e:
        r['phash']=None; r['size']=None

# exact dup by src used on >1 distinct article
from collections import defaultdict
by_src=defaultdict(set)
for r in rows: by_src[r['src']].add(r['href'])
# perceptual clusters
phlist=[(r['src'],imagehash.hex_to_hash(r['phash'])) for r in rows if r['phash']]
seen={}
for r in rows:
    r['dup_articles']=sorted(by_src[r['src']])
    r['is_dup']= len(by_src[r['src']])>1
    # team mismatch
    r['team_title']=team_of(r['title']+' '+r['href'])
    r['team_img']=team_of(os.path.basename(r['src']))
    r['team_mismatch']= r['team_img']!='?' and r['team_title']!='?' and r['team_img']!=r['team_title']
    # crop risk: portrait source into 16:9
    if r['size']:
        w,h=r['size']; r['portrait']= h> w*1.15
    else: r['portrait']=None

# perceptual near-dup across different src files
near=[]
srcs=sorted(set((r['src'],r['phash']) for r in rows if r['phash']))
for i in range(len(srcs)):
    for j in range(i+1,len(srcs)):
        if srcs[i][0]==srcs[j][0]: continue
        d=imagehash.hex_to_hash(srcs[i][1])-imagehash.hex_to_hash(srcs[j][1])
        if d<=6: near.append((srcs[i][0],srcs[j][0],d))

out={'rows':rows,'near_dupes':near}
json.dump(out, open(os.path.join(os.path.dirname(__file__),'audit.json'),'w'), indent=1, default=str)

# print summary
print("TOTAL CARDS:", len(rows))
dsrcs={s:a for s,a in by_src.items() if len(a)>1}
print("\n== EXACT DUPLICATE IMAGES (same file, multiple articles) ==")
for s,a in sorted(dsrcs.items(), key=lambda x:-len(x[1])):
    print(" ", os.path.basename(s), "->", len(a), "articles")
    for h in sorted(a): print("       ", h)
print("\n== TEAM/UNIFORM MISMATCH (img team != article team) ==")
for r in rows:
    if r['team_mismatch']:
        print("  [%s] %-40s title-team=%s img=%s" %(r['page'], os.path.basename(r['src']), r['team_title'], r['team_img']))
print("\n== PORTRAIT SOURCES CROPPED TO 16:9 (crop risk, no focal override) ==")
ov=open(os.path.join(ROOT,'assets','style.css')).read()
overrides=set(re.findall(r'img\[src\*="([^"]+)"\]',ov))
seenport=set()
for r in rows:
    b=os.path.basename(r['src'])
    if r['portrait'] and b not in seenport:
        seenport.add(b)
        key=b.split('.')[0]
        has=any(o in b for o in overrides)
        print("  %-45s %s  focal_override=%s" %(b, r['size'], 'yes' if has else 'NO'))
print("\n== PERCEPTUAL NEAR-DUP (different files, phash<=6) ==")
for a,b,d in near:
    print("  d=%d  %s  ~  %s" %(d, os.path.basename(a), os.path.basename(b)))
print("\n== MISSING FILES ==")
for r in rows:
    if r['sha']=='MISSING': print("  ",r['src'],"(",r['page'],")")
