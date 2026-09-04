# G345 run record

Date: 2026-09-04
Device: CPU only
Python mode: dependency-disabled `python3 -S`; bytecode disabled
GPU: not used

## Preregistration

Commit `d22f1bdb` was pushed to `origin/grok` before execution.
The complete internally qualified result was banked at commit `f20a5072` before sealing for review.

## Production first execution

```bash
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S derive_screen_scalar.py
```

Result: `9822/9824`. Two supplemental strict numerical convergence-order checks failed after both
values reached approximately `1e-11` error. See `PREREGISTRATION_EXECUTION_NOTE.md`.

## Production repaired execution

Same command. Result: `9824/9824`, maximum registered error
`6.951093173576455e-14` in the principal comparison; reference covariance maximum
`4.7375971271501307e-14`.

## Independent execution

```bash
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S verify_screen_scalar_independent.py
```

Result: `4360/4360`; largest error `3.2360683022147896e-09` in the independent Simpson block
composition route.

## Hostile execution

```bash
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S run_catch_proofs.py
```

Result: `17/17` hostile mutations caught.

## Aggregate no-write execution

```bash
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S verify_package.py
```

The first aggregate wording gate passed `16/17`; its self-referential preregistration-hash defect
and repair are preserved in `PREREGISTRATION_EXECUTION_NOTE.md`. The repaired aggregate result is
`17/17`, including all three no-write sub-replays and exact package-byte preservation.

All listed runs were bounded CPU checks. No long solve or background process was started.

## External and final integration gates

The fresh external reviewer authenticated all 29 sealed payloads, reproduced production
`9824/9824`, independent `4360/4360`, hostile `17/17`, and aggregate `17/17`, and independently
checked the load-bearing formulas. It returned:

```text
ACCEPT_G345_BOUNDED_OBSERVER_CALIBRATED_SCREEN_SCALAR
```

The reviewer retained three non-blocking verifier-quality caveats: documentary compact-label
assertions, tautological named coverage assertions whose underlying loops still cover the declared
domain, and brittle text-token guards. They do not change the bounded scientific result and are
preserved in `EXTERNAL_REVIEW_RESPONSE.md`.

After adding exact external-return authentication, the final aggregate contains `19/19` gates.

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B verify_current_scientific_premises.py
PASS: 328-row registry and G345 startup/premise guards

PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest tests/
220 passed, 1 xfailed
```

The first full-suite integration run reached `219 passed, 1 xfailed` and found one documentation-
only failure: the combined G343/G344/G345 pointer in `INDEX.md` exceeded the 220-character line
limit. The pointer was split while keeping the 118-line cap, its targeted test passed, and the clean
full-suite rerun produced the result above. The marked xfail is the existing matter-sector habit-pin
gate and is unrelated to G345.
