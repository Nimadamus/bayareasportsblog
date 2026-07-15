#!/usr/bin/env python3
"""artgen.py - editorial card art for Bay Area Sports Blog (1200x675).

One visual system, two tiers:
  photo_card(src, ...)  real licensed photo -> focal crop -> team duotone wash -> type overlay
  art_card(...)         no correct-team photo exists -> rich abstract sport art -> type overlay

Both tiers share the same bottom-left type block, scrim and brand rule, so a grid of
mixed cards reads as one designed system instead of a wall of gradients.

Abstract art never depicts a player. Sport geometry + texture + team palette only.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H = 1200, 675
FDIR = "C:/Windows/Fonts/"


def _font(name, size):
    for f in (name, 'arialbd.ttf', 'arial.ttf'):
        p = FDIR + f
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


BLACK = lambda s: _font('ariblk.ttf', s)
BOLD = lambda s: _font('arialbd.ttf', s)
REG = lambda s: _font('arial.ttf', s)

TEAMS = {
    'giants':    dict(deep='#1a0c04', mid='#c4501a', accent='#fd5a1e', light='#ffd9b0',
                      kicker='SAN FRANCISCO GIANTS', mono='SF', sport='baseball'),
    '49ers':     dict(deep='#26060b', mid='#a8141f', accent='#e8746f', light='#efd08a',
                      kicker='SAN FRANCISCO 49ERS', mono='49', sport='football'),
    'warriors':  dict(deep='#050e2b', mid='#2c5cbe', accent='#ffc72c', light='#bcd0ff',
                      kicker='GOLDEN STATE WARRIORS', mono='GS', sport='basketball'),
    'athletics': dict(deep='#032a1f', mid='#0d6a4c', accent='#2fd18d', light='#f0c23a',
                      kicker='ATHLETICS', mono='A', sport='baseball'),
    'sharks':    dict(deep='#012322', mid='#087272', accent='#25d6e4', light='#d7eaea',
                      kicker='SAN JOSE SHARKS', mono='SJ', sport='hockey'),
    'raiders':   dict(deep='#0b0b0c', mid='#4a4f55', accent='#cfd6d9', light='#e8ebec',
                      kicker='LAS VEGAS RAIDERS', mono='LV', sport='football'),
    'bay':       dict(deep='#140a20', mid='#5e1a3c', accent='#e11d2a', light='#f5a623',
                      kicker='BAY AREA SPORTS', mono='BA', sport='bridge'),
}


def hx(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def seed_of(s):
    h = 2166136261
    for ch in str(s):
        h = ((h ^ ord(ch)) * 16777619) & 0xffffffff
    return h


class R:
    """Tiny deterministic PRNG so every card is stable across rebuilds."""

    def __init__(self, s):
        self.s = seed_of(s) or 1

    def n(self):
        self.s = (1103515245 * self.s + 12345) & 0x7fffffff
        return self.s

    def f(self, a=0.0, b=1.0):
        return a + (b - a) * (self.n() / float(0x7fffffff))

    def i(self, a, b):
        return a + self.n() % (b - a + 1)

    def pick(self, seq):
        return seq[self.n() % len(seq)]


# ---------------------------------------------------------------- backgrounds
def _gradient(deep, mid, rng):
    """Layered base wash. Direction and falloff vary by seed."""
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    xn, yn = x / W, y / H
    mode = rng.i(0, 2)
    if mode == 0:                                     # diagonal
        a = rng.f(0.3, 0.8)
        t = xn * a + yn * (1 - a)
    elif mode == 1:                                   # radial from a seeded focus
        cx, cy = rng.f(0.55, 0.95), rng.f(0.1, 0.5)
        t = np.sqrt(((xn - cx) * 1.15) ** 2 + (yn - cy) ** 2) / 1.15
        t = 1.0 - np.clip(t, 0, 1)
    else:                                             # sweeping vertical with skew
        t = yn * 0.75 + xn * 0.25
        t = t ** rng.f(0.7, 1.5)
    t = np.clip(t, 0, 1)[..., None]
    D, M = np.array(hx(deep), np.float32), np.array(hx(mid), np.float32)
    img = D * (1 - t) + M * t
    # gentle corner falloff for depth only; the type block lives in HTML now
    fall = np.clip((yn * 0.7 + (1 - xn) * 0.3 - 0.55) / 0.45, 0, 1)[..., None]
    img = img * (1 - fall * 0.14)
    # lift the floor so cards read at thumbnail size instead of going to mud
    img = img * 0.86 + 26.0
    return img


def _grain(img, rng, amt=7.0):
    n = np.random.default_rng(rng.n()).normal(0, amt, (H, W, 1)).astype(np.float32)
    return np.clip(img + n, 0, 255)


def _vignette(im, strength=0.5):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x / W - .5) * 1.1) ** 2 + ((y / H - .5) * 1.25) ** 2)
    v = np.clip(1 - (d - 0.35) * strength * 2.2, 0.25, 1)[..., None]
    return np.clip(np.asarray(im, np.float32) * v, 0, 255)


# ---------------------------------------------------------------- sport marks
def _baseball(d, rng, ACC, LIGHT):
    """Infield geometry: diamond, foul lines, seam arc."""
    ox, oy = rng.f(0.55, 0.86) * W, rng.f(0.62, 0.95) * H
    scale = rng.f(300, 520)
    # foul lines radiating from the plate
    for ang in (math.radians(45), math.radians(135)):
        d.line([(ox, oy), (ox + math.cos(ang) * 1400, oy - math.sin(ang) * 1400)],
               fill=LIGHT + (86,), width=5)
    # diamond
    pts = [(ox, oy), (ox + scale * .72, oy - scale * .72),
           (ox, oy - scale * 1.44), (ox - scale * .72, oy - scale * .72)]
    d.polygon(pts, fill=ACC + (26,))
    d.line(pts + [pts[0]], fill=ACC + (150,), width=6, joint='curve')
    # outfield arc
    d.arc([ox - scale * 1.6, oy - scale * 3.2, ox + scale * 1.6, oy + scale * 0.1],
          200, 340, fill=LIGHT + (70,), width=5)
    # ball seam, offset
    sx, sy = rng.f(0.08, 0.3) * W, rng.f(0.1, 0.4) * H
    r = rng.f(120, 210)
    for k in (-1, 1):
        d.arc([sx - r, sy - r, sx + r, sy + r], 20 + (0 if k > 0 else 180),
              160 + (0 if k > 0 else 180), fill=ACC + (78,), width=7)


def _football(d, rng, ACC, LIGHT):
    """Yard lines, hash marks, chevrons."""
    base = rng.f(0.3, 0.62) * H
    step = rng.i(74, 104)
    skew = rng.f(-0.28, 0.28)
    for i in range(-1, 18):
        x = i * step + rng.f(-8, 8)
        d.line([(x, base), (x + skew * H, H)], fill=LIGHT + (62,), width=4)
    # hash marks
    for row in (base + (H - base) * 0.34, base + (H - base) * 0.68):
        for i in range(-1, 34):
            x = i * (step / 2.0)
            d.line([(x, row), (x + 18, row)], fill=LIGHT + (86,), width=4)
    # chevrons
    cy = rng.f(0.1, 0.36) * H
    for k in range(rng.i(3, 6)):
        x0 = W - 120 - k * 76
        d.polygon([(x0, cy), (x0 + 54, cy + 62), (x0, cy + 124),
                   (x0 - 18, cy + 124), (x0 + 36, cy + 62), (x0 - 18, cy)],
                  fill=ACC + (76,))


def _basketball(d, rng, ACC, LIGHT):
    """Key, three-point arc, ball ribs."""
    cx, cy = rng.f(0.62, 0.92) * W, rng.f(0.5, 0.9) * H
    kw, kh = rng.f(210, 300), rng.f(320, 430)
    d.rectangle([cx - kw / 2, cy - kh, cx + kw / 2, cy], fill=LIGHT + (16,))
    d.rectangle([cx - kw / 2, cy - kh, cx + kw / 2, cy], outline=LIGHT + (80,), width=5)
    d.arc([cx - kw / 2, cy - kh - kw / 2, cx + kw / 2, cy - kh + kw / 2], 0, 180,
          fill=LIGHT + (80,), width=5)
    r3 = rng.f(430, 600)
    d.arc([cx - r3, cy - r3, cx + r3, cy + r3], 182, 358, fill=ACC + (120,), width=6)
    # ball ribs
    bx, by = rng.f(0.06, 0.26) * W, rng.f(0.12, 0.42) * H
    br = rng.f(140, 220)
    d.ellipse([bx - br, by - br, bx + br, by + br], outline=ACC + (85,), width=6)
    d.line([(bx - br, by), (bx + br, by)], fill=ACC + (72,), width=5)
    d.arc([bx - br * 1.7, by - br, bx + br * .3, by + br], 290, 70, fill=ACC + (66,), width=5)
    d.arc([bx - br * .3, by - br, bx + br * 1.7, by + br], 110, 250, fill=ACC + (66,), width=5)


def _hockey(d, rng, ACC, LIGHT):
    """Faceoff circles, blue lines, goal crease."""
    for k in range(rng.i(2, 3)):
        cx = rng.f(0.45, 0.95) * W
        cy = rng.f(0.35, 0.9) * H
        r = rng.f(120, 210)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACC + (14,))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ACC + (120,), width=6)
        d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=ACC + (150,))
        for sx in (-1, 1):
            for sy in (-1, 1):
                d.line([(cx + sx * r * .45, cy + sy * r * .3),
                        (cx + sx * r * .45, cy + sy * r * .75)], fill=LIGHT + (85,), width=5)
    lx = rng.f(0.1, 0.4) * W
    d.rectangle([lx, 0, lx + 14, H], fill=LIGHT + (54,))
    d.rectangle([lx + 150, 0, lx + 158, H], fill=ACC + (44,))


def _bridge(d, rng, ACC, LIGHT):
    """Suspension cables and towers, the only 'bay' mark."""
    base = rng.f(0.62, 0.82) * H
    d.rectangle([0, base, W, base + 8], fill=LIGHT + (70,))
    towers = [rng.f(0.16, 0.3) * W, rng.f(0.66, 0.84) * W]
    top = rng.f(0.08, 0.2) * H
    for tx in towers:
        d.rectangle([tx - 11, top, tx + 11, base], fill=ACC + (135,))
        d.rectangle([tx - 38, top + 40, tx + 38, top + 54], fill=ACC + (105,))
    # main catenary
    for off in (0, 8):
        pts = []
        for i in range(0, 101):
            t = i / 100.0
            x = towers[0] + (towers[1] - towers[0]) * t
            y = top + off + math.sin(math.pi * t) * (base - top) * 0.62
            pts.append((x, y))
        d.line(pts, fill=LIGHT + (95 if off == 0 else 44,), width=5)
    # verticals
    for i in range(1, 20):
        t = i / 20.0
        x = towers[0] + (towers[1] - towers[0]) * t
        y = top + math.sin(math.pi * t) * (base - top) * 0.62
        d.line([(x, y), (x, base)], fill=LIGHT + (50,), width=2)


SPORT = dict(baseball=_baseball, football=_football, basketball=_basketball,
             hockey=_hockey, bridge=_bridge)


# ---------------------------------------------------------------- texture
def _texture(d, rng, ACC, LIGHT):
    kind = rng.i(0, 3)
    if kind == 0:      # halftone, density falls off across the frame
        step = rng.i(26, 40)
        for gy in range(0, H + step, step):
            for gx in range(0, W + step, step):
                t = gx / float(W)
                r = max(0.0, (t - 0.25)) * step * 0.42
                if r > 0.6:
                    d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=LIGHT + (40,))
    elif kind == 1:    # screen-print diagonal rule
        step = rng.i(16, 26)
        for i in range(-H, W + H, step):
            d.line([(i, 0), (i + H * 0.6, H)], fill=LIGHT + (24,), width=2)
    elif kind == 2:    # scoreboard grid
        cw, ch = rng.i(70, 110), rng.i(46, 72)
        for x in range(0, W, cw):
            d.line([(x, 0), (x, H)], fill=LIGHT + (26,), width=1)
        for y in range(0, H, ch):
            d.line([(0, y), (W, y)], fill=LIGHT + (26,), width=1)
    else:              # contour bands
        for k in range(rng.i(5, 9)):
            cy = rng.f(-0.2, 1.1) * H
            amp = rng.f(20, 70)
            pts = [(x, cy + math.sin(x / rng.f(90, 190) + k) * amp) for x in range(0, W + 20, 20)]
            d.line(pts, fill=ACC + (38,), width=3)


# ---------------------------------------------------------------- type system
def _wrap(d, text, fnt, maxw, limit):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:limit]


def _scrim(im):
    """Bottom-up darkening so the type block always has contrast."""
    y = np.mgrid[0:H, 0:W][0].astype(np.float32) / H
    a = np.clip((y - 0.42) / 0.58, 0, 1) ** 1.35
    a = (a * 0.86)[..., None]
    return np.asarray(im, np.float32) * (1 - a)


def _typeset(base, team, name, sub, rng):
    cfg = TEAMS.get(team, TEAMS['bay'])
    ACC, LIGHT = hx(cfg['accent']), hx(cfg['light'])
    im = Image.fromarray(_scrim(base).astype(np.uint8))
    d = ImageDraw.Draw(im, 'RGBA')

    LX, MAXW = 64, W * 0.72
    # measure from the bottom up so long names never collide with the sub
    sf = REG(27)
    subs = _wrap(d, sub, sf, MAXW, 2) if sub else []
    nsz = 78
    nf = BLACK(nsz)
    lines = _wrap(d, name.upper(), nf, MAXW, 3)
    while len(lines) > 2 and nsz > 52:          # shrink rather than spill to 3 lines
        nsz -= 6
        nf = BLACK(nsz)
        lines = _wrap(d, name.upper(), nf, MAXW, 3)
    lh = int(nsz * 1.04)

    bottom = H - 42
    sub_h = len(subs) * 34
    name_h = len(lines) * lh
    y = bottom - sub_h - (10 if subs else 0) - name_h

    # kicker pill
    kf = BOLD(21)
    kt = cfg['kicker']
    kw = d.textlength(kt, font=kf)
    ky = y - 52
    d.rounded_rectangle([LX, ky, LX + kw + 26, ky + 34], 17, fill=ACC + (235,))
    d.text((LX + 13, ky + 7), kt, font=kf, fill=(255, 255, 255))

    for ln in lines:
        d.text((LX, y), ln, font=nf, fill=(255, 255, 255))
        y += lh
    if subs:
        y += 10
        for ln in subs:
            d.text((LX + 2, y), ln, font=sf, fill=LIGHT + (232,))
            y += 34

    # top rule + brand
    d.rectangle([0, 0, W, 5], fill=ACC + (200,))
    bf = BOLD(19)
    d.text((LX, 26), "BAY AREA SPORTS BLOG", font=bf, fill=(255, 255, 255, 150))
    return im


# ---------------------------------------------------------------- public API
def art_card(team, name, sub, out, seed=None, type_on=False):
    """Abstract editorial art. Never depicts a person.

    type_on=False (default) renders art only: the page's own HTML headline does the
    talking, so a grid of cards never double-titles itself. type_on=True bakes the
    type in, for standalone/social renditions.
    """
    cfg = TEAMS.get(team, TEAMS['bay'])
    rng = R(seed if seed is not None else name + sub)
    ACC, LIGHT = hx(cfg['accent']), hx(cfg['light'])

    base = _gradient(cfg['deep'], cfg['mid'], rng)
    base = _grain(base, rng, rng.f(4, 9))
    im = Image.fromarray(base.astype(np.uint8))

    # art layers drawn on their own RGBA plane, then softened slightly
    plane = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(plane, 'RGBA')
    _texture(d, rng, ACC, LIGHT)
    SPORT[cfg['sport']](d, rng, ACC, LIGHT)
    plane = plane.filter(ImageFilter.GaussianBlur(0.4))
    im = Image.alpha_composite(im.convert('RGBA'), plane).convert('RGB')

    # oversized ghost monogram, seeded corner + rotation
    msz = rng.i(340, 470)
    mf = BLACK(msz)
    gl = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gl)
    gd.text((0, 0), cfg['mono'], font=mf, fill=LIGHT + (rng.i(34, 54),))
    gl = gl.rotate(rng.f(-9, 9), resample=Image.BICUBIC, expand=False)
    bb = gl.getbbox()
    if bb:
        gl = gl.crop(bb)
        px = W - gl.width + rng.i(10, 90)
        py = rng.pick([-int(gl.height * 0.14), H - int(gl.height * 0.86)])
        im.paste(gl, (px, py), gl)

    # seeded sweep band keeps same-team cards structurally distinct
    sw = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sw)
    off, wid, skew = rng.i(-100, W), rng.i(150, 300), rng.i(-140, 140)
    sd.polygon([(off, 0), (off + wid, 0), (off + wid + skew, H), (off + skew, H)],
               fill=(255, 255, 255, 12))
    sd.line([(off, 0), (off + skew, H)], fill=ACC + (70,), width=4)
    im = Image.alpha_composite(im.convert('RGBA'), sw).convert('RGB')

    arr = _vignette(im, 0.20)
    im = (_typeset(arr, team, name, sub, rng) if type_on
          else Image.fromarray(arr.astype(np.uint8)))
    im.save(out, 'JPEG', quality=92)
    return out


def photo_card(src, team, name, sub, out, seed=None, type_on=False):
    """Real photo -> focal crop -> team duotone wash. See art_card for type_on."""
    from focal_crop import crop_card
    cfg = TEAMS.get(team, TEAMS['bay'])
    rng = R(seed if seed is not None else src)
    tmp = out + '.crop.jpg'
    crop_card(src, tmp, W, H)
    ph = Image.open(tmp).convert('RGB')
    os.remove(tmp)

    a = np.asarray(ph, np.float32)
    lum = (a[..., 0] * .299 + a[..., 1] * .587 + a[..., 2] * .114) / 255.0
    lum = np.clip((lum - 0.06) / 0.88, 0, 1)
    lum = (lum ** 0.92)[..., None]

    SHAD = np.array(hx(cfg['deep']), np.float32)
    MID = np.array(hx(cfg['mid']), np.float32)
    HIGH = np.array(hx(cfg['light']), np.float32)
    # three-stop duotone: shadow -> team mid -> team light
    t = lum
    lo = SHAD + (MID - SHAD) * np.clip(t / 0.55, 0, 1)
    hi = MID + (HIGH - MID) * np.clip((t - 0.55) / 0.45, 0, 1)
    duo = np.where(t < 0.55, lo, hi)
    # retain a little real colour so faces stay human
    duo = duo * 0.80 + a * 0.20
    im = Image.fromarray(np.clip(duo, 0, 255).astype(np.uint8))

    # accent light-leak so photo cards carry the same energy as the art cards
    leak = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(leak)
    off = rng.i(int(W * .45), int(W * .8))
    ld.polygon([(off, 0), (off + 190, 0), (off + 60, H), (off - 130, H)],
               fill=hx(cfg['accent']) + (26,))
    im = Image.alpha_composite(im.convert('RGBA'),
                               leak.filter(ImageFilter.GaussianBlur(28))).convert('RGB')

    arr = _vignette(im, 0.42)
    im = (_typeset(arr, team, name, sub, rng) if type_on
          else Image.fromarray(arr.astype(np.uint8)))
    im.save(out, 'JPEG', quality=92)
    return out


if __name__ == '__main__':
    import sys
    art_card(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    print('wrote', sys.argv[4])
