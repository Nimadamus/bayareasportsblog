#!/usr/bin/env python3
"""_gen_eeat.py - build the trust pages (editorial standards, corrections,
privacy and ownership) and wire them into the site's identity schema.

Every page is the about.html template with its own <article> content, so the
chrome, CSS and footer are identical to what is already published. The author
identity stays organizational: Bay Area Sports Blog Staff, no named person.

Also:
- index.html Organization node becomes a NewsMediaOrganization carrying
  publishingPrinciples, correctionsPolicy, ethicsPolicy and ownershipFundingInfo
  pointing at these pages, which is the machine-readable half of E-E-A-T
- the shared footers gain links to the three new pages

  python _gen_eeat.py [--check]
"""
import os, re, sys, glob, json

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://bayareasportsblog.com/"
TEMPLATE = 'about.html'

PAGES = {
    'editorial-standards.html': {
        'tag': 'Standards',
        'h1': 'Editorial Standards',
        'title': 'Editorial Standards | Bay Area Sports Blog',
        'desc': "How Bay Area Sports Blog covers the Bay Area: what is opinion, "
                "what is fact, where the numbers come from, and what this blog "
                "will never do.",
        'body': """
<p>Bay Area Sports Blog is an independent, fan-run site covering the 49ers,
Giants, Athletics, Warriors, Sharks, Stanford and Cal. This page explains how
the coverage works, so you know what you are reading before you argue with it.</p>

<h3 style="margin-top:30px">Opinion, and we say so</h3>
<p>Almost everything here is opinion and commentary written from a Bay Area
fan's point of view. It is not neutral and it does not pretend to be. When a
column says a hire was a mistake or a front office blew it, that is a judgment,
not a news report, and it is presented as one.</p>

<h3 style="margin-top:30px">Where the facts come from</h3>
<p>Scores, records, statistics and dates come from official league box scores
and league data. Quotes are what the person actually said. Numbers in a story
are checked against the box score before the story goes up, and a story is
never built on a rumor presented as a fact &mdash; if something is reported
rather than confirmed, the story says it is reported.</p>

<h3 style="margin-top:30px">What this blog does not do</h3>
<ul>
<li>No wire copy is republished here. Every column is written for this site.</li>
<li>No sponsored posts and no paid placements. If that ever changes it will be
disclosed on the <a href="privacy.html">ownership page</a> before it runs.</li>
<li>No headline that the story does not support.</li>
<li>No quietly deleting a story that aged badly. See the
<a href="corrections.html">corrections policy</a>.</li>
</ul>

<h3 style="margin-top:30px">Independence</h3>
<p>Bay Area Sports Blog is not affiliated with, endorsed by or paid by any
team, league, network or sportsbook. Nobody gets a favorable column here
because of a relationship, and nobody loses one either.</p>

<h3 style="margin-top:30px">Betting content</h3>
<p>The betting section is opinion about numbers and angles. It is not advice,
it is not a service, and nothing on this site is a guarantee of anything.
Bet responsibly or, better yet, do not.</p>

<h3 style="margin-top:30px">Getting it wrong</h3>
<p>Mistakes get fixed in the open. The
<a href="corrections.html">corrections policy</a> explains exactly how, and the
<a href="contact.html">contact page</a> is how you tell us about one.</p>
""",
    },
    'corrections.html': {
        'tag': 'Corrections',
        'h1': 'Corrections Policy',
        'title': 'Corrections Policy | Bay Area Sports Blog',
        'desc': "How Bay Area Sports Blog handles mistakes: what gets corrected, "
                "how a corrected story is marked, and how to report an error you "
                "have spotted.",
        'body': """
<p>This site gets things wrong sometimes. When it does, the fix is public and
the record shows it was fixed. That is the whole policy, and the detail is
below.</p>

<h3 style="margin-top:30px">What gets corrected</h3>
<ul>
<li>Wrong scores, records, statistics, dates or standings.</li>
<li>Misattributed or misquoted statements.</li>
<li>Names, positions and roles that are wrong.</li>
<li>Anything reported as fact that turns out not to be.</li>
</ul>

<h3 style="margin-top:30px">What does not get corrected</h3>
<p>An opinion you disagree with is not an error. A prediction that did not come
true is not an error either &mdash; the take stays up, wrong, where everyone
can see it. Taking down a bad call after the fact is the one thing this blog
will not do.</p>

<h3 style="margin-top:30px">How a correction is made</h3>
<p>The story is fixed at the source rather than left standing with a note
somewhere else. The <code>dateModified</code> on the story is updated so the
change is visible to readers and to search engines. When a correction changes
the substance of a story &mdash; not a typo, but a fact the argument rested on
&mdash; a short correction note is added to the story itself saying what was
wrong and when it was fixed.</p>

<h3 style="margin-top:30px">How to report one</h3>
<p>Send it through the <a href="contact.html">contact page</a>. Include the
story and what is wrong with it. Corrections are read and acted on, and you do
not have to be polite about it.</p>
""",
    },
    'privacy.html': {
        'tag': 'Ownership',
        'h1': 'Privacy and Ownership',
        'title': 'Privacy and Ownership | Bay Area Sports Blog',
        'desc': "Who runs Bay Area Sports Blog, how it is funded, and what "
                "happens to your data when you read it. Short version: an "
                "independent site, no trackers.",
        'body': """
<h3>Who runs this</h3>
<p>Bay Area Sports Blog is an independently owned and operated site. It is not
affiliated with, endorsed by or funded by any team, league, network or
sportsbook. Editorial decisions are made by Bay Area Sports Blog staff and by
nobody else.</p>

<h3 style="margin-top:30px">How it is funded</h3>
<p>The site currently runs no advertising, no sponsored posts, no affiliate
placements and no paid subscriptions. If any of that changes, it will be
disclosed on this page and labelled in the stories it affects, before it
runs.</p>

<h3 style="margin-top:30px">What data this site collects</h3>
<p>Bay Area Sports Blog is a static site. There are no accounts, no logins, no
newsletter list and no analytics or advertising trackers on these pages. You
can read the entire site without giving it anything.</p>
<p>Like any site on the internet, the hosting provider that serves these pages
may keep standard server logs, which typically include an IP address, a
timestamp and the page requested. That is the hosting provider's normal
operation, not a profile this site builds or uses.</p>

<h3 style="margin-top:30px">Third-party content</h3>
<p>Where a page embeds a video from an official league channel, that provider
serves the video and may set its own cookies under its own privacy policy.
Nothing about that embed is controlled by this site.</p>

<h3 style="margin-top:30px">Photos and rights</h3>
<p>Photo credits and licences are listed on the <a href="about.html">about
page</a>. If you hold rights to an image used here and want it credited
differently or removed, use the <a href="contact.html">contact page</a> and it
will be handled.</p>

<h3 style="margin-top:30px">Questions</h3>
<p>Anything not answered here goes through the
<a href="contact.html">contact page</a>. See also the
<a href="editorial-standards.html">editorial standards</a> and the
<a href="corrections.html">corrections policy</a>.</p>
""",
    },
}

