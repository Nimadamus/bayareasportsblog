#!/usr/bin/env python3
"""_gen_homepage_live.py: keep The Wire and Last Night in the Bay honest.

Both modules were hand written into index.html and then forgotten. On 15 September 2026
the ticker still read "Deadline / Monday, August 3" and the scoreboard still told people
the 49ers had camp opening this month. Six weeks of rot, above the fold.

Every line this script writes comes out of a live feed field. Nothing is composed,
inferred or rounded:

  Giants, Athletics   statsapi.mlb.com   final scores, opponent, record
  49ers, Warriors     site.api.espn.com  final scores, record, next scheduled game
  Sharks, Raiders     site.api.espn.com  same

Three rules keep it from ever lying:

1. A final score is only shown while it is at most RESULT_DAYS old. An older game is
   treated as no data, which is what killed the August scoreboard.
2. A scheduled game is only shown while it is at most SCHEDULE_DAYS away.
3. Every source is fetched independently. One failure costs that team's tile, not the
   homepage. If everything fails, both modules fall back to content already on disk.

Run it with the rest of the publish chain:

    python _gen_discovery.py
    python _gen_homepage_live.py
    python _gen_feed.py && python _gen_sitemap.py && ...
"""
import os
import re
import sys
import json
import glob
import datetime
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(ROOT, '_homepage_live_cache.json')
PACIFIC = datetime.timezone(datetime.timedelta(hours=-7))  # PDT

RESULT_DAYS = 3        # a final older than this is stale, not news
SCHEDULE_DAYS = 14     # a fixture further out than this is not "next"
TILES = 3
WIRE_ITEMS = 6
TIMEOUT = 20

TEAMS = [
    {'key': 'giants', 'label': 'Giants', 'pill': 'sf', 'hub': 'giants.html',
     'section': 'Giants', 'src': 'mlb', 'id': 137, 'short': 'Giants'},
    {'key': 'athletics', 'label': "A's", 'pill': 'as', 'hub': 'athletics.html',
     'section': 'Athletics', 'src': 'mlb', 'id': 133, 'short': 'Athletics'},
    {'key': '49ers', 'label': '49ers', 'pill': 'niners', 'hub': '49ers.html',
     'section': '49ers', 'src': 'espn', 'path': 'football/nfl', 'abbr': 'sf', 'short': '49ers'},
    {'key': 'warriors', 'label': 'Warriors', 'pill': 'gs', 'hub': 'warriors.html',
     'section': 'Warriors', 'src': 'espn', 'path': 'basketball/nba', 'abbr': 'gs', 'short': 'Warriors'},
    {'key': 'sharks', 'label': 'Sharks', 'pill': 'sj', 'hub': 'sharks.html',
     'section': 'Sharks', 'src': 'espn', 'path': 'hockey/nhl', 'abbr': 'sj', 'short': 'Sharks'},
]


def today():
    return datetime.datetime.now(PACIFIC).date()


def fetch(url):
    # ESPN rejects a User-Agent it does not recognise, including anything with a URL in
    # it, so this deliberately sends urllib's default.
    with urllib.request.urlopen(urllib.request.Request(url), timeout=TIMEOUT) as r:
        return json.load(r)


# ------------------------------------------------------------------ the feeds

_NICKNAMES = {}


def mlb_nickname(team_id, fallback):
    """Padres, not San Diego Padres: the tiles are narrow and always have been."""
    if not _NICKNAMES:
        try:
            for t in fetch('https://statsapi.mlb.com/api/v1/teams?sportId=1')['teams']:
                _NICKNAMES[t['id']] = t.get('teamName') or t['name']
        except Exception:
            pass
    return _NICKNAMES.get(team_id, fallback)


