#!/usr/bin/env python3
"""
bay_daily.py - Daily Bay Area Sports Update generator.

Pulls REAL data from ESPN public feeds for every Bay Area pro team and builds a
dated daily digest page (last game result, next game, record, latest news) plus a
Daily hub index. No fabrication: every score/date/headline comes from the live feed.

Usage:  python bay_daily.py
Output: daily/YYYY-MM-DD.html  +  daily/index.html   (in the bayareasportsblog repo)
"""
import json, os, sys, urllib.request, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
DAILY = os.path.join(ROOT, "daily")
UA = {"User-Agent": "Mozilla/5.0 (BayAreaSportsBlog daily digest)"}

# sport/league, ESPN team abbrev (schedule/team endpoints), ESPN news team id, display, accent
TEAMS = [
    ("football",  "nfl", "sf",  25, "San Francisco 49ers",   "#aa0000"),
    ("baseball",  "mlb", "sf",  26, "San Francisco Giants",   "#fd5a1e"),
    ("baseball",  "mlb", "ath", 11, "Athletics",              "#003831"),
    ("basketball","nba", "gs",   9, "Golden State Warriors",  "#1d428a"),
    ("hockey",    "nhl", "sj",  18, "San Jose Sharks",        "#006d75"),
]

def get(url):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.load(r)
    except Exception as e:
        print("  WARN fetch failed:", url, "->", e)
        return None

def esc(s):
    return (str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
            .replace('"',"&quot;"))

def score_of(comp):
    v = comp.get("score")
    if isinstance(v, dict):
        return v.get("value")
    try:
        return int(v)
    except Exception:
        return None

def last_and_next(sport, league, abbrev):
    """Return (last_completed_event, next_scheduled_event) from the team schedule."""
    d = get("https://site.api.espn.com/apis/site/v2/sports/%s/%s/teams/%s/schedule"
            % (sport, league, abbrev))
    last = nxt = None
    if not d:
        return last, nxt
    for ev in d.get("events", []):
        comp = (ev.get("competitions") or [{}])[0]
        completed = comp.get("status", {}).get("type", {}).get("completed", False)
        if completed:
            last = ev  # keep advancing; schedule is chronological -> last completed wins
        elif nxt is None:
            nxt = ev
    return last, nxt

def describe_last(ev, abbrev, display):
    comp = (ev.get("competitions") or [{}])[0]
    cs = comp.get("competitors", [])
    me = next((c for c in cs if c.get("team", {}).get("abbreviation", "").lower() == abbrev.lower()), None)
    opp = next((c for c in cs if c is not me), None)
    if not me or not opp:
        return None
    ms, os_ = score_of(me), score_of(opp)
    if ms is None or os_ is None:
        return None
    won = me.get("winner", ms > os_)
    home = me.get("homeAway") == "home"
    vs = "vs" if home else "at"
    oppname = opp.get("team", {}).get("displayName", "opponent")
    dt = ev.get("date", "")[:10]
    res = "beat" if won else "lost to"
    tag = "W" if won else "L"
    short = display.split()[-1]
    line = "%s %s %s %d-%d on %s." % (short, res, oppname, max(ms, os_), min(ms, os_), fmt_date(dt))
    return {"tag": tag, "won": won, "line": line, "score": "%d-%d" % (ms, os_),
            "vs": vs, "opp": oppname, "date": dt}

def describe_next(ev, abbrev):
    comp = (ev.get("competitions") or [{}])[0]
    cs = comp.get("competitors", [])
    me = next((c for c in cs if c.get("team", {}).get("abbreviation", "").lower() == abbrev.lower()), None)
    opp = next((c for c in cs if c is not me), None)
    if not opp:
        return None
    home = me and me.get("homeAway") == "home"
    vs = "vs" if home else "at"
    det = comp.get("status", {}).get("type", {}).get("shortDetail", "")
    return "%s %s (%s)" % (vs, opp.get("team", {}).get("displayName", "TBD"), det or ev.get("date","")[:10])

