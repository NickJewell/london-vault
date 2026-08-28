---
type: schema
version: 1.0
status: canonical
---

# London Vault — Semantic Schema & Extraction Rules

This document is the canonical rulebook for extracting entities, relationships, events, and claims from London history texts into this Obsidian vault. Every extraction session must follow it exactly. If a rule here conflicts with an instinct about "better" structure, follow the rule — consistency across chapters and books is worth more than local elegance. Propose schema changes as suggestions to the user; never improvise them mid-extraction.

> **Where the skills live.** The procedures that implement this schema are project skills in `.claude/skills/`:
> `london-vault-setup` (§12), `london-vault-extract` (§11), `london-vault-reconcile` (§11 reconciliation), `london-vault-query` (§5–§6 derived views).
> This document governs the *data model*; the skills govern *procedure*. Where a skill and this document disagree about the model, this document wins.

---

## 1. Vault structure

```
/People
/Places
/Organizations
/Events
/Periods
/Concepts
/Claims
/Sources          (one note per chapter processed)
/_registry        (canonical entity indexes — read before every extraction)
/_templates       (note templates per entity type)
```

**Registry files** (in `/_registry`):

| File | Contents |
|---|---|
| `places.md` | Canonical place notes **with hierarchy shown**, not a flat list. Wards, gates, districts, streets, buildings, and their containment relationships. |
| `people.md` | Canonical person names + all known aliases. |
| `organizations.md` | Guilds, religious houses, companies, institutions. |
| `periods.md` | The period taxonomy (§4). |
| `reigns.md` | Monarch → reign date-range lookup table (§7). |
| `entities.md` | Master cross-type index: canonical name, type, aliases, note path. |

---

## 2. Entity types

Every note carries YAML frontmatter with at minimum: `type`, `aliases`, `first-seen` (source + chapter where first encountered).

| `type` value | Folder | Notes |
|---|---|---|
| `person` | /People | Thin biographies; substance lives in events (§6). |
| `structure` | /Places | Gates, walls, bridges, buildings. |
| `ward` | /Places | The City's 25 wards. |
| `district` | /Places | General areas (e.g. "Aldgate" as a neighbourhood). |
| `street` | /Places | Streets and roads. |
| `parish` | /Places | Ecclesiastical parishes. |
| `settlement` | /Places | London itself, Westminster, Southwark, Lundenwic, etc. |
| `organization` | /Organizations | Guilds, priories, livery companies, Hanseatic League. |
| `event` | /Events | Anything that *happened* at a time (§5). |
| `period` | /Periods | First-class period notes (§4). |
| `concept` | /Concepts | Terms, institutions-as-ideas (e.g. "sanctuary", "liberty"). |
| `claim` | /Claims | First-class claim notes (§8). |
| `source` | /Sources | One per chapter processed. |

---

## 3. Place hierarchy: split by role, not by name

**The Aldgate rule.** One name often denotes several distinct things — a gate, a ward, a district. Never merge these into one note; create a separate note per role, linked explicitly:

```
Aldgate (gate).md      type: structure
Aldgate Ward.md        type: ward
Aldgate (area).md      type: district
```

```yaml
# Aldgate Ward.md
type: ward
part-of: "[[City of London]]"
named-after: "[[Aldgate (gate)]]"
aliases: [Aldgate]
```

This pattern recurs constantly: Bishopsgate, Cripplegate, Ludgate, Newgate (gate/ward/street/prison), Westminster (abbey/palace/city), Southwark (borough/liberty). The registry must list all role-variants of a name.

**Disambiguation rule for extraction:** when the text says "Aldgate" (or any multi-role name), decide from context which role is meant and link to that specific note. If genuinely ambiguous, link the district/area note and add `#flag/ambiguous-place` so it surfaces in review.

**Name drift rule:** if a place is renamed but is the same continuous entity, keep one note and add the old name to `aliases`. If it is genuinely a different thing on the same site (Roman basilica → medieval Leadenhall), create separate notes linked with `on-site-of` and `succeeded-by`.

---

## 4. Periods as first-class notes

The period taxonomy is fixed upfront in `/Periods` and `_registry/periods.md`:

```
Pre-Roman London (before 43)
Roman London (43–410)
Saxon London (410–1066)
Norman London (1066–1154)
Medieval London (1154–1485)
Tudor London (1485–1603)
Stuart London (1603–1714)
Georgian London (1714–1837)
Victorian London (1837–1901)
20th-Century London (1901–2000)
```

The taxonomy lives as data in `.claude/skills/london-vault-setup/assets/taxonomy.json`, and the
period notes and the registry table are generated from it by `scripts/build_periods.py`. Edit the
data and regenerate; do not hand-edit period notes or the registry table, because the note names
carry an en dash and the preceded-by/followed-by chain has to stay consistent in both directions.
Changing the taxonomy is a schema change: it needs the user's approval, and any event or claim
already linking a renamed period must be migrated.

`Pre-Roman London` is open at its start. Its `starts: -4000` is a working bound so that timelines
sort, not a claim about when the story begins; Palaeolithic and Mesolithic material belongs to it
regardless.

```yaml
type: period
starts: 1066
ends: 1154
preceded-by: "[[Saxon London (410–1066)]]"
followed-by: "[[Medieval London (1154–1485)]]"
```

Every event and claim gets **both** a `period` link and an ISO date/range. The period link powers "show me everything Norman" queries; the ISO date makes timelines sortable. Neither substitutes for the other.

---

## 5. The state-vs-event rule

**States go in the place note under a period heading; changes of state become Event notes.**

Place notes are structured diachronically:

