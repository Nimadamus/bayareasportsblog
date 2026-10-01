#!/usr/bin/env python3
"""_masthead_date.py: the masthead date is today's Pacific date, never a frozen one.

Every hub page carries a dateline in the masthead. It was typed in by hand and sat at
"Saturday, July 18, 2026" into October. Two layers keep it honest now:

1. This script rewrites the static text to today's Pacific date, so crawlers and readers
   with scripts off see the day the page was last built.
2. A one line inline script after it replaces the text with the reader's current Pacific
   date at view time, so the page is right even on a day nothing was rebuilt.

    python _masthead_date.py
"""
import os
import re
import glob
import datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.abspath(__file__))
MARK = 'data-dt="live"'
JS = ('<script>(function(){var e=document.querySelectorAll(\'[data-dt="live"]\'),'
      't=new Date().toLocaleDateString("en-US",{timeZone:"America/Los_Angeles",'
      'weekday:"long",month:"long",day:"numeric",year:"numeric"});'
      'for(var i=0;i<e.length;i++)e[i].textContent=t})()</script>')
PAT = re.compile(r'<b (id="dt-today"|class="dt-live")(?: data-dt="live")?>[^<]*</b>([^<]*</div>)(<script>\(function\(\)\{var e=document\.querySelectorAll\(\'\[data-dt="live"\]\'\).*?</script>)?')


def main():
    now = datetime.datetime.now(ZoneInfo('America/Los_Angeles'))
    label = now.strftime('%A, %B ') + str(now.day) + now.strftime(', %Y')
    changed = 0
    for path in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        text = open(path, encoding='utf-8', newline='').read()
        new = PAT.sub(lambda m: '<b %s %s>%s</b>%s%s' % (m.group(1), MARK, label, m.group(2), JS), text)
        if new != text:
            open(path, 'w', encoding='utf-8', newline='').write(new)
            changed += 1
    print('masthead date %s on %d pages' % (label, changed))


if __name__ == '__main__':
    main()