def record_of(sport, league, abbrev):
    d = get("https://site.api.espn.com/apis/site/v2/sports/%s/%s/teams/%s"
            % (sport, league, abbrev))
    try:
        return d["team"]["record"]["items"][0]["summary"]
    except Exception:
        return None

def news_of(sport, league, team_id, n=5):
    d = get("https://site.api.espn.com/apis/site/v2/sports/%s/%s/news?team=%d&limit=%d"
            % (sport, league, team_id, n))
    out = []
    if d:
        for a in d.get("articles", [])[:n]:
            h = a.get("headline")
            if h:
                out.append(h)
    return out

def fmt_date(iso):
    try:
        y, m, dd = iso.split("-")
        months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        return "%s %d" % (months[int(m)], int(dd))
    except Exception:
        return iso

NAV = """      <ul>
        <li><a href="{P}index.html">Home</a></li>
        <li><a class="{DA}" href="{P}daily/index.html">Daily</a></li>
        <li><a href="{P}49ers.html">49ers</a></li>
        <li><a href="{P}warriors.html">Warriors</a></li>
        <li><a href="{P}giants.html">Giants</a></li>
        <li><a href="{P}bayarea.html">Bay Area Sports</a></li>
        <li><a href="{P}history.html">History</a></li>
        <li><a href="{P}flashbacks.html">Flashbacks</a></li>
        <li><a href="{P}columns.html">Columns</a></li>
        <li><a href="{P}about.html">About</a></li>
        <li><a href="{P}contact.html">Contact</a></li>
      </ul>"""

def header(P, active_daily=False):
    return """<header class="site-header">
  <div class="wrap hdr-top">
    <a class="brand" href="{P}index.html">
      <span class="mark">BA</span>
      <span class="name">Bay Area <span>Sports Blog</span><small>49ers &middot; Warriors &middot; Giants &middot; A's &middot; Sharks</small></span>
    </a>
    <button class="nav-toggle" aria-label="Menu" onclick="document.querySelector('nav.main').classList.toggle('open')">&#9776;</button>
    <nav class="main">
{NAV}
    </nav>
  </div>
</header>""".format(P=P, NAV=NAV.format(P=P, DA="active" if active_daily else ""))

FOOT = """<footer class="site-footer">
  <div class="foot-bottom">&copy; 2026 Bay Area Sports Blog. All rights reserved. &middot; <a href="{P}index.html">Home</a> &middot; <a href="{P}daily/index.html">Daily</a> &middot; <a href="{P}about.html">About</a></div>
</footer>"""

def build_team_card(t):
    sport, league, abbrev, tid, display, accent = t
    print(" ", display)
    last_ev, next_ev = last_and_next(sport, league, abbrev)
    rec = record_of(sport, league, abbrev)
    news = news_of(sport, league, tid)
    last = describe_last(last_ev, abbrev, display) if last_ev else None
    nxt = describe_next(next_ev, abbrev) if next_ev else None
    h = ['<div class="dcard" style="border-top:3px solid %s">' % accent]
    h.append('<div class="dc-head"><h3>%s</h3>%s</div>'
             % (esc(display), ('<span class="rec">%s</span>' % esc(rec)) if rec else ""))
    if last:
        badge = '<span class="wl %s">%s</span>' % ("win" if last["won"] else "loss", last["tag"])
        h.append('<p class="dline">%s Last: %s</p>' % (badge, esc(last["line"])))
    if nxt:
        h.append('<p class="dline"><span class="nx">NEXT</span> %s</p>' % esc(nxt))
    if not last and not nxt:
        h.append('<p class="dline off">Offseason. Watching moves, signings, and camp news below.</p>')
    if news:
        h.append('<div class="dc-news"><span class="block-label">In the news</span><ul class="dnews">')
        for hd in news:
            h.append("<li>%s</li>" % esc(hd))
        h.append("</ul></div>")
    h.append("</div>")
    return "\n".join(h)

