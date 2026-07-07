#!/usr/bin/env python3
import io
def tiles(items):
    s='<div class="fact-tiles">'
    for b,l in items: s+='<div class="ft"><b>%s</b><span>%s</span></div>'%(b,l)
    return s+'</div>\n'
def figrow(imgs):
    s='<div class="figrow">'
    for src,alt,cap in imgs: s+='<figure><img src="%s" alt="%s"><figcaption>%s</figcaption></figure>'%(src,alt,cap)
    return s+'</div>\n'
def video(vid,cap):
    return ('<span class="block-label">Highlight Video</span>\n<figure class="videowrap"><div class="vid">'
            '<iframe src="https://www.youtube-nocookie.com/embed/%s" title="%s" loading="lazy" '
            'allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" '
            'allowfullscreen></iframe></div><figcaption>%s</figcaption></figure>\n'%(vid,cap,cap))
def timeline(rows):
    s='<span class="block-label">Championship Timeline</span>\n<ul class="timeline">'
    for yr,txt in rows: s+='<li><span class="yr">%s</span><span class="tl-body">%s</span></li>'%(yr,txt)
    return s+'</ul>\n'
def quote(q,who):
    return '<div class="pullquote"><p>&ldquo;%s&rdquo;</p><cite>%s</cite></div>\n'%(q,who)
def highlights(items):
    s='<span class="block-label">Signature Moments</span>\n<ul class="highlights">'
    for i in items: s+='<li>%s</li>'%i
    return s+'</ul>\n'

