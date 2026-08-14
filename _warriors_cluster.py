#!/usr/bin/env python3
"""_warriors_cluster.py - the Warriors authority foundation.

The archive had seven Warriors pieces and all of them were arguments: the era ending,
the front office failing Curry, the LeBron hypothetical, Kerr and Kuminga. Good columns,
but nothing anyone searching for a fact would ever land on. This adds the four pages
that hold facts, and leaves the arguments where they are.

Deliberately NOT duplicated:
  warriors-front-office-failures-curry-exit-not-preposterous  - opinion on the front
      office, so the roster-construction piece here is about the cap sheet instead
  warriors-out-of-easy-answers      - the era-ending argument
  lebron-curry-warriors-legacy      - the hypothetical
  warriors-kerr-kuminga-role-handling - player development
  warriors-championship-history / 73-9 / flashback-klay - the history is already covered

No schedule hub yet: the 2026-27 NBA schedule is not out. Listed as a gap rather than
guessed at.

  python _warriors_cluster.py [--check]
"""
import os, re, sys, subprocess
import _college_cluster as CC

ROOT = os.path.dirname(os.path.abspath(__file__))

ARTICLES = [
# ------------------------------------------------------------ 1. Curry statistical evergreen
dict(slug='stephen-curry-career-records-three-pointers',
     section='Warriors', tag='Warriors', hub='Warriors',
     title='Stephen Curry by the Numbers: The Records He Already Owns',
     h1="Stephen Curry by the Numbers: The Records He Already Owns, and the Ones Still Moving",
     dek="The three-point record is not a record any more, it is a category he invented "
         "and then left. A permanent page for the numbers, updated as they keep going.",
     desc="Stephen Curry's career records: 4,248 three-pointers, the night he passed Ray "
          "Allen, the first player to 4,000, and how far ahead of the field he actually is.",
     date='2026-08-08',
     card=('warriors', 'Curry by the Numbers', 'The records he owns and the gap behind him'),
     body=[
      "There is a version of the Stephen Curry argument that gets exhausting - the "
      "greatest shooter ever, the most important offensive player of his generation, all "
      "of it true and all of it repeated until it stops landing. This page is the other "
      "version. Just the numbers, kept straight, updated as they move.",
      "<b>The three-point record.</b> Curry has made 4,248 career three-pointers. He took "
      "the all-time lead on 14 December 2021, at Madison Square Garden, when he hit his "
      "2,974th and passed Ray Allen. Sit with those two numbers together for a second. He "
      "broke the record, and then made another twelve hundred and seventy on top of it. "
      "The record was not a finish line, it was a checkpoint he went through at speed.",
      "<b>The gap.</b> The two players closest to him are Damian Lillard at 2,785 and his "
      "old running mate {klay} at 2,657. Both are approaching three thousand. Curry is "
      "past four thousand. That is not a lead, it is a different unit of measurement - "
      "somebody would need to make thirteen hundred more threes than Lillard has managed "
      "in a full career just to draw level.",
      "<b>The 4,000 club.</b> It has one member. Curry became the first player in the "
      "history of the sport to reach four thousand career threes, which is the kind of "
      "milestone that only exists because one person made it necessary to count that "
      "high. When he started, nobody built a leaderboard that went there.",
      "<b>What is still moving.</b> The three-point number obviously, and every game he "
      "plays pushes the eventual record further out of reach for whoever comes next. The "
      "consecutive-games-with-a-three streak is its own running record and he has broken "
      "his own mark more than once. Beyond the shooting, the career totals - points, "
      "assists, the franchise records that were Rick Barry's and Wilt's before him - keep "
      "climbing as long as he is upright.",
      "<b>What the numbers do not say.</b> They do not say what it did to the sport, "
      "which is the part that will matter in fifty years. Every fourteen-year-old pulling "
      "up from four feet behind the line is doing it because of him, and the reason NBA "
      "offenses look the way they do now is downstream of one player proving the maths "
      "worked. That is not a statistic. It is the actual legacy, and it is already "
      "settled regardless of what the {future} looks like.",
      "<b>The honest caveat.</b> He is thirty-eight, playing a position that punishes "
      "thirty-eight, on a roster that has been rebuilt around him twice. The numbers keep "
      "going up because he keeps playing, and the day that stops, they stop. Which is why "
      "the argument about {frontoffice} is not sentimental - every season he is asked to "
      "carry a flawed roster is a season of these numbers spent on a team that could not "
      "win with them.",
      "This page gets updated as the totals move. The era-level argument is in "
      "{easyanswers}, the history is in {history}, and the rest is on the {hub}.",
     ],
     links={'klay': ('flashback-klay-37-point-quarter.html', 'Klay Thompson'),
            'future': ('warriors-2026-27-season-outlook.html', 'the current roster'),
            'frontoffice': ('warriors-front-office-failures-curry-exit-not-preposterous.html',
                            'the front office'),
            'easyanswers': ('warriors-out-of-easy-answers.html', 'our column on the end of the era'),
            'history': ('warriors-championship-history.html', 'the championship history'),
            'hub': ('../warriors.html', 'Warriors hub')},
     related=[('warriors-2026-27-season-outlook.html', 'Warriors', 'The 2026-27 Warriors: What This Roster Actually Is'),
              ('warriors-championship-history.html', 'Warriors', 'From Rick Barry to the Splash Brothers'),
              ('warriors-73-9-best-record-ever-added-durant.html', 'Warriors', '73-9 and Then They Added Durant')]),

# ------------------------------------------------------------ 2. Roster / depth chart
dict(slug='warriors-2026-27-roster-depth-chart',
     section='Warriors', tag='Warriors', hub='Warriors',
     title='The 2026-27 Warriors Roster and Depth Chart',
     h1="The 2026-27 Warriors Roster and Depth Chart, Position by Position",
     dek="Who starts, who comes off the bench, who is hurt, and what the roster looks "
         "like once you account for the two knees nobody wants to talk about.",
     desc="A position-by-position look at the 2026-27 Warriors: projected starters, the "
          "bench, the injury picture, and where this roster is genuinely thin.",
     date='2026-08-08',
     card=('warriors', 'Roster & Depth', 'Starters, bench, and the two knees nobody mentions'),
     body=[
      "A depth chart in the offseason is a projection with a short shelf life, so treat "
      "this as a running record. It gets updated as the roster moves.",
      "<b>Projected starters.</b> {curry} at point guard, Brandin Podziemski at shooting "
      "guard, Gui Santos at small forward, Draymond Green at power forward, and Kristaps "
      "Porzingis at centre. Read that lineup twice, because the two names most people "
      "would expect to see are not in it.",
      "<b>The two knees.</b> Jimmy Butler and Moses Moody have both been left out of "
      "lineup projections because of knee injuries. Butler is the second-highest-paid "
      "player on the roster. A starting five that does not include him is not a plan, it "
      "is a contingency, and how quickly that changes is the single biggest variable in "
      "this team's season.",
      "<b>Guard.</b> Curry, still the entire offense's centre of gravity at thirty-eight. "
      "Podziemski has grown into a real rotation piece rather than a project. Moody at "
      "$12.5 million is the sort of contract that looks fine when he plays and awkward "
      "when he does not.",
      "<b>Wing.</b> Santos in the projected starting five is the story here - a player "
      "on a $4.6 million deal starting for a team paying two players a combined $119 "
      "million tells you exactly where the cap pressure landed. Butler when healthy "
      "changes this room entirely.",
      "<b>Big.</b> Porzingis at centre, with Al Horford re-signed at $5.9 million behind "
      "him. Horford at this stage of his career is a specific kind of useful: he knows "
      "where to be, he can still shoot it, and he does not need plays run for him. On a "
      "roster this top-heavy, that is worth more than the number suggests.",
      "<b>Draymond.</b> Still the defensive organiser, still on $27.6 million, still the "
      "player whose availability and temperament decide what the defence is capable of. "
      "There is no version of a good Warriors defence that does not run through him.",
      "<b>The rookie.</b> Yaxel Lendeborg arrived in the draft. Rookie minutes on a team "
      "trying to win now are earned rather than given, and {kuminga} is the cautionary "
      "tale about how this coaching staff handles young players who are not immediately "
      "ready.",
      "<b>Where it runs thin.</b> Everywhere behind the top six. The cap sheet - "
      "{cap} goes through it in detail - means the back half of this roster is minimum "
      "contracts and hope. If Curry, Green or Porzingis misses time, there is no "
      "replacement on the books, only a redistribution of minutes to players who were "
      "not signed to play them.",
      "The structural read is in the {outlook}, the numbers behind Curry are on {records}, "
      "and everything else is on the {hub}.",
     ],
     links={'curry': ('stephen-curry-career-records-three-pointers.html', 'Stephen Curry'),
            'kuminga': ('warriors-kerr-kuminga-role-handling.html', 'the Kuminga situation'),
            'cap': ('warriors-roster-construction-cap-sheet-2026-27.html', 'our cap piece'),
            'outlook': ('warriors-2026-27-season-outlook.html', 'season outlook'),
            'records': ('stephen-curry-career-records-three-pointers.html', 'the Curry page'),
            'hub': ('../warriors.html', 'Warriors hub')},
     related=[('warriors-2026-27-season-outlook.html', 'Warriors', 'The 2026-27 Warriors: What This Roster Actually Is'),
              ('warriors-roster-construction-cap-sheet-2026-27.html', 'Warriors', 'What $147 Million Actually Bought'),
              ('warriors-kerr-kuminga-role-handling.html', 'Warriors', 'How Steve Kerr Actually Handled Jonathan Kuminga')]),

# ------------------------------------------------------------ 3. Season outlook
dict(slug='warriors-2026-27-season-outlook',
     section='Warriors', tag='Warriors', hub='Warriors',
     title='The 2026-27 Warriors: What This Roster Actually Is',
     h1="The 2026-27 Warriors: What This Roster Actually Is, and What It Can Realistically Be",
     dek="A thirty-eight-year-old point guard, two enormous contracts attached to "
         "uncertain knees, and a supporting cast assembled at the minimum. The honest "
         "version of the season ahead.",
     desc="What the 2026-27 Warriors realistically are: the Curry-Butler-Green core, the "
          "injury questions, the cap reality, and the range of outcomes for the season.",
     date='2026-08-08',
     card=('warriors', 'The 2026-27 Warriors', 'A 38-year-old point guard and two uncertain knees'),
     body=[
      "Here is the sentence that governs this season, and everything else is a footnote "
      "to it: the Golden State Warriors are paying three players roughly $147 million, "
      "two of them are on the wrong side of their peak and one of them has a knee that "
      "kept him out of the projected starting lineup.",
      "<b>What this team is.</b> A Curry team, still. {curry} at thirty-eight remains the "
      "gravitational centre of everything the offense does, and no amount of roster "
      "churn changes the fundamental design: he moves, the defence panics, somebody gets "
      "an open shot. The question was never whether that still works. It is how many "
      "nights a season he can do it.",
      "<b>What was added.</b> Kristaps Porzingis projects into the starting five at "
      "centre, Al Horford came back on a modest deal, and Yaxel Lendeborg arrived in the "
      "draft. That is not a roster overhaul. It is a team trying to put competent, "
      "low-maintenance professionals around a core it cannot afford to change.",
      "<b>What has to happen.</b> Jimmy Butler's knee. He is the second-highest-paid "
      "player here and he is not in the projected starting five. A healthy Butler makes "
      "this a team that can win a playoff series, because he is the only other player on "
      "the roster who can create a shot when the offense breaks down in the fourth "
      "quarter. An unhealthy Butler makes this a team asking a thirty-eight-year-old to "
      "produce forty minutes of miracle every night.",
      "<b>The realistic range.</b> The ceiling, with health, is a team nobody wants to "
      "draw in the first round and that can beat anyone in a seven-game series where "
      "Curry gets hot. The floor, without health, is the play-in and another spring of "
      "the same argument. There is no version of this roster that wins sixty games, and "
      "anyone selling that is selling nostalgia.",
      "<b>The part nobody in the building will say out loud.</b> This is a bridge season "
      "for a franchise that does not have a bridge. The cap sheet is committed, the draft "
      "capital is not abundant, and the plan appears to be to keep Curry surrounded by "
      "professionals until it stops working. {frontoffice} is the argument about whether "
      "that is good enough, and it is not a settled one around here.",
      "<b>What to actually watch.</b> Butler's availability first. Then whether "
      "Podziemski and Santos can genuinely start on a competitive team, because if they "
      "can, the cap problem gets survivable. Then Draymond's minutes and temperament, "
      "because the defence has no organising principle without him. And underneath it "
      "all, whether {records} keep climbing at the rate they have, because those numbers "
      "are the reason anyone is still watching.",
      "The full roster picture is on the {depth}, the money is in {cap}, and the rest of "
      "our coverage is on the {hub}.",
     ],
     links={'curry': ('stephen-curry-career-records-three-pointers.html', 'Stephen Curry'),
            'frontoffice': ('warriors-front-office-failures-curry-exit-not-preposterous.html',
                            'Our front office column'),
            'records': ('stephen-curry-career-records-three-pointers.html', "Curry's records"),
            'depth': ('warriors-2026-27-roster-depth-chart.html', 'depth chart page'),
            'cap': ('warriors-roster-construction-cap-sheet-2026-27.html', 'the cap breakdown'),
            'hub': ('../warriors.html', 'Warriors hub')},
     related=[('warriors-2026-27-roster-depth-chart.html', 'Warriors', 'The 2026-27 Warriors Roster and Depth Chart'),
              ('warriors-roster-construction-cap-sheet-2026-27.html', 'Warriors', 'What $147 Million Actually Bought'),
              ('warriors-out-of-easy-answers.html', 'Warriors', 'The Warriors Are Out of Easy Answers')]),

# ------------------------------------------------------------ 4. Cap sheet / construction
dict(slug='warriors-roster-construction-cap-sheet-2026-27',
     section='Warriors', tag='Warriors', hub='Warriors',
     title='What $147 Million Actually Bought the Warriors',
     h1="What $147 Million in Salary Actually Bought the Warriors, and Why the Rest of the Roster Looks Like That",
     dek="Curry, Butler and Green account for the overwhelming majority of the payroll. "
         "Everything strange about this roster is downstream of that one fact.",
     desc="A look at the 2026-27 Warriors cap sheet: what Curry, Butler and Green cost, "
          "and why the rest of the roster is minimum contracts and draft picks.",
     date='2026-08-08',
     card=('warriors', 'The Cap Sheet', 'Three contracts, and everything downstream of them'),
     body=[
      "Roster construction arguments usually get emotional. This one does not need to. "
      "You can explain almost everything odd about the 2026-27 Warriors with three "
      "numbers off the payroll.",
      "<b>The three numbers.</b> Stephen Curry at $62.5 million. Jimmy Butler at $56.8 "
      "million. Draymond Green at $27.6 million. That is roughly $147 million committed "
      "to three players, two of whom are past their athletic peak and one of whom has a "
      "knee serious enough to keep him out of projected starting lineups.",
      "<b>What that leaves.</b> Moses Moody at $12.5 million is the only other "
      "meaningful salary. After that it is Al Horford at $5.9 million, Brandin "
      "Podziemski at $5.6 million, Gui Santos at $4.6 million. Those are not the "
      "contracts of a supporting cast built to win a title. They are the contracts of "
      "players a team can afford after it has already spent everything.",
      "<b>Why Santos is projected to start.</b> Not because a $4.6 million forward beat "
      "out better options. Because there were no better options to sign. When three "
      "contracts eat the payroll, the fourth through ninth men come from the draft, the "
      "minimum, or internal development. That is the whole explanation, and it is also "
      "the reason {kuminga} mattered more than it appeared to at the time - a homegrown "
      "player who develops into a starter is worth more to this specific roster than to "
      "almost any other team in the league.",
      "<b>The bet the front office made.</b> Butler's contract is the tell. Paying that "
      "much for a player of that age is a declaration that the plan is to win now, with "
      "Curry, while there is still a window. That is a defensible bet. It is also a bet "
      "with no hedge: if the knee does not hold, there is no cap space to fix it, no "
      "expiring contract to trade, and no obvious path back to flexibility for years.",
      "<b>What good roster construction looks like from here.</b> Not a blockbuster - "
      "there is nothing to trade with. It looks like the boring version: hit on the "
      "draft picks, develop the players already on the roster, sign the right veterans "
      "at the minimum, and hope Horford-type signings keep outperforming their money. "
      "That is unglamorous and it is genuinely the only route available.",
      "<b>The honest verdict.</b> This is a roster shaped by decisions made three and "
      "four years ago, not by anything happening this summer. The current front office "
      "is playing a hand it was dealt, and {frontoffice} is where we make the argument "
      "about how it got dealt that way. What is not arguable is the arithmetic: $147 "
      "million to three players means everyone else is playing for scale, and a team "
      "built that way needs its stars available. All of them. Most nights.",
      "The projected lineup is on the {depth}, the season read is in the {outlook}, and "
      "the rest is on the {hub}.",
     ],
     links={'kuminga': ('warriors-kerr-kuminga-role-handling.html', 'the Kuminga episode'),
            'frontoffice': ('warriors-front-office-failures-curry-exit-not-preposterous.html',
                            'our front office column'),
            'depth': ('warriors-2026-27-roster-depth-chart.html', 'depth chart page'),
            'outlook': ('warriors-2026-27-season-outlook.html', 'season outlook'),
            'hub': ('../warriors.html', 'Warriors hub')},
     related=[('warriors-2026-27-roster-depth-chart.html', 'Warriors', 'The 2026-27 Warriors Roster and Depth Chart'),
              ('warriors-front-office-failures-curry-exit-not-preposterous.html', 'Warriors', 'The Front Office Keeps Failing Steph Curry'),
              ('warriors-2026-27-season-outlook.html', 'Warriors', 'The 2026-27 Warriors: What This Roster Actually Is')]),

# ------------------------------------------- 5. development failure column, 14 August
dict(slug='warriors-clinging-to-past-cannot-develop-young-players',
     section='Warriors', tag='Warriors', hub='Warriors',
     title='The Warriors Cling to the Past Because They Cannot Build a Future',
     h1="The Warriors Are Clinging to the Past Because They Cannot Develop a Young Player to Save the Franchise",
     dek="Wiseman, the two timelines, Poole, Kuminga, Moody. A decade of draft capital "
         "went into that list, and the plan for 2026-27 is still a 38-year-old point "
         "guard and whichever veterans would take the minimum. That is not loyalty. "
         "That is a franchise that cannot grow its own.",
     desc="Wiseman, the two timelines, Poole, Kuminga, Moody: why the Warriors keep "
          "buying old veterans - because this franchise cannot develop young players.",
     date='2026-08-14',
     card=('warriors', 'Clinging to the Past', 'A franchise that cannot grow its own'),
     body=[
      "Look at the projected starting five for the 2026-27 Golden State Warriors and "
      "tell me what you see. Stephen Curry, thirty-eight. Draymond Green, deep in his "
      "thirties. Kristaps Porzingis, bought. Al Horford, forty, waiting behind him, "
      "bought. Jimmy Butler, the second-highest-paid player on the roster, bought, and "
      "currently not even in the lineup projection because of his knee. This is not a "
      "basketball team. This is a museum with a payroll, and the reason it is a museum "
      "is the thing nobody at that practice facility wants to say into a microphone: "
      "this franchise cannot develop a young player to save its life, and it has been "
      "proving it for six years straight.",
      "Run the list, because the list is damning. James Wiseman, second overall pick, "
      "the highest pick this franchise had held in a generation, handed to a "
      "win-now locker room with no development plan, no G-League runway, no patience, "
      "and shipped out as a salary line. The famous \"two timelines\" - remember that? "
      "The front office stood at a podium and told us they could contend with Curry "
      "and build the next era at the same time, and what we got was neither: the "
      "young timeline never developed and the old timeline paid the luxury tax for "
      "the privilege of watching it not develop. Jordan Poole got his development "
      "year, got paid, got punched, got traded. {kuminga} is the definitive document "
      "of how this coaching staff handles a young player who is not ready-made for "
      "the system - a season-long negotiation that developed nobody and satisfied "
      "no one. And Moses Moody, the quiet one on the list, spent years earning trust "
      "in eight-minute increments, finally got a real contract, and is now hurt. "
      "That is five first-round investments. The return is one rotation player and "
      "four cautionary tales.",
      "And here is the thing about a franchise that cannot grow its own: it has to "
      "buy everything, and it has to buy old, because old is the only thing the "
      "market sells to a team with no cap room and no patience. That is not a "
      "strategy. That is a habit wearing a strategy's clothes. The {cap} shows where "
      "it leads - roughly $147 million tied up in three players on the wrong side of "
      "their peaks, minimum contracts and hope behind them. Porzingis and Horford "
      "and Butler are not a future. They are a very expensive way of postponing the "
      "question the front office has failed to answer since 2020: who is the next "
      "Warrior? Not the next veteran in a Warriors jersey. The next Warrior.",
      "The bitter joke is that the two young players actually starting this year - "
      "Brandin Podziemski and Gui Santos - are not starting because the development "
      "machine worked. They are starting because the cap sheet forced it. Santos at "
      "$4.6 million starts for a team paying two men a combined $119 million, and "
      "the {depth} says the quiet part plainly: that tells you where the pressure "
      "landed, not where the plan succeeded. Podziemski grew into a real player "
      "mostly by refusing not to. When your development success stories are the "
      "guys who developed in spite of you, you do not have a development program. "
      "You have survivors.",
      "Meanwhile the rookie, Yaxel Lendeborg, walks into the exact machine that "
      "chewed up everyone before him: a win-now roster, a coach who trusts veterans "
      "the way the rest of us trust gravity, and minutes that have to be earned "
      "from men making eight figures who are not going to hand them over. Why would "
      "his story end differently? Nothing about the machine has changed. The people "
      "running it have not changed. The only thing that changes is the name on the "
      "cautionary tale.",
      "And the reason this all keeps working - the reason the building sells out and "
      "the questions stay soft - is the past. The banners do the talking. {curry} is "
      "still out there being the only reason to watch, and every night he cooks for "
      "a quarter, the whole operation gets to point at him instead of at the six "
      "years of failed drafts behind him. The dynasty bought this front office a "
      "decade of benefit of the doubt, and as {easyanswers} argued, that grace "
      "period is over. Clinging to Curry is not a plan. It is an anesthetic. It "
      "works right up until the moment he stops playing, and then this franchise "
      "wakes up in the recovery room with no young core, no cap room, no draft "
      "capital, and a two-decade rebuild staring back at it.",
      "I say all of this as somebody who will watch every game, because that is the "
      "curse of it. The past they are clinging to is my past too. I was there for "
      "the parades. But the parade route does not run through 2027, and somebody in "
      "that building needs to act like they know it. Develop somebody. Anybody. "
      "Prove the machine can produce one more Warrior before the last real one "
      "walks off the floor. The {frontoffice} argument is no longer about whether "
      "they have failed Curry. It is about whether they are capable of anything "
      "else. The rest of the coverage is on the {hub}.",
     ],
     links={'kuminga': ('warriors-kerr-kuminga-role-handling.html', 'The Kuminga saga'),
            'cap': ('warriors-roster-construction-cap-sheet-2026-27.html', 'cap sheet'),
            'depth': ('warriors-2026-27-roster-depth-chart.html', 'depth chart'),
            'curry': ('stephen-curry-career-records-three-pointers.html', 'Curry'),
            'easyanswers': ('warriors-out-of-easy-answers.html', 'our column on the end of the era'),
            'frontoffice': ('warriors-front-office-failures-curry-exit-not-preposterous.html',
                            'front office'),
            'hub': ('../warriors.html', 'Warriors hub')},
     related=[('warriors-out-of-easy-answers.html', 'Warriors',
               "The Warriors Are Out of Easy Answers, and That's the Whole Story"),
              ('warriors-kerr-kuminga-role-handling.html', 'Warriors',
               'How Steve Kerr Actually Handled Jonathan Kuminga'),
              ('warriors-front-office-failures-curry-exit-not-preposterous.html', 'Warriors',
               'The Front Office Keeps Failing Steph Curry')]),
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
