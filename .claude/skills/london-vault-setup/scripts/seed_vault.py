#!/usr/bin/env python3
"""Seed a London vault with the folder structure, registries, templates and period notes.

Idempotent by construction: existing files are never overwritten, only reported. That matters
because seeding may be re-run after a book is part-way extracted, and clobbering a registry that
has twelve chapters of accumulated aliases in it would be unrecoverable from the vault alone.

Usage:
    python3 seed_vault.py [--vault PATH] [--dry-run]
"""
import argparse
import shutil
import sys
from pathlib import Path

FOLDERS = [
    "People", "Places", "Organizations", "Events", "Periods",
    "Concepts", "Claims", "Sources", "_registry", "_templates",
]

GITKEEP = (
    "# Keeps this folder in git while it is empty; Obsidian hides dotfiles, so it is\n"
    "# invisible in the vault. Safe to delete once the folder has notes in it.\n"
)


def main() -> int:
    here = Path(__file__).resolve().parent
    assets = here.parent / "assets"

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--vault", default=".", help="vault root (default: current directory)")
    ap.add_argument("--dry-run", action="store_true", help="report actions without writing")
    args = ap.parse_args()

    vault = Path(args.vault).resolve()
    if not vault.is_dir():
        print(f"error: vault root not found: {vault}", file=sys.stderr)
        return 1
    if not assets.is_dir():
        print(f"error: bundled assets not found at {assets}", file=sys.stderr)
        return 1

    created, skipped = [], []

    def place(src: Path, dest: Path) -> None:
        rel = dest.relative_to(vault)
        if dest.exists():
            skipped.append(str(rel))
            return
        created.append(str(rel))
        if not args.dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)

    for folder in FOLDERS:
        target = vault / folder
        if not target.exists():
            created.append(f"{folder}/")
            if not args.dry_run:
                target.mkdir(parents=True)
        keep = target / ".gitkeep"
        if not keep.exists() and not args.dry_run:
            target.mkdir(parents=True, exist_ok=True)
            keep.write_text(GITKEEP, encoding="utf-8")

    for src in sorted((assets / "registry").glob("*.md")):
        place(src, vault / "_registry" / src.name)
    for src in sorted((assets / "templates").glob("*.md")):
        place(src, vault / "_templates" / src.name)
    for src in sorted((assets / "periods").glob("*.md")):
        place(src, vault / "Periods" / src.name)

    verb = "would create" if args.dry_run else "created"
    print(f"{verb} {len(created)} item(s):")
    for item in created:
        print(f"  + {item}")
    if skipped:
        print(f"\nleft untouched ({len(skipped)} already present):")
        for item in skipped:
            print(f"  = {item}")
        print("\nNothing was overwritten. To refresh a seeded file, diff it against the copy in")
        print("the skill's assets/ directory and merge by hand — a registry accumulates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
