#!/usr/bin/env python3
"""Normalise OCR'd text dropped into _inbox/ and make it ready for extraction.

The pipeline is: photograph a page -> Shortcuts runs OCR -> a .txt lands in _inbox/ -> this
script cleans it into _inbox/clean/ -> london-vault-extract reads the clean file.

Two things make OCR'd book pages different from ordinary text, and both are why this exists
rather than extraction just reading the raw file:

1. **Provenance has to survive the camera.** §10 treats a missing source as an error, and a photo
   carries no book, chapter or page. That metadata comes from a header block Shortcuts writes, or
   from the filename. If neither is present this script refuses to produce a clean file, because
   text with no citation is text that cannot be used.

2. **OCR fails in ways that look like content.** A hyphen at a line break becomes a word split in
   two; a running head becomes a sentence; "1666" becomes "l666" and stays a plausible-looking
   token. Dates are the vault's spine, so mangled years are flagged loudly rather than quietly
   carried into frontmatter.

Nothing here is destructive: raw files are never modified, and every substantive change is
reported and counted in the clean file's header so it can be checked against the photo.

Usage:
    python3 ingest_text.py [--vault PATH] [--dry-run] [--force]
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

INBOX = "_inbox"

LIGATURES = {
    "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl",
    "ﬅ": "st", "ﬆ": "st", "ſ": "s",  # long s, common in older reprints
}
INVISIBLE = dict.fromkeys(map(ord, "​‌‍﻿­"), None)

# A year that has picked up a letter where a digit belongs. These read as plausible tokens, which
# is exactly what makes them dangerous: nothing downstream will notice.
# Letters that OCR substitutes for digits, by position. A trailing 's' is deliberately absent:
# "the 1760s" is a legitimate decade, and flagging it every time would train the reader to skim
# these warnings — which is how the one real mangled year gets waved through.
_SUB = "lIiOoSB"
RE_BAD_YEAR = re.compile(
    rf"\b(?:[{_SUB}]\d{{3}}|\d[{_SUB}]\d{{2}}|\d{{2}}[{_SUB}]\d|\d{{3}}[lIiOoB])\b"
)
RE_YEAR = re.compile(r"\b(1[0-9]{3}|20[0-9]{2})\b")
RE_PAGE_NUM = re.compile(r"^\s*[\[\(]?\s*(\d{1,4})\s*[\]\)]?\s*$")
RE_HYPHEN_BREAK = re.compile(r"(\w+)-\n(\w+)")
RE_FOOTNOTE = re.compile(r"(?<=[a-z])\.\s?\d{1,2}\b|(?<=[a-z]{3})\d{1,2}(?=\s+[A-Z])")
RE_ARTIFACT = re.compile(r"[|~^`\\<>{}]{2,}|[«»]{2,}")
RE_HEADER_KEY = re.compile(r"^([A-Za-z][A-Za-z-]*)\s*:\s*(.*)$")

PROV_KEYS = ("book", "author", "chapter", "chapter-title", "pages", "kind", "note")


def parse_header(text: str) -> tuple[dict, str]:
    """Pull a provenance header off the top of the file, if there is one.

    Accepts a --- fenced block or bare `key: value` lines at the very top, because Shortcuts can
    produce either without fuss and arguing about which is tidier helps nobody.
    """
    lines = text.splitlines()
    meta: dict[str, str] = {}
    i = 0
    fenced = bool(lines) and lines[0].strip() in {"---", "—"}
    if fenced:
        i = 1
    while i < len(lines):
        line = lines[i]
        if fenced and line.strip() in {"---", "—"}:
            i += 1
            break
        m = RE_HEADER_KEY.match(line.strip())
        if not m:
            if fenced:
                i += 1
                continue
            break
        key, value = m.group(1).lower(), m.group(2).strip()
        if key not in PROV_KEYS and not fenced:
            break
        meta[key] = value
        i += 1
    return meta, "\n".join(lines[i:])


def parse_filename(stem: str) -> dict:
    """Recover provenance from a filename like `ackroyd-london__ch08__p214-215`."""
    meta: dict[str, str] = {}
    m = re.search(r"ch(?:apter)?[\s_-]*(\d{1,3})", stem, re.I)
    if m:
        meta["chapter"] = m.group(1).lstrip("0") or "0"
    m = re.search(r"\bpp?[\s_.-]*(\d{1,4})(?:\s*[-–]\s*(\d{1,4}))?", stem, re.I)
    if m:
        meta["pages"] = f"{m.group(1)}-{m.group(2)}" if m.group(2) else m.group(1)
    head = re.split(r"__|\bch(?:apter)?[\s_-]*\d", stem, maxsplit=1, flags=re.I)[0]
    head = head.strip(" _-")
    if head:
        meta["book"] = head.replace("-", " ").replace("_", " ").strip()
        meta["book-from-filename"] = "yes"
    return meta


def normalise_chars(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    for src, dst in LIGATURES.items():
        text = text.replace(src, dst)
    text = text.translate(INVISIBLE)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[   \t]", " ", text)
    text = re.sub(r" {2,}", " ", text)
    return text


def strip_running_heads(lines: list[str], meta: dict) -> tuple[list[str], list[str]]:
    """Drop lines that repeat across pages — book titles, chapter titles, folios.

    Only repeated lines qualify, and only short ones that do not read as prose, because a
    repeated sentence in the text itself would be real content. Everything removed is reported.
    """
    counts = Counter(l.strip() for l in lines if l.strip())
    title_words = set()
    for key in ("book", "chapter-title"):
        if meta.get(key):
            title_words |= {w.lower() for w in re.findall(r"\w+", meta[key]) if len(w) > 3}

    removed: list[str] = []
    heads = set()
    for line, count in counts.items():
        if count < 2 or len(line) > 60:
            continue
        words = {w.lower() for w in re.findall(r"\w+", line)}
        looks_like_title = bool(words & title_words)
        shouty = line.isupper() and len(line) > 3
        unpunctuated = not line.rstrip().endswith((".", "!", "?", ":", ";", ","))
        if looks_like_title or shouty or (unpunctuated and count >= 3):
            heads.add(line)
    if heads:
        kept = []
        for l in lines:
            if l.strip() in heads:
                removed.append(l.strip())
            else:
                kept.append(l)
        lines = kept
    return lines, sorted(set(removed))


def mark_pages(lines: list[str], meta: dict) -> tuple[list[str], list[int]]:
    """Turn standalone page numbers into [p. N] markers so citations stay exact."""
    out, found = [], []
    for line in lines:
        m = RE_PAGE_NUM.match(line)
        if m and line.strip():
            page = int(m.group(1))
            if 1 <= page <= 2000:
                found.append(page)
                out.append(f"\n[p. {page}]\n")
                continue
        out.append(line)
    return out, found


def dehyphenate(text: str) -> tuple[str, list[str]]:
    """Rejoin words split across a line break, keeping genuine compounds hyphenated."""
    joins: list[str] = []

    def repl(m: re.Match) -> str:
        a, b = m.group(1), m.group(2)
        # A capitalised second half is usually a real compound (Anglo-Saxon, St-Botolph),
        # not a typesetter's break, so the hyphen stays.
        if b[:1].isupper():
            joins.append(f"{a}-{b} (kept hyphen)")
            return f"{a}-{b}"
        joins.append(f"{a}-{b} -> {a}{b}")
        return f"{a}{b}"

    return RE_HYPHEN_BREAK.sub(repl, text), joins


def rewrap(text: str) -> str:
    """Join hard-wrapped lines into paragraphs, keeping blank lines as paragraph breaks."""
    paras = re.split(r"\n\s*\n", text)
    out = []
    for para in paras:
        if para.strip().startswith("[p. "):
            out.append(para.strip())
            continue
        joined = " ".join(l.strip() for l in para.splitlines() if l.strip())
        if joined:
            out.append(joined)
    return "\n\n".join(out)


def find_flags(text: str, raw: str) -> list[str]:
    flags = []
    bad_years = sorted(set(RE_BAD_YEAR.findall(text)))
    if bad_years:
        flags.append(
            f"suspect-year: {', '.join(bad_years)} — a letter where a digit belongs. "
            f"Check against the photo before any of these reaches a date: field."
        )
    notes = sorted(set(m.group(0).strip() for m in RE_FOOTNOTE.finditer(text)))[:8]
    if notes:
        flags.append(
            f"footnote-markers: {', '.join(notes)} — superscript note numbers read as inline "
            f"digits. Do not read them as part of a date or a quantity."
        )
    if RE_ARTIFACT.search(text):
        flags.append("artifacts: runs of | ~ ^ \\ < > — likely rule lines or column bleed.")
    letters = sum(c.isalpha() or c.isspace() for c in text)
    if text and letters / max(len(text), 1) < 0.75:
        flags.append(
            f"low-alpha-ratio: {letters / max(len(text), 1):.0%} letters/spaces — the OCR may "
            f"have struggled. Read the clean file against the photo before extracting."
        )
    long_runs = [w for w in text.split() if len(w) > 30]
    if long_runs:
        flags.append(f"long-tokens: {len(long_runs)} word(s) over 30 chars — probable run-together text.")
    if not RE_YEAR.search(text) and len(text) > 800:
        flags.append("no-years-found: a long passage with no 4-digit year. Not an error, just unusual.")
    return flags


def process(path: Path, clean_dir: Path, dry: bool, force: bool) -> tuple[str, list[str]]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    meta, body = parse_header(raw)
    from_name = parse_filename(path.stem)
    book_from_header = bool(meta.get("book"))
    for key, value in from_name.items():
        meta.setdefault(key, value)
    if book_from_header:
        meta.pop("book-from-filename", None)

    log: list[str] = []
    missing = [k for k in ("book", "chapter") if not meta.get(k)]
    if missing and not force:
        return "error", [
            f"NO PROVENANCE ({', '.join(missing)} missing) — skipped.",
            "  Add a header block to the file, or rename it like",
            "  'ackroyd-london__ch08__p214-215.txt'. §10 makes a missing source an error, and",
            "  catching it here costs a rename; catching it after extraction costs a re-read.",
        ]

    text = normalise_chars(body)
    lines = text.split("\n")
    lines, heads = strip_running_heads(lines, meta)
    lines, pages = mark_pages(lines, meta)
    text = "\n".join(lines)
    text, joins = dehyphenate(text)
    text = rewrap(text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    flags = find_flags(text, raw)
    if heads:
        log.append(f"removed {len(heads)} running head/folio line(s): " + "; ".join(heads[:4]))
    if pages:
        meta.setdefault("pages", f"{min(pages)}-{max(pages)}" if len(set(pages)) > 1 else str(pages[0]))
        log.append(f"marked {len(pages)} page boundary/boundaries: {pages}")
    if joins:
        kept = sum(1 for j in joins if "kept" in j)
        log.append(f"rejoined {len(joins) - kept} hyphenated line break(s), kept {kept} compound(s)")

    header = ["# ingest", f"source-file: {path.name}"]
    for key in PROV_KEYS:
        if meta.get(key):
            header.append(f"{key}: {meta[key]}")
    if meta.get("book-from-filename"):
        header.append("book-source: filename (verify the title before it reaches a source: field)")
    for f in flags:
        header.append(f"flag: {f}")
    header.append("#")

    out = clean_dir / f"{path.stem}.txt"
    if out.exists() and not force:
        return "exists", [f"already ingested, left alone: {out.name} (use --force to redo)"]
    if not dry:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(header) + "\n\n" + text, encoding="utf-8")
    log.append(f"{'would write' if dry else 'wrote'} {out.relative_to(clean_dir.parent.parent)}")
    log += [f"FLAG {f}" for f in flags]
    return "ok", log


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vault", default=".")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="overwrite clean files; ingest without provenance")
    args = ap.parse_args()

    vault = Path(args.vault).resolve()
    inbox = vault / INBOX
    if not inbox.is_dir():
        print(f"error: {inbox} not found — run seed_vault.py", file=sys.stderr)
        return 2

    raws = sorted(p for p in inbox.glob("*.txt") if p.is_file())
    if not raws:
        print(f"{INBOX}/ is empty — nothing to ingest.")
        return 0

    tally = Counter()
    for path in raws:
        status, log = process(path, inbox / "clean", args.dry_run, args.force)
        tally[status] += 1
        print(f"\n{path.name}")
        for line in log:
            print(f"  {line}")

    parts = [f"{tally['ok']} ingested"]
    if tally["exists"]:
        parts.append(f"{tally['exists']} already done")
    if tally["error"]:
        parts.append(f"{tally['error']} needing provenance")
    print(f"\n{', '.join(parts)} — clean files in {INBOX}/clean/")
    if tally["ok"]:
        print("Read each clean file against its photo before extracting — the flags above are")
        print("the OCR errors worth checking, not a guarantee there are no others.")
    # Non-zero only when a file needs a human: an already-ingested file is idempotent, not a fault.
    return 1 if tally["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
