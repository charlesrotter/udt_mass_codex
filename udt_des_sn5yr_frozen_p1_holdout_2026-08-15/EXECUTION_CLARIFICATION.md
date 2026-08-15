# Pre-likelihood execution clarification

Date: 2026-08-15

Status: committed before any DES model residual or likelihood was evaluated

After the original preregistration was committed and pushed, the official README, NPZ keys/shapes,
table header, and first five public table rows were inspected solely to determine the parser. No
P1 prediction, residual, chi-square, aggregate magnitude statistic, or shape optimization was
computed.

The following previously implicit implementation choices are fixed now:

1. The secondary DES shape diagnostic uses `s=1/n` on the exact inherited M3 interval
   `1e-4 <= s <= 40`. This is a diagnostic domain, not a prior or primary fitting freedom.
2. The descriptive residual atlas uses exactly ten stable equal-count bins after sorting by the
   selected redshift. It reports counts, redshift bounds, arithmetic mean, and RMS only; it is not
   an acceptance filter and supplies no additional verdict.
3. The production DES marginal covariance is obtained by inverting the full released precision and
   taking the retained covariance block. The independent route uses the algebraically distinct
   precision Schur complement over excluded rows.
4. The primary model uses the numerically stable `expm1/log1p` implementation of the frozen P1
   formula. The independent route uses the direct-power form.
5. No overlap-pruned subset will be constructed in G100. The primary sample is the complete
   `IDSURVEY == 10` subset and is described as substantially independent, never event-disjoint.

These choices cannot be changed after the primary run.
