#!/usr/bin/env python3
"""schema_validate.py: check the JSON-LD on every page against what the markup promises.

Not a substitute for Google's Rich Results test, which needs their service. This catches
the things that actually go wrong on this site: a type that disagrees with
schema_types.json, a headline that has drifted from the H1, a canonical that disagrees
with mainEntityOfPage, a missing date, a second Article node sneaking in, and a
BreadcrumbList whose positions do not run 1..n.

    python tools/schema_validate.py           every article
    python tools/schema_validate.py <slug>    one page
"""
import os
import re
import sys
import json
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = 'https://bayareasportsblog.com/'
LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
ARTICLE_TYPES = ('Article', 'NewsArticle', 'BlogPosting', 'ReportageNewsArticle')
REQUIRED = ('headline', 'image', 'author', 'publisher', 'datePublished',
            'dateModified', 'mainEntityOfPage', 'description')

decl = {}
default_type = 'NewsArticle'
if os.path.exists('schema_types.json'):
    d = json.load(open('schema_types.json', encoding='utf-8'))
    decl, default_type = d.get('types', {}), d.get('_default', 'NewsArticle')

targets = [a for a in sys.argv[1:] if not a.startswith('--')] or [os.path.basename(p)[:-5] for p in sorted(glob.glob('articles/*.html'))]
problems = []      # things that are wrong
warnings = []      # things Google only advises on, or house style drift
counts = {}

for slug in targets:
    path = 'articles/%s.html' % slug
    if not os.path.exists(path):
        problems.append((slug, 'file not found'))
        continue
    html = open(path, encoding='utf-8').read()
    nodes = []
    for block in LD.findall(html):
        try:
            nodes.append(json.loads(block))
        except ValueError as exc:
            problems.append((slug, 'JSON-LD does not parse: %s' % exc))
    arts = [n for n in nodes if n.get('@type') in ARTICLE_TYPES]
    if len(arts) != 1:
        problems.append((slug, 'expected exactly one article node, found %d' % len(arts)))
        continue
    node = arts[0]
    counts[node['@type']] = counts.get(node['@type'], 0) + 1

    want = decl.get(slug, default_type)
    if node['@type'] != want:
        problems.append((slug, 'type is %s, schema_types.json says %s' % (node['@type'], want)))

    for field in REQUIRED:
        if not node.get(field):
            problems.append((slug, 'missing %s' % field))

    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    if h1:
        h1_text = re.sub(r'<[^>]+>', '', h1.group(1)).strip()
        if node.get('headline', '').strip() != h1_text:
            warnings.append((slug, 'headline has drifted from the H1'))
    if len(node.get('headline', '')) > 110:
        warnings.append((slug, 'headline is %d chars, over the 110 guidance' % len(node['headline'])))

    canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    meid = node.get('mainEntityOfPage')
    meid = meid.get('@id') if isinstance(meid, dict) else meid
    if canon and meid and canon.group(1) != meid:
        problems.append((slug, 'mainEntityOfPage disagrees with the canonical'))
    if canon and canon.group(1) != BASE + path.replace('\\', '/'):
        problems.append((slug, 'canonical is not this page'))

    for key in ('datePublished', 'dateModified'):
        if node.get(key) and not re.fullmatch(r'\d{4}-\d{2}-\d{2}', node[key]):
            problems.append((slug, '%s is not an ISO date' % key))
    if node.get('dateModified', '') < node.get('datePublished', ''):
        problems.append((slug, 'dateModified is before datePublished'))

    for extra in ('author', 'publisher'):
        val = node.get(extra)
        if not (val.get('name') if isinstance(val, dict) else val):
            problems.append((slug, '%s has no name' % extra))

    crumbs = [n for n in nodes if n.get('@type') == 'BreadcrumbList']
    for c in crumbs:
        items = c.get('itemListElement', [])
        if [i.get('position') for i in items] != list(range(1, len(items) + 1)):
            problems.append((slug, 'breadcrumb positions do not run 1..n'))
        title = re.search(r'<title>(.*?)</title>', html, re.S)
        allowed = {re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else '',
                   title.group(1).strip() if title else '',
                   node.get('headline', '').strip()}
        if items and items[-1].get('name') and items[-1]['name'].strip() not in allowed:
            warnings.append((slug, 'last breadcrumb matches neither the H1, the title nor the headline'))

print('SCHEMA VALIDATE  pages=%d  types=%s  errors=%d  warnings=%d'
      % (len(targets), counts, len(problems), len(warnings)))
for slug, msg in problems[:40]:
    print('  ERROR %-56s %s' % (slug[:56], msg))
if '--warnings' in sys.argv or not problems:
    for slug, msg in warnings[:40]:
        print('  warn  %-56s %s' % (slug[:56], msg))
sys.exit(2 if problems else 0)
