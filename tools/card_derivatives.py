#!/usr/bin/env python3
"""card_derivatives.py - generate the responsive derivatives for article cards.

The article template hard-codes six derivative URLs plus the full-size .webp for every
card:

    slug-400w.jpg  slug-600w.jpg  slug-800w.jpg
    slug-400w.webp slug-600w.webp slug-800w.webp
    slug.webp

_srcset.py will not make them, because it deliberately skips any <img> that already
carries a srcset attribute - and the article template always does. _webp.py rewrites
markup and has double-wrapped <picture> tags in the past, so it is the wrong tool for
this. That left derivative generation as an undocumented manual step that silently 404s
when forgotten. This script is that step, made repeatable and safe to re-run.

Settings match _srcset.py exactly (JPEG q92 progressive, WEBP q82 method 6, LANCZOS) and
_webp.py for the full-size webp (q82 method 6), so output is identical to what the rest
of the site already ships.

  python tools/card_derivatives.py            # fill every gap under assets/img/cards
  python tools/card_derivatives.py --check    # report gaps, write nothing
  python tools/card_derivatives.py <slug> ... # only these slugs

Exits 2 in --check mode if anything is missing, so it can be used as a gate.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDS = os.path.join(ROOT, 'assets', 'img', 'cards')

WIDTHS = [400, 600, 800]
JPEG_QUALITY, WEBP_QUALITY = 92, 82


def targets(slug):
    """Every derivative the article template references, as (path, width, fmt)."""
    out = []
    for w in WIDTHS:
        out.append((os.path.join(CARDS, '%s-%dw.jpg' % (slug, w)), w, 'JPEG'))
        out.append((os.path.join(CARDS, '%s-%dw.webp' % (slug, w)), w, 'WEBP'))
    out.append((os.path.join(CARDS, '%s.webp' % slug), None, 'WEBP'))
    return out


def build(slug, check):
    src = os.path.join(CARDS, slug + '.jpg')
    if not os.path.exists(src):
        return 0, ['%s.jpg missing - no source card' % slug]
    missing, made = [], 0
    todo = [t for t in targets(slug) if not os.path.exists(t[0])]
    if not todo:
        return 0, []
    if check:
        return 0, [os.path.basename(p) for p, _, _ in todo]

    im = Image.open(src)
    ow, oh = im.size
    base = im.convert('RGB')
    im.close()
    for path, w, fmt in todo:
        if w is None or w >= ow:
            sm = base.copy()
        else:
            sm = base.resize((w, max(1, round(oh * w / float(ow)))), Image.LANCZOS)
        if fmt == 'JPEG':
            sm.save(path, fmt, quality=JPEG_QUALITY, optimize=True, progressive=True)
        else:
            sm.save(path, fmt, quality=WEBP_QUALITY, method=6)
        sm.close()          # Windows/PIL: release the handle before anything replaces it
        made += 1
    base.close()
    return made, missing


def main():
    argv = [a for a in sys.argv[1:] if not a.startswith('--')]
    check = '--check' in sys.argv
    slugs = argv or sorted(
        os.path.splitext(f)[0] for f in os.listdir(CARDS)
        if f.endswith('.jpg') and '-400w' not in f and '-600w' not in f
        and '-800w' not in f)

    total, gaps = 0, []
    for slug in slugs:
        made, miss = build(slug, check)
        total += made
        if miss:
            gaps.append((slug, miss))
        if made:
            print('  %-56s +%d' % (slug[:56], made))

    if check:
        for slug, miss in gaps:
            print('  MISSING %-46s %s' % (slug[:46], ', '.join(miss)))
        print('CARD DERIVATIVES  cards=%d  incomplete=%d' % (len(slugs), len(gaps)))
        raise SystemExit(2 if gaps else 0)

    print('CARD DERIVATIVES  cards=%d  files written=%d' % (len(slugs), total))
    if gaps:
        for slug, miss in gaps:
            print('  UNRESOLVED %-43s %s' % (slug[:43], ', '.join(miss)))
        raise SystemExit(2)


if __name__ == '__main__':
    main()
