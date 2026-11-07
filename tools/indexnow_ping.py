#!/usr/bin/env python3
"""indexnow_ping.py: tell Bing, Yandex and the other IndexNow engines a URL changed.

  python tools/indexnow_ping.py <url> [<url> ...]   these URLs
  python tools/indexnow_ping.py --all               every URL in sitemap.xml

The key file sits at the site root. Google does not use IndexNow; tools in
~/tools/gsc_submit.py cover it. Run this right after the page is live.
"""
import json, os, re, sys, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = 'bayareasportsblog.com'
KEY = '8503f389f331482bb5dd6c5c7618553c'


def main():
    args = sys.argv[1:]
    if args == ['--all']:
        args = re.findall(r'<loc>(.*?)</loc>', open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read())
    if not args:
        sys.exit(__doc__)
    body = json.dumps({'host': HOST, 'key': KEY, 'keyLocation': 'https://%s/%s.txt' % (HOST, KEY), 'urlList': args}).encode()
    req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body, headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        print('IndexNow', urllib.request.urlopen(req, timeout=30).status, len(args), 'urls')
    except urllib.error.HTTPError as e:
        sys.exit('IndexNow failed %s %s' % (e.code, e.read()[:200]))


if __name__ == '__main__':
    main()
