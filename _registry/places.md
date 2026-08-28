---
type: registry
registry: places
---

# Registry — Places

Canonical place names **shown as a hierarchy**, not a flat list (schema §1). Read this before
creating any place note. Two columns matter:

- **Canonical note name** — the exact filename to link to. Copy it; do not retype role suffixes.
- **Status** — `note` means the note exists; `reserved` means the name is fixed but the note is
  created on first encounter in a text, so that its `first-seen` provenance is real (schema §2).
  Never pre-create reserved notes in bulk: a note with no source is a note nobody can check.

## Multi-role names — the Aldgate rule (schema §3)

These names denote several distinct things. Never merge them. Decide the role from context; if
genuinely ambiguous, link the **district/area** note and add `#flag/ambiguous-place`.

| Name in text | Gate | Ward | District/area | Street | Other |
|---|---|---|---|---|---|
| Aldgate | `Aldgate (gate)` | `Aldgate Ward` | `Aldgate (area)` | `Aldgate High Street` | — |
| Bishopsgate | `Bishopsgate (gate)` | `Bishopsgate Ward` | `Bishopsgate (area)` | `Bishopsgate (street)` | — |
| Cripplegate | `Cripplegate (gate)` | `Cripplegate Ward` | `Cripplegate (area)` | — | — |
| Aldersgate | `Aldersgate (gate)` | `Aldersgate Ward` | `Aldersgate (area)` | `Aldersgate Street` | — |
| Newgate | `Newgate (gate)` | — | — | `Newgate Street` | `Newgate Prison` |
| Ludgate | `Ludgate (gate)` | — | `Ludgate (area)` | `Ludgate Hill` | `Ludgate Prison` |
| Moorgate | `Moorgate (gate)` | — | `Moorfields` | `Moorgate (street)` | — |
| Westminster | — | — | — | — | `Westminster Abbey`, `Palace of Westminster`, `City of Westminster` |
| Southwark | — | `Bridge Ward Without` | `Southwark` | — | `Liberty of the Clink`, `Borough High Street` |
| Bridge | — | `Bridge Ward` | — | — | `London Bridge` |
| Tower | — | `Tower Ward` | — | — | `Tower of London`, `Tower Hill` |
| Queenhithe | — | `Queenhithe Ward` | — | — | `Queenhithe (dock)` |
| Billingsgate | — | `Billingsgate Ward` | — | — | `Billingsgate Market` |
| Castle Baynard | — | `Castle Baynard Ward` | — | — | `Baynard's Castle` |
| Smithfield | — | — | `Smithfield` | — | `St Bartholomew's Priory`, `Smithfield Market` |
| Blackfriars | — | — | `Blackfriars` | — | `Blackfriars Priory`, `Blackfriars Bridge` |
| Charterhouse | — | — | `Charterhouse` | — | `London Charterhouse` |
| Temple | — | — | `The Temple` | — | `Temple Church`, `Inner Temple`, `Middle Temple` |
| Cheapside / Cheap | — | `Cheap Ward` | — | `Cheapside` | — |
| Cornhill | — | `Cornhill Ward` | — | `Cornhill (street)` | — |

Add a row whenever extraction turns up a new multi-role name. That is the single highest-value
maintenance act in this registry — an unrecorded multi-role name is how the same gate ends up as
three half-populated notes six chapters later.

## Settlements — top of the hierarchy

| Canonical note name | Type | part-of | Status |
|---|---|---|---|
| `London` | settlement | — | reserved |
| `City of London` | settlement | `[[London]]` | reserved |
| `City of Westminster` | settlement | `[[London]]` | reserved |
| `Southwark` | settlement | `[[London]]` | reserved |
| `Lundenwic` | settlement | — | reserved |
| `Londinium` | settlement | — | reserved |

`Londinium` and `Lundenwic` are separate notes from `London`, not aliases of it: Lundenwic sat
outside the walls around the Strand while the walled Roman city stood largely empty, so merging
them would assert a continuity the archaeology denies. Link with `on-site-of` / `succeeded-by`.

## The 25 wards of the City of London

All are `type: ward`, `part-of: "[[City of London]]"`, status `reserved`.

