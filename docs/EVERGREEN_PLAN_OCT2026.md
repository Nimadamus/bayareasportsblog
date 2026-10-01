# Evergreen opportunity plan, October 2026

**Written 1 October 2026. Nothing in this list is built yet.** It replaces the ordering in
`CONTENT_OPPORTUNITY_AUDIT.md` section H for 49ers and Warriors work; the three pilot pages
from September (Bay Bridge Series, Warriors schedule hub, Chase Center guide) are live and
not repeated here.

**Ranking basis.** No Search Console data is on this machine, so no page here is ranked by
impressions or position. Priority comes from: the query is one people type (a reference
question, not a headline), we have no page answering it, a public feed or record can back
every number, and the page gives a hub something durable to link to. When Search Console
access lands, rerank against real queries before building past item 5.

**Rules that apply to every item.** One page per intent: no "49ers playoff history" next to
"49ers Super Bowl history", no "leaders" next to "records". UPDATE means same URL, history
kept. No dates in URLs. Every figure comes from a feed or record read in the session that
builds the page. Each new page gets linked from its hub (the hub key pages block in
`_gen_hub_status.py`), the sitemap, and at least three existing articles in the same commit.

---

## Priority list

| # | Page | NEW or UPDATE | URL | Parent hub |
|---|------|---------------|-----|------------|
| 1 | 49ers injury report | NEW, living | `articles/49ers-injury-report.html` | 49ers |
| 2 | 49ers playoff and Super Bowl history | NEW | `articles/49ers-playoff-super-bowl-history.html` | 49ers, History |
| 3 | Levi's Stadium guide | NEW | `articles/levis-stadium-guide-parking-transit-bag-policy.html` | 49ers |
| 4 | 49ers all time leaders and records | NEW | `articles/49ers-all-time-leaders-records.html` | 49ers |
| 5 | Brock Purdy career stats | UPDATE | `articles/brock-purdy-career-passer-rating-where-he-ranks.html` | 49ers |
| 6 | Warriors injury report | NEW, living | `articles/warriors-injury-report.html` | Warriors |
| 7 | Warriors all time leaders and records | NEW | `articles/warriors-all-time-leaders-records.html` | Warriors |
| 8 | Stephen Curry career records | UPDATE, living | `articles/stephen-curry-career-records-three-pointers.html` | Warriors |
| 9 | Warriors playoff history | UPDATE | `articles/warriors-championship-history.html` | Warriors, History |
| 10 | Giants and Dodgers rivalry | NEW | `articles/giants-dodgers-rivalry-history.html` | Giants, History |
| 11 | Giants all time leaders and records | NEW | `articles/giants-all-time-leaders-records.html` | Giants |
| 12 | Bay Area retired numbers | NEW | `articles/bay-area-retired-numbers-every-team.html` | Bay Area, History |
| 13 | SAP Center guide | NEW | `articles/sap-center-guide-sharks-arena.html` | Sharks |
| 14 | Sharks all time leaders and records | NEW | `articles/sharks-all-time-leaders-records.html` | Sharks |
| 15 | Oracle Park guide | UPDATE | `articles/oracle-park-mccovey-cove-splash-hits-guide.html` | Giants |
| 16 | Bay Area venues index | NEW | `articles/bay-area-sports-venues-guide.html` | Bay Area |

---

## The detail

### 1. 49ers injury report
- **Query / intent:** "49ers injury report", "49ers injuries", "is Nick Bosa playing". Someone wants who is out this week and when they are back.
- **Existing:** many single injury columns (Bosa calf, Collins patellar, Stribling ankle, Pearsall PCL, the plus 42 roundup). None is the current list.
- **Why it deserves to exist:** the single highest frequency 49ers question during a season, and every injury column we write today becomes a dead end a week later. One living page absorbs that demand and links out to the columns.
- **Built how:** ESPN team injuries feed for status, refreshed by the daily action between markers, prose kept to a short intro. Each player row links to our column on that injury when one exists.
- **Links in:** 49ers hub key pages, every new injury column, the schedule hub. **Links out:** the columns, the depth chart.

