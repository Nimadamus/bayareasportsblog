#!/usr/bin/env python3
"""_gen_team_injuries.py: the Raiders, Giants, A's and Sharks injury reports.

Same machinery as _gen_niners_injuries.py (read that docstring: the feed, the Expected back
rules, no copied comment text, no invented practice data). This file only holds each
team's feed, its league's status vocabulary and its page copy.

    python _gen_team_injuries.py raiders
    python _gen_team_injuries.py giants athletics sharks raiders    (any order, one per run)
"""
import os
import sys
import html
import subprocess

import _gen_niners_injuries as core

LINK = core.LINK
day = core.day

TEAMS = {
    'raiders': dict(
        league='nfl', espn='football/leagues/nfl/teams/13', sched='football/nfl/teams/lv', abbr='LV',
        name='Las Vegas Raiders', sport='American football', section='NFL', tag='Raiders',
        hub=('NFL', 'nfl.html'), template='raiders-2026-season-preview-kubiak-cousins-mendoza-jeanty',
        cover=('raiders',), short='Raiders',
        dek='Who is out, who is questionable and who is on injured reserve for the Silver and Black, kept current through the season at this one address.',
        intro='The Raiders left Oakland, but half the Bay Area still bleeds silver and black, so they get the same daily report as everybody else. Every player on the league injury report is here with his position, the injury, his status, when he is expected back and when it last changed.',
        more=[('raiders-2026-season-preview-kubiak-cousins-mendoza-jeanty', 'our 2026 Raiders season preview')],
        foot=[('../nfl.html', 'NFL'), ('../bayarea.html', 'Bay Area')]),
    'giants': dict(
        league='mlb', espn='baseball/leagues/mlb/teams/26', sched='baseball/mlb/teams/sf', abbr='SF',
        name='San Francisco Giants', sport='Baseball', section='Giants', tag='Giants',
        hub=('Giants', 'giants.html'), template='giants-2026-roster-depth-chart',
        cover=('giants',), short='Giants',
        dek='Who is on the injured list, who is day to day, and when each one is expected back, kept current all year at this one address.',
        intro='Check this page before a Giants game, and through the winter while the rehab list sorts itself out. Every player on the injury report is here with his position, the injury, his status, when he is expected back and when it last changed.',
        more=[('giants-2026-roster-depth-chart', 'Giants roster and depth chart'),
              ('giants-2026-season-hub-results-coverage', '2026 season results')],
        foot=[('../giants.html', 'Giants'), ('../mlb.html', 'MLB')]),
    'athletics': dict(
        league='mlb', espn='baseball/leagues/mlb/teams/11', sched='baseball/mlb/teams/ath', abbr='ATH',
        name='Athletics', sport='Baseball', section='Athletics', tag="A's",
        hub=("A's", 'athletics.html'), template='athletics-2026-roster-depth-chart',
        cover=('athletics',), short="A's",
        dek="Who is on the injured list, who is day to day, and when each one is expected back for the A's, kept current all year at this one address.",
        intro="The A's play in Sacramento now, but they are still the A's to a lot of us. Every player on their injury report is here with his position, the injury, his status, when he is expected back and when it last changed.",
        more=[('athletics-2026-roster-depth-chart', "A's roster and depth chart"),
              ('athletics-2027-outlook-kurtz-de-vries-injuries', 'what 2027 looks like')],
        foot=[('../athletics.html', "A's"), ('../mlb.html', 'MLB')]),
    'sharks': dict(
        league='nhl', espn='hockey/leagues/nhl/teams/18', sched='hockey/nhl/teams/sj', abbr='SJ',
        name='San Jose Sharks', sport='Ice hockey', section='Sharks', tag='Sharks',
        hub=('Sharks', 'sharks.html'), template='sharks-2026-27-roster-depth-chart',
        cover=('sharks', 'macklin-celebrini'), short='Sharks',
        dek='Who is on injured reserve, who is out and who is day to day for San Jose, kept current through the season at this one address.',
        intro='Check this page before a Sharks game. Every player on the injury report is here with his position, the injury, his status, when he is expected back and when it last changed.',
        more=[('sharks-2026-27-roster-depth-chart', 'Sharks roster and depth chart'),
              ('sharks-2026-27-schedule-season-hub', '2026-27 schedule')],
        foot=[('../sharks.html', 'Sharks'), ('../nhl.html', 'NHL')]),
}

