---
type: period
starts: 1980
ends: 2100
preceded-by: "[[Postwar London (1945–1980)]]"
followed-by: 
---

# Modern & Contemporary London (1980–present)

The GLC abolished in 1986, Big Bang and the reinvention of the City, Docklands and Canary Wharf, the Jubilee line extension and Crossrail, and London's return to growth after a century of falling population.

This period is open at its end: `ends` is a working bound so that timelines sort
and date comparisons behave, not a prediction. Material later than the bound still
belongs here — date it with its own ISO year.

This is the last period in the taxonomy, so it has no upper boundary to share.

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
