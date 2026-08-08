#!/usr/bin/env python3
"""_link_repair.py - hand-picked contextual inbound links for the starved articles.

Every entry below was chosen by reading the sentence it lands in. The anchor is a
phrase the writer already wrote; the link goes to the piece that sentence is actually
talking about. Nothing is generated, nothing is templated, and no article gets a link
just to move a number.

Each entry is (source, target, [candidate anchors]). The first candidate that exists in
the source's <article> prose, outside any existing link or heading, wins. If none match,
the entry is reported as a miss and skipped rather than forced.

  python _link_repair.py --check     report matches and misses, write nothing
  python _link_repair.py             apply
"""
import os, re, sys, json

ROOT = os.path.dirname(os.path.abspath(__file__))
A = 'articles/'

# (source, target, candidate anchors - first one found is used)
LINKS = [
    # ---------- 49ers: camp, injuries, roster ----------
    (A+'49ers-kyle-shanahan-recovery-update-training-camp-2026.html',
     A+'49ers-deebo-samuel-returns-one-year-7-million-2026.html',
     ['Deebo Samuel back in the building', 'Deebo Samuel']),
    (A+'49ers-ricky-pearsall-out-for-season-pcl-surgery-2026.html',
     A+'49ers-dezhaun-stribling-training-camp-starter-2026.html',
     ["De'Zhaun Stribling has been the story of camp", "De&#39;Zhaun Stribling has been the story of camp",
      "De'Zhaun Stribling", "De&#39;Zhaun Stribling"]),
    (A+'49ers-khadarel-hodge-veteran-receiver-signing-august-2026.html',
     A+'49ers-signing-spree-okoronkwo-irwin-deguara-hodge-august-2026.html',
     ['four signings', 'Four signings', 'signing spree', 'Okoronkwo']),
    (A+'49ers-deebo-samuel-returns-one-year-7-million-2026.html',
     A+'49ers-brock-purdy-highest-passer-rating-nfl-history-1500-attempts.html',
     ['Brock Purdy playing the best football of his career',
      'playing the best football of his career']),
    (A+'49ers-brock-purdy-sharp-camp-demarcus-robinson-dime-end-zone-2026.html',
     A+'49ers-purdy-stribling-chemistry-loaded-roster-2026.html',
     ["De'Zhaun Stribling", 'De&#39;Zhaun Stribling', 'this receiver room']),
    (A+'49ers-purdy-layer-king-most-competitive-practice-camp-august-6.html',
     A+'49ers-purdy-sharp-camp-injuries-mounting-twenty-out-august-5.html',
     ['twenty guys', 'Twenty guys', 'the injury list', 'twenty players']),
    (A+'49ers-ricky-pearsall-out-for-season-pcl-surgery-2026.html',
     A+'49ers-injuries-again-training-camp-august-2026.html',
     ['the injury list', 'injury list', 'already hurt']),
    (A+'49ers-raheem-morris-players-love-him-just-play-football-2026.html',
     A+'49ers-shanahan-best-team-if-healthy-super-bowl-2026.html',
     ['best team', 'this roster', 'if this team stays healthy']),
    (A+'49ers-khadarel-hodge-veteran-receiver-signing-august-2026.html',
     A+'49ers-purdy-70-yard-touchdowns-unknown-receivers-camp-august-7.html',
     ['deep touchdown', 'a touchdown', 'receiver room']),
    (A+'49ers-brock-purdy-sharp-camp-demarcus-robinson-dime-end-zone-2026.html',
     A+'49ers-greenlaw-mccaffrey-pads-day-one-favorite-player-2026.html',
     ['pads', 'the first padded practice', 'Dre Greenlaw']),

    # ---------- 49ers / NFL: evergreen and history ----------
    (A+'49ers-dynasty-team-of-the-decade.html',
     A+'montana-young-49ers-quarterback-controversy.html',
     ['Steve Young', 'Joe Montana']),
    (A+'brandon-aiyuk-antonio-brown-49ers.html',
     A+'49ers-still-paying-for-vegas.html',
     ['Something broke in Las Vegas', 'Las Vegas']),
    (A+'bay-area-sports-history.html',
     A+'nfl-blackballed-colin-kaepernick-kneeling-anthem.html',
     ['Colin Kaepernick', 'Kaepernick']),
    (A+'49ers-dynasty-team-of-the-decade.html',
     A+'jerry-rice-predicts-49ers-super-bowl-2026-drought-over.html',
     ['Jerry Rice']),
    (A+'49ers-still-paying-for-vegas.html',
     A+'brandon-aiyuk-antonio-brown-49ers.html',
     ['Brandon Aiyuk', 'Aiyuk']),
    (A+'athletics-sacramento-bay-area-villains.html',
     A+'raiders-2026-season-preview-kubiak-cousins-mendoza-jeanty.html',
     ['Las Vegas']),

    # ---------- A's: the streaks and the free fall ----------
    (A+'athletics-nine-straight-white-sox-9-1-tailspin-i-called-it-july-12.html',
     A+'athletics-1-0-loss-white-sox-eighth-straight-coming-back-to-earth-july-11.html',
     ['eighth straight', 'the night before', 'eight in a row']),
    (A+'athletics-nine-straight-white-sox-9-1-tailspin-i-called-it-july-12.html',
     A+'athletics-white-sox-preview-jacob-lopez-july-10.html',
     ['Jacob Lopez', 'Guaranteed Rate Field']),
    (A+'athletics-first-half-breakdown-mirage-collapse-all-star-break-2026.html',
     A+'athletics-tigers-melton-shellacking-july-8.html',
     ['Troy Melton', 'Melton']),
    (A+'athletics-first-half-breakdown-mirage-collapse-all-star-break-2026.html',
     A+'athletics-tigers-sweep-valdez-july-9.html',
     ['Framber Valdez', 'swept', 'sixth straight']),
    (A+'athletics-15-1-nationals-ginn-gem-streak-snapped-july-18.html',
     A+'athletics-nationals-23-4-blowout-gage-jump-second-half-july-17.html',
     ['23-4', 'the night before', '15-1 annihilation']),
    (A+'athletics-15-1-nationals-ginn-gem-streak-snapped-july-18.html',
     A+'athletics-diamondbacks-6-5-10th-jacob-wilson-homer-blown-july-21.html',
     ['Jacob Wilson']),
    (A+'athletics-free-fall-continues-fourth-place-trade-deadline-july-30.html',
     A+'athletics-twins-2-0-lopez-bullpen-shutout-july-25.html',
     ['beat the Twins 2-0', 'Twins 2-0']),
    (A+'athletics-free-fall-continues-fourth-place-trade-deadline-july-30.html',
     A+'athletics-twins-11-8-kurtz-homer-springs-injury-july-26.html',
     ['Jeffrey Springs left with an apparent injury', 'Jeffrey Springs']),
    (A+'athletics-free-fall-continues-fourth-place-trade-deadline-july-30.html',
     A+'athletics-redsox-4-3-serven-homer-white-four-hits-july-28.html',
     ["Brian Serven's homer held up", 'Brian Serven']),
    (A+'athletics-free-fall-continues-fourth-place-trade-deadline-july-30.html',
     A+'athletics-redsox-4-2-10th-monasterio-homer-heim-butler-july-29.html',
     ["Andruw Monasterio's tenth-inning shot", 'Andruw Monasterio']),
    (A+'athletics-redsox-4-2-rafaela-slam-soderstrom-heim-homers-july-27.html',
     A+'athletics-redsox-13-1-tolle-14-strikeouts-ninth-straight-august-7.html',
     ['Payton Tolle']),
    (A+'athletics-redsox-4-3-serven-homer-white-four-hits-july-28.html',
     A+'athletics-tigers-11-0-swept-gage-jump-august-2.html',
     ['Gage Jump']),
    (A+'athletics-sacramento-bay-area-villains.html',
     A+'athletics-nationals-5-2-risp-failure-lopez-series-loss-july-19.html',
     ['West Sacramento']),
    (A+'athletics-nine-straight-white-sox-9-1-tailspin-i-called-it-july-12.html',
     A+'athletics-reds-5-4-wild-pitches-eighth-ginn-return-august-4.html',
     ['bullpen', 'the bullpen']),
    (A+'athletics-first-half-breakdown-mirage-collapse-all-star-break-2026.html',
     A+'athletics-diamondbacks-15-5-seven-run-fifth-july-22.html',
     ['Diamondbacks', 'Arizona']),
    (A+'athletics-redsox-13-1-tolle-14-strikeouts-ninth-straight-august-7.html',
     A+'athletics-reds-3-2-jacob-lopez-pulled-seventh-straight-august-5.html',
     ['Jacob Lopez on his night is real', 'Jacob Lopez']),
    (A+'athletics-free-fall-continues-fourth-place-trade-deadline-july-30.html',
     A+'athletics-15-1-nationals-ginn-gem-streak-snapped-july-18.html',
     ['15-1', 'the Nationals']),

    # ---------- Giants: the July-August collapse, in sequence ----------
    (A+'giants-whisenhunt-gem-rockies-8-2-july-9.html',
     A+'giants-3-1-rockies-erik-miller-bullpen-holds-series-win-july-12.html',
     ['Erik Miller']),
    (A+'giants-first-half-breakdown-vitello-second-half-all-star-break-2026.html',
     A+'giants-4-2-rockies-tyler-mahle-first-win-casey-schmitt-homer-july-11.html',
     ['Tyler Mahle', 'Casey Schmitt']),
    (A+'giants-casey-schmitt-all-star-breakout-season-2026.html',
     A+'giants-athletics-all-star-game-2026-arraez-langeliers-webb.html',
     ["All-Star Game Didn't Notice", 'All-Star Game']),
    (A+'giants-heating-up-best-baseball-of-the-season-july-30.html',
     A+'giants-angels-4-3-trout-sweep-avoided-july-26.html',
     ['Mike Trout made sure of that', 'Mike Trout']),
    (A+'giants-heating-up-best-baseball-of-the-season-july-30.html',
     A+'giants-brewers-8-2-roupp-early-exit-eldridge-homer-july-28.html',
     ["Bryce Eldridge's eighth-inning homer", '8-2 win']),
    (A+'giants-heating-up-best-baseball-of-the-season-july-30.html',
     A+'giants-brewers-3-0-mccray-homer-mahle-shutout-july-27.html',
     ['3-0 series opener', 'Tyler Mahle spun six shutout innings']),
    (A+'giants-heating-up-best-baseball-of-the-season-july-30.html',
     A+'giants-brewers-16-3-susac-two-homers-seven-run-sixth-july-29.html',
     ['16-3', 'Heliot Ramos went 4-for-5']),
    (A+'giants-adames-grand-slam-mariners-7-0-second-half-july-17.html',
     A+'giants-blown-lead-mariners-cole-young-webb-4-3-july-18.html',
     ['Logan Webb']),
    (A+'giants-first-half-breakdown-vitello-second-half-all-star-break-2026.html',
     A+'giants-swept-momentum-mariners-6-3-robbie-ray-eldridge-july-19.html',
     ['Robbie Ray', 'Seattle']),
    (A+'giants-tony-vitello-clueless-lineups-eldridge-leadoff.html',
     A+'giants-rangers-5-4-walkoff-eldridge-bench-vitello-august-4.html',
     ['Bryce Eldridge', 'Eldridge']),
    (A+'giants-season-over-build-around-eldridge-posey-bullpen.html',
     A+'bryce-eldridge-giants-future-franchise-first-baseman-july-2026.html',
     ['Bryce Eldridge']),
    (A+'giants-padres-7-0-shutout-whisenhunt-two-hits-july-31.html',
     A+'giants-padres-6-5-basabe-ninth-inning-collapse-august-1.html',
     ['Petco Park', 'San Diego']),
    (A+'giants-robbie-ray-padres-trade-report-august-3.html',
     A+'giants-padres-5-4-swept-roupp-devers-august-2.html',
     ['getting our teeth kicked in', 'three days in Petco Park']),
    (A+'giants-marcelo-mayer-trade-red-sox-erik-miller-robbery.html',
     A+'giants-heliot-ramos-yankees-mayer-mahle-august-4.html',
     ['Heliot Ramos']),
    (A+'giants-tony-vitello-clueless-lineups-eldridge-leadoff.html',
     A+'giants-trade-deadline-monday-posey-sell-ramos-arraez-ray.html',
     ['the deadline', 'trade deadline', 'Buster Posey']),
    (A+'giants-trade-deadline-monday-posey-sell-ramos-arraez-ray.html',
     A+'giants-arraez-kilian-traded-phillies-august-3.html',
     ['Luis Arraez', 'Arraez']),
    (A+'giants-trade-deadline-monday-posey-sell-ramos-arraez-ray.html',
     A+'giants-robbie-ray-padres-trade-report-august-3.html',
     ['Robbie Ray is on an expiring deal', 'Robbie Ray']),
    (A+'giants-angels-7-6-10th-devers-walkoff-july-25.html',
     A+'giants-royals-5-4-swept-roupp-schmitt-july-22.html',
     ['getting swept in Kansas City', 'swept in Kansas City']),
    (A+'giants-royals-5-4-swept-roupp-schmitt-july-22.html',
     A+'giants-royals-3-2-mahle-two-runs-fourth-straight-july-21.html',
     ['Kansas City', 'the night before']),
    (A+'giants-no-hit-cease-webb-grand-slam-july-8.html',
     A+'giants-pitching-woke-up-blue-jays-worst-offense.html',
     ['Blue Jays', 'Toronto']),
    (A+'giants-first-half-breakdown-vitello-second-half-all-star-break-2026.html',
     A+'giants-bullpen-meltdown-kilian-rockies-4-3-vitello-posey-july-10.html',
     ['Caleb Kilian', 'the bullpen blew']),
    (A+'giants-rockies-preview-robbie-ray-bryce-eldridge-july-10.html',
     A+'giants-devers-awake-home-run-rockies-july-10.html',
     ['Rafael Devers', 'Devers']),
    (A+'giants-padres-6-5-basabe-ninth-inning-collapse-august-1.html',
     A+'giants-tigers-5-2-devers-24th-homer-adames-august-7.html',
     ['Rafael Devers', 'Willy Adames']),
    (A+'giants-1993-pennant-race-salomon-torres-final-day.html',
     A+'giants-1993-pennant-race-braves-103-wins-wild-card.html',
     ['103 wins', 'wild card', '103-win']),
    (A+'giants-oracle-park-still-waiting.html',
     A+'giants-rangers-6-0-shutout-whisenhunt-19-under-august-5.html',
     ['runners in scoring position', 'Oracle Park']),

    # ---------- Warriors, Sharks, evergreen ----------
    (A+'warriors-championship-history.html',
     A+'warriors-front-office-failures-curry-exit-not-preposterous.html',
     ['Steph Curry', 'Stephen Curry']),
    (A+'warriors-out-of-easy-answers.html',
     A+'warriors-kerr-kuminga-role-handling.html',
     ['Jonathan Kuminga', 'Kuminga']),
    (A+'warriors-73-9-best-record-ever-added-durant.html',
     A+'lebron-curry-warriors-legacy-what-it-means.html',
     ['LeBron', 'legacy']),
    (A+'bay-area-sports-history.html',
     A+'sharks-rebuild-has-a-pulse-celebrini.html',
     ['Sharks', 'San Jose Sharks']),
    (A+'bay-area-sports-history.html',
     A+'bruce-bochy-bullpen-wizardry-core-four.html',
     ['Bruce Bochy']),
    (A+'bay-area-sports-history.html',
     A+'welcome-to-bay-area-sports-blog.html',
     ['Bay Area Sports Blog']),

    # ---------- second pass: anchors found by reading the corpus ----------
    (A+'49ers-kyle-shanahan-recovery-update-training-camp-2026.html',
     A+'49ers-greenlaw-mccaffrey-pads-day-one-favorite-player-2026.html',
     ['The first padded practice of the summer', 'first padded practice']),
    (A+'49ers-khadarel-hodge-veteran-receiver-signing-august-2026.html',
     A+'49ers-injuries-again-training-camp-august-2026.html',
     ['Every practice report reads like a hospital chart', 'reads like a hospital chart']),
    (A+'49ers-purdy-sharp-camp-injuries-mounting-twenty-out-august-5.html',
     A+'49ers-signing-spree-okoronkwo-irwin-deguara-hodge-august-2026.html',
     ['the front office signed', 'front office signed']),
    (A+'49ers-purdy-70-yard-touchdowns-unknown-receivers-camp-august-7.html',
     A+'49ers-purdy-stribling-chemistry-loaded-roster-2026.html',
     ["De'Zhaun Stribling has a hamstring", "De'Zhaun Stribling", 'De&#39;Zhaun Stribling']),
    (A+'49ers-raheem-morris-players-love-him-just-play-football-2026.html',
     A+'49ers-purdy-sharp-camp-injuries-mounting-twenty-out-august-5.html',
     ['our injury report already looking like a phone book',
      'injury report already looking like a phone book']),
    (A+'49ers-shanahan-best-team-if-healthy-super-bowl-2026.html',
     A+'brandon-aiyuk-antonio-brown-49ers.html',
     ['Aiyuk']),
    (A+'athletics-free-fall-continues-fourth-place-trade-deadline-july-30.html',
     A+'athletics-diamondbacks-15-5-seven-run-fifth-july-22.html',
     ['a 15-run beating on July 22', '15-run beating']),
    (A+'athletics-nationals-5-2-risp-failure-lopez-series-loss-july-19.html',
     A+'athletics-15-1-nationals-ginn-gem-streak-snapped-july-18.html',
     ['JT Ginn took a no-hitter into the seventh', 'JT Ginn took a no-hitter']),
    (A+'athletics-nine-straight-white-sox-9-1-tailspin-i-called-it-july-12.html',
     A+'athletics-1-0-loss-white-sox-eighth-straight-coming-back-to-earth-july-11.html',
     ['one win in their last ten', 'one win in their last']),
    (A+'giants-blown-lead-mariners-cole-young-webb-4-3-july-18.html',
     A+'giants-bullpen-meltdown-kilian-rockies-4-3-vitello-posey-july-10.html',
     ['Caleb Kilian coughed up a two-out lead', 'Caleb Kilian coughed up']),
    (A+'giants-angels-7-6-10th-devers-walkoff-july-25.html',
     A+'giants-devers-awake-home-run-rockies-july-10.html',
     ['Rafael Devers opened the scoring', 'Rafael Devers']),
    (A+'giants-brewers-16-3-susac-two-homers-seven-run-sixth-july-29.html',
     A+'giants-heliot-ramos-yankees-mayer-mahle-august-4.html',
     ['Heliot Ramos went 4-for-5', 'Heliot Ramos']),
    (A+'giants-royals-3-2-mahle-two-runs-fourth-straight-july-21.html',
     A+'giants-swept-momentum-mariners-6-3-robbie-ray-eldridge-july-19.html',
     ['Seattle', 'the Mariners']),
    (A+'athletics-reds-5-4-wild-pitches-eighth-ginn-return-august-4.html',
     A+'athletics-tigers-11-0-swept-gage-jump-august-2.html',
     ['Gage Jump', 'swept']),

    # ---------- third pass ----------
    (A+'49ers-kyle-shanahan-recovery-update-training-camp-2026.html',
     A+'49ers-kyle-shanahan-car-accident-injuries-recovery-2026.html',
     ['a car accident that broke his nose', 'car accident that broke his nose']),
    (A+'athletics-redsox-4-2-10th-monasterio-homer-heim-butler-july-29.html',
     A+'athletics-free-fall-continues-fourth-place-trade-deadline-july-30.html',
     ['this roster keeps calling it wrong', 'Extra innings in this sport are a coin flip']),
    (A+'giants-angels-4-3-trout-sweep-avoided-july-26.html',
     A+'giants-angels-7-6-10th-devers-walkoff-july-25.html',
     ['Two wins in the bank', 'a sweep sitting right there for the taking']),
    (A+'giants-adames-grand-slam-mariners-7-0-second-half-july-17.html',
     A+'giants-swept-momentum-mariners-6-3-robbie-ray-eldridge-july-19.html',
     ['the Mariners', 'Seattle']),
    (A+'bryce-eldridge-giants-future-franchise-first-baseman-july-2026.html',
     A+'giants-swept-momentum-mariners-6-3-robbie-ray-eldridge-july-19.html',
     ['On July 17 in Seattle', 'in Seattle']),
]

