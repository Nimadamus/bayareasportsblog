# Search Console access checklist

**Written 15 September 2026.** What is needed to unblock the four analyses that no amount
of on site measurement can replace.

**Do not paste a password, an API secret or a service account key into a terminal or a
chat window.** Nothing on this list requires that, and every item below is either a click
in a web UI or a file dropped into the repo.

---

## What already exists

Two Google verification files are live on the site and returning 200:

```
https://bayareasportsblog.com/google415ee1e6530e2d0f.html
https://bayareasportsblog.com/google6f74b54ecd988601.html
```

Bing is verified too, via `BingSiteAuth.xml` (user `CA62AF311BC164299209FD9F74570608`).

So a Search Console property was set up at some point. What does not exist anywhere on
this machine is a credential that can read it. There is no GSC service account, no OAuth
token and no `gcloud` login for this project.

---

## Option A, the one I would pick: add a delegated user

In Search Console, open the `bayareasportsblog.com` property, then Settings, Users and
permissions, Add user.

- Add whichever Google account you want the reporting to run under
- Permission level **Full** if that account should also submit URLs and request indexing, otherwise **Restricted** is enough to read everything on this list

Then tell me which account it is. I never need its password. When you want a pull, you
authorise once in a browser and the token lands in a file I read locally.

**What I need from you:** the property is verified as a Domain property or a URL prefix
property, and the email address you added. That is it.

---

## Option B: a service account, if you prefer no browser step

1. In Google Cloud Console, create a project, or reuse one
2. Enable the **Google Search Console API**
3. Create a service account, no roles needed at the project level
4. Create a JSON key and **save the file to `C:\Users\BL\.secrets\gsc.json`**, do not paste its contents anywhere
5. In Search Console, Settings, Users and permissions, add the service account's email address as a **Restricted** user

**What I need from you:** confirmation that the file is at that path. I read it from disk
and it never enters the transcript.

Worth knowing: the previous Google service account on this machine was deleted on
1 August 2026 and it was a Sheets account, not a Search Console one, so there is nothing to
recover.

---

## Option C: manual export, no access at all

If neither of the above is worth doing, the export does most of the job. In Search
Console, Performance, set the date range to the last 3 months, then Export, and choose
CSV or Google Sheets. Do the same on Pages, Queries and the Index coverage report.

Drop the files anywhere on the machine and tell me where. This is slower and it goes stale,
but it unblocks the four analyses below for one cycle.

---

## What I will pull, and what each answer changes

| Data | What it decides |
|---|---|
| Indexed vs discovered vs excluded URLs | Whether the 220 articles are actually in the index at all. Everything in the content audit assumes they are crawlable, which I proved, not indexed, which I cannot see. |
| Impressions and clicks by page | Which of the 220 are doing anything. Right now every page is treated as equal because I have no way to rank them. |
| Pages with impressions and zero clicks | Title and description rewrites, the cheapest ranking work there is. |
| Queries we already appear for | The only honest source of content ideas. Section C of the content audit is reasoned from query shape, not from demand, and it says so. |
| Average position by page | Anything sitting at 5 to 20 is one improvement away from traffic. Those pages get the work first. |
| CTR by page | Separates a ranking problem from a snippet problem. |
| Coverage and crawl errors | Whether Google is hitting anything I cannot see from a crawl, including soft 404s and any manual action. |
| Sitemap read status and last read date | Whether the two sitemaps are being fetched, and whether the new archive pages were picked up. |

---

## One thing worth doing whether or not GSC happens

There is **no analytics on any of the 253 pages**. No Google Analytics, no Plausible, no
Umami, nothing. Search Console tells you what happens in the search results. It tells you
nothing about what someone does after they arrive, which pages they leave from, or whether
the archive pagination is used.

Two options, both a single script tag in the shared head:

- **Google Analytics 4**, free, integrates with Search Console, needs a cookie banner for EU visitors
- **Plausible or a similar privacy first tool**, roughly 9 dollars a month, no cookie banner, far lighter

This is a decision, not a task. Say which and it goes in with the next publish.
