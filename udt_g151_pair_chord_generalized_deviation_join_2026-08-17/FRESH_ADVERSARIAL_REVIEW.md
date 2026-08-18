# G151 fresh adversarial review

Date: 2026-08-17
Reviewer: fresh read-only Codex subagent
Landing: `REPAIR_REQUIRED`

The reviewer independently confirmed the generic second-derivative decomposition, the full
curvature-commutator sign, and the frozen radial witness values

\[
T_0=1/3,
\quad
\dot\rho_0=3/10,
\quad
\ddot\rho_0=93/100,
\quad
K_n=-93/100.
\]

It required five repairs:

1. For \(\xi=\rho n\), \(\rho\ne0\), a normalized connecting field obeying \([u,\xi]=0\)
   necessarily satisfies
   \(a_n=0\),
   \(\dot\rho=\rho g(n,\nabla_nu)\), and
   \(\Omega=P_H\nabla_nu\). The connecting subsection had omitted these restrictions. Screen
   acceleration \(A\) is an additional first-order readout, not itself next-jet data.
2. The connecting condition is sufficient, not necessary, for the commutator correction to vanish.
   The flat counterexample \(u=\partial_t,\xi=t\partial_x\) has nonzero \(C\) but zero source.
3. Terminal data alone do not define a bracket. The query must supply a smooth two-parameter
   realization and identify its variational field with the working \(\xi\).
4. The coordinate verifier had to check bracket, geodesicity, and Jacobi for all local \(t\), not
   only the marked point. Abstract commutator assignments are regression bookkeeping, while the
   coordinate control independently tests only the radial geodesic reduction.
5. The geodesic-congruence scope and all physical/global open boundaries were otherwise correct.

The reviewer supplied the narrower landing adopted after repair.

