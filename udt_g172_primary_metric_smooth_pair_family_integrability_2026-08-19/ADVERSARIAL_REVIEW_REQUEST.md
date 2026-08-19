# G172 fresh adversarial review request

You are a cold external mathematical reviewer. Inspect only the sealed intake. Do not edit files,
continue the research, use the internet, or access any repository or protected package outside the
intake.

## Primary question

Does the declared primary static-spherical metric, together with the supplied smooth family

\[
F(x^0,r)=(x^0,r,\gamma(r)),
\]

actually prove `SMOOTH_FAMILY_CLOSURE` on the preregistered static, time-orthogonal,
monotone-areal class, or has the package silently assumed a preferred pair family, discarded
angular/mixing information, or widened a local chart result?

## Required checks

1. Reconstruct the pullback independently and verify

   \[
   h=\operatorname{diag}(-e^{-2\phi},e^{2\phi}+r^2a^2),
   \quad
   W=1+r^2e^{-2\phi}a^2,
   \quad
   \Phi=\phi+\tfrac14\log W.
   \]

2. Verify the conditional frame ratio, radial limit, derivative, reversal, and same-family
   telescoping.
3. Adversarially test the integrability claim both from the explicit immersion and from
   \([\partial_{x^0},\partial_r+\gamma'(r)]=0\).
4. Decide whether arbitrary smooth nonnegative `a2(r)` is legitimately characterized without
   selecting a fitted angular curve.
5. Audit reparameterization and the exact failure of areal-radius calibration at `dr/dsigma=0`.
6. Check whether the one-sided center limit has been kept distinct from smooth-center completion.
7. Look for hidden dependence on co-presence, `X_max`, G142--G160, fitting, observations, matter,
   source, action, bootstrap, or a preferred physical path.
8. Determine whether scalar telescoping was improperly promoted to non-scalar transport closure.
9. Run `verify_sealed_intake.py` inside the sealed package and report its exact output.

## Required landing

Return exactly one primary grade:

- `G172_ACCEPTED_WITH_STATED_BOUNDS`
- `G172_REPAIRABLE_SCOPE_OR_ALGEBRA_DEFECT`
- `G172_PRIMARY_LANDING_REJECTED`

State the strongest valid theorem, every material caveat, exact file/line references for defects,
and whether the package may be banked as `VERIFIED_WITH_CAVEATS`.
