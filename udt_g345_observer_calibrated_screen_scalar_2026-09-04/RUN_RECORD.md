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
