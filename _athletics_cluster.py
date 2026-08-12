#!/usr/bin/env python3
"""_athletics_cluster.py - the Athletics cluster, built on the one angle we own.

22 articles in the archive and 16 of them are game recaps. The single strongest page is
athletics-sacramento-bay-area-villains (23 inbound), which is the grievance column - and
that is exactly the right instinct, because the distinctive thing this site can say about
this franchise has nothing to do with the standings.

So this cluster is not generic A's coverage. It is four pages about the actual situation:
a major league team playing in a 14,014-seat minor league park in West Sacramento while a
$2 billion dome goes up on the Las Vegas Strip.

Deliberately NOT duplicated:
  athletics-sacramento-bay-area-villains  the grievance column, 23 inbound - stays the
      emotional piece; the ballpark page here is the factual one
  athletics-first-half-breakdown / free-fall-continues  the season columns

  python _athletics_cluster.py [--check]
"""
import os, re, sys, subprocess
import _college_cluster as CC

ROOT = os.path.dirname(os.path.abspath(__file__))

N = lambda v: '<td class="num">%s</td>' % v
LINEHEAD = ('<thead><tr><th>Team</th>' + ''.join('<th class="num">%d</th>' % i
                                                 for i in range(1, 10))
            + '<th class="num">R</th><th class="num">H</th><th class="num">E</th></tr></thead>')
LINE = lambda team, innings, r, h, e: ('<tr><td>%s</td>%s<td class="num"><b>%s</b></td>'
                                       '<td class="num">%s</td><td class="num">%s</td></tr>'
                                       % (team, ''.join(N(x) for x in innings), r, h, e))

RAYS_AS_LINE = ('<div class="reftable">\n<table>\n<caption>Tampa Bay Rays at Athletics '
                '&mdash; Tuesday 11 August 2026, Sutter Health Park, 8,154</caption>\n'
                + LINEHEAD + '\n<tbody>\n'
                + LINE('Tampa Bay', [2, 0, 1, 3, 0, 1, 2, 3, 0], 12, 11, 0) + '\n'
                + LINE('<b>Athletics</b>', [0, 0, 0, 2, 0, 0, 0, 0, 2], 4, 8, 1)
                + '\n</tbody>\n</table>\n</div>')

RAYS_AS_HOMERS = """<div class="reftable">
<table>
<caption>Every home run hit at Sutter Health Park on 11 August 2026</caption>
<thead><tr><th>Inning</th><th>Batter</th><th>Off</th><th class="num">On</th><th class="num">No.</th></tr></thead>
<tbody>
<tr><td>1st</td><td>Junior Caminero, TB</td><td>Mason Barnett</td><td class="num">1</td><td class="num">35</td></tr>
<tr><td>4th</td><td>Taylor Walls, TB</td><td>Mason Barnett</td><td class="num">1</td><td class="num">1</td></tr>
<tr><td>4th</td><td>Yandy D&iacute;az, TB</td><td>Mason Barnett</td><td class="num">0</td><td class="num">17</td></tr>
<tr><td>4th</td><td><b>Lawrence Butler, ATH</b></td><td>Nick Martinez</td><td class="num">1</td><td class="num">8</td></tr>
<tr><td>6th</td><td>Taylor Walls, TB</td><td>Brady Basso</td><td class="num">0</td><td class="num">2</td></tr>
<tr><td>7th</td><td>Victor Mesa Jr., TB</td><td>Elvis Alvarado</td><td class="num">1</td><td class="num">10</td></tr>
<tr><td>8th</td><td>Carson Williams, TB</td><td>Yunior Tur</td><td class="num">2</td><td class="num">1</td></tr>
</tbody>
</table>
</div>"""

