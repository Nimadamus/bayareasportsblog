# Cal / Stanford gameday workflow — 2026 season

The college season is a recurring system, not a batch. This is the loop for both
programmes, the commands, and the rules that stop it producing filler. It mirrors
`NFL_WEEKLY_WORKFLOW.md`; the difference is that college weeks are irregular — Week 0,
byes, Friday kickoffs — so the loop is keyed to *a game*, not to a weekday.

## The four permanent pages per programme

These get **updated, never duplicated**. Everything published during the season links to
at least one of them.

| Stanford | Cal |
|---|---|
| `stanford-2026-schedule-game-by-game-acc.html` ← results go here | `cal-2026-schedule-game-by-game-acc.html` |
| `stanford-2026-season-preview-pritchard-luck-warren.html` | `cal-2026-season-preview-lupoi-sagapolutele.html` |
| `stanford-hawaii-week-zero-opener-preview.html` | — |
| `andrew-luck-stanford-general-manager-experiment.html` | — |

Shared evergreen: `big-game-cal-stanford-rivalry-history.html`,
`stanford-axe-trophy-history.html`, `cal-stanford-acc-realignment-what-changed.html`.

## The per-game loop

| When | Piece | Notes |
|---|---|---|
| **Game week, 2–4 days out** | Preview | Matchup, both teams' questions, keys. No predicted score. |
| **Immediately after the final whistle** | Nothing | Wait. See the postgame gate below. |
| **Same night / next morning** | Reaction | Only after the result is confirmed from a live source. |
| **+1 day** | Roster/injury implications | **Only if something meaningful changed.** Otherwise update the schedule page. |

**Ceiling: 2–3 pieces per game week per programme.** More and they cannibalise each other
for the same query.

---

## POSTGAME GATE — Stanford vs Hawaii, 29 August 2026

**Nothing in this section may be written before the game is played.** The preview is
already live and deliberately predicts no score.

### Step 0 — confirm the result from a live source
```bash
# do not proceed on memory or on a preseason assumption
# confirm final score, scorers, and any injury news before writing a word
```
If the game is postponed or the result cannot be confirmed, **publish nothing.**

### Step 1 — the reaction piece
- Slug: `stanford-hawaii-week-zero-reaction-<result>` (name it after what happened).
- Must cover: what actually happened, **what changed from preseason expectations**, how
  Davis Warren looked and whether the knee was a factor, whether the new offence looked
  designed, how the defence handled Micah Alejado, and the Miami short week.
- Must link to: `../stanford.html`, the preview, the schedule page, and at least one
  evergreen (`stanford-axe-trophy-history` or `cal-stanford-acc-realignment-what-changed`).
- Build it in `_college_cluster.py`, run `--check`, reject under ~500 words.

### Step 2 — update the permanent pages
- `stanford-2026-schedule-game-by-game-acc.html` — add the result to the Hawaii row and
  link the reaction. This page is the season's record; it is the one that must never fall
  behind.
- `stanford-hawaii-week-zero-opener-preview.html` — add one line at the top pointing to
  the reaction. Do not rewrite the preview into a recap; it keeps its own search intent.
- `stanford-2026-season-preview-pritchard-luck-warren.html` — only if the game changed the
  season's outlook.
- Roster/depth implications: fold into the schedule page unless a starter's status
  genuinely changed.

### Step 3 — update the Stanford hub
`stanford.html`, the `<!-- stanford opener nav -->` block: replace the "Reaction lands
after the game is played" line with the reaction link, and reframe the block around the
Miami game on 4 September.

### Step 4 — update `CONTENT_CALENDAR.md`
Mark the opener done, move the next Stanford entry to the top, and record anything the
game changed about the season's expectations.

### Step 5 — feeds and gates, then push
```bash
python _college_cluster.py            # writes the article + card
python tools/card_derivatives.py      # 400/600/800 jpg+webp + full webp
python _gen_sitemap.py && python _gen_news_sitemap.py
python _gen_search_index.py && python _gen_feed.py
python tools/thumb_gate.py --site
python tools/card_derivatives.py --check
python tools/social_meta_gate.py --check
python _meta_template.py --gate
python _sitemap_audit.py
python _seo_audit.py                  # check near-orphans and 0-in-body-inbound
```
The news sitemap holds a rolling 48 hours, so a reaction published late on the Sunday is
already half-spent. Same-night or next-morning is the whole game.

---

## The rest of the college calendar

| Date | Game | What publishes |
|---|---|---|
| **29 Aug** | Stanford vs Hawaii (Week 0) | Preview live. Reaction after. |
| **4 Sep** | Miami at Stanford | Preview 2–3 days out; short week, so start early |
| **5 Sep** | Cal vs UCLA | **Cal's opener** — preview 3 Sep, reaction after |
| **12 Sep** | Cal at Syracuse | Only if the UCLA result made it interesting |
| **19 Sep** | Stanford at Duke | Preview |
| **26 Sep** | Clemson at Cal | Cal's measuring-stick game |
| **10 Oct** | Stanford at Notre Dame | The marquee game; highest traffic of the regular season |
| **21 Nov** | **Big Game, Berkeley, 129th meeting** | The package: preview, reaction, **and refresh both the Big Game and Axe evergreens with the result and the new series record.** Stanford currently holds the Axe after winning the 128th 31-10; the series stands 66-51-11. |

## Non-negotiables

1. **Never write a reaction before the game.** Fabricating a result is disqualifying.
2. **Research before writing.** Never invent a score, a date, a statistic or an injury.
3. **One query, one page.** Check the archive first; update rather than compete. The
   opener preview was expanded from 536 to 1,255 words rather than being replaced by a
   rival page, and it kept its URL.
4. **No thin pages.** Under ~500 words means it should have been an update.
5. **Every article links up to its hub** and to at least one permanent page.
6. **Cards from `tools/cardgen.py`**, `stanford` or `cal` palette. No stock photos.
7. **All gates pass before commit.**
