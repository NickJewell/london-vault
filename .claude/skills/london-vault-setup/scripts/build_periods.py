#!/usr/bin/env python3
"""Regenerate the period notes and the registry table from assets/taxonomy.json.

The period taxonomy is the one part of the schema where a typo is silent: note names carry an
en dash (U+2013), every event links them by exact name, and the preceded-by/followed-by chain has
to stay consistent in both directions. Hand-editing ten-plus notes to add one period is how that
chain breaks. Edit taxonomy.json instead and run this.

Regenerating notes is safe because period notes hold no extracted content — their bodies are
blurb plus Dataview blocks. Everything else in the vault is append-only by §11.

Usage:
    python3 build_periods.py [--vault PATH] [--assets-only] [--dry-run]

By default it writes both the skill's bundled assets and the vault (so a re-seed and the live
vault cannot disagree). --assets-only skips the vault.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BEGIN = "<!-- BEGIN generated: taxonomy -->"
END = "<!-- END generated: taxonomy -->"


def note_name(p: dict) -> str:
    return f"{p['name']} ({p['label']})"


def render_note(p: dict, prev: dict | None, nxt: dict | None) -> str:
    full = note_name(p)
    preceded = f'"[[{note_name(prev)}]]"' if prev else ""
    followed = f'"[[{note_name(nxt)}]]"' if nxt else ""
    boundary = (
        f"Boundary years belong to the later period: {p['ends']} is the first year of the next\n"
        f"period, not the last of this one (see `_registry/periods.md`). Where a source draws the\n"
        f"line differently, follow the registry and note the discrepancy in the event body — the\n"
        f"value of these links is that they mean the same thing in every chapter.\n"
    ) if nxt else (
        "This is the last period in the taxonomy, so it has no upper boundary to share.\n"
    )
    extra = f"\n{p['note']}\n" if p.get("note") else ""
    open_start = ""
    if p.get("open_start"):
        open_start = (
            "\nThis period is open at its start: `starts` is a working bound so that timelines\n"
            "sort, not a claim about when the story begins.\n"
        )
    if p.get("open_end"):
        open_start += (
            "\nThis period is open at its end: `ends` is a working bound so that timelines sort\n"
            "and date comparisons behave, not a prediction. Material later than the bound still\n"
            "belongs here — date it with its own ISO year.\n"
        )
    return f"""---
type: period
starts: {p['starts']}
ends: {p['ends']}
preceded-by: {preceded}
followed-by: {followed}
---

# {full}

{p['blurb']}
{extra}{open_start}
{boundary}
## Events in this period

```dataview
TABLE date AS "Date", actor AS "Actor", affected AS "Affected", source AS "Source"
FROM "Events"
WHERE contains(period, this.file.link)
SORT date ASC
```

## Claims about this period

```dataview
TABLE confidence AS "Confidence", statement AS "Claim", source AS "Source"
FROM "Claims"
WHERE contains(period, this.file.link)
SORT confidence ASC
```

## Places with material from this period

```dataview
LIST FROM "Places" WHERE contains(file.outlinks, this.file.link)
```
"""


def render_table(periods: list[dict]) -> str:
    lines = [
        BEGIN,
        "",
        "| Period note | Starts | Ends | Preceded by | Followed by |",
        "|---|---|---|---|---|",
    ]
    for i, p in enumerate(periods):
        prev = periods[i - 1]["name"] if i else "—"
        nxt = periods[i + 1]["name"] if i < len(periods) - 1 else "—"
        starts = f"{p['starts']}*" if p.get("open_start") else p["starts"]
        ends = f"{p['ends']}*" if p.get("open_end") else p["ends"]
        lines.append(f"| `[[{note_name(p)}]]` | {starts} | {ends} | {prev} | {nxt} |")
    lines += [
        "",
        "\\* open bound — a working value so timelines sort and date comparisons behave, not a claim.",
        "",
        END,
    ]
    return "\n".join(lines)


def render_entity_rows(periods: list[dict]) -> str:
    lines = [
        BEGIN,
        "",
        "| Canonical name | Type | Aliases | Note path | Status | First seen |",
        "|---|---|---|---|---|---|",
    ]
    for p in periods:
        full = note_name(p)
        lines.append(f"| {full} | period | — | `Periods/{full}.md` | note | seed |")
    lines += ["", END]
    return "\n".join(lines)


def splice(path: Path, block: str, dry: bool) -> str:
    """Replace the generated region of a file, or report that markers are missing."""
    if not path.exists():
        return f"missing (skipped): {path}"
    text = path.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        return f"NO MARKERS (skipped, add {BEGIN} / {END}): {path}"
    head, _, rest = text.partition(BEGIN)
    _, _, tail = rest.partition(END)
    new = head + block + tail
    if new == text:
        return f"unchanged: {path}"
    if not dry:
        path.write_text(new, encoding="utf-8")
    return f"updated: {path}"


def main() -> int:
    here = Path(__file__).resolve().parent
    assets = here.parent / "assets"
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vault", default=".")
    ap.add_argument("--assets-only", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    data = json.loads((assets / "taxonomy.json").read_text(encoding="utf-8"))
    periods = data["periods"]
    for p in periods:
        for key in ("name", "label", "starts", "ends", "blurb"):
            if key not in p:
                print(f"error: period {p.get('name', '?')} missing '{key}'", file=sys.stderr)
                return 2

    names = [note_name(p) for p in periods]
    if len(set(names)) != len(names):
        print("error: duplicate period note names in taxonomy.json", file=sys.stderr)
        return 2

    targets = [assets / "periods"]
    if not args.assets_only:
        vault = Path(args.vault).resolve()
        if not (vault / "Periods").is_dir():
            print(f"error: {vault}/Periods not found — run seed_vault.py first", file=sys.stderr)
            return 2
        targets.append(vault / "Periods")

    actions = []
    for target in targets:
        wanted = {f"{n}.md" for n in names}
        for i, p in enumerate(periods):
            path = target / f"{note_name(p)}.md"
            body = render_note(p, periods[i - 1] if i else None,
                               periods[i + 1] if i < len(periods) - 1 else None)
            if path.exists() and path.read_text(encoding="utf-8") == body:
                continue
            actions.append(f"{'would write' if args.dry_run else 'wrote'}: {path}")
            if not args.dry_run:
                path.write_text(body, encoding="utf-8")
        for stale in sorted(target.glob("*.md")):
            if stale.name not in wanted:
                actions.append(f"STALE (rename or delete by hand): {stale}")

    reg = [assets / "registry" / "periods.md"]
    ent = [assets / "registry" / "entities.md"]
    if not args.assets_only:
        vault = Path(args.vault).resolve()
        reg.append(vault / "_registry" / "periods.md")
        ent.append(vault / "_registry" / "entities.md")
    for path in reg:
        actions.append(splice(path, render_table(periods), args.dry_run))
    for path in ent:
        actions.append(splice(path, render_entity_rows(periods), args.dry_run))

    print(f"{len(periods)} periods in taxonomy.json")
    for line in actions:
        print(f"  {line}")
    if any("STALE" in a for a in actions):
        print("\nStale notes are period notes no longer in the taxonomy. If a period was renamed,")
        print("rename the note and migrate every event/claim linking the old name before deleting.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