R='&rsquo;'; D='&ndash;'
DATA={
 'articles/49ers-dynasty-team-of-the-decade.html':dict(
   hero='<img src="../assets/img/players/montana.jpg" alt="Joe Montana, the quarterback who led the 49ers dynasty" style="width:100%;max-height:520px;object-fit:cover;border-radius:12px;border:1px solid var(--line);margin-bottom:26px">',
   after=(tiles([('5','Super Bowl titles'),('4','Montana rings'),('6','Young TDs, SB XXIX'),('1994','Last title season')])
     +figrow([('../assets/img/players/rice.jpg','Jerry Rice','Jerry Rice, the greatest receiver of all time'),
              ('../assets/img/players/young.jpg','Steve Young','Steve Young, who added a fifth title')])
     +video('xLsFSsHnoxM','The Catch: Joe Montana to Dwight Clark (official NFL)')),
   more='  <p style="margin-top:30px;color:var(--muted);font-size:15px">More: <a href="../49ers.html"',
   before=(timeline([('1981','Super Bowl XVI, the first title, a win over the Cincinnati Bengals'),
                     ('1984','Super Bowl XIX, a dominant win over the Miami Dolphins'),
                     ('1988','Super Bowl XXIII, Montana'+R+'s late drive beats the Bengals again'),
                     ('1989','Super Bowl XXIV, a rout of the Denver Broncos'),
                     ('1994','Super Bowl XXIX, Steve Young throws a record six touchdowns')])
     +quote('Someone take the monkey off my back, please.','Steve Young, on the sideline as Super Bowl XXIX was won')
     +highlights(['The Catch, Montana to Dwight Clark, to reach the first Super Bowl',
                  'Montana'+R+'s game-winning drive in Super Bowl XXIII',
                  'First franchise to win five Super Bowls',
                  'Jerry Rice, the NFL'+R+'s all-time receiving leader',
                  'Steve Young'+R+'s record six touchdown passes in Super Bowl XXIX']))),
 'articles/giants-dynasty-even-year-magic.html':dict(
   hero='<img src="../assets/img/players/posey.jpg" alt="Buster Posey, the catcher at the heart of the Giants dynasty" style="width:100%;max-height:520px;object-fit:cover;border-radius:12px;border:1px solid var(--line);margin-bottom:26px">',
   after=(tiles([('3','World Series titles'),('2010','First SF title'),('4','2012 sweep games'),('7','2014 games to win')])
     +figrow([('../assets/img/players/bumgarner.jpg','Madison Bumgarner','Madison Bumgarner, the October legend'),
              ('../assets/img/players/posey.jpg','Buster Posey','Buster Posey anchored all three titles')])
     +video('vPw-Om2Xf5I','WS 2014 Game 7: Bumgarner tosses five scoreless innings (official MLB)')),
   more='  <p style="margin-top:30px;color:var(--muted);font-size:15px">More: <a href="../giants.html"',
   before=(timeline([('2010','Beat the Texas Rangers in five, Edgar Renteria named Series MVP'),
                     ('2012','Swept the Detroit Tigers, Pablo Sandoval'+R+'s three home runs in Game 1'),
                     ('2014','Beat the Kansas City Royals in seven, Bumgarner'+R+'s Game 7 save')])
     +quote('Play for each other, not yourself. Win each moment. Win each inning. It'+R+'s all we have left.','Hunter Pence, 2012 postseason speech')
     +highlights(['First San Francisco World Series title since the move west',
                  'Sandoval'+R+'s three-homer Game 1 in the 2012 World Series',
                  'Bumgarner'+R+'s five scoreless innings on two days'+R+' rest in Game 7',
                  'Three championship parades in five seasons under Bruce Bochy']))),
 'articles/warriors-championship-history.html':dict(
   hero='<img src="../assets/img/players/curry.jpg" alt="Stephen Curry, the face of the modern Warriors dynasty" style="width:100%;max-height:520px;object-fit:cover;border-radius:12px;border:1px solid var(--line);margin-bottom:26px">',
   after=(tiles([('5','NBA titles'),('1975','First championship'),('4','Curry-era titles'),('2022','Curry Finals MVP')])
     +figrow([('../assets/img/players/thompson.jpg','Klay Thompson','Klay Thompson, the other Splash Brother'),
              ('../assets/img/players/curry.jpg','Stephen Curry','Stephen Curry changed the sport')])
     +video('AOYACk7m7Fk','Warriors at Celtics, Game 6 NBA Finals highlights, June 16, 2022 (official NBA)')),
   more='  <p style="margin-top:30px;color:var(--muted);font-size:15px">More: <a href="../warriors.html"',
   before=(timeline([('1975','Rick Barry leads a stunning Finals sweep as heavy underdogs'),
                     ('2015','First title of the Curry era, a new style is born'),
                     ('2017','Back-to-back begins after adding Kevin Durant'),
                     ('2018','A second straight championship, at peak dominance'),
                     ('2022','The core returns, Curry wins Finals MVP over the Celtics')])
     +quote('From Rick Barry'+R+'s underhand free throws to Curry'+R+'s logo-range threes, greatness here is worth the wait.','Bay Area Sports Blog')
     +highlights(['Rick Barry'+R+'s 1975 Finals sweep, one of the great upsets ever',
                  'The Splash Brothers turning the three-pointer into a philosophy',
                  'Back-to-back titles in 2017 and 2018',
                  'Curry finally winning Finals MVP in 2022']))),
 'articles/bay-area-sports-history.html':dict(
   hero='<img src="../assets/img/players/rice.jpg" alt="Jerry Rice, a symbol of Bay Area sports greatness" style="width:100%;max-height:520px;object-fit:cover;border-radius:12px;border:1px solid var(--line);margin-bottom:26px">',
   after=tiles([('5','49ers Super Bowls'),('3','Giants World Series'),('5','Warriors NBA titles'),('13','Total major titles')]),
   more='  <p style="margin-top:30px;color:var(--muted);font-size:15px">Explore: <a href="../49ers.html"',
   before=(timeline([('1975','Warriors win it all behind Rick Barry'),
                     ('1981'+D+'1994','The 49ers win five Super Bowls'),
                     ('2010'+D+'2014','The Giants win three World Series'),
                     ('2015'+D+'2022','The Warriors win four more NBA titles')])
     +quote('Around here, the bar was set by legends, which is exactly the way we like it.','Bay Area Sports Blog')
     +highlights(['Five Lombardi Trophies for the 49ers',
                  'Three even-year World Series titles for the Giants',
                  'Five NBA championships for the Warriors',
                  'Deep traditions with the Athletics, Sharks, Stanford, and Cal']))),
}
for f,d in DATA.items():
    s=open(f,encoding='utf-8').read()
    assert d['hero'] in s,'hero missing '+f
    s=s.replace(d['hero'],d['hero']+'\n'+d['after'])
    assert d['more'] in s,'more missing '+f
    s=s.replace(d['more'],d['before']+d['more'])
    open(f,'w',encoding='utf-8').write(s)
    print('enriched',f)
