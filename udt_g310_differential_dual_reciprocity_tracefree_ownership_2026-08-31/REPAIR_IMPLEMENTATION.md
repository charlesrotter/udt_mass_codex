# G310 R1/R2 repair implementation

Date: 2026-08-31
Preregistration commit: `71f45256`
Scientific landing: unchanged

## R1 — exact normalization

- production seed changed from `diag(1,1,0,0)` to the exact founded derivative
  `diag(2,2,0,0)`;
- independent `pair_tangent` now returns
  `2*(u_flat tensor u_flat+n_flat tensor n_flat)`;
- all spatial-cross, time-cross, and wrong-sign control coefficients were updated consistently;
- the production and independent outputs now record the factor-two normalization explicitly.

The exact ranks, basis indices, annihilator, coefficient strata, residual, and remaining scalar
datum are unchanged.

## R2 — independent annihilator

The separate verifier now:

1. constructs its own Lorentz-pairing rows from its nine constructive tangent directions;
2. row-reduces those rows with a separate exact `Fraction` implementation;
3. computes the nullspace;
4. verifies rank nine, nullity one, and proportionality to `g_ab`;
5. reads `A_ii=-A_00`, `A_ij=0`, and `A_0i=0` from the computed vector;
6. confirms independently that two different metric multiples satisfy every balance.

It imports no production orbit, rank, pairing, or nullspace helper.

## Repaired live results

- production: 14 checks, PASS;
- independent: 32 checks, PASS;
- hostile controls: 7/7 caught;
- aggregate package replay: PASS.

External repair-only follow-up remains required.
