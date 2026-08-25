#!/usr/bin/env python3
"""humanize.py: contract the longhand verb phrases inside column prose.

VOICE.md rule 1. Only touches text nodes inside <p> elements inside <article>, never
tags, attributes, hrefs, headings, meta, JSON-LD, tables or captions. Text inside double
quotes is left alone so quoted lines stay exactly as they were said.

    python tools/humanize.py --dry articles/*.html    # report only
    python tools/humanize.py articles/<slug>.html     # rewrite in place
    python tools/humanize.py --descaffold "articles/*.html"   # VOICE.md rule 5, one bold lead in
"""
import re, sys, glob, os

# longhand -> contraction. Order matters: longest first.
PAIRS = [
    ("would not", "wouldn't"), ("should not", "shouldn't"), ("could not", "couldn't"),
    ("does not", "doesn't"), ("did not", "didn't"), ("do not", "don't"),
    ("was not", "wasn't"), ("were not", "weren't"), ("is not", "isn't"),
    ("are not", "aren't"), ("has not", "hasn't"), ("have not", "haven't"),
    ("had not", "hadn't"), ("will not", "won't"), ("cannot", "can't"), ("can not", "can't"),
    ("it is", "it's"), ("that is", "that's"), ("there is", "there's"), ("here is", "here's"),
    ("he is", "he's"), ("she is", "she's"), ("what is", "what's"), ("who is", "who's"),
    ("they are", "they're"), ("we are", "we're"), ("you are", "you're"),
    ("I am", "I'm"), ("I have", "I've"), ("I will", "I'll"), ("I would", "I'd"),
    ("we have", "we've"), ("we will", "we'll"), ("they have", "they've"),
    ("they will", "they'll"), ("you have", "you've"), ("you will", "you'll"),
    ("he will", "he'll"), ("she will", "she'll"), ("it will", "it'll"),
    ("we would", "we'd"), ("they would", "they'd"), ("you would", "you'd"),
    ("let us", "let's"),
]
COPULA = {'it is', 'that is', 'there is', 'here is', 'he is', 'she is', 'what is', 'who is',
          'they are', 'we are', 'you are', 'I am'}


def _rx(a):
    # "X have" only contracts before a participle, never before a noun phrase:
    # "I have watched" becomes "I've watched", but "I have no vote" stays put.
    tail = (r'(?! +(to|no|a|an|the|some|any|my|his|her|their|our|it|that|this|one|two|three'
            r'|more|enough|nothing|another|plenty)\b)') if a.endswith(' have') else ''
    # a copula never contracts at the end of a clause: "what they say it is" stays put
    if a in COPULA:
        tail += r'(?![^A-Za-z0-9]*[.,;:!?<])(?! +(and|but|or|so|then|yet|too))'
    return re.compile(r'\b%s\b%s' % (re.escape(a), tail), re.I)


RX = [(_rx(a), b) for a, b in PAIRS]


def convert(seg):
    """seg is a plain text run with no markup and no quotation marks."""
    out = seg
    for rx, repl in RX:
        def sub(m):
            s = m.group(0)
            # preserve capitalisation of the first letter
            r = repl
            if s[0].isupper():
                r = r[0].upper() + r[1:]
            return r
        out = rx.sub(sub, out)
    return out


def process_text(text):
    """Convert outside double quotes only."""
    parts = re.split(r'("[^"]*")', text)
    return ''.join(p if p.startswith('"') else convert(p) for p in parts)


def process_para(p):
    """p is the inner HTML of a <p>. Convert text nodes only."""
    return ''.join(x if x.startswith('<') else process_text(x)
                   for x in re.split(r'(<[^>]+>)', p))


def run(path, dry=False):
    raw = open(path, 'rb').read().decode('utf-8')
    m = re.search(r'(<article[^>]*>)(.*?)(</article>)', raw, re.S)
    if not m:
        return 0
    body = m.group(2)
    n = [0]

    def para(mm):
        inner = mm.group(2)
        new = process_para(inner)
        if new != inner:
            n[0] += 1
        return mm.group(1) + new + mm.group(3)

    body2 = re.sub(r'(<p[^>]*>)(.*?)(</p>)', para, body, flags=re.S)
    if not dry and body2 != body:
        out = raw[:m.start(2)] + body2 + raw[m.end(2):]
        open(path, 'wb').write(out.encode('utf-8'))
    return n[0]


# --------------------------------------------------------------- descaffold
def descaffold(path, keep=1, dry=False):
    """VOICE.md rule 5: at most one bolded thesis lead in per column. Unwraps the rest.
    Only touches <p><b>...</b> openings, never bold used mid sentence."""
    raw = open(path, 'rb').read().decode('utf-8')
    m = re.search(r'(<article[^>]*>)(.*?)(</article>)', raw, re.S)
    if not m:
        return 0
    body = m.group(2)
    seen = [0]

    def fix(mm):
        seen[0] += 1
        if seen[0] <= keep:
            return mm.group(0)
        return '<p>' + mm.group(1)

    body2 = re.sub(r'<p><b>(.*?)</b>', fix, body, flags=re.S)
    n = max(0, seen[0] - keep)
    if n and not dry:
        open(path, 'wb').write((raw[:m.start(2)] + body2 + raw[m.end(2):]).encode('utf-8'))
    return n


def main():
    args = sys.argv[1:]
    dry = '--dry' in args
    scaf = '--descaffold' in args
    args = [a for a in args if a not in ('--dry', '--descaffold')]
    files = []
    for a in args:
        files.extend(glob.glob(a))
    if not files:
        print(__doc__); return 2
    tot = 0
    for f in sorted(files):
        c = descaffold(f, dry=dry) if scaf else run(f, dry)
        tot += c
        if c:
            print('%3d paragraphs  %s' % (c, f))
    print('%s  files=%d  %s=%d' % ('DRY RUN' if dry else 'REWROTE', len(files),
          'lead ins unbolded' if scaf else 'paragraphs touched', tot))
    return 0


if __name__ == '__main__':
    sys.exit(main())
