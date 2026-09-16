"""Content inventory for the opportunity audit. Reads only what is on disk."""
import os
import re
import glob
import json
import math
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STOP = set('the a an and or of in on at to for is are was were be been it its this that with '
           'from by as not but they them he she his her we our you your i me my is has have had '
           'what why how who when where which s t re ve'.split())
RECAP = re.compile(r'\b\d+\s*[-,]\s*\d+\b|\bf/\d+\b|\(\d+\)')
QUERY = re.compile(r'\b(schedule|roster|depth chart|history|record|records|stats|standings|'
                   r'how many|why|who|what|when|where|championship|championships|list|guide|'
                   r'explained|vs|rivalry|all time|payroll|cap|draft|ranking|rankings)\b', re.I)

arts = []
for path in sorted(glob.glob(os.path.join(ROOT, 'articles', '*.html'))):
    raw = open(path, encoding='utf-8').read()

    def grab(p, d=''):
        m = re.search(p, raw, re.S)
        return m.group(1) if m else d

    body = re.search(r'<article[^>]*>(.*?)</article>', raw, re.S)
    text = re.sub(r'<[^>]+>', ' ', body.group(1) if body else raw)
    slug = os.path.basename(path)[:-5]
    out_links = set(re.findall(r'href="([a-z0-9][^"/]*?\.html)"', body.group(1) if body else ''))
    arts.append({
        'slug': slug,
        'title': grab(r'<title>(.*?)</title>'),
        'desc': grab(r'<meta name="description" content="(.*?)">'),
        'date': grab(r'"datePublished":"(.*?)"'),
        'section': grab(r'"articleSection":"(.*?)"'),
        'words': len(text.split()),
        'out': {l[:-5] for l in out_links},
        'recap': bool(RECAP.search(grab(r'<title>(.*?)</title>') + ' ' + slug)),
        'query': bool(QUERY.search(grab(r'<title>(.*?)</title>'))),
    })

inbound = collections.Counter()
for a in arts:
    for t in a['out']:
        inbound[t] += 1
for a in arts:
    a['in'] = inbound[a['slug']]

json.dump(arts, open(os.path.join(ROOT, '_inventory.json'), 'w'), default=list)

print('TOTAL %d articles' % len(arts))
print()
print('A. COVERAGE BY SECTION')
by = collections.defaultdict(list)
for a in arts:
    by[a['section']].append(a)
print('   %-18s %5s %7s %8s %7s %7s  %s' % ('section', 'arts', 'recaps', 'evergrn', 'medwds', 'orphanish', 'newest'))
for sec, rows in sorted(by.items(), key=lambda kv: -len(kv[1])):
    recaps = sum(r['recap'] for r in rows)
    ever = sum(r['query'] for r in rows)
    words = sorted(r['words'] for r in rows)
    thin = sum(1 for r in rows if r['in'] <= 1)
    print('   %-18s %5d %7d %8d %7d %7d     %s'
          % (sec, len(rows), recaps, ever, words[len(words) // 2], thin, max(r['date'] for r in rows)))

print()
print('B. EVERGREEN SHAPED ARTICLES THAT ALREADY EXIST (query term in title, not a recap)')
ever = [a for a in arts if a['query'] and not a['recap']]
ever.sort(key=lambda a: -a['words'])
for a in ever[:30]:
    print('   %-62s %5dw in=%-2d %s %s' % (a['slug'][:62], a['words'], a['in'], a['date'], a['section']))
print('   ... %d total' % len(ever))

print()
print('G. OLDEST CONTENT, EVERGREEN SHAPED, MOST AT RISK OF BEING STALE')
for a in sorted(ever, key=lambda a: a['date'])[:15]:
    print('   %-62s %s %5dw in=%d' % (a['slug'][:62], a['date'], a['words'], a['in']))

print()
print('D. TITLE OVERLAP INSIDE A SECTION (possible cannibalisation)')


def toks(a):
    t = re.findall(r'[a-z0-9]+', (a['title'] + ' ' + a['slug']).lower())
    return {w for w in t if w not in STOP and len(w) > 2 and not w.isdigit()}


pairs = []
for sec, rows in by.items():
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            x, y = toks(rows[i]), toks(rows[j])
            if not x or not y:
                continue
            jac = len(x & y) / float(len(x | y))
            if jac >= 0.34 and not (rows[i]['recap'] and rows[j]['recap']):
                pairs.append((jac, rows[i], rows[j]))
pairs.sort(reverse=True, key=lambda p: p[0])
for jac, x, y in pairs[:18]:
    print('   %.2f  %-46s  %-46s' % (jac, x['slug'][:46], y['slug'][:46]))
print('   ... %d pairs at or above 0.34' % len(pairs))

print()
print('E. LINK EQUITY: evergreen pages with the fewest in body inbound links')
for a in sorted(ever, key=lambda a: (a['in'], -a['words']))[:15]:
    print('   in=%-2d %-62s %s' % (a['in'], a['slug'][:62], a['section']))

print()
print('   recaps that mention a player or venue but link nowhere:',
      sum(1 for a in arts if a['recap'] and not a['out']))
print('   articles with zero outbound internal links:', sum(1 for a in arts if not a['out']))
print('   median outbound links per article:',
      sorted(len(a['out']) for a in arts)[len(arts) // 2])
