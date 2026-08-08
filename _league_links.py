#!/usr/bin/env python3
"""_league_links.py - point each article's "More coverage" line at its league hub.

The league hubs (nfl/mlb/nba/nhl) were built with real content - mlb.html alone carries
136 cards - but they sit almost outside the internal link graph: ~18-20 inbound each,
against ~130 for the team hubs. The nav would not fix that; the nav only exists on 19 of
133 pages. The "More coverage" line at the foot of an article does exist on 81 of them,
sits inside <article>, and already answers "where do I go next" - it just never offered
the league page.

This inserts the matching league hub into that existing line, directly after the team
hub it already links. Nothing else on the page is touched: no nav, no header, no footer,
no hero, no card, no URL, no homepage.

The league is taken from the team hub the line already links, which is the editor's own
classification. If the line has no team hub, the slug prefix is used. If neither
identifies a league, the article is skipped rather than guessed at.

  python _league_links.py [--check]
"""
import os, re, sys, glob, json, collections

ROOT = os.path.dirname(os.path.abspath(__file__))

LEAGUE_OF_HUB = {
    'giants': ('mlb.html', 'Bay Area MLB'),
    'athletics': ('mlb.html', 'Bay Area MLB'),
    '49ers': ('nfl.html', 'Bay Area NFL'),
    'warriors': ('nba.html', 'Bay Area NBA'),
    'sharks': ('nhl.html', 'Bay Area NHL'),
}
# articles whose slug names the league but whose line links no team hub
SLUG_LEAGUE = [
    ('49ers-', 'nfl'), ('giants-', 'mlb'), ('athletics-', 'mlb'),
    ('warriors-', 'nba'), ('sharks-', 'nhl'),
    ('raiders-', 'nfl'), ('nfl-', 'nfl'), ('montana-young', 'nfl'),
    ('brandon-aiyuk', 'nfl'), ('jerry-rice', 'nfl'), ('flashback-the-catch', 'nfl'),
    ('lebron-curry', 'nba'), ('flashback-klay', 'nba'),
    ('barry-bonds', 'mlb'), ('jeff-kent', 'mlb'), ('bruce-bochy', 'mlb'),
    ('bryce-eldridge', 'mlb'), ('tony-vitello', 'mlb'),
    ('flashback-bumgarner', 'mlb'),
]
LEAGUE_NAME = {'nfl': 'Bay Area NFL', 'mlb': 'Bay Area MLB',
               'nba': 'Bay Area NBA', 'nhl': 'Bay Area NHL'}

LINE_RE = re.compile(r'(<p[^>]*>\s*More coverage:.*?</p>)', re.S)
STYLE = 'color:var(--accent2);font-weight:700'


def rd(p):
    return open(os.path.join(ROOT, p), encoding='utf-8', errors='strict').read()


def wr(p, s):
    full = os.path.join(ROOT, p)
    with open(full, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)
    b = open(full, 'rb').read()
    if b'\x00' in b or b.count(b'\xef\xbf\xbd'):
        raise SystemExit('corruption writing %s - ABORT' % p)


def league_for(slug, line):
    for hub, (href, label) in LEAGUE_OF_HUB.items():
        if 'href="../%s.html"' % hub in line:
            return href, label
    for prefix, lg in SLUG_LEAGUE:
        if slug.startswith(prefix):
            return lg + '.html', LEAGUE_NAME[lg]
    return None, None


def main():
    check = '--check' in sys.argv
    placed, no_line, no_league, already = [], [], [], []

    for f in sorted(glob.glob(os.path.join(ROOT, 'articles', '*.html'))):
        rel = 'articles/' + os.path.basename(f)
        slug = os.path.basename(f)[:-5]
        s = rd(rel)
        m = LINE_RE.search(s)
        if not m:
            no_line.append(slug)
            continue
        line = m.group(1)
        href, label = league_for(slug, line)
        if not href:
            no_league.append(slug)
            continue
        if 'href="../%s"' % href in line:
            already.append(slug)
            continue
        new_link = ('<a href="../%s" style="%s">%s</a>' % (href, STYLE, label))
        # sit the league hub straight after the team hub it already links
        anchors = list(re.finditer(r'<a href="\.\./[^"]+"[^>]*>.*?</a>', line, re.S))
        team_idx = None
        for i, a in enumerate(anchors):
            if any(('../%s.html' % hub) in a.group(0) for hub in LEAGUE_OF_HUB):
                team_idx = i
                break
        if team_idx is None:
            team_idx = 0                      # no team hub: lead with the league
        at = anchors[team_idx].end()
        new_line = line[:at] + ' &middot; ' + new_link + line[at:]
        s = s.replace(line, new_line, 1)
        placed.append({'article': rel, 'league': href, 'label': label})
        if not check:
            wr(rel, s)

    json.dump({'placed': placed, 'no_more_coverage_line': no_line,
               'no_league_identified': no_league, 'already_linked': already},
              open(os.path.join(ROOT, '_league_links_report.json'), 'w',
                   encoding='utf-8'), indent=1)
    by = collections.Counter(p['league'] for p in placed)
    print('%s  placed %d  |  no line %d  |  league not identified %d  |  already %d'
          % ('CHECK' if check else 'APPLIED', len(placed), len(no_line),
             len(no_league), len(already)))
    print('  by league: %s' % dict(by))
    if no_league:
        print('  skipped (no league): %s' % ', '.join(no_league[:8]))
    if no_line:
        print('  skipped (no More coverage line): %s' % ', '.join(no_line[:8]))


if __name__ == '__main__':
    main()
