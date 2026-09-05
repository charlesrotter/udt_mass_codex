# G348 run record

Date: 2026-09-04
Python: standard library under `python3 -S`
Device: CPU; no GPU needed for exact rank-four matrix/ODE checks

## Preregistration

- Original preregistration: `17c35cc6`
- Outcome-unseen crossing-order refinement: `23e50369`

## Production

Command:

```text
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S derive_generic_null_screen_area.py
```

First result: `39541/39542`. The sole failed diagnostic and its correction are recorded in
`PREREGISTRATION_EXECUTION_NOTE.md`.

Corrected result: `39542/39542`; 420 noncommuting piecewise-exact symmetric-tide profiles, 420
arbitrary observer cases, 210 reflected frame pairs, and 420 stationary-sewing cases. Maximum
ordinary algebra error was `5.684341886080802e-14`; centered crossing-order diagnostics were below
`3.34e-9`, against `2e-6`.

## Independent

Command:

```text
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S verify_generic_null_screen_area_independent.py
```

Result: `9759/9759`; 150 smooth variable-tide profiles and 21 near-null rapidity cases. Maximum
composition error was `2.377154029176154e-12`, below the `2e-7` independent tolerance.

## Hostile controls

Command:

```text
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S run_catch_proofs.py
```

Result: `21/21` mutations caught.

## Aggregate

The first aggregate returned `17/18` on one line-wrapped documentary phrase. After the recorded
phrase-hook-only repair, the registered no-write aggregate returned `18/18` and changed no package
evidence bytes.

## External review and postreview replay

Fresh external `gpt-5.6-sol` authenticated all 33 manifest payloads, reran `18/18`, independently
reconstructed the theorem, and returned `ACCEPT_G348_GENERIC_NULL_SCREEN_AREA_THEOREM` without
required repair. After importing the exact response and transmission record, the registered
aggregate returned `19/19` and changed no evidence bytes.
