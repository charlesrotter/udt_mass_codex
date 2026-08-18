# G160 exact derivation — time-live pair-first-jet carry

Date: 2026-08-18

## 1. Typed one-carry law

Let `h_B(lambda)` be a supplied regular Lorentzian pair metric on `V_B`, and let

\[
M_{BA}(\lambda):V_A\to V_B
\]

be a supplied smooth orientation-preserving carry. The metric pulled back to `V_A` is

\[
\boxed{\bar h_{B|A}=M_{BA}^T h_BM_{BA}.}
\]

Writing

\[
K_{BA}=\dot M_{BA}M_{BA}^{-1},
\]

direct differentiation gives

\[
\boxed{
\dot{\bar h}_{B|A}
=M_{BA}^T
\left(\dot h_B+K_{BA}^Th_B+h_BK_{BA}\right)
M_{BA}.
}
\]

The first term is the target pair first jet in the chosen target presentation. The two `K` terms
are the moving-carry contribution. This is a presentation split; only the combined carried first
jet is covariant under live independent endpoint gauges.

## 2. What part of the carry rate changes the pair metric?

Define the metric adjoint and its symmetric part by

\[
K^{\dagger_h}=h^{-1}K^Th,
\qquad
S_h(K)=\frac12(K+K^{\dagger_h}).
\]

Then

\[
\boxed{K^Th+hK=2hS_h(K).}
\]

The metric-skew part `A_h(K)=(K-K^{dagger_h})/2` satisfies

\[
A_h(K)^Th+hA_h(K)=0.
\]

Thus only the metric-self-adjoint part of the supplied carry rate reaches the transported pair
metric first jet. The metric-skew part can still matter to frame or path transport; G160 proves only
that it is invisible in this two-tensor channel.

## 3. Three-observer composition

For `A -> B -> C`, suppose

\[
M_{CA}=M_{CB}M_{BA}.
\]

Then

\[
\dot M_{CA}=\dot M_{CB}M_{BA}+M_{CB}\dot M_{BA},
\]

and the right rates obey

\[
\boxed{
K_{CA}=K_{CB}+\operatorname{Ad}_{M_{CB}}K_{BA}.
}
\]

Pulling `(h_C,dot h_C)` first to `B` and then to `A` gives exactly the same pair metric and first
jet as pulling directly with `M_CA`. This is a functorial identity for a supplied closed carry
network, not a law selecting that network.

The converse is false. For `h=diag(-1,1)`, the nonidentity Lorentz stabilizer

\[
L=\begin{pmatrix}5/3&4/3\\4/3&5/3\end{pmatrix}
\]

obeys `L^T hL=h`; direct carry `L` and staged carry `I` therefore return the same stationary pair
first jet despite finite nonclosure. At identity carry, the nonzero rate

\[
K=\begin{pmatrix}0&1\\1&0\end{pmatrix}
\]

satisfies `K^Th+hK=0`, so equality of first jets can also miss rate nonclosure. Carry closure is
sufficient for staged/direct equality, not necessary before quotienting the relevant stabilizer.

For an independently supplied direct route define

\[
F_{ABC}=M_{CB}M_{BA}M_{CA}^{-1}.
\]

Its right rate is

\[
\boxed{
K_F
=K_{CB}+\operatorname{Ad}_{M_{CB}}K_{BA}
-\operatorname{Ad}_{F_{ABC}}K_{CA}.
}
\]

At a point where `F_ABC=I`, first-order closure is equivalent to

\[
K_{CA}=K_{CB}+\operatorname{Ad}_{M_{CB}}K_{BA}.
\]

Rate closure alone does not force a pre-existing nonidentity finite defect to vanish.

## 4. Live endpoint gauges

Let independent endpoint carrier gauges be `P_A(lambda)` and `P_B(lambda)`:

\[
h_B'=P_B^Th_BP_B,
\qquad
M_{BA}'=P_B^{-1}M_{BA}P_A.
\]

With every derivative term retained,

\[
\bar h_{B|A}'=P_A^T\bar h_{B|A}P_A,
\]

\[
\boxed{
\dot{\bar h}_{B|A}'
=\dot P_A^T\bar h_{B|A}P_A
+P_A^T\dot{\bar h}_{B|A}P_A
+P_A^T\bar h_{B|A}\dot P_A.
}
\]

The live target gauge cancels exactly. The source gauge acts by the ordinary live tensor-coordinate
law. Consequently the intrinsic-versus-connection terms cannot separately be called physical.

## 5. General terminal-rate classification

Let `(kappa,phi,beta)` be the terminal coefficients of `h`, and let `m_0,m_1` be the columns of
`M`. On the recharted domain `m_0^Thm_0<0`,

\[
\boxed{\bar\kappa=\kappa+\frac12\log\det M,}
\]

\[
\boxed{\dot{\bar\kappa}=\dot\kappa+\frac12\operatorname{tr}K.}
\]

This determinant/common-scale rate is the universal real character over the full regular
orientation-preserving carry class.

For reciprocal depth,

\[
\bar\phi
=\phi+\frac12\log\det M
-\frac12\log\!\left(\frac{-m_0^Thm_0}{-h_{00}}\right),
\]

so

\[
\boxed{
\dot{\bar\phi}-\dot\phi
=\frac12\operatorname{tr}K
-\frac12\partial_\lambda
\log\!\left(\frac{-m_0^Thm_0}{-h_{00}}\right).
}
\]

