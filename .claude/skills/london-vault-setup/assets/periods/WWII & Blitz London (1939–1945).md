---
type: period
starts: 1939
ends: 1945
preceded-by: "[[Interwar London (1918–1939)]]"
followed-by: "[[Postwar London (1945–1980)]]"
---

# WWII & Blitz London (1939–1945)

Evacuation, the Blitz of 1940–41, the V-1 and V-2 campaigns of 1944–45, and destruction on a scale that set the terms for everything built in the next thirty years.

Boundary years belong to the later period: 1945 is the first year of the next
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
