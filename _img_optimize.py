#!/usr/bin/env python3
"""_img_optimize.py - shrink the images the site actually serves.

Only files referenced from HTML are touched. Filenames, paths and extensions
never change, so og:image, JSON-LD image nodes, alt text, the card grid and the
thumbnail gate all keep working exactly as they did.

What it does, per image:
  - downscales so the long edge is at most MAX_EDGE (article figures render at
    760 CSS px, cards at 1200, so this still leaves 2x headroom)
  - re-encodes JPEG at QUALITY, progressive, EXIF stripped
  - keeps the original if the "optimised" file is not meaningfully smaller

Card images keep their exact 1200x675 geometry - the thumbnail gate enforces
that ratio - so for cards this is a re-encode only, never a resize.

  python _img_optimize.py [--check] [--quality 85] [--max-edge 1800]
"""
import os, re, sys, glob, json

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
MAX_EDGE = 1800
QUALITY = 85
MIN_GAIN = 0.05           # keep the original unless we save at least 5%
CARD_DIR = 'assets/img/cards/'

REF_RE = re.compile(r'(?:src|href|content)="([^"]+\.(?:jpg|jpeg|png))"', re.I)


def referenced():
    out = set()
    for f in (glob.glob(os.path.join(ROOT, '*.html'))
              + glob.glob(os.path.join(ROOT, 'articles', '*.html'))
              + glob.glob(os.path.join(ROOT, 'daily', '*.html'))):
        s = open(f, encoding='utf-8', errors='replace').read()
        for m in REF_RE.finditer(s):
            u = m.group(1).replace('https://bayareasportsblog.com/', '').lstrip('./')
            while u.startswith('../'):
                u = u[3:]
            if os.path.exists(os.path.join(ROOT, u)):
                out.add(u.replace('\\', '/'))
    return sorted(out)


def optimise(rel, quality, max_edge, check):
    full = os.path.join(ROOT, rel)
    before = os.path.getsize(full)
    im = Image.open(full)
    w, h = im.size
    fmt = im.format
    is_card = rel.startswith(CARD_DIR)

    # Cards are already 1200x675 at high quality: re-encoding them buys about a
    # megabyte across the whole site and would perturb the perceptual hashes the
    # thumbnail gate uses to catch duplicate art. Not worth it.
    if is_card:
        return before, before, im.size, im.size, False

    im2 = im
    if max(w, h) > max_edge:
        scale = max_edge / float(max(w, h))
        im2 = im.convert('RGB').resize((max(1, round(w * scale)),
                                        max(1, round(h * scale))),
                                       Image.LANCZOS)
    elif fmt == 'JPEG':
        im2 = im.convert('RGB')

    tmp = full + '.opt'
    if fmt == 'PNG' and im.mode in ('RGBA', 'LA', 'P'):
        im2.save(tmp, 'PNG', optimize=True)
    else:
        im2.convert('RGB').save(tmp, 'JPEG', quality=quality, optimize=True,
                                progressive=True)
    after = os.path.getsize(tmp)
    dims_before, dims_after = im.size, im2.size
    # Windows will not let os.replace() overwrite a file PIL still has open
    im2.close()
    im.close()

    if after >= before * (1 - MIN_GAIN):
        os.remove(tmp)
        return before, before, dims_before, dims_before, False

    if check:
        os.remove(tmp)
        return before, after, dims_before, dims_after, True

    os.replace(tmp, full)
    chk = Image.open(full)
    chk.load()                      # a truncated write raises here
    if open(full, 'rb').read(2) not in (b'\xff\xd8', b'\x89P'):
        raise SystemExit('bad image header after write: %s - ABORT' % rel)
    return before, after, dims_before, dims_after, True


def main():
    check = '--check' in sys.argv
    a = sys.argv
    quality = int(a[a.index('--quality') + 1]) if '--quality' in a else QUALITY
    max_edge = int(a[a.index('--max-edge') + 1]) if '--max-edge' in a else MAX_EDGE

    files = referenced()
    tot_b = tot_a = 0
    changed, rows = 0, []
    for rel in files:
        try:
            b, af, d0, d1, did = optimise(rel, quality, max_edge, check)
        except Exception as e:
            print('  SKIP %s (%s)' % (rel, e))
            continue
        tot_b += b
        tot_a += af
        if did:
            changed += 1
            rows.append({'file': rel, 'before': b, 'after': af,
                         'dims_before': list(d0), 'dims_after': list(d1)})

    rows.sort(key=lambda r: r['before'] - r['after'], reverse=True)
    json.dump({'mode': 'check' if check else 'applied', 'quality': quality,
               'max_edge': max_edge, 'files_scanned': len(files),
               'files_changed': changed,
               'bytes_before': tot_b, 'bytes_after': tot_a, 'changes': rows},
              open(os.path.join(ROOT, '_img_optimize_report.json'), 'w',
                   encoding='utf-8'), indent=1)

    print('%s  %d/%d files  %.1f MB -> %.1f MB  (-%.1f%%)'
          % ('CHECK' if check else 'APPLIED', changed, len(files),
             tot_b / 1048576.0, tot_a / 1048576.0,
             100.0 * (tot_b - tot_a) / tot_b if tot_b else 0))
    for r in rows[:10]:
        print('  %7.0f -> %6.0f KB  %-11s %s'
              % (r['before'] / 1024, r['after'] / 1024,
                 '%dx%d' % tuple(r['dims_after']), r['file']))


if __name__ == '__main__':
    main()
