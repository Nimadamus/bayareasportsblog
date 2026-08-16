#!/usr/bin/env python3
"""_college_hubs.py: turn cal.html and stanford.html into real section fronts.

Both were a heading, fifty words and no way to reach anything. Each now answers the four
questions a section front has to answer above the fold:

  what this section covers      - the intro paragraph, rewritten
  the newest coverage           - "Latest" card grid, newest first
  the strongest evergreen       - "Start here" block for the pieces that stay true
  where to go next              - the other programme, the Big Game, the Bay Area desk

Markup uses the template's own .card / .cardgrid / .section-head classes. No CSS file is
touched, no URL changes, no existing link removed.

  python _college_hubs.py [--check]
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MARK = '<!-- college hub build -->'

CARD = ('      <a class="card" href="articles/%(slug)s.html">\n'
        '        <div class="thumb"><picture><source type="image/webp" srcset="assets/img/cards/%(slug)s-400w.webp 400w, assets/img/cards/%(slug)s-600w.webp 600w, assets/img/cards/%(slug)s-800w.webp 800w, assets/img/cards/%(slug)s.webp 1200w" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 30vw">'
        '<img src="assets/img/cards/%(slug)s.jpg" alt="%(alt)s" width="1200" height="675" decoding="async" loading="lazy" '
        'srcset="assets/img/cards/%(slug)s-400w.jpg 400w, assets/img/cards/%(slug)s-600w.jpg 600w, assets/img/cards/%(slug)s-800w.jpg 800w, assets/img/cards/%(slug)s.jpg 1200w" '
        'sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 30vw" style="width:100%%;height:100%%;object-fit:cover"></picture>'
        '<span>%(kicker)s</span></div>\n'
        '        <div class="c-body">\n'
        '          <h3>%(title)s</h3>\n'
        '          <p>%(blurb)s</p>\n'
        '          <div class="meta">Read the column</div>\n'
        '        </div>\n'
        '      </a>\n')

CAL_LATEST = [
 dict(slug='cal-2026-season-preview-lupoi-sagapolutele', kicker='Cal Preview',
      title='Tosh Lupoi Comes Home to Berkeley, and This Cal Team Might Actually Be Dangerous',
      blurb='A first-year head coach who played on this line, a quarterback who threw for 3,454 yards and came back anyway, and a schedule that misses the ACC&#39;s three biggest names.',
      alt='Bay Area Sports Blog: Cal 2026 season preview, Tosh Lupoi and Jaron-Keawe Sagapolutele'),
 dict(slug='cal-2026-schedule-game-by-game-acc', kicker='Cal',
      title='Cal&#39;s 2026 Schedule, Game by Game, and the Four Weeks That Decide the Season',
      blurb='UCLA to open, Clemson at home in September, a November road stretch that will either make this team or expose it, and the Big Game to finish.',
      alt='Bay Area Sports Blog: Cal 2026 schedule breakdown'),
 dict(slug='cal-stanford-acc-realignment-what-changed', kicker='College Football',
      title='Cal and Stanford Play in the ACC Now, and Nobody Around Here Has Made Peace With It',
      blurb='Two Bay Area schools in a conference built around the Atlantic coast. The travel is absurd, the kickoff times are worse.',
      alt='Bay Area Sports Blog: what ACC realignment changed for Cal and Stanford'),
]
STAN_LATEST = [
 dict(slug='stanford-2026-season-preview-pritchard-luck-warren', kicker='Stanford Preview',
      title='Stanford Hands the Keys to Tavita Pritchard, and Andrew Luck Has to Live With It',
      blurb='A first-time head coach who used to hold the clipboard behind Andrew Luck, a quarterback coming off a knee injury, and a Week 0 kickoff.',
      alt='Bay Area Sports Blog: Stanford 2026 season preview, Tavita Pritchard and Davis Warren'),
 dict(slug='stanford-hawaii-week-zero-opener-preview', kicker='Stanford Preview',
      title='Stanford Opens in Week 0 Against Hawaii, and Getting the Country to Itself Is the Whole Point',
      blurb='One game, one Saturday, and nothing else on the schedule to compete with it. For a programme that needs people to look again, the calendar just did it a favour.',
      alt='Bay Area Sports Blog: Stanford opens Week 0 against Hawaii'),
 dict(slug='andrew-luck-stanford-general-manager-experiment', kicker='Stanford',
      title='Andrew Luck Is Running a Football Program, and the Rest of College Football Should Be Watching',
      blurb='A retired quarterback with a general manager title at his alma mater is either a vanity appointment or the first sane answer to what this sport became.',
      alt='Bay Area Sports Blog: Andrew Luck as Stanford general manager'),
]

EVERGREEN = (
 '<div class="teamblock"><div class="th"><h2>Start here</h2></div>\n'
 '<p style="color:#dfe3ea;margin-bottom:14px">These do not go stale. If you only read '
 'three things in this section, read these.</p>\n'
 '<div class="team-nav">'
 '<a href="articles/big-game-cal-stanford-rivalry-history.html"><span class="dot" style="background:#e11d2a"></span>The Big Game, explained</a>'
 '<a href="articles/stanford-axe-trophy-history.html"><span class="dot" style="background:#8c1515"></span>The Stanford Axe</a>'
 '<a href="articles/cal-stanford-acc-realignment-what-changed.html"><span class="dot" style="background:#003262"></span>What the ACC move cost</a>'
 '</div></div>\n')

CAL_INTRO = (
 'Cal football, basketball and everything else out of Berkeley, covered by people who '
 'live here. Right now that means the 2026 football season: '
 '<a href="articles/cal-2026-season-preview-lupoi-sagapolutele.html">Tosh Lupoi&#39;s first '
 'year as head coach</a>, Jaron-Keawe Sagapolutele returning at quarterback after 3,454 '
 'yards, and <a href="articles/cal-2026-schedule-game-by-game-acc.html">an ACC schedule</a> '
 'that opens against UCLA on 5 September and finishes with '
 '<a href="articles/big-game-cal-stanford-rivalry-history.html">the Big Game</a> at home on '
 '21 November. Memorial Stadium sits in the hills, the rivalry with '
 '<a href="stanford.html">Stanford</a> has been played since 1892, and both of those facts '
 'matter more than whatever the conference standings say.')

STAN_INTRO = (
 'Stanford football and the rest of the Cardinal, covered from the Bay rather than from a '
 'wire desk. The 2026 story is a rebuild with an unusual structure: '
 '<a href="articles/andrew-luck-stanford-general-manager-experiment.html">Andrew Luck is the '
 'general manager</a>, <a href="articles/stanford-2026-season-preview-pritchard-luck-warren.html">Tavita '
 'Pritchard is the new head coach</a>, and the season starts early with '
 '<a href="articles/stanford-hawaii-week-zero-opener-preview.html">a Week 0 game against '
 'Hawaii</a> on 29 August. Then the ACC, Notre Dame, and '
 '<a href="articles/big-game-cal-stanford-rivalry-history.html">the Big Game</a> against '
 '<a href="cal.html">Cal</a> in November.')

NEXT_CAL = (
 '<div class="teamblock"><div class="th"><h2>Where to go next</h2></div>\n'
 '<div class="team-nav">'
 '<a href="stanford.html"><span class="dot" style="background:#8c1515"></span>Stanford</a>'
 '<a href="bayarea.html"><span class="dot" style="background:#003262"></span>Bay Area Sports</a>'
 '<a href="history.html"><span class="dot" style="background:#e9c882"></span>Bay Area History</a>'
 '<a href="index.html"><span class="dot" style="background:#e11d2a"></span>Home</a>'
 '</div></div>\n')
NEXT_STAN = NEXT_CAL.replace(
 '<a href="stanford.html"><span class="dot" style="background:#8c1515"></span>Stanford</a>',
 '<a href="cal.html"><span class="dot" style="background:#003262"></span>Cal</a>')


def rd(p):
    return open(os.path.join(ROOT, p), encoding='utf-8', errors='strict').read()


def wr(p, s):
    full = os.path.join(ROOT, p)
    with open(full, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)
    b = open(full, 'rb').read()
    if b'\x00' in b or b.count(b'\xef\xbf\xbd'):
        raise SystemExit('corruption writing %s, ABORT' % p)


def build(page, intro, latest, nxt):
    s = rd(page)
    if MARK in s:
        return None
    body = (MARK + '\n<section class="section"><div class="wrap">\n'
            '<div class="teamblock"><div class="th"><h2>%s</h2></div>\n'
            '<p style="color:#dfe3ea;margin-bottom:14px">%s</p></div>\n\n'
            '<div class="section-head"><h2>Latest coverage</h2></div>\n'
            '<div class="cardgrid">\n%s</div>\n\n%s\n%s'
            '</div></section>\n'
            % ('Cal Golden Bears' if 'cal' in page else 'Stanford Cardinal',
               intro, ''.join(CARD % c for c in latest), EVERGREEN, nxt))
    # replace the old placeholder section wholesale, keep hero and chrome
    m = re.search(r'<section class="section"><div class="wrap">.*?</div></section>', s, re.S)
    if not m:
        raise SystemExit('no section block found in %s' % page)
    return s[:m.start()] + body + s[m.end():]


def main():
    check = '--check' in sys.argv
    for page, intro, latest, nxt in (('cal.html', CAL_INTRO, CAL_LATEST, NEXT_CAL),
                                     ('stanford.html', STAN_INTRO, STAN_LATEST, NEXT_STAN)):
        out = build(page, intro, latest, nxt)
        if out is None:
            print('  %-14s already built' % page)
            continue
        words = len(re.sub(r'<[^>]+>', ' ', out).split())
        print('  %-14s %d cards, %d words total' % (page, len(latest), words))
        if not check:
            wr(page, out)
    print('%s  college hubs' % ('CHECK' if check else 'APPLIED'))


if __name__ == '__main__':
    main()
