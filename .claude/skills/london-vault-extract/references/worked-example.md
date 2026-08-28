# A chapter passage, extracted end to end

One short passage taken through both passes, so the shape of the output is unambiguous. The book
and page numbers here are illustrative — the structure is what to copy.

## The passage

> Chapter 8, p. 214. *Ackroyd, London: The Biography.*
>
> Bishopsgate had stood since the Roman city, though the gate the Tudors knew was a rebuilding of
> 1479, paid for by the Hanseatic merchants of the Steelyard in return for the right to keep it in
> repair — a bargain that some historians have read as the City selling a piece of its own defence.
> The ward beyond the wall grew rich on the same trade. By the reign of Elizabeth the parish of St
> Botolph without Bishopsgate was among the most crowded in London, and Stow, writing in 1598,
> thought its poverty a disgrace to the City.

## Pass 1 — entities

Every candidate, checked against `_registry/entities.md` before anything is created:

| Mention | Resolution | Action |
|---|---|---|
| "Bishopsgate" (the gate, rebuilt) | `Bishopsgate (gate)` — structure | create; reserved in `places.md` |
| "The ward beyond the wall" | `Bishopsgate Ward` — ward | create |
| "the Roman city" | `Londinium` — settlement | create |
| "Hanseatic merchants" | `Hanseatic League` — organization | create |
| "the Steelyard" | `Steelyard` — structure | create; **new multi-role name?** no — single role |
| "the reign of Elizabeth" | `Elizabeth I` | no note: the reign is used only for dating, and the passage says nothing about her → look up `reigns.md`, no person note |
| "St Botolph without Bishopsgate" | `St Botolph without Bishopsgate` — parish | create |
| "Stow" | `John Stow` — person | create |
| "the City" | `City of London` — settlement | create |
| "the wall" | `London Wall` — structure | create |

Note the two judgement calls. **Elizabeth I gets no note**: she appears only as a dating device,
and §2's `first-seen` would be recording an encounter that did not happen. **"Bishopsgate" splits**
across two roles in three sentences — the gate is rebuilt, the ward grows rich — and each mention
is linked to the role its own sentence is about.

`Steelyard` is worth a second's thought as a multi-role candidate (the Hanseatic depot, the
riverside site, the later wharf). Here the passage means the depot; a later chapter that treats
the site separately would add a row to the multi-role table then.

## Pass 2 — events, claims, relationships

### `Events/Rebuilding of Bishopsgate (1479).md`

```yaml
---
type: event
date: 1479
period: "[[Medieval London (1154–1485)]]"
actor: "[[Hanseatic League]]"
affected: "[[Bishopsgate (gate)]]"
source: "[[Ackroyd, London: The Biography — Chapter 8]]"
page: 214
first-seen: "[[Ackroyd, London: The Biography — Chapter 8]]"
---
```

Body records that the merchants of the Steelyard paid for the rebuilding in exchange for the right
to keep the gate in repair, and that the gate the Tudors knew was this one rather than the Roman
original. 1479 is Medieval, not Tudor — the taxonomy runs to 1485, and the period link follows the
table rather than the passage's mention of "the Tudors".

### `Claims/Bishopsgate bargain as sale of City defence.md`

```yaml
---
type: claim
statement: "The 1479 arrangement, by which Hanseatic merchants funded and maintained Bishopsgate in exchange for repair rights, amounted to the City ceding control of part of its own defences."
asserted-by: "[[Ackroyd, London: The Biography — Chapter 8]]"
confidence: quoted-third-party
evidence: "The 1479 rebuilding agreement, discussed at p. 214"
source: "[[Ackroyd, London: The Biography — Chapter 8]]"
page: 214
involves: ["[[Hanseatic League]]", "[[Bishopsgate (gate)]]", "[[City of London]]"]
date: 1479
period: "[[Medieval London (1154–1485)]]"
---
```

The confidence value is the whole point of this note. The text says "**some historians have
read**" — a hedge, attributing the reading to unnamed others. Recorded as `stated-fact` it would
become, permanently and undetectably, something Ackroyd asserted. The body quotes the hedging
clause verbatim so the reading can be checked.

### `Claims/St Botolph without Bishopsgate poverty (Stow).md`

```yaml
---
type: claim
statement: "The poverty of the parish of St Botolph without Bishopsgate was a disgrace to the City."
asserted-by: "[[John Stow]]"
confidence: quoted-third-party
evidence: "Stow, Survey of London, 1598, cited at p. 214"
source: "[[Ackroyd, London: The Biography — Chapter 8]]"
page: 214
involves: ["[[St Botolph without Bishopsgate]]", "[[City of London]]"]
date: 1598
period: "[[Tudor London (1485–1603)]]"
---
```

Stow's judgement is his, quoted by Ackroyd — `asserted-by` is Stow, `source` is the chapter that
carries it. Keeping those two fields distinct is what lets a later reconciliation ask "what does
this vault have from Stow?" across every book.

### States, not events

"The parish was among the most crowded in London by Elizabeth's reign" is a **state**. It goes in
`Places/St Botolph without Bishopsgate.md` under `## Tudor`, with `date-range: 1558/1603` resolved
from `_registry/reigns.md` and the phrase "by the reign of Elizabeth" preserved in the prose. No
event note: nothing changed at a moment.

"The ward beyond the wall grew rich on the same trade" is also a state — a trend without a date is
not an event. It goes under `## Medieval` in `Places/Bishopsgate Ward.md`.

### Place note sections

`Places/Bishopsgate (gate).md` gains, appended under a `## Ackroyd, London: The Biography —
Chapter 8` heading:

```markdown
## Roman
Stood since the Roman city as part of [[London Wall]].

## Medieval
Rebuilt 1479 at the expense of the Hanseatic merchants of the [[Steelyard]], in return for the
right to keep it in repair → [[Rebuilding of Bishopsgate (1479)]]
```

## Finishing

`Sources/Ackroyd, London: The Biography — Chapter 8.md` records the counts (9 new entities, 1
event, 2 claims), no flags raised, and the judgement calls: Elizabeth I not created as a person;
"Bishopsgate" split gate/ward per sentence; 1479 assigned to Medieval on the boundary rule.

`_registry/entities.md` gains nine rows. `_registry/places.md` gains nothing new to the multi-role
table — Bishopsgate is already there — but `people.md` gains John Stow and `organizations.md` the
Hanseatic League.

```bash
python3 .claude/scripts/validate_vault.py --vault .
git add -A && git commit -m "Extract: Ackroyd, London: The Biography ch.8"
```
