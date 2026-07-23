# Independent Verification Numeric-Comparison Correction

Date: 2026-07-22  
Original preregistration commits: `7573136`, `681d5d5`

## Trigger

The first full independent-verifier run stopped after independently recomputing the atlas because
its auxiliary raw-value comparison used a fixed relative tolerance of `2e-8`. The first retained
difference was a derivative-convergence value of `3.152875216508865e-08` versus
`8.513893137697936e-09`, a difference of `2.3014859027390716e-08`. The independently assigned block
signature and Frobenius class agreed. The production derivative-classification gate is `5e-3`.

This is a verifier-tolerance defect, not authority to change a source, candidate, stencil, physical
premise, production output, or classification threshold.

## Frozen correction

Before editing the verifier:

1. Preserve exact equality for every independently recomputed block signature and Frobenius class.
2. Preserve complete independent coverage of all `30,175` complement-node rows.
3. Compare the three auxiliary floating values with a separately named relative tolerance of
   `1e-6`.
4. Report the maximum observed cross-implementation floating difference.
5. Keep the production thresholds unchanged: derivative convergence `5e-3`, integrable obstruction
   `1e-7`, and nonintegrable obstruction `1e-5`.
6. Fail if either implementation places a row in a different threshold class, irrespective of raw
   numeric proximity.
7. Preserve the first failed transcript and disclose this correction in the final report.

The maximum allowed conclusion is unchanged.
