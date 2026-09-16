#!/usr/bin/env python3
"""_gen_discovery.py: the single owner of internal discovery wiring.

Publishing an article used to mean hand editing every surface it should appear on, so
index.html and blog.html drifted 39 days behind the archive and 118 of 220 articles were
reachable only from a team hub. This script rebuilds the discovery surfaces from the
articles themselves, so a new column lands everywhere it belongs on the next run.

What it owns:

  index.html    The Rundown (5 newest) and the Latest Stories grid (40 newest).
                The lead story stays EDITORIAL: it is read from _discovery.json and is
                only replaced automatically if that article has gone missing.
  blog.html     Page 1 of the archive, plus blog-2.html .. blog-N.html, 40 per page,
                newest first, with crawlable prev/next and page number links.
  team hubs     giants / athletics / 49ers / warriors / sharks: the "Latest in X" grid,
                every article in that section, newest first.

What it does NOT touch: article files, article URLs, canonicals, robots.txt, the JSON-LD
on any page, the feed and sitemap generators, or anything outside its markers.

Existing card markup is reused verbatim wherever the article already has a card on that
surface, so regenerating does not restyle the page. Only genuinely new cards are
synthesised, and they take the grid's dominant width.

Run it after writing an article and before the feed/sitemap generators:

    python _gen_discovery.py
    python _gen_feed.py && python _gen_sitemap.py && python _gen_news_sitemap.py
    python _gen_search_index.py
"""
import os
import re
import sys
import json
import glob
import html

ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(ROOT, '_discovery.json')
PER_PAGE = 40
LATEST_ON_HOME = 40
RUNDOWN = 5

# articleSection -> (hub file, pill class, short label used on a synthesised card)
SECTIONS = {
    'Giants':     ('giants.html',    'sf',     'Giants'),
    'Athletics':  ('athletics.html', 'as',     "A's"),
    '49ers':      ('49ers.html',     'niners', '49ers'),
    'Warriors':   ('warriors.html',  'gs',     'Warriors'),
    'Sharks':     ('sharks.html',    'sj',     'Sharks'),
    'Cal':        (None,             '',       'Cal'),
    'Stanford':   (None,             '',       'Stanford'),
    'NFL':        (None,             'lv',     'Raiders'),
    'Bay Area':   (None,             '',       'Bay Area'),
    'Bay Area Sports': (None,        '',       'Bay Area'),
    'Flashbacks': (None,             '',       'Flashback'),
}

ANCHOR = re.compile(r'<a class="st w\d"[^>]*?href="articles/([^"]+)"[^>]*>.*?</a>', re.S)
RDITEM = re.compile(r'<a class="rd-item"[^>]*>.*?</a>', re.S)
PAGER = re.compile(r'\s*<nav class="pager".*?</nav>', re.S)


def read(path):
    with open(path, encoding='utf-8', newline='') as fh:
        return fh.read()


def write(path, text):
    with open(path, 'w', encoding='utf-8', newline='') as fh:
        fh.write(text)


def manifest():
    """Every article, newest first. Ties break on slug so the order is stable."""
    out = []
    for path in glob.glob(os.path.join(ROOT, 'articles', '*.html')):
        t = read(path)

        def grab(pattern, default=''):
            m = re.search(pattern, t, re.S)
            return m.group(1) if m else default

        slug = os.path.basename(path)[:-5]
        art = {
            'slug': slug,
            'file': 'articles/%s.html' % slug,
            'title': grab(r'<title>(.*?)</title>'),
            'desc': grab(r'<meta name="description" content="(.*?)">'),
            'date': grab(r'"datePublished":"(.*?)"'),
            'section': grab(r'"articleSection":"(.*?)"'),
            'alt': grab(r'<meta property="og:image:alt" content="(.*?)">'),
            'tag': grab(r'<span class="tag">(.*?)</span>'),
        }
        card = grab(r'<meta property="og:image" content="https://bayareasportsblog\.com/assets/img/cards/(.*?)\.jpg"')
        art['card'] = card or slug
        if not art['date']:
            sys.exit('no datePublished in %s' % path)
        out.append(art)
    out.sort(key=lambda a: (a['date'], a['slug']), reverse=True)
    return out


