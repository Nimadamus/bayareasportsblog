#!/usr/bin/env python3
"""_nav_injuries.py: put "Injuries" in the main nav of every page, pointing at the
Bay Area injury report. Idempotent, so it runs in the daily refresh and catches new pages.

  root pages     desk teamnav: inserted right after the Hall of Fame link
  articles/      classic nav:  inserted right before History
  daily/         classic nav:  inserted right before History

  python _nav_injuries.py
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
HUB = 'bay-area-injury-report.html'
DESK = re.compile(r'(\r?\n)([ \t]*)(<a(?: class="on")? data-t="house" href="bay-area-hall-of-fame\.html">Hall of Fame</a>)')
CLASSIC = re.compile(r'(\r?\n)([ \t]*)(<li><a href="\.\./history\.html">History</a></li>)')


def main():
    os.chdir(ROOT)
    n = 0
    for f in glob.glob('*.html') + glob.glob('articles/*.html') + glob.glob('daily/*.html'):
        t = open(f, encoding='utf-8', newline='').read()
        if 'http-equiv="refresh"' in t or 'injury-report.html">Injuries</a>' in t:
            continue
        if f.startswith('articles'):
            on = ' class="on"' if os.path.basename(f) == HUB else ''
            new = CLASSIC.sub(lambda m: '%s%s<li><a%s href="%s">Injuries</a></li>%s%s%s' % (
                m.group(1), m.group(2), on, HUB, m.group(1), m.group(2), m.group(3)), t, count=1)
        elif f.startswith('daily'):
            new = CLASSIC.sub(lambda m: '%s%s<li><a href="../articles/%s">Injuries</a></li>%s%s%s' % (
                m.group(1), m.group(2), HUB, m.group(1), m.group(2), m.group(3)), t, count=1)
        else:
            new = DESK.sub(lambda m: '%s%s%s%s%s<a data-t="house" href="articles/%s">Injuries</a>' % (
                m.group(1), m.group(2), m.group(3), m.group(1), m.group(2), HUB), t, count=1)
        if new != t:
            open(f, 'w', encoding='utf-8', newline='').write(new)
            n += 1
    print('nav injuries link added to %d pages' % n)


if __name__ == '__main__':
    main()
