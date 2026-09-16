# Bay Area Sports Blog, search performance opportunity report

**16 September 2026. HEAD `f75b6ea`. 256 pages, 223 articles.**

## The honest headline

**The HIGH CONFIDENCE section of this report is empty, and it will stay empty until
Search Console access exists.** Every item below sits in MEDIUM or HYPOTHESIS, because
not one click, impression, CTR or average position figure is available to this machine.

Nothing in here should be read as "Google says". Where a number appears it was measured
on our own site, and it says so.

Two things stand between us and the HIGH section, both of them a couple of clicks. They
are in the access section at the bottom.

---

## What is already built and waiting

| Tool | What it does the moment access exists |
|---|---|
| `tools/gsc_pull.py --probe` | says exactly which step is still outstanding, in one line |
| `tools/gsc_pull.py` | pulls totals, pages, queries, page and query pairs, daily series and device split across 7d, 28d, 90d and the previous 28d for comparison, plus sitemap status and URL inspection for the three pilot pages |
| `tools/baseline_check.py` | compares the site against the frozen 16 September baseline and fails on a regression |
| `tools/vitals_lab.py` | Core Web Vitals without a Google key, as a regression tripwire |
| `tools/schema_validate.py` | structured data, 0 errors required |
| `tools/cannibal_check.py` | the intent split between any two pages |

The puller writes one CSV per cut into `data/gsc/`, so the first real analysis is a
reading job, not a building job.

---

# HIGH CONFIDENCE

*Evidence directly supported by Search Console data.*

**Empty.** No Search Console data exists on this machine. Anything placed here without it
would be a guess wearing a suit.

---

# MEDIUM CONFIDENCE

*Strong site evidence, incomplete Google data. Every one of these is a defect I can see
in our own markup or link graph. What I cannot see is whether the page gets any traffic,
which is exactly what decides priority.*

## M1. Two of the three brand new pages have titles that will be truncated

| | |
|---|---|
| **URLs** | `/articles/bay-bridge-series-giants-athletics-history.html` (76 chars), `/articles/chase-center-guide-warriors-arena.html` (72 chars) |
| **Topic** | bay bridge series history, chase center guide |
| **Clicks / impressions / CTR / position** | unknown, needs GSC |
| **Site evidence** | Titles run past the roughly 70 character point where most result layouts cut. "The Bay Bridge Series: What Is Left of It, and What the Record Actually Says" will very likely render as "The Bay Bridge Series: What Is Left of It, and What the Reco..." |
| **Recommended action** | Shorten both to put the query bearing words inside the first 60 characters. Draft: "The Bay Bridge Series: The Complete Giants and A's Record" (56) and "Chase Center Guide: Getting There, Parking, Bag Rules" (52). |
| **Why it may help** | The part of the title that a searcher scans is the part that survives truncation, and on both pages the distinctive words currently sit past the cut. |
| **Risk** | Low. Both pages are two days old with no ranking history to protect. This is the cheapest moment to change them and the cost rises every week. |
| **Approval needed** | Yes, these are title changes. |

## M2. Twenty four descriptions run past the snippet limit

| | |
|---|---|
| **URLs** | 24 articles over 165 characters. Worst: the Bay Bridge page (216), `giants-bryce-eldridge-back-buddy-kennedy-dfa` (205), `athletics-bluejays-6-5-walkoff-mcneil-bolte` (199) |
| **Clicks / impressions / CTR / position** | unknown, needs GSC |
| **Site evidence** | Measured on our own pages. Google rewrites descriptions often enough that this is a soft problem, but where it does use ours the tail is lost. |
| **Recommended action** | **Do nothing yet.** Fix only the ones Search Console shows getting impressions. Rewriting 24 descriptions blind is exactly the mass metadata edit you ruled out. |
| **Why it may help** | A complete sentence in the snippet reads better than a cut one. |
| **Risk** | Low individually, wasted effort in bulk. |
| **Approval needed** | Not yet, there is nothing to approve until the data says which ones matter. |

## M3. The most linked page on the site is one of its thinnest

| | |
|---|---|
| **URL** | `/articles/49ers-2026-schedule-season-hub.html` |
| **Topic** | 49ers schedule 2026, navigational and recurring |
| **Clicks / impressions / CTR / position** | unknown, needs GSC |
| **Site evidence** | 23 in body inbound links, the highest on the site, against 688 words. Every 49ers piece points at it. The equivalent Warriors page we just built carries a full generated table. |
| **Recommended action** | Rebuild it on the same generator pattern as the Warriors hub: full schedule, results filling in as they happen, times, and the shape of the season. Same URL, no redirect. |
| **Why it may help** | It already has the internal authority. It currently cannot satisfy the query it attracts, which is the definition of a page ranking for something it only partially answers. |
| **Risk** | Medium. It is an established URL and the only one on this list with something to lose, so it should be measured before and after. The ESPN NFL endpoint is the same one already in use. |
| **Approval needed** | Yes. |

## M4. Three dead previews still sit in the archive

| | |
|---|---|
| **URLs** | `stanford-hawaii-week-zero-opener-preview` (1,330 words, game played 29 August), `49ers-rams-week-1-preview-melbourne-what-to-watch` (game played 11 September), `giants-rockies-preview-robbie-ray-bryce-eldridge-july-10` |
| **Topic** | each game preview |
| **Clicks / impressions / CTR / position** | unknown, needs GSC |
| **Site evidence** | A preview goes to zero use the moment the whistle blows unless it gets a result section. The Stanford one is our single longest college page. |
| **Recommended action** | Add a result section at the top of each, same URL, and update `dateModified` while leaving `datePublished` alone. |
| **Why it may help** | The traffic that still arrives finds an answer instead of a prediction about a game that has already been played. |
| **Risk** | Low. No URL change, no date fakery. |
| **Approval needed** | Yes, these are content edits to existing articles. |