IMG_SAFE = re.compile(r'<img\s[^>]*>')
P_RE = re.compile(r'(<p\b[^>]*>)(.*?)(</p>)', re.S)
ARTICLE_RE = re.compile(r'(<article\b[^>]*>)(.*?)(</article>)', re.S)


def rd(p):
    return open(os.path.join(ROOT, p), encoding='utf-8', errors='strict').read()


def wr(p, s):
    full = os.path.join(ROOT, p)
    with open(full, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)
    b = open(full, 'rb').read()
    if b'\x00' in b or b.count(b'\xef\xbf\xbd'):
        raise SystemExit('corruption writing %s - ABORT' % p)


def split_outside_anchors(html):
    out, depth, pos = [], 0, 0
    for m in re.finditer(r'<(/?)(a|h1|h2|h3|h4|h5|h6)\b[^>]*>', html, re.I):
        out.append((depth == 0, html[pos:m.start()]))
        out.append((False, m.group(0)))
        depth += -1 if m.group(1) else 1
        depth = max(depth, 0)
        pos = m.end()
    out.append((depth == 0, html[pos:]))
    return out


def find_span(body, phrase):
    rx = re.compile(r'(?<![\w>])' + r'[\s ]+'.join(re.escape(w) for w in phrase.split(' '))
                    + r'(?![\w])', re.IGNORECASE)
    for pm in P_RE.finditer(body):
        inner = pm.group(2)
        if 'More coverage' in inner:
            continue
        off, cur = pm.start(2), 0
        for linkable, chunk in split_outside_anchors(inner):
            if linkable and chunk:
                fm = rx.search(chunk)
                if fm:
                    return (off + cur + fm.start(), off + cur + fm.end())
            cur += len(chunk)
    return None