ARTICLES = [
# ------------------------------------------------------- 1. Sutter Health Park evergreen
dict(slug='sutter-health-park-mlb-guide-dimensions-capacity',
     section='Athletics', tag='Athletics', hub='Athletics',
     title='Sutter Health Park: What It Is Like When MLB Plays in a Triple-A Yard',
     h1="Sutter Health Park: What Actually Happens When a Major League Team Plays in a Triple-A Ballpark",
     dek="Fourteen thousand seats, a 325-foot right field, the third-windiest conditions "
         "in baseball, and a home run rate that ranks second in the major leagues. The "
         "numbers behind the strangest home field in the sport.",
     desc="Sutter Health Park by the numbers: capacity 14,014, the dimensions, the wind, "
          "and why it produces the second-highest home run rate in Major League Baseball.",
     date='2026-08-08',
     card=('athletics', 'Sutter Health Park', 'A 14,014-seat major league home field'),
     body=[
      "There is no precedent for this. A Major League Baseball franchise is playing its "
      "home schedule in a ballpark built for Triple-A, in a city that is not its own, "
      "in front of a fraction of the crowd it used to draw, while it waits for a "
      "building in another state. This page is the factual version of that. The "
      "{grievance} is where we keep the feelings.",
      "<b>The size of it.</b> Sutter Health Park holds 14,014. The fixed seating is "
      "10,624 - the rest is lawn and standing room. For scale, that is a capacity smaller "
      "than most college basketball arenas, hosting a sport that expects forty thousand. "
      "The A's have averaged 9,781 over their time here, which means the building is not "
      "even full most nights.",
      "<b>The dimensions.</b> Left field 330, centre 403, right field 325. Those corner "
      "numbers are short by major league standards and that centre-field number is not, "
      "which produces a strange shape: a park with one of the largest outfield footprints "
      "in the sport and two of the more reachable corners.",
      "<b>The wind, which is the real story.</b> Average wind speed at Sutter Health Park "
      "is 11.1 miles per hour - the third highest in Major League Baseball. Add Sacramento "
      "summer heat, which thins the air and carries a ball further than coastal "
      "conditions ever will, and you get a park that punishes pitchers in a way nothing "
      "in the Bay Area does.",
      "<b>What the numbers actually come out as.</b> Second in Major League Baseball for "
      "home runs. Second for total runs. Third for doubles and triples. Fourth for total "
      "hits. This is one of the most offense-friendly environments in the sport, and it "
      "happened by accident - nobody designed a launching pad, they just moved a major "
      "league team into a minor league park in a hot, windy valley.",
      "<b>Why that matters beyond trivia.</b> Every pitching statistic this franchise "
      "produces right now is distorted, and so is every hitting statistic. A pitcher who "
      "posts a mediocre ERA here might be doing genuinely good work. A hitter whose "
      "numbers look like a breakout might be a product of the air. Anyone evaluating "
      "these players - including whoever runs this team in 2028 - has to correct for a "
      "ballpark that no other franchise has ever had to correct for.",
      "<b>The comparison nobody makes.</b> Across the bay, {oracle} suppresses home runs "
      "by roughly a fifth. Sutter Health Park is near the top of the league for them. Two "
      "teams ninety minutes apart are playing in about as different a pair of environments "
      "as the sport currently offers, and one of those environments is temporary.",
      "<b>Is it a good place to watch a game?</b> Honestly, yes - a small park with a "
      "lawn and good sightlines is a pleasant evening, and people who have gone say so. "
      "That is the uncomfortable part of the whole thing. It is a lovely little ballpark. "
      "It is just not a major league home, and it was never supposed to be one, which is "
      "the whole of {legacy2}. {timeline} covers how long this arrangement has left to "
      "run.",
      "The roster playing in it is on the {depth}, and the rest is on the {hub}.",
     ],
     links={'grievance': ('athletics-sacramento-bay-area-villains.html', 'grievance column'),
            'oracle': ('oracle-park-mccovey-cove-splash-hits-guide.html', 'Oracle Park'),
            'timeline': ('athletics-oakland-sacramento-las-vegas-timeline.html',
                         'The relocation timeline'),
            'legacy2': ('oakland-athletics-legacy-what-the-bay-area-lost.html',
                        'what the Bay Area lost'),
            'depth': ('athletics-2026-roster-depth-chart.html', 'depth chart page'),
            'hub': ('../athletics.html', "A's hub")},
     related=[('athletics-oakland-sacramento-las-vegas-timeline.html', 'Athletics', 'Oakland to Sacramento to Las Vegas: The Timeline'),
              ('athletics-sacramento-bay-area-villains.html', 'Bay Area Villains', "The A's Play in Sacramento Now"),
              ('athletics-2026-roster-depth-chart.html', 'Athletics', "The Athletics Roster and Depth Chart")]),

# ------------------------------------------------------- 2. Relocation timeline evergreen
dict(slug='athletics-oakland-sacramento-las-vegas-timeline',
     section='Athletics', tag='Athletics', hub='Athletics',
     title='Oakland to Sacramento to Las Vegas: The Whole Timeline',
     h1="Oakland to Sacramento to Las Vegas: The Whole Timeline, and Where It Actually Stands",
     dek="Fifty-seven years in Oakland, a temporary stop in a Triple-A park, and a $2 "
         "billion dome on the Strip that is genuinely being built. The dates, kept "
         "updated.",
     desc="The Athletics relocation timeline: leaving Oakland, the West Sacramento years, "
          "and the $2 billion Las Vegas ballpark tracking toward a 2028 opening.",
     date='2026-08-08',
     card=('athletics', 'The Timeline', 'Oakland, West Sacramento, and a dome on the Strip'),
     body=[
      "This is the page that keeps the relocation straight, because the story has moved "
      "in stages and each stage got argued about separately. It gets updated as the dates "
      "move.",
      "<b>Oakland.</b> Fifty-seven years of major league baseball, three consecutive World "
      "Series titles in the early seventies, the Bash Brothers, the twenty-game winning "
      "streak, and a Coliseum that went from serviceable to embarrassing while ownership "
      "and the city spent two decades failing to agree on a replacement. However you "
      "apportion the blame - and this blog has a view - the outcome was a city losing a "
      "franchise it had supported for three generations. {legacy} is the record of what "
      "that actually meant.",
      "<b>West Sacramento, now.</b> The interim arrangement: a major league team playing "
      "at {sutter}, a 14,014-seat Triple-A park, with an average crowd under ten "
      "thousand. Not a home, a waiting room. And unlike most relocations, the fans who "
      "supported this team are close enough to watch it happen and far enough that most "
      "of them do not go.",
      "<b>Las Vegas, the part that is actually real.</b> This is where people who stopped "
      "paying attention are still out of date. The ballpark is under construction on the "
      "Strip, at Tropicana Avenue and Las Vegas Boulevard, on the site of the old "
      "Tropicana hotel. It is a $2 billion, roughly 33,000-seat domed stadium. Test "
      "pilings began in May 2025, the ceremonial groundbreaking was 23 June 2025, and the "
      "build is a 32-month programme aimed at Opening Day 2028.",
      "<b>Where it stands right now.</b> On schedule, by every account from the people "
      "running it. Over a thousand piles are in the ground, some as deep as eighty-five "
      "feet. The lower bowl is taking shape. The first of six roof trusses has been "
      "raised. Whatever anyone in the Bay Area wants to believe, this building is "
      "happening and it is happening roughly on time.",
      "<b>What that means for the schedule of grief.</b> If 2028 holds, this franchise "
      "plays the 2026 and 2027 seasons in West Sacramento and then leaves the region for "
      "good. That is not a distant hypothetical any more. It is two more summers.",
      "<b>The thing worth saying plainly.</b> A domed stadium on the Las Vegas Strip will "
      "probably be a good place to watch a baseball game, and the team will probably draw "
      "better there than it did in a decaying Coliseum. Both of those can be true and it "
      "can still be a civic theft. Oakland did not lose this team because Oakland stopped "
      "caring. {villains} is where we make that argument properly.",
      "<b>The Bay Area question nobody has answered.</b> What happens to the fans. A "
      "supporter in Oakland or the East Bay has three options and all of them are bad: "
      "drive ninety minutes to West Sacramento to watch a team that left, switch to the "
      "Giants and pretend fifty-seven years did not happen, or stop watching baseball. "
      "Most have chosen the third, which is why the attendance numbers look the way they "
      "do and why they are not actually a measurement of anything except grief.",
      "<b>What we are watching next.</b> Construction milestones on the Strip, whether "
      "the 2028 date holds, attendance in West Sacramento across a second full season, "
      "and what happens to the players developed in the interim - because the roster "
      "being assembled now is the one that opens that building. The current group is on "
      "the {depth}.",
      "The rest of our coverage is on the {hub}.",
     ],
     links={'sutter': ('sutter-health-park-mlb-guide-dimensions-capacity.html',
                       'Sutter Health Park'),
            'legacy': ('oakland-athletics-legacy-what-the-bay-area-lost.html',
                       'What the Bay Area lost'),
            'villains': ('athletics-sacramento-bay-area-villains.html', 'Our column on the move'),
            'depth': ('athletics-2026-roster-depth-chart.html', 'depth chart page'),
            'hub': ('../athletics.html', "A's hub")},
     related=[('sutter-health-park-mlb-guide-dimensions-capacity.html', 'Athletics', 'Sutter Health Park: MLB in a Triple-A Yard'),
              ('athletics-sacramento-bay-area-villains.html', 'Bay Area Villains', "The A's Play in Sacramento Now"),
              ('athletics-2026-roster-depth-chart.html', 'Athletics', "The Athletics Roster and Depth Chart")]),

# ------------------------------------------------------- 3. Roster / depth chart
dict(slug='athletics-2026-roster-depth-chart',
     section='Athletics', tag='Athletics', hub='Athletics',
     title='The Athletics Roster and Depth Chart',
     h1="The Athletics Roster and Depth Chart, Position by Position",
     dek="The young core that will actually open the building in Las Vegas, the arms "
         "being asked to pitch in a launching pad, and where this roster runs out.",
     desc="A position-by-position look at the Athletics roster: the young core, the "
          "rotation, and which players are likely to still be here in 2028.",
     date='2026-08-08',
     card=('athletics', 'Roster & Depth', 'The young core that opens the Las Vegas building'),
     body=[
      "The useful way to read this roster is not by the standings. It is by asking which "
      "of these players is still here when the building on the Strip opens, because that "
      "is the only timeline this front office is really working to.",
      "<b>Rotation.</b> {lopez} has been the most watchable thing about this season - he "
      "keeps pitching well enough to win and keeps getting nothing behind him, including "
      "a night he struck out nine on 87 pitches and got pulled anyway. Gage Jump and JT "
      "Ginn have both had games that looked like a future and games that looked like "
      "development. Ginn's return from a blister was one of the few genuinely encouraging "
      "stretches of the summer.",
      "<b>What the ballpark does to all of them.</b> Every one of those evaluations has "
      "to be discounted, because {sutter} produces the second-highest home run rate in "
      "the major leagues. A pitcher surviving here is doing harder work than his ERA "
      "suggests. That is not an excuse, it is a measurement problem, and it is unique to "
      "this franchise.",
      "<b>Bullpen.</b> The part that has cost the most games. Blown leads in the eighth, "
      "extra-inning losses, and at one point a defeat sealed by consecutive wild pitches. "
      "For a team whose starters have generally competed, the back end has been the "
      "difference between a bad season and an embarrassing one.",
      "<b>Infield.</b> Jacob Wilson at shortstop has been a genuine bright spot, "
      "including a homer that stole a game back in the ninth, and on 9 August he {wilson} "
      "- 111 consecutive errorless games at the position, past Mike Bordick's 110 from "
      "2002. By {streak} the streak was at 113. Nick Kurtz started an "
      "All-Star Game. Tyler Soderstrom keeps showing up in the box score for the right "
      "reasons. Brian Serven and Tommy White have both had days worth remembering.",
      "<b>Outfield and DH.</b> Brent Rooker remains the bat that can change a game with "
      "one swing, and Shea Langeliers started an All-Star Game behind the plate. Those "
      "two are the closest thing this roster has to established major league quality.",
      "<b>Where it runs out.</b> Everywhere behind the first six or seven names. This is "
      "a roster being run at the bottom of the payroll during an interim period, and the "
      "depth reflects exactly that. When somebody gets hurt, the replacement is a "
      "prospect who was not ready, which is how a team ends up losing nine in a row twice "
      "in one summer.",
      "<b>How to read a bad record here.</b> This team has lost nine straight twice in "
      "one summer and finished the first half at 41-55, and almost none of that is "
      "information about the players. It is a bottom-five payroll, an interim ballpark "
      "that inflates every number in both directions, and a roster whose best young "
      "pieces are being asked to develop in the least stable environment in the sport. "
      "Judge the individuals; the record belongs to the situation.",
      "<b>The 2028 question.</b> Kurtz, Langeliers, Wilson, Soderstrom, Lopez, Jump - "
      "that is the group young enough to still be here when the {timeline} reaches its "
      "end and the doors open in Las Vegas. Everything else on this roster is temporary "
      "in a more ordinary sense.",
      "The season's games are in the archive on the {hub}, and the ballpark they are "
      "being played in is on the {park}.",
     ],
     links={'lopez': ('athletics-reds-3-2-jacob-lopez-pulled-seventh-straight-august-5.html',
                      'Jacob Lopez'),
            'wilson': ('athletics-red-sox-4-3-muncy-chapman-first-series-win-august-9.html',
                       'set a major league record for shortstops'),
            'streak': ('athletics-rays-12-4-six-homers-taylor-walls-nick-martinez-august-11.html',
                       'the twelve-four loss to Tampa Bay on 11 August'),
            'sutter': ('sutter-health-park-mlb-guide-dimensions-capacity.html',
                       'Sutter Health Park'),
            'timeline': ('athletics-oakland-sacramento-las-vegas-timeline.html', 'timeline'),
            'park': ('sutter-health-park-mlb-guide-dimensions-capacity.html', 'ballpark page'),
            'hub': ('../athletics.html', "A's hub")},
     related=[('sutter-health-park-mlb-guide-dimensions-capacity.html', 'Athletics', 'Sutter Health Park: MLB in a Triple-A Yard'),
              ('athletics-oakland-sacramento-las-vegas-timeline.html', 'Athletics', 'Oakland to Sacramento to Las Vegas'),
              ('athletics-first-half-breakdown-mirage-collapse-all-star-break-2026.html', 'Athletics', "A's at the Break: 41-55")]),

# ------------------------------------------------------- 4. Oakland legacy evergreen
dict(slug='oakland-athletics-legacy-what-the-bay-area-lost',
     section='Athletics', tag='Bay Area Villains', hub='Athletics',
     title='What the Bay Area Actually Lost When the A’s Left Oakland',
     h1="What the Bay Area Actually Lost When the A's Left Oakland, and Why It Still Stings",
     dek="Three straight World Series in the seventies, the Bash Brothers, a twenty-game "
         "winning streak, and a fan base that got told it was the problem. The legacy, "
         "written down before it gets rewritten.",
     desc="The Oakland Athletics legacy: three straight titles in the 1970s, the Bash "
          "Brothers, the twenty-game streak, and what the Bay Area lost when they left.",
     date='2026-08-08',
     card=('athletics', 'Oakland', 'Fifty-seven years, three straight titles, and what is left'),
     body=[
      "The version of this story that will get told in ten years is that Oakland could "
      "not support a baseball team. It is worth writing the real one down now, while "
      "everyone still remembers.",
      "<b>Fifty-seven years.</b> The Athletics played in Oakland from 1968. That is three "
      "generations of families, an entire regional identity, and a franchise that was, "
      "for long stretches, one of the genuinely great operations in the sport.",
      "<b>The seventies.</b> Three consecutive World Series championships. Not a "
      "contender, not a nice story - a dynasty, in green and gold, with a roster full of "
      "personalities that a modern marketing department would not survive. Very few "
      "franchises in the history of the sport have done what those teams did.",
      "<b>The eighties and the Bash Brothers.</b> Canseco and McGwire turned Oakland into "
      "the loudest ballpark in America for a few summers, and the sport into something "
      "bigger and more complicated. That era is remembered nationally as a scandal. "
      "Around here it is also remembered as a time when the Coliseum was the most fun "
      "building in baseball.",
      "<b>Moneyball and the twenty-game streak.</b> A small-market team out-thinking the "
      "sport, and a twenty-game winning streak that remains one of the most extraordinary "
      "runs anyone has produced. That story got a book and a film, and the film made the "
      "franchise a global brand - which is its own bitter joke, given what happened next.",
      "<b>What the fan base actually did.</b> This is the part that gets erased. When "
      "those teams were good, that building was as loud and as committed as anywhere in "
      "the sport. The right-field bleachers were an institution. The drumming, the flags, "
      "the whole culture of it was produced by people who were told for twenty years that "
      "their stadium was inadequate and their attendance was insufficient, while the "
      "product on the field was systematically stripped every time it got good.",
      "<b>The honest accounting.</b> The Coliseum genuinely was a poor facility by the "
      "end. Oakland's political process genuinely failed to deliver a replacement. Both "
      "true. And also true: a franchise that traded away every good player it developed, "
      "ran one of the lowest payrolls in the sport for years, and then pointed at empty "
      "seats as evidence that the market had failed. You do not get to starve a thing "
      "and then call it dead.",
      "<b>The Coliseum itself.</b> It became a punchline - the sewage, the tarps over "
      "the upper deck, the possums. All of that was real and all of it was also the "
      "predictable end state of a building nobody was allowed to invest in. It is worth "
      "remembering that the same concrete bowl once held the loudest crowds in the sport, "
      "and that a stadium does not decay on its own.",
      "<b>What is left.</b> A Triple-A ballpark in {sutter}, two more summers of it, and "
      "then a dome in Nevada. The {timeline} has the dates. The {villains} column has the "
      "anger. This page is just the record, so that when somebody says Oakland did not "
      "care, there is something to point at.",
      "The rest of our coverage is on the {hub}.",
     ],
     links={'sutter': ('sutter-health-park-mlb-guide-dimensions-capacity.html',
                       'West Sacramento'),
            'timeline': ('athletics-oakland-sacramento-las-vegas-timeline.html',
                         'relocation timeline'),
            'villains': ('athletics-sacramento-bay-area-villains.html', 'Bay Area Villains'),
            'hub': ('../athletics.html', "A's hub")},
     related=[('athletics-sacramento-bay-area-villains.html', 'Bay Area Villains', "The A's Play in Sacramento Now"),
              ('athletics-oakland-sacramento-las-vegas-timeline.html', 'Athletics', 'Oakland to Sacramento to Las Vegas'),
              ('bay-area-sports-history.html', 'Bay Area Sports', 'Why the Bay Area Is One of the Greatest Sports Regions')]),

# ------------------------------------- 5. A's 4-3 at Fenway, Sun 9 August 2026
dict(slug='athletics-red-sox-4-3-muncy-chapman-first-series-win-august-9',
     section='Athletics', tag='Athletics', hub='Athletics',
     title="A's 4, Red Sox 3: A Series Win, Their First Since Mid-June",
     h1="Athletics 4, Red Sox 3: Max Muncy Took Aroldis Chapman Off the Monster and the "
        "A's Finally Won a Series Again",
     dek="Down one in the ninth at Fenway, they beat the closer, McNeil got his thousandth "
         "hit, and Jacob Wilson set a major league record nobody in the Bay Area will hear "
         "about.",
     desc="Max Muncy's ninth-inning double off Aroldis Chapman beat Boston 4-3 and gave the "
          "Athletics their first series win since mid-June, plus McNeil's 1,000th hit.",
     date='2026-08-10',
     card=('athletics', 'Series Win', 'Muncy off Chapman at Fenway, first series since June'),
     body=[
      "The Athletics won a series. An actual series. Two out of three at Fenway Park, "
      "finished off on Sunday with a ninth-inning double off the Green Monster against "
      "Aroldis Chapman, and it is the first series this franchise has won since the middle "
      "of June.",
      "Read that again. Mid-June. And the last one came against Colorado in Las Vegas, at "
      "their own Triple-A affiliate's ballpark, which is either a punchline or a business "
      "plan depending on how charitable you are feeling about the people who run this "
      "team.",
      "Here is how Sunday actually went. They scratched runs in the first and the fourth "
      "and had a two-nothing lead in Boston, which for this ballclub is the equivalent of "
      "getting up three touchdowns. The Red Sox tied it in the fifth and then went ahead, "
      "and every single person who has watched an inning of this season knew exactly how "
      "the rest of it was going to go, because that is what the last two months have been. "
      "They lost {ninth} to this same Boston team on Friday. Nine in a row before that. "
      "A tailspin that stopped being funny around the middle of July.",
      "And then they did not fold. Jonah Heim doubles home the tying run with two out in "
      "the eighth. Elvis Alvarado gets three outs. And in the ninth, with Chapman on the "
      "mound - Chapman, who is still throwing gas at thirty-eight and still terrifying - "
      "Max Muncy lines one off the Monster and Oakland, Sacramento, whatever we are "
      "calling them, has the lead. Hogan Harris pitches the ninth for his eleventh save. "
      "Four to three. Series won.",
      "Two other things happened in that game that deserve better than they are going to "
      "get. Jeff McNeil singled in the eighth for the thousandth hit of his career, which "
      "is a genuine milestone for a genuinely good hitter who is finishing his career in "
      "the strangest circumstance in the sport. And Jacob Wilson played his hundred and "
      "eleventh consecutive game at shortstop without an error, which is a major league "
      "record for the position - he passed Mike Bordick's hundred and ten from 2002.",
      "A major league record. Set by a young shortstop who plays his home games in a "
      "fourteen-thousand-seat minor league yard in West Sacramento in front of nine "
      "thousand people, for a franchise that ran away from the seventh-largest market in "
      "America. That is what this move actually costs, and it does not show up in a "
      "relocation press release. Wilson does something no shortstop in the history of "
      "baseball has done and there is no home crowd to stand up for it, no radio call "
      "anybody around here heard, no bar in Oakland going nuts. He did it in Boston, on a "
      "Sunday, in front of thirty-six thousand people who do not care about him.",
      "Forty-seven and seventy-one. That is the record after the win, and it is not going "
      "anywhere good. But this is the part I am not going to be cynical about, because I "
      "grew up in this region and I am not capable of being fully cynical about green and "
      "gold: there are real major league players in that clubhouse. Wilson is a real "
      "shortstop. Muncy took a good closer deep into the ninth and beat him. McNeil has a "
      "thousand hits. Heim came through with two out. That roster is not the problem and "
      "has never been the problem, and {legacy} is the whole argument.",
      "The problem is that they are two summers away from a dome on the Las Vegas Strip "
      "and every one of these afternoons is happening in a holding pattern. A series win "
      "in August in a lost season is supposed to mean something small and warm - your team "
      "took two of three in a hard place to play. Instead it is a thing that happened in a "
      "city they left, on the way to a city they were never from, in a season being played "
      "in a third city entirely.",
      "Take the win anyway. They beat Chapman at Fenway. The dates on the move are in the "
      "{timeline}, the ballpark they are stuck in until 2028 is in {sutter}, who is "
      "actually playing is on the {depth}, and the anger lives in {villains}. The rest is "
      "on the {hub}.",
     ],
     links={'ninth': ('athletics-redsox-13-1-tolle-14-strikeouts-ninth-straight-august-7.html',
                      'thirteen-one'),
            'legacy': ('oakland-athletics-legacy-what-the-bay-area-lost.html',
                       'what the Bay Area lost'),
            'timeline': ('athletics-oakland-sacramento-las-vegas-timeline.html',
                         'relocation timeline'),
            'sutter': ('sutter-health-park-mlb-guide-dimensions-capacity.html',
                       'Sutter Health Park'),
            'depth': ('athletics-2026-roster-depth-chart.html', 'depth chart'),
            'villains': ('athletics-sacramento-bay-area-villains.html', 'Bay Area Villains'),
            'hub': ('../athletics.html', "A's hub")},
     related=[('athletics-redsox-13-1-tolle-14-strikeouts-ninth-straight-august-7.html',
               'Athletics', "Red Sox 13, A's 1: Ninth Straight"),
              ('athletics-2026-roster-depth-chart.html', 'Athletics', "The A's Roster and Depth Chart"),
              ('athletics-sacramento-bay-area-villains.html', 'Bay Area Villains',
               "The A's Play in Sacramento Now")]),

# ------------------------------------- 6. Rays 12-4, Tue 11 August 2026, West Sacramento
dict(slug='athletics-rays-12-4-six-homers-taylor-walls-nick-martinez-august-11',
     section='Athletics', tag='Athletics', hub='Athletics',
     title="Rays 12, A's 4: Six Home Runs, Two of Them From a .216 Hitter",
     h1="Rays 12, Athletics 4: Six Home Runs Left the Yard, Taylor Walls Hit Two of Them, "
        "and Nick Martinez Went the Distance in Front of Eight Thousand People",
     dek="Twenty-two runs allowed in two nights, a complete game thrown against them by a "
         "man who did not walk anybody, and a series lost before the series was over.",
     desc="Tampa Bay hit six home runs in a 12-4 win at Sutter Health Park and Nick "
          "Martinez threw a complete game. The A's fall to 47-73 and lose another series.",
     date='2026-08-12',
     card=('athletics', 'Six Homers', 'Tampa Bay hit six out of a Triple-A yard in West Sacramento'),
     body=[
      "Six home runs. Six. In a ballpark the Athletics do not own, in a city the Athletics "
      "are not from, in front of eight thousand one hundred and fifty-four people on an "
      "eighty-six degree Tuesday night. Tampa Bay beat them twelve to four, the series is "
      "already gone with a game still to play, and this is now twenty-two runs allowed in two "
      "nights against a team that has won eight straight and does not appear likely to stop.",

      '<figure style="margin:0 0 30px;text-align:center">'
      '<picture><source type="image/webp" srcset="../assets/img/players/sutter-health-park-real-400w.webp 400w, '
      '../assets/img/players/sutter-health-park-real-600w.webp 600w, '
      '../assets/img/players/sutter-health-park-real-800w.webp 800w, '
      '../assets/img/players/sutter-health-park-real.webp 1800w" sizes="(max-width: 820px) 92vw, 760px">'
      '<img src="../assets/img/players/sutter-health-park-real.jpg" '
      'alt="Sutter Health Park in West Sacramento, where the Rays beat the Athletics 12-4 on 11 August 2026" '
      'style="display:block;width:100%;max-width:760px;height:auto;margin:0 auto;object-fit:cover;'
      'background:var(--surface);border-radius:12px;border:1px solid var(--line)" width="1200" height="675" '
      'decoding="async" fetchpriority="high" '
      'srcset="../assets/img/players/sutter-health-park-real-400w.jpg 400w, '
      '../assets/img/players/sutter-health-park-real-600w.jpg 600w, '
      '../assets/img/players/sutter-health-park-real-800w.jpg 800w, '
      '../assets/img/players/sutter-health-park-real.jpg 1800w" '
      'sizes="(max-width: 820px) 92vw, 760px"></picture>'
      '<figcaption style="color:var(--muted);font-size:14px;margin-top:10px;font-style:italic">'
      'Sutter Health Park, capacity around fourteen thousand, eight thousand of them filled. '
      'Six baseballs left it on Tuesday and only one belonged to the home team.</figcaption></figure>',

      RAYS_AS_LINE,

      "<b>How fast it was over.</b> One out into the bottom of nothing, Yandy D&iacute;az "
      "singles, Junior Caminero hits his thirty-fifth homer of the season, and it is two-nil "
      "before anybody has found their seat. That is the fifth time in about three weeks that "
      "this team has trailed before it batted. Mason Barnett got four innings and gave up six "
      "runs on five hits, three of which went over the fence, and he walked three and struck "
      "out nobody. Not one strikeout in sixty-seven pitches. His ERA is 6.16 and the shape of "
      "his night is the shape of the whole rotation since the {tolle} at Fenway: the ball is "
      "up, the ball is hard, and the ball keeps landing in the seats.",

      "<b>Taylor Walls.</b> Here is the detail that tells you everything about where this "
      "pitching staff is. Taylor Walls is a good defensive shortstop who came into Tuesday "
      "hitting .216 with no home runs on the season. None. Zero, in a hundred-odd at-bats. He "
      "hit two of them on Tuesday, one off Barnett in the fourth and one off Brady Basso in the "
      "sixth. Eight total bases from a man who had not hit a ball out all year. When a "
      ".216 hitter with nothing in the power column doubles his career damage against your "
      "staff in one evening, that is not variance. That is what a broken pitching staff looks "
      "like from the other dugout.",

      "Then Victor Mesa Jr. hit a two-run shot off Elvis Alvarado in the seventh, and Carson "
      "Williams &mdash; a rookie hitting .108, with no career home runs to his name &mdash; hit "
      "a three-run one off Yunior Tur in the eighth to make it twelve-two. Tur's ERA is now "
      "32.79. I am not going to type anything unkind about a young reliever getting his first "
      "look, but somebody in that organisation should be honest about the fact that they are "
      "running out of arms and the calendar says August.",

      RAYS_AS_HOMERS,

      "<b>Nick Martinez went nine.</b> A hundred and one pitches, eight hits, four runs, five "
      "strikeouts, and not a single walk. Not one. He was still out there in the ninth with a "
      "twelve-four lead because Tampa Bay had no reason to touch a bullpen that did not need "
      "using, and because this lineup gave him no reason to worry. Complete games have gone "
      "nearly extinct in this sport and one just got thrown at the Athletics in a minor league "
      "park by a thirty-five-year-old who used to be a swingman. That is the kind of thing that "
      "happens to teams like this in seasons like this.",

      "<b>What was actually good, because there were three things.</b> Lawrence Butler got hold "
      "of a Martinez pitch in the fourth with Jacob Wilson aboard and hit it to centre for his "
      "eighth home run, and Butler has been buried in a .206 season all year, so take it. "
      "Carlos Cortes doubled home two in the ninth &mdash; his thirteenth double &mdash; which "
      "is the sort of at-bat a lot of players stop taking in a twelve-two game in August in "
      "front of eight thousand people. And Jacob Wilson had a hit, made every play, and "
      "extended his errorless streak at shortstop to a hundred and thirteen consecutive games. "
      "A hundred and thirteen. He {record} at a hundred and eleven on Sunday in Boston and he "
      "has not been charged with one since.",

      "That streak is the single best thing happening in this organisation and almost nobody "
      "in this region has watched a minute of it. It is being set in a fourteen-thousand-seat "
      "Triple-A yard forty minutes up the causeway from a stadium site in Oakland that "
      "ownership walked away from, for a team on its way to {timeline}. The best defensive "
      "season any shortstop has ever put together at this position, and there is no crowd for "
      "it, no local broadcast anybody in the Town is watching, no bar going up when he ranges "
      "into the hole. {legacy} is the whole argument and Jacob Wilson is now Exhibit A for it.",

      "<b>The rest of it.</b> Eight hits, one for three with runners in scoring position, two "
      "double plays grounded into. Henry Bolte made an error and also threw a runner out at "
      "second, which is the most 2026 Athletics sentence I can construct. Jonah Heim went "
      "nought for four. Two hours and twenty-five minutes, which is at least merciful.",

      "Forty-seven and seventy-three. Thirteen and a half games out of a division nobody in "
      "green and gold is thinking about. They won a series in Boston three days ago and it felt "
      "like a small warm thing, and then they came home &mdash; home &mdash; and got outscored "
      "twenty-two to ten in two nights by the best team in the American League East. That is "
      "the season. That has been the season since the middle of June.",

      "There is a game on Wednesday to avoid the sweep. Who is actually available to play it is "
      "on the {depth}, the ballpark they are stuck in until 2028 is in {sutter}, and the anger "
      "about all of it lives in {villains}. The rest is on the {hub}.",
     ],
     links={'tolle': ('athletics-redsox-13-1-tolle-14-strikeouts-ninth-straight-august-7.html',
                      'thirteen-one loss'),
            'record': ('athletics-red-sox-4-3-muncy-chapman-first-series-win-august-9.html',
                       'passed Mike Bordick&rsquo;s major league record'),
            'timeline': ('athletics-oakland-sacramento-las-vegas-timeline.html',
                         'a dome on the Las Vegas Strip in 2028'),
            'legacy': ('oakland-athletics-legacy-what-the-bay-area-lost.html',
                       'What the Bay Area lost'),
            'sutter': ('sutter-health-park-mlb-guide-dimensions-capacity.html',
                       'Sutter Health Park'),
            'depth': ('athletics-2026-roster-depth-chart.html', 'depth chart'),
            'villains': ('athletics-sacramento-bay-area-villains.html', 'Bay Area Villains'),
            'hub': ('../athletics.html', "A's hub")},
     related=[('athletics-red-sox-4-3-muncy-chapman-first-series-win-august-9.html',
               'Athletics', "A's 4, Red Sox 3: Their First Series Win Since June"),
              ('athletics-2026-roster-depth-chart.html', 'Athletics',
               "The A's Roster and Depth Chart"),
              ('sutter-health-park-mlb-guide-dimensions-capacity.html', 'Athletics',
               'Sutter Health Park: MLB in a Triple-A Yard')]),
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
