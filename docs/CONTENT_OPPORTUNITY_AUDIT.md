# Content opportunity audit

**Written 15 September 2026, HEAD `13a870a`, against the 220 articles on disk.**
Nothing here has been built. This is the report that comes before the work.

Two honest limits up front. There is no Search Console access from this machine, so
nothing below is ranked by impressions, clicks or position, and no keyword volume figure
appears anywhere in it. Demand is argued from the shape of the query and from what the
archive already proves we can write. Everything factual about our own content was measured
this session with `inventory.py` and `gaps.py`, both committed next to this file.

---

## A. What we cover heavily, and what we barely cover

| Section | Articles | Recaps | Evergreen shaped | Median words | Newest piece |
|---|---|---|---|---|---|
| Giants | 81 | 40 | 7 | 957 | 15 Sep |
| 49ers | 53 | 3 | 8 | 860 | 14 Sep |
| Athletics | 36 | 32 | 4 | 784 | 15 Sep |
| Warriors | 14 | 5 | 7 | 922 | **25 Aug** |
| Bay Area | 11 | 1 | 4 | 705 | 8 Aug |
| Sharks | 7 | 2 | 6 | 981 | **18 Aug** |
| Bay Area Sports | 5 | 0 | 2 | 1,050 | 8 Aug |
| Stanford | 4 | 0 | 2 | 895 | 8 Aug |
| Cal | 3 | 0 | 2 | 1,089 | 18 Aug |
| Flashbacks | 3 | 0 | 0 | 852 | 7 Jul |
| NFL (Raiders) | 3 | 3 | 0 | 1,165 | 13 Sep |

Read that table as a bet. **53 percent of the archive is Giants and Athletics baseball, and
72 of those 117 pieces are game recaps.** Recaps are the hardest thing a ten week old
domain can rank for: NBC Sports Bay Area, The Athletic, MLB.com and the AP all publish the
same game inside the hour, with wire photos and a decade of authority. We are not going to
win "giants padres score" and we should stop expecting to.

The inverse is the opportunity. **Warriors and Sharks have the highest evergreen ratio on
the site and the fewest articles.** The Sharks section is seven pieces, six of them
reference shaped, median 981 words, and it includes the two best structured pages we own.
Both sections have been dormant since late August while their seasons are about to start:
Sharks preseason opens 20 September and the Warriors open 4 October. That is a coverage
gap with a date on it.

The Raiders sit in a section called NFL with three recaps and no reference page at all.

---

## B. Existing articles that should become the resource, not stay a column

These already carry the right intent and already collect internal links. They are short.
Deepening a page that other pages already point at is worth more than a new URL, and it
costs no crawl budget.

| Page | Words | In body inbound | Why it is the best candidate |
|---|---|---|---|
| `49ers-2026-schedule-season-hub` | 688 | **23** | The most linked page on the whole site and one of the thinnest. Every 49ers piece points here. It should carry the full schedule with results filled in as they happen, opponents, kickoff times and TV, not 688 words. |
| `giants-2026-where-the-rebuild-actually-stands` | 654 | 14 | Written 8 August. The answer has changed: 63 and 89, eliminated, Eldridge at .272 with 17 homers at 21. |
| `49ers-2026-season-preview-roster-schedule-questions` | 667 | 13 | Preview framing decays weekly. Same URL, reframe as the season tracker. |
| `sutter-health-park-mlb-guide-dimensions-capacity` | 606 | 11 | A venue question with a two season shelf life and almost no competition. Dimensions, capacity, heat, shade, parking, what the A's did to it. |
| `giants-2026-roster-depth-chart` | 633 | 10 | Depth chart is a permanent query. Ours is a paragraph count short of useful. |
| `athletics-2026-roster-depth-chart` | 621 | 10 | Same, and materially wrong now: Kurtz, Rooker and Jacob Wilson have all been on the 60 day since. |
| `bay-area-championships-complete-list-by-team` | 1,044 | 9 | Closest thing we have to a linkable reference. Needs a table per franchise and a total. |
| `brock-purdy-career-passer-rating-where-he-ranks` | 643 | 6 | Timed: he passes 1,500 attempts around game five in October and qualifies for the career record. The page exists to catch that and is not ready for it. |

---

## C. Query shaped topics that fit this site and do not exist yet

Measured gaps. Each one was checked against every slug on the site before it went on this
list.

