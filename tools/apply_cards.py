#!/usr/bin/env python3
"""apply_cards.py - build the per-article card image from a manifest and rewrite
every <img src> pointing at that article across ALL site pages to the new card.

Manifest (tools/cards_manifest.json): { "<article_href>": {mode, ...} }
  mode="photo":   {"mode":"photo","src":"assets/img/players/xxx.jpg","alt":"...","team":"giants"}
  mode="graphic": {"mode":"graphic","team":"giants","name":"Erik Miller","sub":"...","alt":"..."}
Output cards -> assets/img/cards/<article-slug>.jpg  (one unique file per article)
"""
import os, re, json, glob, hashlib, sys
sys.path.insert(0, os.path.dirname(__file__))
import artgen
import imagehash
from PIL import Image
_built_hashes=[]   # phash of every card built this run (variety guard)

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDS=os.path.join(ROOT,'assets','img','cards')
os.makedirs(CARDS,exist_ok=True)
MAN=json.load(open(os.path.join(os.path.dirname(__file__),'cards_manifest.json'),encoding='utf-8'))

def slug_of(href): return os.path.splitext(os.path.basename(href))[0]

def build_one(href, spec):
    slug=slug_of(href); dst=os.path.join(CARDS, slug+'.jpg')
    if spec['mode']=='photo':
        artgen.photo_card(os.path.join(ROOT, spec['src']), spec['team'],
                          spec['name'], spec.get('sub',''), dst, seed=slug)
        try: _built_hashes.append(imagehash.phash(Image.open(dst)))
        except Exception: pass
    else:
        # variety guard: re-seed with a salt until perceptually distinct from all built cards
        for salt in range(60):
            artgen.art_card(spec['team'], spec['name'], spec.get('sub',''), dst,
                            seed=slug if salt==0 else slug+'#'+str(salt))
            ph=imagehash.phash(Image.open(dst))
            if all((ph-h)>=8 for h in _built_hashes):
                _built_hashes.append(ph); break
        else:
            _built_hashes.append(ph)
    return 'assets/img/cards/'+slug+'.jpg'

def rewrite_pages(href, cardpath, alt):
    changed=[]
    for page in glob.glob(os.path.join(ROOT,'*.html'))+glob.glob(os.path.join(ROOT,'articles','*.html')):
        html=open(page,encoding='utf-8').read(); orig=html
        # find <a ... href="...href..."> ... <img src="X" alt="Y"> within that anchor
        # simpler: replace any <img src="..."...> that is the card for a link to href
        # We match the anchor block for this href and swap its first img.
        def repl(m):
            block=m.group(0)
            block2=re.sub(r'(<img\s+src=")[^"]+("[^>]*\salt=")[^"]*(")',
                          lambda im: im.group(1)+rel(page,cardpath)+im.group(2)+alt+im.group(3),
                          block, count=1)
            return block2
        pat=re.compile(r'<a\b[^>]*href="(?:\.\./)?'+re.escape(href)+r'"[^>]*>.*?</a>', re.S)
        html=pat.sub(repl, html)
        if html!=orig:
            open(page,'w',encoding='utf-8').write(html); changed.append(os.path.basename(page))
    return changed

def rel(page, cardpath):
    # cardpath is repo-root-relative; pages in /articles need ../
    return ('../'+cardpath) if os.path.dirname(page).endswith('articles') else cardpath

def main():
    reg={}
    total=0; pages_touched=set()
    for href,spec in MAN.items():
        cp=build_one(href,spec)
        ch=rewrite_pages(href, cp, spec.get('alt','Bay Area Sports Blog'))
        pages_touched.update(ch)
        data=open(os.path.join(ROOT,cp),'rb').read()
        reg[href]={'card':cp,'sha256':hashlib.sha256(data).hexdigest(),'mode':spec['mode'],
                   'team':spec.get('team'),'alt':spec.get('alt')}
        total+=1
        print("built %-70s -> %s (%d pages)"%(href, cp, len(ch)))
    json.dump(reg, open(os.path.join(os.path.dirname(__file__),'card_registry.json'),'w'), indent=1)
    print("\n%d cards built, pages touched: %s"%(total, ', '.join(sorted(pages_touched))))

if __name__=='__main__': main()
