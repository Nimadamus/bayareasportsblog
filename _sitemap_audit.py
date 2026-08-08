#!/usr/bin/env python3
"""_sitemap_audit.py - is the sitemap safe to submit?

Cross-checks sitemap.xml and news-sitemap.xml against the files on disk and
against each page's own head. A sitemap that lists a noindex page, a page whose
canonical points somewhere else, or a URL with no file behind it costs crawl
budget and trust, so all three are hard failures here.

Checks:
  MISSING      an indexable page on disk that the sitemap does not list
  DEAD         a sitemap URL with no file behind it
  NOINDEX      a listed URL whose page is noindex
  NONCANONICAL a listed URL that is not its own canonical
  BADIMAGE     an <image:loc> with no file behind it
  DUPE         a URL listed twice
  BADDATE      a lastmod that is not YYYY-MM-DD, or is in the future
  NEWSSTALE    a news-sitemap entry older than 48h (Google's window)
  NEWSTITLE    a news title that does not match the page title
  ROBOTS       a sitemap not declared in robots.txt

Exits 2 on any failure.

  python _sitemap_audit.py [--json]
"""
import os, re, sys, glob, json, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://bayareasportsblog.com/"
# kept in step with _gen_sitemap.py - pages that are live and indexable but deliberately
# not submitted. betting has no content and no plan for any.
EXCLUDE = {'404.html', 'google6f74b54ecd988601.html', 'search.html',
           'betting.html'}
TODAY = datetime.date(2026, 8, 8)

LOC = re.compile(r'<loc>([^<]+)</loc>')
IMGLOC = re.compile(r'<image:loc>([^<]+)</image:loc>')
LASTMOD = re.compile(r'<lastmod>([^<]+)</lastmod>')
URLBLOCK = re.compile(r'<url>(.*?)</url>', re.S)
NEWSDATE = re.compile(r'<news:publication_date>([^<]+)</news:publication_date>')
NEWSTITLE = re.compile(r'<news:title>([^<]*)</news:title>')


def rd(p):
    return open(p, encoding='utf-8', errors='replace').read()


def url_to_path(u):
    if not u.startswith(BASE):
        return None
    rel = u[len(BASE):]
    return 'index.html' if rel == '' else rel


def main():
    fails, notes = [], []
    sm = rd(os.path.join(ROOT, 'sitemap.xml'))
    news = rd(os.path.join(ROOT, 'news-sitemap.xml'))
    robots = rd(os.path.join(ROOT, 'robots.txt'))

    for name in ('sitemap.xml', 'news-sitemap.xml'):
        if BASE + name not in robots:
            fails.append(('ROBOTS', name, 'not declared in robots.txt'))

    # ---- what should be listed
    on_disk = set()
    for f in (glob.glob(os.path.join(ROOT, '*.html'))
              + glob.glob(os.path.join(ROOT, 'articles', '*.html'))
              + glob.glob(os.path.join(ROOT, 'daily', '*.html'))):
        rel = os.path.relpath(f, ROOT).replace(os.sep, '/')
        if rel in EXCLUDE:
            continue
        s = rd(f)
        if re.search(r'<meta name="robots"[^>]*noindex', s, re.I):
            continue
        on_disk.add(rel)

    # ---- what is listed
    listed, seen = [], set()
    for block in URLBLOCK.findall(sm):
        m = LOC.search(block)
        if not m:
            continue
        u = m.group(1)
        p = url_to_path(u)
        listed.append((u, p, block))
        if u in seen:
            fails.append(('DUPE', u, 'listed more than once'))
        seen.add(u)

    for u, p, block in listed:
        if p is None or not os.path.exists(os.path.join(ROOT, p)):
            fails.append(('DEAD', u, 'no file on disk'))
            continue
        s = rd(os.path.join(ROOT, p))
        if re.search(r'<meta name="robots"[^>]*noindex', s, re.I):
            fails.append(('NOINDEX', u, 'page is noindex'))
        can = re.search(r'<link rel="canonical" href="([^"]+)"', s)
        if not can:
            fails.append(('NONCANONICAL', u, 'page has no canonical'))
        elif can.group(1) != u:
            fails.append(('NONCANONICAL', u, 'canonical is ' + can.group(1)))
        lm = LASTMOD.search(block)
        if not lm or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', lm.group(1)):
            fails.append(('BADDATE', u, lm.group(1) if lm else 'missing'))
        else:
            d = datetime.date.fromisoformat(lm.group(1))
            if d > TODAY:
                fails.append(('BADDATE', u, 'lastmod in the future: %s' % d))
        for img in IMGLOC.findall(block):
            ip = url_to_path(img)
            if not ip or not os.path.exists(os.path.join(ROOT, ip)):
                fails.append(('BADIMAGE', u, img))

    for rel in sorted(on_disk - {p for _, p, _ in listed if p}):
        fails.append(('MISSING', rel, 'indexable but not in sitemap'))

    # ---- news sitemap: 48h window, titles must match the page
    for block in URLBLOCK.findall(news):
        m, dm, tm = LOC.search(block), NEWSDATE.search(block), NEWSTITLE.search(block)
        if not m:
            continue
        u = m.group(1)
        p = url_to_path(u)
        if not p or not os.path.exists(os.path.join(ROOT, p)):
            fails.append(('DEAD', u, 'news entry with no file'))
            continue
        if dm:
            d = datetime.date.fromisoformat(dm.group(1)[:10])
            if (TODAY - d).days > 2:
                fails.append(('NEWSSTALE', u, 'published %s' % d))
        if tm:
            s = rd(os.path.join(ROOT, p))
            t = re.search(r'<title>(.*?)</title>', s, re.S)
            page_t = t.group(1).split(' | Bay Area Sports Blog')[0] if t else ''
            if tm.group(1).replace('&#39;', "'") != page_t.replace('&#39;', "'"):
                fails.append(('NEWSTITLE', u, '%r vs page %r'
                              % (tm.group(1)[:40], page_t[:40])))

    notes.append('sitemap urls: %d' % len(listed))
    notes.append('news urls: %d' % len(URLBLOCK.findall(news)))
    notes.append('indexable pages on disk: %d' % len(on_disk))
    notes.append('excluded by design: %s' % ', '.join(sorted(EXCLUDE)))

    if '--json' in sys.argv:
        json.dump({'failures': [{'kind': k, 'url': u, 'detail': d}
                                for k, u, d in fails], 'notes': notes},
                  open(os.path.join(ROOT, '_sitemap_audit.json'), 'w',
                       encoding='utf-8'), indent=1)

    for n in notes:
        print('  ' + n)
    print('SITEMAP AUDIT  failures=%d' % len(fails))
    for k, u, d in fails[:40]:
        print('  %-13s %-64s %s' % (k, u[-64:], d))
    print('AUDIT PASSED.' if not fails else 'AUDIT FAILED.')
    return 2 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
