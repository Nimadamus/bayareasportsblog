#!/usr/bin/env python3
"""diversify_photos.py - give every article its own photo. For each source photo used by
more than one article, keep it on the first article and fetch a different licensed
Commons photo for the rest. A result is only accepted when its file title names the
subject (or, for team fallbacks, the team/venue), it is not already used, and it is not
a perceptual near-duplicate of a photo already in use."""
import os, re, sys, json, time, collections, io
sys.path.insert(0, os.path.dirname(__file__))
from commons_fetch import search, get
from PIL import Image
import imagehash

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
P = 'assets/img/players/'
pick = json.load(open('tools/photo_pick.json'))
DROP = set('real giants 49ers athletics warriors sharks niners card the and of vs 2014 2019 2025 2026 cropped jpg png'.split())
TEAM = {
 '49ers': (['San Francisco 49ers', "Levi's Stadium 49ers", '49ers game', 'Candlestick Park 49ers'], r"49ers|levi|candlestick|niners"),
 'giants': (['San Francisco Giants', 'Oracle Park', 'AT&T Park Giants', 'Giants baseball San Francisco'], r"giants|oracle|at&t park|at.t park|pac bell|sf giants"),
 'athletics': (['Oakland Athletics', 'Athletics baseball', 'Oakland Coliseum', 'Sutter Health Park'], r"athletics|oakland a|coliseum|sutter|a's"),
 'warriors': (['Golden State Warriors', 'Chase Center', 'Warriors basketball'], r"warriors|chase center|oracle arena"),
 'sharks': (['San Jose Sharks', 'SAP Center'], r"sharks|sap center"),
 'raiders': (['Las Vegas Raiders', 'Allegiant Stadium'], r"raiders|allegiant"),
 'stanford': (['Stanford Cardinal football', 'Stanford Stadium'], r"stanford"),
 'cal': (['California Golden Bears', 'California Memorial Stadium'], r"california|golden bears|berkeley"),
}
SUBJ = {'brock-purdy-49ers': 'Brock Purdy', 'purdy': 'Brock Purdy', 'rafael-devers-giants': 'Rafael Devers',
        'commons-giants-tony-vitello-clueless-lineups-eldridge-leadoff': 'Tony Vitello', 'commons-tony-vitello-hire-giants-mistake': 'Tony Vitello',
        'lopez': 'Jacob Lopez', 'rooker': 'Brent Rooker', 'logan-webb-giants-blue-jays': 'Logan Webb', 'robbie-ray-giants': 'Robbie Ray',
        'montana': 'Joe Montana', 'posey': 'Buster Posey', 'adames-giants-grand-slam-mariners': 'Willy Adames',
        'commons-warriors-2026-27-projected-rotation': 'Stephen Curry', 'curry2016': 'Stephen Curry', 'stephen-curry-real': 'Stephen Curry'}


def team_of(slug):
    for t in TEAM:
        if t in slug: return t
    if any(x in slug for x in ('purdy', 'kittle', 'mccaffrey', 'bosa', 'lynch', 'shanahan', 'york', 'montana', 'rice', 'kaepernick', 'mykel', 'mustapha')): return '49ers'
    if any(x in slug for x in ('vitello', 'eldridge', 'posey', 'bonds', 'bochy', 'krukow', 'bumgarner', 'devers', 'oracle')): return 'giants'
    if any(x in slug for x in ('curry', 'klay', 'lendeborg', 'nelson', 'kuminga')): return 'warriors'
    if 'oakland' in slug or 'coliseum' in slug: return 'athletics'
    return None


def subject(src):
    st = os.path.splitext(os.path.basename(src))[0]
    if st in SUBJ: return SUBJ[st]
    w = [x for x in st.split('-') if x not in DROP and not x.isdigit()]
    if len(w) >= 2 and not any(x in ('park', 'stadium', 'center', 'ground', 'field', 'arena', 'palace', 'pavilion') for x in w):
        return ' '.join(x.capitalize() for x in w[:2])
    return None


def main():
    used_urls = set()
    hashes = {}
    for v in set(pick.values()):
        try: hashes[v] = imagehash.phash(Image.open(v).convert('RGB'))
        except Exception: pass
    groups = collections.defaultdict(list)
    for s in sorted(pick): groups[pick[s]].append(s)
    log = []
    for src, arts in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        if len(arts) < 2: continue
        name = subject(src)
        for slug in arts[1:]:
            t = team_of(slug)
            tries = []
            if name: tries.append((name, re.escape(name.split()[-1])))
            if t:
                qs, rx = TEAM[t]
                tries += [(q, rx) for q in qs]
            got = None
            for q, rx in tries:
                try: res = search(q, 25)
                except Exception: time.sleep(30); continue
                time.sleep(3)
                for r in res:
                    if r['url'] in used_urls or not re.search(rx, r['title'], re.I): continue
                    try:
                        data = get(r['url']); im = Image.open(io.BytesIO(data)).convert('RGB')
                    except Exception: continue
                    if min(im.size) < 700: continue
                    h = imagehash.phash(im)
                    if any(h - hh < 10 for hh in hashes.values()): used_urls.add(r['url']); continue
                    dst = P + 'div-%s.jpg' % slug
                    open(dst, 'wb').write(data)
                    used_urls.add(r['url']); hashes[dst] = h
                    got = (dst, r); break
                if got: break
            if got:
                pick[slug] = got[0]
                log.append('%s: %s, photo by %s, %s, %s' % (os.path.basename(got[0])[:-4], got[1]['title'][5:], got[1]['artist'][:80], got[1]['lic'], got[1]['page']))
                print('OK  ', slug, '<-', got[1]['title'][5:], flush=True)
                json.dump(pick, open('tools/photo_pick.json', 'w'), indent=1)
                with open(P + 'CREDITS.txt', 'a', encoding='utf-8') as f: f.write(log[-1] + '\n')
            else:
                print('KEEP', slug, '(no distinct photo found)', flush=True)


if __name__ == '__main__':
    main()
