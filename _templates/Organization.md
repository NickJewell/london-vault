---
type: organization
aliases: []
first-seen: "[[<% Book — Chapter N %>]]"
located-in:
part-of:
founded:
dissolved:
period:
---

# <% Organization %>

What it was, when it operated, what it did in London. Like person notes, keep this thin: what the
organization *did* belongs in event notes with the organization as `actor`.

## Members

`member-of` runs from the person to the organization, so members are found by backlink rather than
listed here — a hand-kept list goes stale the moment the next chapter adds someone.

```dataview
LIST FROM "People" WHERE contains(member-of, this.file.link)
```

## Events

```dataview
TABLE date, affected, source FROM "Events"
WHERE contains(actor, this.file.link) OR contains(participated-in, this.file.link)
SORT date ASC
```