def div_block(text, start):
    """Return (open_end, close_start) for the <div> that starts at `start`."""
    i = text.index('>', start) + 1
    depth = 1
    pos = i
    tag = re.compile(r'<(/?)div\b', re.I)
    while depth:
        m = tag.search(text, pos)
        if not m:
            sys.exit('unbalanced div')
        depth += -1 if m.group(1) else 1
        pos = m.end()
    return i, m.start()


def grid_span(text, nth=0):
    """Byte span of the run of story cards inside the nth <div class="mag">."""
    pos = -1
    for _ in range(nth + 1):
        pos = text.index('<div class="mag">', pos + 1)
    inner_start, inner_end = div_block(text, pos)
    block = text[inner_start:inner_end]
    hits = list(ANCHOR.finditer(block))
    if not hits:
        return None
    return inner_start + hits[0].start(), inner_start + hits[-1].end(), block


def harvest(text, nth=0):
    """slug -> (raw card html, width) for the cards already on this grid."""
    span = grid_span(text, nth)
    if not span:
        return {}, 'w3'
    _, _, block = span
    cards = {}
    widths = []
    for m in ANCHOR.finditer(block):
        raw = m.group(0)
        w = re.search(r'class="st (w\d)"', raw).group(1)
        widths.append(w)
        cards.setdefault(m.group(1)[:-5], (raw, w))
    dominant = max(set(widths), key=widths.count) if widths else 'w3'
    return cards, dominant


def harvest_many(paths):
    """One card-markup registry across several pages, so a card that scrolls off
    page one of the archive keeps its original markup on page four."""
    registry = {}
    widths = {}
    for path in paths:
        if not os.path.exists(path):
            continue
        cards, _ = harvest(read(path))
        for slug, (raw, w) in cards.items():
            registry.setdefault(slug, raw)
            widths.setdefault(slug, w)
    return registry, widths


def reindent(raw, indent):
    """Put a card back at a known indent so regenerating is byte stable.

    The first line carries no padding: the caller drops it at an indent that is
    already in the file, and joins the rest with the same pad.
    """
    lines = raw.split('\r\n')
    if len(lines) == 1:
        return raw.lstrip()
    body = [l for l in lines[1:] if l.strip()]
    base = min(len(l) - len(l.lstrip()) for l in body) if body else 0
    out = [lines[0].lstrip()]
    for line in lines[1:]:
        out.append(' ' * (indent + 2) + line[base:] if line.strip() else line)
    return '\r\n'.join(out)


def restyle(raw, width, heading_attr):
    """Reuse a card's markup on a grid that wants a different width or heading."""
    raw = re.sub(r'class="st w\d"', 'class="st %s"' % width, raw, count=1)
    raw = re.sub(r'<h3[^>]*>', '<h3%s>' % heading_attr, raw, count=1)
    return raw


def synth(art, width, indent, heading_attr=''):
    """A card for an article that has never had one on this surface."""
    s = art['card']
    pill_class = SECTIONS.get(art['section'], (None, '', art['section']))[1]
    label = art['tag'] or SECTIONS.get(art['section'], (None, '', art['section']))[2]
    pad = ' ' * indent
    srcset_w = ('assets/img/cards/{s}-400w.{e} 400w, assets/img/cards/{s}-600w.{e} 600w, '
                'assets/img/cards/{s}-800w.{e} 800w, assets/img/cards/{s}.{e} 1200w')
    sizes = '(max-width: 640px) 92vw, (max-width: 1024px) 48vw, 46vw'
    return (
        '<a class="st {width}" href="{file}">\r\n'
        '{pad}  <div class="st-img"><picture><source type="image/webp" srcset="{webp}" sizes="{sizes}">'
        '<img src="assets/img/cards/{s}.jpg" alt="{alt}" width="1200" height="675" decoding="async" '
        'srcset="{jpg}" sizes="{sizes}"></picture></div>\r\n'
        '{pad}  <div class="st-b">\r\n'
        '{pad}    <div><span class="pill {pill}">{label}</span></div>\r\n'
        '{pad}    <h3{hattr}>{title}</h3>\r\n'
        '{pad}    <p>{desc}</p>\r\n'
        '{pad}    <div class="st-f">Read the column</div>\r\n'
        '{pad}  </div>\r\n'
        '{pad}</a>'
    ).format(pad=pad, width=width, file=art['file'], s=s,
             webp=srcset_w.format(s=s, e='webp'), jpg=srcset_w.format(s=s, e='jpg'),
             sizes=sizes, alt=art['alt'] or art['title'], pill=pill_class, label=label,
             hattr=heading_attr, title=art['title'], desc=art['desc'])


