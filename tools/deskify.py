#!/usr/bin/env python3
"""deskify.py - move a root page from the legacy style.css shell onto The Desk (desk.css).

Rewrites, in place and idempotently:
  <link> style.css -> desk.css
  <header class="site-header"> ... </header>   -> desk-top + masthead + teamnav
  <section class="page-hero">                  -> <section class="sec-hero">
  card lists (.post | .ncard | .mini)          -> .mag grid of .st with varied spans
  <footer class="site-footer"> ... </footer>   -> desk-foot

Content is never invented or dropped: every href, img, alt, headline and dek is carried
across verbatim. Only the wrapper markup changes.
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# page -> (teamnav key, hero accent, monogram)
TEAM = {
    '49ers.html':     ('niners', 'var(--niners)', '49'),
    'warriors.html':  ('gs',     'var(--gs)',     'GS'),
    'giants.html':    ('sf',     'var(--sf)',     'SF'),
    'athletics.html': ('as',     'var(--as)',     'A'),
    'sharks.html':    ('sj',     'var(--sj)',     'SJ'),
    'bayarea.html':   ('lv',     'var(--bay)',    'BA'),
}
NAVKEY = {'blog.html': 'house', 'columns.html': 'house', 'flashbacks.html': 'house'}

# category text -> pill colour class
PILL = [('49er', 'niners'), ('warrior', 'gs'), ('giant', 'sf'), ("a's", 'as'),
        ('athletic', 'as'), ('shark', 'sj'), ('raider', 'lv')]


def pill_for(cat, fallback=''):
    c = cat.lower()
    for k, v in PILL:
        if k in c:
            return v
    return fallback   # e.g. "Bay Area Villains" on the A's page is still an A's card


def masthead(page):
    nav = TEAM.get(page, (NAVKEY.get(page, 'house'),))[0]
    items = [('house', 'index.html', 'Home'), ('niners', '49ers.html', '49ers'),
             ('gs', 'warriors.html', 'Warriors'), ('sf', 'giants.html', 'Giants'),
             ('as', 'athletics.html', "A's"), ('sj', 'sharks.html', 'Sharks'),
             ('lv', 'bayarea.html', 'Bay Area')]
    tail = [('house', 'history.html', 'History'), ('house', 'dynasties.html', 'Dynasties'),
            ('house', 'timeline.html', 'Timeline'), ('house', 'blog.html', 'Blog')]

    def link(t, h, l):
        on = ' class="on"' if (h == page) else ''
        return '        <a%s data-t="%s" href="%s">%s</a>' % (on, t, h, l)
    L = [link(*i) for i in items] + ['        <span class="nv-sp"></span>'] + [link(*i) for i in tail]
    return '''<div class="desk-top">
  <div class="wrap">
    <div><b>Tuesday, July 14, 2026</b> &middot; San Francisco</div>
    <div class="dt-r">
      <a href="blog.html">Latest</a>
      <a href="columns.html">Columns</a>
      <a href="timeline.html">Timeline</a>
      <a href="about.html">About</a>
    </div>
  </div>
</div>

<header class="masthead">
  <div class="wrap">
    <div class="mh-rule">
      <em>Est. by a fan, not a network</em>
      <span></span>
      <em>No wire copy. No neutrality.</em>
    </div>
    <a class="wordmark" href="index.html">Bay Area<br><i>Sports Blog</i></a>
  </div>
</header>

<nav class="teamnav">
  <div class="wrap">
%s
  </div>
</nav>''' % ('\n'.join(L))


FOOTER = '''<footer class="desk-foot">
  <div class="wrap">
    <div class="df-top">
      <div>
        <div class="wm">Bay Area <i>Sports Blog</i></div>
        <p>Written by a fan who actually watches the games. No wire copy, no neutrality, no pretending the A's move was fine.</p>
      </div>
      <div class="df-col">
        <h5>Teams</h5>
        <a href="49ers.html">49ers</a>
        <a href="warriors.html">Warriors</a>
        <a href="giants.html">Giants</a>
        <a href="athletics.html">Athletics</a>
        <a href="sharks.html">Sharks</a>
      </div>
      <div class="df-col">
        <h5>Read</h5>
        <a href="blog.html">Latest Stories</a>
        <a href="columns.html">Columns</a>
        <a href="flashbacks.html">Flashbacks</a>
        <a href="dynasties.html">Dynasties</a>
        <a href="betting.html">Betting</a>
      </div>
      <div class="df-col">
        <h5>The Vault</h5>
        <a href="history.html">Bay Area History</a>
        <a href="timeline.html">Timeline</a>
        <a href="bayarea.html">Bay Area Hub</a>
        <a href="stanford.html">Stanford</a>
        <a href="cal.html">Cal</a>
      </div>
    </div>
    <div class="df-bot">
      <div>&copy; 2026 Bay Area Sports Blog. All rights reserved.</div>
      <div><a href="about.html">About</a> &middot; <a href="contact.html">Contact</a> &middot; <a href="daily/index.html">Daily</a></div>
    </div>
  </div>
</footer>'''


def spans(n):
    """Asymmetric rhythm that always fills a 6-column row, so no ragged holes."""
    ROWS = [(3, 3), (2, 2, 2), ('S4', 2), (2, 2, 2), (3, 3), (2, 2, 2)]
    out, i = [], 0
    while len(out) < n:
        left = n - len(out)
        row = ROWS[i % len(ROWS)]
        i += 1
        if sum(4 if r == 'S4' else r for r in row) > left * 3:
            pass
        if left <= 3:                       # tail row: fill it exactly
            out += {1: ['6'], 2: ['3', '3'], 3: ['2', '2', '2']}[left]
            break
        out += ['4 split' if r == 'S4' else str(r) for r in row]
    return out[:n]


# One precise pattern per dialect keeps the capture groups honest. Every literal gap is
# \s* because these pages mix compact and pretty-printed markup for the same dialect.
DIALECTS = [
    # .post  -> media/body/cat/h3/p/span.rd
    re.compile(r'<a class="post" href="([^"]+)">\s*'
               r'<div class="post-media">\s*<img src="([^"]+)" alt="([^"]*)">\s*</div>\s*'
               r'<div class="post-body">\s*<div class="post-cat">(.*?)</div>\s*'
               r'<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*'
               r'(?:<span class="rd">(.*?)</span>)?\s*</div>\s*</a>', re.S),
    # .ncard -> n-media/n-body/span.catpill/h3/p
    re.compile(r'<a class="ncard" href="([^"]+)">\s*<div class="n-media">\s*<img src="([^"]+)" alt="([^"]*)">\s*</div>\s*'
               r'<div class="n-body">\s*<span class="catpill[^"]*">(.*?)</span>\s*'
               r'<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*()</div>\s*</a>', re.S),
    # .mini  -> m-media/m-body/m-cat/h3/p
    re.compile(r'<a class="mini" href="([^"]+)">\s*'
               r'<div class="m-media">\s*<img src="([^"]+)" alt="([^"]*)">\s*</div>\s*'
               r'<div class="m-body">\s*<div class="m-cat">(.*?)</div>\s*'
               r'<h3>(.*?)</h3>\s*(?:<p>(.*?)</p>)?\s*()</div>\s*</a>', re.S),
]


def build_cards(html, fallback=''):
    """Return (n_found, replacement_fn_applied_html). Converts every card dialect."""
    found = []
    for rx in DIALECTS:
        for m in rx.finditer(html):
            found.append(m)
    if not found:
        return 0, html
    found.sort(key=lambda m: m.start())
    sp = spans(len(found))
    out, cur = [], 0
    for idx, m in enumerate(found):
        href, src, alt, cat, h3, dek, rd = (m.group(1), m.group(2), m.group(3),
                                            m.group(4), m.group(5), m.group(6) or '',
                                            (m.group(7) or '').strip())
        cat = re.sub(r'\s*&middot;\s*', ' ', cat).strip()
        rd = re.sub(r'\s*&rarr;\s*$', '', rd).strip() or 'Read'
        cls = pill_for(cat, fallback)
        card = ('<a class="st w%s" href="%s">\n'
                '  <div class="st-img"><img src="%s" alt="%s"></div>\n'
                '  <div class="st-b">\n'
                '    <div><span class="pill %s">%s</span></div>\n'
                '    <h3>%s</h3>\n'
                '    <p>%s</p>\n'
                '    <div class="st-f">%s</div>\n'
                '  </div>\n'
                '</a>') % (sp[idx], href, src, alt, cls, cat, h3, dek, rd)
        out.append(html[cur:m.start()])
        out.append(card)
        cur = m.end()
    out.append(html[cur:])
    return len(found), ''.join(out)


def deskify(path):
    page = os.path.basename(path)
    html = open(path, encoding='utf-8').read()
    fb = TEAM.get(page, ('',))[0]
    fb = fb if fb in ('niners', 'gs', 'sf', 'as', 'sj') else ''

    if 'assets/desk.css' in html:
        # already on the shell: only sweep up card dialects an earlier pass missed
        n, html2 = build_cards(html, fb)
        if n:
            open(path, 'w', encoding='utf-8').write(html2)
        return page, 'swept', n

    html = html.replace('assets/style.css', 'assets/desk.css')
    html = re.sub(r'<header class="site-header">.*?</header>', lambda m: masthead(page), html, flags=re.S)
    html = re.sub(r'<footer class="site-footer">.*?</footer>', lambda m: FOOTER, html, flags=re.S)

    # page hero -> sec-hero (carry the team accent + add a ghost monogram)
    key, accent, mono = TEAM.get(page, ('house', 'var(--bay)', ''))

    def hero(m):
        body = m.group(1)
        tag = re.search(r'<span class="tag">(.*?)</span>', body, re.S)
        h1 = re.search(r'<h1>(.*?)</h1>', body, re.S)
        # the legacy tag is usually the same word as the h1 ("Giants" / "Giants") --
        # printing it twice reads as a bug, so drop it rather than echo the headline
        if tag and h1 and tag.group(1).strip().lower() == h1.group(1).strip().lower():
            body = body.replace(tag.group(0), '<div class="sh-k">Team Hub</div>', 1)
        else:
            body = body.replace('<span class="tag">', '<div class="sh-k">', 1)
            body = body.replace('</span>', '</div>', 1)
        mo = ('<span class="hero-mono">%s</span>' % mono) if mono else ''
        return ('<section class="sec-hero" style="--th:%s"><div class="wrap">%s%s</div></section>'
                % (accent, body, mo))
    html = re.sub(r'<section class="page-hero"[^>]*><div class="wrap">(.*?)</div></section>',
                  hero, html, flags=re.S)

    n, html = build_cards(html, fb)

    # containers
    html = html.replace('<div class="postlist">', '<div class="mag">')
    html = html.replace('<div class="mini-grid">', '<div class="mag">')
    html = html.replace('<div class="news-grid">', '<div class="mag">')
    html = re.sub(r'<section class="section"><div class="wrap">', '<section class="zone"><div class="wrap">', html)
    html = re.sub(r'<section class="zone plain"><div class="wrap">', '<section class="zone"><div class="wrap">', html)
    html = re.sub(r'<div class="section-head"><h2>(.*?)</h2></div>',
                  r'<div class="sec-head"><div><h2>\1</h2></div><a class="sh-all" href="blog.html">All stories</a></div>',
                  html)
    open(path, 'w', encoding='utf-8').write(html)
    return page, 'ok', n


if __name__ == '__main__':
    targets = sys.argv[1:] or ['49ers.html', 'warriors.html', 'giants.html', 'athletics.html',
                               'sharks.html', 'flashbacks.html', 'blog.html', 'columns.html',
                               'bayarea.html']
    for t in targets:
        p = os.path.join(ROOT, t)
        if not os.path.exists(p):
            print('  MISSING', t); continue
        print('  %-18s %-8s cards=%d' % deskify(p))
