#!/usr/bin/env python3
"""repool_bad.py - replace hand-rejected card photos (wrong team uniform, food, cars,
backs of heads, silhouettes, cut faces, graphics) with a curated, eyeballed pool of
generic team photos (venue / team action, no single wrong player). Pool photos are
spread out by publish date so nearby articles never share a picture.
Indices refer to the listing sheet index file (tools/listing_sheet.py) reviewed 2026-11-03."""
import json, re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
idx = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
pick = json.load(open('tools/photo_pick.json'))
POOL = {   # r2 sheet indices, reviewed 2026-11-03 after the first pass
 '49ers': [1, 2, 4, 10, 11, 17, 23, 25, 26, 27, 32, 35, 36, 38, 44, 48, 50, 51, 52, 59, 60, 68, 69, 72],
 'giants': [128, 137, 144, 146, 152, 153, 155, 160, 166, 170, 171, 172, 176, 177, 182, 185, 188, 190, 191, 193, 198, 200, 204, 209, 212, 213, 220, 270],
 'athletics': [78, 79, 84, 87, 88, 89, 90, 93, 94, 95, 99, 100, 102, 104, 105, 106, 107, 108, 109, 112, 113, 114, 115],
 'warriors': [138, 246, 247, 252, 260, 262, 135, 248, 266, 231],
 'bay': [230, 134, 271, 128], 'cal': [129, 130, 132], 'raiders': [233],
}
BAD = {
 '49ers': [3, 13, 16, 18, 20, 62, 63, 64, 218, 221, 226, 272],
 'athletics': [80, 81, 83, 85, 86, 101, 103],
 'giants': [117, 139, 150, 156, 161, 174, 207, 214, 215, 250],
 'bay': [118, 119, 120], 'cal': [122], 'warriors': [254, 255, 256, 257, 258, 259, 264], 'raiders': [235],
}
# venue photos whose signage / scoreboards read as baked text at card crops (image gate)
EXCL = {'commons-athletics-astros-7-6-six-run-comeback-muncy-august-23', 'div-giants-astros-4-1-whisenhunt-eldridge-homer-hunter-brown-august-11',
        'div-giants-tigers-3-1-10th-webb-eight-innings-wasted-august-9', 'div-giants-tony-vitello-ejected-again-webb-tossed-diamondbacks',
        'commons-giants-red-sox-5-4-wilkinson-fourth-inning-swept-august-23', 'div-giants-trade-deadline-monday-posey-sell-ramos-arraez-ray',
        'div-giants-whisenhunt-gem-rockies-8-2-july-9'}
pool = {t: [pick[idx[i]] for i in v if os.path.basename(pick[idx[i]])[:-4] not in EXCL] for t, v in POOL.items()}


def date(s):
    m = re.search(r'"datePublished":\s*"(\d{4}-\d\d-\d\d)', open('articles/%s.html' % s, encoding='utf-8').read())
    return m.group(1) if m else '2000-01-01'


order = sorted(pick, key=date)                       # oldest -> newest
pos = {s: n for n, s in enumerate(order)}
bad = {idx[i]: t for t, v in BAD.items() for i in v}
last = {}                                            # photo -> latest position used
for s in order:
    if s not in bad: last[pick[s]] = pos[s]
changes = 0
for s in order:
    if s not in bad: continue
    cands = pool[bad[s]]
    # photo whose nearest use (by date position) is furthest away
    def gap(p):
        uses = [pos[o] for o in order if pick[o] == p and o != s]
        return min([abs(pos[s] - u) for u in uses] or [10 ** 6])
    best = max(cands, key=gap)
    pick[s] = best; changes += 1
    print('%-60s -> %s (gap %d)' % (s[:60], os.path.basename(best), gap(best)))
json.dump(pick, open('tools/photo_pick.json', 'w'), indent=1)
open('tools/repool_slugs.txt', 'w', newline='').write('\n'.join(sorted(bad)))
print('reassigned', changes)
