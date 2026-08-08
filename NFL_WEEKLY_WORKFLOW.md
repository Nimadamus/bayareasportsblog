# 49ers weekly content workflow — 2026 season

The season is a recurring system, not a batch. This is the loop, the commands, and the
rules that keep it from producing filler.

## The weekly loop

| When | Piece | Section | Notes |
|---|---|---|---|
| **Mon/Tue** | Reaction — what we learned | `49ers` | Written after the game, never before. Links to that week's preview and to the schedule hub. |
| **Mon/Tue** | Injury / roster update | `49ers` | **Only if something meaningful changed.** A questionable tag is not an article. Update `49ers-2026-roster-depth-chart.html` instead. |
| **Wed/Thu** | Storyline or analytical piece | `49ers` | The week's actual argument. This is the piece with backlink potential. |
| **Fri/Sat** | Game preview | `49ers` | Matchup, what to watch, the number that decides it. |
| **Postgame** | Takeaway piece | `49ers` | Only when the game genuinely produced one. |

**Ceiling: 3–4 pieces per game week.** More than that and they start cannibalising each
other for the same query.

## Non-negotiables

1. **Never write a reaction before the game.** Fabricating a result is worse than
   publishing nothing.
2. **One query, one page.** Before writing, check the archive for an existing piece
   targeting the same intent. If one exists, update it rather than publishing a rival.
3. **Every article links up to `../49ers.html`** and to at least one of the four season
   pages below.
4. **The four permanent pages get updated, not duplicated:**
   - `49ers-2026-season-preview-roster-schedule-questions.html`
   - `49ers-2026-schedule-season-hub.html` ← add each week's preview + reaction link here
   - `49ers-2026-roster-depth-chart.html` ← update on roster moves and injuries
   - `brock-purdy-career-passer-rating-where-he-ranks.html` ← update after the record
     qualifies, roughly game five
5. **Cards come from `tools/cardgen.py`** in the `49ers` palette. No stock photos.
6. **No thin pages.** Under ~500 words means it should have been an update to an
   existing page.

## Publishing commands

```bash
# 1. write the piece into the cluster script's ARTICLES list, then:
python _niners_cluster.py --check     # word count, link count, title/desc lengths
python _niners_cluster.py             # writes html + generates the card

# 2. regenerate the derivatives for the new card (400/600/800 jpg+webp)

# 3. feeds
python _gen_sitemap.py
python _gen_news_sitemap.py           # rolling 48h - this is what feeds Top Stories
python _gen_search_index.py
python _gen_feed.py

# 4. gates - all four must pass before commit
python tools/thumb_gate.py --site
python _meta_template.py --gate
python _sitemap_audit.py
python _seo_audit.py
```

## Why the news sitemap matters most in-season

`news-sitemap.xml` only carries what published in the **last 48 hours**. An empty rolling
window is the difference between appearing in Top Stories during a game week and not
appearing at all. This is the single strongest argument for holding cadence.

## Key 2026 dates

- **10 September** — Week 1 at the Rams, Melbourne Cricket Ground, 5:35pm PT Thursday
- **Week 2** — Miami at Levi's, short turnaround after Australia
- **Week 6** — Washington at Levi's, Monday night
- **Around game five** — Purdy passes 1,500 career attempts and qualifies for the career
  passer rating record. Update the Purdy page that week; it is the biggest single
  traffic event of the season.
- **Mexico City** — Minnesota at Estadio Banorte, a home game that is not at home
