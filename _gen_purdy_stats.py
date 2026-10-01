#!/usr/bin/env python3
"""_gen_purdy_stats.py: keep the Brock Purdy page current, at its existing URL.

articles/brock-purdy-career-passer-rating-where-he-ranks.html is the page Google already
ranks for Purdy (Search Console, Oct 2026: 72 impressions at position 9.7, while the
second Purdy record page sits crawled but not indexed). This script owns its <article>
and its title and description; the URL, the card image and the head chrome stay as they
are.

Every number in the tables comes from ESPN's athlete stats and game log endpoints:
season by season regular season and playoff passing and rushing, career totals, and
the record in games he started. Nothing in the tables is typed in.

Starts: the game log does not say who started. Every Purdy appearance from Week 14 of
2022 on was a start; the four 2022 appearances before that were in relief (Week 13
against Miami is the game he came in for an injured Jimmy Garoppolo), and they are
excluded by date in RELIEF below.

The one hand kept number is the qualified career passer rating leader, which no feed
here provides. It is dated in the copy (LEADER_NOTE) and must be updated by hand when it
changes.

    python _gen_purdy_stats.py
"""
import os
import re
import json
import html
import datetime
import urllib.request
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.abspath(__file__))
SLUG = 'brock-purdy-career-passer-rating-where-he-ranks'
PAGE = os.path.join(ROOT, 'articles', SLUG + '.html')
ATHLETE = 4361741
PACIFIC = ZoneInfo('America/Los_Angeles')
UA = {'User-Agent': 'python-requests/2.31'}
STATS = 'https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/%d/stats?seasontype=%d'
GAMELOG = 'https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/%d/gamelog?season=%d'
FIRST_SEASON = 2022
RELIEF = {'2022-10-09', '2022-10-23', '2022-11-22', '2022-12-04'}
QUALIFY = 1500
LEADER_NOTE = ('Through Week 3 of the 2026 season the qualified leader was Lamar Jackson at 102.4, '
               'with Aaron Rodgers second at 101.9.')
LINK = 'style="color:var(--gold);text-decoration:underline;text-underline-offset:3px"'

H1 = 'Brock Purdy Stats, Record and Where He Actually Ranks'
TITLE = 'Brock Purdy Stats, Record and Where He Ranks All Time'
DESC = ('Brock Purdy career stats with the 49ers, season by season and in the playoffs, his record '
        'as a starter, and how close he is to the career passer rating record.')


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
        return json.loads(r.read().decode('utf-8'))


def season_stats(kind):
    d = fetch(STATS % (ATHLETE, kind))
    out = {}
    for c in d.get('categories', []):
        if c['name'] in ('passing', 'rushing'):
            names = c['names']
            rows = [(s['season']['year'], dict(zip(names, s['stats']))) for s in c.get('statistics', [])]
            out[c['name']] = {'rows': rows, 'total': dict(zip(names, c.get('totals', [])))}
    return out


def records(now):
    reg, post = [0, 0], [0, 0]
    games = []
    for yr in range(FIRST_SEASON, now.year + 1):
        d = fetch(GAMELOG % (ATHLETE, yr))
        ev = d.get('events', {})
        for st in d.get('seasonTypes', []):
            kind = 'post' if 'Post' in st['displayName'] else ('reg' if 'Regular' in st['displayName'] else None)
            if not kind:
                continue
            for c in st.get('categories', []):
                for e in c.get('events', []):
                    g = ev.get(e['eventId'], {})
                    date = (g.get('gameDate') or '')[:10]
                    if date in RELIEF or g.get('gameResult') not in ('W', 'L', 'T'):
                        continue
                    tally = reg if kind == 'reg' else post
                    if g['gameResult'] == 'W':
                        tally[0] += 1
                    elif g['gameResult'] == 'L':
                        tally[1] += 1
                    games.append((date, kind, g))
    return reg, post, games


def n(v):
    return html.escape(str(v))


def pass_table(caption, data):
    p = data['passing']
    body = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
        yr, n(s['gamesPlayed']), n(s['completions']), n(s['passingAttempts']), n(s['completionPct']),
        n(s['passingYards']), n(s['passingTouchdowns']), n(s['interceptions']), n(s['QBRating'])) for yr, s in p['rows'])
    t = p['total']
    body += '<tr><td><b>Career</b></td><td><b>%s</b></td><td><b>%s</b></td><td><b>%s</b></td><td><b>%s</b></td><td><b>%s</b></td><td><b>%s</b></td><td><b>%s</b></td><td><b>%s</b></td></tr>' % (
        n(t['gamesPlayed']), n(t['completions']), n(t['passingAttempts']), n(t['completionPct']),
        n(t['passingYards']), n(t['passingTouchdowns']), n(t['interceptions']), n(t['QBRating']))
    return ('<div class="reftable" role="region" tabindex="0" aria-label="%s">\n<table>\n<caption>%s</caption>\n'
            '<thead><tr><th>Season</th><th>G</th><th>Cmp</th><th>Att</th><th>Pct</th><th>Yds</th><th>TD</th><th>Int</th><th>Rating</th></tr></thead>\n'
            '<tbody>%s</tbody>\n</table>\n</div>' % (n(caption), n(caption), body))


