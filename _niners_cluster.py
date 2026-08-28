#!/usr/bin/env python3
"""_niners_cluster.py: the 49ers 2026 season content system.

Five pieces that are deliberately different from the 24 that already exist. The archive
is full of training-camp columns; what it has never had is the permanent furniture a
season needs: a place that answers "how good is Purdy actually", a place that holds the
roster, a place that holds the schedule, and a preview that is about structure rather
than optimism.

Reuses the article template and renderer from _college_cluster.py so the markup, schema
and card handling stay identical across clusters.

  python _niners_cluster.py [--check]
"""
import os, re, sys, subprocess
import _college_cluster as CC

ROOT = os.path.dirname(os.path.abspath(__file__))

ARTICLES = [
# --------------------------------------------------------------- 1. Purdy evergreen hub
dict(slug='brock-purdy-career-passer-rating-where-he-ranks',
     section='49ers', tag='49ers', hub='49ers',
     title='Where Brock Purdy Actually Ranks, and What He Can Still Reach',
     h1="Where Brock Purdy Actually Ranks Among Quarterbacks, and What He Can Still Reach",
     dek="A permanent page for the argument that will not go away. The career numbers, "
         "the records genuinely within reach, and the ones that are not, updated as the "
         "seasons go.",
     desc="A running look at where Brock Purdy sits historically: career passer rating, "
          "the records in reach, and the milestones that are realistic rather than hype.",
     date='2026-08-08',
     card=('49ers', 'The Purdy Question', 'Career numbers, real records, and what is actually reachable'),
     body=[
      "This is the argument that has followed Brock Purdy since the day he took over, and "
      "it never resolves, because both sides are arguing about different things. One side "
      "points at the numbers. The other side points at the roster around him. This page "
      "exists to keep the numbers straight, and it gets updated as the seasons go.",
      "Start with the one that matters most. Purdy's career passer rating sits at 104.0. "
      "The all-time record for career passer rating is 102.2, held by Aaron Rodgers. That "
      "is not a projection or a hot take, that is where the number is. The catch is the "
      "qualifier: the record requires 1,500 career pass attempts, and Purdy has 1,353. He "
      "gets there roughly five games into 2026, and at that moment, if the number holds, "
      "he owns the record. {chase} covers what that week will actually look like.",
      "Here is the honest caveat, and anyone arguing in good faith has to hold it at the "
      "same time as the record. Passer rating is a counting-era statistic that rewards "
      "efficiency, and Purdy has played his entire career in an offense designed by one "
      "of the best offensive minds in football, throwing to a tight end who will end up "
      "in Canton and a running back who was, for a stretch, the most dangerous weapon in "
      "the sport. Nobody produces a 104.0 alone. That is true, and it does not make the "
      "104.0 disappear.",
      "What is realistically reachable. The career passer rating record is the closest "
      "and the most likely, and it arrives early in 2026. Beyond that, the things worth "
      "watching are the ones that need volume: career completion percentage among "
      "qualified passers, yards per attempt, and the win totals that quarterbacks get "
      "credited with whether they deserve it or not. All of those need him to stay "
      "healthy and to keep playing behind a functioning line, which has not always been "
      "available.",
      "What is not realistically reachable, and it is worth saying plainly. He is not "
      "catching the career volume records, the yardage and touchdown leaderboards belong "
      "to quarterbacks who played twenty years and threw six hundred times a season, and "
      "Purdy started late enough that the arithmetic does not work. Anyone framing his "
      "career as a chase for those numbers is selling something.",
      "The other half of the ledger is the one nobody enjoys: the games that decided "
      "seasons. There is a {vegas} that this fan base has still not processed, and "
      "quarterback legacies get built in February whether that is fair or not. A record "
      "in Week 5 does not settle it. A ring would.",
      "The comparison people reach for around here is the one nobody wins. This is the "
      "franchise of {montana} and Steve Young, and any quarterback who plays well in this "
      "uniform gets measured against two Hall of Famers who won here. It is an unfair "
      "standard and it is also the correct one, because it is the standard the building "
      "itself sets. Purdy has a better career passer rating than either of them. He also "
      "has none of the hardware, and around here the hardware is the argument.",
      "What to watch in 2026 specifically: whether the efficiency survives a receiver "
      "room that has been rebuilt on the fly, whether the offensive line holds up, and "
      "whether {preview} turns out to be as good as it looks on paper. This page gets "
      "updated as those answers arrive. The rest of our coverage is on the {hub}.",
     ],
     links={'chase': ('49ers-brock-purdy-highest-passer-rating-nfl-history-1500-attempts.html',
                      'Our piece on the record chase'),
            'montana': ('montana-young-49ers-quarterback-controversy.html', 'Joe Montana'),
            'vegas': ('49ers-still-paying-for-vegas.html', 'Super Bowl this team is still paying for'),
            'preview': ('49ers-2026-season-preview-roster-schedule-questions.html',
                        'the roster around him'),
            'hub': ('../49ers.html', '49ers hub')},
     related=[('49ers-2026-season-preview-roster-schedule-questions.html', '49ers Preview', 'The 2026 49ers, Position by Position'),
              ('49ers-brock-purdy-highest-passer-rating-nfl-history-1500-attempts.html', '49ers', 'Purdy Is 147 Passes From the Best Passer Rating Ever'),
              ('montana-young-49ers-quarterback-controversy.html', '49ers History', 'Two Hall of Famers, One Job')]),

# --------------------------------------------------------------- 2. Season preview
dict(slug='49ers-2026-season-preview-roster-schedule-questions',
     section='49ers', tag='49ers Preview', hub='49ers',
     title='The 2026 49ers: Roster, Schedule, and the Questions That Decide It',
     h1="The 2026 49ers: What the Roster Actually Looks Like, and the Four Questions That Decide the Season",
     dek="A quarterback playing the best football of his career, a receiver room rebuilt "
         "twice in one summer, a defence under Raheem Morris, and a season that opens on "
         "the other side of the world.",
     desc="A structural preview of the 2026 49ers: the offense, the defence, the "
          "coaching, the schedule, and the four questions that actually decide the year.",
     date='2026-08-08',
     card=('49ers', 'The 2026 49ers', 'Roster, schedule, and the four questions that decide it'),
     body=[
      "Every 49ers preview written this month says the same thing: if they are healthy, "
      "they are a problem. That is true, and it is also useless, because this team has "
      "not been healthy in any season anyone can remember. So here is the version that "
      "tries to be useful, what is actually on the roster, and what has to break right.",
      "<b>The offense.</b> It runs through {purdy}, who is playing the best football of "
      "his career and is a handful of attempts from owning the career passer rating "
      "record. Around him, the receiver room has been rebuilt twice in one summer: Mike "
      "Evans and Christian Kirk arrived as veterans, {deebo} came home on a one-year "
      "deal, {pearsall} was lost for the season before a snap was played, and "
      "{stribling} has forced his way into the conversation as a rookie. George Kittle "
      "is still George Kittle. Christian McCaffrey, when upright, is still the most "
      "dangerous player on the field.",
      "<b>The defence.</b> Raheem Morris runs it, and {morris} explains why that matters "
      "more than the scheme diagram: players play harder for him. Nick Bosa and Fred "
      "Warner are the spine. Dre Greenlaw is back. The August signing spree brought in "
      "Ogbo Okoronkwo and others to fill the gaps that opened, which tells you the front "
      "office knows the depth is thin.",
      "<b>The coaching.</b> Kyle Shanahan is coaching while recovering from a car "
      "accident that was worse than it first sounded. That is not a footnote. A head "
      "coach whose job is play design and game management, working through a physical "
      "recovery during the most demanding stretch of the calendar, is a real variable "
      "that nobody outside the building can measure.",
      "<b>The schedule.</b> It starts in Australia. The 49ers open against the Rams at "
      "the Melbourne Cricket Ground on 10 September, the first regular season game the "
      "NFL has ever played in Melbourne, and {melbourne} covers what that actually costs "
      "a team in Week 1. Miami comes to Levi's in Week 2, Washington on a Monday night "
      "in Week 6, and there is a home game against Minnesota that is not at home at all, "
      "it is in Mexico City. Five prime-time games. The cross-divisional draw is the "
      "NFC East and the AFC West, plus three third-place matchups from a third-place "
      "finish last year.",
      "<b>Question one: does the receiver room hold?</b> Two veterans learning a new "
      "offense, a rookie, and a returning star on a one-year deal is not a settled group. "
      "If it clicks by October this offense is frightening. If it does not, Purdy spends "
      "another year making it work with whoever is standing.",
      "<b>Question two: does the line protect him?</b> Every version of the good 49ers "
      "has been a team that ran the ball and kept the quarterback clean. Every version of "
      "the disappointing 49ers has been a team that could not.",
      "<b>Question three: does the defence stay ahead of its own injury list?</b> Twenty "
      "players missed a single August practice at one point this summer. Depth is not a "
      "luxury on this roster, it is the whole question.",
      "<b>Question four: what does February look like?</b> This franchise does not "
      "measure seasons in wins. It measures them against a Super Bowl it lost and has "
      "never gotten over. Twelve wins and a divisional round exit will be treated around "
      "here as a failure, which is either unreasonable or exactly the right standard, "
      "depending on which bar you are standing in.",
      "The full game-by-game breakdown is in the {sched}, the roster detail is on the "
      "{depth}, and everything else lives on the {hub}.",
     ],
     links={'purdy': ('brock-purdy-career-passer-rating-where-he-ranks.html', 'Brock Purdy'),
            'deebo': ('49ers-deebo-samuel-returns-one-year-7-million-2026.html', 'Deebo Samuel'),
            'pearsall': ('49ers-ricky-pearsall-out-for-season-pcl-surgery-2026.html', 'Ricky Pearsall'),
            'stribling': ('49ers-dezhaun-stribling-training-camp-starter-2026.html', "De'Zhaun Stribling"),
            'morris': ('49ers-raheem-morris-players-love-him-just-play-football-2026.html', 'the Raheem Morris effect'),
            'melbourne': ('49ers-rams-melbourne-nfl-first-game-australia.html', 'our Melbourne piece'),
            'sched': ('49ers-2026-schedule-season-hub.html', 'season schedule hub'),
            'depth': ('49ers-2026-roster-depth-chart.html', 'depth chart page'),
            'hub': ('../49ers.html', '49ers hub')},
     related=[('49ers-2026-schedule-season-hub.html', '49ers', 'The 2026 49ers Schedule, Week by Week'),
              ('49ers-2026-roster-depth-chart.html', '49ers', 'The 2026 49ers Roster and Depth Chart'),
              ('brock-purdy-career-passer-rating-where-he-ranks.html', '49ers', 'Where Brock Purdy Actually Ranks')]),

# --------------------------------------------------------------- 3. Depth chart hub
dict(slug='49ers-2026-roster-depth-chart',
     section='49ers', tag='49ers', hub='49ers',
     title='The 2026 49ers Roster and Depth Chart, Position by Position',
     h1="The 2026 49ers Roster and Depth Chart, Position by Position",
     dek="Who starts, who backs them up, who is hurt, and which position group is one "
         "injury from becoming a problem. Updated through the season.",
     desc="A position-by-position look at the 2026 49ers roster: starters, key backups, "
          "the injury situation, and where the depth actually runs out.",
     date='2026-08-08',
     card=('49ers', 'Roster & Depth', 'Who starts, who backs them up, and where it runs thin'),
     body=[
      "A depth chart in August is a work of fiction with a long revision history, so "
      "treat this as a running record rather than a verdict. It gets updated as the "
      "roster moves.",
      "<b>Quarterback.</b> {purdy} and nobody you want to think about. The single "
      "largest gap between the starter and the backup on the roster, and the reason every "
      "conversation about this season eventually becomes a conversation about protection.",
      "<b>Running back.</b> Christian McCaffrey when healthy, which is the qualifier that "
      "has followed him here. Patrick Taylor Jr and the rest of the room have been "
      "getting real camp work, partly by necessity. The offense changes character "
      "entirely depending on which version of this group is available in December.",
      "<b>Receiver.</b> The most rebuilt group on the team, twice over. Mike Evans and "
      "Christian Kirk came in as veterans. {deebo} returned on a one-year deal. "
      "{stribling} has been the story of camp as a rookie. {pearsall} is out for the "
      "season after PCL surgery, which is the injury that reshaped this room. "
      "{hodge} and Demarcus Robinson are the depth, and both have already had moments "
      "worth writing about in August.",
      "<b>Tight end.</b> George Kittle, still the most reliable thing on the roster, with "
      "Jake Deguara among the summer additions behind him.",
      "<b>Offensive line.</b> The group nobody wants to discuss and everybody should. "
      "This is where seasons are decided for a team built on outside zone and play "
      "action, and it is the unit whose failures are hardest to fix mid-season.",
      "<b>Defensive line.</b> Nick Bosa, plus Ogbo Okoronkwo from the {spree}. Bosa "
      "easing back is the sort of sentence that reads fine in August and terrifies you "
      "in November.",
      "<b>Linebacker.</b> Fred Warner and Dre Greenlaw, both back from the injuries that "
      "gutted this defence for two years. If those two play sixteen games each, the "
      "defence is fine. If they do not, everything else is theoretical.",
      "<b>Secondary.</b> The group most exposed to the depth problem, and the one "
      "{morris} will have to scheme around most.",
      "<b>The injury picture.</b> It has been the defining feature of this camp. Twenty "
      "players missed one August practice. {injuries} covers the pattern, and it is a "
      "pattern rather than bad luck at this point.",
      "<b>Where the depth actually runs out.</b> Three places. Behind the quarterback, "
      "where there is no plan anyone wants to execute. On the offensive line, where the "
      "drop from starter to backup is the difference between an offense and a problem. "
      "And in the secondary, where the scheme asks a lot of players who have not proven "
      "they can hold up over seventeen games. Everywhere else this roster can absorb a "
      "loss. In those three rooms it cannot.",
      "<b>How to read this page as the season goes.</b> Depth charts published in August "
      "describe intentions. What matters is what changes: who moves up when somebody goes "
      "down, which rookie stops being a project, and which veteran signing turns out to "
      "have been a warning rather than an upgrade. This page tracks those movements "
      "rather than restating the official two-deep every week.",
      "The structural read of all this is in the {preview}, and the week-to-week is on "
      "the {sched}. Everything else lives on the {hub}.",
     ],
     links={'purdy': ('brock-purdy-career-passer-rating-where-he-ranks.html', 'Brock Purdy'),
            'deebo': ('49ers-deebo-samuel-returns-one-year-7-million-2026.html', 'Deebo Samuel'),
            'stribling': ('49ers-dezhaun-stribling-training-camp-starter-2026.html', "De'Zhaun Stribling"),
            'pearsall': ('49ers-ricky-pearsall-out-for-season-pcl-surgery-2026.html', 'Ricky Pearsall'),
            'hodge': ('49ers-khadarel-hodge-veteran-receiver-signing-august-2026.html', 'KhaDarel Hodge'),
            'spree': ('49ers-signing-spree-okoronkwo-irwin-deguara-hodge-august-2026.html', 'August signing spree'),
            'morris': ('49ers-raheem-morris-players-love-him-just-play-football-2026.html', 'Raheem Morris'),
            'injuries': ('49ers-injuries-again-training-camp-august-2026.html', 'Our injury column'),
            'preview': ('49ers-2026-season-preview-roster-schedule-questions.html', 'season preview'),
            'sched': ('49ers-2026-schedule-season-hub.html', 'schedule hub'),
            'hub': ('../49ers.html', '49ers hub')},
     related=[('49ers-2026-season-preview-roster-schedule-questions.html', '49ers Preview', 'The 2026 49ers, Position by Position'),
              ('49ers-injuries-again-training-camp-august-2026.html', '49ers', 'It Is August and the 49ers Are Already Hurt'),
              ('49ers-2026-schedule-season-hub.html', '49ers', 'The 2026 49ers Schedule, Week by Week')]),

# --------------------------------------------------------------- 4. Schedule / season hub
dict(slug='49ers-2026-schedule-season-hub',
     section='49ers', tag='49ers', hub='49ers',
     title='The 2026 49ers Schedule, Week by Week',
     h1="The 2026 49ers Schedule, Week by Week, With Every Preview and Reaction",
     dek="The season landing page. Melbourne to open, Mexico City in the middle, five "
         "prime-time games, and links to our coverage of each one as it happens.",
     desc="The 2026 49ers schedule with the structure that matters: the Melbourne opener, "
          "the Mexico City game, five prime-time slots, and our coverage of each week.",
     date='2026-08-08',
     card=('49ers', 'The Schedule', 'Melbourne, Mexico City, five prime-time games'),
     body=[
      "This is the page to keep open on a Sunday. Every week gets a preview before "
      "kickoff and a reaction after it, and both get linked here as they publish, so the "
      "season reads in order rather than as a pile of separate columns.",
      "<b>The shape of it.</b> The 49ers drew the NFC East and the AFC West in "
      "cross-divisional play, plus three matchups against fellow third-place finishers "
      "from the NFC North, AFC East and NFC South, the consequence of finishing third "
      "in the NFC West last season. Five prime-time games, two of them at Levi's.",
      "<b>Before any of it: the preseason closes at the Chargers.</b> Thursday 20 August "
      "at SoFi, seven o'clock Pacific, against Jim Harbaugh, with a joint practice down "
      "in El Segundo two days earlier. It counts for nothing and {harbaugh} explains why "
      "a lot of us will watch every snap of it anyway. It went about as well as a "
      "meaningless August night can go: {sofi}.",
      "<b>Week 1, 10 September: at the Rams, in Melbourne.</b> The NFL's first regular "
      "season game in Melbourne, at the Cricket Ground, kicking off at 5:35pm Pacific on "
      "a Thursday. A divisional road game on the other side of the planet to start the "
      "year is a genuinely strange piece of scheduling and {melbourne} gets into what it "
      "costs.",
      "<b>Week 2: Miami at Levi's.</b> The home opener, and the first chance to see "
      "whatever this offense becomes in front of its own crowd after a trip halfway "
      "around the world.",
      "<b>Week 6: Washington at Levi's, Monday night.</b> One of the two prime-time home "
      "games, and by then we should know whether the receiver room has settled.",
      "<b>Mexico City: Minnesota, at Estadio Banorte.</b> A designated home game that "
      "is not at home. Two of this team's home dates are being played outside the United "
      "States, which is worth remembering when anyone talks about home-field advantage "
      "in January.",
      "<b>What to watch across the year.</b> The record chase is the story that travels: "
      "{purdy} needs a handful of attempts to qualify for the career passer rating "
      "record, which puts it somewhere around the fifth game. Beyond that it is the "
      "familiar things, health, the line, and whether {preview} holds up once the games "
      "are real.",
      "<b>The stretches that decide it.</b> Any NFL season breaks into three or four "
      "runs, and the ones to circle here are the opening fortnight, Melbourne then Miami "
      "on a short turnaround, and whatever the schedule makers did with the December "
      "dates. Teams built on health, and this one is, get judged in December by how much "
      "of the roster is still standing. A soft September means nothing if the group that "
      "walks into December is the same group that limped through last winter.",
      "<b>Why the third-place draw matters.</b> Finishing third in the division last year "
      "handed this team three games against other third-place finishers, from the NFC "
      "North, AFC East and NFC South. That is the league quietly rewarding a bad season "
      "with an easier schedule. If the 49ers are the team they think they are, those "
      "three games are wins, and the difference between eleven and thirteen victories is "
      "exactly that kind of margin.",
      "Weekly previews land late in the week, reactions land after the whistle, and both "
      "get added here. The roster picture is on the {depth}, and the rest of our 49ers "
      "coverage is on the {hub}.",
     ],
     links={'melbourne': ('49ers-rams-melbourne-nfl-first-game-australia.html', 'our Melbourne piece'),
            'harbaugh': ('49ers-chargers-thursday-harbaugh-return-kittle-achilles-recovery.html',
                         'the Harbaugh reunion'),
            'sofi': ('49ers-chargers-41-17-cowing-punt-return-preseason-august-20.html',
                     '49ers 41, Chargers 17 at SoFi'),
            'purdy': ('brock-purdy-career-passer-rating-where-he-ranks.html', 'Brock Purdy'),
            'preview': ('49ers-2026-season-preview-roster-schedule-questions.html', 'the preview'),
            'depth': ('49ers-2026-roster-depth-chart.html', 'depth chart page'),
            'hub': ('../49ers.html', '49ers hub')},
     related=[('49ers-rams-melbourne-nfl-first-game-australia.html', '49ers', 'The NFL Is Opening the 49ers Season in Melbourne'),
              ('49ers-2026-season-preview-roster-schedule-questions.html', '49ers Preview', 'The 2026 49ers, Position by Position'),
              ('49ers-2026-roster-depth-chart.html', '49ers', 'The 2026 49ers Roster and Depth Chart')]),

# --------------------------------------------------------------- 5. Melbourne
dict(slug='49ers-rams-melbourne-nfl-first-game-australia',
     section='49ers', tag='49ers', hub='49ers',
     title='The NFL Is Opening the 49ers Season in Melbourne. Really.',
     h1="The NFL Is Opening the 49ers Season in Melbourne, and Somebody Should Explain the Travel Math",
     dek="A divisional road game against the Rams, at the Melbourne Cricket Ground, in "
         "Week 1. The first regular season game the league has ever played in Australia, "
         "and the 49ers get to be the experiment.",
     desc="The 49ers open 2026 against the Rams at the Melbourne Cricket Ground, the "
          "NFL's first regular season game in Australia. What that costs in Week 1.",
     date='2026-08-08',
     card=('49ers', 'Melbourne', 'A Week 1 divisional game on the other side of the world'),
     body=[
      "On 10 September the San Francisco 49ers will play a regular season football game "
      "at the Melbourne Cricket Ground. Against the Los Angeles Rams. In Week 1. This is "
      "the first regular season game the NFL has ever staged in Australia, and somebody "
      "in a conference room decided the right teams to send were two NFC West rivals who "
      "play each other twice a year anyway.",
      "The MCG is a genuinely great venue, a hundred thousand seats, the most famous "
      "sporting ground in the country, a place built for a sport that involves a lot more "
      "running and a lot fewer helmets. As a spectacle it will be excellent. As a Week 1 "
      "assignment it is something else.",
      "Consider the travel. Melbourne is roughly seventeen hours ahead of Pacific time, "
      "which means a body clock does not shift, it inverts. The flight is the better part "
      "of a day. The league has run games in London and Munich and Mexico City for years "
      "and teams have learned to manage those; nobody has a playbook for Australia, "
      "because nobody has done it. Both sides are equally in the dark, which is the "
      "fairest thing about it.",
      "What it actually costs is the week after. International trips historically wreck "
      "the following week more than the game itself, which is why the league usually "
      "pairs them with a bye. Here the 49ers come home and host Miami in Week 2. A short "
      "week is one thing. A short week after crossing the international date line to play "
      "a divisional game is another.",
      "There is a version of this that works out. Win in Melbourne and the season starts "
      "with a divisional road win, a global audience, and a team that spent a week "
      "bonding on a plane. Lose it and the fan base spends September arguing about why a "
      "team with legitimate ambitions was used as the league's marketing experiment.",
      "This is also not the only trip. There is a designated home game against Minnesota "
      "in Mexico City later in the year. Two of this team's scheduled home dates are "
      "outside the United States. For a franchise whose stadium already has a reputation "
      "for atmosphere problems, giving away a home game to a neutral site abroad is a "
      "choice worth noticing.",
      "The league's argument is that these games grow the sport, and on the evidence of "
      "London that is not nonsense, a market that had no NFL presence twenty years ago "
      "now sustains multiple sold-out games a season. Australia is a genuinely promising "
      "market for the same reasons: an existing football culture, a sports-mad "
      "population, and a stadium that can hold a hundred thousand people. The strategy "
      "is sound. It is the timing that is questionable.",
      "Because Week 1 is not a neutral slot. It is the week a team learns what it is, "
      "with a roster that has not played together and a coaching staff still working out "
      "its rotations. Handing that week to a fourteen-thousand-mile round trip is asking "
      "a lot of a group that has {injuries} before the season has even started.",
      "The rest of the year is laid out in the {sched}, the roster picture is on the "
      "{depth}, and the structural read is in the {preview}. Everything else is on the "
      "{hub}.",
     ],
     links={'sched': ('49ers-2026-schedule-season-hub.html', 'season schedule hub'),
            'depth': ('49ers-2026-roster-depth-chart.html', 'depth chart page'),
            'injuries': ('49ers-injuries-again-training-camp-august-2026.html', 'an injury list this long'),
            'preview': ('49ers-2026-season-preview-roster-schedule-questions.html', 'season preview'),
            'hub': ('../49ers.html', '49ers hub')},
     related=[('49ers-2026-schedule-season-hub.html', '49ers', 'The 2026 49ers Schedule, Week by Week'),
              ('49ers-2026-season-preview-roster-schedule-questions.html', '49ers Preview', 'The 2026 49ers, Position by Position'),
              ('49ers-still-paying-for-vegas.html', '49ers', 'The 49ers Are Still Paying For Vegas')]),

# ------------------------------------------- 6. camp reaction, Saturday 8 August 2026
dict(slug='49ers-defense-purdy-saturday-shanahan-coaching-preseason-opener',
     section='49ers', tag='49ers', hub='49ers',
     title='The Defense Won Saturday. Shanahan Coaches Thursday.',
     h1="The 49ers Defense Won Saturday, and Shanahan Is Coaching the Preseason Opener",
     dek="The defense got the better of Brock Purdy on Saturday, Kyle Shanahan watched it "
         "happen from behind a pair of sunglasses, and he is the one running the sideline "
         "when Tennessee comes to Levi's on Thursday.",
     desc="The 49ers defense got the better of Brock Purdy on Saturday, and Kyle Shanahan "
          "will be coaching the sideline himself in the preseason opener against Tennessee.",
     date='2026-08-09',
     card=('49ers', 'Camp: The Defense Answers', 'Purdy had a hard Saturday, and Shanahan is coaching Thursday'),
     body=[
      "The defense won Saturday. Not a series, not a red zone period that somebody spins "
      "into a headline afterward, the day. Brock Purdy did not have it, and the group on "
      "the other side of the ball is the reason why, and after the last few Augusts around "
      "here that sentence is worth typing slowly.",
      "Understand why this fan base is allergic to camp takes. Every August somebody on "
      "defense makes a play, three hundred people report it as a breakthrough, and then "
      "the season starts and the same unit gets run at for two hundred yards on the "
      "ground by a team that told everybody exactly what it was going to do. We have been "
      "burned by the August version of this defense enough times to know that one good "
      "Saturday is not a season. Fine. Noted.",
      "It still matters, and here is the honest reason. Practice is a closed system. There "
      "is exactly one quarterback in this building who knows the offense the way the man "
      "who designed it knows it, and beating him is the hardest thing the defense gets to "
      "do all week. When {purdy} is off, it is usually because somebody made him off. "
      "Coverage held long enough that the read went to the second and third option. "
      "Pressure showed up before the timing did. That is what a defense winning a day "
      "actually looks like, and it does not happen by accident against this offense.",
      "The other half of it is the part nobody should skip past. Purdy having a rough "
      "Saturday in the second week of August is not a crisis, it is Tuesday. He is not "
      "playing Tennessee for anything on Thursday, he is not playing the Rams for "
      "anything until September, and the quarterback who spent three years turning "
      "seventh-round into a passer-rating argument is allowed to throw a bad ball in "
      "shorts. Anyone building a panic column off it in August is doing the thing this "
      "site exists to complain about.",
      "Then there is Shanahan, standing there in sunglasses, watching his own offense get "
      "handled and giving away nothing, which is the most Shanahan detail imaginable. The "
      "sunglasses are half the man's public personality at this point. You cannot read "
      "him. You never could. He has watched his offense get shut down in far more "
      "expensive settings than a Saturday practice and worn the same expression.",
      "The news underneath the sunglasses is the part with a date attached. He is "
      "coaching the preseason opener. Kyle Shanahan, on the sideline, running the game "
      "against Tennessee at Levi's on Thursday night. Preseason openers are usually "
      "where a head coach delegates, stands with his arms folded, and lets the staff run "
      "the thing while he watches the roster fight for the last eight spots. Not this "
      "one.",
      "You can read that two ways and both are probably a little true. The generous read "
      "is that there is enough new on this roster, and the {depth} has the full picture "
      "of how much, that he wants his hands on the operation from the first snap rather "
      "than the first week of September. The less generous read is that August has been "
      "August around here, {injuries} is not the sentence you want attached to the "
      "second week of camp, and a coach who has been through what this coach has been "
      "through does not hand the wheel to anybody in a year that has to go right.",
      "Either way, Thursday is now worth actually watching, which is not something you "
      "get to say about most preseason openers. The head coach is running it. The defense "
      "just spent Saturday proving it can win a day against the best quarterback it will "
      "see in practice all year. Those two facts arriving in the same week is the first "
      "genuinely encouraging thing this camp has produced.",
      "Keep the expectations where they belong. The season starts in Melbourne on 10 "
      "September and nothing that happens in a Levi's preseason game changes the shape of "
      "it. The rest of the year is laid out in the {sched}, the structural read is in the "
      "{preview}, and everything else lives on the {hub}. But for one Saturday in August, "
      "the defense was the story for the right reason, and the head coach is treating "
      "Thursday like it counts. Take it.",
     ],
     links={'purdy': ('brock-purdy-career-passer-rating-where-he-ranks.html', 'Purdy'),
            'depth': ('49ers-2026-roster-depth-chart.html', 'depth chart page'),
            'injuries': ('49ers-injuries-again-training-camp-august-2026.html', 'the injury list'),
            'sched': ('49ers-2026-schedule-season-hub.html', 'season schedule hub'),
            'preview': ('49ers-2026-season-preview-roster-schedule-questions.html', 'season preview'),
            'hub': ('../49ers.html', '49ers hub')},
     related=[('49ers-brock-purdy-sharp-camp-demarcus-robinson-dime-end-zone-2026.html', '49ers',
               'Purdy Was Sharp in Camp, and the Dime to Robinson Was the Proof'),
              ('49ers-2026-roster-depth-chart.html', '49ers', 'The 2026 49ers Roster, Position by Position'),
              ('49ers-2026-schedule-season-hub.html', '49ers', 'The 2026 49ers Schedule, Week by Week')]),

# ------------------------------------------- 7. RB room + Bosa + Kittle, Monday 10 August 2026
dict(slug='49ers-running-back-room-gutted-mccaffrey-tightness-bosa-soreness-kittle',
     section='49ers', tag='49ers', hub='49ers',
     title='Four Running Backs Down, Bosa Sore, and Kittle Running. Again.',
     h1="The 49ers Are Down Four Running Backs, Bosa Is Sore, and the Only Good News Is George Kittle",
     dek="Christian McCaffrey sat out Monday with tightness, the three backs behind him are "
         "already hurt, the team spent the day auditioning strangers, and Nick Bosa has not "
         "been in pads in a week. Then Kittle went out and ran.",
     desc="McCaffrey out with tightness, the three backs behind him hurt, tryouts for "
          "Nyheim Miller-Hines and Zamir White, Bosa sore, and Kittle running again.",
     date='2026-08-10',
     card=('49ers', 'The RB Room Is Gone', 'McCaffrey sore, three backs hurt, and tryouts on a Monday'),
     body=[
      "It is 10 August. The season is a month away. And on Monday the San Francisco 49ers "
      "held a limited practice without the four running backs that any of us would have "
      "named as the four running backs on this roster. Not one of them. All four.",
      "Christian McCaffrey did not practice. The word out of the building is "
      "<b>tightness</b>, which the coaching staff delivered with the standard shrug, a "
      "little sore, he is doing fine, we are managing him as we go. And look, I have been "
      "doing this long enough to know that tightness in the second week of August is "
      "usually nothing. Teams sit players in August for hangnails. If the name on the "
      "jersey were anybody else I would not have typed a word about it.",
      "But it is not anybody else. It is Christian McCaffrey, and this fan base has been "
      "conditioned like a lab animal. We have watched an entire season of this man "
      "evaporate over something that started as a calf and became an Achilles and became a "
      "year. We have heard <i>managing his workload</i> before. So no, the word tightness "
      "does not scare me. The name attached to it does, and if you tell me you feel "
      "differently I do not believe you.",
      "Now the rest of the room, because this is the part that is genuinely absurd. "
      "<b>Kaelon Black</b>, the rookie, has been off to the side for a while with an "
      "adductor, groin, in the language people actually use. <b>Jordan James</b> is out "
      "with broken ribs, cracked in late July when Fred Warner went to punch the ball out "
      "in practice, which is the single most 49ers sentence of this entire camp. Our own "
      "All-Pro linebacker broke our own running back. And <b>Isaac Guerendo</b> has been "
      "gone since before camp opened with a torn pectoral.",
      "Four deep. Gone. So the 49ers did what a team does when it looks up and finds the "
      "position group empty: they went shopping on a Monday. Tryouts for <b>Nyheim "
      "Miller-Hines</b> and <b>Zamir White</b>, plus a visit with <b>Blake Watson</b>, an "
      "undrafted kid out of Memphis who ran a 4.39 and jumped 41 and a half inches at his "
      "pro day. That is not a panic move and I am not going to pretend it is. It is wear "
      "and tear insurance, bodies to take carries so the ones you care about do not have "
      "to. Every team does it. It is just that most teams are not doing it because their "
      "entire depth chart is in the training room in the second week of August.",
      "Credit where it is owed: <b>Patrick Taylor Jr</b> and <b>Sincere McCormick</b> have "
      "been eating in this camp, <b>Khalil Herbert</b> has been getting real work, and "
      "{deebo} took snaps at running back on Monday because of course he did. That is the "
      "one thing this organisation is genuinely good at, finding a functional body and "
      "handing it the ball. It does not make me feel better about September.",
      "<b>Here is the one that actually worries me, and it is not a running back.</b> Nick "
      "Bosa has not been in pads. He has not been going through individual work. Three "
      "straight open sessions now, and what the team is calling it is <i>soreness</i>. "
      "General soreness. That is the entire explanation. Ask for specifics and you get the "
      "same word again.",
      "Soreness in a knee that had its ACL reconstructed after Week 3 of last season. I am "
      "not going to sit here and manufacture an emergency out of a word, Bosa was never "
      "playing a preseason snap anyway, Warner is not playing one either, and I would be "
      "stunned if Dre Greenlaw sees the field on Thursday. None of these guys need August. "
      "But <i>hasn't been padded up, hasn't done individual</i> is a different sentence "
      "from <i>we are being careful</i>, and this organisation has a long and well "
      "documented history of the second sentence quietly becoming the first one in "
      "October. Put it in the back of your mind. Do not set off the alarm yet. Just leave "
      "your hand near it.",
      "And then, finally, something good. Genuinely good.",
      "<b>George Kittle was out on the practice field before practice and he looked like "
      "George Kittle.</b> Running. Running hard. Making cuts, real ones, not the "
      "tentative jogging-in-a-straight-line stuff you see from a guy protecting a leg. "
      "This is a man who tore his Achilles in the playoff win over the Eagles and had it "
      "surgically repaired shortly after, and four months later he is out there moving "
      "like the injury is a story somebody told him about.",
      "Nobody in the building is going to say the words out loud yet, and they have the "
      "GPS data that says whatever it says about his top speed and how hard he is cutting. "
      "But watching it? I would not rule out Week 1. I am not promising Week 1. I am "
      "saying that if you had asked me in February whether Kittle would be on the field in "
      "Melbourne against the Rams on 10 September, I would have laughed and started "
      "thinking about October. Now I am not laughing. A lot depends on the next four "
      "weeks, and {melbourne} is a brutal place to make your season debut, fourteen "
      "thousand miles, a date line, a divisional opponent, but he is trending toward it, "
      "and after the Monday we just had I am taking every scrap of good news I can get.",
      "That is the state of this thing a month out. The best running back in football is "
      "sore, the three behind him are broken, strangers are auditioning at Levi's on a "
      "Monday afternoon, the best defensive player on the roster has not put pads on in a "
      "week, and the one unambiguously encouraging development is a tight end coming back "
      "from a ruptured Achilles. That is not a camp. That is a triage tent. And we have "
      "{injuries} on this site so many Augusts running that the file practically writes "
      "itself now.",
      "Thursday is the preseason opener against Tennessee, {shanahan} is coaching it "
      "himself, and you will see approximately none of the players discussed above. The "
      "roster picture is on the {depth}, the rest of the year is in the {sched}, the "
      "structural read is in the {preview}, and everything else lives on the {hub}. "
      "Thirty-one days. Somebody get this team a running back.",
      "<b>Update, 12 August:</b> they got one. Zamir White signed a one-year deal two days "
      "after that tryout, and to clear the room for him and two other veterans the 49ers "
      "{churn}.",
     ],
     links={'deebo': ('49ers-deebo-samuel-returns-one-year-7-million-2026.html', 'Deebo Samuel'),
            'melbourne': ('49ers-rams-melbourne-nfl-first-game-australia.html', 'Melbourne'),
            'injuries': ('49ers-injuries-again-training-camp-august-2026.html', 'written this column'),
            'shanahan': ('49ers-defense-purdy-saturday-shanahan-coaching-preseason-opener.html',
                         'Kyle Shanahan'),
            'depth': ('49ers-2026-roster-depth-chart.html', 'depth chart page'),
            'sched': ('49ers-2026-schedule-season-hub.html', 'season schedule hub'),
            'preview': ('49ers-2026-season-preview-roster-schedule-questions.html', 'season preview'),
            'churn': ('49ers-waive-junior-bergen-jack-bouwmeester-kj-henry-corliss-waitman.html',
                      'waived Junior Bergen, Jack Bouwmeester and K.J. Henry'),
            'hub': ('../49ers.html', '49ers hub')},
     related=[('49ers-injuries-again-training-camp-august-2026.html', '49ers', 'It Is August and the 49ers Are Already Hurt'),
              ('49ers-2026-roster-depth-chart.html', '49ers', 'The 2026 49ers Roster and Depth Chart'),
              ('49ers-defense-purdy-saturday-shanahan-coaching-preseason-opener.html', '49ers',
               'The Defense Won Saturday. Shanahan Coaches Thursday.')]),

# ------------------------------------------------- 7. 12 Aug roster churn: Bergen waived
dict(slug='49ers-waive-junior-bergen-jack-bouwmeester-kj-henry-corliss-waitman',
     section='49ers', tag='49ers', hub='49ers',
     title='The 49ers Waived Junior Bergen Again, and Kept the Punter',
     h1="The 49ers Waived Junior Bergen Again, Cut the Punter Competition, and Kept the "
        "Left-Footed Veteran",
     dek="Three names off the 90 on the eve of the preseason opener, Bergen, Bouwmeester "
         "and K.J. Henry, and three one-year deals in their place. Nobody got created "
         "space. Everybody got swapped.",
     desc="The 49ers waived Junior Bergen and Jack Bouwmeester and put K.J. Henry on "
          "waived/injured, then signed Eli Apple, Xavier Thomas and Zamir White.",
     date='2026-08-12',
     card=('49ers', 'Roster Churn', 'Bergen, Bouwmeester and Henry out, three one-year deals in'),
     body=[
      "One position battle in Santa Clara is officially over, and I want to be honest "
      "about how much I care: the 49ers have a punter, his name is <b>Corliss Waitman</b>, "
      "and the reason he has the job is that the other guy is gone. That is the whole "
      "competition. That is how punter competitions end. Somebody gets waived on a Tuesday "
      "in August and the survivor keeps his locker.",
      "The 49ers waived punter <b>Jack Bouwmeester</b>, who had been in the building since "
      "18 July, which is not even a full month of employment. They waived wide receiver "
      "and return specialist <b>Junior Bergen</b>. And they put defensive lineman "
      "<b>K.J. Henry</b> on waived/injured after he came out of the joint work with "
      "Tennessee on Tuesday with something wrong. Three names off the ninety, the day "
      "before the preseason opener.",
      "<b>Start with Bergen, because that one actually stings a little.</b> He was the "
      "final pick of the 2025 draft class, seventh round, 252nd overall out of Montana, "
      "and Shanahan said out loud at the time that the plan was to use him as a return "
      "specialist rather than a receiver. He got a four-year deal worth about $4.3 "
      "million, which in NFL money means the team owed him nothing and could walk away "
      "whenever it wanted. Then he got waived at final cuts a year ago, came back on the "
      "practice squad, signed a reserve/future contract on 20 January, and spent this "
      "entire offseason trying to prove he belonged.",
      "And now he is waived again. Same kid, same result, twelve months apart. I have "
      "watched this franchise draft return men, love them in April, describe them as "
      "weapons in July and cut them in August for as long as I can remember, and I still "
      "do not understand why the return job here is treated like a rotating door instead "
      "of a roster spot. Somebody is going to claim him and he is going to take a kick "
      "back seventy yards against us in November. Write it down.",
      "<b>Bouwmeester never had a chance and everyone knew it.</b> You do not sign a "
      "veteran punter and then hand the job to the guy you brought in three weeks ago "
      "unless he is dramatically better, and he was not, because Waitman is a real NFL "
      "punter with a real NFL body of work. He punted 65 times for Pittsburgh in 2024 at "
      "46.4 a kick with a long of 71. He punted 62 times in 2025 at 45.5 with a long of "
      "67. That is two full seasons of a team that hates giving up field position handing "
      "him the ball and living with the result.",
      "He is also left-footed, and if you have never thought about why that matters, it "
      "matters. A left-footed punter puts the opposite spin on the ball, so the returner "
      "is reading a flight path he does not see ten times a year, and coverage units that "
      "practice against it every day get a small, free edge. It is not a difference maker. "
      "It is a thumb on the scale. This team has spent the last two Augusts collecting "
      "thumbs on scales because the actual difference makers keep ending up in the "
      "training room.",
      "<b>Henry is the one nobody will write about and the one that tells you the most.</b> "
      "He signed on 29 July. He lasted two weeks. He got hurt in a joint practice against "
      "the Titans and the team processed him as waived/injured before the ball was even "
      "kicked off on Thursday. That is not cruelty, that is the business, waived/injured "
      "means he reverts to injured reserve if he clears, and the roster spot opens now "
      "instead of in September. But it is the fourth or fifth time this camp that a body "
      "we brought in to survive August did not survive August.",
      "Because here is the part that made me laugh out loud, and not the good kind. Those "
      "three spots did not stay open for a single afternoon. The same day, the 49ers "
      "signed cornerback <b>Eli Apple</b>, who they had waived themselves on 2 August, "
      "so we cut him and re-signed him inside of two weeks, defensive lineman "
      "<b>Xavier Thomas</b>, and running back <b>Zamir White</b>, the former Raiders "
      "fourth-rounder who was in here for a tryout on Monday. All three on one-year deals. "
      "Three out, three in, ninety men, nothing gained.",
      "White is the one with a purpose, and you already know why if you read {rbroom}. "
      "When your top four backs are hurt or being managed you go get somebody who has "
      "carried the ball in a real game, and White has. He is not the answer. He is a body "
      "with 227 pounds on it who can take twelve carries on Thursday so that the guys we "
      "actually need in Melbourne do not have to.",
      "That is what this roster is right now. A churn machine. Sign a guy, watch him get "
      "hurt, waive him, sign the next guy, and pray that the ones whose names are on the "
      "jerseys people bought are standing upright on 10 September. The {sched} says the "
      "season starts in Australia in twenty-nine days. The {depth} says what we have. The "
      "{preview} says what it is supposed to look like. And on Thursday night {shanahan} "
      "is going to coach a preseason game at Levi's in which almost none of the players "
      "who matter will appear, which is exactly how it should be, and which will still "
      "not stop me from watching every snap of it. The rest of the coverage is on the "
      "{hub}.",
      "We have a punter. It is Corliss Waitman. He kicks with his left foot. In the year "
      "we are supposed to be a Super Bowl team, that is the settled question. Everything "
      "else is a tryout.",
     ],
     links={'rbroom': ('49ers-running-back-room-gutted-mccaffrey-tightness-bosa-soreness-kittle.html',
                       'what happened to the running back room on Monday'),
            'shanahan': ('49ers-defense-purdy-saturday-shanahan-coaching-preseason-opener.html',
                         'Kyle Shanahan'),
            'depth': ('49ers-2026-roster-depth-chart.html', 'depth chart'),
            'sched': ('49ers-2026-schedule-season-hub.html', 'schedule'),
            'preview': ('49ers-2026-season-preview-roster-schedule-questions.html', 'season preview'),
            'hub': ('../49ers.html', '49ers hub')},
     related=[('49ers-running-back-room-gutted-mccaffrey-tightness-bosa-soreness-kittle.html', '49ers',
               'The 49ers Are Down Four Running Backs, Bosa Is Sore, and the Only Good News Is George Kittle'),
              ('49ers-2026-roster-depth-chart.html', '49ers', 'The 2026 49ers Roster and Depth Chart'),
              ('49ers-injuries-again-training-camp-august-2026.html', '49ers',
               'It Is August and the 49ers Are Already Hurt')]),

# ------------------------------------------- 7. preseason wk1 recap, Thursday 13 August
dict(slug='49ers-titans-raiders-cardinals-preseason-recap-rourke-stribling',
     section='49ers', tag='49ers', hub='49ers',
     title='The 49ers Sat Everybody. The Raiders Played Everybody and Lost Worse.',
     h1="The 49ers Sat the Whole Team and Lost to Tennessee, the Raiders Played Their Starters and Got Beat at Home, and Only One of Those Is Fine",
     dek="Preseason week one: Shanahan dressed nobody you have heard of and lost 19-13, "
         "Kurtis Rourke and De'Zhaun Stribling made the night watchable anyway, and in "
         "the desert the Raiders played Cousins and the No. 1 pick and still got run out "
         "of their own building.",
     desc="Preseason week one recap: Shanahan sat every 49ers starter in a 19-13 loss, "
          "Rourke and Stribling impressed, and the Raiders lost 27-14 at home.",
     date='2026-08-14',
     card=('49ers', 'Preseason, Week One', 'We sat everybody. Vegas played everybody. Everybody lost.'),
     body=[
      "Preseason football is back, which means it is time for the annual exercise where "
      "we all watch a game that does not count, played by guys fighting for the bottom "
      "of the roster, and pretend we can be normal about it. The 49ers lost 19-13 to "
      "Tennessee on Thursday night at Levi's, and I want to be very clear about how "
      "little the scoreboard matters, because Kyle Shanahan sat everybody. Not \"rested "
      "a few veterans.\" Everybody. No Purdy, no Kittle, no McCaffrey, no Bosa, no "
      "Warner. If a name on the back of a jersey has ever been on a jersey anybody "
      "bought, that man was in a hoodie on the sideline.",
      "And thank God for that. Have you seen {injuries}? This roster is being held "
      "together with athletic tape and one-year deals. Twenty guys have missed practice "
      "at various points this month, the running back room got {rbroom}, and the season "
      "opens on the other side of the planet in four weeks. The absolute last thing I "
      "needed on a Thursday in August was Christian McCaffrey taking a live tackle in a "
      "game that means nothing. Tennessee played their starters. Their first-team "
      "offense marched 95 yards on our third string for a touchdown on the opening "
      "drive, Tony Pollard walked in, and I felt nothing. That is what a preseason "
      "opener between a team playing its guys and a team hiding its guys looks like, "
      "and Shanahan hiding his guys is the correct call every single time.",
      "Now the part I actually enjoyed, because there was one. Kurtis Rourke was "
      "legitimately good. The kid went 12-of-14 for 101 yards, led the touchdown drive "
      "that Patrick Taylor Jr. finished from a yard out, and looked calm doing it, and "
      "then left with a rib injury, because this is the 49ers and nobody is allowed to "
      "have a clean night, not even the third quarterback in a game that does not "
      "count. 12-of-14. In his first real audition. If the ribs are fine, that is the "
      "most interesting quarterback development of the summer that does not involve the "
      "starter chasing a passer-rating record.",
      "And {stribling} keeps doing it. Seven catches, 63 yards, and the play of the "
      "night for our side, a 32-yard catch on third-and-five when the drive was about "
      "to die. Everything we have been yelling about since camp opened showed up under "
      "actual stadium lights: the hands, the routes, the fact that he is simply open "
      "all the time. The camp hype train has left the station and I am driving it. "
      "Jordan Watkins quietly went 6-for-59 on ten targets too, which means the two "
      "youngest receivers on the field were the two best 49ers on the field, and given "
      "what this receiver room has been through this summer, that is not a small thing.",
      "The rest of the night was preseason mush, and honest mush at that. We moved the "
      "ball, 322 yards, 22 first downs, and finished nothing, going 9-of-19 on third "
      "down and settling for Eddy Pineiro field goals from 41 and 52. Adrian Martinez "
      "was fine in relief, 16-of-30 for 159, more mobile than accurate. The defense "
      "spent the second half living in Will Levis's backfield, with Tatum Bethune and "
      "our new friend Ogbo Okoronkwo both getting home for sacks. Backups losing to "
      "backups by six while the actual team watches in street clothes is the best "
      "possible version of a preseason loss. Moving on.",
      "Meanwhile, in the desert, the franchise that abandoned Oakland had itself a "
      "night. The Raiders played their starters, actually played them, Kirk Cousins "
      "and the No. 1 overall pick and all, in Klint Kubiak's head coaching debut, at "
      "home, in front of their own fans, and lost 27-14 to the Arizona Cardinals. They "
      "scored 14 points in the first half and then got blanked after halftime in their "
      "own building. I need everyone in the Bay to sit with that for a second. We sat "
      "our entire team and lost by six. They played Cousins, who went 5-of-6 with a "
      "touchdown to Michael Mayer, they played Fernando Mendoza, who went 10-of-16 for "
      "96 and hit Jack Bech for a score, they got a 53-yard stiff-arm highlight run "
      "from rookie Mike Washington Jr., and they still could not hold serve at home "
      "against the Cardinals. That is the most Raiders result imaginable: the "
      "highlights go viral, the scoreboard says you lost by 13.",
      "And look, Mendoza is going to be fine, which is the depressing part for them, "
      "the kid looked more comfortable than anything they ran out there last season, "
      "and it did not matter, because the team around the quarterback is still the "
      "team around the quarterback. Some franchises sit their stars in August because "
      "the season has real stakes. Some franchises play their stars in August because "
      "August is the season. I will let you decide which one just moved to Las Vegas. "
      "This is, after all, {vegas} we swore we would never forgive.",
      "So the ledger after week one of fake football: a loss that cost us nothing, a "
      "rib X-ray that better come back clean, two young receivers who look like actual "
      "players, and a rival that keeps finding new rock bottoms with a better roster "
      "than they deserve. The {sched} says Melbourne is in four weeks. The {preview} "
      "says what this team is supposed to be. Nothing that happened Thursday changed "
      "either one, which is exactly what you want from a preseason opener. The rest of "
      "the coverage is on the {hub}.",
     ],
     links={'stribling': ('49ers-dezhaun-stribling-training-camp-starter-2026.html',
                          "De'Zhaun Stribling"),
            'injuries': ('49ers-injuries-again-training-camp-august-2026.html',
                         'the injury list'),
            'rbroom': ('49ers-running-back-room-gutted-mccaffrey-tightness-bosa-soreness-kittle.html',
                       'gutted in a single Monday'),
            'vegas': ('49ers-still-paying-for-vegas.html', 'the city'),
            'sched': ('49ers-2026-schedule-season-hub.html', 'schedule hub'),
            'preview': ('49ers-2026-season-preview-roster-schedule-questions.html', 'season preview'),
            'hub': ('../49ers.html', '49ers hub')},
     related=[('49ers-waive-junior-bergen-jack-bouwmeester-kj-henry-corliss-waitman.html', '49ers',
               'The 49ers Waived Junior Bergen Again, and Kept the Left-Footed Punter'),
              ('49ers-dezhaun-stribling-training-camp-starter-2026.html', '49ers',
               "De'Zhaun Stribling Is Forcing His Way Into the Starting Lineup"),
              ('49ers-2026-schedule-season-hub.html', '49ers',
               'The 2026 49ers Schedule, Week by Week')]),

# ------------------------------------------- 8. Shanahan ring-or-bust column, 14 August
dict(slug='kyle-shanahan-needs-to-win-the-ring-this-year-2026',
     section='49ers', tag='49ers', hub='49ers',
     title='Kyle Shanahan Needs to Win the Ring This Year. Say It Out Loud.',
     h1="Kyle Shanahan Needs to Win the Ring This Year, and Everybody in the Building Knows It",
     dek="Year ten. Two Super Bowls lost, both to the same team, one of them in a city "
         "this fan base still cannot say without wincing. The roster is built, the "
         "quarterback is peaking, and the excuse supply has finally run out.",
     desc="Year ten of Kyle Shanahan, two Super Bowl losses, a peaking Brock Purdy and a "
          "loaded roster: why 2026 is the season the ring becomes the whole job.",
     date='2026-08-14',
     card=('49ers', 'Ring or Bust', 'Year ten. Two lost Super Bowls. No excuses left.'),
     body=[
      "There is a sentence this fan base keeps swallowing every August, and I am done "
      "swallowing it, so here it is in plain English: Kyle Shanahan needs to win the "
      "ring this year. Not \"compete.\" Not \"be in the mix.\" Not another January of "
      "house-money football that ends with somebody else's confetti. The ring. This "
      "year. Say it out loud, because pretending the standard is anything lower is how "
      "a decade slips past you.",
      "Because that is what this is now, a decade. This is year ten of the Shanahan "
      "era. Ten years of the prettiest offense in football, ten years of coaching-tree "
      "worship, ten years of every broadcast telling us we are watching a genius. And "
      "the trophy case from those ten years holds two NFC championships and zero "
      "Lombardis. Two Super Bowls reached, two Super Bowls lost, both to the same "
      "franchise, and the second one in a city whose name we do not say around here, "
      "{vegas} covers what that night did to us, and I am still not over it, and "
      "neither is he. A blown fourth-quarter lead in Miami and an overtime dagger in "
      "the desert. That is the resume. Brilliant, beloved, and empty-handed.",
      "And before anybody starts typing: I know. Nobody schemes a wider-open receiver. "
      "Half the head coaches in this league ran his offense or worked down the hall "
      "from it. The man can call a game. That is precisely why the standard is what it "
      "is. You do not get graded on a curve for being the smartest coach in the "
      "building for ten years. At some point the genius has to cash. Andy Reid heard "
      "this exact conversation for two decades, brilliant, innovative, cannot win the "
      "big one, and then he won it, and now nobody remembers the conversation. That "
      "door swings both ways, and Shanahan is standing in it.",
      "Now look at what he has been handed in 2026, because this is the part that "
      "removes the last excuse. {purdy} is playing the best football of his life and "
      "is five games from owning the career passer rating record outright. The "
      "receiver room got rebuilt into something absurd, Mike Evans, Christian Kirk, "
      "Deebo home on a one-year deal, and a rookie in Stribling who has looked like "
      "the best player on the field since camp opened. Kittle is still Kittle. "
      "McCaffrey, when vertical, is still the most dangerous player in the sport. "
      "Raheem Morris has the defense playing for him, Greenlaw is back, and the front "
      "office spent all of August signing bodies the moment anything cracked. The "
      "{preview} lays it out position by position, and the honest read is simple: "
      "there is no roster in the NFC with fewer holes. \"Best team if healthy\" is not "
      "my phrase. It is everybody's phrase. It has been everybody's phrase for three "
      "years, and it has bought exactly nothing.",
      "Yes, there are real obstacles, and I am not pretending otherwise. The man is "
      "coaching through recovery from a car accident that was worse than the first "
      "reports let on, which is a genuinely hard thing that nobody should wave away. "
      "{injuries} is already longer than anyone wants in August, and the running back "
      "room spent a week held together with tryout guys. The league, in its wisdom, "
      "decided our season should open at the Melbourne Cricket Ground, seventeen time "
      "zones from home, with Miami waiting on a short week after. None of that is "
      "fake. All of it is survivable, and every contender has a version of it. The "
      "teams that win rings are the ones that stop itemizing their obstacles.",
      "Here is the uncomfortable arithmetic underneath all of it. Windows do not "
      "announce when they close. McCaffrey and Kittle are on the back side of their "
      "primes. Deebo is here for one year. Evans is here for the twilight. The cheap "
      "years of the quarterback are gone, which means this is the last version of "
      "this roster that can be this deep. In 2027 something gives, it always does. "
      "Whatever this team is going to be under Kyle Shanahan, it is going to be it "
      "now. There is no version of this era where year twelve is the good part.",
      "And understand what is actually at stake for him, because it is bigger than a "
      "season. This is the franchise of Walsh and Montana and Young and Rice, five "
      "Lombardis in the lobby, and the standard here was set by men who finished the "
      "job. Win it, and Shanahan walks into that room and the decade of near-misses "
      "becomes the story of persistence, the Reid arc, the redemption everybody "
      "writes gladly. Lose again with this roster, and the conversation stops being "
      "\"when does Kyle win one\" and becomes \"does Kyle ever win one,\" and that "
      "second conversation has an expiration date on it in every building in this "
      "league, no matter whose name is on the play sheet.",
      "So no more house money. No more moral victories, no more prettiest-loss-in-"
      "football, no more January exits explained away by a hamstring. The {sched} "
      "starts in Melbourne in four weeks and ends, if it ends right, in February with "
      "a sixth trophy in the lobby. That is the season. That is the whole season. "
      "Ring or bust, and for the first time in ten years, saying it out loud is not "
      "pressure. It is just the truth. The rest of the coverage is on the {hub}.",
     ],
     links={'vegas': ('49ers-still-paying-for-vegas.html', 'the Super Bowl this team is still paying for'),
            'purdy': ('brock-purdy-career-passer-rating-where-he-ranks.html', 'Brock Purdy'),
            'preview': ('49ers-2026-season-preview-roster-schedule-questions.html', 'season preview'),
            'injuries': ('49ers-injuries-again-training-camp-august-2026.html', 'The injury list'),
            'sched': ('49ers-2026-schedule-season-hub.html', 'schedule'),
            'hub': ('../49ers.html', '49ers hub')},
     related=[('49ers-still-paying-for-vegas.html', '49ers', 'The 49ers Are Still Paying For Vegas'),
              ('49ers-shanahan-best-team-if-healthy-super-bowl-2026.html', '49ers',
               'Shanahan Says This Is His Best Team If Healthy'),
              ('49ers-2026-season-preview-roster-schedule-questions.html', '49ers Preview',
               'The 2026 49ers, Position by Position')]),

# --------------------------------------------------------- 7. Stribling reach take
dict(slug='49ers-dezhaun-stribling-reach-draft-grade-critics-wrong-2026',
     section='49ers', tag='49ers Column', hub='49ers',
     title="They Called De'Zhaun Stribling a Reach. Nobody Is Laughing Now",
     h1="Everybody Laughed at the 49ers for Taking De'Zhaun Stribling. It Is the 49ers Doing the Laughing Now",
     dek="Draft night was a pile-on. The grades were bad, the takes were worse, and the "
         "same people who called this a reach have spent all summer watching the kid "
         "torch our own defence and then do it again under stadium lights.",
     desc="Draft night said the 49ers reached for De'Zhaun Stribling. One camp and one "
          "preseason game later, that take has aged like milk.",
     date='2026-08-15',
     card=('49ers', 'Who Is Laughing Now', "They called Stribling a reach. He has been the best rookie in camp"),
     body=[
      "I want everybody who dunked on this pick to sit still for a minute, because I have "
      "been waiting all summer for this and I am not going to be gracious about it. "
      "Draft night, the second the 49ers turned the card in for De'Zhaun Stribling, the "
      "whole internet went off. Reach. Panic pick. Value left on the board. Grades in the "
      "C range from people who had never watched a full game of his and were reading off "
      "a board somebody else made. I sat there getting texts from friends who root for "
      "other teams, all of them some version of \"lol.\" Fine. Great. Hope you enjoyed it.",
      "Because here is where we are in the middle of August. That kid has been the single "
      "best story of this training camp, and it has not been close. {camp} was not a "
      "one-day flash and it never turned into one. He strung good day onto good day onto "
      "good day against a secondary that is not exactly a JV squad, and by the second week "
      "the reps he was winning stopped getting the rookie qualifier attached to them. "
      "{chem} with Brock Purdy showed up early and then just kept deepening, which is the "
      "part that actually matters, because quarterbacks do not throw back-shoulder balls "
      "to guys they are not sure about.",
      "And then the lights came on and he did it in a real stadium in front of real "
      "people. {recap}: seven catches, 63 yards, and a 32-yard grab on third-and-five with "
      "the drive dying. That is not a padded stat line against fourth-stringers in garbage "
      "time. That is a receiver being the reason a possession stayed alive. Seven targets, "
      "seven answers. The hands, the routes, the fact that he is somehow always open, all "
      "the stuff we had been yelling about for three weeks travelled straight from the "
      "practice field to an actual game without losing anything on the way.",
      "So what exactly was the reach? Explain it to me. Because from where I am sitting "
      "the \"reach\" is a 22-year-old who came into a receiver room stacked with veterans, "
      "took reps from people making real money, and is now the most likely candidate on "
      "this roster to be a Week 1 starter. Rooms do not hand out jobs out of politeness. "
      "He is not getting these looks because the depth chart is empty, it is the opposite. "
      "Mike Evans is in the building. Christian Kirk is here. {pearsall} took the receiver "
      "room's worst news of the summer and the room did not collapse, and a big reason it "
      "did not collapse is standing there in a rookie jersey catching everything thrown "
      "near him.",
      "I know exactly why the take existed, by the way. The draft-industrial complex is "
      "built on consensus boards, and consensus boards are built on other people's "
      "consensus boards, and the second a team picks a guy fifteen spots before the "
      "internet agreed he should go, the algorithm spits out \"reach\" whether the player "
      "is good or not. Nobody grading picks that night was grading the player. They were "
      "grading how closely the 49ers agreed with a spreadsheet. That is not analysis. That "
      "is a group project where everybody copied the same homework.",
      "And look, I am the last person who hands this front office free credit. I have "
      "spent years watching this organisation find creative new ways to make me insane, "
      "and I will be first in line the next time they whiff. But this one they got right, "
      "and they got it right by trusting their own eyes instead of the board everybody "
      "else was reading off. That deserves to be said out loud, especially in a summer "
      "where {injuries} has been the running theme and good news has been rationed.",
      "The only thing left to do now is the part that scares me, which is the part where "
      "we ask him to do it in games that count. Preseason is preseason. Camp is camp. "
      "September is a different animal, the schedule opens on the other side of the "
      "planet, and this league has humbled a hundred August legends. I am not putting him "
      "in Canton. I am saying the argument has flipped completely: it is no longer \"can "
      "he make the roster,\" it is \"how do you possibly keep him off the field.\" That is "
      "a full 180 from where the national conversation had him in April.",
      "So enjoy the quiet, everybody. The grades are still up on the internet with a C "
      "next to them, and the guy those grades were about is the best rookie receiver I "
      "have watched in this uniform in years. Reach. Sure. Keep laughing. The rest of our "
      "coverage is on the {hub}.",
     ],
     links={'camp': ('49ers-dezhaun-stribling-training-camp-starter-2026.html',
                     'What he did in camp'),
            'chem': ('49ers-purdy-stribling-chemistry-loaded-roster-2026.html',
                     'The chemistry'),
            'recap': ('49ers-titans-raiders-cardinals-preseason-recap-rourke-stribling.html',
                      'In the preseason opener against Tennessee'),
            'pearsall': ('49ers-ricky-pearsall-out-for-season-pcl-surgery-2026.html',
                         'Losing Ricky Pearsall for the season'),
            'injuries': ('49ers-injuries-again-training-camp-august-2026.html',
                         'the injury list'),
            'hub': ('../49ers.html', '49ers hub')},
     related=[('49ers-dezhaun-stribling-training-camp-starter-2026.html', '49ers Column',
               "De'Zhaun Stribling Is Making a Starting Job Look Inevitable"),
              ('49ers-titans-raiders-cardinals-preseason-recap-rourke-stribling.html', '49ers Column',
               'The 49ers Sat Everybody and Lost by Six'),
              ('49ers-2026-season-preview-roster-schedule-questions.html', '49ers Preview',
               'The 2026 49ers, Position by Position')]),

# --------------------------------------------- 8. Veteran/young mix, drafts trending up
dict(slug='49ers-veteran-young-core-mix-recent-drafts-better-2026',
     section='49ers', tag='49ers Column', hub='49ers',
     title='The 49ers Finally Have the Mix Right, and the Drafts Are Why',
     h1='The 49ers Finally Have the Right Mix of Veterans and Kids, and the Last Few Drafts Are the Reason',
     dek="A Hall of Fame core in its prime, veterans on short deals who know exactly what "
         "they are here for, and a young group that is finally producing instead of "
         "developing. It has been a long time since all three were true at once.",
     desc="A veteran core in its prime, smart short-term signings, and draft picks who "
          "actually play. The 49ers roster balance is the best it has been in years.",
     date='2026-08-15',
     card=('49ers', 'Veterans and Kids', 'The roster balance is the best it has been in years'),
     body=[
      "I have spent enough years yelling about this roster to have earned the right to say "
      "something nice about it, so here it is. For the first time in a while, the 49ers "
      "are not a team with a great top and nothing underneath, and they are not a team "
      "full of projects waiting to become something. They are both halves at once, and the "
      "reason is the part of this operation I have historically been hardest on: the "
      "drafting. It got better. Genuinely better. I am as surprised as anybody.",
      "Start with the veterans, because that is the part that has always been here. Trent "
      "Williams is still Trent Williams. George Kittle is still the most reliable thing in "
      "the building and will end up in Canton. Fred Warner and Dre Greenlaw are both back "
      "from the injuries that gutted this defence for two years, and if those two play a "
      "full season the whole thing works. Nick Bosa is Nick Bosa. Christian McCaffrey, "
      "when healthy, changes what the offense even is. That is a genuine championship "
      "spine, and it is in its prime right now, not three years from now.",
      "Then look at how they filled in around it, because this is the smartest the front "
      "office has looked in a while. Mike Evans as a proven X. Christian Kirk on a one-year "
      "deal. Deebo Samuel back on a short-money contract. Ogbo Okoronkwo, KhaDarel Hodge, "
      "Demarcus Robinson, all veterans, all on deals that expire before they become "
      "regrets. That is the whole trick with veteran signings and this team used to be "
      "terrible at it: get the production without buying the decline years. Nobody in that "
      "group is going to be an albatross on the cap sheet in 2029.",
      "And now the part that actually changed. The young players are not projects anymore, "
      "they are contributors. {stribling} is the loudest example, a rookie the entire "
      "internet mocked on draft night who has been the best story of camp and then went out "
      "and caught seven balls in the preseason opener. But he is not alone, and that is the "
      "point. Jordan Watkins quietly went 6-for-59 on ten targets in that same game. "
      "{rourke} went 12-of-14 in his first real audition at quarterback. Carver Willis is "
      "getting real offensive line reps as a rookie. That is four young players producing "
      "in one August, which is four more than some of the classes around here produced in "
      "three years.",
      "Because let us be honest about what this used to look like. There was a long stretch "
      "where a 49ers draft class meant one guy who might start in year three, one special "
      "teamer, and four names you would be Googling in 2027 to remember who they were. "
      "{bergen} was the last pick of the 2025 draft and got waived twice trying to stick. "
      "That is normal, seventh-rounders are lottery tickets and nobody is owed anything. "
      "But the middle rounds used to be a wasteland too, and a team paying Purdy, Williams, "
      "Kittle, Bosa and Warner cannot afford a wasteland in the middle rounds. That is the "
      "math that decides whether a contending window is three years or eight.",
      "The thing that makes me believe this is not a fluke is what happened when the worst "
      "news of the summer hit. {pearsall} was the first-round pick who was finally supposed "
      "to be the answer at receiver, and he is gone for the year after PCL surgery. Losing "
      "a first-round receiver would have flattened the 2023 or 2024 version of this "
      "offense. This one shrugged and reloaded, because the room behind him was actually "
      "stocked, veterans who have done it and kids who are doing it. Depth is not a thing "
      "you notice until you need it, and this team needed it in July and had it.",
      "I am not going to pretend the roster is finished, because {depth} makes it very "
      "clear where it is not. There is no plan behind Brock Purdy that anybody wants to "
      "execute. The offensive line drops off a cliff after the starters. The secondary is "
      "asking a lot of players who have not held up over seventeen games. Those are real "
      "problems and one bad Sunday turns any of them into the story of the season. Nobody "
      "should read this as a coronation.",
      "But the shape is right, and the shape is what I have been complaining about for "
      "years. You want your stars in their prime, your veterans on short money, and your "
      "young guys pushing the veterans for snaps instead of holding a clipboard. All three "
      "of those are true right now. Whether that turns into anything in February is a "
      "different question and one this franchise has answered badly twice. {preview} lays "
      "out what has to go right. The rest of our coverage is on the {hub}.",
     ],
     links={'stribling': ('49ers-dezhaun-stribling-reach-draft-grade-critics-wrong-2026.html',
                          "De'Zhaun Stribling"),
            'rourke': ('49ers-titans-raiders-cardinals-preseason-recap-rourke-stribling.html',
                       'Kurtis Rourke'),
            'bergen': ('49ers-waive-junior-bergen-jack-bouwmeester-kj-henry-corliss-waitman.html',
                       'Junior Bergen'),
            'pearsall': ('49ers-ricky-pearsall-out-for-season-pcl-surgery-2026.html',
                         'Ricky Pearsall'),
            'depth': ('49ers-2026-roster-depth-chart.html', 'the depth chart'),
            'preview': ('49ers-2026-season-preview-roster-schedule-questions.html',
                        'The season preview'),
            'hub': ('../49ers.html', '49ers hub')},
     related=[('49ers-dezhaun-stribling-reach-draft-grade-critics-wrong-2026.html', '49ers Column',
               "They Called Stribling a Reach. Nobody Is Laughing Now"),
              ('49ers-2026-roster-depth-chart.html', '49ers',
               'The 2026 49ers Roster and Depth Chart, Position by Position'),
              ('49ers-2026-season-preview-roster-schedule-questions.html', '49ers Preview',
               'The 2026 49ers, Position by Position')]),

# ------------------------------- 11. Harbaugh returns Thursday + Kittle update, 16 August 2026
dict(slug='49ers-chargers-thursday-harbaugh-return-kittle-achilles-recovery',
     section='49ers', tag='49ers', hub='49ers',
     title='Harbaugh Comes Back Thursday, and Kittle Finally Sounds Like Himself',
     h1="Jim Harbaugh Comes Back on Thursday, and George Kittle Finally Sounds Like Himself Again",
     dek="The 49ers are at SoFi on Thursday night against the man who dragged this "
         "franchise back to life and then got run out of the building. And the best news "
         "of the week has nothing to do with him.",
     desc="The 49ers play Harbaugh's Chargers at SoFi on Thursday night, and George "
          "Kittle says his Achilles recovery is hitting every marker with Week 1 in reach.",
     date='2026-08-16',
     card=('49ers', 'Harbaugh Comes Back', 'Thursday at SoFi, and the Kittle news we wanted'),
     body=[
      "Jim Harbaugh is on the other sideline Thursday night and I have been trying all "
      "week to decide how I feel about it. I still do not know. The 49ers are at SoFi at "
      "seven o'clock on Thursday, it is a preseason game, it means nothing, and I am going "
      "to watch every snap of it like it is January.",
      "Because it is him. It is the guy who walked into a building that had been "
      "irrelevant for a decade and made it terrifying inside of one season. Forty four "
      "wins, nineteen losses and a tie. Three straight NFC Championship Games. A Super "
      "Bowl that we should have won and that I still refuse to discuss in detail with "
      "anybody. He did all of that in four years, and then it ended, because of course it "
      "ended, over egos and pride and a front office that decided it would rather be right "
      "than be good.",
      "And I am still mad about it. Twelve years later. I am aware of how that sounds.",
      "So Thursday is going to be strange. He gets the handshake, he gets the nice video "
      "package, somebody at the network will use the word <i>reunion</i> about eleven "
      "times, and none of it changes that we spent a decade after him trying to find that "
      "exact feeling again.",
      "<b>Now the part that actually matters.</b> George Kittle stood there this week and "
      "sounded like George Kittle again, and I did not realise how badly I needed to hear "
      "it until he opened his mouth.",
      "You remember how this started. Eleven January, the playoff game against "
      "Philadelphia, and his right Achilles went. That is the injury that used to end "
      "careers and still ends seasons, and he is thirty two years old, and every one of us "
      "did the same grim arithmetic that night about what a tight end looks like on the "
      "other side of one of those.",
      "He has been on the physically unable to perform list all camp. He says he expects "
      "to come off it before the season. He says he is hitting the markers, that he is "
      "getting close, that he wants to be back in pads sooner rather than later. He would "
      "not put a date on it, which is the correct answer and also a deeply annoying one. "
      "And the detail that got me is the speed. He is reportedly running at numbers close "
      "to where he was before the thing tore. Eight months after an Achilles.",
      "The one honest caveat, because I have been burned by August optimism more times "
      "than I can count: the work left is calf strength, getting the repaired side back to "
      "matching the other one, and that is exactly the part nobody can rush and nobody can "
      "see from the outside. It is also the part that decides whether he is himself in "
      "December or whether he spends the year being managed. So no, he is not playing "
      "Thursday, he should not play Thursday, and if anybody at that facility even "
      "considers putting him on a field at SoFi in August for a game that does not count I "
      "will drive down there personally.",
      "Week 1 is in Australia against the Rams and that is the date he is aiming at. That "
      "is the one I care about. The full picture of who is available and who is not is on "
      "the {depth}, and it has not been a kind summer, as {rbroom} covered in painful "
      "detail.",
      "<b>What Thursday is actually for.</b> Tuesday is the part that matters more, when "
      "the two teams practise together down in El Segundo, because joint practices are "
      "where real football gets played in August and the game afterwards is mostly "
      "paperwork. Thursday is roster spots. It is the back half of the receiver room and "
      "the last three defensive line jobs and whichever young corner decides he wants to "
      "make somebody's life difficult. Watch those guys. Nothing else on that field is "
      "going to tell you anything about September.",
      "Harbaugh, meanwhile, will do what Harbaugh does, which is treat a preseason game "
      "like a street fight and get genuinely furious about a holding call in the third "
      "quarter with his fourth string offense on the field. That is not an act. That was "
      "never an act. It is the entire reason it worked here and the entire reason it "
      "eventually did not.",
      "There is also the small matter of our own head coach, who is putting himself back "
      "together after the car accident and is expected to be there for Week 1, which is "
      "its own kind of August storyline that I would very much like to stop having. The "
      "structural read on this roster is in the {preview}, the whole year is laid out in "
      "the {sched}, and everything else lives on the {hub}.",
      "But strip all of it away and this is the week the news was good. Kittle is running "
      "and he is happy about it. The old man is coming back to town for one night. Go "
      "watch it, yell at your television about 2013 for a while, and then let the guy with "
      "the Achilles take all the time he needs.",
     ],
     links={'depth': ('49ers-2026-roster-depth-chart.html', 'depth chart page'),
            'rbroom': ('49ers-running-back-room-gutted-mccaffrey-tightness-bosa-soreness-kittle.html',
                       'the state of the running back room'),
            'sched': ('49ers-2026-schedule-season-hub.html', 'season schedule hub'),
            'preview': ('49ers-2026-season-preview-roster-schedule-questions.html', 'season preview'),
            'hub': ('../49ers.html', '49ers hub')},
     related=[('49ers-running-back-room-gutted-mccaffrey-tightness-bosa-soreness-kittle.html', '49ers',
               'Four Running Backs Down, Bosa Sore, and Kittle Running. Again.'),
              ('49ers-2026-schedule-season-hub.html', '49ers', 'The 2026 49ers Schedule, Week by Week'),
              ('49ers-2026-roster-depth-chart.html', '49ers',
               'The 2026 49ers Roster and Depth Chart, Position by Position')]),

# ------------------------------------------------- 49ers 41, Chargers 17, preseason wk 2
dict(slug='49ers-chargers-41-17-cowing-punt-return-preseason-august-20',
     section='49ers', tag='49ers', hub='49ers',
     title='49ers 41, Chargers 17: The Best Night of the Summer',
     h1="49ers 41, Chargers 17: Jacob Cowing Went Eighty Three Yards Down the SoFi Sideline and the Whole Night Turned Into Something",
     dek="Forty one points on Jim Harbaugh's defence in his own building. Three hundred "
         "and twenty one yards. A hundred and forty six on the ground. And a receiver who "
         "lost an entire year to a hamstring taking a punt to the house. I know it is "
         "August. I do not care.",
     desc="49ers 41, Chargers 17 at SoFi: Jacob Cowing took a punt 83 yards, the run game "
          "piled up 146, and San Francisco led Harbaugh's Chargers 20 to 3 at the half.",
     date='2026-08-20',
     card=('49ers', '41 to 17 at SoFi', 'Cowing goes 83 yards and the depth shows up'),
     body=[
      "Forty one to seventeen. In his building. On his defence. On a Thursday night in "
      "August in front of sixty two thousand people who came out to watch Jim Harbaugh be "
      "Jim Harbaugh again, and who instead watched the San Francisco 49ers hang forty one "
      "on the Los Angeles Chargers and make it look casual.",
      "I spent {preview} telling you Thursday was going to be strange and that none of it "
      "would mean anything. I was half right. It was strange. And then somewhere around "
      "the middle of the second quarter it stopped being a preseason game to me and "
      "started being the most encouraging three hours this franchise has produced since "
      "January, and I have decided I am not going to apologise for that.",
      '<div class="reftable" role="region" tabindex="0" aria-label="San Francisco 49ers at Los Angeles Chargers, Thursday 20 August 2026, SoFi Stadium, 62,156">\n'
      '<table>\n'
      '<caption>San Francisco 49ers at Los Angeles Chargers, Thursday 20 August 2026, SoFi Stadium, 62,156</caption>\n'
      '<thead><tr><th>Team</th><th class="num">1</th><th class="num">2</th><th class="num">3</th><th class="num">4</th><th class="num">Final</th></tr></thead>\n'
      '<tbody>\n'
      '<tr><td><b>San Francisco</b></td><td class="num">0</td><td class="num">20</td><td class="num">7</td><td class="num">14</td><td class="num"><b>41</b></td></tr>\n'
      '<tr><td>Los Angeles</td><td class="num">0</td><td class="num">3</td><td class="num">6</td><td class="num">8</td><td class="num"><b>17</b></td></tr>\n'
      '</tbody>\n</table>\n</div>',
      "<b>Start with the play, because everybody is going to be talking about the play.</b> "
      "Second quarter. Chargers punt. Jacob Cowing fields it, and instead of the little "
      "four yard fair catch shuffle we have watched from this return unit for two years, "
      "he takes one step, finds a crease that should not have been there, and he is gone. "
      "Eighty three yards. Nobody laid a hand on him after the first fifteen.",
      "You have to understand what that is for him. Cowing lost an entire season to a "
      "hamstring. All of it. He came in with the kind of speed that makes coaches talk in "
      "italics, and then he spent a year on a table instead of a field, and if you have "
      "followed this roster at all you know that is usually where the story quietly ends. "
      "Instead he stood there afterwards and called it a special moment, and Kyle "
      "Shanahan, who compliments almost nothing in August, called it a big time play.",
      "Eighty three yards, from a man who did not play a snap last year. That is the whole "
      "reason preseason exists.",
      "<b>Now the part I could not stop thinking about, which is the run game.</b> A "
      "hundred and forty six rushing yards. Against a Harbaugh front. With Christian "
      "McCaffrey standing on the sideline in a hat after taking warmups and getting shut "
      "down with tightness, which after {rbroom} is exactly the sentence that ruins my "
      "week.",
      "It did not matter. Sincere McCormick took six carries for fifty three yards and "
      "walked in from seven. Khalil Herbert punched one in from a yard out. Adrian "
      "Martinez, the quarterback, ran nine yards for another one. Three different men, "
      "three different rushing touchdowns, on a night when the back who is supposed to do "
      "all of that was in street clothes.",
      '<div class="reftable" role="region" tabindex="0" aria-label="Team statistics, 49ers at Chargers, 20 August 2026">\n'
      '<table>\n'
      '<caption>Team statistics, 49ers at Chargers, 20 August 2026</caption>\n'
      '<thead><tr><th>&nbsp;</th><th class="num">San Francisco</th><th class="num">Los Angeles</th></tr></thead>\n'
      '<tbody>\n'
      '<tr><td>Total yards</td><td class="num"><b>321</b></td><td class="num">229</td></tr>\n'
      '<tr><td>Rushing yards</td><td class="num"><b>146</b></td><td class="num">68</td></tr>\n'
      '<tr><td>Passing yards</td><td class="num"><b>175</b></td><td class="num">161</td></tr>\n'
      '<tr><td>Time of possession</td><td class="num"><b>32:56</b></td><td class="num">27:04</td></tr>\n'
      '<tr><td>Penalties</td><td class="num">&nbsp;</td><td class="num">7</td></tr>\n'
      '<tr><td>Punts</td><td class="num">&nbsp;</td><td class="num">8</td></tr>\n'
      '</tbody>\n</table>\n</div>',
      "Sixty eight rushing yards for them. A hundred and forty six for us. That is not a "
      "preseason fluke. That is one offensive line getting movement and the other one not "
      "getting it, for three straight hours, through four different sets of bodies.",
      "<b>Brock Purdy played one drive and I have nothing to complain about.</b> Four of "
      "six for twenty nine yards, moved the ball, the drive stalled, they punted, he put "
      "his coat on. That is the correct amount of Brock Purdy in a game that does not "
      "count, and if you were hoping for more you have not been paying attention to how "
      "Shanahan handles his quarterback in August. Mac Jones came in and went six of "
      "thirteen for eighty nine, which is fine. Nobody signed Mac Jones to be interesting.",
      "Across the field, Justin Herbert took the opening series, threw one completion for "
      "nine yards to Charlie Kolar, and went three and out. That was his night. Trey "
      "Lance, who some of you still have complicated feelings about, went ten of sixteen "
      "for seventy three, which is a lot of completions for not very many yards and tells "
      "you roughly everything about how that offence looked.",
      '<div class="reftable" role="region" tabindex="0" aria-label="Quarterbacks, 49ers at Chargers, 20 August 2026">\n'
      '<table>\n'
      '<caption>Quarterbacks, 49ers at Chargers, 20 August 2026</caption>\n'
      '<thead><tr><th>Quarterback</th><th class="num">Comp</th><th class="num">Att</th><th class="num">Yds</th></tr></thead>\n'
      '<tbody>\n'
      '<tr><td><b>Brock Purdy, SF</b></td><td class="num">4</td><td class="num">6</td><td class="num">29</td></tr>\n'
      '<tr><td>Mac Jones, SF</td><td class="num">6</td><td class="num">13</td><td class="num">89</td></tr>\n'
      '<tr><td>Justin Herbert, LAC</td><td class="num">1</td><td class="num">2</td><td class="num">9</td></tr>\n'
      '<tr><td>Trey Lance, LAC</td><td class="num">10</td><td class="num">16</td><td class="num">73</td></tr>\n'
      '</tbody>\n</table>\n</div>',
      "<b>De&rsquo;Zhaun Stribling had four catches for forty six yards and most of them "
      "moved the chains.</b> I have been loud about this kid since camp opened and I am "
      "going to keep being loud about him. Everybody spent draft weekend telling us he was "
      "a reach, and {stribling} has been the most reliable third down target on this "
      "roster for a month. Four catches, several of them on third down, in August, in a "
      "stadium that is not his.",
      "KhaDarel Hodge matched him with four for forty six, which is a nice thing to be "
      "able to say about {hodge} this soon after he signed. Jordan Watkins caught three "
      "for forty one and took one in from seventeen. That is a receiver room where the "
      "front half is hurt and the back half went out and produced anyway.",
      "<b>The special teams unit had the best night of anybody.</b> Beyond the punt "
      "return, Nick Martin knocked the ball loose on a kickoff return in the fourth "
      "quarter and Hodge fell on it. Eddy Pineiro hit from forty eight and forty five and "
      "did not miss an extra point in five tries. If you have watched this franchise lose "
      "games in January because of a kicker and a return unit, and you have, then you "
      "understand why a quiet, clean, occasionally violent night from that phase of the "
      "team is worth more to me than any throw Purdy could have made.",
      "<b>Now the honest column, because I am not going to pretend it was perfect.</b> "
      "Adrian Martinez threw a ball into the flat in the third quarter and Junior Colson "
      "picked it and walked sixteen yards into the end zone untouched. Untouched. Nobody "
      "within five yards of him. That is the kind of play that gets a young quarterback "
      "cut in about ten days, and it was the only genuinely bad thing the offence did all "
      "night. Martinez then went out and scored twice more, once with his legs and once on "
      "the throw to Watkins, which is either resilience or a complete absence of memory, "
      "and at his age those are the same thing.",
      "Credit where it is due, too, because Colson had lost his own entire season to a "
      "shoulder and that was his first live football in a year. Two men on that field came "
      "back from a lost year and both of them scored. Say what you want about August. That "
      "is a good night for football.",
      "<b>The Chargers beat themselves in a way that should worry them.</b> Seven "
      "penalties, four of them on offence, and the flags kept landing on the plays that "
      "actually worked. An eighteen yard throw from Lance to Oronde Gadsden came back on "
      "an illegal shift. A Lance run came back. A twenty one yard run from Keaton Mitchell "
      "came back on an illegal formation. A Kimani Vidal run came back on another shift. "
      "Eight punts. Their left tackle went out in the second quarter and never came back. "
      "Harbaugh teams do not usually look like that, and if you enjoyed watching a "
      "Harbaugh sideline boil over about procedural penalties for three quarters, well, so "
      "did I, and I should probably examine that at some point.",
      "<b>So what does any of it mean.</b> Nothing, technically. It is a preseason game. "
      "The starters played about a dozen snaps between them. McCaffrey did not dress, "
      "George Kittle is still working his way back from the Achilles, Nick Bosa is being "
      "handled like porcelain, and most of the first team defence watched this in a "
      "headset.",
      "Here is what I think it means anyway. This roster is deep in the exact places it "
      "has not been deep in years. The third and fourth running backs gained yards against "
      "real defenders. The fifth and sixth receivers caught the ball on third down. The "
      "return game, which has been a genuine liability, produced eighty three yards on one "
      "play. Every one of those is a September problem being solved in August, and for a "
      "team that has spent two seasons getting dismantled by its own injury report, depth "
      "is not a luxury item. It is the whole season.",
      "One and one in the preseason, which means nothing, and the full picture of who is "
      "healthy and who is not is on the {depth}. Week 1 is at the Rams in Melbourne on the "
      "tenth of September, which is still the strangest sentence in {melbourne}, and the "
      "whole year is laid out in the {sched}. Everything else lives on the {hub}.",
      "But for one Thursday night in Los Angeles, in a building belonging to the coach who "
      "used to be ours, the 49ers were faster, tougher, better coached and considerably "
      "more fun than the other team, and a kid who spent a year on a training table ran a "
      "punt eighty three yards. Enjoy it. We do not get many of these in August.",
     ],
     links={'preview': ('49ers-chargers-thursday-harbaugh-return-kittle-achilles-recovery.html',
                        'all of last week'),
            'rbroom': ('49ers-running-back-room-gutted-mccaffrey-tightness-bosa-soreness-kittle.html',
                       'the state of the running back room'),
            'stribling': ('49ers-dezhaun-stribling-reach-draft-grade-critics-wrong-2026.html',
                          'the kid everybody called a reach'),
            'hodge': ('49ers-khadarel-hodge-veteran-receiver-signing-august-2026.html',
                      'the veteran they brought in'),
            'depth': ('49ers-2026-roster-depth-chart.html', 'depth chart page'),
            'melbourne': ('49ers-rams-melbourne-nfl-first-game-australia.html',
                          'the Australia trip'),
            'sched': ('49ers-2026-schedule-season-hub.html', 'season schedule hub'),
            'hub': ('../49ers.html', '49ers hub')},
     related=[('49ers-chargers-thursday-harbaugh-return-kittle-achilles-recovery.html', '49ers',
               'Harbaugh Comes Back Thursday, and Kittle Finally Sounds Like Himself'),
              ('49ers-dezhaun-stribling-reach-draft-grade-critics-wrong-2026.html', '49ers',
               'De' + "'" + 'Zhaun Stribling Was Not a Reach and the Grades Were Wrong'),
              ('49ers-2026-schedule-season-hub.html', '49ers',
               'The 2026 49ers Schedule, Week by Week')]),
dict(slug='raiders-texans-22-20-oconnell-mendoza-pick-six-preseason-august-20',
     section='NFL', tag='Raiders', hub='NFL',
     title='Raiders 22, Texans 20: The No. 1 Pick Threw a Pick Six',
     h1="Fernando Mendoza Threw a Pick Six on His Third Pass, Aidan O'Connell Cleaned Up the Rest of It, and the Raiders Won 22 to 20 in Houston",
     dek="Twenty two points, three touchdowns, one made extra point out of three, and a "
         "one yard sneak with fourteen seconds left. The most Raiders win imaginable, and "
         "the rookie has a lot of film to sit through.",
     desc="Raiders 22, Texans 20: Fernando Mendoza threw a pick six on his third pass and "
          "Aidan O'Connell snuck one in from a yard out with fourteen seconds left.",
     date='2026-08-20',
     card=('raiders', '22 to 20 in Houston', 'The rookie threw a pick six, the backup won it'),
     body=[
      "Here is the thing about watching this team from up here, three states and one very "
      "bitter divorce away from where they used to play: you never stop reading the box "
      "score. You tell yourself you are done. You are not done. So on Thursday night, "
      "while the other game involving a California team was busy being a party, the "
      "Raiders were in Houston assembling the single most Raiders sequence of events "
      "available to a football team, and yes, obviously, we read all of it.",

      "They fell behind seventeen to nothing in the first quarter. The first overall pick "
      "in the draft threw a pick six on his third professional pass. And then they won the "
      "game, twenty two to twenty, on a one yard quarterback sneak from Aidan O'Connell "
      "with fourteen seconds on the clock. If you had told a room full of people in 2003 "
      "that this would be the shape of a Raiders night in 2026, nobody would have blinked. "
      "The uniform changed cities. The genre did not.",

      '<div class="reftable" role="region" tabindex="0" aria-label="Las Vegas Raiders at Houston Texans, Thursday 20 August 2026">\n'
      '<table>\n'
      '<caption>Las Vegas Raiders at Houston Texans, Thursday 20 August 2026</caption>\n'
      '<thead><tr><th>Team</th><th class="num">1</th><th class="num">2</th><th class="num">3</th><th class="num">4</th><th class="num">Final</th></tr></thead>\n'
      '<tbody>\n'
      '<tr><td><b>Las Vegas</b></td><td class="num">0</td><td class="num">3</td><td class="num">7</td><td class="num">12</td><td class="num"><b>22</b></td></tr>\n'
      '<tr><td>Houston</td><td class="num">17</td><td class="num">3</td><td class="num">0</td><td class="num">0</td><td class="num"><b>20</b></td></tr>\n'
      '</tbody>\n</table>\n</div>',

      "<b>Start with the pick six, because that is what everybody is going to remember.</b> "
      "Fernando Mendoza is the Heisman winner who took Indiana to a national championship "
      "and then went first overall, and this was supposed to be the night he started "
      "looking like all of that. Third pass of the game. Wade Woodaz reads it, takes it "
      "eighty yards the other way, and it is fourteen to nothing before the rookie has "
      "completed anything worth writing down. Woody Marks had already run one in from "
      "twenty. Ka'imi Fairbairn tacked on from fifty one. Seventeen points in a first "
      "quarter, against a defense that is supposed to be the finished half of this roster.",

      "Mendoza finished eight of fifteen for eighty six yards with the interception, a "
      "passer rating of forty two point six, and a first half only workload. Afterwards he "
      "said there is a lot more learning to do, that this level is a whole step further "
      "and the margins are so small that one tiny mistake can lead to catastrophe. That is "
      "a rookie describing his own pick six with more composure than most veterans manage, "
      "and honestly it is the most encouraging thing he did all night.",

      "<b>What actually won the game.</b> O'Connell came out for the second half and went "
      "fifteen of twenty four for a hundred and sixty six yards with nothing given away, "
      "and the run game finally turned over. Mike Washington Jr. nine carries for fifty "
      "six. Dylan Laube six for thirty seven and a four yard touchdown. Dare Ogunbowale "
      "four for thirty five and a nineteen yard touchdown. A hundred and fifty nine "
      "rushing yards is not nothing when the entire premise of a Kubiak offense is that "
      "you are supposed to be able to hand the ball off and mean it.",

      '<div class="reftable" role="region" tabindex="0" aria-label="Team statistics, Raiders at Texans, 20 August 2026">\n'
      '<table>\n'
      '<caption>Team statistics, Raiders at Texans, 20 August 2026</caption>\n'
      '<thead><tr><th>&nbsp;</th><th class="num">Las Vegas</th><th class="num">Houston</th></tr></thead>\n'
      '<tbody>\n'
      '<tr><td>Total yards</td><td class="num"><b>412</b></td><td class="num">219</td></tr>\n'
      '<tr><td>Passing yards</td><td class="num"><b>241</b></td><td class="num">141</td></tr>\n'
      '<tr><td>Rushing yards</td><td class="num"><b>159</b></td><td class="num">78</td></tr>\n'
      '<tr><td>Turnovers</td><td class="num"><b>1</b></td><td class="num">2</td></tr>\n'
      '</tbody>\n</table>\n</div>',

      "<b>Four hundred and twelve yards.</b> That is the number that survives the night. "
      "Houston finished with two hundred and nineteen. The Raiders nearly doubled up a "
      "playoff team on total offense with their starting quarterback standing on the "
      "sideline in a cap, and they still needed a sneak in the final minute, because the "
      "kicking went sideways in a way that would be funny if it were not the sort of thing "
      "that loses actual games in October. Matt Gay hit from fifty two. Kansei Matsuzawa "
      "went one for three on extra points. Three touchdowns and one extra point is how a "
      "team scores twenty two.",

      '<div class="reftable" role="region" tabindex="0" aria-label="Quarterbacks, Raiders at Texans, 20 August 2026">\n'
      '<table>\n'
      '<caption>Quarterbacks, Raiders at Texans, 20 August 2026</caption>\n'
      '<thead><tr><th>Quarterback</th><th class="num">Comp</th><th class="num">Att</th><th class="num">Yds</th><th class="num">Int</th></tr></thead>\n'
      '<tbody>\n'
      '<tr><td><b>Aidan O&rsquo;Connell, LV</b></td><td class="num">15</td><td class="num">24</td><td class="num">166</td><td class="num">0</td></tr>\n'
      '<tr><td>Fernando Mendoza, LV</td><td class="num">8</td><td class="num">15</td><td class="num">86</td><td class="num">1</td></tr>\n'
      '<tr><td>C.J. Stroud, HOU</td><td class="num">4</td><td class="num">6</td><td class="num">27</td><td class="num">0</td></tr>\n'
      '<tr><td>Davis Mills, HOU</td><td class="num">11</td><td class="num">15</td><td class="num">93</td><td class="num">0</td></tr>\n'
      '<tr><td>Brett Rypien, HOU</td><td class="num">6</td><td class="num">10</td><td class="num">44</td><td class="num">1</td></tr>\n'
      '</tbody>\n</table>\n</div>',

      "<b>The Kirk Cousins arrangement.</b> He did not play. Most of the starters did not "
      "play, which is the whole reason a rookie was out there throwing his third pass into "
      "traffic in the first place. We got into all of it in {preview} and nothing on "
      "Thursday changes the read: this is a team that spent real money on a quarterback in "
      "his late thirties and then drafted the guy who is going to take the job from him, "
      "and everybody involved has to walk around pretending that is a normal way to build "
      "a football team.",

      "<b>The injuries.</b> Chigozie Anusiem went off on a cart with a knee. Buddy Johnson "
      "took a shot to the shoulder and came back. In August one of those is a story and "
      "one is a footnote, and you do not find out which for about ten days.",

      "<b>Kubiak, afterwards.</b> He said they have another week of playing and that he "
      "does not want anyone to be comfortable in their job. Standard preseason coach "
      "speak, except that this is a roster where the bottom twenty five spots are "
      "genuinely open, and a fifty two yard field goal sharing a night with two missed "
      "extra points is exactly the kind of thing that ends somebody's summer.",

      "<b>Where it leaves them.</b> One and one, in a preseason nobody should read too "
      "closely, with the first overall pick sitting on one bad quarter and one good quote. "
      "Last week they played their actual starters and got run out of their own building "
      "by Arizona, which we wrote up in {week1}. This week they sat everybody and won. "
      "Preseason is a coin. What you can say is that the ball came out of the backfield "
      "well, the second unit did not fold at seventeen to nothing, and O'Connell is still "
      "the most competent thing on that quarterback depth chart even when he is nominally "
      "third in line.",

      "And for the record, on the very same night, the team that stayed put hung forty one "
      "on the Chargers at SoFi. We wrote that one up as well, {niners}, and it is a much "
      "more enjoyable read. But this is the Bay Area, and a lot of us have a silver and "
      "black thing buried somewhere that we have never properly dealt with, so here we "
      "are at eleven at night reading a preseason box score out of Houston. The rest of "
      "the league coverage sits on the {hub}.",
     ],
     links={'preview': ('raiders-2026-season-preview-kubiak-cousins-mendoza-jeanty.html',
                        'the season preview'),
            'week1': ('49ers-titans-raiders-cardinals-preseason-recap-rourke-stribling.html',
                      'the week one recap'),
            'niners': ('49ers-chargers-41-17-cowing-punt-return-preseason-august-20.html',
                       '49ers 41, Chargers 17'),
            'hub': ('../nfl.html', 'NFL page')},
     related=[('raiders-2026-season-preview-kubiak-cousins-mendoza-jeanty.html', 'NFL',
               'The 2026 Raiders: Kubiak, Cousins, Mendoza and Jeanty'),
              ('49ers-chargers-41-17-cowing-punt-return-preseason-august-20.html', '49ers',
               '49ers 41, Chargers 17: The Best Night of the Summer'),
              ('49ers-titans-raiders-cardinals-preseason-recap-rourke-stribling.html', '49ers',
               'The 49ers Sat Everybody. The Raiders Played Everybody and Lost Worse.')]),
# --------------------------------------------------------------- Raiders preseason finale
dict(slug='49ers-raiders-18-12-pineiro-six-field-goals-preseason-finale',
     section='49ers', tag='49ers', hub='49ers',
     title='49ers 18, Raiders 12: A Kicker Won a Football Game',
     h1="49ers 18, Raiders 12: Eddy Pineiro Kicked Six and Won the Whole Thing",
     dek="Six field goals, none missed, one from 59, and a defense that did not let the "
         "Raiders in the end zone once. The summer ends 2-1 and the cuts come Sunday.",
     desc="49ers 18, Raiders 12 in the preseason finale. Eddy Pineiro went 6-for-6 "
          "including a 59 yarder and the defense allowed no touchdowns.",
     date='2026-08-27',
     card=('49ers', 'Six For Six', 'Pineiro kicks every point in an 18-12 win at Allegiant'),
     body=[
      "<b>Eighteen points, zero touchdowns, and I stayed up for all of it.</b> That's the "
      "honest summary of a Thursday night in Las Vegas that had no business being as fun "
      "as it was. Eddy Pineiro scored every single point the 49ers put on the board, six "
      "field goals on six attempts, and the defense would not let the Raiders into the "
      "end zone once. Final was 18-12. Four field goals for them, six for us, and that "
      "was the football game.",

      "The distances, because they matter: 24, 25, 48, 51, 54, 59. Three of them from "
      "fifty plus. The 59 was the one where I actually got off the couch, which is a "
      "ridiculous thing to do in the last week of August, and I did it anyway. There's a "
      "specific kind of calm that comes over you when a kicker just is not going to miss, "
      "and this team has spent a lot of recent Januarys with the opposite feeling, so let "
      "me have this one.",

      "Adrian Martinez ran the offense for most of the night and moved it well enough to "
      "keep handing Pineiro the ball inside the forty, which in preseason terms is close "
      "to a compliment. Jordan Watkins was the best skill player on the field for either "
      "side, four catches for 64 and another 21 on three carries, and he keeps doing this "
      "in games that supposedly do not count. Jordan James got his first work of the "
      "summer after the ribs, eight carries for 35 and a 20 yard catch, and he looked like "
      "somebody who has been waiting three weeks to hit somebody.",

      "The defense is what I keep thinking about. Fernando Mendoza threw an interception "
      "to Tatum Bethune. Darrell Luter Jr. tipped a ball into that pick and broke up "
      "another one. Keion White and Ogbo Okoronkwo both got home for sacks. And Jaden "
      "Dugger, a rookie linebacker most of this fan base could not have picked out of a "
      "lineup in July, led everybody with ten tackles and was in the backfield on back to "
      "back plays in the second half. Ten tackles in August is how a guy makes a roster.",

      "Now the part nobody enjoys. The cuts are Sunday. Fifty three, and this summer "
      "produced more players who deserve a spot than there are spots, which sounds like a "
      "good problem until you remember that a real person gets a phone call. Dugger played "
      "himself onto something. Watkins has been the most consistent guy on the field for "
      "three straight weeks. Somebody who was good enough is going to be gone by Sunday "
      "night and we'll all forget his name by October.",

      "So the preseason closes at 2-1. It means nothing and I'll take it anyway. Two weeks "
      "ago they hung forty one on the Chargers, which we wrote up as {chargers}, and that "
      "was the loud one. This was the strange one. A silver and black building, a Bay Area "
      "kicker going perfect, and a defense that made Kirk Cousins and the first overall "
      "pick settle for field goals all night.",

      "Melbourne is next. Actually next, real football, September 10, and a bunch of us "
      "are going to be awake at hours that make no sense for a Week 1 game in Australia. "
      "The full slate is on the {schedule}, the rest of the coverage sits on the {hub}, "
      "and I'm going to go to bed thinking about a 59 yard field goal in a game that did "
      "not count.",
     ],
     links={'chargers': ('49ers-chargers-41-17-cowing-punt-return-preseason-august-20.html',
                         '49ers 41, Chargers 17'),
            'schedule': ('49ers-2026-schedule-season-hub.html', '2026 schedule hub'),
            'hub': ('../49ers.html', '49ers hub')},
     related=[('49ers-chargers-41-17-cowing-punt-return-preseason-august-20.html', '49ers',
               '49ers 41, Chargers 17: The Best Night of the Summer'),
              ('49ers-2026-schedule-season-hub.html', '49ers Schedule',
               'The 2026 49ers Schedule, Week by Week'),
              ('49ers-2026-roster-depth-chart.html', '49ers Roster',
               'The 2026 49ers Roster and Depth Chart')]),
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
