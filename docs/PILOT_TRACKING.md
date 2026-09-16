# Pilot page tracking

Three evergreen pages shipped on 15 and 16 September 2026. This file is where their
numbers live so they can be judged over months rather than days.

**Do not read anything into the first few weeks.** A new URL on a domain that went live on
6 July 2026 is not going to tell us much before it has been crawled, indexed and given
time to settle. The point of writing the baseline down now is that we will not be able to
reconstruct it later.

---

## Day zero baseline, 16 September 2026

Everything in this table was measured on the deployed site. The Search Console columns are
empty because the credential does not exist yet, not because the numbers are zero.

| | Bay Bridge Series | Warriors schedule hub | Chase Center guide |
|---|---|---|---|
| URL | `/articles/bay-bridge-series-giants-athletics-history.html` | `/articles/warriors-2026-27-schedule-season-hub.html` | `/articles/chase-center-guide-warriors-arena.html` |
| Published | 2026-09-15 | 2026-09-15 | 2026-09-15 |
| Schema | Article | Article | Article |
| HTTP | 200 | 200 | 200 |
| Crawl depth from the homepage | 2 | 2 | 2 |
| Inbound internal links | 8 (5 articles, 3 hubs) | 9 (5 articles, 4 hubs) | 8 (4 articles, 4 hubs) |
| Outbound internal links | 6 | 6 | 6 |
| Words | 1,616 total, 1,303 prose | 1,197 total, 390 prose | 886 |
| In sitemap | yes | yes | yes |
| In news sitemap | rolling 48h window only | rolling 48h window only | rolling 48h window only |
| Lab LCP mobile | 360ms | 240ms | 248ms |
| Lab CLS | 0.000 | 0.000 | 0.000 |
| **Indexed status** | unknown, needs GSC | unknown, needs GSC | unknown, needs GSC |
| **Clicks** | | | |
| **Impressions** | | | |
| **CTR** | | | |
| **Average position** | | | |
| **Top queries** | | | |

## Update dependency

| Page | Source | Cadence | Failure behaviour |
|---|---|---|---|
| Bay Bridge Series | `statsapi.mlb.com` head to head | six games a year, so effectively May and June | feed, then cache, then leave the page alone |
| Warriors hub | `site.api.espn.com` schedule | every publish through the season | same, and a game that is not final never gets a score |
| Chase Center | none, static | review once a year | not applicable |

## What to record, and when

Fill the Search Console rows on the first pull after access exists, and then at 28 days,
90 days and six months from publication. Keep every snapshot, do not overwrite: the shape
of the curve is the finding, not any single number.

Questions each page is being asked to answer:

- **Bay Bridge Series.** Does a genuinely unique local reference page earn impressions on a ten week old domain, and does it pick up the "do the A's still play the Giants" kind of query? This is the clearest test of whether originality beats authority on a small site.
- **Warriors schedule hub.** Does an auto updating navigational page behave differently from a written one? The 49ers equivalent is the most linked page on the site, so this also tests whether that pattern reproduces.
- **Chase Center guide.** Does a practical page with no feed behind it hold up? It is the control against the two data driven pages.

## Known caveats to carry into the analysis

1. The domain is ten weeks old. Attribution of anything to page quality before roughly January 2027 is guesswork.
2. All three shipped within 24 hours of each other, so they share a cohort and cannot be compared against a page published at a different time without saying so.
3. The Warriors hub launches before the season it covers. Its curve should be read against the 21 October opener, not against its publication date.
4. Nothing here has been submitted for indexing by hand, and the news sitemap only carries a rolling 48 hour window, so discovery is through the sitemap, the homepage and the hub cards.
