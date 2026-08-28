---
type: registry
registry: entities
---

# Registry — Master Entity Index

The cross-type index: every canonical name in the vault, its type, aliases, and note path. **Read
this before creating any note** (schema §11, pass 1) and update it after every chapter. It is the
single mechanism keeping chapter 12 consistent with chapter 2 — everything else in the workflow
depends on it being current, so update it in the same commit as the notes it describes.

`Status` is `note` (the note exists) or `reserved` (name fixed in a type registry, note created on
first encounter with real provenance).

<!-- BEGIN generated: taxonomy -->

| Canonical name | Type | Aliases | Note path | Status | First seen |
|---|---|---|---|---|---|
| Pre-Roman London (before 43) | period | — | `Periods/Pre-Roman London (before 43).md` | note | seed |
| Roman London (43–410) | period | — | `Periods/Roman London (43–410).md` | note | seed |
| Saxon London (410–1066) | period | — | `Periods/Saxon London (410–1066).md` | note | seed |
| Norman London (1066–1154) | period | — | `Periods/Norman London (1066–1154).md` | note | seed |
| Medieval London (1154–1485) | period | — | `Periods/Medieval London (1154–1485).md` | note | seed |
| Tudor London (1485–1603) | period | — | `Periods/Tudor London (1485–1603).md` | note | seed |
| Stuart London (1603–1714) | period | — | `Periods/Stuart London (1603–1714).md` | note | seed |
| Georgian London (1714–1837) | period | — | `Periods/Georgian London (1714–1837).md` | note | seed |
| Victorian London (1837–1901) | period | — | `Periods/Victorian London (1837–1901).md` | note | seed |
| 20th-Century London (1901–2000) | period | — | `Periods/20th-Century London (1901–2000).md` | note | seed |

<!-- END generated: taxonomy -->

Names reserved but not yet noted live in the type registries (`places.md`, `people.md`,
`organizations.md`) — those are the working lists during extraction. This table is the union, and
what a reconciliation pass reads first.
