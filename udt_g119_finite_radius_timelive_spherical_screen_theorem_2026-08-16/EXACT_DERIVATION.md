# G119 exact derivation — finite-radius time-live spherical screen theorem

Date: 2026-08-16

## 1. Declared geometry and query

Let a supplied smooth time-oriented spherically symmetric spacetime be a warped product

\[
(M,g)=(B^2,h)\times_R(S^2,\gamma),
\qquad
g=h_{ab}(x)dx^a dx^b+R(x)^2\gamma_{AB}d\vartheta^A d\vartheta^B.
\tag{1}
\]

Here `R>=0` is the areal radius. Supply a regular center event `p`, a unit central observer
velocity `u_o`, and one radial null initial vector `K_o` normalized by

\[
g(K_o,K_o)=0,\qquad -g(K_o,u_o)=1.
\tag{2}
\]

The point-observer exponential query gives one affinely parameterized radial null geodesic
`gamma(lambda)`. The theorem is branchwise; it does not select this history or query as universal.

## 2. Rotational variations construct the screen

Choose two infinitesimal rotations `X_1,X_2` whose values at the initial sky direction form an
orthonormal basis of the unit-sphere tangent plane. Their spherical action lifts to spacetime
isometries `Psi_A(s)`. Since every rotation fixes the regular center, the families

\[
\gamma_{A,s}(\lambda)=\Psi_A(s)\gamma(\lambda)
\]

are geodesic variations with the same vertex. Their variation fields

\[
J_A=\left.\frac{\partial\gamma_{A,s}}{\partial s}\right|_{s=0}
\tag{3}
\]

therefore satisfy the exact Jacobi equation

\[
\nabla_K\nabla_KJ_A+\operatorname{Riem}(J_A,K)K=0.
\tag{4}
\]

On an interval with `R>0`, let `Xi_A` be the lifted angular field and define

\[
E_A=\frac{\Xi_A}{R}.
\]

The warped-product connection gives

\[
\nabla_K\Xi_A=\frac{K(R)}{R}\Xi_A,
\qquad
\nabla_KE_A=0.
\tag{5}
\]

Thus `(E_1,E_2)` is a parallel orthonormal screen and the rotational Jacobi fields are exactly

\[
\boxed{J_A=R E_A.}
\tag{6}
\]

At a regular center it is cleaner to continue a signed warping amplitude `rho` through the center,
with `|rho|=R`. Elementary flatness and (2) give

\[
\rho(0)=0,\qquad \dot\rho(0)=1
\tag{7}
\]

for the outgoing orientation. Hence (6) has precisely the point-observer vertex conditions
`D(0)=0`, `D_KD(0)=I` in matched orthonormal sky and parallel-screen bases. An affine rescaling
changes the derivative with respect to affine parameter but not the map from unit sky angle to
physical endpoint separation.

## 3. Independent curvature route

The projection of a radial geodesic to `(B,h)` is an affinely parameterized `h`-geodesic. The mixed
warped-product curvature is

\[
\operatorname{Riem}(E_A,K)K
=-\frac{\nabla^h_K\nabla^h_KR}{R}E_A
=-\frac{\ddot R}{R}E_A.
\tag{8}
\]

Therefore the screen tidal matrix is

\[
\mathcal R_\perp=-\frac{\ddot R}{R}I_2,
\tag{9}
\]

and direct substitution of `D=R I_2` gives

\[
\ddot{\mathcal D}+\mathcal R_\perp\mathcal D=0.
\tag{10}
\]

`derive_spherical_screen.py` independently reconstructs the relevant four-dimensional Christoffel
and Riemann components for generic functions `A(t,r),B(t,r),R(t,r)` and obtains the exact residual

\[
R^\theta{}_{a\theta b}K^aK^b+\frac{\ddot R}{R}=0.
\]

No field equation, staticity assumption, weak-field expansion, or fitted profile enters either
route.

## 4. Basis-covariant theorem

In matched bases, (6) is `D_sky=rho I_2`. Under independent passive orthonormal changes `Q_o` of
the observer sky basis and `Q_s` of the endpoint screen basis,

\[
\mathcal D\longmapsto Q_s^T\mathcal D Q_o
=R\,O,
\qquad O\in O(2),
\tag{11}
\]

where the sign of `rho` can be absorbed into `O`. Consequently, on every regular branch,

\[
\boxed{\mathcal D_{\rm sky}=R O,\quad O\in O(2),\quad
|\det\mathcal D_{\rm sky}|=R^2.}
\tag{12}
\]

The signed determinant is `R^2 det(O)` and changes under an orientation-reversing basis choice.
The absolute determinant is the basis-free physical screen area. If orientations and their carry
are fixed consistently, `O` lies in `SO(2)`.

