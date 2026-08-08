#!/usr/bin/env python3
"""_internal_links.py - automated contextual internal-linking engine.

Adds true in-body editorial links: it finds a phrase already written in one
article's prose that uniquely names another article's subject, and wraps that
existing phrase in an anchor. It never writes new copy, never adds a section,
card or widget, and never touches anything outside <article>...</article>.

Candidate anchor phrases for a target article are contiguous n-grams of its
<h1> that are backed by its own slug (so they are the editor's own keywords),
and that resolve to exactly ONE article on the site. Ambiguous phrases are
discarded, so an anchor can only ever point at the one piece it names.

Priority goes to articles the crawl baseline flagged with zero in-body inbound
links.

  python _internal_links.py                 # dry run, writes the report only
  python _internal_links.py --apply         # rewrite the HTML
  python _internal_links.py --max-out 3 --max-in 4

Report: _internal_links_report.json
"""
import os, re, sys, glob, json, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(ROOT, 'articles')
REPORT = os.path.join(ROOT, '_internal_links_report.json')

MAX_OUT = 3          # new links added per source article
MAX_IN = 4           # new inbound links a single target may collect
MIN_PHRASE_CHARS = 13
MIN_PHRASE_WORDS = 2
MAX_PHRASE_WORDS = 6

# words that carry no topical signal, so a phrase made only of these is useless
STOP = set("""a an the and or but of to in on at by for from with without into over
under as is are was were be been being it its this that these those he she they
him her them his their you your we our i me my not no nor if then than so such
about after again all also am any because before both did do does doing down
during each few first got had has have how just least less like made make many
more most much never new next now off once only other out own same second still
some there through too two up very what when where which while who whom why will
would can could should may might must one three four five six seven eight nine
ten again against here how ever even back get gets going gone got""".split())

# generic sport words: allowed inside a phrase, never enough on their own
GENERIC = set("""game games win wins won loss losses lose lost season seasons team
teams year years night day days start starts started inning innings quarter half
point points run runs hit hits score scored scoring play plays player players
camp practice roster deal contract trade traded sign signed signing coach
manager pitcher hitter receiver quarterback defense offense bay area sports blog
column columns 49ers giants warriors athletics sharks stanford cal""".split())

TEAM_PREFIX = ('49ers', 'giants', 'warriors', 'athletics', 'sharks', 'stanford',
               'cal', 'bayarea', 'dynasties', 'flashbacks', 'history', 'betting')

H1_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.S)
ARTICLE_RE = re.compile(r'(<article\b[^>]*>)(.*?)(</article>)', re.S)
P_RE = re.compile(r'(<p\b[^>]*>)(.*?)(</p>)', re.S)
TAG_RE = re.compile(r'<[^>]+>')


def rd(p):
    return open(p, encoding='utf-8', errors='replace').read()


def text_of(html):
    s = TAG_RE.sub(' ', html)
    s = s.replace('&amp;', '&').replace('&nbsp;', ' ')
    s = re.sub(r'&[a-z]+;|&#\d+;', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def words(s):
    return re.findall(r"[a-z0-9][a-z0-9'\-]*", s.lower())


def slug_tokens(slug):
    parts = [t for t in slug.split('-') if t]
    while parts and parts[0] in TEAM_PREFIX:
        parts = parts[1:]
    # drop trailing date noise: month names, bare numbers, years
    months = {'january', 'february', 'march', 'april', 'may', 'june', 'july',
              'august', 'september', 'october', 'november', 'december'}
    return [t for t in parts if t not in months and not re.fullmatch(r'\d{1,4}', t)]


def candidate_phrases(h1_text, slug):
    """n-grams of the H1 that are backed by the article's own slug."""
    stoks = set(slug_tokens(slug))
    w = words(h1_text)
    out = []
    for n in range(MAX_PHRASE_WORDS, MIN_PHRASE_WORDS - 1, -1):
        for i in range(len(w) - n + 1):
            gram = w[i:i + n]
            if gram[0] in STOP or gram[-1] in STOP:
                continue
            content = [t for t in gram if t not in STOP]
            if len(content) < 2:
                continue
            phrase = ' '.join(gram)
            if len(phrase) < MIN_PHRASE_CHARS:
                continue
            # must be the editor's own keywords, and not purely generic filler
            backed = [t for t in content if t in stoks]
            if len(backed) < max(2, (len(content) + 1) // 2):
                continue
            # anchor readability: a link must not open or close on filler, and
            # must carry at least two words of real subject matter
            if gram[0] in GENERIC or gram[-1] in GENERIC:
                continue
            specific = [t for t in backed if t not in GENERIC]
            if len(specific) < 2:
                continue
            if sum(1 for t in gram if t in GENERIC) > 1:
                continue
            out.append((phrase, specific))
    return out


def phrase_regex(phrase):
    parts = [re.escape(t) for t in phrase.split(' ')]
    # tolerate whitespace, nbsp and hyphen/space drift between words
    return re.compile(r'(?<![\w>])' + r'[\s \-]+'.join(parts) + r'(?![\w])',
                      re.IGNORECASE)


def split_outside_anchors(html):
    """Yield (is_linkable, chunk) - text outside tags and outside <a>...</a>."""
    out, depth, pos = [], 0, 0
    for m in re.finditer(r'<(/?)(a|h1|h2|h3|h4|h5|h6)\b[^>]*>', html, re.I):
        out.append((depth == 0, html[pos:m.start()]))
        out.append((False, m.group(0)))
        depth += -1 if m.group(1) else 1
        depth = max(depth, 0)
        pos = m.end()
    out.append((depth == 0, html[pos:]))
    return out


# Relative-time phrases a recap uses to refer to the previous game. These are
# linked only to the same team's immediately preceding dated article, so the
# reference is exactly the piece the sentence is pointing at.
# phrases that mean "yesterday" - only valid when the two dates are 1 day apart
NIGHT_PHRASES = [
    'the night before', 'the previous night', 'a night earlier',
    'the night prior', 'the day before', 'the previous day', 'last night',
    'yesterday',
]
# phrases that mean "the last game" - valid up to a few days apart. "last time
# out" is deliberately excluded: in this prose it means a pitcher's previous
# start, which is not the team's previous game.
GAME_PHRASES = ['the game before', 'the previous game', 'the night before that']
# phrases that mean the first game of the current series
OPENER_PHRASES = ['the series opener', 'the opener of the series',
                  'the first game of the series', 'the series-opening',
                  'in the opener', 'the opener']

MONTHS = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5,
          'june': 6, 'july': 7, 'august': 8, 'september': 9, 'october': 10,
          'november': 11, 'december': 12}


def slug_date(slug):
    """(month, day) trailing date in a slug, or None."""
    m = re.search(r'-(' + '|'.join(MONTHS) + r')-(\d{1,2})$', slug)
    if m:
        return (MONTHS[m.group(1)], int(m.group(2)))
    return None


def slug_team(slug):
    for t in TEAM_PREFIX:
        if slug.startswith(t + '-'):
            return t
    return None


def slug_opponent(slug):
    t = slug_team(slug)
    if not t:
        return None
    rest = slug[len(t) + 1:].split('-')
    return rest[0] if rest and not re.fullmatch(r'\d+', rest[0]) else None


_CUM = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]


