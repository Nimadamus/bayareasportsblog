#!/usr/bin/env python3
"""_gen_niners_injuries.py: the 49ers injury report, one permanent URL.

articles/49ers-injury-report.html is a living page, not a weekly post. Every run rewrites
the tables between the markers and the page dates; the URL never changes, so the page
keeps whatever authority it earns across the season.

Source: the league injury feed as published through ESPN's core API
(sports.core.api.espn.com, team 25). For each player it gives a status (Active,
Questionable, Doubtful, Out, Injured Reserve), a designation where one applies (IR,
PUP-R and the like), the body part and the injury detail, and the time of the last
change.

Expected back (Nima 2026-11-13: show when each player is expected back). In order:
  - a game designation (questionable, doubtful, probable) is shown as that word;
  - a reported timeline found in the latest update ("six weeks", "two to three weeks",
    "eight months", "out for the season") is shown in digits with the date it was
    reported, e.g. "6 weeks (reported Nov 3)";
  - otherwise the feed's estimated return date, labeled "est.";
  - otherwise "No timeline yet".
Only the timeline is taken from the update text; the comment itself is never printed.

What the page deliberately does NOT show:
  - the feed's comment text. It is someone else's reporting.
  - practice participation. The feed does not carry it, and nothing is inferred.

Players whose latest entry is Active and is older than CLEARED_DAYS drop off the page.

    python _gen_niners_injuries.py           rebuild from the feed
    python _gen_niners_injuries.py --check   exit 1 if the page is missing its markers

Failure: if the feed cannot be read, the page is left exactly as it is, and the strip's
"Updated" date stays on the last good pull, which is visible to readers and to
tools/staleness_check.py.
"""
import os
import re
import sys
import json
import html
import glob
import datetime
import urllib.request
import concurrent.futures as cf
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://bayareasportsblog.com/'
SLUG = '49ers-injury-report'
PAGE = os.path.join(ROOT, 'articles', SLUG + '.html')
TEMPLATE = os.path.join(ROOT, 'articles', '49ers-2026-roster-depth-chart.html')
PACIFIC = ZoneInfo('America/Los_Angeles')
UA = {'User-Agent': 'python-requests/2.31'}
FEED = 'https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams/25/injuries?limit=200'
SCHED = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/sf/schedule'
START, END = '<!-- injuries:start -->', '<!-- injuries:end -->'
CLEARED_DAYS = 10
# Reserve list designations the feed uses, in words. Anything on one of these goes in the
# reserve table rather than the game status tables.
LIST_LABELS = {'IR-R': 'designated to return', 'PUP-R': 'PUP list', 'PUP-P': 'PUP list',
               'NFI-R': 'non football injury list', 'NFI-P': 'non football injury list',
               'RESERVE-DNR': 'reserve, did not report', 'SUSP': 'suspended'}
PUBLISHED = '2026-10-01'
# Team identity. _gen_warriors_injuries.py reuses this module and overrides these.
TEAM_ABBR = 'SF'
LEAGUE = 'nfl'
CARD_ALT = ''
CARD_ALTS = {'raiders': 'Raiders fans in costume in the stands at a home game',
             'giants': 'Giants fans watching a night game at Oracle Park',
             'athletics': "Brent Rooker of the A's in the outfield at the Oakland Coliseum",
             'sharks': 'The Sharks warming up on the ice at SAP Center before a playoff game',
             'hub': 'San Francisco and the Golden Gate Bridge from the Marin Headlands'}
TEAM_NAME, SPORT, SECTION = 'San Francisco 49ers', 'American football', '49ers'
HUB_NAME, HUB_FILE, PAGE_NAME = '49ers', '49ers.html', '49ers Injury Report'
COVER_PREFIXES = ('49ers', 'nick-bosa', 'brock-purdy')
LINK = 'style="color:var(--gold);text-decoration:underline;text-underline-offset:3px"'

TITLE = '49ers Injury Report Today: Who Is Out, Questionable and on IR'
DESC = ('The current San Francisco 49ers injury report: every player listed out, doubtful, '
        'questionable, on injured reserve or PUP, with the injury and the latest update.')


