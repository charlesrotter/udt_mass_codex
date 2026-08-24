# G245 exact derivation — metric-owned observer null-cone field

Date: 2026-08-24

## Scope and conventions

Let `(M,g)` be a smooth, time-oriented Lorentzian four-manifold with signature `(-,+,+,+)`. Supply
one observer event `o` and one future metric-unit clock vector `U in T_o M`, so

\[
g(U,U)=-1.
\]

This is a local metric theorem. The complete metric history, the observer germ, and the future-cone
orientation are supplied. No source population, endpoint incidence, preferred ray, detector law,
observational outcome, `X_max`, or fitted coefficient enters.

## 1. The metric and observer own the entire local direction fiber

The rest space

\[
E_o=U^\perp
\]

has a positive-definite metric induced by `g`. Its unit sphere

\[
\mathbb S_o^2=\{n\in E_o:g(n,n)=1\}
\]

is the observer's celestial direction sphere. For every `n in S_o^2`, define

\[
k(n)=U+n.
\]

Then

\[
g(k,k)=-1+1=0,
\qquad -g(U,k)=1.
\]

Conversely, let `ell` be any future null vector at `o` in a specified null direction. Its uniquely
normalized representative is

\[
k=\frac{\ell}{-g(U,\ell)}.
\]

Writing `k=U+n` gives `n in U^perp` and `g(n,n)=1`. Therefore

\[
\boxed{
\mathbb S_o^2\longleftrightarrow
\{\text{future null rays at }o\},
\qquad n\longmapsto U+n
}
\]

is a bijection after the observer normalization `-g(U,k)=1`. The construction returns all
directions; it selects none of them as preferred.

## 2. The exponential map generates the local cone

On the domain on which the metric exponential map exists, define

\[
F(\lambda,n)=\operatorname{Exp}_o\!\bigl(\lambda k(n)\bigr),
\qquad \lambda\ge 0.
\]

For fixed `n`, `lambda -> F(lambda,n)` is the unique affinely parametrized null geodesic with
initial tangent `k(n)`. For sufficiently small `lambda>0`, the map has rank three and parametrizes
the punctured local future null cone. The vertex at `lambda=0` is intentionally singular as an
angular parametrization because all directions meet there.

The maximal parametrized domain ends direction by direction if the exponential map ceases to
exist. Angular rank can fail at a conjugate point. Distinct direction labels can also reach the
same spacetime point at a cut or self-intersection without erasing their distinct labels. None of
these facts supplies a global branch-aggregation rule.

## 3. Angular differentiation is the vertex Jacobi map

Take `v in T_n S_o^2` and vary `n` through a curve with tangent `v`. The angular derivative

\[
J_v(\lambda)=d_nF(\lambda,n)[v]
\]

is the variation field of a geodesic family. With `k=partial_lambda F`, it obeys the exact Jacobi
equation

\[
\frac{D^2J_v}{d\lambda^2}+R(J_v,k)k=0,
\]

with vertex data

\[
J_v(0)=0,
\qquad
\frac{DJ_v}{d\lambda}(0)=v.
\]

Choose parallel orthonormal screen bases along a ray. The screen components form the G188 matrix
Jacobi map `D(lambda)` and tidal matrix `T(lambda)`:

\[
D''+TD=0,
\qquad D(0)=0,
\qquad D'(0)=I,
\qquad T^\dagger=T.
\]

Thus G188's formerly conditional screen propagator is not an extra angular mechanism on this local
cone: it is the angular differential of the metric exponential map.

## 4. G244 area and shape are induced cone geometry

Let `F_lambda(n)=F(lambda,n)`. The angular pullback metric on a regular constant-affine cut is

\[
H=F_\lambda^*g=D^\dagger D.
\]

Consequently

\[
\det H=(\det D)^2,
\qquad
A=|\det D|,
\qquad
C=\frac{H}{A},
\qquad
\det C=1
\]

where `D` is invertible. The scalar shape magnitude used in G244 is

\[
\mathfrak s=\frac{(\operatorname{tr}C)^2}{4}-1
=\frac{(\operatorname{tr}H)^2}{4\det H}-1\ge 0.
\]

It vanishes exactly when the two singular values of `D` agree. These are properties of the induced
cone cut, not a post-readout correction and not a fitted angular template.

Under passive endpoint and initial `O(2)` screen changes,

