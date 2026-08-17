# Fresh adversarial review request — G135 projective pair separation

Date: 2026-08-17

Mode: read-only, zero-context, adversarial. Do not continue the research or edit files.

## Question

Does G135 correctly derive a canonical projective reciprocal coordinate from a supplied complete
calibrated pair metric, while correctly refusing to promote it to physical separation or a numerical
`X_max` without an additional owned statement?

## Required checks

1. Reconstruct the complete type chain

   ```text
   B,Q,S,Y,Z -> h -> T,L,beta -> phi_pair,q -> chi.
   ```

   Confirm that no angular/mixing channel is attached after terminal readout.
2. Independently verify

   ```text
   chi=(L-T)/(L+T)=(1-q)/(1+q)=tanh(phi_pair)
   ```

   and the sum/contrast basis conjugation of `D(phi)`.
3. Test whether `chi` is genuinely basis/covariance meaningful given the fixed physical
   clock/ruler calibration, or merely a coordinate artifact. Distinguish abstract channel exchange
   from a physical causal transformation.
4. Re-solve the anchored first-degree fractional-linear classification without assuming the answer.
   State exactly which anchors and class are load-bearing.
5. Attack unrestricted uniqueness. Verify the smooth counterfamilies, including the neutral-slope
   matched family and exact `-45/29728` witness.
6. Verify the fractional-linear composition law and the distinction between signed ordered
   comparison and nonnegative separation magnitude.
7. Attack the physical-distance claim using the `h` versus `4h` countermodel. Decide whether the
   countermodel merely separates projective position from proper length or also defeats the proposed
   constitutive interpretation.
8. Check that observed `c_E` does not dimensionally or algebraically fix `X_max`.
9. Check the historical regrade: strong local CSN is inactive; common scale must remain retained even
   though `chi` is scale-neutral; the full orchestra now precedes the readout.
10. Independently run or reconstruct the production, independent, catch-proof, source-hash, and
    premise gates. Hunt shared-code, tautology, output-only, and loose-claim false passes.

## Required landing

Return exactly one primary verdict:

- `VERIFIED_WITH_CAVEATS__BOUNDED_LANDING_SOUND`;
- `REPAIR_REQUIRED__LANDING_SURVIVES`;
- `REFUTED__PROJECTIVE_DERIVATION_FAILS`;
- `REFUTED__PHYSICAL_PROMOTION_PRESENT`;
- or another precisely defined result.

State separately:

- what is `DERIVED`;
- what is only `DERIVED_IN_CLASS`;
- what is `CONDITIONAL`;
- what remains `OPEN`;
- whether the proposed “positional means anchored projective readout” clause is already entailed by
  the active founding sources, a clarification requiring owner adoption, or a genuinely new premise.

Do not derive an action, source, bootstrap law, matter model, observation, signal law, metric history,
or numerical `X_max`.
