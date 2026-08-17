# G148 fresh adversarial review

Date: 2026-08-17

Verdict: `REPAIR_REQUIRED`

The fresh zero-context reviewer reran:

- production: `29/29`;
- independent: `23/23`;
- package: `90/90`;
- frozen source hashes: `5/5`.

The sign audit passed. With `a_n=g(nabla_u u,n)`, differentiated orthogonality and `g(u,u)=-1`
indeed give

\[
\nabla_u n=a_nu+\Omega
\]

and the ambient norm contains `-rho^2 a_n^2`.

## Required repairs

1. Separate the arbitrary registered matrix-family parameter `lambda` from covariant query-clock
   differentiation. The witness verifies algebraic first-variation liveness of `h`, `phi_pair`, and
   coordinate projector components; it does not compute the Levi-Civita connection or independently
   verify `nabla_u n`, `a_n`, or `Omega`.
2. Keep `xi=rho n` `CHOSE / WORKING`, not derived physical carrier. The bounded calculation bypasses
   rather than resolves G147's carrier ownership gate; independent-carrier `O(2)` remains.
3. Restrict regime statements to exact coefficient limits. No physical regime pattern follows
   without supplied `dot phi`, `Omega`, and `a_n`, whose boundedness at the limits is not proved.

## Maximum defensible landing

```text
WORKING_RELATION_FIRST_REPRESENTATION_ONLY__
EXACT_COVARIANT_FIRST_JET_IDENTITY_FOR_A_SUPPLIED_SMOOTH_REGULAR_CALIBRATED_PAIR__
LAMBDA_WITNESS_ESTABLISHES_COMPLETE_PAIR_ALGEBRAIC_FIRST_VARIATION_LIVENESS_ONLY__
COEFFICIENT_LIMITS_CHARACTERIZED__
PHYSICAL_CARRIER_HISTORY_DYNAMICS_AND_OBSERVATIONAL_REGIME_PATTERN_OPEN
```

No files were changed by the reviewer.
