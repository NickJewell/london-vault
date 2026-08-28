---
type: period
starts: 1901
ends: 1918
preceded-by: "[[Victorian London (1837–1901)]]"
followed-by: "[[Interwar London (1918–1939)]]"
---

# Edwardian & WWI London (1901–1918)

Edwardian confidence and its unravelling: suburban growth along the new tube lines, the LCC at its most ambitious, and the first air raids on the city — Zeppelins from 1915, Gothas from 1917.

Boundary years belong to the later period: 1918 is the first year of the next
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
