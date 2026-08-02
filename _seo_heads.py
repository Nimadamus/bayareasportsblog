#!/usr/bin/env python3
"""Idempotent SEO head injection for every page on the site.

Adds, only where missing:
  - <meta name="robots" content="index,follow,max-image-preview:large,...">
  - Open Graph + Twitter card tags (derived from title / description / canonical)
  - <link rel="alternate" type="application/rss+xml"> pointing at feed.xml
  - BreadcrumbList JSON-LD on articles and hub pages
  - WebSite (+SearchAction) and Organization JSON-LD on the homepage
  - CollectionPage JSON-LD on the team / section hubs

Never writes a noindex. Run: python _seo_heads.py
"""
import os, re, glob, json

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://bayareasportsblog.com/"
SITE = "Bay Area Sports Blog"
DEFAULT_OG = BASE + "assets/img/cards/welcome-to-bay-area-sports-blog.jpg"

ROBOTS = ('<meta name="robots" content="index,follow,max-image-preview:large,'
          'max-snippet:-1,max-video-preview:-1">')
FEED = ('<link rel="alternate" type="application/rss+xml" '
        'title="Bay Area Sports Blog" href="%sfeed.xml">' % BASE)

SKIP = {'google6f74b54ecd988601.html'}

# hub page -> (breadcrumb label, og image)
HUBS = {
    'index.html':      ('Home',              None),
    '49ers.html':      ('49ers',             'assets/img/cards/49ers-dynasty-team-of-the-decade.jpg'),
    'warriors.html':   ('Warriors',          'assets/img/cards/warriors-championship-history.jpg'),
    'giants.html':     ('Giants',            'assets/img/cards/giants-dynasty-even-year-magic.jpg'),
    'athletics.html':  ("A's",               'assets/img/cards/athletics-sacramento-bay-area-villains.jpg'),
    'sharks.html':     ('Sharks',            'assets/img/cards/sharks-rebuild-has-a-pulse-celebrini.jpg'),
    'bayarea.html':    ('Bay Area Sports',   None),
    'history.html':    ('History',           'assets/img/cards/bay-area-sports-history.jpg'),
    'dynasties.html':  ('Dynasties',         None),
    'timeline.html':   ('Timeline',          None),
    'flashbacks.html': ('Flashbacks',        None),
    'columns.html':    ('Columns',           None),
    'blog.html':       ('Blog',              None),
    'stanford.html':   ('Stanford',          None),
    'cal.html':        ('Cal',               None),
    'betting.html':    ('Betting',           None),
    'about.html':      ('About',             None),
    'contact.html':    ('Contact',           None),
    'search.html':     ('Search',            None),
}


def field(pattern, html):
    m = re.search(pattern, html, re.S | re.I)
    return m.group(1).strip() if m else ''


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;'))


def unesc(s):
    for a, b in (('&amp;', '&'), ('&quot;', '"'), ('&#39;', "'"),
                 ('&middot;', '·'), ('&mdash;', '—')):
        s = s.replace(a, b)
    return s


def ldjson(obj):
    return '<script type="application/ld+json">%s</script>' % json.dumps(
        obj, ensure_ascii=False, separators=(',', ':'))


def inject(html, blocks):
    """Insert blocks immediately before </head>."""
    if not blocks:
        return html
    add = '\n'.join(blocks) + '\n'
    return re.sub(r'</head>', add + '</head>', html, count=1)


