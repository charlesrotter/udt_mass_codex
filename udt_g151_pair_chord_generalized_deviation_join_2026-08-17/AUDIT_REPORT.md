# G151 audit report — pair chord generalized-deviation join

Date: 2026-08-17
Status: `VERIFIED_WITH_CAVEATS`

## Exact generic result

For the working relation vector \(\xi=\rho n\), \(\rho=X_{\max}\tanh\phi_{\rm pair}\), the complete
next pair-frame derivative is

\[
\begin{aligned}
\nabla_u^2\xi={}&
[\ddot\rho+\rho(a_n^2-\|\Omega\|^2)]n\\
&+[2\dot\rho a_n+\rho(\dot a_n+g(\Omega,A))]u\\
&+2\dot\rho\Omega+\rho(a_nA+\Pi),
\end{aligned}
\]

where \(A=P_H\nabla_u u\) is an additional first-order readout and
\(\Pi=P_H\nabla_u\Omega\).

For \(C=[u,\xi]\), the exact commutator identity is

\[
\nabla_u^2\xi+R(\xi,u)u-\nabla_\xi(\nabla_u u)
=\nabla_uC+\nabla_Cu.
\]

A terminal pair readout does not own \(C\). A smooth two-parameter query must identify its
variational field with \(\xi\).

## Connecting and geodesic reductions

The canonical sufficient connecting reduction \(C=0\), away from \(\rho=0\), forces

\[
a_n=0,
\qquad
\dot\rho=\rho g(n,\nabla_nu),
\qquad
\Omega=P_H\nabla_nu.
\]

It is not necessary: nonzero commutator sources can exceptionally cancel. If the entire supplied
variation is geodesic, the exact Jacobi reduction is

\[
\nabla_u^2\xi+R(\xi,u)u=0.
\]

The radial and screen equations are

\[
\ddot\rho-\rho\|\Omega\|^2+\rho K_n=0,
\qquad
2\dot\rho\Omega+\rho\Pi+\rho K_H=0.
\]

These constrain one supplied connecting congruence; they do not select it or provide dynamics.

## Evidence gates

- preregistration and exact witness frozen in commits `68bc9d56`, `69f5e5c2`;
- exact generic decomposition and reciprocal derivatives: PASS;
- exact nonlinear coordinate control, all local `t`: PASS;
- marked values `dot(rho)=3/10`, `ddot(rho)=93/100`, `K_n=-93/100`: PASS;
- injected mutations: PASS;
- fresh adversarial review: `REPAIR_REQUIRED`, then `FOLLOWUP_PASS`;
- physical/global premise audit: all remain open.

The coordinate control independently certifies the radial geodesic sign/type only. Abstract
commutator substitutions are regression bookkeeping; active screen and acceleration-gradient
sectors are analytically derived but lack a second independent coordinate witness here.

## Landing

```text
VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_FOLLOWUP_PASS__
EXACT_GENERIC_SECOND_DERIVATIVE_DECOMPOSITION_FOR_THE_WORKING_CHORD__
FULL_CURVATURE_COMMUTATOR_IDENTITY_WITH_QUERY_OWNED_C_SOURCE__
CONNECTING_TWO_PARAMETER_REALIZATION_IS_A_SUFFICIENT_REDUCTION_AND_FORCES_AN_ZERO_AWAY_FROM_COINCIDENCE__
GEODESIC_CONGRUENCE_JACOBI_REDUCTION_CONDITIONAL__
EXACT_RADIAL_WARPED_CONTROL__
NECESSITY_PHYSICAL_QUERY_HISTORY_DYNAMICS_REGIME_XMAX_AND_COMPLETION_OPEN
```

