#!/usr/bin/env python3
"""_link_candidates.py - find honest inbound-link opportunities for starved articles.

For every article the crawl says has no in-body inbound link, this looks for other
articles whose prose already talks about the same thing: the same player, the same
opponent, the same streak, the same trade. It returns the actual sentence so a human
can judge whether a link there would help a reader or just pad a number.

It proposes. It does not write anything.

  python _link_candidates.py [--max 3] > candidates.txt
"""
import os, re, sys, glob, json, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(ROOT, 'articles')

TEAMS = ('49ers', 'giants', 'athletics', 'warriors', 'sharks')
MONTHS = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
          'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11,
          'december': 12}
_CUM = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

STOPNAME = {'The', 'A', 'An', 'And', 'But', 'It', 'He', 'She', 'They', 'That', 'This',
            'There', 'What', 'When', 'Where', 'Why', 'How', 'If', 'So', 'For', 'In',
            'On', 'At', 'To', 'Of', 'With', 'From', 'By', 'Is', 'Was', 'Are', 'Were',
            'Final', 'Giants', 'Athletics', 'Warriors', 'Sharks', 'Bay', 'Area',
            'Sports', 'Blog', 'Column', 'Read', 'More', 'Home', 'Latest', 'August',
            'July', 'June', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'National', 'American', 'League', 'Series', 'Night'}


def rd(p):
    return open(p, encoding='utf-8', errors='replace').read()


def body_of(html):
    m = re.search(r'<article[^>]*>(.*?)</article>', html, re.S)
    return m.group(1) if m else ''


def text_of(html):
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', html, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = (s.replace('&amp;', '&').replace('&#39;', "'").replace('&nbsp;', ' ')
          .replace('&mdash;', '-').replace('&quot;', '"'))
    return re.sub(r'\s+', ' ', s).strip()


def slug_date(slug):
    m = re.search(r'-(' + '|'.join(MONTHS) + r')-(\d{1,2})$', slug)
    return _CUM[MONTHS[m.group(1)] - 1] + int(m.group(2)) if m else None


def slug_team(slug):
    return next((t for t in TEAMS if slug.startswith(t + '-')), None)


def names_in(txt):
    """Multi-word proper nouns: 'Jacob Lopez', 'Bryce Eldridge', 'Macklin Celebrini'."""
    out = set()
    for m in re.finditer(r"\b([A-Z][a-z'\-]+(?:\s+[A-Z][a-z'\-]+){1,2})\b", txt):
        p = m.group(1)
        parts = p.split()
        if any(w in STOPNAME for w in parts):
            continue
        if len(p) < 8:
            continue
        out.add(p)
    return out


def main():
    mx = int(sys.argv[sys.argv.index('--max') + 1]) if '--max' in sys.argv else 3
    audit = json.load(open(os.path.join(ROOT, '_seo_audit.json'), encoding='utf-8'))
    bic = audit['body_inbound_counts']

    arts = {}
    for f in sorted(glob.glob(os.path.join(ART, '*.html'))):
        rel = 'articles/' + os.path.basename(f)
        html = rd(f)
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
        arts[rel] = {
            'slug': os.path.basename(f)[:-5], 'html': html,
            'h1': text_of(h1.group(1)) if h1 else '',
            'body': text_of(body_of(html)),
            'raw_body': body_of(html),
            'date': slug_date(os.path.basename(f)[:-5]),
            'team': slug_team(os.path.basename(f)[:-5]),
        }

    starved = [a for a in arts if bic.get(a, 0) == 0]
    print('# starved articles: %d\n' % len(starved))

    for tgt in starved:
        t = arts[tgt]
        keys = names_in(t['h1']) | {n for n in names_in(t['body'][:600])}
        # drop names that appear in more than a quarter of the corpus - too generic
        freq = collections.Counter()
        for a in arts.values():
            for k in keys:
                if k in a['body']:
                    freq[k] += 1
        keys = {k for k in keys if 1 <= freq[k] <= max(3, len(arts) // 6)}

        cands = []
        for src, a in arts.items():
            if src == tgt:
                continue
            if ('href="%s"' % os.path.basename(tgt)) in a['raw_body']:
                continue                       # already links there
            hits = [k for k in keys if k in a['body']]
            if not hits:
                continue
            sent = ''
            for k in hits:
                m = re.search(r'([^.!?]*\b' + re.escape(k) + r'\b[^.!?]*[.!?])', a['body'])
                if m and len(m.group(1)) < 400:
                    sent = m.group(1).strip()
                    break
            score = 0
            score += 3 if a['team'] and a['team'] == t['team'] else 0
            score += 2 * len(hits)
            if a['date'] and t['date']:
                gap = abs(a['date'] - t['date'])
                score += 3 if gap <= 3 else (2 if gap <= 10 else 0)
            if a['date'] is None:              # evergreen / explainer piece
                score += 2
            cands.append((score, src, hits, sent))

        cands.sort(key=lambda c: -c[0])
        print('=' * 100)
        print('TARGET  %s' % tgt)
        print('   H1   %s' % t['h1'][:96])
        print('   keys %s' % ', '.join(sorted(keys)[:8]))
        if not cands:
            print('   NO CANDIDATE - nothing else on the site mentions this')
        for score, src, hits, sent in cands[:mx]:
            print('   -> [%2d] %s' % (score, src))
            print('        hits: %s' % ', '.join(hits[:4]))
            print('        sent: %s' % sent[:230])
        print()


if __name__ == '__main__':
    main()
