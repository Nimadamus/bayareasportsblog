#!/usr/bin/env python3
"""Fail if a published meta description decodes to more than 160 characters.

Ahrefs flags meta descriptions over 160 characters. Run from the repo root:

    python tools/desc_len_check.py
"""
import glob
import os
import re
import sys
from html import unescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = re.compile(
    r'<meta\s+name="description"\s+content="([^"]*)"',
    re.I,
)
LIMIT = 160


def main():
    bad = []
    for path in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        if rel.startswith("docs/") or "/node_modules/" in rel:
            continue
        text = open(path, encoding="utf-8", errors="replace").read()
        m = META.search(text)
        if not m:
            continue
        desc = unescape(re.sub(r"\s+", " ", m.group(1))).strip()
        if len(desc) > LIMIT:
            bad.append((len(desc), rel))
    if bad:
        for n, rel in sorted(bad, reverse=True):
            print(f"{n}\t{rel}")
        print(f"{len(bad)} meta descriptions over {LIMIT}")
        return 1
    print(f"ok, no meta description over {LIMIT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
