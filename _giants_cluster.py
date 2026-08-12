#!/usr/bin/env python3
"""_giants_cluster.py - the Giants authority foundation.

The Giants archive is the largest on the site: 46 articles, 20 of them game recaps, and
the strongest evergreen pages anywhere on the blog. What it does not have is furniture -
a roster page, a page that says where the rebuild actually stands after the selloff, a
records page, or anything about the ballpark itself.

Deliberately NOT duplicated - the archive already owns these:
  bryce-eldridge-giants-future-franchise-first-baseman  1,515w, the definitive Eldridge piece
  giants-season-over-build-around-eldridge-posey-bullpen 26 inbound, the July argument
  giants-trade-deadline-monday-posey-sell-ramos-arraez-ray  the deadline column
  tony-vitello-hire-giants-mistake / -not-ready / -clueless-lineups  the manager case
  barry-bonds-giants-home-run-king  the Bonds column
  giants-dynasty-even-year-magic / flashback-bumgarner / bruce-bochy  the dynasty
  giants-1993-pennant-race-*  the 1993 race
  giants-oracle-park-still-waiting  the October drought column - NOT a park guide

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
                      'Francisco Giants &mdash; Tuesday 11 August 2026, Oracle Park, '
                      '30,093</caption>\n' + LINEHEAD + '\n<tbody>\n'
                      + LINE('Houston', [0, 1, 0, 0, 0, 0, 0, 0, 0], 1, 5, 2) + '\n'
                      + LINE('<b>San Francisco</b>', [0, 1, 0, 1, 1, 1, 0, 0, 'X'], 4, 9, 0)
                      + '\n</tbody>\n</table>\n</div>')

GIANTS_ASTROS_BOX = """<div class="reftable">
<table>
<caption>Pitching &mdash; Astros at Giants, 11 August 2026</caption>
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
      "at the time and still looks like one. Beyond that it is arms and lottery tickets - "
      "the Mahle deal brought back a twenty-four-year-old who went straight to Sacramento. "
      "None of it is a franchise-altering haul. All of it is better than watching those "
      "contracts expire for nothing, which is what happened the last time.",
      "<b>What is actually left.</b> {eldridge} is the centre of everything now, and our "
      "long piece on him remains the best case for optimism on this roster. Rafael Devers "
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
      "to .500. That is the trap this franchise has fallen into repeatedly - buying just "
      "enough to be uninteresting, finishing fourth, and arriving at the next deadline "
      "with nothing to sell and nothing to promote. The selloff only means something if "
      "the next move is patience.",
      "The roster detail is on the {depth}, the season's games are in the {season}, and "
      "the rest is on the {hub}.",
     ],
     links={'arraez': ('giants-arraez-kilian-traded-phillies-august-3.html', 'Luis Arraez'),
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
      "a lost season is that those innings are free - the wins were never coming, so the "
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
     card=('giants', 'The 2026 Season', 'Hope, collapse, selloff - in order'),
     body=[
      "This is the page to start from if you want the season as a story rather than as a "
      "pile of separate columns. It gets updated as games are played.",
      "<b>The shape of it.</b> The Giants spent the first half hanging around, arrived at "
      "the All-Star break at 41-55, and then got worse. By the deadline they were "
      "nineteen games under .500 and selling. That is the arc, and every individual game "
      "below is a variation on it.",
      "<b>July: the month it ended.</b> The bullpen defined it. {kilian} coughed up a "
      "two-out lead to the worst team in baseball, and that game turned out to be the "
      "template. There was a genuinely good stretch at the end of the month - "
      "{heating} covers the run where they beat the best team in baseball twice and hung "
      "sixteen on Milwaukee - but it was a mirage inside a losing season.",
      "<b>The All-Star break.</b> {firsthalf} is the accounting: 41-55, a lost first "
      "half, and a rookie manager learning on the job in public.",
      "<b>August: the selloff.</b> Three days in San Diego where they got swept, and then "
      "the deadline. {deadline} was the argument beforehand; {rebuild} is where things "
      "actually stand now. And then the eight-nothing loss to Detroit on 8 August, where "
      "{roupp} in front of a full ballpark - the clearest picture yet of where this "
      "clubhouse stands on its manager. The day after that, {webb} and lost anyway in ten "
      "innings, which is the other half of the same problem. Then on 11 August, {astros} "
      "for win number fifty, which is the first genuinely encouraging night since the "
      "deadline.",
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
      "391, and right field is 309 - which sounds like a bandbox until you understand "
      "what sits behind that right-field wall and how quickly the fence runs away from "
      "the plate into right-centre. The short porch is a target for maybe a dozen swings "
      "a season. Everything else that goes that way dies in the gap.",
      "<b>The wind.</b> The genuine equaliser, and the reason batted-ball data at this "
      "park does not travel. Evening games get a cold, heavy marine air that takes real "
      "distance off a fly ball. Hitters who arrive here from warmer parks spend a season "
      "learning that the ball they crushed in July would have been out somewhere else.",
      "<b>What the numbers say.</b> Recent park factors put runs at 94 and home runs at "
      "78, against a league average of 100. Runs are suppressed slightly. Home runs are "
      "suppressed enormously - roughly a fifth fewer than a neutral park. Oracle Park is "
      "not a mild pitcher's park. It is one of the hardest places in baseball to hit a "
      "ball out.",
      "<b>McCovey Cove.</b> The water beyond right field is named for Willie McCovey, and "
      "the name came from sportswriters rather than a marketing department - the thought "
      "being that McCovey, who spent his career fighting the wind at Candlestick, would "
      "have put dozens of balls in there had he played on the water instead.",
      "<b>Splash hits.</b> A home run that clears the right-field wall and reaches the "
      "water on the fly. The first belonged to {bonds}, off a Mets left-hander on 1 May "
      "2000, which is about as fitting as sporting history gets. And here is the detail "
      "that tells you everything about the geometry: no right-handed hitter has ever put "
      "one in the Cove the opposite way. Not one, in a quarter of a century.",
      "<b>Why it matters to how the team is built.</b> A park that eats home runs "
      "rewards contact, speed, defence and pitching, and punishes a roster built on "
      "slug. That is not a coincidence in the {dynasty} - those teams were pitching and "
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
      "which is the single most Vitello sequence of the season - wrong on the decision, "
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
      "young players are real - and we cannot even get a clean answer to that, because "
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
      "Basabe gets on, Drew Gilbert hits an infield single - an <i>infield single</i>, "
      "which is the most 2026 Giants way imaginable to score a run - and it is one-all. "
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
      "line single to left. One-all. In the fourth, Drew Cavanaugh &mdash; the rookie catcher, "
      "twenty-eight games in, hitting .242 &mdash; singled Gilbert home and then stole the first "
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
      "up twice. After the summer this bullpen has had &mdash; after the eighth innings in San "
      "Diego, after {webb} &mdash; that deserves to be written down somewhere.",

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