**Tier one, permanent demand and we have the material**

1. Warriors 2026-27 schedule and season hub. Every other team we cover has one. The Warriors, our second biggest brand, do not.
2. Athletics 2026 schedule and results hub. Same gap, and the A's hub has 36 articles with nowhere central to land.
3. Giants franchise records and all time leaders. Nothing on the site answers it.
4. 49ers franchise records and all time leaders. Same.
5. Warriors franchise records and all time leaders. Same.

**Tier two, strong local intent, low competition, we have a real angle**

6. Giants and Dodgers: the oldest rivalry in the sport. We have 81 Giants pieces and not one rivalry page.
7. The Bay Bridge Series, and what happens to it now that the A's are in Sacramento and going to Las Vegas. Nobody else can write this the way this site can.
8. Chase Center guide. We own Oracle Park, Sutter Health Park, the Coliseum, Candlestick and Oracle Arena. Chase Center is the hole in the set.
9. Levi's Stadium guide. Mentioned in recaps, never explained.
10. Retired numbers across the Bay Area franchises. One page, five franchises, a table, permanent.

**Tier three, editorial with evergreen legs**

11. 49ers and Seahawks, what is left of it. Rivalry demand spikes twice a season.
12. Greatest Bay Area athlete by franchise. Argument pages earn links when the argument is good, and argument is this site's whole voice.

I am deliberately not proposing a how to watch or TV channel page. It needs re-verification
every few weeks, it goes wrong silently, and being wrong about a broadcast is the kind of
error that costs trust for a page that will never rank against the leagues themselves.

---

## D. Cannibalisation

Almost none, which is a real result. Across 220 articles, only three same section pairs
share a third or more of their title tokens:

| Overlap | Pair |
|---|---|
| 0.40 | `cal-2026-schedule-game-by-game-acc` and `cal-basketball-schedule-2026-27` |
| 0.38 | `49ers-dynasty-team-of-the-decade` and `49ers-still-paying-for-vegas` |
| 0.38 | `macklin-celebrini-sharks-records-contract` and `sharks-rebuild-has-a-pulse-celebrini` |

Only the first is a genuine intent collision, football schedule against basketball
schedule under one team name, and the fix is the title and the H1, not a merge or a
redirect. The other two are a shared subject with different arguments, which is what a blog
is supposed to do.

**The real duplication risk is the 72 game recaps**, which do not collide with each other
by title but all compete for the same kind of query and all lose. That is an editorial mix
question, not a technical one.

---

## E. Internal linking

- **50 of 220 articles have no outbound internal link at all.** The median article has two.
- 23 recaps name a player or a venue we have a page about and link to nothing.
- Three evergreen pages have zero in body inbound links: `49ers-veteran-young-core-mix-recent-drafts-better-2026`, `49ers-landed-melbourne-15-hour-flight-17-hour-time-difference`, `giants-bryce-eldridge-back-buddy-kennedy-dfa`.
- Six more sit at one or two, including `sharks-playoff-history`, `when-were-the-san-jose-sharks-founded` and both college schedule pages.

The pattern: hub pages and navigation carry every article, which is why the crawl is clean,
but the articles do not carry each other. In body links from a recap to the reference page
it mentions are the ones that pass context. That is the cheapest remaining win on the site
and it needs no new pages.

**Taxonomy defect found while measuring this.** Six articles carry an `articleSection` that
contradicts their own subject:

```
athletics-1-0-loss-white-sox-eighth-straight-coming-back-to-earth   section=Bay Area
athletics-sacramento-bay-area-villains                             section=Bay Area
athletics-tigers-melton-shellacking-july-8                         section=Bay Area
athletics-tigers-sweep-valdez-july-9                               section=Bay Area
athletics-white-sox-preview-jacob-lopez-july-10                    section=Bay Area
giants-athletics-all-star-game-2026-arraez-langeliers-webb         section=Bay Area
```

**Correction, 15 September 2026: this was my error and the six are not defects.** Five of
them carry the visible tag `Bay Area Villains`, which is one of the site's named recurring
column series, and the sixth is tagged `Bay Area, All-Star Game` and covers Giants and A's
players on the same night. Their `articleSection` agrees with the tag a reader actually
sees. Changing them would break a deliberate editorial series to satisfy a script that
assumed a slug prefix should equal a section. **Nothing was changed.** The only real
consequence is that the five sit outside the generated A's hub grid while still being
linked from `athletics.html`, which is the correct outcome for a Bay Area series.

