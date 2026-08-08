# Bay Area Sports Blog — SEO / content continuation handoff

**Written 2026-08-08. Supersedes `Desktop\BAYAREA_SPORTS_BLOG_SEO_CONTENT_HANDOFF.md`
(HEAD `c278981`, 155 pages).** This copy lives in the repo because the Desktop has
already lost four documents from this workstream once; a mirror is kept on the Desktop
for convenience but git is the source of truth.

Everything below is verified state. Re-verify commands are in §8.

---

## 1. Current state

```
repo:    C:\Users\Nima\bayareasportsblog   (GitHub: Nimadamus/bayareasportsblog)
branch:  master        HEAD: ac35832       working tree: clean (0 dirty)
origin/master...master: in sync
live:    https://bayareasportsblog.com     (GitHub Pages, custom domain, HTTPS enforced)
```

| Metric | Value |
|---|---|
| pages | 165 |
| articles | 138 |
| hubs | 27 |
| sitemap URLs | 164 |
| orphans / near-orphans | 0 / 0 |
| broken internal links | 0 |
| duplicate titles / descriptions | 0 / 0 |
| canonical mismatches | 0 |
| invalid JSON-LD / noindexed | 0 / 0 |
| image defects (alt, dims, lazy-first) | 0 |
| articles with 0 in-body inbound | 4 (all deliberate — see §7) |
| meta gate | 165/165, 0 violations |
| thumbnail gate | 407/407 |
| card derivatives | 138 cards, 0 incomplete |
| social meta gate | 0 needing fixes, 0 problems |

**Status: technical/structural SEO is CLEAN and Nima has explicitly ended audit work.**
Growth now comes from timely coverage, topical authority, internal-link compounding,
evergreen refreshes and backlinks. Run the gate suite *after* publishing, not as a source
of work.

---

## 2. What changed since the previous handoff (`c278981` → `ac35832`)

### `f2d3265` — Bay Area history / evergreen cluster
Four reference pages, not more columns: `bay-area-championships-complete-list-by-team`
(943w), `oakland-coliseum-history-what-happens-to-it-now` (912w),
`bay-area-franchise-relocations-teams-that-left` (1,073w),
`candlestick-park-history-wind-the-catch-demolition` (1,007w). The two thin flashbacks
were **expanded rather than replaced**: `flashback-the-catch-1982` 402w → 950w,
`flashback-klay-37-point-quarter` 392w → 940w.

Also: `tools/card_derivatives.py` (new) — generates the 400/600/800 jpg+webp plus the
full-size webp the article template references. This had been an undocumented manual step
that 404'd silently when forgotten; `_srcset.py` cannot do it because it skips images
that already carry `srcset`. And `_college_cluster.render_body` no longer wraps
block-level markup in `<p>`, so reference tables are valid HTML (`.reftable` CSS added).

### `80fc161` — Sharks cluster, built from one article
`sharks-2026-27-schedule-season-hub` (839w), `sharks-2026-27-roster-depth-chart`
(1,022w), `macklin-celebrini-sharks-records-contract` (730w),
`san-jose-sharks-history-no-stanley-cup` (914w).

### `8b20787` — social-meta cleanup + Oracle Arena
**50 pages carried two `og:image` tags** — the page's own card, then the generic
`welcome-to-bay-area-sports-blog.jpg` — so which image a crawler used was undefined.
15 pages had the same on `twitter:image`; 35 had exactly one `twitter:image` and it was
the generic card. `tools/social_meta_gate.py` (new) fixed all 50 and now gates against
regression.

`oracle-arena-roaracle-history-oakland-warriors` (948w) closed the last venue gap.
`history.html` had a chapter plate pointing at `timeline.html#venues` instead of an
article, and the timeline's three venue cards were prose dead ends; all now point at real
articles. No public URLs changed and no redirects were added.

### `ac35832` — Stanford opener mini-cluster
`stanford-hawaii-week-zero-opener-preview` **expanded in place, 536w → 1,255w, same
URL** — it had omitted that Hawaii won this fixture 23-20 last August on a walk-off field
goal. `stanford-2026-schedule-game-by-game-acc` (822w, new). Two factual corrections on
the Big Game page: it said "127 meetings, Stanford 65-51-11"; the 2025 game was the
**128th** and the series is **66-51-11**. Both that page and the Axe page now state
Stanford holds the Axe.

`COLLEGE_GAMEDAY_WORKFLOW.md` (new) — the Cal/Stanford loop and the postgame gate.

