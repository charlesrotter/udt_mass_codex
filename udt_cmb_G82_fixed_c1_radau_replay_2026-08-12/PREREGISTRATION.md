# G82 preregistration — fixed-C1 non-DOP853 replay

Date: 2026-08-12

Base: `e36752ed5e01d45f46812cb154415683a353030f`

Status before calculation: `PREREGISTERED__NO_G82_OUTCOME_INSPECTED`

## Whole bounded question

Does the exact already-frozen G81 nonradial control `C1_FULL_ANGULAR` retain its forward/reverse
screen-covariance result when the direct-Christoffel neighboring-ray calculation is replayed with
the implicit `Radau` integrator family instead of `DOP853`?

This is a numerical-method sensitivity test. It is metric-led but does not explore new metric,
profile, endpoint, direction, screen, source, or physical parameter space.

## Frozen control

The sole control is copied byte-for-value from the G81 C1 row:

```text
metric/profile       G75_AM_S01_E05
receiver             x=1/4, theta=pi/2, psi=0
endpoint             first outward x=1 crossing
direction            (12/13,3/13,4/13)
forward screen       (0,4/5,-3/5), (-5/13,36/65,48/65)
source rotation A    [[3/5,-4/5],[4/5,3/5]]
receiver rotation B  [[5/13,-12/13],[12/13,5/13]]
finite differences   delta=1e-4 and 5e-5
reverse tangent      -k_source/Z
```

No value may be retuned or replaced after the outcome is seen.

## Numerical method

The replay imports the frozen G81 metric, Christoffel, neighboring-ray, projection, and gate
implementation. It replaces only its integration function with SciPy `solve_ivp(method="Radau")`
using:

```text
rtol      5e-11
atol      5e-13
max_step  1/512
```

This is integrator-family independence only. It is not an independent metric implementation or
independent observer-query derivation.

## Certification contract

G82 passes only if all of the following hold without adjustment:

- both forward and reverse event crossings occur;
- the complete G81 frequency, endpoint, null, production-map, unrotated reciprocity, rotated
  covariance, and area gates pass at their frozen thresholds;
- the maximum coarse/fine finite-difference relative change is below `2e-4`;
- each fine Radau forward/reverse/rotated matrix agrees with the frozen G81 DOP853 neighboring-ray
  matrix within relative `2e-4`;
- exact C1 identity, source hashes, method name, tolerances, and authority boundary remain intact.

A failure is reported as a numerical-method disagreement on this one control. It may not be
repaired by changing the ray, endpoint, rotations, finite-difference deltas, or tolerance gates.

## Catch-proof contract

The final verifier must reject: a missing or duplicated C1; inclusion of C0 or a new control;
changed direction, screen, rotations, deltas, endpoint, or profile; DOP853 masquerading as Radau;
loosened gates; partial tangent reversal; omitted transpose, `Z`, `A`, or `B`; source mutation;
claiming absolute independence; claiming a UDT selector, physical endpoint/profile/scale,
`X_max`, CMB/SNe observable, bootstrap closure, action, matter, or future signal.

## Maximum conclusion

If every gate passes:

`G81_C1_SCREEN_COVARIANCE_SURVIVES_ONE_FIXED_NON_DOP853_RADAU_REPLAY`

This would close only the requested integrator-family sensitivity check. The scientific maximum
remains G81's externally reviewed
`DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS`.
