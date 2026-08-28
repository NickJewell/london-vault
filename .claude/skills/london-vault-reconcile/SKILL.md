---
name: london-vault-reconcile
description: Audit the London history Obsidian vault for probable duplicate entities, conflicting or contradictory claims, schema violations, missing provenance, and unresolved flag tags (ambiguous-place, ambiguous-date, vocab-gap, unnamed-actor). Use when the user asks to reconcile, audit, check, clean up, spot-check or health-check the vault, asks whether two notes are the same entity, asks what flags or loose ends are outstanding, wants to know where sources contradict each other, or after finishing a book or a run of chapters. Also use when validation errors are reported during extraction and need working through.
---

# London Vault — Reconciliation

The periodic pass §11 asks for: probable duplicate entities, conflicting claims, and `#flag/*`
tags awaiting resolution. Its value is cumulative — every chapter adds a little drift, and drift
that is caught at chapter 10 costs a conversation, while the same drift caught at chapter 40 costs
a re-read.

Reconciliation **reports and proposes; it does not silently merge.** Merges are irreversible from
the vault alone, and the judgement they need — are these two real entities or one? — is the
user's. Bring them a decision, not a fait accompli.

## Run the two checks

```bash
python3 .claude/scripts/validate_vault.py --vault .     # schema conformance + flag inventory
python3 .claude/scripts/find_duplicates.py --vault .     # duplicate and near-duplicate candidates
```

`validate_vault.py` reports ERROR (schema violations — missing source on an event or claim, an
invalid `confidence`, an event with no period, a malformed date), WARN (missing `first-seen` or
`page`, out-of-vocabulary keys, alias collisions), and INFO (links with no note yet, which are
normal for reserved names). It also inventories every `#flag/*` in the vault.

`find_duplicates.py` groups notes by normalised name, then by fuzzy similarity within a type, and
separately confirms multi-role name sets, which §3 *expects* to look like duplicates.

## Working the results

Take them in this order. Each stage can create or dissolve work in the next, so doing them out of
order means doing some of them twice.

### 1. Schema errors

Fix these first and without ceremony: they are unambiguous, and while they stand, the queries the
vault exists to support return wrong answers rather than incomplete ones. An event missing its
`period` link is silently absent from "everything Norman" — nothing looks broken.

Missing `source` on an extracted note is the one error that may not be locally fixable. If the
note's provenance genuinely cannot be reconstructed, say so rather than inventing a plausible
chapter reference: an invented citation is worse than an acknowledged gap, because it looks
checkable and isn't.

### 2. Duplicate candidates

For each candidate group, read both notes and their `first-seen` before deciding. Three outcomes:

- **Same entity** → merge into the note with the earlier `first-seen` (it holds the true first
  encounter), append the other's content under its own source heading, add the loser's name to
  `aliases`, repoint inbound links, update `_registry/entities.md`, delete the empty note.
- **Different entities** → add a disambiguating qualifier to both names if they are confusable
  (`Thomas More (1478–1535)`), and note the distinction in the registry so the next chapter does
  not re-derive it.
- **Multi-role variants** → correct as they stand (§3). Confirm the registry's multi-role table
  has a row for the name; if not, that is the fix.

Propose merges to the user in a batch with the evidence for each, rather than one at a time — the
comparison between candidates is usually what makes the call obvious.

### 3. Conflicting claims

`find_duplicates.py` surfaces near-duplicate claim statements. Two claims saying nearly the same
thing from different sources are usually a **corroboration**: link them `supports`. Two saying
opposite things are a **dispute**: link them `disputes` and set both to `confidence: disputed`.

Do not resolve the disagreement by deleting a claim or picking a winner. A vault that records two
historians disagreeing is more useful than one that records whichever was extracted second — and
the disagreement is often the most interesting thing on the page.

### 4. Flags

| Flag | Resolution |
|---|---|
| `#flag/ambiguous-place` | Re-read the passage with `references/disambiguation.md` from `london-vault-extract`. Often a later chapter has since made the role obvious. Repoint the link and remove the flag. |
| `#flag/ambiguous-date` | Try `_registry/reigns.md` again; a later chapter may date the same event. If it stays undatable, leave the flag — it is doing its job. |
| `#flag/vocab-gap` | Collect these and put them to the user **together**. §9 forbids extending the vocabulary without approval, and one considered decision across eight gaps is better than eight improvisations. |
| `#flag/unnamed-actor` | Check whether a later chapter names the office-holder. If so, create the person note and repoint. |

A flag that cannot be resolved stays. Flags are not a defect backlog to drive to zero; they are
the vault's record of what the sources do not settle, and clearing one by guessing converts an
honest uncertainty into a confident error.

### 5. Registry drift

The registries only work if they are current. Check that every note has a row in
`_registry/entities.md`, that reserved names which have since acquired notes are marked `note`
rather than `reserved`, and that every multi-role name met so far has a row in `places.md`.

## Reporting back

Give the user, briefly:

1. Errors fixed (with counts).
2. Merge proposals, each with both note paths, both `first-seen` values, and the evidence.
3. Claim conflicts found, with the two statements side by side.
4. Flags resolved, and flags that remain with a line on why.
5. Any schema question the pass raised — a vocabulary gap, a type that does not fit, a period
   boundary that keeps causing trouble. §12 is explicit that the fix belongs in the schema and the
   templates, not only in the affected notes, so these are worth raising even when the immediate
   instance was patched.

Commit the fixes as `Reconcile: <what changed>`, separately from any extraction commit, so a
reconciliation can be reviewed or reverted without disturbing a chapter's extraction.
