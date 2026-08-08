#!/usr/bin/env python3
"""_league_link.py - add the matching league hub to each article's "More coverage" line.

The league hubs (nfl/mlb/nba/nhl) carry real content - mlb.html alone lists 136 stories -
but almost no internal authority: 18-20 inbound links each against roughly 130 for the
team hubs. The site nav only exists on 19 of 133 pages, so putting them there buys very
little. The "More coverage" line at the end of an article is on 81 of them, already sits
inside <article>, and already answers "where do I go next" - it just never offered the
league page.

This inserts one link into that existing line, immediately after the team-section link:

  More coverage: Giants section  ->  Giants section - Bay Area MLB - ... home

The league is derived from the article's own subject. Articles with no league (regional
history, the welcome post) get nothing, and the 22 articles that have no "More coverage"
line are left alone rather than having a new element injected into them.

  python _league_link.py --check     report, write nothing
  python _league_link.py             apply
"""
import os, re, sys, glob, json

ROOT = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(ROOT, 'articles')

LEAGUE = {'nfl': 'Bay Area NFL', 'mlb': 'Bay Area MLB',
          'nba': 'Bay Area NBA', 'nhl': 'Bay Area NHL'}

# team hub in the line -> league hub
BY_TEAM_LINK = {'49ers': 'nfl', 'giants': 'mlb', 'athletics': 'mlb',
                'warriors': 'nba', 'sharks': 'nhl'}

# articles whose league is obvious from the subject but whose "More coverage" line
# points at a section rather than a team (flashbacks, bayarea, history, columns)
BY_SLUG = [
    (re.compile(r'^(49ers|raiders)-'), 'nfl'),
    (re.compile(r'^(giants|athletics)-'), 'mlb'),
    (re.compile(r'^(warriors|sharks)-'), 'nhl_or_nba'),   # resolved below
    (re.compile(r'^flashback-the-catch'), 'nfl'),
    (re.compile(r'^flashback-klay'), 'nba'),
    (re.compile(r'^flashback-bumgarner'), 'mlb'),
    (re.compile(r'^(montana-young|brandon-aiyuk|jerry-rice|nfl-blackballed)'), 'nfl'),
    (re.compile(r'^(barry-bonds|jeff-kent|bruce-bochy|bryce-eldridge|tony-vitello)'), 'mlb'),
    (re.compile(r'^lebron-curry'), 'nba'),
]

LINE_RE = re.compile(r'(<p[^>]*>More coverage:.*?</p>)', re.S)
TEAM_LINK_RE = re.compile(r'(<a href="\.\./([a-z0-9\-]+)\.html"[^>]*>[^<]*</a>)')
STYLE = ' style="color:var(--accent2);font-weight:700"'


def league_for(slug, line):
    for m in TEAM_LINK_RE.finditer(line):
        t = m.group(2)
        if t in BY_TEAM_LINK:
            return BY_TEAM_LINK[t]
    for rx, lg in BY_SLUG:
        if rx.match(slug):
            if lg == 'nhl_or_nba':
                return 'nhl' if slug.startswith('sharks-') else 'nba'
            return lg
    return None


def rd(p):
    return open(p, encoding='utf-8', errors='strict').read()


def wr(p, s):
    with open(p, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)
    b = open(p, 'rb').read()
    if b'\x00' in b or b.count(b'\xef\xbf\xbd'):
        raise SystemExit('corruption writing %s - ABORT' % p)


def main():
    check = '--check' in sys.argv
    done, skipped, noline, noleague = [], [], [], []

    for f in sorted(glob.glob(os.path.join(ART, '*.html'))):
        slug = os.path.basename(f)[:-5]
        s = rd(f)
        m = LINE_RE.search(s)
        if not m:
            noline.append(slug)
            continue
        line = m.group(1)
        lg = league_for(slug, line)
        if not lg:
            noleague.append(slug)
            continue
        if ('../%s.html' % lg) in line:
            skipped.append(slug)
            continue
        anchor = '<a href="../%s.html"%s>%s</a>' % (lg, STYLE, LEAGUE[lg])
        tm = TEAM_LINK_RE.search(line)
        if tm and tm.group(2) in BY_TEAM_LINK:
            new_line = line[:tm.end()] + ' &middot; ' + anchor + line[tm.end():]
        else:
            # no team link in the line: sit the league link before the home link
            hm = re.search(r'<a href="\.\./index\.html"', line)
            if not hm:
                noleague.append(slug)
                continue
            new_line = line[:hm.start()] + anchor + ' &middot; ' + line[hm.start():]
        s = s.replace(line, new_line, 1)
        done.append({'slug': slug, 'league': lg})
        if not check:
            wr(f, s)

    json.dump({'added': done, 'already_had': skipped,
               'no_more_coverage_line': noline, 'no_league': noleague},
              open(os.path.join(ROOT, '_league_link_report.json'), 'w', encoding='utf-8'),
              indent=1)
    by = {}
    for d in done:
        by[d['league']] = by.get(d['league'], 0) + 1
    print('%s  added %d league links  %s'
          % ('CHECK' if check else 'APPLIED', len(done), by))
    print('  already had one: %d' % len(skipped))
    print('  no "More coverage" line (left alone): %d' % len(noline))
    print('  no league (regional/house pieces): %d  %s'
          % (len(noleague), noleague[:6]))


if __name__ == '__main__':
    main()
