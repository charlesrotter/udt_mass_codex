# G173 fresh adversarial review request

You are a cold external mathematical reviewer. Inspect only the sealed intake. Do not edit files,
continue the research, use the internet, or access any repository or protected package outside the
intake.

## Primary question

Does the declared primary static-spherical metric actually prove
`PULLBACK_EXTENDS__CALIBRATION_ATLAS_NONUNIQUE` for supplied smooth static time-orthogonal families

\[
F(x^0,\sigma)=(x^0,r(\sigma),\gamma(\sigma)),
\]

or has G173 mistaken a coordinate change for physics, overlooked a unique metric calibration, or
misclassified a radial turn as regular?

## Required checks

1. Independently reconstruct

   \[
   h=\operatorname{diag}(-e^{-2\phi},e^{2\phi}v^2+r^2b^2)
   \]

   and classify `v=0,b>0` versus `v=b=0`.
2. Verify the raw readout's affine shift under every regular reparameterization and the invariant
   calibrated formula for a positive weight-one density `m`.
3. Recover G172 exactly from `m_r=abs(v)` on `v!=0` and audit the transition to any non-areal chart.
4. Adversarially determine whether both

   \[
   m_A^2=v^2+r^2b^2,
   \qquad
   m_P^2=v^2+e^{-2\phi}r^2b^2
   \]

   are genuinely constructed from the declared metric/presentation and supplied tangent, transform
   lawfully, recover the pure-radial result, stay positive at a genuine turn, and disagree.
5. Prove or refute the no-go: numerical equality with G172 on every punctured monotone neighborhood
   forces `m=abs(v)` and prevents a positive finite calibration at the turn.
6. Check that calibration nonuniqueness is bounded to the active gates and is not promoted to a
   claim that physical UDT has multiple rulers.
7. Check reversal/telescoping only within one calibration and prevent cross-calibration or
   non-scalar transport promotion.
8. Look for hidden co-presence, `X_max`, G142--G160, fitting, observations, action, source, matter,
   bootstrap, preferred family, or global-completion input.
9. Run `verify_sealed_intake.py` and report its exact output.

## Required landing

Return exactly one:

- `G173_ACCEPTED_WITH_STATED_BOUNDS`
- `G173_REPAIRABLE_SCOPE_OR_ALGEBRA_DEFECT`
- `G173_PRIMARY_LANDING_REJECTED`

State the strongest valid theorem, every caveat, exact file/line references for defects, and whether
the package may be banked as `VERIFIED_WITH_CAVEATS`.
