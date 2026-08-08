#!/usr/bin/env python3
"""_gen_news_sitemap.py - Google News sitemap (news-sitemap.xml).

Google News only accepts articles published in the last 48 hours, so this file
is small by design and must be regenerated whenever articles are added. Dates
come from the datePublished in each article's JSON-LD (never invented).

Run: python _gen_news_sitemap.py
"""
import os, re, glob, json, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://bayareasportsblog.com/"
NAME = "Bay Area Sports Blog"
WINDOW_HOURS = 48


def rd(p):
    return open(p, encoding='utf-8', errors='replace').read()


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def main():
    os.chdir(ROOT)
    today = datetime.date.today()
    cutoff = today - datetime.timedelta(days=2)
    rows = []
    for f in sorted(glob.glob('articles/*.html')):
        s = rd(f)
        m = re.search(r'"datePublished":"(\d{4}-\d{2}-\d{2})"', s)
        if not m:
            continue
        d = datetime.date.fromisoformat(m.group(1))
        if d < cutoff:
            continue
        t = re.search(r'<title>(.*?)</title>', s, re.S)
        title = t.group(1).strip() if t else NAME
        loc = BASE + f.replace(os.sep, '/')
        rows.append((loc, title, d.isoformat()))

    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">']
    for loc, title, d in rows:
        out += ['  <url>',
                '    <loc>%s</loc>' % esc(loc),
                '    <news:news>',
                '      <news:publication>',
                '        <news:name>%s</news:name>' % NAME,
                '        <news:language>en</news:language>',
                '      </news:publication>',
                '      <news:publication_date>%s</news:publication_date>' % d,
                '      <news:title>%s</news:title>' % esc(title),
                '    </news:news>',
                '  </url>']
    out.append('</urlset>')
    open('news-sitemap.xml', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    print('wrote news-sitemap.xml: %d articles in the last %dh' % (len(rows), WINDOW_HOURS))


if __name__ == '__main__':
    main()
