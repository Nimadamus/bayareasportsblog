#!/usr/bin/env python3
"""Fetch a real, freely-licensed player/subject photo for an article or section.

RULE: every image on Bay Area Sports Blog must represent its article/section.
  - 49ers article  -> the player it is about (e.g. Brandon Aiyuk)
  - Warriors section -> a Warriors star (e.g. Stephen Curry)
  - Giants -> a Giants player   Sharks -> a Sharks player   A's -> an A's player
Never use a generic "looks sporty" stock photo.

Source: Wikipedia REST summary -> Wikimedia Commons original image (freely
licensed for living athletes: CC BY / CC BY-SA). Attribution is fetched too and
must be added to about.html Photo Credits.

Usage:
  python fetch_player_image.py "Brandon Aiyuk" aiyuk
  python fetch_player_image.py "Stephen Curry" curry
Outputs: assets/img/players/<slug>.<ext>  and prints the credit line to append
to the About page Photo Credits list.
"""
import sys, os, json, re, urllib.parse, urllib.request

UA = "BayAreaSportsBlog/1.0 (nj2121@gmail.com)"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'img', 'players')

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return urllib.request.urlopen(req, timeout=30).read()

def strip(html): return re.sub('<[^>]+>', '', html or '').strip()

def main():
    if len(sys.argv) < 3:
        print("usage: fetch_player_image.py \"Player Name\" <slug>"); sys.exit(1)
    name, slug = sys.argv[1], sys.argv[2]
    title = name.replace(' ', '_')
    # 1) lead image URL
    summ = json.loads(get("https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(title)))
    src = (summ.get('originalimage') or summ.get('thumbnail') or {}).get('source')
    if not src:
        print("no image found for", name); sys.exit(2)
    ext = os.path.splitext(urllib.parse.urlparse(src).path)[1].lower() or '.jpg'
    os.makedirs(OUT, exist_ok=True)
    dest = os.path.join(OUT, slug + ext)
    data = get(src)
    if data[:3] not in (b'\xff\xd8\xff', b'\x89PN'):
        print("downloaded file is not a JPEG/PNG"); sys.exit(3)
    open(dest, 'wb').write(data)
    # 2) attribution from Commons
    fname = os.path.basename(urllib.parse.urlparse(src).path)
    fname = urllib.parse.unquote(fname)
    api = ("https://commons.wikimedia.org/w/api.php?action=query&titles=File:"
           + urllib.parse.quote(fname) + "&prop=imageinfo&iiprop=extmetadata&format=json")
    try:
        p = next(iter(json.loads(get(api))['query']['pages'].values()))
        m = p.get('imageinfo', [{}])[0].get('extmetadata', {})
        author = strip(m.get('Artist', {}).get('value', '')) or 'Wikimedia Commons'
        lic = strip(m.get('LicenseShortName', {}).get('value', '')) or 'see file page'
    except Exception:
        author, lic = 'Wikimedia Commons', 'see file page'
    print("saved:", os.path.relpath(dest))
    print("ref  : assets/img/players/%s%s" % (slug, ext))
    print("credit (add to about.html): %s photo by %s, %s" % (name, author, lic))

if __name__ == '__main__':
    main()
