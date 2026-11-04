#!/usr/bin/env python3
"""hof_autolink.py: link the first plain mention of each Bay Area Hall of Famer in every
article body to that inductee's page. Idempotent. Only touches text inside <p> elements
inside <article>, never inside an existing link, never the dek/byline, at most 4 new links
per article, and never a player the article already links to.
Usage: python tools/hof_autolink.py [--dry]"""
import glob, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry" in sys.argv
MAX_PER_ARTICLE = 4


def players():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "_hof", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        if d.get("hold") or not os.path.exists(os.path.join(ROOT, d["slug"] + ".html")):
            continue
        out.append((d["name"], d["slug"]))
    # longer names first so "Dwight Clark" never collides with a shorter match
    return sorted(out, key=lambda x: -len(x[0]))


P_RE = re.compile(r"(<p(?:\s[^>]*)?>)(.*?)(</p>)", re.S)


def link_in_p(inner, name, href):
    """Replace the first occurrence of name in inner that sits outside any <a>...</a> or tag."""
    depth, i = 0, 0
    for m in re.finditer(r"<a\b[^>]*>|</a>|<[^>]+>|[^<]+", inner):
        tok = m.group(0)
        if tok.startswith("<a") and not tok.startswith("<abbr"):
            depth += 1
        elif tok == "</a>":
            depth = max(0, depth - 1)
        elif not tok.startswith("<") and depth == 0:
            k = re.search(r"(?<![\w>])" + re.escape(name) + r"(?![\w])", tok)
            if k:
                a, b = m.start() + k.start(), m.start() + k.end()
                return inner[:a] + f'<a href="{href}">{name}</a>' + inner[b:], True
    return inner, False


def main():
    roster = players()
    changed = 0
    for fp in sorted(glob.glob(os.path.join(ROOT, "articles", "*.html"))):
        s = open(fp, encoding="utf-8", newline="").read()
        a0, a1 = s.find("<article"), s.rfind("</article>")
        if a0 < 0 or a1 < 0:
            continue
        body = s[a0:a1]
        added = 0
        for name, slug in roster:
            if added >= MAX_PER_ARTICLE:
                break
            href = f"../{slug}.html"
            if f'href="{href}"' in body or name not in body:
                continue
            done = False

            def sub(m):
                nonlocal done
                if done or "font-style:italic" in m.group(1) or 'class="byline"' in m.group(1):
                    return m.group(0)
                new, ok = link_in_p(m.group(2), name, href)
                if ok:
                    done = True
                    return m.group(1) + new + m.group(3)
                return m.group(0)
            body = P_RE.sub(sub, body)
            if done:
                added += 1
        if added:
            changed += 1
            print(os.path.basename(fp), added)
            if not DRY:
                open(fp, "w", encoding="utf-8", newline="").write(s[:a0] + body + s[a1:])
    print("articles changed:", changed)


if __name__ == "__main__":
    main()
