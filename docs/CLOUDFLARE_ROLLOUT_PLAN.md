# Cloudflare rollout plan — bayareasportsblog.com

**Status: NOT STARTED. Needs Nima's explicit go-ahead before any nameserver change.**

Rebuilt 2026-08-08 in the repo. The original lived on the Desktop and was lost; every
DNS value below was re-resolved live against 8.8.8.8 on 2026-08-08 rather than recalled,
and every header and compression figure was measured against production the same day.
**Do not run this migration from memory. Re-verify §1 immediately before starting.**

---

## 1. Current production state (verified 2026-08-08)

### Registrar and nameservers
```
registrar nameservers:  dns1.registrar-servers.com
                        dns2.registrar-servers.com     (Namecheap FreeDNS)
```

### Apex A records — GitHub Pages
```
bayareasportsblog.com.  A  185.199.108.153
bayareasportsblog.com.  A  185.199.109.153
bayareasportsblog.com.  A  185.199.110.153
bayareasportsblog.com.  A  185.199.111.153
```

### www
```
www.bayareasportsblog.com.  CNAME  nimadamus.github.io.
```

### MX — email forwarding. THIS IS THE PART THAT BREAKS THINGS.
Priorities re-resolved live; they are **not** all equal, which is the specific thing
the lost plan warned about:

| Priority | Host |
|---|---|
| 10 | eforward1.registrar-servers.com |
| 10 | eforward2.registrar-servers.com |
| 10 | eforward3.registrar-servers.com |
| 15 | eforward4.registrar-servers.com |
| 20 | eforward5.registrar-servers.com |

### SPF TXT
```
bayareasportsblog.com.  TXT  "v=spf1 include:spf.efwd.registrar-servers.com ~all"
```

### Live response headers (measured)
```
apex GET /            HTTP/1.1 200   Server: GitHub.com   Cache-Control: max-age=600
assets/style.css      HTTP/1.1 200   Cache-Control: max-age=600   Content-Encoding: gzip
https://www/          HTTP/1.1 301 -> https://bayareasportsblog.com/
http://apex/          HTTP/1.1 301 -> https://bayareasportsblog.com/
```

Two facts drive the whole business case:

1. **GitHub Pages sends `Cache-Control: max-age=600` on everything** — HTML, CSS, JS,
   and content-hashed immutable images alike. Ten minutes. There is no way to change it
   from the Pages side.
2. **GitHub Pages serves gzip, not Brotli.**

---

## 2. What the migration is actually worth (measured, not estimated)

Brotli quality 11 versus gzip level 9 on this site's own text assets, measured
2026-08-08:

| File | raw | gzip | brotli | saving |
|---|---|---|---|---|
| `index.html` | 114,833 | 18,890 | 13,552 | **28.3%** |
| `assets/style.css` | 44,454 | 9,225 | 8,027 | 13.0% |
| `assets/desk.css` | 43,353 | 9,005 | 7,872 | 12.6% |
| `sitemap.xml` | 59,468 | 4,429 | 3,774 | 14.8% |
| a long article page | 16,486 | 5,002 | 3,990 | 20.2% |
| `assets/search-index.json` | 42,337 | 14,071 | 12,039 | 14.4% |
| **total** | 320,931 | 60,622 | 49,254 | **18.8%** |

**Certain wins:**
- Brotli on text: ~19% less transfer overall, ~28% on the homepage document specifically.
- Asset caching: `max-age=600` → one year immutable on hashed assets, via a Cache Rule.
  Repeat visits stop re-fetching CSS and card images every ten minutes.
- Edge POPs closer to readers than GitHub's `sea` region (observed in
  `x-github-edge-region` on production).

**Blocked-on-CDN work this unblocks** — two performance experiments were built, measured
and reverted because they made things worse without a CDN in front, and must not be
retried until after this migration:
- self-hosted fonts (mobile LCP regressed 3,969 ms → 4,834 ms)
- critical CSS inlining (FCP/LCP flat, plus a 43,071 → 14,517 px document-height flash)

---

## 3. Preconditions

- [ ] Nima's explicit go-ahead. Nameserver changes are outward-facing and affect email.
- [ ] Re-run every lookup in §1 and diff against this file. If anything differs, update
      this file first.
- [ ] Confirm the Cloudflare account and that the free plan is acceptable (it is —
      Brotli and Cache Rules are all free-tier).
- [ ] Screenshot or export the complete Namecheap Advanced DNS record list before
      touching anything. That export is the rollback source of truth.

---

## 4. Migration steps, in order

### Step 1 — Add the site to Cloudflare, DO NOT change nameservers yet
Add `bayareasportsblog.com`. Cloudflare will scan and import existing records.

### Step 2 — Audit the imported records against §1, record by record
The scan is not trustworthy. Verify by hand:

| Record | Value | Proxy status |
|---|---|---|
| A `@` | 185.199.108.153 | **Proxied** (orange) |
| A `@` | 185.199.109.153 | **Proxied** |
| A `@` | 185.199.110.153 | **Proxied** |
| A `@` | 185.199.111.153 | **Proxied** |
| CNAME `www` | nimadamus.github.io | **Proxied** |
| MX `@` | eforward1.registrar-servers.com | **DNS only** (grey), priority 10 |
| MX `@` | eforward2.registrar-servers.com | **DNS only**, priority 10 |
| MX `@` | eforward3.registrar-servers.com | **DNS only**, priority 10 |
| MX `@` | eforward4.registrar-servers.com | **DNS only**, priority 15 |
| MX `@` | eforward5.registrar-servers.com | **DNS only**, priority 20 |
| TXT `@` | `v=spf1 include:spf.efwd.registrar-servers.com ~all` | n/a |

