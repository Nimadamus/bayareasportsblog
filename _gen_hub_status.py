#!/usr/bin/env python3
"""_gen_hub_status.py: a live status strip at the top of every team hub.

The hub intros are prose and prose goes stale. This strip is the part that has to be true
today: the record, the last game, the next game. Every value comes out of a live feed:

  Giants, Athletics   statsapi.mlb.com   schedule, standings, season dates
  49ers, Warriors     site.api.espn.com  schedule and record
  Sharks              site.api.espn.com  same

Dates and times are converted to Pacific before they are written. Nothing relative
("today", "last night") is ever written, because the pages are static and the words would
be wrong the next morning. If a feed fails, that hub keeps the strip it already has.

    python _gen_hub_status.py
"""
import os
import re
import json
import datetime
import urllib.request
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.abspath(__file__))
PACIFIC = ZoneInfo('America/Los_Angeles')
UA = {'User-Agent': 'python-requests/2.31'}   # ESPN 403s browser style agents
START, END = '<!-- hub-status:start -->', '<!-- hub-status:end -->'

TEAMS = [
    {'hub': 'giants.html', 'src': 'mlb', 'id': 137},
    {'hub': 'athletics.html', 'src': 'mlb', 'id': 133},
    {'hub': '49ers.html', 'src': 'espn', 'path': 'football/nfl', 'abbr': 'sf'},
    {'hub': 'warriors.html', 'src': 'espn', 'path': 'basketball/nba', 'abbr': 'gs'},
    {'hub': 'sharks.html', 'src': 'espn', 'path': 'hockey/nhl', 'abbr': 'sj'},
]


DIVISIONS = {200: 'AL West', 201: 'AL East', 202: 'AL Central',
             203: 'NL West', 204: 'NL East', 205: 'NL Central'}


def ordinal(n):
    return '%d%s' % (n, 'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th'))


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode('utf-8'))


def pacific(utc):
    return datetime.datetime.strptime(utc[:16], '%Y-%m-%dT%H:%M').replace(
        tzinfo=datetime.timezone.utc).astimezone(PACIFIC)


def day(dt):
    return dt.strftime('%a, %b ') + str(dt.day)


def clock(dt):
    return dt.strftime('%I:%M %p').lstrip('0')


def mlb(team, now):
    season = fetch('https://statsapi.mlb.com/api/v1/seasons/%d?sportId=1' % now.year)['seasons'][0]
    start = (now - datetime.timedelta(days=60)).date()
    end = (now + datetime.timedelta(days=30)).date()
    data = fetch('https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId=%d&startDate=%s&endDate=%s'
                 % (team['id'], start, end))
    last = nxt = None
    for d in data.get('dates', []):
        for g in d['games']:
            home = g['teams']['home']['team']['id'] == team['id']
            us, them = (g['teams']['home'], g['teams']['away']) if home else (g['teams']['away'], g['teams']['home'])
            row = {'when': pacific(g['gameDate']), 'home': home, 'them': them['team']['name']}
            state = g['status']['abstractGameState']
            if state == 'Final' and us.get('score') is not None:
                row.update(ours=us['score'], theirs=them['score'])
                last = row
            elif state == 'Preview' and nxt is None:
                nxt = row
    record = standing = None
    for block in fetch('https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season=%d' % now.year)['records']:
        for t in block['teamRecords']:
            if t['team']['id'] == team['id']:
                record = '%d-%d' % (t['wins'], t['losses'])
                div = DIVISIONS.get(block.get('division', {}).get('id'))
                if div and t.get('divisionRank'):
                    standing = '%s in %s' % (ordinal(int(t['divisionRank'])), div)
    over = nxt is None and now.date().isoformat() > season['regularSeasonEndDate']
    return {'record': record, 'season': str(now.year), 'last': last, 'next': nxt, 'over': over,
            'standing': standing}


def espn(team, now):
    sched = fetch('https://site.api.espn.com/apis/site/v2/sports/%s/teams/%s/schedule'
                  % (team['path'], team['abbr']))
    last = nxt = None
    for ev in sched.get('events', []):
        comp = ev['competitions'][0]
        sides = {('us' if c['team']['abbreviation'].lower() == team['abbr'] else 'them'): c
                 for c in comp['competitors']}
        if len(sides) != 2:
            continue
        kind = (ev.get('seasonType') or {}).get('name', '')
        row = {'when': pacific(ev['date']), 'home': sides['us'].get('homeAway') == 'home',
               'them': sides['them']['team']['displayName'],
               'pre': kind.lower().startswith('pre')}
        status = comp['status']['type']
        if status.get('completed'):
            try:
                row.update(ours=int(sides['us']['score']['displayValue']),
                           theirs=int(sides['them']['score']['displayValue']))
            except (KeyError, TypeError, ValueError):
                continue
            last = row
        elif nxt is None and status.get('name') == 'STATUS_SCHEDULED':
            nxt = row
    season = (sched.get('requestedSeason') or {}).get('displayName', str(now.year))
    info = fetch('https://site.api.espn.com/apis/site/v2/sports/%s/teams/%s'
                 % (team['path'], team['abbr']))['team']
    return {'record': sched['team'].get('recordSummary'), 'season': season,
            'last': last, 'next': nxt, 'over': False, 'standing': info.get('standingSummary')}


