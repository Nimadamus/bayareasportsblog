#!/usr/bin/env python3
"""vitals_lab.py: Core Web Vitals measured locally, no Google API key required.

Google's field data needs either Search Console or a PageSpeed Insights key, and this site
has neither yet. This is the lab substitute: a real Chromium render at phone and desktop
sizes with LCP, CLS and transfer size read off the page's own performance entries.

Lab numbers are not field numbers. They are measured on a fast machine on a fast
connection, so treat them as a floor, not as what a visitor on a phone experiences. What
they are good for is regression: run them before and after a change and compare.

    python tools/vitals_lab.py                       the default page set
    python tools/vitals_lab.py <url> [<url> ...]     specific pages
"""
import sys
import json
import statistics

BASE = 'https://bayareasportsblog.com/'
DEFAULT = ['', 'blog.html', 'giants.html',
           'articles/bay-bridge-series-giants-athletics-history.html',
           'articles/warriors-2026-27-schedule-season-hub.html',
           'articles/chase-center-guide-warriors-arena.html']

COLLECT = """() => new Promise(resolve => {
  const out = {lcp: 0, cls: 0, transfer: 0, dcl: 0, load: 0};
  try {
    new PerformanceObserver(list => {
      for (const e of list.getEntries()) out.lcp = Math.max(out.lcp, e.startTime);
    }).observe({type: 'largest-contentful-paint', buffered: true});
    new PerformanceObserver(list => {
      for (const e of list.getEntries()) if (!e.hadRecentInput) out.cls += e.value;
    }).observe({type: 'layout-shift', buffered: true});
  } catch (e) {}
  setTimeout(() => {
    for (const r of performance.getEntriesByType('resource')) out.transfer += r.transferSize || 0;
    const nav = performance.getEntriesByType('navigation')[0];
    if (nav) {
      out.transfer += nav.transferSize || 0;
      out.dcl = nav.domContentLoadedEventEnd;
      out.load = nav.loadEventEnd;
    }
    resolve(out);
  }, 3500);
})"""


def main():
    from playwright.sync_api import sync_playwright
    paths = sys.argv[1:] or DEFAULT
    rows = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='msedge', headless=True)
        for label, viewport, mobile in (('mobile', {'width': 390, 'height': 844}, True),
                                        ('desktop', {'width': 1440, 'height': 900}, False)):
            ctx = browser.new_context(viewport=viewport, is_mobile=mobile, device_scale_factor=2)
            page = ctx.new_page()
            for path in paths:
                url = path if path.startswith('http') else BASE + path
                try:
                    page.goto(url, wait_until='load', timeout=60000)
                    m = page.evaluate(COLLECT)
                except Exception as exc:
                    print('%-9s %-58s FAILED %s' % (label, path[-58:], exc.__class__.__name__))
                    continue
                rows.append((label, path, m))
                print('%-9s %-58s LCP %6.0fms  CLS %.3f  transfer %5.0fKB  load %6.0fms'
                      % (label, (path or '/')[-58:], m['lcp'], m['cls'],
                         m['transfer'] / 1024.0, m['load']))
            ctx.close()
        browser.close()

    print()
    for label in ('mobile', 'desktop'):
        sub = [m for l, _, m in rows if l == label]
        if not sub:
            continue
        print('%-8s median LCP %.0fms  median CLS %.3f  median transfer %.0fKB  (n=%d)'
              % (label, statistics.median(x['lcp'] for x in sub),
                 statistics.median(x['cls'] for x in sub),
                 statistics.median(x['transfer'] for x in sub) / 1024.0, len(sub)))
    bad_lcp = [(l, p) for l, p, m in rows if m['lcp'] > 2500]
    bad_cls = [(l, p) for l, p, m in rows if m['cls'] > 0.1]
    print('over the 2500ms LCP threshold:', bad_lcp or 'none')
    print('over the 0.1 CLS threshold   :', bad_cls or 'none')


if __name__ == '__main__':
    main()
