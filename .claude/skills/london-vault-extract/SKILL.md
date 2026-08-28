---
name: london-vault-extract
description: Extract entities, events, relationships and claims from a chapter of a London history book into this Obsidian vault, following the two-pass workflow in the vault's semantic schema. Use whenever the user supplies or points at a chapter, section, or passage of a London history text and wants it read into the vault — phrasings like "extract chapter 4", "process this chapter of Ackroyd", "add this text to the vault", "do the next chapter", "run the entity pass", or simply pasting a long passage of London history alongside this vault. Also use when adding notes about London people, places, events or historians' claims that came from a book, since the same schema, provenance and registry rules apply.
---

# London Vault — Chapter Extraction

Implements §11 of `_schema/london-vault-schema.md`, which is canonical for the data model. **Read
the schema and the registries before extracting anything** — not as ceremony, but because the
whole value of this vault is that chapter 12 uses the same names as chapter 2, and the registries
are the only record of what those names are.

```bash
cat _schema/london-vault-schema.md          # the rulebook
cat _registry/entities.md                   # what already exists
cat _registry/places.md                     # multi-role names and hierarchy
cat _registry/reigns.md                     # for any reign-relative date
```

If `_registry/` is missing, stop and run `london-vault-setup` first. Extracting into an unseeded
vault produces notes that nothing can be reconciled against.

## Before you start: what you are being asked for

Establish these, and ask if the text does not tell you — a chapter extracted under the wrong
provenance is worse than one not extracted, because it looks finished:

- **Book title and author** — exactly as it should appear in every `source:` link from now on.
- **Chapter number and title.**
- **Page numbers**, or at minimum the page range. §10 treats a missing `source` as an error, and
  page numbers are what make a claim checkable a year later. If the text genuinely has no page
  numbers (an ebook, a plain-text file), say so once, use section or paragraph references, and
  record the substitution in the `/Sources` note rather than leaving `page:` blank.

## Pass 1 — entities

Read the whole chapter first. Then list every entity it mentions: people, places, organizations,
concepts. Do **not** create anything yet.

For each candidate, in this order:

1. **Check `_registry/entities.md`.** Match against canonical names *and* aliases. A name already
   in the vault is not a new entity, however differently the text spells it.
2. **Check whether it is a new alias** of something already there. "Dick Whittington" against an
   existing `Richard Whittington` is an alias to append, not a note to create. Appending aliases is
   the highest-value output of this pass — it is what stops the vault fragmenting.
3. **Apply the multi-role rule** (§3) if the name appears in the multi-role table in
   `_registry/places.md`, or if it plausibly should. See `references/disambiguation.md` for how to
   decide a role from context; this is the single most error-prone step in the workflow.
4. **Only then create a note**, from the matching template in `_templates/`, in the folder its
   `type` dictates (§2).

Every new note needs `type`, `aliases`, and `first-seen` at minimum. `first-seen` is the source
and chapter where this entity was first encountered, and it never changes on later chapters — it
records when the vault first heard of the thing, which is different from where the best material
about it lives.

**What is not an entity.** Passing mentions with no content attached ("as in Paris or Antwerp")
do not need notes. A note that exists only because a word appeared once adds a node to the graph
and nothing to the vault. Create a note when the text says something *about* the thing.

**Unnamed actors.** "The Bishop of London ordered..." with no name given is an office, not a
person. Route it to an event with the office or organization as `actor` and tag
`#flag/unnamed-actor`; inventing a person note from an office is how a vault acquires people who
never existed.

At the end of pass 1 you should have: an explicit list of resolved entity names (canonical spelling
for every mention in the chapter), the new notes, and the aliases to append. Carry that list into
pass 2 — resolving relationships against unresolved names is what produces duplicate-riddled
vaults.

## Pass 2 — relationships, events, claims

With the resolved entity list in hand, work through the chapter again.

### Events (§5)

The governing distinction is **state vs. event**: a state is how something *was* and belongs in a
place note under a period heading; a change of state is an event note.

- "The gate stood two storeys high" → state → `Places/Aldgate (gate).md`, under `## Medieval`.
- "The gate was rebuilt in 1215" → event → `Events/Rebuilding of Aldgate (1215).md`, linked from
  that same period section with an arrow.

Event notes need `date:` **or** `date-range:` (never both), `period:`, `source:`, `page:`, and
whichever of `actor:`/`affected:` the text supports. Both the ISO date and the period link are
required and neither substitutes for the other (§4): the date sorts timelines, the link answers
"show me everything Norman".

Name events so they are self-identifying in a link list: `<What happened> (<year>)` —
`Rebuilding of Bishopsgate (1479)`, `Grant of the 1155 Charter`. A link to
`[[Rebuilding of Bishopsgate (1479)]]` tells a reader what they are about to open; a link to
`[[Bishopsgate rebuild]]` does not.

