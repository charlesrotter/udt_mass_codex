# G311 exact derivation — full covariant content of Universal Reciprocity

Date: 2026-09-01
Status: `G311_ACCEPTED_WITH_RESPONSE_CONSTITUTION_BOUNDARY`

## 1. Primary landing

```text
FULL_COVARIANT_RECIPROCITY_CLOSES_RESPONSE_SHAPE_ONLY
__RESPONSE_CONSTITUTION_REMAINS_OPEN
```

Strongest conditional consequence:

```text
G301_FAITHFUL_BRANCH_GIVES_EINSTEIN_SPACE_DYNAMICS
```

Universal Reciprocity is Charles Rotter's owner-adopted provisional postulate. It is not derived or
canon. G311 extends its response-shape theorem to every locally admissible regular pair germ without
assuming a physical astronomical population. It does not prove that the postulate selects G301's
response architecture over every higher-order, nonlocal, auxiliary, or source-dependent response.

## 2. Every orthonormal pair plane is a locally admissible observer-pair germ

Let `p` lie in a regular Lorentz manifold `(M,g)`, and let `(u,n)` satisfy

\[
g(u,u)=-1,\qquad g(n,n)=1,\qquad g(u,n)=0,
\]

with `u` future pointing. Define a short spacelike geodesic

\[
\alpha(\sigma)=\exp_p(\sigma n)
\]

and parallel-transport `u` along `alpha` to a unit timelike field `U(sigma)`. For sufficiently small
parameters, set

\[
F(\tau,\sigma)=\exp_{\alpha(\sigma)}\!\bigl(\tau U(\sigma)\bigr).
\]

For each fixed `sigma`, `tau -> F(tau,sigma)` is a timelike geodesic. At `(0,0)`,

\[
F_*\partial_\tau=u,\qquad F_*\partial_\sigma=n.
\]

The derivative has rank two, so `F` is a local immersion after shrinking the domain. Its pullback
metric is Lorentzian near the origin by continuity. Extending `(u,n)` to a local orthonormal tetrad
supplies the two screen directions without changing the pair plane. Thus every orthonormal
timelike--spacelike plane is realized by a regular local freely falling observer-pair germ.

This proves **local kinematic admissibility**. It does not prove that Nature globally populates every
germ, that the surface extends through caustics, or that one global relation network contains every
such pair. Those global questions are unnecessary for a postulate universally quantified over all
locally admissible responses.

## 3. Exact covariant response-shape theorem

The reciprocal tangent on the realized plane is

\[
H(u,n)=2\left(u^\flat\!\otimes u^\flat+n^\flat\!\otimes n^\flat\right).
\]

Its metric trace is zero:

\[
\operatorname{tr}_g H=2[-1+1]=0.
\]

The exact all-plane construction independently rederives

\[
\operatorname{span}\{H(u,n)\}=S^2_0(T_p^*M),\qquad \dim S^2_0=9.
\]

Let `E_ab` be the symmetric covariant response object to which DDR applies, without yet fixing its
formula. Decompose it invariantly as

\[
E_{ab}=E^{\mathrm{TF}}_{ab}+\frac14(\operatorname{tr}_gE)g_{ab},
\qquad
E^{\mathrm{TF}}_{ab}=E_{ab}-\frac14(\operatorname{tr}_gE)g_{ab}.
\]

Because the trace line is orthogonal to every reciprocal tangent,

\[
\langle E,H\rangle_g=\langle E^{\mathrm{TF}},H\rangle_g.
\]

The metric pairing restricted to `S^2_0` is nondegenerate. Universal Reciprocity/DDR on every
locally admissible pair therefore gives the fully covariant pointwise equation

\[
\boxed{E^{\mathrm{TF}}_{ab}=0}
\]

or equivalently

\[
\boxed{E_{ab}=\lambda(x)g_{ab}.}
\]

No chart, symmetry reduction, action, source, observation, mass law, scale, or `X_max` entered.
The trace-free projector was also checked under an exact rational Lorentz boost.

### Rank-deficient boundary

If the admissible pair-tangent span has rank `r`, the balance supplies `r` independent functionals
on the nine-dimensional response-shape space. Exactly

\[
\boxed{9-r}
\]

shape directions remain. The production census verifies every rank from one through nine. A single
radial pair has rank one and leaves eight shape directions; it cannot support the full equation.

## 4. Pointwise balance does not by itself make the trace constant

Metricity gives

\[
\nabla^a(\lambda g_{ab})=\nabla_b\lambda.
\]

Therefore the additional identity `nabla^a E_ab=0` would imply `d lambda=0` on each connected
region. Diffeomorphism covariance alone does not supply this identity. It follows for some response
architectures—for example from a separately owned diffeomorphism-invariant action—but no such
action is active here.

The exact counterfamily

\[
E_{ab}=\lambda(x)g_{ab}
\]

satisfies every pointwise reciprocal balance for an arbitrary smooth nonconstant `lambda`. G311
therefore does not promote the retained trace into a connected constant at the response-agnostic
level.

