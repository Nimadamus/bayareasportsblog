"""Snippet truncation risk and internal support, both measurable without Search Console."""
import os
import re
import glob
import json

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

rows = []
for f in sorted(glob.glob('articles/*.html')):
    t = open(f, encoding='utf-8').read()
    slug = os.path.basename(f)[:-5]
    title = re.search(r'<title>(.*?)</title>', t, re.S).group(1)
    desc = re.search(r'<meta name="description" content="(.*?)">', t, re.S)
    desc = desc.group(1) if desc else ''
    body = re.search(r'<article[^>]*>(.*?)</article>', t, re.S)
    body = body.group(1) if body else ''
    rows.append({'slug': slug, 'title': title, 'tlen': len(title),
                 'desc': desc, 'dlen': len(desc),
                 'date': re.search(r'"datePublished":"(.*?)"', t).group(1),
                 'out': len({m for m in re.findall(r'href="([a-z0-9][^"/]*?)\.html"', body)})})

inb = {r['slug']: 0 for r in rows}
for f in glob.glob('articles/*.html'):
    t = open(f, encoding='utf-8').read()
    me = os.path.basename(f)[:-5]
    for s in inb:
        if s != me and 'href="%s.html"' % s in t:
            inb[s] += 1
for r in rows:
    r['in'] = inb[r['slug']]

print('TITLES OVER 70 CHARS, truncated in most result layouts')
for r in sorted(rows, key=lambda r: -r['tlen'])[:8]:
    if r['tlen'] > 70:
        print('  %3d  %-58s %s' % (r['tlen'], r['slug'][:58], r['title'][:80]))

print()
print('DESCRIPTIONS OVER 165 CHARS, tail gets cut (%d total)' % sum(1 for r in rows if r['dlen'] > 165))
for r in sorted(rows, key=lambda r: -r['dlen'])[:12]:
    print('  %3d  %-58s in=%-2d %s' % (r['dlen'], r['slug'][:58], r['in'], r['date']))

print()
print('BEST INTERNALLY SUPPORTED PAGES, where a CTR fix would pay most')
for r in sorted(rows, key=lambda r: -r['in'])[:12]:
    print('  in=%-3d out=%-2d %-58s t=%d d=%d' % (r['in'], r['out'], r['slug'][:58], r['tlen'], r['dlen']))

print()
print('EVERGREEN SHAPED PAGES WITH THE WEAKEST SUPPORT')
Q = re.compile(r'\b(schedule|roster|depth chart|history|record|records|guide|explained|vs)\b', re.I)
weak = [r for r in rows if Q.search(r['title']) and r['in'] <= 2]
for r in sorted(weak, key=lambda r: r['in'])[:12]:
    print('  in=%-2d %-58s %s' % (r['in'], r['slug'][:58], r['date']))