---

## F. Missing hubs

1. **Warriors season hub** and **Athletics season hub**. Every other team has one.
2. **A venues hub.** Five venue pages exist with no page tying them together: Oracle Park, Sutter Health Park, the Coliseum, Candlestick, Oracle Arena. A venues index is the natural parent and would give all five an inbound link from one place.
3. **A Raiders home.** Three recaps in a section called NFL with no hub, no reference page and no obvious place for a reader to land.

---

## G. Content that is outdated and worth refreshing at the same URL

Never a new URL for any of these. The page exists, it ranks or it does not, and moving it
throws away whatever it has.

| Page | Problem |
|---|---|
| `stanford-hawaii-week-zero-opener-preview` | 1,330 words previewing a game that was played on 29 August. Previews go to zero the moment the whistle blows unless they get a result section. |
| `49ers-rams-week-1-preview-melbourne-what-to-watch` | Same. The game was played 11 September. |
| `giants-rockies-preview-robbie-ray-bryce-eldridge-july-10` | Same, from July, and it has one inbound link. |
| `cal-2026-schedule-game-by-game-acc`, `stanford-2026-schedule-game-by-game-acc` | Schedule pages with no results in them, three weeks into the season. A schedule page that does not fill in is a schedule page people stop returning to. |
| `athletics-2026-roster-depth-chart` | Kurtz, Rooker and Jacob Wilson are all on the 60 day injured list and the chart does not say so. |
| `giants-2026-where-the-rebuild-actually-stands` | Written on 8 August, before the last six weeks happened. |
| `warriors-*` (14 pages) | Section untouched since 25 August. Season opens 4 October. |
| `sharks-*` (7 pages) | Section untouched since 18 August. Preseason opens 20 September. |

---

## H. Proposed evergreen pages

Ranked. None of these is built. Each says why it earns its URL, and each names the pages
that would link to it on the day it ships, because an evergreen page with no inbound links
is just a file.

### 1. Warriors 2026-27 schedule and season hub
- **Target:** warriors schedule 2026 27, warriors season hub, warriors games this week
- **Intent:** navigational and recurring. Somebody wants to know when the next game is and what happened in the last one.
- **Why us:** the 49ers, Sharks, Cal and Stanford versions already exist and work. This is the one missing piece of a pattern the site already runs, and the season starts 4 October.
- **Links in from:** `warriors.html`, all 14 Warriors articles, `warriors-2026-27-roster-depth-chart`, `warriors-roster-construction-cap-sheet-2026-27`, `nba.html`
- **Type:** evergreen, refreshed through the season

### 2. Athletics 2026 schedule, results and where the season went
- **Target:** athletics schedule, a's results 2026, athletics record
- **Intent:** navigational, plus a large secondary audience asking what has happened to this franchise.
- **Why us:** 36 A's articles with no central landing page. We are also one of very few outlets covering a Sacramento era team as a Bay Area story rather than a curiosity.
- **Links in from:** `athletics.html`, `mlb.html`, all 32 A's recaps, `athletics-oakland-sacramento-las-vegas-timeline`, `sutter-health-park-mlb-guide-dimensions-capacity`
- **Type:** evergreen

### 3. Giants franchise records and all time leaders
- **Target:** giants all time home run leaders, giants franchise records, giants career leaders
- **Intent:** informational, permanent, answered with tables.
- **Why us:** 81 Giants articles give us the internal link supply to make it rank, and the voice to make the list readable instead of a stat dump.
- **Links in from:** `giants.html`, `giants-2026-roster-depth-chart`, `flashback-bumgarner-2014-world-series`, `bay-area-championships-complete-list-by-team`, every Devers and Eldridge piece
- **Type:** evergreen

### 4. 49ers franchise records and all time leaders
- **Target:** 49ers all time passing leaders, 49ers franchise records
- **Intent:** informational, permanent.
- **Why us:** the Purdy passer rating page is already built to catch an October record and has nowhere to send a reader afterwards. This is that page.
- **Links in from:** `49ers.html`, `brock-purdy-career-passer-rating-where-he-ranks`, `49ers-dynasty-team-of-the-decade`, `49ers-2026-schedule-season-hub`
- **Type:** evergreen

