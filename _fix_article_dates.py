#!/usr/bin/env python3
"""_fix_article_dates.py - add datePublished / dateModified to Article JSON-LD
nodes that still lack them. Dates come from git: the commit that first added the
file, and the commit that last touched it. Nothing else in the node is changed.

  python _fix_article_dates.py [--check]
"""
import os, re, sys, glob, json, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def git_dates(rel):
    def run(args):
        r = subprocess.run(['git'] + args, cwd=ROOT, capture_output=True, text=True,
                           timeout=60)
        return [x for x in r.stdout.split() if x]
    added = run(['log', '--diff-filter=A', '--format=%ad', '--date=short',
                 '--follow', '--', rel])
    last = run(['log', '-1', '--format=%ad', '--date=short', '--', rel])
    pub = added[-1] if added else (last[0] if last else None)
    mod = last[0] if last else pub
    return pub, mod


def main():
    check = '--check' in sys.argv
    fixed = 0
    for f in sorted(glob.glob(os.path.join(ROOT, 'articles', '*.html'))):
        rel = 'articles/' + os.path.basename(f)
        s = open(f, encoding='utf-8', errors='strict').read()
        out, changed = s, False
        for m in LD_RE.finditer(s):
            try:
                node = json.loads(m.group(1))
            except Exception:
                continue
            if node.get('@type') not in ('Article', 'NewsArticle'):
                continue
            if 'datePublished' in node and 'dateModified' in node:
                continue
            pub, mod = git_dates(rel)
            if not pub:
                print('no git history for %s - skipped' % rel)
                continue
            node.setdefault('datePublished', pub)
            node['dateModified'] = node.get('dateModified') or mod
            new = json.dumps(node, separators=(',', ':'), ensure_ascii=False)
            out = out.replace(m.group(1), new, 1)
            changed = True
            print('%-56s published %s  modified %s'
                  % (rel.split('/')[-1][:56], node['datePublished'],
                     node['dateModified']))
        if changed:
            fixed += 1
            if not check:
                with open(f, 'w', encoding='utf-8', newline='') as fh:
                    fh.write(out)
                b = open(f, 'rb').read()
                if b'\x00' in b or b.count(b'\xef\xbf\xbd'):
                    raise SystemExit('corruption writing %s - ABORT' % f)
    print(('CHECK ' if check else 'APPLIED ') + '%d articles' % fixed)


if __name__ == '__main__':
    main()
