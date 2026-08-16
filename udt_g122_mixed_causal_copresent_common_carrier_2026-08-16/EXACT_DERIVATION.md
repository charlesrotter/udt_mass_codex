# G122 exact derivation — mixed causal/co-present common carrier

Date: 2026-08-16

Status: `BLIND_VERIFIED_WITH_CAVEATS__REPAIRS_VERIFIED`

## 1. Result first

For one supplied observer-exponential query, the metric supplies a common pathwise dependency
record for terminal pair and causal/sky channels, but it does **not** thereby turn them into two
arrows on one common linear carrier.

That common dependency record is

\[
\mathfrak J(F,g)
=\left(g,F;T,K,J_A,\Pi_A=D_KJ_A;\nabla,R[g]\right)_{\rm branch}.
\tag{1}
\]

The longitudinal pair metric and reciprocal depth are one evaluation of (1). The transverse
Jacobi phase propagation is another. They are connected because they come from the same `g` and
`F`; they are not identical mathematical objects.

The preregistered common-carrier square cannot be formed from the terminal pair data. A nonzero
linear map from full transverse phase into a target built solely from the screen-trivial terminal
pair metric is forbidden by residual `O(2)` covariance. This does not exclude maps using the full
jet's screen-charged or mixed covariants. Such a construction would be additional typed data beyond
the terminal pair readout and remains unconstructed here.

In particular, G122 does not construct or exhaust an independent direct `A-B` pair immersion or an
arrow `R_BA^pair`. It classifies the relation between terminal pair readouts and causal phase on the
two supplied source legs.

The strongest landing is

```text
COMMON_OBSERVER_EXPONENTIAL_PATHWISE_DEPENDENCY_RECORD_DERIVED_CONDITIONALLY
__NO_DATA_FREE_INFORMATION_PRESERVING_LINEAR_SOLDER_FROM_TERMINAL_PAIR_DATA
__CAUSAL_PHASE_AND_TERMINAL_PAIR_ARE_DISTINCT_NATURAL_EVALUATIONS
__G116_LOCAL_TWO_JET_SCALAR_JUNCTION_ONLY
__DIRECT_AB_PAIR_MAP_UNTESTED
__NO_HISTORY_SELECTOR_FOUND_IN_DECLARED_TEST
```

## 2. Exact types

For one observer branch let

\[
H=T_{(\tau,\lambda)}\Sigma_\parallel,
\qquad \operatorname{rank}H=2,
\]

be the longitudinal query domain. Let `S` be the rank-two positive screen quotient. The causal
phase fiber is

\[
V=S\oplus S,
\qquad X=(J,\Pi),\quad \Pi=D_KJ.
\tag{2}
\]

The observer exponential has differential

\[
dF=(T,K,J_1,J_2).
\tag{3}
\]

The longitudinal evaluator is

\[
\mathfrak J(F,g)
\longmapsto
h_\parallel=\operatorname{Gram}_g(T,K)
\longmapsto
(T_{\rm pair},L_{\rm pair},\beta,\phi_{\rm pair}).
\tag{4}
\]

The causal evaluator is

\[
\mathfrak J(F,g)
\longmapsto
(J_A,D_KJ_A)
\longmapsto
P:V_{\rm initial}\to V_{\rm endpoint}.
\tag{5}
\]

Equation (4) returns a bilinear form and scalar/state readouts on `H`. Equation (5) returns a
symplectic phase propagator on `V`. The direct pair metric does not itself return an arrow
`V_A -> V_B`.

For two observer branches reaching a supplied common source, define the joined dependency record

\[
\mathfrak J_{AB}^{S}
=\left(\mathfrak J_A,\mathfrak J_B;g,s,U_s,C_{BA}\right).
\tag{6}
\]

It derives the G114 carried causal edge

\[
R_{BA}^{\rm causal}=P_B^{-1}C_{BA}P_A
\tag{7}
\]

and the two endpoint pair readouts. This notation asserts shared data, not a proved categorical
fiber product. An independently supplied direct `A-B` pair immersion would add a further leg to
(6); G122 does not construct or analyze that leg and does not silently identify it with either
source branch.

## 3. The exact `O(2)` no-go

Passive screen changes act on the phase fiber by

\[
(J,\Pi)\mapsto(\rho J,\rho\Pi),
\qquad \rho\in O(2).
\tag{8}
\]

The longitudinal pair metric and its scalar readouts are unchanged. Therefore any linear map built
solely from those screen-trivial terminal pair data must obey

\[
q(\rho\oplus\rho)=q.
\tag{9}
\]

