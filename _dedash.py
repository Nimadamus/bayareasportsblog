#!/usr/bin/env python3
"""_dedash.py: remove every dash used as punctuation from the site's copy.

Standing editorial rule: no dashes in anything published here. Em dashes, en dashes and
the spaced hyphen are the loudest tell that a machine wrote the sentence, so they are
banned outright. Hyphens inside a word, a score or a season label (third-and-five, 7-1,
2026-27) are ordinary sports spelling and are left alone.

The rewrite is deliberately surgical. It only ever touches the characters at and around
a dash, and it never runs a cleanup pass over the rest of the file, because attribute
values and URLs elsewhere in the markup are not ours to reformat. Files are read and
written as bytes so CRLF line endings survive untouched.

  dash between digits          5 - 4, 2026–27    ->  5-4, 2026-27
  dash between month names     Nov–Feb           ->  Nov to Feb
  dash after , ; : . ! ?       one thing, - two  ->  the dash is dropped
  dash anywhere else           clause - clause   ->  clause, clause

  python _dedash.py --check          report only, exit 1 if anything would change
  python _dedash.py                  rewrite every html and xml file in place
  python _dedash.py path [path ...]  rewrite only those files
"""
import os, re, sys

SKIP_DIRS = {'.git', '__pycache__', 'assets', '_probe', 'node_modules'}
SELF = os.path.basename(__file__)

DASH = '[—–−]'
H = '[ \t]'

# html entities render as real dashes on the page, so they are the same problem wearing a
# disguise. Normalised to a literal dash first, then handled by the rules below.
ENTITY = re.compile(r'&mdash;|&ndash;|&#8212;|&#8211;|&#x2013;|&#x2014;', re.I)
MONTHS = (r'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|January|February|March'
          r'|April|June|July|August|September|October|November|December')

RANGE_MON = re.compile(r'\b(' + MONTHS + r')' + H + r'*(?:' + DASH + r'|-)' + H +
                       r'*(' + MONTHS + r')\b')
RANGE_NUM = re.compile(r'(\d)' + H + r'*' + DASH + H + r'*(\d)')
RANGE_SPN = re.compile(r'(\d) - (\d)')

# a dash used as punctuation: the unicode dashes anywhere, or a hyphen with a space on
# both sides, which reads as a dash even though it is typed as a hyphen
PUNCT_DASH = re.compile(H + r'*' + DASH + H + r'*|(?<=\S) - (?=\S)')

CLOSERS = ',;:.!?'
HAS_DASH = re.compile(DASH + r'|(?<=\S) - (?=\S)')


def _replace(text):
    """Swap each punctuation dash for a comma, reading the original text to decide.

    The match already swallows the spaces either side, so the replacement carries its own
    spacing. Nothing outside a match is ever touched.
    """
    def sub(m):
        j = m.start() - 1
        while j >= 0 and text[j] in ' \t':
            j -= 1
        prev = text[j] if j >= 0 else ''
        # already punctuated, or a second dash in a row: the comma is there, just space it
        eol = m.end() >= len(text) or text[m.end()] in '\r\n'
        if prev in CLOSERS or prev in '—–−':
            return '' if eol else ' '
        return ',' if eol else ', '

    return PUNCT_DASH.sub(sub, text)


# a dash left hanging at the end of a source string literal, where the sentence carries
# on in the next literal of an implicit concatenation. Only used in literal mode, because
# in a finished html file a trailing dash is not a seam.
SEAM_TAIL = re.compile(r'(?<=\S)' + H + r'+(?:' + DASH + r'|-)' + H + r'*\Z')


def dedash(text, seams=False):
    text = ENTITY.sub('—', text)
    if seams:
        text = SEAM_TAIL.sub(', ', text)
    if not HAS_DASH.search(text):
        return text
    text = RANGE_MON.sub(r'\1 to \2', text)
    text = RANGE_NUM.sub(r'\1-\2', text)
    # note: a *spaced* hyphen between digits is not a range, it is a separator
    # ("9/10 - 8:35 PM"), so it falls through to the comma rule below rather than
    # being closed up into something that reads like a score.
    return _replace(text)


def targets(argv):
    paths = [a for a in argv if not a.startswith('--')]
    if paths:
        return paths
    out = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(('.html', '.xml')) and f != SELF:
                out.append(os.path.join(root, f))
    return out


def main():
    check = '--check' in sys.argv
    changed = 0
    for p in targets(sys.argv[1:]):
        try:
            raw = open(p, 'rb').read()
        except OSError:
            continue
        if b'\x00' in raw:
            print('SKIP (null bytes) %s' % p)
            continue
        new = dedash(raw.decode('utf-8')).encode('utf-8')
        if new == raw:
            continue
        changed += 1
        print('  %s' % p.replace(os.sep, '/'))
        if check:
            continue
        with open(p, 'wb') as fh:
            fh.write(new)
        back = open(p, 'rb').read()
        if b'\x00' in back or not back:
            raise SystemExit('corruption writing %s' % p)
    print('%s  files=%d' % ('WOULD CHANGE' if check else 'DEDASHED', changed))
    return 1 if (check and changed) else 0


if __name__ == '__main__':
    sys.exit(main())
