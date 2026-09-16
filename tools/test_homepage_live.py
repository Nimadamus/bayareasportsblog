"""Failure drills for _gen_homepage_live.py.

Each scenario rewrites index.html from the committed copy, swaps the feed layer for a
hostile one, regenerates, and asserts on what actually landed in the HTML.
"""
import os
import re
import sys
import json
import shutil
import subprocess
import importlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)
CACHE = os.path.join(ROOT, '_homepage_live_cache.json')


def reset():
    subprocess.run(['git', 'checkout', '--', 'index.html'], cwd=ROOT, check=True)


def page():
    return open('index.html', encoding='utf-8').read()


def scoreboard():
    return re.search(r'<div class="scores">.*?</div>\s*</div>\s*</section>', page(), re.S).group(0)


def rail():
    return re.search(r'<div class="tk-rail">.*?</div>', page(), re.S).group(0)


def run(mod, label):
    try:
        mod.main()
        print('  generated ok')
    except Exception as exc:
        print('  GENERATOR CRASHED:', exc.__class__.__name__, exc)
        return False
    body = page()
    checks = {
        'page intact': '</html>' in body and body.count('<div class="scores">') == 1,
        'three tiles': len(re.findall(r'<a class="sc-game', scoreboard())) == 3,
        'wire populated': len(re.findall(r'<span class="tk-i', rail())) == 12,
        'no August rot': 'Camp opens this month' not in body and 'August 3' not in rail(),
    }
    for name, ok in checks.items():
        print('   %-16s %s' % (name, 'PASS' if ok else 'FAIL'))
    return all(checks.values())


results = {}

print('1. LIVE FEEDS')
reset()
if os.path.exists(CACHE):
    os.remove(CACHE)
import _gen_homepage_live as live
results['live'] = run(live, 'live')
live_tiles = re.findall(r'<span class="sc-run[^"]*">(\d+)</span>', scoreboard())
print('   scores rendered:', live_tiles)

print('2. EVERY FEED DOWN, NO CACHE')
reset()
if os.path.exists(CACHE):
    os.remove(CACHE)
importlib.reload(live)
live.fetch = lambda url: (_ for _ in ()).throw(OSError('network down'))
results['down'] = run(live, 'down')
print('   any score on the board:', bool(re.findall(r'sc-run[^"]*">\d', scoreboard())), '(expected False)')
results['down'] &= not re.findall(r'sc-run[^"]*">\d', scoreboard())

print('3. MALFORMED PAYLOADS')
reset()
importlib.reload(live)
live.fetch = lambda url: {'dates': 'not-a-list', 'team': None, 'events': [{'no': 'competitions'}]}
results['junk'] = run(live, 'junk')

print('4. STALE FEED, EVERY GAME SIX WEEKS OLD')
reset()
importlib.reload(live)
old = {'date': '2026-08-02', 'us': 'San Francisco Giants', 'them': 'Padres',
       'home': False, 'ours': 4, 'theirs': 5, 'won': False}


def stale_mlb(team):
    return {'final': dict(old), 'next': dict(old), 'record': '47-65'}


live.mlb_team = stale_mlb
live.espn_team = stale_mlb
results['stale'] = run(live, 'stale')
shown = re.findall(r'sc-run[^"]*">(\d+)<', scoreboard())
print('   stale scores leaked onto the page:', shown, '(expected [])')
print('   47-65 anywhere in the wire       :', '47-65' in rail(), '(expected False)')
results['stale'] &= not shown and '47-65' not in rail()

print('5. IDEMPOTENT')
reset()
importlib.reload(live)
live.main()
first = page()
live.main()
results['idempotent'] = (first == page())
print('   second run identical:', results['idempotent'])

reset()
if os.path.exists(CACHE):
    os.remove(CACHE)
print()
print('RESULTS:', json.dumps({k: bool(v) for k, v in results.items()}))
print('ALL PASS' if all(results.values()) else 'FAILURES PRESENT')
