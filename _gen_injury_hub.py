#!/usr/bin/env python3
"""_gen_injury_hub.py: the Bay Area injury report, every team on one page.

articles/bay-area-injury-report.html is built from the team pages themselves: it reads the
region between the injuries markers on each team's report (written minutes earlier by
_gen_niners_injuries.py, _gen_warriors_injuries.py and _gen_team_injuries.py) and lays them
out one team after another. It fetches nothing, so it can never disagree with the team pages.

Run it after the team generators:

    python _gen_injury_hub.py
"""
import os
import re
import html
import datetime

import _gen_niners_injuries as core

TEAMS = [('49ers', '49ers-injury-report', '49ers.html', 'NFL'),
         ('Raiders', 'raiders-injury-report', 'nfl.html', 'NFL'),
         ('Warriors', 'warriors-injury-report', 'warriors.html', 'NBA'),
         ('Giants', 'giants-injury-report', 'giants.html', 'MLB'),
         ("A's", 'athletics-injury-report', 'athletics.html', 'MLB'),
         ('Sharks', 'sharks-injury-report', 'sharks.html', 'NHL')]

core.SLUG = 'bay-area-injury-report'
core.PAGE = os.path.join(core.ROOT, 'articles', core.SLUG + '.html')
core.TEMPLATE = os.path.join(core.ROOT, 'articles', '49ers-injury-report.html')
core.TEAM_NAME, core.SPORT, core.SECTION = 'Bay Area sports teams', 'Multiple', 'Bay Area'
core.HUB_NAME, core.HUB_FILE, core.PAGE_NAME = 'Bay Area', 'bayarea.html', 'Bay Area Injury Report'
core.PUBLISHED = '2026-11-13'
core.TITLE = 'Bay Area Injury Report: 49ers, Raiders, Warriors, Giants'
core.DESC = ("Every Bay Area team's injury report on one page: the 49ers, Raiders, Warriors, Giants, A's "
             "and Sharks, with each injury, the status and when the player is expected back.")
LINK = core.LINK


def team_block(label, slug, hub, league):
    path = os.path.join(core.ROOT, 'articles', slug + '.html')
    if not os.path.exists(path):
        return None, None
    t = open(path, encoding='utf-8').read()
    m = re.search(re.escape(core.START) + r'(.*?)' + re.escape(core.END), t, re.S)
    if not m:
        return None, None
    region = m.group(1).strip()
    lead = re.search(r'<p><b>Updated (.*?)\.</b> (.*?)</p>', region, re.S)
    rows = len(re.findall(r'<tr><td>', region))
    anchor = slug.replace('-injury-report', '')
    block = ('  <section id="%s" style="scroll-margin-top:80px">\n  <h2>%s injury report</h2>\n  %s\n'
             '  <p><a href="%s.html" %s>Full %s injury report</a> &middot; <a href="../%s" %s>%s news</a></p>\n'
             '  </section>\n' % (anchor, html.escape(label), region, slug, LINK, html.escape(label), hub, LINK,
                                html.escape(label)))
    glance = '<tr><td><a href="#%s" %s>%s</a></td><td>%s</td><td>%d</td><td>%s</td></tr>' % (
        anchor, LINK, html.escape(label), league, rows,
        html.escape(lead.group(1)) if lead else 'not yet')
    return block, glance


