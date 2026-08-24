#!/usr/bin/env python3
"""voice_gate.py: score a column against VOICE.md and print every machine tell in it.

Usage:
    python tools/voice_gate.py articles/<slug>.html   # one column, verbose
    python tools/voice_gate.py --all                  # every article, worst first
    python tools/voice_gate.py --all --min 70         # exit 1 if anything is under 70

Scores the prose only. Nav, head, tables and footers are stripped first. A HUMAN score
of 100 is a clean column. Ship at 70 or better.
"""
import os, re, sys, glob, html

# ---------------------------------------------------------------- body extraction
TAGS = re.compile(r'<[^>]+>')

def prose(path):
    t = open(path, encoding='utf-8').read()
    m = re.search(r'<article[^>]*>(.*?)</article>', t, re.S)
    if not m:
        return ''
    body = m.group(1)
    body = re.sub(r'<div class="reftable".*?</div>\s*', ' ', body, flags=re.S)
    body = re.sub(r'<table.*?</table>', ' ', body, flags=re.S)
    body = re.sub(r'<h1.*?</h1>', ' ', body, flags=re.S)
    body = re.sub(r'<div class="byline".*?</div>', ' ', body, flags=re.S)
    body = re.sub(r'<picture.*?</picture>', ' ', body, flags=re.S)
    body = re.sub(r'<p style="margin-top:30px.*?</p>', ' ', body, flags=re.S)
    paras = re.findall(r'<p[^>]*>(.*?)</p>', body, re.S)
    return [html.unescape(TAGS.sub('', p)).strip() for p in paras if TAGS.sub('', p).strip()]

def has_table(path):
    t = open(path, encoding='utf-8').read()
    m = re.search(r'<article[^>]*>(.*?)</article>', t, re.S)
    return bool(m and '<table' in m.group(1))

def bold_leads(path):
    t = open(path, encoding='utf-8').read()
    m = re.search(r'<article[^>]*>(.*?)</article>', t, re.S)
    return len(re.findall(r'<p><b>', m.group(1))) if m else 0

# ---------------------------------------------------------------- tells
CONTRACTABLE = re.compile(
    r"\b(do not|does not|did not|is not|are not|was not|were not|has not|have not|had not|"
    r"cannot|can not|could not|would not|should not|will not|it is|that is|there is|he is|"
    r"she is|they are|we are|you are|i am|i have|i will|you will|they will|we will|let us)\b", re.I)
CONTRACTION = re.compile(r"\b\w+['’](t|s|re|ve|ll|d|m)\b", re.I)

PHRASES = [
 (r"\bhere('s| is| are) (the thing|what|where|why|how)\b", 6, "here is the thing"),
 (r"\bthat('s| is) not (a |an |just )?[\w ]{2,28}[.,] (that('s| is)|it('s| is))\b", 6, "that is not X, that is Y"),
 (r"\bis not (just|only) [\w ]{2,30}[,.] (it('s| is)|that('s| is))\b", 6, "not just X, it is Y"),
 (r"\bmake no mistake\b", 5, "make no mistake"),
 (r"\bat the end of the day\b", 5, "at the end of the day"),
 (r"\b(it (is|'s) worth noting|it should be (said|noted)|to be fair,)", 5, "hedge preamble"),
 (r"\bthat('s| is) (the |not a )?(whole point|cliche)\b", 5, "that is the whole point / not a cliche"),
 (r"\b(time will tell|only time will tell|it will be interesting to see)\b", 6, "survey voice"),
 (r"\bthere are (arguments|cases) (on both sides|to be made)\b", 6, "survey voice"),
 (r"\b(according to|reports say|per (sources|reports)|sources said)\b", 8, "cited a source"),
 (r"\b(the atmosphere was|the energy was) (electric|palpable)\b", 5, "stock atmosphere"),
 (r"\bhere('s| is) where i land\b", 5, "here is where I land"),
 (r"\bevery single time\b", 3, "every single time"),
 (r"\bin (today's|this) (fast paced|modern) \w+", 5, "essay filler"),
]

# first person + lived detail
LIVED = re.compile(
 r"\b(i |i'|my |we |us |me\b|watched|remember|sitting|stood|screamed|yelled|turned it off|"
 r"group chat|my dad|my kid|my brother|the bar|parking lot|bart|the 101|the 880|candlestick|"
 r"the stick|oracle|chase center|levi's|coliseum|oracle park|fog|last call)", re.I)

def tricolons(paras):
    hits = []
    for p in paras:
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
        for i in range(len(sents) - 2):
            trio = sents[i:i + 3]
            ends = [re.sub(r'[^a-z ]', '', s.lower()).split()[-2:] for s in trio if s.split()]
            starts = [re.sub(r'[^a-z ]', '', s.lower()).split()[:2] for s in trio if s.split()]
            if len(ends) == 3 and ends[0] == ends[1] == ends[2]:
                hits.append(' / '.join(trio)[:110])
            elif len(starts) == 3 and starts[0] == starts[1] == starts[2]:
                hits.append(' / '.join(trio)[:110])
    return hits