# links appended to the two shared footers
FOOT_SIMPLE_OLD = '<a href="contact.html">Contact</a>'
FOOT_SIMPLE_NEW = ('<a href="contact.html">Contact</a> &middot; '
                   '<a href="editorial-standards.html">Standards</a> &middot; '
                   '<a href="corrections.html">Corrections</a>')
FOOT_DESK_OLD = '<a href="about.html">About</a> &middot; <a href="contact.html">Contact</a>'
FOOT_DESK_NEW = ('<a href="about.html">About</a> &middot; '
                 '<a href="contact.html">Contact</a> &middot; '
                 '<a href="editorial-standards.html">Standards</a> &middot; '
                 '<a href="corrections.html">Corrections</a> &middot; '
                 '<a href="privacy.html">Privacy</a>')

ABOUT_EXTRA = """
<h3 style="margin-top:30px">How this blog works</h3>
<p>Bay Area Sports Blog publishes game coverage, columns and flashbacks across
the 49ers, Giants, Athletics, Warriors, Sharks, Stanford and Cal, plus a
betting section and a history section for the stuff worth remembering. Stories
are written for this site, not aggregated from a wire.</p>
<p>Three pages explain the rest: the
<a href="editorial-standards.html">editorial standards</a> say what is opinion
and where the facts come from, the
<a href="corrections.html">corrections policy</a> says what happens when
something is wrong, and the <a href="privacy.html">privacy and ownership</a>
page says who runs the site, how it is funded and what it does with your data.
The short answer to that last one is nothing.</p>
"""


def rd(p):
    return open(os.path.join(ROOT, p), encoding='utf-8', errors='strict').read()


def wr(p, s):
    full = os.path.join(ROOT, p)
    with open(full, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)
    b = open(full, 'rb').read()
    if b'\x00' in b or b.count(b'\xef\xbf\xbd'):
        raise SystemExit('corruption writing %s - ABORT' % p)