---

## 3. All seven clusters now have a foundation

Cal/Stanford (10), 49ers (5), Warriors (4), Giants (4), Athletics (4), Bay Area history
(5 + 2 expansions), Sharks (4). **The next work is event-driven, not another
foundation.**

---

## 4. Next scheduled publishing triggers

`CONTENT_CALENDAR.md` is the publishing memory and holds the full table. In date order:

| Date | What | Gate |
|---|---|---|
| **29 Aug** | Stanford vs Hawaii, Week 0, 4pm PT, ACC Network | **Preview is LIVE. Reaction only after the result is confirmed from a live source** — `COLLEGE_GAMEDAY_WORKFLOW.md` |
| **4 Sep** | Miami at Stanford — six-day turnaround | preview 2–3 Sep |
| **5 Sep** | Cal vs UCLA — Cal's opener | preview ~3 Sep, reaction after |
| **8–9 Sep** | 49ers Week 1 preview | `NFL_WEEKLY_WORKFLOW.md` |
| **10 Sep** | 49ers at Rams, Melbourne | reaction after |
| **late Sep** | Warriors camp; Butler knee status | only on meaningful news |
| **on release** | NBA 2026-27 schedule → Warriors schedule hub | the one missing permanent page |
| **1 Oct** | Sharks opening night vs Florida, SAP Center | preview + reaction |
| **early Oct** | Giants + Athletics season reviews | — |
| **~game five (Oct)** | **Purdy passes 1,500 attempts and qualifies for the career passer-rating record** | **biggest single traffic event of the season; page already built** |
| **10 Oct** | Stanford at Notre Dame | marquee college game |
| **21 Nov** | **Big Game, Berkeley, 129th meeting** | package + refresh the Big Game and Axe evergreens with the result and new series record |
| **quarterly** | Las Vegas construction milestones | update the A's timeline page |
| **when it closes** | Oak View Group buying Oakland Arena | update the Oracle Arena page |
| **spring 2028** | **Opening Day in Las Vegas** | the biggest scheduled story this site owns |

---

## 5. Strongest opportunities

**Traffic:** the Purdy record page in October — known date, national story, page built to
catch it. Runners-up: the five depth-chart pages, which carry recurring high-intent
queries with no seasonal decay.

**Backlinks / citation:** `bay-area-championships-complete-list-by-team` and the venue
set (`oakland-coliseum-history-…`, `candlestick-park-history-…`,
`oracle-arena-roaracle-history-…`) — reference pages nobody else has consolidated. The
compounding one is `athletics-oakland-sacramento-las-vegas-timeline`, which every Vegas
construction story to 2028 needs. Also `big-game-cal-stanford-rivalry-history`.

**Unique local angle:** the A's cluster — national outlets treat the move as a business
story; this site treats it as a civic theft with receipts.

---

## 6. Build method (unchanged)

All clusters use one renderer. `_<cluster>_cluster.py` does
`import _college_cluster as CC` and calls `CC.build(article_dict)`, which gives identical
markup, NewsArticle schema, `mainEntityOfPage`, `articleSection`, breadcrumbs, og/twitter,
the "More coverage" line and the related block for free.

1. Article dict keys: `slug, section, tag, hub, title (<=70 chars), h1, dek,
   desc (70-165 chars), date, card=(palette,name,subhead), body=[paragraphs with
   {placeholder} links], links={placeholder:(href,text)}, related=[(href,kicker,title)]`.
   A body item that starts with a block-level tag (`<div class="reftable">`, `<table>`,
   `<ul>`) is emitted unwrapped, so reference tables are valid.
2. `python _<cluster>_cluster.py --check` prints word count, links, title/desc lengths.
   **Reject anything under ~500 words** and expand before publishing.
3. `python _<cluster>_cluster.py` writes the HTML and generates the card.
4. `python tools/card_derivatives.py` fills the derivatives. No longer manual.
5. Add a hub block (see the `<!-- ... nav -->` comments in the team hubs).
6. Regenerate feeds, run the gates, commit, push.

Palettes: `giants, 49ers, warriors, athletics, sharks, raiders, cal, stanford, bay`.

---

## 7. Editorial and SEO rules (non-negotiable)

1. **Never write a game reaction before the game.** Confirm the result from a live
   source first. If it cannot be confirmed, publish nothing.
2. **Research before writing.** Never invent a score, date, contract or statistic.
3. **One query, one page.** Check the archive; update rather than compete. Both thin
   flashbacks and the Stanford opener preview were expanded in place, keeping their URLs.
