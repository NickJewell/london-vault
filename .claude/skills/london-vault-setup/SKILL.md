---
name: london-vault-setup
description: Seed or repair the London history Obsidian vault's structure — the folder tree, the six _registry files (places with hierarchy, people, organizations, periods, the monarch/reign lookup table, the master entity index), the period notes, and the per-type note templates. Use this whenever starting a new London vault, beginning a new book in an existing vault, or when extraction reports that a registry or template is missing; and use it before any extraction run, since the schema requires the registries to exist first. Also use when asked to add the wards, the City gates, the period taxonomy, or the reign table to the vault.
---

# London Vault — Setup

This skill implements §12 (setup order) of `_schema/london-vault-schema.md`. Read that document
first if it is present; it is canonical for the data model, and this skill only covers procedure.

Seeding exists because three things must be right *before* any text is read: the period taxonomy,
the reign table, and the list of multi-role place names. Each of those is something a model will
otherwise reconstruct from memory mid-extraction, slightly differently each time — and the damage
is invisible, because a wrong reign range in frontmatter looks exactly like a right one.

## Running the seed

```bash
python3 .claude/skills/london-vault-setup/scripts/seed_vault.py --vault . --dry-run   # inspect
python3 .claude/skills/london-vault-setup/scripts/seed_vault.py --vault .             # apply
```

It creates the ten folders, copies the six registries into `_registry/`, the eight templates into
`_templates/`, and the period notes into `Periods/`. **It never overwrites.** Anything
already present is reported and left alone, because a registry that has been through six chapters
of extraction holds accumulated aliases that exist nowhere else.

Then confirm what landed:

```bash
ls _registry _templates Periods
```

## Changing the period taxonomy

The taxonomy is data: `assets/taxonomy.json`. The period notes in `Periods/`, the table in
`_registry/periods.md`, and the period rows in `_registry/entities.md` are all generated from it.

```bash
python3 .claude/skills/london-vault-setup/scripts/build_periods.py --vault . --dry-run
python3 .claude/skills/london-vault-setup/scripts/build_periods.py --vault .
```

Regenerating period notes is safe in a way that regenerating any other note would not be: their
bodies are a blurb and Dataview blocks, with no extracted content to lose. Everything else in the
vault stays append-only (§11).

Adding a period is a schema change and needs the user's approval (§4). Two things to settle before
touching the data:

- **Renames migrate.** Every event and claim links a period by exact name, so renaming
  `Postwar London (1945–1980)` orphans every link to it. The generator reports leftover notes
  as STALE but will not rewrite links — grep for the old name and fix them in the same commit, or
  do the rename before any extraction has happened.
- **Boundaries move events.** Narrowing a period reassigns events that sat in the part now covered
  by a neighbour. Nothing detects this: the old link still resolves, it is just wrong. Check
  affected events by date range after any boundary change.

The generated regions are delimited by `<!-- BEGIN generated: taxonomy -->` markers. Prose outside
them is preserved; edits inside them are overwritten on the next run.

## What is deliberately *not* seeded

The 25 wards, the 7 gates, the landmarks and the monarchs have their canonical names reserved in
the registries, but **no notes**. Their notes get created the first time a text actually says
something about them, so that `first-seen` records a real source (§2).

This is worth defending when it feels like a shortcut is available. A vault pre-populated with 25
empty ward stubs looks further along but is strictly worse: every stub is unfalsifiable (nothing
in it came from anywhere), the graph fills with nodes no chapter supports, and a genuine gap —
"we have read eight chapters and none of them mentions Bassishaw" — becomes undetectable. Reserved
names give you the consistency benefit of pre-seeding (everyone links to `Aldgate Ward`, spelled
that way) without the fiction.

## Auditing after chapter 1

§12 is explicit that chapter 1 is processed **alone** and then audited hard, before any batching.
The audit is not a formality — it is the only cheap moment to find a systematic error, because
every later chapter compounds whatever chapter 1 established.

Check these four, in this order, since each can mask the next:

1. **Multi-role names.** Did every mention of Aldgate/Bishopsgate/Newgate/Westminster/Southwark
   resolve to a *specific* role note, or did some collapse into one general note? Look for a place
   note whose body mixes a gate's architecture with a ward's governance — that is a merge that
   should have been a split.
2. **Hedged claims.** Re-read the chapter's hedges ("some historians argue", "it may be that",
   "tradition holds") against the `confidence` values. Every hedge flattened to `stated-fact` is a
   silent corruption; this is the failure mode that is unrecoverable later, because the vault no
   longer records that a hedge was there.
3. **Dates.** Every reign-relative date traceable to `_registry/reigns.md` rather than to memory?
   Every event carrying **both** `period:` and an ISO date? Original phrasing preserved in bodies?
4. **State vs. event.** Did changes of state ("rebuilt in 1479") become event notes, or get
   written as prose inside place notes? Prose-only changes are invisible to every timeline query
   the schema is built to support.

When the audit finds a problem, §12 is emphatic about the fix: **change the schema document and
the templates, not just the output.** Fixing only chapter 1's notes leaves the same mistake
waiting for chapter 2. If the schema itself needs changing, propose it to the user — never
improvise a schema change mid-extraction.

## Starting a new book in an existing vault

Do not re-seed. Instead:

1. Read the existing `_registry/entities.md` — the new book shares the vault's entity space, and
   the whole point of the registry is that book two's "Whittington" resolves to book one's note.
2. Create the `/Sources` notes as chapters are processed, named `<Book Title> — Chapter N`, which
   keeps provenance unambiguous when two books cover the same ground.
3. Expect disagreements between books. Two sources contradicting each other is not a problem to
   resolve during extraction — it is exactly what claim notes with `disputes` are for (§8).

## Obsidian plugins

The schema's derived views (a person's footprint, "everything Norman", timelines) are Dataview
queries, and the templates ship with them. Dataview is installed in this vault, so they render.

If a seed lands in a vault without it, the queries are inert code fences and everything else still
works — notes, links, frontmatter and the graph are plain Markdown. Do not try to install plugins
by editing `.obsidian/community-plugins.json`: the plugin's code is not there, and listing it
without its files gives Obsidian a broken entry rather than a working plugin. Tell the user to
install it from Obsidian's community plugins instead.