def score(path):
    paras = prose(path)
    if not paras:
        return None
    text = ' '.join(paras)
    words = len(text.split())
    hits = []
    pts = 100

    # 1. contractions
    n_contr = len(CONTRACTION.findall(text))
    n_expand = len(CONTRACTABLE.findall(text))
    total = n_contr + n_expand
    rate = n_contr / total if total else 1.0
    if total >= 6 and rate < 0.55:
        cost = min(30, int((0.55 - rate) * 60))
        pts -= cost
        hits.append('CONTRACTIONS  %d of %d contractable spots are written out longhand (%.0f%% contracted, want 55%%+)  [-%d]'
                    % (n_expand, total, rate * 100, cost))

    # 2. banned phrases
    for pat, cost, label in PHRASES:
        for m in re.finditer(pat, text, re.I):
            pts -= cost
            hits.append('PHRASE        "%s"  ->  %s  [-%d]' % (m.group(0)[:60], label, cost))

    # 3. three beat lists
    for t in tricolons(paras):
        pts -= 5
        hits.append('TRICOLON      %s  [-5]' % t)

    # 4. rhythm: paragraph length variance
    plens = [len(p.split()) for p in paras]
    if len(plens) >= 6:
        mean = sum(plens) / len(plens)
        sd = (sum((x - mean) ** 2 for x in plens) / len(plens)) ** 0.5
        if mean and sd / mean < 0.45:
            pts -= 10
            hits.append('RHYTHM        every paragraph is the same size (mean %.0f words, spread %.0f%%, want 45%%+)  [-10]'
                        % (mean, sd / mean * 100))
    if len(plens) >= 6 and min(plens) > 12:
        pts -= 6
        hits.append('RHYTHM        no short punch paragraph anywhere (shortest is %d words)  [-6]' % min(plens))

    # 5. sentence length variance
    sents = [s for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    slens = [len(s.split()) for s in sents]
    if len(slens) >= 12:
        mean = sum(slens) / len(slens)
        sd = (sum((x - mean) ** 2 for x in slens) / len(slens)) ** 0.5
        if mean and sd / mean < 0.5:
            pts -= 8
            hits.append('RHYTHM        sentences all the same length (mean %.0f words, spread %.0f%%, want 50%%+)  [-8]'
                        % (mean, sd / mean * 100))

    # 6. lived detail
    lived = len(LIVED.findall(text))
    per1k = lived / (words / 1000.0) if words else 0
    if per1k < 8:
        cost = 12 if per1k < 4 else 6
        pts -= cost
        hits.append('NOBODY HOME   only %d first person / lived detail markers in %d words  [-%d]' % (lived, words, cost))

    # 7. bolded thesis leads
    bl = bold_leads(path)
    if bl > 2:
        cost = min(12, (bl - 2) * 3)
        pts -= cost
        hits.append('SCAFFOLD      %d bolded thesis lead ins, VOICE.md allows 1  [-%d]' % (bl, cost))

    # 8. table in a column
    if has_table(path) and not re.search(r'(depth-chart|schedule|roster|records|history|guide|hub|preview|stats)', path):
        pts -= 10
        hits.append('TABLE         reference table inside an opinion column  [-10]')

    return max(0, pts), hits, words


def main():
    args = sys.argv[1:]
    minimum = None
    if '--min' in args:
        i = args.index('--min'); minimum = int(args[i + 1]); del args[i:i + 2]

    if '--all' in args:
        rows = []
        for p in sorted(glob.glob('articles/*.html')):
            r = score(p)
            if r: rows.append((r[0], p, r[1]))
        rows.sort()
        for s, p, h in rows:
            print('%3d  %s' % (s, p))
        print('ARTICLES=%d  MEDIAN=%d  UNDER_70=%d' % (
            len(rows), rows[len(rows) // 2][0], sum(1 for r in rows if r[0] < 70)))
        if minimum is not None and rows and rows[0][0] < minimum:
            print('GATE FAILED: %s scored %d, floor is %d' % (rows[0][1], rows[0][0], minimum))
            return 1
        return 0

    if not args:
        print(__doc__); return 2
    for p in args:
        r = score(p)
        if not r:
            print('no <article> prose found in %s' % p); return 2
        s, h, w = r
        print('\n%s   %d words' % (p, w))
        print('HUMAN SCORE  %d / 100   %s' % (s, 'PASS' if s >= 70 else 'REWRITE IT'))
        if h:
            print('')
            for line in h: print('  ' + line)
        else:
            print('  clean')
        if minimum is not None and s < minimum:
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
