#!/usr/bin/env python3
"""_history_cluster.py: the Bay Area history / evergreen cluster.

The archive already owns the *columns*: all four dynasty eras, The Catch, Bumgarner
2014, Klay's 37, Bonds, Kent, Bochy's bullpen, Montana-Young, the 1993 pennant race,
the Big Game, the Axe, Oracle Park, Sutter Health Park and the A's relocation.

What it does not own is a *reference*. bay-area-sports-history is a column, it argues.
These four pages answer questions with tables and dates, which is what gets cited and
linked. Deliberately NOT duplicated:

  bay-area-sports-history          the regional argument column, stays the argument
  dynasties.html / timeline.html   the hub framing, these are the supporting articles
  oakland-athletics-legacy-*       the A's grief piece, the Coliseum page here is the
                                   building, not the franchise
  flashback-the-catch-1982         the moment, the Candlestick page here is the venue
  athletics-oakland-sacramento-*   the A's move specifically, the relocations page here
                                   is the regional pattern, and links down to it

  python _history_cluster.py [--check]
"""
import os, re, sys, subprocess
import _college_cluster as CC

ROOT = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------- tables

TITLE_TABLE = """<div class="reftable">
<table>
<caption>Bay Area major-league championships, by franchise</caption>
<thead><tr><th>Franchise</th><th>League</th><th>Bay Area era</th><th>Titles</th><th>Years</th></tr></thead>
<tbody>
<tr><td>San Francisco 49ers</td><td>NFL</td><td class="num">1946, </td><td class="num">5</td><td class="num">1981, 1984, 1988, 1989, 1994</td></tr>
<tr><td>Golden State Warriors</td><td>NBA</td><td class="num">1962, </td><td class="num">5</td><td class="num">1975, 2015, 2017, 2018, 2022</td></tr>
<tr><td>Oakland Athletics</td><td>MLB</td><td class="num">1968-2024</td><td class="num">4</td><td class="num">1972, 1973, 1974, 1989</td></tr>
<tr><td>San Francisco Giants</td><td>MLB</td><td class="num">1958, </td><td class="num">3</td><td class="num">2010, 2012, 2014</td></tr>
<tr><td>Oakland Raiders</td><td>NFL</td><td class="num">1960-81, 1995-2019</td><td class="num">2</td><td class="num">1976, 1980</td></tr>
<tr><td>San Jose Earthquakes</td><td>MLS</td><td class="num">1996-2005, 2008, </td><td class="num">2</td><td class="num">2001, 2003</td></tr>
<tr><td>San Jose Sharks</td><td>NHL</td><td class="num">1991, </td><td class="num">0</td><td>, </td></tr>
<tr><td>Golden State Valkyries</td><td>WNBA</td><td class="num">2025, </td><td class="num">0</td><td>, </td></tr>
</tbody>
<tfoot><tr><td colspan="3">Total, Bay Area era</td><td class="num">21</td><td>, </td></tr></tfoot>
</table>
</div>"""

DECADE_TABLE = """<div class="reftable">
<table>
<caption>The same 21 titles, by decade</caption>
<thead><tr><th>Decade</th><th>Titles</th><th>Who won them</th></tr></thead>
<tbody>
<tr><td class="num">1960s</td><td class="num">0</td><td>The Raiders won the 1967 AFL Championship and lost Super Bowl II</td></tr>
<tr><td class="num">1970s</td><td class="num">5</td><td>Athletics 1972, 1973, 1974; Warriors 1975; Raiders 1976</td></tr>
<tr><td class="num">1980s</td><td class="num">6</td><td>Raiders 1980; 49ers 1981, 1984, 1988, 1989; Athletics 1989</td></tr>
<tr><td class="num">1990s</td><td class="num">1</td><td>49ers 1994</td></tr>
<tr><td class="num">2000s</td><td class="num">2</td><td>Earthquakes 2001, 2003</td></tr>
<tr><td class="num">2010s</td><td class="num">6</td><td>Giants 2010, 2012, 2014; Warriors 2015, 2017, 2018</td></tr>
<tr><td class="num">2020s</td><td class="num">1</td><td>Warriors 2022</td></tr>
</tbody>
</table>
</div>"""

ELSEWHERE_TABLE = """<div class="reftable">
<table>
<caption>Titles these franchises won somewhere else, not Bay Area championships</caption>
<thead><tr><th>Franchise</th><th>Won as</th><th>Titles</th><th>Years</th></tr></thead>
<tbody>
<tr><td>Giants</td><td>New York Giants</td><td class="num">5</td><td class="num">1905, 1921, 1922, 1933, 1954</td></tr>
<tr><td>Athletics</td><td>Philadelphia Athletics</td><td class="num">5</td><td class="num">1910, 1911, 1913, 1929, 1930</td></tr>
<tr><td>Warriors</td><td>Philadelphia Warriors</td><td class="num">2</td><td class="num">1947, 1956</td></tr>
<tr><td>Raiders</td><td>Los Angeles Raiders</td><td class="num">1</td><td class="num">1983</td></tr>
</tbody>
<tfoot><tr><td colspan="2">Total won elsewhere</td><td class="num">13</td><td>, </td></tr></tfoot>
</table>
</div>"""

