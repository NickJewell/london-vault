---
type: period
starts: 1945
ends: 1980
preceded-by: "[[WWII & Blitz London (1939–1945)]]"
followed-by: "[[Modern & Contemporary London (1980–present)]]"
---

# Postwar London (1945–1980)

Reconstruction and the Abercrombie plan, the new towns, Windrush and post-war migration, comprehensive redevelopment and the tower block, the GLC, and the long collapse of the docks.

Named 1945–1980 rather than 1945–1979 to keep the taxonomy's shared-boundary convention: a period's label ends on the year the next one begins, so no year falls between two periods. The substance is unchanged — 1979 is the last full year of this period.

Boundary years belong to the later period: 1980 is the first year of the next
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
