#!/usr/bin/env python3
"""gsc_pull.py: pull everything we need out of Search Console in one go.

Nothing about this script asks anybody to paste a secret. It reads a service account key
that already sits on disk at ~/.secrets/tmr-play-sa.json, or whatever --key points at.

    python tools/gsc_pull.py --probe        say exactly what is still missing
    python tools/gsc_pull.py                pull everything into data/gsc/
    python tools/gsc_pull.py --property sc-domain:bayareasportsblog.com

What it writes into data/gsc/, one CSV per cut, plus summary.json:

    totals_<window>.csv          clicks, impressions, CTR, position for the window
    pages_<window>.csv           page level
    queries_<window>.csv         query level
    page_query_<window>.csv      the pair, which is what the opportunity work runs on
    dates_<window>.csv           daily series
    devices_<window>.csv         device split
    sitemaps.csv                 submitted, last downloaded, warnings, errors
    inspect_<slug>.json          URL inspection for the pages named in PILOT_PAGES

Windows: 7d, 28d, 90d, and prev28d so the report can compare the last 28 days against the
28 before them. Search Console data lags about two days, so every window ends three days
back rather than today, which keeps the comparison honest instead of counting a partial day.
"""
import os
import sys
import csv
import json
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'gsc')
KEY = os.path.expanduser(os.environ.get('GSC_KEY', r'~/.secrets/tmr-play-sa.json'))
PROPERTY = 'sc-domain:bayareasportsblog.com'
FALLBACK_PROPERTY = 'https://bayareasportsblog.com/'
SCOPE = ['https://www.googleapis.com/auth/webmasters.readonly']
LAG_DAYS = 3
ROW_LIMIT = 25000

PILOT_PAGES = [
    'https://bayareasportsblog.com/articles/bay-bridge-series-giants-athletics-history.html',
    'https://bayareasportsblog.com/articles/warriors-2026-27-schedule-season-hub.html',
    'https://bayareasportsblog.com/articles/chase-center-guide-warriors-arena.html',
]


def windows():
    end = datetime.date.today() - datetime.timedelta(days=LAG_DAYS)
    return {
        '7d': (end - datetime.timedelta(days=6), end),
        '28d': (end - datetime.timedelta(days=27), end),
        '90d': (end - datetime.timedelta(days=89), end),
        'prev28d': (end - datetime.timedelta(days=55), end - datetime.timedelta(days=28)),
    }


def client(key_path):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    creds = service_account.Credentials.from_service_account_file(key_path, scopes=SCOPE)
    return build('searchconsole', 'v1', credentials=creds, cache_discovery=False)


def explain(exc):
    """Turn an HttpError into the one sentence that says what to do next."""
    try:
        msg = json.loads(exc.content.decode('utf-8', 'replace'))['error']['message']
    except Exception:
        msg = str(exc)
    status = getattr(getattr(exc, 'resp', None), 'status', '?')
    if 'has not been used' in msg or 'is disabled' in msg:
        return ('The Search Console API is not enabled on this Google Cloud project.\n'
                '  Fix: open the link in the message below and press Enable.\n  %s' % msg)
    if status == 403:
        return ('The credential works but it has no access to the property.\n'
                '  Fix: Search Console, Settings, Users and permissions, Add user,\n'
                '       paste the service account email, permission Restricted.\n  %s' % msg)
    if status == 404:
        return ('That property does not exist under this account.\n'
                '  Check whether the property is a Domain property (sc-domain:...) or a\n'
                '  URL prefix property (https://...).\n  %s' % msg)
    return 'HTTP %s: %s' % (status, msg)


def probe(key_path):
    print('key file        :', key_path, '(exists)' if os.path.exists(key_path) else '(MISSING)')
    if not os.path.exists(key_path):
        return 1
    info = json.load(open(key_path, encoding='utf-8'))
    print('service account :', info.get('client_email'))
    print('project         :', info.get('project_id'))
    from googleapiclient.errors import HttpError
    try:
        api = client(key_path)
        sites = api.sites().list().execute().get('siteEntry', [])
    except HttpError as exc:
        print('\nNOT READY YET\n  ' + explain(exc))
        return 2
    except Exception as exc:
        print('\nNOT READY YET\n  %s' % exc)
        return 2
    print('properties      : %d' % len(sites))
    for s in sites:
        print('   %-48s %s' % (s.get('siteUrl'), s.get('permissionLevel')))
    if not sites:
        print('\nNOT READY YET\n  The API is enabled and the credential works, but this account is')
        print('  not on any property. Add it in Search Console as a Restricted user.')
        return 2
    print('\nREADY. Run: python tools/gsc_pull.py')
    return 0


