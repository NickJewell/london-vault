---
type: registry
registry: periods
---

# Registry — Periods

The period taxonomy is **fixed**. Do not add, rename, or re-bound a period without the
user's explicit approval — every event and claim in the vault links to these exact names,
so a rename is a vault-wide migration, not an edit.

Each period has a first-class note in `/Periods` (schema §4). Every event and claim gets
**both** a `period:` link from this table **and** an ISO `date:`/`date-range:` — the link
answers "show me everything Norman", the date makes timelines sortable.

<!-- BEGIN generated: taxonomy -->

| Period note | Starts | Ends | Preceded by | Followed by |
|---|---|---|---|---|
| `[[Pre-Roman London (before 43)]]` | -4000* | 43 | — | Roman London |
| `[[Roman London (43–410)]]` | 43 | 410 | Pre-Roman London | Saxon London |
| `[[Saxon London (410–1066)]]` | 410 | 1066 | Roman London | Norman London |
| `[[Norman London (1066–1154)]]` | 1066 | 1154 | Saxon London | Medieval London |
| `[[Medieval London (1154–1485)]]` | 1154 | 1485 | Norman London | Tudor London |
| `[[Tudor London (1485–1603)]]` | 1485 | 1603 | Medieval London | Stuart London |
| `[[Stuart London (1603–1714)]]` | 1603 | 1714 | Tudor London | Georgian London |
| `[[Georgian London (1714–1837)]]` | 1714 | 1837 | Stuart London | Victorian London |
| `[[Victorian London (1837–1901)]]` | 1837 | 1901 | Georgian London | Edwardian & WWI London |
| `[[Edwardian & WWI London (1901–1918)]]` | 1901 | 1918 | Victorian London | Interwar London |
| `[[Interwar London (1918–1939)]]` | 1918 | 1939 | Edwardian & WWI London | WWII & Blitz London |
| `[[WWII & Blitz London (1939–1945)]]` | 1939 | 1945 | Interwar London | Postwar London |
| `[[Postwar London (1945–1980)]]` | 1945 | 1980 | WWII & Blitz London | Modern & Contemporary London |
| `[[Modern & Contemporary London (1980–present)]]` | 1980 | 2100* | Postwar London | — |

\* open bound — a working value so timelines sort and date comparisons behave, not a claim.

<!-- END generated: taxonomy -->

## Assigning a period

Pick the period containing the event's date. Note names use an **en dash (–)**, not a hyphen —
copy them from this table rather than retyping, or the links will not resolve.

**Boundary years belong to the later period** (a period's `starts` year is inside it, its
`ends` year is the next period's start). 1066 is Norman, not Saxon; 1485 is Tudor; 1603 is
Stuart. Where a source treats the boundary differently, follow this table anyway and note the
discrepancy in the body — consistency is what makes the period queries trustworthy.

**Spanning events** (a `date-range` crossing a boundary, e.g. 1042/1087) take the period of the
range's **start**, and mention the span in the body. If the event is genuinely about the
transition itself, link both periods as a list.

**Before 43 CE**: use `[[Pre-Roman London (before 43)]]`, however early the material — the period
is open at its start, and its nominal `starts: -4000` is a sorting bound, not a boundary. BCE
years go in frontmatter as negative numbers (`date: -55`) with "55 BCE" written in the body.

**Recent material**: `[[Modern & Contemporary London (1980–present)]]` is open at its end, so it
takes everything from 1980 onward. Its nominal `ends: 2100` exists so date comparisons behave; it
is not a boundary, and nothing after it needs a flag.

**Boundary labels**: a period's label ends on the year the next one begins, so `Postwar London
(1945–1980)` runs to the end of 1979 and 1980 opens the next period. This is why Postwar is
labelled 1945–1980 rather than 1945–1979 — the convention keeps any year from falling between two
periods.
