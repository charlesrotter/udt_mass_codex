# G70 complete-query-owned restriction and channel atlas — audit report

## Landing

`IDENTIFIABILITY_NUMERICALLY_UNRESOLVED`.

Evidence state: `INTERNALLY_VERIFIED__EXTERNAL_REVIEW_PENDING`.

The strict landing is caused by `15/285` preregistered weaker-model cells between the frozen rank
thresholds. A robust bounded sub-result survives: all `45/45` known-source-covariance-plus-carry
cells are `FULL_RANK_OBSERVED`. Current UDT sources own neither the required physical source
covariance nor observation-level access to the carry channel, so this is an algebraic sufficiency
result—not a physical CMB solution.

## Main observations

- The exact frozen universe contains `315` input maps, `15` sensitivity centers, `19` model
  variants, and `285` restriction-rank rows.
- Production positive-definite matrix logs reconstruct within `3.866e-16`; independent SciPy
  `logm/expm` reconstruction is within `1.081e-14`.
- The independent implementation matches every sensitivity matrix within `8.248e-15` relative and
  reproduces all full and two-parameter rank classifications.
- Overall: `46` full, `224` deficient, and `15` unresolved rows.
- Unrestricted source covariance remains exactly compensating; unrestricted covariance plus carry
  is still at most one-channel information.
- Fixed source shape with unknown amplitude never robustly recovers full three-parameter rank.
- Known source covariance without carry distinguishes every two-parameter restriction, but no
  three-parameter row is full.
- Known source covariance including amplitude plus carry is full rank in all `45/45` cells, though
  condition numbers reach `1.3434e5`.
- Two fixed-shape channels with independent unknown amplitudes yield `0/45` full-rank rows.
- No observational anchor, coefficient, ODE solve, fit, eigenspectrum solve, or GPU process was
  used.

## Ownership adjudication

The supplied G68 control query owns a fixed screen and the metric derives `D` and geometric `psi` on
that query. The current evidence does not own a physical CMB query, endpoint, profile, source
covariance, source normalization, scalar-TT carry readout, or polarization source/transport law.
Those remain `OPEN`; the algebra controls remain `CHOSE_CONTROL`.

Accordingly, G70 does not authorize a fit. A successful inverse calculation after supplying a known
source and carry readout would show compatibility under those premises, not derivation of them.

## Four evidence gates

1. **Preregistered:** yes, commit `79a72836`; rectangular-rank and parameter-restriction conventions
   clarified before calculation at `cb5cfae0`.
2. **Full or bounded:** complete over the exact 315-map, 15-center, 19-variant control universe; not
   all profiles, endpoints, sources, queries, or observation laws.
3. **Independent:** separate SciPy-logm implementation reproduces all 285 matrices and classifications
   without importing the production builder; the exact congruence theorem is separately challenged.
   Cold semantic external review remains pending.
4. **Premises:** audited in `OWNERSHIP_LEDGER.tsv`; every helpful physical restriction remains open.

## Authority boundary

This is a local algebraic restriction and ownership atlas. It does not select a physical source,
endpoint, profile, last-scattering surface, TT/TE/EE/BB spectrum, polarization law, coefficient,
action, bootstrap closure, `X_max` value, or signalling rule. The one R04 cell above the full-rank
threshold does not justify promoting that weak model because the family also contains unresolved and
deficient cells.

## Next gate

Submit the package to sealed adversarial review, focusing on matrix-log typing, rectangular rank,
near-threshold cells, source-amplitude profiling, the exact ownership census, and whether R05's
apparent sufficiency is merely a supplied-source tautology. If upheld, the next scientific question
is not a fit: determine whether the complete physical query or global metric completion supplies any
source normalization, endpoint/profile selection, or independently observable carry channel. Do not
invent one to close the inverse problem.
