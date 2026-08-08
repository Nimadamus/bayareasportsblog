#!/usr/bin/env python3
"""_gen_sport_hubs.py - build the league hubs (nfl / mlb / nba / nhl).

A league hub is the team-hub template with the same masthead, nav, hero, card
grid and footer; the only difference is that its stories are grouped under a
per-team <h2> using the existing sec-head style. Card markup is reused verbatim
from the team hubs, so alt text, dimensions and the thumbnail gate all carry
over unchanged.

  python _gen_sport_hubs.py            # write nfl.html, mlb.html, nba.html, nhl.html
  python _gen_sport_hubs.py --check    # report what would change, write nothing
"""
import os, re, sys, glob, json, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://bayareasportsblog.com/"
TEMPLATE = '49ers.html'

# league -> hero copy, theme, and the team sections in display order
SPORTS = {
    'nfl': {
        'name': 'NFL',
        'h1': 'Bay Area NFL',
        'title': 'Bay Area NFL | 49ers Coverage | Bay Area Sports Blog',
        'desc': "San Francisco 49ers coverage from Bay Area Sports Blog: camp, "
                "injuries, roster moves, Purdy, and every Sunday storyline.",
        'mono': 'NFL', 'theme': 'niners',
        'teams': [('49ers', '49ers.html')],
    },
    'mlb': {
        'name': 'MLB',
        'h1': 'Bay Area MLB',
        'title': "Bay Area MLB | Giants and A's Coverage | Bay Area Sports Blog",
        'desc': "San Francisco Giants and Athletics coverage from Bay Area Sports "
                "Blog: every game, the trade deadline, and where both teams are going.",
        'mono': 'MLB', 'theme': 'sf',
        'teams': [('Giants', 'giants.html'), ("Athletics", 'athletics.html')],
    },
    'nba': {
        'name': 'NBA',
        'h1': 'Bay Area NBA',
        'title': 'Bay Area NBA | Warriors Coverage | Bay Area Sports Blog',
        'desc': "Golden State Warriors coverage from Bay Area Sports Blog: the "
                "roster, the rotation, and what this era has left.",
        'mono': 'NBA', 'theme': 'gs',
        'teams': [('Warriors', 'warriors.html')],
    },
    'nhl': {
        'name': 'NHL',
        'h1': 'Bay Area NHL',
        'title': 'Bay Area NHL | Sharks Coverage | Bay Area Sports Blog',
        'desc': "San Jose Sharks coverage from Bay Area Sports Blog: the rebuild, "
                "the young core, and the road back to relevance.",
        'mono': 'NHL', 'theme': 'sj',
        'teams': [('Sharks', 'sharks.html')],
    },
}

CARD_SOURCES = ['49ers.html', 'giants.html', 'athletics.html', 'warriors.html',
                'sharks.html', 'bayarea.html', 'blog.html', 'index.html',
                'columns.html', 'history.html', 'dynasties.html',
                'flashbacks.html', 'timeline.html']

CARD_RE = re.compile(r'<a\b[^>]*\bhref="(articles/[^"]+\.html)"[^>]*>.*?</a>', re.S)
PUB_RE = re.compile(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})')


def rd(p):
    return open(os.path.join(ROOT, p), encoding='utf-8', errors='replace').read()


def card_index():
    """href -> card anchor HTML, taken from the first source page that has it."""
    out = {}
    for pg in CARD_SOURCES:
        if not os.path.exists(os.path.join(ROOT, pg)):
            continue
        s = rd(pg)
        for m in CARD_RE.finditer(s):
            href, block = m.group(1), m.group(0)
            if '<img' in block and href not in out:
                out[href] = block
    return out


def hub_members(hub):
    """Articles the team hub itself links, i.e. the editor's own membership."""
    s = rd(hub)
    seen, order = set(), []
    for m in CARD_RE.finditer(s):
        h = m.group(1)
        if h not in seen:
            seen.add(h)
            order.append(h)
    return order


def published(href):
    p = os.path.join(ROOT, href)
    if not os.path.exists(p):
        return '0000-00-00'
    m = PUB_RE.search(rd(href))
    return m.group(1) if m else '0000-00-00'


def first_image_priority(html, first):
    """The first image on a page must not be lazy; everything below it must be."""
    def fix(m):
        tag = m.group(0)
        tag = re.sub(r'\s+loading="[^"]*"', '', tag)
        tag = re.sub(r'\s+fetchpriority="[^"]*"', '', tag)
        add = ' fetchpriority="high"' if first else ' loading="lazy"'
        return tag[:-1].rstrip() + add + '>'
    return re.sub(r'<img\s[^>]*>', fix, html, count=1)


