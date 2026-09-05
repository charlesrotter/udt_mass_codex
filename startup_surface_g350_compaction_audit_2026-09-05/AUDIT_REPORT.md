# G350 startup-surface compaction audit

Date: 2026-09-05
Starting scientific commit: `77cb8d1c3c0287241479246cf74c976073708cfa`
Preregistration commits: `9cccb31d`, `455b63e8`

## Landing

`STARTUP_SURFACE_COMPACTED_AND_SEMANTICALLY_GUARDED__NO_SCIENTIFIC_CHANGE`

## What changed

- Corrected the stale `AGENTS.md` registry count from 320 to 333.
- Replaced repeated G313--G350 chronology with one bounded dependency table and kept exact
  row-level ownership in `CURRENT_SCIENTIFIC_PREMISES.tsv`.
- Centralized old startup snapshots in `archive/STARTUP_SURFACE_HISTORY.md` and added a Git-backed
  pre-compaction pointer without copying or rewriting scientific evidence.
- Replaced the active verifier's duplicated per-generation prose requirements with semantic
  ownership, frontier-range, current-route, archive-integrity, protected-work, and next-gate
  checks. Exact validation of all 333 registry rows remains. The obsolete 1,200-line legacy
  validator was removed; Git and the archive index retain historical recovery.
- Updated routing tests to mutate those semantic boundaries rather than require every historical G
  token in current prose.
- Repaired one hostile-rehearsal clipping risk by binding the supplied regular calibrated-pair
  qualification directly to `phi_pair=delta_AB` wherever it is displayed.

The eight startup-facing documents fell from 964 to 620 lines. No premise row, scientific package,
metric, kernel, result, observational grade, or canon file changed.

## Verification gates

| Gate | Result |
|---|---|
| Preregistered | `PASS` — committed before outcomes (`9cccb31d`, scope note `455b63e8`) |
| Bounded scope | `PASS` — startup docs, archive pointer/index, active startup verifier and routing tests only |
| Full premise audit | `PASS` — G242--G350/W5/W6 guards, 333 rows, archive integrity, `X_max`, 754 historical dispositions |
| Focused mutation suite | `PASS` — 62 passed, 1 deselected |
| Repository purity/regression suite | `PASS` — 137 passed, 1 expected xfail |
| Ordinary zero-context rehearsal | `PASS_WITH_EXPECTED_PRECOMMIT_DURABILITY_CAVEAT` |
| Hostile zero-context rehearsal | `PASS_AFTER_CLIPPING_REPAIR_WITH_EXPECTED_PRECOMMIT_DURABILITY_CAVEAT` |
| First independent catch-proof verifier | `REFUTED` — found two false-pass holes before banking |
| Repair-only independent verifier | `VERIFIED_WITH_CAVEATS` — both repairs failed closed |
| Final exact-tree independent verifier | `VERIFIED_WITH_CAVEATS` — six mutations failed closed; one live validator |

Commands used:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B -S verify_current_scientific_premises.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_startup_surface.py -k 'not full_foundational_premise_verifier_is_in_pytest'
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests
```

The repository suite's single xfail is the already-declared matter-sector habit-pin gap; this
documentation audit neither repairs nor widens it.

The first independent verifier found that the draft did not bind G350 specifically to the next
gate and did not reject an additive contradictory promotion of Universal Reciprocity to
`DERIVED`. Both defects were repaired before banking, given explicit mutation tests, and
independently replayed. The final verifier found no functional defect. Its remaining caveat is
pre-commit durability/remote freshness, closed only by the final commit and push.

## Scientific ceiling

This audit establishes only that a fresh worker can recover the current bounded claim, premise
ownership, protected-work boundary, and next gate from a smaller and semantically guarded startup
surface. It does not validate UDT science, derive a carried field or conservation law, select
`p,q`, choose a universe/history/scale/`X_max`, or canonize anything.

## Current gate retained

MAP/PONDER whether UDT should add a carried-object layer, exposing separately what is carried, its
observer weight, conservation versus local balance, and caustic/label handling. Every option is a
`NEW PREMISE`; no derivation or computation begins before Charles decides whether the layer belongs
in UDT.
