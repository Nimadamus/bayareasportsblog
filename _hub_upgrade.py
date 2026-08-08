#!/usr/bin/env python3
"""_hub_upgrade.py - additive upgrades to the team hubs.

1. footer: the four league hubs are added to the existing Teams column on every
   root page that has one (no new column, no new component, no copy rewritten)
2. team hero: the existing "Team Hub" kicker gains a link to that team's league
   hub, so the league hubs are reachable from the team pages
3. LCP: the first card image on a hub is no longer lazy-loaded
4. ItemList JSON-LD listing the hub's stories in display order (additive schema)

Idempotent: running it twice changes nothing.

  python _hub_upgrade.py [--check]
"""
import os, re, sys, glob, json

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://bayareasportsblog.com/"

LEAGUE_OF = {
    '49ers.html': ('nfl.html', 'Bay Area NFL'),
    'giants.html': ('mlb.html', 'Bay Area MLB'),
    'athletics.html': ('mlb.html', 'Bay Area MLB'),
    'warriors.html': ('nba.html', 'Bay Area NBA'),
    'sharks.html': ('nhl.html', 'Bay Area NHL'),
}
LEAGUE_LINKS = ('        <a href="nfl.html">NFL</a>\n'
                '        <a href="mlb.html">MLB</a>\n'
                '        <a href="nba.html">NBA</a>\n'
                '        <a href="nhl.html">NHL</a>\n')
SHARKS_LINK = '        <a href="sharks.html">Sharks</a>\n'

HUBS = ['index.html', '49ers.html', 'giants.html', 'athletics.html',
        'warriors.html', 'sharks.html', 'bayarea.html', 'stanford.html',
        'cal.html', 'blog.html', 'columns.html', 'history.html',
        'dynasties.html', 'flashbacks.html', 'betting.html', 'timeline.html']

CARD_RE = re.compile(r'<a\b[^>]*\bhref="(articles/[^"]+\.html)"[^>]*>.*?</a>', re.S)
H1_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.S)


def rd(p):
    return open(p, encoding='utf-8', errors='replace').read()


def wr(p, s):
    with open(p, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)
    if b'\x00' in open(p, 'rb').read():
        raise SystemExit('NULL-byte corruption writing %s - ABORT' % p)


def add_footer_leagues(s):
    if '<a href="nfl.html">NFL</a>' in s or SHARKS_LINK not in s:
        return s
    return s.replace(SHARKS_LINK, SHARKS_LINK + LEAGUE_LINKS, 1)


def add_hero_league(s, page):
    if page not in LEAGUE_OF:
        return s
    href, name = LEAGUE_OF[page]
    old = '<div class="sh-k">Team Hub</div>'
    if old not in s:
        return s
    new = ('<div class="sh-k">Team Hub &middot; <a href="%s">%s</a></div>'
           % (href, name))
    return s.replace(old, new, 1)


def unlazy_first_image(s):
    m = re.search(r'<img\s[^>]*>', s)
    if not m:
        return s
    tag = m.group(0)
    if 'fetchpriority="high"' in tag and 'loading="lazy"' not in tag:
        return s
    new = re.sub(r'\s+loading="[^"]*"', '', tag)
    new = re.sub(r'\s+fetchpriority="[^"]*"', '', new)
    new = new[:-1].rstrip() + ' fetchpriority="high">'
    return s[:m.start()] + new + s[m.end():]


def add_itemlist(s, page):
    if '"@type":"ItemList"' in s or '"@type": "ItemList"' in s:
        return s
    hrefs, seen = [], set()
    for m in CARD_RE.finditer(s):
        h = m.group(1)
        if h not in seen:
            seen.add(h)
            hrefs.append(h)
    if len(hrefs) < 3:
        return s
    items = []
    for i, h in enumerate(hrefs, 1):
        p = os.path.join(ROOT, h)
        name = ''
        if os.path.exists(p):
            m = H1_RE.search(rd(p))
            if m:
                name = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(1))).strip()
        it = {"@type": "ListItem", "position": i, "url": BASE + h}
        if name:
            it["name"] = name
        items.append(it)
    node = {"@context": "https://schema.org", "@type": "ItemList",
            "itemListOrder": "https://schema.org/ItemListOrderDescending",
            "numberOfItems": len(items), "itemListElement": items}
    tag = ('<script type="application/ld+json">%s</script>\n'
           % json.dumps(node, separators=(',', ':'), ensure_ascii=False))
    return s.replace('</head>', tag + '</head>', 1)


def main():
    check = '--check' in sys.argv
    pages = [p for p in HUBS if os.path.exists(os.path.join(ROOT, p))]
    pages += [p for p in ('nfl.html', 'mlb.html', 'nba.html', 'nhl.html')
              if os.path.exists(os.path.join(ROOT, p))]
    # every root page carrying the shared footer, so the league links are sitewide
    pages += [os.path.basename(f) for f in glob.glob(os.path.join(ROOT, '*.html'))
              if os.path.basename(f) not in pages]

    for page in pages:
        p = os.path.join(ROOT, page)
        s0 = rd(p)
        s = add_footer_leagues(s0)
        s = add_hero_league(s, page)
        if page in HUBS or page in ('nfl.html', 'mlb.html', 'nba.html', 'nhl.html'):
            if 'class="mag"' in s:
                s = unlazy_first_image(s)
                s = add_itemlist(s, page)
        if s == s0:
            continue
        what = []
        if 'nfl.html">NFL' in s and 'nfl.html">NFL' not in s0:
            what.append('footer-leagues')
        if 'sh-k">Team Hub &middot;' in s and 'sh-k">Team Hub &middot;' not in s0:
            what.append('hero-league')
        if 'ItemList' in s and 'ItemList' not in s0:
            what.append('itemlist')
        if 'fetchpriority' in s and s.count('fetchpriority') > s0.count('fetchpriority'):
            what.append('lcp')
        print('%-18s %s' % (page, ' '.join(what) or 'changed'))
        if not check:
            wr(p, s)


if __name__ == '__main__':
    main()
