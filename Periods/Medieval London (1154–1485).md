---
type: period
starts: 1154
ends: 1485
preceded-by: "[[Norman London (1066–1154)]]"
followed-by: "[[Tudor London (1485–1603)]]"
---

# Medieval London (1154–1485)

Mayoralty, guilds and livery companies, the Black Death, the Peasants' Revolt, and the long argument between the City and the Crown.

Boundary years belong to the later period: 1485 is the first year of the next period, not the last
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
