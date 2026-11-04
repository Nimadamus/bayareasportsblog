#!/usr/bin/env python3
"""Bay Area Hall of Fame: one page per inductee plus the hub.

Data lives in _hof/<slug>.json (shape in _hof/SCHEMA.md). Every fact in those files
was verified against a fetched source, listed in that file's "sources".

  python _gen_hall_of_fame.py          # writes /<slug>.html for every inductee + bay-area-hall-of-fame.html

Player pages sit at the site root so the URL is the player's name
(bayareasportsblog.com/barry-bonds.html). Photos are Wikimedia Commons, credited on the page.
"""
import glob, html, json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://bayareasportsblog.com"
TEAM = {
    "sf": "Giants", "as": "A's", "niners": "49ers", "gs": "Warriors", "sj": "Sharks",
    "lv": "Raiders", "cal": "Cal", "stanford": "Stanford",
}
TEAM_ORDER = ["sf", "niners", "gs", "as", "sj", "lv", "cal", "stanford"]
TEAM_LONG = {
    "sf": "San Francisco Giants", "as": "Oakland Athletics", "niners": "San Francisco 49ers",
    "gs": "Golden State Warriors", "sj": "San Jose Sharks", "lv": "Oakland Raiders",
    "cal": "Cal Golden Bears", "stanford": "Stanford Cardinal",
}
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;0,9..144,900;1,9..144,500;1,9..144,700;1,9..144,900&family=Archivo:wght@400;500;600;700;800&family=Archivo+Narrow:wght@500;600;700&display=swap">\n'
         '<link rel="stylesheet" href="assets/desk.css">')

e = lambda s: html.escape(str(s or ""), quote=True)


def load():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "_hof", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        d.setdefault("sort", 999)
        ph = (d.get("photo") or {}).get("file")
        if d.get("hold") or not ph or not os.path.exists(os.path.join(ROOT, ph)):
            print("HELD (no photo yet):", d["slug"])
            continue
        out.append(d)
    out.sort(key=lambda d: (d["sort"], d["name"]))
    return out


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


