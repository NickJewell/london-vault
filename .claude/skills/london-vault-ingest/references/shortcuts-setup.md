# Capturing pages with Apple Shortcuts

The goal is that a page arrives in `_inbox/` as text with its book, chapter and page attached. The
OCR is the easy half; attaching provenance is the half that has to be designed, because the phone
cannot infer it and nobody will reconstruct it later.

## Where the files land

Shortcuts writes into the Obsidian vault folder on iCloud Drive, at `_inbox/`. Obsidian sees the
file, obsidian-git commits it on its next backup, and it reaches the repo where extraction happens.

Two things to know:

- **obsidian-git on mobile does not always back up on its own.** After a capture session, open
  Obsidian and run the backup command, or the pages sit on the phone. If a scan seems to have
  vanished, this is almost always why.
- **Vault files sync through iCloud, so give it a moment.** A file written by Shortcuts may take a
  few seconds to appear on the desktop.

## The Shortcut

Six actions. Build it once.

1. **Select Photos** (or take the photos first and share them to the Shortcut) — allow multiple.
2. **Extract Text from Image** — this is Apple's on-device OCR, the Live Text engine.
3. **Ask for Input** → Text → "Book?" — or, better, **Choose from Menu** listing the two or three
   books you are actually working through, so a typo cannot invent a new book name. Consistency in
   this string matters: it becomes the `source:` link on every note the page produces, and two
   spellings of one book title split the vault's provenance in half.
4. **Ask for Input** → Number → "Chapter?"
5. **Ask for Input** → Text → "Page(s)?" — accepts `214` or `214-215`.
6. **Text** action, combining the answers with the OCR output:

   ```
   book: [Book]
   author: [Author]
   chapter: [Chapter]
   pages: [Pages]

   [Extracted Text]
   ```

7. **Save File** → destination `Obsidian/<vault>/_inbox/`, filename
   `[Book-slug]__ch[Chapter]__p[Pages].txt`, with *Overwrite If File Exists* **off** so a repeated
   run cannot silently replace a capture.

The blank line after the header matters — it is what separates provenance from text.

## The two provenance formats

The ingest script accepts either. It prefers the header, because a header survives a rename and a
filename does not.

**Header block** (recommended), the first lines of the file:

```
book: Ackroyd, London: The Biography
author: Peter Ackroyd
chapter: 8
chapter-title: The Wall and the Gates
pages: 214-215
```

`book` and `chapter` are required; the rest are optional. A `---` fenced block works too, if that
is easier to produce.

**Filename**, as a fallback:

```
ackroyd-london__ch08__p214-215.txt
```

The parser looks for `ch<N>` and `p<N>` or `p<N>-<N>` anywhere in the name, and treats whatever
precedes them as the book. A filename-derived book title is marked in the clean file's header as
needing verification, since `ackroyd-london` is a slug, not a title.

Files with neither are refused, with a message saying what to add. That refusal is deliberate:
ingesting them anyway would produce clean text that looks ready and cannot legally be cited.

## Multi-page captures

One photo per page keeps everything simple, and page markers then come straight from the filename.

If a capture holds several pages, leave the printed page numbers in the OCR output — the script
turns standalone numeric lines into `[p. N]` markers, so extraction can cite the exact page a
passage sits on rather than the file's whole range. Do not manually delete page numbers from raw
files thinking you are tidying them; you are removing the only page evidence in the text.

## Things that will bite

- **Two-column pages.** Apple's OCR reads across columns on some layouts, interleaving two columns
  into nonsense that is grammatical enough to look real. Check the first capture from any new book
  before scanning fifty pages. If it interleaves, photograph one column at a time.
- **Footnotes.** They OCR into the body as if they were text, and their superscript markers become
  inline digits. The script flags the markers; the footnote text itself you have to spot by eye.
  Footnote content is often *more* citable than the body — but it is a different claim, from a
  different part of the page, and it needs its own page reference.
- **Curl and shadow.** Text near the gutter distorts, and OCR guesses. A page photographed flat is
  worth two photographed at an angle.
- **Running heads.** Stripped automatically when they repeat, which needs at least two pages in one
  file. In a single-page capture the running head stays; delete it from the clean file, not the raw.
- **Long s (`ſ`).** Facsimiles of pre-1800 printing OCR the long s as `f` about as often as `s`.
  The script maps the real `ſ` character to `s`, but it cannot rescue an `f` that OCR was confident
  about. Read any facsimile page carefully — "ſuburbs" as "fuburbs" is the visible kind, and
  "beſt" as "beft" is the kind that gets extracted.

## Sanity check before a long session

Capture one page, run the ingest, and read the clean file against the photo end to end. Confirm the
paragraphs are whole, the years are right, and the header carries the book you meant. Ten minutes
here is worth more than any amount of cleanup later, because errors that survive into extraction
get copied into frontmatter, and frontmatter is what everything else trusts.