### 5. Giants and Dodgers: the oldest rivalry in baseball
- **Target:** giants dodgers rivalry history, giants dodgers all time record
- **Intent:** informational with a strong emotional read, which is exactly this site's register.
- **Why us:** 81 Giants pieces and no rivalry page is the largest single content hole in the biggest section. The all time series record is a fact nobody has to guess at, and the argument around it is ours.
- **Links in from:** `giants.html`, `bay-area-sports-history`, `giants-2026-where-the-rebuild-actually-stands`, every Dodgers recap
- **Type:** evergreen with an editorial spine

### 6. The Bay Bridge Series, and what is left of it
- **Target:** bay bridge series history, giants a's rivalry, do the a's still play the giants
- **Intent:** informational with real current confusion behind it.
- **Why us:** no other outlet has both a Giants section and an A's section written by the same fed up fan. The relocation gives it an ending, which most rivalry pages do not have.
- **Links in from:** `bayarea.html`, `athletics-oakland-sacramento-las-vegas-timeline`, `bay-area-franchise-relocations-teams-that-left`, `oakland-coliseum-history-what-happens-to-it-now`, `giants-athletics-all-star-game-2026-arraez-langeliers-webb`
- **Type:** evergreen

### 7. Chase Center guide
- **Target:** chase center seating, chase center guide, warriors arena
- **Intent:** practical, pre visit.
- **Why us:** it completes a venue set we already own five of, and `oracle-arena-roaracle-history-oakland-warriors` is the natural companion piece, the old barn and the new one.
- **Links in from:** `warriors.html`, `oracle-arena-roaracle-history-oakland-warriors`, `bay-area-sports-history`, the proposed venues hub
- **Type:** evergreen

### 8. Bay Area venues index
- **Target:** bay area stadiums, bay area sports venues
- **Intent:** navigational.
- **Why us:** the five venue pages exist and are orphaned from each other. This is a hub, not an article, and it is the cheapest page on this list.
- **Links in from:** `bayarea.html`, `history.html`, all five venue pages
- **Type:** evergreen hub

### 9. Retired numbers across the Bay Area
- **Target:** giants retired numbers, 49ers retired numbers, warriors retired numbers
- **Intent:** informational, permanent, table shaped.
- **Why us:** one page can serve five franchises and nobody local has built it as a set.
- **Links in from:** `bay-area-championships-complete-list-by-team`, `bay-area-sports-history`, all five team hubs
- **Type:** evergreen

### 10. Levi's Stadium guide
- **Target:** levis stadium guide, levis stadium heat, levis stadium parking
- **Intent:** practical, pre visit, with a genuine local complaint at the centre of it.
- **Why us:** the sun side seating problem is a real thing every Bay Area fan knows and no official page will say out loud.
- **Links in from:** `49ers.html`, `49ers-2026-schedule-season-hub`, the venues hub
- **Type:** evergreen

### 11. 49ers and Seahawks, what is left of it
- **Target:** 49ers seahawks rivalry, 49ers seahawks all time record
- **Intent:** informational, spikes twice a season.
- **Type:** editorial with an evergreen record table

### 12. The best Bay Area athlete, franchise by franchise
- **Target:** greatest 49ers player, greatest giants player, best bay area athletes
- **Intent:** informational and argumentative.
- **Why us:** this is the site's voice with a permanent query attached. It is also the most linkable thing on the list, because people link to arguments they disagree with.
- **Type:** editorial with evergreen structure

---

## The order I would actually do this in

1. **Internal links first.** 50 articles with no outbound link and 23 recaps that name a page we own. No new URLs, no crawl cost, immediate context for everything already published. This is section E and it is the highest ratio of value to risk on the page.
2. **Deepen the eight pages in section B**, starting with `49ers-2026-schedule-season-hub`, which 23 of our own pages already point at.
3. **Refresh section G**, especially the three dead previews and the two college schedule pages, before their seasons end and the traffic is gone for the year.
4. **Then build H1 through H4**, the four pages with dated demand: two season hubs before their seasons start, two records pages before the Purdy record lands in October.
5. Everything below that once there is Search Console data to aim with.

---

## What the three pilot pages taught us, 15 September 2026

Added after building `bay-bridge-series-giants-athletics-history`,
`warriors-2026-27-schedule-season-hub` and `chase-center-guide-warriors-arena`. The next
batch should be planned against this section, not against the assumptions above it.

