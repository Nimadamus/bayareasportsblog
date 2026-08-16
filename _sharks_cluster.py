#!/usr/bin/env python3
"""_sharks_cluster.py: the Sharks cluster, built from zero.

One article existed on this franchise before today: sharks-rebuild-has-a-pulse-celebrini,
a 632-word column. The NHL season opens 1 October and the site had nothing to rank with.

Four pages, following the shape that worked for the other clusters: a depth chart, a
season/schedule hub, a player reference page for the one genuinely national story, and a
franchise evergreen. Every number here comes from the 2025-26 season record, the 2026
draft and the July 2026 transaction log.

Deliberately NOT duplicated:
  sharks-rebuild-has-a-pulse-celebrini   the rebuild column, stays the argument; the
      Celebrini page here is the reference (records, contract, where he ranks)
  bay-area-championships-complete-list-by-team   the Sharks' zero is a row on that
      ledger; the history page here explains it

  python _sharks_cluster.py [--check]
"""
import os, re, sys, subprocess
import _college_cluster as CC

ROOT = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------- tables

FORWARDS = """<div class="reftable">
<table>
<caption>Projected forward lines, 2026-27</caption>
<thead><tr><th>Line</th><th>Left wing</th><th>Centre</th><th>Right wing</th></tr></thead>
<tbody>
<tr><td class="num">1</td><td>Igor Chernyshov</td><td>Macklin Celebrini</td><td>Will Smith</td></tr>
<tr><td class="num">2</td><td>Mason Marchment</td><td>Michael Misa</td><td>Tyler Toffoli</td></tr>
<tr><td class="num">3</td><td>Ivar Stenberg</td><td>Alexander Wennberg</td><td>Collin Graf</td></tr>
<tr><td class="num">4</td><td>Kiefer Sherwood</td><td>Zack Ostapchuk</td><td>Adam Gaudette</td></tr>
</tbody>
<tfoot><tr><td colspan="4">Also in the mix: Ty Dellandrea, Barclay Goodrow</td></tr></tfoot>
</table>
</div>"""

DEFENCE = """<div class="reftable">
<table>
<caption>Projected defence pairs and goaltending, 2026-27</caption>
<thead><tr><th>Pair</th><th>Left</th><th>Right</th></tr></thead>
<tbody>
<tr><td class="num">1</td><td>Darnell Nurse</td><td>Jacob Trouba</td></tr>
<tr><td class="num">2</td><td>Sam Dickinson</td><td>Michael Kesselring</td></tr>
<tr><td class="num">3</td><td>Luca Cagnoni</td><td>Dmitry Orlov</td></tr>
<tr><td>Depth</td><td>Nolan Allan</td><td>Eric Pohlkamp</td></tr>
<tr><td>Goal</td><td>Yaroslav Askarov</td><td>Alex Nedeljkovic, Eric Comrie</td></tr>
</tbody>
</table>
</div>"""

SCORING = """<div class="reftable">
<table>
<caption>2025-26 scoring leaders, the baseline this roster is trying to beat</caption>
<thead><tr><th>Player</th><th>GP</th><th>G</th><th>A</th><th>Pts</th><th>Status</th></tr></thead>
<tbody>
<tr><td>Macklin Celebrini</td><td class="num">82</td><td class="num">45</td><td class="num">70</td><td class="num">115</td><td>Signed long-term</td></tr>
<tr><td>Will Smith</td><td class="num">69</td><td class="num">24</td><td class="num">35</td><td class="num">59</td><td>Returns</td></tr>
<tr><td>Alexander Wennberg</td><td class="num">80</td><td class="num">18</td><td class="num">37</td><td class="num">55</td><td>Returns</td></tr>
<tr><td>William Eklund</td><td class="num">78</td><td class="num">15</td><td class="num">38</td><td class="num">53</td><td>Traded to Ottawa</td></tr>
<tr><td>Tyler Toffoli</td><td class="num">79</td><td class="num">19</td><td class="num">30</td><td class="num">49</td><td>Returns</td></tr>
<tr><td>Collin Graf</td><td class="num">81</td><td class="num">21</td><td class="num">25</td><td class="num">46</td><td>Returns</td></tr>
</tbody>
</table>
</div>"""

