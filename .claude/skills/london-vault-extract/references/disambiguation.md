# Deciding which role a multi-role name takes

The Aldgate rule (schema §3) says one name can denote a gate, a ward, and a district, and that
these are never merged. The hard part is not the rule — it is deciding, sentence by sentence,
which one a text means. This file is the decision procedure and the cases that recur.

Get this wrong in one direction and the vault fragments; wrong in the other and a gate's
architecture ends up mixed into a ward's governance in a single note that no query can separate.

## The procedure

1. **Look at the verb and the predicate, not the name.** The name is identical across roles; what
   is said about it is not. Gates are built, rebuilt, closed, guarded, demolished. Wards elect,
   are assessed, return aldermen, have populations. Districts are lived in, are poor or rich, have
   character. Streets run, are widened, are paved.
2. **Look at the preposition.** "at Aldgate" and "by Aldgate" usually mean the structure; "in
   Aldgate" usually means the area or ward; "along Aldgate" means the street.
3. **Look at what it is being compared to.** A list of wards means the ward. A list of gates means
   the gate. Authors are consistent within a passage far more often than within a chapter.
4. **Check the date against the role's existence.** Moorgate is not a gate before 1415. Farringdon
   Within and Without do not exist before 1394. Bridge Ward Without is not a ward before 1550.
   A date that predates a role rules that role out — the most reliable check available.
5. **Still genuinely ambiguous?** Link the **district/area** note and tag `#flag/ambiguous-place`.
   The area note is the right default because it is the loosest claim: it says the text was about
   that part of London, which is true under every reading, rather than asserting a specific
   structure or jurisdiction the text may not have meant.

Do not resolve ambiguity by creating a new undifferentiated note. That is the one move that makes
the problem permanent — a note named `Aldgate` with no role becomes a magnet for every future
mention, and unpicking it later means re-reading every chapter that touched it.

## Worked cases

| Passage | Role | Why |
|---|---|---|
| "the Jewish community settled near Aldgate" | district — `Aldgate (area)` | "near" plus a residential subject; it is a neighbourhood claim |
| "Chaucer lived in rooms above Aldgate" | structure — `Aldgate (gate)` | rooms above it: only a building has an above |
| "Aldgate returned its alderman in 1381" | ward — `Aldgate Ward` | returning an alderman is a ward's function |
| "the wall ran from Aldgate to Bishopsgate" | structure ×2 | wall stretches are measured gate to gate |
| "Aldgate was among the poorest quarters" | district | "quarters" is the giveaway; poverty is described of areas |
| "he was imprisoned in Newgate" | `Newgate Prison` | imprisonment names the prison, not the gate — even before the prison was formally distinct |
| "the road west through Newgate" | `Newgate (gate)` | passage through is what a gate is for |
| "Newgate was widened in 1867" | `Newgate Street` | a 19th-century widening postdates the gate's 1767 demolition — the date rules the gate out |
| "the Abbey" in a Westminster passage | `Westminster Abbey` | — |
| "the King removed to Westminster" | `Palace of Westminster` | a king removes to a residence, not a church or a city |
| "Westminster's population doubled" | `City of Westminster` | populations belong to settlements |
| "the stews of Southwark" | `Southwark` (district) | unless the text is specifically about the Bishop of Winchester's jurisdiction, in which case `Liberty of the Clink` |
| "Bridge Without sent no member" | `Bridge Ward Without` | a ward's representation |

## When the text conflates roles itself

Historians write "Aldgate grew rich" meaning the area, then two sentences later "Aldgate was
rebuilt" meaning the gate, without marking the switch. Follow the meaning per sentence, not per
paragraph. Each statement gets linked to the role it is actually about — an extraction is allowed
to be more precise than its source, and this is the main place where that precision is added.

What an extraction is **not** allowed to do is be more precise than the evidence. If the author
genuinely does not distinguish — some 19th-century topographers never do — flag it rather than
picking a role to look decisive. The flag costs a minute of the user's review; a wrong confident
resolution costs a chapter of re-reading to find.

## New multi-role names

When a chapter turns up a name with roles not yet in the `places.md` table — Queenhithe as dock
and ward, Billingsgate as ward and market, Blackfriars as priory and district and bridge — add a
row to the table in the same commit. That table is how the *next* chapter avoids re-deriving the
same distinction, possibly differently. Adding a row is a registry update, not a schema change:
the schema fixes the *rule*, and the table is just the accumulating list of names it applies to.

## Name drift vs. genuine succession

Related, and easy to confuse:

- **Renamed, same thing** → one note, old name into `aliases`. A street renamed in 1885 is the
  same street.
- **Different thing, same site** → two notes, linked `on-site-of` and `succeeded-by`. The Roman
  basilica and medieval Leadenhall; Old St Paul's and Wren's cathedral.

The test that usually settles it: did the thing ever stop existing? If there was a moment when
the old thing was gone and the new one not yet there, they are two notes. Continuous existence
under a new name is one note. When a source is unclear on whether a rebuilding was continuous,
prefer two notes with `succeeded-by` — splitting later requires re-reading, but two notes can be
merged from the vault alone.
