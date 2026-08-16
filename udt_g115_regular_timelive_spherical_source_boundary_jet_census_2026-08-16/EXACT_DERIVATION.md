# G115 exact derivation — regular time-live spherical source-boundary jets

Date: 2026-08-16

## 1. Complete smooth central two-jet

Use the dimension-matched coordinate `T=c_E t`. On a regular spherical `X>0` center patch, central
proper time and local areal radius put the metric into

\[
g=-N^2dT^2+L^2(dR+\beta dT)^2+R^2d\Omega^2.
\]

A smooth rotationally invariant scalar is even in signed radial distance, while the coefficient of
a smooth radial vector is odd. Elementary flatness and central proper-time normalization therefore
give, at a chosen central event,

\[
N=1+n(T)R^2+O(R^4),\qquad
L=1+\ell(T)R^2+O(R^4),\qquad
\beta=b(T)R+O(R^3).
\]

The functions `n`, `ell`, and `b` are free coordinate representatives of metric-history jets. Their
dimensions in the `T,R` length chart are `L^-2`, `L^-2`, and `L^-1`; `dot b=d b/dT` has dimension
`L^-2`. The observed
`c_E` fixes the clock/ruler conversion used by `T`; no scale-neutrality premise is used.

This gauge is not fully fixed. The residual areal-time slicing

\[
T'=T+a(T)R^2+O(R^4)
\]

preserves the declared form and sends

\[
\begin{aligned}
b'&=b+2a,&
\ell'&=\ell-2ab-2a^2,&
n'&=n+2ab+2a^2-\dot a,\\
\dot b'&=\dot b+2\dot a,&
q'&=q+2a,&
\dot q'&=\dot q+2\dot a.
\end{aligned}
\]

The individual letters are therefore not invariants. The combinations used below are

\[
\ell-n+b^2-\dot b/2,\quad 2\ell+b^2,\quad 2\ell+2n+\dot b,
\]

\[
b-q,\quad b^2/2-n+\dot b/2-\dot q.
\]

Direct symbolic substitution verifies all five are invariant under the residual slicing.

## 2. One complete observer map

For the outgoing central radial-null branch, write

\[
F(\tau,R,\vartheta)
=\bigl(T(\tau,R),R,n_{\rm sky}(\tau,\vartheta)\bigr).
\]

The exact null equation is

\[
\frac{\partial T}{\partial R}=\frac{L}{N-L\beta}.
\]

At `tau=0`, direct series solution gives

\[
T=R+\frac b2R^2
+\frac{b^2+\ell-n+\dot b}{3}R^3+O(R^4),
\qquad
T_\tau=1+\frac{\dot b}{2}R^2+O(R^3).
\]

Let

\[
w_A=(\partial_\tau n_{\rm sky})_A,\qquad w^2=\gamma^{AB}w_Aw_B.
\]

This is lawful celestial-query data only when labels are tied to an independently supplied
instrument or sky-transport protocol: holding such an actively carried label fixed traces a
different pair surface than holding a nonrotating carried label fixed. Under a passive
time-dependent relabeling of the same celestial sphere, `w_A` changes inhomogeneously and can be
removed locally; its contribution is then label gauge. It is not identified with the historical
scalar `mu_lock`.

In a matched orthonormal angular basis, the full pullback has blocks

\[
\mathcal H=F^*g=
\begin{pmatrix}
h_\parallel&C\\
C^T&h_\angle
\end{pmatrix},
\]

with

\[
\begin{aligned}
h_{00}&=-1+\left(b^2-\dot b-2n+w^2\right)R^2+O(R^3),\\
h_{01}&=-1-\left(\ell+n+\frac{\dot b}{2}\right)R^2+O(R^3),\\
h_{11}&=0,\\
C_{0A}&=R^2w_A+O(R^3),\qquad C_{1A}=0,\\
h_{AB}&=R^2\gamma_{AB}.
\end{aligned}
\]

Thus the angular and mixed data enter before the fixed-label terminal readout. Nothing has been
appended after the pair metric was constructed.

## 3. Three distinct scalar channels

The regular calibrated terminal decomposition gives

\[
\kappa_{\rm pair}
=\frac12\left(\ell+n+\frac{\dot b}{2}\right)R^2+O(R^3),
\]

\[
\boxed{
\phi_{\rm pair}^{\rm fixed\ label}
=\frac12\left(\ell-n+b^2-\frac{\dot b}{2}+w^2\right)R^2+O(R^3)
}.
\]

If the angular directions are instead orthogonally quotiented by the Schur complement, the
`w^2` term cancels:

\[
\phi_{\rm pair}^{\rm quotient}
=\frac12\left(\ell-n+b^2-\frac{\dot b}{2}\right)R^2+O(R^3).
\]

These are two different, precisely typed query/reduction choices. The present derivation does not
promote one as the universal mixed-geometry scalar.

Independently, the spherical areal scalar is

\[
X=g^{ab}\partial_aR\partial_bR
=1-(2\ell+b^2)R^2+O(R^3),
\]

so the conditional positive-`X` areal potential is

\[
\phi_{\rm areal}
=-\frac12\log X
=\left(\ell+\frac{b^2}{2}\right)R^2+O(R^3).
\]

Finally, let `u` be the Eulerian radial-frame timelike unit vector and supply a smooth spherical
source congruence

\[
U_s=\Gamma(u+v e_R),\qquad v=q(T)R+O(R^3).
\]

For the outgoing photon, direct affine propagation and endpoint contraction give

\[
\boxed{
\log\frac{\omega_s}{\omega_o}
=(b-q)R
+\left(\frac{b^2}{2}-n+\frac{\dot b}{2}-\dot q\right)R^2
+O(R^3)
}.
\]