GOALIES = """<div class="reftable">
<table>
<caption>2025-26 goaltending, the number that decides this season</caption>
<thead><tr><th>Goaltender</th><th>GP</th><th>Record</th><th>GAA</th><th>SV%</th></tr></thead>
<tbody>
<tr><td>Yaroslav Askarov</td><td class="num">47</td><td class="num">21-20-4</td><td class="num">3.63</td><td class="num">.884</td></tr>
<tr><td>Alex Nedeljkovic</td><td class="num">40</td><td class="num">18-14-4</td><td class="num">2.87</td><td class="num">.896</td></tr>
</tbody>
</table>
</div>"""

MOVES = """<div class="reftable">
<table>
<caption>The 2026 offseason, in and out</caption>
<thead><tr><th>Direction</th><th>Player</th><th>Detail</th></tr></thead>
<tbody>
<tr><td>In</td><td>Darnell Nurse, D</td><td>Trade with Edmonton for Shakir Mukhamadullin and Zack Sharp, 1 July</td></tr>
<tr><td>In</td><td>Jacob Trouba, D</td><td>Four-year free agent deal, 1 July</td></tr>
<tr><td>In</td><td>Mason Marchment, F</td><td>Five-year free agent deal</td></tr>
<tr><td>In</td><td>Eric Comrie, G</td><td>Two-year free agent deal</td></tr>
<tr><td>In</td><td>Ivar Stenberg, F</td><td>Second overall pick, 2026 draft</td></tr>
<tr><td>In</td><td>Keaton Verhoeff, D</td><td>Ninth overall pick, acquired from Ottawa</td></tr>
<tr><td>In</td><td>Ryan Lin, D</td><td>21st overall pick, traded up to take him</td></tr>
<tr><td>Out</td><td>William Eklund, F</td><td>To Ottawa with Kasper Halttunen and Brandon Svoboda for the ninth pick</td></tr>
<tr><td>Out</td><td>Mario Ferraro, D</td><td>To Winnipeg</td></tr>
<tr><td>Out</td><td>Vincent Desharnais, D</td><td>To Washington</td></tr>
<tr><td>Out</td><td>Laurent Brossoit, G</td><td>To Anaheim</td></tr>
</tbody>
</table>
</div>"""

OCTOBER = """<div class="reftable">
<table>
<caption>October 2026, game by game</caption>
<thead><tr><th>#</th><th>Date</th><th>Opponent</th><th>Where</th></tr></thead>
<tbody>
<tr><td class="num">1</td><td class="num">Thu 1 Oct</td><td>Florida</td><td>Home</td></tr>
<tr><td class="num">2</td><td class="num">Sat 3 Oct</td><td>Los Angeles</td><td>Home</td></tr>
<tr><td class="num">3</td><td class="num">Mon 5 Oct</td><td>Dallas</td><td>Away</td></tr>
<tr><td class="num">4</td><td class="num">Thu 8 Oct</td><td>St. Louis</td><td>Away</td></tr>
<tr><td class="num">5</td><td class="num">Sat 10 Oct</td><td>Edmonton</td><td>Home</td></tr>
<tr><td class="num">6</td><td class="num">Tue 13 Oct</td><td>Boston</td><td>Home</td></tr>
<tr><td class="num">7</td><td class="num">Thu 15 Oct</td><td>Nashville</td><td>Away</td></tr>
<tr><td class="num">8</td><td class="num">Sat 17 Oct</td><td>Detroit</td><td>Away</td></tr>
<tr><td class="num">9</td><td class="num">Mon 19 Oct</td><td>Toronto</td><td>Away</td></tr>
<tr><td class="num">10</td><td class="num">Tue 20 Oct</td><td>Montreal</td><td>Away</td></tr>
<tr><td class="num">11</td><td class="num">Thu 22 Oct</td><td>Ottawa</td><td>Away</td></tr>
<tr><td class="num">12</td><td class="num">Sat 24 Oct</td><td>Boston</td><td>Away</td></tr>
<tr><td class="num">13</td><td class="num">Tue 27 Oct</td><td>Buffalo</td><td>Home</td></tr>
<tr><td class="num">14</td><td class="num">Thu 29 Oct</td><td>Vancouver</td><td>Home</td></tr>
<tr><td class="num">15</td><td class="num">Sat 31 Oct</td><td>Ottawa</td><td>Home</td></tr>
</tbody>
</table>
</div>"""

