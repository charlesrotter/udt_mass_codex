# Exact derivation — complete-angular mode ownership

Date: 2026-08-09  
Status: `CONDITIONAL_MODE_DECOMPOSITION_DERIVED; PHYSICAL_COMPLETION_AND_POPULATION_PROJECTION_OPEN`

## 1. What is being extended

The corrected FD1 atlas solves the scalar operator on the declared `2+1`-dimensional equatorial
metric

```text
ds_C0^2=-A dt^2+dr^2/A+r^2 dpsi^2+2h dt dpsi.
```

Its integer `m` is exactly the Fourier character of the chosen `psi` circle. That ownership is
valid in C0. It does not yet say how a C0 radial eigenfunction extends through a complete angular
screen.

The clean axis-regular round-screen completion named by RA1 is the conditional representative C1:

```text
ds_C1^2 = -A dt^2 + dr^2/A + r^2 dtheta^2
          + r^2 sin^2(theta)dpsi^2
          + 2 h sin^2(theta) dt dpsi.
```

The `sin^2(theta)` factor is required for regularity of the axial one-form at the poles. C1 is
`CHOSE`; no current UDT selector privileges a round screen, this axial lift, or its global
completion.

## 2. Exact C1 inverse, density, and scalar operator

Set

```text
D(r,theta)=A(r)r^2+h(r)^2 sin^2(theta).
```

Then

```text
det(g) = -r^2 sin^2(theta) D/A,
sqrt(-g) = S = r sin(theta) sqrt(D/A),

g^tt       = -r^2/D,
g^tpsi     =  h/D,
g^psipsi   =  A/[sin^2(theta)D],
g^rr       =  A,
g^thetatheta = 1/r^2.
```

For

```text
Psi=exp(-i omega t+i m psi)u(r,theta),
```

the exact scalar equation `Box_g Psi=0` is

```text
0 = S^-1 partial_r(S A partial_r u)
  + S^-1 partial_theta(S partial_theta u/r^2)
  + [r^2 omega^2+2h omega m-A m^2/sin^2(theta)]u/D.       (1)
```

This is still only the chosen scalar diagnostic, not native UDT dynamics.

## 3. The equatorial atlas does not lift as the same radial problem

At `theta=pi/2`, define `D_eq=A r^2+h^2` and `W=sqrt(D_eq/A)`. C0 has density `W`; C1 has

```text
S_eq = r W.
```

Therefore, even after suppressing all polar dependence, the C1 radial flux is

```text
(r W)^-1 partial_r(r W A partial_r R),
```

whereas C0 used

```text
W^-1 partial_r(W A partial_r R).
```

The extra factor is the volume of the angular dimension that C0 omitted. The time/azimuth
potential agrees at the equator, but the differential operator does not. Consequently the 10,080
FD1 roots remain valid observations of C0 and cannot be relabeled as C1 full-angular roots.

## 4. Generic C1 modes are a coupled two-dimensional problem

Write

```text
B(r)=h(r)^2/[A(r)r^2].
```

The mixed logarithmic-volume derivative is exactly

```text
partial_r partial_theta log S
 = B'(r)sin(theta)cos(theta)/[1+B(r)sin^2(theta)]^2.       (2)
```

For a product ansatz `u=R(r)Theta(theta)`, the ratio of the two principal coefficients forces the
only separation multiplier, up to a constant, to be `r^2`. After that multiplication, the
theta-derivative of the radial first-derivative coefficient is

```text
r^2 A B'(r)sin(theta)cos(theta)/[1+B(r)sin^2(theta)]^2.
```

It is nonzero whenever `B'` is nonzero. In the frozen FD1 family

```text
A=(1-r)^n,
h=hbar r^2(1-r)^q,
B=hbar^2 r^2(1-r)^(2q-n),
```

and `B` is not constant for any constant `(n,q)` when `hbar` is nonzero. Hence the C1 realization is
generically nonseparable: each fixed-`m` problem is a coupled PDE in `(r,theta)`, not one of the old
radial ladders.

