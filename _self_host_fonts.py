#!/usr/bin/env python3
"""_self_host_fonts.py - serve the site's fonts from this domain.

The head currently loads a stylesheet from fonts.googleapis.com, which then
points at fonts.gstatic.com. That is a third-party origin, its own DNS and TLS
handshake, and a render-blocking round trip before any text can settle.

This downloads the exact files that stylesheet serves, writes @font-face rules
into the stylesheets the site already loads (so there is no new request at all),
and removes the Google Fonts markup from every head.

Same families, weights, styles and unicode-ranges. font-display:swap is kept as
it was, so there is no FOIT and no new swap behaviour. The font-family stacks in
the CSS - and therefore every system fallback - are untouched.

Fraunces, Archivo and Archivo Narrow are SIL Open Font License 1.1; the licence
text ships in assets/fonts/.

  python _self_host_fonts.py --fetch     download woff2 + licences (no edits)
  python _self_host_fonts.py [--check]   write the @font-face css, strip the head
  python _self_host_fonts.py --revert    put the Google Fonts markup back
"""
import os, re, sys, glob, json, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(ROOT, 'assets', 'fonts')
CSS_FILES = ['assets/desk.css', 'assets/style.css']
KEEP_SUBSETS = ('latin', 'latin-ext')   # the site is English; see the README note
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36')
LICENCES = {
    'OFL-fraunces.txt': 'https://raw.githubusercontent.com/google/fonts/main/ofl/fraunces/OFL.txt',
    'OFL-archivo.txt': 'https://raw.githubusercontent.com/google/fonts/main/ofl/archivo/OFL.txt',
    'OFL-archivo-narrow.txt': 'https://raw.githubusercontent.com/google/fonts/main/ofl/archivonarrow/OFL.txt',
}

