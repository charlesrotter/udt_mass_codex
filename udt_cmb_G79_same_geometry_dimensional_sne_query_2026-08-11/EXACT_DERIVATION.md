# G79 exact derivation — one dimensional redshift and area query on one geometry

Date: 2026-08-11

Status before fresh external review:
`PROVISIONAL_INTERNALLY_VERIFIED__FRESH_ADVERSARIAL_REVIEW_REQUIRED`

## 1. Scoped metric and query

The outcome-independent preregistered selection rule returns the first nonzero row of the frozen
G75 atlas:

```text
profile_id = G75_AM_S01_E05
A(x)       = 1 - x^2/4
q(s)       = s^2/20
h(x)       = x^2 q(x^2) = x^6/20.
```

This is a `CHOSE_CONTROL` geometry, not a physical profile.  Its dimensional metric is

```text
ds^2 = -A(x)c_E^2 dt^2 + R^2 A(x)^(-1) dx^2
       + R^2 x^2(dtheta^2 + sin(theta)^2 dpsi^2)
       + 2 R c_E h(x) sin(theta)^2 dt dpsi.
```

The receiver is the coordinate-stationary observer at `x_r=1/4`; the source is the first outward
crossing of the control sphere `x_s=1`.  The ray is the outward radial member of the receiver's
complete metric-orthonormal sky.  Both endpoint observers are proportional to the stationary
Killing field.  These are query choices.  Neither endpoint is last scattering or `X_max`.

With `tau=c_E t/R`,

```text
ds^2 = R^2 dSigma^2.
```

This factorization determines the scale power of the Jacobi result; it does not make the physical
metric scale-free and it does not determine `R`.

## 2. Stationary endpoint redshift

Let `K=partial_tau`.  Along the null ray,

```text
E = -g(K,k)
```

is conserved.  A coordinate-stationary observer has four-velocity

```text
U = K/sqrt(A),
```

so its measured frequency is

```text
omega = -g(U,k) = E/sqrt(A).
```

For a source at `x_s` and receiver at `x_r`, the registered convention gives

```text
1+z = omega_source/omega_receiver = sqrt(A_receiver/A_source).
```

Here,

```text
A_receiver = 63/64,
A_source   = 3/4,
1+z        = sqrt(21)/4 = 1.14564392373896...,
phi_pair   = log(sqrt(21)/4) = 0.13596685774182....
```

Direct endpoint contraction agrees with this exact Killing result to
`2.886579864025407e-15`.  The mixing profile is not set to zero.  It does not enter this particular
stationary endpoint ratio because Killing energy and the endpoint lapse own the ratio; it remains
active in the null route, screen transport, and area response.

## 3. Angular distance and physical scale

The full null path, parallel screen, curvature, and two-column Jacobi system are integrated in the
dimensionless metric.  If `D_hat` is the resulting dimensionless screen Jacobi matrix, the
physical matrix is

```text
D = R D_hat,
```

and the angular diameter distance is

```text
d_A = sqrt(|det D|) = R sqrt(|det D_hat|).
```

The highest registered refinement gives

```text
D_hat = [[0.7559967070430084, -1.0146339127533253e-22],
         [-1.0146395760931919e-22, 0.7559733363044177]],

d_A/R = 0.7559850215834019.
```

All three `1024/2048/4096` maximum-step controls agree at roundoff scale.  The endpoint is regular,
with no post-origin caustic.  The complete residuals are recorded in `DERIVATION_RESULT.json`.

An independently written direct-Christoffel plus neighboring-ray implementation does not use the
production Riemann or Jacobi equation.  It returns

```text
d_A/R                         = 0.7559850216165416,
relative full-D difference    = 4.3838551044245423e-11,
redshift absolute difference = 6.661338147750939e-16,
maximum endpoint null error   = 2.1058184982859585e-15.
```

## 4. Exact SNe type join, without a fit

The frozen SNe assembly conditionally identifies its radial profile with angular distance:

```text
d_A = r.
```

That makes its P1 distance the same output type as the G79 `d_A`, but only under that already
registered conditional readout premise.  P1 is not inserted into the metric and no fit is run.
At the single G79 point,

```text
R/R_w = [1-(1+z)^(-2/n)] / (d_A/R).
```

This is a no-fit compatibility expression with free `n`; it is not a determination of `R`, `R_w`,
or a physical profile.

## 5. Conditional lens-plus-redshift temperature readout

Geometry has now supplied two distinct pieces for this one query:

1. an endpoint frequency multiplier `1/(1+z)`;
2. an angular Jacobi/lens map `D`.

If, separately, a one-parameter thermal source spectrum is supplied and transforms only by the
derived frequency ratio, then

```text
T_observed/T_source = 1/(1+z) = exp(-phi_pair) = 4/sqrt(21).
```

Only after the dimensional SNe relation and/or the physical `X_max` endpoint curve has been mapped,
a future whole-sky query with source-direction map `F_sky(n)` and direction-dependent redshift could
use the corresponding **conditional** readout

```text
T_observed(n) = T_source(F_sky(n)) / [1+z(n)].
```

This records—but does not yet activate—the user's old lenses-plus-redshift picture: the lens remaps
which source direction is seen, while reciprocal clock dilation rescales the thermal
frequency/temperature parameter.  It remains a typed future readout, not a native CMB source or
thermalization law.  A uniform source and direction-independent redshift remain uniform; lensing
alone does not create a temperature pattern in this conditional order-zero statement.

## 6. Exact landing

```text
DERIVED_CONDITIONAL_ON_ONE_FROZEN_GEOMETRY_AND_ONE_CHOSEN_STATIONARY_QUERY
```

This is the first same-geometry join in this arc that returns both `phi_pair` and `d_A/R` before
consulting P1.  It does not select the physical profile, `R`, endpoint, `X_max`, source state, SNe
fit, CMB temperature field, CMB spectrum, action, matter law, or bootstrap rule.