```markdown
# Bishopsgate (gate)

## Roman
Built as part of [[London Wall]], c. 200 CE...

## Medieval
Rebuilt 1479 by [[Hanseatic League]] merchants... → [[Rebuilding of Bishopsgate (1479)]]

## Demolition
Demolished 1760... → [[Removal of the City gates (1760s)]]
```

"Bishopsgate was rebuilt in 1479" therefore produces an event note:

```yaml
# Rebuilding of Bishopsgate (1479).md
type: event
date: 1479
actor: "[[Hanseatic League]]"
affected: "[[Bishopsgate (gate)]]"
period: "[[Medieval London (1154–1485)]]"
source: "[[Book Title — Chapter 8]]"
page: 214
```

This is what makes queries like "all structural changes to the wall and gates, sorted by date" possible.

---

## 6. People: thin notes, event-driven substance

Person notes contain a short biography summary, aliases, and frontmatter links (`resided-at`, `buried-at`, `member-of`). Do **not** hand-write "activities" sections. A person's footprint across the city is derived: a Dataview query on their note surfaces every event where they appear as `actor`, grouped by place. Extraction therefore routes all "Henry II did X" statements into event notes:

```yaml
# Grant of the 1155 Charter.md
type: event
date: 1155
actor: "[[Henry II]]"
affected: "[[City of London]]"
period: "[[Medieval London (1154–1485)]]"
source: "[[Book Title — Chapter 4]]"
page: 88
```

Offices held (Lord Mayor, Bishop of London) use `held-office` with date qualifiers in the note body.

---

## 7. Dating conventions

- Normalize all dates to ISO in frontmatter: `date: 1189`, `date: 1666-09-02`, or `date-range: 1066/1087`. Keep the original vague phrasing in the note body ("shortly after the Conquest").
- Resolve reign-relative dates ("in the reign of Richard II") to approximate ISO ranges using `_registry/reigns.md` (`date-range: 1377/1399`) and record the original phrasing in the body. Never guess a reign range from memory — use the registry table.
- BCE years are negative: `date: -55` for Caesar's expeditions of 55 BCE, `date-range: -800/43`
  for the Iron Age. Write "55 BCE" in the body — the negative number is for sorting, and nobody
  reads `-55` as a year. Note that 1 BCE is `-1` and there is no year zero, so a span crossing the
  era is one year shorter than subtraction suggests; say so in the body if it matters.
- "12th century" → `date-range: 1100/1199`. Circa dates: `date: 1200` with `date-precision: circa` and the c. phrasing in the body.

---

## 8. Claims as first-class notes

Claims, interpretations, and disputes are notes, not properties. Each claim note carries:

```yaml
type: claim
statement: "Paraphrased assertion in one or two sentences"
asserted-by: "[[Author Name]]"      # or a quoted third party
confidence: stated-fact             # stated-fact | author-interpretation | quoted-third-party | disputed
evidence: "Charter of 1155, cited at p. 91"
source: "[[Book Title — Chapter 4]]"
page: 91
involves: ["[[Henry II]]", "[[City of London]]"]
```

Counterclaims are claim notes linked with `disputes`; corroborations with `supports`. Watch for hedged claims — "some historians argue" must never be flattened into a stated fact. The `confidence` field exists precisely to preserve this.

---

## 9. Relationship vocabulary (controlled — do not extend without user approval)

**Containment / spatial:**
`part-of`, `contains`, `located-in`, `adjacent-to`, `named-after`, `on-site-of`, `succeeded-by`

**Event / agency:**
`actor`, `affected`, `participated-in`, `caused`, `commissioned`, `granted-to`, `destroyed`, `rebuilt`, `resided-at`, `buried-at`, `held-office`

**People / organizations:**
`member-of`, `influenced`

**Sequence:**
`preceded-by`, `followed-by`

**Claims / sources:**
`disputes`, `supports`, `cited-by`

Use these exact kebab-case keys, either as frontmatter properties or inline Dataview fields (`caused:: [[Great Fire of London (1666)]]`). If a relationship in the text doesn't fit the vocabulary, use the nearest term and flag with `#flag/vocab-gap` rather than inventing a new key.

---

## 10. Provenance on everything

Every extracted note and every appended section records: source work, chapter, page/section, and (for claims) confidence. Each chapter processed also gets a `/Sources` note summarizing what was extracted from it. Extraction without provenance is unusable six months later — treat a missing `source` field as an error.

---

## 11. Extraction workflow (per chapter)

Run two passes:

1. **Entity pass.** Extract all entities. Check each against `_registry/entities.md` before creating anything. Output: new entity notes, and new aliases appended to existing entities. Apply the Aldgate disambiguation rule (§3) here.
2. **Relationship/claim pass.** With the resolved entity list in context, extract relationships, events with dates, and claims.

**Merge rules:**
- Never overwrite existing note content. Append new material under a `## <Book> — Chapter N` heading so provenance stays visible.
- After each chapter, update the `_registry` files — this is what keeps chapter 12 consistent with chapter 2.
- Commit after each chapter: registry update + new/modified notes in one commit, message `Extract: <Book> ch.<N>`.

**Chapters over ~30–40k words:** split at section boundaries and pass the running entity registry into each part.

**Periodic reconciliation:** on request, scan the vault for probable duplicate entities, conflicting claims, and `#flag/*` tags awaiting resolution.

---

## 12. Setup order (new vault or new book)

1. Seed `_registry` before any extraction: the 25 wards, the seven gates (Aldgate, Bishopsgate, Cripplegate, Aldersgate, Newgate, Ludgate, Moorgate), the period taxonomy, the monarch/reign table, and major landmarks (Tower of London, St Paul's, London Bridge, Thames, London Wall, Westminster).
2. Process chapter 1 only, then audit hard — especially multi-role name disambiguation, hedged-claim handling, and date resolution. Fix this document and the templates, not the output.
3. Only then batch remaining chapters.
