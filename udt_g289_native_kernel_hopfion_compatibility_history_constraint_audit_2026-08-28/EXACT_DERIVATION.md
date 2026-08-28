# G289 exact derivation — Hopfion compatibility and history restriction

Date: 2026-08-28

## 1. Fresh scope

The current metric is the theory. The old Hopfion reports are used only to type the comparison
object: a static unit-vector field with fixed round target `S2`, conditional `L2+L4` energy, and
fixed computational boundary. No old formula proves the bridge below.

## 2. Local null-direction embedding

Let `U` be a supplied unit timelike observer and `(e1,e2,e3)` a supplied orthonormal spatial frame.
For any unit component vector `n`,

\[
k=U+n^i e_i,
\qquad n^i n_i=1,
\]

satisfies

\[
g(k,k)=g(U,U)+n^i n^j g(e_i,e_j)=-1+1=0.
\]

Thus every unit-vector configuration can be embedded locally as a section of the projectivized
null cone after an observer/frame is supplied. This works for every regular metric, including every
positive primary profile `f(r)` and every analytic-even G288 center germ. It fixes only a null
direction; it does not supply pair depth, projective magnitude, branch population, or history.

## 3. Celestial sphere versus fixed round target

A Lorentz boost preserves the null-line sphere but does not act as a round-sphere isometry. For a
boost of speed `beta` in the third direction,

\[
n'_\perp=\frac{n_\perp}{\gamma(1-\beta n_3)},
\qquad
n'_3=\frac{n_3-\beta}{1-\beta n_3}.
\]

For every tangent variation `dn` on the unit sphere,

\[
|dn'|^2=\frac{|dn|^2}{\gamma^2(1-\beta n_3)^2}.
\]

The map is conformal, but its factor varies with direction. The exact witness
`beta=3/5`, `gamma=5/4`, `n=(1,0,0)` scales both tangent norms by `16/25` and a squared two-area by
`256/625`. Therefore the historical fixed round-target `L2` and `L4` densities do not descend from
the null-line conformal sphere without supplying an observer reduction and a target metric.

A constant global boost still induces an orientation-preserving target diffeomorphism, so this fact
does not by itself erase the integer Hopf class. It does show that the historical energy/stability
functional is not owned by the observer-independent null cone.

## 4. Frame-gauge obstruction to raw component charge

There is a stronger global distinction. Write a unit quaternion as `q=(a,b,c,d)`. Rotating one
constant component direction by the local frame map `Ad_q` gives

\[
n(q)=\left(
2(bd+ac),
2(cd-ab),
a^2-b^2-c^2+d^2
\right).
\]

Direct algebra gives `|n(q)|=1`. Its north and south fibers are

\[
q=(\cos u,0,0,\sin u),
\qquad
q=(0,\cos u,\sin u,0),
\]

the standard linked Hopf circles. A fresh Hopf-coordinate calculation gives
`|integral(A wedge dA)|=4 pi^2`, hence unit charge in the registered normalization.

The map `Ad_q:S3->SO(3)` is identity at the compactification basepoint and is an allowed smooth
large local frame rotation unless an additional framing restriction is imposed. Consequently a
constant component section can be represented with raw component Hopf class zero in one
trivialization and magnitude one in another. Equivalently, the fibration

\[
SO(2)\longrightarrow SO(3)\longrightarrow S^2
\]

induces an isomorphism `pi3(SO(3))->pi3(S2)`.

Therefore the fixed-target component Hopf integer does not descend through the full local frame
gauge currently allowed by the projective/frame-carried kernel. A boundary framing, restricted
gauge class, or connection-dependent invariant could repair this, but none is presently derived.

## 5. Exact history counterfamily

On a bounded spatial ball, take

\[
g_\alpha=e^{2\alpha r^2}\eta.
\]

Every member is regular, time-oriented, and has exactly the same null lines. The same geometric
null-direction texture therefore embeds in every member. Yet their scalar curvature at the center
is

\[
R[g_\alpha](0)=-36\alpha.
\]

The members are geometrically inequivalent. All current pullback, frame-carry, metricity, Cartan,
and composition identities continue to evaluate each supplied metric. Hence existence of the null
texture does not reject any member and is not a nonidentity history law.

The same conclusion is visible inside the primary family: the orthonormal-frame embedding works for
every positive `f(r)`, so it constrains none of G288's coefficients `c2,c4,...`.

## 6. Status of the earlier stability result

The historical corrected no-null field is not algebraically inconsistent with UDT. It can be
embedded on a supplied quiet/static background after choosing an observer, spatial trivialization,
round target, constant exterior, `L2+L4` functional, and fixed boundary. Its static finite-box
stability remains valid only under those conditional premises.

What has not been shown is that:

- the metric selects the carrier section or framing;
- the historical action descends from the kernel;
- the configuration remains stable on a dynamic or curved UDT history;
- the field backreacts on the metric; or
- topological persistence rejects one of the conformal or G286 history twins.

## 7. Exact landing

```text
LOCAL_NULL_DIRECTION_EMBEDDING_EXISTS
__FIXED_ROUND_S2_HOPFION_REQUIRES_SUPPLIED_FRAME_TARGET_AND_BOUNDARY
__RAW_HOPF_CLASS_DOES_NOT_DESCEND_THROUGH_FULL_LOCAL_FRAME_GAUGE
__CONFORMAL_HISTORY_TWINS_CARRY_THE_SAME_NULL_TEXTURE
__STATIC_HOPFION_IS_CONDITIONALLY_COMPATIBLE_NOT_A_CURRENT_HISTORY_SELECTOR
```

This is a mixed result: local compatibility is positive; native carrier ownership and present
history selection are negative at the declared scope. A future gauge-covariant section/connection
and time-live persistence law could change the second conclusion.
