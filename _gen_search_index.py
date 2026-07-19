#!/usr/bin/env python3
"""Build assets/search-index.json from every article page.
Run after adding articles: python _gen_search_index.py"""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'assets', 'search-index.json')

def field(pattern, html):
    m = re.search(pattern, html, re.S | re.I)
    return re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''

items = []
adir = os.path.join(ROOT, 'articles')
for f in sorted(os.listdir(adir)):
    if not f.endswith('.html'):
        continue
    html = open(os.path.join(adir, f), encoding='utf-8', errors='ignore').read()
    title = field(r'<title>(.*?)</title>', html).split('|')[0].strip()
    desc = field(r'<meta name="description" content="(.*?)"', html)
    tag = field(r'<span class="tag">(.*?)</span>', html) or 'Column'
    date = field(r'"datePublished"\s*:\s*"(.*?)"', html)
    items.append({'u': 'articles/' + f, 't': title, 'd': desc, 'k': tag, 'dt': date})

items.sort(key=lambda x: x['dt'], reverse=True)
with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(items, fh, ensure_ascii=False)
print(f'wrote {OUT}: {len(items)} articles')