## 5. Conditional G301 faithful-response branch

Inside G301's explicit lane,

\[
E_{ab}=aR_{ab}+bR g_{ab},
\]

where the response is smooth at the flat quiet point, scale-free of curvature weight one, local and
metric-only through curvature order, symmetric rank two, and has `a != 0`. Then

\[
E^{\mathrm{TF}}_{ab}
=a\left(R_{ab}-\frac14R g_{ab}\right).
\]

Universal Reciprocity gives

\[
\boxed{R_{ab}-\frac14R g_{ab}=0.}
\]

The contracted Bianchi identity then yields

\[
\nabla_bR=0,
\qquad
R=R_0,
\qquad
\boxed{R_{ab}=\frac{R_0}{4}g_{ab}.}
\]

This is an exact nonlinear covariant equation. It has the mathematical form of an Einstein-space
condition, but it was reached here from the adopted reciprocal balance plus the conditional G301
response classification, not by importing a GR field equation. `R0` is a connected solution datum,
not an inserted cosmological term or calibrated value.

## 6. What “history” becomes on the conditional branch

Write `Lambda=R0/4` only as shorthand for the connected scalar datum. In harmonic coordinates the
principal part is

\[
R_{\mu\nu}
=-\frac12g^{\rho\sigma}\partial_\rho\partial_\sigma g_{\mu\nu}
+Q_{\mu\nu}(g,\partial g),
\]

so `R_mn=Lambda g_mn` is a quasilinear hyperbolic metric system after coordinate gauge is fixed.
On a spacelike initial slice, the induced metric `gamma_ij` and extrinsic curvature `K_ij` obey

\[
{}^{(3)}R+K^2-K_{ij}K^{ij}=2\Lambda,
\]

\[
D_j(K^{ij}-\gamma^{ij}K)=0.
\]

The 12 initial components, four constraints, and four coordinate-gauge directions leave four local
phase-space degrees of freedom, or two metric configuration degrees of freedom per spatial point,
plus the one connected scalar datum. This is the standard geometric Cauchy count applied to the
conditionally derived equation; it imports no GR source or physical interpretation.

Accordingly, a field law need not choose one unique universe. It specifies which evolving metrics
are lawful; admissible initial data select one history. On the primary static-spherical branch, the
functional freedom correspondingly collapses to

\[
f(r)=1+\frac br-\frac{R_0}{12}r^2,
\]

where `b` is Weyl/initial-state data and `R0` is the connected scalar datum. Neither is fixed by
Universal Reciprocity alone.

## 7. Why covariance alone does not select the G301 response

Consider the smooth time-live metric

\[
g_b=-dt^2+e^{2bt^2}(dx^2+dy^2+dz^2).
\]

The independent Christoffel/Riemann calculation gives

\[
R=12b(1+4bt^2),
\]

and

\[
S_{ab}=R_{ab}-\frac14Rg_{ab}
=\operatorname{diag}\!\left(-3b,-be^{2bt^2},-be^{2bt^2},-be^{2bt^2}\right).
\]

For `b != 0`, the Ricci response fails full-plane DDR. The same direct calculation gives

\[
C_{abcd}=0.
\]

Hence the higher-curvature natural symmetric response

\[
Q_{ab}=C_{acde}C_b{}^{cde}
\]

vanishes and satisfies every reciprocal balance on the same non-Einstein metric. This is not a
competitor inside G301: it has higher curvature weight, zero quiet principal response, and is
excluded by G301's declared class. It is a decisive counterexample to the stronger claim that
covariance plus Universal Reciprocity alone chooses Ricci as the response.

## 8. Exact remaining premise boundary

Existing UDT structure strongly supports—but does not yet derive—the G301 lane:

- G296 derives that curvature is the first local natural nonidentity home for a metric-only law;
- W3 requires a nondegenerate GR field limit in the quiet regime;
- W4 supplies one complete metric for clocks, rulers, free fall, null response, and screens;
- the absence of an owned vacuum length plus smooth curvature-weight-one behavior removes local
  nonlinear curvature dressings inside G301.

What remains unowned is the global law-level declaration that the **complete** UDT response stays in
that conservative local curvature-order, metric-only, smooth scale-free rank-two class, rather than
acquiring higher-order, nonlocal, auxiliary, source, or singular contributions away from the quiet
regime. Universal Reciprocity then fixes its trace-free zero set, but does not choose this response
constitution merely by being covariant.

## 9. Completeness ledger

This is one full-local-metric tile, not a global-universe classification. It covers all ten metric
components, all locally admissible pair planes, and no symmetry reduction. It drops singular and
caustic strata, global topology and completion, actual observer population, sources, matter, mass,
observations, boundaries, absolute scale, and physical `X_max`. Those omissions cannot be promoted
to negatives.

No metric component, reciprocal kernel, angular orchestra, or terminal readout changed. Screen,
angular, shift, and mixing data remain part of the complete metric/pair pullback upstream of DDR.