def strip(s, now):
    cell = '<div><b>%s</b> %s</div>'
    cells = []
    if s['record'] and set(s['record']) - set('0-'):   # skip 0-0 before opening night
        label = '%s final record' % s['season'] if s['over'] else '%s record' % s['season']
        cells.append(cell % (label, s['record']))
        if s.get('standing'):   # only once games count, a 0-0 rank is alphabetical noise
            cells.append(cell % ('Standing', s['standing']))
    if s['last']:
        g = s['last']
        res = 'W' if g['ours'] > g['theirs'] else ('L' if g['ours'] < g['theirs'] else 'T')
        cells.append(cell % ('Last game', '%s %d-%d %s %s, %s' % (
            res, g['ours'], g['theirs'], 'vs' if g['home'] else 'at', g['them'], day(g['when']))))
    if s['next']:
        g = s['next']
        cells.append(cell % ('Next game', '%s, %s %s %s%s' % (
            day(g['when']), clock(g['when']), 'vs' if g['home'] else 'at', g['them'],
            ' (preseason)' if g.get('pre') else '')))
    elif s['over']:
        cells.append(cell % ('Status', 'offseason'))
    cells.append('<div style="color:var(--muted)">Updated %s Pacific</div>' % day(now))
    return (START + '\r\n<section class="zone tight"><div class="wrap">'
            '<div style="display:flex;flex-wrap:wrap;gap:8px 28px;font-size:15px;line-height:1.5;'
            'padding:12px 16px;border:1px solid var(--line,rgba(127,127,127,.25));border-radius:10px">'
            + ''.join(cells) + '</div></div></section>\r\n' + END)

