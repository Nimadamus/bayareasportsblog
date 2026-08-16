#!/usr/bin/env python3
"""_dedash_py.py: strip punctuation dashes from the copy held inside the build scripts.

The article HTML is generated from the string literals in the cluster scripts, so
cleaning the HTML alone is cosmetic: the next `python _niners_cluster.py` would put every
dash straight back. This does the same rewrite as _dedash.py, but only inside string
literals, located with the ast module rather than by pattern matching.

Working on literals only is the whole point. A blind pass over a .py file would rewrite
subtraction (`len(a) - len(b)`) into a comma and break the script.

  python _dedash_py.py --check          report only
  python _dedash_py.py [path ...]       rewrite (defaults to the cluster + hub scripts)
"""
import ast, io, os, sys, tokenize

import _dedash

DEFAULT = ['_niners_cluster.py', '_giants_cluster.py', '_athletics_cluster.py',
           '_warriors_cluster.py', '_sharks_cluster.py', '_history_cluster.py',
           '_college_cluster.py', '_college_hubs.py', '_hub_copy.py', '_hub_upgrade.py',
           '_gen_sport_hubs.py', '_meta_fix.py', 'bay_daily.py']


def rewrite(src):
    """Return src with every string literal dedashed, or src unchanged."""
    out = []
    changed = 0
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        out.append(tok)
    pieces = []
    for tok in out:
        if tok.type == tokenize.STRING:
            try:
                value = ast.literal_eval(tok.string)
            except Exception:
                pieces.append(tok)
                continue
            if isinstance(value, str):
                new = _dedash.dedash(value, seams=True)
                if new != value:
                    changed += 1
    if not changed:
        return src, 0
    # rebuild by slicing the original text, working backwards so offsets stay valid
    lines = src.splitlines(keepends=True)
    starts = [0]
    for ln in lines:
        starts.append(starts[-1] + len(ln))

    def off(pos):
        row, col = pos
        return starts[row - 1] + col

    edits = []
    for tok in out:
        if tok.type != tokenize.STRING:
            continue
        try:
            value = ast.literal_eval(tok.string)
        except Exception:
            continue
        if not isinstance(value, str):
            continue
        if _dedash.dedash(value, seams=True) == value:
            continue
        # rewrite the raw source between the quotes rather than re-quoting the decoded
        # value: that way embedded quotes and escapes survive exactly as written
        raw = tok.string
        q = "'''" if raw.endswith("'''") else '"""' if raw.endswith('"""') else raw[-1]
        prefix = raw[:raw.index(q)]
        inner = raw[len(prefix) + len(q):-len(q)]
        edits.append((off(tok.start), off(tok.end),
                      prefix + q + _dedash.dedash(inner, seams=True) + q))
    for a, b, text in sorted(edits, reverse=True):
        src = src[:a] + text + src[b:]
    return src, len(edits)


def main():
    check = '--check' in sys.argv
    paths = [a for a in sys.argv[1:] if not a.startswith('--')] or DEFAULT
    total = 0
    for p in paths:
        if not os.path.exists(p):
            continue
        raw = open(p, 'rb').read()
        if b'\x00' in raw:
            print('SKIP (null bytes) %s' % p)
            continue
        src = raw.decode('utf-8')
        new, n = rewrite(src)
        if not n:
            continue
        total += n
        print('  %-28s literals rewritten: %d' % (p, n))
        if check:
            continue
        compile(new, p, 'exec')          # never write a file that will not parse
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write(new)
    print('%s  literals=%d' % ('WOULD CHANGE' if check else 'DEDASHED', total))
    return 1 if (check and total) else 0


if __name__ == '__main__':
    sys.exit(main())