4. **No thin pages.** Under ~500 words means it should have been an update.
5. **Do not manufacture filler to fill idle time.** Standing instruction from Nima.
6. **Never noindex anything.**
7. **Never cite sources in article copy** — house style.
8. **Voice:** homer Bay Area fan, frustrated, especially about the Giants.
9. **Images are original editorial cards** from `cardgen.py`, never stock photos.
10. **Every article links up to its hub** and to at least one permanent page.
11. **The homepage (`index.html`) is locked** — no structural, nav, copy or H1 changes
    without explicit approval.
12. **`betting.html`** is permanently excluded from the sitemap; it stays live and is
    never noindexed.

**The four articles that deliberately keep 0 in-body inbound links** (nothing on the site
mentions their subject; a link would be invented): `athletics-tigers-melton-shellacking-july-8`,
`athletics-tigers-sweep-valdez-july-9`, `athletics-white-sox-preview-jacob-lopez-july-10`,
`nfl-blackballed-colin-kaepernick-kneeling-anthem`.

---

## 8. Validation commands

```bash
cd C:/Users/Nima/bayareasportsblog

# feeds - after any content change
python _gen_sitemap.py
python _gen_news_sitemap.py        # rolling 48h window
python _gen_search_index.py
python _gen_feed.py

# the gates - ALL must pass before commit
python tools/thumb_gate.py --site
python tools/card_derivatives.py --check
python tools/social_meta_gate.py --check
python _meta_template.py --gate
python _sitemap_audit.py
python _seo_audit.py               # check near-orphans and 0-in-body-inbound
```

---

## 9. Known traps

- **`_webp.py` has double-wrapped `<picture>` tags** across 89 files once. If you run it,
  check `grep -c '<picture><picture>'` and `git checkout -- '*.html'` if it happened.
- **`_srcset.py` skips images that already carry `srcset`** — which the article template
  always does. That is why `tools/card_derivatives.py` exists.
- **New pages publish as near-orphans**, and a page linked only from hubs still counts as
  0 in-body inbound. Re-run `_seo_audit.py` and add a genuine in-body link from a sibling.
- **C: drive null-byte corruption** is a live hazard. Every writer script checks for NULL
  bytes and U+FFFD after writing. Keep that pattern.
- **Windows/PIL:** close image handles before `os.replace`, or writes fail with
  `WinError 5`.
- **`/assets/` filenames are not content-hashed** — relevant to any edge caching.

---

## 10. External blockers (not reasons to edit the site)

- **Search Console** — no credential on this machine. Blocks four analyses: pages ranking
  5–20, high-impression/low-CTR, query cannibalisation, index-coverage exclusions. The
  property is otherwise ready (verification file 200, both sitemaps in robots.txt).
- **Cloudflare** — plan rebuilt at `docs/CLOUDFLARE_ROLLOUT_PLAN.md` with DNS re-resolved
  live rather than recalled. **The MX blocker is resolved**: priorities are 10/10/10/15/20
  and the SPF record is recorded. Brotli measured at 18.8% over gzip. **Needs Nima's
  explicit go — it is a nameserver change that affects email.**

---

## 11. Companion documents

| File | What | Status |
|---|---|---|
| `docs/SEO_CONTENT_HANDOFF.md` | this file | **present, in git** |
| `CONTENT_CALENDAR.md` | **the publishing memory — read first** | present, in git |
| `NFL_WEEKLY_WORKFLOW.md` | the recurring 49ers loop | present, in git |
| `COLLEGE_GAMEDAY_WORKFLOW.md` | Cal/Stanford loop + the 29 Aug postgame gate | present, in git |
| `docs/CLOUDFLARE_ROLLOUT_PLAN.md` | CDN migration, not started | present, in git |
| `docs/SEO_BASELINE_FROZEN.md` | technical-SEO baseline | present, in git |
| `docs/INTERNAL_LINK_AND_HUB_REPORT.md` | link-graph record, GSC checklist | present, in git |

The four `Desktop\BAYAREA_*` documents referenced by the previous handoff were lost and
have been rebuilt in `docs/`. **Treat the Desktop as unreliable storage; write future
reports into the repo so git covers them.**

---

## 12. What happens next

Nothing publishes until an event fires. The next one is **Stanford vs Hawaii on 29
August**, and the only work is the postgame reaction — gated on confirming the result.
Do not manufacture pages to fill the gap.