The `h=0` control C2 is separable. Equation (1) becomes the round-sphere equation with
`Y_ell^m(theta,psi)` and radial equation

```text
partial_r(r^2 A partial_r R)
 + [r^2 omega^2/A-ell(ell+1)]R = 0.                       (3)
```

## 5. What owns the angular labels

### C1: axial mixing on

The Lie derivative of C1 along `partial_psi` vanishes exactly, so C1 has a conditional `U(1)`
decomposition. Its integer `m` is the character of that axial isometry. North/south reflection also
survives. Thus a full C1 mode can be classified by

```text
(m, north/south parity, coupled radial-polar branch).
```

A nonaxial round-sphere generator `J_x` does not survive. One exact component is

```text
(L_Jx g)_(t theta)=h cos(psi),
```

which is nonzero for generic `h`. Therefore C1 has no `SO(3)` theorem relating its `m=-1,0,+1`
sectors.

### C2: symmetry-restored limit

At `h=0`, `SO(3)` is restored. Multiplets are defined by one fixed `ell`, with
`m=-ell,...,+ell`; the regular center power is `r^ell`. The C0 center power was `r^|m|` because C0
was a two-dimensional disk problem.

A C0 Fourier character `m` can extend into every full spherical harmonic with `ell>=|m|`. It does
not choose an `ell`. Even the minimal extension would put C0 `m=0` in `ell=0` and C0 `|m|=1` in
`ell=1`, so an equal-radial-index C0 triple is not an `ell=1` spherical triplet. The previous
same-index pairing therefore has no representation-theoretic ownership even in the symmetry-
restored control.

### C3/C4: registered complete-screen freedom

The registered screen has an independent area mode and two shears; its values and global
realization are unselected. A smooth positive area witness such as

```text
V(theta,psi)=1+epsilon sin(theta)cos(psi),  |epsilon|<1,
```

already has `partial_psi V != 0` at generic points and therefore no axial `U(1)`. This is an
availability counterexample, not a proposed universe. It proves that `m` is not a universal label
over the currently admitted complete-screen configuration arena.

Existing complete `S3` controls likewise establish compatible configurations, not a selected
WR-L/round/axial completion. Cross-splicing them to C1 would manufacture the missing join.

## 6. Projection is not population

Conditional symmetry projectors do exist once a symmetry is supplied. In C1,

```text
(P_m f)(psi)=(1/2pi) integral_0^(2pi) exp(-i m alpha)f(psi+alpha)dalpha
```

decomposes the scalar space into every integer `m`. It selects no preferred `m` and no amplitude.
In C2 the invariant object is the projector onto a complete fixed-`ell` eigenspace; an individual
`m` requires an axis, which may be supplied by an observer query but is not a universal population
law.

Four distinct objects must not be merged:

1. the complete-pair tangent-space reciprocal/screen projector;
2. a symmetry projector on the scalar function space;
3. a spectral projector after a self-adjoint boundary realization is chosen; and
4. physical mode weights in a state, source, covariance, or Green-function readout.

The metric can conditionally provide the first two. The third additionally needs the probe and a
domain/boundary realization; FD1 explicitly leaves D/N free. The fourth needs a state/source or
response prescription. Evaluating modes at two observer endpoints supplies a linear query, not
their amplitudes. A Green kernel further needs boundary and causal/response data. None of those
operations is selected by current metric, Reciprocity, or complete-pair premises.

## 7. Exact landing

`DERIVED`, conditional on C1:

- the full operator (1);
- generic radial/polar nonseparability;
- `U(1)` `m` ownership plus north/south parity;
- restoration of `SO(3)` multiplets only at `h=0`;
- the exact operator mismatch between C0 and C1.

`DERIVED` as nonselection over C0-C4:

- the FD1 same-index triple has no full-angular multiplet ownership;
- no universal `m` label survives all admitted complete screens;
- symmetry projectors decompose all modes but select no physical population.

`OPEN`:

- the physical complete angular lift;
- the full-angular spectrum of any selected nonzero-mixing completion;
- observer-pair response, mode weights, source statistics, polarization, and FD2.

No CMB datum entered the derivation.
