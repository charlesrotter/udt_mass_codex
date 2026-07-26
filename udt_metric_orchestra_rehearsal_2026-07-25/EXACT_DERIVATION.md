# Exact common-domain derivation

## Scope

This document derives geometric identities on the preregistered conditional
toric finite-cell coframe.  It does not assert that this coframe family is an
on-shell UDT universe, and it does not introduce an action or a field equation.
All curvature objects below are metric curvature, not GR field equations.

Use `x0=c_E t`, base coordinates `(x0,x)`, and torus coordinates `(y,z)`.  The
coframe is

```text
theta0 = exp(-phi) dx0
theta1 = exp(+phi) dx
(theta2,theta3)^T = D[(dy,dz)^T + S(dx0,dx)^T]

D = [[r,k r],[0,q]]
r = exp(sigma/2-alpha)
q = exp(sigma/2+alpha).
```

The eight chart amplitudes are
`(phi,sigma,alpha,k,S10,S11,S20,S21)`.  Only `phi`'s reciprocal clock/ruler
role is founded.  The other seven directions complete this bounded coframe
chart but are not selected physical fields.

## Exact algebraic blocks

The coframe determinant and metric determinant are

```text
det(E) = exp(sigma)
det(g) = -exp(2 sigma).
```

Therefore the oriented four-volume density is `exp(sigma)` in the `x0`
coordinate and `c_E exp(sigma)` in the observational `t` coordinate.  The
reciprocal `exp(-phi)` clock and `exp(+phi)` ruler cancel exactly from
four-volume.  They do not cancel from every lower-dimensional volume:

```text
observer-rest spatial volume = exp(phi+sigma)
x-boundary induced volume    = exp(-phi+sigma).
```

The angular metric is `G_ang=exp(sigma) H`, where

```text
H = [[exp(-2 alpha),              k exp(-2 alpha)],
     [k exp(-2 alpha), (k^2+exp(4 alpha))exp(-2 alpha)]]
det(H)=1.
```

Thus `sigma` is a common angular log-area direction, while `(alpha,k)` span
the complete positive determinant-one angular shape chart at a point.

For a general covector
`p=p0 dx0+p1 dx+p2 dy+p3 dz`, the exact inverse-metric norm is

```text
g^-1(p,p) = -exp(2phi)(p0-p2 S10-p3 S20)^2
            +exp(-2phi)(p1-p2 S11-p3 S21)^2
            +exp(-sigma+2alpha)p2^2
            +exp(-sigma-2alpha)(p3-k p2)^2.
```

This is a direct all-sector coupling whenever the tested covector has angular
components.  For torus-invariant `dphi`, `p2=p3=0`, it reduces exactly to

```text
g^-1(dphi,dphi) = -exp(2phi)(partial_0 phi)^2
                  +exp(-2phi)(partial_1 phi)^2.
```

The torus connection components are chart/gauge dependent.  Their exact
base curvatures are

```text
F1 = partial_0 S11 - partial_1 S10
F2 = partial_0 S21 - partial_1 S20.
```

## Neutral-point curvature trace

At the neutral regular point, allow all 16 independent first base jets.  With
`f0=partial_0 f` and `f1=partial_1 f`, exact scalar curvature is

```text
R = 4(phi0+sigma0/2)^2 + sigma0^2/2
    +2 alpha0^2 + k0^2/2 +(F1^2+F2^2)/2
    -4(phi1-sigma1/2)^2 - sigma1^2/2
    -2 alpha1^2 - k1^2/2.
```

Equivalently, the exact expanded polynomial frozen in `ALGEBRA_RESULT.json`
and `CURVATURE_RATE_HESSIAN.tsv` is

```text
R = S11_0^2/2-S11_0 S10_1+S21_0^2/2-S21_0 S20_1
    +2 alpha0^2+k0^2/2+4 phi0^2+4 phi0 sigma0+3 sigma0^2/2
    +S10_1^2/2+S20_1^2/2
    -2 alpha1^2-k1^2/2-4 phi1^2+4 phi1 sigma1-3 sigma1^2/2.
```

The connection terms are exactly `(F1^2+F2^2)/2`.  The temporal/spatial signs
are Lorentzian trace signs, not an energy or stability conclusion.

Only 16 upper-triangle Hessian pairs survive this scalar trace.  Pure second
jets survive in the scalar only for `phi_00`, `phi_11`, `sigma_00`, and
`sigma_11`.

## Full Ricci response

The full symmetric Ricci tensor retains much more information:

- 59 upper-triangle first-rate pairs are nonzero, rather than 16;
- 17 of 24 pure second-jet controls are nonzero, rather than four;
- the family-level first-rate graph in the preregistered coframe chart is
  connected across all eight instruments;
- `phi` couples directly to `sigma`, `alpha`, and `k` at this point;
- the four connection components couple to `sigma`, `alpha`, and `k`, and to
  one another;
- there is no direct `phi`-to-`S` first-rate edge at this neutral point, so
  angular area/shape provide the exact two-step bridge;
- tracing the Ricci tensor cancels the `phi-alpha`, `phi-k`, shape-connection,
  and many connection-connection responses.

After exact connection-gauge reduction, the four chart amplitudes `S10,S11,
S20,S21` contribute through the two curvature channels `F1,F2`.  The reduced
six-node chart-family graph `{phi,sigma,alpha,k,F1,F2}` has 19 edges including
self-edges and remains connected.  `phi` has no direct `F1` or `F2` edge;
`sigma`, `alpha`, and `k` supply the bridge.  The exact edge list is
`GAUGE_REDUCED_RICCI_GRAPH.tsv`.

The second-jet channels separate cleanly:

```text
phi    -> base clock/ruler curvature (R00,R11)
sigma  -> base plus angular common-area curvature (R00,R01,R11,R22,R33)
alpha  -> opposite angular diagonal response (R22,-R33)
k      -> angular off-diagonal response R23
S1     -> mixed base/angular responses R02,R12
S2     -> mixed base/angular responses R03,R13.
```

Exact components and coefficients are in `RICCI_RATE_COUPLINGS.tsv` and
`RICCI_SECOND_JET_RESPONSE.tsv`.  An independent 70-digit metric finite-
difference calculation reconstructed all 2,560 Ricci-Hessian entries and all
240 Ricci second-jet entries without importing the symbolic production code.

## What is and is not derived

The metric supplies a genuine coupling grammar in this domain: volume,
angular shape, connection curvature, causal depth, boundary geometry, and
Ricci curvature can coexist and respond jointly on one domain.  The tensor response is
an orchestra in a precise limited sense: its chosen-chart instrument-family
graph is connected even though its scalar trace sounds like several isolated
sections.  Connectivity of this component graph is not itself asserted as a
new frame-independent invariant.

The metric has not supplied a score.  No geometric identity here selects a
profile, relative physical weight, boundary functional, global completion,
density, matter source, carrier, action, or bootstrap fixed point.  The result
is an exact partial response map `R_geom`, not the missing admissibility map
`A` and not a field equation.
