# F01/F02 observer-sky Jacobi controls — audit report

## Verdict

`LOCAL_SKY_MAP_GEOMETRY_DISTINGUISHES_F01_F02_WITH_PROFILE_REMAINDER`.

Final evidence grade: `VERIFIED_WITH_CAVEATS` after a sealed 33-file gpt-5.4 rederivation.

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

## Final evidence status

1. **Preregistered:** yes. `0634b7f8...` is the frozen base; commit `456aeec5` banked the
   preregistration before curvature evaluation. These are distinct, consistent provenance facts.
2. **Full or bounded:** full over the declared F01/F02 local symbolic-jet controls and all exact
   special subloci of the derived cubic coefficient; not a global-profile or all-query census.
3. **Independent:** the partially independent local computational route passes `6/6`, using the
   lowered Riemann formula and a standalone F01 rebuild while sharing the declared metric/query and
   SymPy. A fresh sealed reviewer verified `33/33` hashes and independently rederived every
   load-bearing formula.
4. **Premises:** audited in `PREMISE_LEDGER.tsv`; both geometries and the query are explicit controls.

The `14/14` package checks are artifact/algebra consistency gates and the `12/12` mutations certify
validator sensitivity; neither is presented as independent semantic proof.

## Authority boundary

No CMB prediction, TT power, polarization prediction, physical screen/profile/branch selection,
FD2 restart, source law, local signalling, action, bootstrap result, `X_max` value, or dynamics is
authorized by this return.

## Next gate

The sealed reviewer returned `VERIFIED_WITH_CAVEATS`. A separately preregistered finite-path control
may now be considered only if it supplies an explicit endpoint, complete profile, and branch/caustic
policy without selecting them to force a result.
