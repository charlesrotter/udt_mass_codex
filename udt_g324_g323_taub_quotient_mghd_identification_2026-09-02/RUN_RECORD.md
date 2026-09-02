# G324 run record

Date: 2026-09-02

## Question

Determine whether every explicit registered G323 Taub quotient is already the smooth G322 MGHD of
its own fixed datum, without adding a physical law, scale, topology choice, or occupancy rule.

## Preregistration

Frozen and pushed at `c2476011` before outcome-bearing checks.

## Initial local commands

Run from this package directory:

```text
python3 -S derive_taub_mghd.py
python3 -S verify_independent.py
python3 -S run_catch_proofs.py
```

Initial results passed. After correcting the bounded primary-source excerpt accounting, all three
commands and the aggregate verifier are replayed before sealing. Exact stdout, assertion counts,
Python version, hashes, and final states are recorded by the generated artifacts and package
verification result.

## Resource statement

CPU-only exact/analytic checks. No GPU, long solve, fit, observational outcome, or network access
is used by the registered replay. Network access was used only to inspect the primary arXiv theorem
source before sealing its bounded evidence record.