def mlb_team(team):
    """Last final and next scheduled game for an MLB club."""
    end = today() + datetime.timedelta(days=SCHEDULE_DAYS)
    start = today() - datetime.timedelta(days=RESULT_DAYS + 2)
    url = ('https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId=%d'
           '&startDate=%s&endDate=%s' % (team['id'], start, end))
    data = fetch(url)
    final, nxt = None, None
    for day in data.get('dates', []):
        for g in day['games']:
            state = g['status']['detailedState']
            away, home = g['teams']['away'], g['teams']['home']
            us, them = (home, away) if home['team']['id'] == team['id'] else (away, home)
            row = {'date': day['date'], 'us': us['team']['name'],
                   'them': mlb_nickname(them['team']['id'], them['team']['name']),
                   'home': home['team']['id'] == team['id']}
            if state == 'Final' and us.get('score') is not None:
                row.update(ours=us['score'], theirs=them['score'],
                           won=us['score'] > them['score'])
                final = row
            elif state in ('Scheduled', 'Pre-Game') and nxt is None:
                nxt = row
    rec = fetch('https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season=%d'
                % today().year)
    record = None
    for block in rec.get('records', []):
        for t in block['teamRecords']:
            if t['team']['id'] == team['id']:
                record = '%d-%d' % (t['wins'], t['losses'])
    return {'final': final, 'next': nxt, 'record': record}


def espn_team(team):
    base = 'https://site.api.espn.com/apis/site/v2/sports/%s/teams/%s' % (team['path'], team['abbr'])
    info = fetch(base)['team']
    record = None
    for item in info.get('record', {}).get('items', []):
        record = item.get('summary') or record
        break

    final, nxt = None, None
    sched = fetch(base + '/schedule')
    for ev in sched.get('events', []):
        comp = ev['competitions'][0]
        status = comp['status']['type']
        sides = {}
        for c in comp['competitors']:
            sides['us' if c['team']['abbreviation'].lower() == team['abbr'] else 'them'] = c
        if 'us' not in sides or 'them' not in sides:
            continue
        date = ev['date'][:10]
        row = {'date': date, 'us': sides['us']['team']['displayName'],
               'them': sides['them']['team'].get('name') or sides['them']['team']['displayName'],
               'home': sides['us'].get('homeAway') == 'home'}
        if status.get('completed'):
            try:
                ours = int((sides['us'].get('score') or {}).get('displayValue'))
                theirs = int((sides['them'].get('score') or {}).get('displayValue'))
            except (TypeError, ValueError):
                continue
            row.update(ours=ours, theirs=theirs, won=bool(sides['us'].get('winner')))
            final = row
        elif nxt is None and status.get('name') == 'STATUS_SCHEDULED':
            nxt = row
    return {'final': final, 'next': nxt, 'record': record}


def collect():
    """One dict per team. A source that throws costs that team only."""
    cache = {}
    if os.path.exists(CACHE):
        try:
            cache = json.load(open(CACHE, encoding='utf-8'))
        except ValueError:
            cache = {}
    out = {}
    for team in TEAMS:
        try:
            out[team['key']] = mlb_team(team) if team['src'] == 'mlb' else espn_team(team)
            print('  %-10s ok' % team['key'])
        except Exception as exc:
            out[team['key']] = cache.get(team['key'], {'final': None, 'next': None, 'record': None})
            print('  %-10s FEED FAILED (%s), using cache' % (team['key'], exc.__class__.__name__))
    json.dump(out, open(CACHE, 'w', encoding='utf-8'), indent=1)
    return out


# ------------------------------------------------------------------ filtering

def as_date(value):
    try:
        return datetime.date(*(int(x) for x in value.split('-')))
    except Exception:
        return None


def fresh_final(row):
    d = as_date((row or {}).get('date', ''))
    if not d or 'ours' not in row:
        return None
    return row if 0 <= (today() - d).days <= RESULT_DAYS else None


def upcoming(row):
    d = as_date((row or {}).get('date', ''))
    if not d:
        return None
    return row if 0 <= (d - today()).days <= SCHEDULE_DAYS else None