### 2. 49ers playoff and Super Bowl history
- **Query / intent:** "49ers Super Bowl wins", "how many Super Bowls have the 49ers won", "49ers playoff history". Reference lookup.
- **Existing:** `49ers-dynasty-team-of-the-decade` (an argument about the 80s), `bay-area-championships-complete-list-by-team` (titles only, all teams). Neither lists every playoff season.
- **Why:** answers a factual question with a full table (every postseason, result, opponent, score) that the dynasty column cannot be turned into without losing its voice. One page covers both phrasings, so no separate Super Bowl page.
- **Links in:** dynasty column, The Catch, Montana and Young, championships list, 49ers hub. **Links out:** the same, plus Candlestick.

### 3. Levi's Stadium guide
- **Query / intent:** "Levi's Stadium parking", "Levi's Stadium bag policy", "how to get to Levi's Stadium". Practical, high volume on game weeks.
- **Existing:** none. The Chase Center guide proved the format.
- **Why:** practical venue guides pull non fan traffic (concerts, college games) and earn links from local forums. Built from the stadium's own published policies, read in session.
- **Links in:** 49ers hub, schedule hub, venues index. **Links out:** Candlestick history, Chase Center guide.

### 4. 49ers all time leaders and records
- **Query / intent:** "49ers all time passing leaders", "49ers rushing leaders", "49ers records".
- **Existing:** Purdy pages touch passer rating only.
- **Why:** classic reference page that does not decay, and the place every Purdy, McCaffrey and Kittle milestone column should link. Leaders, single season records, retired numbers link out to item 12.
- **Links in:** Purdy pages, Montana and Young, dynasty. **Links out:** player columns.

### 5. Brock Purdy career stats (UPDATE)
- **Query / intent:** "Brock Purdy stats", "Brock Purdy career passer rating".
- **Existing:** `brock-purdy-career-passer-rating-where-he-ranks` already ranks for the passer rating angle.
- **Why UPDATE, not NEW:** a separate "Purdy stats" page would compete with it. Add a feed driven career and season table between markers on the same URL.

### 6. Warriors injury report
Same model as item 1, ESPN NBA injuries feed. Build in mid October so it is live for the opener.

### 7. Warriors all time leaders and records
- **Query / intent:** "Warriors all time scoring leaders", "Warriors records".
- **Existing:** Curry records page (one player), championship history (titles).
- **Why:** reference anchor for the franchise, links to Curry, 73-9, Nelson, Klay's 37 point quarter. Retired numbers link out to item 12.

### 8. Stephen Curry career records (UPDATE)
Make the three point total and the core career numbers feed driven so the page is never behind. Same URL.

### 9. Warriors playoff history (UPDATE)
Extend `warriors-championship-history` with every playoff season, result and opponent. Same URL, so it answers both "Warriors championships" and "Warriors playoff history" without a second page.

### 10. Giants and Dodgers rivalry
- **Query / intent:** "Giants Dodgers rivalry", "Giants vs Dodgers all time record".
- **Existing:** none beyond recaps.
- **Why:** the oldest rivalry in the sport, head to head record from the MLB stats API, the 1951 and 1993 races (link the 1993 piece), Bonds. Strong link target and outreach asset.

### 11. Giants all time leaders and records
Same pattern as 4 and 7. Links to Bonds, Kent, even year titles.

### 12. Bay Area retired numbers
- **Query / intent:** "49ers retired numbers", "Warriors retired jerseys", "Giants retired numbers".
- **Why one page and not five:** retired numbers is a short list per team. One page with a section per franchise is more useful than five thin pages and is exactly the kind of cross team reference other sites cite. Team leaders pages link to their section by anchor.

### 13. SAP Center guide
Same model as Chase Center and Levi's. Sharks hub has no venue page.

### 14. Sharks all time leaders and records
Thornton, Marleau, Pavelski, Celebrini's 115 point season. Links to playoff history and founding page.

### 15. Oracle Park guide (UPDATE)
The existing page covers dimensions, wind and McCovey Cove. Add the visitor half (transit, parking, bag policy, gates) at the same URL instead of a second Oracle Park page.

