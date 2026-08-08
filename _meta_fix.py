#!/usr/bin/env python3
"""_meta_fix.py - metadata and schema hardening (no visible copy is rewritten).

- meta description trimmed to <=165 chars at a sentence or clause boundary, and
  og:description / twitter:description kept in sync with it
- the seven thin hub descriptions expanded past 70 chars
- the homepage/welcome duplicate description broken
- short image alts replaced with the richer alt the site already uses for that
  exact image file
- BreadcrumbList added to index.html and 404.html
- index.html gets the H1 it was missing, off-screen so the locked homepage
  layout is untouched (see NOTE below)

NOTE on the homepage H1: the visible lead-story headline is styled by
`.lm-body h2`, so promoting it to <h1> would need a CSS rule and would change
the homepage. The H1 here is real, honest page-topic text positioned off-screen.
Swap it for a visible H1 whenever the homepage layout is open for changes.

  python _meta_fix.py [--check]
"""
import os, re, sys, glob, json, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://bayareasportsblog.com/"
DESC_MAX = 165
ALT_MIN = 15

HUB_DESCS = {
    'athletics.html': "Athletics coverage from Bay Area Sports Blog: every game, the move out of Oakland, and what is left of a fan base that got nothing for its loyalty.",
    'betting.html': "Bay Area sports betting angles from a fan who watches the games: value spots, the numbers that actually matter, and lines worth a second look.",
    'cal.html': "Cal Golden Bears coverage from Bay Area Sports Blog: football, basketball, the conference move, and the rivalry games that still decide a season.",
    'contact.html': "Contact Bay Area Sports Blog with a tip, a correction, an argument, or a story you think we should be covering. Everything that comes in gets read.",
    'sharks.html': "San Jose Sharks coverage from Bay Area Sports Blog: the rebuild, the young core, and the long road back to relevance in the NHL.",
    'stanford.html': "Stanford Cardinal coverage from Bay Area Sports Blog: football, basketball, the conference move, and the programs that keep quietly producing pros.",
    'warriors.html': "Golden State Warriors coverage from Bay Area Sports Blog: the roster, the rotation, Steph's window, and what this era has left at Chase Center.",
}

# hand-written where a clean sentence cut would land under 70 chars, plus the
# rewrite that breaks the homepage/welcome duplicate flagged by the crawl
UNIQUE_DESCS = {
    'articles/welcome-to-bay-area-sports-blog.html':
        "Why this blog exists: a Bay Area fan writing about the 49ers, Giants, "
        "A's, Warriors and Sharks with no wire copy and no neutrality.",
    'articles/bruce-bochy-bullpen-wizardry-core-four.html':
        "Bruce Bochy managed the Giants bullpen like a chess grandmaster. How "
        "Lopez, Casilla, Romo and Affeldt became the Core Four behind three "
        "World Series titles.",
    'articles/giants-1993-pennant-race-salomon-torres-final-day.html':
        "The 1993 Giants won 103 games and still missed October. Inside the last "
        "great pennant race and the final-day loss to the Dodgers that ended it.",
    'articles/giants-heating-up-best-baseball-of-the-season-july-30.html':
        "Over five games the Giants beat the best team in baseball twice, won one "
        "in extra innings and hung sixteen runs on a 67-win club.",
    'articles/giants-season-over-build-around-eldridge-posey-bullpen.html':
        "At 35-49 and 17 games back the Giants season is done, and the path "
        "forward runs through Bryce Eldridge and a bullpen Posey has to rebuild.",
    'articles/giants-trade-deadline-monday-posey-sell-ramos-arraez-ray.html':
        "Forty-seven and sixty-four, ten games out, Heliot Ramos on the block and "
        "a bullpen that has cost this team a dozen games. Posey has to sell.",
}

# images the site never gives a descriptive alt anywhere
ALT_OVERRIDES = {
    'tony-vitello-not-ready-cant-talk-down-quote.jpg':
        'Tony Vitello, manager of the San Francisco Giants',
    'giants-first-half-breakdown-vitello-second-half-all-star-break-2026.jpg':
        'Tony Vitello, manager of the San Francisco Giants',
}

HOME_H1 = ('<h1 style="position:absolute;width:1px;height:1px;overflow:hidden;'
           'clip:rect(0 0 0 0);white-space:nowrap">Bay Area Sports Blog: 49ers, '
           'Giants, Athletics, Warriors and Sharks</h1>')

TITLE_MAX = 70
TITLES = {}
_tp = os.path.join(ROOT, '_titles.json')
if os.path.exists(_tp):
    TITLES = {k: v for k, v in
              json.load(open(_tp, encoding='utf-8')).items() if not k.startswith('_')}
    over = {k: len(v) for k, v in TITLES.items() if len(v) > TITLE_MAX}
    if over:
        raise SystemExit('titles over %d chars: %s' % (TITLE_MAX, over))

TITLE_RE = re.compile(r'(<title>)(.*?)(</title>)', re.S)
OG_TITLE_RE = re.compile(r'(<meta property="og:title" content=")([^"]*)(")')
TW_TITLE_RE = re.compile(r'(<meta name="twitter:title" content=")([^"]*)(")')
DESC_RE = re.compile(r'(<meta name="description" content=")([^"]*)(")')
OG_DESC_RE = re.compile(r'(<meta property="og:description" content=")([^"]*)(")')
TW_DESC_RE = re.compile(r'(<meta name="twitter:description" content=")([^"]*)(")')
IMG_RE = re.compile(r'<img\s[^>]*>')


