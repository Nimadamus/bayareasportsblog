# Evergreen pilot, three proposals

**Written 15 September 2026, HEAD `f73d398`. Nothing here is built.**

Everything marked **verified** was measured on this machine this session. Everything marked
**hypothesis** is an argument about search intent with no ranking data behind it, because
there is still no Search Console credential here. The two are never mixed.

---

## What changed the shortlist

The content audit ranked Giants franchise records and 49ers franchise records first and
second. **I tested whether we can source them and we cannot**, so they are not in this
pilot.

MLB's `statsapi` team leaders endpoint returns **season** leaders, not franchise career
leaders. Asking it for Giants home run leaders today returns Devers at 37, not Bonds at
586. There is no public feed that gives franchise career leaders, and the site that does
have them is not ours to scrape. A records page we cannot source is a records page we
cannot keep accurate, which fails your fourth criterion outright. Both are parked until
there is a licensed data route.

What survived is three pages we can actually source, keep correct, and defend.

---

## 1. The Bay Bridge Series

| | |
|---|---|
| **URL** | `/articles/bay-bridge-series-giants-athletics-history.html` |
| **Title** | The Bay Bridge Series: What Is Left of It, and What the Record Actually Says |
| **Primary intent** | Informational, with genuine live confusion behind it. Somebody wants to know whether the Giants and the A's still play, where, and who has won more. |
| **Primary topic** | bay bridge series history |
| **Secondary** | giants a's rivalry, do the a's still play the giants, giants athletics all time record, bay bridge series 2026 |
| **Links in on day one** | `bayarea.html`, `athletics-oakland-sacramento-las-vegas-timeline` (in=12), `bay-area-franchise-relocations-teams-that-left`, `oakland-coliseum-history-what-happens-to-it-now` (in=5), `giants-athletics-all-star-game-2026-arraez-langeliers-webb`, `athletics-sacramento-bay-area-villains` (in=11) |
| **Future links** | every A's recap that mentions Sacramento or Las Vegas, which is most of them, and any Giants piece about interleague play |
| **Update load** | Six games a year. Effectively static between May and June. |

**Sources, verified.** `statsapi.mlb.com/api/v1/schedule?teamId=137&opponentId=133` returns
every meeting with final scores. I ran it for 2026: six meetings, three in May at Sutter
Health Park, the rest at Oracle. Repeating that per season from 1997 gives the complete
head to head with no manual entry and no scraping. Venue names come back in the same
response, which matters here because the venue is half the story.

**Why this site and not a generic one.** No other outlet has a Giants section and an A's
section written by the same fed up fan. Everyone else covers the A's as a curiosity or not
at all. We have 36 A's pieces, 81 Giants pieces and a relocation cluster already built, and
this is the one rivalry page in American sport with an ending attached to it: 2027 is the
last Sacramento season and 2028 is Las Vegas. That ending is the article.

**Structure.** What it was and why the Bay Bridge name stuck, including 1989. The all time
series record as a table, season by season, home and away. What happened to it when the A's
left Oakland. What 2027 looks like and what happens after. Then the part only we will
write, which is whether it is still a rivalry when one side has no city.

**Cannibalisation check.** Compared against all 220. The relocation timeline covers the
move, the villains column covers the grievance, the All Star Game piece covers one night in
July. **None of them targets the series or carries the head to head record.** No overlap.

---

## 2. Warriors 2026-27 schedule and season hub

| | |
|---|---|
| **URL** | `/articles/warriors-2026-27-schedule-season-hub.html` |
| **Title** | Warriors 2026-27 Schedule, Results and Where the Season Actually Stands |
| **Primary intent** | Navigational and recurring. When is the next game, what happened in the last one, what is the record. |
| **Primary topic** | warriors schedule 2026 27 |
| **Secondary** | warriors next game, warriors record, warriors results, warriors games this week |
| **Links in on day one** | `warriors.html`, `nba.html`, `warriors-2026-27-roster-depth-chart`, `warriors-roster-construction-cap-sheet-2026-27`, `warriors-2026-27-projected-rotation`, `warriors-championship-history` (in=8), and the 14 Warriors articles through the hub grid |
| **Future links** | every Warriors column and recap from opening night onward, the same way the 49ers hub collects them |
| **Update load** | Continuous, and that is the point of piloting it. |

**Sources, verified.** `site.api.espn.com/.../basketball/nba/teams/gs/schedule` returns the
full season with completed results and scheduled fixtures. I read it today: the Warriors
open 4 October at the Clippers, zero completed games so far. The fetch layer, the staleness
rules and the failure handling already exist in `_gen_homepage_live.py`, shipped this
session and drilled against dead feeds, malformed payloads and stale data.

