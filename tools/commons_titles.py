#!/usr/bin/env python3
"""commons_titles.py name=File:Title [...] - download exact Commons files (licence checked)
to assets/img/players/<name>.jpg and append CREDITS.txt."""
import sys, os, time
sys.path.insert(0, os.path.dirname(__file__))
from commons_fetch import search, get

cred = []
for arg in sys.argv[1:]:
    name, title = arg.split('=', 1)
    dst = 'assets/img/players/%s.jpg' % name
    if os.path.exists(dst):
        print('HAVE', name); continue
    for i in range(3):
        try:
            res = search(title); break
        except Exception as e:
            res = None; time.sleep(20)
    if not res:
        print('NONE', name, title); time.sleep(5); continue
    r = res[0]
    open(dst, 'wb').write(get(r['url']))
    cred.append('%s: %s, photo by %s, %s, %s' % (name, r['title'][5:], r['artist'][:80], r['lic'], r['page']))
    print('OK  ', name, r['title'][5:], r['lic'])
    time.sleep(6)
if cred:
    with open('assets/img/players/CREDITS.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(cred) + '\n')
