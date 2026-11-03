#!/usr/bin/env python3
"""commons_search.py "query" [...] - list licensed Commons JPEG candidates (title, size, license)."""
import sys, time, json, urllib.parse
sys.path.insert(0, __import__('os').path.dirname(__file__))
from commons_fetch import search, get, API

for q in sys.argv[1:]:
    print('==', q)
    for i, r in enumerate(search(q, 20)):
        d = json.loads(get(API + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'titles': r['title'], 'prop': 'imageinfo', 'iiprop': 'size'})))
        ii = list(d['query']['pages'].values())[0]['imageinfo'][0]
        print('  %d %s %dx%d %s' % (i, r['title'][5:][:80], ii['width'], ii['height'], r['lic']))
    time.sleep(2)
