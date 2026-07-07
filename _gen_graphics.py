#!/usr/bin/env python3
"""Generate article-specific editorial SVG graphics (team colors + subject).
Safe: no logos, no player likeness photos, no copyrighted art. Type + team palette only.
"""
import os
OUT = os.path.join(os.path.dirname(__file__), 'assets', 'img')
os.makedirs(OUT, exist_ok=True)

TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" role="img" aria-label="{aria}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{c1}"/>
      <stop offset="60%" stop-color="{c2}"/>
      <stop offset="100%" stop-color="#0b0d11"/>
    </linearGradient>
    <linearGradient id="acc" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{a1}"/>
      <stop offset="1" stop-color="{a2}"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="675" fill="url(#bg)"/>
  <!-- diagonal accent field -->
  <polygon points="760,0 1200,0 1200,675 560,675" fill="{a1}" fill-opacity="0.10"/>
  <!-- motion lines -->
  <g stroke="#ffffff" stroke-opacity="0.06" stroke-width="3">
    <line x1="620" y1="70" x2="1200" y2="70"/>
    <line x1="660" y1="150" x2="1200" y2="150"/>
    <line x1="700" y1="230" x2="1200" y2="230"/>
  </g>
  <!-- big translucent watermark (number or monogram) -->
  <text x="1150" y="560" text-anchor="end" font-family="Arial Black, Arial, sans-serif" font-size="440" font-weight="900" fill="url(#acc)" fill-opacity="0.16">{watermark}</text>
  <!-- accent underline -->
  <rect x="90" y="150" width="86" height="12" rx="6" fill="{a1}"/>
  <!-- team wordmark -->
  <text x="88" y="250" font-family="Arial, sans-serif" font-size="30" font-weight="700" letter-spacing="6" fill="{a2}">{line1}</text>
  <text x="84" y="360" font-family="Arial Black, Arial, sans-serif" font-size="104" font-weight="900" fill="#ffffff" letter-spacing="-2">{line2}</text>
  <!-- subject -->
  <text x="90" y="430" font-family="Arial, sans-serif" font-size="30" fill="#d7dbe3">{sub}</text>
  <!-- footer tag -->
  <text x="90" y="600" font-family="Arial, sans-serif" font-size="22" font-weight="800" letter-spacing="3" fill="{a1}">BAY AREA SPORTS BLOG &#183; {tag}</text>
</svg>
'''

ITEMS = {
 # 49ers scarlet + gold, Aiyuk #11
 'aiyuk':     dict(c1='#3d060b', c2='#7a0d17', a1='#c9302c', a2='#e0b64d', watermark='11',
                   line1='SAN FRANCISCO', line2='49ERS', sub='The Aiyuk spiral after the Super Bowl', tag='49ERS COLUMN',
                   aria='49ers editorial graphic: the Aiyuk spiral'),
 # 49ers generic tile
 'niners':    dict(c1='#3d060b', c2='#7a0d17', a1='#c9302c', a2='#e0b64d', watermark='SF',
                   line1='SAN FRANCISCO', line2='49ERS', sub='Niners analysis and Sunday storylines', tag='49ERS',
                   aria='49ers section graphic'),
 # Warriors royal blue + gold
 'warriors':  dict(c1='#08183a', c2='#1d428a', a1='#2f5bbf', a2='#ffc72c', watermark='GS',
                   line1='GOLDEN STATE', line2='WARRIORS', sub='Out of easy answers', tag='WARRIORS COLUMN',
                   aria='Warriors editorial graphic'),
 # Giants orange + black
 'giants':    dict(c1='#1a0f06', c2='#8a3a12', a1='#fd5a1e', a2='#f2c17a', watermark='SF',
                   line1='SAN FRANCISCO', line2='GIANTS', sub='Oracle Park is still waiting', tag='GIANTS COLUMN',
                   aria='Giants editorial graphic'),
 # Athletics green + gold
 'athletics': dict(c1='#04241b', c2='#0a4130', a1='#0e7a58', a2='#efb21e', watermark="A's",
                   line1='BAY AREA', line2="ATHLETICS", sub='A’s baseball coverage', tag="A'S",
                   aria='Athletics section graphic'),
 # Sharks teal + black
 'sharks':    dict(c1='#03211f', c2='#064a4a', a1='#009aa6', a2='#dfe3e6', watermark='SJ',
                   line1='SAN JOSE', line2='SHARKS', sub='NHL news and analysis', tag='SHARKS',
                   aria='Sharks section graphic'),
 # Betting gold on dark
 'betting':   dict(c1='#141007', c2='#2c2109', a1='#f5a623', a2='#ffd97a', watermark='%',
                   line1='BAY AREA', line2='BETTING', sub='Angles, lines, and value spots', tag='BETTING',
                   aria='Betting section graphic'),
 # Bay Area welcome
 'bayarea':   dict(c1='#141820', c2='#2a1030', a1='#e11d2a', a2='#f5a623', watermark='BA',
                   line1='WELCOME TO', line2='BAY AREA', sub='49ers, Warriors, Giants, A’s, Sharks and more', tag='THE BLOG',
                   aria='Bay Area Sports Blog welcome graphic'),
}

for name, d in ITEMS.items():
    svg = TEMPLATE.format(**d)
    with open(os.path.join(OUT, name + '.svg'), 'w', encoding='utf-8') as f:
        f.write(svg)
    print('wrote', name + '.svg')
