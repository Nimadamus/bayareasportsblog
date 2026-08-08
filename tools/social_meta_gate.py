#!/usr/bin/env python3
"""social_meta_gate.py - one og:image per page, and it must be the page's own card.

The defect this fixes: 50 pages carried two social blocks in <head>. The early one had
the page's real card; the later, template-generated one was filled with the generic
`welcome-to-bay-area-sports-blog.jpg`. Result: two `og:image` tags per page with
different values, so which image a given crawler shows was undefined - Facebook takes
the first, several others take the last. Sharing an article could surface the generic
site card instead of the article's own.

Fifteen pages had the same problem on `twitter:image`, and thirty-five had exactly one
`twitter:image` which was the generic card - deleting that one would leave none, so it
gets rewritten to the page's own image instead.

Rules applied, all conservative:
  og:image          keep the FIRST (the page's own card). Drop later ones ONLY if they
                    point at the generic welcome card; anything else is reported, not
                    touched.
  twitter:image     >1 -> keep the first, drop generic ones. Exactly 1 and generic while
                    og:image differs -> rewrite it to the og:image value.
  og:type, twitter:card, twitter:title, twitter:description
                    keep the FIRST, drop later duplicates. The first is the one that
                    matches <title> / <meta description> / og:title on every affected
                    page, so this also makes the set self-consistent.

Ordering note: `og:image:width` / `og:image:height` / `og:image:alt` sit after the
removed tag in these files. Per the Open Graph spec those structured properties attach
to the preceding `og:image`, so removing the later duplicate makes them describe the
surviving card - which is the intent.

  python tools/social_meta_gate.py           # fix
  python tools/social_meta_gate.py --check   # report only, exits 2 if anything is wrong
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERIC = 'welcome-to-bay-area-sports-blog.jpg'

# The page that legitimately owns the generic card.
OWNER = 'welcome-to-bay-area-sports-blog'

DEDUPE = ['og:type', 'twitter:card', 'twitter:title', 'twitter:description']


def prop_re(tag):
    kind = 'property' if tag.startswith('og:') else 'name'
    return re.compile(r'[ \t]*<meta %s="%s" content="([^"]*)">\n?' % (kind, re.escape(tag)))


def values(s, tag):
    return prop_re(tag).findall(s)


def drop_nth(s, tag, keep_index=0, only_if=None):
    """Remove every occurrence of `tag` except the one at keep_index.

    If `only_if` is given, an occurrence is removed only when the predicate accepts its
    value; occurrences that fail the predicate are left in place and reported."""
    out, skipped, i = [], [], 0
    rx = prop_re(tag)
    res, pos = [], 0
    for m in rx.finditer(s):
        res.append(m)
    if len(res) < 2:
        return s, []
    new, last = [], 0
    for i, m in enumerate(res):
        if i == keep_index:
            continue
        if only_if and not only_if(m.group(1)):
            skipped.append(m.group(1))
            continue
        new.append(m)
    for m in new:
        out.append(s[last:m.start()])
        last = m.end()
    out.append(s[last:])
    return ''.join(out), skipped


def fix_file(path, check):
    slug = os.path.splitext(os.path.basename(path))[0]
    s0 = open(path, encoding='utf-8').read()
    s = s0
    notes, problems = [], []

    og = values(s, 'og:image')
    if slug != OWNER and len(og) > 1:
        s, skipped = drop_nth(s, 'og:image', 0, only_if=lambda v: GENERIC in v)
        removed = len(og) - len(values(s, 'og:image'))
        if removed:
            notes.append('og:image -%d' % removed)
        for v in skipped:
            problems.append('%s: extra og:image is not the generic card: %s' % (slug, v))

    # An article's canonical social image is its own 1200x675 card. The pages here
    # declare og:image:width/height as 1200x675, so pointing og:image at anything else
    # (a portrait player photo, say) makes the declared dimensions a lie and the card
    # render badly. twitter:image is left alone - a different image there is editorial.
    own_card = os.path.join(ROOT, 'assets', 'img', 'cards', slug + '.jpg')
    if (slug != OWNER and os.sep + 'articles' + os.sep in path
            and os.path.exists(own_card)):
        want = 'https://bayareasportsblog.com/assets/img/cards/%s.jpg' % slug
        cur = values(s, 'og:image')
        if len(cur) == 1 and cur[0] != want:
            s = s.replace('<meta property="og:image" content="%s">' % cur[0],
                          '<meta property="og:image" content="%s">' % want, 1)
            notes.append('og:image -> own card')

    primary = (values(s, 'og:image') or [''])[0]
    tw = values(s, 'twitter:image')
    if slug != OWNER:
        if len(tw) > 1:
            s, skipped = drop_nth(s, 'twitter:image', 0, only_if=lambda v: GENERIC in v)
            removed = len(tw) - len(values(s, 'twitter:image'))
            if removed:
                notes.append('twitter:image -%d' % removed)
            for v in skipped:
                problems.append('%s: extra twitter:image is not the generic card: %s'
                                % (slug, v))
        elif len(tw) == 1 and GENERIC in tw[0] and primary and GENERIC not in primary:
            s = s.replace('<meta name="twitter:image" content="%s">' % tw[0],
                          '<meta name="twitter:image" content="%s">' % primary, 1)
            notes.append('twitter:image retargeted')

    for tag in DEDUPE:
        v = values(s, tag)
        if len(v) > 1:
            s, _ = drop_nth(s, tag, 0)
            notes.append('%s -%d' % (tag, len(v) - len(values(s, tag))))

    if s == s0:
        return None, problems

    if check:
        return notes, problems

    with open(path, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)
    b = open(path, 'rb').read()
    if b'\x00' in b or b.count(b'\xef\xbf\xbd'):
        raise SystemExit('corruption writing %s - ABORT' % path)
    return notes, problems


def main():
    check = '--check' in sys.argv
    pages = sorted(glob.glob(os.path.join(ROOT, 'articles', '*.html'))
                   + glob.glob(os.path.join(ROOT, '*.html')))
    touched, all_problems = 0, []
    for p in pages:
        notes, problems = fix_file(p, check)
        all_problems += problems
        if notes:
            touched += 1
            print('  %-56s %s' % (os.path.basename(p)[:56], ', '.join(notes)))
    for msg in all_problems:
        print('  PROBLEM  %s' % msg)

    print('SOCIAL META GATE  pages=%d  %s=%d  problems=%d'
          % (len(pages), 'needing fixes' if check else 'fixed', touched,
             len(all_problems)))
    if check and (touched or all_problems):
        raise SystemExit(2)
    if all_problems:
        raise SystemExit(2)
    if not check:
        print('GATE PASSED.' if not touched else 'FIXED %d pages.' % touched)


if __name__ == '__main__':
    main()