HOWTO = {
    'nfl': ('<b>Out</b> means he will not play in the next game. <b>Doubtful</b> means he is unlikely to. '
            '<b>Questionable</b> is a genuine maybe, and plenty of questionable players suit up. '
            '<b>Injured reserve</b> takes a player off the active roster for at least four games, and '
            '<b>PUP</b> is the physically unable to perform list, for players still recovering from an injury they already had.'),
    'mlb': ('<b>Out</b> means he is on the injured list or otherwise unavailable. The injured list comes in a '
            '10 day version for position players, a 15 day version for pitchers, a 7 day concussion list, and a '
            '60 day list that also takes him off the 40 man roster. <b>Day to day</b> means a minor problem, '
            'decided game by game. Over the winter the list stays up with the players rehabbing for spring.'),
    'nhl': ('<b>Injured reserve</b> means he is out at least a week and is off the active roster. '
            '<b>Non roster</b> injured reserve is for a player hurt before the season started, and '
            '<b>long term</b> injured reserve is for a player out at least 10 games and 24 days. '
            '<b>Out</b> means he will miss the next game, and <b>day to day</b> means a minor problem, decided game by game.'),
}

LABELS = {
    'nfl': core.LIST_LABELS,
    'mlb': {'7-DAY IL': '7 day IL', '10-DAY IL': '10 day IL', '15-DAY IL': '15 day IL', '60-DAY IL': '60 day IL'},
    'nhl': {'IR-NR': 'non roster', 'IR-LT': 'long term', 'LTIR': 'long term'},
}


def summary(now, nxt, counts):
    words = ', '.join('%d %s' % (n, w) for w, n in counts)
    return '<p><b>Updated %s.</b> %s.%s</p>' % (day(now, True), words[0].upper() + words[1:],
                                                (' Next game: %s.' % html.escape(nxt)) if nxt else '')


def cleared_line(cleared):
    if not cleared:
        return ''
    names = ', '.join('%s (%s)' % (html.escape(r['name']), html.escape(r['pos']))
                      for r in sorted(cleared, key=lambda r: r['name']))
    return '<p><b>Back off the report in the last %d days:</b> %s.</p>' % (core.CLEARED_DAYS, names)


def region_mlb(rows, now, nxt, cover):
    for r in rows:      # a Day-To-Day entry that carries an IL tag is on the injured list
        if r['list'].upper().endswith(' IL') and r['status'] != 'Active':
            r['status'] = 'Out'
            r['back'] = core.expected(r)
    out = [r for r in rows if r['status'] == 'Out']
    dtd = [r for r in rows if r['status'] not in ('Out', 'Active')]
    cleared = [r for r in rows if r['status'] == 'Active']
    parts = [summary(now, nxt, [('on the injured list or out', len(out)), ('day to day', len(dtd))]),
             core.table('Injured list and out', out, cover),
             core.table('Day to day', dtd, cover)]
    if not out and not dtd:
        parts.append('<p>Nobody is on the injury report right now.</p>')
    parts.append(cleared_line(cleared))
    return core.START + '\n' + '\n'.join(p for p in parts if p) + '\n' + core.END


def region_nhl(rows, now, nxt, cover):
    ir = [r for r in rows if r['status'] == 'Injured Reserve' or r['list'].upper() in LABELS['nhl']]
    out = [r for r in rows if r['status'] == 'Out' and r not in ir]
    dtd = [r for r in rows if r['status'] not in ('Out', 'Active') and r not in ir]
    cleared = [r for r in rows if r['status'] == 'Active']
    parts = [summary(now, nxt, [('on injured reserve', len(ir)), ('out', len(out)), ('day to day', len(dtd))]),
             core.table('Injured reserve', ir, cover), core.table('Out', out, cover),
             core.table('Day to day', dtd, cover)]
    if not ir and not out and not dtd:
        parts.append('<p>Nobody is on the injury report right now.</p>')
    parts.append(cleared_line(cleared))
    return core.START + '\n' + '\n'.join(p for p in parts if p) + '\n' + core.END


