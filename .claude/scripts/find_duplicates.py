#!/usr/bin/env python3
"""Find probable duplicate entities and near-duplicate claims in a London vault (§11).

Duplicates are the characteristic failure of long extractions: chapter 2 creates
"Richard Whittington", chapter 9 creates "Dick Whittington", and nothing in either note reveals
the other exists. This groups notes by a normalised name, then by fuzzy similarity, and reports
candidates for a human to judge.

It deliberately reports rather than merges. Two notes with similar names are sometimes two real
entities — Edward IV and Edward VI, St Botolph Aldgate and St Botolph Aldersgate — and a merge is
not reversible from the vault alone.

Multi-role name variants (Aldgate (gate) / Aldgate Ward / Aldgate (area)) are expected by §3 and
are reported separately, as confirmation rather than as a problem.

Usage:
    python3 find_duplicates.py [--vault PATH] [--threshold 0.86]
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_vault import (  # noqa: E402
    CONTENT_DIRS, SKIP_DIRS, ROLE_SUFFIX, ROLE_WORD, parse_frontmatter, as_text, base_name,
)

normalise = base_name


def role_of(name: str) -> str:
    m = ROLE_SUFFIX.search(name)
    if m:
        return m.group(1).lower()
    m2 = ROLE_WORD.search(name)
    return m2.group(1).lower() if m2 else ""


PLACE_TYPES = {"structure", "ward", "district", "street", "parish", "settlement"}


def is_multirole(members: list[dict]) -> bool:
    """True when a shared base name is the Aldgate rule working, not a duplicate.

    §3 requires one note per role, so several notes sharing a base name are expected — but only
    when they really are distinct roles: each carries a different role marker in its name, or
    they are places of distinct types. Two same-type notes with the same base name are a
    duplicate however tidily they are named.
    """
    roles = [m["role"] for m in members]
    if all(roles) and len(set(roles)) == len(members):
        return True
    types = [m["type"] for m in members]
    return (
        len(set(types)) == len(members)
        and all(t in PLACE_TYPES for t in types)
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vault", default=".")
    ap.add_argument("--threshold", type=float, default=0.86, help="fuzzy similarity cutoff (0-1)")
    args = ap.parse_args()

    vault = Path(args.vault).resolve()
    notes = []
    for p in sorted(vault.rglob("*.md")):
        rel = p.relative_to(vault)
        if any(part in SKIP_DIRS for part in rel.parts) or rel.parts[0] not in CONTENT_DIRS:
            continue
        fm, _, _ = parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        raw_aliases = fm.get("aliases") or []
        notes.append({
            "name": p.stem,
            "path": str(rel),
            "type": as_text(fm.get("type")).strip(),
            "aliases": [str(a) for a in raw_aliases] if isinstance(raw_aliases, list) else [],
            "norm": normalise(p.stem),
            "role": role_of(p.stem),
            "statement": as_text(fm.get("statement")).strip(),
        })

    if not notes:
        print("no content notes found — nothing to reconcile")
        return 0

    exact, multirole, fuzzy, alias_hits = [], [], [], []

    groups: dict[str, list[dict]] = defaultdict(list)
    for n in notes:
        groups[n["norm"]].append(n)
    for norm, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        if is_multirole(members):
            multirole.append((norm, members))
        else:
            exact.append((norm, members))

    # Claims and source notes are excluded from name-similarity: claim filenames are descriptive
    # sentences and source notes are "<Book> — Chapter N" by construction, so both are near-
    # identical by name without being duplicates. Claims are compared on their statements below.
    singles = [
        n for n in notes
        if len(groups[n["norm"]]) == 1 and n["type"] not in {"claim", "source"}
    ]
    for i, a in enumerate(singles):
        for b in singles[i + 1:]:
            if a["type"] != b["type"] or not a["norm"] or not b["norm"]:
                continue
            ratio = difflib.SequenceMatcher(None, a["norm"], b["norm"]).ratio()
            if ratio >= args.threshold:
                fuzzy.append((round(ratio, 3), a, b))

    alias_index: dict[str, list[str]] = defaultdict(list)
    for n in notes:
        for a in n["aliases"]:
            alias_index[normalise(str(a))].append(n["name"])
    for n in notes:
        for owner in alias_index.get(n["norm"], []):
            # A role-variant sharing the base name's alias is what §3 asks for, not a duplicate:
            # Aldgate Ward and Aldgate (area) both legitimately alias "Aldgate".
            if owner == n["name"] or base_name(owner) == n["norm"]:
                continue
            alias_hits.append((n["name"], owner))

    claims = [n for n in notes if n["type"] == "claim" and n["statement"]]
    claim_pairs = []
    for i, a in enumerate(claims):
        for b in claims[i + 1:]:
            ratio = difflib.SequenceMatcher(None, a["statement"].lower(), b["statement"].lower()).ratio()
            if ratio >= 0.75:
                claim_pairs.append((round(ratio, 3), a, b))

    def section(title: str, rows: list, render) -> None:
        print(f"\n## {title} ({len(rows)})")
        if not rows:
            print("  none")
            return
        for row in rows:
            render(row)

    section("Probable duplicate entities", exact, lambda r: [
        print(f"  '{r[0]}':"),
        [print(f"      {m['path']}  (type: {m['type'] or '?'})") for m in r[1]],
    ])

    section("Near-duplicate names (same type)", sorted(fuzzy, reverse=True), lambda r: print(
        f"  {r[0]:.2f}  {r[1]['path']}  ~  {r[2]['path']}"))

    section("Note whose name is another note's alias", alias_hits, lambda r: print(
        f"  '{r[0]}' is listed as an alias of '{r[1]}' — one of them should not exist"))

    section("Near-duplicate claims", sorted(claim_pairs, reverse=True), lambda r: print(
        f"  {r[0]:.2f}  {r[1]['path']}\n        ~  {r[2]['path']}"))

    section("Multi-role name sets (expected under §3)", multirole, lambda r: print(
        f"  '{r[0]}': " + ", ".join(f"{m['name']} [{m['type'] or '?'}]" for m in r[1])))

    total = len(exact) + len(fuzzy) + len(alias_hits)
    print(f"\n{total} candidate group(s) for review; {len(claim_pairs)} claim pair(s) worth comparing.")
    print("Nothing was merged. Judge each candidate against the sources before acting —")
    print("two similar names are often two real entities, and a merge cannot be undone from the vault.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