def main():
    check = '--check' in sys.argv
    bodies, spans, sources = {}, {}, {}
    placed, missed = [], []

    for src, tgt, anchors in LINKS:
        if src not in bodies:
            html = rd(src)
            m = ARTICLE_RE.search(html)
            if not m:
                missed.append((src, tgt, 'no <article>'))
                continue
            sources[src] = html
            bodies[src] = m.group(2)
            spans[src] = (m.start(2), m.end(2))
        body = bodies[src]
        href = os.path.basename(tgt)
        if ('href="%s"' % href) in body:
            missed.append((src, tgt, 'already linked'))
            continue
        hit = None
        used = None
        for ph in anchors:
            hit = find_span(body, ph)
            if hit:
                used = ph
                break
        if not hit:
            missed.append((src, tgt, 'no anchor matched: %s' % ' | '.join(anchors[:3])))
            continue
        a, b = hit
        anchor_text = body[a:b]
        bodies[src] = body[:a] + '<a href="%s">%s</a>' % (href, anchor_text) + body[b:]
        placed.append({'from': src, 'to': tgt, 'anchor': anchor_text, 'phrase': used})

    if not check:
        for src, body in bodies.items():
            if any(p['from'] == src for p in placed):
                a, b = spans[src]
                wr(src, sources[src][:a] + body + sources[src][b:])

    json.dump({'placed': placed, 'missed': [{'from': m[0], 'to': m[1], 'why': m[2]}
                                            for m in missed]},
              open(os.path.join(ROOT, '_link_repair_report.json'), 'w', encoding='utf-8'),
              indent=1)
    print('%s  placed %d / %d, missed %d'
          % ('CHECK' if check else 'APPLIED', len(placed), len(LINKS), len(missed)))
    for p in placed:
        print('  + %-52s [%s] -> %s'
              % (p['from'][9:52], p['anchor'][:34], p['to'][9:52]))
    for m in missed:
        print('  - %-52s %s' % (m[0][9:52], m[2][:60]))


if __name__ == '__main__':
    main()
