# Numerical-control preregistration

Date: 2026-08-12  
Parent preregistration commit: `0e36e507`

This file fixes the constructive G85 controls before any curvature outcome is evaluated.

## G85 point and free controls

All G85 evaluations use the regular off-axis seam point

```text
chi = pi/2,
theta = 1.1,
psi = 0.37.
```

The time-live control function uses `omega=1.1`. The three `(epsilon,tau)` controls are

```text
C0     = ( 0.0,  0.0),
CMINUS = (-0.3, +0.4),
CPLUS  = (+0.3, +0.4).
```

The constructive amplitudes are

```text
B = 0.6 for A03 and shift-supported A05,
L = 0.45 for A04.
```

Every value above is `pinned-by-HABIT` as a finite numerical coverage witness, not a physical
constant. The sign pair in `epsilon` and the zero control are retained; no result may be called a
continuous-parameter classification.

For A03 and A04 the inherited stationary profile is evaluated exactly as

```text
h(chi)=4 sin(chi)^2 q(4 sin(chi)^2)
```

for all 196 frozen `q`. For shift-supported A05 the source's explicit equatorial-band witness
`h=0` is used, with every source profile identity retained even though the local metric then becomes
profile-independent.

## G63 point controls

For each of the exact 14 frozen G63 samples, use the existing source-owned local points:

```text
p = initial_point(sample),
q = p + source endpoint_atlas q offset,
r = p + source endpoint_atlas r offset.
```

These are `pinned-by-HABIT` inherited diagnostic tiles. They test local persistence only.

## Finite-difference ladder

The independent route evaluates coordinate derivatives on the ladder

```text
h = 8e-4, 4e-4, 2e-4
```

using fourth-order centered first derivatives for both metric and connection. The middle value is
the reporting route; the outer values are convergence controls. Failure to reach the parent
cross-route tolerance returns `NUMERICALLY_UNRESOLVED`.
