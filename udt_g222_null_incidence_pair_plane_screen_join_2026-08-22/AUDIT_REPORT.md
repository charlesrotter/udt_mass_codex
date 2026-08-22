# G222 audit report

Date: 2026-08-22

## Landing

```text
SUPPLIED_NULL_FAMILY_OWNS_FULL_RANK_TWO_PAIR_PLANE_CONDITIONALLY
__CONSERVED_NULL_AREA_DENSITY_COMPLETES_RECIPROCAL_RULER
__G188_SCREEN_IS_CANONICAL_NORMAL_CHANNEL
__GLOBAL_RULER_COORDINATE_AND_PHYSICAL_PROTOCOL_REMAIN_OPEN
```

## What was learned

The same supplied null-incidence family that gives G221's scalar clock chord also supplies the
missing second tangent. Its pullback is

\[
h=
\begin{pmatrix}
g(J,J)&-a\\
-a&0
\end{pmatrix},
\qquad
a=-g(J,K)>0,
\qquad
\det h=-a^2.
\]

The area density `a` is conserved along each affine null generator. At the observer boundaries,

\[
a=\mathcal W_A=r_{AB}\mathcal W_B,
\]

so G221 is recovered exactly. On the clock-regular stratum, G176 fixes the reciprocal ruler density
to `m=a`, and the completed pair metric is `[[-T^2,-1],[-1,0]]` in its calibrated vertical coframe.

G188's quotient screen is canonically and isometrically the normal plane of this pair surface. Its
quotient connection and tidal operator explicitly intertwine with normal projection, so its matrix
Jacobi response remains a separate normal channel.

## New boundary exposed

The vertical ruler density need not be one global coordinate differential. An exact flat null
ribbon has `a=1+epsilon y` and therefore

\[
d(a\,d\lambda)=\epsilon\,dy\wedge d\lambda\ne0
\]

while retaining the exact G221 frequency ratio and a regular rank-two pair plane. Thus G176's
pointwise/fiberwise density theorem survives, but global ruler-coordinate carry requires a separate
closedness condition.

## Evidence

- preregistered at commit `6df659bf`;
- 10 frozen source hashes;
- 43 symbolic and direct exact checks;
- 12,000 independent finite-algebra Fraction cases and 396,000 exact rational assertions;
- 12,000 screen-isometry, connection-intertwining, tidal-intertwining, and explicit flat-ribbon
  cases each;
- 18 payload-contract field mutations rejected, explicitly not graded as theorem mutation tests;
- complete-tree no-write replay covering the package and all 10 frozen load-bearing sources;
- exact full-sector complete-coframe witness and exact nonclosed flat-ribbon witness.

The general differential-geometric theorem is carried by the written proof; finite rational sampling
is cross-check evidence, not its proof.

## What was not learned

The result does not select null as the universal physical observer relation, populate observers or
branches, aggregate multiple images, produce a global ruler coordinate, choose a complete metric
realization, or derive `X_max`, transfer, observation, action, source, matter, bootstrap, mass, or
signalling.

Current grade:

```text
ACCEPT_WITH_REPAIRS__REPAIR_REVIEW_PENDING
```