def query(api, prop, start, end, dimensions, extra=None):
    body = {'startDate': str(start), 'endDate': str(end), 'rowLimit': ROW_LIMIT,
            'dataState': 'final'}
    if dimensions:
        body['dimensions'] = dimensions
    if extra:
        body.update(extra)
    rows, start_row = [], 0
    while True:
        body['startRow'] = start_row
        res = api.searchanalytics().query(siteUrl=prop, body=body).execute()
        got = res.get('rows', [])
        rows.extend(got)
        if len(got) < ROW_LIMIT:
            break
        start_row += ROW_LIMIT
    return rows


def write_csv(name, dimensions, rows):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(list(dimensions) + ['clicks', 'impressions', 'ctr', 'position'])
        for r in rows:
            w.writerow(list(r.get('keys', [])) +
                       [r.get('clicks', 0), r.get('impressions', 0),
                        round(r.get('ctr', 0) * 100, 3), round(r.get('position', 0), 2)])
    return len(rows)


def main():
    key_path = KEY
    if '--key' in sys.argv:
        key_path = os.path.expanduser(sys.argv[sys.argv.index('--key') + 1])
    prop = PROPERTY
    if '--property' in sys.argv:
        prop = sys.argv[sys.argv.index('--property') + 1]
    if '--probe' in sys.argv:
        sys.exit(probe(key_path))

    from googleapiclient.errors import HttpError
    try:
        api = client(key_path)
        have = {s['siteUrl'] for s in api.sites().list().execute().get('siteEntry', [])}
    except HttpError as exc:
        sys.exit('cannot reach Search Console.\n  ' + explain(exc))
    if prop not in have:
        if FALLBACK_PROPERTY in have:
            prop = FALLBACK_PROPERTY
        else:
            sys.exit('property %s is not on this account. Visible: %s' % (prop, sorted(have)))
    print('property:', prop)

    os.makedirs(OUT, exist_ok=True)
    summary = {'property': prop, 'pulled': datetime.datetime.now().isoformat(timespec='seconds'),
               'windows': {}, 'lag_days': LAG_DAYS}

    for label, (start, end) in windows().items():
        print('\n%s  %s to %s' % (label, start, end))
        totals = query(api, prop, start, end, [])
        t = totals[0] if totals else {}
        summary['windows'][label] = {
            'start': str(start), 'end': str(end),
            'clicks': t.get('clicks', 0), 'impressions': t.get('impressions', 0),
            'ctr_pct': round(t.get('ctr', 0) * 100, 3), 'position': round(t.get('position', 0), 2)}
        write_csv('totals_%s.csv' % label, [], totals)
        print('   totals: %s clicks, %s impressions, CTR %.2f%%, position %.1f'
              % (t.get('clicks', 0), t.get('impressions', 0),
                 t.get('ctr', 0) * 100, t.get('position', 0)))
        for name, dims in (('pages', ['page']), ('queries', ['query']),
                           ('page_query', ['page', 'query']), ('dates', ['date']),
                           ('devices', ['device'])):
            n = write_csv('%s_%s.csv' % (name, label), dims, query(api, prop, start, end, dims))
            print('   %-12s %d rows' % (name, n))

    try:
        sm = api.sitemaps().list(siteUrl=prop).execute().get('sitemap', [])
        with open(os.path.join(OUT, 'sitemaps.csv'), 'w', newline='', encoding='utf-8') as fh:
            w = csv.writer(fh)
            w.writerow(['path', 'lastSubmitted', 'lastDownloaded', 'warnings', 'errors', 'isPending'])
            for s in sm:
                w.writerow([s.get('path'), s.get('lastSubmitted'), s.get('lastDownloaded'),
                            s.get('warnings'), s.get('errors'), s.get('isPending')])
        print('\nsitemaps: %d' % len(sm))
        summary['sitemaps'] = len(sm)
    except HttpError as exc:
        print('\nsitemaps unavailable: %s' % explain(exc))

    for url in PILOT_PAGES:
        slug = url.rstrip('/').split('/')[-1].replace('.html', '')
        try:
            res = api.urlInspection().index().inspect(
                body={'inspectionUrl': url, 'siteUrl': prop}).execute()
            json.dump(res, open(os.path.join(OUT, 'inspect_%s.json' % slug), 'w',
                                encoding='utf-8'), indent=1)
            status = res.get('inspectionResult', {}).get('indexStatusResult', {})
            print('inspect %-46s %s / %s' % (slug[:46], status.get('verdict'),
                                             status.get('coverageState')))
        except HttpError as exc:
            print('inspect %-46s unavailable: %s' % (slug[:46], explain(exc).splitlines()[0]))

    json.dump(summary, open(os.path.join(OUT, 'summary.json'), 'w', encoding='utf-8'), indent=1)
    print('\nwrote %s' % OUT)
    print('Core Web Vitals are not in this API. Field data needs a PageSpeed Insights key,')
    print('and tools/vitals_lab.py measures the lab numbers without one.')


if __name__ == '__main__':
    main()
