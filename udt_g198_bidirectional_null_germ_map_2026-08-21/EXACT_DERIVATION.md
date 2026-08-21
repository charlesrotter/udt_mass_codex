# G198 exact derivation — two opposite null germs on one metric

Date: 2026-08-21

## Declared family

G198 changes no metric input from G196:

\[
\theta^0=a(\eta)d\eta,\qquad
\theta^1=a(\eta)dz,\qquad
\theta_{\rm screen}=a(\eta)\left[dX+M(\eta,z)X(d\eta+dz)\right],
\]

where `a>0` and `M` is an arbitrary real `2x2` `C2` field in this chosen family. On `X=0`,

\[
h=a^2(-d\eta^2+dz^2),\qquad \det E=a^4,\qquad \det g=-a^8.
\]

The two supplied future null tangents are

\[
k_\pm=a^{-2}(\partial_\eta\pm\partial_z).
\]

The production code constructs the full metric, inverse, Christoffels, and Riemann tensor before
contracting either tangent. It does not obtain the minus result by `z -> -z`.

## Direct metric results

Both tangents are affine null geodesics and have the same positive unit-clock frequency,

\[
\nabla_{k_\pm}k_\pm=0,
\qquad
-g(a^{-1}\partial_\eta,k_\pm)=a^{-1}.
\]

Write

\[
M=S+\Omega,\qquad S^T=S,\qquad \Omega^T=-\Omega,
\]

and

\[
\tau_0=\frac{H^2-H'}{a^4},\qquad H=\frac{a'}a.
\]

For the outgoing germ the direct reconstruction exactly regresses G196:

\[
C_{+,s}=2\Omega,
\]

\[
T_+=\tau_0I+a^{-4}\left(2D_+S-4S^2-4[S,\Omega]\right),
\qquad D_+=\partial_\eta+\partial_z.
\]

For the opposite germ the result is instead

\[
\boxed{C_{-,s}=0},
\]

\[
\boxed{T_-=\tau_0I}.
\]

Thus every `M`-dependent screen connection and tide term vanishes on the incoming germ, while the
common conformal-scale tide remains. The result is asymmetric because the declared metric coframe
contains `M X(deta+dz)` and no independent `deta-dz` screen component.

Both tides are self-adjoint in the physical screen metric.

## Direct coordinate Jacobi equations

For a coordinate screen vector `Y`, direct evaluation of

\[
\nabla_k\nabla_kY+R(Y,k)k
\]

gives the outgoing G196 operator

\[
(D_+-2M^T)(D_++2M)Y=0,
\]

and the exact incoming control

\[
\boxed{D_-^2Y=0},
\qquad D_-=\partial_\eta-\partial_z.
\]

Let `u` be the null coordinate with `d/du=D_-`; the affine tangent is `k_-=a^-2D_-`. With the
parent normalization `a(0)=1`, the vertex-normalized coordinate solution is `Y_-(u)=uI`. The
orthonormal-screen physical Jacobi map is

\[
D_-(u)=a(u)uI.
\]

Therefore

\[
\det D_-(u)=a(u)^2u^2>0
\]

for every nonvertex point of a connected regular incoming interval. This is an exact sign proof,
not a finite sample inference.

## What the two rays do not determine

For any fixed real matrix coefficient, the field perturbation

\[
\Delta M=(\eta-z)^2(\eta+z)^2 C
\]

and its first relevant directional derivative vanish on both rays `z=eta` and `z=-eta`, but it is
nonzero off their union. Hence the two-germ result cannot reconstruct arbitrary `M(eta,z)`.

## Exact landing

```text
OPPOSITE_GERM_NULL_CONTROL__ASYMMETRY_IS_METRIC_ENCODED
```

This is a conditional theorem for the displayed G196 family and the two supplied central germs.
It is not a universal claim that one direction in UDT must be quiet.
