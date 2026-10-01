#!/usr/bin/env python3
"""_trust_schema.py: the identity half of the structured data, enforced on every page.

What it fixes, all of it in JSON-LD only, nothing visible changes:

1. Articles named their author and publisher as a bare Organization with a name and
   nothing else, so nothing tied a story back to the site's About page or home page.
   The author now carries the About page as its url, the publisher carries the home
   page and the same logo the home page Organization declares, and every article
   carries url equal to its canonical, with mainEntityOfPage pointing at the same URL.
2. The trust pages were all typed CollectionPage. About is an AboutPage, Contact is a
   ContactPage, the three policy pages are plain WebPages.
3. The home page Organization claimed a diversityPolicy that pointed at the editorial
   standards page, which has no diversity policy in it. A claim the page does not back
   up is removed rather than kept.
4. The 404 page declared a canonical and a breadcrumb, which a not found page should
   never do.
5. The five team hubs say which team they are about (SportsTeam), which is a fact.

Idempotent. Run it after any new article, and the daily refresh action runs it too, so a
new article cannot ship with the old shape for more than a few hours.

    python _trust_schema.py            rewrite
    python _trust_schema.py --check    exit 1 if anything would change
"""
import os
import re
import sys
import glob
import json

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://bayareasportsblog.com/'
NAME = 'Bay Area Sports Blog'
LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)
ARTICLE_TYPES = ('NewsArticle', 'Article', 'BlogPosting')

PAGE_TYPES = {
    'about.html': 'AboutPage',
    'contact.html': 'ContactPage',
    'editorial-standards.html': 'WebPage',
    'corrections.html': 'WebPage',
    'privacy.html': 'WebPage',
}

TEAMS = {
    '49ers.html': ('San Francisco 49ers', 'American football'),
    'warriors.html': ('Golden State Warriors', 'Basketball'),
    'giants.html': ('San Francisco Giants', 'Baseball'),
    'athletics.html': ('Athletics', 'Baseball'),
    'sharks.html': ('San Jose Sharks', 'Ice hockey'),
}


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))


def org_logo():
    text = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    for m in LD.finditer(text):
        d = json.loads(m.group(2))
        for item in d.get('@graph', [d]):
            if item.get('@type') == 'NewsMediaOrganization' and item.get('logo'):
                return item['logo']
    raise SystemExit('home page Organization logo not found')


def fix_article(item, canonical, logo):
    item['author'] = {'@type': 'Organization', 'name': NAME, 'url': BASE + 'about.html'}
    item['publisher'] = {'@type': 'Organization', 'name': NAME, 'url': BASE,
                         'logo': {'@type': 'ImageObject', 'url': logo}}
    if canonical:
        item['url'] = canonical
        item['mainEntityOfPage'] = {'@type': 'WebPage', '@id': canonical}
    pub, mod = item.get('datePublished', ''), item.get('dateModified', '')
    if pub and (not mod or mod < pub):
        item['dateModified'] = pub
    return item


def process(path, logo):
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    text = open(path, encoding='utf-8', newline='').read()
    orig = text
    m = re.search(r'<link rel="canonical" href="([^"]+)"', text)
    canonical = m.group(1) if m else None

    if rel == '404.html':
        text = re.sub(r'\s*<link rel="canonical" href="[^"]*">', '', text)
        text = LD.sub('', text)
        return text, orig

    def repl(m):
        try:
            d = json.loads(m.group(2))
        except ValueError:
            return m.group(0)
        items = d.get('@graph', [d]) if isinstance(d, dict) else d
        for item in items:
            t = item.get('@type')
            if t in ARTICLE_TYPES:
                fix_article(item, canonical, logo)
            elif t == 'NewsMediaOrganization':
                item.pop('diversityPolicy', None)
            elif t == 'CollectionPage' and rel in PAGE_TYPES:
                item['@type'] = PAGE_TYPES[rel]
            if t == 'CollectionPage' and rel in TEAMS:
                name, sport = TEAMS[rel]
                item['about'] = {'@type': 'SportsTeam', 'name': name, 'sport': sport}
        return m.group(1) + dump(d) + m.group(3)

    text = LD.sub(repl, text)
    return text, orig


def main():
    check = '--check' in sys.argv
    logo = org_logo()
    paths = sorted(glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'articles', '*.html')))
    changed = []
    for p in paths:
        new, old = process(p, logo)
        if new != old:
            changed.append(os.path.relpath(p, ROOT))
            if not check:
                open(p, 'w', encoding='utf-8', newline='').write(new)
    print('%s %d of %d pages' % ('would change' if check else 'changed', len(changed), len(paths)))
    if check and changed:
        sys.exit(1)


if __name__ == '__main__':
    main()