### 1. Test the data before ranking the idea

The single biggest lesson. This audit ranked Giants and 49ers franchise records first and
second on topical credibility alone. Both died on sourcing: MLB's statsapi team leaders
endpoint returns **season** leaders, not career, so asking for Giants home run leaders
returns the current season's leader rather than the franchise's. No public feed carries
franchise career leaders.

**Rule for the next batch: every proposal must name the endpoint or the source before it
gets a rank, and the endpoint must be called once to prove it returns what the page needs.**

### 2. Two corrections to section C

- **Warriors franchise records is not a gap.** `stephen-curry-career-records-three-pointers` already covers the records this site can credibly speak to. The gap probe missed it because it searched for slugs containing `warriors-record`. Slug pattern matching is not a content inventory.
- **The Warriors do not open on 4 October.** That is the preseason opener. ESPN's team schedule endpoint returns preseason by default and needs `?seasontype=2` for the regular season, which opens **21 October at the Lakers**. Any future schedule work must pass that parameter.

### 3. What the feeds actually give, and what they do not

| Need | Source | Verdict |
|---|---|---|
| Head to head series history | `statsapi.mlb.com/schedule?teamId=&opponentId=` per season | Works perfectly. 160 meetings, venues included. This is the pattern for any rivalry page. |
| Team schedule and results | `site.api.espn.com/.../teams/<abbr>/schedule?seasontype=2` | Works. Send urllib's default User-Agent, ESPN 403s anything it does not recognise, including any string containing a URL. |
| Franchise career leaders | none found | Blocked. |
| Venue facts | no feed | Human verified per fact, and anything unconfirmed gets left out. The Chase Center page carries no opening date and no construction cost for exactly that reason. |
| Team venue metadata from ESPN | `teams/gs` franchise record | **Stale, do not use.** It still returns Oracle Arena. The per game `competitions[].venue` payload is correct. |

### 4. Feeds are incomplete in ways a reader will notice

The league listing for the Warriors carries 80 games. The NBA plays 82. The page says so in
its own section rather than padding the table with dates nobody has committed to. Any future
schedule page needs the same honesty valve, because the alternative is a table that quietly
disagrees with reality.

### 5. The generated region pattern works, use it again

All three new pages, plus the homepage, now follow the same shape: prose a human wrote,
data between HTML comment markers, a generator that rewrites only what is inside the
markers, and a `--check` flag that fails if the page has drifted. Four generators run in the
publish chain now. Next season's Bay Bridge results are a command, not a rewrite.

Failure order is the same in all of them: live feed, then the cached pull, then stop without
touching the page. A stale table is worse than an unchanged one.

### 6. Inbound links for a brand new page are capped by existing wording

The plan called for six in body inbound links on the Bay Bridge page. It got two, because
only two existing sentences had wording a link could wrap without rewriting. The Warriors
hub got one, the Chase Center guide got two.

**The realistic yield is one to two in body links per new page.** Hub cards carry the rest,
and they are what actually produced reachability in the crawl. Plan for that rather than
promising six.

### 7. Voice gate interactions worth knowing

Bolded functional labels, the kind a practical guide wants for "From BART" and "From
Caltrain", trip the scaffold rule at four and cost six points. Converting them to `h3`
subheads fixed it and improved the document outline at the same time. A reference page with
a long table also needs a deliberate short paragraph somewhere or the rhythm check fires.

### 8. Schema type is worth a decision before the next batch

All three pages inherited `NewsArticle` from the article template, same as the other 220.
For an evergreen reference page `Article` is the more accurate type, and the Bay Bridge and
Chase Center pages are not news in any sense. **Not changed**, because it affects the shared
template and was out of scope. Worth deciding before more evergreen pages are built.

### 9. Result at the end of the pilot

| | Before pilot | After |
|---|---|---|
| Articles | 220 | 223 |
| Pages crawled | 254 | 257 |
| Non 200 responses | 0 | 0 |
| Orphans / near orphans | 0 / 0 | 0 / 0 |
| Duplicate titles or descriptions | 0 | 0 |
| Voice gate under 70 | 0 | 0 |
| Generators in the publish chain | 1 | 4 |

The three pages cost three new URLs and added no defects. Depth from the homepage held at a
maximum of four clicks.
