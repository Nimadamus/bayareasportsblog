#!/usr/bin/env python3
"""commons_fetch.py - fetch freely licensed photos from Wikimedia Commons for article
cards that have no real photo. Input tools/photo_queries.json {slug: query or "lib:path"}.
Saves assets/img/players/commons-<slug>.jpg, appends CREDITS.txt, updates photo_pick.json.
Skips files whose license is not CC BY / CC BY-SA / CC0 / public domain."""
import os, re, json, sys, time, urllib.request, urllib.parse, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
UA = {'User-Agent': 'BayAreaSportsBlogCardBot/1.0 (bayareasportsblog.com)'}
API = 'https://commons.wikimedia.org/w/api.php?'
OKLIC = re.compile(r'^(cc[- ]by(-sa)?[- ]?\d|cc0|public domain|pd)', re.I)
SKIP = re.compile(r'logo|map|signature|svg|card|diagram|chart|seal|crest|uniform|jersey|ticket|book|coin|stamp|wordmark|plaque|grave', re.I)


def get(url):
    req = urllib.request.Request(url, headers=UA)
    for i in range(4):
        try:
            return urllib.request.urlopen(req, timeout=40).read()
        except Exception as e:
            if i == 3: raise
            time.sleep(3 * (i + 1))


def search(q, n=15):
    p = {'action': 'query', 'format': 'json', 'generator': 'search', 'gsrnamespace': 6,
         'gsrsearch': q + ' filetype:bitmap', 'gsrlimit': n, 'prop': 'imageinfo',
         'iiprop': 'url|size|extmetadata|mime', 'iiurlwidth': 1800}
    if q.startswith('File:'):   # exact file title
        p = {'action': 'query', 'format': 'json', 'titles': q, 'prop': 'imageinfo',
             'iiprop': 'url|size|extmetadata|mime', 'iiurlwidth': 1800}
    d = json.loads(get(API + urllib.parse.urlencode(p)))
    pages = sorted(d.get('query', {}).get('pages', {}).values(), key=lambda x: x.get('index', 99))
    out = []
    for pg in pages:
        ii = (pg.get('imageinfo') or [{}])[0]
        md = ii.get('extmetadata', {})
        lic = html.unescape(re.sub('<[^>]+>', '', md.get('LicenseShortName', {}).get('value', '')))
        art = html.unescape(re.sub('<[^>]+>', '', md.get('Artist', {}).get('value', ''))).strip()
        if ii.get('mime') != 'image/jpeg' or SKIP.search(pg['title']): continue
        if ii.get('width', 0) < 900 or ii.get('height', 0) < 600: continue
        if not OKLIC.search(lic): continue
        out.append(dict(title=pg['title'], url=ii.get('thumburl') or ii['url'], lic=lic, artist=art or 'unknown',
                        page=ii.get('descriptionurl', '')))
    return out


def main():
    qs = json.load(open('tools/photo_queries.json', encoding='utf-8'))
    pick = json.load(open('tools/photo_pick.json'))
    used = set(v for v in pick.values() if v)
    only = set(sys.argv[1:])
    credits = []
    for slug, q in qs.items():
        if only and slug not in only: continue
        if q.startswith('lib:'):
            pick[slug] = q[4:]; print('LIB ', slug, q[4:]); continue
        dst = 'assets/img/players/commons-%s.jpg' % slug
        rank = 0
        if '#' in q: q, rank = q.split('#'); rank = int(rank)
        try:
            res = search(q)
        except Exception as e:
            print('ERR ', slug, e); continue
        res = [r for r in res if r['url'] not in used]
        if len(res) <= rank:
            print('NONE', slug, q); continue
        r = res[rank]
        open(dst, 'wb').write(get(r['url']))
        used.add(r['url'])
        pick[slug] = dst
        credits.append('%s: %s, photo by %s, %s, %s' % (slug, r['title'][5:], r['artist'][:80], r['lic'], r['page']))
        print('OK  ', slug, '<-', r['title'][5:], '|', r['lic'])
        time.sleep(2.5)
    json.dump(pick, open('tools/photo_pick.json', 'w'), indent=1)
    if credits:
        with open('assets/img/players/CREDITS.txt', 'a', encoding='utf-8') as f:
            f.write('\n' + '\n'.join(credits) + '\n')


if __name__ == '__main__':
    main()
