#!/usr/bin/env python3
"""_webp.py - add WebP alongside every served JPEG/PNG and offer it via <picture>.

The <img> tag is left exactly as it is - same src, alt, width, height, loading
and fetchpriority - and is simply wrapped:

    <picture><source type="image/webp" srcset="...webp"><img src="...jpg" ...></picture>

So the JPEG stays the real, canonical file. og:image, twitter:image and the
JSON-LD image nodes all keep pointing at the JPEG, which is what social and
search crawlers want, and any browser without WebP support still gets the JPEG.
CSS is unaffected: no rule on this site targets img as a direct child.

  python _webp.py [--check] [--quality 82]
"""
import os, re, sys, glob, json

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
QUALITY = 82
MIN_GAIN = 0.05

IMG_RE = re.compile(r'<img\s[^>]*>')
SRC_RE = re.compile(r'src="([^"]+)"')


def local_path(src):
    u = src.replace('https://bayareasportsblog.com/', '').lstrip('./')
    while u.startswith('../'):
        u = u[3:]
    return u


def build_webp(quality, check):
    made, saved_b, saved_a = 0, 0, 0
    srcs = set()
    for f in (glob.glob(os.path.join(ROOT, '*.html'))
              + glob.glob(os.path.join(ROOT, 'articles', '*.html'))
              + glob.glob(os.path.join(ROOT, 'daily', '*.html'))):
        s = open(f, encoding='utf-8', errors='replace').read()
        for m in IMG_RE.finditer(s):
            sm = SRC_RE.search(m.group(0))
            if sm and re.search(r'\.(jpg|jpeg|png)$', sm.group(1), re.I):
                srcs.add(local_path(sm.group(1)))
    for rel in sorted(srcs):
        full = os.path.join(ROOT, rel)
        if not os.path.exists(full):
            continue
        out = os.path.splitext(full)[0] + '.webp'
        jb = os.path.getsize(full)
        if os.path.exists(out):
            saved_b += jb
            saved_a += os.path.getsize(out)
            continue
        if check:
            made += 1
            continue
        im = Image.open(full)
        im.load()
        im.convert('RGB').save(out, 'WEBP', quality=quality, method=6)
        im.close()
        wb = os.path.getsize(out)
        if wb >= jb * (1 - MIN_GAIN):     # WebP not worth it for this one
            os.remove(out)
            continue
        made += 1
        saved_b += jb
        saved_a += wb
    return made, saved_b, saved_a, sorted(srcs)


def wrap(page, check):
    p = os.path.join(ROOT, page)
    s0 = open(p, encoding='utf-8', errors='strict').read()
    out, pos, n = [], 0, 0
    for m in IMG_RE.finditer(s0):
        sm = SRC_RE.search(m.group(0))
        if not sm:
            continue
        src = sm.group(1)
        if not re.search(r'\.(jpg|jpeg|png)$', src, re.I):
            continue
        webp_rel = os.path.splitext(local_path(src))[0] + '.webp'
        if not os.path.exists(os.path.join(ROOT, webp_rel)):
            continue
        # already wrapped?
        if s0[max(0, m.start() - 220):m.start()].rfind('<picture>') > \
           s0[max(0, m.start() - 220):m.start()].rfind('</picture>'):
            continue
        webp_src = re.sub(r'\.(jpg|jpeg|png)$', '.webp', src, flags=re.I)
        out.append(s0[pos:m.start()])
        out.append('<picture><source type="image/webp" srcset="%s">%s</picture>'
                   % (webp_src, m.group(0)))
        pos = m.end()
        n += 1
    if not n:
        return 0
    out.append(s0[pos:])
    s = ''.join(out)
    if not check:
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write(s)
        b = open(p, 'rb').read()
        if b'\x00' in b or b.count(b'\xef\xbf\xbd'):
            raise SystemExit('corruption writing %s - ABORT' % page)
    return n


def main():
    check = '--check' in sys.argv
    a = sys.argv
    quality = int(a[a.index('--quality') + 1]) if '--quality' in a else QUALITY

    made, jb, wb, srcs = build_webp(quality, check)
    print('%s  webp written: %d  (jpeg %.1f MB -> webp %.1f MB for those)'
          % ('CHECK' if check else 'BUILD', made, jb / 1048576.0, wb / 1048576.0))

    pages = ([os.path.basename(f) for f in sorted(glob.glob(os.path.join(ROOT, '*.html')))]
             + ['articles/' + os.path.basename(f)
                for f in sorted(glob.glob(os.path.join(ROOT, 'articles', '*.html')))]
             + ['daily/' + os.path.basename(f)
                for f in sorted(glob.glob(os.path.join(ROOT, 'daily', '*.html')))])
    total, touched = 0, 0
    for pg in pages:
        n = wrap(pg, check)
        if n:
            touched += 1
            total += n
    print('%s  <picture> wrappers: %d across %d pages'
          % ('CHECK' if check else 'APPLIED', total, touched))
    json.dump({'mode': 'check' if check else 'applied', 'quality': quality,
               'webp_files': made, 'wrappers': total, 'pages': touched,
               'jpeg_bytes': jb, 'webp_bytes': wb},
              open(os.path.join(ROOT, '_webp_report.json'), 'w', encoding='utf-8'),
              indent=1)


if __name__ == '__main__':
    main()