def when(date_str):
    d = as_date(date_str)
    if not d:
        return ''
    if d == today():
        return 'Today'
    if d == today() + datetime.timedelta(days=1):
        return 'Tomorrow'
    return d.strftime('%A, %B %d').replace(' 0', ' ')


# ---------------------------------------------------------- our own articles

def articles():
    out = []
    for path in glob.glob(os.path.join(ROOT, 'articles', '*.html')):
        t = open(path, encoding='utf-8').read()

        def grab(pattern):
            m = re.search(pattern, t, re.S)
            return m.group(1) if m else ''
        out.append({'slug': os.path.basename(path)[:-5],
                    'title': grab(r'<title>(.*?)</title>'),
                    'date': grab(r'"datePublished":"(.*?)"'),
                    'section': grab(r'"articleSection":"(.*?)"'),
                    'tag': grab(r'<span class="tag">(.*?)</span>')})
    out.sort(key=lambda a: (a['date'], a['slug']), reverse=True)
    return out


def column_for(team, game, arts):
    """Our own column about this game, if one exists. Never a guess: the piece has to
    be in the right section, published within two days of the game, and name the
    opponent or carry the score."""
    played = as_date(game['date'])
    if not played:
        return None
    opponent = game['them'].split()[-1].lower()
    score = '%d-%d' % (max(game['ours'], game['theirs']), min(game['ours'], game['theirs']))
    loose = score.replace('-', ' ')
    for art in arts:
        if art['section'] != team['section']:
            continue
        d = as_date(art['date'])
        if not d or not (0 <= (d - played).days <= 2):
            continue
        hay = (art['title'] + ' ' + art['slug']).lower()
        if opponent in hay or score in hay or loose in hay:
            return art
    return None


# ------------------------------------------------------------------ rendering

def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def tiles(data, arts):
    """Newest Bay Area finals first, then the nearest fixture, then hub tiles."""
    finals = []
    for team in TEAMS:
        game = fresh_final(data.get(team['key'], {}).get('final'))
        if game:
            finals.append((game['date'], team, game))
    finals.sort(key=lambda r: r[0], reverse=True)

    out = []
    used = set()
    for _, team, game in finals[:TILES]:
        used.add(team['key'])
        art = column_for(team, game, arts)
        href = 'articles/%s.html' % art['slug'] if art else team['hub']
        tail = 'The column &rarr;' if art else 'The hub &rarr;'
        note = 'Final &middot; %s &middot; %s' % (esc(when(game['date'])), tail)
        us_cls = ' w' if game['won'] else ''
        them_cls = '' if game['won'] else ' w'
        out.append(
            '      <a class="sc-game" href="%s">\r\n'
            '        <div class="sc-row"><span class="sc-team%s">%s</span><span class="sc-run%s">%d</span></div>\r\n'
            '        <div class="sc-row"><span class="sc-team%s">%s</span><span class="sc-run%s">%d</span></div>\r\n'
            '        <div class="sc-note">%s</div>\r\n'
            '      </a>' % (href, us_cls, esc(team['label']), '' if game['won'] else ' l', game['ours'],
                            them_cls, esc(game['them']), ' l' if game['won'] else '', game['theirs'], note))

    for team in TEAMS:
        if len(out) >= TILES:
            break
        if team['key'] in used:
            continue
        nxt = upcoming(data.get(team['key'], {}).get('next'))
        if not nxt:
            continue
        used.add(team['key'])
        line = '%s %s' % ('at' if not nxt['home'] else 'vs', nxt['them'])
        out.append(
            '      <a class="sc-game off" href="%s">\r\n'
            '        <div class="sc-row"><span class="sc-team">%s</span><span class="sc-run">&nbsp;</span></div>\r\n'
            '        <div class="sc-row"><span class="sc-team">%s</span><span class="sc-run">&nbsp;</span></div>\r\n'
            '        <div class="sc-note">Next &middot; %s &middot; The hub &rarr;</div>\r\n'
            '      </a>' % (team['hub'], esc(team['label']), esc(line), esc(when(nxt['date']))))

    for team in TEAMS:                      # last resort: no feed said anything usable
        if len(out) >= TILES:
            break
        if team['key'] in used:
            continue
        used.add(team['key'])
        out.append(
            '      <a class="sc-game off" href="%s">\r\n'
            '        <div class="sc-row"><span class="sc-team">%s</span><span class="sc-run">&nbsp;</span></div>\r\n'
            '        <div class="sc-row"><span class="sc-team">Latest coverage</span><span class="sc-run">&nbsp;</span></div>\r\n'
            '        <div class="sc-note">The hub &rarr;</div>\r\n'
            '      </a>' % (team['hub'], esc(team['label'])))
    return out


