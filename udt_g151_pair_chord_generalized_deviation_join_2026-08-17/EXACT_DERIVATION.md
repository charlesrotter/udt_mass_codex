# G151 exact derivation — pair chord and generalized deviation

Date: 2026-08-17

## 1. Exact next pair-frame derivative

On one supplied smooth regular calibrated pair, retain the G148 working representation

\[
\xi=\rho n,
\qquad
\rho=X_{\max}\tanh\phi_{\rm pair}.
\]

Let \(u\) be the unit pair clock, \(n\) the unit ruler, and \(H\) their positive orthogonal screen.
Decompose both frame derivatives without freezing the screen:

\[
\nabla_u u=a_n n+A,
\qquad A=P_H\nabla_u u,
\]

\[
\nabla_u n=a_nu+\Omega,
\qquad \Omega=P_H\nabla_u n.
\]

Define the screen derivative

\[
\Pi=P_H\nabla_u\Omega.
\]

Differentiating \(g(\Omega,u)=g(\Omega,n)=0\) fixes the parts that must not be discarded:

\[
\boxed{
\nabla_u\Omega
=g(\Omega,A)u-\|\Omega\|^2n+\Pi.}
\]

Twice differentiating \(\xi=\rho n\) now gives the exact identity

\[
\boxed{
\begin{aligned}
\nabla_u^2\xi={}&
\left[\ddot\rho+\rho(a_n^2-\|\Omega\|^2)\right]n\\
&+\left[2\dot\rho a_n+\rho\left(\dot a_n+g(\Omega,A)\right)\right]u\\
&+2\dot\rho\,\Omega+\rho\left(a_nA+\Pi\right).
\end{aligned}}
\]

No field equation or dynamics entered. The screen acceleration \(A\) is an additional first-order
readout not included in G150's four named outputs. The quantities \(\dot a_n\) and \(\Pi\) are next
clock derivatives, while \(\nabla_\xi(\nabla_u u)\) is the transverse acceleration gradient. They
are supplied metric/query data, not selected amplitudes.

The scalar derivatives are fixed once the supplied history gives \(\phi\):

\[
\dot\rho=X_{\max}\operatorname{sech}^2\phi\,\dot\phi,
\]

\[
\ddot\rho=X_{\max}\operatorname{sech}^2\phi
\left(\ddot\phi-2\tanh\phi\,\dot\phi^2\right).
\]

## 2. The exact curvature join and its owner

Use the convention

\[
R(X,Y)Z=\nabla_X\nabla_YZ-\nabla_Y\nabla_XZ-\nabla_{[X,Y]}Z.
\]

For a general relation vector, let

\[
C=[u,\xi].
\]

The full curvature commutator identity is

\[
\boxed{
\nabla_u^2\xi+R(\xi,u)u-\nabla_\xi(\nabla_u u)
=\nabla_u C+\nabla_Cu.}
\]

Thus curvature is present generally, but it does not close chord change without the query-owned
commutator source. A terminal endpoint readout alone does not even define this bracket. The query
must supply a smooth two-parameter realization and identify its variational vector with the working
\(\xi\). The canonical clean reduction follows when that connecting field satisfies

\[
[u,\xi]=0.
\]

Torsion freedom then gives \(\nabla_u\xi=\nabla_\xi u\), and the curvature commutator gives

\[
\boxed{
\nabla_u^2\xi+R(\xi,u)u-\nabla_\xi(\nabla_u u)=0.}
\]

This is generalized deviation. The acceleration-gradient term is part of the exact relation; it
cannot be replaced by the pointwise scalar \(a_n\) or omitted by analogy.

A generic terminal relation vector need not obey \([u,\xi]=0\). Without that query-owned condition,
the curvature commutator retains \(\nabla_uC+\nabla_Cu\); it does not close the chord's change from
curvature and acceleration gradient alone.

The connecting condition is sufficient, not logically necessary, for the commutator source to
vanish. In flat spacetime, \(u=\partial_t\) and \(\xi=t\partial_x\) give
\(C=\partial_x\ne0\), while \(\nabla_uC+\nabla_Cu=0\).