def build_grid(arts, cards, default_width, indent, heading_attr='', widths=None):
    """Cards for `arts`, reusing existing markup, first card gets fetchpriority.

    `widths` is this grid's own slug -> width map, so a card keeps the width it
    already had here and only genuinely new cards take the grid default.
    """
    widths = widths or {}
    out = []
    for art in arts:
        raw = cards.get(art['slug'])
        if raw:
            raw = raw.replace(' fetchpriority="high"', '')
            raw = restyle(raw, widths.get(art['slug'], default_width), heading_attr)
        else:
            raw = synth(art, default_width, indent, heading_attr)
        out.append(reindent(raw, indent))
    # the card at the top of a grid is the LCP candidate: eager and high priority.
    # every other card is lazy, including one that used to lead a page and has since
    # been pushed down by newer stories.
    for i, raw in enumerate(out):
        raw = raw.replace(' loading="lazy"', '')
        if i:
            raw = raw.replace(' decoding="async"', ' decoding="async" loading="lazy"', 1)
        else:
            raw = raw.replace(' decoding="async"', ' decoding="async" fetchpriority="high"', 1)
        out[i] = raw
    return ('\r\n' + ' ' * indent).join(out)


def replace_grid(path, arts, nth=0, heading_attr='', fallback=None):
    text = read(path)
    own, dominant = harvest(text, nth)
    span = grid_span(text, nth)
    if not span:
        print('  %-16s no story grid, skipped' % os.path.basename(path))
        return 0
    registry = dict(fallback or {})
    registry.update({slug: raw for slug, (raw, _) in own.items()})
    widths = {slug: w for slug, (_, w) in own.items()}
    start, end, _ = span
    line_start = text.rfind('\n', 0, start) + 1
    indent = len(text[line_start:start])
    grid = build_grid(arts, registry, dominant, indent, heading_attr, widths)
    write(path, text[:start] + grid + text[end:])
    return len(arts)


# ---------------------------------------------------------------- index.html

def lead_article(arts):
    configured = None
    if os.path.exists(CONFIG):
        configured = json.load(open(CONFIG, encoding='utf-8')).get('lead')
    if configured:
        for a in arts:
            if a['slug'] == configured:
                return a, True
        print('  lead %s is gone, falling back to the newest article' % configured)
    return arts[0], False