def build_head(slug, cfg, og_image):
    url = BASE + slug + '.html'
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList",
              "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
                  {"@type": "ListItem", "position": 2, "name": cfg['h1'], "item": url}]}
    coll = {"@context": "https://schema.org", "@type": "CollectionPage",
            "name": cfg['h1'], "url": url, "description": cfg['desc'],
            "inLanguage": "en-US",
            "isPartOf": {"@type": "WebSite", "name": "Bay Area Sports Blog",
                         "url": BASE}}
    j = lambda d: json.dumps(d, separators=(',', ':'))
    return """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(url)s">
<link rel="stylesheet" href="assets/desk.css">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<link rel="alternate" type="application/rss+xml" title="Bay Area Sports Blog" href="%(base)sfeed.xml">
<meta property="og:site_name" content="Bay Area Sports Blog">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="website">
<meta property="og:title" content="%(h1)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s">
<meta property="og:image" content="%(img)s">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(h1)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="%(img)s">
<script type="application/ld+json">%(crumbs)s</script>
<script type="application/ld+json">%(coll)s</script>
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="675">
<meta property="og:image:alt" content="Bay Area Sports Blog: %(h1)s">
</head>
""" % {'title': cfg['title'], 'desc': cfg['desc'], 'url': url, 'base': BASE,
       'h1': cfg['h1'], 'img': og_image, 'crumbs': j(crumbs), 'coll': j(coll)}


def main():
    check = '--check' in sys.argv
    tpl = rd(TEMPLATE)
    cards = card_index()

    # chrome lifted verbatim from the team-hub template
    chrome_start = tpl.index('<body>')
    nav_end = tpl.index('</nav>') + len('</nav>')
    chrome = tpl[chrome_start:nav_end]
    chrome = chrome.replace(' class="on"', '')          # no team is current
    foot = tpl[tpl.index('<footer class="desk-foot">'):]

    wrote = []
    for slug, cfg in SPORTS.items():
        sections, total, og = [], 0, None
        for team, hub in cfg['teams']:
            hrefs = [h for h in hub_members(hub) if h in cards]
            hrefs.sort(key=published, reverse=True)
            if not hrefs:
                continue
            blocks = []
            for h in hrefs:
                b = cards[h]
                blocks.append(first_image_priority(b, first=(total == 0 and not blocks)))
                if og is None:
                    m = re.search(r'src="(assets/img/cards/[^"]+)"', b)
                    og = BASE + m.group(1) if m else None
            total += len(hrefs)
            sections.append(
                '<section class="zone"><div class="wrap">\n'
                '<div class="sec-head"><div><h2>%s</h2></div>'
                '<a class="sh-all" href="%s">%s hub</a></div>\n'
                '<div class="mag">\n%s\n</div>\n</div></section>'
                % (team, hub, team, '\n'.join(blocks)))
        if not sections:
            print('SKIP %s - no cards' % slug)
            continue

        hero = ('<section class="sec-hero" style="--th:var(--%s)"><div class="wrap">\n'
                '<div class="sh-k">League Hub</div>\n<h1>%s</h1>\n<p>%s</p>\n'
                '<span class="hero-mono">%s</span></div></section>'
                % (cfg['theme'], cfg['h1'], cfg['desc'], cfg['mono']))

        html = (build_head(slug, cfg, og or (BASE + 'assets/img/cards/'
                                             '49ers-dynasty-team-of-the-decade.jpg'))
                + chrome + '\n' + hero + '\n' + '\n'.join(sections) + '\n\n' + foot)

        out = os.path.join(ROOT, slug + '.html')
        old = open(out, encoding='utf-8', errors='replace').read() if os.path.exists(out) else ''
        if check:
            print('%-8s %3d stories  %s' % (slug, total,
                                            'unchanged' if old == html else 'WOULD WRITE'))
            continue
        with open(out, 'w', encoding='utf-8', newline='') as fh:
            fh.write(html)
        if b'\x00' in open(out, 'rb').read():
            raise SystemExit('NULL-byte corruption writing %s - ABORT' % out)
        wrote.append((slug, total))

    for slug, total in wrote:
        print('wrote %-9s %3d stories' % (slug + '.html', total))


if __name__ == '__main__':
    main()
