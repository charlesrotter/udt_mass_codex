# G277 R2B covariance-handling preregistration

Date: 2026-08-26

## Triggered preregistered failure

R2 required raw Pantheon+ covariance symmetry to absolute tolerance `1e-12`. The observed raw
maximum transpose mismatch is `3.0000000000038676e-08`, so that gate is **FAIL**. The threshold is
not changed and the failure remains part of the evidence.

No fit, scale, residual, or covariance-weighted alternative result was inspected before this R2B
contract.

## Bounded numerical question

The release labels the file as a covariance and the official likelihood consumes it as one. Test
whether the structural scale/absolute-magnitude rank is robust to the three standard
finite-serialization interpretations:

1. `C_mean = (C + C.T)/2`;
2. `C_lower`, reflecting the raw lower triangle across the diagonal;
3. `C_upper`, reflecting the raw upper triangle across the diagonal.

These are numerical representations of the supplied covariance, not new physical premises.

## Frozen gates

For the exact official row mask `(zHD > 0.01) OR IS_CALIBRATOR` and actual design columns
`[log_scale, shared_absolute_magnitude]`:

1. preserve and report the raw symmetry failure;
2. require every one of `C_mean`, `C_lower`, and `C_upper` to be finite and positive definite by
   Cholesky factorization;
3. require the covariance-weighted `2 x 2` Fisher matrix from every route to have rank `2` and
   smallest/largest eigenvalue ratio greater than `1e-12`;
4. require every corresponding Fisher entry and eigenvalue to agree with the `C_mean` route to
   relative tolerance `1e-4`, using denominator `max(1, abs(reference))`;
5. require the classification to remain explicitly conditional on the published shared-SNe-
   standardization and transfer/distance bridge.

If any route fails, do not claim actual-covariance-weighted identifiability. The exact unweighted
rank theorem may remain, but the dataset-weighted upgrade fails.

## Wording ceiling

If all R2B gates pass, write:

```text
actual released covariance-weighted rank is robust across three preregistered symmetric
interpretations, with the raw 3e-8 asymmetry retained as a release-format caveat
```

Never write that the raw matrix itself passed exact symmetry or exact positive-definiteness.
