#!/usr/bin/env python3
"""Build feed.xml (RSS 2.0) from every article page.
Run after adding articles: python _gen_feed.py
"""
import os, re, glob, json
from email.utils import format_datetime
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://bayareasportsblog.com/"
LIMIT = 40


def field(pattern, html):
    m = re.search(pattern, html, re.S | re.I)
    if not m:
        return ''
    s = re.sub(r'\s+', ' ', m.group(1)).strip()
    for ent, ch in (('&middot;', '·'), ('&amp;', '&'), ('&#39;', "'"), ('&quot;', '"'), ('&mdash;', '—')):
        s = s.replace(ent, ch)
    return s


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;').replace("'", '&#39;'))


items = []
for p in sorted(glob.glob(os.path.join(ROOT, 'articles', '*.html'))):
    html = open(p, encoding='utf-8', errors='ignore').read()
    slug = os.path.basename(p)
    title = field(r'<title>(.*?)</title>', html).split('|')[0].strip()
    desc = field(r'<meta name="description" content="(.*?)"', html)
    date = field(r'"datePublished"\s*:\s*"(.*?)"', html) or '2026-01-01'
    tag = field(r'<span class="tag">(.*?)</span>', html) or 'Column'
    img = field(r'<meta property="og:image" content="(.*?)"', html)
    items.append({'u': BASE + 'articles/' + slug, 't': title, 'd': desc,
                  'dt': date, 'k': tag, 'img': img})

items.sort(key=lambda x: x['dt'], reverse=True)
items = items[:LIMIT]

now = format_datetime(datetime.now(timezone.utc))


def pub(d):
    try:
        return format_datetime(datetime.strptime(d, '%Y-%m-%d').replace(tzinfo=timezone.utc))
    except Exception:
        return now


out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">',
       '<channel>',
       '  <title>Bay Area Sports Blog</title>',
       '  <link>%s</link>' % BASE,
       '  <description>Every Bay Area team, argued about properly. The 49ers, Warriors, Giants, A\'s and Sharks, written by a fan, not a network.</description>',
       '  <language>en-us</language>',
       '  <copyright>Copyright 2026 Bay Area Sports Blog</copyright>',
       '  <lastBuildDate>%s</lastBuildDate>' % now,
       '  <atom:link href="%sfeed.xml" rel="self" type="application/rss+xml"/>' % BASE]

for it in items:
    out.append('  <item>')
    out.append('    <title>%s</title>' % esc(it['t']))
    out.append('    <link>%s</link>' % it['u'])
    out.append('    <guid isPermaLink="true">%s</guid>' % it['u'])
    out.append('    <pubDate>%s</pubDate>' % pub(it['dt']))
    out.append('    <category>%s</category>' % esc(it['k']))
    out.append('    <description>%s</description>' % esc(it['d']))
    if it['img']:
        out.append('    <enclosure url="%s" type="image/jpeg" length="0"/>' % esc(it['img']))
    out.append('  </item>')

out += ['</channel>', '</rss>', '']
open(os.path.join(ROOT, 'feed.xml'), 'w', encoding='utf-8').write('\n'.join(out))
print('wrote feed.xml: %d items' % len(items))