def head(title, desc, url, image, ldjson, ogtype="website"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
{FONTS}
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<link rel="alternate" type="application/rss+xml" title="Bay Area Sports Blog" href="{SITE}/feed.xml">
<meta property="og:site_name" content="Bay Area Sports Blog">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{ogtype}">
<meta property="og:title" content="{e(title.split(' | ')[0])}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="675">
<meta property="og:image:alt" content="Bay Area Sports Blog: {e(title.split(' | ')[0])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title.split(' | ')[0])}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{image}">
{ldjson}
<style>{CSS}</style>
</head>
<body>
"""


CHROME_TOP = """
<div class="desk-top" role="region" aria-label="Today and quick links">
  <div class="wrap">
    <div><b class="dt-live" data-dt="live">&nbsp;</b> &middot; San Francisco</div>
    <div class="dt-r" role="navigation" aria-label="Quick links">
      <a href="blog.html">Latest</a>
      <a href="columns.html">Columns</a>
      <a href="timeline.html">Timeline</a>
      <a href="search.html">Search</a>
      <a href="about.html">About</a>
    </div>
  </div>
</div>

<header class="masthead">
  <div class="wrap">
    <div class="mh-rule">
      <em>Est. by a fan, not a network</em>
      <span></span>
      <em>No wire copy. No neutrality.</em>
    </div>
    <a class="wordmark" href="index.html">Bay Area<br><i>Sports Blog</i></a>
  </div>
</header>

<nav class="teamnav">
  <div class="wrap">
    <a data-t="house" href="index.html">Home</a>
    <a data-t="niners" href="49ers.html">49ers</a>
    <a data-t="gs" href="warriors.html">Warriors</a>
    <a data-t="sf" href="giants.html">Giants</a>
    <a data-t="as" href="athletics.html">A's</a>
    <a data-t="sj" href="sharks.html">Sharks</a>
    <a data-t="lv" href="bayarea.html">Bay Area</a>
    <span class="nv-sp"></span>
    <a data-t="house" href="history.html">History</a>
    <a class="on" data-t="house" href="bay-area-hall-of-fame.html">Hall of Fame</a>
    <a data-t="house" href="dynasties.html">Dynasties</a>
    <a data-t="house" href="timeline.html">Timeline</a>
    <a data-t="house" href="blog.html">Blog</a>
  </div>
</nav>
"""

CHROME_BOTTOM = """
<footer class="desk-foot">
  <div class="wrap">
    <div class="df-top">
      <div>
        <div class="wm">Bay Area <i>Sports Blog</i></div>
        <p>49ers, Warriors, Giants, A's, Sharks and Bay Area sports commentary.</p>
      </div>
      <div class="df-col">
        <h5 role="heading" aria-level="4">Teams</h5>
        <a href="49ers.html">49ers</a>
        <a href="warriors.html">Warriors</a>
        <a href="giants.html">Giants</a>
        <a href="athletics.html">A's</a>
        <a href="sharks.html">Sharks</a>
      </div>
      <div class="df-col">
        <h5>Archive</h5>
        <a href="dynasties.html">Dynasties</a>
        <a href="timeline.html">Timeline</a>
        <a href="blog.html">Blog</a>
        <a href="columns.html">Opinion</a>
        <a href="about.html">About</a>
      </div>
      <div class="df-col">
        <h5>The Vault</h5>
        <a href="bay-area-hall-of-fame.html">Bay Area Hall of Fame</a>
        <a href="history.html">Bay Area History</a>
        <a href="flashbacks.html">Flashbacks</a>
        <a href="bayarea.html">Bay Area Hub</a>
      </div>
    </div>
    <div class="df-bot">
      <div>&copy; 2026 Bay Area Sports Blog. All rights reserved.</div>
      <div><a href="about.html">About</a> &middot; <a href="contact.html">Contact</a> &middot; <a href="editorial-standards.html">Standards</a> &middot; <a href="corrections.html">Corrections</a> &middot; <a href="privacy.html">Privacy</a></div>
    </div>
  </div>
</footer>
<script>
(function(){
  var e=document.querySelectorAll('[data-dt="live"]'),t=new Date().toLocaleDateString("en-US",{timeZone:"America/Los_Angeles",weekday:"long",month:"long",day:"numeric",year:"numeric"});
  for(var i=0;i<e.length;i++)e[i].textContent=t;
  document.querySelectorAll('.yt').forEach(function(b){b.addEventListener('click',function(){
    var f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+b.dataset.id+'?autoplay=1&rel=0';
    f.title=b.getAttribute('aria-label');f.allow='accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
    f.allowFullscreen=true;b.replaceWith(f);});});
})();
</script>
</body>
</html>
"""

CSS = """
.hof-hero{position:relative;padding:44px 0 40px;border-bottom:1px solid var(--rule);overflow:hidden}
.hof-hero:after{content:"";position:absolute;left:0;right:0;bottom:0;height:4px;background:var(--th)}
.hof-grid{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:44px;align-items:center}
.hof-photo{margin:0;border:1px solid var(--rule2);background:#000;position:relative}
.hof-photo img{display:block;width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;object-position:50% 22%}
.hof-photo figcaption{font-size:12px;color:var(--dim);padding:9px 12px;background:var(--paper);line-height:1.5}
.hof-photo figcaption a{color:var(--muted);text-decoration:underline}
.hof-k{font-family:var(--cond);font-size:13px;letter-spacing:.3em;text-transform:uppercase;color:var(--th);font-weight:700}
.hof-k a{color:inherit}
.hof-hero h1{font-family:var(--display);font-weight:900;font-size:clamp(44px,6.4vw,84px);line-height:.95;letter-spacing:-.02em;margin:12px 0 0;text-transform:none}
.hof-nick{font-family:var(--display);font-style:italic;font-size:22px;color:var(--gold);margin-top:10px}
.hof-dek{font-size:18px;line-height:1.6;color:#d8d4c6;margin-top:18px;max-width:58ch;font-style:italic}
.hof-meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}
.hof-meta span{font-family:var(--cond);font-size:12px;letter-spacing:.16em;text-transform:uppercase;border:1px solid var(--rule2);padding:6px 10px;color:var(--text)}
.hof-tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin-top:26px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.hof-tiles div{padding:16px 14px 14px;border-right:1px solid var(--rule)}
.hof-tiles div:last-child{border-right:0}
.hof-tiles b{display:block;font-family:var(--display);font-weight:900;font-style:italic;font-size:34px;line-height:1;color:var(--th)}
.hof-tiles span{display:block;margin-top:8px;font-family:var(--cond);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);line-height:1.35}
.hof-body{max-width:780px}
.hof-two{display:grid;grid-template-columns:minmax(0,780px) minmax(0,1fr);gap:56px;align-items:start}
.hof-aside{position:sticky;top:76px;background:var(--paper);border:1px solid var(--rule2);border-top:3px solid var(--th);padding:22px 22px 18px}
.hof-aside h3{font-family:var(--cond);font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:var(--th);margin:0 0 12px}
.hof-aside dl{display:grid;grid-template-columns:auto 1fr;gap:8px 14px;margin:0 0 20px;font-size:14.5px}
.hof-aside dt{color:var(--muted);font-family:var(--cond);letter-spacing:.08em;text-transform:uppercase;font-size:12px;padding-top:2px}
.hof-aside dd{margin:0;color:var(--text)}
.hof-aside ul{margin:0;padding:0 0 0 16px}
.hof-aside li{font-size:14.5px;line-height:1.5;color:#e0dccf;margin-bottom:7px}
.hof-aside .hq{border:0;padding:0;background:none}
.hof-aside.pull{padding:26px 24px 22px}
.hof-body p{font-size:18px;line-height:1.75;color:#e6e2d6;margin:0 0 1.15em}
.hof-sec{padding:50px 0}
.hof-sec + .hof-sec{border-top:1px solid var(--rule)}
.moments{list-style:none;margin:0;padding:0;display:grid;gap:26px}
.moment{display:grid;grid-template-columns:150px minmax(0,1fr);gap:26px;border-left:3px solid var(--th);padding:4px 0 4px 22px}
.moment .m-date{font-family:var(--cond);font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--th);font-weight:700;line-height:1.4}
.moment h3{font-family:var(--display);font-size:24px;font-weight:700;line-height:1.2;text-transform:none;margin:0 0 10px}
.moment p{font-size:17px;line-height:1.7;color:#e0dccf;margin:0 0 .9em}
.yt{position:relative;display:block;width:100%;aspect-ratio:16/9;border:1px solid var(--rule2);background:#000 center/cover no-repeat;cursor:pointer;padding:0}
.yt:before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.05),rgba(0,0,0,.55))}
.yt .play{position:absolute;left:50%;top:50%;width:68px;height:48px;margin:-24px 0 0 -34px;background:#e62117;border-radius:12px}
.yt .play:after{content:"";position:absolute;left:27px;top:14px;border-style:solid;border-width:10px 0 10px 17px;border-color:transparent transparent transparent #fff}
.yt .yt-t{position:absolute;left:14px;right:14px;bottom:12px;color:#fff;font-weight:700;font-size:15px;text-align:left;line-height:1.3;text-shadow:0 1px 3px #000}
iframe{display:block;width:100%;aspect-ratio:16/9;border:0}
.moment .yt,.moment iframe{max-width:640px;margin-top:6px}
.vids{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}
.vids figure{margin:0}
.vids figcaption{font-size:13px;color:var(--muted);margin-top:8px}
.gal{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:22px}
.gal figure{margin:0}
.gal img{display:block;width:100%;height:360px;object-fit:cover;border-radius:4px;background:var(--paper)}
.gal figcaption{font-size:13px;color:var(--muted);margin-top:8px;line-height:1.45}
.gal figcaption a{color:inherit;text-decoration:underline}
.gal.one{grid-template-columns:minmax(0,680px)}
.gal.one img{height:auto}
.quotes{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}
.hq{margin:0;background:var(--paper);border:1px solid var(--rule2);border-top:3px solid var(--th);padding:24px 24px 20px}
.hq p{font-family:var(--display);font-style:italic;font-size:21px;line-height:1.45;color:var(--text);margin:0}
.hq footer{margin-top:16px;font-size:14px;color:var(--muted);line-height:1.5}
.hq footer b{color:var(--text);font-weight:700}
.stats-wrap{overflow-x:auto;border:1px solid var(--rule2);-webkit-overflow-scrolling:touch}
table.stats{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums;font-size:14px;white-space:nowrap}
table.stats th{font-family:var(--cond);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);text-align:right;padding:10px 12px;border-bottom:1px solid var(--rule2);background:var(--paper2);position:sticky;top:0}
table.stats td{text-align:right;padding:8px 12px;border-bottom:1px solid var(--rule);color:#d9d5c8}
table.stats th:nth-child(-n+2),table.stats td:nth-child(-n+2){text-align:left}
table.stats tr.bay td{color:var(--text);background:color-mix(in srgb,var(--th) 9%,transparent)}
table.stats tr.bay td:first-child{box-shadow:inset 3px 0 0 var(--th)}
table.stats tr.car td{font-weight:800;color:var(--text);border-top:2px solid var(--th);background:var(--paper2)}
.stats-note{font-size:13px;color:var(--dim);margin-top:10px}
.honors{columns:2;column-gap:40px;margin:0;padding:0 0 0 18px}
.honors li{font-size:16.5px;line-height:1.6;color:#e0dccf;margin-bottom:8px;break-inside:avoid}
.hof-next{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.hof-next a{display:block;border:1px solid var(--rule2);padding:18px 20px;background:var(--paper)}
.hof-next a:hover{border-color:var(--th)}
.hof-next small{display:block;font-family:var(--cond);font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}
.hof-next b{display:block;font-family:var(--display);font-size:22px;margin-top:6px}
.hof-next a:last-child{text-align:right}
.hof-rel{display:flex;flex-wrap:wrap;gap:12px 26px;margin-top:20px}
.hof-rel a{color:var(--gold);font-weight:600;border-bottom:1px solid rgba(233,200,130,.44)}
.plate.hof .pl-img{aspect-ratio:4/5}
.plate.hof .pl-img img{filter:none;height:100%;object-position:50% 20%}
.plate.hof .pl-nick{font-family:var(--display);font-style:italic;color:var(--muted);font-size:15px}
.hof-team{--th:var(--gold)}
.plate[data-c=lv]{--th:var(--lv)}
.hof-jump{position:sticky;top:var(--navh,52px);z-index:55;background:rgba(9,14,13,.94);backdrop-filter:blur(6px);border-bottom:1px solid var(--rule)}
.hof-jump .wrap{display:flex;gap:10px;align-items:center;padding-top:12px;padding-bottom:12px;overflow-x:auto;scrollbar-width:none}
.hof-jump .wrap::-webkit-scrollbar{display:none}
.hof-jump a{flex:0 0 auto;display:inline-flex;gap:8px;align-items:center;border:1px solid var(--rule2);padding:8px 13px;
  font-family:var(--cond);font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#e9e6da}
.hof-jump a:hover{border-color:var(--th);color:#fff}
.hof-jump a i{font-style:normal;color:var(--th);font-weight:800}
.hof-find{flex:1 0 200px;max-width:320px;margin-left:auto;background:var(--paper);border:1px solid var(--rule2);color:#fff;
  font:inherit;font-size:14px;padding:9px 12px}
.hof-find:focus{outline:2px solid var(--gold);outline-offset:1px}
.hof-none{display:none;padding:40px 0;color:var(--muted);font-size:16px}
.chapter[id]{scroll-margin-top:130px}
.ch-count{font-family:var(--cond);font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);align-self:end}
.hof-new{padding:40px 0 10px}
.hof-more{margin-top:40px}
.hof-more .plates{margin-top:18px}
.faq{max-width:820px;border-top:1px solid var(--rule)}
.faq details{border-bottom:1px solid var(--rule);padding:16px 0}
.faq summary{cursor:pointer;font-family:var(--display);font-weight:700;font-size:19px;list-style:none;padding-right:30px;position:relative}
.faq summary::-webkit-details-marker{display:none}
.faq summary:after{content:"+";position:absolute;right:4px;top:0;color:var(--th);font-weight:900}
.faq details[open] summary:after{transform:rotate(45deg)}
.faq p{margin-top:10px;color:#d6d3c6;font-size:16px;line-height:1.65}
@media(max-width:460px){.plates.hofp{grid-template-columns:1fr 1fr;gap:10px}.plates.hofp .plate.hof .pl-b{padding:10px 10px 12px;gap:4px}.plates.hofp .plate.hof h3{font-size:15px}.plates.hofp .plate .pl-yr{font-size:9.5px;letter-spacing:.14em}.plates.hofp .plate .stamp{font-size:9.5px;padding:4px 7px}.plates.hofp .plate.hof .pl-nick{font-size:13px}}
.hof-more .ch-k{font-family:var(--cond);font-size:12px;letter-spacing:.3em;text-transform:uppercase;color:var(--th)}
.hof-more-h{font-family:var(--display);font-weight:900;font-size:clamp(26px,3vw,36px);text-transform:none;margin-top:6px}
[data-c=sf]{--th:var(--sf)} [data-c=niners]{--th:var(--niners)} [data-c=gs]{--th:var(--gs)}
[data-c=as]{--th:var(--as)} [data-c=sj]{--th:var(--sj)} [data-c=lv]{--th:var(--lv)}
[data-c=cal],[data-c=stanford],[data-c=house]{--th:var(--gold)}
@media(max-width:900px){
 .hof-grid{grid-template-columns:1fr;gap:26px}
 .hof-photo{max-width:440px}
 .quotes,.vids{grid-template-columns:1fr}
 .gal img{height:auto;max-height:520px}
 .honors{columns:1}
 .hof-two{grid-template-columns:1fr;gap:30px}
 .hof-aside{position:static}
}
@media(max-width:640px){
 .hof-hero{padding:26px 0 30px}
 .hof-tiles{grid-template-columns:repeat(2,1fr)}
 .hof-tiles div:nth-child(2){border-right:0}
 .hof-tiles div:nth-child(-n+2){border-bottom:1px solid var(--rule)}
 .hof-tiles b{font-size:28px}
 .hof-body p{font-size:17px}
 .moment{grid-template-columns:1fr;gap:6px;padding-left:16px}
 .moment h3{font-size:21px}
 .hq p{font-size:19px}
 .hof-next{grid-template-columns:1fr}
 .hof-next a:last-child{text-align:left}
 .hof-sec{padding:38px 0}
 .hof-find{flex-basis:170px;order:-1;margin-left:0}
}
"""


def fmt_date(iso):
    import datetime
    try:
        d = datetime.date.fromisoformat(iso)
        return d.strftime("%B ") + str(d.day) + d.strftime(", %Y")
    except Exception:
        return iso


def yt(v, label):
    vid = e(v["id"])
    t = e(v.get("title") or label)
    return (f'<button class="yt" type="button" data-id="{vid}" aria-label="Play video: {t}" '
            f'style="background-image:url(https://i.ytimg.com/vi/{vid}/hqdefault.jpg)">'
            f'<span class="play"></span><span class="yt-t">{t}</span></button>')


def chapter(num, kicker, title, body, sub=""):
    sub_html = f'<div class="ch-sub">{e(sub)}</div>' if sub else ""
    return f"""
<section class="hof-sec">
  <div class="wrap">
    <div class="ch-head">
      <div class="ch-num">{num}</div>
      <div>
        <div class="ch-k">{e(kicker)}</div>
        <h2>{e(title)}</h2>{sub_html}
      </div>
    </div>
    {body}
  </div>
</section>"""


def photo_src(d):
    return d["photo"]["file"].replace("\\", "/")


def card_path(d):
    return f"assets/img/cards/hof-{d['slug']}.jpg"


def make_card(d):
    """1200x675 social card: the whole real portrait, no baked text, centred on the player's face,
    set on a soft blurred continuation of the same photo so every listing crop keeps the face."""
    from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import photo_cards
    src = os.path.join(ROOT, d.get("card_photo") or photo_src(d))
    dst = os.path.join(ROOT, card_path(d))
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src) and not os.environ.get("HOF_RECARD"):
        return
    if d.get("card_mode") == "tight":      # tight face crop, for photos with lettering in the background
        photo_cards.render(os.path.relpath(src, ROOT).replace(os.sep, "/"), dst)
        print("card", d["slug"], "tight")
        return
    W, H = 1200, 675
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    ph = im.resize((max(1, round(im.width * H / im.height)), H), Image.LANCZOS)
    if ph.width > W:                      # landscape source: crop to the card, face centred
        ph = ph.crop(((ph.width - W) // 2, 0, (ph.width - W) // 2 + W, H))
    cx = ph.width / 2.0
    fs = [f for f in photo_cards.faces(ph) if f[2] >= ph.width * 0.10 and f[1] + f[3] / 2 < H * 0.7]
    if fs:
        cx = fs[0][0] + fs[0][2] / 2.0
    x0 = int(round(W / 2.0 - cx))
    bg = im.resize((W, max(H, round(im.height * W / im.width))), Image.BILINEAR)
    bg = bg.crop((0, (bg.height - H) // 4, W, (bg.height - H) // 4 + H)).filter(ImageFilter.GaussianBlur(38))
    bg = ImageEnhance.Brightness(bg).enhance(0.5)
    mask = Image.new("L", ph.size, 255)
    md = ImageDraw.Draw(mask)
    fe = max(10, ph.width // 30)
    for i in range(fe):
        v = int(255 * i / fe)
        md.line([(i, 0), (i, H)], fill=v)
        md.line([(ph.width - 1 - i, 0), (ph.width - 1 - i, H)], fill=v)
    bg.paste(ph, (x0, 0), mask if ph.width < W else None)
    ImageEnhance.Sharpness(bg).enhance(1.05).save(dst, "JPEG", quality=90, optimize=True, progressive=True)
    print("card", d["slug"], "face" if fs else "centre", f"x0 {x0}")


SPORT = {"sf": "Baseball", "as": "Baseball", "niners": "American football", "lv": "American football",
         "gs": "Basketball", "sj": "Ice hockey", "cal": "", "stanford": ""}
PROFILE_RE = re.compile(r"^https://(www\.)?(baseball-reference\.com/(players|managers)/|pro-football-reference\.com/(players|coaches)/|"
                        r"basketball-reference\.com/(players|coaches)/|hockey-reference\.com/players/|baseballhall\.org/hall-of-famers/|"
                        r"profootballhof\.com/players/|hoophall\.com/hall-of-famers/|hhof\.com/)", re.I)


def same_as(d):
    """Authoritative profile URLs for this person, taken only from the verified sources list."""
    from urllib.parse import unquote
    out = []
    for u in d.get("sources", []):
        if "web.archive.org" in u or "#" in u:
            continue
        if "wikipedia.org/wiki/" in u:
            t = unquote(u.rsplit("/wiki/", 1)[1]).replace("_", " ")
            if re.sub(r"\s*\(.*\)$", "", t).strip().lower() != d["name"].lower():
                continue
        elif not PROFILE_RE.match(u):
            continue
        if u not in out:
            out.append(u)
    return out[:8]


def license_url(lic):
    m = re.match(r"\s*CC\s*BY(-SA)?\s*(\d\.\d)", lic or "", re.I)
    if m:
        return f"https://creativecommons.org/licenses/by{'-sa' if m.group(1) else ''}/{m.group(2)}/"
    if re.match(r"\s*CC0", lic or "", re.I):
        return "https://creativecommons.org/publicdomain/zero/1.0/"
    if re.match(r"\s*(public domain|pd)", lic or "", re.I):
        return "https://creativecommons.org/publicdomain/mark/1.0/"
    return ""


def faq_items(d, team):
    """Plain answers built only from the page's own verified data."""
    name, last = d["name"], d["name"].split()[-1]
    long_team = d.get("team") or TEAM_LONG.get(d["team_key"], team)
    pos = (d.get("position") or "").lower()
    items = []
    active = (d.get("bay_years") or "").endswith("present")
    if d.get("bay_years"):
        noun = {"left field": "left fielder", "center field": "center fielder", "right field": "right fielder",
                "first base": "first baseman", "second base": "second baseman", "third base": "third baseman"}.get(pos, pos)
        if noun in ("manager", "head coach"):
            role = f" as {noun}"
        elif noun:
            role = f", playing {noun}" if " and " in noun else f" as {'an' if noun[0] in 'aeiou' else 'a'} {noun}"
        else:
            role = ""
        yrs = d.get("team_years") or d["bay_years"]
        if ", " in yrs:
            n = yrs.count(", ") + 1
            when = f"over {n} stints ({yrs.rsplit(', ', 1)[0]} and {yrs.rsplit(', ', 1)[1]})"
        elif yrs.endswith(" to present"):
            when = f"since {yrs[:-11]}"
        else:
            when = f"from {yrs}"
        items.append((f"What years was {name} with the {long_team}?",
                      f"{name} {'has been' if when.startswith('since') else 'was'} with the {long_team} {when}{role}."))
    if d.get("numbers"):
        nums = d["numbers"]
        items.append((f"What number did {name} wear?",
                      f"{name} {'wears' if active else 'wore'} number{'s' if ',' in nums else ''} {nums}."))
    if d.get("tiles"):
        lc = lambda x: x[0].lower() + x[1:] if len(x) > 1 and x[1].islower() else x
        parts = [f"{t['value']} {lc(t['label'])}" for t in d["tiles"][:4]]
        items.append((f"What are {name}'s signature numbers?", "; ".join(parts) + "."))
    if d.get("honors"):
        items.append((f"What were {name}'s biggest honors?", "; ".join(d["honors"][:5]) + "."))
    if d.get("clutch_moments"):
        ms = d["clutch_moments"][:3]
        items.append((f"What are some of {last}'s biggest moments?",
                      "; ".join(f"{m['headline']} ({fmt_date(m['date'])})" for m in ms) + ". Every one is in the Clutch Moments section above."))
    return items


def faq_html(items):
    return '<div class="faq">' + "".join(
        f'<details{" open" if i == 0 else ""}><summary>{e(q)}</summary><p>{e(a)}</p></details>' for i, (q, a) in enumerate(items)) + "</div>"


def player_page(d, prev, nxt, players=()):
    slug, name, key = d["slug"], d["name"], d["team_key"]
    team = TEAM.get(key, d.get("team", ""))
    url = f"{SITE}/{slug}.html"
    title = d.get("seo_title") or f"{name}: {team} Legend, Stats and Clutch Moments"
    if len(title) > 62:
        title = f"{name}: {team} Stats and Clutch Moments"
    desc = d["meta_description"]
    image = f"{SITE}/{card_path(d)}"
    p = d["photo"]
    person = {"@type": "Person", "name": name, "image": f"{SITE}/{photo_src(d)}",
              "description": desc, "affiliation": {"@type": "SportsTeam", "name": d.get("team") or TEAM_LONG.get(key, team)}}
    if d.get("nickname"):
        person["alternateName"] = d["nickname"]
    person["url"] = url
    if d.get("position"):
        person["jobTitle"] = d["position"]
    person["memberOf"] = {"@type": "SportsTeam", "name": d.get("team") or TEAM_LONG.get(key, team),
                          "sport": SPORT.get(key, "")}
    if d.get("honors"):
        person["award"] = d["honors"][:12]
    same = same_as(d)
    if same:
        person["sameAs"] = same
    img = {"@type": "ImageObject", "url": f"{SITE}/{photo_src(d)}", "caption": d["photo"].get("caption") or name}
    if d["photo"].get("author"):
        img["creditText"] = d["photo"]["author"]
        img["creator"] = {"@type": "Person", "name": d["photo"]["author"]}
    lic = license_url(d["photo"].get("license"))
    if lic:
        img["license"] = lic
    if d["photo"].get("commons_page"):
        img["acquireLicensePage"] = d["photo"]["commons_page"]
    person["image"] = img
    faq = faq_items(d, team)
    ld = jsonld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Bay Area Hall of Fame", "item": f"{SITE}/bay-area-hall-of-fame.html"},
        {"@type": "ListItem", "position": 3, "name": name, "item": url}]}) + "\n" + jsonld(
        {"@context": "https://schema.org", "@type": "ProfilePage", "name": title.split(" | ")[0], "url": url,
         "dateCreated": d.get("inducted"), "dateModified": d.get("verified_on"), "mainEntity": person,
         "isPartOf": {"@type": "CollectionPage", "name": "Bay Area Hall of Fame", "url": f"{SITE}/bay-area-hall-of-fame.html"}})
    if faq:
        ld += "\n" + jsonld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})

    tiles = "".join(f'<div><b>{e(t["value"])}</b><span>{e(t["label"])}</span></div>' for t in d["tiles"][:4])
    meta = "".join(f"<span>{e(x)}</span>" for x in [d.get("position"), d.get("bay_years"),
                                                   ("No. " + d["numbers"]) if d.get("numbers") else ""] if x)
    credit = e(p.get("caption"))
    if p.get("commons_page"):
        credit += (f' Photo: {e(p.get("author"))}, <a href="{e(p.get("commons_page"))}" rel="nofollow noopener" '
                   f'target="_blank">{e(p.get("license"))}</a>, via Wikimedia Commons.')
    nick = f'<div class="hof-nick">&ldquo;{e(d["nickname"])}&rdquo;</div>' if d.get("nickname") else ""

    hero = f"""
<section class="hof-hero" data-c="{key}">
  <div class="wrap hof-grid">
    <figure class="hof-photo">
      <img src="{photo_src(d)}" alt="{e(p.get('alt') or name)}" width="900" height="1125" fetchpriority="high" decoding="async">
      <figcaption>{credit}</figcaption>
    </figure>
    <div>
      <div class="hof-k"><a href="bay-area-hall-of-fame.html">Bay Area Hall of Fame</a> &middot; {e(team)}</div>
      <h1>{e(d.get("display_name") or name)}</h1>{"" if d.get("display_name") else nick}
      <p class="hof-dek">{e(d["dek"])}</p>
      <div class="hof-meta">{meta}</div>
      <div class="hof-tiles">{tiles}</div>
    </div>
  </div>
</section>"""

    secs, n = [], 0

    def nxtnum():
        nonlocal n
        n += 1
        return f"{n:02d}"

    glance = "".join(f"<dt>{k}</dt><dd>{e(v)}</dd>" for k, v in [
        ("Team", d.get("team")), ("Position", d.get("position")), ("Years", d.get("bay_years")),
        ("Number", d.get("numbers"))] if v)
    aside = (f'<aside class="hof-aside"><h3>At a Glance</h3><dl>{glance}</dl><h3>Honors and Records</h3><ul>'
             + "".join(f"<li>{e(h)}</li>" for h in d["honors"]) + "</ul></aside>")
    secs.append(chapter(nxtnum(), "The Story", f"The {name} Story",
                        '<div class="hof-two"><div class="hof-body">' + "".join(f"<p>{e(x)}</p>" for x in d["bio"]) + "</div>" + aside + "</div>"))
    if d.get("our_take"):
        secs.append(chapter(nxtnum(), "From the Stands", "What He Meant to Us",
                            '<div class="hof-body">' + "".join(f"<p>{e(x)}</p>" for x in d["our_take"]) + "</div>"))
    if d.get("gallery"):
        figs = []
        for g in d["gallery"]:
            cr = e(g.get("caption"))
            if g.get("commons_page"):
                cr += (f' Photo: {e(g.get("author"))}, <a href="{e(g["commons_page"])}" rel="nofollow noopener" '
                       f'target="_blank">{e(g.get("license"))}</a>, via Wikimedia Commons.')
            figs.append(f'<figure><img src="{e(g["file"])}" alt="{e(g.get("alt"))}" width="{g.get("w", 1000)}" height="{g.get("h", 750)}" '
                        f'loading="lazy" decoding="async" style="object-position:{e(g.get("pos", "center 30%"))}"><figcaption>{cr}</figcaption></figure>')
        secs.append(chapter(nxtnum(), "The Photo Album", "In Pictures", f'<div class="gal{" one" if len(figs) == 1 else ""}">{"".join(figs)}</div>'))
    def hq(q):
        return (f'<blockquote class="hq"><p>&ldquo;{e(q["text"])}&rdquo;</p><footer><b>{e(q["speaker"])}</b>'
                f'{", " + e(q["role"]) if q.get("role") else ""}{"<br>" + e(q["context"]) if q.get("context") else ""}</footer></blockquote>')
    quotes = list(d["quotes"])
    pull = quotes.pop(0) if len(quotes) > 2 else None
    side = f'<aside class="hof-aside pull">{hq(pull)}</aside>' if pull else ""
    secs.append(chapter(nxtnum(), "Under Pressure", "Why He Was Clutch",
                        '<div class="hof-two"><div class="hof-body">' + "".join(f"<p>{e(x)}</p>" for x in d["why_clutch"]) + "</div>" + side + "</div>"))
    used = set()
    items = []
    for m in d["clutch_moments"]:
        vid = ""
        if m.get("video_id"):
            v = next((v for v in d.get("videos", []) if v["id"] == m["video_id"]), {"id": m["video_id"], "title": m["headline"]})
            vid = yt(v, m["headline"])
            used.add(m["video_id"])
        paras = m["text"] if isinstance(m["text"], list) else [m["text"]]
        items.append(f'<li class="moment"><div class="m-date">{e(fmt_date(m["date"]))}</div><div>'
                     f'<h3>{e(m["headline"])}</h3>' + "".join(f"<p>{e(x)}</p>" for x in paras) + vid + "</div></li>")
    secs.append(chapter(nxtnum(), "The Big Moments", "Clutch Moments", f'<ol class="moments">{"".join(items)}</ol>'))
    rest = [v for v in d.get("videos", []) if v["id"] not in used]
    if rest:
        vids = "".join(f'<figure>{yt(v, v.get("title", ""))}<figcaption>{e(v.get("title"))} &middot; {e(v.get("channel"))}</figcaption></figure>' for v in rest)
        secs.append(chapter(nxtnum(), "Watch It Again", "The Highlights", f'<div class="vids">{vids}</div>'))
    qs = "".join(hq(q) for q in quotes)
    secs.append(chapter(nxtnum(), "In Their Words", f"What They Said About {name.split()[-1]}", f'<div class="quotes">{qs}</div>'))

    st = d["stats"]
    bay = set(st.get("bay_teams", []))
    ti = st["columns"].index("Team") if "Team" in st["columns"] else 1
    th = "".join(f'<th scope="col">{e(c)}</th>' for c in st["columns"])
    rows = "".join(f'<tr{" class=bay" if r[ti] in bay else ""}>' + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in st["rows"])
    if st.get("career"):
        rows += '<tr class="car">' + "".join(f"<td>{e(c)}</td>" for c in st["career"]) + "</tr>"
    grp = st.get("label") or ("batting" if st.get("group") == "hitting" else "pitching")
    stats = (f'<div class="stats-wrap"><table class="stats"><caption class="sr-only" style="position:absolute;left:-9999px">{e(name)} career {grp} stats by season</caption>'
             f'<thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>'
             f'<p class="stats-note">{e(st.get("note") or "Regular season. Highlighted rows are his Bay Area seasons.")} Scroll the table sideways on a phone.</p>')
    for extra in st.get("extra_tables", []):
        xth = "".join(f'<th scope="col">{e(c)}</th>' for c in extra["columns"])
        xi = extra["columns"].index("Team") if "Team" in extra["columns"] else 1
        xrows = "".join(f'<tr{" class=bay" if len(r) > xi and r[xi] in bay else ""}>' + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in extra["rows"])
        if extra.get("career"):
            xrows += '<tr class="car">' + "".join(f"<td>{e(c)}</td>" for c in extra["career"]) + "</tr>"
        stats += (f'<h3 class="ch-k" style="margin:30px 0 12px">{e(extra["title"])}</h3><div class="stats-wrap"><table class="stats">'
                  f'<thead><tr>{xth}</tr></thead><tbody>{xrows}</tbody></table></div>')
    secs.append(chapter(nxtnum(), "By the Numbers", "Career Stats", stats))
    if faq:
        secs.append(chapter(nxtnum(), "Quick Answers", f"{name}: Fast Facts", faq_html(faq)))
    rel = ""
    if d.get("related_articles"):
        links = []
        for a in d["related_articles"]:
            fp = os.path.join(ROOT, a)
            if not os.path.exists(fp):
                continue
            m = re.search(r"<h1[^>]*>(.*?)</h1>", open(fp, encoding="utf-8").read(), re.S)
            links.append(f'<a href="{e(a)}">{re.sub("<[^>]+>", "", m.group(1)).strip() if m else e(a)}</a>')
        if links:
            rel = '<h3 class="ch-k" style="margin-top:34px">Keep reading</h3><div class="hof-rel">' + "".join(links) + "</div>"
    nav = (f'<div class="hof-next"><a href="{prev["slug"]}.html"><small>Previous inductee</small><b>{e(prev["name"])}</b></a>'
           f'<a href="{nxt["slug"]}.html"><small>Next inductee</small><b>{e(nxt["name"])}</b></a></div>') if prev is not d else ""
    mates = [p for p in players if p["team_key"] == key and p["slug"] != slug]
    if len(mates) > 4:
        i0 = next((i for i, p in enumerate(players) if p["slug"] == slug), 0)
        mates = sorted(mates, key=lambda p: (players.index(p) - i0) % len(players))[:4]
    more = (f'<div class="hof-more"><div class="ch-k">{e(TEAM_LONG.get(key, team))}</div><h2 class="hof-more-h">More {e(team)} Hall of Famers</h2>'
            f'<div class="plates four hofp">{"".join(plate(p) for p in mates)}</div></div>') if mates else ""
    tail = f"""
<section class="hof-sec" data-c="{key}">
  <div class="wrap">
    {nav}
    {more}
    <p style="margin-top:22px"><a class="sh-all" href="bay-area-hall-of-fame.html">Every Bay Area Hall of Famer</a></p>
    {rel}
  </div>
</section>"""
    body = f'<main data-c="{key}"><article>' + hero + "".join(secs) + "</article>" + tail + "\n</main>\n"
    return head(title, desc, url, image, ld, "profile") + CHROME_TOP + body + CHROME_BOTTOM


def hub(players):
    url = f"{SITE}/bay-area-hall-of-fame.html"
    title = "Bay Area Hall of Fame: The Greatest Legends in Bay Area Sports"
    desc = ("The Bay Area Hall of Fame: Giants, 49ers, Warriors, A's, Sharks and Raiders legends with full stats, "
            "clutch moments, video and what the people who watched them said.")[:155].rsplit(" ", 1)[0]
    image = f"{SITE}/{card_path(players[0])}" if players else ""
    ld = jsonld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Bay Area Hall of Fame", "item": url}]}) + "\n" + jsonld(
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Bay Area Hall of Fame", "url": url, "description": desc,
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/{p['slug']}.html", "name": p["name"]} for i, p in enumerate(players)]}})
    teams = [k for k in TEAM_ORDER if any(p["team_key"] == k for p in players)]
    names = [TEAM[k] for k in teams]
    franchises = ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else "".join(names)
    hero = f"""
<section class="vault-hero">
  <div class="wrap">
    <div class="vh-k">From the Vault</div>
    <h1>The Bay Area Hall of Fame</h1>
    <p class="vh-lede">Our guys. The ones who wanted the bat, the ball or the puck when the whole building was standing up. {e(franchises)} legends, every one with a full page: the life story, every season of stats, the moments that made us lose our minds, the video, and what the people who played with and against them said. More plaques go up all the time. For the eras they built, open <a href="history.html">Bay Area History</a> and the <a href="dynasties.html">Dynasties</a> hub.</p>
    <div class="vh-stats">
      <div class="vh-stat"><b>{len(players)}</b><span>Inductees</span></div>
      <div class="vh-stat"><b>{len(teams)}</b><span>{"Franchise" if len(teams) == 1 else "Franchises"}</span></div>
      <div class="vh-stat"><b>{sum(len(p.get("clutch_moments") or []) for p in players)}</b><span>Clutch moments</span></div>
    </div>
  </div>
</section>"""
    chips = "".join(f'<a href="#hof-{k}" data-c="{k}">{e(TEAM[k])} <i>{sum(1 for p in players if p["team_key"] == k)}</i></a>' for k in teams)
    jump = f"""
<nav class="hof-jump" aria-label="Jump to a franchise">
  <div class="wrap">{chips}<input class="hof-find" type="search" placeholder="Find a legend" aria-label="Find a Hall of Famer by name"></div>
</nav>"""
    newest = max(p.get("inducted", "") for p in players)
    fresh = [p for p in players if p.get("inducted", "") == newest]
    new_sec = ""
    if newest and len(fresh) < len(players):
        new_sec = f"""
<section class="chapter hof-new">
  <div class="wrap">
    <div class="ch-head">
      <div class="ch-num">NEW</div>
      <div><div class="ch-k">Inducted {e(fmt_date(newest))}</div><h2>The Newest Plaques</h2></div>
      <div class="ch-count">{len(fresh)} added</div>
    </div>
    <div class="plates four hofp">{"".join(plate(p) for p in fresh)}
    </div>
  </div>
</section>"""
    secs = []
    for i, k in enumerate(teams):
        mine = [p for p in players if p["team_key"] == k]
        secs.append(f"""
<section class="chapter hof-team-sec" id="hof-{k}">
  <div class="wrap">
    <div class="ch-head">
      <div class="ch-num">{i + 1:02d}</div>
      <div><div class="ch-k">{e(TEAM_LONG[k])}</div><h2>{e(TEAM[k])} Hall of Famers</h2></div>
      <div class="ch-count">{len(mine)} {"inductee" if len(mine) == 1 else "inductees"}</div>
    </div>
    <div class="plates four hofp">{"".join(plate(p) for p in mine)}
    </div>
  </div>
</section>""")
    find_js = """
<p class="wrap hof-none" id="hof-none">No Hall of Famer by that name yet. More plaques go up all the time.</p>
<script>(function(){var q=document.querySelector('.hof-find');if(!q)return;q.addEventListener('input',function(){
var v=q.value.trim().toLowerCase(),any=false;document.querySelectorAll('.hof-team-sec').forEach(function(s){var n=0;
s.querySelectorAll('.plate').forEach(function(a){var ok=!v||a.textContent.toLowerCase().indexOf(v)>-1;a.style.display=ok?'':'none';if(ok)n++;});
s.style.display=n?'':'none';if(n)any=true;});var nw=document.querySelector('.hof-new');if(nw)nw.style.display=v?'none':'';
document.getElementById('hof-none').style.display=any?'none':'block';});})();</script>"""
    return head(title, desc, url, image, ld) + CHROME_TOP + "<main>" + hero + jump + new_sec + "".join(secs) + find_js + "\n</main>\n" + CHROME_BOTTOM


def plate(p, img_prefix=""):
    k = p["team_key"]
    nick = f'<span class="pl-nick">{e(p["nickname"])}</span>' if p.get("nickname") else ""
    return f'''
        <a class="plate hof" data-c="{k}" href="{img_prefix}{p["slug"]}.html">
          <div class="pl-img"><img src="{img_prefix}{photo_src(p)}" alt="{e(p["photo"].get("alt") or p["name"])}" width="900" height="1125" loading="lazy" decoding="async"><span class="stamp">{e(TEAM[k])}</span></div>
          <div class="pl-b"><span class="pl-yr">{e(p.get("position"))} &middot; {e(p.get("bay_years"))}</span><h3>{e(p["name"])}</h3>{nick}</div>
        </a>'''


def main():
    players = load()
    if not players:
        print("no inductees in _hof/")
        return
    for i, d in enumerate(players):
        make_card(d)
        prev, nxt = players[i - 1], players[(i + 1) % len(players)]
        open(os.path.join(ROOT, d["slug"] + ".html"), "w", encoding="utf-8", newline="\n").write(player_page(d, prev, nxt, players))
        print("wrote", d["slug"] + ".html")
    open(os.path.join(ROOT, "bay-area-hall-of-fame.html"), "w", encoding="utf-8", newline="\n").write(hub(players))
    print("wrote bay-area-hall-of-fame.html with", len(players), "inductees")
    team_strips(players)
    search_index(players)
    sitemap_sync(players)


def sitemap_sync(players):
    """Every inductee page is in sitemap.xml with its card and hero photo as image entries."""
    fp = os.path.join(ROOT, "sitemap.xml")
    s = open(fp, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    orig = s
    for p in players:
        loc = f"{SITE}/{p['slug']}.html"
        m = re.search(r"  <url>\s*<loc>" + re.escape(loc) + r"</loc>.*?</url>", s, re.S)
        lastmod = p.get("verified_on") or p.get("inducted") or ""
        if m:
            lm = re.search(r"<lastmod>([^<]+)</lastmod>", m.group(0))
            lastmod = lm.group(1) if lm else lastmod
        imgs = [f"{SITE}/{card_path(p)}", f"{SITE}/{photo_src(p)}"]
        block = nl.join(["  <url>", f"    <loc>{loc}</loc>", f"    <lastmod>{lastmod}</lastmod>",
                         "    <changefreq>weekly</changefreq>", "    <priority>0.6</priority>"] +
                        [f"    <image:image><image:loc>{html.escape(u)}</image:loc></image:image>" for u in imgs] + ["  </url>"])
        if m:
            s = s[:m.start()] + block + s[m.end():]
        else:
            i = s.rindex("</urlset>")
            s = s[:i] + block + nl + s[i:]
    if s != orig:
        open(fp, "w", encoding="utf-8", newline="").write(s)
        print("sitemap synced")


def search_index(players):
    """Hall of Famers are findable from search.html (k = Hall of Fame)."""
    fp = os.path.join(ROOT, "assets", "search-index.json")
    raw = open(fp, encoding="utf-8").read()
    data = json.loads(raw)
    hof = {p["slug"] + ".html" for p in players}
    data = [x for x in data if x.get("u") not in hof]
    for p in players:
        data.append({"u": p["slug"] + ".html", "t": f"{p['name']}: Bay Area Hall of Fame",
                     "d": p.get("meta_description") or p.get("dek", ""), "k": "Hall of Fame", "dt": p.get("inducted", "")})
    ascii_only = all(ord(c) < 128 for c in raw)
    open(fp, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=ascii_only))


TEAM_HUBS = {"sf": "giants.html", "niners": "49ers.html", "gs": "warriors.html", "as": "athletics.html", "sj": "sharks.html"}


def team_strips(players):
    """Keep a marked Hall of Fame strip on each team hub, just above the footer."""
    for k, f in TEAM_HUBS.items():
        fp = os.path.join(ROOT, f)
        mine = [p for p in players if p["team_key"] == k]
        if not mine or not os.path.exists(fp):
            continue
        s = open(fp, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in s else "\n"
        block = (f'<!-- HOF-STRIP:start --><section class="zone"><div class="wrap">\n'
                 f'<div class="sec-head"><div><h2>{e(TEAM[k])} in the Bay Area Hall of Fame</h2></div>'
                 f'<a class="sh-all" href="bay-area-hall-of-fame.html#hof-{k}">All {len(mine)} {e(TEAM[k])} Hall of Famers</a></div>\n'
                 f'<div class="plates four hofp">{"".join(plate(p) for p in mine[:8])}\n</div>\n</div></section><!-- HOF-STRIP:end -->').replace("\n", nl)
        if "<!-- HOF-STRIP:start -->" in s:
            new = re.sub(r"<!-- HOF-STRIP:start -->.*?<!-- HOF-STRIP:end -->", lambda m: block, s, flags=re.S)
        else:
            anchor = "</div>" + nl + '<footer class="desk-foot">'
            if s.count(anchor) != 1:
                print("SKIP strip (no anchor):", f)
                continue
            new = s.replace(anchor, block + nl + anchor)
        if new != s:
            open(fp, "w", encoding="utf-8", newline="").write(new)
            print("strip", f, len(mine))


if __name__ == "__main__":
    main()
