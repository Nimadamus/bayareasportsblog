# Bay Area Sports Blog — sitewide content calendar

The site now runs several content engines on different calendars. This file is the
memory: which cluster needs attention, when, and why. Update the status column as things
publish.

**Last updated: 2026-08-08** (Warriors + Giants clusters built)

---

## Active clusters

| Cluster | Status | Next event / date | Next article opportunity | Publish window | Type | Next refresh |
|---|---|---|---|---|---|---|
| **49ers** | foundation built (5 pieces) | **Week 1, 10 Sep** — at Rams, Melbourne | Week 1 preview | 8–9 Sep | news | weekly, in season |
| 49ers | — | Week 2, Miami at Levi's | reaction + preview | 14–20 Sep | news | weekly |
| 49ers | — | **~game five** | Purdy passes 1,500 attempts, qualifies for the career passer-rating record | day of | **update the Purdy page** | biggest single traffic event of the season |
| 49ers | — | Mexico City vs Minnesota | game week coverage | TBD | news | weekly |
| **Cal / Stanford** | foundation built (8 pieces) | **Stanford vs Hawaii, 29 Aug** (Week 0) | Stanford opener reaction | 29–30 Aug | news | — |
| Cal / Stanford | — | **Cal vs UCLA, 5 Sep** | Cal opener reaction | 5–6 Sep | news | — |
| Cal / Stanford | — | **Big Game, 21 Nov, Berkeley** | Big Game week package | 17–21 Nov | news + refresh evergreen | refresh the Big Game and Axe pages that week |
| **Warriors** | foundation built (4 pieces) | NBA 2026-27 schedule release | **schedule / season hub** | on release | news→permanent | the one missing permanent page |
| **Giants** | foundation built (4 pieces) | rest of the 2026 season, to early Oct | recaps + rebuild-page updates | ongoing | news | update the rebuild page on every roster move |
| Giants | — | end of season, early Oct | season-in-review, 2027 offseason preview | Oct | news→permanent | — |
| Giants | — | offseason, Nov–Feb | manager decision, rotation signings, Eldridge spring watch | as they happen | news | — |
| Warriors | — | training camp, late Sep | camp storylines, Butler knee status | late Sep | news | weekly once season starts |
| Warriors | — | opening night, late Oct | season opener preview + reaction | late Oct | news | weekly |

## Permanent pages — update, never duplicate

| Page | Cluster | Refresh trigger |
|---|---|---|
| `brock-purdy-career-passer-rating-where-he-ranks` | 49ers | after the record qualifies (~game 5), then end of season |
| `49ers-2026-schedule-season-hub` | 49ers | every week — add that week's preview + reaction link |
| `49ers-2026-roster-depth-chart` | 49ers | on roster moves and meaningful injuries |
| `49ers-2026-season-preview-roster-schedule-questions` | 49ers | once at midseason |
| `warriors-2026-27-roster-depth-chart` | Warriors | on roster moves, Butler/Moody knee news |
| `warriors-2026-27-season-outlook` | Warriors | at camp, and again at the quarter mark |
| `stephen-curry-career-records-three-pointers` | Warriors | when the three-point total moves meaningfully |
| `warriors-roster-construction-cap-sheet-2026-27` | Warriors | at the trade deadline |
| `giants-2026-where-the-rebuild-actually-stands` | Giants | every roster move, and at the end of the season |
| `giants-2026-roster-depth-chart` | Giants | on roster moves and call-ups |
| `giants-2026-season-hub-results-coverage` | Giants | after each game — add the recap link |
| `oracle-park-mccovey-cove-splash-hits-guide` | Giants | rarely — evergreen, check park factors each offseason |
| `big-game-cal-stanford-rivalry-history` | Cal/Stanford | after each Big Game — add the result |
| `stanford-axe-trophy-history` | Cal/Stanford | after each Big Game |
| `cal-2026-schedule-game-by-game-acc` | Cal | as results come in |

## Next clusters, ranked by real opportunity

Prioritised on traffic upside × existing site authority × season timing × how weak the
national competition is.

| Rank | Cluster | Why now | Timing | Existing authority |
|---|---|---|---|---|
| ~~1~~ | ~~Giants~~ | **BUILT 2026-08-08.** 4 pages: rebuild state, depth chart, season hub, Oracle Park evergreen. | — | — |
| **1** | **Athletics** | 22 articles and the single most distinctive angle we own — a franchise playing major-league games in a Triple-A park while waiting on Las Vegas. National outlets cover it as a business story; nobody covers it as a fan grievance. Genuine backlink potential. | Sep, then the Vegas timeline | strong |
| **2** | **Bay Area history / evergreen** | `bay-area-sports-history` already has the most inbound links of any article. The Dynasties and Timeline pages exist but are thin on supporting articles. Pure evergreen, no season dependency, best link-earning category. | any time — filler between seasons | high inbound, low article count |
| **3** | **Sharks** | One article. NHL season starts October. Celebrini is a real national story. But the archive is so thin that this is a build-from-zero, and the audience is the smallest of the five. | Oct | weakest |

## Rules that apply to every cluster

1. **Never write a reaction before the game.** Fabricating results is disqualifying.
2. **One query, one page.** Check the archive before writing; update rather than compete.
3. **Every article links up to its hub** and to at least one permanent page.
4. **No thin pages.** Under ~500 words means it should have been an update.
5. **Cards from `tools/cardgen.py`** — team palette, no stock photos, no likenesses.
6. **All four gates pass before commit:** `tools/thumb_gate.py --site`,
   `_meta_template.py --gate`, `_sitemap_audit.py`, `_seo_audit.py`.
7. **The news sitemap only holds 48 hours.** Cadence is the whole game in season.

## Known gaps, deliberately unfilled

- Warriors schedule hub — waiting on the NBA schedule release
- Weekly 49ers previews/reactions — waiting on games
- Cal/Stanford game reactions — waiting on games
- Sharks anything — needs a decision on whether to invest in the smallest audience
- `betting.html` — permanently out of the sitemap; that content lives on TMR/BetLegend
