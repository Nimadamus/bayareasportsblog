#!/usr/bin/env python3
"""injury_index_check.py: ask Search Console whether the 7 injury report pages are indexed.
Writes docs/injury_index_check_<date>.txt. Run once, a week after launch (scheduled task
BASB_InjuryIndexCheck_1120), or any time by hand."""
import datetime, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = 'https://bayareasportsblog.com/articles/%s-injury-report.html'
urls = [U % t for t in ('49ers', 'raiders', 'warriors', 'giants', 'athletics', 'sharks', 'bay-area')]
out = os.path.join(ROOT, 'docs', 'injury_index_check_%s.txt' % datetime.date.today().isoformat())
r = subprocess.run([sys.executable.replace('pythonw', 'python'), os.path.expanduser('~/tools/gsc_submit.py')] + urls,
                   capture_output=True, text=True, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
open(out, 'w', encoding='utf-8').write(r.stdout + r.stderr)
print(out)
