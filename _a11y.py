#!/usr/bin/env python3
"""_a11y.py: bring every page on the site up to WCAG 2.1 AA, as measured by axe-core.

Run against the whole site this fixes four families of finding that axe reported on
2026-08-18, when the seven Search Console pages were published and the rest of the site
was audited for the first time:

  landmark-one-main   pages had no main landmark at all
  region              blocks of content sat outside any landmark
  heading-order       heading levels skipped, so a screen reader outline had holes
  label               the contact form inputs were not associated with their labels

Everything here is additive markup: attributes, ids, and one landmark wrapper inserted
between the existing header and footer. That wrapper is a div carrying role="main" and
not a <main> element, because assets/style.css styles `main` as a boxed container and a
real <main> visibly redraws betting, cal, contact and stanford. No copy changes, no
layout changes, no CSS class changes. The colour contrast failures are fixed separately in assets/desk.css and
assets/style.css, because those are stylesheet values rather than markup.

Reads and writes BYTES so the CRLF line endings on this repo survive untouched.

  python _a11y.py [--check]
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP = {'google6f74b54ecd988601.html'}

RE_H = re.compile(rb'<h([1-6])\b([^>]*)>')
RE_ARIA_LEVEL = re.compile(rb'aria-level\s*=')


def add_attrs(tag, attrs):
    """Insert attributes just before the closing angle bracket of an open tag."""
    return tag[:-1].rstrip() + b' ' + attrs + b'>'


def fix_main_landmark(s):
    """Every page needs exactly one main landmark."""
    if re.search(rb'<main[\s>]', s) or b'role="main"' in s:
        return s, 0
    # article template: the <article class="article"> IS the main content
    m = re.search(rb'<article class="article"[^>]*>', s)
    if m:
        s = s[:m.start()] + add_attrs(m.group(0),
                                      b'role="main" aria-labelledby="article-title"') + s[m.end():]
        h1 = re.search(rb'<h1(?![^>]*\bid=)([^>]*)>', s)
        if h1:
            s = s[:h1.start()] + add_attrs(h1.group(0), b'id="article-title"') + s[h1.end():]
        return s, 1
    # desk template: wrap everything between the header and the footer.
    # NOT a <main> element. assets/style.css styles `main` as a boxed container with a
    # max-width, border, padding and shadow, so inserting a real <main> visibly redraws
    # betting, cal, contact and stanford. A div carrying role="main" is the same landmark
    # to a screen reader and carries no styling at all.
    i, j = s.find(b'</header>'), s.find(b'<footer')
    if i == -1 or j == -1 or j < i:
        return s, 0
    i += len(b'</header>')
    return s[:i] + b'\n<div role="main">' + s[i:j] + b'</div>\n' + s[j:], 1


def fix_orphans_before_main(s):
    """index.html keeps a visually hidden h1 and the ticker above <main>, which leaves
    them outside every landmark. Move the opening <main> up above them instead of moving
    the elements, so the homepage geometry is untouched."""
    m = re.search(rb'<main>', s)
    if not m:
        return s, 0
    h1 = re.search(rb'<h1[\s>]', s)
    if not h1 or h1.start() > m.start():
        return s, 0
    body = s[h1.start():m.start()]
    if b'<footer' in body or b'</header>' in body:
        return s, 0
    return s[:h1.start()] + b'<main>\n' + body + s[m.end():], 1


def fix_desk_top(s):
    """The utility bar above the masthead sits outside every landmark, so screen reader
    users who navigate by landmark skip straight past the date and the quick links.
    Naming it as a region puts it back on the map without moving a single pixel."""
    m = re.search(rb'<div class="desk-top"(?![^>]*role=)[^>]*>', s)
    if not m:
        return s, 0
    s = (s[:m.start()]
         + add_attrs(m.group(0), b'role="region" aria-label="Today and quick links"')
         + s[m.end():])
    n = 1
    d = re.search(rb'<div class="dt-r"(?![^>]*role=)[^>]*>', s)
    if d:
        s = (s[:d.start()]
             + add_attrs(d.group(0), b'role="navigation" aria-label="Quick links"')
             + s[d.end():])
    return s, n


def fix_related_landmark(s):
    """The related-columns block sits outside the article, so it needs its own name."""
    m = re.search(rb'<section class="related">(\s*)<h3>([^<]*)</h3>', s)
    if not m:
        return s, 0
    return (s[:m.start()]
            + b'<section class="related" aria-labelledby="related-heading">' + m.group(1)
            + b'<h3 id="related-heading">' + m.group(2) + b'</h3>'
            + s[m.end():]), 1


def fix_scrollable_tables(s):
    """A .reftable scrolls sideways on a phone, so it must be reachable and named."""
    n = 0
    out, pos = [], 0
    for m in re.finditer(rb'<div class="reftable"(?![^>]*role=)[^>]*>', s):
        cap = re.search(rb'<caption[^>]*>(.*?)</caption>', s[m.end():m.end() + 4000], re.S)
        label = b'Reference table'
        if cap:
            label = re.sub(rb'<[^>]+>', b'', cap.group(1)).strip()
            label = (label.replace(b'&rsquo;', b"'").replace(b'&amp;', b'and')
                          .replace(b'&middot;', b',').replace(b'&nbsp;', b' '))
            label = re.sub(rb'\s+', b' ', label) or b'Reference table'
        out.append(s[pos:m.start()])
        out.append(add_attrs(m.group(0),
                             b'role="region" tabindex="0" aria-label="' + label + b'"'))
        pos = m.end()
        n += 1
    out.append(s[pos:])
    return b''.join(out), n


def fix_heading_order(s):
    """Never let a heading level skip. Where the markup does, the real level is declared
    with role=heading and aria-level, which leaves the visual styling exactly alone."""
    out, pos, prev, n = [], 0, 0, 0
    for m in RE_H.finditer(s):
        lvl = int(m.group(1))
        attrs = m.group(2)
        if RE_ARIA_LEVEL.search(attrs):
            prev = int(RE_ARIA_LEVEL.split(attrs)[1].strip(b' "\'')[0:1] or lvl)
            continue
        if prev and lvl > prev + 1:
            want = prev + 1
            out.append(s[pos:m.start()])
            out.append(add_attrs(m.group(0),
                                 b'role="heading" aria-level="%d"' % want))
            pos = m.end()
            prev = want
            n += 1
        else:
            prev = lvl
    out.append(s[pos:])
    return b''.join(out), n


def fix_contact_labels(s):
    """The contact form labels were floating next to their inputs, not tied to them."""
    n = 0
    for label, field, fid in ((b'Name', b'name', b'cf-name'),
                              (b'Email', b'email', b'cf-email'),
                              (b'Message', b'message', b'cf-message')):
        m = re.search(rb'<label>' + label + rb'</label><(input|textarea)([^>]*name="'
                      + field + rb'"[^>]*)>', s)
        if not m:
            continue
        tag = b'<%s%s id="%s">' % (m.group(1), m.group(2), fid)
        s = s[:m.start()] + b'<label for="' + fid + b'">' + label + b'</label>' + tag + s[m.end():]
        n += 1
    return s, n


def main():
    check = '--check' in sys.argv
    files = sorted(glob.glob(os.path.join(ROOT, '*.html'))
                   + glob.glob(os.path.join(ROOT, 'articles', '*.html')))
    totals = dict(main=0, desktop=0, related=0, tables=0, headings=0, labels=0, files=0)
    for p in files:
        if os.path.basename(p) in SKIP:
            continue
        orig = open(p, 'rb').read()
        s = orig
        s, a = fix_main_landmark(s)
        s, f = fix_desk_top(s)
        s, g = fix_orphans_before_main(s)
        s, b = fix_related_landmark(s)
        s, c = fix_scrollable_tables(s)
        s, d = fix_heading_order(s)
        e = 0
        if os.path.basename(p) == 'contact.html':
            s, e = fix_contact_labels(s)
        if s == orig:
            continue
        totals['main'] += a; totals['desktop'] += f; totals['related'] += b
        totals['tables'] += c; totals['main'] += g
        totals['headings'] += d; totals['labels'] += e; totals['files'] += 1
        print('  %-52s main=%d utilbar=%d related=%d tables=%d headings=%d labels=%d'
              % (os.path.relpath(p, ROOT), a, f, b, c, d, e))
        if check:
            continue
        if b'\x00' in s:
            raise SystemExit('refusing to write null bytes into %s' % p)
        open(p, 'wb').write(s)
    print('%s  files=%d  main=%d utilbar=%d related=%d tables=%d headings=%d labels=%d'
          % ('CHECK' if check else 'WROTE', totals['files'], totals['main'], totals['desktop'],
             totals['related'], totals['tables'], totals['headings'], totals['labels']))


if __name__ == '__main__':
    main()
