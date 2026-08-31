import glob, os, re, sys, datetime
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
BASE = "https://bayareasportsblog.com/"
# search.html is the site-search UI, not a destination page: it stays indexable
# (nothing here is ever noindexed) but it does not belong in a submitted sitemap.
#
# cal and stanford were temporarily unlisted while they had zero articles; they were
# relisted 2026-08-08 once the college football cluster gave them real coverage.
# betting stays out: decided 2026-08-08 that the betting desk lives on TMR and
# BetLegend, not on this blog.
EXCLUDE = {'404.html', 'google6f74b54ecd988601.html', 'search.html'}
order = ['index.html','nfl.html','mlb.html','nba.html','nhl.html',
         '49ers.html','warriors.html','giants.html','bayarea.html',
         'history.html','flashbacks.html','columns.html','athletics.html','sharks.html',
         'stanford.html','cal.html','betting.html','about.html','contact.html']
DAILY = {'index.html','blog.html','giants.html','49ers.html','warriors.html',
         'athletics.html','sharks.html'}

def published(path, html):
    m = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})"', html)
    if m:
        return m.group(1)
    return datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()

def card_for(html):
    m = re.search(r'<meta property="og:image" content="(.*?)"', html)
    return m.group(1) if m else None

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;')

roots = [f for f in glob.glob('*.html') if f not in EXCLUDE]
roots = sorted(roots, key=lambda f: (order.index(f) if f in order else 999, f))
arts = sorted(glob.glob('articles/*.html'))
daily = sorted(glob.glob('daily/*.html'))

entries = []   # (loc, lastmod, changefreq, priority, image)
for f in roots:
    html = open(f, encoding='utf-8', errors='ignore').read()
    loc = BASE if f == 'index.html' else BASE + f
    pri = '1.0' if f == 'index.html' else ('0.8' if f in order else '0.6')
    entries.append((loc, published(f, html), 'daily' if f in DAILY else 'weekly', pri, card_for(html)))
for f in daily:
    html = open(f, encoding='utf-8', errors='ignore').read()
    entries.append((BASE + f.replace(os.sep, '/'), published(f, html), 'monthly', '0.5', card_for(html)))

art_rows = []
for f in arts:
    html = open(f, encoding='utf-8', errors='ignore').read()
    art_rows.append((BASE + f.replace(os.sep, '/'), published(f, html), 'monthly', '0.7', card_for(html)))
# newest articles first so crawlers meet the fresh URLs early
art_rows.sort(key=lambda r: r[1], reverse=True)
entries += art_rows

xml = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
       'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
for loc, lastmod, freq, pri, img in entries:
    xml.append('  <url>')
    xml.append('    <loc>%s</loc>' % loc)
    xml.append('    <lastmod>%s</lastmod>' % lastmod)
    xml.append('    <changefreq>%s</changefreq>' % freq)
    xml.append('    <priority>%s</priority>' % pri)
    if img:
        xml.append('    <image:image><image:loc>%s</image:loc></image:image>' % esc(img))
    xml.append('  </url>')
xml += ['</urlset>', '']
open('sitemap.xml', 'w', encoding='utf-8').write('\n'.join(xml))
print("sitemap urls:", len(entries))