def fetch(url):
    req = urllib.request.Request(url.replace('http://', 'https://'), headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode('utf-8'))


def pull():
    index = fetch(FEED)
    with cf.ThreadPoolExecutor(10) as ex:
        items = list(ex.map(lambda i: fetch(i['$ref']), index.get('items', [])))
    latest = {}
    for it in items:
        aid = it['athlete']['$ref'].split('/athletes/')[1].split('?')[0]
        if aid not in latest or it['date'] > latest[aid]['date']:
            latest[aid] = it
    now = datetime.datetime.now(datetime.timezone.utc)
    keep = {}
    for aid, it in latest.items():
        when = datetime.datetime.strptime(it['date'][:16], '%Y-%m-%dT%H:%M').replace(tzinfo=datetime.timezone.utc)
        if it['status'] == 'Active' and (now - when).days > CLEARED_DAYS:
            continue
        keep[aid] = (it, when)
    with cf.ThreadPoolExecutor(10) as ex:
        people = dict(zip(keep, ex.map(lambda a: fetch(keep[a][0]['athlete']['$ref']), keep)))
    rows = []
    for aid, (it, when) in keep.items():
        p = people[aid]
        d = it.get('details') or {}
        ret = None
        if d.get('returnDate'):
            try:
                ret = datetime.date.fromisoformat(d['returnDate'][:10])
            except ValueError:
                ret = None
        rows.append({
            'name': p.get('displayName', ''),
            'last': p.get('lastName', ''),
            'pos': (p.get('position') or {}).get('abbreviation', ''),
            'status': it['status'],
            'list': ((d.get('fantasyStatus') or {}).get('abbreviation') or ''),
            'injury': injury_text(d),
            'when': when.astimezone(PACIFIC),
            'ret': ret,
            'short': it.get('shortComment') or '',
            'long': it.get('longComment') or '',
        })
    for r in rows:
        r['game'] = game_tag(r)
        r['back'] = expected(r)
    return rows


# ---- expected back --------------------------------------------------------------------
WORDNUM = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
           'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12}
_N = r'(\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)'
TIMELINE = re.compile(r'\b%s(?:\s*(?:to|-|or)\s*%s)?[\s-]+(day|week|month)s?\b' % (_N, _N), re.I)
CUE = re.compile(r'miss|out\b|sidelin|recover|timeline|absence|shelved|expected|require|return|'
                 r'back\b|ready|evaluat|surgery|rehab|week-to-week', re.I)
NOT_AHEAD = re.compile(r'injured list|\bIL\b|last (season|year)|previous|earlier|\bago\b|\bsince\b|has missed|'
                       r'have missed|had missed|missed the (last|past)|over the (last|past)|(past|last) %s|'
                       r'contract|option|signed|deal\b|suspen|window|practice|exemption' % _N, re.I)
SEASON_OVER = re.compile(r'season-ending|out for the (rest of the )?season|(rest|remainder) of the (\d{4} )?(regular )?season', re.I)
GAME_WORD = re.compile(r'\b(?:is|was|remains|been|listed as|considered|will be|status is)\s+'
                       r'(probable|questionable|doubtful|out|available|a game-time decision)\b', re.I)


def in_season(today):
    m, d = today.month, today.day
    return {'nfl': m >= 9 or m <= 1, 'nba': m >= 10 or m <= 5, 'nhl': m >= 10 or m <= 5,
            'mlb': (m, d) >= (3, 20) and m <= 10}.get(LEAGUE, True)


def num(s):
    return int(s) if s.isdigit() else WORDNUM[s.lower()]


def sentences(r):
    for text in (r['short'], r['long']):
        for s in re.split(r'(?<=[.!?])\s+', text):
            yield s


def season_end(today):
    """First day after this league's current season, for reading estimated return dates."""
    y = today.year
    if LEAGUE == 'nfl':
        return datetime.date(y + 1 if today.month >= 3 else y, 1, 20)     # after the regular season
    if LEAGUE in ('nba', 'nhl'):
        return datetime.date(y + 1 if today.month >= 7 else y, 6, 1)
    return datetime.date(y, 11, 1)


