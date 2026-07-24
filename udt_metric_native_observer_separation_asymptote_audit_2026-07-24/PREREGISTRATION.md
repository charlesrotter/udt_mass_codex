# Metric-native observer-separation asymptote audit — preregistration

Date: 2026-07-24

Base: `25ab620363e07b49dc5268f8714ea2314523d2d1`

Mode: `MAP -> OBSERVE -> DERIVE`, exact CPU algebra only

Status: `PREREGISTERED_BEFORE_PRODUCTION_DERIVATION`

## Owner clarification being tested

Charles's proposed physical reading is:

> `X_max` is the maximum nonnegative separation between two observers. It
> should be the finite separation approached when reciprocal clock dilation
> tends to infinity, analogous to the limiting behavior at `c` in SR.

The audit does not assume that the positional relation is `tanh`. It asks
whether the current complete metric derives the relation.

## Whole question

Given the registered reciprocal clock-distance block and the complete
shift/angular coframe parent:

1. what nonnegative two-observer separations are intrinsic to the supplied
   metric/coframe data;
2. which, if any, is uniquely selected without an action, source, carrier,
   boundary rule, mass law, empirical fit, or desired profile;
3. whether the selected separation is a function of the reciprocal depth
   `phi`;
4. whether its `phi -> +infinity` limit is finite and supplies a global
   observer-pair diameter `X_max`; and
5. whether the result is invariant under observer-frame and admissible chart
   changes.

## Metric-led scope

The audit is metric-led. It will derive from:

- the reciprocal clock/ruler coframe pair;
- the complete ten-slot exponential triangular coframe;
- supplied observer directions or a supplied reciprocal clock leg;
- the induced positive spatial quadratic form;
- exact path length, endpoint, and diameter definitions; and
- the registered conditional WR-L slice as one controlled realization.

It will not use an empirical target to choose a distance or profile.

## Frozen candidate readings

Every candidate is retained through adjudication:

1. coordinate reach;
2. radial slice-proper length;
3. full coframe-horizontal path length;
4. hypersurface-induced geodesic distance when the clock distribution is
   integrable;
5. horizontal/sub-Riemannian distance when it is not integrable;
6. optical depth;
7. areal/angular distance;
8. spacelike world-function distance in a convex normal neighborhood;
9. a supplied one-dimensional projective readout, including `tanh(phi)`;
10. global diameter obtained by taking the supremum of a valid nonnegative
    pair distance over a declared observer/event-pair domain.

Coordinate, optical, areal, projective, and local radial readings may not be
silently relabeled as the global diameter.

## Exact test families frozen before outcome

### F1 — reciprocal radial profile family

Use

```text
theta0 = exp(-phi) c_E dt
theta1 = exp(+phi) dr
```

and test whether the clock factor alone fixes proper separation as a
function of `phi`. If an arbitrary smooth increasing candidate `D(phi)` can
be realized by a regular monotone profile `r(phi)`, uniqueness fails at this
scope.

At minimum retain bounded `tanh`, bounded exponential, and unbounded linear
controls.

### F2 — conditional WR-L realization

For

```text
A = exp(-2 phi) = 1-r/X
```

derive, without identifying them:

- coordinate reach;
- slice-proper radial length;
- optical depth;
- projective `tanh` readout; and
- their asymptotic endpoints.

### F3 — complete ten-slot coframe

For

```text
theta0 = u dx0 + b dx1
theta1 = w dx1
theta2 = (r a20+e a30)dx0 + (r a21+e a31)dx1 + r dx2 + e dx3
theta3 = t a30 dx0 + t a31 dx1 + t dx3
```

with positive `u,w,r,t`, impose only the local clock-horizontal condition
`theta0=0` and derive the complete positive spatial line element. No angular
or shift amplitude may be omitted.

### F4 — angular/global countercontrols

Construct complete positive spatial geometries with the same radial
clock-dilation profile but different angular size, topology, or completion.
Test whether their global diameters differ. This family is load-bearing:
if it succeeds, clock dilation alone cannot determine global `X_max`.

### F5 — observer/coframe control

Test whether the proposed distance is invariant under:

- spatial rotations of a fixed clock frame;
- coordinate relabeling;
- local Lorentz coframe boosts that preserve `g` but change the clock leg;
- constant common rescaling; and
- the two current physical-metric/conformal-class ontology branches.

## Premise rules

- `c_E` is an `OBSERVED` clock-length conversion anchor.
- Reciprocal-c plus dual Reciprocity plus composition derive the positive
  reciprocal pair, with the recorded readout premises.
- `phi` is the signed logarithmic reciprocal imbalance.
- Nonnegative physical separation is required.
- GR-like macro observer reciprocity is retained as covariance/equivalence of
  descriptions, not identical metric components.
- Strong local Common-Scale Neutrality is challenged and not derived.
- A calibrated physical metric is an owner-motivated `WORKING` ontology for
  this audit, with the conformal-class branch retained as a countercontrol.
- Global co-presence does not silently provide a foliation, event-pairing
  map, or clock congruence unless the metric/coframe supplies it.
- The local WR-L `X` is not identified with global `X_max`.

## Certification and falsification contract

The audit may conclude `DERIVED` only if the current metric data uniquely
supply:

1. an observer/event-pair domain;
2. a nonnegative symmetric separation satisfying the required metric
   properties on that domain;
3. a frame/chart invariant construction;
4. a unique relation between that separation and clock dilation;
5. a finite common infinite-dilation endpoint; and
6. a proof that the endpoint is the global observer-pair diameter.

The unique-derivation claim fails if any of the following survives:

- two admissible `D(phi)` laws with the same reciprocal clock block;
- two intrinsic distance readings with different endpoints in one fixed
  metric;
- two complete angular/global completions with the same clock law and
  different diameters;
- a dependence on a chosen clock congruence or event pairing;
- a dependence on an unselected common scale;
- a local radial endpoint mislabeled as a pair diameter; or
- a projective/WR-L relation inserted rather than derived.

## Independent verification

A production SymPy derivation and a separate standard-library implementation
must independently reconstruct all load-bearing identities. The independent
route may not import production code. Exercised corruption catches must
reject at least:

- dropping an angular or shift term;
- identifying coordinate, proper, optical, and projective readings;
- promoting local `X` to global `X_max`;
- claiming uniqueness in the arbitrary-profile family;
- erasing clock-leg dependence;
- ignoring a common-scale change; and
- changing a frozen source identity.

## Maximum allowed conclusion

At most:

```text
THE_CURRENT_COMPLETE_METRIC_DOES_OR_DOES_NOT_UNIQUELY_DERIVE_A
NONNEGATIVE_OBSERVER-SEPARATION LAW WHOSE INFINITE-DILATION
ASYMPTOTE IS GLOBAL X_MAX, WITH EVERY ADDITIONAL PREMISE NAMED.
```

No action, source, carrier, matter, mass, density, boundary charge, empirical
fit, canonization, navigation edit, GPU work, or repository reorganization
is authorized.
