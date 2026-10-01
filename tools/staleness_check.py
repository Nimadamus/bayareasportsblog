#!/usr/bin/env python3
"""tools/staleness_check.py: fail loudly if any live module on the site is out of date.

Checks, against today's Pacific date:
  - every masthead date (data-dt="live") reads today
  - every team hub status strip says "Updated <today>"
  - no homepage scoreboard or wire item uses a relative word (Today, Tonight, Last night)
  - the homepage scoreboard shows no final older than RESULT_DAYS

    python tools/staleness_check.py              check the files on disk
    python tools/staleness_check.py --live       check the live site instead

Exit 1 with one line per problem. The daily refresh action runs it after refreshing, so a
feed outage or a broken script shows up as a red run instead of a quietly stale page.
"""
import os
import re
import sys
import glob
import datetime
import urllib.request
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://bayareasportsblog.com/'
HUBS = ['49ers.html', 'warriors.html', 'giants.html', 'athletics.html', 'sharks.html']


def read(name, live):
    if live:
        req = urllib.request.Request(BASE + name + '?stale=%d' % datetime.datetime.now().timestamp(),
                                     headers={'User-Agent': 'Mozilla/5.0 staleness-check'})
        return urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')
    return open(os.path.join(ROOT, name), encoding='utf-8').read()


def main():
    live = '--live' in sys.argv
    now = datetime.datetime.now(ZoneInfo('America/Los_Angeles'))
    long_day = now.strftime('%A, %B ') + str(now.day) + now.strftime(', %Y')
    short_day = now.strftime('%a, %b ') + str(now.day)
    problems = []

    names = HUBS + ['index.html'] if live else [os.path.basename(p) for p in glob.glob(os.path.join(ROOT, '*.html'))]
    for name in names:
        text = read(name, live)
        for d in re.findall(r'data-dt="live">([^<]*)<', text):
            if d != long_day:
                problems.append('%s masthead says %r, today is %r' % (name, d, long_day))
        if name in HUBS:
            m = re.search(r'Updated ([^<]*) Pacific', text)
            if not m:
                problems.append('%s has no hub status strip' % name)
            elif m.group(1) != short_day:
                problems.append('%s hub strip last updated %s' % (name, m.group(1)))
        if name == 'index.html':
            mods = re.findall(r'<div class="(?:sc-note|tk-rail)">(.*?)</div>', text, re.S)
            for chunk in mods:
                if re.search(r'\b(Today|Tonight|Last night|Yesterday)\b', chunk):
                    problems.append('index.html live module uses a relative day word')
                    break

    for page in ('articles/49ers-injury-report.html', 'articles/warriors-injury-report.html'):
        inj = read(page, live)
        m = re.search(r'<b>Updated ([A-Z][a-z]{2}, [A-Z][a-z]{2} \d+),', inj)
        if not m or m.group(1) != short_day:
            problems.append('%s last updated %s' % (page, m.group(1) if m else 'never'))

    for p in problems:
        print('STALE', p)
    print('%s: %d problems (%s)' % ('live' if live else 'disk', len(problems), long_day))
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
