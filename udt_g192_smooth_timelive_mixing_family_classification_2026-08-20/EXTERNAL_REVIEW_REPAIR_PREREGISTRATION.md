# G192 external-review repair preregistration

Date: 2026-08-20

The first sealed external review returned `G192_ACCEPTED_WITH_REPAIRS`. It found no scientific
counterexample to the bounded two-function classification, but identified two genuine evidence-
harness false-pass risks.

The repair is restricted to the following verifier changes:

1. `verify_package.py` will parse the fresh JSON printed by each registered child replay and compare
   it field-for-field with the corresponding sealed JSON artifact. A successful child exit plus a
   stale artifact will no longer pass.
2. The hostile catches currently implemented as source-text substring tests will be replaced by
   structural checks:
   - the returned Jacobi matrix will be parsed as a symbolic `2 x 2` matrix and verified to retain
     both modal projectors, symmetry, determinant, and a generically nonzero cross term;
   - the returned positive mode will be parsed symbolically and its registered factorized residual
     recomputed;
   - omitted-input claims will be checked against executable Python syntax and the functional atoms
     of the parsed scientific outputs, rather than raw source substrings.
3. A hostile package-level mutation will demonstrate that changing a sealed JSON artifact while the
   fresh child replay remains unchanged is caught.
4. A fresh sealed repair-only intake will be built and the exact no-write replay must finish without
   modifying the intake.

The following may not change:

- the coframe, metric, pair surface, affine ray, frequency, curvature, Jacobi, factorization,
  caustic, turn, or descent formulas;
- the 10 named histories, 256 random histories, seed, grids, tolerances, or 2,134 independent
  assertions;
- the bounded premise/status ledger or scientific landing;
- `PRODUCTION_RESULT.json` or `INDEPENDENT_VERIFICATION.json` (required byte-identical to the first
  reviewed intake).

`CATCH_PROOF_RESULT.json` is expected to change because lexical evidence is being replaced by
structural evidence. Its existing numerical deletion/sign/branch controls and all 18 registered
catch names must remain green. The repair cannot self-promote G192; the follow-up reviewer must
return the final grade.
