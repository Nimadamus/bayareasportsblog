import glob, os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
BASE = "https://bayareasportsblog.com/"
EXCLUDE = {'404.html', 'google6f74b54ecd988601.html'}
order = ['index.html','49ers.html','warriors.html','giants.html','bayarea.html',
         'history.html','flashbacks.html','columns.html','athletics.html','sharks.html',
         'stanford.html','cal.html','betting.html','about.html','contact.html']
roots = [f for f in glob.glob('*.html') if f not in EXCLUDE]
roots = sorted(roots, key=lambda f: (order.index(f) if f in order else 999, f))
arts = sorted(glob.glob('articles/*.html'))
daily = sorted(glob.glob('daily/*.html'))
urls = []
for f in roots:
    urls.append(BASE if f == 'index.html' else BASE + f)
for f in daily:
    urls.append(BASE + f.replace(os.sep, '/'))
for f in arts:
    urls.append(BASE + f.replace(os.sep, '/'))
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    xml += '  <url><loc>%s</loc></url>\n' % u
xml += '</urlset>\n'
open('sitemap.xml', 'w', encoding='utf-8').write(xml)
print("sitemap urls:", len(urls))
for u in urls:
    print("  ", u)
