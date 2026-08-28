#!/usr/bin/env python3
"""Check a London vault against the semantic schema in _schema/london-vault-schema.md.

Catches the errors that are cheap to fix now and expensive once more chapters sit on top of
them: missing provenance (§10), out-of-vocabulary types and relationship keys (§2, §9),
events missing a period or an ISO date (§4, §5), claims with an invalid confidence value (§8),
malformed dates (§7), and links that point at notes which do not exist.

Shared by the london-vault-extract and london-vault-reconcile skills.

Usage:
    python3 validate_vault.py [--vault PATH] [--strict] [--quiet]

Exit status is 1 if any ERROR is found (also on any WARN under --strict), else 0.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:  # keep the script usable on a bare Python
    yaml = None

CONTENT_DIRS = [
    "People", "Places", "Organizations", "Events",
    "Periods", "Concepts", "Claims", "Sources",
]
SKIP_DIRS = {"_registry", "_templates", "_schema", "_inbox", ".obsidian", ".git", ".claude"}

TYPES_BY_DIR = {
    "People": {"person"},
    "Places": {"structure", "ward", "district", "street", "parish", "settlement"},
    "Organizations": {"organization"},
    "Events": {"event"},
    "Periods": {"period"},
    "Concepts": {"concept"},
    "Claims": {"claim"},
    "Sources": {"source"},
}
ALL_TYPES = {t for ts in TYPES_BY_DIR.values() for t in ts}

RELATIONSHIP_KEYS = {
    "part-of", "contains", "located-in", "adjacent-to", "named-after", "on-site-of",
    "succeeded-by", "actor", "affected", "participated-in", "caused", "commissioned",
    "granted-to", "destroyed", "rebuilt", "resided-at", "buried-at", "held-office",
    "member-of", "influenced", "preceded-by", "followed-by", "disputes", "supports",
    "cited-by",
}
METADATA_KEYS = {
    "type", "aliases", "first-seen", "source", "page", "date", "date-range",
    "date-precision", "period", "statement", "asserted-by", "confidence", "evidence",
    "involves", "book", "author", "chapter", "chapter-title", "pages", "extracted",
    "starts", "ends", "founded", "dissolved", "tags", "cssclasses",
}
KNOWN_KEYS = RELATIONSHIP_KEYS | METADATA_KEYS
CONFIDENCE = {"stated-fact", "author-interpretation", "quoted-third-party", "disputed"}

RE_YEAR = re.compile(r"^-?\d{1,4}$")
RE_ISO_DATE = re.compile(r"^-?\d{1,4}(-\d{2}(-\d{2})?)?$")
RE_RANGE = re.compile(r"^(-?\d{1,4}(-\d{2}(-\d{2})?)?)/(-?\d{1,4}(-\d{2}(-\d{2})?)?)$")
RE_LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
RE_FLAG = re.compile(r"#flag/[a-z-]+")

# Shared with find_duplicates.py: reduce a note name to the entity it names, so that the
# multi-role variants §3 requires (Aldgate (gate) / Aldgate Ward / Aldgate (area)) collapse to
# one base. They are expected to share an alias, and must not be reported as duplicates.
ROLE_SUFFIX = re.compile(
    r"\s*\((gate|area|street|dock|ward|prison|borough|liberty|\d{3,4}[\u2013-]\d{3,4})\)\s*$", re.I)
ROLE_WORD = re.compile(r"\s+(ward|within|without)$", re.I)
_NOISE = re.compile(r"[^\w\s]")
_SAINT = re.compile(r"^(st|saint)\b\.?\s*", re.I)
_STOPWORDS = {"the", "of", "a", "an"}


def base_name(name: str) -> str:
    """Normalise a note name to its entity base for duplicate/alias comparison."""
    n = ROLE_SUFFIX.sub("", name)
    n = ROLE_WORD.sub("", n)
    n = _SAINT.sub("st ", n.strip())
    n = _NOISE.sub(" ", n).lower()
    return " ".join(w for w in n.split() if w not in _STOPWORDS)


def parse_frontmatter(text: str) -> tuple[dict, str, bool]:
    """Return (frontmatter, body, had_frontmatter)."""
    if not text.startswith("---"):
        return {}, text, False
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text, False
    raw = text[3:end].strip("\n")
    body = text[end + 4:]
    if yaml is not None:
        try:
            data = yaml.safe_load(raw)
            return (data if isinstance(data, dict) else {}), body, True
        except Exception:
            return {}, body, True
    # Fallback: flat key: value lines, enough for the subset this schema uses.
    data: dict = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or line.startswith((" ", "\t", "-")):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        data[key.strip()] = val.strip().strip('"').strip("'")
    return data, body, True


def as_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return " ".join(as_text(v) for v in value)
    return str(value)


def is_blank(value) -> bool:
    return value is None or (isinstance(value, str) and not value.strip()) or value == []


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []

    def add(self, level: str, path: str, message: str) -> None:
        self.rows.append((level, path, message))

    def count(self, level: str) -> int:
        return sum(1 for lv, _, _ in self.rows if lv == level)


def check_dates(fm: dict, rel: str, rep: Report) -> None:
    date, drange = fm.get("date"), fm.get("date-range")
    if not is_blank(date) and not is_blank(drange):
        rep.add("ERROR", rel, "has both date and date-range; use exactly one (§7)")
    if not is_blank(date) and not RE_ISO_DATE.match(as_text(date).strip()):
        rep.add("ERROR", rel, f"date '{as_text(date)}' is not ISO (YYYY, YYYY-MM or YYYY-MM-DD) (§7)")
    if not is_blank(drange) and not RE_RANGE.match(as_text(drange).strip()):
        rep.add("ERROR", rel, f"date-range '{as_text(drange)}' is not ISO start/end, e.g. 1066/1087 (§7)")
    prec = fm.get("date-precision")
    if not is_blank(prec) and as_text(prec).strip() not in {"circa", "exact", "approximate"}:
        rep.add("WARN", rel, f"date-precision '{as_text(prec)}' is unusual; §7 uses 'circa'")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vault", default=".", help="vault root (default: current directory)")
    ap.add_argument("--strict", action="store_true", help="exit non-zero on warnings too")
    ap.add_argument("--quiet", action="store_true", help="summary only")
    args = ap.parse_args()

    vault = Path(args.vault).resolve()
    if not vault.is_dir():
        print(f"error: vault root not found: {vault}", file=sys.stderr)
        return 2

    rep = Report()
    notes: dict[str, Path] = {}
    all_md = [
        p for p in vault.rglob("*.md")
        if not any(part in SKIP_DIRS for part in p.relative_to(vault).parts)
    ]
    for p in all_md:
        notes.setdefault(p.stem, p)

    aliases: dict[str, str] = {}
    flags: dict[str, list[str]] = defaultdict(list)
    checked = 0

    for path in sorted(all_md):
        rel = str(path.relative_to(vault))
        top = path.relative_to(vault).parts[0]
        if top not in CONTENT_DIRS:
            continue
        checked += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        fm, body, had_fm = parse_frontmatter(text)

        if not had_fm:
            rep.add("ERROR", rel, "no YAML frontmatter; every note needs at least type/aliases/first-seen (§2)")
            continue

        ntype = as_text(fm.get("type")).strip()
        if not ntype:
            rep.add("ERROR", rel, "missing 'type' (§2)")
        elif ntype not in ALL_TYPES:
            rep.add("ERROR", rel, f"type '{ntype}' is outside the schema's type list (§2)")
        elif ntype not in TYPES_BY_DIR[top]:
            expected = "/".join(sorted(TYPES_BY_DIR[top]))
            rep.add("ERROR", rel, f"type '{ntype}' does not belong in /{top} (expected {expected}) (§2)")

        for alias in (fm.get("aliases") or []) if isinstance(fm.get("aliases"), list) else []:
            key = str(alias).strip().lower()
            if not key:
                continue
            clash = aliases.get(key)
            if clash and clash != path.stem and base_name(clash) != base_name(path.stem):
                # Same alias on two different entities is a duplicate risk; the same alias on
                # role-variants of one name (Aldgate Ward / Aldgate (area)) is what §3 asks for.
                rep.add("WARN", rel, f"alias '{alias}' also claimed by '{clash}' (§11 duplicate risk)")
            else:
                aliases.setdefault(key, path.stem)

        # Provenance (§10). Period notes are seeded, not extracted, so they carry none.
        if ntype != "period":
            if is_blank(fm.get("first-seen")):
                rep.add("WARN", rel, "missing 'first-seen' (§2)")
            if ntype in {"event", "claim"} and is_blank(fm.get("source")):
                rep.add("ERROR", rel, "missing 'source' — provenance is mandatory (§10)")
            if ntype in {"event", "claim"} and is_blank(fm.get("page")):
                rep.add("WARN", rel, "missing 'page'; §10 wants page/section on every extraction")
            if ntype == "source" and is_blank(fm.get("book")):
                rep.add("WARN", rel, "source note missing 'book'")

        check_dates(fm, rel, rep)

        if ntype == "event":
            if is_blank(fm.get("date")) and is_blank(fm.get("date-range")):
                rep.add("ERROR", rel, "event has neither date nor date-range (§5)")
            if is_blank(fm.get("period")):
                rep.add("ERROR", rel, "event missing 'period' link; the ISO date does not substitute (§4)")
            if is_blank(fm.get("actor")) and is_blank(fm.get("affected")):
                rep.add("WARN", rel, "event has neither actor nor affected; nothing links it to the vault (§5)")

        if ntype == "claim":
            conf = as_text(fm.get("confidence")).strip()
            if not conf:
                rep.add("ERROR", rel, "claim missing 'confidence' — the field that preserves hedging (§8)")
            elif conf not in CONFIDENCE:
                rep.add("ERROR", rel, f"confidence '{conf}' not one of {'|'.join(sorted(CONFIDENCE))} (§8)")
            if is_blank(fm.get("statement")):
                rep.add("ERROR", rel, "claim missing 'statement' (§8)")
            if is_blank(fm.get("asserted-by")):
                rep.add("WARN", rel, "claim missing 'asserted-by' (§8)")
            if is_blank(fm.get("involves")):
                rep.add("WARN", rel, "claim missing 'involves'; it will not surface on any entity note (§8)")

        if ntype == "period":
            for key in ("starts", "ends"):
                if is_blank(fm.get(key)):
                    rep.add("WARN", rel, f"period missing '{key}' (§4)")

        for key in fm:
            k = str(key).strip()
            if k not in KNOWN_KEYS:
                rep.add(
                    "WARN", rel,
                    f"key '{k}' is outside the controlled vocabulary; use the nearest term "
                    f"and tag #flag/vocab-gap rather than inventing a key (§9)",
                )

        # Inline Dataview fields are equally part of the vocabulary (§9).
        for m in re.finditer(r"^\s*([a-z][a-z-]{2,})::", body, re.MULTILINE):
            k = m.group(1)
            if k not in KNOWN_KEYS:
                rep.add("WARN", rel, f"inline field '{k}::' is outside the controlled vocabulary (§9)")

        for m in RE_FLAG.finditer(text):
            flags[m.group(0)].append(rel)

        for m in RE_LINK.finditer(text):
            target = m.group(1).strip()
            if target and target not in notes:
                rep.add("INFO", rel, f"link [[{target}]] has no note yet")

    if not args.quiet:
        for level in ("ERROR", "WARN", "INFO"):
            rows = [r for r in rep.rows if r[0] == level]
            if not rows:
                continue
            print(f"\n{level} ({len(rows)})")
            for _, path, message in rows:
                print(f"  {path}: {message}")

    if flags:
        print(f"\nFLAGS awaiting resolution ({sum(len(v) for v in flags.values())})")
        for tag, paths in sorted(flags.items()):
            print(f"  {tag}: {len(paths)}")
            for p in sorted(set(paths)):
                print(f"      {p}")

    errors, warns, infos = rep.count("ERROR"), rep.count("WARN"), rep.count("INFO")
    print(f"\nchecked {checked} note(s): {errors} error(s), {warns} warning(s), {infos} info")
    if errors:
        print("Errors are schema violations — fix them before committing the chapter.")
    return 1 if errors or (args.strict and warns) else 0


if __name__ == "__main__":
    raise SystemExit(main())