Set `rho=-I_2`. Then

\[
-q=q,
\]

so

\[
\boxed{q=0}.
\tag{10}
\]

This is not a dimensional argument. It is a representation-covariant no-go within the declared
terminal-data class. The zero map cannot certify physical agreement because it erases the entire
phase state.

If the target is instead declared to transform as a screen, exact `O(2)` equivariance gives

\[
q(J,\Pi)=aJ+b\Pi.
\tag{11}
\]

That is a two-parameter family, not an arrow selected by terminal pair data. The full jet can carry
screen-charged and mixed covariants, so this audit does not prove that all enlarged query classes
lack a solder. It proves only that the terminal pair metric does not supply one. Moreover,
retaining only position `J` loses the caustic-robust phase information that motivated G114.

Thus a nonzero common square needs additional query structure. It cannot be recovered by calling
equal-sized matrices the same object.

## 4. Flat exact catch proof

For the Minkowski observer exponential

\[
F(\tau,\lambda,a,b)
=(\tau+\lambda,\lambda\sqrt{1-a^2-b^2},\lambda a,\lambda b),
\]

at `a=b=0`,

\[
dF=
\begin{pmatrix}
1&1&0&0\\
0&1&0&0\\
0&0&\lambda&0\\
0&0&0&\lambda
\end{pmatrix}.
\tag{12}
\]

The complete pullback is

\[
F^*\eta=
\begin{pmatrix}
-1&-1&0&0\\
-1&0&0&0\\
0&0&\lambda^2&0\\
0&0&0&\lambda^2
\end{pmatrix}.
\tag{13}
\]

The pair block is regular and Lorentzian, with determinant `-1`. Its transverse screen projection
has rank zero. The angular Jacobi map is `lambda I_2`, rank two for `lambda>0`. They coexist inside
one full differential but cannot be the same map.

At an ordinary isotropic position caustic, `D=0` while the full phase propagator can be `-I_4`.
Therefore a projection that keeps only the rank-two position block is not an equivalent carrier.

## 5. The lawful local two-jet scalar junction

The two channels do possess a local metric-derived relationship. G116 gives, on the regular
central time-live two-jet,

\[
\phi_{\rm pair}=p_2R^2+O(R^3),
\]

\[
\zeta
=v_{\rm rel}R+
\left(p_2+\dot v_{\rm rel}-\frac{\mathcal A_{\rm opt}}4\right)R^2
+O(R^3).
\]

Hence

\[
\boxed{
\zeta-\phi_{\rm pair}
=v_{\rm rel}R+
\left(\dot v_{\rm rel}-\frac{\mathcal A_{\rm opt}}4\right)R^2
+O(R^3)
}.
\tag{14}
\]

This is exactly the kind of joint result the common dependency record supports: terminal reciprocal depth,
relative shift, and optical expansion enter one derived relation without being collapsed into one
object.

On the pure stationary reciprocal branch,

\[
v_{\rm rel}=\dot v_{\rm rel}=\mathcal A_{\rm opt}=0,
\]

so `zeta=phi_pair`. On a generic live branch they differ. Requiring equality generally would turn
off or finely cancel live shift and optical channels. It is not a consistency condition supplied
by the metric.

## 6. Why no history selector was found in this test

The common dependency construction and its evaluator identities hold for every smooth regular
metric and correctly typed query in the declared class. The `O(2)` theorem rules out one
terminal-data-only comparison; it does not exclude one regular history while retaining another.

Likewise, the nonzero right-hand side of (14) is physical geometric content of the supplied live
query, not a failure residual. A history-selection law would need an independently owned condition
on the complete network, not an instruction to set the orchestra terms to zero.

## 7. What is established and what remains open

`DERIVED_CONDITIONALLY`:

- one supplied observer-exponential metric/query history supports both longitudinal pair and
  transverse phase evaluations;
- the pair and phase outputs are differently typed;
- residual screen covariance forbids a data-free nonzero linear solder from terminal pair data
  into full transverse phase;
- G116 is a local `O(R^2)` scalar junction and reduces correctly on the pure reciprocal branch.

`OPEN`:

- the independent direct `A-B` pair immersion and any phase arrow it might support;
- the finite-radius time-live form of the scalar/multichannel junction;
- a physical history-selection or global-completion law;
- a nonzero direct pair phase arrow, if a future query supplies additional structure;
- nonspherical, cut-locus, and global branch assembly.

No action, matter law, radiation theory, `X_max`, bootstrap premise, SNe, BAO, or CMB input was used.