def build_digest(date_str, pretty):
    cards = "\n".join(build_team_card(t) for t in TEAMS)
    P = "../"
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Daily Bay Area Sports Update: {pretty} | Bay Area Sports Blog</title>
<meta name="description" content="Every Bay Area team in one place for {pretty}: 49ers, Giants, Athletics, Warriors, and Sharks. Latest game results, next games, records, and every roster and front-office move.">
<link rel="canonical" href="https://bayareasportsblog.com/daily/{date}.html">
<link rel="stylesheet" href="{P}assets/style.css">
</head>
<body>
{HEAD}
<section class="page-hero"><div class="wrap">
<span class="tag">Daily Update</span>
<h1>Around the Bay: {pretty}</h1>
<p>Every Bay Area team in one place. Latest results, the next game, records, and the roster and front-office moves that matter, refreshed daily.</p>
</div></section>
<section class="section"><div class="wrap">
<div class="dgrid">
{CARDS}
</div>
<p style="margin-top:26px;color:var(--muted);font-size:14px">Game results, schedules, and team news are compiled from live league data feeds. <a href="index.html" style="color:var(--accent2);font-weight:700">See all daily updates &rarr;</a></p>
</div></section>
{FOOT}
</body>
</html>""".format(pretty=esc(pretty), date=date_str, P=P,
                  HEAD=header(P, active_daily=True), CARDS=cards, FOOT=FOOT.format(P=P))
    os.makedirs(DAILY, exist_ok=True)
    with open(os.path.join(DAILY, date_str + ".html"), "w", encoding="utf-8") as f:
        f.write(html)
    return date_str + ".html"

def rebuild_index():
    files = sorted([f for f in os.listdir(DAILY)
                    if f.endswith(".html") and f != "index.html"], reverse=True)
    P = "../"
    rows = []
    for f in files:
        ds = f[:-5]
        rows.append('<a class="mini" href="%s"><div class="m-body"><div class="m-cat">Daily Update</div>'
                    '<h3>Around the Bay: %s</h3></div></a>' % (f, esc(pretty_of(ds))))
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Daily Bay Area Sports Updates | Bay Area Sports Blog</title>
<meta name="description" content="The daily Bay Area sports desk: every game, every result, every roster and front-office move for the 49ers, Giants, Athletics, Warriors, and Sharks.">
<link rel="canonical" href="https://bayareasportsblog.com/daily/index.html">
<link rel="stylesheet" href="{P}assets/style.css">
</head>
<body>
{HEAD}
<section class="page-hero"><div class="wrap">
<span class="tag">Daily</span>
<h1>Daily Bay Area Sports Updates</h1>
<p>One page, every Bay Area team, every day. Game results, next games, records, and every roster and front-office move for the 49ers, Giants, Athletics, Warriors, and Sharks.</p>
</div></section>
<section class="section"><div class="wrap">
<div class="mini-grid dindex">
{ROWS}
</div>
</div></section>
{FOOT}
</body>
</html>""".format(P=P, HEAD=header(P, active_daily=True), ROWS="\n".join(rows), FOOT=FOOT.format(P=P))
    with open(os.path.join(DAILY, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

def pretty_of(ds):
    try:
        y, m, d = ds.split("-")
        return datetime.date(int(y), int(m), int(d)).strftime("%A, %B %-d, %Y")
    except Exception:
        try:
            y, m, d = ds.split("-")
            return datetime.date(int(y), int(m), int(d)).strftime("%A, %B %d, %Y").replace(" 0", " ")
        except Exception:
            return ds

def main():
    today = datetime.date.today().isoformat() if len(sys.argv) < 2 else sys.argv[1]
    pretty = pretty_of(today)
    print("Building Daily Bay Area Update for", today)
    fn = build_digest(today, pretty)
    rebuild_index()
    print("Wrote daily/%s and rebuilt daily/index.html" % fn)

if __name__ == "__main__":
    main()
