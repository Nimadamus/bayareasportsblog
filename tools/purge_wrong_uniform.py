#!/usr/bin/env python3
"""purge_wrong_uniform.py - remove every reference to known wrong-uniform / prior-team
source photos from the live site. Article bodies + og:image + json-ld -> that article's
own card. Listing/home/timeline decorative refs -> the linked article's card (or a mapped
correct card for non-article nodes). Idempotent."""
import os, re, glob, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WRONG={'rooker.jpg','willy-adames-giants.jpg','rafael-devers-giants.jpg','curry.jpg'}
CARDS='assets/img/cards'
man=json.load(open(os.path.join(os.path.dirname(__file__),'cards_manifest.json'),encoding='utf-8'))
# card path per article slug
slugcard={os.path.splitext(os.path.basename(h))[0]: CARDS+'/'+os.path.splitext(os.path.basename(h))[0]+'.jpg' for h in man}
# decorative fallbacks for non-article timeline nodes (correct-team existing cards)
DECOR={'curry.jpg':'warriors-championship-history','rooker.jpg':'athletics-sacramento-bay-area-villains'}

def wrong_in(s): return any('players/'+w in s for w in WRONG)
changed=[]

# 1) article self-pages: body hero + og + json-ld -> own card
for f in glob.glob(os.path.join(ROOT,'articles','*.html')):
    slug=os.path.splitext(os.path.basename(f))[0]
    if slug not in slugcard: continue
    card=slugcard[slug]; s=open(f,encoding='utf-8').read(); o=s
    absu='https://bayareasportsblog.com/'+card
    # og:image + json-ld absolute urls (any players/* -> card)
    s=re.sub(r'(og:image" content=")https://bayareasportsblog\.com/assets/img/players/[^"]+(")', r'\1'+absu+r'\2', s)
    s=re.sub(r'("image":")https://bayareasportsblog\.com/assets/img/players/[^"]+(")', r'\1'+absu+r'\2', s)
    # body hero <img ...players/WRONG...> -> card (relative ../)
    for w in WRONG:
        s=re.sub(r'src="\.\./assets/img/players/'+re.escape(w)+r'"',
                 'src="../'+card+'"', s)
    if s!=o: open(f,'w',encoding='utf-8').write(s); changed.append(os.path.basename(f))

# 2) any page: <a href="articles/X"> ... <img src=players/WRONG> -> X's card
def fix_anchor(html, page):
    def repl(m):
        block=m.group(0); href=m.group(1); slug=os.path.splitext(os.path.basename(href))[0]
        if slug not in slugcard: return block
        card=slugcard[slug]; rel=('../'+card) if page.startswith('articles/') else card
        return re.sub(r'src="(?:\.\./)?assets/img/players/[^"]+"', 'src="'+rel+'"', block, count=1)
    return re.sub(r'<a\b[^>]*href="(?:\.\./)?(articles/[^"]+\.html)"[^>]*>.*?</a>', repl, html, flags=re.S)

for f in glob.glob(os.path.join(ROOT,'*.html'))+glob.glob(os.path.join(ROOT,'articles','*.html')):
    page=os.path.relpath(f,ROOT).replace(os.sep,'/'); s=open(f,encoding='utf-8').read(); o=s
    if wrong_in(s): s=fix_anchor(s,page)
    # 3) leftover decorative (timeline tl-node href=timeline.html, feature dc-media) -> mapped card
    for w,card_slug in DECOR.items():
        if 'players/'+w in s and card_slug in slugcard:
            rel=('../'+slugcard[card_slug]) if page.startswith('articles/') else slugcard[card_slug]
            s=s.replace('assets/img/players/'+w, rel)
    if s!=o: open(f,'w',encoding='utf-8').write(s); changed.append(os.path.basename(f))

print("purge touched:", sorted(set(changed)))
# report any remaining
rem=[]
for f in glob.glob(os.path.join(ROOT,'**','*.html'),recursive=True):
    s=open(f,encoding='utf-8').read()
    for w in WRONG:
        if 'players/'+w in s: rem.append((os.path.relpath(f,ROOT),w))
print("REMAINING wrong-uniform refs:", len(rem))
for r in rem[:40]: print("  ",r)