\[
D\mapsto Q_e^\dagger DQ_o,
\qquad
H\mapsto Q_o^\dagger HQ_o.
\]

Therefore `A` and `s` are scalar invariants and `C` is an observer-sky tensor. The sign of `det D`
is not an ordinary scalar under reflections; it is orientation-line valued.

## 5. Exact native evolution

Set

\[
V=D'.
\]

Then the complete first-order system is

\[
D'=V,
\qquad
V'=-TD.
\]

Its Wronskian

\[
W=D^\dagger V-V^\dagger D
\]

is conserved. The vertex data make `W=0`. Direct differentiation gives

\[
H'=V^\dagger D+D^\dagger V,
\]

\[
H''=2V^\dagger V-2D^\dagger TD.
\]

On a regular stratum define the optical matrix

\[
B=VD^{-1}.
\]

Wronskian zero makes `B` self-adjoint, and

\[
B'=-T-B^2.
\]

Write

\[
B=\frac{\theta}{2}I+\Sigma,
\qquad \operatorname{tr}\Sigma=0,
\qquad
\widehat T=T-\frac{\operatorname{tr}T}{2}I.
\]

The exact two-screen-dimensional equations are

\[
\theta'=-\operatorname{tr}T-\frac{\theta^2}{2}
-\operatorname{tr}(\Sigma^2),
\]

\[
\Sigma'=-\theta\Sigma-\widehat T,
\]

\[
A'=\theta A,
\qquad
C'=\frac{2}{A}D^\dagger\Sigma D.
\]

No linearization is used. These equations show how the metric tide drives area and shape, but they
do not turn `H` into an autonomous state. Exact controls with the same `H` and `H'` but different
orientation of `D` relative to anisotropic `T` have different `H''`. The full phase data must be
retained.

## 6. Exact vertex classification

For

\[
T(\lambda)=T_0+\lambda T_1+O(\lambda^2),
\]

the vertex initial-value problem gives

\[
D=\lambda I-\frac{\lambda^3}{6}T_0
-\frac{\lambda^4}{12}T_1+O(\lambda^5),
\]

\[
H=\lambda^2\left[
I-\frac{\lambda^2}{3}T_0
-\frac{\lambda^3}{6}T_1+O(\lambda^4)
\right],
\]

\[
A=\lambda^2\left[
1-\frac{\lambda^2}{6}\operatorname{tr}T_0
-\frac{\lambda^3}{12}\operatorname{tr}T_1+O(\lambda^4)
\right],
\]

\[
C=I-\frac{\lambda^2}{3}\widehat T_0
-\frac{\lambda^3}{6}\widehat T_1+O(\lambda^4).
\]

Hence the leading scalar shape magnitude is

\[
\mathfrak s
=\frac{\lambda^4}{18}\operatorname{tr}(\widehat T_0^2)
+O(\lambda^5).
\]

This is a local series theorem only. It does not prescribe finite-distance loudness, a cosmological
history, or a feature scale.

## 7. Degenerate strata and full-phase carry

The exact control

\[
D(\lambda)=\operatorname{diag}(\sin\lambda,\lambda)
\]

has rank one at `lambda=pi`. There

\[
H=\operatorname{diag}(0,\pi^2)
\]

is still a lawful semidefinite pullback tensor. The signed determinant

\[
\Delta=\lambda\sin\lambda
\]

crosses zero with slope `-pi`, so `A=|Delta|` has a cusp and normalized `C=H/A` is undefined at the
caustic. The full four-by-four Jacobi phase remains symplectic and invertible, with determinant one.
Neither `D^{-1}` nor multiplication of position blocks is allowed there.

## Landing and exact ceiling

```text
OBSERVER_GERM_AND_METRIC_OWN_LOCAL_DIRECTION_LABELLED_NULL_CONE_FIELD
__G244_AREA_SHAPE_ARE_INDUCED_CONE_GEOMETRY
__SOURCE_POPULATION_GLOBAL_BRANCH_AND_PHYSICAL_HISTORY_REMAIN_OPEN
```

The theorem removes one piece of scaffolding: a separate local null-sheet choice is unnecessary
once `(g,o,U)` is supplied. It does not select the physical metric history, the population of
observers or sources, the endpoints that Nature populates, a detector/transfer law, or a global
rule across cuts, caustics, and incomplete rays.