The sign changes with the declared ray/reversal convention. The structural fact does not: a
supplied source congruence can own a linear frequency term even though every regular central
terminal reciprocal potential above begins at quadratic order. The frequency ratio is not silently
renamed `phi_pair`.

## 4. Affine ray and angular phase carrier

Direct Christoffel reconstruction gives the leading radial affine equation

\[
\frac{d\log K^R}{dR}
=-\left(2\ell+2n+\dot b\right)R+O(R^2).
\]

Define

\[
\mathcal A=2\ell+2n+\dot b.
\]

With central normalization `K^R(0)=1`,

\[
K^R=1-\frac{\mathcal A}{2}R^2+O(R^3),
\qquad
R(\lambda)=\lambda-\frac{\mathcal A}{6}\lambda^3+O(\lambda^4).
\]

Spherical symmetry makes the central angular Jacobi map isotropic, not inactive:

\[
D_{\rm sky}=R(\lambda)I_2,
\qquad
\dot D_{\rm sky}=K^R I_2.
\]

Its leading optical tidal matrix is `mathcal A I_2`. The full phase carrier
`(J,D_KJ)` remains symplectic through the retained order. Spherical symmetry derives zero shear on
this central radial class; it was not frozen to obtain a desired answer.

The observer vertex plane carried to a noncaustic source is therefore, in source-normalized phase
coordinates,

\[
\Lambda(q_o)=\{(x,q_ox):x\in\mathbb R^2\},
\qquad
q_o=\frac{\widehat K(R)}{R}.
\]

The local jet does not imply a later caustic. The separate exact oscillator control verifies only
the kinematic statement that `D=0` can coexist with an invertible symplectic phase carrier.

## 5. Source-boundary types

### Marked point event

Keeping the endpoint fixed imposes `J_s=0`, the vertical position boundary. For `R_s!=0`,
`Lambda(q_o)` intersects it only in zero dimension. At a genuine vertical caustic with nonzero
momentum block, the intersection is two-dimensional. A point event is not a resolved image.

### Resolved source screen

A source rest screen owns a two-dimensional allowed **position** tangent. It does not own a
momentum-versus-position graph. Consequently its positional map has rank two away from a caustic,
but a phase-intersection rank is undefined until a source covector, transfer, emission rule, or
equivalent boundary plane is supplied.

### Regular phase boundary

In a nonvertical chart, any supplied Lagrangian boundary plane is

\[
B_H=\{(x,Hx)\},\qquad H=H^T.
\]

Then

\[
d=\dim\bigl(\Lambda(q_o)\cap B_H\bigr)
=\operatorname{nullity}(H-q_oI_2).
\]

Therefore

\[
\begin{array}{c|c}
d&\text{exact condition}\\ \hline
2&H=q_oI_2\\
1&\det(H-q_oI_2)=0\ \text{but}\ H\ne q_oI_2\\
0&\det(H-q_oI_2)\ne0.
\end{array}
\]

The rank is invariant under common source-screen rotation.

### Spherical source worldtube

Supply a timelike spherical worldtube, its unit flow `U_s`, outward unit normal `nu_s`, and one
null-normal branch `k_s=U_s +/- nu_s`. Warped-product geometry gives

\[
\left(\nabla_{e_A}k_s\right)_{\rm screen}
=\frac{k_s(R)}{R}e_A.
\]

Thus its induced source phase graph is isotropic,

\[
H_s=\frac{k_s(R)}{R}I_2.
\]

There is a prior zero-order gate: the central observer ray must satisfy the boundary phase-point
condition `widehat K_s=k_s`. If it does not, the ray is not an admissible QW realization; tangent
planes based at different phase points must not be reported as a rank-zero match. If the condition
holds, then `q_o=widehat K_s(R)/R=H_s`, so the spherical tangent match is automatically rank two.
Rank one is absent in this exact spherical QW class but survives for a supplied anisotropic boundary
`H`. The worldtube, orientation, and null branch are query data; this conditional match is not a
physical source-selection law.

## 6. Three-observer consequence

After source-sky transport, spherical observer image planes are all scalar graphs. Hence

\[
\dim(\Lambda_i\cap\Lambda_j)
=\begin{cases}
2,&q_i=q_j,\\
0,&q_i\ne q_j.
\end{cases}
\]

A common two-dimensional beam exists for three such faces iff `q_A=q_B=q_C`. This is a
nontrivial compatibility sublocus, but the local center jet neither guarantees three rays to one
event nor selects the equality. Multiple distinct central observers or global branches require
geometry beyond this one-center local census.

## 7. Controls and scope

- Flat center: `n=ell=b=dot b=w=q=0` returns `phi_pair=phi_areal=0`, `D=lambda I`.
- Static reciprocal center: for `phi=pR^2+...`, `n=-p`, `ell=p`, and `b=w=0`, both terminal and
  areal potentials return `pR^2`; the measured static source frequency also returns the expected
  quadratic clock term when `q=0`.
- Time-live dependence enters the gauge-invariant combinations displayed in section 1 without an
  equation of motion; nonzero `b` or `dot b` alone has no invariant meaning.
- Actively instrument-tied celestial drift enters the fixed-label pair and mixed blocks before
  readout; passive sky relabeling does not create a physical term.
- The source-congruence coefficient `q` changes the frequency channel without changing the metric.

The metric and query therefore derive a coherent local multichannel score, but regularity does not
select the gauge-equivalence class of history jets, the source history, the active celestial
transport protocol, a source boundary, or a global common-source branch. The verification witness
also contains `dot n`, `dot ell`, and `ddot b`; order counting shows they first enter beyond the
retained output order, so they are not load-bearing G115 coefficients.
