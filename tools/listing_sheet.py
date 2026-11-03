#!/usr/bin/env python3
"""listing_sheet.py out_prefix - render every article card as the listing shows it
(4:3 centre crop of the 16:9 card) into numbered contact sheets for review."""
import os, sys, json, re, glob
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
pick = json.load(open('tools/photo_pick.json'))
slugs = sorted(pick)
if len(sys.argv) > 2: slugs = [s for s in slugs if s in set(sys.argv[2:])]
TW, TH, COLS, PER = 200, 150, 8, 96
f = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 11)
idx = {}
for n in range(0, len(slugs), PER):
    chunk = slugs[n:n + PER]
    rows = (len(chunk) + COLS - 1) // COLS
    sh = Image.new('RGB', (COLS * TW, rows * (TH + 16)), (20, 20, 20))
    d = ImageDraw.Draw(sh)
    for i, s in enumerate(chunk):
        t = open('articles/%s.html' % s, encoding='utf-8').read()
        m = re.search(r'cards/(.*?)\.jpg"', t)
        im = Image.open('assets/img/cards/%s.jpg' % (m.group(1) if m else s)).convert('RGB')
        w, h = im.size; cw = int(h * 4 / 3); im = im.crop(((w - cw) // 2, 0, (w - cw) // 2 + cw, h)).resize((TW, TH))
        x, y = (i % COLS) * TW, (i // COLS) * (TH + 16)
        sh.paste(im, (x, y)); d.line([(x + TW // 2, y), (x + TW // 2, y + 6)], fill=(255, 0, 0))
        k = n + i; idx[k] = s
        d.text((x + 2, y + TH + 1), '%d %s' % (k, s[:28]), fill=(230, 230, 230), font=f)
    sh.save('%s_%d.jpg' % (sys.argv[1], n // PER), quality=80)
json.dump(idx, open(sys.argv[1] + '_idx.json', 'w'), indent=0)
print('sheets', (len(slugs) + PER - 1) // PER)
