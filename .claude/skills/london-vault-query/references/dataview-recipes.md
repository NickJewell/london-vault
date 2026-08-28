# Dataview recipes for the London vault

Query blocks to paste into notes, with the reasoning behind each. All assume the schema's
frontmatter conventions, so they are also a check on those conventions: a query that cannot be
written usually means the data model was not followed.

## On entity notes

**Events where this person or organization acted** — the derived "activities" section that §6
forbids writing by hand:

````
```dataview
TABLE date AS "Date", affected AS "Affected", period AS "Period", source AS "Source"
FROM "Events"
WHERE contains(actor, this.file.link) OR contains(participated-in, this.file.link)
SORT date ASC
```
````

**Footprint grouped by place** — the "where in the city did this person leave a mark" view:

````
```dataview
TABLE rows.file.link AS "Events", rows.date AS "Dates"
FROM "Events"
WHERE contains(actor, this.file.link)
GROUP BY affected AS "Place"
```
````

**Events at this place**, including events that merely happened there:

````
```dataview
TABLE date AS "Date", actor AS "Actor", source AS "Source"
FROM "Events"
WHERE contains(affected, this.file.link) OR contains(located-in, this.file.link)
SORT date ASC
```
````

**What contains this place / what this place contains** — the hierarchy, read both ways:

````
```dataview
LIST FROM "Places" WHERE contains(part-of, this.file.link) OR contains(located-in, this.file.link)
```
````

**Members of an organization**, by backlink rather than a hand-kept list that goes stale:

````
```dataview
LIST FROM "People" WHERE contains(member-of, this.file.link)
```
````

## Timelines

**Everything in a period**, on the period note:

````
```dataview
TABLE date, actor, affected, source FROM "Events"
WHERE contains(period, this.file.link) SORT date ASC
```
````

**A century, by date rather than by period link** — useful precisely because it cross-checks the
period assignments: an event that appears here but not on its period note has a mislinked period.

````
```dataview
TABLE date, actor, affected FROM "Events"
WHERE date >= date("1600-01-01") AND date <= date("1699-12-31") SORT date ASC
```
````

Note that `date-range` events will not match a date comparison — they are a different field. To
catch both, query them separately and merge by eye; a single query that handles both is possible
but fragile enough that it tends to hide the cases it drops.

**Spanning several periods** — the 20th century is divided into five periods (Edwardian & WWI,
Interwar, WWII & Blitz, Postwar, Modern & Contemporary), so "the whole 20th century" is an OR
across them rather than one link:

````
```dataview
TABLE date, actor, affected, period FROM "Events"
WHERE any(map(period, (p) => contains(meta(p).path, "London (19")))
SORT date ASC
```
````

That relies on a naming coincidence and will not age well. Prefer the date form, which says what
it means and is immune to the taxonomy being resubdivided again:

````
```dataview
TABLE date, actor, affected, period FROM "Events"
WHERE date >= date("1901-01-01") AND date < date("2001-01-01")
SORT date ASC
```
````

The general point: **query by period link when you mean the era, by date when you mean the span.**
"Everything Interwar" is a period question — the link carries the judgement that an event belongs
to that era, which a date range cannot reconstruct. "Everything between 1901 and 2000" is a date
question, and going through period links would make it hostage to how the taxonomy is cut.

**Structural changes to the wall and gates** — the §5 query the state-vs-event rule exists for:

````
```dataview
TABLE date AS "Date", actor AS "Actor", affected AS "Structure", source AS "Source"
FROM "Events"
WHERE any(map(affected, (a) => contains(string(a), "gate") OR contains(string(a), "Wall")))
SORT date ASC
```
````

A cleaner version once enough structures exist: link each gate `part-of: "[[London Wall]]"` and
query the places first. Matching on the substring "gate" is a convenience that will eventually
catch something like `Billingsgate Ward` — worth remembering when a result looks odd.

## Claims and provenance

**Everything hedged or disputed** — the audit §8 is built for. Run this after every book:

````
```dataview
TABLE confidence, statement, asserted-by, source FROM "Claims"
WHERE confidence != "stated-fact" SORT confidence ASC
```
````

**Claims involving this entity**, on any entity note:

````
```dataview
TABLE confidence, statement, source FROM "Claims"
WHERE contains(involves, this.file.link) SORT confidence ASC
```
````

**Disputes**, as pairs:

````
```dataview
TABLE statement, asserted-by, disputes FROM "Claims"
WHERE disputes SORT file.name ASC
```
````

**What one chapter contributed** — for auditing an extraction:

````
```dataview
TABLE type, file.folder AS "Folder" FROM ""
WHERE contains(string(source), "Chapter 8") OR contains(string(first-seen), "Chapter 8")
SORT file.folder ASC
```
````

**Notes missing provenance** — should always return empty; §10 treats a missing source as an
error, and this is the standing check on that:

````
```dataview
LIST FROM "Events" OR "Claims" WHERE !source
```
````

**Everything from one author across books** — why `asserted-by` and `source` are separate fields:

````
```dataview
TABLE statement, confidence, source FROM "Claims"
WHERE contains(asserted-by, [[John Stow]])
```
````

## Flags

**Everything awaiting resolution**, for a reconciliation pass:

````
```dataview
TABLE file.tags AS "Flags", source FROM #flag
SORT file.folder ASC
```
````

## Gotchas

- **En dash.** Period names contain `–` (U+2013), not `-`. Copy names from `_registry/periods.md`.
- **`contains()` for link fields.** A field may hold one link or a list; `contains()` handles both,
  `=` handles only the first case and fails silently on the second.
- **`date` vs `date-range`.** Different fields with different types. A query that sorts on `date`
  drops every ranged event — usually the older material, which is exactly the material a
  long-timeline query is about.
- **Quote the links in YAML.** `actor: "[[Henry II]]"`. Unquoted, YAML reads `[[...]]` as a nested
  list and the link is lost.
- **Inline fields need `::`** and must start the line to be reliably picked up.
