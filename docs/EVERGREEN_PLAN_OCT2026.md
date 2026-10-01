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