def timeline(r, today):
    """A reported timeline from the latest update, or None."""
    age = (today - r['when'].date()).days
    for s in sentences(r):
        if (SEASON_OVER.search(s) and in_season(today) and age < 200
                and not re.search(r'last (season|year)|previous', s, re.I)):
            return 'Out for the season'
    if age > 75:
        return None
    for s in sentences(r):
        for m in TIMELINE.finditer(s):
            if not CUE.search(s) or NOT_AHEAD.search(s):
                continue
            a, b, unit = num(m.group(1)), m.group(2), m.group(3).lower()
            top = num(b) if b else a
            end = r['when'].date() + datetime.timedelta(days=top * {'day': 1, 'week': 7, 'month': 30}[unit])
            if end < today:
                continue                   # that timeline has already run out
            if not in_season(today) and unit != 'month':
                continue                   # a short layoff in the offseason says nothing about return
            span = '%d' % a if not b else '%d to %d' % (a, num(b))
            plural = '' if (not b and a == 1) else 's'
            text = '%s %s%s' % (span, unit, plural)
            if re.search(r'evaluat', s, re.I):
                text = 'Checked again in ' + text
            return '%s (reported %s)' % (text, r['when'].strftime('%b ') + str(r['when'].day))
    return None


def game_tag(r):
    """Probable / Questionable / Doubtful / Out for a day to day player, from a fresh update."""
    if r['status'] not in ('Day-To-Day', 'Day to day'):
        return ''
    if (datetime.datetime.now(PACIFIC) - r['when']).days > 2:
        return ''
    m = GAME_WORD.search(r['short'])
    if not m:
        return ''
    w = m.group(1).lower()
    return {'available': 'Available', 'a game-time decision': 'Questionable'}.get(w, w.capitalize())


def short_date(d):
    return d.strftime('%b ') + str(d.day) + (', %d' % d.year if d.year != datetime.date.today().year else '')


def expected(r):
    today = datetime.datetime.now(PACIFIC).date()
    st = r['status']
    if st == 'Active':
        return 'Cleared'
    word = {'Questionable': 'Questionable', 'Doubtful': 'Doubtful', 'Probable': 'Probable'}
    if st in word:
        return word[st]
    if r.get('game'):
        return {'Out': 'Out next game', 'Available': 'Available'}.get(r['game'], r['game'])
    tl = timeline(r, today)
    if tl:
        return tl
    if st in ('Day-To-Day', 'Day to day'):
        return 'Day to day'
    ret = r.get('ret')
    if ret and ret > today:
        days = (ret - today).days
        if LEAGUE == 'mlb' and not in_season(today) and ret.month in (2, 3):
            return 'Spring training'
        if in_season(today) and ret >= season_end(today):
            return 'Out for the season (est.)'
        if days <= 10:
            return 'Est. %s' % short_date(ret)
        if days <= 70:
            return 'About %d weeks (est. %s)' % (max(2, round(days / 7.0)), short_date(ret))
        return 'About %d months (est. %s)' % (max(2, round(days / 30.4)), ret.strftime('%b %Y'))
    return 'No timeline yet'


def injury_text(d):
    if not d:
        return ''
    kind = d.get('type', '')
    if ' - ' in kind:                      # "Knee - ACL" reads as "Knee (ACL)"
        a, b = kind.split(' - ', 1)
        kind = '%s (%s)' % (a, b)
    parts = [kind]
    detail = d.get('detail', '')
    if detail and detail != 'Not Specified' and detail.lower() != kind.lower():
        parts.append(detail.lower())
    side = d.get('side', '')
    if side and side != 'Not Specified':
        parts.append(side.lower())
    return ', '.join(p for p in parts if p)


def next_game():
    try:
        for ev in fetch(SCHED).get('events', []):
            st = ev['competitions'][0]['status']['type']
            if st.get('name') == 'STATUS_SCHEDULED':
                comp = ev['competitions'][0]['competitors']
                us = [c for c in comp if c['team']['abbreviation'] == TEAM_ABBR][0]
                them = [c for c in comp if c['team']['abbreviation'] != TEAM_ABBR][0]
                when = datetime.datetime.strptime(ev['date'][:16], '%Y-%m-%dT%H:%M').replace(
                    tzinfo=datetime.timezone.utc).astimezone(PACIFIC)
                soon = (when - datetime.datetime.now(PACIFIC)).days < 14   # far off times are placeholders
                return '%s %s, %s' % ('vs' if us.get('homeAway') == 'home' else 'at',
                                      them['team']['displayName'], day(when, soon))
    except Exception:
        return None
    return None


