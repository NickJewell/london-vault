---
type: period
starts: 1918
ends: 1939
preceded-by: "[[Edwardian & WWI London (1901–1918)]]"
followed-by: "[[WWII & Blitz London (1939–1945)]]"
---

# Interwar London (1918–1939)

Ribbon development and Metro-land, the LCC cottage estates, the slump and the hunger marches, Underground expansion under Pick and Holden, and the first arguments for a Green Belt.

Boundary years belong to the later period: 1939 is the first year of the next
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
