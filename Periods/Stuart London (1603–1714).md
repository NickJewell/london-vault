---
type: period
starts: 1603
ends: 1714
preceded-by: "[[Tudor London (1485–1603)]]"
followed-by: "[[Georgian London (1714–1837)]]"
---

# Stuart London (1603–1714)

Civil War, the Great Plague of 1665, the Great Fire of 1666 and the rebuilding, the Bank of England, and the beginnings of the West End.

Boundary years belong to the later period: 1714 is the first year of the next
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
