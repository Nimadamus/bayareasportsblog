#!/usr/bin/env python3
"""_dashscan.py: report every dash used as punctuation across the site.

Counts em dashes, en dashes and the spaced hyphen (` - `) that reads as a dash. Does not
count hyphens inside words or numbers, which are ordinary spelling rather than dashes.
"""
import os, re, sys

SKIP_DIRS = {'.git', '__pycache__', 'assets', '_probe', 'node_modules'}
EXTS = ('.html', '.py', '.md')
SPACED = re.compile(r'(?<=\S) - (?=\S)')


def counts(text):
    return text.count('—'), text.count('–'), len(SPACED.findall(text))


def main():
    rows = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if not f.endswith(EXTS):
                continue
            p = os.path.join(root, f).replace(os.sep, '/').lstrip('./')
            if os.path.basename(p) == os.path.basename(__file__):
                continue
            try:
                t = open(p, encoding='utf-8').read()
            except Exception:
                continue
            em, en, sp = counts(t)
            if em + en + sp:
                rows.append((em + en + sp, em, en, sp, p))
    for tot, em, en, sp, p in sorted(rows, reverse=True):
        print('%4d  em=%-4d en=%-3d spaced=%-4d  %s' % (tot, em, en, sp, p))
    print('FILES=%d  TOTAL=%d' % (len(rows), sum(r[0] for r in rows)))
    return 1 if rows else 0


if __name__ == '__main__':
    sys.exit(main())