def day(dt, with_time=False):
    s = dt.strftime('%a, %b ') + str(dt.day)
    if with_time:
        s += ', ' + dt.strftime('%I:%M %p').lstrip('0') + ' Pacific'
    return s


def coverage():
    """Our own 49ers injury columns, newest first, with the player names they mention."""
    out = []
    pat = re.compile(r'injur|surgery|out-for|calf|ankle|acl|pcl|patellar|hamstring|tendon|achilles|mcl|soreness|tightness')
    for path in glob.glob(os.path.join(ROOT, 'articles', '*.html')):
        slug = os.path.basename(path)[:-5]
        if slug == SLUG or not slug.startswith(COVER_PREFIXES):
            continue
        if not pat.search(slug):
            continue
        text = open(path, encoding='utf-8').read()
        m = re.search(r'"datePublished":"(\d{4}-\d{2}-\d{2})"', text)
        t = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)
        if m and t:
            out.append((m.group(1), slug, re.sub(r'<[^>]+>', '', t.group(1)).strip()))
    return sorted(out, reverse=True)


def table(caption, rows, cover):
    if not rows:
        return ''
    body = []
    for r in sorted(rows, key=lambda r: (r['pos'], r['name'])):
        link = next((s for _, s, _t in cover if r['last'] and r['last'].lower() in s.split('-')), None)
        name = html.escape(r['name'])
        if link:
            name = '<a href="%s.html" %s>%s</a>' % (link, LINK, name)
        label = LIST_LABELS.get(r['list'].upper(), '') if r['list'] else ''
        shown = r['game'] if r.get('game') in ('Probable', 'Questionable', 'Doubtful') else r['status']
        shown = 'Day to day' if shown == 'Day-To-Day' else shown
        status = shown + (' (%s)' % label if label else '')
        body.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><b>%s</b></td><td>%s</td></tr>' % (
            name, html.escape(r['pos']), html.escape(r['injury'] or 'Not disclosed'),
            html.escape(status), html.escape(r.get('back') or ''), day(r['when'])))
    return ('<div class="reftable" role="region" tabindex="0" aria-label="%s">\n<table>\n<caption>%s</caption>\n'
            '<thead><tr><th>Player</th><th>Pos</th><th>Injury</th><th>Status</th><th>Expected back</th><th>Last update</th></tr></thead>\n'
            '<tbody>\n%s\n</tbody>\n</table>\n</div>' % (html.escape(caption), html.escape(caption), '\n'.join(body)))


def region(rows, now, nxt, cover):
    lists = [r for r in rows if r['status'] == 'Injured Reserve' or r['list'].upper() in LIST_LABELS]
    q = [r for r in rows if r['status'] == 'Questionable' and r not in lists]
    out = [r for r in rows if r['status'] not in ('Questionable', 'Active') and r not in lists]
    cleared = [r for r in rows if r['status'] == 'Active']
    counts = '%d out or doubtful, %d questionable, %d on injured reserve, PUP or another reserve list' % (len(out), len(q), len(lists))
    parts = ['<p><b>Updated %s.</b> %s.%s</p>' % (
        day(now, True), counts[0].upper() + counts[1:],
        (' Next game: %s.' % html.escape(nxt)) if nxt else '')]
    parts.append(table('Out or doubtful', out, cover))
    parts.append(table('Questionable', q, cover))
    parts.append(table('Injured reserve, PUP and other reserve lists', lists, cover))
    if cleared:
        names = ', '.join('%s (%s)' % (html.escape(r['name']), html.escape(r['pos']))
                          for r in sorted(cleared, key=lambda r: r['name']))
        parts.append('<p><b>Back off the report in the last %d days:</b> %s.</p>' % (CLEARED_DAYS, names))
    return START + '\n' + '\n'.join(p for p in parts if p) + '\n' + END


