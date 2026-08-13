# R2 outcome-blind control-summary preregistration

Date: 2026-08-13
Status: `PREREGISTERED_AFTER_ATLAS_VERIFICATION__BEFORE_COMPLETE_CONTROL_SUMMARY`

R2 has passed the corrected independent verifier. The complete control tables have not yet been
aggregated or ranked. This bounded summary is frozen before that aggregation.

## Question

How large are the already preregistered random-density, weight-lane, and North/South differences
across the complete R2 atlas, and what neutral numerical vocabulary describes the central curves?

## Frozen summaries

For both `max_abs_difference` and `rms_difference`, report count, minimum, quartiles, median, 90th
and 95th percentiles, and maximum:

- overall for each of `RANDOM_DENSITY`, `WEIGHT_LANE`, and `CAP`;
- random-density differences grouped separately by ratio pair, sample, and factor;
- weight-lane differences grouped separately by lane pair, sample, and factor;
- cap differences grouped separately by sample, factor, and weight lane.

For each matched random-density query, also record whether the `10x-20x` RMS difference is no larger
than the `5x-20x` RMS difference. Report only the complete count and fraction overall and grouped
separately by sample, factor, cap, and lane. This is a convergence diagnostic, not a pass/fail gate.

For the descriptor atlas, report count, finite-value status, degeneracy counts, and the same fixed
quantiles for RMS, total variation, first- and second-difference RMS, strict maximum count, strict
minimum count, plateau count, and zero-crossing count. Report overall and separately by sample and
factor.

## Forbidden returns

Do not rank or select individual curves, extrema, DCT coefficients, lags, angular positions, shells,
redshifts, caps, weights, or random ratios. Do not infer a preferred period, oscillation, physical
scale, BAO mechanism, UDT mechanism, CMB relation, `X_max`, or statistical significance. North/South
and other raw differences have no significance interpretation until R3 supplies data-only
covariance or replication controls.

Maximum conclusion: a verified descriptive map of numerical and control dependence in the R2
central-pattern atlas.
