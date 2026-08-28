# Inbox

Landing folder for pages captured on a phone: photograph → Shortcuts OCR → a `.txt` here.

| Folder | Holds |
|---|---|
| `_inbox/` | raw OCR text exactly as Shortcuts wrote it — **do not edit these** |
| `_inbox/clean/` | normalised, provenance-checked text, ready for extraction |
| `_inbox/done/` | raw files whose chapter has been extracted |

```bash
python3 .claude/scripts/ingest_text.py --vault .
```

Every file needs its book and chapter, either as a header block on the first lines —

```
book: Ackroyd, London: The Biography
chapter: 8
pages: 214-215
```

— or in the filename, as `ackroyd-london__ch08__p214-215.txt`. Files with neither are refused
rather than ingested, because a photograph carries no citation and nothing downstream can invent
one.

Raw files are kept, not deleted. They are the only way to tell later whether a surprising claim
came from the book or from the OCR.

Setup and troubleshooting: `.claude/skills/london-vault-ingest/references/shortcuts-setup.md`.