### 16. Bay Area venues index
A small hub page that lists every venue guide (Chase Center, Oracle Park, Levi's, SAP Center, Sutter Health Park, plus the history pages for Candlestick, Oracle Arena and the Coliseum). Built last, once at least three guides exist.

---

## Not proposed, and why
- Separate "49ers Super Bowl appearances" and "49ers Super Bowl wins" pages: same intent as item 2.
- "Chase Center parking", "Chase Center bag policy" as separate pages: the existing guide covers both.
- Per team "retired numbers" pages: item 12.
- Off site reference databases (championship database, injury database, relocation timeline): worth doing after items 1 to 5, because items 1 and 2 are the seed data for them.

---

## Reranked against Search Console, 1 October 2026

Evidence is in `docs/GSC_REPORT_OCT2026.md`. Search Console cannot show demand for a page
that does not exist, so "no evidence" below means the site has no signal yet, not that
nobody searches it. The strongest general signal: reference pages earn 84% of impressions
from a third of the pages, and 49ers news earns almost nothing.

| # | Page | Decision | Evidence |
|---|------|----------|----------|
| 1 | 49ers injury report | **BUILT 1 Oct** | No direct query data (no page existed). Built because reference pages are what this site ranks with, 49ers news is not working, and the season is live. |
| 2 | 49ers playoff and Super Bowl history | BUILD LATER | dynasties (123 impr, pos 11), montana-young (67, 10) and the championships list (56, 7.7) already take this intent. Building now would split it. Revisit when 49ers history queries reach the top 10. |
| 3 | Levi's Stadium guide | BUILD LATER | The Chase Center guide sits at position 47 with 28 impressions. Venue guides have not proven themselves here yet. |
| 4 | 49ers all time leaders and records | BUILD LATER | No signal. |
| 5 | Brock Purdy career stats | **UPDATE EXISTING** (next) | Main Purdy page 72 impr at 9.7; the second Purdy record page is crawled but not indexed. Strengthen the main page and point the second one at it. |
| 6 | Warriors injury report | **BUILD NOW** (before the regular season opener) | "golden state warriors roster updates 2026" at 5.7 and depth chart queries at 5.8 to 10 show Google trusts us on current Warriors roster status. |
| 7 | Warriors all time leaders and records | BUILD LATER | "stephen curry records" at 40, "golden state warriors best players" at 6 (1 impr). Thin. |
| 8 | Stephen Curry career records | UPDATE EXISTING (low) | 7 impr at 29. |
| 9 | Warriors playoff history | **UPDATE EXISTING** | championship history 19 impr at 21.6; "did the 73 9 warriors win the finals" (22.3) and "did the 73 9 warriors win the championship" (37.5) need this answered on our pages. |
| 10 | Giants and Dodgers rivalry | BUILD LATER | No signal. |
| 11 | Giants all time leaders and records | BUILD LATER; **UPDATE the Bonds page first** | Barry Bonds page: 190 impr at 41, the biggest Giants asset, with "when did barry bonds play / retire" at 65. A career facts section on that page comes first. |
| 12 | Bay Area retired numbers | BUILD LATER | No signal. |
| 13 | SAP Center guide | BUILD LATER | No signal; venue guides unproven. |
| 14 | Sharks all time leaders and records | **BUILD NOW** (after the Warriors report) | Sharks reference pages earn the most per page on the site (8 pages, 440 impr): playoff history 141 at 8.0, depth chart 127 at 10, founding 46, "has san jose won a stanley cup". |
| 15 | Oracle Park guide | UPDATE EXISTING (medium) | 44 impr at 18.4. |
| 16 | Bay Area venues index | DO NOT BUILD | No signal, thin hub, would compete with the team hubs. |

New items the data surfaced that were not on the list:
- **Sutter Health Park guide (UPDATE):** 118 impr at 21.3, the best A's page.
- **Sharks no Stanley Cup history (UPDATE):** 111 impr at 38.1.
- **KD and 73-9 question (DONE 1 Oct):** title and description now answer it.
- **Sharks playoff history (DONE 1 Oct):** title and description name the last trip.