On the invertible stratum, the optical matrix in a parallel screen frame is

\[
\mathfrak B=(D_K\mathcal D)\mathcal D^{-1}
=\frac{K(R)}{R}I_2.
\tag{13}
\]

Its shear, physical twist, and trace-free screen strain vanish exactly. A changing passive screen
frame may add an antisymmetric connection term but cannot change (12).

## 5. Complete stratum classification

| Stratum | `D_sky` | Rank | Correct carrier/conclusion |
|---|---:|---:|---|
| observer coincidence | `0` | 0 | vertex condition; `D_KD=I` in matched normalized bases |
| regular finite branch, `R>0` | `R O` | 2 | exact theorem (12); inverse/Riccati chart lawful |
| areal turning point, `K(R)=0`, `R>0` | `R O` | 2 | zero expansion, not a caustic |
| regular spherical caustic, `R=0` | `0` | 0 | retain full phase `(D,D_KD)`; inverse/Riccati diverges |
| orientation-reversed basis | `R O`, `det O=-1` | 2 | signed determinant flips; absolute area unchanged |
| multiple radial preimages | one `R O_b` per branch `b` | branchwise | no metric-derived occupancy or aggregation weight |

There is no rank-one caustic in this exact central spherical class. At a finite regular caustic,
the signed amplitude cannot satisfy `rho=dot rho=0`: uniqueness for the regular scalar Jacobi ODE
would then force `rho` to vanish identically, contradicting (7). Hence the position block collapses
while the phase carrier survives. The exact control `rho=sin(lambda)` at `lambda=pi` realizes this
with position rank zero and derivative rank two.

The theorem is local-to-branch and does not claim that a global screen section exists. Multiple
exponential preimages remain multiple branches even when their area determinants agree.
Passage through another regular center is precisely another `R=0` rank-zero spherical-caustic
event in this classification; a signed amplitude continues the phase carrier onto the next branch.

## 6. Explicit time-live control

The independent verifier uses the nonstatic flat-FLRW metric

\[
ds^2=-dt^2+(1+t)^2\left(dr^2+r^2d\Omega^2\right).
\tag{14}
\]

With the central normalization in (2), an outgoing affine radial ray is

\[
s=\sqrt{1+2\lambda},\qquad t=s-1,\qquad r=\log s,
\]

and its areal radius is

\[
R(\lambda)=s\log s.
\tag{15}
\]

Direct coordinate curvature gives

\[
\mathcal R_\perp=(1+2\lambda)^{-2}I_2.
\]

The null, affine geodesic, Jacobi, and vertex residuals vanish exactly. A separate DOP853
integration on 1,201 points through `lambda=12` reproduces (15) with maximum absolute error
`8.991030142624368e-12` against a preregistered `2e-10` tolerance.

## 7. Radiometric and SNe regrade

G94's regular single-branch theorem is

\[
F_o=\frac{L_\Omega\mathcal T}{Z_\omega^3d_A^2}.
\]

Equation (12) now makes its central-spherical time-live specialization exact at arbitrary finite
radius:

\[
\boxed{F_o=\frac{L_\Omega\mathcal T}{Z_\omega^3R^2}.}
\tag{16}
\]

This removes an independent tensor-valued isotropic P1 screen ansatz on the declared class. It does
not remove the scalar history or transfer. The frozen P1 luminosity curve still constrains only

\[
\frac{R(Z)}{\sqrt{\mathcal T(Z)}}
=n\sqrt Z\left(1-Z^{-2/n}\right)
\tag{17}
\]

after the conditional release-frequency adoption and source calibration. Transparent transfer
`T=1/Z` remains an additional conditional closure, not a consequence of (12).

## 8. Bounded landing

```text
FINITE_RADIUS_TIMELIVE_CENTRAL_SPHERICAL_SCREEN_THEOREM_DERIVED
__D_SKY_EQUALS_R_TIMES_O2_ON_EVERY_REGULAR_BRANCH
__ABS_DETERMINANT_EQUALS_R_SQUARED
__ZERO_SHEAR_AND_NO_RANK_ONE_CAUSTIC
__FULL_PHASE_CARRIER_SURVIVES_REGULAR_CAUSTICS
__INDEPENDENT_P1_SCREEN_MATRIX_REMOVED_IN_DECLARED_CLASS
__TRANSFER_RADIUS_FREQUENCY_HISTORY_QUERY_AND_GLOBAL_SELECTION_OPEN
```

No physical history, observed-redshift protocol, source transfer, SNe outcome, `X_max`, bootstrap,
action, matter, mass, or signalling law is derived.
