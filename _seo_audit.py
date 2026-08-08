#!/usr/bin/env python3
"""_seo_audit.py - full local crawl + SEO health snapshot.

Reads every HTML file in the repo, builds the internal link graph and reports
the things that actually move rankings: orphans, broken links, duplicate
titles/descriptions, heading structure, schema coverage, canonical sanity,
image alt quality and per-page inbound link counts.

Writes _seo_audit.json (machine readable) and prints a summary.
Run: python _seo_audit.py [--json-only]
"""
import os, re, glob, json, sys, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://bayareasportsblog.com/"
SKIP_FILES = {'google6f74b54ecd988601.html'}
# Pages that are intentionally not part of the editorial graph
NON_EDITORIAL = {'404.html', 'search.html', 'google6f74b54ecd988601.html'}


def rd(p):
    return open(p, encoding='utf-8', errors='replace').read()


def norm(p):
    return p.replace(os.sep, '/')


def all_pages():
    top = [norm(f) for f in sorted(glob.glob(os.path.join(ROOT, '*.html')))]
    art = [norm(f) for f in sorted(glob.glob(os.path.join(ROOT, 'articles', '*.html')))]
    rel = [os.path.relpath(f, ROOT).replace(os.sep, '/') for f in top + art]
    return [f for f in rel if f not in SKIP_FILES]


TITLE = re.compile(r'<title>(.*?)</title>', re.S)
DESC = re.compile(r'<meta[^>]+name="description"[^>]+content="([^"]*)"')
CANON = re.compile(r'<link rel="canonical" href="([^"]+)"')
H1 = re.compile(r'<h1[^>]*>(.*?)</h1>', re.S)
H2 = re.compile(r'<h2[^>]*>(.*?)</h2>', re.S)
H3 = re.compile(r'<h3[^>]*>(.*?)</h3>', re.S)
HREF = re.compile(r'href="([^"#?]+)')
IMG = re.compile(r'<img\s([^>]*)>')
ATTR = re.compile(r'(\w[\w-]*)="([^"]*)"')
LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s).strip()


def resolve(src_page, href):
    """Resolve an href found on src_page to a repo-relative path, or None if external."""
    if href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:', 'data:')):
        if href.startswith(BASE):
            # absolute self-URL -> root-relative, NOT relative to the source page
            href = '/' + href[len(BASE):]
        else:
            return None
    if "'" in href or '+' in href or '{' in href:
        return None  # JS template fragment, not a real link
    if href.startswith('/'):
        # root-relative: the site is served from the domain root
        target = os.path.normpath(href.lstrip('/')).replace(os.sep, '/')
    else:
        base_dir = os.path.dirname(src_page)
        target = os.path.normpath(os.path.join(base_dir, href)).replace(os.sep, '/')
    if target in ('.', ''):
        target = 'index.html'
    if target.endswith('/'):
        target += 'index.html'
    return target


