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
    record = None
    for block in fetch('https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season=%d' % now.year)['records']:
        for t in block['teamRecords']:
            if t['team']['id'] == team['id']:
                record = '%d-%d' % (t['wins'], t['losses'])
    over = nxt is None and now.date().isoformat() > season['regularSeasonEndDate']
    return {'record': record, 'season': str(now.year), 'last': last, 'next': nxt, 'over': over}


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
    return {'record': sched['team'].get('recordSummary'), 'season': season,
            'last': last, 'next': nxt, 'over': False}


def strip(s, now):
    cell = '<div><b>%s</b> %s</div>'
    cells = []
    if s['record'] and set(s['record']) - set('0-'):   # skip 0-0 before opening night
        label = '%s final record' % s['season'] if s['over'] else '%s record' % s['season']
        cells.append(cell % (label, s['record']))
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
        open(path, 'w', encoding='utf-8', newline='').write(text)
        print('%-15s %s' % (team['hub'], re.sub(r'\s*<[^>]+>\s*', ' ', block.split('border-radius:10px">', 1)[1])[:180]))


if __name__ == '__main__':
    main()