> **If a single MX record or the SPF TXT is missing or carries the wrong priority when
> the nameservers cut over, inbound email to the domain stops.** MX records must never
> be proxied — Cloudflare's proxy does not handle SMTP, and an orange-clouded MX resolves
> to a Cloudflare anycast IP that will not accept mail.

### Step 3 — Set SSL/TLS mode to **Full (strict)** BEFORE the cutover
GitHub Pages has "Enforce HTTPS" on and serves a valid certificate. With Cloudflare in
"Flexible" mode, Cloudflare requests the origin over HTTP, GitHub 301s to HTTPS,
Cloudflare follows it back to itself, and the site enters an infinite redirect loop
(`ERR_TOO_MANY_REDIRECTS`). **Full (strict) is the only correct setting here.**

### Step 4 — Speed settings
- Brotli: **on** (Speed → Optimization → Content Optimization).
- Early Hints: on.
- HTTP/3 (QUIC): on.
- Auto Minify: **leave off.** The build already ships minified/normalised assets and
  the site has documented CRLF/asset-hashing sensitivities; a second minifier is risk
  without measured benefit.
- Rocket Loader: **off.** It reorders script execution and this site has inline
  boot scripts.

### Step 5 — Cache Rules (this is where the caching win comes from)
1. **Immutable assets** — if URI path starts with `/assets/` → Cache eligible, Edge TTL
   1 year, Browser TTL 1 year.
2. **HTML** — if URI path ends with `.html` OR path equals `/` → Edge TTL 1 hour,
   Browser TTL respect-origin (leaves the 600 s browser cache in place so publishes
   still surface quickly).
3. **Feeds** — `/sitemap.xml`, `/news-sitemap.xml`, `/feed.xml` → Edge TTL 5 minutes.
   The news sitemap is a rolling 48-hour window and must not be cached hard.

Note the site currently has **no content hashing in asset filenames**. A one-year TTL on
`/assets/` therefore requires a purge on deploy — see step 8. If asset hashing is added
later, the purge step can be dropped for hashed files.

### Step 6 — Cut the nameservers over at Namecheap
Domain → Nameservers → Custom DNS → the two Cloudflare nameservers Cloudflare assigns.
Propagation is typically minutes to a couple of hours.

### Step 7 — Verify within the first ten minutes
```bash
# should now be Cloudflare, not GitHub.com
curl -sI https://bayareasportsblog.com/ | grep -iE '^(HTTP|server|cf-ray|cache-control|content-encoding)'

# brotli must appear
curl -sI -H 'Accept-Encoding: br' https://bayareasportsblog.com/assets/style.css | grep -i content-encoding

# no redirect loop
curl -sIL https://bayareasportsblog.com/ | grep -c '^HTTP'

# www and http still 301 to the apex
curl -sI https://www.bayareasportsblog.com/ | grep -iE '^(HTTP|location)'
curl -sI http://bayareasportsblog.com/  | grep -iE '^(HTTP|location)'

# EMAIL - the five MX records and the SPF TXT must be unchanged
nslookup -type=MX  bayareasportsblog.com 1.1.1.1
nslookup -type=TXT bayareasportsblog.com 1.1.1.1
```
Then send a live test message to the forwarded address and confirm it arrives. Do not
consider the migration done until a real email has landed.

Also re-run the four site gates (`docs/SEO_BASELINE_FROZEN.md` §"How to re-verify") and
confirm both sitemaps still return 200 through the proxy.

### Step 8 — Add a purge to the deploy path
Because `/assets/` filenames are not content-hashed, a deploy that changes CSS or a card
image needs an edge purge or readers keep the old file for up to a year. Either:
- purge-everything via the Cloudflare API as a post-push step, or
- purge by URL for the specific changed files.

Until that automation exists, **purge manually from the dashboard after any deploy that
touches `/assets/`.**

---

## 5. Rollback

Point the Namecheap nameservers back to `dns1.registrar-servers.com` and
`dns2.registrar-servers.com` and re-enter the records from the §1 table (or the export
taken in the preconditions). GitHub Pages continues serving the apex directly and the
site is exactly as it is today. Nothing in the repo changes during this migration, so
there is no code rollback.

---

## 6. Known traps

- **Flexible SSL causes a redirect loop.** Full (strict), always.
- **Never proxy an MX record.** Grey cloud, every time.
- **MX priorities are not uniform** (10/10/10/15/20). Copying them all as priority 10
  changes mail routing behaviour.
- **Cloudflare's record scan misses records.** Verify by hand against §1.
- **The news sitemap is a 48-hour rolling window.** Hard-caching it at the edge makes it
  stale and useless to Google News.
- **`/assets/` has no cache-busting hashes.** A one-year TTL without a purge step will
  serve stale CSS.
- **Do not retry self-hosted fonts or critical CSS before this is live.** Both were
  measured as regressions on the current stack.
