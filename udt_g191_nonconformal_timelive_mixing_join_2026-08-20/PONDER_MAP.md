# G191 ponder map

## The stripped test

G190 passed with a time-live but conformally flat control. G188 passed with a mixed but stationary
control. G191 switches both features on inside one complete coframe:

```text
time-live common scale + live base-to-screen mixing
    -> completed pair null germ
    -> one affine ray
    -> frequency and full matrix screen together
```

The limit `mu=0` must return the G190 control. The limit `H=0` must return the G188 screen after
affine normalization. The joint case is not allowed to inherit either answer by assertion.

## Why this is a useful falsifier

Time dependence changes the affine clock and frequency. Mixing changes the curvature tide and
cross-image response. If the derivation is coherent, both effects must coexist in one metric
connection and one Jacobi equation. A post-processing construction can easily pass either limit
while failing the simultaneous case.

## Regression alarms

- Do not import P1, a static radius/redshift curve, or G116 coefficients.
- Do not append mixing after calculating the frequency.
- Do not scalarize the matrix screen.
- Do not call the analytic witness the physical universe.
- Do not infer flux, luminosity, SNe agreement, or `X_max`.