MOVES_TABLE = """<div class="reftable">
<table>
<caption>Every completed move into, out of, or inside the Bay Area</caption>
<thead><tr><th>Year</th><th>Franchise</th><th>Move</th><th>Kind</th></tr></thead>
<tbody>
<tr><td class="num">1958</td><td>Giants</td><td>New York to San Francisco</td><td>arrival</td></tr>
<tr><td class="num">1962</td><td>Warriors</td><td>Philadelphia to San Francisco</td><td>arrival</td></tr>
<tr><td class="num">1968</td><td>Athletics</td><td>Kansas City to Oakland</td><td>arrival</td></tr>
<tr><td class="num">1971</td><td>Warriors</td><td>San Francisco to Oakland, renamed Golden State</td><td>internal</td></tr>
<tr><td class="num">1982</td><td>Raiders</td><td>Oakland to Los Angeles</td><td>departure</td></tr>
<tr><td class="num">1995</td><td>Raiders</td><td>Los Angeles back to Oakland</td><td>return</td></tr>
<tr><td class="num">2006</td><td>Earthquakes</td><td>San Jose to Houston, became the Dynamo</td><td>departure</td></tr>
<tr><td class="num">2008</td><td>Earthquakes</td><td>expansion club returns to San Jose</td><td>return</td></tr>
<tr><td class="num">2014</td><td>49ers</td><td>San Francisco to Santa Clara, kept the name</td><td>internal</td></tr>
<tr><td class="num">2019</td><td>Warriors</td><td>Oakland to San Francisco, Chase Center</td><td>internal</td></tr>
<tr><td class="num">2020</td><td>Raiders</td><td>Oakland to Las Vegas</td><td>departure</td></tr>
<tr><td class="num">2025</td><td>Athletics</td><td>Oakland to West Sacramento, temporarily</td><td>departure</td></tr>
<tr><td class="num">2028</td><td>Athletics</td><td>West Sacramento to Las Vegas, scheduled</td><td>departure</td></tr>
</tbody>
</table>
</div>"""

ARENA_NAMES = """<div class="reftable">
<table>
<caption>One building, four names</caption>
<thead><tr><th>Years</th><th>Name</th><th>What it was</th></tr></thead>
<tbody>
<tr><td class="num">1966-1996</td><td>Oakland, Alameda County Coliseum Arena</td><td>The round building next to the stadium</td></tr>
<tr><td class="num">1997-2005</td><td>The Arena in Oakland</td><td>Reopened after a rebuild of more than $121 million</td></tr>
<tr><td class="num">2006-2019</td><td>Oracle Arena</td><td>Roaracle; three championships</td></tr>
<tr><td class="num">2019, </td><td>Oakland Arena</td><td>A concert building with no team</td></tr>
</tbody>
</table>
</div>"""

NEARMISS_TABLE = """<div class="reftable">
<table>
<caption>Moves that were agreed, filed or announced and did not happen</caption>
<thead><tr><th>Year</th><th>Franchise</th><th>Where it nearly went</th><th>What stopped it</th></tr></thead>
<tbody>
<tr><td class="num">1976</td><td>Giants</td><td>Toronto</td><td>A city injunction bought time; Bob Lurie bought the club and kept it</td></tr>
<tr><td class="num">1992</td><td>Giants</td><td>St. Petersburg, Florida</td><td>National League owners voted the sale down; a local group bought in</td></tr>
<tr><td class="num">2006-09</td><td>Athletics</td><td>Fremont</td><td>The Cisco Field plan collapsed under local opposition</td></tr>
<tr><td class="num">2009-15</td><td>Athletics</td><td>San Jose</td><td>The Giants would not give up territorial rights; the courts backed baseball</td></tr>
<tr><td class="num">2018-23</td><td>Athletics</td><td>Howard Terminal, Oakland</td><td>Never financed or approved; the franchise chose Las Vegas instead</td></tr>
</tbody>
</table>
</div>"""

# --------------------------------------------------------------------------- articles

