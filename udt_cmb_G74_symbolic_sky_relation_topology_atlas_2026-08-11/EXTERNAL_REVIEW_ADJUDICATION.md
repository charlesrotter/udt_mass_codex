# G74 external-review adjudication

Date: 2026-08-11

External verdict: `VERIFIED_WITH_CAVEATS`.

Effective evidence state:
`EXTERNALLY_VERIFIED_WITH_METHOD_INDEPENDENCE_AND_PREREG_WORDING_CAVEATS`.

Primary landing: `MIXED_GLOBAL_COMPLETION_CLASSES`.

## What survived adversarial review

The reviewer verified every `34/34` sealed payload hash before reading the scientific sources and
then independently rederived or recomputed the load-bearing result:

- the exact center census is `9` eligible and `12` blocked;
- the tapered and sign-changing rows contain a `y|y|` center witness with exact one-sided
  second-derivative jump `8 epsilon`, while persistent rows have zero jump;
- `C2` is the correct classical gate for the declared connection/curvature/Jacobi atlas;
- endpoint Jacobi rank loss, endpoint grazing, and chart/screen degeneracy remain distinct;
- an everywhere-regular whole-sky `S^2 -> S^2` local diffeomorphism is one-sheeted and has degree
  `+1` or `-1`;
- axisymmetric twist `psi(theta)` drops out of the signed area Jacobian only in the declared class;
- the three F01 optical geometries have constant sectional curvature and exact degree-one sky maps;
- the six persistent controls remain only sampled-regular, not global theorems;
- the twelve blocked profiles were neither repaired nor silently solved.

Its fresh face reconstruction gave degree exactly `1.0` for all nine eligible controls and again
found the worst finest signed-area ratio
`0.5505843446454626` at `G68_F02_AP_P20`. A fresh worst-row production replay reproduced the
`4.922697873263042e-6` step-refinement drift. A fresh direct-Christoffel replay on all `162` level-2
directions of `G68_F02_AM_P20` gave maximum endpoint error
`1.2166590761244587e-6`, null residual `3.774758283725532e-15`, and positive minimum endpoint radial
speed `0.8970684713477242`.

## Caveats and correction ownership

The reviewer found no scientific correction. Three evidence-description corrections apply:

1. The preregistered label “Cartesian Hamiltonian variables” does not describe the implemented
   independent route. The code directly constructs Christoffels and integrates the geodesic
   equation in position/velocity variables.
2. That route is not clean-room independent: it shares the frozen profile loader and icosphere
   helper and uses saved production endpoints as comparison targets. It is nevertheless a valid
   separate-equation numerical cross-check because it does not reuse the production Hamiltonian
   right-hand side.
3. The executable exact checks are mnemonic regression checks. The mathematical proofs reside in
   `EXACT_DERIVATION.md`, the cited standard arguments, and the external rederivation.

The original preregistration and sealed package remain historical evidence. This additions-only
adjudication supersedes only those method/evidence descriptions.

## Status ledger

- `DERIVED`: F01 degree-one result; center `C2` obstruction; endpoint factorization; whole-sphere
  covering theorem; axisymmetric Jacobian and its exact scope.
- `OBSERVED`: the six persistent control maps are sampled regular and degree one on the registered
  meshes and step refinements.
- `CHOSE_QUERY_CONTROL`: null generators, observer event, comparison sphere, frozen 21-profile
  universe, meshes, and integration controls.
- `CONDITIONAL`: every sky map is conditional on its supplied profile/query and symbolic positive
  scale.
- `OPEN`: physical CMB metric, source, endpoint, scale, branch combination, spectrum,
  polarization, `X_max`, bootstrap law, action, and matter source.

## Maximum justified conclusion

Exactly three F01 controls are exact degree-one whole-sky diffeomorphisms; six persistent controls
are `OBSERVED_SAMPLED_REGULAR_NOT_GLOBAL_PROOF`; twelve tapered/sign-changing controls are
`BLOCKED_SUPPLIED_PROFILE_NOT_C2_AT_CENTER`. This is the complete classification of the exact
frozen control universe under the declared query, not a physical CMB solution or a census of all
UDT metrics.

## Next gate

Derive or identify a globally center-regular complete-metric profile family before asking it for a
physical CMB pattern. Then compute its global angular-scale response, including angular transport,
across broad nonzero source ensembles. Do not fit peaks, select a universe scale, activate
bootstrap, or infer a source law at this gate.

