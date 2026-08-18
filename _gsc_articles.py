#!/usr/bin/env python3
"""_gsc_articles.py: seven pages built for seven live Google Search Console queries.

These are queries the site already draws impressions for. Three of them already had a
page and are rebuilt IN PLACE at the same URL so the ranking history is kept:

  warriors depth chart 2026 27     -> articles/warriors-2026-27-roster-depth-chart.html
  bonds giants                     -> articles/barry-bonds-giants-home-run-king.html
  cal game schedule                -> articles/cal-2026-schedule-game-by-game-acc.html

Four are new:

  projected rotation               -> articles/warriors-2026-27-projected-rotation.html
  sharks playoff history           -> articles/sharks-playoff-history.html
  when was san jose sharks founded -> articles/when-were-the-san-jose-sharks-founded.html
  cal basketball schedule 2026     -> articles/cal-basketball-schedule-2026-27.html

The depth chart dict was REMOVED from _warriors_cluster.py and the Cal football schedule
dict was REMOVED from _college_cluster.py, so every page has exactly one owner and a
future cluster run cannot revert this copy.

House rules that apply here: no dashes used as punctuation, no bold in body copy, no
source lists, real photos with descriptive alt text, and nothing asserted that was not
verified first.

  python _gsc_articles.py [--check]
"""
import os, re, sys, json, subprocess
import _college_cluster as CC
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = CC.BASE
CARDS = CC.CARDS

HUBS = {'Warriors': ('../warriors.html', 'Warriors', 'warriors.html'),
        'Sharks':   ('../sharks.html', 'Sharks', 'sharks.html'),
        'Giants':   ('../giants.html', 'Giants', 'giants.html'),
        'Cal':      ('../cal.html', 'Cal', 'cal.html'),
        'Bay Area': ('../bayarea.html', 'Bay Area Sports', 'bayarea.html')}


PLAYERS = os.path.join(ROOT, 'assets', 'img', 'players')
SIZES = '(max-width: 820px) 92vw, 760px'


def derivatives(slug):
    """Make sure the narrow rungs and the WebP twin exist for one photo, without touching
    any derivative that is already on disk and already referenced by another page."""
    src = os.path.join(PLAYERS, slug + '.jpg')
    im = Image.open(src)
    w, h = im.size
    rungs = [r for r in (400, 600, 800) if r < w]
    for r in rungs:
        for ext, kw in (('.jpg', dict(format='JPEG', quality=92, optimize=True,
                                      progressive=True)),
                        ('.webp', dict(format='WEBP', quality=82, method=6))):
            out = os.path.join(PLAYERS, '%s-%dw%s' % (slug, r, ext))
            if not os.path.exists(out):
                im.convert('RGB').resize((r, round(h * r / w)), Image.LANCZOS).save(out, **kw)
    full = os.path.join(PLAYERS, slug + '.webp')
    if not os.path.exists(full):
        im.convert('RGB').save(full, format='WEBP', quality=82, method=6)
    return w, h, rungs


def _picture(slug, alt, extra=''):
    w, h, rungs = derivatives(slug)
    jpg = ', '.join(['../assets/img/players/%s-%dw.jpg %dw' % (slug, r, r) for r in rungs]
                    + ['../assets/img/players/%s.jpg %dw' % (slug, w)])
    web = ', '.join(['../assets/img/players/%s-%dw.webp %dw' % (slug, r, r) for r in rungs]
                    + ['../assets/img/players/%s.webp %dw' % (slug, w)])
    return ('<picture><source type="image/webp" srcset="%s" sizes="%s">'
            '<img src="../assets/img/players/%s.jpg" alt="%s" width="%d" height="%d" '
            'loading="lazy" decoding="async" srcset="%s" sizes="%s"%s></picture>'
            % (web, SIZES, slug, CC.esc(alt), w, h, jpg, SIZES, extra)), w


def fig(slug, alt, caption):
    """A single in body photo at its real intrinsic size, so nothing shifts on load."""
    style = (' style="display:block;width:100%%;max-width:%dpx;height:auto;margin:0 auto 10px;'
             'border-radius:12px;border:1px solid var(--line)"')
    pic, w = _picture(slug, alt, '')
    pic = pic.replace(' decoding="async"', ' decoding="async"' + (style % min(w, 760)), 1)
    return ('<figure style="margin:26px 0">%s'
            '<figcaption style="text-align:center;color:var(--muted);font-size:13px">%s'
            '</figcaption></figure>' % (pic, caption))


def figrow(a, b):
    """Two photos side by side, the pattern the history pages already use."""
    out = ['<figure class="figrow orig">']
    for slug, alt, cap in (a, b):
        pic, _w = _picture(slug, alt)
        out.append('<figure>%s<figcaption>%s</figcaption></figure>' % (pic, cap))
    out.append('</figure>')
    return ''.join(out)


def table(caption, heads, rows, foot=None):
    h = ''.join('<th scope="col">%s</th>' % x for x in heads)
    body = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in rows)
    f = ('<tfoot><tr>%s</tr></tfoot>'
         % ''.join('<td>%s</td>' % c for c in foot)) if foot else ''
    return ('<div class="reftable"><table><caption>%s</caption><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody>%s</table></div>' % (caption, h, body, f))


def faq(pairs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for q, a in pairs]}


def build(a):
    """CC.TEMPLATE, with a hub map that reaches the team hubs, plus optional extra schema."""
    slug, url = a['slug'], BASE + 'articles/' + a['slug'] + '.html'
    img = BASE + 'assets/img/cards/' + slug + '.jpg'
    hub_href, hub_name, crumb_file = HUBS[a['hub']]
    art = {"@context": "https://schema.org", "@type": "NewsArticle",
           "headline": a['h1'], "image": img,
           "author": {"@type": "Organization", "name": "Bay Area Sports Blog"},
           "publisher": {"@type": "Organization", "name": "Bay Area Sports Blog"},
           "description": a['desc'], "datePublished": a['date'], "dateModified": a['date'],
           "mainEntityOfPage": {"@type": "WebPage", "@id": url},
           "articleSection": a['section']}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList",
              "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
                {"@type": "ListItem", "position": 2, "name": hub_name,
                 "item": BASE + crumb_file},
                {"@type": "ListItem", "position": 3, "name": a['h1'], "item": url}]}
    j = lambda d: json.dumps(d, separators=(',', ':'), ensure_ascii=False)

    more = ('  <p style="margin-top:30px;color:var(--muted);font-size:15px">More coverage: '
            '<a href="%s" style="color:var(--accent2);font-weight:700">%s section</a> &middot; '
            '<a href="../bayarea.html" style="color:var(--accent2);font-weight:700">Bay Area Sports</a> &middot; '
            '<a href="../index.html" style="color:var(--accent2);font-weight:700">Bay Area Sports Blog home</a></p>'
            % (hub_href, hub_name))
    rel = '\n'.join(
        '    <a href="%s"><div class="rc">%s</div><h4>%s</h4></a>' % (h, CC.esc(k), CC.esc(t))
        for h, k, t in a['related'])

    html = CC.TEMPLATE % dict(
        title=CC.esc(a['title']), desc=CC.esc(a['desc']), url=url, img=img,
        h1=CC.esc(a['h1']), dek=a['dek'], tag=CC.esc(a['tag']), section=CC.esc(a['section']),
        art=j(art), crumbs=j(crumbs), slug=slug,
        body=CC.render_body(a['body'], a['links']), more=more, rel=rel,
        alt=CC.esc('Bay Area Sports Blog: ' + a['h1']))
    extra = ''.join('<script type="application/ld+json">%s</script>\n' % j(x)
                    for x in a.get('schema', []))
    if extra:
        html = html.replace('</head>', extra + '</head>')
    return html