def main():
    os.chdir(ROOT)
    pages = all_pages()
    data = {}
    for p in pages:
        s = rd(p)
        t = TITLE.search(s)
        d = DESC.search(s)
        c = CANON.search(s)
        schemas = []
        bad_ld = 0
        for block in LD.findall(s):
            try:
                j = json.loads(block)
                ty = j.get('@type')
                schemas.append(ty if isinstance(ty, str) else str(ty))
            except Exception:
                bad_ld += 1
        imgs = []
        for m in IMG.finditer(s):
            a = dict(ATTR.findall(m.group(1)))
            imgs.append(a)
        data[p] = {
            'title': strip_tags(t.group(1)) if t else None,
            'desc': d.group(1) if d else None,
            'canonical': c.group(1) if c else None,
            'h1': [strip_tags(x) for x in H1.findall(s)],
            'h2': len(H2.findall(s)),
            'h3': len(H3.findall(s)),
            'schemas': schemas,
            'bad_ld': bad_ld,
            'imgs': imgs,
            'bytes': len(s.encode('utf-8')),
            'noindex': 'noindex' in s.lower(),
            'links_out': [],
            'body_links_out': [],
        }
        # separate nav/footer/related links from true in-body editorial links
        body = s
        m = re.search(r'<article[^>]*>(.*?)</article>', s, re.S)
        art_body = m.group(1) if m else ''
        for h in HREF.findall(body):
            r = resolve(p, h)
            if r:
                data[p]['links_out'].append(r)
        for h in HREF.findall(art_body):
            r = resolve(p, h)
            if r and r.startswith('articles/') or (r and r in NON_EDITORIAL) is False and r:
                data[p]['body_links_out'].append(r)

    # ---- link graph
    inbound = collections.Counter()
    body_inbound = collections.Counter()
    broken = []
    existing = set(pages) | {'google6f74b54ecd988601.html'}
    for p, v in data.items():
        for tgt in set(v['links_out']):
            if tgt in existing:
                inbound[tgt] += 1
            elif os.path.exists(os.path.join(ROOT, tgt)):
                pass  # non-HTML asset, fine
            else:
                broken.append({'from': p, 'to': tgt})
        for tgt in set(v['body_links_out']):
            if tgt in existing and tgt != p:
                body_inbound[tgt] += 1

    articles = [p for p in pages if p.startswith('articles/')]
    hubs = [p for p in pages if not p.startswith('articles/')]

    orphans = [p for p in articles if inbound[p] == 0]
    near_orphans = [p for p in articles if 0 < inbound[p] <= 2]
    no_body_inbound = [p for p in articles if body_inbound[p] == 0]

    # ---- duplicates
    by_title = collections.defaultdict(list)
    by_desc = collections.defaultdict(list)
    for p, v in data.items():
        if v['title']:
            by_title[v['title']].append(p)
        if v['desc']:
            by_desc[v['desc']].append(p)
    dup_titles = {k: v for k, v in by_title.items() if len(v) > 1}
    dup_descs = {k: v for k, v in by_desc.items() if len(v) > 1}

    # ---- head / structure problems
    multi_h1 = [p for p, v in data.items() if len(v['h1']) > 1]
    no_h1 = [p for p, v in data.items() if len(v['h1']) == 0]
    no_desc = [p for p, v in data.items() if not v['desc']]
    long_title = [p for p, v in data.items() if v['title'] and len(v['title']) > 70]
    short_desc = [p for p, v in data.items() if v['desc'] and len(v['desc']) < 70]
    long_desc = [p for p, v in data.items() if v['desc'] and len(v['desc']) > 165]
    bad_canon = []
    for p, v in data.items():
        want = BASE if p == 'index.html' else BASE + p
        if v['canonical'] != want:
            bad_canon.append({'page': p, 'has': v['canonical'], 'want': want})
    no_article_schema = [p for p in articles
                         if not any(x in ('NewsArticle', 'Article') for x in data[p]['schemas'])]
    no_breadcrumb = [p for p in pages if 'BreadcrumbList' not in data[p]['schemas']]
    invalid_ld = [p for p, v in data.items() if v['bad_ld']]
    noindexed = [p for p, v in data.items() if v['noindex']]

    # ---- images
    img_no_alt, img_weak_alt, img_no_dim, img_lazy_first = [], [], [], []
    for p, v in data.items():
        for i, a in enumerate(v['imgs']):
            alt = a.get('alt', '')
            if 'alt' not in a:
                img_no_alt.append({'page': p, 'src': a.get('src')})
            elif len(alt) < 15:
                img_weak_alt.append({'page': p, 'src': a.get('src'), 'alt': alt})
            if 'width' not in a:
                img_no_dim.append({'page': p, 'src': a.get('src')})
            if i == 0 and a.get('loading') == 'lazy':
                img_lazy_first.append(p)

    out = {
        'counts': {
            'pages': len(pages), 'articles': len(articles), 'hubs': len(hubs),
            'indexable': len(pages) - len(noindexed),
        },
        'orphans': orphans,
        'near_orphans': near_orphans,
        'articles_with_no_in_body_inbound_link': len(no_body_inbound),
        'broken_links': broken,
        'duplicate_titles': dup_titles,
        'duplicate_descriptions': dup_descs,
        'multi_h1': multi_h1, 'no_h1': no_h1, 'no_desc': no_desc,
        'title_over_70': len(long_title), 'desc_under_70': len(short_desc),
        'desc_over_165': len(long_desc),
        'canonical_mismatch': bad_canon,
        'articles_missing_article_schema': no_article_schema,
        'pages_missing_breadcrumb': no_breadcrumb,
        'invalid_jsonld': invalid_ld,
        'noindexed_pages': noindexed,
        'images_no_alt': img_no_alt, 'images_weak_alt': img_weak_alt,
        'images_no_dimensions': img_no_dim,
        'first_image_lazy': img_lazy_first,
        'inbound_counts': dict(inbound),
        'body_inbound_counts': dict(body_inbound),
    }
    json.dump(out, open('_seo_audit.json', 'w', encoding='utf-8'), indent=1)

    if '--json-only' in sys.argv:
        return
    print('pages %d  articles %d  hubs %d  indexable %d'
          % (out['counts']['pages'], out['counts']['articles'],
             out['counts']['hubs'], out['counts']['indexable']))
    print('orphans                       :', len(orphans), orphans[:5])
    print('near-orphans (<=2 inbound)    :', len(near_orphans))
    print('articles w/ 0 in-body inbound :', len(no_body_inbound))
    print('broken internal links         :', len(broken), broken[:5])
    print('duplicate titles              :', len(dup_titles))
    print('duplicate descriptions        :', len(dup_descs))
    print('multi-H1 / no-H1              :', len(multi_h1), '/', len(no_h1))
    print('canonical mismatches          :', len(bad_canon), bad_canon[:3])
    print('articles missing Article schema:', len(no_article_schema))
    print('pages missing BreadcrumbList  :', len(no_breadcrumb), no_breadcrumb[:6])
    print('invalid JSON-LD               :', len(invalid_ld))
    print('noindexed pages               :', len(noindexed))
    print('images: no alt %d / weak alt %d / no dims %d / first-img lazy %d'
          % (len(img_no_alt), len(img_weak_alt), len(img_no_dim), len(img_lazy_first)))
    print('titles >70ch %d  desc <70ch %d  desc >165ch %d'
          % (len(long_title), len(short_desc), len(long_desc)))


if __name__ == '__main__':
    main()