def article(now, nxt, rows, cover):
    blocks, glance = [], []
    for label, slug, hub, league in TEAMS:
        b, g = team_block(label, slug, hub, league)
        if b:
            blocks.append(b)
            glance.append(g)
    jump = ' &middot; '.join('<a href="#%s" %s>%s</a>' % (s.replace('-injury-report', ''), LINK, html.escape(l))
                             for l, s, _h, _lg in TEAMS)
    return ('''<article class="article" role="main" aria-labelledby="article-title">
  <span class="tag">Bay Area</span>
  <h1 id="article-title">Bay Area Injury Report</h1>
  <p style="font-size:19px;color:#cdd2db;margin:-4px 0 20px;font-style:italic">Every Bay Area team on one page: who is hurt, how bad it is, and when he is expected back.</p>
  <div class="byline">Bay Area Sports Blog Staff &middot; Bay Area &middot; Updated %(upd)s</div>
  <picture><source type="image/webp" srcset="../assets/img/cards/%(slug)s-400w.webp 400w, ../assets/img/cards/%(slug)s-600w.webp 600w, ../assets/img/cards/%(slug)s-800w.webp 800w, ../assets/img/cards/%(slug)s.webp 1200w" sizes="(max-width: 820px) 92vw, 760px"><img src="../assets/img/cards/%(slug)s.jpg" alt="%(alt)s" width="1200" height="675" decoding="async" fetchpriority="high" srcset="../assets/img/cards/%(slug)s-400w.jpg 400w, ../assets/img/cards/%(slug)s-600w.jpg 600w, ../assets/img/cards/%(slug)s-800w.jpg 800w, ../assets/img/cards/%(slug)s.jpg 1200w" sizes="(max-width: 820px) 92vw, 760px"></picture>

  <p>The 49ers, the Raiders, the Warriors, the Giants, the A's and the Sharks, all in one place. Yes, the Raiders and the A's left town. Their fans did not, so they stay on the list. Every table refreshes several times a day from the league injury reports, so this one link is all you need.</p>
  <p><b>Jump to:</b> %(jump)s</p>

  <div class="reftable" role="region" tabindex="0" aria-label="Injury reports at a glance">
<table>
<caption>At a glance</caption>
<thead><tr><th>Team</th><th>League</th><th>Players listed</th><th>Last refreshed</th></tr></thead>
<tbody>
%(glance)s
</tbody>
</table>
</div>

%(blocks)s
  <h2>How to read it</h2>
  <p><b>Out</b> means he misses the next game. <b>Doubtful</b> means he probably will too, <b>questionable</b> is a real maybe, and <b>probable</b> means expect him out there. <b>Day to day</b> means a minor problem, decided game by game. <b>Injured reserve</b> in football and hockey, and the <b>injured list</b> in baseball, take a player off the active roster for a set minimum stretch.</p>
%(backnote)s

  <h2>Where the numbers come from</h2>
  <p>Status, designation and injury come from the league injury reports as published through ESPN, read automatically several times a day. Nothing in the tables is typed in by hand. See our <a href="../editorial-standards.html" %(link)s>editorial standards</a> and <a href="../corrections.html" %(link)s>corrections policy</a>.</p>
%(siblings)s
  <p style="margin-top:30px;color:var(--muted);font-size:15px">More coverage: <a href="../bayarea.html" style="color:var(--accent2);font-weight:700">Bay Area</a> &middot; <a href="../nfl.html" style="color:var(--accent2);font-weight:700">NFL</a> &middot; <a href="../nba.html" style="color:var(--accent2);font-weight:700">NBA</a> &middot; <a href="../mlb.html" style="color:var(--accent2);font-weight:700">MLB</a> &middot; <a href="../nhl.html" style="color:var(--accent2);font-weight:700">NHL</a></p>
</article>''' % {'upd': core.day(now), 'slug': core.SLUG, 'alt': html.escape(core.CARD_ALTS.get('hub', 'Bay Area injury report'), quote=True),
                 'jump': jump, 'glance': '\n'.join(glance), 'blocks': '\n'.join(blocks),
                 'backnote': core.BACKNOTE, 'link': LINK, 'siblings': core.siblings()})


def main():
    now = datetime.datetime.now(core.PACIFIC)
    base = open(core.PAGE if os.path.exists(core.PAGE) else core.TEMPLATE, encoding='utf-8', newline='').read()
    page = core.build_head(base, now)
    page = re.sub(r'<article class="article".*?</article>', lambda m: article(now, None, [], []), page, flags=re.S)
    if not os.path.exists(core.PAGE):     # the template's related strip is 49ers only; point it at the teams
        rel = ''.join('    <a href="%s.html"><div class="rc">%s</div><h4>%s Injury Report</h4></a>\n' % (s, html.escape(l), html.escape(l))
                      for l, s, _h, _lg in TEAMS[:3])
        page = re.sub(r'(<div class="rel-grid">\s*\n).*?(\s*</div>\s*</section>)', lambda m: m.group(1) + rel.rstrip('\n') + m.group(2), page, count=1, flags=re.S)
    open(core.PAGE, 'w', encoding='utf-8', newline='').write(page)
    print('bay area injury hub: %d teams' % page.count('<section id='))


if __name__ == '__main__':
    main()
