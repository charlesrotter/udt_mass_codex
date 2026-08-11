# F01/F02 observer-sky Jacobi controls — audit report

## Verdict

`LOCAL_SKY_MAP_GEOMETRY_DISTINGUISHES_F01_F02_WITH_PROFILE_REMAINDER`.

On one identical preregistered observer-sky query, F01 has zero radial screen tidal matrix for
arbitrary regular local `A(r)`. F02 has the exact local matrix `diag(0,tau)`, with `tau` determined
by `A,h` and their first two radial derivatives. The antisymmetric/rotation channel vanishes at
this order. Generic weak mixing enters at quadratic order.

## What was accomplished

- The observer-sky projection is now a typed metric/Jacobi object rather than an unexplained affine
  conversion.
- F01 and F02 are demonstrably different on the same query without an eigensolve or data fit.
- F01 integrates conditionally to `D=sI` along a regular radial branch.
- F02 supplies a directional, non-affine correction, but its finite value remains profile- and
  endpoint-dependent.
- The old scale freedom has the correct geometric home but is not numerically closed. The old
  ladder offset remains boundary/operator-owned and is not produced by screen geometry.

## Evidence status before external review

1. **Preregistered:** yes, commit `456aeec5`, before curvature evaluation.
2. **Full or bounded:** full over the declared F01/F02 local symbolic-jet controls and all exact
   special subloci of the derived cubic coefficient; not a global-profile or all-query census.
3. **Independent:** local independent implementation passes `6/6`, using the lowered Riemann formula
   and a standalone F01 rebuild. Fresh external semantic review remains required before banking a
   verified scientific verdict.
4. **Premises:** audited in `PREMISE_LEDGER.tsv`; both geometries and the query are explicit controls.

Current evidence grade: `LEAD_INDEPENDENTLY_REPRODUCED_PENDING_ADVERSARIAL_REVIEW`.

## Authority boundary

No CMB prediction, TT power, polarization prediction, physical screen/profile/branch selection,
FD2 restart, source law, local signalling, action, bootstrap result, `X_max` value, or dynamics is
authorized by this return.

## Next gate

Obtain a fresh adversarial review of the exact query typing, curvature contraction, F01 global
extension, F02 formula, weak-mixing order, and projection-freedom ownership. Only after acceptance
should a separately preregistered finite-path control be considered.
