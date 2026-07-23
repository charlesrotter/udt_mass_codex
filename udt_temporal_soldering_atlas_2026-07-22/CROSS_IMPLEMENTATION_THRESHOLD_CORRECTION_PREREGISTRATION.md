# Cross-Implementation Threshold Correction — Preregistration

Date: 2026-07-22  
Prior verification-correction commit: `b45d8fb`

## Trigger

The corrected full independent replay reproduced all path signatures and all but two of the `30,175`
Frobenius classes. The exact conflicts are:

1. `B3_R13_3_MB / M04_D / node 0`: independent `NUMERIC_UNCERTAIN_OBSTRUCTION`, production
   `NUMERICALLY_INTEGRABLE_LOCAL`;
2. `B3_V007_MF / M04_D / node 16`: independent `NUMERICALLY_INTEGRABLE_LOCAL`, production
   `NUMERIC_UNCERTAIN_OBSTRUCTION`.

No row disagrees between integrable and nonintegrable. These two threshold disagreements invalidate
an unconditional `719` all-node-integrable path count.

## Frozen two-node refinement

Before inspecting smaller-step values:

1. Freeze the candidate set to the two exact rows above. No other row may be retuned.
2. Recompute each row through both the production and independent analytic routes at
   `h = 1e-4, 5e-5, 2.5e-5, 1.25e-5`.
3. Preserve every obstruction and successive derivative-convergence value.
4. Classify `REFINED_INTEGRABLE` only if both routes put each of their last two obstruction values at
   or below `1e-7`, retain derivative convergence at or below `5e-3`, and agree.
5. Classify `REFINED_NONINTEGRABLE` only if both routes put each of their last two obstruction values
   at or above `1e-5`, retain derivative convergence at or below `5e-3`, and agree.
6. Otherwise classify `CROSS_IMPLEMENTATION_NUMERIC_UNCERTAIN_OBSTRUCTION`.
7. Preserve the original production atlas unchanged. Add a consolidated cross-implementation table
   rather than silently rewriting it.
8. Any path containing a consolidated uncertain row is not counted all-node integrable.
9. The full independent verifier must reproduce the exact two-row disagreement set and fail on any
   additional signature or class disagreement.

The production thresholds, candidate universe, physical premises, and maximum conclusion remain
unchanged.
