# G251 R1/R2 repair implementation record

Date: 2026-08-24

Repair authority: `REPAIR_PREREGISTRATION.md`, committed and pushed at `bd8f0a2b` before changes.

## R1

- `ATTACHMENT_OWNERSHIP.tsv` now contains explicit Boolean `E`, `I`, `C`, and `W` cells for all 18
  candidates.
- Every leg has an exact manifest source, source-resolving locator, and concise evidence statement:
  72/72 cited cells.
- Production builds candidate-specific evidence rows and validates every locator.
- The independent implementation rebuilds the expected ledger bytes without importing production
  code or output; its SHA-256 equals the saved ledger SHA-256.
- Four new hostile mutations reject an erased `I` leg, blank citation, unknown source, and
  mismatched locator. Final hostile result: 26/26 caught.

The explicit ledger records three owned weight-zero evaluators—reciprocal redshift/clock ratio,
causal cones, and normalized Jacobi shape—that cannot calibrate the homothety. This makes the
preregistered leg typing explicit without changing any final candidate classification or landing.

## R2

- `verify_sealed_premise_registry.py` provides a no-write, self-contained audit of the exact sealed
  233-row registry, required columns, unique IDs, and load-bearing G249/G250 scope statements.
- `SEALED_PREMISE_REGISTRY_RESULT.json` records its exact passing output.
- `verify_package.py` replays it exactly.
- `COMMANDS.md` distinguishes this sealed registry audit from the broader repository-only
  `verify_current_scientific_premises.py`, which also passes before banking.

No observational value, fitted coefficient, new scientific source, anchor, history, branch
population, or outcome entered either repair. Fresh repair-only external follow-up accepted both
repairs without changing the landing.
