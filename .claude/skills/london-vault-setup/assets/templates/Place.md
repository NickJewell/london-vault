---
type: <% structure | ward | district | street | parish | settlement %>
aliases: []
first-seen: "[[<% Book — Chapter N %>]]"
part-of:
located-in:
named-after:
on-site-of:
succeeded-by:
---

# <% Name (role) %>

One or two sentences of identification — what this is and where. The history goes in the period
sections below, not here.

Place notes are structured **diachronically**: one heading per period in which the source says
something about this place, in chronological order. A *state* ("the gate stood two storeys high",
"the ward was the poorest in the City") is described here under its period. A *change of state*
("rebuilt in 1479", "demolished in 1760") becomes an event note, linked from the relevant section
with an arrow — schema §5. That split is what makes "all structural changes to the wall and gates,
sorted by date" a query rather than a re-read.

## Roman

## Saxon

## Norman

## Medieval

## Tudor

## Stuart

## Georgian

## Victorian

## 20th century

Delete the period headings this source says nothing about; keep the order of the rest.

## Events here

```dataview
TABLE date AS "Date", actor AS "Actor", period AS "Period", source AS "Source"
FROM "Events"
WHERE contains(affected, this.file.link) OR contains(located-in, this.file.link)
SORT date ASC
```
