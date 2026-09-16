"""Side by side check that the hub and the outlook are not chasing the same intent."""
import re
import os
import sys
import glob
import collections

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PAGES = sys.argv[1:] or ['warriors-2026-27-schedule-season-hub', 'warriors-2026-27-season-outlook']
PREDICT = re.compile(r'\b(ceiling|floor|realistic|prediction|predict|expect|should be|'
                     r'projected|outlook|range of outcomes|if healthy|contend)\b', re.I)
FACTUAL = re.compile(r'\b(schedule|opponent|home|road|tip|result|date|record|back to back|'
                     r'homestand|opener)\b', re.I)

for slug in PAGES:
    t = open('articles/%s.html' % slug, encoding='utf-8').read()
    body = re.search(r'<article[^>]*>(.*?)</article>', t, re.S).group(1)
    text = re.sub(r'<[^>]+>', ' ', body)
    print('=' * 96)
    print(slug)
    print('  TITLE :', re.search(r'<title>(.*?)</title>', t, re.S).group(1))
    print('  H1    :', re.sub(r'<[^>]+>', '', re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S).group(1)))
    print('  DESC  :', re.search(r'<meta name="description" content="(.*?)">', t, re.S).group(1)[:150])
    print('  H2s   :', ' | '.join(re.sub(r'<[^>]+>', '', h) for h in re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.S))[:190])
    print('  words :', len(text.split()))
    print('  prediction words: %-3d  schedule words: %d'
          % (len(PREDICT.findall(text)), len(FACTUAL.findall(text))))

# anchor text pointing at each page from anywhere on the site
print()
print('INBOUND ANCHOR TEXT')
for slug in PAGES:
    hits = []
    for f in glob.glob('*.html') + glob.glob('articles/*.html'):
        if os.path.basename(f)[:-5] == slug:
            continue
        html = open(f, encoding='utf-8').read()
        for m in re.finditer(r'<a[^>]+href="[^"]*%s\.html"[^>]*>(.*?)</a>' % re.escape(slug), html, re.S):
            txt = re.sub(r'<[^>]+>', ' ', m.group(1)).strip()
            txt = re.sub(r'\s+', ' ', txt)
            if txt and len(txt) < 120:
                hits.append((os.path.basename(f), txt))
    print(' ', slug)
    for f, txt in hits[:8]:
        print('     %-52s "%s"' % (f[:52], txt[:70]))
    if not hits:
        print('     none')

# title token overlap
def toks(s):
    return {w for w in re.findall(r'[a-z0-9]+', s.lower()) if len(w) > 2}


a = toks(open('articles/%s.html' % PAGES[0], encoding='utf-8').read().split('<title>')[1].split('</title>')[0])
b = toks(open('articles/%s.html' % PAGES[1], encoding='utf-8').read().split('<title>')[1].split('</title>')[0])
print()
print('title token overlap (jaccard): %.2f   shared: %s' % (len(a & b) / len(a | b), sorted(a & b)))
