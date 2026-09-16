# Declared page intent

Pages that sit close enough to each other to converge by accident. Each entry says what
that page is for and, just as importantly, what it must never start doing. Anyone editing
one of these, human or script, checks here first.

`tools/cannibal_check.py <slug> <slug>` prints the live comparison: title, H1, description,
H2 outline, word count, topic word balance and the anchor text pointing at each page. Run it
after editing either side of a pair.

---

## Warriors: schedule hub against season outlook

The only pair on the site that was ever at real risk, because both carry the team name and
the season in the title.

| | `warriors-2026-27-schedule-season-hub` | `warriors-2026-27-season-outlook` |
|---|---|---|
| **Intent** | Navigational and recurring | Informational and argumentative |
| **The question it answers** | When do they play, who, where, and what happened | How good is this team and what can it realistically do |
| **Title** | The 2026-27 Warriors Schedule, Game by Game | The 2026-27 Warriors: What This Roster Actually Is |
| **H1** | Same as title | Same as title, plus "and What It Can Realistically Be" |
| **Body** | Dates, opponents, home and away, results, schedule shape | Roster, injuries, cap, range of outcomes |
| **Anchor text it should attract** | "the 2026-27 schedule", "opening night", "when they play" | "the season outlook", "what this roster is" |
| **Schema** | Article | NewsArticle |
| **Updates** | Every publish, from the feed | Editorial, by hand |

**The hub must never** carry a prediction, a ceiling, a floor, a projection or an opinion
about whether the roster is good. The moment it does, it starts competing with the outlook
for the same query and both lose.

**The outlook must never** grow a schedule table or a results list. If it needs a date, it
links to the hub.

Measured at the last check: title token overlap 0.33, and the only shared tokens are the
team name and the year. The hub carries 20 schedule words against 3 prediction words, the
outlook 1 against 5. Each links to the other, saying which is which.

---

## Venues: Chase Center against Oracle Arena

| | `chase-center-guide-warriors-arena` | `oracle-arena-roaracle-history-oakland-warriors` |
|---|---|---|
| **Intent** | Practical, pre visit | Historical |
| **The question** | How do I get there and what do I need to know | What was that building and what happened to it |
| **Tense** | Present | Past |
| **Schema** | Article | NewsArticle |

Title overlap 0.06. They want to link to each other and they do. The Chase Center page is
allowed one honest paragraph of comparison, because that comparison is the reason a reader
from the East Bay is on the page at all. It is not allowed to become a second history of
the old arena.

---

## The Bay Bridge Series against the relocation cluster

`bay-bridge-series-giants-athletics-history` owns the head to head record and the ballparks.
`athletics-oakland-sacramento-las-vegas-timeline` owns the move itself.
`bay-area-franchise-relocations-teams-that-left` owns every Bay Area departure as a set.
`athletics-sacramento-bay-area-villains` owns the grievance.

Four pages, four jobs, no overlap in intent. The series page is the only one that carries a
record table, and it states its own scope in the body: regular season, 1997 to 2026, with
the 1989 World Series reported separately and kept out of the totals.

---

## 49ers: season hub as a calendar

`49ers-2026-schedule-season-hub` was 688 words of editorial carrying 23 in body inbound
links, which is the most on the site. It now opens with the same three generated regions as
the Warriors hub, next game, season shape and the week by week table, and the editorial that
was already there sits underneath them under its own heading.

**The rule is the same as the Warriors pair.** The table and the shape list are facts from
the league feed. The prose below is allowed to argue, because it always did and it is what
gives the page a voice, but it must never contradict the table above it and the table must
never carry a prediction. If that page ever needs a real forecast section, it goes on a
different URL.

---

## Rules for anything added later

1. Two pages may share a subject. They may not share an intent.
2. If a new page would answer the same question as an existing one, improve the existing one instead. That decision is in the content audit and it has not changed.
3. A page whose job is to be checked repeatedly, a schedule or a record, is navigational. It does not argue.
4. A page whose job is to argue does not carry the table. It links to the page that does.
5. Declare the intent here on the day the page ships, not the first time somebody notices a collision.
