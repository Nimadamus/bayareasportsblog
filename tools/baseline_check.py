#!/usr/bin/env python3
"""baseline_check.py: has anything regressed against the frozen baseline?

The site reached a clean technical state on 16 September 2026 and that state is recorded
in baseline.json. This re-measures the same things and prints a diff. Counts that are
allowed to grow, pages and articles, only fail when they shrink. Counts that must stay at
zero fail the moment they do not.

    python tools/baseline_check.py              measure and compare
    python tools/baseline_check.py --freeze     overwrite the baseline with today
    python tools/baseline_check.py --live       also crawl the deployed site
"""
import os
import re
import sys
import json
import glob
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASELINE = os.path.join(ROOT, 'baseline.json')

GROW_OK = {'pages', 'articles', 'hubs', 'sitemap_urls', 'crawled_urls', 'articles_reached'}
MUST_BE_ZERO = {'orphans', 'near_orphans', 'broken_links', 'duplicate_titles',
                'duplicate_descriptions', 'noindexed', 'invalid_jsonld', 'schema_errors',
                'voice_under_70', 'non_200'}


def audit_numbers():
    out = subprocess.run([sys.executable, '_seo_audit.py'], capture_output=True, text=True).stdout
    grab = lambda pat, d=0: int(re.search(pat, out).group(1)) if re.search(pat, out) else d
    m = re.search(r'pages (\d+)\s+articles (\d+)\s+hubs (\d+)', out)
    nums = {
        'pages': int(m.group(1)) if m else 0,
        'articles': int(m.group(2)) if m else 0,
        'hubs': int(m.group(3)) if m else 0,
        'orphans': grab(r'orphans\s+:\s+(\d+)'),
        'near_orphans': grab(r'near-orphans \(<=2 inbound\)\s+:\s+(\d+)'),
        'broken_links': grab(r'broken internal links\s+:\s+(\d+)'),
        'duplicate_titles': grab(r'duplicate titles\s+:\s+(\d+)'),
        'duplicate_descriptions': grab(r'duplicate descriptions\s+:\s+(\d+)'),
        'invalid_jsonld': grab(r'invalid JSON-LD\s+:\s+(\d+)'),
        'noindexed': grab(r'noindexed pages\s+:\s+(\d+)'),
    }
    sm = open('sitemap.xml', encoding='utf-8').read()
    nums['sitemap_urls'] = sm.count('<loc>')

    v = subprocess.run([sys.executable, 'tools/voice_gate.py', '--all', '--min', '70'],
                       capture_output=True, text=True).stdout
    mv = re.search(r'ARTICLES=(\d+)\s+MEDIAN=(\d+)\s+UNDER_70=(\d+)', v)
    if mv:
        nums['voice_articles'] = int(mv.group(1))
        nums['voice_median'] = int(mv.group(2))
        nums['voice_under_70'] = int(mv.group(3))

    s = subprocess.run([sys.executable, 'tools/schema_validate.py'], capture_output=True, text=True).stdout
    ms = re.search(r'errors=(\d+)\s+warnings=(\d+)', s)
    if ms:
        nums['schema_errors'] = int(ms.group(1))
        nums['schema_warnings'] = int(ms.group(2))
    mt = re.search(r"types=(\{[^}]*\})", s)
    if mt:
        nums['schema_types'] = mt.group(1)
    return nums


def live_numbers():
    import urllib.request
    from urllib.parse import urljoin, urldefrag
    BASE = 'https://bayareasportsblog.com/'
    seen, bad, frontier = {}, [], ['']

    def norm(u):
        u = urldefrag(u)[0].split('?')[0]
        if not u.startswith(BASE):
            return None
        p = u[len(BASE):]
        return '' if p in ('', 'index.html') else p

    while frontier:
        nxt = []
        for path in frontier:
            try:
                with urllib.request.urlopen(urllib.request.Request(BASE + path), timeout=30) as r:
                    body = r.read().decode('utf-8', 'replace')
                    seen[path] = r.status
            except Exception as exc:
                seen[path] = getattr(exc, 'code', 0)
                bad.append((path, seen[path]))
                continue
            for href in re.findall(r'<a[^>]+href="([^"]+)"', body):
                if href.startswith(('mailto:', 'tel:', 'javascript:')):
                    continue
                t = norm(urljoin(BASE + path, href))
                if t is None or not (t == '' or t.endswith('.html')):
                    continue
                if t not in seen and t not in nxt:
                    nxt.append(t)
        frontier = nxt
    return {'crawled_urls': len(seen), 'non_200': len(bad),
            'articles_reached': sum(1 for p in seen if p.startswith('articles/'))}


def main():
    nums = audit_numbers()
    if '--live' in sys.argv:
        nums.update(live_numbers())

    if '--freeze' in sys.argv:
        import datetime
        nums['_frozen'] = datetime.date.today().isoformat()
        json.dump(nums, open(BASELINE, 'w', encoding='utf-8'), indent=1, sort_keys=True)
        print('baseline frozen:', json.dumps(nums, indent=1, sort_keys=True))
        return 0

    if not os.path.exists(BASELINE):
        sys.exit('no baseline.json, run with --freeze first')
    base = json.load(open(BASELINE, encoding='utf-8'))
    fails, notes = [], []
    for key, want in sorted(base.items()):
        if key.startswith('_') or key not in nums:
            continue
        got = nums[key]
        if got == want:
            continue
        if key in MUST_BE_ZERO:
            fails.append('%-26s %s -> %s' % (key, want, got))
        elif key in GROW_OK:
            (notes if got > want else fails).append('%-26s %s -> %s' % (key, want, got))
        else:
            notes.append('%-26s %s -> %s' % (key, want, got))

    print('BASELINE CHECK against %s' % base.get('_frozen'))
    for n in notes:
        print('  ok    %s' % n)
    for f in fails:
        print('  FAIL  %s' % f)
    if not fails:
        print('  no regressions')
    return 2 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
