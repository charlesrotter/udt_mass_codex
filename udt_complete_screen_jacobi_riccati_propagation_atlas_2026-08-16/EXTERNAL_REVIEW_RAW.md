# External adversarial review — raw return

Reviewer: external Codex `gpt-5.4`, high reasoning, ephemeral, web disabled, sealed read-only intake
Intake: `/tmp/udt_g108_screen_review_pd6t652_`
`REVIEW_SCOPE.json` SHA-256: `27885911911e040da252c0cec10206b9c30b1c3de794e2340922078865eccf0b`
Date: 2026-08-16

## Landing

`DERIVATION_VALID_CONDITIONALLY__TYPE_TIE_EXPLICIT`

I independently re-derived the load-bearing identities behind `EXACT_DERIVATION.md`:
`sqrt(det(W^T W))=|det W|`, `d_lambda log|det W|=tr(Wdot W^-1)`, the
depth-reparameterized Jacobi/Riccati system, and `a_eff=a` for
`W=e^(a delta)R(b delta)W0`. I found no factor, sign, or unit error on the declared regular stratum.

## Findings

1. The sealed evidence trail has one scope-packaging defect. `REVIEW_SCOPE.json` does not declare
   `build_review_intake.py`, but `verify_package.py` and `PACKAGE_VERIFICATION_RESULT.json` treat it
   as a required present file. Repair: either add that file to the sealed intake or remove it from
   the verifier's required set and regenerate the package-verification result. Bounded conclusion
   change: no, but the current sealed `all_required_files_present` claim is not fully auditable from
   the declared intake.

2. The core type distinction is mathematically handled, but the summary layer should restate it
   more sharply. The source chain correctly says `Y,Z` belong to the supplied pair/query rather
   than the metric alone, and the main derivation makes the decisive conditional tie explicit. But
   `AUDIT_REPORT.md` compresses this into prose that can be read as if `Q(SY+Z)` is automatically
   the Jacobi map. Repair: in the report and landing, say “when the supplied query identifies this
   same product block with the physical Jacobi screen map.” Bounded conclusion change: no.

3. The package correctly denies that constant determinant rate alone recovers the whole G107
   matrix family, but it should state the exact missing condition. Repair: add the precise criterion
   that full-family recovery needs `K=W_,delta W^-1=aI+b epsilon` in an oriented orthonormal screen
   frame, equivalently vanishing symmetric trace-free part plus constant isotropic trace. Without
   that, only the determinant character is recovered. Bounded conclusion change: no.

## Maximum conclusion

On the regular local rank-two stratum, and only when the supplied observer query ties the same
complete pair-screen block `W=Q(SY+Z)` to the physical Jacobi screen map, the package's rate
identity is valid:

`a_eff=(1/2)d_delta log A_perp=tr(Wdot W^-1)/(2 delta_dot)`.

The G107 constant `a` is recovered only as the constant isotropic no-shear special subfamily, not
as a generic consequence of determinant growth alone. The result remains conditional on supplied
metric history, query, branch, initial screen data, and monotone `delta(lambda)`, with failure at
coincidence/caustic/nonmonotone-depth/branch-change strata. I found no smuggled BAO/CMB/SNe,
`X_max`, source, action, matter, bootstrap, or signalling conclusion.
