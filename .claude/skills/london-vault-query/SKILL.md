---
name: london-vault-query
description: Answer questions from the London history Obsidian vault and build the Dataview queries that derive its views — a person's footprint across the city, everything in a period, structural changes to the wall and gates sorted by date, claims by confidence level, what a given book contributed, timelines. Use when the user asks what the vault knows about a person, place, period or theme, asks for a timeline or a sorted list of events, asks to add or fix a Dataview block in a note, or asks how to see something the vault should be able to show. Also use when a query returns nothing and the reason needs diagnosing.
---

# London Vault — Querying and derived views

The schema is built so that the interesting questions are *queries*, not re-reads: a person's
footprint (§6), everything Norman (§4), all structural changes to the wall and gates sorted by
date (§5). This skill covers writing those queries and answering questions from the vault.

Dataview is installed, so the query blocks in the templates render and a question can be answered
by adding a query to a note. But you cannot see what a query renders — Dataview evaluates inside
Obsidian, not here. When the user wants an *answer* rather than a query block, read the vault
directly as below; when they want a *view*, write the query into the note. Do not write a query,
assume its output, and report that as the answer.

## Answering from the vault directly

For a question the user wants answered rather than a query block installed, read the vault:

```bash
grep -rl 'actor:.*Henry II' Events/                       # what did Henry II do
grep -rl 'period:.*Norman London' Events/ Claims/          # everything Norman
grep -rh '^date:' Events/ | sort                           # a crude timeline
grep -rl 'confidence: disputed' Claims/                    # where sources disagree
grep -rl 'source:.*Chapter 8' . --include='*.md'           # what chapter 8 contributed
```

Read the notes the grep finds rather than answering from filenames — the frontmatter is a handle,
not the content, and the judgement calls that matter are usually in the body.

Always answer with provenance. Every fact in the vault carries a source and page precisely so that
an answer can carry them too; an answer without them puts the user back where they started.

## Query recipes

The full set, with the reasoning behind each, is in `references/dataview-recipes.md` — read it
when writing a query block into a note, or when a query returns nothing and you need the usual
causes. The four that matter most:

**A person's footprint** (§6 — this is what justifies thin person notes):

````
```dataview
TABLE date AS "Date", affected AS "Affected", period AS "Period", source AS "Source"
FROM "Events"
WHERE contains(actor, this.file.link) OR contains(participated-in, this.file.link)
SORT date ASC
```
````

**Everything in a period** (§4 — why the period link exists alongside the ISO date):

````
```dataview
TABLE date, actor, affected, source FROM "Events"
WHERE contains(period, this.file.link) SORT date ASC
```
````

**Structural changes to the wall and gates, sorted by date** (§5 — the query the state-vs-event
rule is built for):

````
```dataview
TABLE date AS "Date", actor AS "Actor", affected AS "Structure", source AS "Source"
FROM "Events"
WHERE any(map(affected, (a) => contains(string(a), "gate") OR contains(string(a), "Wall")))
SORT date ASC
```
````

**Hedged and disputed claims** (§8 — the audit the `confidence` field exists for):

````
```dataview
TABLE confidence, statement, asserted-by, source FROM "Claims"
WHERE confidence != "stated-fact" SORT confidence ASC
```
````

## When a query returns nothing

Almost always one of five things, in rough order of likelihood:

1. **The link is a string, not a link.** `period: Norman London (1066–1154)` does not match
   `contains(period, this.file.link)`; it needs `period: "[[Norman London (1066–1154)]]"`.
2. **En dash vs. hyphen.** Period note names use `–` (U+2013). A link typed with `-` silently
   fails to resolve. This is the single most common cause.
3. **The material was written as prose, not as an event.** A rebuilding described in a place note's
   body but never given an event note is invisible to every event query — a state-vs-event error
   (§5), and the fix is to create the event, not to loosen the query.
4. **Wrong folder.** `FROM "Events"` misses an event note filed under `/Places`.
5. **The block is not tagged `dataview`**, so it renders as a plain code fence. The opening fence
   must read ```` ```dataview ````.

Before concluding the vault lacks something, check 1–3 — the difference between "the vault does
not know this" and "the vault knows this and the query cannot see it" matters enormously, and only
the first is a reason to go back to the book.

## Reporting a gap

If the vault genuinely does not have what was asked for, say which chapters have been extracted
(`ls Sources/`) and what would have to be read to fill the gap. Do not fill it from general
knowledge of London history: an unsourced note is indistinguishable from an extracted one once it
is in the vault, and it defeats the provenance discipline that makes everything else trustworthy.
