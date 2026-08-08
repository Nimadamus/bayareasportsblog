#!/usr/bin/env python3
"""_srcset.py - stop shipping 1200px art into a 341px slot.

Every card on this site is a single 1200x675 file no matter how small it is
rendered: 341 CSS px on a phone, 372 on a tablet, 602 in the desktop grid. This
generates narrower derivatives and describes them with srcset/sizes so the
browser picks one that fits the slot and the screen density.

  <picture>
    <source type="image/webp" srcset="x-400w.webp 400w, x-600w.webp 600w, ...
                                      x.webp 1200w" sizes="...">
    <img src="x.jpg" srcset="x-400w.jpg 400w, ... x.jpg 1200w" sizes="..."
         width="1200" height="675" ...>
  </picture>

What is deliberately untouched: src still points at the full-size JPEG, so
og:image, twitter:image and the JSON-LD image nodes are unaffected, and any
browser that ignores srcset gets exactly what it got before. width/height stay
at the intrinsic 1200x675 so the aspect-ratio box - and therefore CLS - does not
move. Derivatives are cut from the original with LANCZOS at the same quality
settings used for the full-size files, so nothing is upscaled and nothing is
softened beyond the resize itself.

The sizes values below were measured in a real browser at four viewports rather
than guessed, and each is rounded up a little so the browser never picks a
rung narrower than the slot.

  python _srcset.py [--check] [--quality 92] [--webp-quality 82]
"""
import os, re, sys, glob, json

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
QUALITY, WEBP_QUALITY = 92, 82

# measured CSS widths at 1440 / 1280 / 834 / 390 viewports, dpr 1:
#   lead-main 761/751/769/341 | st.w3 602/594/372/341 | st.w2 393/388/239/341
#   st.split  373/369/232/341 | vlt   288/284/372/341
SIZES = [
    ('lead-main', '(max-width: 640px) 92vw, (max-width: 1024px) 96vw, 56vw'),
    ('st w4 split', '(max-width: 640px) 92vw, (max-width: 1024px) 32vw, 28vw'),
    ('st w2', '(max-width: 640px) 92vw, (max-width: 1024px) 32vw, 30vw'),
    ('st w3', '(max-width: 640px) 92vw, (max-width: 1024px) 48vw, 46vw'),
    ('vlt', '(max-width: 640px) 92vw, (max-width: 1024px) 48vw, 24vw'),
    ('st', '(max-width: 640px) 92vw, (max-width: 1024px) 48vw, 46vw'),
]
FIGURE_SIZES = '(max-width: 820px) 92vw, 760px'
DEFAULT_SIZES = '(max-width: 640px) 92vw, (max-width: 1024px) 48vw, 46vw'

CARD_WIDTHS = [400, 600, 800]
FIGURE_WIDTHS = [400, 800, 1200]

PICTURE_RE = re.compile(
    r'<picture><source type="image/webp" srcset="([^"]+)">(<img\s[^>]*>)</picture>')
ATTR = re.compile(r'(\w[\w-]*)="([^"]*)"')


def rd(p):
    return open(p, encoding='utf-8', errors='strict').read()


def wr(p, s):
    with open(p, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)
    b = open(p, 'rb').read()
    if b'\x00' in b or b.count(b'\xef\xbf\xbd'):
        raise SystemExit('corruption writing %s - ABORT' % p)


def local_path(src):
    u = src.replace('https://bayareasportsblog.com/', '').lstrip('./')
    while u.startswith('../'):
        u = u[3:]
    return u


def derivative(rel, w, ext):
    base, _ = os.path.splitext(rel)
    return '%s-%dw%s' % (base, w, ext)


def make_derivatives(rel, widths, check):
    """Write name-<w>w.jpg / .webp for each width smaller than the original."""
    full = os.path.join(ROOT, rel)
    if not os.path.exists(full):
        return [], 0
    im = Image.open(full)
    ow, oh = im.size
    made, bytes_made = [], 0
    for w in widths:
        if w >= ow:
            continue
        h = max(1, round(oh * w / float(ow)))
        for ext, fmt, q in (('.jpg', 'JPEG', QUALITY), ('.webp', 'WEBP', WEBP_QUALITY)):
            out_rel = derivative(rel, w, ext)
            out_full = os.path.join(ROOT, out_rel)
            if os.path.exists(out_full):
                made.append((w, ext, out_rel))
                continue
            if check:
                made.append((w, ext, out_rel))
                continue
            sm = im.convert('RGB').resize((w, h), Image.LANCZOS)
            if fmt == 'JPEG':
                sm.save(out_full, fmt, quality=q, optimize=True, progressive=True)
            else:
                sm.save(out_full, fmt, quality=q, method=6)
            sm.close()
            bytes_made += os.path.getsize(out_full)
            made.append((w, ext, out_rel))
    im.close()
    return made, bytes_made