def make_article(key, cfg):
    def article(now, nxt, rows, cover):
        more = ' and '.join('<a href="%s.html" %s>%s</a>' % (s, LINK, html.escape(t)) for s, t in cfg['more'])
        recent = ''.join('<li><a href="%s.html" %s>%s</a></li>' % (s, LINK, html.escape(t)) for _, s, t in cover[:6])
        recent_block = ('  <h2>Our %s injury coverage</h2>\n  <ul>%s</ul>\n' % (html.escape(cfg['short']), recent)) if recent else ''
        foot = ' &middot; '.join('<a href="%s" style="color:var(--accent2);font-weight:700">%s</a>' % (h, html.escape(n))
                                 for h, n in cfg['foot'])
        return ('''<article class="article" role="main" aria-labelledby="article-title">
  <span class="tag">%(tag)s</span>
  <h1 id="article-title">%(page)s</h1>
  <p style="font-size:19px;color:#cdd2db;margin:-4px 0 20px;font-style:italic">%(dek)s</p>
  <div class="byline">Bay Area Sports Blog Staff &middot; %(tag)s &middot; Updated %(upd)s</div>
  <picture><source type="image/webp" srcset="../assets/img/cards/%(slug)s-400w.webp 400w, ../assets/img/cards/%(slug)s-600w.webp 600w, ../assets/img/cards/%(slug)s-800w.webp 800w, ../assets/img/cards/%(slug)s.webp 1200w" sizes="(max-width: 820px) 92vw, 760px"><img src="../assets/img/cards/%(slug)s.jpg" alt="%(alt)s" width="1200" height="675" decoding="async" fetchpriority="high" srcset="../assets/img/cards/%(slug)s-400w.jpg 400w, ../assets/img/cards/%(slug)s-600w.jpg 600w, ../assets/img/cards/%(slug)s-800w.jpg 800w, ../assets/img/cards/%(slug)s.jpg 1200w" sizes="(max-width: 820px) 92vw, 760px"></picture>

  <p>%(intro)s It refreshes several times a day, so the link never changes.</p>

  <h2>The current report</h2>
%(region)s

  <h2>How to read it</h2>
  <p>%(howto)s</p>
%(backnote)s

  <h2>Where the numbers come from</h2>
  <p>Status, designation and injury come from the league injury report as published through ESPN, read automatically. Nothing in the tables is typed in by hand. When the team announces something the feed has not caught yet, it shows up here on the next refresh, usually within a few hours. See our <a href="../editorial-standards.html" %(link)s>editorial standards</a> and <a href="../corrections.html" %(link)s>corrections policy</a>.</p>

%(recent)s  <p>For more, see %(more)s.</p>
%(siblings)s
  <p style="margin-top:30px;color:var(--muted);font-size:15px">More coverage: %(foot)s</p>
</article>''' % {'tag': html.escape(cfg['tag']), 'page': html.escape(core.PAGE_NAME), 'dek': html.escape(cfg['dek']),
                 'upd': day(now), 'slug': core.SLUG, 'alt': html.escape(core.CARD_ALT, quote=True),
                 'intro': html.escape(cfg['intro']), 'region': core.region(rows, now, nxt, cover),
                 'howto': HOWTO[cfg['league']], 'backnote': core.BACKNOTE, 'link': LINK,
                 'recent': recent_block, 'more': more, 'siblings': core.siblings(), 'foot': foot})
    return article


def configure(key):
    cfg = TEAMS[key]
    core.SLUG = '%s-injury-report' % key
    core.PAGE = os.path.join(core.ROOT, 'articles', core.SLUG + '.html')
    core.TEMPLATE = os.path.join(core.ROOT, 'articles', cfg['template'] + '.html')
    core.FEED = 'https://sports.core.api.espn.com/v2/sports/%s/injuries?limit=200' % cfg['espn']
    core.SCHED = 'https://site.api.espn.com/apis/site/v2/sports/%s/schedule' % cfg['sched']
    core.TEAM_ABBR, core.LEAGUE = cfg['abbr'], cfg['league']
    core.TEAM_NAME, core.SPORT, core.SECTION = cfg['name'], cfg['sport'], cfg['section']
    core.HUB_NAME, core.HUB_FILE = cfg['hub']
    core.PAGE_NAME = '%s Injury Report' % cfg['short']
    core.CARD_ALT = core.CARD_ALTS.get(key, '%s injury report' % cfg['short'])
    core.PUBLISHED = '2026-11-13'
    core.COVER_PREFIXES = cfg['cover']
    core.LIST_LABELS = LABELS[cfg['league']]
    st = {'nfl': 'Who Is Out, Questionable and on IR', 'mlb': 'Who Is on the IL and When They Return',
          'nhl': 'Who Is Out and on Injured Reserve'}[cfg['league']]
    core.TITLE = '%s Injury Report Today: %s' % (cfg['short'], st)
    core.DESC = ('The current %s injury report: every player listed, the injury, the status and when he is '
                 'expected back, refreshed several times a day.' % cfg['name'])
    if cfg['league'] == 'mlb':
        core.region = region_mlb
    elif cfg['league'] == 'nhl':
        core.region = region_nhl
    core.article = make_article(key, cfg)


if __name__ == '__main__':
    keys = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(keys) > 1:      # the core module holds one team at a time, so run each in its own process
        rc = 0
        for k in keys:
            rc |= subprocess.call([sys.executable, os.path.abspath(__file__), k])
        sys.exit(rc)
    if not keys or keys[0] not in TEAMS:
        sys.exit('usage: _gen_team_injuries.py %s' % ' | '.join(TEAMS))
    configure(keys[0])
    core.main()
