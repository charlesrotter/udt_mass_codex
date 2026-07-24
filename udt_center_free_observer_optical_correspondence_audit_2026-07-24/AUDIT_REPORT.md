# Center-free observer optical-correspondence audit

Date: 2026-07-24

Base: `c67c0c1bcd94af6364d93f21fd9dd3a2194f5d3b`

Preregistration: `c1d1e00aa4cc326f70df552d854d4606de447491`

Pre-compute source addendum:
`1e50f033a4d2489a1b1c3006a899c35645cb9027`

Grade: **VERIFIED-WITH-CAVEATS**

## Result

The complete metric does contain a native observer-to-observer optical
object, but it is not generally one scalar distance.

Given observer events and a path, the metric determines:

- endpoint clock comparison;
- transverse angular/screen transport;
- the change in transverse area;
- a pathwise area radius.

Because the event pairing and path can be nonunique, the correct object is a
set-valued bilocal correspondence. This is derived geometry. Interpreting
its null member as physical light or information propagation remains an
additional premise.

## The two exact constructions

Two constructions survive:

1. spacetime-null screen transport;
2. simultaneous observer-rest spatial screen transport.

They coincide in ultrastatic and special centered controls, but a
time-dependent metric counterexample proves they are not universally the
same. Co-presence does not yet provide an equation selecting one.

## Complementary branch result

The two strongest registered branches contain opposite halves of the desired
structure.

### Round B19

The conditional round branch is genuinely center-free. Every observer sees

```text
pair distance D in [0,pi b],
area radius D_A=b sin(D/b).
```

At the antipode, pair distance is maximal while `D_A` returns to zero and the
path becomes a family. Its lapse is constant, so there is no reciprocal
clock dilation.

### WR-L

In proper radial coordinate,

```text
N(D)=1-D/(2X),
R(D)=D-D^2/(4X).
```

The centered radial readout gives

```text
1+z=1/N=exp(phi),
D_A=R(D)=X[1-exp(-2phi)].
```

This is precisely the clock/area combination used by the successful
registered SNe result. But `D_A` is not proper distance, and the WR-L chart
cannot be smoothly recentered as one global manifold:

```text
K_rad=1/(2XR),
K_tan=1/(XR).
```

Its center is also irregular if included. Therefore the SNe shape survives
as an **observed local residual readout**; its promotion to a global
center-free universe remains open.

## Why this matters

The missing UDT object is now sharper. It is not merely a preferred
saturating function. It is one complete bilocal longitudinal–transverse
metric correspondence:

```text
longitudinal: reciprocal clock/depth comparison
transverse:   angular Jacobi/area transport
global:       observer chart transitions, path families, and completion.
```

Round B19 supplies the transverse/global side without dilation. WR-L
supplies the longitudinal/centered-transverse side without a global
center-free realization. They may not be spliced across different branches.

## Static endpoint warning

An exact constant-curvature control has infinite static clock dilation at
`pi b/2` while the complete spatial diameter is `pi b`. Thus:

- infinite-dilation endpoint;
- optical caustic;
- maximum areal radius;
- proper radial endpoint;
- global observer-pair diameter

are distinct metric objects unless a complete branch proves their equality.

## Branch census

- 12/12 finite-cell completions: no complete `g,phi` witness.
- 28/28 equation/evidence families: B19 is the sole complete conditional
  center-free optical witness; B21/WR-L is local and residual.
- squashed `S3`: complete centerless off-shell correspondence, but
  direction-dependent cut/area atlas remains open.
- temporal-`phi`: conditional rest-space construction, no complete branch or
  physical representative.

## Evidence

- 84 exact SymPy/source/registry checks, including a direct Christoffel/Riemann reconstruction;
- 72 independent standard-library/Fraction checks;
- 14 exercised adversarial catches;
- exact screen-gauge invariance;
- round, flat, hyperbolic, WR-L, constant-curvature, time-live, and
  event-pairing controls;
- complete 12/28 fixed-registry accounting.

No fresh independent model-family context was authorized, so the result is
`VERIFIED-WITH-CAVEATS`, not canon.

## Authority boundary

This audit does not:

- choose null versus co-present rest pairing;
- derive physical signal propagation;
- promote the WR-L SNe readout to a global cosmology;
- derive physical `X_max`;
- select or splice a branch;
- add an action, source, carrier, boundary, density, or mass law;
- make BAO, CMB, black-hole, or particle claims.

No GPU work, canonization, navigation edit, or repository reorganization was
performed.