The connecting reduction also restricts the previously free first-order readouts. For
\(\xi=\rho n\), \(\rho\ne0\), project \(C=0\) onto \(u,n,H\):

\[
\boxed{a_n=0,}
\]

\[
\boxed{\dot\rho=\rho\,g(n,\nabla_nu),}
\]

\[
\boxed{\Omega=P_H\nabla_nu.}
\]

This does not contradict G150: G150 allowed every smooth regular query jet, while this is a smaller
query class with a supplied two-parameter connecting realization.

## 3. Conditional geodesic-congruence reduction

If the supplied query is a congruence of geodesics, so \(\nabla_u u=0\) throughout the variation,
the exact reduction is

\[
\boxed{\nabla_u^2\xi+R(\xi,u)u=0.}
\]

This is a conditional Jacobi equation, not a UDT equation of motion.

Write

\[
R(n,u)u=K_n n+K_H,
\qquad K_H\in H.
\]

Because geodesicity sets \(a_n=A=0\), the radial and screen projections are

\[
\boxed{\ddot\rho-\rho\|\Omega\|^2+\rho K_n=0,}
\]

\[
\boxed{2\dot\rho\,\Omega+\rho\Pi+\rho K_H=0.}
\]

These equations show what curvature can do once the correct relation type is supplied: it couples
radial reciprocal change and angular-frame turn. They do not choose \(K_n,K_H\), the history, or
the query.

## 4. Exact nonlinear coordinate witness

The preregistered control uses

\[
g=-T(t)^2dt^2+L(t)^2dx^2+dy^2+dz^2,
\]

\[
L=1+t/10+t^2/20,
\qquad
T=L(2-L)/(2+L),
\qquad X_{\max}=2.
\]

For \(F(t,\sigma)=(t,\sigma,0,0)\), the terminal pair readout satisfies exactly

\[
\phi_{\rm pair}=\tfrac12\log(L/T)=\operatorname{artanh}(L/2),
\qquad
\rho=2\tanh\phi_{\rm pair}=L.
\]

With \(u=T^{-1}\partial_t\), \(\xi=\partial_x=Ln\), the independent coordinate calculation finds

\[
[u,\xi]=0,
\qquad
\nabla_u u=0,
\]

and at \(t=0\),

\[
\dot\rho=3/10,
\qquad
\ddot\rho=93/100,
\qquad
K_n=-93/100.
\]

The direct \(\nabla_u^2\xi\) and \(R(\xi,u)u\) cancel exactly. This witness verifies the sign,
normalization, and connecting-field type. Its lapse/profile was chosen for that check and is not a
physical UDT history or an \(X_{\max}\) determination.

## 5. What changed

G150 proved that four first-order chord readouts are free in the unrestricted local class. G151 does
not reverse that result. It identifies the smallest additional structure that can relate their
change: a query-owned connecting congruence, plus its metric curvature and (for accelerated
families) transverse acceleration gradient.

Thus curvature is not a missing coefficient bolted onto the first-order chord. It is the next-order
compatibility of an actual family of observer relations.

## Maximum conclusion

```text
EXACT_NEXT_PAIR_FRAME_CHORD_IDENTITY_ON_SUPPLIED_SMOOTH_REGULAR_PAIR__
FULL_CURVATURE_COMMUTATOR_IDENTITY_WITH_QUERY_OWNED_C_SOURCE__
CONNECTING_TWO_PARAMETER_REALIZATION_IS_A_SUFFICIENT_REDUCTION_AND_FORCES_AN_ZERO_AWAY_FROM_COINCIDENCE__
GENERALIZED_DEVIATION_DERIVED_WITH_ACCELERATION_GRADIENT__
GEODESIC_JACOBI_REDUCTION_CONDITIONAL__
EXACT_RADIAL_WARPED_CONTROL__
NECESSITY_PHYSICAL_QUERY_HISTORY_DYNAMICS_REGIME_AMPLITUDES_XMAX_AND_GLOBAL_COMPLETION_OPEN
```
