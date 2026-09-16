#!/usr/bin/env python3
"""_gen_warriors_hub.py: keep the Warriors schedule hub current.

The hub is a schedule page and nothing else. It answers when the next game is, who it is
against, and what happened in the ones already played. The argument about how good this
roster is lives in warriors-2026-27-season-outlook and the two pages are deliberately kept
apart, so nothing in here predicts anything.

Everything is read from site.api.espn.com and written between markers. The prose around
the markers is never touched.

    python _gen_warriors_hub.py             refresh from the feed
    python _gen_warriors_hub.py --check     fail if the page has drifted, change nothing

Failure behaviour, in order: the live feed, then the cached pull in
data/warriors_schedule.json, then nothing at all. The page is never left showing a result
the feed did not give us, and a game whose status is not final never gets a score.
"""
import os
import re
import sys
import json
import time
import datetime
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
ARTICLE = os.path.join(ROOT, 'articles', 'warriors-2026-27-schedule-season-hub.html')
CACHE = os.path.join(ROOT, 'data', 'warriors_schedule.json')
BASE = 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/gs'
ABBR = 'gs'
PACIFIC = datetime.timezone(datetime.timedelta(hours=-7))
MARKS = {
    'next': ('<!-- NEXT GAME START -->', '<!-- NEXT GAME END -->'),
    'table': ('<!-- SCHEDULE TABLE START -->', '<!-- SCHEDULE TABLE END -->'),
    'shape': ('<!-- SCHEDULE SHAPE START -->', '<!-- SCHEDULE SHAPE END -->'),
}


def fetch(url):
    # ESPN rejects a User-Agent it does not recognise, so send urllib's default
    with urllib.request.urlopen(urllib.request.Request(url), timeout=25) as r:
        return json.load(r)


def games():
    out = []
    for season_type, label in ((1, 'Preseason'), (2, 'Regular season')):
        data = fetch('%s/schedule?seasontype=%d' % (BASE, season_type))
        for ev in data.get('events', []):
            comp = ev['competitions'][0]
            sides = {}
            for c in comp['competitors']:
                sides['us' if c['team']['abbreviation'].lower() == ABBR else 'them'] = c
            if 'us' not in sides or 'them' not in sides:
                continue
            status = comp['status']['type']
            row = {
                'kind': label,
                'iso': ev['date'],
                'home': sides['us'].get('homeAway') == 'home',
                'them': sides['them']['team']['displayName'],
                'venue': comp.get('venue', {}).get('fullName', ''),
                'state': status.get('name', ''),
                'final': bool(status.get('completed')),
                'us_score': None, 'them_score': None, 'won': None,
            }
            if row['final']:
                try:
                    row['us_score'] = int((sides['us'].get('score') or {}).get('displayValue'))
                    row['them_score'] = int((sides['them'].get('score') or {}).get('displayValue'))
                    row['won'] = bool(sides['us'].get('winner'))
                except (TypeError, ValueError):
                    row['final'] = False       # a final we cannot read is not a final
            out.append(row)
    out.sort(key=lambda r: r['iso'])
    return out


def record():
    try:
        info = fetch(BASE)['team']
        for item in info.get('record', {}).get('items', []):
            if item.get('summary'):
                return item['summary']
    except Exception:
        pass
    return None


def load():
    try:
        rows = games()
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        json.dump({'rows': rows, 'record': record(), 'pulled': datetime.datetime.now(PACIFIC).isoformat()},
                  open(CACHE, 'w', encoding='utf-8'), indent=1)
        return rows, record(), 'feed'
    except Exception as exc:
        print('feed failed (%s)' % exc.__class__.__name__)
        if os.path.exists(CACHE):
            c = json.load(open(CACHE, encoding='utf-8'))
            return c['rows'], c.get('record'), 'cache'
        sys.exit('no feed and no cache, leaving the page untouched')


def local(iso):
    return datetime.datetime.fromisoformat(iso.replace('Z', '+00:00')).astimezone(PACIFIC)


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def next_block(rows, rec):
    upcoming = [r for r in rows if not r['final'] and local(r['iso']) > datetime.datetime.now(PACIFIC)]
    played = [r for r in rows if r['final'] and r['kind'] == 'Regular season']
    bits = []
    if upcoming:
        n = upcoming[0]
        when = local(n['iso'])
        bits.append('<b>Next up:</b> %s %s, %s at %s, %s.%s'
                    % ('vs' if n['home'] else 'at', esc(n['them']),
                       when.strftime('%A %B %d').replace(' 0', ' '),
                       when.strftime('%I:%M %p').lstrip('0').lower().replace(' 0', ' '),
                       esc(n['venue'] or 'venue to be confirmed'),
                       ' That one is preseason.' if n['kind'] == 'Preseason' else ''))
    else:
        bits.append('<b>Next up:</b> nothing scheduled in the feed right now.')
    if played:
        wins = sum(1 for r in played if r['won'])
        bits.append(' Regular season record %d-%d through %d games%s.'
                    % (wins, len(played) - wins, len(played),
                       ', league listing %s' % esc(rec) if rec else ''))
    elif rec:
        bits.append(' League record listing: %s.' % esc(rec))
    else:
        bits.append(' No regular season games have been played yet.')
    return '\r\n  <p class="hub-next">%s</p>\r\n  ' % ''.join(bits)


