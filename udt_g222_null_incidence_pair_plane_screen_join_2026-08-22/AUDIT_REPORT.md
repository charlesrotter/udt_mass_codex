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
matrix Jacobi response remains a separate normal channel.

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
- 38 symbolic and direct exact checks;
- 12,000 independent Fraction cases and 276,000 exact checks;
- 12,000 screen-isometry, affine-reparameterization, and integrability-boundary cases each;
- 18 injected algebraic, semantic, and ownership mutations rejected;
- exact full-sector complete-coframe witness and exact nonclosed flat-ribbon witness.

## What was not learned

The result does not select null as the universal physical observer relation, populate observers or
branches, aggregate multiple images, produce a global ruler coordinate, choose a complete metric
realization, or derive `X_max`, transfer, observation, action, source, matter, bootstrap, mass, or
signalling.

Current grade:

```text
INDEPENDENTLY_VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_REVIEW_PENDING
```
