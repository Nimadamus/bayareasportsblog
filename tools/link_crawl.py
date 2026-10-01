#!/usr/bin/env python3
"""tools/link_crawl.py: crawl the site on disk the way a crawler would, from index.html.

Reports, per page: inbound links from other pages (all, and contextual body links only,
meaning outside header, nav and footer), click depth from the home page, broken internal
links, and pages that are in the sitemap but reachable by no link at all.

    python tools/link_crawl.py              summary
    python tools/link_crawl.py --json out   also write the full table
"""
import os
import re
import sys
import json
import glob
import collections
from urllib.parse import urlparse, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = 'bayareasportsblog.com'
CHROME = re.compile(r'<(header|nav|footer)\b.*?</\1>', re.S | re.I)
HREF = re.compile(r'<a\b[^>]*\bhref="([^"#?]*)(?:[#?][^"]*)?"', re.I)


def pages():
    out = []
    for pat in ('*.html', 'articles/*.html', 'daily/*.html', 'tools/*.html', 'tools/*/index.html', '*/index.html'):
        out += [os.path.relpath(p, ROOT).replace(os.sep, '/') for p in glob.glob(os.path.join(ROOT, pat))]
    return sorted(set(p for p in out if not p.startswith(('google', 'node_modules'))))


def resolve(src, href):
    if not href or href.startswith(('mailto:', 'tel:', 'javascript:')):
        return None
    u = urlparse(href)
    if u.scheme in ('http', 'https'):
        if u.netloc.replace('www.', '') != HOST:
            return None
        path = u.path.lstrip('/')
    elif u.path.startswith('/'):
        path = unquote(u.path).lstrip('/')
    else:
        base = os.path.dirname(src)
        path = os.path.normpath(os.path.join(base, unquote(u.path))).replace(os.sep, '/')
        if path == '.':
            path = ''
    if path == '' or path.endswith('/'):
        path += 'index.html'
    return path


def main():
    all_pages = pages()
    known = set(all_pages)
    inbound = collections.defaultdict(set)
    body_in = collections.defaultdict(set)
    outlinks = {}
    broken = collections.defaultdict(set)
    for p in all_pages:
        text = open(os.path.join(ROOT, p), encoding='utf-8', errors='replace').read()
        body = CHROME.sub('', text)
        targets = set()
        for href in HREF.findall(text):
            t = resolve(p, href)
            if t is None:
                continue
            if not os.path.exists(os.path.join(ROOT, t)):
                broken[p].add(href)
                continue
            if t.endswith('.html') and t != p:
                targets.add(t)
                inbound[t].add(p)
        for href in HREF.findall(body):
            t = resolve(p, href)
            if t and t != p and os.path.exists(os.path.join(ROOT, t)):
                body_in[t].add(p)
        outlinks[p] = targets

    depth = {'index.html': 0}
    queue = ['index.html']
    while queue:
        cur = queue.pop(0)
        for t in sorted(outlinks.get(cur, ())):
            if t in known and t not in depth:
                depth[t] = depth[cur] + 1
                queue.append(t)

    sitemap = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    in_map = set(resolve('', u) for u in re.findall(r'<loc>([^<]+)</loc>', sitemap))

    rows = []
    for p in all_pages:
        rows.append({'page': p, 'in': len(inbound[p]), 'body_in': len(body_in[p]),
                     'depth': depth.get(p), 'in_sitemap': p in in_map})
    arts = [r for r in rows if r['page'].startswith('articles/')]
    print('pages %d, articles %d, sitemap urls %d' % (len(rows), len(arts), len(in_map)))
    print('sitemap urls missing on disk:', sorted(u for u in in_map if u not in known))
    print('orphans (no inbound link at all):', [r['page'] for r in rows if r['in'] == 0 and r['page'] != 'index.html'])
    print('unreachable from home:', [r['page'] for r in rows if r['depth'] is None and r['page'] not in ('404.html',)])
    print('depth distribution:', collections.Counter(r['depth'] for r in rows))
    print('articles with <=2 contextual inbound links: %d' % sum(1 for r in arts if r['body_in'] <= 2))
    print('broken internal links: %d on %d pages' % (sum(len(v) for v in broken.values()), len(broken)))
    for p, hs in sorted(broken.items())[:40]:
        print('  %s -> %s' % (p, sorted(hs)))
    if '--json' in sys.argv:
        json.dump({'rows': rows, 'broken': {k: sorted(v) for k, v in broken.items()}},
                  open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)


if __name__ == '__main__':
    main()
