#!/usr/bin/env python3
"""_giants_cluster.py: the Giants authority foundation.

The Giants archive is the largest on the site: 46 articles, 20 of them game recaps, and
the strongest evergreen pages anywhere on the blog. What it does not have is furniture -
a roster page, a page that says where the rebuild actually stands after the selloff, a
records page, or anything about the ballpark itself.

Deliberately NOT duplicated, the archive already owns these:
  bryce-eldridge-giants-future-franchise-first-baseman  1,515w, the definitive Eldridge piece
  giants-season-over-build-around-eldridge-posey-bullpen 26 inbound, the July argument
  giants-trade-deadline-monday-posey-sell-ramos-arraez-ray  the deadline column
  tony-vitello-hire-giants-mistake / -not-ready / -clueless-lineups  the manager case
  barry-bonds-giants-home-run-king  the Bonds column
  giants-dynasty-even-year-magic / flashback-bumgarner / bruce-bochy  the dynasty
  giants-1993-pennant-race-*  the 1993 race
  giants-oracle-park-still-waiting  the October drought column, NOT a park guide

  python _giants_cluster.py [--check]
"""
import os, re, sys, subprocess
import _college_cluster as CC

ROOT = os.path.dirname(os.path.abspath(__file__))

N = lambda v: '<td class="num">%s</td>' % v
LINE = lambda team, innings, r, h, e: ('<tr><td>%s</td>%s<td class="num"><b>%s</b></td>'
                                       '<td class="num">%s</td><td class="num">%s</td></tr>'
                                       % (team, ''.join(N(x) for x in innings), r, h, e))
LINEHEAD = ('<thead><tr><th>Team</th>' + ''.join('<th class="num">%d</th>' % i
                                                 for i in range(1, 10))
            + '<th class="num">R</th><th class="num">H</th><th class="num">E</th></tr></thead>')

GIANTS_ASTROS_LINE = ('<div class="reftable">\n<table>\n<caption>Houston Astros at San '
                      'Francisco Giants, Tuesday 11 August 2026, Oracle Park, '
                      '30,093</caption>\n' + LINEHEAD + '\n<tbody>\n'
                      + LINE('Houston', [0, 1, 0, 0, 0, 0, 0, 0, 0], 1, 5, 2) + '\n'
                      + LINE('<b>San Francisco</b>', [0, 1, 0, 1, 1, 1, 0, 0, 'X'], 4, 9, 0)
                      + '\n</tbody>\n</table>\n</div>')

GIANTS_ASTROS_BOX = """<div class="reftable">
<table>
<caption>Pitching, Astros at Giants, 11 August 2026</caption>
<thead><tr><th>Pitcher</th><th class="num">IP</th><th class="num">H</th><th class="num">R</th><th class="num">ER</th><th class="num">BB</th><th class="num">SO</th><th class="num">P</th></tr></thead>
<tbody>
<tr><td>Hunter Brown, HOU (L)</td><td class="num">5.0</td><td class="num">5</td><td class="num">3</td><td class="num">3</td><td class="num">3</td><td class="num">4</td><td class="num">89</td></tr>
<tr><td>Enyel De Los Santos, HOU</td><td class="num">0.2</td><td class="num">2</td><td class="num">1</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">11</td></tr>
<tr><td>Bennett Sousa, HOU</td><td class="num">1.1</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">3</td><td class="num">19</td></tr>
<tr><td>AJ Blubaugh, HOU</td><td class="num">1.0</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">1</td><td class="num">18</td></tr>
<tr><td><b>Carson Whisenhunt, SF (W)</b></td><td class="num">5.2</td><td class="num">4</td><td class="num">1</td><td class="num">1</td><td class="num">3</td><td class="num">2</td><td class="num">96</td></tr>
<tr><td>Carson Seymour, SF</td><td class="num">2.0</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">2</td><td class="num">30</td></tr>
<tr><td>Reiver Sanmartin, SF</td><td class="num">0.1</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">5</td></tr>
<tr><td>JT Brubaker, SF (S)</td><td class="num">1.0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">7</td></tr>
</tbody>
</table>
</div>"""

WEBB_ROCKIES_LINE = ('<div class="reftable">\n<table>\n<caption>Colorado Rockies at San '
                     'Francisco Giants, Saturday 15 August 2026, Oracle Park, '
                     '35,069</caption>\n' + LINEHEAD + '\n<tbody>\n'
                     + LINE('Colorado', [0, 0, 1, 0, 0, 0, 0, 0, 0], 1, 5, 0) + '\n'
                     + LINE('<b>San Francisco</b>', [0, 0, 1, 6, 0, 0, 0, 0, 'X'], 7, 10, 0)
                     + '\n</tbody>\n</table>\n</div>')

WEBB_ROCKIES_BOX = """<div class="reftable">
<table>
<caption>Pitching, Rockies at Giants, 15 August 2026</caption>
<thead><tr><th>Pitcher</th><th class="num">IP</th><th class="num">H</th><th class="num">R</th><th class="num">ER</th><th class="num">BB</th><th class="num">SO</th><th class="num">P</th></tr></thead>
<tbody>
<tr><td>Michael Lorenzen, COL (L)</td><td class="num">3.2</td><td class="num">4</td><td class="num">6</td><td class="num">6</td><td class="num">3</td><td class="num">1</td><td class="num">82</td></tr>
<tr><td>Parker Mushinski, COL</td><td class="num">0.1</td><td class="num">3</td><td class="num">1</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">15</td></tr>
<tr><td>Tanner Gordon, COL</td><td class="num">4.0</td><td class="num">3</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">4</td><td class="num">63</td></tr>
<tr><td><b>Logan Webb, SF (W)</b></td><td class="num">6.0</td><td class="num">4</td><td class="num">1</td><td class="num">1</td><td class="num">0</td><td class="num">7</td><td class="num">80</td></tr>
<tr><td>Carson Seymour, SF</td><td class="num">2.0</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">3</td><td class="num">24</td></tr>
<tr><td>Dylan Smith, SF</td><td class="num">1.0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">1</td><td class="num">10</td></tr>
</tbody>
</table>
</div>"""

ROCKIES_13_7_LINE = ('<div class="reftable">\n<table>\n<caption>Colorado Rockies at San '
                     'Francisco Giants, Sunday 16 August 2026, Oracle Park, '
                     '32,063</caption>\n' + LINEHEAD + '\n<tbody>\n'
                     + LINE('<b>Colorado</b>', [0, 4, 0, 0, 2, 4, 3, 0, 0], 13, 9, 1) + '\n'
                     + LINE('San Francisco', [1, 4, 1, 0, 1, 0, 0, 0, 0], 7, 11, 1)
                     + '\n</tbody>\n</table>\n</div>')

ROCKIES_13_7_BOX = """<div class="reftable">
<table>
<caption>Pitching, Rockies at Giants, 16 August 2026</caption>
<thead><tr><th>Pitcher</th><th class="num">IP</th><th class="num">H</th><th class="num">R</th><th class="num">ER</th><th class="num">BB</th><th class="num">SO</th></tr></thead>
<tbody>
<tr><td>Grant Hughes, COL</td><td class="num">4.0</td><td class="num">8</td><td class="num">7</td><td class="num">7</td><td class="num">1</td><td class="num">2</td></tr>
<tr><td>Nick Frasso, COL (W)</td><td class="num">1.0</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">1</td><td class="num">2</td></tr>
<tr><td>Parker Mushinski, COL</td><td class="num">1.0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">1</td><td class="num">0</td></tr>
<tr><td>Jimmy Herget, COL</td><td class="num">1.0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">1</td><td class="num">1</td></tr>
<tr><td>Zach Agnos, COL</td><td class="num">2.0</td><td class="num">2</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">2</td></tr>
<tr><td>Blade Tidwell, SF</td><td class="num">4.1</td><td class="num">3</td><td class="num">6</td><td class="num">6</td><td class="num">5</td><td class="num">1</td></tr>
<tr><td>Sam Hentges, SF (L)</td><td class="num">1.1</td><td class="num">1</td><td class="num">2</td><td class="num">2</td><td class="num">2</td><td class="num">1</td></tr>
<tr><td><b>Jonathan Brubaker, SF</b></td><td class="num">0.0</td><td class="num">0</td><td class="num">2</td><td class="num">2</td><td class="num">2</td><td class="num">0</td></tr>
<tr><td>Reiver Sanmartin, SF</td><td class="num">0.2</td><td class="num">2</td><td class="num">1</td><td class="num">1</td><td class="num">0</td><td class="num">0</td></tr>
<tr><td>Keaton Winn, SF</td><td class="num">0.2</td><td class="num">2</td><td class="num">2</td><td class="num">2</td><td class="num">1</td><td class="num">0</td></tr>
<tr><td>Tyler Harris, SF</td><td class="num">1.0</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">2</td></tr>
<tr><td>Jason Foley, SF</td><td class="num">1.0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">1</td></tr>
</tbody>
</table>
</div>"""

ASTROS_RUBBER_LINE = ('<div class="reftable">\n<table>\n<caption>Houston Astros at San '
                      'Francisco Giants, Wednesday 12 August 2026, Oracle Park, '
                      '28,101</caption>\n' + LINEHEAD + '\n<tbody>\n'
                      + LINE('Houston', [0, 0, 0, 0, 0, 0, 1, 1, 0], 2, 4, 0) + '\n'
                      + LINE('<b>San Francisco</b>', [1, 0, 0, 0, 0, 0, 0, 0, 0], 1, 5, 1)
                      + '\n</tbody>\n</table>\n</div>')

ASTROS_RUBBER_BOX = """<div class="reftable">
<table>
<caption>Pitching, Astros at Giants, 12 August 2026</caption>
<thead><tr><th>Pitcher</th><th class="num">IP</th><th class="num">H</th><th class="num">R</th><th class="num">ER</th><th class="num">BB</th><th class="num">SO</th><th class="num">P</th></tr></thead>
<tbody>
<tr><td>Bryan King, HOU</td><td class="num">0.2</td><td class="num">0</td><td class="num">1</td><td class="num">1</td><td class="num">2</td><td class="num">1</td><td class="num">19</td></tr>
<tr><td>Enyel De Los Santos, HOU</td><td class="num">0.1</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">1</td><td class="num">0</td><td class="num">9</td></tr>
<tr><td>Tatsuya Imai, HOU</td><td class="num">3.0</td><td class="num">3</td><td class="num">0</td><td class="num">0</td><td class="num">2</td><td class="num">3</td><td class="num">55</td></tr>
<tr><td>AJ Blubaugh, HOU</td><td class="num">1.2</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">2</td><td class="num">18</td></tr>
<tr><td>Steven Okert, HOU</td><td class="num">1.1</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">17</td></tr>
<tr><td>Bryan Abreu, HOU</td><td class="num">1.0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">2</td><td class="num">12</td></tr>
<tr><td>Josh Hader, HOU</td><td class="num">1.0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">8</td></tr>
<tr><td><b>Adrian Houser, SF</b></td><td class="num">6.0</td><td class="num">2</td><td class="num">0</td><td class="num">0</td><td class="num">1</td><td class="num">5</td><td class="num">73</td></tr>
<tr><td>Sam Hentges, SF</td><td class="num">0.1</td><td class="num">1</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">12</td></tr>
<tr><td>Keaton Winn, SF</td><td class="num">1.2</td><td class="num">1</td><td class="num">1</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">16</td></tr>
<tr><td>Reiver Sanmartin, SF</td><td class="num">1.0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">2</td><td class="num">15</td></tr>
</tbody>
</table>
</div>"""

GUARDIANS_8_1_LINE = ('<div class="reftable">\n<table>\n<caption>San Francisco Giants at '
                      'Cleveland Guardians, Tuesday 18 August 2026, Progressive Field, '
                      '21,309</caption>\n' + LINEHEAD + '\n<tbody>\n'
                      + LINE('San Francisco', [0, 1, 0, 0, 0, 0, 0, 0, 0], 1, 7, 2) + '\n'
                      + LINE('<b>Cleveland</b>', [3, 2, 0, 2, 0, 0, 1, 0, 'X'], 8, 12, 0)
                      + '\n</tbody>\n</table>\n</div>')

GUARDIANS_8_1_BOX = """<div class="reftable">
<table>
<caption>Pitching, Giants at Guardians, 18 August 2026</caption>
<thead><tr><th>Pitcher</th><th class="num">IP</th><th class="num">H</th><th class="num">R</th><th class="num">ER</th><th class="num">BB</th><th class="num">SO</th></tr></thead>
<tbody>
<tr><td><b>Carson Whisenhunt, SF (L)</b></td><td class="num">4.0</td><td class="num">9</td><td class="num">7</td><td class="num">6</td><td class="num">2</td><td class="num">1</td></tr>
<tr><td>Trent Harris, SF</td><td class="num">2.0</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">5</td></tr>
<tr><td>Reiver Sanmartin, SF</td><td class="num">2.0</td><td class="num">2</td><td class="num">1</td><td class="num">0</td><td class="num">1</td><td class="num">2</td></tr>
<tr><td>Foster Griffin, CLE (W)</td><td class="num">6.0</td><td class="num">5</td><td class="num">1</td><td class="num">1</td><td class="num">2</td><td class="num">6</td></tr>
<tr><td>Matt Festa, CLE</td><td class="num">1.1</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">3</td></tr>
<tr><td>Tim Herrin, CLE</td><td class="num">1.0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">2</td></tr>
<tr><td>Craig Yoho, CLE</td><td class="num">0.2</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">1</td></tr>
</tbody>
</table>
</div>"""

