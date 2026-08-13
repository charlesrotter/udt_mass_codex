# R2 verifier correction preregistration

Date: 2026-08-13
Status: `PREREGISTERED_AFTER_GATE_FAILURE__IMPLEMENTATION_REPAIR_ONLY`

## Observed failure

The frozen `verify_r2.py` completed the saved-atlas reconstruction and the nine full-catalog
TreeCorr component anchors, then stopped in `verify_brute_anchors` at the compact weighted-sum
tolerance. No `R2_VERIFICATION_RESULT.json` was written.

All twelve compact integer pair-count vectors agreed exactly between direct all-pairs counting and
TreeCorr. The four weighted CMASS cases differed by approximately `5.4e-10` through `5.8e-9`
relative, exceeding the compact `5e-12` tolerance. The eight remaining cases agreed exactly.

## Diagnosis fixed before rerun

The R2 preregistration requires the compact direct calculation to certify the primary pair result.
The verifier implementation instead compared the direct calculation only with TreeCorr. A
three-way diagnostic found:

- direct versus primary Corrfunc: exact integer counts in all twelve cases; maximum weighted
  relative difference `5.758092004939054e-13` and maximum absolute difference
  `5.7838178690872155e-12`;
- direct versus TreeCorr: exact integer counts, but maximum weighted relative difference
  `5.781399141702682e-9` in the compact CMASS cases;
- unit-weight LOWZ and random-random cases were exact across all methods.

Thus the production engine satisfies the frozen compact tolerance. The failure is a type error in
the verifier: it applied the primary/direct tolerance to the independent TreeCorr accumulator.

## Frozen repair

Before the corrected rerun:

1. keep the full-catalog TreeCorr anchors unchanged, including their frozen `5e-9` relative or
   `1e-7` absolute weighted tolerance;
2. change only the compact anchor comparator from direct-versus-TreeCorr to
   direct-versus-primary-Corrfunc;
3. keep the compact exact integer-count and `5e-12` relative or `1e-10` absolute weighted gates
   unchanged;
4. retain all twelve compact cases and all other verifier checks unchanged;
5. report this post-failure implementation repair in the final evidence grade.

This correction cannot promote R2 beyond `VERIFIED-WITH-CAVEATS`. It does not alter any production
pair count, curve, descriptor, tolerance, catalog selection, or scientific conclusion.