# The reference pages each hub should always point at, grouped the way a reader looks for
# them. Anchors describe the page in plain words, they are not keyword strings. A slug that
# no longer exists on disk is dropped rather than linked.
KSTART, KEND = '<!-- hub-keys:start -->', '<!-- hub-keys:end -->'
KEYPAGES = {
    '49ers.html': [
        ('This season', [('49ers-2026-schedule-season-hub', '2026 schedule and results'),
                         ('49ers-2026-roster-depth-chart', 'Roster and depth chart'),
                         ('49ers-injury-report', 'Injury report'),
                         ('49ers-2026-season-preview-roster-schedule-questions', 'Season preview')]),
        ('Players', [('brock-purdy-career-passer-rating-where-he-ranks', 'Where Brock Purdy ranks all time'),
                     ('49ers-brock-purdy-highest-passer-rating-nfl-history-1500-attempts', 'Purdy and the passer rating record')]),
        ('History', [('49ers-dynasty-team-of-the-decade', 'The 1980s dynasty'),
                     ('montana-young-49ers-quarterback-controversy', 'Montana and Young'),
                     ('flashback-the-catch-1982', 'The Catch'),
                     ('candlestick-park-history-wind-the-catch-demolition', 'Candlestick Park'),
                     ('bay-area-championships-complete-list-by-team', 'Every Bay Area title')]),
    ],
    'warriors.html': [
        ('This season', [('warriors-2026-27-schedule-season-hub', '2026-27 schedule and results'),
                         ('warriors-2026-27-roster-depth-chart', 'Roster and depth chart'),
                         ('warriors-2026-27-projected-rotation', 'Projected rotation'),
                         ('warriors-roster-construction-cap-sheet-2026-27', 'Cap sheet'),
                         ('warriors-2026-27-season-outlook', 'Season outlook')]),
        ('Players', [('stephen-curry-career-records-three-pointers', 'Stephen Curry career records'),
                     ('stephen-curry-two-year-116-million-extension-warriors', "Curry's extension through 2029")]),
        ('History and venues', [('warriors-championship-history', 'Championship history'),
                                ('warriors-73-9-best-record-ever-added-durant', 'The 73-9 season'),
                                ('oracle-arena-roaracle-history-oakland-warriors', 'Oracle Arena'),
                                ('chase-center-guide-warriors-arena', 'Chase Center guide')]),
    ],
    'giants.html': [
        ('This season', [('giants-2026-season-hub-results-coverage', '2026 season results'),
                         ('giants-2026-roster-depth-chart', 'Roster and depth chart'),
                         ('giants-2027-farm-system-bright-future', 'The farm system and 2027')]),
        ('Players', [('bryce-eldridge-giants-future-franchise-first-baseman-july-2026', 'Bryce Eldridge'),
                     ('josuar-gonzalez-giants-top-prospect-18-year-old-shortstop', 'Josuar Gonzalez'),
                     ('barry-bonds-giants-home-run-king', 'Barry Bonds'),
                     ('jeff-kent-giants-mvp-second-baseman', 'Jeff Kent')]),
        ('History and venues', [('giants-dynasty-even-year-magic', 'The even year titles'),
                                ('flashback-bumgarner-2014-world-series', 'Bumgarner in 2014'),
                                ('giants-1993-pennant-race-salomon-torres-final-day', 'The 1993 race'),
                                ('bay-bridge-series-giants-athletics-history', 'Bay Bridge Series'),
                                ('oracle-park-mccovey-cove-splash-hits-guide', 'Oracle Park and McCovey Cove'),
                                ('candlestick-park-history-wind-the-catch-demolition', 'Candlestick Park')]),
    ],
    'athletics.html': [
        ('This season', [('athletics-2026-roster-depth-chart', 'Roster and depth chart'),
                         ('athletics-2027-outlook-kurtz-de-vries-injuries', 'Looking ahead to 2027')]),
        ('The move', [('athletics-oakland-sacramento-las-vegas-timeline', 'Oakland to Las Vegas timeline'),
                      ('sutter-health-park-mlb-guide-dimensions-capacity', 'Sutter Health Park guide')]),
        ('History', [('oakland-athletics-legacy-what-the-bay-area-lost', 'What Oakland lost'),
                     ('oakland-coliseum-history-what-happens-to-it-now', 'The Oakland Coliseum'),
                     ('bay-bridge-series-giants-athletics-history', 'Bay Bridge Series')]),
    ],
    'sharks.html': [
        ('This season', [('sharks-2026-27-schedule-season-hub', '2026-27 schedule'),
                         ('sharks-2026-27-roster-depth-chart', 'Roster and depth chart')]),
        ('Players', [('macklin-celebrini-sharks-records-contract', 'Macklin Celebrini by the numbers')]),
        ('History', [('when-were-the-san-jose-sharks-founded', 'How the Sharks were founded'),
                     ('sharks-playoff-history', 'Playoff history'),
                     ('san-jose-sharks-history-no-stanley-cup', 'Franchise history')]),
    ],
}


def keys_block(hub):
    rows = []
    for group, links in KEYPAGES[hub]:
        found = [(s, a) for s, a in links if os.path.exists(os.path.join(ROOT, 'articles', s + '.html'))]
        if found:
            rows.append('<div><b>%s:</b> %s</div>' % (group, ' &middot; '.join(
                '<a href="articles/%s.html" style="color:var(--gold);text-decoration:underline;'
                'text-underline-offset:3px">%s</a>' % (s, a) for s, a in found)))
    return (KSTART + '\r\n<section class="zone tight"><div class="wrap">'
            '<div style="display:grid;gap:6px;font-size:15px;line-height:1.55">'
            + ''.join(rows) + '</div></div></section>\r\n' + KEND)


def main():
    now = datetime.datetime.now(PACIFIC)
    for team in TEAMS:
        path = os.path.join(ROOT, team['hub'])
        text = open(path, encoding='utf-8', newline='').read()
        try:
            s = (mlb if team['src'] == 'mlb' else espn)(team, now)
        except Exception as exc:
            print('%-15s FEED FAILED (%s), strip left as is' % (team['hub'], exc.__class__.__name__))
            continue
        block = strip(s, now)
        if START in text:
            text = re.sub(re.escape(START) + '.*?' + re.escape(END), lambda m: block, text, flags=re.S)
        else:
            # first run: directly above the hub's intro section
            m = re.search(r'<section class="zone"><div class="wrap">\s*<div class="sec-head"><div><h2>', text)
            text = text[:m.start()] + block + '\r\n' + text[m.start():]
        kb = keys_block(team['hub'])
        if KSTART in text:
            text = re.sub(re.escape(KSTART) + '.*?' + re.escape(KEND), lambda m: kb, text, flags=re.S)
        else:
            text = text.replace(END, END + '\r\n' + kb, 1)
        open(path, 'w', encoding='utf-8', newline='').write(text)
        print('%-15s %s' % (team['hub'], re.sub(r'\s*<[^>]+>\s*', ' ', block.split('border-radius:10px">', 1)[1])[:180]))


if __name__ == '__main__':
    main()
