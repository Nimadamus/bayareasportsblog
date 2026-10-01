#!/usr/bin/env python3
"""_gen_warriors_injuries.py: the Warriors injury report, one permanent URL.

Same machinery as _gen_niners_injuries.py (read that docstring for the rules: no return
dates, no copied comment text, no invented practice data). This file only swaps in the
Warriors feed, the NBA status vocabulary and the Warriors page copy.

NBA teams have no injured reserve, so the page has two tables: players ruled out, and
players listed day to day, questionable, doubtful or probable.

    python _gen_warriors_injuries.py
"""
import os
import html

import _gen_niners_injuries as core

core.SLUG = 'warriors-injury-report'
core.PAGE = os.path.join(core.ROOT, 'articles', core.SLUG + '.html')
core.TEMPLATE = os.path.join(core.ROOT, 'articles', 'warriors-2026-27-roster-depth-chart.html')
core.FEED = 'https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/teams/9/injuries?limit=200'
core.SCHED = 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/gs/schedule'
core.TEAM_ABBR = 'GS'
core.TEAM_NAME, core.SPORT, core.SECTION = 'Golden State Warriors', 'Basketball', 'Warriors'
core.HUB_NAME, core.HUB_FILE, core.PAGE_NAME = 'Warriors', 'warriors.html', 'Warriors Injury Report'
core.COVER_PREFIXES = ('warriors', 'stephen-curry', 'steph-curry', 'jimmy-butler', 'draymond')
core.LIST_LABELS = {}
core.TITLE = 'Warriors Injury Report: Who Is Out and Who Is Day to Day'
core.DESC = ('The current Golden State Warriors injury report: every player ruled out or listed '
             'day to day, with the injury, the status and the latest update.')
LINK = core.LINK
day = core.day


def region(rows, now, nxt, cover):
    for r in rows:                     # the feed spells it Day-To-Day
        if r['status'] == 'Day-To-Day':
            r['status'] = 'Day to day'
    out = [r for r in rows if r['status'] == 'Out']
    listed = [r for r in rows if r['status'] not in ('Out', 'Active')]
    cleared = [r for r in rows if r['status'] == 'Active']
    parts = ['<p><b>Updated %s.</b> %d ruled out, %d day to day or questionable.%s</p>' % (
        day(now, True), len(out), len(listed),
        (' Next game: %s.' % html.escape(nxt)) if nxt else '')]
    parts.append(core.table('Out', out, cover))
    parts.append(core.table('Day to day, questionable or doubtful', listed, cover))
    if not out and not listed:
        parts.append('<p>Nobody is on the injury report right now.</p>')
    if cleared:
        names = ', '.join('%s (%s)' % (html.escape(r['name']), html.escape(r['pos']))
                          for r in sorted(cleared, key=lambda r: r['name']))
        parts.append('<p><b>Back off the report in the last %d days:</b> %s.</p>' % (core.CLEARED_DAYS, names))
    return core.START + '\n' + '\n'.join(p for p in parts if p) + '\n' + core.END


def article(now, nxt, rows, cover):
    recent = ''.join('<li><a href="%s.html" %s>%s</a></li>' % (s, LINK, html.escape(t)) for _, s, t in cover[:6])
    recent_block = ('  <h2>Our Warriors injury coverage</h2>\n  <ul>%s</ul>\n' % recent) if recent else ''
    return ('''<article class="article" role="main" aria-labelledby="article-title">
  <span class="tag">Warriors</span>
  <h1 id="article-title">Warriors Injury Report</h1>
  <p style="font-size:19px;color:#cdd2db;margin:-4px 0 20px;font-style:italic">Who is out and who is day to day for Golden State, kept current through the season at this one address.</p>
  <div class="byline">Bay Area Sports Blog Staff &middot; Warriors &middot; Updated %(upd)s</div>
  <picture><source type="image/webp" srcset="../assets/img/cards/%(slug)s-400w.webp 400w, ../assets/img/cards/%(slug)s-600w.webp 600w, ../assets/img/cards/%(slug)s-800w.webp 800w, ../assets/img/cards/%(slug)s.webp 1200w" sizes="(max-width: 820px) 92vw, 760px"><img src="../assets/img/cards/%(slug)s.jpg" alt="Warriors injury report card from Bay Area Sports Blog" width="1200" height="675" decoding="async" fetchpriority="high" srcset="../assets/img/cards/%(slug)s-400w.jpg 400w, ../assets/img/cards/%(slug)s-600w.jpg 600w, ../assets/img/cards/%(slug)s-800w.jpg 800w, ../assets/img/cards/%(slug)s.jpg 1200w" sizes="(max-width: 820px) 92vw, 760px"></picture>

  <p>Check this page before a Warriors game. Every player on the league injury report is here with his position, the injury, his status and when it last changed. It refreshes several times a day, so the link never changes from one week to the next.</p>

  <h2>The current report</h2>
%(region)s

  <h2>How to read it</h2>
  <p><b>Out</b> means he will not play in the next game. <b>Day to day</b> means the injury is minor enough that the call gets made close to tip off, and on game day the league report turns that into <b>questionable</b>, <b>doubtful</b> or <b>probable</b>. The NBA has no injured reserve, so a long injury simply stays on the report as out.</p>
  <p>You will not find return dates here unless the team has announced one. Estimated timelines are guesses, and we do not print guesses as news. The same goes for practice participation: if the feed does not report it, we do not make it up.</p>

  <h2>Where the numbers come from</h2>
  <p>Status and injury come from the league injury report as published through ESPN, read automatically. Nothing in the tables is typed in by hand. See our <a href="../editorial-standards.html" %(link)s>editorial standards</a> and <a href="../corrections.html" %(link)s>corrections policy</a>.</p>

%(recent)s  <p>For who plays when somebody sits, see the <a href="warriors-2026-27-roster-depth-chart.html" %(link)s>Warriors depth chart</a> and our <a href="warriors-2026-27-projected-rotation.html" %(link)s>projected rotation</a>. Every game and result is on the <a href="warriors-2026-27-schedule-season-hub.html" %(link)s>Warriors schedule page</a>, and the long view of the roster is in the <a href="warriors-2026-27-season-outlook.html" %(link)s>season outlook</a>.</p>

  <p style="margin-top:30px;color:var(--muted);font-size:15px">More coverage: <a href="../warriors.html" style="color:var(--accent2);font-weight:700">Warriors</a> &middot; <a href="../nba.html" style="color:var(--accent2);font-weight:700">NBA</a></p>
</article>''' % {'upd': day(now), 'slug': core.SLUG, 'region': region(rows, now, nxt, cover),
                 'recent': recent_block, 'link': LINK})


core.region = region
core.article = article

if __name__ == '__main__':
    core.main()
