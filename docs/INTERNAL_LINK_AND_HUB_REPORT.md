# Internal-link repair and hub-authority record

Rebuilt 2026-08-08 in the repo. Two Desktop documents covered this work —
`BAYAREA_SPORTS_BLOG_INTERNAL_LINK_REPAIR_REPORT.md` and
`BAYAREA_SPORTS_BLOG_HUB_AUTHORITY_UPGRADE_REPORT.md` — and both were lost. They were
**historical records of completed work**, not open task lists, so nothing is outstanding
because of the loss.

**The live state is machine-generated and committed to git.** Prefer these over any prose
summary, including this one:

| File | What it holds |
|---|---|
| `_seo_audit.json` | full crawl: link graph, inbound counts per page, orphans, near-orphans, broken links, schema and image checks |
| `_link_repair_report.json` | the internal-link repair pass and what it changed |
| `_league_links_report.json` | league-hub (`nfl` / `mlb` / `nba` / `nhl`) linking pass |

Regenerate the first with `python _seo_audit.py`.

---

## Current link-graph state (2026-08-08)

- 0 orphans
- 0 near-orphans (≤2 inbound)
- 0 broken internal links
- 4 articles with 0 in-body inbound links, all deliberate (listed in
  `docs/SEO_BASELINE_FROZEN.md`)

## Hub inventory

27 hubs. The team hubs (`49ers`, `warriors`, `giants`, `athletics`, `cal`, `stanford`)
each carry a hand-written nav block linking that cluster's permanent pages — see the
`<!-- ... nav -->` comment blocks for the pattern. The history hubs are `history.html`,
`dynasties.html`, `timeline.html`, `bayarea.html` and `flashbacks.html`.

`history.html` gained a fourth chapter, "The Reference Desk", with the Bay Area history
cluster. `bayarea.html` gained a "Bay Area history and reference" block and its ItemList
JSON-LD was extended from 3 to 7 items.

## Working rules

1. Every article links up to its hub and to at least one permanent page.
2. New pages routinely publish as near-orphans — re-run `_seo_audit.py` after every
   cluster and fix by linking from a sibling page where the reference is genuine.
3. Never force a link. If nothing on the site genuinely mentions a subject, the article
   keeps 0 in-body inbound links and gets recorded as deliberate.
4. `python _link_candidates.py --max 2` proposes inbound links for starved articles.

## GSC checklist (blocked, kept for when a credential exists)

Once a Search Console credential is available, run in this order:
1. Pages ranking 5–20 — the cheapest wins on the site.
2. High-impression / low-CTR pages — title and description rewrites.
3. Query cannibalisation — two pages competing for one query; consolidate, do not
   compete.
4. Index-coverage exclusions — anything crawled and not indexed.

The property is otherwise ready: verification file returns 200, both sitemaps are in
`robots.txt`.
