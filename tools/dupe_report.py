"""dupe_report.py: group the thumb_gate PHASH duplicates so you can tell an accident
from the house template.

thumb_gate counts one failure per card per page, so a handful of look-alike files reads
as dozens of failures. This prints the actual groups with each file's sha1, which
articles use it, and the hamming distances inside the group. Same sha on two articles is
an accident. Different shas with different headline text is cardgen doing its job.
"""
import os
import re
import sys
import glob
import hashlib
from collections import defaultdict
from PIL import Image
import imagehash

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
PHASH_MIN = 6

srcs = set()
for page in glob.glob(os.path.join(ROOT, '*.html')):
    html = open(page, encoding='utf-8').read()
    for a in re.finditer(r'<a\b[^>]*\bhref="((?:\.\./)?(?:articles/)?[^"]+\.html)"[^>]*>(.*?)</a>', html, re.S):
        href, block = a.group(1), a.group(2)
        if 'articles/' not in href:
            continue
        im = re.search(r'<img\s+src="([^"]+)"[^>]*\salt="([^"]*)"', block, re.S)
        if im:
            srcs.add((im.group(1), os.path.basename(href)))

by_file = defaultdict(set)
for src, href in srcs:
    by_file[src].add(href)

meta = {}
for src in by_file:
    p = os.path.join(ROOT, src.lstrip('./'))
    while '../' in p:
        p = p.replace('../', '')
    if not os.path.exists(p):
        continue
    im = Image.open(p)
    meta[src] = {'ph': imagehash.phash(im), 'sha': hashlib.sha1(open(p, 'rb').read()).hexdigest()[:12],
                 'size': os.path.getsize(p), 'path': p}

# union find over near duplicate pairs
parent = {s: s for s in meta}


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(a, b):
    parent[find(a)] = find(b)


keys = list(meta)
pairs = []
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        d = meta[keys[i]]['ph'] - meta[keys[j]]['ph']
        if d < PHASH_MIN:
            pairs.append((d, keys[i], keys[j]))
            union(keys[i], keys[j])

groups = defaultdict(list)
for s in meta:
    groups[find(s)].append(s)

print('cards with art:', len(meta), '| near duplicate pairs:', len(pairs))
print()
n = 0
for root, members in sorted(groups.items()):
    if len(members) < 2:
        continue
    n += 1
    shas = {meta[m]['sha'] for m in members}
    ds = [d for d, a, b in pairs if a in members and b in members]
    kind = 'IDENTICAL FILE' if len(shas) == 1 else 'near duplicate'
    print('GROUP %d  %s  distance %s' % (n, kind, sorted(set(ds))))
    for m in sorted(members):
        print('   %-62s sha=%s  %6dB  articles=%s'
              % (os.path.basename(m), meta[m]['sha'], meta[m]['size'], sorted(by_file[m])[:2]))
    print()
