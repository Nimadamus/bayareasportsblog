#!/usr/bin/env python3
"""_schema_normalize.py - finish the article schema.

Three gaps the audit found, all invisible to readers:

1. articleSection was empty on 102 of 103 articles. The visible tag on the page carries
   the section ("Giants Column", "Bay Area Villains", "49ers Panic Meter"), but it never
   made it into the JSON-LD, so nothing downstream can cluster by topic.
2. mainEntityOfPage was missing on 84 articles - present only on the ones built from the
   newer template.
3. The type was split 85 NewsArticle / 18 Article for no reason anyone can point at.

Point 3 is now a DECLARED choice rather than a blanket rule. schema_types.json holds the
pages whose type is deliberate: an evergreen reference page is an Article, a recap or a
reported piece is a NewsArticle. Anything not listed gets the default. This script
enforces the declaration in both directions, so a page cannot drift back by accident and
a stray Article cannot creep in unlisted.

The VISIBLE tags are deliberately left alone. "Giants October Watch", "Bay Area
Villains" and "49ers Panic Meter" are editorial section names, not sloppiness, and
flattening them would rewrite the site's voice to tidy a schema field. Instead the tag
is MAPPED to a canonical section for the schema only.

  python _schema_normalize.py [--check]
"""
import os, re, sys, glob, json, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://bayareasportsblog.com/"

# page level schema type, see schema_types.json
_types_path = os.path.join(ROOT, 'schema_types.json')
if os.path.exists(_types_path):
    _decl = json.load(open(_types_path, encoding='utf-8'))
    DEFAULT_TYPE = _decl.get('_default', 'NewsArticle')
    DECLARED_TYPES = _decl.get('types', {})
else:
    DEFAULT_TYPE, DECLARED_TYPES = 'NewsArticle', {}


def schema_type_for(slug):
    """The type this page is supposed to carry."""
    return DECLARED_TYPES.get(slug, DEFAULT_TYPE)

# visible tag (entities stripped, punctuation normalised) -> canonical schema section
SECTION_RULES = [
    ('49ers', '49ers'), ('niners', '49ers'), ('raiders', 'NFL'),
    ('giants', 'Giants'), ("a's", 'Athletics'), ('athletics', 'Athletics'),
    ('warriors', 'Warriors'), ('sharks', 'Sharks'),
    ('flashback', 'Flashbacks'), ('history', 'History'),
    ('dynast', 'Dynasties'), ('villain', 'Bay Area'), ('bay area', 'Bay Area'),
    ('all-star', 'Bay Area'), ('betting', 'Betting'),
]
SLUG_RULES = [
    ('49ers-', '49ers'), ('giants-', 'Giants'), ('athletics-', 'Athletics'),
    ('warriors-', 'Warriors'), ('sharks-', 'Sharks'),
    ('flashback-', 'Flashbacks'), ('raiders-', 'NFL'), ('nfl-', 'NFL'),
    ('lebron-', 'Warriors'), ('montana-', '49ers'), ('brandon-aiyuk', '49ers'),
    ('jerry-rice', '49ers'), ('barry-bonds', 'Giants'), ('jeff-kent', 'Giants'),
    ('bruce-bochy', 'Giants'), ('bryce-eldridge', 'Giants'),
    ('tony-vitello', 'Giants'), ('bay-area', 'Bay Area'), ('welcome-', 'Bay Area'),
]

LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
TAG_RE = re.compile(r'<span class="tag">(.*?)</span>', re.S)


def rd(p):
    return open(os.path.join(ROOT, p), encoding='utf-8', errors='strict').read()


def wr(p, s):
    full = os.path.join(ROOT, p)
    with open(full, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)
    b = open(full, 'rb').read()
    if b'\x00' in b or b.count(b'\xef\xbf\xbd'):
        raise SystemExit('corruption writing %s - ABORT' % p)


def section_for(tag, slug):
    t = re.sub(r'<[^>]+>', '', tag or '')
    t = (t.replace('&middot;', ' ').replace('&#39;', "'").replace('&amp;', '&')).lower()
    for needle, sec in SECTION_RULES:
        if needle in t:
            return sec
    for prefix, sec in SLUG_RULES:
        if slug.startswith(prefix):
            return sec
    return None


def main():
    check = '--check' in sys.argv
    stats = collections.Counter()
    sections = collections.Counter()
    unresolved = []

    for f in sorted(glob.glob(os.path.join(ROOT, 'articles', '*.html'))):
        rel = 'articles/' + os.path.basename(f)
        slug = os.path.basename(f)[:-5]
        s = rd(rel)
        tm = TAG_RE.search(s)
        sec = section_for(tm.group(1) if tm else '', slug)
        if not sec:
            unresolved.append(slug)

        out = s
        changed = False
        for block in LD_RE.findall(s):
            try:
                node = json.loads(block)
            except Exception:
                continue
            if node.get('@type') not in ('Article', 'NewsArticle'):
                continue
            before = json.dumps(node, sort_keys=True)
            want = schema_type_for(slug)
            if node['@type'] != want:
                node['@type'] = want
                stats['type_set_' + want] += 1
            url = BASE + rel
            if 'mainEntityOfPage' not in node:
                node['mainEntityOfPage'] = {'@type': 'WebPage', '@id': url}
                stats['mainEntityOfPage_added'] += 1
            if not node.get('articleSection') and sec:
                node['articleSection'] = sec
                stats['articleSection_added'] += 1
            if sec:
                sections[sec] += 1
            if json.dumps(node, sort_keys=True) != before:
                out = out.replace(block, json.dumps(node, separators=(',', ':'),
                                                    ensure_ascii=False), 1)
                changed = True
        if changed:
            stats['articles_touched'] += 1
            if not check:
                wr(rel, out)

    print('%s  %s' % ('CHECK' if check else 'APPLIED',
                      '  '.join('%s=%d' % kv for kv in sorted(stats.items()))))
    print('  sections assigned: %s' % dict(sections.most_common()))
    if unresolved:
        print('  NO SECTION RESOLVED (left empty rather than guessed): %s'
              % ', '.join(unresolved))


if __name__ == '__main__':
    main()
