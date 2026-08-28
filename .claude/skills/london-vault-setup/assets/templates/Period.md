---
type: period
starts:
ends:
preceded-by:
followed-by:
---

# <% Period name %>

Period notes are generated from `assets/taxonomy.json` by `london-vault-setup`'s
`build_periods.py`, so this template is for reference, not for routine use. Adding a period is a
schema change (§4): put it to the user, edit the taxonomy data, and regenerate — hand-writing a
period note leaves the registry table and the preceded-by/followed-by chain out of step.

## Events in this period

```dataview
TABLE date, actor, affected, source FROM "Events"
WHERE contains(period, this.file.link)
SORT date ASC
```