def process(path):
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    if os.path.basename(path) in SKIP:
        return None
    html = open(path, encoding='utf-8', errors='ignore').read()
    if '</head>' not in html:
        return None
    orig = html
    is_article = rel.startswith('articles/')
    is_daily = rel.startswith('daily/')
    hub = HUBS.get(rel)

    title = unesc(field(r'<title>(.*?)</title>', html)).split(' | ')[0].strip()
    desc = unesc(field(r'<meta name="description" content="(.*?)"', html))
    canon = field(r'<link rel="canonical" href="(.*?)"', html) or (BASE + rel)
    prefix = '../' if (is_article or is_daily) else ''

    blocks = []

    if 'name="robots"' not in html:
        blocks.append(ROBOTS)
    if 'application/rss+xml' not in html:
        blocks.append(FEED)

    # ---- Open Graph / Twitter -------------------------------------------
    if 'property="og:title"' not in html:
        if hub and hub[1] and os.path.exists(os.path.join(ROOT, hub[1])):
            og_img = BASE + hub[1]
        else:
            og_img = DEFAULT_OG
        ogtype = 'article' if is_article else 'website'
        blocks += [
            '<meta property="og:site_name" content="%s">' % SITE,
            '<meta property="og:locale" content="en_US">',
            '<meta property="og:type" content="%s">' % ogtype,
            '<meta property="og:title" content="%s">' % esc(title),
            '<meta property="og:description" content="%s">' % esc(desc),
            '<meta property="og:url" content="%s">' % canon,
            '<meta property="og:image" content="%s">' % og_img,
            '<meta name="twitter:card" content="summary_large_image">',
            '<meta name="twitter:title" content="%s">' % esc(title),
            '<meta name="twitter:description" content="%s">' % esc(desc),
            '<meta name="twitter:image" content="%s">' % og_img,
        ]
    elif 'og:site_name' not in html:
        blocks += ['<meta property="og:site_name" content="%s">' % SITE,
                   '<meta property="og:locale" content="en_US">']

    # ---- structured data -------------------------------------------------
    if 'BreadcrumbList' not in html:
        crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE}]
        if is_article:
            section = field(r'<span class="tag">(.*?)</span>', html) or 'Columns'
            sec_url = BASE + 'blog.html'
            for f, (label, _img) in HUBS.items():
                if label.lower().rstrip('s') in section.lower():
                    sec_url = BASE + f
                    break
            crumbs.append({"@type": "ListItem", "position": 2,
                           "name": unesc(section), "item": sec_url})
            crumbs.append({"@type": "ListItem", "position": 3,
                           "name": title, "item": canon})
        elif hub and rel != 'index.html':
            crumbs.append({"@type": "ListItem", "position": 2,
                           "name": hub[0], "item": canon})
        if len(crumbs) > 1:
            blocks.append(ldjson({"@context": "https://schema.org",
                                  "@type": "BreadcrumbList",
                                  "itemListElement": crumbs}))

    if rel == 'index.html' and '"WebSite"' not in html:
        blocks.append(ldjson({
            "@context": "https://schema.org", "@type": "WebSite",
            "name": SITE, "url": BASE,
            "description": desc,
            "inLanguage": "en-US",
            "potentialAction": {
                "@type": "SearchAction",
                "target": {"@type": "EntryPoint",
                           "urlTemplate": BASE + "search.html?q={search_term_string}"},
                "query-input": "required name=search_term_string"}}))
        blocks.append(ldjson({
            "@context": "https://schema.org", "@type": "Organization",
            "name": SITE, "url": BASE, "logo": DEFAULT_OG,
            "description": "Bay Area sports coverage of the 49ers, Warriors, "
                           "Giants, A's and Sharks, written by a fan.",
            "areaServed": "San Francisco Bay Area"}))

    if hub and rel != 'index.html' and '"CollectionPage"' not in html:
        blocks.append(ldjson({
            "@context": "https://schema.org", "@type": "CollectionPage",
            "name": title, "url": canon, "description": desc,
            "inLanguage": "en-US",
            "isPartOf": {"@type": "WebSite", "name": SITE, "url": BASE}}))

    # ---- article freshness ----------------------------------------------
    if is_article and '"dateModified"' not in html:
        m = re.search(r'("datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})")', html)
        if m:
            html = html.replace(m.group(1),
                                m.group(1) + ',"dateModified":"%s"' % m.group(2), 1)

    html = inject(html, blocks)
    if html != orig:
        open(path, 'w', encoding='utf-8', newline='').write(html)
        return rel, len(blocks)
    return None


def main():
    pages = (sorted(glob.glob(os.path.join(ROOT, '*.html'))) +
             sorted(glob.glob(os.path.join(ROOT, 'articles', '*.html'))) +
             sorted(glob.glob(os.path.join(ROOT, 'daily', '*.html'))))
    changed = [r for r in (process(p) for p in pages) if r]
    for rel, n in changed:
        print('%-72s +%d' % (rel, n))
    print('%d/%d pages updated' % (len(changed), len(pages)))


if __name__ == '__main__':
    main()
