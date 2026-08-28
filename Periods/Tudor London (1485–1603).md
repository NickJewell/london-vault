---
type: period
starts: 1485
ends: 1603
preceded-by: "[[Medieval London (1154–1485)]]"
followed-by: "[[Stuart London (1603–1714)]]"
---

# Tudor London (1485–1603)

Dissolution of the monasteries redraws the map of the city; population growth, the first suburbs, and the Royal Exchange.

Boundary years belong to the later period: 1603 is the first year of the next
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
