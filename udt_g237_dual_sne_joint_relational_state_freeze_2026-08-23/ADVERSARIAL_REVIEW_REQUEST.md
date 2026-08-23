# G237 fresh adversarial review request

## Proposed landing

```text
JOINT_DUAL_SNE_RELATIVE_STATE_FROZEN_WITH_CAVEATS
__BLOCK_DIAGONAL_CROSS_RELEASE_COVARIANCE_CHOSEN
__NO_PROFILE_LAW_PREDICTION_OR_HELDOUT_VALIDATION
```

Audit this landing from scratch. Do not continue the research, propose a profile, fit a cosmology,
or inspect observational outcomes outside the intake.

## Required checks

1. **Type and scope.** Is this correctly typed as a processed observational state assembly under a
   bounded query and imported transfer, rather than a metric solve, physical profile law, or SNe
   prediction?
2. **Estimator.** Derive the two-estimate precision combination and covariance. Confirm that its
   minimized quadratic equals the G236 shape-difference chi-square.
3. **Raw simultaneous GLS.** Recompute one or more resolutions directly from the released rows,
   with one common relative state and two catalog offsets. Audit the Pantheon covariance selection
   and DES omitted-block Schur complement.
4. **Cross-release covariance.** Decide whether zero unknown cross-release covariance after exact-CID
   de-overlap is honestly and consistently marked as a chosen approximation. Identify any sentence
   that overstates independence or uncertainty.
5. **Numerical gates.** Verify counts, degrees of freedom, chi-square identities, all four raw
   adequacy gates, cross-route tolerances, the 56 state rows, and the immutable `K=12` freeze.
6. **Controls.** Audit duplicate-input, release-swap, weak-catalog, and validator-mutation controls
   for circularity, vacuity, or insufficient tolerance.
7. **No hidden law fit.** Search for P1, `X_max`, Lambda-CDM distances, `tanh`, optimizer-selected
   knots, smoothing, monotonicity, post-readout angular corrections, BAO/CMB outcomes, or any
   interpolation promoted to physics.
8. **Evidence contract.** Verify preregistration chronology from the included Git evidence, frozen
   source hashes, implementation independence, premise ledger, and maximum-conclusion wording.
9. **Next gate.** Judge whether carrying the state without refitting into a separately typed held-out
   query is legitimate, while retaining the need for a BAO/CMB source and operator audit.

## Required verdict

Return exactly one primary verdict:

- `G237_ACCEPTED_WITH_CAVEATS__JOINT_STATE_FREEZE_RETAINED`
- `G237_ACCEPTED__JOINT_STATE_FREEZE_RETAINED`
- `G237_SCIENTIFIC_OR_EVIDENCE_REPAIR_REQUIRED`
- `G237_TYPE_DATA_OR_INFERENCE_FAILURE`

List required repairs separately from optional improvements. State explicitly whether any
scientific, statistical, type, source-provenance, scaffolding, or evidence-contract error was found.