def build(page, cfg, tpl):
    url = BASE + page
    head_end = tpl.index('</head>')
    head, rest = tpl[:head_end], tpl[head_end:]

    def rep(rx, val, s):
        return re.sub(rx, lambda m: m.group(1) + val + m.group(3), s, count=1)

    head = rep(r'(<title>)(.*?)(</title>)', cfg['title'], head)
    head = rep(r'(<meta name="description" content=")([^"]*)(")', cfg['desc'], head)
    head = rep(r'(<link rel="canonical" href=")([^"]*)(")', url, head)
    head = rep(r'(<meta property="og:url" content=")([^"]*)(")', url, head)
    head = rep(r'(<meta property="og:title" content=")([^"]*)(")', cfg['h1'], head)
    head = rep(r'(<meta name="twitter:title" content=")([^"]*)(")', cfg['h1'], head)
    head = rep(r'(<meta property="og:description" content=")([^"]*)(")', cfg['desc'], head)
    head = rep(r'(<meta name="twitter:description" content=")([^"]*)(")', cfg['desc'], head)
    head = rep(r'(<meta property="og:image:alt" content=")([^"]*)(")',
               'Bay Area Sports Blog: ' + cfg['h1'], head)

    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList",
              "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
                  {"@type": "ListItem", "position": 2, "name": cfg['h1'],
                   "item": url}]}
    head = re.sub(r'<script type="application/ld\+json">\{[^<]*"BreadcrumbList".*?</script>',
                  '<script type="application/ld+json">%s</script>'
                  % json.dumps(crumbs, separators=(',', ':')), head, count=1, flags=re.S)

    body = ('<article class="article"><span class="tag">%s</span><h1>%s</h1>\n'
            '<div class="byline">Bay Area Sports Blog Staff</div>\n%s</article>'
            % (cfg['tag'], cfg['h1'], cfg['body'].strip()))
    a0 = rest.index('<article class="article">')
    a1 = rest.index('</article>') + len('</article>')
    return head + rest[:a0] + body + rest[a1:]


def upgrade_identity(s):
    """index.html Organization -> NewsMediaOrganization with the policy links."""
    m = re.search(r'<script type="application/ld\+json">(\{[^<]*"Organization"[^<]*\})</script>', s)
    if not m:
        return s
    node = json.loads(m.group(1))
    node['@type'] = 'NewsMediaOrganization'
    node['publishingPrinciples'] = BASE + 'editorial-standards.html'
    node['correctionsPolicy'] = BASE + 'corrections.html'
    node['ethicsPolicy'] = BASE + 'editorial-standards.html'
    node['ownershipFundingInfo'] = BASE + 'privacy.html'
    node['diversityPolicy'] = BASE + 'editorial-standards.html'
    return s.replace(m.group(1), json.dumps(node, separators=(',', ':'),
                                            ensure_ascii=False), 1)


def main():
    check = '--check' in sys.argv
    tpl = rd(TEMPLATE)

    for page, cfg in PAGES.items():
        html = build(page, cfg, tpl)
        old = rd(page) if os.path.exists(os.path.join(ROOT, page)) else ''
        if old == html:
            continue
        print('%-26s %s' % (page, 'would write' if check else 'written'))
        if not check:
            wr(page, html)

    # about.html gains the trust-page links and a scope paragraph
    a = rd('about.html')
    if 'editorial-standards.html' not in a:
        a = a.replace('<h3 style="margin-top:30px">Photo Credits</h3>',
                      ABOUT_EXTRA.strip() + '\n<h3 style="margin-top:30px">Photo Credits</h3>', 1)
        print('about.html                 %s' % ('would extend' if check else 'extended'))
        if not check:
            wr('about.html', a)

    # footers, sitewide
    n = 0
    for f in (sorted(glob.glob(os.path.join(ROOT, '*.html')))
              + sorted(glob.glob(os.path.join(ROOT, 'articles', '*.html')))):
        rel = os.path.relpath(f, ROOT).replace(os.sep, '/')
        s0 = rd(rel)
        s = s0
        if 'editorial-standards.html">Standards' not in s:
            if FOOT_DESK_OLD in s:
                s = s.replace(FOOT_DESK_OLD, FOOT_DESK_NEW, 1)
            elif FOOT_SIMPLE_OLD in s:
                s = s.replace(FOOT_SIMPLE_OLD, FOOT_SIMPLE_NEW, 1)
            else:
                # article footers link up a level and end on About
                old = '<a href="../about.html">About</a>'
                if old in s:
                    s = s.replace(old, old + ' &middot; '
                                  '<a href="../editorial-standards.html">Standards</a>'
                                  ' &middot; '
                                  '<a href="../corrections.html">Corrections</a>', 1)
        if rel == 'index.html':
            s = upgrade_identity(s)
        if s != s0:
            n += 1
            if not check:
                wr(rel, s)
    print('footers/identity updated on %d pages%s' % (n, ' (check)' if check else ''))


if __name__ == '__main__':
    main()
