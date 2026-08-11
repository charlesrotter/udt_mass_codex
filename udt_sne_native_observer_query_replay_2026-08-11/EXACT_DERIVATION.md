# Exact native-query retyping of the frozen SNe profiles

## 1. Correct object type

The current pair-immersion architecture begins with a supplied regular calibrated relation
`F:Sigma -> (M,g)` and its induced Lorentzian two-metric `h=F* g`. On the regular stratum,

```text
T^2=-h_00,
L^2=h_11-h_01^2/h_00,
phi_pair=(1/2)log(L/T)=(1/4)log[(-det h)/h_00^2].
```

This is a terminal evaluator. It does not select the SNe event pair, immersion, branch, screen, or
flux transport.

For the frozen SNe query, the registered observational identification is

```text
1+z=exp(phi_pair).
```

It follows conditionally that

```text
c_eff^(pair)/c_E=exp(-2 phi_pair)=(1+z)^(-2).
```

This is the supplied-pair cone readout. It is not a material propagation speed or a universal
mixed-geometry law. `c_E` fixes the clock/ruler calibration but cancels from the dimensionless SNe
shape.

## 2. Frozen profile families in the corrected variable

Writing `phi=phi_pair`, the three historical profile families are:

```text
P1: r(phi)=R_w [1-exp(-2 phi/n)],
P2: r(phi)=2 X phi,
P3: r(phi)=X [exp(2 phi/alpha)-1].
```

Substitution of `phi=log(1+z)` gives exactly:

```text
P1: r(z)=R_w [1-(1+z)^(-2/n)],
P2: r(z)=2 X log(1+z),
P3: r(z)=X [(1+z)^(2/alpha)-1].
```

Therefore the corrected terminal variable does not alter any historical profile formula.

## 3. Registered area/flux readout

The frozen SNe assembly additionally supplies

```text
d_A=r,
d_L=(1+z)^2 d_A=exp(2 phi_pair) r(phi_pair).
```

Thus

```text
P1: d_L=(1+z)^2 R_w [1-(1+z)^(-2/n)],
P2: d_L=2 X (1+z)^2 log(1+z),
P3: d_L=X (1+z)^2 [(1+z)^(2/alpha)-1].
```

At `n=1`, P1 still reduces exactly to

```text
d_L=R_w z(z+2).
```

The exact checks are in `derive_query_equivalence.py` and `QUERY_EQUIVALENCE.json`.

These area/flux relations are retained **conditional readout premises**. The pair metric alone does
not derive its immersion, second fundamental form, full screen-area map, source physics, or flux
transport.

## 4. What the orchestra changes—and what it does not yet calculate

The complete metric can contribute reciprocal, angular, shift, and mixing terms to the induced
pair metric before `phi_pair` is evaluated. Therefore a complete SNe realization may change both:

```text
the map from the observer query to phi_pair,
the map from that realization to d_A.
```

The current bank establishes this structural possibility. It does not select the physical SNe
immersion, screen, branch, time-live history, or coefficient-free curve through the orchestra
atlas. Consequently there is no owned additive “orchestra correction” to insert into P1/P2/P3.

Retyping the already-fitted scalar as `phi_pair` is mathematically consistent, but it does not prove
that the frozen P1 profile is the output of the complete native geometry. It changes the
interpretation, not the fitted numbers.

## 5. Exact scoped landing

```text
BASELINE_REPRODUCED__NATIVE_RETYPE_ALGEBRAICALLY_IDENTICAL
AND
NO_OWNED_COMPLETE_SNE_QUERY_CORRECTION.
```

The observed P1 fit remains a useful conditional macro anchor. A genuinely improved native result
requires the upstream complete SNe query/realization and screen-area law to be derived or otherwise
owned first; it cannot be manufactured by adding fit freedom.