| Ward note | Named after (`named-after`) |
|---|---|
| `Aldersgate Ward` | `[[Aldersgate (gate)]]` |
| `Aldgate Ward` | `[[Aldgate (gate)]]` |
| `Bassishaw Ward` | — |
| `Billingsgate Ward` | `[[Billingsgate (dock)]]` |
| `Bishopsgate Ward` | `[[Bishopsgate (gate)]]` |
| `Bread Street Ward` | `[[Bread Street]]` |
| `Bridge Ward` | `[[London Bridge]]` |
| `Broad Street Ward` | `[[Broad Street]]` |
| `Candlewick Ward` | `[[Candlewick Street]]` |
| `Castle Baynard Ward` | `[[Baynard's Castle]]` |
| `Cheap Ward` | `[[Cheapside]]` |
| `Coleman Street Ward` | `[[Coleman Street]]` |
| `Cordwainer Ward` | — |
| `Cornhill Ward` | `[[Cornhill (street)]]` |
| `Cripplegate Ward` | `[[Cripplegate (gate)]]` |
| `Dowgate Ward` | `[[Dowgate]]` |
| `Farringdon Within` | `[[Farringdon Ward]]` |
| `Farringdon Without` | `[[Farringdon Ward]]` |
| `Langbourn Ward` | — |
| `Lime Street Ward` | `[[Lime Street]]` |
| `Portsoken Ward` | — |
| `Queenhithe Ward` | `[[Queenhithe (dock)]]` |
| `Tower Ward` | `[[Tower of London]]` |
| `Vintry Ward` | — |
| `Walbrook Ward` | `[[Walbrook]]` |

Ward notes worth knowing about before you meet them in a text:

- **Farringdon** was a single ward until 1394, when it split into Within and Without. A text
  discussing pre-1394 Farringdon means the undivided ward: link `Farringdon Ward` (reserved) and
  record the split as an event.
- **Bridge Ward Without** covered Southwark and was a ward in name from 1550; it was merged into
  Bridge Ward in 1978, which is why the modern count is 25 rather than 26. Texts before 1978 that
  say "the twenty-six wards" are correct for their date — do not "fix" them.
- **Cripplegate** and **Farringdon** both have Within/Without divisions; only Farringdon's are
  separate wards.
- **Portsoken** lay outside the wall and was held by the Knighten Guild, then by Holy Trinity
  Priory — its alderman was the prior, which is unusual enough that texts often dwell on it.

## The gates of the City wall

All `type: structure`, `part-of: "[[London Wall]]"`, status `reserved`.

| Gate note | Notes |
|---|---|
| `Aldgate (gate)` | Roman origin; rebuilt 1215, 1607–09; demolished 1761 |
| `Bishopsgate (gate)` | Roman origin; rebuilt 1479 by Hanseatic merchants, 1735; demolished 1760 |
| `Cripplegate (gate)` | Roman origin (fort gate); demolished 1760 |
| `Aldersgate (gate)` | Roman origin; rebuilt 1617; demolished 1761 |
| `Newgate (gate)` | Roman origin; rebuilt after 1666; demolished 1767. Distinct from `Newgate Prison` |
| `Ludgate (gate)` | Rebuilt 1215, 1586; demolished 1760 |
| `Moorgate (gate)` | Not Roman — a postern of 1415, widened 1472; demolished 1762 |

Related openings that are **not** among the seven and get their own notes: `Bridge Gate` (on
London Bridge), `Postern Gate` (by the Tower), `Aldermanbury Postern`, `Temple Bar` (a City
boundary marker on the Strand, not a wall gate — a frequent confusion worth checking).

## Major landmarks and features

| Canonical note name | Type | Status |
|---|---|---|
| `Tower of London` | structure | reserved |
| `St Paul's Cathedral` | structure | reserved |
| `Old St Paul's` | structure | reserved |
| `London Bridge` | structure | reserved |
| `London Wall` | structure | reserved |
| `Westminster Abbey` | structure | reserved |
| `Palace of Westminster` | structure | reserved |
| `Guildhall` | structure | reserved |
| `Royal Exchange` | structure | reserved |
| `Baynard's Castle` | structure | reserved |
| `The Monument` | structure | reserved |
| `River Thames` | feature | reserved |
| `Walbrook` | feature | reserved |
| `River Fleet` | feature | reserved |
| `Moorfields` | district | reserved |
| `Smithfield` | district | reserved |
| `The Strand` | street | reserved |
| `Cheapside` | street | reserved |
| `Fleet Street` | street | reserved |
| `Watling Street` | street | reserved |

`Old St Paul's` (the Norman cathedral burnt in 1666) and `St Paul's Cathedral` (Wren's, from
1675) are separate notes on the same site — a textbook `on-site-of` / `succeeded-by` pair under
the name-drift rule (§3), not one note with a long history section. The Saxon and earlier
cathedrals on the site fold into `Old St Paul's` unless a text treats them as distinct builds.

`River Thames` and `Walbrook` use `type: feature`, which is **outside** the schema's type list
(§2). Rivers are not settlements, structures, or districts, and forcing one of those would be a
lie in the data. Tag these notes `#flag/vocab-gap` so the gap surfaces for the user's ruling.
