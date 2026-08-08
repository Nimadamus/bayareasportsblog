#!/usr/bin/env python3
"""_hub_copy.py - give the team and league hubs something to actually read.

Each hub was a one-line hero over a wall of cards: 130-160 words of unique prose on
pages carrying up to 136 story cards. This adds a short editorial block under the hero
explaining what the hub covers, where that team's season actually is, and which pieces
are worth starting with - with the internal links written into the sentences rather
than bolted on as a list.

Markup reuses what the hubs already have: a <section class="zone">, the existing
sec-head/h2 pattern, and paragraphs. The only inline styles are a reading measure and
the muted body colour already used elsewhere in the codebase. No CSS file is touched,
no card, no hero, no nav, no URL.

  python _hub_copy.py [--check]
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MARK = '<!-- hub intro -->'

P = ('<p style="color:var(--muted);font-size:16px;line-height:1.68;margin:0 0 15px">'
     '%s</p>')


def block(heading, paras):
    body = '\n'.join(P % p for p in paras)
    return ('%s\n<section class="zone"><div class="wrap">\n'
            '<div class="sec-head"><div><h2>%s</h2></div></div>\n'
            '<div style="max-width:72ch">\n%s\n</div>\n</div></section>\n'
            % (MARK, heading, body))


COPY = {
 'giants.html': ('Where the Giants season actually is', [
   'This is the Giants hub: every game recap, every column, and every argument we have '
   'had about this team since the season turned. If you want the short version of 2026, '
   'it is that the Giants spent July losing the games that decide seasons and August '
   'taking themselves apart. They went from hanging around .500 to nineteen games under '
   'it, and the front office answered the way front offices answer that.',
   'The deadline is the spine of the story. <a href="articles/giants-trade-deadline-monday-posey-sell-ramos-arraez-ray.html">Buster '
   'Posey had one decision to make</a> and he made it: <a href="articles/giants-arraez-kilian-traded-phillies-august-3.html">Luis '
   'Arraez went to Philadelphia</a>, <a href="articles/giants-robbie-ray-padres-trade-report-august-3.html">Robbie Ray went to the '
   'Padres</a>, and <a href="articles/giants-heliot-ramos-yankees-mayer-mahle-august-4.html">Heliot Ramos and Tyler Mahle went out '
   'in the part of the selloff nobody talked about</a>. What came back that matters is '
   '<a href="articles/giants-marcelo-mayer-trade-red-sox-erik-miller-robbery.html">Marcelo Mayer for a reliever who walks '
   'everybody</a>.',
   'What is left to watch is the young core. <a href="articles/bryce-eldridge-giants-future-franchise-first-baseman-july-2026.html">Bryce '
   'Eldridge is the only future this roster has</a>, <a href="articles/giants-casey-schmitt-all-star-breakout-season-2026.html">Casey '
   'Schmitt forced his way into the lineup and stayed there</a>, and Rafael Devers has '
   'quietly had the season nobody is discussing. The manager question is its own thread: '
   'we did not like <a href="articles/tony-vitello-hire-giants-mistake.html">the Tony Vitello hire</a> and have not '
   'pretended otherwise since.',
   'The bullpen is the other constant. If you want the pattern rather than one bad night, '
   'start with <a href="articles/giants-season-over-build-around-eldridge-posey-bullpen.html">the column that called the season '
   'over</a>. Older Giants coverage - the even-year dynasty, Bonds, the 1993 race - lives '
   'in <a href="history.html">Bay Area History</a>. Everything current sits below.']),

 '49ers.html': ('The 49ers, going into 2026', [
   'This is the 49ers hub: training camp, injuries, roster moves, and the columns that '
   'come out of them. August 2026 has a simple shape. The quarterback is playing the best '
   'football of his career and the medical staff is busier than the coaching staff.',
   '<a href="articles/49ers-brock-purdy-highest-passer-rating-nfl-history-1500-attempts.html">Brock Purdy is 147 attempts from the '
   'highest career passer rating in NFL history</a>, and camp has looked like it: '
   '<a href="articles/49ers-purdy-70-yard-touchdowns-unknown-receivers-camp-august-7.html">seventy-yard touchdowns to receivers '
   'nobody has heard of</a>, <a href="articles/49ers-brock-purdy-sharp-camp-demarcus-robinson-dime-end-zone-2026.html">a dime to '
   'Demarcus Robinson in the back of the end zone</a>, and real chemistry with '
   '<a href="articles/49ers-dezhaun-stribling-training-camp-starter-2026.html">rookie De\'Zhaun Stribling</a>.',
   'The other half is the injury list. <a href="articles/49ers-ricky-pearsall-out-for-season-pcl-surgery-2026.html">Ricky Pearsall '
   'is out for the year</a> before a single kickoff, <a href="articles/49ers-injuries-again-training-camp-august-2026.html">the '
   'receiver room keeps thinning</a>, and <a href="articles/49ers-kyle-shanahan-car-accident-injuries-recovery-2026.html">Kyle '
   'Shanahan is coaching while he recovers from a car accident</a> that was worse than it '
   'first sounded. The front office response was <a href="articles/49ers-signing-spree-okoronkwo-irwin-deguara-hodge-august-2026.html">four '
   'signings in a week</a>, plus <a href="articles/49ers-deebo-samuel-returns-one-year-7-million-2026.html">Deebo Samuel coming '
   'home on a one-year deal</a>.',
   'For the argument about how good this can be, there is the case that '
   '<a href="articles/49ers-shanahan-best-team-if-healthy-super-bowl-2026.html">this is the best roster Shanahan has ever had</a>, '
   'and the reason to be careful about it. The dynasty years, the Montana-Young era and '
   'the Super Bowl that still stings are in <a href="dynasties.html">Bay Area Dynasties</a> '
   'and <a href="history.html">History</a>.']),

 'athletics.html': ("The A's, in West Sacramento, in free fall", [
   "This is the Athletics hub. Fifty-seven years of Oakland baseball are boxed up and "
   "parked in a Triple-A ballpark while everyone waits on Las Vegas, and "
   "<a href=\"articles/athletics-sacramento-bay-area-villains.html\">that is the whole ugly story</a>. "
   "The baseball happening inside it deserves writing about anyway, so we do.",
   "The 2026 season was a mirage that ended on schedule. They were over .500 in June, then "
   "came the streaks: <a href=\"articles/athletics-nine-straight-white-sox-9-1-tailspin-i-called-it-july-12.html\">nine "
   "straight in July</a>, <a href=\"articles/athletics-first-half-breakdown-mirage-collapse-all-star-break-2026.html\">41-55 at "
   "the break</a>, and <a href=\"articles/athletics-free-fall-continues-fourth-place-trade-deadline-july-30.html\">a free fall "
   "that never actually stopped</a>. The one night that broke the pattern - "
   "<a href=\"articles/athletics-15-1-nationals-ginn-gem-streak-snapped-july-18.html\">a 15-1 win that snapped a ten-game "
   "skid</a> - was worth checking the box score three times.",
   "There is real talent here, which is what makes it maddening. Jacob Lopez keeps "
   "<a href=\"articles/athletics-twins-2-0-lopez-bullpen-shutout-july-25.html\">pitching well enough to win</a> and keeps "
   "getting nothing behind him. Nick Kurtz and Shea Langeliers both started an All-Star "
   "Game. Gage Jump, Jacob Wilson, Brian Serven and Tyler Soderstrom all show up in these "
   "recaps for the right reasons.",
   "Every game gets covered here, wins and losses. The A's dynasty years and the "
   "Moneyball era are in <a href=\"dynasties.html\">Bay Area Dynasties</a>; the rest of the "
   "league is in <a href=\"mlb.html\">Bay Area MLB</a>."]),

 'warriors.html': ('The Warriors, on the other side of the run', [
   'This is the Warriors hub: the roster, the rotation, and what this era has left at '
   'Chase Center. The dynasty is not the story anymore. What to do about the end of it is.',
   'Two threads run through the coverage. One is the front office: '
   '<a href="articles/warriors-front-office-failures-curry-exit-not-preposterous.html">it keeps failing Steph Curry, and "he '
   'could leave" no longer sounds crazy</a>. The other is the young core and how it is '
   'handled - <a href="articles/warriors-kerr-kuminga-role-handling.html">how Steve Kerr actually handled Jonathan '
   'Kuminga</a> is the case study, and '
   '<a href="articles/warriors-out-of-easy-answers.html">the team is out of easy answers</a> either way.',
   'The championship years are not gone, just filed: '
   '<a href="articles/warriors-73-9-best-record-ever-added-durant.html">73-9 and then adding Kevin Durant</a>, '
   '<a href="articles/warriors-championship-history.html">Rick Barry through the Splash Brothers</a>, and '
   '<a href="articles/flashback-klay-37-point-quarter.html">the night Klay scored 37 in a quarter</a>. '
   'For the league-wide view, see <a href="nba.html">Bay Area NBA</a>.']),

 'sharks.html': ('The Sharks rebuild, early days', [
   'This is the Sharks hub. Coverage here is early and honest about it: the South Bay has '
   'been hard to watch for a while, and this blog is not going to pretend a rebuild is '
   'further along than it is.',
   'The reason to pay attention now has a name. '
   '<a href="articles/sharks-rebuild-has-a-pulse-celebrini.html">Macklin Celebrini is why the rebuild finally has a '
   'pulse</a>, and that piece is the place to start. As the season gets going, game '
   'coverage and columns will land here; the league page is '
   '<a href="nhl.html">Bay Area NHL</a>, and the wider regional story is in '
   '<a href="bayarea.html">the Bay Area hub</a>.']),

 'mlb.html': ('Two baseball teams, two different kinds of bad', [
   'This is the league page for Bay Area baseball: the Giants and the Athletics, every '
   'game, in one place. 2026 gave the region two losing teams that are losing for '
   'completely different reasons, which makes reading them side by side more interesting '
   'than it should be.',
   'The <a href="giants.html">Giants</a> had a roster good enough to matter and spent the '
   'deadline taking it apart - Arraez, Ray, Ramos and Mahle all gone, with '
   '<a href="articles/bryce-eldridge-giants-future-franchise-first-baseman-july-2026.html">Bryce Eldridge</a> left as the thing '
   'to watch. The <a href="athletics.html">Athletics</a> are a franchise in transit, playing '
   'major-league games in a Triple-A park in West Sacramento while the Las Vegas move '
   'grinds on.',
   'What you get here: every recap for both clubs in date order, the deadline coverage, '
   'the manager arguments, and the All-Star week when '
   '<a href="articles/giants-athletics-all-star-game-2026-arraez-langeliers-webb.html">the Bay actually had people in the '
   'game</a>. Older baseball - the even-year dynasty, Bonds, the 1993 race - is in '
   '<a href="history.html">History</a>.']),

 'nfl.html': ('Bay Area football, both of them', [
   'This is the league page for Bay Area football. In practice that means the '
   '<a href="49ers.html">49ers</a>, who get covered every day of camp and every week of the '
   'season, plus the occasional look at the Raiders now that they play their home games in '
   'Nevada and still take a piece of this region with them.',
   'The 2026 story so far is a quarterback playing at a historic level behind an injury '
   'list that will not stop growing - <a href="articles/49ers-brock-purdy-highest-passer-rating-nfl-history-1500-attempts.html">Purdy '
   'is inside 150 attempts of the best career passer rating ever recorded</a>, while camp '
   'keeps costing this team receivers. For the other franchise, there is the '
   '<a href="articles/raiders-2026-season-preview-kubiak-cousins-mendoza-jeanty.html">Raiders 2026 preview</a>.',
   'Football history gets its own rooms: <a href="dynasties.html">the 1980s dynasty</a>, '
   '<a href="articles/montana-young-49ers-quarterback-controversy.html">Montana and Young</a>, '
   '<a href="articles/flashback-the-catch-1982.html">The Catch</a>, and '
   '<a href="articles/nfl-blackballed-colin-kaepernick-kneeling-anthem.html">what the league did to Colin '
   'Kaepernick</a>.']),

 'nba.html': ('Bay Area basketball in one place', [
   'This is the league page for Bay Area basketball, which means the '
   '<a href="warriors.html">Golden State Warriors</a>: the roster, the rotation, the front '
   'office, and the question of how much of this era is left.',
   'Current coverage is about the end of a dynasty rather than the middle of one - what '
   'happens to the young players, whether the front office is still worthy of Steph Curry, '
   'and what the next good Warriors team even looks like. The banner years are still here '
   'too, from <a href="articles/warriors-73-9-best-record-ever-added-durant.html">73-9</a> to '
   '<a href="articles/lebron-curry-warriors-legacy-what-it-means.html">the LeBron-and-Curry thought '
   'experiment</a> and the full <a href="articles/warriors-championship-history.html">championship '
   'history</a>.']),

 'nhl.html': ('Bay Area hockey', [
   'This is the league page for Bay Area hockey: the '
   '<a href="sharks.html">San Jose Sharks</a>, the rebuild, and the young core it is being '
   'built around.',
   'Coverage here is just getting going, and there is one piece worth your time right now: '
   '<a href="articles/sharks-rebuild-has-a-pulse-celebrini.html">the rebuild finally has a pulse, and his name is Macklin '
   'Celebrini</a>. More lands as the season starts. The rest of the region is in '
   '<a href="bayarea.html">the Bay Area hub</a>.']),
}

HERO_END = re.compile(r'(</section>)', re.S)


def rd(p):
    return open(os.path.join(ROOT, p), encoding='utf-8', errors='strict').read()


def wr(p, s):
    full = os.path.join(ROOT, p)
    with open(full, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)
    b = open(full, 'rb').read()
    if b'\x00' in b or b.count(b'\xef\xbf\xbd'):
        raise SystemExit('corruption writing %s - ABORT' % p)


def main():
    check = '--check' in sys.argv
    total = 0
    for page, (heading, paras) in COPY.items():
        s = rd(page)
        if MARK in s:
            print('  %-16s already has the intro' % page)
            continue
        i = s.find('<section class="sec-hero"')
        if i < 0:
            print('  %-16s NO HERO - skipped' % page)
            continue
        j = s.index('</section>', i) + len('</section>')
        new = s[:j] + '\n' + block(heading, paras) + s[j:]
        words = sum(len(re.sub(r'<[^>]+>', ' ', p).split()) for p in paras)
        links = sum(p.count('<a href=') for p in paras)
        total += words
        print('  %-16s +%4d words, %2d contextual links' % (page, words, links))
        if not check:
            wr(page, new)
    print('%s  %d hubs, %d words of new hub copy'
          % ('CHECK' if check else 'APPLIED', len(COPY), total))


if __name__ == '__main__':
    main()
