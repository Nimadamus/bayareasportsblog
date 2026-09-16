# Technical baseline, frozen 16 September 2026

The machine readable copy is `baseline.json` at the repo root. This file explains it.

Every number here was measured on the day it was frozen, at HEAD `f75b6ea`, against the
deployed site and not against the working tree.

| Measure | Frozen value | Rule |
|---|---|---|
| Pages | 256 | may grow, failing if it shrinks |
| Articles | 223 | may grow |
| Hubs | 33 | may grow |
| Sitemap URLs | 256 | may grow |
| URLs crawled from the homepage | 257 | may grow |
| Articles reached by crawl | 223 | may grow, and must equal the article count |
| Non 200 responses | 0 | must stay 0 |
| Orphans | 0 | must stay 0 |
| Near orphans, 2 or fewer inbound | 0 | must stay 0 |
| Broken internal links | 0 | must stay 0 |
| Duplicate titles | 0 | must stay 0 |
| Duplicate descriptions | 0 | must stay 0 |
| Noindexed pages | 0 | must stay 0 |
| Invalid JSON-LD | 0 | must stay 0 |
| Schema errors | 0 | must stay 0 |
| Schema warnings | 69 | pre existing on older articles, tracked not gated |
| Schema types | 220 NewsArticle, 3 Article | changes only through `schema_types.json` |
| Voice gate articles | 223 | |
| Voice gate median | 84 | |
| Voice gate under 70 | 0 | must stay 0 |

Lab Core Web Vitals on the same day, measured with `tools/vitals_lab.py`, a real Chromium
render rather than a Google API:

| | Median LCP | Median CLS | Median transfer |
|---|---|---|---|
| Mobile, 390px | 268ms | 0.000 | 38KB |
| Desktop, 1440px | 130ms | 0.000 | 20KB |

Nothing was over the 2,500ms LCP threshold or the 0.1 CLS threshold. The heaviest page is
the homepage at 281KB on mobile. **These are lab numbers on a fast machine and a fast
connection.** They are a regression tripwire, not a claim about what a real visitor sees.
Field data needs either Search Console or a PageSpeed Insights key and the site has
neither yet.

## How to use it

```
python tools/baseline_check.py          # compare, non zero exit on a regression
python tools/baseline_check.py --live   # also crawl the deployed site
python tools/baseline_check.py --freeze # re-freeze, only after a deliberate change
```

Run the comparison after any SEO change. A count that must stay at zero and does not is a
failure. A count allowed to grow that shrinks is also a failure, because that is how pages
quietly fall out of the crawl.

Re-freeze only when the new numbers are the intended result of work that was approved, and
say so in the commit that does it.
