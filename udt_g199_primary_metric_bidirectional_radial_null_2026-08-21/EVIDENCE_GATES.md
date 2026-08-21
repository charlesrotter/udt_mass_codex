# G199 evidence gates

Date: 2026-08-21

## Preregistration

`MAP.md` and `PREREGISTRATION.md` were committed and pushed at `1514ed99` before the confirmatory
scripts or result artifacts were created.

## Bounded completeness

The exact calculation covers both normalized future radial null germs for arbitrary local smooth
positive `f`, arbitrary `f'` and `f''`, and every regular event with `r>0` in the declared primary
static-spherical metric.  It does not claim nonradial or generalized-metric completeness.

## Independent verification

- production: direct SymPy inverse metric, Christoffels, Riemann tensor, screen contraction, and
  Jacobi residual; 65/65 assertions;
- independent: standalone standard-library exact-`Fraction` reconstruction from metric two-jets;
  2,000/2,000 nonflat cases, 60,000 assertions, and 2,000 opposite-sign comparisons;
- the independent verifier imports no production module and reads no production artifact;
- hostile catches: 9/9.

## Premise audit

The primary metric is pinned only within the declared static-spherical slice.  The profile `f(r)`
is supplied.  The pair/query and affine calibration are supplied.  Completed-pair Dual Reciprocity
retains its `WORKING_FOUNDATIONAL_CLARIFICATION` grade.  No G191--G198 chiral coframe term,
observation, transfer, source, action, matter, `X_max`, or protected work enters the derivation.

## Mechanical gates

- `verify_package.py`: PASS; 12 source hashes, 65 production assertions, 60,000 independent
  assertions, 2,000 nonflat cases, nine hostile catches, no-write replay.
- `python3 verify_current_scientific_premises.py`: PASS on the 183-row exact registry.
- repository test suite: 114 passed, one registered xfail.
- `git diff --check`: PASS.
- protected local work remained untracked and untouched; only the G199 package and current startup,
  registry, verifier, and test surfaces are staged for banking.
