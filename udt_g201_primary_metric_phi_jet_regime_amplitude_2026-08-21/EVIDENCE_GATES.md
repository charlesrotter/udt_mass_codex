# G201 evidence gates

Date: 2026-08-21

## Preregistration

`MAP.md` and `PREREGISTRATION.md` were committed and pushed at `28d48506` before confirmatory
implementation.

## Bounded completeness

The exact theorem covers the local two-mode amplitude of every smooth positive primary-metric
second jet at a regular normalized nonradial source.  It classifies local cancellation and one
exact integrated zero-tide family.  It does not select a global history or classify every finite
path, turning point, cut, focal point, or completion.

## Independent verification

- production: exact SymPy metric-to-phi substitution and analytic controls, 20/20 assertions;
- independent: standard-library exact-`Fraction` metric-jet reconstruction, 23,606 assertions;
- 10,000 arbitrary jets, 1,000 arbitrary-phi cancellations, and 400 exact smooth-family controls;
- both signs of the smooth-family constant covered;
- no production import or artifact read;
- hostile catches: 9/9.

## Premise audit

The primary metric is pinned only within the declared static-spherical slice.  `phi(r)` and its
jets remain supplied history.  The incidence is a supplied query.  Reciprocal contrast is only an
algebraic diagnostic, not a new physical score.  No profile fit, transfer, `X_max`, source, action,
matter, bootstrap, or protected work enters.

## Mechanical gates

- package replay: PASS; nine source hashes, 20 symbolic assertions, 23,606 independent assertions,
  10,000 arbitrary jets, 1,000 cancellation cases, 400 smooth-family controls, nine catches;
- premise verifier: PASS on the 185-row exact registry;
- repository tests: 116 passed, one registered xfail;
- diff check: PASS;
- protected local work remains untouched.