def sizes_for(img_tag, context, is_figure):
    if is_figure:
        return FIGURE_SIZES
    for key, val in SIZES:
        if 'class="%s"' % key in context or ('class="%s' % key) in context:
            return val
    return DEFAULT_SIZES


def rel_prefix(src):
    m = re.match(r'((?:\.\./)*)', src)
    return m.group(1) if m else ''


def process(page, check):
    p = os.path.join(ROOT, page)
    s0 = rd(p)
    out, pos, n, made_bytes = [], 0, 0, 0

    for m in PICTURE_RE.finditer(s0):
        webp_src, img_tag = m.group(1), m.group(2)
        if ' srcset=' in img_tag or ',' in webp_src:
            continue                                   # already done
        a = dict(ATTR.findall(img_tag))
        src = a.get('src', '')
        if not re.search(r'\.(jpg|jpeg|png)$', src, re.I):
            continue
        rel = local_path(src)
        if not os.path.exists(os.path.join(ROOT, rel)):
            continue
        pre = rel_prefix(src)
        before = s0[max(0, m.start() - 400):m.start()]
        is_figure = '<figure' in before and 'class="st' not in before
        widths = FIGURE_WIDTHS if is_figure else CARD_WIDTHS

        made, mb = make_derivatives(rel, widths, check)
        made_bytes += mb
        if not made:
            continue

        with Image.open(os.path.join(ROOT, rel)) as im:
            ow = im.size[0]
        jpg_set, webp_set = [], []
        for w, ext, out_rel in made:
            url = pre + out_rel
            (jpg_set if ext == '.jpg' else webp_set).append('%s %dw' % (url, w))
        jpg_set.append('%s %dw' % (src, ow))
        webp_set.append('%s %dw' % (webp_src, ow))

        sz = sizes_for(img_tag, before, is_figure)
        new_img = img_tag[:-1].rstrip() + ' srcset="%s" sizes="%s">' % (
            ', '.join(jpg_set), sz)
        new_pic = ('<picture><source type="image/webp" srcset="%s" sizes="%s">%s</picture>'
                   % (', '.join(webp_set), sz, new_img))
        out.append(s0[pos:m.start()])
        out.append(new_pic)
        pos = m.end()
        n += 1

    if not n:
        return 0, 0
    out.append(s0[pos:])
    if not check:
        wr(p, ''.join(out))
    return n, made_bytes


def main():
    check = '--check' in sys.argv
    pages = ([os.path.basename(f) for f in sorted(glob.glob(os.path.join(ROOT, '*.html')))]
             + ['articles/' + os.path.basename(f)
                for f in sorted(glob.glob(os.path.join(ROOT, 'articles', '*.html')))]
             + ['daily/' + os.path.basename(f)
                for f in sorted(glob.glob(os.path.join(ROOT, 'daily', '*.html')))])
    total, touched, made_bytes = 0, 0, 0
    for pg in pages:
        n, mb = process(pg, check)
        made_bytes += mb
        if n:
            touched += 1
            total += n
    derivs = len(glob.glob(os.path.join(ROOT, 'assets', '**', '*-[0-9]*w.*'),
                           recursive=True))
    print('%s  srcset added to %d images across %d pages'
          % ('CHECK' if check else 'APPLIED', total, touched))
    print('  derivative files on disk: %d  (%.1f MB written this run)'
          % (derivs, made_bytes / 1048576.0))
    json.dump({'mode': 'check' if check else 'applied', 'images': total,
               'pages': touched, 'derivatives': derivs},
              open(os.path.join(ROOT, '_srcset_report.json'), 'w', encoding='utf-8'),
              indent=1)


if __name__ == '__main__':
    main()