def table_block(rows):
    body = []
    month = None
    for r in rows:
        when = local(r['iso'])
        tag = when.strftime('%B %Y')
        if tag != month:
            month = tag
            body.append('  <tr class="month"><td colspan="4"><b>%s</b></td></tr>' % tag)
        if r['final']:
            result = '%s %d-%d' % ('W' if r['won'] else 'L',
                                   max(r['us_score'], r['them_score']),
                                   min(r['us_score'], r['them_score']))
        elif r['state'] == 'STATUS_SCHEDULED':
            result = when.strftime('%I:%M %p').lstrip('0').lower()
        else:
            result = 'TBD'
        body.append('  <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                    % (when.strftime('%a %b %d').replace(' 0', ' '),
                       'vs' if r['home'] else 'at', esc(r['them']),
                       result + ('' if r['kind'] == 'Regular season' else ' <span class="pre">preseason</span>')))
    pre = sum(1 for r in rows if r['kind'] == 'Preseason')
    reg = len(rows) - pre
    caption = ('Golden State Warriors 2026-27 schedule as published by the league: '
               '%d preseason games and %d regular season games. All times Pacific.' % (pre, reg))
    return ('\r\n  <div class="reftable" role="region" tabindex="0" aria-label="%s">\r\n'
            '  <table>\r\n  <caption>%s</caption>\r\n'
            '  <thead><tr><th>Date</th><th>H/A</th><th>Opponent</th><th>Result or tip</th></tr></thead>\r\n'
            '  <tbody>\r\n%s\r\n  </tbody>\r\n  </table>\r\n  </div>\r\n  '
            % (caption, caption, '\r\n'.join(body)))


def shape_block(rows):
    """Facts about the schedule itself, all counted from the feed."""
    reg = [r for r in rows if r['kind'] == 'Regular season']
    if not reg:
        return '\r\n  <p>The regular season schedule is not published yet.</p>\r\n  '
    home = sum(1 for r in reg if r['home'])
    days = sorted({local(r['iso']).date() for r in reg})
    b2b = sum(1 for a, b in zip(days, days[1:]) if (b - a).days == 1)

    def longest(want_home):
        best = run = 0
        for r in reg:
            run = run + 1 if r['home'] == want_home else 0
            best = max(best, run)
        return best

    first, last = local(reg[0]['iso']), local(reg[-1]['iso'])
    opener = reg[0]
    home_games = [r for r in reg if r['home']]
    home_opener = home_games[0] if home_games else None
    lines = []
    lines.append('<li><b>Opening night</b> is %s, %s %s.</li>'
                 % (first.strftime('%A %B %d').replace(' 0', ' '),
                    'vs' if opener['home'] else 'at', esc(opener['them'])))
    if home_opener and home_opener is not opener:
        ho = local(home_opener['iso'])
        lines.append('<li><b>The home opener</b> is %s against %s.</li>'
                     % (ho.strftime('%A %B %d').replace(' 0', ' '), esc(home_opener['them'])))
    lines.append('<li><b>%d home games and %d on the road</b>, finishing %s.</li>'
                 % (home, len(reg) - home, last.strftime('%B %d').replace(' 0', ' ')))
    lines.append('<li><b>Longest homestand %d games, longest road trip %d.</b></li>'
                 % (longest(True), longest(False)))
    lines.append('<li><b>%d back to backs</b> on the calendar as published.</li>' % b2b)
    return ('\r\n  <ul class="hub-shape" style="margin:0 0 22px;padding-left:22px">'
            '\r\n    %s\r\n  </ul>\r\n  ' % '\r\n    '.join(lines))


def splice(text, key, block, check):
    start, end = MARKS[key]
    a, b = text.index(start) + len(start), text.index(end)
    if text[a:b] == block:
        return text, False
    if check:
        sys.exit('OUT OF DATE (%s): run _gen_warriors_hub.py' % key)
    return text[:a] + block + text[b:], True


def touch_modified(text):
    """A data refresh is a modification. datePublished never moves."""
    today = datetime.date.today().isoformat()
    return re.sub(r'"dateModified":"[^"]*"', '"dateModified":"%s"' % today, text, count=1)


def main():
    check = '--check' in sys.argv
    rows, rec, source = load()
    if not rows:
        sys.exit('feed returned no games, leaving the page untouched')
    text = open(ARTICLE, encoding='utf-8', newline='').read()
    changed = False
    for key, block in (('next', next_block(rows, rec)),
                       ('shape', shape_block(rows)),
                       ('table', table_block(rows))):
        text, did = splice(text, key, block, check)
        changed |= did
    if changed:
        open(ARTICLE, 'w', encoding='utf-8', newline='').write(touch_modified(text))
    played = sum(1 for r in rows if r['final'])
    print('%s: %d games listed, %d final (%s)'
          % ('rewrote' if changed else 'up to date', len(rows), played, source))


if __name__ == '__main__':
    main()
