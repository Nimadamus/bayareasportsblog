# SEO staging batch, 20 Oct 2026

Branch `seo-staging-20261020`. Nothing here is on production until it is merged to master
(GitHub Pages builds from master only).

## Baseline (Search Console, URL prefix property, pulled 20 Oct 2026)

| Window (ends 17 Oct) | Clicks | Impressions | CTR | Avg position |
|---|---|---|---|---|
| Last 28 days | 24 | 2,628 | 0.91% | 14.2 |
| Previous 28 days | 8 | 1,160 | 0.69% | 19.6 |
| Last 90 days | 39 | 4,787 | 0.81% | 18.0 |

Index status, URL Inspection API on all 311 sitemap URLs:

| Coverage state | URLs |
|---|---|
| Submitted and indexed | 279 |
| Crawled, currently not indexed | 19 |
| Discovered, currently not indexed | 9 |
| Unknown to Google | 3 |
| API error (retry) | 1 |

Read: the 9 "discovered" URLs are all news published 4 to 20 Oct. That is crawl lag on a
low authority site, not a technical fault: every one returns 200, self canonical, no
noindex, in sitemap.xml and news-sitemap.xml. The fix is internal links from pages Google
already crawls often, not markup. The 19 "crawled, not indexed" are mostly dated July
and August game recaps plus three history pages that overlap stronger hubs.

Evergreen pages carried about 80% of 28 day impressions; posts since 15 Sep carried 524 of
2,759. 132 of 261 articles had zero impressions in 28 days.

## Fact check before editing

Purdy career passer rating, ESPN career feed (the same feed the page reads), read 20 Oct:
1,524 attempts, 1,038 completions, 13,145 yards, 98 TD, 39 INT, rating 105.5 (computed
105.55). He crossed 1,500 attempts on 19 Oct vs Washington (six yard completion to
McCaffrey), entering at 105.4 on 1,495. Prior qualified leader Lamar Jackson, 102.7.
The live recap said 105.6 (one wire report's figure); staged as 105.5 to match the feed.

## Changes in this batch

1. `_gen_purdy_stats.py` + Purdy page: record copy rewritten now that he qualifies (was
   "through Week 3 Jackson 102.4, waiting on volume"). Title, H1, description updated.
   The generator runs three times a day from master, so the fix must be in the generator
   or the daily job reverts it.
2. Record chase column (Aug): dated update line that he got there, dateModified 20 Oct.
   Kept as its own URL: it is a dated opinion column, already points to the stats page,
   and no redirect is warranted.
3. Recap column: 105.6 corrected to 105.5 on 1,524 attempts.
4. CTR titles, evidence backed only:
   - `robb-nen.html`: "Robb Nen: Bay Area Hall of Fame | ..." to "Robb Nen Career: 206 Giants
     Saves and the 2002 World Series". Query "robb nen" 32 impressions, position 10.5, 0
     clicks. Persisted through a new optional `seo_title` field in `_hof/robb-nen.json`.
   - `warriors.html`: "Warriors | Bay Area Sports Blog" to "Warriors Blog: Golden State
     Warriors News, Takes and Analysis". Query "warriors blog" 22 impressions, position 8.4,
     0 clicks. Persisted in `_seo_heads.py`.
5. Contextual links from the 49ers schedule page (indexed) to six stuck news URLs:
   Seattle win, Judon cut, Greenlaw suspension, Bosa ruled out, Jennings and Buckner
   trade columns. Purdy stats page links to the Washington recap.
6. Regenerated `assets/search-index.json` and `sitemap.xml` (lastmod).

Deliberately not changed: the 73-9 page (title already answers the query exactly; zero
clicks is the answer box), injury reports (a ranking problem at positions 25 to 58, not
CTR), and the hall of fame generator output (it is not idempotent; regenerating rewrote 10
enriched pages, so Nen was edited in place).

## Gates, staging vs master

| Gate | master | staging |
|---|---|---|
| `_dashscan.py` published html/xml hits | 1 (daily/2026-09-07.html) | same |
| `tools/social_meta_gate.py` | PASS | PASS |
| `_meta_template.py --gate` FAIL lines | 41 | 41 |
| `_sitemap_audit.py` | 2 missing | same 2 |
| `_seo_audit.py` broken links / dup titles / desc >165 | 0 / 1 / 26 | 0 / 1 / 26 |
| `tools/schema_validate.py` warnings | 2 | 2 |
| voice gate, recap column | 94 | 94 |

## Redirect candidates (draft only, nothing implemented)

GitHub Pages cannot send a 301; the only option is a stub page with meta refresh plus
canonical, which Google treats as a soft redirect. Recommend none this week. Candidates to
revisit once the URLs below have 28 days of data after the linking change:

| From | To | Evidence | Risk |
|---|---|---|---|
| articles/warriors-championship-history.html | history.html or dynasties.html | crawled, not indexed | low, 0 impressions |
| articles/bay-area-sports-history.html | history.html | crawled, not indexed | low |
| articles/giants-dynasty-even-year-magic.html | dynasties.html | crawled, not indexed | low |

Backlinks were not audited (no link data source is connected); check before any merge.

## Approvals needed

1. Merge `seo-staging-20261020` to master (production deploy). The recap figure fix and
   Purdy page are time sensitive this week.
2. Any redirect or merge of the three history URLs above: not requested now.
3. Cloudflare and nameservers: untouched, still waiting on a separate go.
