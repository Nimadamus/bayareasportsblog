#!/usr/bin/env python3
"""home_unique.py - every card on the homepage gets its own photo, and any homepage card that
fails the image gate is swapped for a curated team pool photo (tools/photo_pool.json, built
from the 2026-11-03 eyeball review). Newest card keeps its photo; later duplicates move.
Prints the slugs it changed (feed them to photo_cards.py)."""
import os, re, sys, json
from PIL import Image
import imagehash
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, os.path.expanduser('~/tools/image_gate'))
import image_gate as G
pick = json.load(open('tools/photo_pick.json'))
pool = json.load(open('tools/photo_pool.json'))
card2slug = {}
for s in pick:
    m = re.search(r'og:image" content="https://bayareasportsblog\.com/assets/img/cards/(.*?)\.jpg"', open('articles/%s.html' % s, encoding='utf-8').read())
    card2slug[m.group(1) if m else s] = s
home = []
for c in re.findall(r'assets/img/cards/([a-z0-9\-]+?)(?:-\d+w)?\.(?:jpg|webp)', open('index.html', encoding='utf-8').read()):
    if c in card2slug and card2slug[c] not in home: home.append(card2slug[c])


def team(s):
    for t in ('49ers', 'giants', 'athletics', 'warriors', 'sharks', 'raiders', 'stanford', 'cal'):
        if t in s: return t
    if any(x in s for x in ('purdy', 'york', 'mykel', 'bosa', 'kittle', 'shanahan', 'lynch', 'rice', 'montana', 'kaepernick', 'aiyuk')): return '49ers'
    if any(x in s for x in ('curry', 'lebron', 'klay', 'nelson')): return 'warriors'
    if any(x in s for x in ('vitello', 'bochy', 'bonds', 'oracle-park', 'kent', 'josuar', 'bumgarner')): return 'giants'
    if 'celebrini' in s: return 'sharks'
    return 'bay'


H = {}
def ph(p):
    if p not in H: H[p] = imagehash.phash(Image.open(p).convert('RGB'))
    return H[p]


changed, taken = [], []
for s in home:                                   # homepage order = newest first
    src = pick[s]
    card = [c for c, v in card2slug.items() if v == s][0]
    bad = not G.check('assets/img/cards/%s.jpg' % card, 'card')['ok']
    dup = any(ph(src) - ph(t) < 10 for t in taken)
    if bad or dup:
        for cand in pool.get(team(s), []) + pool['bay']:
            if any(ph(cand) - ph(t) < 10 for t in taken): continue
            pick[s] = src = cand; changed.append(s); break
    taken.append(src)
json.dump(pick, open('tools/photo_pick.json', 'w'), indent=1)
print(' '.join(changed))
