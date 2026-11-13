#!/usr/bin/env python3
"""injury_autolink.py: point injury talk in our articles at the live injury reports.

1. Every article that is about a team with an injury report and talks about an injury
   (injury, injured, IR, injured list, out for the season, day to day, surgery, ...) gets
   one plain line at the end of the article body:
       "Who else is hurt? The 49ers injury report is updated through the day."
   The line sits between <!-- inj-link --> markers, so reruns replace it rather than add
   another, and an article that already links the report in its own words is left alone.
2. nfl.html gets a short "Injury reports" row (Raiders and 49ers) under its hero, between
   <!-- nfl-inj --> markers.

Idempotent; runs in the daily refresh so new articles pick it up.

    python tools/injury_autolink.py
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK = 'style="color:var(--gold);text-decoration:underline;text-underline-offset:3px"'
# articleSection -> (report slug, team name in the sentence)
SECTION = {'49ers': ('49ers-injury-report', '49ers'), 'Warriors': ('warriors-injury-report', 'Warriors'),
           'Giants': ('giants-injury-report', 'Giants'), 'Athletics': ('athletics-injury-report', "A's"),
           'Sharks': ('sharks-injury-report', 'Sharks')}
# NFL section stories are mostly Raiders, but some are league stories: require the word.
RAIDERS = ('raiders-injury-report', 'Raiders')
HURT = re.compile(r'\binjur|\binjured reserve\b|\binjured list\b|\bon IR\b|out for the season|season.ending|'
                  r'day to day|\bsurgery\b|\btorn\b|\bsprain|\bstrain|\bconcussion', re.I)
MARK = re.compile(r'\r?\n?<!-- inj-link -->.*?<!-- /inj-link -->', re.S)
NFL_MARK = re.compile(r'<!-- nfl-inj -->.*?<!-- /nfl-inj -->\r?\n?', re.S)


def body_text(t):
    m = re.search(r'<article class="article".*?</article>', t, re.S)
    return re.sub(r'<[^>]+>', ' ', m.group(0)) if m else ''


def target(t, slug):
    if slug.endswith('injury-report'):
        return None
    sec = re.search(r'"articleSection":"(.*?)"', t)
    sec = sec.group(1) if sec else ''
    if sec in SECTION:
        return SECTION[sec]
    if sec == 'NFL' and re.search(r'\bRaiders\b', body_text(t)):
        return RAIDERS
    return None


def articles():
    n = 0
    for path in glob.glob(os.path.join(ROOT, 'articles', '*.html')):
        slug = os.path.basename(path)[:-5]
        t = open(path, encoding='utf-8', newline='').read()
        clean = MARK.sub('', t)
        tgt = target(clean, slug)
        new = clean
        if tgt and HURT.search(body_text(clean)):
            rep, team = tgt
            m = re.search(r'<article class="article".*?</article>', clean, re.S)
            if ('href="%s.html"' % rep) not in m.group(0):
                nl = '\r\n' if '\r\n' in clean else '\n'
                line = ('%s<!-- inj-link --><p>Who else is hurt? The <a href="%s.html" %s>%s injury report</a> '
                        'is updated through the day, with every player\'s status and when he is expected back.</p>'
                        '<!-- /inj-link -->' % (nl, rep, LINK, team))
                # before the "More coverage" footer line when there is one, else before </article>
                art = m.group(0)
                k = art.rfind('<p style="margin-top:30px')
                k = k if k != -1 else art.rfind('</article>')
                art = art[:k].rstrip() + line + nl + '  ' + art[k:].lstrip()
                new = clean[:m.start()] + art + clean[m.end():]
        if new != t:
            open(path, 'w', encoding='utf-8', newline='').write(new)
            n += 1
    return n


def nfl_page():
    path = os.path.join(ROOT, 'nfl.html')
    t = open(path, encoding='utf-8', newline='').read()
    block = ('<!-- nfl-inj --><section class="zone tight"><div class="wrap"><div style="font-size:15px;line-height:1.55">'
             '<b>Injury reports:</b> <a href="articles/raiders-injury-report.html" %s>Raiders injury report</a> &middot; '
             '<a href="articles/49ers-injury-report.html" %s>49ers injury report</a> &middot; '
             '<a href="articles/bay-area-injury-report.html" %s>Every Bay Area team</a>'
             '</div></div></section><!-- /nfl-inj -->\r\n' % (LINK, LINK, LINK))
    clean = NFL_MARK.sub('', t)
    hero_end = clean.index('</div></section>', clean.index('<section class="sec-hero"')) + len('</div></section>')
    nl = '\r\n' if '\r\n' in clean else '\n'
    new = clean[:hero_end] + nl + block.rstrip('\r\n') + clean[hero_end:]
    if new != t:
        open(path, 'w', encoding='utf-8', newline='').write(new)
        return 1
    return 0


if __name__ == '__main__':
    print('injury autolink: %d articles, nfl.html %d' % (articles(), nfl_page()))
