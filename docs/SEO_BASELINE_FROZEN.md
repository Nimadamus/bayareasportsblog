# Technical-SEO baseline — bayareasportsblog.com

Regenerated 2026-08-08 in the repo. The original lived on the Desktop and was lost; the
Desktop is treated as unreliable storage, so this file is committed to git.

This is not a to-do list. On-site technical SEO is **complete and frozen** — the current
phase is content growth. These numbers exist so that a regression is detectable.

---

## Baseline (all four gates, 2026-08-08, after the Bay Area history cluster)

| Metric | Value |
|---|---|
| pages | 159 |
| articles | 132 |
| hubs | 27 |
| indexable | 159 |
| sitemap URLs | 158 |
| news sitemap URLs | 35 (rolling 48h) |
| orphans | 0 |
| near-orphans (≤2 inbound) | 0 |
| broken internal links | 0 |
| duplicate titles / descriptions | 0 / 0 |
| multi-H1 / no-H1 | 0 / 0 |
| canonical mismatches | 0 |
| articles missing Article schema | 0 |
| pages missing BreadcrumbList | 0 |
| invalid JSON-LD | 0 |
| noindexed pages | 0 |
| images: no alt / weak alt / no dims / lazy-first | 0 / 0 / 0 / 0 |
| titles >70ch / desc <70ch / desc >165ch | 0 / 0 / 0 |
| meta gate | 159/159, 0 violations |
| thumbnail gate | 405/405 |
| card derivative gate | 132 cards, 0 incomplete |
| sitemap audit | 0 failures |

**Live Core Web Vitals** (Lighthouse 12 desktop medians, last measured pre-cluster):
LCP 2.6 s, FCP 1.9 s, CLS 0.022, TBT 0. Homepage transfer ~496 KiB.

**Prior baseline for comparison:** 130 pages / 127 sitemap URLs at commit `511c016`
(the original freeze), then 155 pages / 154 sitemap URLs at `c278981` (after the five
team clusters).

---

## How to re-verify

```bash
cd C:/Users/Nima/bayareasportsblog

# feeds first - run after any content change
python _gen_sitemap.py
python _gen_news_sitemap.py        # rolling 48h window
python _gen_search_index.py
python _gen_feed.py

# the gates - ALL must pass before commit
python tools/thumb_gate.py --site        # card images, exits 2 on fail
python tools/card_derivatives.py --check # 400/600/800 jpg+webp + full webp, exits 2
python _meta_template.py --gate          # metadata standard, exits 2 on fail
python _sitemap_audit.py                 # sitemap validity, exits 2 on fail
python _seo_audit.py                     # full crawl + link graph
```

`python tools/card_derivatives.py` (no flag) fills any gap it finds. This used to be an
undocumented manual step that silently 404'd when forgotten.

---

## Deliberate non-changes — do not "fix" these

- **25 distinct visible tag strings are editorial section names**, not sloppiness.
  Schema `articleSection` is mapped from them. The visible tags stay.
- **Four articles keep 0 in-body inbound links** because nothing on the site genuinely
  mentions their subject, and a link would be invented:
  `athletics-tigers-melton-shellacking-july-8`,
  `athletics-tigers-sweep-valdez-july-9`,
  `athletics-white-sox-preview-jacob-lopez-july-10`,
  `nfl-blackballed-colin-kaepernick-kneeling-anthem`.
- **`betting.html`** is permanently excluded from the sitemap — that desk lives on TMR
  and BetLegend, not this blog. It stays live, footer-linked, and is never noindexed.
- **`cal.html` / `stanford.html`** are back in the sitemap as of the college cluster.
- **The homepage H1 is off-screen by design**, pending a decision. A visible one needs a
  `.lm-body h1` rule and Nima's sign-off. The homepage is otherwise locked: no
  structural, nav, copy or H1 changes without explicit approval.
- **Author is `Organization`** by choice, not omission.
- **Never noindex anything.** Standing rule.

---

## Known traps

- **`_webp.py` has double-wrapped `<picture>` tags** across 89 tracked files once. If you
  run it, immediately check `grep -c '<picture><picture>'` and
  `git checkout -- '*.html'` if it happened.
- **`_srcset.py` skips images that already carry `srcset`** — which the article template
  always does. That is why `tools/card_derivatives.py` exists.
- **New pages publish as near-orphans.** Always re-run `_seo_audit.py` after a cluster
  and link the new page from a sibling where the reference is genuine.
- **C: drive null-byte corruption** is a live hazard on this machine. Every writer script
  checks for NULL bytes and U+FFFD after writing. Keep that pattern.
- **Windows/PIL:** close image handles before `os.replace`, or writes fail with
  `WinError 5`.
- **`/assets/` filenames are not content-hashed.** Relevant to any future edge caching —
  see `docs/CLOUDFLARE_ROLLOUT_PLAN.md`.

---

## External blockers — tracked, not reasons to edit the site

1. **Search Console** — no GSC credential exists on this machine. Blocks four analyses:
   pages ranking 5–20, high-impression/low-CTR, query cannibalisation, index-coverage
   exclusions. The property is otherwise ready: verification file returns 200 and both
   sitemaps are declared in `robots.txt`.
2. **Cloudflare** — plan rebuilt at `docs/CLOUDFLARE_ROLLOUT_PLAN.md`. Needs Nima's go.
   The Namecheap MX priorities that previously blocked it have now been re-resolved live
   and are recorded in that file.
