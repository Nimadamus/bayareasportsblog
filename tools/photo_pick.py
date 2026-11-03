#!/usr/bin/env python3
"""photo_pick.py - choose the real source photo for every article card.
Order: cards_manifest photo src -> real photo used in the article -> library name match.
Writes tools/photo_pick.json {slug: src or null}."""
import os, re, glob, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
BAD=re.compile(r'panel|stat|chart|graphic|table|card|logo|-\d+w\.')
GENERIC=set('real 49ers giants athletics warriors sharks niners stadium park center the and of vs week preseason win falcons 2013 2014 2025 2026 seattle lumen field aerial walk out handoff scoreboard midfield snap blowout nationals tigers blue jays angels broncos salute to service michigan mariners grand slam pick 124 cardinals yards scrimmage 116 levis rams tackle'.split())
man=json.load(open('tools/cards_manifest.json'))
lib=[p.replace(os.sep,'/') for p in glob.glob('assets/img/players/*') if p.lower().endswith(('.jpg','.png','.jpeg')) and not BAD.search(os.path.basename(p))]
# prefer jpg over same-stem png/webp
keys={}
for p in lib:
    toks=[t for t in re.split(r'[-_.]',os.path.splitext(os.path.basename(p))[0].lower()) if t and t not in GENERIC and not t.isdigit()]
    if toks: keys[p]=toks
def libmatch(slug):
    st=set(slug.split('-')); best=None; bs=0
    for p,toks in keys.items():
        hit=[t for t in toks if t in st and len(t)>2]
        if not hit: continue
        s=len(hit)*10+sum(len(t) for t in hit)
        if s>bs: bs=s; best=p
    return best
out={}
for a in sorted(glob.glob('articles/*.html')):
    slug=os.path.basename(a)[:-5]; key='articles/%s.html'%slug
    m=man.get(key,{})
    src=None
    if m.get('mode')=='photo' and m.get('src') and os.path.exists(m['src']): src=m['src']
    if not src:
        t=open(a,encoding='utf-8').read()
        for p in dict.fromkeys(re.findall(r'(assets/img/players/[^"\s]+?\.(?:jpg|png))',t)):
            if not BAD.search(os.path.basename(p)) and os.path.exists(p): src=p; break
    if not src: src=libmatch(slug)
    out[slug]=src
json.dump(out,open('tools/photo_pick.json','w'),indent=1)
none=[s for s,v in out.items() if not v]
print(len(out),'articles; no photo',len(none)); print('\n'.join(none))
