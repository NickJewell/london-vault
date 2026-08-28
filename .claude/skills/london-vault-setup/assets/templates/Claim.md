---
type: claim
statement: "<% The assertion, paraphrased in one or two sentences %>"
asserted-by: "[[<% Author or quoted third party %>]]"
confidence: <% stated-fact | author-interpretation | quoted-third-party | disputed %>
evidence: "<% What the assertion rests on, and where %>"
source: "[[<% Book — Chapter N %>]]"
page:
involves: []
disputes:
supports:
date:
period: "[[<% Period %>]]"
first-seen: "[[<% Book — Chapter N %>]]"
---

# <% Short label for the claim %>

The passage in the author's own terms, with the hedging **intact**. If the text says "some
historians argue", the note says "some historians argue" and `confidence: quoted-third-party` — a
hedged claim flattened into a stated fact is the one extraction error that cannot be detected
later from the vault alone, because the hedge is gone and nothing looks wrong.

Quote the sentence that carries the hedge if there is any doubt about which reading is right.

## Confidence

- `stated-fact` — the author asserts it flatly as established.
- `author-interpretation` — the author's own reading, argued rather than reported.
- `quoted-third-party` — attributed to someone else ("Stow says", "some historians argue").
- `disputed` — the author records disagreement, or this claim is contradicted by another note.

## Related claims

`disputes:: [[Other claim]]` / `supports:: [[Other claim]]`
