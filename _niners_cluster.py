#!/usr/bin/env python3
"""_niners_cluster.py - the 49ers 2026 season content system.

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
      "catching the career volume records - the yardage and touchdown leaderboards belong "
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
      "tries to be useful - what is actually on the roster, and what has to break right.",
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
      "in Week 6, and there is a home game against Minnesota that is not at home at all "
      "- it is in Mexico City. Five prime-time games. The cross-divisional draw is the "
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
      "from the NFC North, AFC East and NFC South - the consequence of finishing third "
      "in the NFC West last season. Five prime-time games, two of them at Levi's.",
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
      "familiar things - health, the line, and whether {preview} holds up once the games "
      "are real.",
      "<b>The stretches that decide it.</b> Any NFL season breaks into three or four "
      "runs, and the ones to circle here are the opening fortnight - Melbourne then Miami "
      "on a short turnaround - and whatever the schedule makers did with the December "
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
      "The MCG is a genuinely great venue - a hundred thousand seats, the most famous "
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
      "London that is not nonsense - a market that had no NFL presence twenty years ago "
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
