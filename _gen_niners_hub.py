#!/usr/bin/env python3
"""_gen_niners_hub.py: put a real schedule table on the 49ers season hub.

The hub was 688 words and the most linked page on the site at 23 in body inbound links, so
it attracted a navigational query it could not answer. This fills three marked regions on
the SAME URL, the way _gen_warriors_hub.py does for the Warriors: the next game, the shape
of the season, and the week by week table with results filling in as they are played.

Editorial and predictive material stays out. This page is the calendar.

    python _gen_niners_hub.py             refresh from the feed
    python _gen_niners_hub.py --check     fail if the page has drifted, change nothing

Failure order: live feed, then the cached pull, then leave the page untouched. A game is
only shown as final when the league has it final and the score parses, so a stale or half
written result never reaches the page.
"""
import os
import re
import sys
import json
import datetime
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(ROOT, 'articles', '49ers-2026-schedule-season-hub.html')
CACHE = os.path.join(ROOT, 'data', 'niners_schedule.json')
BASE = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/sf'
ABBR = 'sf'
PACIFIC = datetime.timezone(datetime.timedelta(hours=-7))
HOME_VENUE = "Levi's Stadium"
INTERNATIONAL = {'Melbourne Cricket Ground', 'Estadio Banorte', 'Estadio Azteca',
                 'Tottenham Hotspur Stadium', 'Wembley Stadium', 'Allianz Arena',
                 'Deutsche Bank Park', 'Santiago Bernabeu Stadium', 'Croke Park'}
MARKS = {
    'next': ('<!-- NEXT GAME START -->', '<!-- NEXT GAME END -->'),
    'shape': ('<!-- SEASON SHAPE START -->', '<!-- SEASON SHAPE END -->'),
    'table': ('<!-- SCHEDULE TABLE START -->', '<!-- SCHEDULE TABLE END -->'),
}


def fetch(url):
    # ESPN rejects a User-Agent it does not recognise, so send urllib's default
    with urllib.request.urlopen(urllib.request.Request(url), timeout=25) as r:
        return json.load(r)


def games():
    out = []
    data = fetch('%s/schedule?seasontype=2' % BASE)
    for ev in data.get('events', []):
        comp = ev['competitions'][0]
        sides = {}
        for c in comp['competitors']:
            sides['us' if c['team']['abbreviation'].lower() == ABBR else 'them'] = c
        if 'us' not in sides or 'them' not in sides:
            continue
        status = comp['status']['type']
        row = {'week': (ev.get('week') or {}).get('number'),
               'iso': ev['date'],
               'home': sides['us'].get('homeAway') == 'home',
               'them': sides['them']['team']['displayName'],
               'venue': comp.get('venue', {}).get('fullName', ''),
               'state': status.get('name', ''),
               'final': bool(status.get('completed')),
               'us_score': None, 'them_score': None, 'won': None}
        if row['final']:
            try:
                row['us_score'] = int((sides['us'].get('score') or {}).get('displayValue'))
                row['them_score'] = int((sides['them'].get('score') or {}).get('displayValue'))
                row['won'] = bool(sides['us'].get('winner'))
            except (TypeError, ValueError):
                row['final'] = False
        out.append(row)
    out.sort(key=lambda r: r['iso'])
    return out


def load():
    try:
        rows = games()
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        json.dump(rows, open(CACHE, 'w', encoding='utf-8'), indent=1)
        return rows, 'feed'
    except Exception as exc:
        print('feed failed (%s)' % exc.__class__.__name__)
        if os.path.exists(CACHE):
            return json.load(open(CACHE, encoding='utf-8')), 'cache'
        sys.exit('no feed and no cache, leaving the page untouched')


def local(iso):
    return datetime.datetime.fromisoformat(iso.replace('Z', '+00:00')).astimezone(PACIFIC)


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def clock(dt):
    return dt.strftime('%I:%M %p').lstrip('0').lower()


def next_block(rows):
    played = [r for r in rows if r['final']]
    upcoming = [r for r in rows if not r['final'] and local(r['iso']) > datetime.datetime.now(PACIFIC)]
    bits = []
    if upcoming:
        n = upcoming[0]
        when = local(n['iso'])
        bits.append('<b>Next up:</b> week %s, %s %s, %s at %s, %s.'
                    % (n['week'], 'vs' if n['home'] else 'at', esc(n['them']),
                       when.strftime('%A %B %d').replace(' 0', ' '), clock(when),
                       esc(n['venue'] or 'venue to be confirmed')))
    else:
        bits.append('<b>Next up:</b> nothing scheduled in the feed right now.')
    if played:
        wins = sum(1 for r in played if r['won'])
        bits.append(' Record %d-%d through %d game%s.'
                    % (wins, len(played) - wins, len(played), '' if len(played) == 1 else 's'))
    else:
        bits.append(' No games have been played yet.')
    return '\r\n  <p class="hub-next">%s</p>\r\n  ' % ''.join(bits)