def do_index(arts, fallback=None):
    text = read('index.html')
    lead, kept = lead_article(arts)

    m = re.search(r'<a class="lead-main"[^>]*>.*?</a>', text, re.S)
    if not m:
        sys.exit('no .lead-main on index.html')
    raw = m.group(0)
    if not kept:
        s = lead['card']
        raw = re.sub(r'href="articles/[^"]+"', 'href="%s"' % lead['file'], raw, count=1)
        raw = re.sub(r'assets/img/cards/[a-z0-9\-]+((?:-\d+w)?\.(?:jpg|webp))',
                     lambda mm: 'assets/img/cards/%s%s' % (s, mm.group(1)), raw)
        raw = re.sub(r'<h2>.*?</h2>', '<h2>%s</h2>' % lead['title'], raw, count=1, flags=re.S)
        raw = re.sub(r'<p>.*?</p>', '<p>%s</p>' % lead['desc'], raw, count=1, flags=re.S)
        text = text[:m.start()] + raw + text[m.end():]
        write('index.html', text)

    # The Rundown: the newest articles that are not the lead.
    text = read('index.html')
    items = list(RDITEM.finditer(text))
    if len(items) != RUNDOWN:
        sys.exit('expected %d rundown items, found %d' % (RUNDOWN, len(items)))
    picks = [a for a in arts if a['slug'] != lead['slug']][:RUNDOWN]
    line_start = text.rfind('\n', 0, items[0].start()) + 1
    pad = ' ' * (items[0].start() - line_start)
    rows = []
    for n, art in enumerate(picks, 1):
        label = SECTIONS.get(art['section'], (None, '', art['section']))[2]
        rows.append(
            '{pad}<a class="rd-item" href="{file}">\r\n'
            '{pad}  <div class="n">{n}</div>\r\n'
            '{pad}  <h4><span class="k">{label}</span>{title}</h4>\r\n'
            '{pad}</a>'.format(pad=pad, file=art['file'], n=n, label=label, title=art['title']))
    text = text[:line_start] + '\r\n'.join(rows) + text[items[-1].end():]
    write('index.html', text)

    n = replace_grid('index.html', arts[:LATEST_ON_HOME], fallback=fallback)
    return lead, kept, n


# ------------------------------------------------------------ the archive

def pager(page, pages, indent):
    pad = ' ' * indent
    link = ('background:var(--surface2);border:1px solid var(--line);border-radius:999px;'
            'padding:9px 15px;font-size:12.5px;font-weight:800;color:var(--text);'
            'text-decoration:none;display:inline-block')
    here = link + ';border-color:var(--accent);color:#fff'

    def href(p):
        return 'blog.html' if p == 1 else 'blog-%d.html' % p

    parts = []
    if page > 1:
        parts.append('<a href="%s" style="%s" rel="prev">Newer stories</a>' % (href(page - 1), link))
    for p in range(1, pages + 1):
        style = here if p == page else link
        aria = ' aria-current="page"' if p == page else ''
        parts.append('<a href="%s" style="%s"%s>%d</a>' % (href(p), style, aria, p))
    if page < pages:
        parts.append('<a href="%s" style="%s" rel="next">Older stories</a>' % (href(page + 1), link))
    inner = ('\r\n' + pad + '  ').join(parts)
    return ('{pad}<nav class="pager" aria-label="Archive pages" '
            'style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:center;'
            'margin:34px 0 6px">\r\n{pad}  {inner}\r\n{pad}</nav>').format(pad=pad, inner=inner)