SEASONS = """<div class="reftable">
<table>
<caption>The seasons that actually mattered</caption>
<thead><tr><th>Season</th><th>What happened</th></tr></thead>
<tbody>
<tr><td class="num">1991-92</td><td>Expansion season, played at the Cow Palace in Daly City</td></tr>
<tr><td class="num">1992-93</td><td>One of the worst records in NHL history</td></tr>
<tr><td class="num">1993-94</td><td>First playoff berth, and a first-round upset of the heavily favoured Red Wings</td></tr>
<tr><td class="num">2008-09</td><td>Presidents&rsquo; Trophy for the league&rsquo;s best record, out in the first round</td></tr>
<tr><td class="num">2009-10</td><td>Western Conference Final</td></tr>
<tr><td class="num">2010-11</td><td>Western Conference Final again</td></tr>
<tr><td class="num">2015-16</td><td><b>Stanley Cup Final</b>, lost to Pittsburgh in six</td></tr>
<tr><td class="num">2018-19</td><td>Western Conference Final; the Game 7 comeback against Vegas</td></tr>
<tr><td class="num">2019-2025</td><td>Six straight years out of the playoffs, ending in back-to-back last-place finishes</td></tr>
<tr><td class="num">2025-26</td><td>39-35-8, 86 points, a 34-point jump, still no playoffs</td></tr>
</tbody>
</table>
</div>"""

# --------------------------------------------------------------------------- articles