def shape_block(rows):
    if not rows:
        return '\r\n  <p>The schedule is not published yet.</p>\r\n  '
    home = sum(1 for r in rows if r['home'])
    weeks = sorted(r['week'] for r in rows if r['week'])
    missing = [w for w in range(1, (max(weeks) if weeks else 0) + 1) if w not in weeks]
    first, last = local(rows[0]['iso']), local(rows[-1]['iso'])
    prime = [r for r in rows if local(r['iso']).hour >= 17]
    lines = ['<li><b>Opens</b> %s, %s %s.</li>'
             % (first.strftime('%A %B %d').replace(' 0', ' '),
                'vs' if rows[0]['home'] else 'at', esc(rows[0]['them']))]
    if missing:
        lines.append('<li><b>Bye</b> in week %s.</li>' % ', '.join(str(m) for m in missing))
    lines.append('<li><b>%d home, %d away</b>, finishing %s.</li>'
                 % (home, len(rows) - home, last.strftime('%B %d').replace(' 0', ' ')))
    lines.append('<li><b>%d games kicking at 5pm Pacific or later</b>, which is the prime time count.</li>'
                 % len(prime))
    # a home game that is not at Levi's, or a road game the league has moved abroad
    odd = []
    for r in rows:
        if r['home'] and r['venue'] and HOME_VENUE not in r['venue']:
            odd.append('%s at %s, a home game that is not at home' % (esc(r['them']), esc(r['venue'])))
        elif not r['home'] and r['venue'] and r['venue'] in INTERNATIONAL:
            odd.append('%s at %s' % (esc(r['them']), esc(r['venue'])))
    if odd:
        lines.append('<li><b>Not at Levi\'s and not a normal road trip:</b> %s.</li>' % '; '.join(odd))
    return ('\r\n  <ul class="hub-shape" style="margin:0 0 22px;padding-left:22px">\r\n    %s\r\n  </ul>\r\n  '
            % '\r\n    '.join(lines))


def table_block(rows):
    body = []
    for r in rows:
        when = local(r['iso'])
        if r['final']:
            result = '%s %d-%d' % ('W' if r['won'] else 'L',
                                   max(r['us_score'], r['them_score']),
                                   min(r['us_score'], r['them_score']))
        elif r['state'] == 'STATUS_SCHEDULED':
            result = clock(when)
        else:
            result = 'TBD'
        body.append('  <tr><td class="num">%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                    % (r['week'] or '', when.strftime('%a %b %d').replace(' 0', ' '),
                       'vs' if r['home'] else 'at', esc(r['them']), result))
    played = sum(1 for r in rows if r['final'])
    caption = ('San Francisco 49ers 2026 regular season, %d games as published by the league, '
               '%d played. All times Pacific.' % (len(rows), played))
    return ('\r\n  <div class="reftable" role="region" tabindex="0" aria-label="%s">\r\n'
            '  <table>\r\n  <caption>%s</caption>\r\n'
            '  <thead><tr><th class="num">Wk</th><th>Date</th><th>H/A</th><th>Opponent</th>'
            '<th>Result or kick</th></tr></thead>\r\n'
            '  <tbody>\r\n%s\r\n  </tbody>\r\n  </table>\r\n  </div>\r\n  '
            % (caption, caption, '\r\n'.join(body)))


def touch_modified(text):
    today = datetime.date.today().isoformat()
    return re.sub(r'"dateModified":"[^"]*"', '"dateModified":"%s"' % today, text, count=1)


def splice(text, key, block, check):
    start, end = MARKS[key]
    if start not in text:
        sys.exit('marker %s is missing from the article' % start)
    a, b = text.index(start) + len(start), text.index(end)
    if text[a:b] == block:
        return text, False
    if check:
        sys.exit('OUT OF DATE (%s): run _gen_niners_hub.py' % key)
    return text[:a] + block + text[b:], True


def main():
    check = '--check' in sys.argv
    rows, source = load()
    if not rows:
        sys.exit('feed returned no games, leaving the page untouched')
    text = open(ARTICLE, encoding='utf-8', newline='').read()
    changed = False
    for key, block in (('next', next_block(rows)), ('shape', shape_block(rows)),
                       ('table', table_block(rows))):
        text, did = splice(text, key, block, check)
        changed |= did
    if changed:
        open(ARTICLE, 'w', encoding='utf-8', newline='').write(touch_modified(text))
    print('%s: %d games listed, %d played (%s)'
          % ('rewrote' if changed else 'up to date', len(rows),
             sum(1 for r in rows if r['final']), source))


if __name__ == '__main__':
    main()
