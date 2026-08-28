---
type: period
starts: 1837
ends: 1901
preceded-by: "[[Georgian London (1714–1837)]]"
followed-by: "[[Edwardian & WWI London (1901–1918)]]"
---

# Victorian London (1837–1901)

Railways, sewers, the Underground, the Metropolitan Board of Works, and the slums that all of it was meant to answer.

Boundary years belong to the later period: 1901 is the first year of the next
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
