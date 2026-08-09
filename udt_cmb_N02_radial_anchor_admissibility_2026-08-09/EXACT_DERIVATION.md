# Exact N02 radial-anchor admissibility derivation

## Scope

This audit asks whether any already-banked P1 profile can support a complete regular C1/C2
center-to-wall control problem. C1/C2 and scalar `Box_g` remain `CHOSE`. No radial equation is
integrated and no spectrum or boundary is selected.

## 1. Complete-metric center, not scalar-center habit

For the conditional C1 metric

```text
ds^2=-A dt^2+dr^2/A+r^2 dtheta^2+r^2 sin^2(theta)dpsi^2
     +2h sin^2(theta)dt dpsi,
```

write the center expansions

```text
A=1+a r+b r^2+O(r^3),
h=k r^2+c r^3+O(r^4).
```

A direct four-dimensional Ricci calculation, retaining the mixing terms, gives

```text
lim_(r->0+) r RicciScalar = -6a.                         (1)
```

The finite mixing contribution cannot cancel this residue. For the banked P1 family

```text
A=(1-r)^n=1-nr+n(n-1)r^2/2+...,
```

so `a=-n` and

```text
RicciScalar = 6n/r+O(1).                                (2)
```

Every registered `n` is positive. Thus every frozen P1 row has a curvature-singular full
spherical center. This does not invalidate P1 as a fitted observer-relation/equatorial profile; it
blocks silently reusing that profile as a smooth complete spherical metric.

The axial one-form supplies a second, independent necessary condition. In Cartesian coordinates,

```text
sin^2(theta)dpsi = (-y dx+x dy)/r^2.
```

Therefore `h=O(r^2)` is necessary at a collapsing axial orbit. The corrected FD1 family
`h=hbar r^2(1-r)^q` passes that leading-order condition, although this audit does not claim full
Cartesian smoothness of its noninteger radial profile. The older RA1 literal lineage
`h=h0(1-r)^q` fails even the necessary order. Neither fact repairs the independent P1 curvature
residue (2).

## 2. Nonzero-mixing wall matrices

Put `u=1-r` and retain the banked corrected family

```text
A=u^n,
h=hbar r^2 u^q,
B=hbar^2 r^2 u^(2q-n).
```

Every registered `q/qcrit` is below one, with `qcrit=1-n/2`. Hence

```text
2q-n<0,
B->infinity.
```

For any fixed finite harmonic block, the exact N01 matrices have the large-`B` structure

```text
W ~ sqrt(B) W_inf,       M ~ B^(-1/2) M_inf,
K ~ sqrt(B) K_inf,       H ~ B^(-1/2) H_inf,             (3)
```

where the limiting matrices are finite and the principal `W_inf,M_inf` forms are positive. The
constant `m=0,ell=0` angular direction is retained; its vanished `K` term only softens the endpoint.
Equation (3) gives

```text
P = r^2 A W              ~ |hbar| r^3 u^p W_inf,
Q2 = (r^2/A) M           ~ r |hbar|^(-1) u^(-p) M_inf,
Q1 = (2hm/A) M           ~ 2m sign(hbar) r u^(-n/2) M_inf,
p = q+n/2.                                                   (4)
```

The Liouville distance behaves as

```text
x ~ u^(1-p)/[|hbar|(1-p)].                               (5)
```

Because `q<qcrit`, `p<1`, so the wall is at finite `x`. After constant finite-block congruence
normalization, the angular and rotation terms scale relative to `Q2` as

```text
K/Q2 ~ x^[2q/(1-p)],
H/Q2 ~ x^[n/(1-p)],
Q1/Q2 ~ x^[q/(1-p)].                                    (6)
```

For all 21 registered `(n,q)` strata, the strongest exponent satisfies

```text
2q/(1-p)>-2.
```

Thus (6) is sub-inverse-square. For each fixed finite harmonic truncation and finite frequency,
both local solution families are square integrable: the nonzero-mixing wall is limit-circle and a
self-adjoint extension remains free. Vector Dirichlet `R=0` and vector flux-Neumann `P R'=0` are
admissible separated control members, not selected physics and not an exhaustive extension family.
No uniform infinite-harmonic endpoint theorem is claimed.

## 3. Round wall

For `h=0`, the round C2 equation has

```text
P~u^n,        Q2~u^(-n),        x~integral u^(-n)du.
```

All three registered `n` exceed one, so the wall lies at infinite Liouville distance. The angular
potential decays there and the endpoint is limit-point. It has a unique asymptotic domain; D/N are
not freely specifiable wall data. This is a continuum control, not a discrete wall ladder.

## 4. Landing

The wall audit is productive: nonzero mixing changes the P1 wall from the round infinite-distance
limit-point case to a finite-distance limit-circle family. But the complete center audit blocks
every frozen P1 row before a regular center-to-wall C1/C2 eigensystem exists.

Therefore no N02 eigensolve is admissible from the banked profile set. A later step must first map
the role and regular-center conditions of complete radial profiles without altering P1 to obtain a
desired spectrum. N01's local angular matrix architecture remains valid for regular interior
`r>0`; only its proposed global radial continuation is blocked.