def region(reg_stats, post_stats, reg, post, now):
    t = reg_stats['passing']['total']
    att = int(str(t['passingAttempts']).replace(',', ''))
    need = max(0, QUALIFY - att)
    rush = reg_stats['rushing']['total']
    prush = post_stats['rushing']['total']
    pt = post_stats['passing']['total']
    qual = ('He has %s career attempts, so he needs %d more to qualify.' % ('{:,}'.format(att), need)
            if need else 'He has %s career attempts, which clears the qualifying line.' % '{:,}'.format(att))
    return '''<!-- purdy:start -->
<p><b>Updated %(upd)s.</b> Regular season: %(rg)s games, %(yds)s yards, %(td)s touchdowns, %(int)s interceptions, a %(rate)s passer rating, and a %(rw)d and %(rl)d record as a starter. Playoffs: %(pg)s games, a %(pw)d and %(pl)d record, %(ptd)s touchdowns, %(pint)s interceptions and an %(prate)s rating.</p>
%(regtable)s
%(posttable)s
<p><b>Rushing.</b> Regular season: %(ra)s carries, %(ry)s yards, %(rtd)s touchdowns. Playoffs: %(pra)s carries, %(pry)s yards, %(prtd)s touchdown%(prs)s.</p>
<h2>The career passer rating record</h2>
<p>Purdy's career regular season passer rating is <b>%(rate)s</b>. The NFL only ranks quarterbacks with at least 1,500 career attempts. %(qual)s %(leader)s So the number is already above anyone on the qualified list; what he is waiting on is volume. Our <a href="49ers-brock-purdy-highest-passer-rating-nfl-history-1500-attempts.html" %(link)s>record chase piece</a> covers what the week he qualifies will look like.</p>
<!-- purdy:end -->''' % {
        'upd': now.strftime('%a, %b ') + str(now.day), 'rg': n(t['gamesPlayed']), 'yds': n(t['passingYards']),
        'td': n(t['passingTouchdowns']), 'int': n(t['interceptions']), 'rate': n(t['QBRating']),
        'rw': reg[0], 'rl': reg[1], 'pg': n(pt['gamesPlayed']), 'pw': post[0], 'pl': post[1],
        'ptd': n(pt['passingTouchdowns']), 'pint': n(pt['interceptions']), 'prate': n(pt['QBRating']),
        'regtable': pass_table('Regular season passing by season', reg_stats),
        'posttable': pass_table('Playoff passing by season', post_stats),
        'ra': n(rush['rushingAttempts']), 'ry': n(rush['rushingYards']), 'rtd': n(rush['rushingTouchdowns']),
        'pra': n(prush['rushingAttempts']), 'pry': n(prush['rushingYards']), 'prtd': n(prush['rushingTouchdowns']),
        'prs': '' if str(prush['rushingTouchdowns']) == '1' else 's',
        'qual': qual, 'leader': LEADER_NOTE, 'link': LINK}