ARTICLES = [

# ------------------------------------------------------------- 1. Championship ledger
dict(slug='bay-area-championships-complete-list-by-team',
     section='Bay Area Sports', tag='Bay Area History', hub='Bay Area Sports',
     title='Every Bay Area Championship: The Complete List, Team by Team',
     h1="Every Championship the Bay Area Has Won, Team by Team and Decade by Decade",
     dek="Twenty-one titles across six franchises and five leagues, with the years, the "
         "decades, and an honest accounting of the ones that do not count. The reference "
         "page, not the argument.",
     desc="A complete reference list of Bay Area championships: 49ers, Warriors, "
          "Athletics, Giants, Raiders, Earthquakes and Sharks, with every title year.",
     date='2026-08-08',
     card=('bay', 'The Championship Ledger', 'Twenty-one titles, six franchises, five leagues'),
     body=[
      "Somebody asks this at a bar roughly once a month and nobody in the room ever has "
      "the whole answer. This page is the whole answer. It is a ledger, not a column, "
      "{regional} is where we make the case for the region. Here we just count.",

      "<b>The rule this page uses.</b> A championship counts if the franchise won it "
      "while based in the Bay Area. That excludes the five World Series the Giants won "
      "in New York, the five the Athletics won in Philadelphia, the two the Warriors won "
      "in Philadelphia, and the Super Bowl the Raiders won in Los Angeles. Those are real "
      "titles and they belong to those franchises; they are not things that happened "
      "here. Football and soccer titles are listed by season, so the 49ers' 1981 title "
      "is the Super Bowl played in January 1982.",

      TITLE_TABLE,

      "<b>Twenty-one.</b> Six Bay Area franchises have won something; two have not. Five "
      "different leagues are represented. For a single metropolitan area that is an "
      "absurd number, and it is the reason this region gets talked about the way it does.",

      "<b>Now look at when they happened.</b> This is the part people get wrong, because "
      "the titles are not spread out. They come in clusters, and between the clusters "
      "there are stretches where nothing happens at all.",

      DECADE_TABLE,

      "<b>Two golden ages, one dead zone, one modern boom.</b> The seventies and eighties "
      "produced eleven of the twenty-one, {ninersdyn} overlapping with {athletics} and a "
      "Warriors team nobody expected. Then the nineties produced exactly one and the "
      "2000s produced two, both of them soccer. Then the 2010s produced six in nine "
      "years, split between {giantsdyn} and {warriorsdyn}, which is why anyone who grew "
      "up here between 2010 and 2018 has a completely distorted idea of how often this is "
      "supposed to happen.",

      "<b>The 2020s are the problem.</b> One title in six-plus years, and it is the 2022 "
      "Warriors. Since then: a Giants rebuild that has not produced a contender, an "
      "Athletics franchise that has physically left, a 49ers team that keeps reaching "
      "Super Bowls and losing them, and a Sharks side that has never won anything. The "
      "region is in one of its dead zones and it is worth saying that out loud rather "
      "than living off 2015.",

      "<b>The near misses, which are their own list.</b> The 49ers have lost three Super "
      "Bowls since 2012 and each one was inside a possession late. The Giants lost the "
      "2002 World Series after leading Game 6 by five runs in the seventh. The Warriors "
      "blew a 3-1 lead in 2016 with the {record73} behind them. The Sharks reached the "
      "Stanley Cup Final in 2016 and lost it. The Athletics won three straight pennants "
      "into 1990 and were swept by Cincinnati. Twenty-one is the number in the ledger; "
      "the number of times this region got to the last round is meaningfully higher, and "
      "so is the accumulated damage.",

      "<b>What the franchises won before they got here.</b> Included for completeness, "
      "because it is the single most common source of confusion in any argument about "
      "this. When somebody says the Giants have eight World Series or the A's have nine, "
      "this is where the rest of them are.",

      ELSEWHERE_TABLE,

      "<b>So the honest phrasing is:</b> the Giants are a nine-title franchise with three "
      "titles in San Francisco. The Athletics are a nine-title franchise with four in "
      "Oakland. The Warriors are a seven-title franchise with five in the Bay Area. The "
      "Raiders won three Super Bowls, two of them in Oakland. Use whichever number you "
      "like, but say which one you are using.",

      "<b>Zero, twice.</b> The {sharks} have never won a Stanley Cup in thirty-five "
      "seasons, and the Valkyries have existed since 2025. One of those is a wound and "
      "the other is a franchise that has not had time yet.",

      "<b>And one that left with its titles.</b> Four of the twenty-one belong to a "
      "franchise that no longer plays here. The Athletics won three consecutive World "
      "Series in the early seventies and another in 1989, and in 2028 those banners are "
      "scheduled to hang in Nevada. {legacy} is the record of what that means. The "
      "Raiders took two more with them in 2020. Nearly a third of everything on this page "
      "was won by teams that are gone.",

      "The individual eras are covered properly elsewhere: {ninersdyn}, {warriorsdyn}, "
      "{giantsdyn}, and the {timeline2} lays the whole thing out chronologically. The "
      "{hub} has the rest.",
     ],
     links={'regional': ('bay-area-sports-history.html',
                         'Why the Bay Area is one of the great sports regions'),
            'ninersdyn': ('49ers-dynasty-team-of-the-decade.html', "the 49ers dynasty"),
            'warriorsdyn': ('warriors-championship-history.html',
                            "the Warriors' championship run"),
            'giantsdyn': ('giants-dynasty-even-year-magic.html', "the Giants' even-year run"),
            'athletics': ("oakland-athletics-legacy-what-the-bay-area-lost.html",
                          "the Oakland A's"),
            'record73': ('warriors-73-9-best-record-ever-added-durant.html',
                         'best regular season in NBA history'),
            'sharks': ('san-jose-sharks-history-no-stanley-cup.html', 'Sharks'),
            'legacy': ('oakland-athletics-legacy-what-the-bay-area-lost.html',
                       'What the Bay Area lost'),
            'timeline2': ('../timeline.html', 'Bay Area sports timeline'),
            'hub': ('../history.html', 'history section')},
     related=[('bay-area-sports-history.html', 'Bay Area Sports', 'Why the Bay Area Is One of the Greatest Sports Regions'),
              ('bay-area-franchise-relocations-teams-that-left.html', 'Bay Area History', 'Every Bay Area Franchise Move'),
              ('oakland-coliseum-history-what-happens-to-it-now.html', 'Bay Area History', 'The Oakland Coliseum: What Happens to It Now')]),

# ------------------------------------------------------------------- 2. The Coliseum
dict(slug='oakland-coliseum-history-what-happens-to-it-now',
     section='Bay Area Sports', tag='Bay Area History', hub='Bay Area Sports',
     title='The Oakland Coliseum: What It Was and What Happens to It Now',
     h1="The Oakland Coliseum: What It Was, What Ruined It, and What Happens to It Now",
     dek="Opened in 1966 for $25.5 million, home to two championship franchises, wrecked "
         "by a 1996 renovation nobody wanted, and now the middle of a $5 billion "
         "redevelopment. The building, not the grievance.",
     desc="The Oakland Coliseum explained: the 1966 opening, the Raiders and A's years, "
          "the Mount Davis renovation, the final MLB game, and the redevelopment now.",
     date='2026-08-08',
     card=('athletics', 'The Coliseum', 'A concrete bowl, two dynasties, and 112 acres'),
     body=[
      "Every story about the Athletics leaving mentions this building and almost none of "
      "them explain it. So: what the Coliseum actually was, how it went from one of the "
      "better stadiums in America to a national punchline, and what is happening to the "
      "site right now, which is more interesting than most people realise.",

      "<b>What was built.</b> The Oakland-Alameda County Coliseum opened on 18 September "
      "1966 at a cost of $25.5 million, part of a 120-acre complex that also included the "
      "arena next door. The design was the good idea of its era: a symmetrical concrete "
      "bowl sunk into the ground so that most of the seating sat below street level, "
      "which kept the profile low and left the view open to the Oakland hills beyond the "
      "outfield. It was not a beautiful building. It was a genuinely well-sited one.",

      "<b>Who played in it.</b> The Raiders from 1966 to 1981 and again from 1995 to "
      "2019. The Athletics from 1968 to 2024. The Warriors were next door at {arena} "
      "from 1971 until they crossed the bay in 2019. For a stretch in the seventies and "
      "eighties this parking lot held three professional franchises, and it is the place "
      "where more than half of everything on the {ledger} was won.",

      "<b>What happened there.</b> Three consecutive World Series championships in the "
      "early seventies. Two Raiders Super Bowl teams. The Bash Brothers. The twenty-game "
      "winning streak in 2002. The 1989 World Series, which the A's won in a series "
      "interrupted by an earthquake. The right-field bleachers, the drums, the flags, a "
      "supporter culture that visiting teams genuinely disliked playing in front of.",

      "<b>Then 1996, which is the part that actually killed it.</b> To bring the Raiders "
      "back from Los Angeles, the public paid roughly $200 million to bolt an enormous "
      "upper deck onto the east side of the stadium. It added football seats. It also "
      "walled off the view of the hills that was the single best feature of the original "
      "design, put thousands of baseball seats at a distance and an angle nobody wanted "
      "to sit at, and turned an open bowl into a closed concrete box. Fans named it Mount "
      "Davis, and for the entire baseball season afterwards it sat under tarps, a "
      "monument, tarped, to a decision made for a football team that left again anyway.",

      "<b>The decay was a policy, not an accident.</b> The sewage backups that made "
      "national news, most notoriously when it flooded the clubhouses in 2013. The "
      "possums. The tarps over the upper deck. All of it was real and all of it was the "
      "predictable end state of a building that two governments and one ownership group "
      "spent twenty years refusing to invest in while they argued about a replacement. "
      "Stadiums do not rot on their own. This one was left to.",

      "<b>What it was, uniquely, at the end.</b> The last stadium in America shared "
      "full-time by a Major League Baseball team and an NFL team. Everywhere else that "
      "arrangement ended in the nineties and 2000s, because it is a bad arrangement: the "
      "dirt infield sits in the middle of the football field in September, and neither "
      "sport gets the building it wants. Oakland kept it going until 2019 because Oakland "
      "could not afford to stop.",

      "<b>The last game.</b> 26 September 2024. The Athletics beat the Texas Rangers 3-2 "
      "in front of 46,889 people, which is close to a sellout and roughly five times what "
      "the franchise had been drawing. Fifty-seven seasons ended in a building that was "
      "full for the first time in years, which tells you something that the attendance "
      "argument never did. The rest of that story is on the {timeline} and the {legacy}.",

      "<b>What is there now.</b> Not nothing. Oakland Roots SC and Oakland Soul SC play "
      "there, and the San Francisco Unicorns have used it for cricket. The concrete bowl "
      "that a major league franchise called inadequate is currently hosting professional "
      "sport in front of crowds that fill the lower deck.",

      "<b>The sale, which is genuinely happening.</b> The city and the county each owned "
      "half through the Coliseum Authority. Both halves are going to Oakland Acquisition "
      "Co., an entity formed by the African American Sports and Entertainment Group with "
      "financing from Loop Capital, after the Athletics assigned their own purchase right "
      "to the group in 2025. The City Council approved amended terms on 13 July 2026, "
      "including a provision that gives Oakland 6 per cent of annual gross ticket sales "
      "from events at the complex, the city estimates roughly $3 million a year into the "
      "general fund.",

      "<b>What they intend to build.</b> More than $5 billion across the full 112 acres "
      "over something like thirty years: housing in the thousands of units, with about a "
      "quarter of it deed-restricted affordable, plus retail, restaurants and "
      "entertainment space. Thirty-year masterplans in the Bay Area have a poor record, "
      "{candlestick} sat empty for a decade after demolition, so the correct posture is "
      "interested scepticism rather than either cynicism or excitement.",

      "<b>The thing worth holding onto.</b> A stadium is not the reason a city loses a "
      "team. Oakland was told for twenty years that this building was the problem, and "
      "the building is still standing, still hosting sport, and about to become the "
      "largest redevelopment site in the East Bay. The team is the thing that left. "
      "{villains} is where we say what we think about that.",

      "More on the era this building held: {ledger}, the {timeline}, and the {hub}.",
     ],
     links={'ledger': ('bay-area-championships-complete-list-by-team.html',
                       'Bay Area championship ledger'),
            'arena': ('oracle-arena-roaracle-history-oakland-warriors.html',
                      'the arena'),
            'timeline': ('athletics-oakland-sacramento-las-vegas-timeline.html',
                         'relocation timeline'),
            'legacy': ('oakland-athletics-legacy-what-the-bay-area-lost.html',
                       'record of what was lost'),
            'candlestick': ('candlestick-park-history-wind-the-catch-demolition.html',
                            'Candlestick Park'),
            'villains': ('athletics-sacramento-bay-area-villains.html', 'Our column on the move'),
            'hub': ('../history.html', 'history section')},
     related=[('bay-area-franchise-relocations-teams-that-left.html', 'Bay Area History', 'Every Bay Area Franchise Move'),
              ('oakland-athletics-legacy-what-the-bay-area-lost.html', 'Athletics', "What the Bay Area Lost When the A's Left"),
              ('candlestick-park-history-wind-the-catch-demolition.html', 'Bay Area History', 'Candlestick Park: The Wind and The Catch')]),

# ------------------------------------------------------------------- 3. Relocations
dict(slug='bay-area-franchise-relocations-teams-that-left',
     section='Bay Area Sports', tag='Bay Area History', hub='Bay Area Sports',
     title='Every Bay Area Franchise Move: The Teams That Left and Nearly Left',
     h1="Every Bay Area Franchise Move: Who Arrived, Who Left, and Who Nearly Did",
     dek="Thirteen completed moves, five that were agreed and then stopped, and a "
         "regional pattern nobody has written down in one place: this is a market that "
         "keeps almost losing teams, and lately keeps actually losing them.",
     desc="A reference list of every Bay Area sports franchise relocation: the Raiders "
          "twice, the Athletics, the Warriors, the 49ers, and the moves that were blocked.",
     date='2026-08-08',
     card=('bay', 'The Moves', 'Thirteen relocations and five that were stopped'),
     body=[
      "The Athletics leaving got treated nationally as a one-off. It is not a one-off. "
      "This region has been losing, nearly losing, and internally shuffling franchises "
      "for seventy years, and the pattern only becomes visible when you put every move on "
      "one page. So here is every move.",

      MOVES_TABLE,

      "<b>Read the Kind column.</b> Four arrivals, all of them between 1958 and 1968, "
      "when the Bay Area went from having no major league team to having five in a "
      "decade. Then thirty years of nothing. Then a run of departures and internal moves "
      "that is still going.",

      "<b>The Raiders, twice, which is the defining case.</b> Al Davis moved the club to "
      "Los Angeles for the 1982 season after a legal fight with the NFL that changed how "
      "American sports leagues can restrict relocation. They came back in 1995 to a deal "
      "that included the $200 million upper deck at the {coliseum}, public money, spent "
      "on a stadium modification, to bring back a team that had already left once. In "
      "2017 the league approved a move to Las Vegas and the franchise left again in 2020. "
      "Oakland paid off debt on that renovation for years after the team it was built for "
      "had gone. If you want to understand why the East Bay reacts to relocation talk the "
      "way it does, it is this: they have done this before, they paid for it, and it "
      "happened anyway.",

      "<b>The Athletics, which is the current one.</b> Arrived from Kansas City in 1968, "
      "spent fifty-seven seasons in Oakland, and are now playing in a Triple-A park in "
      "West Sacramento while a domed stadium goes up on the Las Vegas Strip. The full "
      "sequence, with construction milestones, is on the {astimeline}, and {sutter} is "
      "the interim ballpark explained.",

      "<b>The internal moves, which people forget count.</b> The Warriors have played in "
      "San Francisco, then Oakland, then San Francisco again, and the 2019 move to Chase "
      "Center took a franchise out of the building where it won three championships in "
      "front of an Oakland crowd, and put it in a more expensive arena across the bay. "
      "The 49ers left San Francisco entirely in 2014 for Santa Clara, roughly forty miles "
      "south, and kept the city's name on the jersey. Neither one shows up on a list of "
      "franchises that abandoned a region, and both of them moved a team away from the "
      "people who filled the old building.",

      "<b>Now the ones that did not happen.</b> This is the list that actually makes the "
      "point, because in two separate decades the Giants had a signed deal to leave and "
      "in both cases something outside the franchise stopped it.",

      NEARMISS_TABLE,

      "<b>1976.</b> Horace Stoneham, the man who had already moved this franchise once, "
      "from New York in 1958, agreed to sell to a Toronto group backed by Labatt. The "
      "Giants were going to be a Canadian team a year before the Blue Jays existed. San "
      "Francisco went to court for an injunction, the delay held long enough for Bob "
      "Lurie to put a local purchase together, and the franchise stayed. That is how "
      "close it was.",

      "<b>1992.</b> Lurie himself agreed to sell to investors who intended to move the "
      "club to the Suncoast Dome in St. Petersburg. National League owners voted the sale "
      "down and a local group led by Peter Magowan bought instead. Everything that "
      "followed, {bonds}, {kent}, {bochy}, {evenyear}, three World Series, happens "
      "because of a vote in a room the Giants did not control. That whole era, including "
      "the {pennant93} the very next season, exists on a coin flip.",

      "<b>The A's near-misses are the mirror image.</b> Fremont collapsed. San Jose was "
      "blocked because the Giants hold territorial rights over Santa Clara County and "
      "would not release them; San Jose sued Major League Baseball over it and the courts "
      "sided with baseball's antitrust exemption in 2015. Howard Terminal was announced "
      "in 2018 and never financed. The franchise spent seventeen years failing to move "
      "eleven miles and then moved five hundred.",

      "<b>The pattern, stated plainly.</b> Bay Area franchises do not leave because the "
      "Bay Area will not support them, the arrivals in the sixties, the crowds in the "
      "seventies and eighties, and the sellout at the {coliseum} in September 2024 all "
      "say otherwise. They leave because this is an expensive, politically fragmented "
      "region where getting a stadium built requires agreement between a city, a county, "
      "an ownership group and often a second city forty miles away, and that agreement "
      "keeps failing. Two of those failures were rescued by outsiders. The rest were not.",

      "<b>What is still exposed.</b> The Athletics are scheduled to be gone by 2028. The "
      "{raiders} are already in Nevada. Levi's Stadium is a Santa Clara asset and the "
      "49ers' relationship with that city has been openly hostile at points. The Sharks "
      "play in a city-owned arena in San Jose on a lease that will eventually need "
      "renegotiating. Nobody should assume the list above is finished.",

      "The buildings themselves are covered on the {coliseum} page and the {candlestick} "
      "page; the count of what was won before all this is on the {ledger}. The {hub} has "
      "the rest.",
     ],
     links={'coliseum': ('oakland-coliseum-history-what-happens-to-it-now.html',
                         'Coliseum'),
            'astimeline': ('athletics-oakland-sacramento-las-vegas-timeline.html',
                           "A's relocation timeline"),
            'sutter': ('sutter-health-park-mlb-guide-dimensions-capacity.html',
                       'Sutter Health Park'),
            'bonds': ('barry-bonds-giants-home-run-king.html', 'Bonds'),
            'kent': ('jeff-kent-giants-mvp-second-baseman.html', 'Kent'),
            'bochy': ('bruce-bochy-bullpen-wizardry-core-four.html', "Bochy's bullpens"),
            'evenyear': ('giants-dynasty-even-year-magic.html', 'the even-year dynasty'),
            'pennant93': ('giants-1993-pennant-race-braves-103-wins-wild-card.html',
                          '1993 pennant race'),
            'raiders': ('raiders-2026-season-preview-kubiak-cousins-mendoza-jeanty.html',
                        'Raiders'),
            'candlestick': ('candlestick-park-history-wind-the-catch-demolition.html',
                            'Candlestick'),
            'ledger': ('bay-area-championships-complete-list-by-team.html',
                       'championship ledger'),
            'hub': ('../history.html', 'history section')},
     related=[('oakland-coliseum-history-what-happens-to-it-now.html', 'Bay Area History', 'The Oakland Coliseum: What Happens to It Now'),
              ('bay-area-championships-complete-list-by-team.html', 'Bay Area History', 'Every Bay Area Championship'),
              ('athletics-oakland-sacramento-las-vegas-timeline.html', 'Athletics', 'Oakland to Sacramento to Las Vegas')]),

# ------------------------------------------------------------------- 4. Candlestick
dict(slug='candlestick-park-history-wind-the-catch-demolition',
     section='Bay Area Sports', tag='Bay Area History', hub='Bay Area Sports',
     title='Candlestick Park: The Wind, The Catch, and the End of the Stick',
     h1="Candlestick Park: The Wind, The Catch, the Earthquake, and What Is There Now",
     dek="Opened in 1960 for $15 million on the coldest, windiest point in San Francisco. "
         "Fifty-five years, two franchises, one earthquake, the Beatles' last concert, "
         "and a site that is finally being built on.",
     desc="Candlestick Park explained: the wind, the 1989 earthquake, The Catch, the "
          "Giants and 49ers years, the 2015 demolition and the site's redevelopment.",
     date='2026-08-08',
     card=('49ers', 'Candlestick Park', 'Fifty-five years on the windiest point in the city'),
     body=[
      "There is a generation in this region that never sat in it, and a generation that "
      "cannot talk about it without complaining about the cold for ten minutes first. "
      "Both are correct. Candlestick Park was a badly sited, badly conceived, genuinely "
      "unpleasant stadium, and losing it took something out of the city that Levi's "
      "Stadium has never come close to replacing.",

      "<b>What was built, and where.</b> Candlestick opened on 12 April 1960 at a cost of "
      "about $15 million, on Candlestick Point in the southeast corner of San Francisco. "
      "Baseball capacity started at 43,765 and eventually pushed past 60,000; as a "
      "football stadium it opened at around 45,000 in 1971 and finished near 69,700. It "
      "was the first modern ballpark of its kind on the West Coast and it was put on a "
      "windswept promontory sticking into the bay, which is the single fact that explains "
      "everything else about it.",

      "<b>The wind.</b> Not a quirk, a defining feature. Cold air came off the water and "
      "swirled inside the bowl in ways nobody modelled before they poured the concrete. "
      "Willie Mays reckoned it cost him more than a hundred home runs. Fans wore parkas "
      "in July and the club handed out badges to people who sat through extra innings in "
      "the freezing fog. Across town, {oracle} was eventually built with the water on the "
      "other side and the wind mostly behind you, and the difference between the two "
      "parks is the difference between a city that learned and a city that guessed.",

      "<b>The Stu Miller story, told correctly.</b> At the 1961 All-Star Game the "
      "reliever Stu Miller was charged with a balk, and the legend became that a gust of "
      "wind physically blew him off the mound. Miller spent the rest of his life saying "
      "that was not what happened, he swayed, he did not get blown over, and the live "
      "radio call did not mention it. The story survived anyway, because it was the "
      "perfect Candlestick story and nobody wanted the accurate version.",

      "<b>The Catch.</b> 10 January 1982, NFC Championship, Montana rolling right with "
      "the season ending and Dwight Clark going up at the back of the end zone. It sent "
      "the 49ers to their first Super Bowl and it started everything on the {ledger} that "
      "has a 49ers logo next to it. {catch} is the moment itself, told properly. This "
      "page is the building it happened in, and the building matters: the wind, the mud, "
      "the noise off that concrete.",

      "<b>The earthquake.</b> 17 October 1989. Game 3 of the World Series, Giants against "
      "the Athletics, the only all-Bay Area World Series there has ever been, and at "
      "5:04 p.m., minutes before first pitch, the Loma Prieta earthquake hit with the "
      "stadium full. Sixty thousand people were inside a fifty-year-old concrete bowl "
      "during a 6.9. It held. The structure flexed rather than failing, the crowd walked "
      "out, and the Series stopped for ten days. Whatever else anyone says about that "
      "stadium, it did the one thing that mattered on the one day it was asked.",

      "<b>The Giants' half.</b> 1960 to 1999. Mays, McCovey, Marichal, then the lean "
      "years, then Bonds arriving in 1993 for the {pennant93}, a 103-win season that "
      "ended without a playoff spot, in a stadium the franchise had twice nearly left. "
      "The last game there was 30 September 1999, a 9-4 loss to the Dodgers, which is "
      "about as Candlestick an ending as could have been arranged.",

      "<b>The 49ers' half.</b> 1971 to 2013, which covers the entire dynasty. Five Super "
      "Bowl titles were won by a team that played its home games here. Montana and Young "
      "and the whole {mvsy} argument happened on this field. The last event was 23 "
      "December 2013, a 34-24 win over Atlanta, and then the franchise moved forty miles "
      "south to Santa Clara, which is its own entry on the {moves} page.",

      "<b>The Beatles, which is not a footnote.</b> On 29 August 1966 the Beatles played "
      "their final commercial concert here. Not their final performance ever, but the "
      "last time they played a ticketed show for a paying audience, and it happened in a "
      "cold, half-empty ballpark on the edge of San Francisco. Forty-eight years later, "
      "on 14 August 2014, Paul McCartney played the last event the building ever hosted "
      "before demolition. The same man closed it that helped make it famous.",

      "<b>The end.</b> Demolition ran from 4 February to 24 September 2015. They did not "
      "implode it, the neighbourhood was too close, so it came down piece by piece over "
      "eight months, which meant everyone in the southeast of the city got to watch it "
      "disappear slowly.",

      "<b>And then nothing, for a decade.</b> The site was supposed to become a "
      "neighbourhood almost immediately. Instead it sat as bare ground while the plan "
      "stayed tangled up with the radiological cleanup scandal at the neighbouring "
      "Hunters Point Shipyard. San Francisco formally separated the two projects in "
      "November 2024, and the Candlestick side is now moving: a 270-acre masterplan, "
      "groundbreaking in 2026, first phase infrastructure supporting roughly 675 homes, "
      "and eventually more than 7,200 residences plus offices, retail and parkland. The "
      "first homes are expected around 2030 and the full build runs decades.",

      "<b>Which is the second time this region has done this.</b> Tear down or empty out "
      "the stadium, promise a neighbourhood, deliver a decade of bare ground. The "
      "{coliseum} is entering that exact process now with a thirty-year masterplan of its "
      "own. Watching what actually gets built at Candlestick Point over the next five "
      "years is the single best available guide to what will really happen in East "
      "Oakland.",

      "<b>What it was worth.</b> Not the concrete. Candlestick was where the 49ers dynasty "
      "was built and where an entire region sat through a 6.9 earthquake together, and "
      "it was fifteen minutes from downtown instead of forty. The 49ers gained a better "
      "stadium and lost the city. Both things are true and only one of them shows up in "
      "the revenue numbers.",

      "More: {catch}, the {ledger}, the {moves} page, and the {hub}.",
     ],
     links={'oracle': ('oracle-park-mccovey-cove-splash-hits-guide.html', 'Oracle Park'),
            'ledger': ('bay-area-championships-complete-list-by-team.html',
                       'championship ledger'),
            'catch': ('flashback-the-catch-1982.html', 'The Catch'),
            'pennant93': ('giants-1993-pennant-race-braves-103-wins-wild-card.html',
                          '1993 pennant race'),
            'mvsy': ('montana-young-49ers-quarterback-controversy.html',
                     'Montana versus Young'),
            'moves': ('bay-area-franchise-relocations-teams-that-left.html',
                      'franchise relocations'),
            'coliseum': ('oakland-coliseum-history-what-happens-to-it-now.html',
                         'Oakland Coliseum'),
            'hub': ('../history.html', 'history section')},
     related=[('flashback-the-catch-1982.html', 'Flashback', 'The Catch, 1982'),
              ('49ers-dynasty-team-of-the-decade.html', '49ers', 'The Team of the Decade'),
              ('oakland-coliseum-history-what-happens-to-it-now.html', 'Bay Area History', 'The Oakland Coliseum')]),

# ------------------------------------------------------------------ 5. Oracle Arena
dict(slug='oracle-arena-roaracle-history-oakland-warriors',
     section='Bay Area Sports', tag='Bay Area History', hub='Bay Area Sports',
     title='Oracle Arena: How Roaracle Became the Loudest Building in the NBA',
     h1="Oracle Arena: How a 1966 Concrete Drum Became Roaracle, and What Is In It Now",
     dek="Opened in 1966, the oldest arena in the league by the end, 19,596 seats, three "
         "championships, and a farewell that nobody in Oakland asked for. The building "
         "the Warriors left.",
     desc="Oracle Arena explained: the 1966 opening, the Roaracle years, three Warriors "
          "titles, the last game in June 2019, and what the building is used for now.",
     date='2026-08-08',
     card=('warriors', 'Roaracle', 'Nineteen thousand five hundred and ninety-six seats'),
     body=[
      "The Warriors won three championships in this building and then left it, and the "
      "official story is that they needed a modern arena. The true story is that they "
      "needed a more expensive one. Either way the building is still standing, still "
      "full most weekends, and nobody has written down what it actually was.",

      "<b>What it is.</b> A round concrete arena that opened on 9 November 1966, on the "
      "same 120-acre site as the {coliseum} and connected to it by a walkway over the "
      "car park. The two buildings were conceived together as one civic project, which is "
      "why the arena has spent its whole life being described as the thing next to the "
      "stadium. Capacity 19,596. By the time the Warriors left it was the oldest arena in "
      "the National Basketball Association.",

      ARENA_NAMES,

      "<b>The Warriors moved in for 1971-72</b>, the season the club stopped being the "
      "San Francisco Warriors and became Golden State, which is covered properly on the "
      "{moves} page. They stayed until 2019. The farewell campaign called it 47 seasons "
      "and nobody in Oakland was in the mood to argue about the arithmetic.",

      "<b>The 1975 title, and the best piece of trivia this region owns.</b> The Warriors "
      "swept Washington for the championship in 1975, and two of their home games in that "
      "Finals were not played here at all. The arena was booked. For the Ice Follies. A "
      "team on its way to a sweep of the NBA Finals had to move across the bay to the Cow "
      "Palace because the ice show had the room. That is a complete summary of how this "
      "franchise was regarded before Stephen Curry.",

      "<b>Then two decades of being terrible in a loud building.</b> Between 1975 and 2015 "
      "the Warriors made the playoffs rarely and won one series that anybody outside the "
      "East Bay remembers. What the building had in that period was the crowd. Sellouts "
      "through genuinely bad seasons, a season-ticket base that renewed out of stubbornness "
      "rather than hope, and a noise level that visiting teams complained about while the "
      "home side was losing sixty games. That is where the name came from. Roaracle was "
      "earned during the losing, not during the parade years, and people forget that "
      "because it is inconvenient.",

      "<b>The rebuild that saved it.</b> The arena was gutted and rebuilt starting in 1996 "
      "at a cost of more than $121 million, reopening for the autumn of 1997 with the "
      "seating bowl, concourses and suites it kept until the end. Public money again, and "
      "again for a tenant that would eventually leave, the same pattern as Mount Davis "
      "next door, on a smaller scale and with a longer payoff.",

      "<b>And then it became the loudest building in American basketball.</b> Three "
      "championships in four years: 2015, 2017, 2018. The {record73} season in between. "
      "The night {klay} scored 37 points in a single quarter without missing a shot. A "
      "generation of people in the East Bay for whom this concrete drum is simply where "
      "the best team any of us will ever see played its home games. Five of the "
      "{ledger} were won by a team based in this arena.",

      "<b>The last night.</b> 13 June 2019, Game 6 of the NBA Finals. Toronto won 114-110 "
      "and took the title on this floor. Klay Thompson tore his ACL in the third quarter, "
      "was helped off, came back out of the tunnel to shoot two free throws, made both, "
      "and left again. The building's final act was a championship being handed to "
      "somebody else and its most beloved player being carried out of it. Nobody in "
      "Oakland has ever needed a metaphor explained to them since.",

      "<b>Then they moved.</b> Chase Center opened in San Francisco for 2019-20, a better "
      "arena, more revenue, more expensive seats, and forty minutes and a bridge toll away "
      "from the people who filled the old one through the losing years. It is on the "
      "{moves} page as an internal move, which is technically correct and misses the "
      "point entirely.",

      "<b>What is in it now, which is the part nobody expects.</b> It is called Oakland "
      "Arena again and it is a working concert venue with a full calendar, major touring "
      "acts across pop, hip-hop, country and Latin music have played it through 2026. A "
      "building written off as obsolete for professional basketball turns out to be a "
      "perfectly good 19,000-seat room when somebody wants to sell 19,000 tickets.",

      "<b>Its future is a separate negotiation from the stadium's.</b> The Coliseum land "
      "is going to the group redeveloping the 112 acres; the arena has drawn its own "
      "prospective buyer in the Oak View Group, the venue company co-founded by the music "
      "executive Irving Azoff, at a price reported north of $100 million. That has not "
      "closed, and the city and county remain responsible for running the place in the "
      "meantime. The {coliseum} page tracks the larger deal.",

      "<b>What it was worth.</b> The Warriors are a better business in San Francisco and "
      "nobody at that club will ever say publicly that the move cost them anything. But "
      "the atmosphere they spent forty years building was not portable, because it was "
      "not made of architecture, it was made of people who could afford to come. "
      "{warriorsdyn} is the record of what was won here. This page is the room it "
      "happened in.",

      "More: the {coliseum} next door, {candlestick} across the bay, and the {hub}.",
     ],
     links={'coliseum': ('oakland-coliseum-history-what-happens-to-it-now.html',
                         'Oakland Coliseum'),
            'moves': ('bay-area-franchise-relocations-teams-that-left.html',
                      'franchise moves'),
            'record73': ('warriors-73-9-best-record-ever-added-durant.html',
                         '73-9'),
            'klay': ('flashback-klay-37-point-quarter.html', 'Klay Thompson'),
            'ledger': ('bay-area-championships-complete-list-by-team.html',
                       "region's twenty-one championships"),
            'warriorsdyn': ('warriors-championship-history.html',
                            "The Warriors' championship history"),
            'candlestick': ('candlestick-park-history-wind-the-catch-demolition.html',
                            'Candlestick'),
            'hub': ('../history.html', 'history section')},
     related=[('oakland-coliseum-history-what-happens-to-it-now.html', 'Bay Area History', 'The Oakland Coliseum: What Happens to It Now'),
              ('warriors-championship-history.html', 'Warriors', "The Warriors' Championship History"),
              ('bay-area-championships-complete-list-by-team.html', 'Bay Area History', 'Every Bay Area Championship')]),
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