def wire(data, arts):
    """Six factual lines. Feed first, our own headlines to fill."""
    items = []
    finals = []
    for team in TEAMS:
        game = fresh_final(data.get(team['key'], {}).get('final'))
        if game:
            finals.append((game['date'], team, game))
    finals.sort(key=lambda r: r[0], reverse=True)

    for _, team, game in finals:
        verb = 'beat' if game['won'] else 'lost to'
        hi, lo = max(game['ours'], game['theirs']), min(game['ours'], game['theirs'])
        text = '%s %s %d-%d' % (verb, game['them'], hi, lo)
        record = data.get(team['key'], {}).get('record')
        if record:
            text = '%s, %s' % (record, text)
        items.append(('up' if game['won'] else 'dn', team['label'], text))

    for team in TEAMS:
        nxt = upcoming(data.get(team['key'], {}).get('next'))
        if not nxt or len(items) >= WIRE_ITEMS:
            continue
        if any(i[1] == team['label'] for i in items):
            continue
        items.append(('', team['label'],
                      'Next %s %s %s' % (when(nxt['date']), 'at' if not nxt['home'] else 'vs', nxt['them'])))

    for art in arts:                        # always available, even with every feed down
        if len(items) >= WIRE_ITEMS:
            break
        label = art['tag'] or art['section']
        items.append(('', label, art['title']))

    return ['        <span class="tk-i%s"><b>%s</b><s>/</s>%s</span>'
            % (' ' + cls if cls else '', esc(label), esc(text)) for cls, label, text in items[:WIRE_ITEMS]]


# ------------------------------------------------------------------ the page

def splice(text, opener, body):
    """Replace the children of the div that starts at `opener`."""
    start = text.index(opener)
    i = text.index('>', start) + 1
    depth, pos = 1, i
    tag = re.compile(r'<(/?)div\b', re.I)
    while depth:
        m = tag.search(text, pos)
        depth += -1 if m.group(1) else 1
        pos = m.end()
    return text[:i] + body + text[m.start():]


def main():
    os.chdir(ROOT)
    print('feeds:')
    data = collect()
    arts = articles()

    rail = wire(data, arts)
    body = ('\r\n' + '\r\n'.join(rail) + '\r\n'
            + '        <!-- duplicated for a seamless loop -->\r\n'
            + '\r\n'.join(rail) + '\r\n      ')
    text = splice(open('index.html', encoding='utf-8', newline='').read(),
                  '<div class="tk-rail">', body)

    cards = tiles(data, arts)
    keep = re.search(r'\s*<div class="sc-tag">.*?</div>', text, re.S).group(0)
    text = splice(text, '<div class="scores">', keep + '\r\n' + '\r\n'.join(cards) + '\r\n    ')
    open('index.html', 'w', encoding='utf-8', newline='').write(text)

    print('wire   : %d items' % len(rail))
    for card in cards:
        who = re.search(r'sc-team[^>]*>([^<]+)<', card).group(1)
        note = re.search(r'sc-note">([^<]+)<', card).group(1)
        print('  tile   %-10s %s' % (who, note.replace('&middot;', '|').replace('&rarr;', '')))
    if not any('sc-game"' in c for c in cards):
        print('  no fresh finals anywhere, scoreboard is running on fallbacks')


if __name__ == '__main__':
    main()
