---
type: event
aliases: []
date:
date-range:
date-precision:
period: "[[<% Period %>]]"
actor:
affected:
caused:
source: "[[<% Book — Chapter N %>]]"
page:
first-seen: "[[<% Book — Chapter N %>]]"
---

# <% What happened (year) %>

What the source says happened, in a few sentences, with the original dating phrasing preserved
("shortly after the Conquest", "in the reign of Richard II") — the ISO date in frontmatter is a
resolution of that phrasing, and a later reader needs to see what was resolved from what.

Fill **exactly one** of `date:` or `date-range:`, never both, and always fill `period:` as well:
the ISO value sorts timelines, the period link answers "show me everything Norman", and neither
substitutes for the other (§4). Delete the frontmatter keys you do not use rather than leaving
them empty — an empty key reads as "checked, nothing there", which is a claim you may not be
making.

## Source

<% Book Title %>, ch. <% N %>, p. <% page %>.