**Why this page is the right pilot.** It is the only one of the three that tests whether an
**auto updating reference page** works on this site. Every other team we cover has a season
hub. The 49ers version is the most linked page on the whole site at 23 in body inbound
links, which is the evidence that the pattern works here. The Warriors, our second biggest
brand, do not have one, and the season starts in nineteen days.

**Structure.** Next game at the top, then the full schedule table with results filled in as
they happen, the record, and a short honest paragraph about where the season stands that
gets rewritten as it goes. Below that, links out to the depth chart, the cap sheet and the
rotation piece, so the four Warriors reference pages finally form a cluster instead of four
strangers.

**Cannibalisation check, and the one real risk here.** `warriors-2026-27-season-outlook`
exists and is the closest thing on the site. **These two must be kept apart deliberately:**
the outlook is an argument about how the season will go, the hub is where you check what
happened. If they drift together we will have built the one cannibalisation problem the
audit says we currently do not have. The mitigation is in the title and the H1, no
prediction language on the hub, and a link between them saying which is which.

**A caution you should weigh.** Warriors coverage has been dormant since 25 August. A hub
collects links from articles that exist. If the section stays quiet, this page will sit
with six inbound links instead of twenty three. It is worth building anyway because the
season restarts the section, but the hub does not fix the section on its own.

---

## 3. Chase Center guide

| | |
|---|---|
| **URL** | `/articles/chase-center-guide-warriors-arena.html` |
| **Title** | Chase Center: What It Costs, What It Feels Like, and What We Gave Up for It |
| **Primary intent** | Practical and pre visit, with a second audience that just wants to argue about the move from Oakland. |
| **Primary topic** | chase center guide |
| **Secondary** | chase center seating, warriors arena, chase center parking, chase center vs oracle arena |
| **Links in on day one** | `warriors.html`, `oracle-arena-roaracle-history-oakland-warriors` (in=3), `bay-area-sports-history`, `warriors-out-of-easy-answers`, and the proposed venues index if that gets built |
| **Future links** | every Warriors home game piece, and it is the natural companion link from the Oracle Arena history |
| **Update load** | Low. Capacity, layout and transit change rarely. Prices need a look once a year. |

**Sources.** Static and verifiable: published capacity and layout, the transit options, the
arena's own documented specifications. No feed needed, which is exactly why the maintenance
cost is low. **This is the one proposal that needs a human to check the facts once rather
than an API**, and I would want the page to carry only what can be confirmed rather than
anything about atmosphere dressed up as fact.

**Why this site.** We already own five venue pages: Oracle Park, Sutter Health Park, the
Coliseum, Candlestick and Oracle Arena. That is a proven cluster and Chase Center is the
hole in it. More to the point, we are the site that wrote the Roaracle piece, so we can do
the comparison honestly. Every official page about Chase Center is a sales document. Ours
would say what the move actually cost the people who used to drive to Oakland, and three
articles already mention the building without explaining it.

**Structure.** Getting there, including the Muni and ferry options that actually work.
Seating and where the money goes. What it is like compared to the old building. What
changed for the fans who did not follow the team across the bridge. Short, specific,
useful.

**Cannibalisation check.** `oracle-arena-roaracle-history-oakland-warriors` is about the old
arena and its history. Different building, different intent, and the two pages want to link
to each other. No overlap with anything else on the site.

---

## Why not the others yet

- **Giants and Dodgers rivalry.** The biggest term on the list and the most competitive. It also needs the all time series record, which has the same sourcing problem as the franchise records pages, going back to 1890. Worth doing properly later, not as a pilot.
- **Retired numbers across the Bay Area.** Strong and static, and it was the runner up to Chase Center. It wants a players and history cluster we do not have yet, so it would land with thin internal support.
- **Athletics 2026 season hub.** The audit ranked it second. The 2026 season ends on 27 September, twelve days out, so a 2026 hub has almost no shelf life left. This should be built as the 2027 hub in March, when it has a full season in front of it.
- **Levi's Stadium guide and the venues index.** Both cheap and both good. They belong in the batch after the pilot, and the venues index is worth more once Chase Center exists to go in it.

---

## What I need to proceed

Approval on which of the three to build, in what order. Each is a single page. None changes
an existing URL, none needs a redirect, and each ships with its inbound links in the same
commit per the no orphans rule.
