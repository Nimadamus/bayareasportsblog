#!/usr/bin/env python3
"""card_alts.py - rewrite every card image alt (listings, article hero, og:image:alt,
twitter:image:alt) to describe the real photo now on the card, not the old graphic."""
import os, re, json, glob, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
pick = json.load(open('tools/photo_pick.json'))
man = json.load(open('tools/cards_manifest.json'))
man_alt = {v['src']: v['alt'] for v in man.values() if v.get('mode') == 'photo' and v.get('src') and v.get('alt')}
TEAMS = {'giants': 'San Francisco Giants', '49ers': 'San Francisco 49ers', 'athletics': 'Athletics', 'warriors': 'Golden State Warriors',
         'sharks': 'San Jose Sharks', 'raiders': 'Raiders', 'stanford': 'Stanford', 'cal': 'Cal'}
credit = {}
for line in open('assets/img/players/CREDITS.txt', encoding='utf-8', errors='ignore'):
    m = re.match(r'^([a-z0-9\-]+): (.+?)\.(?:jpe?g|JPE?G|png), photo by', line)
    if m: credit[m.group(1)] = m.group(2)


def clean(t):
    t = re.sub(r'\([^)]*\)', '', t).replace('_', ' ')
    t = re.sub(r'\b\d{6,}\b|\b(?:IMG|DSC)\w*', '', t)
    t = re.sub(r'\s+', ' ', t).strip(' -,')
    return t


def describe(src):
    stem = os.path.splitext(os.path.basename(src))[0]
    for k in (stem, stem.replace('commons-', '').replace('div-', '')):
        if k in credit: return clean(credit[k])
    if stem.startswith(('commons-', 'div-')) and stem.split('-', 1)[1] in credit:
        return clean(credit[stem.split('-', 1)[1]])
    if src in man_alt: return man_alt[src]
    w = [x for x in stem.split('-') if x not in ('real',) and not x.isdigit()]
    team = next((TEAMS[x] for x in w if x in TEAMS), '')
    name = ' '.join(x.capitalize() for x in w if x not in TEAMS)
    return '%s, %s' % (name, team) if team and name else (name or team)


def card_of(art):
    m = re.search(r'og:image" content="https://bayareasportsblog\.com/assets/img/cards/(.*?)\.jpg"', open(art, encoding='utf-8').read())
    return m.group(1) if m else None


alts = {}
for slug, src in pick.items():
    c = card_of('articles/%s.html' % slug)
    if c and src: alts[c] = html.escape(describe(src), quote=True)
json.dump(alts, open('tools/card_alts.json', 'w'), indent=1)

IMGTAG = re.compile(r'<img\b[^>]*?src="[^"]*?assets/img/cards/([a-z0-9\-]+?)(?:-\d+w)?\.(?:jpg|webp)"[^>]*>')
changed = 0
for f in glob.glob('*.html') + glob.glob('articles/*.html'):
    t = open(f, encoding='utf-8', newline='').read(); o = t
    def fix(m):
        c = m.group(1); tag = m.group(0)
        if c not in alts: return tag
        return re.sub(r'\salt="[^"]*"', ' alt="%s"' % alts[c], tag, count=1)
    t = IMGTAG.sub(fix, t)
    if f.startswith('articles'):
        c = card_of(f)
        if c in alts:
            t = re.sub(r'(<meta (?:property="og:image:alt"|name="twitter:image:alt") content=")[^"]*(")', lambda m: m.group(1) + alts[c] + m.group(2), t)
    if t != o:
        open(f, 'w', encoding='utf-8', newline='').write(t); changed += 1
print('alts', len(alts), 'files changed', changed)
