#!/usr/bin/env python3
"""photo_cards.py - rebuild every article card as a clean real photo (1200x675):
no baked text, no tint, the subject centred so the 4:3 and 3:4 listing crops
(object-fit: cover, centred) keep the face in the middle.

Source per article comes from tools/photo_pick.json (photo_pick.py + commons_fetch.py).
Card file name is the article's og:image card name. Derivatives are deleted and rebuilt
with card_derivatives.py.

  python tools/photo_cards.py            # all articles
  python tools/photo_cards.py <slug> ... # only these
"""
import os, re, sys, glob, json, subprocess
import cv2, numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, os.path.expanduser('~/tools/image_gate'))
import image_gate as GATE   # every card must pass the universal gate before it is kept
W, H = 1200, 675
T = W / float(H)
YUNET = os.path.join(ROOT, 'tools', 'models', 'yunet.onnx')   # OpenCV Zoo face detector
FOCUS = os.path.join(ROOT, 'tools', 'photo_focus.json')        # manual {src: [x, y, size]} fractions


def faces(im):
    """Faces as (x, y, w, h), strongest subject first: score x size, small faces ignored."""
    iw, ih = im.size
    s = min(1.0, 1280.0 / max(iw, ih))
    sm = im.resize((max(1, int(iw * s)), max(1, int(ih * s))))
    bgr = cv2.cvtColor(np.array(sm), cv2.COLOR_RGB2BGR)
    det = cv2.FaceDetectorYN.create(YUNET, '', (bgr.shape[1], bgr.shape[0]), 0.75, 0.3, 5000)
    _, res = det.detect(bgr)
    out = []
    for r in (res if res is not None else []):
        x, y, w, h, score = r[0] / s, r[1] / s, r[2] / s, r[3] / s, r[14]
        if w < min(iw, ih) * 0.035: continue
        out.append((x, y, w, h, score * w * h))
    out.sort(key=lambda f: -f[4])
    return [f[:4] for f in out]


def render(src, dst, mult=3.2):
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    iw, ih = im.size
    focus = json.load(open(FOCUS)) if os.path.exists(FOCUS) else {}
    if src in focus:
        fx, fy, fsz = focus[src]
        fs = [(fx * iw - fsz * iw / 2, fy * ih - fsz * iw / 2, fsz * iw, fsz * iw)]
    else:
        fs = faces(im)
    # largest box of card ratio that fits
    if iw / float(ih) > T: ch = ih; cw = ch * T
    else: cw = iw; ch = cw / T
    if fs:
        fx, fy, fw, fh = fs[0]
        cx, cy = fx + fw / 2.0, fy + fh / 2.0
        # shrink the box until the face can sit dead centre horizontally,
        # but never tighter than head and shoulders or below 640 px wide
        half = min(cx, iw - cx)
        minw = max(680.0, fh * mult * T)
        if cw / 2.0 > half:
            cw = max(min(cw, 2 * half), min(cw, minw)); ch = cw / T
        left = cx - cw / 2.0
        top = min(cy - ch * 0.40, fy - 0.8 * fh)   # face above the middle, full head room
        mode = 'face'
        # still cannot centre (face near an edge of a tight photo): extend the frame
        # sideways with a soft blurred continuation of the photo, so the subject sits
        # in the middle without cropping into the head
        need = int(max(0, -left, left + cw - iw)) + 2
        if need > 2 and abs((cx - max(0, min(left, iw - cw))) / cw - 0.5) > 0.06:
            cv = Image.new('RGB', (iw + 2 * need, ih))
            bg = im.resize((iw + 2 * need, int(ih * (iw + 2 * need) / iw)), Image.BILINEAR)
            bg = bg.crop((0, (bg.size[1] - ih) // 2, bg.size[0], (bg.size[1] - ih) // 2 + ih))
            bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(40))).enhance(0.55)
            cv.paste(bg, (0, 0))
            mask = Image.new('L', (iw, ih), 255)
            md = ImageDraw.Draw(mask); feather = max(8, iw // 40)
            for i in range(feather):
                a = int(255 * i / feather)
                md.line([(i, 0), (i, ih)], fill=a); md.line([(iw - 1 - i, 0), (iw - 1 - i, ih)], fill=a)
            cv.paste(im, (need, 0), mask)
            im = cv; iw = cv.size[0]; cx += need; left += need
            mode = 'face+ext'
    else:
        left = (iw - cw) / 2.0
        top = (ih - ch) * (0.12 if ih > iw * 0.9 else 0.40)
        mode = 'centre'
    left = max(0, min(left, iw - cw)); top = max(0, min(top, ih - ch))
    box = (int(left), int(top), int(left + cw), int(top + ch))
    card = im.crop(box).resize((W, H), Image.LANCZOS)
    card = ImageEnhance.Sharpness(card).enhance(1.05)
    card.save(dst, 'JPEG', quality=90, optimize=True, progressive=True)
    off = None
    if fs:
        off = ((cx - box[0]) / (box[2] - box[0]) - 0.5)
    return mode, (box[2] - box[0]), off


def card_name(path):
    t = open(path, encoding='utf-8').read()
    m = re.search(r'og:image" content="https://bayareasportsblog\.com/assets/img/cards/(.*?)\.jpg"', t)
    return m.group(1) if m else os.path.basename(path)[:-5]


def main():
    pick = json.load(open('tools/photo_pick.json'))
    only = set(sys.argv[1:])
    done, report = [], []
    for slug, src in sorted(pick.items()):
        if only and slug not in only: continue
        if not src or not os.path.exists(src):
            report.append((slug, 'NO SOURCE', 0, None)); continue
        card = card_name('articles/%s.html' % slug)
        dst = 'assets/img/cards/%s.jpg' % card
        for mult in (3.2, 4.2, 5.5, 8.0, 14.0):
            mode, cw, off = render(src, dst, mult)
            g = GATE.check(dst, 'card')
            if g['ok']: break
        if not g['ok']:
            mode = 'GATE FAIL: ' + '; '.join(g['why'])
        for d in glob.glob('assets/img/cards/%s-[468]00w.*' % card) + ['assets/img/cards/%s.webp' % card]:
            if os.path.exists(d): os.remove(d)
        done.append(card)
        report.append((slug, mode, cw, off))
    for s, m, cw, off in report:
        flag = ''
        if m == 'NO SOURCE' or m.startswith('GATE'): flag = '  <-- FIX'
        elif cw < 700: flag = '  <-- low res'
        elif off is not None and abs(off) > 0.12: flag = '  <-- off centre %.2f' % off
        if flag or only: print('%-70s %-6s %4d%s' % (s[:70], m, cw, flag))
    print('cards rebuilt', len(done))
    for i in range(0, len(done), 60):
        subprocess.check_call([sys.executable, 'tools/card_derivatives.py'] + done[i:i + 60], stdout=subprocess.DEVNULL)


if __name__ == '__main__':
    main()
