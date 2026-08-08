#!/usr/bin/env python3
"""_font_loading.py - take Google Fonts out of the critical request chain.

Today the font stylesheet is pulled in with an @import at the top of desk.css
and style.css. That serialises three round trips before anything can paint:
  HTML -> desk.css -> fonts.googleapis.com/css2 -> fonts.gstatic.com/*.woff2

This moves the font stylesheet into <head> and adds preconnects, so the font
CSS and the site CSS are fetched in parallel instead of one after the other.

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="<same url>">

The stylesheet is still render-blocking, deliberately. Loading it asynchronously
(rel=preload + onload swap) was measured and was worse: the LCP element here is
the Fraunces wordmark, so an async swap paints it in the fallback face first and
repaints later - LCP moved out and CLS went 0.021 -> 0.044, TBT 0 -> 120 ms.
Removing the chain gets the paint win without the repaint cost.

The URL is byte-for-byte the one already in the CSS, so the families, weights,
axes and display=swap are all unchanged - same fonts, same rendered result.
Nothing else in the head, body, CSS or copy is touched.

  python _font_loading.py [--check] [--revert]
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
CSS_FILES = ['assets/desk.css', 'assets/style.css']
IMPORT_RE = re.compile(r'^@import url\((\'|")(https://fonts\.googleapis\.com/[^\'"]+)\1\);\s*\n',
                       re.M)
MARK = '<!-- fonts: preconnect + stylesheet in head (was an @import chained behind the site CSS) -->'


def rd(p):
    return open(os.path.join(ROOT, p), encoding='utf-8', errors='strict').read()


def wr(p, s):
    full = os.path.join(ROOT, p)
    with open(full, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)
    b = open(full, 'rb').read()
    if b'\x00' in b or b.count(b'\xef\xbf\xbd'):
        raise SystemExit('corruption writing %s - ABORT' % p)


def font_url():
    for c in CSS_FILES:
        m = IMPORT_RE.search(rd(c))
        if m:
            return m.group(2)
    # already stripped: recover it from a page that has the head block
    for f in glob.glob(os.path.join(ROOT, '*.html')):
        m = re.search(r'<link rel="stylesheet" href="([^"]+fonts\.googleapis[^"]+)">',
                      open(f, encoding='utf-8', errors='replace').read())
        if m:
            return m.group(1)
    return None


def head_block(url):
    return (
        '%s\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="%s">\n' % (MARK, url))


def pages():
    return ([os.path.basename(f) for f in sorted(glob.glob(os.path.join(ROOT, '*.html')))]
            + ['articles/' + os.path.basename(f)
               for f in sorted(glob.glob(os.path.join(ROOT, 'articles', '*.html')))]
            + ['daily/' + os.path.basename(f)
               for f in sorted(glob.glob(os.path.join(ROOT, 'daily', '*.html')))])


def main():
    check = '--check' in sys.argv
    revert = '--revert' in sys.argv
    url = font_url()
    if not url:
        raise SystemExit('could not find the Google Fonts url')

    n_css, n_html = 0, 0

    for c in CSS_FILES:
        s0 = rd(c)
        if revert:
            if '@import url(' not in s0:
                s = re.sub(r'(^/\*.*?\*/\s*\n)?', lambda m: (m.group(0) or '')
                           + "@import url('%s');\n" % url, s0, count=1, flags=re.S)
                n_css += 1
                if not check:
                    wr(c, s)
            continue
        s = IMPORT_RE.sub('', s0)
        if s != s0:
            n_css += 1
            if not check:
                wr(c, s)

    for pg in pages():
        s0 = rd(pg)
        if revert:
            s = re.sub(re.escape(MARK) + r'\n(?:<link[^>]*>\n|<noscript>[^\n]*</noscript>\n)+',
                       '', s0)
        else:
            if MARK in s0 or '<head>' not in s0:
                continue
            # sits directly before the site stylesheet so both fetch together
            m = re.search(r'<link rel="stylesheet" href="[^"]*\.css">', s0)
            if not m:
                continue
            s = s0[:m.start()] + head_block(url) + s0[m.start():]
        if s != s0:
            n_html += 1
            if not check:
                wr(pg, s)

    print('%s%s  css files %d, pages %d'
          % ('CHECK ' if check else 'APPLIED ', ' (revert)' if revert else '',
             n_css, n_html))
    print('  font url: %s' % url[:110])


if __name__ == '__main__':
    main()
