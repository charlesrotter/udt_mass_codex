# Fresh adversarial review request — G100 DES frozen-P1 holdout

Perform a cold, read-only semantic and numerical audit. Do not edit files, continue the research,
fit a new model, or use internet sources. Treat the intake as the entire source universe.

## Required checks

1. Reconstruct the exact primary statistic from the supplied Dovekie table, compact precision, and
   frozen G99 P1 contract. Confirm or refute the reported `chi2`, offset, degrees of freedom, and
   tail probabilities.
2. Audit the DES-only covariance operation. Determine whether production's
   `(W^-1)_KK` and the independent precision Schur complement are the correct marginal-data
   operations and whether simply taking `W_KK` would be wrong.
3. Audit the preregistration chronology and the disclosed `1635 -> 1623` dry-gate repair. Determine
   whether any outcome was visible before the repair and whether the repair changes anything beyond
   source typing.
4. Audit the primary landing `LOW_CHI2_COVARIANCE_OR_EFFECTIVE_DOF_WARNING`. In particular, determine
   whether the reference `chi2_(N-1)` distribution is exact, approximate, or unjustified for this
   released BEAMS-renormalized Hubble diagram. Do not invent an effective degree count.
5. Independently verify the secondary shape result `n_DES`, its `Delta chi2=1` interval, and
   `Delta chi2=2.6827` versus frozen G99. Audit the wording “modest shift, no significant tension.”
6. Audit the no-Lambda-CDM-distance statement. Distinguish direct use of a Lambda-CDM distance from
   inheritance of SALT3/BEAMS/selection/bias-corrected `MU` processing.
7. Hunt for silent fitting freedom, forbidden metadata consumption, covariance double counting,
   row-order errors, use of a secondary to repair the primary, or overstatement of robustness.
8. Audit the maximum conclusion: one frozen conditional curve survives without a large-residual
   rejection, but P1, complete history, native transfer, absolute scale, `X_max`, and UDT generally
   remain unproved.

## Required return

Return exactly one primary landing:

- `PASS`;
- `PASS_WITH_CAVEATS`;
- `BLOCK_NUMERICAL_OR_TYPE_ERROR`;
- `BLOCK_INTERPRETATION_OVERREACH`.

List every load-bearing number independently reconstructed, every caveat that must enter the banked
claim, and the smallest exact repair for any blocker. Do not propose BAO/CMB work or a replacement
cosmology.
