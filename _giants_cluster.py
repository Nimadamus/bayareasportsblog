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
      "clubhouse stands on its manager.",
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
