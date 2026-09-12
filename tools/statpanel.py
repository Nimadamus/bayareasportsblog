#!/usr/bin/env python3
"""statpanel.py - in-body editorial stat art (1200x675) for a column.

Same visual system as artgen cards (team gradient, grain, sport geometry, ghost
monogram, brand rule) but the type block is a stat, not a headline: one oversized
hero numeral, a label, and up to four supporting figures across the bottom.

  python tools/statpanel.py giants "36" "HOME RUNS" "RAFAEL DEVERS, 2026" \
      "8TH IN MLB|.862 OPS|96 RBI|.258 AVG" assets/img/players/out.jpg
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import artgen as A
from artgen import W, H, hx, R, BLACK, BOLD, _font

REG = lambda s: _font('arial.ttf', s)


def panel(team, hero, label, kicker, figures, out, seed=None):
    cfg = A.TEAMS.get(team, A.TEAMS['bay'])
    rng = R(seed if seed is not None else hero + label + kicker)
    ACC, LIGHT = hx(cfg['accent']), hx(cfg['light'])

    base = A._gradient(cfg['deep'], cfg['mid'], rng)
    base = A._grain(base, rng, rng.f(4, 8))
    im = Image.fromarray(base.astype(np.uint8))

    plane = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(plane, 'RGBA')
    A._texture(d, rng, ACC, LIGHT)
    A.SPORT[cfg['sport']](d, rng, ACC, LIGHT)
    plane = plane.filter(ImageFilter.GaussianBlur(0.5))
    im = Image.alpha_composite(im.convert('RGBA'), plane).convert('RGB')
    im = Image.fromarray(A._vignette(im, 0.45).astype(np.uint8))

    # ghost monogram, always opposite the hero numeral
    mono = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    md = ImageDraw.Draw(mono, 'RGBA')
    mf = BLACK(430)
    md.text((W - 70, -40), cfg['mono'], font=mf, fill=LIGHT + (26,), anchor='ra')
    im = Image.alpha_composite(im.convert('RGBA'), mono).convert('RGB')

    # readability scrim under the type, left to right
    sc = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sc, 'RGBA')
    for i in range(W):
        a = int(150 * max(0.0, 1.0 - (i / (W * 0.82)) ** 1.6))
        sd.line([(i, 0), (i, H)], fill=(6, 8, 10, a))
    sd.rectangle([0, H - 190, W, H], fill=(6, 8, 10, 120))
    im = Image.alpha_composite(im.convert('RGBA'), sc).convert('RGB')

    d = ImageDraw.Draw(im, 'RGBA')

    # kicker
    kf = BOLD(24)
    d.text((72, 74), kicker.upper(), font=kf, fill=ACC + (255,))
    d.line([(72, 116), (72 + d.textlength(kicker.upper(), font=kf), 116)],
           fill=ACC + (150,), width=3)

    # hero numeral, scaled so long strings still fit the left half
    size = 300 if len(hero) <= 2 else 230 if len(hero) <= 5 else 170
    hf = BLACK(size)
    while d.textlength(hero, font=hf) > W * 0.62 and size > 90:
        size -= 10
        hf = BLACK(size)
    hy = 138
    lf = BOLD(44)
    # shrink until the hero plus its label clear the bottom figure strip
    while d.textbbox((70, hy), hero, font=hf)[3] + 18 + 48 > H - 178 and size > 90:
        size -= 10
        hf = BLACK(size)
    d.text((74, hy + 6), hero, font=hf, fill=(0, 0, 0, 110))      # drop
    d.text((70, hy), hero, font=hf, fill=(255, 255, 255, 255))
    bb = d.textbbox((70, hy), hero, font=hf)
    d.text((76, bb[3] + 18), label.upper(), font=lf, fill=LIGHT + (245,))

    # supporting figures across the bottom
    figs = [f.strip() for f in figures.split('|') if f.strip()]
    if figs:
        d.line([(72, H - 150), (W - 72, H - 150)], fill=LIGHT + (60,), width=2)
        colw = (W - 144) / len(figs)
        for i, f in enumerate(figs):
            x = 72 + colw * i
            if ' ' in f:
                big, small = f.split(' ', 1)
            else:
                big, small = f, ''
            bf, sf = BLACK(48), BOLD(20)
            d.text((x, H - 128), big, font=bf, fill=ACC + (255,))
            if small:
                d.text((x, H - 66), small.upper(), font=sf, fill=(232, 236, 240, 215))

    # brand rule
    d.rectangle([0, H - 8, W, H], fill=ACC + (230,))
    d.text((W - 72, 74), 'BAY AREA SPORTS BLOG', font=BOLD(19),
           fill=(232, 236, 240, 170), anchor='ra')

    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, quality=92, optimize=True, progressive=True)
    im.save(os.path.splitext(out)[0] + '.webp', quality=82, method=6)
    print('wrote', out)


if __name__ == '__main__':
    team, hero, label, kicker, figures, out = sys.argv[1:7]
    panel(team, hero, label, kicker, figures, out)
