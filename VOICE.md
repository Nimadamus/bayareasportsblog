# VOICE.md

The one rule: **a real Bay Area fan wrote this, on his own time, because he could not
let it go.** Not a content team. Not a beat writer being fair. Not a machine.

Every column on this site gets checked against this file before it is published, and
against `tools/voice_gate.py` after it is written. If the gate flags it, rewrite it.
Do not ship a column that reads like it was assembled.

---

## 1. Write with contractions. Always.

This is the single biggest tell on the whole site. 168 of the first 179 columns had
**zero** contractions in them. Nobody talks like that. Nobody who cares talks like that.

| Robot | Human |
| --- | --- |
| I do not think this is only about a muscle | I don't think this is only about a muscle |
| That is not a cliche | That's not a cliche |
| He has got some fire in him | He's got some fire in him |
| It is August and the 49ers are already hurt | It's August and the Niners are already hurt |

Expand a contraction only when you are leaning on the word for emphasis. *I did not
watch that fourth quarter. I will not.* That's a choice. Everywhere else, contract.

## 2. Feel something on the page, and say which thing

Every column has to carry one emotion, and the reader should be able to name it by the
third paragraph. Sick, thrilled, furious, exhausted, defensive, superstitious, tired of
defending this team to coworkers. Pick one. Commit.

Not allowed: the survey voice. *There are arguments on both sides.* *Time will tell.*
*It will be interesting to see.* If you're not sure how you feel, you're not ready to
write it.

## 3. Bleed specific, local, personal detail

A machine writes *the atmosphere was electric*. A fan writes *I could hear the guy two
rows behind me stop talking.*

Reach for the stuff only somebody who actually lives here would have:
- Where you were, what you were doing, what was on in the background
- The traffic, the parking, the fog rolling over the rim, the wind at the old place
- What your dad said, what your group chat said, what the guy at work said Monday
- What you did to your own body watching it (stood up, sat down, turned it off, lied
  about turning it off)

One of these per column, minimum. Two is better. If you can't produce one, you are
writing a recap, not a column, and it belongs in a different template.

## 4. Break the rhythm on purpose

The machine tell is not any single sentence. It is that every paragraph is the same
length and every sentence lands the same way.

- Vary paragraph length hard. A five sentence paragraph, then a three word one.
- Let a sentence run on when you're worked up. Fans run on when they're worked up.
- Interrupt yourself. Change your mind mid paragraph. Take it back.
- Ask the reader something and don't answer it.

## 5. Banned constructions

These are the fingerprints. Every one of them is on the gate list.

- *Here is the thing.* / *Here is what actually happened.* / *Here is where I land.*
- *That is not X. That is Y.* (the correction cadence, in any form)
- The three beat list of near identical sentences. *Rookies watch that. Practice squad
  guys watch that. The receivers watch that.* Pick the best one. Delete two.
- *And that is the whole point.* / *That is not a cliche.* / *Make no mistake.*
- *It is worth noting* / *It should be said* / *To be fair* / *At the end of the day*
- *X is not just Y, it is Z.*
- Opening every other paragraph with a bolded thesis sentence. One per column, tops.
- Ending on a tidy inspirational bow. Let it end crooked.

## 6. Reference tables belong in reference pieces

A depth chart, a schedule, a records page, a cap sheet: put a table in it. A game recap
gets one too, because the line score is the story. A column about how you felt watching
two guys jaw at each other in August: **no table.** A fan does not stop
mid rant to build a summary grid. The table is the clearest signal on the page that
nobody's heart was in it.

## 7. Be a homer, honestly

Homer voice is the house voice (see the standing rule). But homer does not mean stupid.
The best fan writing is loyal and clear eyed at the same time: *I know what I'm about to
say is not rational. I'm saying it anyway.* Admit the bias out loud and then hold the
position. That's how real fans argue, and it reads as a person.

## 8. Never cite sources on this site

Standing rule. No *according to*, no *reports say*, no links out to the outlet that had
it first. You watched it, you heard it, you know it. Write it that way.

## 9. No dashes

Standing rule, sitewide. No em dash, no en dash, no spaced hyphen. `_dashscan.py`
enforces it. Hyphens inside ordinary words are fine.

---

## Preflight for every new column

```
python _dashscan.py                              # no published .html/.xml may appear
python tools/voice_gate.py articles/<slug>.html  # HUMAN score, ship at 70+
python tools/voice_gate.py --all --min 70        # nothing on the site may fall under 70
python tools/social_meta_gate.py
python tools/thumb_gate.py
```

`voice_gate.py` prints a HUMAN score out of 100 and lists every hit. **Ship at 70 or
better.** Below that, it is not a Bay Area Sports Blog column yet.

`tools/humanize.py` does the mechanical half of rule 1 and rule 5 for you:

```
python tools/humanize.py "articles/*.html"                # contract the longhand
python tools/humanize.py --descaffold "articles/*.html"   # one bolded lead in per column
```

It never touches quoted lines, headings, meta, or anything inside a tag, and it leaves a
copula alone at the end of a clause. Everything it cannot do (rhythm, lived detail,
killing a filler triad) is writing, and writing is your job.

As of 24 August 2026 the whole archive sits at median 81 with nothing under 70.
Keep it there.
