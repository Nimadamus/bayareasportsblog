import json
import os
import re
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
arts = json.load(open(os.path.join(ROOT, '_inventory.json')))
slugs = {a['slug'] for a in arts}
blob = ' '.join(a['slug'] + ' ' + a['title'].lower() for a in arts)

print('NON RECAP ARTICLES BY SECTION')
by = collections.defaultdict(list)
for a in arts:
    if not a['recap']:
        by[a['section']].append(a)
for sec in ('Warriors', 'Sharks', 'Bay Area', 'Bay Area Sports', 'Cal', 'Stanford', 'Flashbacks'):
    print(' [%s]' % sec)
    for a in sorted(by.get(sec, []), key=lambda x: x['slug']):
        print('   %-62s %5dw in=%-2d %s' % (a['slug'][:62], a['words'], a['in'], a['date']))

print()
print('REFERENCE TOPICS: does anything on the site already cover it?')
probes = {
    'levis stadium guide': ['levi'],
    'chase center guide': ['chase-center', 'chase center'],
    'oracle park guide': ['oracle-park'],
    'sutter health park': ['sutter'],
    'coliseum history': ['coliseum'],
    'candlestick': ['candlestick'],
    'giants schedule hub': ['giants-2026-season-hub', 'giants-2026-schedule'],
    'giants roster depth': ['giants-2026-roster-depth'],
    'giants all time records': ['giants-record', 'giants-all-time', 'giants-franchise-record'],
    'giants world series history': ['world-series'],
    '49ers schedule hub': ['49ers-2026-schedule'],
    '49ers roster depth': ['49ers-roster', '49ers-depth'],
    '49ers super bowl history': ['super-bowl'],
    '49ers all time records': ['49ers-record', '49ers-all-time'],
    'warriors schedule': ['warriors-2026-27-schedule', 'warriors-schedule'],
    'warriors roster depth': ['warriors-roster', 'warriors-2026-27-roster'],
    'warriors championships': ['warriors-champ', 'warriors-title'],
    'warriors records': ['warriors-record', 'warriors-all-time'],
    'sharks schedule': ['sharks-2026-27-schedule', 'sharks-schedule'],
    'sharks roster depth': ['sharks-2026-27-roster', 'sharks-roster'],
    'athletics schedule hub': ['athletics-2026-schedule', 'athletics-2026-season-hub'],
    'athletics roster depth': ['athletics-2026-roster-depth'],
    'athletics vegas timeline': ['oakland-sacramento-las-vegas', 'vegas-timeline'],
    'bay area championships list': ['bay-area-championships'],
    'bay area relocations': ['franchise-relocations'],
    'giants vs dodgers rivalry': ['giants-dodgers', 'dodgers-rivalry'],
    '49ers vs seahawks rivalry': ['seahawks-rivalry', '49ers-seahawks'],
    'warriors vs kings/lakers rivalry': ['warriors-lakers', 'warriors-kings'],
    'bay bridge series': ['bay-bridge'],
    'big game cal stanford': ['big-game'],
    'how to watch / tv channels': ['how-to-watch', 'tv-channel', 'streaming'],
    'ticket / attendance guide': ['tickets', 'attendance'],
    'draft history': ['draft'],
    'payroll / cap': ['payroll', 'cap-sheet', 'luxury-tax'],
    'retired numbers': ['retired-number'],
    'hall of fame': ['hall-of-fame'],
    'mount rushmore / greatest players': ['greatest', 'rushmore', 'best-players'],
    'stadium seating / parking': ['parking', 'seating'],
}
for label, needles in sorted(probes.items()):
    hits = [s for s in slugs if any(n in s for n in needles)]
    mark = 'HAVE' if hits else 'GAP '
    print('  %s %-34s %s' % (mark, label, ', '.join(sorted(hits)[:3])))
