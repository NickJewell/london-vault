---
type: registry
registry: people
---

# Registry — People

Canonical person names and **all** known aliases. Check here before creating a person note; the
alias column is what stops "Dick Whittington", "Richard Whittington" and "Whittington" becoming
three notes with a third of a life each.

## Naming convention

- **Monarchs**: regnal name and number, no epithet — `Henry II`, `Richard I`, `Edward the
  Confessor` (no number exists, so the epithet is the name). Epithets go in `aliases`:
  `Richard the Lionheart`, `William the Conqueror`.
- **Everyone else**: the fullest form the sources give — `Richard Whittington`, not `Dick
  Whittington` or `Whittington`.
- **Disambiguate by dates when two people share a name**: `Thomas More (1478–1535)`. Only add the
  qualifier when there is an actual collision; a qualifier on a unique name is noise that every
  future link has to reproduce exactly.
- **Titles and offices are not names.** "the Bishop of London" is an office
  (`held-office`), not a person. If the text never names the holder, do not invent a person note —
  route the statement to an event with the organization or office as `actor` and flag
  `#flag/unnamed-actor`.

## Register

| Canonical name | Aliases | Note | First seen |
|---|---|---|---|

Monarchs are **not** pre-seeded here. Their reign dates live in `reigns.md`, which is a lookup
table, not a claim that the vault knows anything about them; a person note gets created the first
time a text actually says something about the person, so that `first-seen` means what it says.
When you do create one, copy the canonical name from `reigns.md` exactly.