ARTICLES = [
# --------------------------------------------------------- 1. Where the rebuild stands
dict(slug='giants-2026-where-the-rebuild-actually-stands',
     section='Giants', tag='Giants', hub='Giants',
     title='Where the Giants Rebuild Actually Stands After the Selloff',
     h1="Where the Giants Rebuild Actually Stands After the Selloff, and What 2027 Has to Look Like",
     dek="Four veterans gone in a week, a rookie manager still learning, and a farm "
         "system that has to produce now. The state of the thing, kept updated.",
     desc="After the 2026 deadline selloff, what the Giants roster actually is, what came "
          "back, and what has to happen in 2027 for any of it to matter.",
     date='2026-08-08',
     card=('giants', 'The Rebuild', 'What is left after the selloff, and what 2027 needs'),
     body=[
      "This is the page that keeps the state of the rebuild straight, because the "
      "argument moves faster than the roster does. It gets updated as things change.",
      "<b>What happened.</b> The Giants got to the deadline nineteen games under .500 and "
      "Buster Posey finally did the thing this fan base had been demanding for two years: "
      "he sold. {arraez} went to Philadelphia. {ray} went to San Diego. {ramos} went to "
      "the Yankees and Tyler Mahle went to Atlanta. Four useful veterans out the door in "
      "roughly a week, which is not a teardown by modern standards but is the most honest "
      "thing this front office has done since he took the job.",
      "<b>What came back.</b> The headline return is {mayer}, which we called a robbery "
      "at the time and still looks like one. Beyond that it is arms and lottery tickets, "
      "the Mahle deal brought back a twenty-four-year-old who went straight to Sacramento. "
      "None of it is a franchise-altering haul. All of it is better than watching those "
      "contracts expire for nothing, which is what happened the last time.",
      "<b>What is actually left.</b> {eldridge} is the centre of everything now, and our "
      "long piece on him remains the best case for optimism on this roster. Behind him, {josuar} is the genuine star candidate at the bottom of the system. Rafael Devers "
      "has quietly had a season nobody discussed. {schmitt} forced his way into the lineup "
      "and stayed. Logan Webb is still Logan Webb. Beyond that it thins out fast, which is "
      "the whole point of the exercise.",
      "<b>The manager question.</b> Unresolved and getting louder. We did not like "
      "{vitello} when it was announced and nothing about the lineup decisions since has "
      "changed that, and on 8 August {roupp} in front of everybody without consequence. "
      "The honest counter-argument is that a rookie manager handed a "
      "selling roster is being judged on an impossible assignment. Both things can be "
      "true, and 2027 is when the excuse expires.",
      "<b>The bullpen.</b> Still the thing that decided more games than any other single "
      "factor, and still unaddressed in any structural way. A team cannot rebuild its way "
      "out of a bullpen problem in one offseason, but it can stop pretending the problem "
      "is bad luck.",
      "<b>What 2027 has to look like.</b> Three things, in order. Eldridge has to be a "
      "middle-of-the-order bat rather than a prospect. The rotation behind Webb has to "
      "produce two starters from inside the organisation rather than another winter of "
      "expensive one-year arms. And somebody has to decide, publicly, whether Vitello is "
      "the manager of the next good Giants team or the man who bridged to them.",
      "<b>The constraint everybody forgets.</b> Whatever this front office builds has to "
      "work in {park}, which suppresses home runs by roughly a fifth. A rebuild pointed at "
      "slug does not survive contact with that ballpark. The teams that won here were "
      "pitching, defence and contact, and the park has not changed just because the roster "
      "did.",
      "<b>What would make this a failure.</b> Spending the winter on veterans to get back "
      "to .500. That is the trap this franchise has fallen into repeatedly, buying just "
      "enough to be uninteresting, finishing fourth, and arriving at the next deadline "
      "with nothing to sell and nothing to promote. The selloff only means something if "
      "the next move is patience.",
      "The roster detail is on the {depth}, the season's games are in the {season}, and "
      "the rest is on the {hub}.",
     ],
     links={'arraez': ('giants-arraez-kilian-traded-phillies-august-3.html', 'Luis Arraez'),
            'josuar': ('josuar-gonzalez-giants-top-prospect-18-year-old-shortstop.html',
                       'Josuar Gonzalez'),
            'ray': ('giants-robbie-ray-padres-trade-report-august-3.html', 'Robbie Ray'),
            'ramos': ('giants-heliot-ramos-yankees-mayer-mahle-august-4.html', 'Heliot Ramos'),
            'mayer': ('giants-marcelo-mayer-trade-red-sox-erik-miller-robbery.html', 'Marcelo Mayer'),
            'eldridge': ('bryce-eldridge-giants-future-franchise-first-baseman-july-2026.html',
                         'Bryce Eldridge'),
            'schmitt': ('giants-casey-schmitt-all-star-breakout-season-2026.html', 'Casey Schmitt'),
            'vitello': ('tony-vitello-hire-giants-mistake.html', 'the Vitello hire'),
            'roupp': ('giants-landen-roupp-showed-up-tony-vitello-tigers-8-0-august-8.html',
                      'a pitcher waved him off his own mound'),
            'park': ('oracle-park-mccovey-cove-splash-hits-guide.html', 'Oracle Park'),
            'depth': ('giants-2026-roster-depth-chart.html', 'depth chart page'),
            'season': ('giants-2026-season-hub-results-coverage.html', 'season hub'),
            'hub': ('../giants.html', 'Giants hub')},
     related=[('giants-2026-roster-depth-chart.html', 'Giants', 'The Giants Roster and Depth Chart'),
              ('bryce-eldridge-giants-future-franchise-first-baseman-july-2026.html', 'Giants', 'Bryce Eldridge Is the Only Future This Team Has'),
              ('giants-season-over-build-around-eldridge-posey-bullpen.html', 'Giants', 'This Season Is Over. Build Around Eldridge.')]),

# --------------------------------------------------------- 2. Roster / depth chart
dict(slug='giants-2026-roster-depth-chart',
     section='Giants', tag='Giants', hub='Giants',
     title='The Giants Roster and Depth Chart After the Deadline',
     h1="The Giants Roster and Depth Chart After the Deadline, Position by Position",
     dek="Who is left, who is playing every day, and which positions are being held "
         "together by whoever was available. Updated as the roster moves.",
     desc="A position-by-position look at the Giants roster after the 2026 deadline: who "
          "is left, who plays every day, and where the depth genuinely ran out.",
     date='2026-08-08',
     card=('giants', 'Roster & Depth', 'Who is left after the deadline, position by position'),
     body=[
      "A depth chart on a selling team is a moving target. This one gets updated as the "
      "roster changes, and after this deadline it changed a lot.",
      "<b>Rotation.</b> Logan Webb at the top, and then a genuine question. {ray} is gone "
      "to San Diego and Tyler Mahle is gone to Atlanta, which removed two of the four "
      "arms that actually took the ball on schedule. Landen Roupp and Carson Whisenhunt "
      "have had the innings handed to them, with mixed and instructive results. Whisenhunt "
      "in particular has looked like a real thing on his good nights.",
      "<b>Bullpen.</b> The unit that has decided this season, mostly badly. Erik Miller "
      "has been the closest thing to reliable, Caleb Kilian went to Philadelphia in the "
      "Arraez deal, and the rest has been a rotating cast of arms asked to protect leads "
      "they were not equipped to protect. This is the single clearest offseason priority.",
      "<b>Infield.</b> {eldridge} at first is the future and increasingly the present. "
      "{schmitt} has played his way into an everyday job wherever they can find him one. "
      "Rafael Devers has been the most productive bat on the roster. {mayer} arrived from "
      "Boston as the return that actually mattered. Willy Adames anchors the middle.",
      "<b>Outfield.</b> Thinner than it was. {ramos} went to the Yankees, which took the "
      "most established bat out of the group and handed real playing time to Grant McCray "
      "and whoever else has earned a look. This is where a rebuilding team is supposed to "
      "find out things, and it is finding out things.",
      "<b>Catcher.</b> Patrick Bailey and the depth behind him, on a roster where the "
      "position has not been the problem.",
      "<b>Where the depth ran out.</b> Two places, and they are the same two every year. "
      "Starting pitching behind Webb, where the drop-off is immediate. And late-inning "
      "relief, where the drop-off is fatal. Everything else on this roster can survive an "
      "injury. Those two cannot.",
      "<b>What to watch as this updates.</b> Which of the young arms holds a rotation "
      "spot into 2027, whether Eldridge's role grows to match the hype, and whether "
      "{vitello} settles on a lineup for longer than a week at a time.",
      "<b>The Devers question nobody is asking.</b> He has been the most productive bat "
      "on this roster all season and it has gone almost entirely undiscussed, because a "
      "losing team makes individual excellence invisible. That is worth naming here, "
      "because it is also the argument for keeping him: a rebuild needs somebody in the "
      "middle of the order who is already good while the young players arrive.",
      "<b>How the young arms actually looked.</b> Whisenhunt has had nights that "
      "genuinely looked like a major-league starter and nights that looked like a "
      "prospect, which is exactly what a rebuilding team should be finding out in "
      "August. Roupp has been given the same runway. Neither has settled it. The point of "
      "a lost season is that those innings are free, the wins were never coming, so the "
      "information is the return.",
      "<b>What the depth chart does not show.</b> The Sacramento pipeline is now carrying "
      "more weight than it has in years, because four veterans left in a week and "
      "somebody has to play. Watch which names come up and stay up. That is the single "
      "most informative thing about the last two months of a season like this one.",
      "The state-of-the-rebuild read is in {rebuild}, the games are in the {season}, and "
      "everything else is on the {hub}.",
     ],
     links={'ray': ('giants-robbie-ray-padres-trade-report-august-3.html', 'Robbie Ray'),
            'eldridge': ('bryce-eldridge-giants-future-franchise-first-baseman-july-2026.html',
                         'Bryce Eldridge'),
            'schmitt': ('giants-casey-schmitt-all-star-breakout-season-2026.html', 'Casey Schmitt'),
            'mayer': ('giants-marcelo-mayer-trade-red-sox-erik-miller-robbery.html', 'Marcelo Mayer'),
            'ramos': ('giants-heliot-ramos-yankees-mayer-mahle-august-4.html', 'Heliot Ramos'),
            'vitello': ('giants-tony-vitello-clueless-lineups-eldridge-leadoff.html', 'Vitello'),
            'rebuild': ('giants-2026-where-the-rebuild-actually-stands.html', 'our rebuild page'),
            'season': ('giants-2026-season-hub-results-coverage.html', 'season hub'),
            'hub': ('../giants.html', 'Giants hub')},
     related=[('giants-2026-where-the-rebuild-actually-stands.html', 'Giants', 'Where the Giants Rebuild Actually Stands'),
              ('giants-2026-season-hub-results-coverage.html', 'Giants', 'The 2026 Giants Season, Game by Game'),
              ('bryce-eldridge-giants-future-franchise-first-baseman-july-2026.html', 'Giants', 'Bryce Eldridge Is the Only Future This Team Has')]),

# --------------------------------------------------------- 3. Season hub
dict(slug='giants-2026-season-hub-results-coverage',
     section='Giants', tag='Giants', hub='Giants',
     title='The 2026 Giants Season, Game by Game',
     h1="The 2026 Giants Season, Game by Game, With Every Column We Wrote About It",
     dek="A season that started with hope, collapsed in July and got sold off in August. "
         "The landing page for all of it, in order.",
     desc="The 2026 Giants season in order: the July collapse, the deadline selloff, and "
          "every recap and column we published along the way.",
     date='2026-08-08',
     card=('giants', 'The 2026 Season', 'Hope, collapse, selloff, in order'),
     body=[
      "This is the page to start from if you want the season as a story rather than as a "
      "pile of separate columns. It gets updated as games are played.",
      "<b>The shape of it.</b> The Giants spent the first half hanging around, arrived at "
      "the All-Star break at 41-55, and then got worse. By the deadline they were "
      "nineteen games under .500 and selling. That is the arc, and every individual game "
      "below is a variation on it.",
      "<b>July: the month it ended.</b> The bullpen defined it. {kilian} coughed up a "
      "two-out lead to the worst team in baseball, and that game turned out to be the "
      "template. There was a genuinely good stretch at the end of the month, "
      "{heating} covers the run where they beat the best team in baseball twice and hung "
      "sixteen on Milwaukee, but it was a mirage inside a losing season.",
      "<b>The All-Star break.</b> {firsthalf} is the accounting: 41-55, a lost first "
      "half, and a rookie manager learning on the job in public.",
      "<b>August: the selloff.</b> Three days in San Diego where they got swept, and then "
      "the deadline. {deadline} was the argument beforehand; {rebuild} is where things "
      "actually stand now. And then the eight-nothing loss to Detroit on 8 August, where "
      "{roupp} in front of a full ballpark, the clearest picture yet of where this "
      "clubhouse stands on its manager. The day after that, {webb} and lost anyway in ten "
      "innings, which is the other half of the same problem. Then on 11 August, {astros} "
      "for win number fifty, which is the first genuinely encouraging night since the "
      "deadline. On 15 August {webbrockies}, which is the clearest single argument on this "
      "page for why he is the one man on the roster nobody should be arguing about. Then "
      "on 16 August {rockies137}, a home series lost to the worst team in the league, and "
      "the two afternoons together are this whole season in miniature.",
      "<b>What is still worth watching.</b> Devers has been quietly excellent. "
      "{eldridge} is the reason to keep the television on. And there is the ordinary, "
      "stubborn pleasure of watching a bad team occasionally beat a good one, which is "
      "most of what baseball is.",
      "<b>The games that actually explain the season.</b> Four of them, in order. The "
      "{nohit}, where Dylan Cease nearly no-hit one of the worst Giants lineups anyone "
      "here can remember, and which set the tone in early July. The {kilianloss}, the "
      "template for every bullpen collapse that followed. The {padres} sweep in San "
      "Diego, three days that turned the deadline from a question into a decision. And "
      "the {rangers} shutout, eleven men left on base, nineteen games under, which was "
      "the moment even the optimists stopped.",
      "<b>The counter-programming.</b> It was not all misery, and pretending otherwise "
      "would be dishonest. {adames} opened the second half with a grand slam and a "
      "shutout in Seattle. There was a stretch at the end of July where this team beat "
      "the best club in baseball twice and put sixteen on Milwaukee. {devers} has been "
      "quietly excellent all year. A bad season still contains good baseball; it just "
      "does not add up to anything.",
      "<b>What a season like this is actually for.</b> Information. Which young arms can "
      "hold a rotation spot, whether Eldridge is what the scouting said, whether the "
      "manager can manage. Those answers are worth more in a lost year than four extra "
      "wins would have been, which is the one genuinely consoling thing about August.",
      "<b>How this page works.</b> Recaps go up after games, columns go up when something "
      "deserves an argument, and both get linked here so the season reads in sequence. "
      "The roster is on the {depth}, and everything else is on the {hub}.",
     ],
     links={'kilian': ('giants-bullpen-meltdown-kilian-rockies-4-3-vitello-posey-july-10.html',
                       'Caleb Kilian'),
            'nohit': ('giants-no-hit-cease-webb-grand-slam-july-8.html', 'Cease near-no-hitter'),
            'kilianloss': ('giants-bullpen-meltdown-kilian-rockies-4-3-vitello-posey-july-10.html',
                           'Rockies bullpen meltdown'),
            'padres': ('giants-padres-5-4-swept-roupp-devers-august-2.html', 'Padres'),
            'rangers': ('giants-rangers-6-0-shutout-whisenhunt-19-under-august-5.html', 'Rangers'),
            'adames': ('giants-adames-grand-slam-mariners-7-0-second-half-july-17.html', 'Willy Adames'),
            'devers': ('giants-tigers-5-2-devers-24th-homer-adames-august-7.html', 'Rafael Devers'),
            'heating': ('giants-heating-up-best-baseball-of-the-season-july-30.html',
                        'our column on the hot streak'),
            'firsthalf': ('giants-first-half-breakdown-vitello-second-half-all-star-break-2026.html',
                          'The first-half breakdown'),
            'deadline': ('giants-trade-deadline-monday-posey-sell-ramos-arraez-ray.html',
                         'The deadline column'),
            'roupp': ('giants-landen-roupp-showed-up-tony-vitello-tigers-8-0-august-8.html',
                      'Landen Roupp waved Tony Vitello off the mound'),
            'webb': ('giants-tigers-3-1-10th-webb-eight-innings-wasted-august-9.html',
                     'Logan Webb threw eight innings without an earned run'),
            'astros': ('giants-astros-4-1-whisenhunt-eldridge-homer-hunter-brown-august-11.html',
                       'Carson Whisenhunt outpitched Hunter Brown in a four-one win'),
            'webbrockies': ('giants-rockies-7-1-logan-webb-consummate-pro-august-15.html',
                            'Logan Webb went six innings without a walk and beat Colorado '
                            'seven to one'),
            'rockies137': ('giants-rockies-13-7-devers-25th-bullpen-destroyed-august-16.html',
                           'the bullpen gave away a thirteen to seven loss'),
            'rebuild': ('giants-2026-where-the-rebuild-actually-stands.html',
                        'the state of the rebuild'),
            'eldridge': ('bryce-eldridge-giants-future-franchise-first-baseman-july-2026.html',
                         'Bryce Eldridge'),
            'depth': ('giants-2026-roster-depth-chart.html', 'depth chart page'),
            'hub': ('../giants.html', 'Giants hub')},
     related=[('giants-2026-where-the-rebuild-actually-stands.html', 'Giants', 'Where the Giants Rebuild Actually Stands'),
              ('giants-2026-roster-depth-chart.html', 'Giants', 'The Giants Roster and Depth Chart'),
              ('giants-first-half-breakdown-vitello-second-half-all-star-break-2026.html', 'Giants', 'Giants at the Break: 41-55')]),

# --------------------------------------------------------- 4. Oracle Park evergreen
dict(slug='oracle-park-mccovey-cove-splash-hits-guide',
     section='Giants', tag='Giants History', hub='Giants',
     title='Oracle Park and McCovey Cove: How the Ballpark Actually Plays',
     h1="Oracle Park and McCovey Cove: Why the Ballpark Plays the Way It Does",
     dek="A short right field on the water, a cavernous right-centre, a wind that eats "
         "fly balls, and a body of water named after a man who never got to hit into it.",
     desc="How Oracle Park actually plays: the dimensions, the wind, McCovey Cove, splash "
          "hits, and why it suppresses home runs more than almost any park in baseball.",
     date='2026-08-08',
     card=('giants', 'Oracle Park', 'The Cove, the wind, and why the park plays that way'),
     body=[
      "Every ballpark has a personality and most of them are marketing. Oracle Park's is "
      "real, measurable, and it has shaped how the Giants have been built for a quarter "
      "of a century.",
      "<b>The dimensions.</b> The park opened in 2000. Left field is 339 feet, centre is "
      "391, and right field is 309, which sounds like a bandbox until you understand "
      "what sits behind that right-field wall and how quickly the fence runs away from "
      "the plate into right-centre. The short porch is a target for maybe a dozen swings "
      "a season. Everything else that goes that way dies in the gap.",
      "<b>The wind.</b> The genuine equaliser, and the reason batted-ball data at this "
      "park does not travel. Evening games get a cold, heavy marine air that takes real "
      "distance off a fly ball. Hitters who arrive here from warmer parks spend a season "
      "learning that the ball they crushed in July would have been out somewhere else.",
      "<b>What the numbers say.</b> Recent park factors put runs at 94 and home runs at "
      "78, against a league average of 100. Runs are suppressed slightly. Home runs are "
      "suppressed enormously, roughly a fifth fewer than a neutral park. Oracle Park is "
      "not a mild pitcher's park. It is one of the hardest places in baseball to hit a "
      "ball out.",
      "<b>McCovey Cove.</b> The water beyond right field is named for Willie McCovey, and "
      "the name came from sportswriters rather than a marketing department, the thought "
      "being that McCovey, who spent his career fighting the wind at Candlestick, would "
      "have put dozens of balls in there had he played on the water instead.",
      "<b>Splash hits.</b> A home run that clears the right-field wall and reaches the "
      "water on the fly. The first belonged to {bonds}, off a Mets left-hander on 1 May "
      "2000, which is about as fitting as sporting history gets. And here is the detail "
      "that tells you everything about the geometry: no right-handed hitter has ever put "
      "one in the Cove the opposite way. Not one, in a quarter of a century.",
      "<b>Why it matters to how the team is built.</b> A park that eats home runs "
      "rewards contact, speed, defence and pitching, and punishes a roster built on "
      "slug. That is not a coincidence in the {dynasty}, those teams were pitching and "
      "defence and timely hitting, which is exactly what this park pays for. Every time "
      "the Giants have tried to build a lineup of sluggers, the park has quietly taken a "
      "percentage.",
      "<b>The other thing it is.</b> The most beautiful place to watch baseball in the "
      "country, and it has not had enough October nights to match. {waiting} is our "
      "column about that particular grievance. The current state of the roster is in "
      "{rebuild}, and the rest is on the {hub}.",
     ],
     links={'bonds': ('barry-bonds-giants-home-run-king.html', 'Barry Bonds'),
            'dynasty': ('giants-dynasty-even-year-magic.html', 'even-year dynasty'),
            'waiting': ('giants-oracle-park-still-waiting.html', 'Oracle Park Is Still Waiting'),
            'rebuild': ('giants-2026-where-the-rebuild-actually-stands.html', 'our rebuild page'),
            'hub': ('../giants.html', 'Giants hub')},
     related=[('giants-oracle-park-still-waiting.html', 'Giants', 'The Giants Keep Promising October'),
              ('barry-bonds-giants-home-run-king.html', 'Giants History', 'Barry Bonds: The Loudest Bat San Francisco Ever Saw'),
              ('giants-dynasty-even-year-magic.html', 'Giants History', 'Even-Year Magic: The Giants Dynasty')]),

# ------------------------------------------- 5. Roupp shows up Vitello, Sat 8 August 2026
dict(slug='giants-landen-roupp-showed-up-tony-vitello-tigers-8-0-august-8',
     section='Giants', tag='Giants', hub='Giants',
     title='Roupp Showed Up Vitello, and That Is the Whole Season',
     h1="Landen Roupp Showed Up Tony Vitello on the Mound, and That One Moment Explains "
        "This Entire Giants Season",
     dek="A pitcher with a 4.22 ERA glared at his manager, shook his head and waved him "
         "back toward the dugout in front of everybody. Nobody in that ballpark was "
         "surprised, and that is the problem.",
     desc="Landen Roupp glared at Tony Vitello and waved him off in the Giants' 8-0 loss "
          "to Detroit. It says everything about a manager this clubhouse has stopped "
          "playing for.",
     date='2026-08-09',
     card=('giants', 'Nobody Respects Him', 'Roupp waved off his own manager, and the season made sense'),
     body=[
      "Eight to nothing. At home. To Detroit. On a Saturday afternoon at the most "
      "beautiful ballpark in America, in front of people who paid actual money, and the "
      "only thing anybody is going to remember from it is a pitcher with a 4.22 ERA "
      "standing on the mound telling his manager to go away.",
      "If you missed it: Landen Roupp walks three men in a row in the sixth. Three. In a "
      "row. Tony Vitello comes out to get him, which is not a controversial decision, it "
      "is the only decision, and Roupp gives him a look. Shakes his head. Starts scraping "
      "the dirt off his cleats like a man being asked to leave a bar. Then puts his hands "
      "up at his chest and waves his own manager back toward the dugout. Stay there. I "
      "have got it.",
      "He did not have it. He had walked three straight guys.",
      "And here is where this fan base is supposed to get mad at the pitcher, and honestly "
      "I am not. I would rather have a guy who hates coming out of the game than another "
      "polite arm handing over the ball with a shrug. \"As a competitor I kinda wanna try "
      "to clean up my own mess,\" is what Roupp said afterward, and fine, good, be a "
      "competitor. Logan Webb has been a competitor here for years and has somehow "
      "managed it without ever waving a manager off in public, but fine.",
      "The part that actually matters is what happened next, which is nothing. Vitello "
      "got to a microphone and said Roupp is the \"exact kind of guy you want to coach.\" "
      "That is it. That is the response. Your pitcher publicly told you to stay in the "
      "dugout in front of a sellout crowd and a television camera and your answer is a "
      "compliment.",
      "You want to know why nobody on this team plays like it matters? That is why. There "
      "is no cost to anything. There is no line. Bruce Bochy would have handled that in "
      "about four seconds and none of us would have ever heard about it, because the "
      "players knew exactly where the line was and none of them wanted to find out what "
      "was on the other side of it. This man does not have a line. He has a personality "
      "and a smile and a set of quotes, and a roster that has clearly worked out that the "
      "quotes are all there is.",
      "That is the thing that got exposed on Saturday, and it is bigger than one pitcher "
      "having a moment. Players do not do that to a manager they are playing for. They do "
      "it to a manager they have already stopped hearing. You can talk yourself into a "
      "rookie manager learning on the job right up until the day one of your own guys "
      "waves you off the mound and the rest of the dugout does not so much as move.",
      "And it is not as if he has earned the benefit of the doubt with the actual job. The "
      "lineups have been indefensible all year. He hit {leadoff}, which is a thing a man "
      "does when he has confused being unpredictable with being smart. He {benched} in a "
      "one-run game against Texas and then had to use him off the bench anyway to tie it, "
      "which is the single most Vitello sequence of the season, wrong on the decision, "
      "bailed out by the kid, still lost the game. Every week it is a new batting order, "
      "new positions, guys hitting in spots that make no sense for the roster or the "
      "ballpark, and no visible idea underneath any of it.",
      "Add the ejections. Add {bullpen}, which he has burned through all season with no "
      "apparent plan for who pitches when. Add a clubhouse that just watched a "
      "twenty-something starter show him up on national television and pay absolutely no "
      "price for it. That is not a rebuild problem. That is not Buster Posey's fault, and "
      "believe me, there is plenty on that list that is. That is a manager problem.",
      "We said this was a mistake when it {hire}. We said it again when the lineups "
      "started arriving. It has been a bad year for being right about this team and this "
      "is one more.",
      "So here is where it lands. This season is gone, it has been gone since July, the "
      "veterans are on other teams and the only reason left to watch is to find out which "
      "young players are real, and we cannot even get a clean answer to that, because "
      "they are being used by a man who changes his mind every night. {rebuild} spells out "
      "what 2027 has to look like. Step one is not a free agent. Step one is deciding "
      "whether the person filling out the lineup card is somebody this roster will "
      "actually run through a wall for, because Saturday was the answer to that question "
      "and the answer was no.",
      "Eight to nothing, and the story was the manager getting waved off his own mound. "
      "The rest of the year is in the {season}, and everything else we have written about "
      "this mess is on the {hub}.",
     ],
     links={'leadoff': ('giants-tony-vitello-clueless-lineups-eldridge-leadoff.html',
                        'Bryce Eldridge leadoff'),
            'benched': ('giants-rangers-5-4-walkoff-eldridge-bench-vitello-august-4.html',
                        'sat Eldridge'),
            'bullpen': ('giants-bullpen-meltdown-kilian-rockies-4-3-vitello-posey-july-10.html',
                        'the bullpen'),
            'hire': ('tony-vitello-hire-giants-mistake.html', 'was announced'),
            'rebuild': ('giants-2026-where-the-rebuild-actually-stands.html',
                        'Our rebuild page'),
            'season': ('giants-2026-season-hub-results-coverage.html', 'season hub'),
            'hub': ('../giants.html', 'Giants hub')},
     related=[('giants-tony-vitello-clueless-lineups-eldridge-leadoff.html', 'Giants',
               'Tony Vitello Has No Idea What He Is Doing With This Lineup'),
              ('tony-vitello-hire-giants-mistake.html', 'Giants', 'The Vitello Hire Was a Mistake'),
              ('giants-2026-where-the-rebuild-actually-stands.html', 'Giants',
               'Where the Giants Rebuild Actually Stands')]),

# --------------------------------------- 6. Tigers 3-1 in ten, Sun 9 August 2026
dict(slug='giants-tigers-3-1-10th-webb-eight-innings-wasted-august-9',
     section='Giants', tag='Giants', hub='Giants',
     title='Tigers 3, Giants 1 (F/10): We Wasted Eight Innings of Logan Webb',
     h1="Tigers 3, Giants 1 in Ten Innings: Logan Webb Gave Us Eight Innings of Nothing "
        "and This Team Could Not Find Him Two Runs",
     dek="Eight innings. Four hits. No earned runs. One walk. And the Giants lost it in "
         "the tenth anyway, because of course they did.",
     desc="Logan Webb threw eight innings and allowed no earned runs, and the Giants still "
          "lost 3-1 in ten to Detroit. Seven hits, seven left on, twenty games under.",
     date='2026-08-10',
     card=('giants', 'Wasted', 'Webb went eight and got one run of support'),
     body=[
      "Eight innings. Four hits. One walk. Not a single earned run. Logan Webb went out "
      "there on a Sunday at Oracle Park and gave this organisation the best afternoon any "
      "pitcher has given it in weeks, and the San Francisco Giants handed him one run and "
      "then lost the game in extra innings. Three to one. Series lost. Twenty games under "
      "five hundred.",
      "I want to be clear about what I watched, because the box score does not do it "
      "justice. Webb had nothing to work with and knew it. Detroit's kid Troy Melton was "
      "throwing a 1.46 ERA at our lineup and our lineup was doing exactly what it has done "
      "all summer, which is take strike one and jog back to the dugout. Six scoreless "
      "innings from Melton. Four hits off him. And Webb just kept matching it, inning "
      "after inning, with a defence behind him that let the only run of his afternoon score "
      "on a ground ball double play in the sixth. Unearned. Of course it was unearned. He "
      "was not even allowed to lose it honestly.",
      "Then the seventh, and for about twenty minutes this felt like a baseball game. "
      "Basabe gets on, Drew Gilbert hits an infield single, an <i>infield single</i>, "
      "which is the most 2026 Giants way imaginable to score a run, and it is one-all. "
      "That is our offence. Seven hits, one run, seven men left on base, and the run we "
      "did score never left the dirt.",
      "And Webb keeps going. Seventh, fine. Eighth, fine. He finishes the eighth having "
      "given up four hits all day and this team still has not scored him a second run. "
      "Somebody tell me what he is supposed to do. Pitch the tenth as well? Hit? Because "
      "at this point that is the only thing left he has not been asked to do for this "
      "franchise.",
      "Then the tenth, and you knew. Every single person in that ballpark knew. Sam "
      "Hentges comes in, gets one out, and Detroit puts a pinch-hitter up who lines a "
      "single to right to score Greene, and then a fielder's choice makes it three-one and "
      "we are all just sitting there watching Kenley Jansen and Tyler Holton strike out the "
      "side to close it. Six outs, six strikeouts between them, and our half of the tenth "
      "was over before the beer line moved.",
      "Thirty-two thousand people paid to be there. Two hours and forty-six minutes. And "
      "the takeaway is that Logan Webb, one of the best twenty pitchers in this sport, is "
      "burning the prime of his career on a team that cannot score him two runs on a "
      "Sunday afternoon in August.",
      "That is the part that actually makes me angry, and it is not really about this "
      "game. Webb has been here through all of it. He was here for the ninety-eight-win "
      "team that never got to do anything about it. He was here for every winter where "
      "this front office told us they were in on somebody and then were not. He was here "
      "for the {deadline}, and he is still here now, throwing eight-inning shutout ball for "
      "a forty-nine and sixty-nine ballclub with a rookie manager and a lineup full of "
      "auditions. Ask yourself honestly how many more of these he has in him before "
      "somebody in that building has to have a very uncomfortable conversation about "
      "whether this is fair to him.",
      "And yes, {vitello} is involved here, because he is involved in everything now. I am "
      "not going to pretend that a different manager scores four runs off Troy Melton. He "
      "does not. But this is the third game in about a week where the story is that the "
      "Giants got a good start and could not put a rally together, and the man writing the "
      "lineup card has spent the entire season telling us that the batting order is the one "
      "thing he has real opinions about. On Saturday he got {roupp}. On Sunday he got eight "
      "shutout innings from his ace and turned it into a loss. Both of those are his week.",
      "The small consolations, because there were two. Rafael Devers had two more hits and "
      "is still, quietly, the most productive bat on this roster, which we {devers} last "
      "week and nobody outside this fan base has noticed. And Gilbert had two of the seven "
      "hits, which for a kid getting his run in a lost August is worth writing down.",
      "But that is what this is now. Two hits from a kid we are evaluating and an ace "
      "getting wasted. Detroit takes the series two to one and goes home. We are forty-nine "
      "and sixty-nine, twenty under, and there are still seven weeks of this left.",
      "Eight innings, no earned runs, and a loss. Put that on the tombstone of the 2026 "
      "season. The rest of the year is in the {season}, where the roster actually stands is "
      "in {rebuild}, and everything else is on the {hub}.",
     ],
     links={'deadline': ('giants-trade-deadline-monday-posey-sell-ramos-arraez-ray.html',
                         'selloff at the deadline'),
            'vitello': ('giants-tony-vitello-clueless-lineups-eldridge-leadoff.html',
                        'Tony Vitello'),
            'roupp': ('giants-landen-roupp-showed-up-tony-vitello-tigers-8-0-august-8.html',
                      'waved off his own mound in an eight-nothing loss'),
            'devers': ('giants-tigers-5-2-devers-24th-homer-adames-august-7.html',
                       'wrote about'),
            'rebuild': ('giants-2026-where-the-rebuild-actually-stands.html',
                        'the rebuild page'),
            'season': ('giants-2026-season-hub-results-coverage.html', 'season hub'),
            'hub': ('../giants.html', 'Giants hub')},
     related=[('giants-landen-roupp-showed-up-tony-vitello-tigers-8-0-august-8.html', 'Giants',
               'Roupp Showed Up Vitello, and That Is the Whole Season'),
              ('giants-2026-season-hub-results-coverage.html', 'Giants',
               'The 2026 Giants Season, Game by Game'),
              ('giants-2026-where-the-rebuild-actually-stands.html', 'Giants',
               'Where the Giants Rebuild Actually Stands')]),

# ------------------------------------- 7. Giants 4-1 over Houston, Tue 11 August 2026
dict(slug='giants-astros-4-1-whisenhunt-eldridge-homer-hunter-brown-august-11',
     section='Giants', tag='Giants', hub='Giants',
     title='Giants 4, Astros 1: Carson Whisenhunt Was Worth the Wait',
     h1="Giants 4, Astros 1: Carson Whisenhunt Outpitched Hunter Brown, Bryce Eldridge Hit "
        "Number Twelve, and For One Night This Looked Like a Baseball Team",
     dek="Five and two-thirds of one-run ball from the kid, four unanswered runs off a "
         "Houston ace, and the fiftieth win of a season nobody enjoyed getting to.",
     desc="Carson Whisenhunt outpitched Hunter Brown in a 4-1 win at Oracle Park. Eldridge "
          "homered, Cavanaugh and Koss drove in runs, and the Giants got to fifty wins.",
     date='2026-08-12',
     card=('giants', 'Whisenhunt', 'The kid beat Hunter Brown and the Giants got to fifty'),
     body=[
      "I have spent most of this summer writing about what is wrong with the San Francisco "
      "Giants, so let me be a fair witness for one night. On Tuesday at Oracle Park they took "
      "a first-place team, handed the ball to a twenty-five-year-old left-hander carrying a "
      "six-run ERA, and beat Houston four to one. Four unanswered runs. Nine hits. No errors. "
      "A bullpen that got ten outs and did not let a single runner past first base. Start to "
      "finish it was the cleanest nine innings this team has played in a month.",

      '<figure style="margin:0 0 30px;text-align:center">'
      '<picture><source type="image/webp" srcset="../assets/img/players/oracle-park-real-400w.webp 400w, '
      '../assets/img/players/oracle-park-real-800w.webp 800w, ../assets/img/players/oracle-park-real.webp 1200w" '
      'sizes="(max-width: 820px) 92vw, 760px">'
      '<img src="../assets/img/players/oracle-park-real.jpg" '
      'alt="Oracle Park in San Francisco, where the Giants beat the Astros 4-1 on 11 August 2026" '
      'style="display:block;width:100%;max-width:760px;height:auto;margin:0 auto;object-fit:cover;'
      'background:var(--surface);border-radius:12px;border:1px solid var(--line)" width="1200" height="675" '
      'decoding="async" fetchpriority="high" '
      'srcset="../assets/img/players/oracle-park-real-400w.jpg 400w, '
      '../assets/img/players/oracle-park-real-800w.jpg 800w, '
      '../assets/img/players/oracle-park-real.jpg 1200w" sizes="(max-width: 820px) 92vw, 760px"></picture>'
      '<figcaption style="color:var(--muted);font-size:14px;margin-top:10px;font-style:italic">'
      'Thirty thousand and ninety-three on a sixty-two degree Tuesday night, wind blowing out to '
      'centre field. They saw the best start of Carson Whisenhunt&rsquo;s career.</figcaption></figure>',

      GIANTS_ASTROS_LINE,

      "<b>The start.</b> Carson Whisenhunt went five and two-thirds, gave up four hits and one "
      "run, walked three, struck out two and threw ninety-six pitches. On paper that is an "
      "ordinary Tuesday. In the context of his season it is the best night he has had in the "
      "major leagues. Go back through the six starts. He threw seven shutout innings at San "
      "Diego on the last day of July and looked like a rotation piece, then {shutout} five days "
      "later and looked like a Triple-A arm getting found out. Nineteen earned runs in "
      "twenty-eight innings. Eighteen walks. A 6.11 ERA that is not lying about anything.",

      "What was different on Tuesday is that he pitched backwards when he had to. The three "
      "walks were not fun and the sixth got away from him a little, but he never handed Houston "
      "the one big swing, and this is a Houston lineup with Yordan Alvarez hitting .322 and "
      "Isaac Paredes and Christian Walker behind him. The Astros went nought for four with "
      "runners in scoring position and left nine men on. Their entire evening was an Alvarez "
      "sacrifice fly in the second inning. That is the whole Houston night.",

      "<b>How we scored, which is the part I did not see coming.</b> Rafael Devers walked twice, "
      "because that is what Devers does now, and came around in the second on a Drew Gilbert "
      "line single to left. One-all. In the fourth, Drew Cavanaugh, the rookie catcher, "
      "twenty-eight games in, hitting .242, singled Gilbert home and then stole the first "
      "base of his major league life. In the fifth, Bryce Eldridge got a pitch from Hunter Brown "
      "and hit it to dead centre for number twelve. In the sixth, Christian Koss, who walked in "
      "hitting .167, ripped a double into left to score Cavanaugh and then jogged into third "
      "when Jeremy Pe&ntilde;a threw the ball away for the second time in the game. Four to one, "
      "and it never felt close after that.",

      "Read that list of names again. Gilbert, Cavanaugh, Eldridge, Koss. Not one of them was on "
      "this roster two years ago and two of them were not on it in April. That is supposed to be "
      "the entire point of a season like 2026, and Tuesday is the first night in weeks where it "
      "looked like a point instead of an excuse. {eldridge} is a twelve-homer, .775-OPS first "
      "baseman at an age when most players are still riding buses in Double-A, and he did that "
      "to one of the ten best starters in the American League.",

      "<b>Hunter Brown, for what it is worth.</b> Five innings, five hits, three earned, three "
      "walks, eighty-nine pitches to get fifteen outs. He came in at 3.68 and he was not sharp, "
      "but the Giants also made him work, which they have not done to good pitching since about "
      "the middle of July. Willy Adames had two hits including his twenty-fifth double and a "
      "stolen base. Osleivis Basabe had two more. Nine hits out of a lineup that has been "
      "getting six.",

      "The one thing that has not changed is the thing that has cost this club about eleven "
      "wins: two for thirteen with runners in scoring position and eight men left on base. In a "
      "different game that is a loss and we have all watched roughly thirty of those. Victor "
      "Bericoto struck out three times and grounded into a double play. Jung Hoo Lee went nought "
      "for four and stranded four. There is still a lot of bad baseball buried inside a "
      "four-one win.",

      "<b>The bullpen, and I do not say this often.</b> Carson Seymour got seven outs and struck "
      "out two. Reiver Sanmartin got the last one of the eighth. JT Brubaker threw seven pitches "
      "in the ninth for the save. Ten outs, nobody past first base, and not one arm had to warm "
      "up twice. After the summer this bullpen has had, after the eighth innings in San "
      "Diego, after {webb}, that deserves to be written down somewhere.",

      GIANTS_ASTROS_BOX,

      "So they are fifty and seventy. Win number fifty took a hundred and twenty games and it is "
      "not going to be a headline anywhere outside this page, which is precisely why it is on "
      "this page. Houston took Monday six-three. We took Tuesday. Wednesday is the rubber game "
      "against a first-place team we have no business splitting with, let alone beating, and if "
      "{vitello} manages to take that one he is going to get a paragraph out of me that is not a "
      "complaint. I am prepared to write it. I have the paragraph ready.",

      "One last thing about Whisenhunt, because I think it matters more than the final score "
      "does. This organisation spent two months trading away everything that was not bolted to "
      "the floor and then asked a fan base to be patient with whatever was left. Patience is a "
      "great deal easier when the kid you were told to be patient about goes out on a Tuesday in "
      "August and outpitches Hunter Brown. That is the whole ask. Do that eight or nine more "
      "times between now and the end of September and the winter gets a lot less miserable "
      "around here.",

      "Every result and what is left of the schedule is in the {season}, where this roster "
      "honestly stands is in {rebuild}, and the rest of it lives on the {hub}.",
     ],
     links={'shutout': ('giants-rangers-6-0-shutout-whisenhunt-19-under-august-5.html',
                        'Texas knocked him around in a six-nothing shutout loss'),
            'eldridge': ('bryce-eldridge-giants-future-franchise-first-baseman-july-2026.html',
                         'Bryce Eldridge'),
            'vitello': ('giants-tony-vitello-clueless-lineups-eldridge-leadoff.html',
                        'Tony Vitello'),
            'webb': ('giants-tigers-3-1-10th-webb-eight-innings-wasted-august-9.html',
                     'after the tenth inning against Detroit on Sunday'),
            'rebuild': ('giants-2026-where-the-rebuild-actually-stands.html',
                        'the rebuild page'),
            'season': ('giants-2026-season-hub-results-coverage.html', 'season hub'),
            'hub': ('../giants.html', 'Giants hub')},
     related=[('giants-tigers-3-1-10th-webb-eight-innings-wasted-august-9.html', 'Giants',
               'Tigers 3, Giants 1: Eight Innings of Webb, Wasted'),
              ('giants-2026-season-hub-results-coverage.html', 'Giants',
               'The 2026 Giants Season, Game by Game'),
              ('giants-2026-where-the-rebuild-actually-stands.html', 'Giants',
               'Where the Giants Rebuild Actually Stands')]),

# --------------------------------------------------------- recap: 12 August, rubber game
dict(slug='giants-astros-2-1-adames-back-spasms-bericoto-error-houser-august-12',
     section='Giants', tag='Giants', hub='Giants',
     title='Astros 2, Giants 1: Six Shutout Innings, One Drop, One Bad Back',
     h1="Astros 2, Giants 1: Adrian Houser Threw Six Shutout Innings, a Rookie Dropped a "
        "Fly Ball, and Willy Adames Walked Off Holding His Back",
     dek="One run in the first inning and nothing for eight after it, a three-base error "
         "in the seventh that tied it, and our shortstop arguing with his manager about "
         "coming out of a game nobody will remember.",
     desc="Astros 2, Giants 1 at Oracle Park: Adrian Houser's six shutout innings wasted, "
          "a Bericoto error tied it, and Willy Adames left with back spasms.",
     date='2026-08-12',
     card=('giants', 'Adames', 'Houser was perfect, the defence was not, and the back went'),
     body=[
      "{whisenhunt}, and I sat down and wrote something nice about this team, an "
      "actual, unforced compliment, in August, in a fifty-win season. Twenty-four hours "
      "later the San Francisco Giants went out on Wednesday afternoon and lost the rubber "
      "game to Houston two to one in the most 2026 way available to them. One run. Five hits. A dropped fly "
      "ball. And Willy Adames walking off the field in the eighth inning with his hand on "
      "his lower back, arguing with the manager the whole way. I should have known better. "
      "Every time I say something kind about this club it charges me interest the next day.",

      '<figure style="margin:0 0 30px;text-align:center">'
      '<picture><source type="image/webp" srcset="../assets/img/players/oracle-park-real-400w.webp 400w, '
      '../assets/img/players/oracle-park-real-800w.webp 800w, ../assets/img/players/oracle-park-real.webp 1200w" '
      'sizes="(max-width: 820px) 92vw, 760px">'
      '<img src="../assets/img/players/oracle-park-real.jpg" '
      'alt="Oracle Park in San Francisco, where the Giants lost 2-1 to the Astros on 12 August 2026" '
      'style="display:block;width:100%;max-width:760px;height:auto;margin:0 auto;object-fit:cover;'
      'background:var(--surface);border-radius:12px;border:1px solid var(--line)" width="1200" height="675" '
      'decoding="async" fetchpriority="high" '
      'srcset="../assets/img/players/oracle-park-real-400w.jpg 400w, '
      '../assets/img/players/oracle-park-real-800w.jpg 800w, '
      '../assets/img/players/oracle-park-real.jpg 1200w" sizes="(max-width: 820px) 92vw, 760px"></picture>'
      '<figcaption style="color:var(--muted);font-size:14px;margin-top:10px;font-style:italic">'
      'Twenty-eight thousand, one hundred and one people came to a Wednesday afternoon '
      'rubber game and got exactly one Giants run for the trouble.</figcaption></figure>',

      ASTROS_RUBBER_LINE,

      "<b>Start with the part that should have been the story.</b> Adrian Houser had not "
      "started a major league game since June. On Wednesday he went six innings, gave up two "
      "hits, walked one, struck out five and did the whole thing on seventy-three pitches. "
      "Seventy-three. Fifty of them strikes. Against a first-place lineup with Yordan Alvarez "
      "in it. He was in and out of the dugout so fast the grounds crew barely had time to "
      "rake. That is a professional pitcher taking a bad team's afternoon and making it look "
      "organised, and if this club had scored him two runs it would have been the easiest win "
      "of the month.",

      "They scored him one, in the first inning, before most of the ballpark had sat down. "
      "Adames singled the rally into being and came around on a Victor Bericoto single to "
      "left. One-nothing. That was the offence. That was all of it. Houston then ran seven "
      "pitchers at us, a bullpen game, on the road, in a rubber match, and we "
      "put up eight consecutive zeroes against a parade of arms that included a guy in his "
      "first big-league season and a middle-innings bulk man nobody outside Houston can pick "
      "out of a line-up. Tatsuya Imai came in and threw three shutout innings on fifty-five "
      "pitches. Steven Okert, Bryan Abreu and Josh Hader closed it out by retiring nine of "
      "the last ten. Five hits total. Two of them by Christian Koss, who is hitting .186.",

      "<b>Now the seventh, because that is where it actually went.</b> Houser's day was done "
      "at seventy-three pitches, which I have opinions about, and Sam Hentges came in and "
      "gave up a single to Alvarez. Fine. Isaac Paredes grounded to short and Adames flipped "
      "it to second for the out, and that is the flip, right there, that is the moment "
      "his back went. Then Daulton Varsho hit a fly ball to left field. A routine fly ball to "
      "left field. Bericoto dropped it. Not a dive, not the sun, not the wind off McCovey "
      "Cove. He dropped it, and by the time it was over Paredes was standing on third and "
      "Varsho was on second on a single error. Nelson Vel&aacute;zquez pinch-hit a sacrifice "
      "fly to centre and the game was tied. Houser's line stays clean, which is the cruellest "
      "part of the box score: six shutout innings and the game got taken from him by a "
      "twenty-three-year-old who could not squeeze a can of corn.",

      "I am not going to bury the kid. Bericoto is a rookie left fielder who is hitting .273 "
      "with a .500 slugging percentage and who drove in the only run we scored. He is exactly "
      "the sort of player this whole miserable summer is supposed to be about. But this is "
      "the thing nobody wants to say out loud about a rebuild: you spend the year watching "
      "young players learn how to play the outfield in the major leagues, at Oracle Park, in "
      "front of paying customers, and some afternoons the tuition bill arrives in the seventh "
      "inning of a one-run game.",

      "<b>The eighth was almost worse because nobody made a mistake.</b> Keaton Winn threw a "
      "pitch to Taylor Trammell, Trammell tripled to right, Nick Allen hit a sacrifice fly to "
      "left, two to one, done. Three pitches, one run, no defensive alibi. Then Abreu struck "
      "out the side's worth of our hitters in the bottom half and Hader needed eight pitches "
      "in the ninth. Andrew Knizner fouled out, Koss flied out, Jung Hoo Lee grounded out to "
      "second to end it. Lee, by the way, went nought for five and saw twenty-three pitches "
      "doing it.",

      ASTROS_RUBBER_BOX,

      "<b>And then Adames.</b> He came out after the seventh, Koss slid over to short, Buddy "
      "Kennedy went to third, and the man who signed the biggest free-agent contract in the "
      "history of this franchise spent the rest of the afternoon in the clubhouse with back "
      "spasms. Tony Vitello said afterwards that he had to fight him tooth and nail to get "
      "him out of the game. Read that again. It is 12 August, the Giants are twenty-one games "
      "under .500, and Willy Adames is arguing with his manager about staying in a game that "
      "means nothing to anybody, with a back that has been bothering him on and off since "
      "June. He is hitting .224. He has been hitting .224 all summer while people around here "
      "have been unkind about him. He also singled, walked, scored our only run and refused "
      "to come out. I have watched players on better Giants teams give less of a damn than "
      "that.",

      "The word is that it is not an injured-list situation and that he will sit Friday night "
      "against Colorado. I hope that is true, and I hope somebody in that building has the "
      "sense to give him more than one day, because there is precisely nothing left to play "
      "for and a shortstop with a chronic back is a problem you take into 2027 if you are "
      "stupid about it in August. Sit him a week. Nobody is catching anybody.",

      "So the series goes to Houston, two games to one. Fifty and seventy-one. That is the "
      "record, and the schedule says there are still forty-one of these to sit through. The "
      "one genuinely useful thing to come out of Wednesday is Houser, and the plan, as I "
      "understand it, is to leave him in the rotation the rest of the way and find out "
      "whether he is worth a contract for next year. Good. That is the correct use of "
      "September for a team in this position, and it is the same argument I have been making "
      "on {rebuild} for a month: every remaining start belongs to somebody you are trying to "
      "learn something about.",

      "What I cannot make peace with is the shape of it. Six shutout innings from a "
      "thirty-three-year-old on a one-year look, a rookie drops a fly ball, the shortstop "
      "hurts himself making a routine flip, and a team that scored four the night before "
      "manages one. There is no villain in this one. {vitello} did not lose it, he ran "
      "his starter six clean innings and got the ball to the right arms. Nobody sulked. They "
      "just are not good enough, and the honest, tiring truth about a season like this one is "
      "that most of the losses look exactly like Wednesday: quiet, forgettable, over by four "
      "o'clock, and one small piece of somebody's body a little more broken than it was at "
      "noon.",

      "Colorado comes in on Friday and we get to do it again. Every result is in the "
      "{season}, where this roster actually stands is in {rebuild}, and the rest of it lives "
      "on the {hub}.",
     ],
     links={'whisenhunt': ('giants-astros-4-1-whisenhunt-eldridge-homer-hunter-brown-august-11.html',
                           'Carson Whisenhunt beat Hunter Brown on Tuesday night'),
            'vitello': ('giants-tony-vitello-clueless-lineups-eldridge-leadoff.html',
                        'Tony Vitello'),
            'rebuild': ('giants-2026-where-the-rebuild-actually-stands.html',
                        'the rebuild page'),
            'season': ('giants-2026-season-hub-results-coverage.html', 'season hub'),
            'hub': ('../giants.html', 'Giants hub')},
     related=[('giants-astros-4-1-whisenhunt-eldridge-homer-hunter-brown-august-11.html', 'Giants',
               'Giants 4, Astros 1: Carson Whisenhunt Was Worth the Wait'),
              ('giants-2026-season-hub-results-coverage.html', 'Giants',
               'The 2026 Giants Season, Game by Game'),
              ('giants-2026-where-the-rebuild-actually-stands.html', 'Giants',
               'Where the Giants Rebuild Actually Stands')]),

# --------------------------------------------------------- recap: 15 August, Webb beats Colorado
dict(slug='giants-rockies-7-1-logan-webb-consummate-pro-august-15',
     section='Giants', tag='Giants', hub='Giants',
     title='Giants 7, Rockies 1: Logan Webb Is the Consummate Pro',
     h1="Giants 7, Rockies 1: Logan Webb Does Not Care That This Season Is Over, and That "
        "Is Exactly Why He Is the Best Thing We Have",
     dek="Six innings, four hits, no walks, seven strikeouts, eighty pitches. A six-run "
         "fourth behind him. The one man in that clubhouse who has never once mailed in "
         "an August.",
     desc="Giants 7, Rockies 1 at Oracle Park: Logan Webb went six innings with no walks "
          "and seven strikeouts, Drew Gilbert drove in three, and a six-run fourth ended it.",
     date='2026-08-15',
     card=('giants', 'Logan Webb', 'Six innings, no walks, seven strikeouts, eighty pitches'),
     body=[
      "Friday night Kyle Freeland walked into Oracle Park and beat us five to two. Kyle "
      "Freeland, of the forty-nine-win Colorado Rockies. I went to bed "
      "genuinely wondering whether there was a floor left to hit. Saturday afternoon Logan "
      "Webb took the ball and the whole thing looked like baseball again for two hours and "
      "twenty-six minutes. Seven to one. Six innings, four hits, one run, no walks, seven "
      "strikeouts, eighty pitches. That is the entire column, honestly, and everything "
      "after this paragraph is me trying to explain why a routine August start by a "
      "twenty-nine-year-old on a seventy-two-loss team made me angrier and happier at the "
      "same time than anything else this month.",

      '<figure style="margin:0 0 30px;text-align:center">'
      '<picture><source type="image/webp" srcset="../assets/img/players/logan-webb-giants-blue-jays-400w.webp 400w, '
      '../assets/img/players/logan-webb-giants-blue-jays-800w.webp 800w, '
      '../assets/img/players/logan-webb-giants-blue-jays-1200w.webp 1200w, '
      '../assets/img/players/logan-webb-giants-blue-jays.webp 1280w" sizes="(max-width: 820px) 92vw, 760px">'
      '<img src="../assets/img/players/logan-webb-giants-blue-jays.jpg" '
      'alt="Logan Webb of the San Francisco Giants, who beat the Rockies 7-1 at Oracle Park on 15 August 2026" '
      'style="display:block;width:100%;max-width:760px;height:auto;margin:0 auto;object-fit:contain;'
      'background:var(--surface);border-radius:12px;border:1px solid var(--line)" width="1200" height="675" '
      'decoding="async" fetchpriority="high" '
      'srcset="../assets/img/players/logan-webb-giants-blue-jays-400w.jpg 400w, '
      '../assets/img/players/logan-webb-giants-blue-jays-800w.jpg 800w, '
      '../assets/img/players/logan-webb-giants-blue-jays-1200w.jpg 1200w, '
      '../assets/img/players/logan-webb-giants-blue-jays.jpg 1280w" sizes="(max-width: 820px) 92vw, 760px"></picture>'
      '<figcaption style="color:var(--muted);font-size:14px;margin-top:10px;font-style:italic">'
      'Thirty-five thousand and sixty-nine people on a cloudy Saturday afternoon, and Logan '
      'Webb gave every one of them a professional baseball game.</figcaption></figure>',

      WEBB_ROCKIES_LINE,

      "<b>Start with the walks, because that is the tell.</b> Zero. Twenty-two men came to "
      "the plate against him and not one of them got a free base. Fifty-seven of his eighty "
      "pitches were strikes. He got four ground-ball outs and five in the air and he was "
      "back in the dugout before the beer line moved. The only run he gave up was in the "
      "third, when Ezequiel Tovar singled, went to third, and came home on a Cole Carrigg "
      "ground ball to left. That is it. That is the damage. Against a lineup that has lost "
      "seventy-four games he did not get cute, did not nibble, did not throw an extra "
      "twenty pitches proving something to nobody in the middle of August.",

      "And that is the whole point of him. Look at what this team has put in front of Logan "
      "Webb this year and then look at what he has done anyway: eight and seven with a 3.50 "
      "earned run average, a hundred and thirty-nine innings, a hundred and ten strikeouts "
      "against thirty-two walks, a 1.06 WHIP. Eight wins. Eight. On a club that has scored "
      "him nothing for four months. Go back further: thirty-three starts in 2023, thirty-three "
      "in 2024, thirty-four in 2025, two hundred and sixteen innings, two hundred and four, "
      "two hundred and seven. A hundred and ninety-nine starts and twelve hundred innings "
      "into a career spent entirely in this uniform, and he has never once been the guy who "
      "found a reason not to take the ball.",

      "<b>Then the fourth inning, which was the funniest thing I have seen at Oracle Park in "
      "a month.</b> Michael Lorenzen had already given up a Drew Gilbert home run in the "
      "third, number six, into the right-field seats, tying it at one, and in "
      "the fourth the whole thing came apart on him. Turner Hill sacrifice fly, Jung Hoo Lee "
      "in. Gilbert singled to centre and both Drew Cavanaugh and Buddy Kennedy scored. "
      "Rafael Devers hit his twenty-ninth double, a ground-rule job down the left-field "
      "line, and Christian Koss scored. Bryce Eldridge lined a single to centre and Devers "
      "scored. Six runs. Lorenzen never got out of the inning, three and two thirds, "
      "six earned, eighty-two pitches, and he hit Kennedy for good measure. Parker Mushinski "
      "came in and let both inherited runners score, because of course he did.",

      "Drew Gilbert finished three for four with a walk, a home run, three runs batted in "
      "and two runs scored, and if you want one small honest reason to keep watching this "
      "team in September, he is a decent candidate. Jung Hoo Lee was two for three with a "
      "walk. Ten hits, no errors, seven runs. Ten hits out of a lineup that has been "
      "scratching for five all summer. It can be done. It just apparently requires Colorado.",

      WEBB_ROCKIES_BOX,

      "<b>The bullpen, briefly, because they were fine.</b> Carson Seymour went two "
      "innings, one hit, three strikeouts, twenty-four pitches. Dylan Smith threw a "
      "one-two-three ninth on ten pitches. Three innings, no runs, nobody warming up twice. "
      "After the summer these arms have had, a clean handoff in a six-run game still counts "
      "as news around here.",

      "Now the part that actually eats at me. Logan Webb is twenty-nine years old. He has "
      "given this franchise every healthy start of his professional life and what he has to "
      "show for it is one October cameo and a decade of front offices explaining that the "
      "window is opening soon. He was an All-Star selection this year and {allstar}. He "
      "threw eight innings against Detroit on 9 August and {webbtigers}. The man is running "
      "out of prime and this organisation keeps handing him seasons like this one to be "
      "excellent inside of. That is not his failure. It is entirely {rebuild} of the people "
      "who built the roster around him.",

      "So: fifty-one and seventy-two, the series with Colorado is level at one apiece, and "
      "we needed our best pitcher on the mound to split two games with a team that has lost "
      "seventy-four. Nobody is putting a banner up for that. But I have watched this club "
      "for long enough to know what it looks like when a professional shows up on a nothing "
      "Saturday in a nothing season, and Webb did the exact things he does in April of a "
      "year that matters: pounded the zone, worked fast, no walks, gave the ball to the "
      "manager with the game already won. There is no version of the next good Giants team "
      "that does not start with him, and there is no version of this season I will remember "
      "fondly except the days he pitched.",

      "Every result is in the {season}, where this roster actually stands is in the "
      "{rebuildpage}, and the rest of it lives on the {hub}.",
     ],
     links={'allstar': ('giants-athletics-all-star-game-2026-arraez-langeliers-webb.html',
                        'never even got into the game'),
            'webbtigers': ('giants-tigers-3-1-10th-webb-eight-innings-wasted-august-9.html',
                           'this lineup could not find him two runs'),
            'rebuild': ('giants-2026-where-the-rebuild-actually-stands.html', 'the failure'),
            'rebuildpage': ('giants-2026-where-the-rebuild-actually-stands.html',
                            'rebuild page'),
            'season': ('giants-2026-season-hub-results-coverage.html', 'season hub'),
            'hub': ('../giants.html', 'Giants hub')},
     related=[('giants-tigers-3-1-10th-webb-eight-innings-wasted-august-9.html', 'Giants',
               'Tigers 3, Giants 1: Eight Innings of Webb, Wasted'),
              ('giants-2026-season-hub-results-coverage.html', 'Giants',
               'The 2026 Giants Season, Game by Game'),
              ('giants-2026-where-the-rebuild-actually-stands.html', 'Giants',
               'Where the Giants Rebuild Actually Stands')]),

# ------------------------------ Rockies 13, Giants 7, Sunday 16 August 2026, Oracle Park
dict(slug='giants-rockies-13-7-devers-25th-bullpen-destroyed-august-16',
     section='Giants', tag='Giants', hub='Giants',
     title='Rockies 13, Giants 7: Devers Hit His 25th and It Did Not Matter',
     h1="Rockies 13, Giants 7: Rafael Devers Hit His Twenty-Fifth, We Led in the Sixth, "
        "and the Pitching Staff Set Fire to the Whole Afternoon",
     dek="A seven to six lead going to the sixth. Then seven unanswered to the worst team "
         "in the National League, in our building, on a Sunday, in front of thirty two "
         "thousand people who paid to watch it.",
     desc="Rockies 13, Giants 7 at Oracle Park: Rafael Devers homered for his 25th, the "
          "Giants led into the sixth, and the bullpen gave up seven unanswered to Colorado.",
     date='2026-08-16',
     card=('giants', 'Rockies 13, Giants 7', 'Devers hit his 25th and the bullpen burned it'),
     body=[
      "I want to be clear about what happened here, because the final score does not do it "
      "justice. We led this game. In the fifth inning we were winning it seven to six "
      "against the Colorado Rockies, who came into today with fifty wins, who are the "
      "worst team in the National League, who we had just beaten by six runs less than "
      "twenty four hours earlier. Rafael Devers had already hit his twenty fifth home run "
      "of the season. Eleven hits. A four run inning. And then the sixth inning started "
      "and this pitching staff handed the game over the way you hand a stranger your "
      "wallet.",
      "Seven unanswered runs. Thirteen to seven. At home. On a Sunday. In front of thirty "
      "two thousand and sixty three people who could have done anything else with their "
      "afternoon.",

      ROCKIES_13_7_LINE,

      "<b>Start with Devers, because it is the only thing worth being happy about.</b> "
      "Second inning, two on, and he put one into the right field seats. Three hundred and "
      "eighty feet. Number twenty five. Kennedy and Gilbert came in ahead of him and just "
      "like that we were up five to four after being down four to one. That is a real "
      "season he is having in a park that eats left handed power for breakfast, and the "
      "{oracle} explains exactly how hard that is to do here. He deserves better than the "
      "three hours that followed.",
      "<b>Blade Tidwell walked five men in four and a third innings.</b> Five. I do not "
      "need a pitcher to be good in August on a seventy three loss team. I genuinely do "
      "not. I need him to throw the ball over the plate against a lineup that has lost "
      "seventy four games. Six earned runs, three hits allowed, five walks. You have to "
      "work at it to give up six runs on three hits. That takes commitment.",
      "<b>And then the bullpen, which I am going to describe slowly.</b> Sam Hentges came "
      "in and gave up two. Fine. Then Jonathan Brubaker came in and did not record a "
      "single out. Not one. Zero innings pitched, two walks, two runs. He threw a wild "
      "pitch that scored Veen to tie it, and then he hit Carrigg with a pitch, with the "
      "bases loaded, to give Colorado the lead. That is how we lost the lead in this "
      "baseball game. A wild pitch and a hit batsman. Nobody hit anything. We just gave it "
      "to them.",
      "Then Reiver Sanmartin gave up another, and Moniak singled to left and two more "
      "scored because somebody kicked the ball around behind him, and Keaton Winn gave up "
      "two more, and by the time Brendan Sullivan hit a three run homer in the seventh the "
      "afternoon had stopped being a baseball game and become a public event. Four "
      "relievers. Two and two thirds innings. Seven earned runs.",

      ROCKIES_13_7_BOX,

      "<b>Here is the part that actually stings.</b> Their bullpen threw five shutout "
      "innings. Colorado's starter gave up seven runs in four innings and their relief "
      "corps, a group of men most of you could not pick out of a police lineup, came in "
      "and shut us out the rest of the way. Frasso, Mushinski, Herget, Agnos. Five "
      "innings, three hits, nothing. The worst team in the league has a bullpen that can "
      "hold a lead and we do not. Sit with that one.",
      "<b>The series.</b> Freeland beat us Friday. {webbrockies} on Saturday, which was "
      "the one afternoon this weekend that felt like a professional baseball operation. "
      "And then this. We lost a home series to Colorado. In August. There are fewer than "
      "forty games left and we are fifty one and seventy three, which puts us exactly one "
      "game ahead of the team that just came into our park and did that to us.",
      "<b>What I am not going to do is blame Vitello for this one.</b> I have spent most "
      "of this summer doing exactly that, and {vitello} is still the argument I would have "
      "on any other day. But you cannot manage your way out of a reliever who cannot find "
      "the plate. He put four arms in the game and every one of them made it worse. At "
      "some point the roster is the problem, and the roster is what {rebuild} has been "
      "about since the deadline.",
      "<b>What it means, if it means anything.</b> Devers is going to finish with thirty "
      "or more home runs in this ballpark and almost nobody outside this city will notice. "
      "Eldridge keeps hitting. Gilbert keeps hitting. There are pieces here. And every "
      "third day something like this happens and reminds you that pieces are not a team, "
      "and that the single most expensive thing to fix in baseball is a bullpen, and that "
      "this front office has not seriously tried to fix it in three years.",
      "The rest of the season is in the {season}, the roster is on the {depth}, and the "
      "rest is on the {hub}. I need a minute.",
     ],
     links={'oracle': ('oracle-park-mccovey-cove-splash-hits-guide.html',
                       'Oracle Park page'),
            'webbrockies': ('giants-rockies-7-1-logan-webb-consummate-pro-august-15.html',
                            'Logan Webb gave us seven to one'),
            'vitello': ('giants-tony-vitello-clueless-lineups-eldridge-leadoff.html',
                        'the Vitello case'),
            'rebuild': ('giants-2026-where-the-rebuild-actually-stands.html',
                        'the state of the rebuild'),
            'season': ('giants-2026-season-hub-results-coverage.html', 'season hub'),
            'depth': ('giants-2026-roster-depth-chart.html', 'depth chart page'),
            'hub': ('../giants.html', 'Giants hub')},
     related=[('giants-rockies-7-1-logan-webb-consummate-pro-august-15.html', 'Giants',
               'Giants 7, Rockies 1: Logan Webb Is the Consummate Pro'),
              ('giants-2026-season-hub-results-coverage.html', 'Giants',
               'The 2026 Giants Season, Game by Game'),
              ('giants-2026-where-the-rebuild-actually-stands.html', 'Giants',
               'Where the Giants Rebuild Actually Stands')]),
# ------------------------------------------- Josuar Gonzalez, the 18-year-old shortstop
dict(slug='josuar-gonzalez-giants-top-prospect-18-year-old-shortstop',
     section='Giants', tag='Giants', hub='Giants',
     title='Josuar Gonzalez Is the Best Giants Prospect in a Generation',
     h1="Josuar Gonzalez Is Eighteen Years Old, He Is Hitting .339 in Low-A, and He Is "
        "the Best Thing This Franchise Has Signed in a Generation",
     dek="A switch-hitting shortstop out of San Cristobal who walks more than he strikes "
         "out, runs like a scalded cat, and has already been ranked seventh in all of "
         "baseball. Finally, something to be excited about.",
     desc="Josuar Gonzalez is 18, a switch-hitting shortstop ranked as high as seventh in "
          "baseball, and he is hitting .339 at Low-A San Jose. Why Giants fans should care.",
     date='2026-08-18',
     card=('giants', 'Josuar Gonzalez', 'Eighteen years old and already the best thing we have'),
     body=[
      "I have watched this organisation sign, draft, promote and ruin position players for "
      "my entire adult life. I have been told about Angel Villalona. I have been told "
      "about Gary Brown. I sat through the Joey Bart years and the Marco Luciano years, "
      "and every March where somebody in Scottsdale said the words high ceiling into a "
      "microphone about a kid who never hit a big league slider. So understand that I do "
      "not say this lightly, and that I have earned the right to be a cynic about it: "
      "Josuar Gonzalez is the best prospect this franchise has had since Buster Posey, he "
      "is eighteen years old, and he is doing it right now, an hour down the road in San "
      "Jose, while the big club loses home series to Colorado.",

      "<b>Start with who he is.</b> Gonzalez is a switch-hitting shortstop from San "
      "Cristobal in the Dominican Republic. He turns nineteen in October. He is listed at "
      "a shade under six feet and something like a hundred and seventy pounds, which is to "
      "say he is a teenager who has not finished being built yet. The Giants signed him in "
      "January of 2025 for two million nine hundred and ninety seven thousand five hundred "
      "dollars, the second largest international bonus this franchise has ever handed "
      "anybody, and he was not a flier. He was the consensus best position player "
      "available on the entire international market that year, the number one prospect out "
      "of Latin America, and the number two name in the class behind only Roki Sasaki, who "
      "was already a finished major league pitcher. The comparisons scouts reached for at "
      "the time were a young Jose Reyes and Francisco Lindor. Nobody has reached for those "
      "names about anybody else we have signed in twenty years.",

      "<b>Then he went out and hit.</b> At seventeen, in the Dominican Summer League, he "
      "put up a .288 average with a .404 on base percentage and a .455 slug across fifty "
      "two games, with four home runs and thirty three stolen bases. He walked in 16.2 "
      "percent of his plate appearances and struck out in 15.8 percent. Read those last "
      "two numbers again. A seventeen year old kid, in his first professional summer, "
      "against men, drew more walks than he took strikeouts. That is not a tools report. "
      "That is a baseball player.",

      "<b>This year has been a demolition.</b> He opened 2026 in the Arizona Complex "
      "League and hit .343 with a .451 on base and a .515 slug over thirty games, two home "
      "runs, eight stolen bases, a 16.4 percent walk rate. On the twenty fourth of July "
      "the Giants moved him and Luis Hernandez, who is seventeen, up to Low-A San Jose "
      "together, which is the sort of aggressive assignment an organisation only makes "
      "when the reports coming back have started to get embarrassing. He responded by "
      "hitting .339 with a .455 on base and a .613 slugging percentage across his first "
      "sixteen games in a full season league: two homers, three steals, a .274 isolated "
      "power, a 16.9 percent walk rate against an 18.2 percent strikeout rate, and a 162 "
      "wRC+. Put the whole season together across both stops and it is .342 with a .452 on "
      "base and a .553 slug, four home runs, eleven stolen bases and a 148 wRC+, at an age "
      "where his American equivalents are picking a college.",

      "<b>The walk rate is the tell, and it is the reason I believe this one.</b> Toolsy "
      "teenagers hit .340 in complex leagues all the time. Those leagues are full of arms "
      "who cannot find the strike zone, so a kid with fast hands and no discipline can put "
      "up a beautiful line and then get eaten alive the first time a twenty three year old "
      "throws him a slider on 1-2. That is the Luciano story, roughly, and it is the story "
      "of a dozen other names that have been shoved at this fan base. Gonzalez is the "
      "opposite profile. He has walked in better than sixteen percent of his plate "
      "appearances at every single stop, at every level, in every league, against every "
      "age group he has faced, including the jump to full season ball at eighteen. Plate "
      "discipline travels. It is the most portable skill in the minor leagues and it is "
      "the exact thing this organisation has spent fifteen years failing to develop in "
      "anybody.",

      "<b>The tools underneath it are not small either.</b> The people who put numbers on "
      "this stuff have him at plus plus speed and plus plus defence at shortstop with an "
      "above average arm, which means he is a real everyday shortstop and not a second "
      "baseman in waiting. He has been measured at over 109 miles an hour off the bat, a "
      "genuine major league number, out of a body that has not filled out yet. He is more "
      "polished from the left side than the right. The power is projection rather than "
      "production at the moment, which is exactly what you would expect and exactly what "
      "the grades say. The bet is that he grows into twenty to twenty five home runs while "
      "keeping the discipline and the shortstop glove. If he does that he is a perennial "
      "All-Star. If he only gets halfway there he is still the starting shortstop on a "
      "good team, which this franchise has not developed for itself since the Obama "
      "administration.",

      "<b>The national lists have noticed, and fast.</b> In May one of them put him "
      "seventh in all of baseball, with the note that he could easily be the number one "
      "prospect in the sport by January. The ranking that moves slowest had him thirtieth "
      "in the winter and eighteenth in its August update. The other big list has him "
      "somewhere in the middle teens. That range, seventh to eighteenth, is the whole "
      "argument in one line: everybody agrees he is a top twenty prospect in baseball, and "
      "the evaluators who have watched him most closely this summer are the ones with him "
      "highest. Eighteen year olds who climb these lists in August are not a normal "
      "occurrence.",

      "<b>Now the cold water, because I am not going to do to you what this club's "
      "marketing department does to you every February.</b> He is eighteen. He has played "
      "sixteen games above the complex level. A hamstring has already cost him time this "
      "season, and the gap between San Jose and a major league batter's box is four "
      "levels, three winters and roughly a thousand things that go wrong for teenagers. "
      "The realistic arrival is 2029, and the honest sentence is that most eighteen year "
      "old shortstops ranked inside the top twenty never become stars. That is simply what "
      "the base rate says. The reason to be excited is not that he is a certainty. It is "
      "that for once we are holding the lottery ticket everybody else wants, instead of "
      "the one we talked ourselves into.",

      "<b>He is also not alone, which is the genuinely new part.</b> This organisation now "
      "has five players inside the top hundred prospects in the sport, and three of them "
      "are shortstops who are not yet twenty. Hernandez is seventeen and hitting alongside "
      "him at San Jose. Jhonny Level is in there too. Jackson Flora is an arm and Bo "
      "Davidson is a bat. That is a real farm system for the first time since the last "
      "decade, and it exists because somebody finally decided to spend properly in Latin "
      "America instead of treating the international market as a rounding error. Whatever "
      "else you want to say about this front office, and {rebuild} says most of it, they "
      "got that part right.",

      "<b>So where does he actually play?</b> Willy Adames is the shortstop here and he is "
      "signed for years yet, so the tidy answer is that this sorts itself out later and "
      "the honest answer is that you do not block a potential franchise shortstop with a "
      "contract, you move somebody. Adames can play third. Marcelo Mayer, who came back in "
      "the deadline robbery, is another middle infielder in the same queue. Having too "
      "many good young shortstops is a problem this franchise has literally never had and "
      "I am not going to spend August of 2026 worrying about it.",

      "<b>What it means for right now, which is the part that hurts.</b> The 2026 Giants "
      "are fifty one and seventy three and just handed a home series to the worst team in "
      "the National League. The manager question is unresolved, the bullpen is a running "
      "joke, and {devers} was the only thing worth watching on Sunday afternoon. "
      "{eldridge} is the bat that arrives first and carries the middle of the order. But "
      "the difference between a rebuild and a rebrand is whether there is a genuine star "
      "at the end of it, and for the first time since Posey came up out of Fresno there is "
      "a real candidate, and he is a teenager who plays the hardest position on the field "
      "and walks more than he strikes out.",

      "Write the name down. Josuar Gonzalez. In three years, when this team is worth "
      "watching in September again, you are going to want to be able to say you knew in "
      "August of 2026, in a nothing week, in a nothing season, while we were losing to "
      "Colorado.",

      "Where the rest of the rebuild stands is on the {rebuildpage}, the roster as it "
      "exists today is on the {depth}, every game is in the {season}, and the rest lives "
      "on the {hub}.",
     ],
     links={'rebuild': ('giants-2026-where-the-rebuild-actually-stands.html',
                        'the rebuild page'),
            'devers': ('giants-rockies-13-7-devers-25th-bullpen-destroyed-august-16.html',
                       'Rafael Devers hitting his twenty fifth'),
            'eldridge': ('bryce-eldridge-giants-future-franchise-first-baseman-july-2026.html',
                         'Bryce Eldridge'),
            'rebuildpage': ('giants-2026-where-the-rebuild-actually-stands.html',
                            'rebuild page'),
            'depth': ('giants-2026-roster-depth-chart.html', 'depth chart page'),
            'season': ('giants-2026-season-hub-results-coverage.html', 'season hub'),
            'hub': ('../giants.html', 'Giants hub')},
     related=[('bryce-eldridge-giants-future-franchise-first-baseman-july-2026.html', 'Giants',
               'Bryce Eldridge Is the Only Future This Team Has'),
              ('giants-2026-where-the-rebuild-actually-stands.html', 'Giants',
               'Where the Giants Rebuild Actually Stands'),
              ('giants-2026-roster-depth-chart.html', 'Giants',
               'The Giants Roster and Depth Chart')]),

# ------------------------------------------ Guardians 8, Giants 1, Tue 18 August 2026
dict(slug='giants-guardians-8-1-bryce-eldridge-14th-homer-august-18',
     section='Giants', tag='Giants', hub='Giants',
     title='Guardians 8, Giants 1: Eldridge Homered, Nothing Else Happened',
     h1="Guardians 8, Giants 1: Bryce Eldridge Hit His Fourteenth in Cleveland and That "
        "Was the Entire San Francisco Giants Offense",
     dek="One run. One. A twenty one year old put a baseball four hundred and five feet "
         "into the night in the second inning and the other eight men in that lineup gave "
         "us nothing for the remaining seven and a half.",
     desc="Guardians 8, Giants 1 in Cleveland: Bryce Eldridge homered for his 14th, Jo "
          "Adell drove in six, and one run was the entire Giants offense. They are 51-74.",
     date='2026-08-18',
     card=('giants', 'One Run in Cleveland', 'Eldridge hit number fourteen and nobody else did anything'),
     body=[
      "One run. That is what we scored on Tuesday night in Cleveland. One. Bryce Eldridge "
      "hit a baseball four hundred and five feet to dead centre field in the second inning, "
      "and if you got up during the fourth to make a sandwich you missed every single thing "
      "the San Francisco Giants offence did in three hours of professional baseball. Eight "
      "to one. Seven hits. Two errors. And a game that was effectively finished eleven "
      "pitches into the bottom of the first.",

      "I am so tired of typing sentences like that one.",

      GUARDIANS_8_1_LINE,

      "<b>Start with the kid, because the kid is the only reason any of us watched past the "
      "fourth.</b> Second inning, nobody on, and Eldridge got a pitch out over the plate and "
      "hit it a hundred and four miles an hour to the middle of the ballpark. Four hundred "
      "and five feet. Number fourteen. He is twenty one years old. He has played eighty two "
      "big league games, he is hitting .250 with a .343 on base and a .445 slug, and he has "
      "walked forty two times, which is a thing most twenty one year olds in this league "
      "cannot do because they are too busy swinging at sliders in the other batter&rsquo;s "
      "box. Two for four on the night. He looks like a hitter. He looks like the only hitter.",

      "That is not a compliment to this roster. That is an indictment of it. A rookie first "
      "baseman is carrying the only watchable at bats on a team with a hundred and twenty "
      "five games in the books, and {eldridge} has been the argument on this site since "
      "July. He is going to be a problem for the rest of the league in about eighteen "
      "months. Right now he is a problem for us, because every night he does something and "
      "nobody around him does anything at all.",

      "<b>Now Carson Whisenhunt, and I want to be fair to him for exactly one sentence "
      "before I am not.</b> He is a young starter on a bad team in a lost August. Fine. Nine "
      "hits in four innings. Seven runs. Twenty seven outs are available in a baseball game "
      "and he recorded twelve of them while the Cleveland Guardians, who are not the 1927 "
      "Yankees, hit line drive after line drive after line drive.",

      "It was over in the first. Kwan and Ram&iacute;rez get on, and Jo Adell hits a three "
      "run home run, his nineteenth, into the left field seats before anybody in that "
      "ballpark had finished sitting down. Second inning, Kwan and Ram&iacute;rez get on "
      "again, and Adell singles them both in. Fourth inning, Adell singles again, Drew "
      "Gilbert kicks the ball around out in left, and everybody moves up a base for free. "
      "Then a ground out brings in another one.",

      "<b>Jo Adell drove in six runs by himself. The San Francisco Giants drove in one.</b> "
      "One man in a Cleveland uniform had six times the offensive night that our entire "
      "roster managed. Sit with that for a second, because I have been sitting with it since "
      "the fourth inning and it has not gotten any better.",

      GUARDIANS_8_1_BOX,

      "<b>Foster Griffin.</b> Look him up. A journeyman left hander went six innings against "
      "us and gave up one run, and the one run was a solo homer from a twenty one year old "
      "rookie. Five hits, two walks, six strikeouts. Then Cleveland ran three relievers out "
      "there for the last three innings and we did nothing against them either. One hit. "
      "Nine innings, seven hits, one run, against a pitching staff nobody outside Ohio could "
      "name.",

      "<b>The rest of the lineup, in the order I got angry at them.</b> Rafael Devers went "
      "nought for four with three strikeouts. Victor Bericoto, nought for four. Andrew "
      "Knizner is hitting .000. Buddy Kennedy is hitting .111. Christian Koss is at .202. "
      "That is not a slump, that is a roster. And then the two errors, because of course "
      "there were two errors, because this team has spent all summer finding new ways to "
      "give the other side extra outs and extra bases and extra innings.",

      "<b>Here is the part that makes me want to put a brick through something.</b> Trent "
      "Harris and Reiver Sanmartin came in and threw four innings and gave up one run "
      "between them. Five strikeouts from Harris in two innings. The bullpen was fine. The "
      "bullpen has been the villain of this entire season and on Tuesday it was fine, and it "
      "did not matter even slightly, because by the time they got the ball the game had "
      "already been handed over.",

      "Fifty one and seventy four. Thirty seven games left in a season that stopped meaning "
      "anything at the deadline. This team is going to lose ninety something games, in a "
      "year where the manager was a first time hire, the best hitters got traded, and the "
      "one genuinely thrilling thing on the whole roster is a first baseman who has not been "
      "old enough to drink for very long.",

      "I am not doing the Vitello rant tonight. {vitello} is still there and I still believe "
      "every word of it, but you do not manage your way out of nine hits in four innings and "
      "seven hits in nine. That is the roster. That is {rebuild}, and it is why {josuar} in "
      "Low A matters more to me right now than anything happening in the actual major league "
      "standings, which is a miserable thing to admit in August.",

      "Watch the kid. That is the whole instruction for the rest of this season. Watch "
      "Eldridge, count the home runs, and try not to think about the other eight spots. The "
      "rest of the year is in {season}, the roster is on the {depth}, and everything else is "
      "on the {hub}.",

      "And if you want to feel better about it, do not look across the bay, because "
      "{athletics} handed a two run ninth inning lead back to Kansas City on the same night. "
      "It was that kind of evening for baseball around here.",
     ],
     links={'eldridge': ('bryce-eldridge-giants-future-franchise-first-baseman-july-2026.html',
                         'the Eldridge column'),
            'vitello': ('giants-tony-vitello-clueless-lineups-eldridge-leadoff.html',
                        'The Vitello case'),
            'rebuild': ('giants-2026-where-the-rebuild-actually-stands.html',
                        'where the rebuild actually stands'),
            'josuar': ('josuar-gonzalez-giants-top-prospect-18-year-old-shortstop.html',
                       'an eighteen year old shortstop'),
            'season': ('giants-2026-season-hub-results-coverage.html', 'the season hub'),
            'depth': ('giants-2026-roster-depth-chart.html', 'depth chart page'),
            'athletics': ('athletics-royals-4-3-ninth-inning-collapse-witt-walkoff-august-18.html',
                          'the Athletics'),
            'hub': ('../giants.html', 'Giants hub')},
     related=[('bryce-eldridge-giants-future-franchise-first-baseman-july-2026.html', 'Giants',
               'Bryce Eldridge Is the Only Future This Team Has'),
              ('giants-rockies-13-7-devers-25th-bullpen-destroyed-august-16.html', 'Giants',
               'Rockies 13, Giants 7: Devers Hit His 25th and It Did Not Matter'),
              ('giants-2026-season-hub-results-coverage.html', 'Giants',
               'The 2026 Giants Season, Game by Game')]),

dict(slug='giants-guardians-5-2-adames-homer-gavin-williams-eleven-strikeouts-august-20',
     section='Giants', tag='Giants', hub='Giants',
     title='Guardians 5, Giants 2: Eleven Strikeouts, Series Won Anyway',
     h1="Gavin Williams Struck Out Eleven, the Giants Lost the Finale, and They Still Left Cleveland Having Won the Series",
     dek="Three run first, a Willy Adames homer that travelled four hundred and eighteen "
         "feet, five hits total, and a road series won by a team that is twenty four and a "
         "half games out. Both of those things are true.",
     desc="Guardians 5, Giants 2: Gavin Williams struck out eleven, Willy Adames hit a 418 "
          "foot two run homer, and San Francisco still left Cleveland with the series.",
     date='2026-08-20',
     card=('giants', 'Series won, finale lost', 'Adames goes 418 feet, Williams fans eleven'),
     body=[
      "You take the series. That is the honest headline here, and it is the one nobody "
      "around here is in the mood to write, because taking a road series in the third week "
      "of August at fifty two and seventy five is like winning an argument you already "
      "lost in April. But they did take it. Eight to one on Tuesday, one to nothing on "
      "Wednesday behind a shutout that had no business happening, and then Thursday the "
      "bill came due in the first inning and never got any smaller.",

      '<div class="reftable" role="region" tabindex="0" aria-label="San Francisco Giants at Cleveland Guardians, Thursday 20 August 2026, Progressive Field, 24,448">\n'
      '<table>\n'
      '<caption>San Francisco Giants at Cleveland Guardians, Thursday 20 August 2026, Progressive Field, 24,448</caption>\n'
      '<thead><tr><th>Team</th><th class="num">1</th><th class="num">2</th><th class="num">3</th><th class="num">4</th><th class="num">5</th><th class="num">6</th><th class="num">7</th><th class="num">8</th><th class="num">9</th><th class="num">R</th><th class="num">H</th><th class="num">E</th></tr></thead>\n'
      '<tbody>\n'
      '<tr><td>San Francisco</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">2</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num"><b>2</b></td><td class="num">5</td><td class="num">2</td></tr>\n'
      '<tr><td><b>Cleveland</b></td><td class="num">3</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">1</td><td class="num">0</td><td class="num">1</td><td class="num">X</td><td class="num"><b>5</b></td><td class="num">9</td><td class="num">0</td></tr>\n'
      '</tbody>\n</table>\n</div>',

      "<b>The first inning was the game.</b> Landen Roupp got three outs eventually and it "
      "cost him three runs to do it, on a Jose Ramirez single, a Nolan Lowe sacrifice fly "
      "and a Patrick Bailey base hit. Three nothing before the Giants had swung at "
      "anything that mattered. Against a pitcher having the night Gavin Williams was about "
      "to have, that is not a deficit, that is a verdict.",

      "<b>Eleven strikeouts in five and two thirds.</b> Williams struck out eleven of the "
      "seventeen outs he recorded. Read that again. San Francisco put five hits on the "
      "board all night and four of them came off him, and one of those four went four "
      "hundred and eighteen feet to right center in the fourth with Rafael Devers standing "
      "on base, which is the only genuinely fun thing that happened.",

      "<b>Willy Adames is doing this again.</b> Two run homer, no doubt about it off the "
      "bat, and it accounted for the entire offensive output. That is the second straight "
      "series where he has been the only reliable source of hard contact in the middle of "
      "this lineup. It is also the second straight series where being the only reliable "
      "source of hard contact has been worth exactly one loss and one win.",

      '<div class="reftable" role="region" tabindex="0" aria-label="Pitching lines, Giants at Guardians, 20 August 2026">\n'
      '<table>\n'
      '<caption>Pitching lines, Giants at Guardians, 20 August 2026</caption>\n'
      '<thead><tr><th>Pitcher</th><th class="num">IP</th><th class="num">H</th><th class="num">R</th><th class="num">ER</th><th class="num">BB</th><th class="num">K</th></tr></thead>\n'
      '<tbody>\n'
      '<tr><td><b>Landen Roupp, SF (L, 7 and 13)</b></td><td class="num">5.1</td><td class="num">5</td><td class="num">4</td><td class="num">3</td><td class="num">4</td><td class="num">2</td></tr>\n'
      '<tr><td>Sam Hentges, SF</td><td class="num">0.2</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">1</td></tr>\n'
      '<tr><td>Carson Seymour, SF</td><td class="num">1.0</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">2</td></tr>\n'
      '<tr><td>JT Brubaker, SF</td><td class="num">1.0</td><td class="num">2</td><td class="num">1</td><td class="num">0</td><td class="num">0</td><td class="num">1</td></tr>\n'
      '<tr><td>Gavin Williams, CLE (W, 12 and 7)</td><td class="num">5.2</td><td class="num">4</td><td class="num">2</td><td class="num">2</td><td class="num">3</td><td class="num">11</td></tr>\n'
      '<tr><td>Cade Smith, CLE (S, 32)</td><td class="num">1.0</td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="num">2</td><td class="num">1</td></tr>\n'
      '</tbody>\n</table>\n</div>',

      "<b>Roupp is now seven and thirteen.</b> Four walks in five and a third is the part "
      "that should bother you more than the four runs, because only three of them were "
      "earned and the two errors behind him did not help. He has been serviceable for "
      "long stretches of a season nobody is watching, and he has a record that makes him "
      "look like a disaster, which is roughly the experience of every Giants starter this "
      "year.",

      "<b>The bullpen was fine, again.</b> Hentges, Carson Seymour and JT Brubaker covered "
      "the last two and two thirds and gave up one unearned run between them. The relief "
      "corps has quietly stopped being the problem, which matters, because for about six "
      "weeks in the middle of the summer it was the entire problem. We got into that in "
      "{rockies}, back when they were handing away thirteen run nights.",

      "<b>Where the season actually is.</b> Fifty two and seventy five. Last in the "
      "National League West. Twenty four and a half games behind the Dodgers, which is not "
      "a gap, it is a different sport being played in the same division. There are thirty "
      "five games left and the only real question is which of the young players get to "
      "spend September finding out whether they can do this.",

      "<b>What is worth watching from here.</b> Bryce Eldridge had a hit and is still the "
      "reason to turn the thing on, and we made that argument at length in {eldridge}. "
      "Devers scored the only run he was involved in. Josuar Gonzalez is eighteen and "
      "playing shortstop somewhere in this system, and {josuar} is the piece on that. The "
      "list of things to care about in a fifty two and seventy five season is short, but "
      "it is not empty, and it is all on {season}.",

      "<b>And the honest part.</b> Winning two of three in Cleveland in August is a nice "
      "night for the people who still travel to see this team and means nothing to the "
      "standings. What it does tell you is that the pitching, which was supposed to be the "
      "one thing carrying this roster, is still functional: one run allowed on Wednesday, "
      "four on Thursday with only three earned. The offense is the thing that has been "
      "broken since May, and {rebuild} covers exactly how long the repair is going to "
      "take.",

      "Across the way, it was worse. The A's got swept in four in Kansas City, and "
      "{athletics} is the receipt on that one. Two teams from this corner of the country, "
      "both of them out of it in August, one of them not even playing here any more. The "
      "rest of it lives on the {hub}.",
     ],
     links={'eldridge': ('bryce-eldridge-giants-future-franchise-first-baseman-july-2026.html',
                         'the Eldridge column'),
            'rockies': ('giants-rockies-13-7-devers-25th-bullpen-destroyed-august-16.html',
                        'the Colorado wreck'),
            'rebuild': ('giants-2026-where-the-rebuild-actually-stands.html',
                        'where the rebuild actually stands'),
            'josuar': ('josuar-gonzalez-giants-top-prospect-18-year-old-shortstop.html',
                       'an eighteen year old shortstop'),
            'season': ('giants-2026-season-hub-results-coverage.html', 'the season hub'),
            'athletics': ('athletics-royals-6-2-four-game-sweep-witt-gage-jump-august-20.html',
                          'the sweep in Kansas City'),
            'hub': ('../giants.html', 'Giants hub')},
     related=[('giants-guardians-1-0-houser-dylan-smith-shutout-august-19.html', 'Giants',
               'Giants 1, Guardians 0: A Shutout Nobody Saw Coming'),
              ('giants-2026-season-hub-results-coverage.html', 'Giants',
               'The 2026 Giants Season, Game by Game'),
              ('giants-2026-where-the-rebuild-actually-stands.html', 'Giants',
               'Where the Rebuild Actually Stands')]),
]


def main():
    check = '--check' in sys.argv
    only = next((x.split('=', 1)[1] for x in sys.argv if x.startswith('--only=')), None)
    for a in ARTICLES:
        if only and a['slug'] != only:
            continue
        p = os.path.join(ROOT, 'articles', a['slug'] + '.html')
        card = os.path.join(CC.CARDS, a['slug'] + '.jpg')
        words = sum(len(re.sub(r'<[^>]+>', ' ', x).split()) for x in a['body'])
        print('  %-52s %4dw  %2d links  title %2d  desc %3d'
              % (a['slug'][:52], words, sum(x.count('{') for x in a['body']),
                 len(a['title']), len(a['desc'])))
        if check:
            continue
        if not os.path.exists(card):
            subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'cardgen.py'),
                            a['card'][0], a['card'][1], a['card'][2], card], check=True)
        out = CC.build(a)
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write(out)
        b = open(p, 'rb').read()
        if b'\x00' in b or b.count(b'\xef\xbf\xbd'):
            raise SystemExit('corruption writing %s' % p)
    print('%s  %d articles' % ('CHECK' if check else 'WROTE', len(ARTICLES)))


if __name__ == '__main__':
    main()
