---
type: period
starts: 410
ends: 1066
preceded-by: "[[Roman London (43–410)]]"
followed-by: "[[Norman London (1066–1154)]]"
---

# Saxon London (410–1066)

The walled city stands mostly empty while Lundenwic grows along the Strand; Alfred re-occupies the walls in 886 and the burh becomes London again.

Boundary years belong to the later period: 1066 is the first year of the next period, not the last
of this one (see `_registry/periods.md`). Where a source draws the line differently, follow the
registry and note the discrepancy in the event body — the value of these links is that they mean
the same thing in every chapter.

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
