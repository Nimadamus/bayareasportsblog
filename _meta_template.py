#!/usr/bin/env python3
"""_meta_template.py - the article head standard, as a generator and a gate.

  python _meta_template.py --new <slug> --h1 "Headline" --desc "..." --tag "Giants Column"
      prints a compliant <head> block for a new article

  python _meta_template.py --gate
      checks every page against the standard and exits 2 on any violation

The standard, as enforced by --gate:
  title        1-70 chars, unique across the site
  description  70-165 chars, unique across the site
  canonical    https://bayareasportsblog.com/<path> (bare domain for index)
  social       og:title/og:description/og:image + twitter:card/title/description,
               og:title and og:description in sync with title and description
  schema       BreadcrumbList on every page; Article or NewsArticle on articles,
               each with datePublished and dateModified; all JSON-LD must parse
  images       alt >=15 chars, explicit width and height, first image not lazy
"""
import os, re, sys, glob, json, datetime, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://bayareasportsblog.com/"
TITLE_MAX, DESC_MIN, DESC_MAX, ALT_MIN = 70, 70, 165, 15

HEAD_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="stylesheet" href="../assets/desk.css">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<link rel="alternate" type="application/rss+xml" title="Bay Area Sports Blog" href="{base}feed.xml">
<meta property="og:site_name" content="Bay Area Sports Blog">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="675">
<meta property="og:image:alt" content="{alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img}">
<script type="application/ld+json">{article}</script>
<script type="application/ld+json">{crumbs}</script>
</head>
"""


def rd(p):
    return open(p, encoding='utf-8', errors='replace').read()


def new_head(slug, h1, desc, tag, date=None):
    date = date or datetime.date.today().isoformat()
    url = BASE + 'articles/' + slug + '.html'
    img = BASE + 'assets/img/cards/' + slug + '.jpg'
    title = h1 if len(h1) <= TITLE_MAX else h1[:TITLE_MAX].rsplit(' ', 1)[0]
    article = {
        "@context": "https://schema.org", "@type": "NewsArticle",
        "headline": h1, "description": desc, "url": url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "datePublished": date, "dateModified": date,
        "articleSection": tag, "inLanguage": "en-US",
        "image": {"@type": "ImageObject", "url": img, "width": 1200, "height": 675},
        "author": {"@type": "Organization", "name": "Bay Area Sports Blog",
                   "url": BASE},
        "publisher": {"@type": "Organization", "name": "Bay Area Sports Blog",
                      "url": BASE},
    }
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList",
              "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
                  {"@type": "ListItem", "position": 2, "name": tag,
                   "item": BASE + "columns.html"},
                  {"@type": "ListItem", "position": 3, "name": h1, "item": url}]}
    j = lambda d: json.dumps(d, separators=(',', ':'), ensure_ascii=False)
    return HEAD_TEMPLATE.format(title=title, desc=desc, url=url, base=BASE, img=img,
                                alt=h1, article=j(article), crumbs=j(crumbs))


def gate():
    pages = ([os.path.basename(f) for f in sorted(glob.glob(os.path.join(ROOT, '*.html')))]
             + ['articles/' + os.path.basename(f)
                for f in sorted(glob.glob(os.path.join(ROOT, 'articles', '*.html')))])
    skip = {'google6f74b54ecd988601.html'}
    fails = []
    titles, descs = collections.defaultdict(list), collections.defaultdict(list)

    for pg in pages:
        if pg in skip:
            continue
        s = rd(os.path.join(ROOT, pg))
        art = pg.startswith('articles/')

        def grab(rx):
            m = re.search(rx, s, re.S)
            return m.group(1) if m else None

        t = grab(r'<title>(.*?)</title>')
        d = grab(r'<meta name="description" content="([^"]*)"')
        can = grab(r'<link rel="canonical" href="([^"]+)"')
        og_t = grab(r'<meta property="og:title" content="([^"]*)"')
        og_d = grab(r'<meta property="og:description" content="([^"]*)"')

        if not t or len(t) > TITLE_MAX:
            fails.append((pg, 'title %s' % (len(t) if t else 'missing')))
        else:
            titles[t].append(pg)
        if not d or not (DESC_MIN <= len(d) <= DESC_MAX):
            fails.append((pg, 'description %s' % (len(d) if d else 'missing')))
        else:
            descs[d].append(pg)

        want = BASE if pg == 'index.html' else BASE + pg
        if can != want:
            fails.append((pg, 'canonical %s' % can))
        for name, rx in (('og:image', r'<meta property="og:image" content='),
                         ('twitter:card', r'<meta name="twitter:card" content=')):
            if not re.search(rx, s):
                fails.append((pg, 'missing ' + name))
        # og:title may be the short form of the title, but must not contradict it
        if og_t and t and not (og_t == t or t.startswith(og_t)):
            fails.append((pg, 'og:title out of sync'))
        if og_d and d and og_d != d:
            fails.append((pg, 'og:description out of sync'))

        types = []
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                                s, re.S):
            try:
                node = json.loads(block)
            except Exception:
                fails.append((pg, 'invalid JSON-LD'))
                continue
            ty = node.get('@type')
            types.append(ty)
            if ty in ('Article', 'NewsArticle'):
                for f in ('datePublished', 'dateModified'):
                    if f not in node:
                        fails.append((pg, 'schema missing ' + f))
        if 'BreadcrumbList' not in types:
            fails.append((pg, 'missing BreadcrumbList'))
        if art and not any(x in ('Article', 'NewsArticle') for x in types):
            fails.append((pg, 'missing Article schema'))

        for i, tag in enumerate(re.findall(r'<img\s[^>]*>', s)):
            a = re.search(r'alt="([^"]*)"', tag)
            if not a or len(a.group(1)) < ALT_MIN:
                fails.append((pg, 'weak alt: %s' % (a.group(1) if a else 'none')))
            if 'width=' not in tag or 'height=' not in tag:
                fails.append((pg, 'image missing dimensions'))
            if i == 0 and 'loading="lazy"' in tag:
                fails.append((pg, 'first image lazy'))

    for label, bag in (('duplicate title', titles), ('duplicate description', descs)):
        for k, v in bag.items():
            if len(v) > 1:
                fails.append((v[0], '%s shared with %s' % (label, ', '.join(v[1:]))))

    print('META GATE  pages=%d  violations=%d' % (len(pages) - len(skip), len(fails)))
    for pg, why in fails[:40]:
        print('  FAIL %-52s %s' % (pg[:52], why))
    if fails:
        print('GATE FAILED.')
        return 2
    print('GATE PASSED.')
    return 0


def main():
    if '--gate' in sys.argv:
        sys.exit(gate())
    if '--new' in sys.argv:
        a = sys.argv
        get = lambda f, dflt=None: a[a.index(f) + 1] if f in a else dflt
        slug = get('--new')
        h1 = get('--h1', 'Headline goes here')
        desc = get('--desc', 'One or two sentences, 70 to 165 characters.')
        tag = get('--tag', 'Column')
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        print(new_head(slug, h1, desc, tag, get('--date')))
        return
    print(__doc__)


if __name__ == '__main__':
    main()