def article(picture, reg_region):
    L = LINK
    return '''<article class="article" role="main" aria-labelledby="article-title">
  <span class="tag">49ers</span>
  <h1 id="article-title">%(h1)s</h1>
  <p style="font-size:19px;color:#cdd2db;margin:-4px 0 20px;font-style:italic">A permanent page for the argument that won't go away: the career numbers, the playoff record, the records genuinely within reach and the ones that aren't, kept current as the seasons go.</p>
  <div class="byline">Bay Area Sports Blog Staff &middot; 49ers</div>
  %(picture)s

  <p>This is the argument that has followed Brock Purdy since the day he took over, and it never resolves, because both sides are arguing about different things. One side points at the numbers. The other side points at the roster around him. This page exists to keep the numbers straight, and the tables below refresh on their own.</p>

  <h2>Brock Purdy career stats</h2>
%(region)s

  <h2>The playoff record</h2>
  <p>Purdy has started every one of his playoff games. The first run ended in the NFC Championship Game in Philadelphia, where he got hurt early and the 49ers lost 31 to 7. The second ended in overtime of the Super Bowl against Kansas City, 25 to 22, the game this fan base <a href="49ers-still-paying-for-vegas.html" %(L)s>is still paying for</a>. Last season he won the Wild Card game in Philadelphia 23 to 19 and then lost 41 to 6 in Seattle. His playoff passer rating sits well below his regular season number, and that gap is the most honest criticism anyone has of him.</p>

  <h2>The honest caveat</h2>
  <p>Anyone arguing in good faith has to hold this at the same time as the numbers. Passer rating rewards efficiency, and Purdy has played his entire career in an offense designed by one of the best offensive minds in football, throwing to a tight end who will end up in Canton and a running back who was, for a stretch, the most dangerous weapon in the sport. Nobody produces numbers like these alone. That's true, and it doesn't make them disappear.</p>

  <h2>What he can reach, and what he can't</h2>
  <p>The career passer rating record is the closest thing and the most likely. Beyond that, the things worth watching need volume: career completion percentage among qualified passers, yards per attempt, and the win totals quarterbacks get credited with whether they deserve it or not. All of it needs him healthy and behind a functioning line.</p>
  <p>What isn't reachable is worth saying plainly. He isn't catching the career yardage and touchdown leaderboards. Those belong to quarterbacks who played twenty years and threw six hundred times a season, and Purdy started late enough that the arithmetic doesn't work. Anyone framing his career as a chase for those numbers is selling something.</p>

  <h2>Measured against Montana and Young</h2>
  <p>This is the franchise of Joe Montana and Steve Young, and any quarterback who plays well in this uniform gets measured against two Hall of Famers who won here. It's an unfair standard and it's also the correct one, because it's the standard the building sets. Purdy's career passer rating is higher than either of theirs. He also has none of the hardware, and around here the hardware is the argument. The full story of that rivalry is in <a href="montana-young-49ers-quarterback-controversy.html" %(L)s>Two Hall of Famers, One Job</a>, and the titles are counted in <a href="bay-area-championships-complete-list-by-team.html" %(L)s>every Bay Area championship</a> and <a href="49ers-dynasty-team-of-the-decade.html" %(L)s>the dynasty years</a>.</p>

  <h2>Keep reading</h2>
  <p>The season so far, game by game, is on the <a href="49ers-2026-schedule-season-hub.html" %(L)s>49ers schedule page</a>. Who is catching his passes and who is protecting him is in the <a href="49ers-2026-roster-depth-chart.html" %(L)s>roster and depth chart</a>, and who is hurt this week is on the <a href="49ers-injury-report.html" %(L)s>49ers injury report</a>. The fan's case after three games is <a href="brock-purdy-best-quarterback-stats-dont-lie-kyle-kittle-excuses.html" %(L)s>Brock Purdy might be the best QB ever</a>, and the preseason view is in the <a href="49ers-2026-season-preview-roster-schedule-questions.html" %(L)s>2026 season preview</a>. Everything else is on the <a href="../49ers.html" %(L)s>49ers hub</a>.</p>

  <p style="margin-top:24px;color:var(--muted);font-size:14px">Statistics: ESPN, read automatically. The qualified passer rating leaders are from the league's career list as compiled by Pro Football Reference and are dated in the text.</p>
  <p style="margin-top:30px;color:var(--muted);font-size:15px">More coverage: <a href="../49ers.html" style="color:var(--accent2);font-weight:700">49ers</a> &middot; <a href="../nfl.html" style="color:var(--accent2);font-weight:700">NFL</a></p>
</article>''' % {'picture': picture, 'region': reg_region, 'L': L, 'h1': H1}


def main():
    now = datetime.datetime.now(PACIFIC)
    try:
        reg_stats, post_stats = season_stats(2), season_stats(3)
        reg, post, games = records(now)
    except Exception as exc:
        print('FEED FAILED (%s), page left as is' % exc.__class__.__name__)
        raise SystemExit(1)
    text = open(PAGE, encoding='utf-8', newline='').read()
    picture = re.search(r'<picture>.*?</picture>(?:</picture>)?', text, re.S).group(0)
    text = re.sub(r'<article class="article".*?</article>',
                  lambda m: article(picture, region(reg_stats, post_stats, reg, post, now)), text, flags=re.S)
    esc = html.escape
    text = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % esc(TITLE, quote=False), text, count=1)
    for sel in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        text = re.sub(r'<meta %s content="[^"]*">' % sel, '<meta %s content="%s">' % (sel, esc(DESC)), text)
    for sel in ('property="og:title"', 'name="twitter:title"'):
        text = re.sub(r'<meta %s content="[^"]*">' % sel, '<meta %s content="%s">' % (sel, esc(TITLE)), text)
    text = re.sub(r'("description":")[^"]*(")', lambda m: m.group(1) + DESC + m.group(2), text, count=1)
    # dateModified follows the data: the date of his most recent game, not the run date
    last_game = max(d for d, _k, _g in games) if games else now.date().isoformat()
    text = re.sub(r'"dateModified":"[^"]*"', '"dateModified":"%s"' % last_game, text, count=1)
    text = re.sub(r'("headline":")[^"]*(")', lambda m: m.group(1) + H1 + m.group(2), text, count=1)
    text = re.sub(r'("position":3,"name":")[^"]*(")', lambda m: m.group(1) + H1 + m.group(2), text, count=1)
    open(PAGE, 'w', encoding='utf-8', newline='').write(text)
    print('purdy: regular %d-%d, playoffs %d-%d' % (reg[0], reg[1], post[0], post[1]))


if __name__ == '__main__':
    main()
