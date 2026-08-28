---
type: person
aliases: []
first-seen: "[[<% Book — Chapter N %>]]"
resided-at:
buried-at:
member-of:
held-office:
---

# <% Name %>

Two or three sentences: who they were, when, and why this vault has heard of them. No more.

Do **not** write an "activities" or "career" section here. Everything this person *did* belongs in
event notes with `actor: "[[<% Name %>]]"`, and the section below derives it — a hand-written
narrative would drift out of step with the events the moment the next chapter is extracted, and
you would have no way to tell which version was right.

## Offices

`held-office:: [[Office]]` with dates in prose beside it, e.g.
`held-office:: [[Lord Mayor of London]]` — 1397, 1398, 1406, 1419.

## Footprint

```dataview
TABLE date AS "Date", affected AS "Affected", period AS "Period", source AS "Source"
FROM "Events"
WHERE contains(actor, this.file.link) OR contains(participated-in, this.file.link)
SORT date ASC
```

## Claims involving this person

```dataview
TABLE confidence, statement, source
FROM "Claims"
WHERE contains(involves, this.file.link)
SORT confidence ASC
```
