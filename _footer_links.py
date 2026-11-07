#!/usr/bin/env python3
"""_footer_links.py: one row of the pages people actually search for, in every footer.

Search Console shows the demand is for the injury reports, the schedules and the reference
pages, and those pages sit deep behind the daily columns. A plain footer row hands each of
them a link from every page on the site. Idempotent, so it's safe in the daily refresh.

  python _footer_links.py
"""
import glob, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
MARK = re.compile(r'<!-- foot-pop -->.*?<!-- /foot-pop -->\r?\n?', re.S)
LINKS = [
    ('49ers-injury-report.html', '49ers Injury Report'),
    ('warriors-injury-report.html', 'Warriors Injury Report'),
    ('49ers-2026-schedule-season-hub.html', '49ers Schedule'),
    ('warriors-2026-27-schedule-season-hub.html', 'Warriors Schedule'),
    ('49ers-playoff-super-bowl-history.html', '49ers Super Bowl History'),
    ('bay-area-championships-complete-list-by-team.html', 'Bay Area Championships'),
    ('levis-stadium-guide-parking-transit-bag-policy.html', "Levi's Stadium Guide"),
    ('chase-center-guide-warriors-arena.html', 'Chase Center Guide'),
]


def row(prefix):
    items = ' &middot; '.join('<a href="%s%s">%s</a>' % (prefix, f, t) for f, t in LINKS)
    return '<!-- foot-pop --><div class="foot-pop"><b>Most searched:</b> %s</div><!-- /foot-pop -->\r\n' % items


def main():
    os.chdir(ROOT)
    n = 0
    for f in glob.glob('*.html') + glob.glob('articles/*.html') + glob.glob('daily/*.html'):
        t = open(f, encoding='utf-8', newline='').read()
        m = re.search(r'<footer class="(site-footer|desk-foot)">', t)
        if not m or 'http-equiv="refresh"' in t:
            continue
        prefix = '' if f.startswith('articles') else ('../articles/' if f.startswith('daily') else 'articles/')
        new = MARK.sub('', t)
        i = new.index(m.group(0)) + len(m.group(0))
        new = new[:i] + '\r\n' + row(prefix.replace('\\', '/')) + new[i:].lstrip('\r\n')
        if new != t:
            open(f, 'w', encoding='utf-8', newline='').write(new)
            n += 1
    print('footer links updated on %d pages' % n)


if __name__ == '__main__':
    main()
