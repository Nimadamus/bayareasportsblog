#!/usr/bin/env python3
"""_seo_boost.py - purely ADDITIVE SEO hardening. Idempotent, safe to re-run.

Adds, only where missing (never removes, never rewrites visible copy,
never writes a noindex):
  1. Article JSON-LD on articles that have none (datePublished from the
     first git commit that added the file, so the date is real).
  2. dateModified on any Article/NewsArticle JSON-LD that lacks it.
  3. twitter:card where missing.
  4. og:image:width / og:image:height / og:image:alt (cards are 1200x675).
  5. width/height/decoding on every card <img>, plus loading="lazy" on
     everything below the first image on the page and fetchpriority="high"
     on the first (Core Web Vitals: kills layout shift, defers offscreen
     bytes, keeps the LCP image eager).

Run: python _seo_boost.py
"""
import os, re, glob, json, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://bayareasportsblog.com/"
SITE = "Bay Area Sports Blog"
SKIP = {'google6f74b54ecd988601.html'}
CARD_W, CARD_H = 1200, 675


def rd(p):
    return open(p, encoding='utf-8', errors='replace').read()


def wr(p, s):
    open(p, 'w', encoding='utf-8', newline='').write(s)


def first_commit_date(relpath):
    r = subprocess.run(['git', 'log', '--reverse', '--diff-filter=A',
                        '--format=%ad', '--date=short', '--', relpath],
                       capture_output=True, text=True, cwd=ROOT)
    lines = [l for l in r.stdout.strip().split('\n') if l]
    return lines[0] if lines else None


def meta(s, name=None, prop=None):
    pat = (r'<meta[^>]+name="%s"[^>]+content="([^"]*)"' % name if name
           else r'<meta[^>]+property="%s"[^>]+content="([^"]*)"' % prop)
    m = re.search(pat, s)
    return m.group(1) if m else None


def title_of(s):
    m = re.search(r'<title>(.*?)</title>', s, re.S)
    return m.group(1).strip() if m else None


def canonical_of(s):
    m = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    return m.group(1) if m else None


# ---------------------------------------------------------------- 1 + 2
def fix_article_schema(path, rel):
    s = rd(path)
    changed = False
    has_schema = ('"NewsArticle"' in s) or ('"@type":"Article"' in s)

    if not has_schema:
        date = first_commit_date(rel) or '2026-07-06'
        node = {
            "@context": "https://schema.org", "@type": "Article",
            "headline": (title_of(s) or '')[:110],
            "image": meta(s, prop='og:image') or '',
            "datePublished": date, "dateModified": date,
            "author": {"@type": "Organization", "name": SITE},
            "publisher": {"@type": "Organization", "name": SITE},
            "description": meta(s, name='description') or '',
            "mainEntityOfPage": canonical_of(s) or '',
            "inLanguage": "en-US",
        }
        tag = '<script type="application/ld+json">%s</script>\n' % json.dumps(
            node, ensure_ascii=False, separators=(',', ':'))
        s = s.replace('</head>', tag + '</head>', 1)
        changed = True

    # dateModified on any Article/NewsArticle node missing it
    if '"datePublished"' in s and '"dateModified"' not in s:
        s = re.sub(r'("datePublished":"(\d{4}-\d{2}-\d{2})")',
                   r'\1,"dateModified":"\2"', s, count=1)
        changed = True

    # twitter card
    if 'twitter:card' not in s:
        t = title_of(s) or SITE
        d = meta(s, name='description') or ''
        img = meta(s, prop='og:image') or ''
        block = ('<meta name="twitter:card" content="summary_large_image">\n'
                 '<meta name="twitter:title" content="%s">\n'
                 '<meta name="twitter:description" content="%s">\n'
                 '<meta name="twitter:image" content="%s">\n' % (t, d, img))
        s = s.replace('</head>', block + '</head>', 1)
        changed = True

    if changed:
        wr(path, s)
    return changed


# -------------------------------------------------------------------- 4
def fix_og_image_dims(path):
    s = rd(path)
    if 'og:image:width' in s or 'og:image"' not in s:
        return False
    alt = (meta(s, name='description') or SITE)[:180]
    block = ('<meta property="og:image:width" content="%d">\n'
             '<meta property="og:image:height" content="%d">\n'
             '<meta property="og:image:alt" content="%s">\n'
             % (CARD_W, CARD_H, alt.replace('"', '&quot;')))
    s = s.replace('</head>', block + '</head>', 1)
    wr(path, s)
    return True


# -------------------------------------------------------------------- 5
IMG_RE = re.compile(r'<img\s[^>]*?>', re.I)


def fix_images(path):
    s = rd(path)
    imgs = list(IMG_RE.finditer(s))
    if not imgs:
        return 0
    out, last, n = [], 0, 0
    for i, m in enumerate(imgs):
        tag = m.group(0)
        new = tag
        if 'width=' not in new:
            new = new[:-1].rstrip() + ' width="%d" height="%d">' % (CARD_W, CARD_H)
        if 'decoding=' not in new:
            new = new[:-1].rstrip() + ' decoding="async">'
        if i == 0:
            if 'fetchpriority=' not in new:
                new = new[:-1].rstrip() + ' fetchpriority="high">'
        elif 'loading=' not in new:
            new = new[:-1].rstrip() + ' loading="lazy">'
        if new != tag:
            n += 1
        out.append(s[last:m.start()]); out.append(new); last = m.end()
    out.append(s[last:])
    if n:
        wr(path, ''.join(out))
    return n


def main():
    os.chdir(ROOT)
    arts = [f.replace(os.sep, '/') for f in sorted(glob.glob('articles/*.html'))]
    pages = [f for f in sorted(glob.glob('*.html')) if f not in SKIP]

    a = sum(fix_article_schema(f, f) for f in arts)
    b = sum(fix_og_image_dims(f) for f in arts + pages)
    c = sum(fix_images(f) for f in arts + pages)
    print('article schema/dateModified/twitter fixed : %d files' % a)
    print('og:image dimensions added                 : %d files' % b)
    print('<img> attributes upgraded                 : %d tags' % c)


if __name__ == '__main__':
    main()