MARK = '<!-- fonts: preconnect + stylesheet in head (was an @import chained behind the site CSS) -->'
HEAD_BLOCK_RE = re.compile(
    re.escape(MARK) + r'\n'
    r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\n'
    r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\n'
    r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/[^"]+)">\n')
CSS_MARK = '/* Self-hosted fonts.'


def rd(p):
    return open(os.path.join(ROOT, p), encoding='utf-8', errors='strict').read()


def wr(p, s):
    full = os.path.join(ROOT, p)
    with open(full, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)
    b = open(full, 'rb').read()
    if b'\x00' in b or b.count(b'\xef\xbf\xbd'):
        raise SystemExit('corruption writing %s - ABORT' % p)


def google_url():
    for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        m = HEAD_BLOCK_RE.search(open(f, encoding='utf-8', errors='replace').read())
        if m:
            return m.group(1)
    return None


def get(url, binary=True):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=90) as f:
        return f.read() if binary else f.read().decode('utf-8')


def faces(url):
    css = get(url, binary=False)
    out = []
    for sub, body in re.findall(r'/\*\s*([a-z\-]+)\s*\*/\s*@font-face\s*\{(.*?)\}', css, re.S):
        if sub not in KEEP_SUBSETS:
            continue
        fam = re.search(r"font-family:\s*'([^']+)'", body).group(1)
        style = re.search(r'font-style:\s*([^;]+);', body).group(1).strip()
        wght = re.search(r'font-weight:\s*([^;]+);', body).group(1).strip()
        src = re.search(r'url\((https://[^)]+\.woff2)\)', body).group(1)
        urange = re.search(r'unicode-range:\s*([^;]+);', body).group(1).strip()
        name = '%s-%s-%s-%s.woff2' % (fam.lower().replace(' ', '-'), wght, style, sub)
        out.append(dict(fam=fam, style=style, wght=wght, src=src, urange=urange,
                        sub=sub, name=name))
    return out


def fetch(url):
    os.makedirs(FONT_DIR, exist_ok=True)
    rows = faces(url)
    got = 0
    for r in rows:
        p = os.path.join(FONT_DIR, r['name'])
        if not os.path.exists(p):
            open(p, 'wb').write(get(r['src']))
            got += 1
        r['bytes'] = os.path.getsize(p)
    for name, u in LICENCES.items():
        p = os.path.join(FONT_DIR, name)
        if not os.path.exists(p):
            open(p, 'wb').write(get(u))
    json.dump(rows, open(os.path.join(ROOT, '_fonts_manifest.json'), 'w',
                         encoding='utf-8'), indent=1)
    print('fetched %d new woff2 (%d faces, %.0f KB total) + %d licences'
          % (got, len(rows), sum(r['bytes'] for r in rows) / 1024.0, len(LICENCES)))
    return rows


def face_css(rows):
    out = ['/* Self-hosted fonts. Same families, weights, styles and unicode-ranges',
           '   that fonts.googleapis.com served; files taken from that same stylesheet.',
           '   Fraunces, Archivo and Archivo Narrow are SIL Open Font License 1.1;',
           '   see assets/fonts/OFL-*.txt. font-display:swap is unchanged. */']
    for r in sorted(rows, key=lambda r: (r['fam'], r['style'], int(r['wght']), r['sub'])):
        out.append("@font-face{font-family:'%s';font-style:%s;font-weight:%s;"
                   "font-display:swap;src:url(fonts/%s) format('woff2');"
                   "unicode-range:%s}" % (r['fam'], r['style'], r['wght'],
                                          r['name'], r['urange']))
    return '\n'.join(out) + '\n'


# The faces the masthead and nav paint with on every page. Self-hosting moved
# first paint about a second earlier, which meant the browser started painting
# in Georgia/Arial before these arrived and then swapped - visible as a jump in
# CLS. Preloading exactly these four gets them in flight with the stylesheet.
PRELOAD = [
    'fraunces-900-normal-latin.woff2',      # "Bay Area" in the wordmark
    'fraunces-900-italic-latin.woff2',      # "Sports Blog" in the wordmark
    'archivo-400-normal-latin.woff2',       # body copy
    'archivo-narrow-700-normal-latin.woff2',  # nav, kickers, labels
]
PRELOAD_MARK = '<!-- fonts: preload the faces the masthead paints with -->'


def preload_block(prefix):
    out = [PRELOAD_MARK]
    for f in PRELOAD:
        out.append('<link rel="preload" as="font" type="font/woff2" '
                   'href="%sassets/fonts/%s" crossorigin>' % (prefix, f))
    return '\n'.join(out) + '\n'


def pages():
    return ([os.path.basename(f) for f in sorted(glob.glob(os.path.join(ROOT, '*.html')))]
            + ['articles/' + os.path.basename(f)
               for f in sorted(glob.glob(os.path.join(ROOT, 'articles', '*.html')))]
            + ['daily/' + os.path.basename(f)
               for f in sorted(glob.glob(os.path.join(ROOT, 'daily', '*.html')))])


def main():
    check = '--check' in sys.argv
    url = google_url() or json.load(open(os.path.join(ROOT, '_fonts_url.json'))) \
        if os.path.exists(os.path.join(ROOT, '_fonts_url.json')) else google_url()

    if '--fetch' in sys.argv:
        if not url:
            raise SystemExit('no Google Fonts url found in any head')
        fetch(url)
        return

    if '--revert' in sys.argv:
        raise SystemExit('revert with git: git checkout -- assets/ *.html articles/ daily/')

    mf = os.path.join(ROOT, '_fonts_manifest.json')
    if not os.path.exists(mf):
        raise SystemExit('run --fetch first')
    rows = json.load(open(mf, encoding='utf-8'))
    missing = [r['name'] for r in rows
               if not os.path.exists(os.path.join(FONT_DIR, r['name']))]
    if missing:
        raise SystemExit('missing font files, refusing to strip Google Fonts: %s'
                         % missing[:3])

    block = face_css(rows)
    n_css = 0
    for c in CSS_FILES:
        s0 = rd(c)
        if CSS_MARK in s0:
            continue
        n_css += 1
        if not check:
            wr(c, block + s0)

    n_html, n_pre = 0, 0
    do_preload = '--preload' in sys.argv
    for pg in pages():
        s0 = rd(pg)
        s = HEAD_BLOCK_RE.sub('', s0)
        if s != s0:
            n_html += 1
        if do_preload and PRELOAD_MARK not in s:
            m = re.search(r'<link rel="stylesheet" href="([^"]*)assets/[^"]*\.css">', s)
            if m:
                s = s[:m.start()] + preload_block(m.group(1)) + s[m.start():]
                n_pre += 1
        if s != s0 and not check:
            wr(pg, s)

    print('%s  css files %d, pages stripped %d, preloads added %d, faces %d'
          % ('CHECK' if check else 'APPLIED', n_css, n_html, n_pre, len(rows)))


if __name__ == '__main__':
    main()
