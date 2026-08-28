---
type: period
starts: -4000
ends: 43
preceded-by: 
followed-by: "[[Roman London (43–410)]]"
---

# Pre-Roman London (before 43)

Thames-valley prehistory before the invasion of 43: Neolithic and Bronze Age activity along the river, Bronze Age timber structures and weapon deposits, and the Iron Age territories of the Trinovantes and Catuvellauni.

The starting bound of 4000 BCE is a convention, not a finding — it marks roughly where Thames-valley evidence becomes continuous rather than scattered. Earlier Palaeolithic and Mesolithic material belongs in this period too; date it with its own ISO year and ignore the nominal bound.

The substantive point most sources make about this period is a negative one: there is no evidence of a substantial settlement on the site the Romans chose, which makes Londinium a foundation rather than a continuation. Where an author argues otherwise, that is a claim note (§8), not a correction to this period.

This period is open at its start: `starts` is a working bound so that timelines
sort, not a claim about when the story begins.

Boundary years belong to the later period: 43 is the first year of the next
period, not the last of this one (see `_registry/periods.md`). Where a source draws the
line differently, follow the registry and note the discrepancy in the event body — the
value of these links is that they mean the same thing in every chapter.

## Events in this period

```dataview
TABLE date AS "Date", actor AS "Actor", affected AS "Affected", source AS "Source"
FROM "Events"
WHERE contains(period, this.file.link)
SORT date ASC
```

## Claims about this period

```dataview
TABLE confidence AS "Confidence", statement AS "Claim", source AS "Source"
FROM "Claims"
WHERE contains(period, this.file.link)
SORT confidence ASC
```

## Places with material from this period

```dataview
LIST FROM "Places" WHERE contains(file.outlinks, this.file.link)
```
