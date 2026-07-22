# Preregistered Bivector Tolerance Correction

Date: 2026-07-21

The preserved `FRESH_ADVERSARIAL_FINAL_REVIEW.md` failed the package because the production
bivector complementary-projector pairing check retained one literal `1e-7` acceptance threshold.
The controlling preregistered projector tolerance is `1e-9`; the independent verifier already uses
that value. The saved atlas contains zero candidate curvature-eigenbivector planes, so the defect is
outcome-silent, but the implementation contract still fails.

This correction is committed before changing the classifier. Exactly one scientific-code mutation
is authorized: replace that literal complementary-pair threshold with `RANK_TOL`. No family,
configuration, output row, uncertainty band, eigenvalue clustering rule, premise, or maximum
conclusion may be changed.

The previous counts are observations to retest, not targets. The full builder, independent verifier,
manifest, and repository gates must run again in order. A new fresh read-only adversarial review is
required before final banking.