def do_archive(arts, fallback=None):
    base = read('blog.html')
    pages = (len(arts) + PER_PAGE - 1) // PER_PAGE
    # the registry spans every archive page that already exists, so regenerating
    # does not lose the markup of a card that has scrolled onto a later page
    existing = ['blog.html'] + sorted(glob.glob('blog-*.html'))
    cards, widths = harvest_many(existing)
    base = PAGER.sub('', base)  # never stack a second pager on a re-run
    for slug, raw in (fallback or {}).items():
        cards.setdefault(slug, raw)
    _, dominant = harvest(base, 0)
    made = []
    for page in range(1, pages + 1):
        chunk = arts[(page - 1) * PER_PAGE: page * PER_PAGE]
        path = 'blog.html' if page == 1 else 'blog-%d.html' % page
        text = base
        url = 'https://bayareasportsblog.com/%s' % path

        if page > 1:
            label = 'Latest Stories, page %d' % page
            text = re.sub(r'<title>.*?</title>', '<title>%s | Bay Area Sports Blog</title>' % label,
                          text, count=1, flags=re.S)
            desc = ('Page %d of the Bay Area Sports Blog archive. Every column, recap and '
                    'history piece we have published, newest first.' % page)
            text = re.sub(r'(<meta name="description" content=")[^"]*(")', r'\g<1>%s\g<2>' % desc, text, count=1)
            text = re.sub(r'(<meta property="og:title" content=")[^"]*(")', r'\g<1>%s\g<2>' % label, text, count=1)
            text = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', r'\g<1>%s\g<2>' % label, text, count=1)
            text = re.sub(r'(<meta property="og:description" content=")[^"]*(")', r'\g<1>%s\g<2>' % desc, text, count=1)
            text = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")', r'\g<1>%s\g<2>' % desc, text, count=1)
            text = re.sub(r'<h1>.*?</h1>', '<h1>%s</h1>' % label, text, count=1, flags=re.S)
        # every archive page points its canonical and og:url at itself
        text = re.sub(r'(<link rel="canonical" href=")[^"]*(")', r'\g<1>%s\g<2>' % url, text, count=1)
        text = re.sub(r'(<meta property="og:url" content=")[^"]*(")', r'\g<1>%s\g<2>' % url, text, count=1)
        # structured data has to describe THIS page, not page one's card list
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
            try:
                data = json.loads(block)
            except ValueError:
                continue
            kind = data.get('@type')
            changed = False
            if kind in ('CollectionPage', 'WebPage'):
                data['url'] = url
                if 'name' in data and page > 1:
                    data['name'] = 'Latest Stories, page %d' % page
                changed = True
            elif kind == 'BreadcrumbList' and page > 1:
                last = data['itemListElement'][-1]
                last['name'] = 'Latest Stories, page %d' % page
                last['item'] = url
                changed = True
            elif kind == 'ItemList':
                data['itemListElement'] = [
                    {'@type': 'ListItem', 'position': i,
                     'url': 'https://bayareasportsblog.com/%s' % a['file'],
                     'name': a['title']}
                    for i, a in enumerate(chunk, 1)]
                data['numberOfItems'] = len(chunk)
                changed = True
            if changed:
                text = text.replace(block, json.dumps(data, separators=(',', ':')), 1)

        span = grid_span(text, 0)
        start, end, _ = span
        line_start = text.rfind('\n', 0, start) + 1
        indent = len(text[line_start:start])
        grid = build_grid(chunk, cards, dominant, indent, ' role="heading" aria-level="2"', widths)
        text = text[:start] + grid + text[end:]

        # the pager goes directly after the grid's wrapper
        inner_start, inner_end = div_block(text, text.index('<div class="mag">'))
        nav = pager(page, pages, max(indent - 2, 2))
        close = text.index('</div>', inner_end)
        text = text[:close + 6] + '\r\n' + nav + text[close + 6:]

        write(path, text)
        made.append((path, len(chunk)))
    return made, pages


def main():
    os.chdir(ROOT)
    arts = manifest()
    print('articles: %d  (newest %s)' % (len(arts), arts[0]['date']))

    # one shared pool of existing card markup, so a card that moves between
    # surfaces keeps the look it already had rather than being rebuilt
    surfaces = (['index.html', 'blog.html'] + sorted(glob.glob('blog-*.html'))
                + [h for h, _, _ in SECTIONS.values() if h])
    shared, _ = harvest_many(surfaces)

    lead, kept, n = do_index(arts, shared)
    print('index.html     lead=%s (%s), rundown=%d, latest grid=%d'
          % (lead['slug'], 'editorial' if kept else 'fallback', RUNDOWN, n))

    made, pages = do_archive(arts, shared)
    print('archive        %d pages, %d per page' % (pages, PER_PAGE))
    for path, count in made:
        print('  %-14s %d cards' % (path, count))

    for section, (hub, _, _) in SECTIONS.items():
        if not hub or not os.path.exists(hub):
            continue
        rows = [a for a in arts if a['section'] == section]
        count = replace_grid(hub, rows, fallback=shared)
        if count:
            print('  %-14s %d cards (section %s)' % (hub, count, section))

    covered = set()
    for path in ['index.html'] + [p for p, _ in made] + [h for h, _, _ in SECTIONS.values() if h]:
        if os.path.exists(path):
            covered |= set(re.findall(r'href="articles/([^"#]+)"', read(path)))
    missing = [a['slug'] for a in arts if a['slug'] + '.html' not in covered]
    print('reachable from generated surfaces: %d/%d' % (len(arts) - len(missing), len(arts)))
    if missing:
        sys.exit('UNREACHABLE: %s' % missing)


if __name__ == '__main__':
    main()
