# Cold external review dispatch — R17 depth / normal-holonomy joint

Audit this package and only the exact sources in `SOURCE_MANIFEST.tsv` as a read-only adversary.
Reconstruct the load-bearing mathematics rather than trusting the stated ruling or scripts.

## Required questions

1. **Global type.** Verify that the globally correct target is the product of the additive
   reciprocal-line groupoid with the oriented normal-isometry groupoid, locally represented by
   `R x SO(2)` only after endpoint frames are chosen. Reject any silent identification of different
   endpoint fibers with one fixed matrix group.
2. **Composition.** Starting from `delta_K=phi(q)-phi(p)` and metric-projected normal parallel
   transport `U_gamma:H_p->H_q`, verify composition, inversion, endpoint gauge covariance, and the
   conformal screen family `C_w=exp(w delta_K)U_gamma` for all real `w`.
3. **Complete-coframe weight.** Independently check that
   `q_H=exp(2 lambda phi)(sigma1^2+sigma2^2)` fixes `w=-lambda` on inherited reference-vector
   coefficients and `w=+lambda` on the variance-dual reference-coframe representation. State any
   transpose/inverse convention needed. Determine whether this is only a screen representation or
   can defensibly be promoted to the full observer arrow.
4. **Open-path gauge theorem.** Test whether independent endpoint `SO(2)` frame changes act
   transitively on an unframed open-path rotation, so that no nonconstant order-zero real scalar can
   depend on `U_gamma`. Test loops and two-path relative holonomy separately, including the optional
   `O(2)` quotient.
5. **Character theorem.** Classify all continuous real characters factoring through the local
   order-zero model group `R x SO(2)` without assuming angle-linearity. Verify that reciprocal
   normalization leaves only `delta_K`. Do not inflate this into a classification of arbitrary
   path-groupoid cocycles, endpoint coboundaries, or derivative-dependent line integrals.
6. **Extension law.** Verify that every continuous action `R->Aut(SO(2))` is trivial, and identify
   precisely what changes if the discrete orientation-reversal channel is retained.
7. **Independence.** Reproduce the C08 control `delta(loop)=0`, `B_0(1)=4097/4096`, and
   `F23=-4097/2048`, and decide whether it suffices to show that reciprocal depth does not determine
   angular holonomy.
8. **Higher-jet scope.** Verify the elementary fact that a supplied one-form has an additive line
   integral. Audit the `alpha=I dphi` construction and the rectangle control. The rectangle is
   explicitly **not** an R17 solution witness. Determine whether the supplied stationary
   cohomogeneity-one R17 geometry itself owns any endpoint-frame-invariant non-exact scalar one-form
   independent of `dphi`, or whether that remains open.
9. **Ownership.** Hunt any manifest-backed equation selecting a path, a physical non-isometric
   observer arrow, a branch, `lambda`, a higher-jet one-form, or a universal mixed-geometry
   `c_eff`. Do not infer selection from a representation identity or a numerical witness.
10. Hunt circular verification, hidden trivializations, orientation mistakes, variance-sign errors,
    group-versus-groupoid category errors, and claims exceeding stationary regular R17.

Return exactly one primary verdict: `VERIFIED_AS_STATED`, `VERIFIED_WITH_CORRECTIONS`,
`GLOBAL_TYPE_FAILURE`, `COMPOSITION_FAILURE`, `COFRAME_WEIGHT_FAILURE`,
`GAUGE_OR_CHARACTER_FAILURE`, `HIGHER_JET_SCOPE_FAILURE`, `OWNERSHIP_FAILURE`, or a more precise
landing. State the maximum defensible claim and every remaining open seam.

Do not edit files, continue the research, inspect anything outside the sealed intake, or inspect
the protected curvature-atlas contents.
