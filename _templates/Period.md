---
type: period
starts:
ends:
preceded-by:
followed-by:
---

# <% Period name %>

The nine period notes are seeded by `london-vault-setup` and the taxonomy is fixed (§4). This
template exists for reference, not for routine use — creating a tenth period is a schema change,
so put it to the user rather than filling this in mid-extraction.

## Events in this period

```dataview
TABLE date, actor, affected, source FROM "Events"
WHERE contains(period, this.file.link)
SORT date ASC
```