def article(now, nxt, rows, cover):
    recent = ''.join('<li><a href="%s.html" %s>%s</a></li>' % (s, LINK, html.escape(t)) for _, s, t in cover[:6])
    return ('''<article class="article" role="main" aria-labelledby="article-title">
  <span class="tag">49ers</span>
  <h1 id="article-title">49ers Injury Report</h1>
  <p style="font-size:19px;color:#cdd2db;margin:-4px 0 20px;font-style:italic">Who is out, who is questionable, and who is on injured reserve, kept current through the season at this one address.</p>
  <div class="byline">Bay Area Sports Blog Staff &middot; 49ers &middot; Updated %(upd)s</div>
  <picture><source type="image/webp" srcset="../assets/img/cards/%(slug)s-400w.webp 400w, ../assets/img/cards/%(slug)s-600w.webp 600w, ../assets/img/cards/%(slug)s-800w.webp 800w, ../assets/img/cards/%(slug)s.webp 1200w" sizes="(max-width: 820px) 92vw, 760px"><img src="../assets/img/cards/%(slug)s.jpg" alt="49ers injury report card from Bay Area Sports Blog" width="1200" height="675" decoding="async" fetchpriority="high" srcset="../assets/img/cards/%(slug)s-400w.jpg 400w, ../assets/img/cards/%(slug)s-600w.jpg 600w, ../assets/img/cards/%(slug)s-800w.jpg 800w, ../assets/img/cards/%(slug)s.jpg 1200w" sizes="(max-width: 820px) 92vw, 760px"></picture>

  <p>This is the page to check before a 49ers game. Every player on the league injury report is here with his position, the injury, his status and when it last changed. It refreshes several times a day, so you never need a new link for a new week.</p>

  <h2>The current report</h2>
%(region)s

  <h2>How to read it</h2>
  <p><b>Out</b> means he will not play in the next game. <b>Doubtful</b> means he is unlikely to. <b>Questionable</b> means it is a genuine maybe, and plenty of questionable players suit up. <b>Injured reserve</b> takes a player off the active roster for at least four games, and <b>PUP</b> is the physically unable to perform list, used for players still recovering from an injury they already had.</p>
%(backnote)s

  <h2>Where the numbers come from</h2>
  <p>Status, designation and injury come from the league injury report as published through ESPN, read automatically. Nothing in the tables is typed in by hand. When the team announces something the feed has not caught yet, it shows up here on the next refresh, usually within a few hours. See our <a href="../editorial-standards.html" %(link)s>editorial standards</a> and <a href="../corrections.html" %(link)s>corrections policy</a>.</p>

  <h2>Our 49ers injury coverage</h2>
  <ul>%(recent)s</ul>
  <p>For the full roster and who steps in behind each injured starter, see the <a href="49ers-2026-roster-depth-chart.html" %(link)s>49ers roster and depth chart</a>. Results and the rest of the schedule are on the <a href="49ers-2026-schedule-season-hub.html" %(link)s>49ers schedule page</a>.</p>

%(siblings)s
  <p style="margin-top:30px;color:var(--muted);font-size:15px">More coverage: <a href="../49ers.html" style="color:var(--accent2);font-weight:700">49ers</a> &middot; <a href="../nfl.html" style="color:var(--accent2);font-weight:700">NFL</a></p>
</article>''' % {'upd': day(now), 'slug': SLUG, 'region': region(rows, now, nxt, cover),
                 'recent': recent, 'link': LINK, 'backnote': BACKNOTE, 'siblings': siblings()})


# Every injury report on the site; each page links to all the others.
REPORTS = [('bay-area-injury-report', 'Every Bay Area team'), ('49ers-injury-report', '49ers'),
           ('raiders-injury-report', 'Raiders'), ('warriors-injury-report', 'Warriors'),
           ('giants-injury-report', 'Giants'), ('athletics-injury-report', "A's"),
           ('sharks-injury-report', 'Sharks')]

