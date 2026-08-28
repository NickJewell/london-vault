---
name: london-vault-ingest
description: Take OCR'd page text captured on a phone into the London vault — normalise raw .txt files dropped in _inbox/ by an Apple Shortcuts scan, check that book/chapter/page provenance survived the camera, flag OCR damage (mangled years, footnote markers, running heads, hyphen breaks), and hand the cleaned text to extraction. Use when the user mentions scanned or photographed pages, OCR, Shortcuts, the inbox, raw text files waiting to be processed, "I've added some pages", "process the new scans", or asks how to get a book into the vault from photographs. Also use when setting up or debugging the capture pipeline itself.
---

# London Vault — Ingesting scanned pages

The pipeline: photograph a page → Shortcuts runs OCR → a `.txt` lands in `_inbox/` → this skill
cleans it → `london-vault-extract` reads the clean file.

The step that matters is the boring one. A photograph carries no book title, no chapter, no page
number, and §10 treats a missing source as an error — so provenance has to be attached at capture
time, by the person holding the phone, or it is gone. Everything else here is recoverable by
re-reading the page; provenance is not, because six months later nobody remembers which book the
photo of a page about Bishopsgate came from.

## Folders

```
_inbox/          raw OCR text as Shortcuts wrote it — never edit these
_inbox/clean/    normalised, provenance-checked, ready for extraction
_inbox/done/     raw files moved here once their chapter has been extracted
```

Raw files stay in the repo. They are small, and they are the only way to tell later whether a
strange claim came from the book or from the OCR.

`.txt` rather than `.md` is deliberate: Obsidian will not index them as notes, so they stay out of
the graph, out of Dataview results, and out of the vault validator.

## Running it

```bash
python3 .claude/scripts/ingest_text.py --vault . --dry-run
python3 .claude/scripts/ingest_text.py --vault .
```

What it does, and why each step earns its place:

| Step | Reason |
|---|---|
| Reads provenance from a header block, else the filename | Without book + chapter it refuses to produce a clean file at all |
| Ligatures, long s, invisible characters | `ﬁ` and `ſ` break every grep and search you will later run |
| Strips repeated running heads and folios | A running head reads as a sentence and ends up quoted as one |
| Turns standalone page numbers into `[p. N]` markers | Keeps `page:` exact when one file spans several pages |
| Rejoins hyphenated line breaks | "re-\npair" is one word; keeps genuine compounds (`Anglo-Saxon`) hyphenated |
| Rewraps hard line breaks into paragraphs | Extraction reads sentences, not typeset lines |
| Flags mangled years, footnote markers, artifacts | See below — this is the part that protects the vault |

It never modifies a raw file, and it will not overwrite an existing clean file without `--force`.

## The flags are the point

The header of every clean file carries the flags found in it. Read them before extracting.

- **`suspect-year`** — `l598`, `176o`, `16O6`: a letter sitting where a digit belongs. These are
  the dangerous ones, because they still look like years. Dates are the vault's spine, and a
  mangled year in a `date:` field is invisible from then on. **Check every one against the photo
  before it reaches frontmatter.** If you cannot check it, record the phrasing in the body, omit
  the date, and tag `#flag/ambiguous-date`.
- **`footnote-markers`** — `defence.12`: a superscript note number OCR'd as an inline digit. Never
  read one as part of a date or a quantity. Leave it in the text rather than deleting it, so the
  next reader can see what it was.
- **`low-alpha-ratio`**, **`artifacts`**, **`long-tokens`** — the OCR struggled. Read the clean
  file against the photo before extracting anything from it; a bad scan produces confident
  nonsense, which is worse than an obvious gap.

A file with no flags is not a file with no errors. The checks catch known failure modes, not all
of them.

## Then extract

Clean files are ordinary text with a provenance header. Hand one to `london-vault-extract`, which
does the two-pass workflow as usual, using the header's `book`, `chapter` and `pages` for every
`source:` and `page:` field. Where the text carries `[p. N]` markers, cite the page the passage
actually sits on rather than the file's whole range — that precision is the entire reason the
markers exist.

After a chapter's clean files are extracted, move their raw files to `_inbox/done/` so the inbox
shows only what is still outstanding:

```bash
mv _inbox/<book>__ch08__*.txt _inbox/done/
```

Commit the raw and clean files in the same commit as the extraction they fed, so a chapter's
evidence and its output travel together.

## Capture setup

`references/shortcuts-setup.md` has the Shortcuts build, the two provenance formats, the naming
convention, and what to do about multi-page and multi-column captures. Read it when setting the
pipeline up or when files keep arriving without usable provenance.

## When the source is not a book page

The vault's provenance model assumes book, chapter, page. A photograph of a plaque, an information
board, a map, or an archive document has none of those, and there is no schema answer for it yet —
`/Sources` is defined as one note per chapter (§2).

Do not improvise a citation format for these. Ingest them with a `kind:` line in the header, leave
them in `_inbox/`, and put the question to the user: a non-book source needs a decision about what
a `/Sources` note means for it before anything is extracted, or the vault ends up with two
incompatible provenance conventions and no way to tell them apart later.
