#!/usr/bin/env python3
"""_gen_bay_bridge_series.py: keep the Bay Bridge Series page's numbers correct.

The page is prose plus one table, and the table is the part that changes. This pulls every
Giants against Athletics meeting from statsapi, writes the season by season rows and the
running totals into the marked region of the article, and leaves every word alone.

Adding next season's results is running this script. Nobody has to retype a record.

    python _gen_bay_bridge_series.py            refresh from the feed
    python _gen_bay_bridge_series.py --check    fail if the page is out of date, change nothing

If the feed is unreachable the cached pull in data/bay_bridge_series.json is used, and if
that is missing too the script exits without touching the page. A stale table is worse
than no update.
"""
import os
import re
import sys
import json
import time
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(ROOT, 'articles', 'bay-bridge-series-giants-athletics-history.html')
CACHE = os.path.join(ROOT, 'data', 'bay_bridge_series.json')
GIANTS, ATHLETICS = 137, 133
FIRST_SEASON = 1997          # interleague play begins
START = '<!-- SERIES TABLE START -->'
END = '<!-- SERIES TABLE END -->'


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url), timeout=30) as r:
        return json.load(r)


def pull(last_season):
    rows = []
    for year in range(FIRST_SEASON, last_season + 1):
        url = ('https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId=%d&opponentId=%d'
               '&startDate=%d-01-01&endDate=%d-12-31&gameType=R'
               % (GIANTS, ATHLETICS, year, year))
        data = fetch(url)
        for day in data.get('dates', []):
            for g in day['games']:
                if g['status']['detailedState'] != 'Final':
                    continue
                away, home = g['teams']['away'], g['teams']['home']
                sf_home = home['team']['id'] == GIANTS
                sf = home if sf_home else away
                oak = away if sf_home else home
                if sf.get('score') is None or oak.get('score') is None:
                    continue
                rows.append({'year': year, 'date': day['date'], 'sf': sf['score'],
                             'oak': oak['score'], 'sf_home': sf_home,
                             'venue': g.get('venue', {}).get('name', '')})
        time.sleep(0.1)
    return rows


def load():
    season = time.localtime().tm_year
    try:
        rows = pull(season)
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        json.dump(rows, open(CACHE, 'w', encoding='utf-8'), indent=1)
        return rows, 'feed'
    except Exception as exc:
        print('feed failed (%s), falling back to the cache' % exc.__class__.__name__)
        if os.path.exists(CACHE):
            return json.load(open(CACHE, encoding='utf-8')), 'cache'
        sys.exit('no feed and no cache, leaving the page untouched')


def seasons(rows):
    out = {}
    for r in rows:
        s = out.setdefault(r['year'], {'g': 0, 'sf': 0, 'oak': 0, 'venues': set()})
        s['g'] += 1
        s['venues'].add(r['venue'])
        if r['sf'] > r['oak']:
            s['sf'] += 1
        elif r['oak'] > r['sf']:
            s['oak'] += 1
    return out


def short_venue(name):
    """The Coliseum was renamed five times. Readers do not care, the table has no room."""
    if 'Coliseum' in name:
        return 'Coliseum'
    if 'Candlestick' in name or '3Com' in name:
        return 'Candlestick'
    if name in ('PacBell Park', 'SBC Park', 'AT&T Park', 'Oracle Park'):
        return 'Giants park'
    if 'Sutter' in name:
        return 'Sutter Health Park'
    return name


def render(rows):
    data = seasons(rows)
    sf_total = sum(v['sf'] for v in data.values())
    oak_total = sum(v['oak'] for v in data.values())
    body = []
    for year in sorted(data):
        v = data[year]
        if v['sf'] > v['oak']:
            who = 'Giants %d-%d' % (v['sf'], v['oak'])
        elif v['oak'] > v['sf']:
            who = "A's %d-%d" % (v['oak'], v['sf'])
        else:
            who = 'Split %d-%d' % (v['sf'], v['oak'])
        venues = ', '.join(sorted({short_venue(x) for x in v['venues']}))
        body.append('  <tr><td>%d</td><td class="num">%d</td><td class="num">%d</td>'
                    '<td class="num">%d</td><td>%s</td><td>%s</td></tr>'
                    % (year, v['g'], v['sf'], v['oak'], who, venues))

    first, last = min(data), max(data)
    caption = ('San Francisco Giants against the Athletics, regular season meetings %d to %d. '
               'Source: the official schedule and score for every game.' % (first, last))
    head = ('  <caption>%s</caption>\r\n'
            '  <thead><tr><th>Season</th><th class="num">Games</th><th class="num">Giants</th>'
            '<th class="num">A\'s</th><th>Season series</th><th>Where they played</th></tr></thead>'
            % caption)
    foot = ('  <tfoot><tr><td><b>%d to %d</b></td><td class="num"><b>%d</b></td>'
            '<td class="num"><b>%d</b></td><td class="num"><b>%d</b></td>'
            '<td colspan="2"><b>%s</b></td></tr></tfoot>'
            % (first, last, len(rows), sf_total, oak_total,
               'Giants lead the regular season series' if sf_total > oak_total
               else ("A's lead the regular season series" if oak_total > sf_total
                     else 'Dead even')))

    sf_home = [r for r in rows if r['sf_home']]
    oak_home = [r for r in rows if not r['sf_home']]
    splits = ('<p class="series-splits">Home and away, same source: the Giants are '
              '%d-%d in games at their own ballpark and %d-%d in games at the A\'s, '
              'which across %d meetings is about as close as a rivalry gets.</p>'
              % (sum(1 for r in sf_home if r['sf'] > r['oak']),
                 sum(1 for r in sf_home if r['oak'] > r['sf']),
                 sum(1 for r in oak_home if r['sf'] > r['oak']),
                 sum(1 for r in oak_home if r['oak'] > r['sf']),
                 len(rows)))

    table = ('\r\n  <div class="reftable" role="region" tabindex="0" aria-label="%s">\r\n'
             '  <table>\r\n%s\r\n  <tbody>\r\n%s\r\n  </tbody>\r\n%s\r\n  </table>\r\n'
             '  </div>\r\n\r\n  %s\r\n  ' % (caption, head, '\r\n'.join(body), foot, splits))
    return table, sf_total, oak_total, len(rows)


def main():
    check = '--check' in sys.argv
    rows, source = load()
    table, sf, oak, games = render(rows)
    text = open(ARTICLE, encoding='utf-8', newline='').read()
    a, b = text.index(START) + len(START), text.index(END)
    if text[a:b] == table:
        print('up to date: %d games, Giants %d, A\'s %d (%s)' % (games, sf, oak, source))
        return
    if check:
        sys.exit('OUT OF DATE: run _gen_bay_bridge_series.py')
    open(ARTICLE, 'w', encoding='utf-8', newline='').write(text[:a] + table + text[b:])
    print('rewrote the table: %d games, Giants %d, A\'s %d (%s)' % (games, sf, oak, source))


if __name__ == '__main__':
    main()