def rd(p):
    return open(p, encoding='utf-8', errors='strict').read()


def wr(p, s):
    with open(p, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)
    b = open(p, 'rb').read()
    if b'\x00' in b:
        raise SystemExit('NULL-byte corruption writing %s - ABORT' % p)
    if b.count(b'\xef\xbf\xbd'):
        raise SystemExit('encoding damage writing %s - ABORT' % p)


def pages():
    return ([os.path.basename(f) for f in sorted(glob.glob(os.path.join(ROOT, '*.html')))]
            + ['articles/' + os.path.basename(f)
               for f in sorted(glob.glob(os.path.join(ROOT, 'articles', '*.html')))])


def shorten_desc(d):
    """Pack whole sentences up to the limit; fall back to a clause boundary."""
    if len(d) <= DESC_MAX:
        return d
    sents = re.split(r'(?<=[.!?])\s+', d)
    out = ''
    for s in sents:
        cand = (out + ' ' + s).strip() if out else s
        if len(cand) <= DESC_MAX:
            out = cand
        else:
            break
    if out:
        return out
    # one very long sentence: cut at the last clause break that fits
    head = d[:DESC_MAX]
    cut = max(head.rfind(', '), head.rfind(' — '), head.rfind('; '),
              head.rfind(' and '), head.rfind(' but '))
    if cut < 60:
        cut = head.rfind(' ')
    out = d[:cut].rstrip(' ,;:—-')
    return out + '.' if not out.endswith(('.', '!', '?')) else out


def best_alts(all_pages):
    """src basename -> the longest descriptive alt the site already uses."""
    best = {}
    for pg in all_pages:
        s = rd(os.path.join(ROOT, pg))
        for m in IMG_RE.finditer(s):
            src = re.search(r'src="([^"]+)"', m.group(0))
            alt = re.search(r'alt="([^"]*)"', m.group(0))
            if not src or not alt:
                continue
            k = os.path.basename(src.group(1))
            a = alt.group(1)
            if len(a) >= ALT_MIN and len(a) > len(best.get(k, '')):
                best[k] = a
    best.update(ALT_OVERRIDES)
    return best


def fix_alts(s, best):
    def sub(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag)
        alt = re.search(r'alt="([^"]*)"', tag)
        if not src or not alt or len(alt.group(1)) >= ALT_MIN:
            return tag
        good = best.get(os.path.basename(src.group(1)))
        if not good or len(good) < ALT_MIN:
            return tag
        return tag[:alt.start(1)] + good.replace('"', '&quot;') + tag[alt.end(1):]
    return IMG_RE.sub(sub, s)


def sync_desc(s, desc):
    esc = desc.replace('"', '&quot;')
    s = DESC_RE.sub(lambda m: m.group(1) + esc + m.group(3), s, count=1)
    s = OG_DESC_RE.sub(lambda m: m.group(1) + esc + m.group(3), s, count=1)
    s = TW_DESC_RE.sub(lambda m: m.group(1) + esc + m.group(3), s, count=1)
    return s


def add_breadcrumb(s, page):
    if 'BreadcrumbList' in s:
        return s
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE}]
    if page == '404.html':
        items.append({"@type": "ListItem", "position": 2, "name": "Page not found",
                      "item": BASE + "404.html"})
    node = {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": items}
    tag = ('<script type="application/ld+json">%s</script>\n'
           % json.dumps(node, separators=(',', ':')))
    return s.replace('</head>', tag + '</head>', 1)


def add_home_h1(s):
    if re.search(r'<h1[^>]*>', s):
        return s
    m = re.search(r'</nav>', s)
    if not m:
        return s
    return s[:m.end()] + '\n' + HOME_H1 + s[m.end():]


def main():
    check = '--check' in sys.argv
    all_pages = pages()
    best = best_alts(all_pages)
    stats = collections.Counter()

    for page in all_pages:
        p = os.path.join(ROOT, page)
        s0 = rd(p)
        s = s0

        s = fix_alts(s, best)
        if s != s0:
            stats['alts'] += 1

        if page in TITLES:
            new_t = TITLES[page]
            social = new_t.split(' | Bay Area Sports Blog')[0]
            before = s
            s = TITLE_RE.sub(lambda m: m.group(1) + new_t + m.group(3), s, count=1)
            esc = social.replace('"', '&quot;')
            s = OG_TITLE_RE.sub(lambda m: m.group(1) + esc + m.group(3), s, count=1)
            s = TW_TITLE_RE.sub(lambda m: m.group(1) + esc + m.group(3), s, count=1)
            if s != before:
                stats['title'] += 1

        m = DESC_RE.search(s)
        if m:
            cur = m.group(2)
            new = UNIQUE_DESCS.get(page) or HUB_DESCS.get(page) or shorten_desc(cur)
            if new != cur:
                s = sync_desc(s, new)
                stats['desc_trimmed' if len(cur) > DESC_MAX else 'desc_rewritten'] += 1

        if page in ('index.html', '404.html'):
            before = s
            s = add_breadcrumb(s, page)
            if s != before:
                stats['breadcrumb'] += 1
        if page == 'index.html':
            before = s
            s = add_home_h1(s)
            if s != before:
                stats['home_h1'] += 1

        if s != s0 and not check:
            wr(p, s)

    print(('CHECK ' if check else 'APPLIED ')
          + ' '.join('%s=%d' % kv for kv in sorted(stats.items())))


if __name__ == '__main__':
    main()
