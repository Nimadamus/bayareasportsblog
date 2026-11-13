#!/usr/bin/env python3
"""injury_changed.py: which injury report pages changed in substance since the last commit.

Compares the table rows (player, injury, status, expected back, last update) of every
articles/*injury-report.html in the working tree against HEAD. Timestamps like "Updated
Fri, Nov 13, 7:42 AM" are ignored, so a refresh that found nothing new reports nothing.
Prints one live URL per changed page; prints nothing when nothing changed.

    python tools/injury_changed.py
"""
import glob
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://bayareasportsblog.com/'


def rows(text):
    return re.findall(r'<tr><td>.*?</tr>', text or '')


def main():
    os.chdir(ROOT)
    for f in sorted(glob.glob('articles/*injury-report.html')):
        f = f.replace(os.sep, '/')
        now = open(f, encoding='utf-8').read()
        try:
            old = subprocess.run(['git', 'show', 'HEAD:' + f], capture_output=True, check=True).stdout.decode('utf-8')
        except subprocess.CalledProcessError:
            old = ''
        if rows(now) != rows(old):
            print(BASE + f)


if __name__ == '__main__':
    main()