BACKNOTE = ('  <p><b>Expected back</b> is the latest timeline we can stand behind. When the update names one, '
            'like six weeks or two to three weeks, it shows here in plain numbers with the date it was reported. '
            'When it does not, you see the estimated return date carried on the league report, marked est. '
            'Timelines move, and this page moves with them. If nothing has been reported, it says no timeline yet. '
            'Practice participation is not shown: if the feed does not report it, we do not guess at it.</p>')


def siblings():
    links = ' &middot; '.join('<a href="%s.html" %s>%s</a>' % (s, LINK, html.escape(n))
                              for s, n in REPORTS if s != SLUG and os.path.exists(os.path.join(ROOT, 'articles', s + '.html')))
    return '  <h2>Every Bay Area injury report</h2>\n  <p>%s</p>\n' % links


def build_head(template, now):
    url = BASE + 'articles/' + SLUG + '.html'
    img = BASE + 'assets/img/cards/' + SLUG + '.jpg'
    t = template
    t = re.sub(r'<title>.*?</title>', '<title>%s</title>' % TITLE, t, flags=re.S)
    for prop, val in (('description', DESC),):
        t = re.sub(r'<meta name="%s" content="[^"]*">' % prop, '<meta name="%s" content="%s">' % (prop, val), t)
    t = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url, t)
    repl = {'og:title': TITLE, 'og:description': DESC, 'og:url': url, 'og:image': img,
            'og:image:alt': 'Bay Area Sports Blog: ' + PAGE_NAME}
    for k, v in repl.items():
        t = re.sub(r'<meta property="%s" content="[^"]*">' % re.escape(k), '<meta property="%s" content="%s">' % (k, html.escape(v, quote=True)), t)
    for k, v in {'twitter:title': TITLE, 'twitter:description': DESC, 'twitter:image': img}.items():
        t = re.sub(r'<meta name="%s" content="[^"]*">' % re.escape(k), '<meta name="%s" content="%s">' % (k, v), t)
    art = {'@context': 'https://schema.org', '@type': 'Article', 'headline': TITLE, 'image': img,
           'author': {'@type': 'Organization', 'name': 'Bay Area Sports Blog', 'url': BASE + 'about.html'},
           'publisher': {'@type': 'Organization', 'name': 'Bay Area Sports Blog', 'url': BASE},
           'description': DESC, 'datePublished': PUBLISHED, 'dateModified': now.date().isoformat(),
           'mainEntityOfPage': {'@type': 'WebPage', '@id': url}, 'url': url, 'articleSection': SECTION,
           'about': {'@type': 'SportsTeam', 'name': TEAM_NAME, 'sport': SPORT}}
    crumbs = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE},
        {'@type': 'ListItem', 'position': 2, 'name': HUB_NAME, 'item': BASE + HUB_FILE},
        {'@type': 'ListItem', 'position': 3, 'name': PAGE_NAME, 'item': url}]}
    blocks = re.findall(r'<script type="application/ld\+json">.*?</script>', t, re.S)
    t = t.replace(blocks[0], '<script type="application/ld+json">%s</script>' % json.dumps(art, ensure_ascii=False, separators=(',', ':')), 1)
    t = t.replace(blocks[1], '<script type="application/ld+json">%s</script>' % json.dumps(crumbs, ensure_ascii=False, separators=(',', ':')), 1)
    return t


def main():
    if '--check' in sys.argv:
        ok = os.path.exists(PAGE) and START in open(PAGE, encoding='utf-8').read()
        print('ok' if ok else 'missing')
        sys.exit(0 if ok else 1)
    now = datetime.datetime.now(PACIFIC)
    try:
        rows = pull()
    except Exception as exc:
        print('FEED FAILED (%s), page left as is' % exc.__class__.__name__)
        sys.exit(1)
    nxt = next_game()
    cover = coverage()
    base = open(PAGE if os.path.exists(PAGE) else TEMPLATE, encoding='utf-8', newline='').read()
    page = build_head(base, now)
    page = re.sub(r'<article class="article".*?</article>', lambda m: article(now, nxt, rows, cover), page, flags=re.S)
    open(PAGE, 'w', encoding='utf-8', newline='').write(page)
    print('injury report: %d players listed, next game %s' % (len(rows), nxt))


if __name__ == '__main__':
    main()