For shift, let

\[
N=m_0^Thm_1,
\qquad D=m_0^Thm_0<0.
\]

Then

\[
\bar\beta=\frac ND,
\qquad
\boxed{\dot{\bar\beta}=\frac{\dot ND-N\dot D}{D^2},}
\]

with both the metric first jet and live column motion included in `dot N,dot D`.

The same determinant-one lower-shear carry applied to `diag(-1,1)` and `diag(-4,1)` gives clock-norm
ratios `3/4` and `15/16`, and different shifts. Therefore neither the reciprocal nor shift change
is a carry-only scalar over unrestricted `GL+(2)`.

## 6. Flag-preserving `B+(2)` subcase

For the already declared positive upper-triangular carry

\[
M=\begin{pmatrix}a&b\\0&d\end{pmatrix},
\qquad a,d>0,
\]

define

\[
\sigma(M)=\frac12\log(ad),
\qquad
\chi(M)=\frac12\log\frac da,
\qquad
r=\frac da,
\qquad
s=\frac ba.
\]

Because the clock/ruler flag is preserved, the terminal laws reduce exactly to

\[
\boxed{
\bar\kappa=\kappa+\sigma,
\qquad
\bar\phi=\phi+\chi,
\qquad
\bar\beta=s+r\beta.
}
\]

For `K=dot M M^-1`,

\[
\boxed{
\dot{\bar\kappa}=\dot\kappa+\frac12\operatorname{tr}K,
}
\]

\[
\boxed{
\dot{\bar\phi}=\dot\phi+\frac12(K_{11}-K_{00}),
}
\]

\[
\boxed{
\dot{\bar\beta}
=r\left[\dot\beta+K_{01}+(K_{11}-K_{00})\beta\right].
}
\]

The conditional pair calibration obeys

\[
\left(\frac{c_{\rm eff}^{({\rm pair})}}{c_E}\right)^{\!\rm bar}
=\frac ad\left(\frac{c_{\rm eff}^{({\rm pair})}}{c_E}\right),
\]

and its logarithmic rate acquires `K_00-K_11`.

These formulas give one complete sufficient class for exact reciprocal and shift channel laws.
The unrestricted `GL+(2)` counterexample rules out a universal carry-only law on that whole class;
it does not make positive `B+(2)` necessary for every special subfamily. For example, `-I` is
orientation-preserving and outside positive `B+(2)`, but leaves every pair metric and terminal
coefficient unchanged.

## 7. Total comparison rate

With the G142 total transition

\[
C_{BA}=R_BM_{BA}R_A^{-1},
\]

define

\[
\Gamma_{BA}=\dot C_{BA}C_{BA}^{-1},
\qquad
\Omega_i=\dot R_iR_i^{-1}.
\]

Then

\[
\boxed{
\Gamma_{BA}
=\Omega_B
+\operatorname{Ad}_{R_B}K_{BA}
-\operatorname{Ad}_{C_{BA}}\Omega_A.
}
\]

Endpoint scores and carry rate are gauge-dependent pieces. The joined `C_BA` and `Gamma_BA` are
unchanged under the live endpoint gauge laws. If total transitions compose, differentiation gives

\[
\Gamma_{CA}=\Gamma_{CB}+\operatorname{Ad}_{C_{CB}}\Gamma_{BA}.
\]

## 8. Scalar closure remains weaker than matrix closure

At finite identity carry, take the rate defect

\[
N=\begin{pmatrix}0&1\\0&0\end{pmatrix}.
\]

It has

\[
\operatorname{tr}N=0,
\qquad N_{11}-N_{00}=0,
\qquad N\ne0.
\]

Common-scale and reciprocal scalar rate defects both vanish while the shift/matrix-rate defect is
nonzero. Scalar closure therefore cannot replace complete first-order carry closure.

## 9. Landing and scope

`TIMELIVE_PAIR_FIRST_JET_CARRY_DERIVED__FULL_GLPLUS2_PULLBACK_AND_RIGHT_CONNECTION_COMPOSITION_EXACT__CARRY_CLOSURE_SUFFICIENT_NOT_NECESSARY_DUE_TO_LORENTZ_STABILIZER__ONLY_COMBINED_CARRIED_FIRST_JET_IS_LIVE_SOURCE_GAUGE_COVARIANT__JOINED_TOTAL_RATE_IS_LIVE_ENDPOINT_GAUGE_INVARIANT__KAPPA_HAS_UNIVERSAL_DETERMINANT_RATE__NO_PHI_BETA_CARRY_ONLY_LAW_ON_UNRESTRICTED_GLPLUS2__BPLUS2_SUFFICIENT_NOT_NECESSARY_FOR_EXACT_CHARACTER_LAWS__SCALAR_RATE_CLOSURE_WEAKER_THAN_MATRIX_RATE_CLOSURE__PHYSICAL_CARRY_HISTORY_QUERY_LAMBDA_AND_COMPLETION_OPEN`

- `DERIVED_CONDITIONAL`: every displayed identity for supplied smooth regular typed data;
- `OPEN`: physical carry, query population, history, parameter ownership, singular/global strata;
- not derived: a fixed channel balance, regime profile, dynamics, observations, `X_max`, light,
  action, source, bootstrap, matter, mass, or completion.