## M5. The A's depth chart is materially wrong

| | |
|---|---|
| **URL** | `/articles/athletics-2026-roster-depth-chart.html` |
| **Topic** | athletics depth chart, a permanent query |
| **Clicks / impressions / CTR / position** | unknown, needs GSC |
| **Site evidence** | Kurtz, Rooker and Jacob Wilson have all been on the 60 day injured list since 31 July, 8 June and 16 August. The chart does not say so. 10 in body inbound links. |
| **Recommended action** | Update the chart. This is a correctness problem before it is an SEO one. |
| **Why it may help** | Accuracy. A depth chart that is wrong about three of the best players is worse than no depth chart. |
| **Risk** | Low. |
| **Approval needed** | Yes. |

## M6. Six evergreen pages have almost no internal support

| | |
|---|---|
| **URLs** | `cal-basketball-schedule-2026-27` (1 inbound), `sharks-playoff-history`, `stanford-2026-schedule-game-by-game-acc`, `stanford-axe-trophy-history`, `stanford-hawaii-week-zero-opener-preview`, `giants-rockies-preview-robbie-ray-bryce-eldridge-july-10` (2 each) |
| **Topic** | schedules, rivalry and franchise history |
| **Clicks / impressions / CTR / position** | unknown, needs GSC |
| **Site evidence** | Measured on the link graph. Reference pages with the right shape and nothing pointing at them. |
| **Recommended action** | Wait for the data. If any of these already earns impressions, it is the strongest signal on the site: a page ranking despite weak support, which is your category E and the cheapest win there is. If none does, leave them. |
| **Why it may help** | Internal links are the one ranking factor entirely inside our control. |
| **Risk** | Low, and lower still if it is targeted rather than mechanical. |
| **Approval needed** | Report first, as instructed. |

---

# HYPOTHESES

*Worth testing. Not supported enough to act on.*

## H1. The recap archive may be earning nothing at all

72 of 117 Giants and A's pieces are game recaps. My argument has been that a ten week old
domain cannot win those queries against NBC Sports Bay Area and MLB.com. **That is an
argument, not a measurement.** The first page level pull settles it. If recaps do earn
impressions, the content mix conclusion in the opportunity audit is wrong and should be
rewritten. If they earn nothing, the case for shifting the mix gets its evidence.

**Test:** page level data for 90 days, grouped by whether the slug matches a score pattern.

## H2. Discovery may be the constraint rather than quality

The site was published on 6 July 2026 and the homepage and archive were frozen from
7 August until 15 September, which is most of its life. It is entirely possible that a
large part of the archive has never been crawled properly, in which case the content
questions in the audit are premature and the index coverage report is the only thing that
matters.

**Test:** indexed against discovered but not indexed against crawled but not indexed.

## H3. The three pilot pages are a controlled experiment and should be read as one

Same cohort, same week, three different shapes: unique local reference with a data table,
auto updating navigational hub, static practical guide. Whichever shape performs is the
template for the next batch. Baselines are recorded in `PILOT_TRACKING.md`.

**Test:** the 90 day and six month snapshots, read together rather than individually.

## H4. Our own queries may already point at pages we have not built

Category H in your list, and the one I am most interested in. If Google associates the
site with a topic where we have only recaps and no reference page, that is a far better
signal than anything in the content audit, because it is demand we have already proven we
can attract.

**Test:** queries with impressions where the ranking page is a recap rather than a
reference page.

## H5. Lab vitals are clean, field vitals are unknown

Median lab LCP is 268ms on mobile and CLS is 0.000 across the six pages measured. Real
users on real connections will be slower and the site has no CDN in front of it. The
Cloudflare rollout plan has been sitting approved in principle and unexecuted since
8 August.

**Test:** field data, which needs a PageSpeed Insights key or Search Console.

---

# What I need from you, and it is two clicks

The credential already exists on this machine. Nothing needs to be created, downloaded,
pasted or typed into a terminal.

**Step 1. Enable the API.** Open this and press Enable:

```
https://console.developers.google.com/apis/api/searchconsole.googleapis.com/overview?project=429392135630
```

**Step 2. Grant read only access.** In Search Console, open the bayareasportsblog.com
property, then Settings, Users and permissions, Add user. Paste this address and set the
permission to **Restricted**, which is read only and the minimum that works:

```
tmr-play-publisher@serene-voltage-507909-a8.iam.gserviceaccount.com
```

Then tell me, and I run `python tools/gsc_pull.py`.

**Two things worth knowing before you do it.** That service account already belongs to
another project of yours, so this reuses an identity rather than creating one. If you would
rather Bay Area Sports Blog had its own, say so and I will write the instructions for a
dedicated one instead. And Restricted is genuinely read only: it cannot submit sitemaps,
request indexing or change settings. If you later want me to submit URLs for indexing, that
needs Full, and it is worth deciding that separately rather than granting it now.

**Optional third step, for field Core Web Vitals.** PageSpeed Insights and the Chrome UX
Report both refuse anonymous requests from here. A free API key in the same project, saved
to a file rather than pasted, unlocks real user LCP and CLS. Worth doing, not urgent.

---

# What happens on the first pull

1. `tools/gsc_pull.py` writes every cut into `data/gsc/`.
2. HIGH CONFIDENCE gets populated and most of what is currently in MEDIUM either gets promoted with numbers attached or dropped.
3. H1 and H2 get settled, which decides whether the next phase is content or crawl.
4. `PILOT_TRACKING.md` gets its first real row.
5. This report gets rewritten with clicks, impressions, CTR and position against every item, and then we decide what to build.

No pages get created before that.