**People generate events, not biography** (§6). Every "Henry II did X" becomes an event with
`actor: "[[Henry II]]"`. Person notes stay thin — a short biographical summary and frontmatter
links, no hand-written activities section. The footprint is derived by query, and a hand-written
narrative would silently drift out of step with the events the next chapter adds.

### Dates (§7)

- Plain year → `date: 1189`. Full date → `date: 1666-09-02`. Span → `date-range: 1066/1087`.
- Reign-relative → look it up in `_registry/reigns.md`. **Never from memory.** Regnal dates are
  recalled correctly often enough to feel safe and wrongly often enough to poison a timeline.
- Century → `date-range: 1100/1199`. Circa → `date: 1200` plus `date-precision: circa`.
- **Always keep the original phrasing in the note body** — "shortly after the Conquest", "in the
  reign of Richard II". The ISO value is an interpretation, and a later reader needs to see what it
  was interpreted from. This is not optional colour; it is the audit trail.

Genuinely undatable? Record the phrasing, omit the date keys rather than guessing, and tag
`#flag/ambiguous-date`.

### Claims (§8)

A claim note is warranted when the text asserts something *interpretive* — a cause, a
significance, a disputed origin, an attribution — rather than reporting a plain fact. "The Fire
began in Pudding Lane" is an event. "The Fire's real cause was the City's refusal to enforce its
own building regulations" is a claim.

The `confidence` field is the reason claims are notes at all:

| Value | The text reads like |
|---|---|
| `stated-fact` | the author asserts it flatly as established |
| `author-interpretation` | the author's own reading, argued rather than reported |
| `quoted-third-party` | attributed to someone else — "Stow says", "some historians argue" |
| `disputed` | the author records disagreement, or another note contradicts this one |

**Hedges must survive extraction.** "Some historians argue that..." recorded as `stated-fact` is
the one error the vault cannot detect later: the hedge is gone, and nothing about the note looks
wrong. When a hedge is present, quote the hedging sentence in the body so the reading can be
checked. When two claims conflict, link them with `disputes` and set both to `disputed` — a
contradiction between two sources is a finding, not a problem to resolve during extraction.

### Relationships (§9)

Use the controlled vocabulary exactly, in kebab-case, as frontmatter properties or inline
Dataview fields (`caused:: [[Great Fire of London (1666)]]`). The full list is in schema §9.

If a relationship in the text does not fit, use the nearest term and tag `#flag/vocab-gap`. Do not
invent a key. An invented key is invisible to every query built on the vocabulary, so the
relationship is recorded but unfindable — worse than the approximation plus a flag, which is both
findable and honest about being approximate.

## Writing to the vault

**Never overwrite existing content** (§11). New material on an existing note is appended under a
heading naming its source:

```markdown
## Ackroyd, London: The Biography — Chapter 4
```

This is what keeps provenance visible at the paragraph level rather than only in frontmatter. When
a later chapter contradicts an earlier one, both stay, each under its own heading, and the
disagreement becomes visible instead of being resolved by whoever wrote last.

On existing notes, append to `aliases` rather than replacing, and leave `first-seen` alone.

## Finish the chapter

1. **Write the `/Sources` note** — `Sources/<Book> — Chapter N.md` from `_templates/Source.md`,
   summarising what was extracted, which flags were raised, and the judgement calls made
   (which role a multi-role name resolved to and why; how a vague date was resolved; any close
   call on a claim's confidence). This section is what makes an extraction auditable later.
2. **Update the registries** — `entities.md` always, plus whichever type registries gained names
   or aliases. New multi-role names go in the `places.md` table. §11 puts this in the same breath
   as extraction for a reason: it is the mechanism that keeps chapter 12 consistent with chapter 2,
   and it is worthless if it lags.
3. **Validate**:
   ```bash
   python3 .claude/scripts/validate_vault.py --vault .
   ```
   It checks provenance, the type and confidence enums, the relationship vocabulary, date formats,
   period/date pairing, and unresolved links. Fix what it reports before committing — these are
   the errors that are cheap now and expensive once six more chapters sit on top of them.
4. **Commit** — registry updates and new/modified notes together, message `Extract: <Book> ch.<N>`
   exactly. One chapter per commit means a bad extraction can be reverted as a unit.

## Long chapters

Over roughly 30–40k words, split at section boundaries rather than arbitrary word counts, and pass
the running entity list into each part. The list is the state that must survive the split — if
part 2 starts without knowing what part 1 resolved, it will re-resolve the same names differently,
which is the exact failure the registry exists to prevent.

## References

- `references/disambiguation.md` — deciding which role a multi-role name takes, with worked cases.
  Read this during pass 1 the first few times; it is where extractions most often go wrong.
- `references/worked-example.md` — a short passage extracted end to end: entity list, notes,
  events, a hedged claim, registry diff and commit. Read it if the shape of the output is unclear.