ARTICLES = [

# ------------------------------------------------------------------ 1. Depth chart
dict(slug='sharks-2026-27-roster-depth-chart',
     section='Sharks', tag='Sharks', hub='Sharks',
     title='The Sharks Roster and Depth Chart for 2026-27',
     h1="The Sharks Roster and Depth Chart for 2026-27, Line by Line",
     dek="A 115-point centre, two reclamation projects on the blue line, three first-round "
         "picks, and a save percentage that has to come up. Where this roster actually "
         "stands going into October.",
     desc="The San Jose Sharks 2026-27 roster and depth chart: projected forward lines, "
          "defence pairs, goaltending, and every move made in the 2026 offseason.",
     date='2026-08-08',
     card=('sharks', 'Roster & Depth', 'Celebrini, two rebuilt pairs, and a goaltending question'),
     body=[
      "This is the first Sharks roster in about six years that is worth reading closely, "
      "because for the first time since the rebuild started there is a top line you would "
      "not swap for anybody's and a reason to care about the standings before March. "
      "{pulse} is the column about what that feels like. This is the depth chart.",

      "<b>The top line is the team.</b> Macklin Celebrini put up 115 points last season, "
      "which is more than double what the second-highest scorer on this roster managed, "
      "and the {celebrini} page has the full accounting of what that means. Will Smith on "
      "his right is the other genuine piece. Everything else on this forward group is "
      "either a supporting part or a bet.",

      FORWARDS,

      "<b>The second line is the actual question.</b> Michael Misa is being asked to "
      "centre a scoring line at twenty. Mason Marchment was signed for five years to be "
      "the proven goal-scorer this group did not have, and Tyler Toffoli is the veteran "
      "who has to keep producing at an age where that stops being guaranteed. If that "
      "line works, San Jose has two units that can score and the whole season changes. If "
      "it does not, opponents put their best defenders on Celebrini and the rest of the "
      "lineup goes quiet, which is exactly what happened in stretches last year.",

      "<b>Ivar Stenberg is not a normal rookie.</b> The second overall pick had 33 points "
      "in 43 games in the Swedish Hockey League as an eighteen-year-old and won rookie of "
      "the year doing it. He was widely considered the player in this draft class most "
      "likely to step straight into an NHL lineup, and he is currently projected on the "
      "third line rather than in junior. That is a real thing to watch in October.",

      "<b>The blue line got rebuilt in a single day.</b> On 1 July the Sharks traded for "
      "Darnell Nurse and signed Jacob Trouba, which is two names that used to mean top-"
      "pairing defenceman and now mean something more complicated. Both are on the wrong "
      "side of thirty and both have been criticised for years in bigger markets. San Jose "
      "is betting that a lower-pressure room and a smaller defensive workload gets useful "
      "seasons out of them while the actual future arrives.",

      DEFENCE,

      "<b>The future on defence is the second pair.</b> Sam Dickinson is twenty and "
      "Michael Kesselring is twenty-six, and if those two settle into a real middle "
      "pairing this season it matters more to 2029 than anything Nurse or Trouba does. "
      "Behind them, Keaton Verhoeff went ninth overall and Ryan Lin went 21st, the Sharks "
      "traded up for Lin, so the organisation now has three first-round defencemen in the "
      "system at once.",

      "<b>And then there is the goaltending, which is the whole season.</b>",

      GOALIES,

      "<b>Read that table again.</b> A .884 save percentage from the goaltender the "
      "franchise traded for as its answer in net is not a rebuilding number, it is a "
      "losing number, and Yaroslav Askarov played 47 games behind it. Alex Nedeljkovic "
      "was the better of the two in every category while playing seven fewer games. Eric "
      "Comrie was signed on a two-year deal because the club clearly knows this. A team "
      "that scored enough to finish 39-35-8 with that goaltending is a team that makes the "
      "playoffs with league-average goaltending. That is the entire margin.",

      "<b>What the offence looked like last year.</b> Including the man who is no longer "
      "here, William Eklund was fourth in scoring and was traded to Ottawa as the cost of "
      "moving up for Verhoeff, which tells you how this front office is thinking.",

      SCORING,

      "<b>Where this roster runs out.</b> Behind the top six forwards and the top four "
      "defencemen, it is prospects and depth signings. That is normal for a team at this "
      "stage and it is why an injury to Celebrini would end the season inside two weeks. "
      "The bottom six is functional rather than dangerous, and the fourth line exists to "
      "not lose minutes rather than to win them.",

      "<b>The honest projection.</b> This is a bubble team. Better than last year on "
      "paper, in a Pacific Division that is not the Atlantic, with an elite centre and a "
      "goaltending situation that could swing fifteen points in either direction. The "
      "games are on the {hubpage}, the offseason ledger is below, and {history} is why "
      "nobody around here is getting ahead of themselves.",

      MOVES,

      "The rest of our coverage is on the {hub}.",
     ],
     links={'pulse': ('sharks-rebuild-has-a-pulse-celebrini.html',
                      'The rebuild finally has a pulse'),
            'celebrini': ('macklin-celebrini-sharks-records-contract.html',
                          'Celebrini records and contract'),
            'hubpage': ('sharks-2026-27-schedule-season-hub.html', 'season hub'),
            'history': ('san-jose-sharks-history-no-stanley-cup.html',
                        'thirty-five years without a Cup'),
            'hub': ('../sharks.html', 'Sharks hub')},
     related=[('sharks-2026-27-schedule-season-hub.html', 'Sharks', 'The Sharks 2026-27 Schedule and Season Hub'),
              ('macklin-celebrini-sharks-records-contract.html', 'Sharks', 'Macklin Celebrini: The Records and the Contract'),
              ('san-jose-sharks-history-no-stanley-cup.html', 'Sharks', 'Thirty-Five Years, No Stanley Cup')]),

# ------------------------------------------------------------- 2. Schedule / season hub
dict(slug='sharks-2026-27-schedule-season-hub',
     section='Sharks', tag='Sharks', hub='Sharks',
     title='The Sharks 2026-27 Schedule and Season Hub',
     h1="The Sharks 2026-27 Schedule and Season Hub: Every Game, Kept Updated",
     dek="The schedule landed on 16 July and it opens on 1 October against the Florida "
         "Panthers at SAP Center. This page tracks the season as it happens.",
     desc="The San Jose Sharks 2026-27 season hub: schedule, opening night, the storylines "
          "that decide the year, and links to our coverage as it publishes.",
     date='2026-08-08',
     card=('sharks', '2026-27 Season', 'Opening night, 1 October, SAP Center'),
     body=[
      "This is the page that holds the season together. It gets updated as games are "
      "played and as coverage publishes, so bookmark this one rather than hunting through "
      "the archive.",

      "<b>Opening night.</b> Thursday 1 October 2026, at home at SAP Center, against the "
      "Florida Panthers. The full schedule was released on 16 July. Starting a rebuild "
      "year against one of the hardest teams in the league to play against is either bad "
      "luck or a useful early measurement, and we will know which within sixty minutes.",

      OCTOBER,

      "<b>The first month is harder than it looks.</b> Fifteen games, and eight of them "
      "away, including a six-game eastern trip from 15 to 24 October that runs Nashville, "
      "Detroit, Toronto, Montreal, Ottawa and Boston, with the Toronto and Montreal games "
      "on consecutive nights. A young team can be buried by that trip before American "
      "Thanksgiving, and a good one can announce itself. The Ottawa game on 22 October is "
      "the first look at William Eklund in someone else's sweater after the summer trade "
      "that brought back the ninth overall pick.",

      "<b>And the last one.</b> The regular season finishes at home against Anaheim on 10 "
      "April 2027. If this team is still playing for something that week, the streak the "
      "{history} page describes is about to end.",

      "<b>Where the season is being run from.</b> Ryan Warsofsky is the head coach, Mike "
      "Grier is the general manager, and the building is SAP Center in downtown San Jose, "
      "which, for the record, is the only major professional arena in the Bay Area that "
      "has not moved cities in the last decade. The {moves} page has the rest of that "
      "regional pattern.",

      "<b>What has to be true for this to be a good season.</b> Three things, in order of "
      "how much they matter.",

      "<b>One: the goaltending has to be league-average.</b> Yaroslav Askarov posted a "
      ".884 save percentage across 47 games last season and the team still won 39. There "
      "is no version of a playoff push that starts anywhere other than in the crease, and "
      "the {depth} lays out exactly how big that gap is.",

      "<b>Two: somebody other than Macklin Celebrini has to score.</b> He put up 115 "
      "points and the next man had 59. That is not a supporting cast, that is a solo "
      "album. Michael Misa on the second line and Mason Marchment on a five-year deal are "
      "the two bets designed to fix it. The {celebrini} page has what he did last year in "
      "full.",

      "<b>Three: the young defence has to hold up.</b> Darnell Nurse and Jacob Trouba are "
      "here to absorb hard minutes for two or three years. Sam Dickinson and Michael "
      "Kesselring are here to become the actual pairing. If the veterans crater and the "
      "kids are not ready, this becomes a long winter regardless of what the top line "
      "does.",

      "<b>The realistic target.</b> The Sharks have missed the playoffs seven years "
      "running. Last season they gained 34 points on the year before, one of the biggest "
      "single-season improvements in franchise history, and still finished eleventh in the "
      "West. The gap to a wild card is not enormous any more. A first playoff appearance "
      "since 2019 is genuinely on the table and would be the biggest thing to happen to "
      "this franchise in seven years.",

      "<b>The thing that would make it a bad season.</b> Not losing, this team is allowed "
      "to lose. It would be Celebrini getting hurt, or the goaltending staying where it "
      "is and wasting a year of an elite centre's prime. Development years are cheap. "
      "Wasted years of a player like that are not.",

      "<b>What we will be publishing.</b> Game coverage through the season, roster updates "
      "on the {depth} as moves happen, and updates to the {celebrini} page as the numbers "
      "move. The archive so far is short, {pulse} is the column that started it, and "
      "that changes from October.",

      "<b>Dates worth marking now.</b> Opening night on 1 October against Florida. The "
      "first proper measurement of whether the second line works, which will be obvious by "
      "American Thanksgiving. The trade deadline, where a team on the bubble has to decide "
      "whether it is buying for the first time since 2019. And the end of the season, "
      "where either the streak ends at seven or this page gets a very different tone.",

      "{history} is the long view: thirty-five seasons, one Stanley Cup Final, no Cup. "
      "The rest of our coverage is on the {hub}.",
     ],
     links={'moves': ('bay-area-franchise-relocations-teams-that-left.html',
                      'Bay Area franchise moves'),
            'depth': ('sharks-2026-27-roster-depth-chart.html', 'depth chart page'),
            'celebrini': ('macklin-celebrini-sharks-records-contract.html',
                          'Celebrini records and contract'),
            'pulse': ('sharks-rebuild-has-a-pulse-celebrini.html',
                      'The rebuild finally has a pulse'),
            'history': ('san-jose-sharks-history-no-stanley-cup.html',
                        'The franchise history page'),
            'hub': ('../sharks.html', 'Sharks hub')},
     related=[('sharks-2026-27-roster-depth-chart.html', 'Sharks', 'The Sharks Roster and Depth Chart'),
              ('macklin-celebrini-sharks-records-contract.html', 'Sharks', 'Macklin Celebrini: The Records and the Contract'),
              ('san-jose-sharks-history-no-stanley-cup.html', 'Sharks', 'Thirty-Five Years, No Stanley Cup')]),

# ------------------------------------------------------------------- 3. Celebrini
dict(slug='macklin-celebrini-sharks-records-contract',
     section='Sharks', tag='Sharks', hub='Sharks',
     title='Macklin Celebrini: The Records, the Contract, Where He Ranks',
     h1="Macklin Celebrini: The Franchise Record, the Biggest Contract in Hockey, and Where He Actually Ranks",
     dek="One hundred and fifteen points at twenty, Joe Thornton's franchise record gone, "
         "and an $18.8 million annual salary that is the highest in the National Hockey "
         "League. The numbers, kept updated.",
     desc="Macklin Celebrini by the numbers: the 115-point franchise record season, his "
          "NHL-high $18.8 million contract, and how his start compares.",
     date='2026-08-08',
     card=('sharks', 'Celebrini', "115 points, a franchise record, and hockey's biggest salary"),
     body=[
      "The Bay Area has spent a decade not paying attention to hockey and has therefore "
      "mostly missed the fact that the best young player in the sport is playing in San "
      "Jose. This is the reference page for that. {pulse} is where we get excited about "
      "it.",

      "<b>The season.</b> Eighty-two games, 45 goals, 70 assists, 115 points. That is the "
      "single-season scoring record for this franchise, and the man it took it from is Joe "
      "Thornton, a Hart Trophy winner and the defining Shark of the previous era. "
      "Celebrini got the record in the final game of the regular season, which is a "
      "reasonably cinematic way to do it.",

      "<b>The gap, which is the actually shocking part.</b> The second-highest scorer on "
      "the team had 59 points. Celebrini nearly doubled the output of the next man on his "
      "own roster across a full season. That does not usually happen to good players on "
      "bad teams; it happens to great players on teams that have nothing else, and the "
      "{depth} is the honest accounting of what else there is.",

      "<b>The rate, for people who prefer rates.</b> 3.95 points per sixty minutes, fifth "
      "in the entire league, not fifth among young players, fifth overall, and the "
      "highest figure ever recorded by a player under twenty-one in the analytics era. He "
      "was not compiling on a big minutes load. He was scoring at a rate that belongs to "
      "the best handful of players in the world, at an age where almost nobody is doing "
      "it.",

      "<b>The contract.</b> Five years at $18.8 million per season, the highest annual "
      "salary in the National Hockey League. San Jose paid the number rather than argue "
      "about it, which is the correct decision and also the most encouraging thing this "
      "ownership has done in a decade. A small-market franchise coming off six years of "
      "irrelevance just made the biggest financial commitment in the sport to keep its "
      "own player. That is not a rebuilding move; it is a statement that the rebuild has "
      "a subject.",

      "<b>What it costs them.</b> A lot. That cap number means the roster around him has "
      "to be built cheap, which is exactly why the summer was spent on a trade for a "
      "defenceman with term, a free agent defenceman on the wrong side of thirty, and "
      "three first-round picks rather than a marquee winger. Every dollar decision this "
      "front office makes for the next five years is downstream of this contract.",

      "<b>Where he ranks, honestly.</b> Careful here, because Bay Area sports writing has "
      "a long tradition of getting carried away. He is not yet Connor McDavid and one "
      "115-point season does not make a career. What is true is narrower and still "
      "extraordinary: at twenty he has already produced the best offensive season in the "
      "history of this franchise, at a per-minute rate that ranks with the best players "
      "alive, on a team that finished eleventh in its conference. The list of players who "
      "have done that at that age is short enough to be interesting.",

      "<b>The comparison that actually matters locally.</b> This region has had exactly "
      "one athlete in the last fifteen years who was the best in the world at his "
      "position while playing here, and the {curry} page covers him. Celebrini is not "
      "there. But he is the first person since to make it a reasonable conversation, and "
      "the Sharks are the only franchise in the Bay Area with a player whose ceiling is "
      "that word.",

      "<b>What has to happen next.</b> Two things. He has to do it again, one season is "
      "a season, three is a player. And the club has to put a second scoring line and a "
      "goaltender around him, because 115 points bought 86 standings points and no "
      "playoffs, and there is a version of this where he spends his best years carrying a "
      "team that never quite arrives. The {history} page is thirty-five years of exactly "
      "that happening to this franchise.",

      "<b>How this page gets updated.</b> Every time the franchise record moves, every "
      "time the contract situation changes, and at the end of each season with the full "
      "line. The games themselves are tracked on the {hubpage}.",

      "More on the region he is playing in: the {ledger} has every Bay Area championship, "
      "and the Sharks' entry on it is a zero. The rest of our coverage is on the {hub}.",
     ],
     links={'pulse': ('sharks-rebuild-has-a-pulse-celebrini.html',
                      'The rebuild finally has a pulse'),
            'depth': ('sharks-2026-27-roster-depth-chart.html', 'roster and depth chart'),
            'curry': ('stephen-curry-career-records-three-pointers.html',
                      'Stephen Curry records'),
            'history': ('san-jose-sharks-history-no-stanley-cup.html',
                        'franchise history'),
            'hubpage': ('sharks-2026-27-schedule-season-hub.html', 'season hub'),
            'ledger': ('bay-area-championships-complete-list-by-team.html',
                       'championship ledger'),
            'hub': ('../sharks.html', 'Sharks hub')},
     related=[('sharks-rebuild-has-a-pulse-celebrini.html', 'Sharks', 'The Sharks Rebuild Finally Has a Pulse'),
              ('sharks-2026-27-roster-depth-chart.html', 'Sharks', 'The Sharks Roster and Depth Chart'),
              ('san-jose-sharks-history-no-stanley-cup.html', 'Sharks', 'Thirty-Five Years, No Stanley Cup')]),

# --------------------------------------------------------------- 4. Franchise history
dict(slug='san-jose-sharks-history-no-stanley-cup',
     section='Sharks', tag='Bay Area History', hub='Sharks',
     title='Thirty-Five Years, One Final, No Cup: The Sharks History',
     h1="Thirty-Five Years, One Final, and No Stanley Cup: The San Jose Sharks History",
     dek="An expansion team in a building in Daly City, one of the worst seasons in league "
         "history, two decades of playoff hockey, a Presidents' Trophy, one Final, and "
         "still nothing in the case.",
     desc="The San Jose Sharks franchise history: the 1991 expansion, the 2016 Stanley Cup "
          "Final, the 2019 Game 7 comeback, and why they have never won a Cup.",
     date='2026-08-08',
     card=('sharks', 'The Sharks', 'Thirty-five years, one Final, no Cup'),
     body=[
      "On the {ledger}, every championship this region has won, twenty-one of them across "
      "six franchises, there is one line with a zero on it, and this is the page that "
      "explains it. It is not a story about a bad franchise. That is what makes it hurt.",

      "<b>Where they came from.</b> The NHL awarded San Jose an expansion team for 1991 to "
      "Gordon and George Gund, who had previously owned the California Seals, so Bay Area "
      "hockey came back to a region that had already lost a team once. The first two "
      "seasons were played at the Cow Palace in Daly City, which is not San Jose and was "
      "not new in 1991, while the arena downtown was built.",

      "<b>The beginning was genuinely terrible.</b> The 1992-93 season produced one of the "
      "worst records in the history of the National Hockey League. Then in 1993-94 they "
      "moved into the new building, made the playoffs for the first time, and knocked out "
      "a Detroit team that was supposed to win the whole thing. Two years, from historic "
      "embarrassment to the biggest upset of the postseason. It was the first sign that "
      "this franchise was going to do everything the difficult way.",

      SEASONS,

      "<b>The long good era, which is the actual tragedy.</b> From 2004 to 2019 the Sharks "
      "made the playoffs in all but one season. That is a fifteen-year run of relevance "
      "that most franchises never have. They won a Presidents' Trophy in 2009 for the best "
      "record in the league and lost in the first round. They reached back-to-back Western "
      "Conference Finals in 2010 and 2011. Joe Thornton and Patrick Marleau played most of "
      "their careers here and are two of the better players of their generation, and "
      "neither of them ever lifted a Cup in teal.",

      "<b>2016, the one time it was actually there.</b> The Sharks reached the Stanley Cup "
      "Final for the only time in franchise history and lost to Pittsburgh in six games. "
      "Not swept, not embarrassed, beaten by a better team in a series that was closer "
      "than the scoreline. It is the high-water mark and it is now a decade old.",

      "<b>2019, the greatest thing that ever happened in that building.</b> Game 7 against "
      "Vegas, the Sharks four goals down in the third period, a five-minute major called, "
      "and then five goals in barely four minutes on the same power play. SAP Center has "
      "never been louder and probably never will be. They won it in overtime, went to the "
      "Conference Final, lost, and then the franchise fell off a cliff for six years. "
      "That is a fairly complete summary of what it is like to support this team.",

      "<b>Then the collapse.</b> Six straight seasons out of the playoffs, ending with "
      "back-to-back finishes at the bottom of the league. Thornton and Marleau left. The "
      "building emptied out. In a region that had the Warriors winning championships and "
      "the Giants and 49ers taking up all the oxygen, a bad hockey team in San Jose became "
      "genuinely invisible, which is how a market with a real hockey audience ended up "
      "with almost nobody paying attention.",

      "<b>Why they have never won, honestly.</b> There is no curse and there is no single "
      "villain. There is a long stretch of very good regular-season teams that ran into "
      "either a hotter goaltender or a deeper opponent, a 2016 team that got to the last "
      "round and met a Pittsburgh side at its peak, and a front office that kept the "
      "window open a year or two longer than it should have. Being consistently good and "
      "never great is a specific kind of failure and this franchise is the league's "
      "clearest example of it.",

      "<b>Where it stands now.</b> Better than it has in years. Last season produced 86 "
      "points and a 34-point improvement, one of the biggest year-over-year jumps in club "
      "history, and it still was not enough for a playoff spot, seven straight years out "
      "now. But there is a twenty-year-old centre who just broke Thornton's franchise "
      "scoring record and signed the largest contract in the sport, and that is a "
      "different kind of starting point than the last rebuild had. {celebrini} is the "
      "reference page on him and the {depth} is what is around him.",

      "<b>What it would mean.</b> The A's are leaving, the Raiders are gone, the Warriors "
      "moved across the bay and the Giants are rebuilding. San Jose has held onto its team "
      "for thirty-five years without ever threatening to move it and without ever winning "
      "anything. A Stanley Cup in that building would be the single best sports story this "
      "region could produce, precisely because nobody outside of it is expecting one. The "
      "{hubpage} tracks the attempt.",

      "The rest of our coverage is on the {hub}, and the regional context is on the "
      "{ledger} and the {moves} page.",
     ],
     links={'ledger': ('bay-area-championships-complete-list-by-team.html',
                       'Bay Area championship ledger'),
            'celebrini': ('macklin-celebrini-sharks-records-contract.html',
                          'Macklin Celebrini'),
            'depth': ('sharks-2026-27-roster-depth-chart.html', 'depth chart'),
            'hubpage': ('sharks-2026-27-schedule-season-hub.html', 'season hub'),
            'moves': ('bay-area-franchise-relocations-teams-that-left.html',
                      'franchise relocations'),
            'hub': ('../sharks.html', 'Sharks hub')},
     related=[('bay-area-championships-complete-list-by-team.html', 'Bay Area History', 'Every Bay Area Championship'),
              ('macklin-celebrini-sharks-records-contract.html', 'Sharks', 'Macklin Celebrini: The Records and the Contract'),
              ('sharks-2026-27-roster-depth-chart.html', 'Sharks', 'The Sharks Roster and Depth Chart')]),
]


def main():
    check = '--check' in sys.argv
    for a in ARTICLES:
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
