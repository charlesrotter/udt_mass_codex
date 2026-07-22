# Third fresh-review adjudication

Date: 2026-07-22

The third fresh `FAIL` is accepted in full. It independently reproduced the scientific results and
retained the registered maximum and `LEAD`, but rejected the second correction's claim of
fail-closed package certification.

| blocker | repair | result |
|---|---|---|
| coordinated point-census redistribution survived | require the exact `67,396 / 33 / 27` mutually exclusive census and `60` uncertainty-bearing total | coordinated redistribution and negative-count mutations rejected |
| coordinated edge split and fabricated reason survived | require exactly `63,438` eligible plus `50` skipped, with the sole registered skip reason | the review's `1 + 63,487` fabricated split is rejected |
| negative numerical residuals survived | require every residual finite and nonnegative, within its registered tolerance | negative-residual mutation rejected |
| non-finite determinant not excluded | require finite positive sampled minimum absolute determinant | infinite-determinant mutation rejected |
| fabricated seed source path survived | require the exact frozen repository source path as well as its hash | source-path mutation rejected |
| package verifier inherited flexible accounting | independently lock the same point/edge census in `verify_package.py` | coordinated mutation fails at both validation layers |

The corrected full replay reproduces the unchanged scientific result and now exercises 29/29
corrupted-record catches. No atlas row, scientific premise, status, or maximum conclusion changed.
