# G236 fresh adversarial review request

## Proposed landing

```text
DUAL_SNE_RELATIONAL_STATE_CONCORDANCE_LEAD
__TWO_DEOVERLAPPED_PROCESSED_RELEASES_SUPPORT_ONE_RELATIVE_R_OF_PHI_SHAPE
__NO_P1_XMAX_LCDM_DISTANCE_OR_PHYSICAL_PROFILE_FIT
__OBSERVATIONAL_PROCESSING_AND_IMPORTED_TRANSFER_CAVEATS_RETAINED
```

Audit this landing from scratch. Do not continue the research, invent a physical profile, fit a
cosmology, or propose a new UDT law.

## Required checks

1. **Type and algebra.** Conditional on the declared central-static query and imported transparent
   transfer, is
   `m - 10 log10(1+z) = 5 log10 R(phi) + catalog_offset`, with `phi=log(1+z)`, the correct
   relative-state observable for both the Pantheon+ corrected-magnitude and DES distance-modulus
   release columns? Identify any hidden non-additive mismatch between those release types.
2. **Processing ceiling.** Does the package consistently retain the fact that both releases are
   standardized and bias-corrected, with conventional astrophysical and reference-cosmology cargo?
   Does any sentence accidentally promote the result to raw-light, model-independent, predicted,
   native-transfer, or derived-profile evidence?
3. **Sample and overlap.** Verify the frozen cuts, exact counts `768` and `1623`, the 203 removed
   Pantheon+ survey-10 rows, the 148 exact CID overlaps, and the common depth support. Decide whether
   this is a defensible known-object de-overlap while leaving shared calibration systematics open.
4. **Covariance handling.** Check that Pantheon+ uses the correct retained covariance submatrix and
   that the DES subset covariance is obtained by marginalizing the full released precision rather
   than taking its principal submatrix. Verify the independent Schur-complement precision route.
5. **Finite-resolution inference.** Audit the offset/first-knot gauge, spline design, residual degrees
   of freedom, raw chi-square calculation, shape contrast, covariance sum, and frozen conservative
   ceilings. State whether the conclusion is only compatibility at the four registered resolutions.
6. **No hidden physical fit.** Search the implementations and evidence for P1, `X_max`, `tanh`, a
   Lambda-CDM distance curve, optimizer-selected knots, smoothing, monotonicity, a physical profile
   coefficient, or a post-readout angular correction. Distinguish numerical representation from a
   physical ansatz.
7. **Independent evidence.** Inspect the production Cholesky route and independent precision/Schur
   route for shared-code false independence, hardcoded outcomes, circular checks, insufficient
   tolerances, or vacuous hostiles. Recompute bounded load-bearing values if useful without editing
   evidence files.
8. **State/law reframe.** Is it valid to say the releases support a common processed observational
   projection of a relational state while explicitly not deriving the state, its governing law, a
   complete history, or UDT? Is the proposed held-out-channel next gate logically clean?
9. **Evidence contract.** Verify preregistration preceded outcomes, the pre-outcome hostile repair
   changed no observed result, all source hashes are frozen, premise/tests gates passed, and the
   maximum conclusion remains source- and query-bounded.

## Required verdict

Return exactly one primary verdict:

- `G236_ACCEPTED__CONCORDANCE_LEAD_RETAINED`
- `G236_ACCEPTED_WITH_CAVEATS`
- `G236_SCIENTIFIC_REPAIR_REQUIRED`
- `G236_TYPE_DATA_OR_INFERENCE_FAILURE`

List required repairs separately from optional improvements. State explicitly whether any
scientific, statistical, type, data-provenance, or evidence-contract error was found.