ARTICLES = [

# ------------------------------------------------- 1. warriors depth chart 2026 27
dict(slug='warriors-2026-27-roster-depth-chart',
     section='Warriors', tag='Warriors', hub='Warriors',
     title='Warriors Depth Chart 2026-27: Every Position, Explained',
     h1='The Warriors Depth Chart for 2026-27, Position by Position',
     dek='The projected starting five, the bench behind it, the two knees that decide the '
         'season, and the spots where this roster is genuinely thin.',
     desc='The Warriors depth chart for 2026-27: the projected starters, the bench behind '
          'them, where Jimmy Butler and Moses Moody fit, and where this roster runs out.',
     date='2026-08-18',
     card=('warriors', 'Warriors Depth Chart 2026-27', 'Every position, top to bottom'),
     body=[
      "Here is the Warriors depth chart for 2026-27 as it stands in the middle of August, "
      "with camp still weeks away and the opener set for 21 October in Los Angeles. Steph "
      "Curry, Brandin Podziemski, Gui Santos, Draymond Green and Kristaps Porzingis project "
      "as the starting five. Al Horford, De'Anthony Melton, Gary Payton II and Will Richard "
      "are the veteran bench. Yaxel Lendeborg is the rookie. And the two players who would "
      "redraw every line of this chart, Jimmy Butler and Moses Moody, are both coming back "
      "from knee surgery.",

      table('Golden State Warriors projected depth chart, 2026-27',
            ['Position', 'Starter', 'Second', 'Third'],
            [['Point guard', 'Stephen Curry', "De'Anthony Melton", 'Gary Payton II'],
             ['Shooting guard', 'Brandin Podziemski', 'Will Richard', 'Moses Moody (rehab)'],
             ['Small forward', 'Gui Santos', 'Jimmy Butler (rehab)', 'Lajae Jones'],
             ['Power forward', 'Draymond Green', 'Yaxel Lendeborg', 'Gui Santos'],
             ['Centre', 'Kristaps Porzingis', 'Al Horford', 'Charles Bassey']]),

      "<h2>Why the starting five looks like that</h2>",

      "Read that lineup twice, because the two names most people expect to see are not in "
      "it. Butler is the second best player on this roster when he is upright and he is not "
      "going to be upright in October. He tore the ACL in his right knee on 19 January at "
      "Chase Center against Miami, of all opponents, and had surgery on 9 February. The "
      "realistic target for a player of his age coming off that operation is somewhere "
      "around midseason, which is roughly what the front office has been signalling all "
      "summer. February is a reasonable bet. November is not.",

      fig('jimmy-butler',
          'Jimmy Butler, who tore his right ACL in January 2026 and is expected back around '
          'midseason for the Golden State Warriors',
          'Butler is the whole variable. The chart above is what this team looks like without him'),

      "Moody is the other one. He tore the patellar tendon in his left knee against Dallas "
      "on 23 March, which carries a nine to twelve month recovery, and the update out of his "
      "rehab in the Bay is that he hoped to be running and doing on court work by September. "
      "That is encouraging for March, not for opening night. Put him down as a second half "
      "addition and be pleasantly surprised if it comes sooner.",

      "<h2>Guard</h2>",

      "Curry is thirty-eight and still the entire centre of gravity of this offense, which "
      "is both the best thing about the roster and the most uncomfortable sentence anybody "
      "in this fan base has to say out loud. Everything the team does well starts with two "
      "defenders chasing him around a screen. The numbers are on the {currypage}, and they "
      "are still moving.",

      "Podziemski has grown from a curiosity into an actual starting guard, and he is the one "
      "young player on this roster the coaching staff has trusted without needing to be "
      "argued into it. Melton and Payton were both brought back on 1 August, which tells you "
      "exactly how the front office feels about continuity right now. Payton is thirty-three "
      "and still the best point of attack defender on the team. Will Richard inherits the "
      "backup wing minutes that used to belong to Moody.",

      "<h2>Wing</h2>",

      "This is the thin spot, and it is thin because of a trade. Jonathan Kuminga and Buddy "
      "Hield went to Atlanta at the deadline for Porzingis, which fixed the centre position "
      "and emptied the wing. Gui Santos starting for a team with this payroll is not a plan "
      "anybody drew up in June, it is what is left. Santos plays hard, cuts well and does not "
      "need the ball, and if this season goes right he is the seventh best player on a "
      "healthy roster rather than the third best on this one. How the staff handled Kuminga "
      "on the way out is its own argument, and we have made it {kuminga}.",

      "<h2>Big</h2>",

      "Porzingis is the real addition and the reason the deadline trade made sense. Seven "
      "foot two, shoots it from range, protects the rim, and arrives with a medical history "
      "that includes the POTS diagnosis that cost him most of a season in Boston. He "
      "re-signed on 30 June. Horford came back on 6 July, and at forty he is a specific kind "
      "of useful: he knows where to be, he can still shoot it, and he does not need plays run "
      "for him. Charles Bassey is the third centre.",

      figrow(('porzingis',
              'Kristaps Porzingis, the projected starting centre on the Warriors 2026-27 depth chart',
              'Porzingis, acquired at the deadline and re-signed on 30 June'),
             ('horford',
              'Al Horford, re-signed by the Warriors in July 2026 as the backup centre',
              'Horford, back for another year at forty')),

      "Draymond re-signed on 30 July and remains the player who decides what the defence is "
      "capable of. There is no version of a good Warriors defence that does not run through "
      "him, and there is no version of a calm Warriors season that does not depend on his "
      "temperament. Both of those things have been true for a decade and neither is changing "
      "now.",

      "<h2>The rookie and the two way spots</h2>",

      "Yaxel Lendeborg came in at eleven in the draft out of Michigan, a six foot nine "
      "forward who can handle it a little and guard more than one position. Lajae Jones went "
      "at fifty four out of Florida State. Rookie minutes on a team trying to win now are "
      "earned rather than handed out, and this staff has a long and well documented history "
      "of {development}, so temper the expectations for game one and watch what has happened "
      "by January.",

      "<h2>Who left</h2>",

      "Quinten Post signed an offer sheet with Memphis and Golden State declined to match. "
      "Pat Spencer went to Phoenix. Nate Williams took a deal in Japan. Kuminga and Hield "
      "were gone at the deadline. That is a lot of bodies out of a roster that finished 37-45 "
      "last season, took the tenth seed, won its first play in game and then lost to Phoenix "
      "to end it.",

      "<h2>Where it runs thin</h2>",

      "Everywhere behind the top seven. This is a roster with two enormous salaries, a "
      "handful of sensible veteran deals, and then minimum contracts and hope. If Curry, "
      "Green or Porzingis misses a month there is no replacement on the books, only a "
      "redistribution of minutes to players who were not signed to play them. The {capsheet} "
      "goes through why that is, and it is not an accident, it is the arithmetic consequence "
      "of paying two players what this team pays two players.",

      "Steve Kerr signed a new two year deal in May and used forty three different starting "
      "lineups last season, which is less a coaching philosophy than a medical report. The "
      "chart at the top of this page assumes a healthy October. Nothing about the last two "
      "seasons suggests that is the way to bet.",

      fig('chase-center',
          'Chase Center in San Francisco, where the Warriors open at home on 23 October 2026 '
          'against the Memphis Grizzlies',
          'The home opener is 23 October against Memphis, two nights after Los Angeles'),

      "<h2>The calendar</h2>",

      "Golden State opens on the road at the Lakers on Wednesday 21 October in a national "
      "television window, then comes home to Chase Center on Friday 23 October against "
      "Memphis. Camp is where the rotation questions get answered, and the rotation is a "
      "different question from the depth chart, which is exactly why we split it out into "
      "{rotation}.",

      "This page is a running record and gets updated on every roster move, every injury "
      "update and every meaningful change to the pecking order. The bigger argument about "
      "where this team is heading is in the {outlook}, and the rest of it is on the {hub}.",
     ],
     links={'currypage': ('stephen-curry-career-records-three-pointers.html', 'Curry records page'),
            'kuminga': ('warriors-kerr-kuminga-role-handling.html', 'more than once'),
            'development': ('warriors-clinging-to-past-cannot-develop-young-players.html',
                            'not developing young players'),
            'capsheet': ('warriors-roster-construction-cap-sheet-2026-27.html', 'cap sheet page'),
            'rotation': ('warriors-2026-27-projected-rotation.html',
                         'a separate projected rotation page'),
            'outlook': ('warriors-2026-27-season-outlook.html', 'season outlook'),
            'hub': ('../warriors.html', 'Warriors hub')},
     related=[('warriors-2026-27-projected-rotation.html', 'Warriors',
               'Warriors Projected Rotation 2026-27: Who Actually Plays'),
              ('warriors-roster-construction-cap-sheet-2026-27.html', 'Warriors',
               'The Cap Sheet That Built This Roster'),
              ('warriors-2026-27-season-outlook.html', 'Warriors',
               'What the 2026-27 Warriors Actually Are')]),

# ------------------------------------------------- 2. projected rotation
dict(slug='warriors-2026-27-projected-rotation',
     section='Warriors', tag='Warriors', hub='Warriors',
     title='Warriors Projected Rotation 2026-27: Who Actually Plays',
     h1='The Warriors Projected Rotation for 2026-27, and Who Actually Closes',
     dek='A depth chart says who is on the roster. A rotation says who gets the minutes '
         'that matter. Here is the projection, and the four decisions it hinges on.',
     desc='Our projected Warriors rotation for 2026-27: the ten men who play, the minutes '
          'each should get, who closes, and what changes when Jimmy Butler is back.',
     date='2026-08-18',
     card=('warriors', 'Projected Rotation 2026-27', 'The ten men who actually play'),
     body=[
      "A depth chart tells you who is on the roster. A projected rotation tells you who Steve "
      "Kerr actually trusts at nine o'clock on a Tuesday night in January, and those are not "
      "the same list. Here is our projected Warriors rotation for 2026-27, built off the "
      "roster as it stands in August, carrying the caveat that hangs over everything with "
      "this team now: it assumes a level of health this group has not had in two years.",

      table('Projected Warriors rotation for opening night, 2026-27',
            ['Player', 'Role', 'Projected minutes'],
            [['Stephen Curry', 'Starter, offensive engine', '32'],
             ['Brandin Podziemski', 'Starter, secondary creator', '30'],
             ['Draymond Green', 'Starter, defensive organiser', '28'],
             ['Kristaps Porzingis', 'Starter, rim protection and spacing', '28'],
             ['Gui Santos', 'Starter, connector and cutter', '26'],
             ['Al Horford', 'Backup centre and closing option', '20'],
             ["De'Anthony Melton", 'Backup guard', '20'],
             ['Yaxel Lendeborg', 'Rookie forward', '16'],
             ['Gary Payton II', 'Defensive specialist', '16'],
             ['Will Richard', 'Backup wing', '14']],
            ['Ten man rotation', 'Butler and Moody unavailable', '240 minutes']),

      "Ten players is roughly where Kerr likes to live before injuries force him deeper. Last "
      "season he was forced deeper constantly. Forty three different starting lineups in one "
      "year is not a rotation, it is triage, and the fact that this team still won a play in "
      "game before Phoenix ended it at 37-45 says something about how hard the healthy nights "
      "were being worked.",

      fig('stephen-curry-real',
          'Stephen Curry, who at thirty-eight still anchors the Golden State Warriors rotation '
          'going into the 2026-27 season',
          'The whole rotation is built around getting Curry the right thirty-two minutes'),

      "<h2>The Curry minutes question</h2>",

      "Thirty-two minutes a night is the number this staff has protected for a while now, and "
      "at thirty-eight it is the right one. The interesting part is not the total, it is the "
      "distribution. Kerr has spent years staggering Curry so that he opens the second and "
      "fourth quarters with the bench, because a bench unit with Curry on it is a playoff team "
      "and a bench unit without him has historically been an adventure. Expect the same shape: "
      "a heavy first quarter, an early rest, a long stretch to open the second, and then "
      "whatever the game demands after that.",

      "<h2>Who closes</h2>",

      "Closing lineups are where a rotation gets honest. Our projection for a tight game in "
      "November, with Butler still rehabbing, is Curry, Podziemski, Santos, Green and "
      "Porzingis, with Horford swapped in for Porzingis when the Warriors want five out and "
      "everything switchable, which has been the Golden State answer to a jam for a decade. "
      "Payton closes on nights when the other team has one guard who simply has to be stopped. "
      "That is several different fifth men depending on the matchup, and Kerr has never been "
      "shy about changing his mind at a timeout.",

      "<h2>What changes when Butler is back</h2>",

      "Everything. Butler tore his right ACL on 19 January and had surgery on 9 February, and "
      "the honest timeline puts him somewhere around February rather than the start of the "
      "season. When he returns he does not simply slot into Santos's minutes, he takes the "
      "ball. Butler on the floor turns Curry from the only creator into a player who can move "
      "without the ball for a full possession, which is the version of this offense the front "
      "office thought it was buying. Santos drops to sixteen minutes, Richard probably falls "
      "out on healthy nights, and the rotation tightens to nine.",

      "Moody is the other returning piece. Torn left patellar tendon on 23 March, nine to "
      "twelve months, with on court work targeted for September. If he is right by the trade "
      "deadline he is a starter's worth of wing defence and catch and shoot volume arriving "
      "off the bench, and he is the difference between a rotation that has enough wings and "
      "one that does not.",

      figrow(('porzingis',
              'Kristaps Porzingis, whose workload limits shape the Warriors frontcourt rotation '
              'in 2026-27',
              'Porzingis and his workload are the frontcourt question'),
             ('green',
              'Draymond Green, the Warriors defensive organiser and the player the rotation runs through',
              'Green decides what this defence can be')),

      "<h2>The rookie minutes</h2>",

      "Yaxel Lendeborg went eleventh out of Michigan and there is a version of this season "
      "where he is playing twenty minutes a night by February. There is also a version where "
      "he plays nine. This coaching staff has a long history of preferring the known quantity "
      "in a tight game, which is the entire {kuminga} argument compressed into one sentence, "
      "and a team paying this much money to win right now is not a natural environment for "
      "rookie development. Sixteen minutes is the projection and neither side of it would "
      "surprise us.",

      "<h2>The frontcourt problem nobody wants to say out loud</h2>",

      "Porzingis and Horford are the two best bigs on this roster and neither is a safe bet "
      "for seventy five games. Porzingis carries a real medical history, including the POTS "
      "diagnosis that wiped out most of a season in Boston, and Horford is forty years old. "
      "Rest at centre is not a maybe here, it is a scheduling assumption, and third centre "
      "minutes matter more on this roster than they do on almost any other team in the league. "
      "That is the quiet reason Green will spend more time at the five than anybody would like.",

      "<h2>What we are actually watching in camp</h2>",

      "Four things. Whether Santos holds the starting job or Lendeborg takes it off him. "
      "Whether Podziemski is a thirty minute player on a good team or a nice piece on a bad "
      "one. How many minutes the staff is willing to play Green at centre. And whether Melton, "
      "who has his own injury history, can hold twenty minutes a night as the backup guard, "
      "because if he cannot then the entire second unit has to be redrawn before Christmas.",

      "The roster itself, position by position, is on the {depthchart}. The money that produced "
      "this rotation is on the {capsheet}. The season opens on 21 October at the Lakers and the "
      "home opener is 23 October against Memphis, and the argument about what this team really "
      "is lives in the {outlook}.",
     ],
     links={'kuminga': ('warriors-kerr-kuminga-role-handling.html', 'Kuminga'),
            'depthchart': ('warriors-2026-27-roster-depth-chart.html', 'depth chart page'),
            'capsheet': ('warriors-roster-construction-cap-sheet-2026-27.html', 'cap sheet page'),
            'outlook': ('warriors-2026-27-season-outlook.html', 'season outlook')},
     related=[('warriors-2026-27-roster-depth-chart.html', 'Warriors',
               'The Warriors Depth Chart for 2026-27'),
              ('warriors-2026-27-season-outlook.html', 'Warriors',
               'What the 2026-27 Warriors Actually Are'),
              ('stephen-curry-career-records-three-pointers.html', 'Warriors',
               'Stephen Curry by the Numbers')]),

# ------------------------------------------------- 3. sharks playoff history
dict(slug='sharks-playoff-history',
     section='Sharks', tag='Sharks', hub='Sharks',
     title='San Jose Sharks Playoff History: Every Run, Year by Year',
     h1='San Jose Sharks Playoff History: Every Run, Every Collapse, All of It',
     dek='Twenty-one trips to the postseason, five conference finals, one Stanley Cup Final '
         'and no parade. The complete record, and the nights that still hurt.',
     desc='The complete San Jose Sharks playoff history: all 21 postseason trips, the 1994 '
          'upset, the 2016 Stanley Cup Final, the 2019 comeback and the drought since.',
     date='2026-08-18',
     card=('sharks', 'Sharks Playoff History', 'Every run, year by year'),
     body=[
      "The San Jose Sharks have reached the playoffs twenty-one times in thirty-five seasons. "
      "They have won twenty playoff series and lost twenty-one. They have played in five "
      "conference finals, reached one Stanley Cup Final, in 2016, and lost it to Pittsburgh in "
      "six games. They have never won a Cup, and they have not been in the postseason since "
      "2019. That is the whole record in five sentences, and every one of them is the setup "
      "for a story.",

      "<h2>The complete playoff record, season by season</h2>",

      table('San Jose Sharks postseason results, 1991-92 to 2025-26',
            ['Season', 'How far they got'],
            [['1993-94', 'Beat Detroit in seven, lost to Toronto in the second round'],
             ['1994-95', 'Beat Calgary in seven, swept by Detroit in the second round'],
             ['1997-98', 'Lost to Dallas in the first round'],
             ['1998-99', 'Lost to Colorado in the first round'],
             ['1999-2000', 'Beat St. Louis in seven, lost to Dallas in the second round'],
             ['2000-01', 'Lost to St. Louis in the first round'],
             ['2001-02', 'Beat Phoenix, lost to Colorado in seven in the second round'],
             ['2003-04', 'Beat St. Louis and Colorado, lost the Western Conference Final to Calgary'],
             ['2005-06', 'Beat Nashville, lost to Edmonton in the second round'],
             ['2006-07', 'Beat Nashville, lost to Detroit in the second round'],
             ['2007-08', 'Beat Calgary in seven, lost to Dallas in the second round'],
             ['2008-09', "Presidents' Trophy with 117 points, out in the first round to Anaheim"],
             ['2009-10', 'Beat Colorado and Detroit, swept by Chicago in the conference final'],
             ['2010-11', 'Beat Los Angeles and Detroit, lost the conference final to Vancouver'],
             ['2011-12', 'Lost to St. Louis in the first round'],
             ['2012-13', 'Swept Vancouver, lost to Los Angeles in seven'],
             ['2013-14', 'Led Los Angeles three games to none and lost in seven'],
             ['2015-16', 'Beat Los Angeles, Nashville and St. Louis, lost the Stanley Cup Final to Pittsburgh'],
             ['2016-17', 'Lost to Edmonton in the first round'],
             ['2017-18', 'Swept Anaheim, lost to Vegas in the second round'],
             ['2018-19', 'Beat Vegas and Colorado in seven each, lost the conference final to St. Louis'],
             ['2019-20 to 2025-26', 'Seven straight seasons out of the playoffs']],
            ['21 appearances', '20 series won, 21 series lost, 0 Stanley Cups']),

      "<h2>1994, the upset that put the franchise on the map</h2>",

      "Third season in the league. Second season anybody could stand to watch. The Sharks "
      "finished eighth in the Western Conference with eighty-two points and drew a Detroit "
      "team with a hundred, and the series went the distance. Game 7 was 30 April 1994 at Joe "
      "Louis Arena and Jamie Baker scored at 13:25 of the third to win it 3-2, with Arturs "
      "Irbe standing on his head in goal. It was the first time an eighth seed had ever "
      "beaten a first seed in North American professional sport. Toronto ended the run in the "
      "second round, and nobody in San Jose cared very much, because a franchise that had lost "
      "seventy-one games the year before had just knocked out the best team in hockey.",

      figrow(('irbe',
              'Arturs Irbe, the San Jose Sharks goaltender during the 1994 playoff upset of '
              'the Detroit Red Wings',
              'Irbe, the goalie who made the 1994 upset possible'),
             ('owen-nolan',
              'Owen Nolan, the San Jose Sharks captain through the playoff teams of the late '
              '1990s and early 2000s',
              'Owen Nolan, who captained the next wave of playoff teams')),

      "<h2>The 2000s, when they were good every single year</h2>",

      "This is the part that gets forgotten by everyone outside the market. From 2003-04 "
      "through 2018-19 the Sharks made the playoffs in every season except one. They were not "
      "a plucky little club sneaking in either. In 2008-09 they won the Presidents' Trophy "
      "with fifty-three wins and one hundred and seventeen points, the best record in the "
      "league, and then lost in the first round to Anaheim, which is the single most San Jose "
      "thing that has ever happened.",

      "The conference finals came in 2004 against Calgary, in 2010 against Chicago and in 2011 "
      "against Vancouver. Two of those Chicago and Vancouver teams went on to win Cups. That is "
      "the honest framing of the Joe Thornton and Patrick Marleau years: they ran into the best "
      "teams of the era, repeatedly, at the exact moment it mattered most.",

      figrow(('joe-thornton',
              'Joe Thornton, who spent most of his career with the San Jose Sharks without winning a Stanley Cup',
              'Thornton played fifteen seasons here and never lifted the Cup'),
             ('marleau',
              'Patrick Marleau, the San Jose Sharks all time leader in games played',
              'Marleau, the franchise leader in games, also with no ring')),

      "<h2>2014, the collapse nobody in this market has forgiven</h2>",

      "San Jose won the first three games of the first round against Los Angeles, 6-3, 7-2 and "
      "then 4-3 in overtime on a Patrick Marleau goal. Then they lost four in a row: 6-3, 3-0, "
      "4-1 and 5-1. The Kings became only the fourth team in NHL history to come back from "
      "three games down, and then they went and won the Stanley Cup, which turned a bad week "
      "into a permanent piece of Bay Area sporting folklore. Marleau lost the captaincy in the "
      "aftermath. Thornton lost it too. The franchise spent a year arguing with itself in "
      "public.",

      "<h2>2016, the one time it was actually there</h2>",

      "They got past Los Angeles in five, survived Nashville in seven, and then beat St. Louis "
      "in six to win the Western Conference for the only time in franchise history. Logan "
      "Couture was the leading scorer of the entire postseason. Joe Pavelski wore the C. Martin "
      "Jones played the best hockey of his career. And then Pittsburgh, with Sidney Crosby at "
      "the peak of everything, won the Final in six. Not a sweep, not an embarrassment, just a "
      "better team. It remains the high-water mark and it is now ten years old.",

      figrow(('couture',
              'Logan Couture, who led all scorers in the 2016 NHL playoffs during the San Jose '
              'Sharks run to the Stanley Cup Final',
              'Couture led the entire 2016 postseason in scoring'),
             ('pavelski',
              'Joe Pavelski, the San Jose Sharks captain during the 2016 run to the Stanley '
              'Cup Final',
              'Pavelski wore the C for the only Final this club has reached')),

      "<h2>2019, the loudest four minutes in the building's history</h2>",

      "Game 7 against Vegas, 23 April 2019. San Jose trailed 3-0 in the third period. Cody "
      "Eakin was given a five minute major and a game misconduct on the play that left Joe "
      "Pavelski bleeding on the ice, and in the space of that one power play the Sharks scored "
      "four times, Logan Couture twice, then Tomas Hertl, then Kevin Labanc. Vegas tied it. "
      "Barclay Goodrow won it at 18:19 of overtime. The league later apologised to Vegas for "
      "the call and suspended both referees for the rest of the playoffs, which is a detail "
      "that Sharks fans have decided to live with.",

      "They then beat Colorado in seven and lost the conference final to St. Louis in six. "
      "SAP Center has never been louder than it was on that April night, and unless something "
      "changes it never will be, because that was the last playoff game the San Jose Sharks "
      "have played.",

      fig('sap-center',
          'SAP Center in San Jose, home of the Sharks and the site of the 2019 Game 7 comeback '
          'against the Vegas Golden Knights',
          'The Shark Tank, where the 2019 comeback happened and where the drought is now seven years old'),

      "<h2>The drought, and why this one might finally end</h2>",

      "Seven straight seasons out, from 2019-20 through 2025-26, including back to back "
      "finishes at the bottom of the league. Thornton and Marleau went. The building emptied. "
      "In a region where the Warriors were winning titles and the Giants and 49ers took up all "
      "the oxygen, a bad hockey team in San Jose became genuinely invisible.",

      "Last season was different in a way the standings barely captured. Thirty-nine wins, "
      "eighty-six points, a thirty-four point jump, one of the largest year over year "
      "improvements in club history, and still not enough for a playoff spot. But there is a "
      "twenty year old centre who has already broken Thornton's franchise scoring record and "
      "signed the largest contract in the sport, and that is a completely different starting "
      "point than the last rebuild had. {celebrini} is the page on him.",

      "<h2>What is left to say</h2>",

      "The Sharks are the clearest example in hockey of a specific kind of failure: "
      "consistently very good, never quite great, and unlucky at the exact moments that "
      "decide things. There is no curse and there is no single villain, just a fifteen year "
      "run of teams that met better ones. The broader franchise story is in {history}, the "
      "roster as it stands is on the {depth}, and this season's attempt gets tracked on the "
      "{hub2}. The regional context, including the one line on the ledger with a zero on it, "
      "is on the {ledger}.",
     ],
     links={'celebrini': ('macklin-celebrini-sharks-records-contract.html',
                          'Macklin Celebrini'),
            'history': ('san-jose-sharks-history-no-stanley-cup.html',
                        'our franchise history page'),
            'depth': ('sharks-2026-27-roster-depth-chart.html', 'depth chart'),
            'hub2': ('sharks-2026-27-schedule-season-hub.html', 'season hub'),
            'ledger': ('bay-area-championships-complete-list-by-team.html',
                       'Bay Area championship ledger')},
     related=[('san-jose-sharks-history-no-stanley-cup.html', 'Sharks',
               'Thirty-Five Years, One Final, No Cup'),
              ('when-were-the-san-jose-sharks-founded.html', 'Sharks',
               'When Were the San Jose Sharks Founded?'),
              ('macklin-celebrini-sharks-records-contract.html', 'Sharks',
               'Macklin Celebrini, the Records and the Contract')]),

# ------------------------------------------------- 4. when was san jose sharks founded
dict(slug='when-were-the-san-jose-sharks-founded',
     section='Sharks', tag='Sharks', hub='Sharks',
     title='When Were the San Jose Sharks Founded? The Full Origin Story',
     h1='When Were the San Jose Sharks Founded, and How Did It Actually Happen',
     dek='The short answer is 9 May 1990. The longer answer involves a sold hockey team in '
         'Minnesota, a rejected nickname and two seasons in a livestock arena in Daly City.',
     desc='The San Jose Sharks were founded on 9 May 1990 and began play in 1991-92. The Gund '
          'brothers, the North Stars swap, the Cow Palace years and how they got the name.',
     date='2026-08-18',
     card=('sharks', 'When the Sharks Were Founded', 'The 1990 expansion, the whole story'),
     schema=[faq([
        ("When were the San Jose Sharks founded?",
         "The San Jose Sharks were awarded to Gordon and George Gund III on 9 May 1990, after "
         "the brothers agreed on 5 May 1990 to sell their stake in the Minnesota North Stars. "
         "The team began play in the 1991-92 NHL season."),
        ("When did the San Jose Sharks play their first game?",
         "The Sharks played their first NHL game on 4 October 1991, losing 4-3 to the Vancouver "
         "Canucks at the Pacific Coliseum. Their first win came on 8 October 1991 against "
         "Calgary at the Cow Palace, with Kelly Kisio scoring the winner at 16:45 of the third "
         "period."),
        ("Where did the San Jose Sharks play before SAP Center?",
         "The Sharks played their first two seasons, 1991-92 and 1992-93, at the Cow Palace in "
         "Daly City while their arena in San Jose was being built. They moved into the San Jose "
         "Arena, now SAP Center, for the 1993-94 season."),
        ("How much did the San Jose Sharks expansion franchise cost?",
         "The ownership group paid an expansion fee of 45 million US dollars.")])],
     body=[
      "The San Jose Sharks were founded on 9 May 1990, when the NHL formally approved an "
      "expansion franchise for the San Francisco Bay Area, and they played their first game "
      "on 4 October 1991. If that is all you came for, you can stop reading. But the way it "
      "happened is one of the strangest ownership stories in the history of the league, and it "
      "is worth the extra five minutes.",

      "<h2>It started with a team in Minnesota</h2>",

      "Gordon and George Gund III owned the Minnesota North Stars and did not want to. What "
      "they wanted was a hockey team in the Bay Area, a region they had a history with: the "
      "Gunds had owned the Cleveland Barons, the franchise that began life as the California "
      "Golden Seals in Oakland before it was moved east and eventually folded into Minnesota. "
      "So on 5 May 1990 they agreed to sell their North Stars stake to a group led by Howard "
      "Baldwin, and four days later, on 9 May, the league gave them what they had asked for: "
      "an expansion team for the Bay Area, for an expansion fee of forty-five million dollars.",

      "That trade of a team for a team is why the Sharks did not start from nothing the way "
      "most expansion clubs do. As part of the arrangement, San Jose held a dispersal draft "
      "and took twenty-four players out of the Minnesota organisation, and then went through a "
      "regular expansion draft against the rest of the league. It was still a bad roster. It "
      "was just a bad roster with a head start.",

      "<h2>How they became the Sharks</h2>",

      "The name came from a public contest and more than five thousand entries. The winner of "
      "the vote was Blades. The Gunds rejected it, on the reasonable grounds that a hockey "
      "team named after a weapon was not the image they wanted, and went with the runner up "
      "instead.",

      "Sharks was not a random pick either. The stretch of Pacific water off this coast is "
      "known as the red triangle because of its shark population, which is why there is a "
      "triangle in the logo. Matt Levine, the club's first marketing chief, put the reasoning "
      "plainly at the time: sharks are relentless, determined, swift, agile, bright and "
      "fearless, and the plan was to build an organisation with those qualities. Then they "
      "chose Pacific teal, a colour no professional team in North America was using, and by "
      "the mid nineties that jersey was one of the best selling pieces of merchandise in world "
      "sport. The logo, a shark biting a hockey stick in half, arrived in 1991 and has barely "
      "changed since.",

      "<h2>Two seasons in a cow barn</h2>",

      "Here is the part people forget. The San Jose Sharks did not play in San Jose for the "
      "first two years of their existence. The arena downtown was not built yet, so the club "
      "played the 1991-92 and 1992-93 seasons at the Cow Palace in Daly City, a building that "
      "opened in 1941 and is named after exactly what you think it is named after. It is about "
      "forty miles up the peninsula from San Jose and it is not, by any definition, a modern "
      "NHL arena.",

      fig('cow-palace',
          'The Cow Palace in Daly City, where the San Jose Sharks played their first two NHL '
          'seasons in 1991-92 and 1992-93',
          'The Cow Palace in Daly City, the first home of a team called the San Jose Sharks'),

      "They averaged 10,888 fans in that first season anyway. Bay Area hockey had been gone "
      "since the Seals left in 1976 and there was clearly an audience waiting for it, even in "
      "a livestock hall in the wrong city.",

      "<h2>The first season, and the second one</h2>",

      "Jack Ferreira was the first general manager. George Kingston was the first head coach. "
      "Doug Wilson, acquired from Chicago, was the first captain. The first game was 4 October "
      "1991 at the Pacific Coliseum in Vancouver, a 4-3 loss, and the first win came four days "
      "later on 8 October at the Cow Palace, when Kelly Kisio scored at 16:45 of the third to "
      "beat Calgary. Pat Falloon, the second overall pick in the 1991 draft, led the team with "
      "twenty-five goals and fifty-nine points. Jeff Hackett won eleven games in goal and was "
      "voted the team's most valuable player, which tells you plenty. Link Gaetz took three "
      "hundred and twenty-six penalty minutes, which tells you the rest.",

      fig('doug-wilson',
          'Doug Wilson, the first captain in San Jose Sharks history and later the general '
          'manager of the franchise',
          'Doug Wilson, the first captain, acquired from Chicago before a game had been played'),

      "The record was 17-58-5. And then it got worse. The 1992-93 season finished 11-71-2, one "
      "of the worst records anybody has ever put up in the National Hockey League. Seventy-one "
      "losses. If you were around for it, you remember that the crowd showed up anyway.",

      "<h2>1993, when everything changed at once</h2>",

      "The San Jose Arena opened in 1993, the team finally moved into the city on its jersey, "
      "and in the same season the Sharks made the playoffs for the first time and knocked out "
      "the Detroit Red Wings, who had the best record in the Western Conference. Two years "
      "after one of the worst seasons in league history. The building has been called the Shark "
      "Tank ever since, it is now SAP Center, and it is still the loudest room in Northern "
      "California when the hockey is good.",

      fig('sap-center',
          'SAP Center in San Jose, opened in 1993 as the San Jose Arena and known as the Shark Tank',
          'SAP Center, opened in 1993 as the San Jose Arena, and home ever since'),

      "<h2>Why the origin story still matters</h2>",

      "Because San Jose has kept this team for thirty-five years without once seriously "
      "threatening to move it, in a region that has watched the Raiders leave twice, the "
      "Warriors cross the bay and the A's pack up for Nevada. The {relocations} page is a long "
      "one around here. The Sharks are not on it, and the reason traces directly back to a "
      "family that wanted a Bay Area hockey team badly enough to give up a team in Minnesota "
      "to get one.",

      "The rest of the story is the hard part. Thirty-five years, {playoffs}, one Stanley Cup "
      "Final and no parade. The franchise history is in {history}, the current roster is on the "
      "{depth}, and the season that starts in October gets tracked on the {hub2}.",
     ],
     links={'relocations': ('bay-area-franchise-relocations-teams-that-left.html',
                            'franchise relocations'),
            'playoffs': ('sharks-playoff-history.html', 'twenty-one playoff appearances'),
            'history': ('san-jose-sharks-history-no-stanley-cup.html', 'our franchise history page'),
            'depth': ('sharks-2026-27-roster-depth-chart.html', 'depth chart'),
            'hub2': ('sharks-2026-27-schedule-season-hub.html', 'season hub')},
     related=[('sharks-playoff-history.html', 'Sharks',
               'San Jose Sharks Playoff History, Year by Year'),
              ('san-jose-sharks-history-no-stanley-cup.html', 'Sharks',
               'Thirty-Five Years, One Final, No Cup'),
              ('bay-area-franchise-relocations-teams-that-left.html', 'Bay Area History',
               'Every Bay Area Team That Left')]),

# ------------------------------------------------- 5. bonds giants
dict(slug='barry-bonds-giants-home-run-king',
     section='Giants', tag='Giants', hub='Giants',
     title='Barry Bonds and the Giants: The Years, the Numbers, the Argument',
     h1='Barry Bonds and the Giants: Fifteen Years, 586 Home Runs and an Argument That Will Not End',
     dek='What he actually did in San Francisco, season by season, and why the debate about '
         'him has never been the same debate as the one about how good he was.',
     desc='Barry Bonds played fifteen seasons for the Giants and hit 586 of his 762 home runs '
          'here. The 73 home run year, the 2002 World Series, and the argument.',
     date='2026-08-18',
     card=('giants', 'Bonds and the Giants', 'Fifteen years, 586 home runs'),
     schema=[faq([
        ("How many years did Barry Bonds play for the Giants?",
         "Barry Bonds played fifteen seasons for the San Francisco Giants, from 1993 through "
         "2007, after seven seasons with the Pittsburgh Pirates."),
        ("How many home runs did Barry Bonds hit for the Giants?",
         "Bonds hit 586 of his 762 career home runs with the San Francisco Giants."),
        ("Did Barry Bonds ever win a World Series with the Giants?",
         "No. The closest he came was 2002, when the Giants lost the World Series to the "
         "Anaheim Angels in seven games. Bonds hit .471 with four home runs in that series."),
        ("Have the Giants retired Barry Bonds' number?",
         "Yes. The Giants retired number 25 on 11 August 2018, making Bonds the tenth player "
         "in franchise history to have his number retired.")])],
     body=[
      "Barry Bonds played fifteen seasons for the San Francisco Giants, from 1993 through 2007, "
      "and hit 586 of his 762 career home runs in this uniform. He won five of his seven Most "
      "Valuable Player awards here, four of them in a row. He never won a World Series here. "
      "The Giants retired his number 25 on 11 August 2018 and the Hall of Fame never let him "
      "in. Those facts sit next to each other and they are all true at once, which is more or "
      "less the whole Barry Bonds experience for anybody who watched it from a seat in this "
      "city.",

      table('Barry Bonds with the San Francisco Giants',
            ['', ''],
            [['Seasons', '1993 to 2007, fifteen years'],
             ['Home runs as a Giant', '586 of his 762 career total'],
             ['MVP awards as a Giant', 'Five, including four straight from 2001 to 2004'],
             ['Single season record', '73 home runs in 2001'],
             ['Career walks', '2,558, with 688 of them intentional'],
             ['World Series', 'One appearance, 2002, lost in seven games'],
             ['Number 25', 'Retired by the Giants on 11 August 2018']]),

      "<h2>He came home in 1993</h2>",

      "This part gets glossed over and it should not. Bonds was not a free agent signing who "
      "happened to land here. His father Bobby was a Giant. His godfather is Willie Mays. He "
      "grew up around this organisation, went off to Pittsburgh, won two MVPs there, and then "
      "came back after the 1992 season on what was at the time the largest contract in the "
      "history of the sport. It felt like the family getting its most famous son back, and the "
      "franchise had just been within days of moving to Florida, so it also felt like proof "
      "that the Giants were going to exist.",

      "Then he hit forty-six home runs, drove in a hundred and twenty-three, won the MVP, and "
      "the team won a hundred and three games and missed the playoffs entirely because there "
      "was no wild card yet and Atlanta won a hundred and four. We have written about {y1993} "
      "more than once, because it remains the single most unfair thing that has happened to a "
      "team in this city.",

      figrow(('bonds',
              'Barry Bonds batting for the San Francisco Giants, where he hit 586 of his 762 career home runs',
              'Bonds in San Francisco, where he hit 586 of his 762'),
             ('mays',
              "Willie Mays, Barry Bonds' godfather and the standard every Giants hitter is measured against",
              "Willie Mays, his godfather and the standard he was measured against")),

      "<h2>2001, and the four years that made no sense</h2>",

      "In 2001 he hit seventy-three home runs. The record had been sixty-one for decades before "
      "Mark McGwire pushed it to seventy, and everyone assumed that was the ceiling for a "
      "generation. Bonds went past it in a season that stopped feeling like baseball somewhere "
      "around August.",

      "What followed was the most absurd four year stretch any hitter has ever had. Four "
      "straight MVP awards from 2001 through 2004, giving him seven for his career, which is "
      "three more than anybody else in the history of the game. In 2004 he hit .362 with a .609 "
      "on base percentage, a number that looks like a misprint, and walked two hundred and "
      "thirty-two times, a hundred and twenty of those intentionally. That is not a statistic. "
      "That is opposing managers filing a white flag in the box score, night after night, "
      "because handing him first base was the smarter baseball decision.",

      "By the end he had 2,558 walks and 688 intentional walks, both records that will not be "
      "approached. He is also the only player in the history of baseball with five hundred home "
      "runs and five hundred stolen bases, which is the part of his career that gets buried "
      "under the last decade of it. He was a Gold Glove left fielder eight times and a "
      "fourteen time All Star.",

      "<h2>2002, the one that got away</h2>",

      "The Giants reached the World Series in 2002 and Bonds was unplayable. He hit .471 with "
      "four home runs, he reached base in twenty-one of thirty plate appearances, and the "
      "Angels walked him thirteen times, seven of them intentionally, because the alternative "
      "was worse. His on base percentage for that series was .700, which remains a World Series "
      "record.",

      "And they lost in seven. Game 6 is a wound this city has never properly dressed, a five "
      "run lead in the seventh inning of a game that would have won the franchise its first "
      "title in San Francisco, gone. Bonds did everything a hitter can do in a World Series and "
      "went home without a ring. The Giants would win three of them later, in {evenyear}, with "
      "him retired and watching.",

      fig('oracle-park-real',
          'Oracle Park in San Francisco, where Barry Bonds hit home runs 715 and 756 and where '
          'splash hits land in McCovey Cove',
          'The park was built for him, and the cove behind right field is named for the man before him'),

      "<h2>The chase, 715 and 756</h2>",

      "On 28 May 2006 he hit number 715 off Byung-hyun Kim to pass Babe Ruth. On 7 August 2007 "
      "he hit number 756 off Mike Bacsik of the Washington Nationals to pass Hank Aaron and "
      "become the all time home run king. Both happened at this ballpark, in front of this "
      "city. He played his final major league game on 26 September 2007, went nought for three, "
      "and that was it. The record still stands at 762 and nobody active is remotely close.",

      "The other thing this ballpark gave him was the water. McCovey Cove exists as a piece of "
      "baseball vocabulary largely because of what he did to right field for a decade, and the "
      "{splash} is still mostly his list.",

      "<h2>The argument</h2>",

      "Here is the part nobody gets to dodge. Bonds is tied permanently to the steroid era, he "
      "was the central figure in the BALCO case, and the Hall of Fame voters made their "
      "statement by leaving him out across all ten years of his eligibility. That is the "
      "shadow and it is not lifting.",

      "What the shadow does not do is change what he was before any of it. He won MVPs in 1990 "
      "and 1992 in Pittsburgh as a lean, fast, brilliant defensive left fielder who stole "
      "bases. He was already a first ballot player at twenty-eight. The argument about the "
      "second half of his career is real and it is worth having honestly. The argument about "
      "whether he was the most dangerous hitter anybody in this city ever watched is not an "
      "argument. He was. It is not close.",

      "<h2>What it was actually like</h2>",

      "You did not get up for a hot dog when his spot in the order came around. Nobody did. "
      "Forty thousand people would stop mid sentence and turn toward the plate because there "
      "was a real chance the next four seconds would be something you told people about. "
      "Pitchers refused to throw him strikes and it did not matter. Half the ones he did get "
      "ended up in the bay.",

      "The Giants retired 25 in 2018 with Willie Mays standing next to him. Whatever the "
      "national conversation decided about Barry Bonds, San Francisco settled its own version "
      "of it a long time ago. The rest of our Giants coverage is on the {hub}, the other MVP in "
      "those lineups is {kent}, and the wider regional record is in {history}.",
     ],
     links={'y1993': ('giants-1993-pennant-race-braves-103-wins-wild-card.html',
                      'the 1993 pennant race'),
            'evenyear': ('giants-dynasty-even-year-magic.html', '2010, 2012 and 2014'),
            'splash': ('oracle-park-mccovey-cove-splash-hits-guide.html', 'splash hit list'),
            'kent': ('jeff-kent-giants-mvp-second-baseman.html', 'Jeff Kent'),
            'history': ('bay-area-sports-history.html', 'Bay Area sports history'),
            'hub': ('../giants.html', 'Giants hub')},
     related=[('jeff-kent-giants-mvp-second-baseman.html', 'Giants',
               'Jeff Kent, the Other MVP in That Lineup'),
              ('giants-dynasty-even-year-magic.html', 'Giants',
               'Even Year Magic: The Giants Dynasty'),
              ('oracle-park-mccovey-cove-splash-hits-guide.html', 'Giants',
               'McCovey Cove and the Splash Hit List')]),

# ------------------------------------------------- 6. cal game schedule
dict(slug='cal-2026-schedule-game-by-game-acc',
     section='Cal', tag='Cal', hub='Cal',
     title='Cal Football Schedule 2026: Every Game, Date, Time and TV',
     h1='The Cal Football Schedule for 2026, Game by Game',
     dek='All twelve games, kickoff times and networks where they are set, plus where this '
         'season is actually won or lost.',
     desc='The full Cal Golden Bears 2026 football schedule: every game, date, kickoff time '
          'and TV network, from the UCLA opener to the Big Game on 21 November.',
     date='2026-08-18',
     card=('cal', 'Cal Football Schedule 2026', 'All twelve games, dates and TV'),
     body=[
      "Cal opens the 2026 season at home against UCLA on Saturday 5 September at 7:30pm on "
      "ESPN, and finishes at home against Pittsburgh on 28 November. The Big Game against "
      "Stanford is at Memorial Stadium on 21 November. Here is the whole thing, with kickoff "
      "times and networks where they have been set.",

      table('California Golden Bears 2026 football schedule',
            ['Date', 'Opponent', 'Site', 'Time (PT) and TV'],
            [['Sat 5 Sep', 'UCLA', 'Berkeley', '7:30pm, ESPN'],
             ['Sat 12 Sep', 'at Syracuse', 'JMA Wireless Dome', '12:30pm, ACC Network'],
             ['Sat 19 Sep', 'Wagner', 'Berkeley', '12:30pm, ACC Network'],
             ['Fri 25 Sep', 'Clemson', 'Berkeley', '7:30pm, ESPN'],
             ['Sat 3 Oct', 'at UNLV', 'Allegiant Stadium, Las Vegas', '12:30pm, CBS Sports Network'],
             ['Sat 10 Oct', 'Virginia Tech', 'Berkeley', 'Time to be announced'],
             ['Sat 17 Oct', 'Wake Forest', 'Berkeley', 'Time to be announced'],
             ['Sat 24 Oct', 'at SMU', 'Gerald J. Ford Stadium, Dallas', 'Time to be announced'],
             ['Sat 31 Oct', 'at NC State', 'Carter-Finley Stadium, Raleigh', 'Time to be announced'],
             ['Sat 7 Nov', 'Open date', '', ''],
             ['Sat 14 Nov', 'at Virginia', 'Scott Stadium, Charlottesville', 'Time to be announced'],
             ['Sat 21 Nov', 'Stanford, the Big Game', 'Berkeley', 'Time to be announced'],
             ['Sat 28 Nov', 'Pittsburgh', 'Berkeley', 'Time to be announced']],
            ['Seven home games', 'Four road games, one neutral', 'Bye on 7 November']),

      fig('memorial-stadium',
          'California Memorial Stadium in Berkeley, where Cal plays seven home games in 2026 '
          'including the Big Game against Stanford',
          'Seven games in Berkeley this year, including the Big Game on 21 November'),

      "<h2>September</h2>",

      "UCLA on the 5th matters more than its billing. A home win over a Los Angeles school in "
      "Tosh Lupoi's first game as head coach sets a tone that the whole building can feel, and "
      "this program has spent a decade badly needing a September that starts well. Syracuse on "
      "the road a week later is the kind of trip that used to be unimaginable for a Berkeley "
      "team and is now just part of life in the ACC. Wagner is a breather. Clemson on Friday "
      "night the 25th is the measuring stick, in prime time, at home, on ESPN, and nobody "
      "outside Strawberry Canyon expects Cal to win it, which is exactly why a close one would "
      "be worth something.",

      fig('tosh-lupoi',
          'Tosh Lupoi, the Cal Golden Bears head coach going into his first season in charge '
          'in 2026',
          'Lupoi played on this offensive line. Now he gets the whole thing'),

      "<h2>October</h2>",

      "This is the month. UNLV in Las Vegas on the 3rd is a real road game in a real stadium "
      "against a program that has been better than Cal recently, and there is no polite way to "
      "say that. Then Virginia Tech and Wake Forest at home on consecutive Saturdays, which are "
      "the two most winnable ACC games on the schedule and therefore the two that decide "
      "everything. Take both and this team is alive in November. Split them and it is another "
      "year of almost.",

      "The back half of the month is a two week trip, SMU in Dallas on the 24th and NC State in "
      "Raleigh on the 31st. Come out of it 1-1 with the bye week waiting and the season is "
      "still in front of this team. Come out 0-2 and the Big Game becomes the only thing left "
      "to play for, which is not nothing around here, but it is not what this roster was built "
      "for.",

      "<h2>November</h2>",

      "An open date on the 7th, Virginia on the road on the 14th, then Stanford at home on the "
      "21st and Pitt on the 28th to close. A bye before a three game finish is a gift to a "
      "first year staff. Finishing the Big Game at Memorial Stadium is a bigger one.",

      "One warning about that sequence, because it is genuinely strange. Ending with Stanford "
      "and then Pitt means the emotional peak of the season arrives with one game still left "
      "to play. Teams have been known to win the Big Game and then no show the following "
      "Saturday. If Cal is chasing a bowl bid in late November, that Pittsburgh game is going "
      "to matter far more than anybody wants it to.",

      "<h2>Who is not on this schedule</h2>",

      "Miami, Louisville and Florida State. Three of the names that actually decide the ACC, "
      "and Cal does not play any of them. In a conference this lopsided that is worth more than "
      "any preseason ranking anybody hands out, and combined with Jaron-Keawe Sagapolutele "
      "choosing to come back it gives this program the most favourable set up it has been "
      "handed in years. The full case is in the {preview}.",

      "<h2>The trap game</h2>",

      "Wagner on 19 September, and not for the reason you think. Nobody loses that game. The "
      "risk is where it sits, between a road trip to Syracuse and the biggest home game of the "
      "non conference schedule against Clemson. A team with a new staff gets one week where the "
      "intensity naturally drops, immediately before the game everybody has circled. Programs "
      "still learning who they are have a habit of showing up flat the following Saturday.",

      "<h2>The bowl maths, plainly</h2>",

      "Six wins gets Cal to a bowl game. Look at the twelve dates and count honestly. Wagner "
      "is one. UCLA at home in the opener is a coin flip. UNLV on the road, Virginia Tech and "
      "Wake Forest at home, Syracuse away, Virginia away and Pittsburgh at home are the seven "
      "games in the middle where a bowl either happens or does not, and Cal needs five of "
      "those seven. Clemson and the Big Game are their own category, one a genuine long shot "
      "and one a game where the record stops mattering entirely.",

      "That is not an unreasonable ask. It is also not a gift, and this program has spent "
      "several seasons finding a way to lose exactly two of the games in that middle group "
      "that it had no business losing. The margin here is small enough that one bad "
      "Saturday in October is the whole difference.",

      "<h2>How this page works</h2>",

      "Kickoff times for the second half of the season get released in windows, usually about "
      "twelve days out, and this table gets updated as they land, along with results once the "
      "season starts. The reason a team from Berkeley is playing in Raleigh at all is covered "
      "in {realignment}. Stanford's schedule is {stanford}, the history of the game that "
      "closes the home season is in {biggame}, and basketball season has its own page now at "
      "{hoops}. Everything else is on the {hub}.",
     ],
     links={'preview': ('cal-2026-season-preview-lupoi-sagapolutele.html', 'season preview'),
            'realignment': ('cal-stanford-acc-realignment-what-changed.html',
                            'our realignment explainer'),
            'stanford': ('stanford-2026-schedule-game-by-game-acc.html', 'here'),
            'biggame': ('big-game-cal-stanford-rivalry-history.html', 'the Big Game history'),
            'hoops': ('cal-basketball-schedule-2026-27.html', 'the Cal basketball schedule'),
            'hub': ('../cal.html', 'Cal hub')},
     related=[('cal-2026-season-preview-lupoi-sagapolutele.html', 'Cal',
               'Cal 2026: Lupoi, Sagapolutele and a Real Chance'),
              ('cal-basketball-schedule-2026-27.html', 'Cal',
               'Cal Basketball Schedule 2026-27'),
              ('big-game-cal-stanford-rivalry-history.html', 'Cal',
               'The Big Game: A Rivalry History')]),

# ------------------------------------------------- 7. cal basketball schedule 2026
dict(slug='cal-basketball-schedule-2026-27',
     section='Cal', tag='Cal', hub='Cal',
     title='Cal Basketball Schedule 2026-27: Every Game Announced',
     h1='The Cal Basketball Schedule for 2026-27, and Everything Announced So Far',
     dek='The non conference slate is out, the ACC opponents are set, and the dates for '
         'conference play are still coming. Here is the whole picture, kept current.',
     desc='The Cal basketball schedule for 2026-27: the announced non conference games, every '
          'ACC opponent home and away, and the 2025-26 results for reference.',
     date='2026-08-18',
     card=('cal', 'Cal Basketball 2026-27', 'The schedule, as it is announced'),
     body=[
      "Cal opens the 2026-27 basketball season at home against Radford on 4 November, hosts "
      "USC on 11 November and Vanderbilt on 6 December, and plays eighteen ACC games with "
      "Stanford home and away. The non conference schedule was released on 16 August. The ACC "
      "opponents and sites were announced back in May, but the conference dates have not been "
      "published yet, so the second half of this page is a list of opponents rather than a "
      "calendar. It gets filled in here as soon as the league puts the dates out.",

      "<h2>Non conference schedule</h2>",

      table('Cal non conference schedule, 2026-27 (announced 16 August)',
            ['Date', 'Opponent', 'Site'],
            [['Wed 4 Nov', 'Radford', 'Haas Pavilion'],
             ['Wed 11 Nov', 'USC', 'Haas Pavilion'],
             ['Sat 14 Nov', 'Utah Tech', 'Haas Pavilion'],
             ['Thu 19 Nov', 'East Texas A&amp;M', 'Haas Pavilion'],
             ['Mon 23 Nov', 'Alabama State', 'Haas Pavilion'],
             ['Sat 28 Nov', 'Minnesota', 'Sanford Pentagon, Sioux Falls'],
             ['Wed 2 Dec', 'at Utah', 'Salt Lake City'],
             ['Sun 6 Dec', 'Vanderbilt', 'Haas Pavilion'],
             ['Thu 10 Dec', 'Southeastern Louisiana', 'Haas Pavilion'],
             ['Sat 12 Dec', 'UC Riverside', 'Haas Pavilion'],
             ['Sun 20 Dec', 'Southern', 'Haas Pavilion'],
             ['Tue 22 Dec', 'Northeastern', 'Haas Pavilion']],
            ['Eleven home games', 'One road game, one neutral', 'More dates to be added']),

      "Eleven of the thirteen non conference games are at Haas, one is at Utah and one is in "
      "South Dakota. That is a schedule built to bank wins before Christmas, and there is "
      "nothing wrong with that as long as the two real tests get taken seriously. USC on 11 "
      "November and Vanderbilt on 6 December are the games that will tell you something. Both "
      "are expected to be near the top of their conferences and both are at home, which is "
      "exactly the kind of game Cal needs to start winning if the NCAA tournament is ever going "
      "to be a real conversation in Berkeley again.",

      fig('haas-pavilion',
          'Haas Pavilion in Berkeley, where Cal plays eleven non conference home games and nine '
          'ACC home games in the 2026-27 season',
          'Twenty home games at Haas this season if the ACC dates hold to form'),

      "<h2>ACC opponents</h2>",

      "The ACC plays an eighteen game conference schedule made up of two home and away series, "
      "seven home only opponents and seven road only opponents, with one league team missed "
      "entirely each year. Cal draws Stanford and NC State twice, which means the Bay Area "
      "rivalry is on the calendar home and away again, and the team they do not play in "
      "2026-27 is Georgia Tech.",

      table('Cal ACC opponents, 2026-27 (dates not yet released)',
            ['Format', 'Opponents'],
            [['Home and away', 'Stanford, NC State'],
             ['At Haas Pavilion', 'Boston College, Florida State, Miami, Syracuse, Virginia, '
              'Virginia Tech, Wake Forest'],
             ['On the road', 'Clemson, Duke, Louisville, North Carolina, Notre Dame, '
              'Pittsburgh, SMU'],
             ['Not played', 'Georgia Tech']],
            ['Eighteen games', 'Nine at home, nine away']),

      "That road list is brutal. Duke, North Carolina, Louisville and Clemson away from home in "
      "one season is about as difficult a set of trips as this conference can hand out, and it "
      "is going to be worth remembering in March when somebody looks at the record without "
      "looking at where the games were played. The flip side is that Florida State, Miami, "
      "Virginia and Syracuse all have to come to Berkeley, and Haas at full volume on a "
      "Saturday is still a genuinely hard place to play.",

      "<h2>Where the program actually is</h2>",

      "Cal went 22-12 last season and 9-9 in the ACC in Mark Madsen's third year, tied for "
      "ninth in the league, and reached the second round of the NIT before Saint Joseph's won "
      "at Haas by a point. That was the best Cal team in a decade. It also started 12-1, the "
      "program's best start since 1959-60, then went .500 in conference play, which is the part "
      "that stings. There were real wins in there: North Carolina at home, UCLA on a neutral "
      "floor, both games against Stanford, a one point win at Miami.",

      fig('mark-madsen',
          'Mark Madsen, the Cal Golden Bears head basketball coach going into his fourth season '
          'in 2026-27',
          "Madsen's fourth year, coming off the program's best season in a decade"),

      "<h2>Why the schedule matters more than usual this year</h2>",

      "Because the roster turned over again. Cal has spent the last three offseasons rebuilding "
      "through the portal, and 2026-27 is no different: Jordan Ross arrives at guard by way of "
      "Georgia and Saint Mary's, Michael Cooper comes in from Wright State after leading his "
      "team in scoring, Nojus Indrusaitis arrives from Pitt, Jake Wilkins and Amier Ali add "
      "size on the wing, and Lee Dort is back in the middle. Madsen said in the summer that he "
      "had not settled on a starting five or a rotation, which is a normal thing for a coach "
      "to say in July and an entirely honest thing to say about this particular roster.",

      "A team that is still figuring out who it is benefits enormously from eleven home games "
      "before conference play. It also means the November results will look better than the "
      "team actually is, and everybody in Berkeley should keep that in mind before the "
      "December schedule turns serious.",

      "<h2>When the ACC dates come out</h2>",

      "The conference typically releases its full basketball calendar with dates and television "
      "windows in the late summer or early autumn, after the opponents and sites have already "
      "been published in the spring. The opponents above are confirmed. The dates are not. When "
      "they land, the table gets rebuilt as a proper calendar, and the two Stanford games will "
      "be the first ones anybody looks for. The history of that rivalry, on the football side "
      "at least, is in {biggame}.",

      "<h2>Last season, game by game</h2>",

      "Keeping this here because a lot of people searching for the Cal basketball schedule are "
      "actually looking for what happened in 2026, not what is coming.",

      table('Cal basketball 2025-26 results',
            ['Date', 'Opponent', 'Result'],
            [['3 Nov', 'CSU Bakersfield', 'Won 87-60'],
             ['6 Nov', 'Wright State', 'Won 77-67'],
             ['10 Nov', 'Cal State Fullerton', 'Won 93-65'],
             ['13 Nov', 'at Kansas State', 'Lost 96-99'],
             ['18 Nov', 'Presbyterian', 'Won 67-57'],
             ['21 Nov', 'Sacramento State', 'Won 91-67'],
             ['25 Nov', 'UCLA, neutral', 'Won 80-72'],
             ['2 Dec', 'Utah', 'Won 79-72'],
             ['6 Dec', 'Pacific', 'Won 67-61'],
             ['9 Dec', 'Dominican', 'Won 93-71'],
             ['13 Dec', 'Northwestern State', 'Won 79-70'],
             ['19 Dec', 'Morgan State', 'Won 97-50'],
             ['21 Dec', 'Columbia', 'Won 74-56'],
             ['30 Dec', 'Louisville', 'Lost 70-90'],
             ['2 Jan', 'Notre Dame', 'Won 72-71'],
             ['7 Jan', 'at Virginia', 'Lost 60-84'],
             ['10 Jan', 'at Virginia Tech', 'Lost 75-78'],
             ['14 Jan', 'Duke', 'Lost 56-71'],
             ['17 Jan', 'North Carolina', 'Won 84-78'],
             ['24 Jan', 'at Stanford', 'Won 78-66'],
             ['28 Jan', 'at Florida State', 'Lost 61-63'],
             ['31 Jan', 'at Miami', 'Won 86-85'],
             ['4 Feb', 'Georgia Tech', 'Won 90-85'],
             ['7 Feb', 'Clemson', 'Lost 55-77'],
             ['11 Feb', 'at Syracuse', 'Lost 100-107 in double overtime'],
             ['14 Feb', 'at Boston College', 'Won 86-75'],
             ['21 Feb', 'Stanford', 'Won 72-66'],
             ['25 Feb', 'SMU', 'Won 73-69'],
             ['28 Feb', 'Pittsburgh', 'Lost 56-72'],
             ['4 Mar', 'at Georgia Tech', 'Won 76-65'],
             ['7 Mar', 'at Wake Forest', 'Lost 73-80'],
             ['11 Mar', 'Florida State, ACC tournament', 'Lost 89-95'],
             ['18 Mar', 'UIC, NIT first round', 'Won 91-73'],
             ['22 Mar', "Saint Joseph's, NIT second round", 'Lost 75-76']],
            ['Final record', '22-12 overall, 9-9 ACC', 'NIT second round']),

      "<h2>How this page works</h2>",

      "This is a live page, not a one time post. The ACC dates go in as soon as the conference "
      "releases them, tip times and television go in as they are set, and results go in through "
      "the winter. Football has its own schedule page at {football}, the reason a Berkeley team "
      "plays in Chapel Hill in the first place is covered in {realignment}, and everything else "
      "Cal is on the {hub}.",
     ],
     links={'football': ('cal-2026-schedule-game-by-game-acc.html', 'the 2026 Cal football schedule'),
            'realignment': ('cal-stanford-acc-realignment-what-changed.html',
                            'our realignment explainer'),
            'biggame': ('big-game-cal-stanford-rivalry-history.html', 'the Big Game history'),
            'hub': ('../cal.html', 'Cal hub')},
     related=[('cal-2026-schedule-game-by-game-acc.html', 'Cal',
               'The Cal Football Schedule for 2026'),
              ('cal-stanford-acc-realignment-what-changed.html', 'Cal',
               'What ACC Realignment Actually Changed'),
              ('big-game-cal-stanford-rivalry-history.html', 'Cal',
               'The Big Game: A Rivalry History')]),
]


def main():
    check = '--check' in sys.argv
    for a in ARTICLES:
        p = os.path.join(ROOT, 'articles', a['slug'] + '.html')
        card = os.path.join(CARDS, a['slug'] + '.jpg')
        words = sum(len(re.sub(r'<[^>]+>', ' ', x).split()) for x in a['body'])
        links = sum(x.count('{') for x in a['body'])
        print('  %-46s %5dw  %2d links  title %2d  desc %3d'
              % (a['slug'][:46], words, links, len(a['title']), len(a['desc'])))
        if check:
            continue
        if not os.path.exists(card):
            subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'cardgen.py'),
                            a['card'][0], a['card'][1], a['card'][2], card], check=True)
        html_out = build(a)
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write(html_out)
        b = open(p, 'rb').read()
        if b'\x00' in b or b.count(b'\xef\xbf\xbd'):
            raise SystemExit('corruption writing %s' % p)
    print('%s  %d articles' % ('CHECK' if check else 'WROTE', len(ARTICLES)))


if __name__ == '__main__':
    main()
