# External cold review — raw return

Model: `gpt-5.4`  
Mode: sealed 50-file read-only intake; network search disabled  
Date: 2026-08-11

## Findings

1. The sealed-intake provenance replay is broken as shipped. `SOURCE_MANIFEST.tsv` records
   root-relative paths, but `verify_preregistration.py` and `verify_package.py` resolve them directly
   under `HERE.parent`, so both fail immediately on `CURRENT_SCIENTIFIC_PREMISES.tsv`. I replayed the
   22 hashes manually under the sealed `sources/` transport layout and all 22 matched, so this is a
   packaging/provenance defect, not a scientific formula defect.
2. The catch-proof runner is not read-only replayable in this intake. `run_catch_proofs.py` rewrites
   tracked outputs and fails on the read-only filesystem. The checked-in catch-proof result can still
   be inspected, but the package overstates rerunnability inside a sealed cold review.

## Primary landing

`MULTIPLE_GEOMETRIC_SURVIVOR_FAMILIES`.

## Reconstructed load-bearing checks

- The production solver does solve the stated Levi-Civita geodesic and transport equations, and its
  two coframe families match the frozen derivations: the R17 implementation matches the R17
  foliation and path-connection formulas; the time-live block coframe matches the complete time-live
  orchestra derivation.
- `phi_pair=phi` is correctly typed on R17. The exact source gives `E=span(T,Z)`, leaf metric `h`,
  `det(h)=-1`, and `phi_pair=(1/4)log[(-det h)/h00^2]=phi`. The solver's
  `J=(partial_t,2 partial_psi)` pullback is consistent with that typing.
- Endpoint scalar descent and nontrivial holonomy coexist without contradiction because they are
  different typed objects: endpoint coboundary on the pair leaf versus path-labelled Levi-Civita
  and normal-bundle transport on supplied loops.
- I independently recomputed one R17 witness without importing the production solver: `R17_0_Z`
  gave atlas defect `3.7125e-16`, `phi_pair` identity defect `2.78e-17`, timelike endpoint
  `(0.5294790635590257, 1.2197350654971326, 0.3556112552446236, 0.41980720426753343)`,
  `dexp_min_sv=0.349330467...`, Hopf-loop `||P-I||=1.419905283...`, and normal angle
  `7.149032687...`, matching the frozen rows to about `1e-12`.
- I independently recomputed one time-live witness without importing the production solver: `TL_Z`
  gave atlas defect `2.4851e-16`, timelike endpoint
  `(0.5593452471552482, -0.17109245548196195, 0.2817816180624038, -0.12527600117120885)`,
  `dexp_min_sv=0.381822959...`, and `TX_RECTANGLE ||P-I||=0.00489410054...`, matching the
  frozen rows to about `1e-12`.
- The independent RK4/finite-difference implementation is numerically independent enough for the
  survivor classifications. It does not import the production solver and uses different derivative
  and integrator choices. It reproduces all `56/56` classes with maxima `1.08e-11`, `6.63e-10`, and
  `2.10e-13`. It is not a second source-derivation pipeline, so it certifies numerical
  regularity/classification, not independent ownership typing.
- No reported survivor depends on imported dynamics, source, action, matter, bootstrap tuning,
  `c_E`, or `X_max`. I found no such quantities entering the solver.
- The global/local and stationary/time-live labels are accurate as stated: R17 is
  `GLOBAL_RxS3_SOURCE_OWNED`; time-live is `LOCAL_OFFSHELL_ONLY`; propagator rows explicitly avoid
  dynamical-stability inference.

## Corrections

- Correct the package claim from “sealed-intake verifier passes as shipped” to “sealed-intake source
  hashes pass after resolving manifest paths under `sources/`.”
- Correct the package claim from “catch proofs rerun here” to “checked-in catch-proof outputs report
  `23/23 PASS`; rerun is blocked in read-only intake.”
- Do not weaken the scientific scope beyond its current bounded qualifiers; do not strengthen it
  beyond them either.

## Maximum justified conclusion

Within the 14 preregistered witnesses, declared paths, and affine endpoint `s=0.4`, both endpoint
reciprocal-depth and path-labelled transport channels remain regular geometric survivors, and R17
additionally shows nonzero normal-bundle holonomy. This is bounded geometric coexistence only, not a
physical selector, native dynamics result, or stability claim.

## Smallest prior joint

Before the proposed coupled-channel readout audit, the smaller prior joint is procedural: fix the
sealed-source replay contract so manifest hashes and catch proofs rerun read-only inside the intake.
The next scientific question is secondary to that provenance/reproducibility repair.
