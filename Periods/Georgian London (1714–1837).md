---
type: period
starts: 1714
ends: 1837
preceded-by: "[[Stuart London (1603–1714)]]"
followed-by: "[[Victorian London (1837–1901)]]"
---

# Georgian London (1714–1837)

The gates come down, the squares go up, the docks are built, and London becomes the largest city in the world.

Boundary years belong to the later period: 1837 is the first year of the next
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