def day_index(md):
    return _CUM[md[0] - 1] + md[1]


def find_in_body(body, rx):
    """First offset span of rx inside a <p>, outside any anchor/heading."""
    for pm in P_RE.finditer(body):
        inner = pm.group(2)
        if 'More coverage' in inner:
            continue
        off, cur = pm.start(2), 0
        for linkable, chunk in split_outside_anchors(inner):
            if linkable and chunk:
                fm = rx.search(chunk)
                if fm:
                    return (off + cur + fm.start(), off + cur + fm.end())
            cur += len(chunk)
    return None


def load():
    arts = {}
    for f in sorted(glob.glob(os.path.join(ART, '*.html'))):
        rel = 'articles/' + os.path.basename(f)
        s = rd(f)
        m = H1_RE.search(s)
        if not m:
            continue
        slug = os.path.basename(f)[:-5]
        arts[rel] = {
            'path': f, 'slug': slug, 'html': s,
            'h1': text_of(m.group(1)),
            'phrases': candidate_phrases(text_of(m.group(1)), slug),
        }
    return arts


def main():
    apply = '--apply' in sys.argv
    max_out = int(_arg('--max-out', MAX_OUT))
    max_in = int(_arg('--max-in', MAX_IN))

    arts = load()

    # phrase -> targets; keep only phrases that name exactly one article
    owner = collections.defaultdict(set)
    spec_of = {}
    for rel, a in arts.items():
        for p, specific in a['phrases']:
            owner[p].add(rel)
            spec_of[p] = specific
    unique = {p: next(iter(t)) for p, t in owner.items() if len(t) == 1}
    # longest phrase wins, so the most specific anchor is tried first
    ordered = sorted(unique.items(), key=lambda kv: -len(kv[0]))

    # priority: targets the baseline flagged with no in-body inbound link
    need = set()
    try:
        base = json.load(open(os.path.join(ROOT, '_seo_audit.json'), encoding='utf-8'))
        bic = base.get('body_inbound_counts', {})
        need = {r for r in arts if bic.get(r, 0) == 0}
    except Exception:
        pass

    # working copy of each article body, edited in place as links are placed
    bodies, spans = {}, {}
    for rel, a in arts.items():
        am = ARTICLE_RE.search(a['html'])
        if am:
            bodies[rel] = am.group(2)
            spans[rel] = (am.start(2), am.end(2))

    inbound_new = collections.Counter()
    outbound_new = collections.Counter()
    linked_pairs = set()
    plan = []

    def relevant(src, tgt, phrase):
        """Only link across teams when the anchor is unmistakably specific."""
        st, tt = slug_team(arts[src]['slug']), slug_team(arts[tgt]['slug'])
        if st and st == tt:
            return True
        return len(spec_of.get(phrase, [])) >= 3

    def place(src, tgt, rx, phrase, kind):
        """Wrap the first eligible occurrence of rx in src's body with a link."""
        if src == tgt or src not in bodies:
            return False
        if kind == 'phrase' and not relevant(src, tgt, phrase):
            return False
        if (src, tgt) in linked_pairs:
            return False
        if outbound_new[src] >= max_out or inbound_new[tgt] >= max_in:
            return False
        hit = find_in_body(bodies[src], rx)
        if not hit:
            return False
        a, b = hit
        anchor = bodies[src][a:b]
        bodies[src] = (bodies[src][:a]
                       + '<a href="%s">%s</a>' % (os.path.basename(tgt), anchor)
                       + bodies[src][b:])
        inbound_new[tgt] += 1
        outbound_new[src] += 1
        linked_pairs.add((src, tgt))
        plan.append({'from': src, 'to': tgt, 'anchor': anchor, 'phrase': phrase,
                     'kind': kind, 'starved_target': tgt in need})
        return True

    phrases_by_target = collections.defaultdict(list)
    for phrase, tgt in ordered:
        phrases_by_target[tgt].append(phrase)

    # ---- pass 1: chronological references inside same-team dated coverage.
    # "last night" is only wired up when the previous piece really is one day
    # earlier; "the series opener" only to the first game of the same series.
    dated = collections.defaultdict(list)
    for rel, a in arts.items():
        d, t = slug_date(a['slug']), slug_team(a['slug'])
        if d and t:
            dated[t].append((day_index(d), rel))
    prev_of, opener_of = {}, {}
    for t, items in dated.items():
        items.sort()
        for i in range(1, len(items)):
            prev_of[items[i][1]] = (items[i][0] - items[i - 1][0], items[i - 1][1])
            # walk back over the unbroken run of games against this opponent
            opp = slug_opponent(arts[items[i][1]]['slug'])
            j = i
            while (j - 1 >= 0
                   and slug_opponent(arts[items[j - 1][1]]['slug']) == opp
                   and items[j][0] - items[j - 1][0] <= 2):
                j -= 1
            if j < i and opp:
                opener_of[items[i][1]] = items[j][1]
    for src in sorted(bodies):
        placed = False
        gap_tgt = prev_of.get(src)
        if gap_tgt:
            gap, tgt = gap_tgt
            buckets = []
            if gap == 1:
                buckets += NIGHT_PHRASES
            if gap <= 3:
                buckets += GAME_PHRASES
            for phrase in buckets:
                if place(src, tgt, phrase_regex(phrase), phrase, 'chrono'):
                    placed = True
                    break
        op = opener_of.get(src)
        if op and not placed:
            for phrase in OPENER_PHRASES:
                if place(src, op, phrase_regex(phrase), phrase, 'chrono-opener'):
                    break

    # ---- pass 2: breadth - give every starved target one in-body inbound link
    for depth in (1, 2):
        for tgt in sorted(need):
            if inbound_new[tgt] >= depth:
                continue
            for phrase in phrases_by_target.get(tgt, []):
                rx = phrase_regex(phrase)
                done = False
                for src in sorted(bodies, key=lambda s: outbound_new[s]):
                    if place(src, tgt, rx, phrase, 'phrase'):
                        done = True
                        break
                if done:
                    break

    # ---- pass 3: remaining capacity for well-linked targets
    for src in sorted(bodies):
        if outbound_new[src] >= max_out:
            continue
        for phrase, tgt in ordered:
            if outbound_new[src] >= max_out:
                break
            if tgt in need:
                continue
            place(src, tgt, phrase_regex(phrase), phrase, 'phrase')

    changed = {}
    for rel in bodies:
        if outbound_new[rel]:
            s, (a, b) = arts[rel]['html'], spans[rel]
            changed[rel] = s[:a] + bodies[rel] + s[b:]

    json.dump({'links_added': len(plan), 'source_articles_touched': len(changed),
               'targets_gaining_links': len(inbound_new),
               'starved_targets_fixed': sum(1 for t in inbound_new if t in need),
               'unique_phrase_vocabulary': len(unique),
               'caps': {'max_out': max_out, 'max_in': max_in},
               'applied': apply, 'links': plan},
              open(REPORT, 'w', encoding='utf-8'), indent=1)

    if apply:
        for rel, new in changed.items():
            out = arts[rel]['path']
            with open(out, 'w', encoding='utf-8', newline='') as fh:
                fh.write(new)
            if b'\x00' in open(out, 'rb').read():
                raise SystemExit('NULL-byte corruption writing %s - ABORT' % out)

    print('%s: %d links, %d source articles, %d targets (%d previously starved)'
          % ('APPLIED' if apply else 'DRY RUN', len(plan), len(changed),
             len(inbound_new), sum(1 for t in inbound_new if t in need)))
    print('unique-phrase vocabulary: %d' % len(unique))
    for r in plan[:12]:
        print('  %s  --[%s]-->  %s' % (r['from'].split('/')[-1][:38],
                                       r['anchor'], r['to'].split('/')[-1][:38]))


def _arg(flag, default):
    if flag in sys.argv:
        return sys.argv[sys.argv.index(flag) + 1]
    return default


if __name__ == '__main__':
    main()
