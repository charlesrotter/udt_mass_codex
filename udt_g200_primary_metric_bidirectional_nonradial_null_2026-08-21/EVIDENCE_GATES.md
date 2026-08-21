# G200 evidence gates

Date: 2026-08-21

## Preregistration

`MAP.md` and `PREREGISTRATION.md` were committed and pushed at `7b92835e` before confirmatory
implementation or result artifacts were created.

## Bounded completeness

The exact calculation covers both reversed equatorial nonradial null germs for arbitrary smooth
positive local `f`, arbitrary derivatives through `f'''`, and every regular event with `r>0` and
real nonzero radial velocity.  It proves the same-event law and vertex series through the first
possible split at fourth order.  It does not claim complete long-path, turning, cut, focal, or
global completeness.

## Independent verification

- production: direct SymPy inverse metric, Christoffels, Riemann tensor, geodesics, quotient
  screens, tidal contractions, and branchwise Jacobi series; 64/64 assertions;
- independent: standalone standard-library exact-`Fraction` radial-dual reconstruction from metric
  coordinate third jets; 2,000 cases and 38,160 assertions;
- all 2,000 independent cases had at least one nonzero tidal-gradient mode;
- 40 exact flat controls;
- the independent verifier imports no production module and reads no production artifact;
- hostile catches: 9/9.

## Premise audit

The primary metric is pinned only within the declared static-spherical slice.  The local profile
jet is supplied.  The pair query and affine calibration are supplied.  Completed-pair Dual
Reciprocity retains its `WORKING_FOUNDATIONAL_CLARIFICATION` grade.  No G191--G198 chiral coframe,
fit, observation, transfer, source, action, matter, `X_max`, or protected work enters.

## Mechanical gates

- `verify_package.py`: PASS; nine source hashes, 64 production assertions, 38,160 independent
  assertions, 2,000 exact third-jet cases, 40 flat controls, nine hostile catches, no-write replay;
- `python3 verify_current_scientific_premises.py`: PASS on the 184-row exact registry;
- repository test suite: 115 passed, one registered xfail;
- `git diff --check`: PASS;
- protected local work remains untracked and untouched.
