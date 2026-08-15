# Preregistration — overlapping complete-pair live compatibility and reciprocal-response atlas

Date: 2026-08-14

Mode: `MAP -> OBSERVE -> PONDER -> DERIVE`; metric-led, exact symbolic/CPU

Outcome at registration: **NOT YET EVALUATED**

## 1. Whole question

The externally checked uncompressed evaluator derives, for one supplied complete coframe and one
supplied pair realization,

```text
E=[[B,0],[Q S,Q]],
J=[Y;Z],
h=J^T E^T eta_4 E J
 =Y^T B^T eta_2 B Y +(S Y+Z)^T Q^T Q(S Y+Z).
```

It retains `B,Q,S,Y,Z` and all five first derivatives but supplies no live history. The present
audit asks the next bounded question:

> When several regular observer-pair realizations overlap in one supplied complete metric, do the
> metric, founding ordered-comparison semantics, and exact middle-calibration rules impose a
> nonidentity compatibility law that selects or restricts their live histories?

The audit must also test, without assuming the desired answer:

> Does any such overlap law force the complete reciprocal response to be loud at both reciprocal
> ends and quiet in an intermediate regime, or does that shape remain only a conditional response
> slice among other lawful live histories?

No observational data, fitted coefficient, physical `X_max` realization, bootstrap law, action,
source, carrier, or matter model enters.

## 2. Typed overlap atlas

Four cases are tested separately.

### O1 — one pair surface, two charts

Let `F_alpha=F_beta o psi_ba` on a genuine overlap and define

```text
R_ba=d psi_ba,
J_alpha=J_beta R_ba,
V_alpha=E J_alpha=V_beta R_ba,
h_alpha=R_ba^T h_beta R_ba.
```

The exact live law to be proved or falsified is

```text
dot J_alpha=dot J_beta R_ba+J_beta dot R_ba,
dot V_alpha=dot V_beta R_ba+V_beta dot R_ba,
dot h_alpha
 =R_ba^T dot h_beta R_ba
  +dot R_ba^T h_beta R_ba
  +R_ba^T h_beta dot R_ba.
```

On a triple chart overlap, `R_ca=R_cb R_ba`. These are candidates for `DERIVED` chart
compatibility identities, not physical history equations.

### O2 — distinct pair surfaces sharing one observer seam

At a common event use pair tangent frames

```text
J_1=[u,r_1],
J_2=[u,r_2],
```

with the same calibrated observer tangent `u`. The metric automatically gives the same clock entry

```text
(h_1)00=(h_2)00=g(u,u).
```

The cross and ruler entries need not agree unless a stronger common-surface or common-terminal-state
condition is supplied. The audit must construct or reject exact regular witnesses with the same
clock entry but different `phi_pair`.

### O3 — one common calibrated terminal network

If an `A-B` relation ends at the literal same middle state at which a `B-C` relation begins, the
positive triangular terminal coframe must match. If separately rebuilt states are `B_in` and
`B_out`, an explicit reset

```text
M_B=B_out B_in^-1
```

is required. The audit must distinguish exact matching constraints from a physical rule selecting
the common family.

### O4 — path- or branch-labelled relations

Direct and composite arrows may differ by lawful holonomy. The audit must not impose universal
flat descent or erase path labels merely to obtain a scalar rule.

## 3. Joint ambient Gram compatibility

For simultaneous pair tangents collected as columns of one matrix `mathcal J`, define

```text
mathcal K=mathcal J^T g mathcal J=(E mathcal J)^T eta_4(E mathcal J).
```

Every pair metric is a selected `2 x 2` restriction of `mathcal K`. The audit will determine the
complete finite-dimensional restrictions that follow solely from a common four-dimensional
Lorentz metric:

- `rank(mathcal K)<=4`;
- negative index at most one;
- vanishing of every `5 x 5` Gram determinant when five or more tangent vectors are retained;
- exact equalities induced by literally shared tangent columns.

These may be nonidentity network-compatibility constraints. They must not be called an evolution
law or a selector of the physical network unless they exclude otherwise regular complete histories
rather than only inconsistent simultaneous presentations.

## 4. Complete live variables

The primary local arena retains:

- arbitrary smooth regular `B(lambda,x) in GL(2,R)`;
- arbitrary smooth regular `Q(lambda,x) in GL(2,R)`;
- all four entries of `S(lambda,x) in Mat(2,R)`;
- every pair-specific rank-two `J_alpha=[Y_alpha;Z_alpha]`;
- all derivatives `dot B,dot Q,dot S,dot Y_alpha,dot Z_alpha`;
- every overlap transition `R_ba` and `dot R_ba` when O1 applies;
- exact middle terminal coframes and reset matrices when O3 applies.

No matrix block is frozen in the primary overlap test. Fixed objects appear only in explicitly
labelled response controls.

## 5. Loud-ends / quiet-middle tests

On an invertible-`Y`, A-calibrated cell define

```text
B=[[T,T beta],[0,L]],
T=sigma exp(-phi),
L=sigma exp(+phi),
P=C^T q C=[[a,d],[d,e]],
n_beta=e-2 beta d+beta^2 a,
Pi=B^-T P B^-1.
```

Two readouts are preregistered so that a convenient scalar cannot be selected after inspection:

```text
A_trace=tr(Pi)
       =[a exp(+2phi)+n_beta exp(-2phi)]/sigma^2,

M_terminal=phi_pair-phi.
```

### LQ1 — fixed reciprocal-response control

Hold `P,sigma,beta` fixed and vary only `phi`. The existing conditional theorem predicts that when
`a>0` and `n_beta>0`, `A_trace` is strictly convex with one minimum. The audit must independently
replay this theorem and classify all `rank(P)=0,1,2` boundary strata. It must separately determine,
not assume, the end and stationary-point behavior of `M_terminal` on its regular A-clock domain.

This control is a partial derivative through configuration space, not a physical history.

### LQ2 — fully live overlap-compatible histories

Allow `P,sigma,beta` and the underlying `Q,S,Y,Z` to vary with `phi` while satisfying the applicable
O1--O4 overlap laws. A universal overlap-derived loud/quiet theorem is certified only if **every**
regular two-sided family with both reciprocal projections nonzero has the registered end growth and
an intermediate minimum in the same declared readout.

One exact regular overlap-compatible counterfamily with flat or monotone response falsifies
universal selection. Conversely, one family with a quiet middle proves only survival, not
selection. The audit must deliberately seek both survivors and counterfamilies.

### LQ3 — uncompressed ownership

Every constructed `P(phi)` family must be lifted back to explicit `Q,S,Y,Z`; no scalar or Gram
history may be treated as physical merely because it is easy to write. At least one exact family
must keep `S` genuinely live, and at least one must use a nonidentity chart overlap.

## 6. Premise classification

- `c_E`: `OBSERVED` pair clock/ruler calibration.
- reciprocal exponential character on supplied depth: `DERIVED`.
- complete coframe chart: `CONDITIONAL` regular local metric chart.
- ambient metric history and pair realizations: `SUPPLIED/CONDITIONAL`.
- O1 chart-overlap laws: candidates for `DERIVED` identities.
- O2 shared-clock equality: candidate for `DERIVED` on a supplied shared observer tangent.
- O3 exact terminal matching and reset algebra: already `DERIVED CONDITIONAL`; physical family
  ownership remains `OPEN`.
- O4 holonomy: lawful path-labelled geometry; flat descent is not assumed.
- joint Gram rank/inertia restrictions: candidates for `DERIVED` simultaneous-realizability laws.
- physical live history, universal loud/quiet regime, regime locations, and a scalar `mu`: `OPEN`.
- bootstrap: inactive `WORKING HYPOTHESIS`.

## 7. Falsification and certification contract

The overlap algebra is falsified by any nonzero exact residual in O1 or by failure of a declared
common-column or joint-Gram restriction.

A nonidentity physical history law is **not** certified by chart covariance, matching definitions,
Maurer--Cartan/Bianchi identities, or Gram rank alone. It requires an exact metric/founding
condition that excludes at least one otherwise regular smooth complete history after quotienting
presentation freedom.

A universal loud/quiet law is falsified by one fully lifted, regular, overlap-compatible history
without the claimed two-ended/intermediate behavior.

Certification requires:

1. exact symbolic production algebra;
2. an independent implementation not importing production functions;
3. hostile controls for omitted `dot R`, a mismatched middle state silently set to identity, a
   diagonal/frozen orchestra substitute, and a Gram-only family without an explicit lift;
4. a complete premise audit;
5. explicit separation of conditional survivors from universally selected behavior.

## 8. Preregistered primary landings

Return exactly one:

1. `OVERLAP_SUPPLIES_NONIDENTITY_LIVE_HISTORY_LAW_AND_SELECTS_TWO_SIDED_QUIET_MIDDLE`;
2. `OVERLAP_SUPPLIES_NONIDENTITY_SIMULTANEOUS_COMPATIBILITY_BUT_NOT_LIVE_REGIME_SELECTION`;
3. `OVERLAP_ADDS_ONLY_CHART_QUERY_AND_JOINT_GRAM_COMPATIBILITY__ALL_SMOOTH_HISTORY_CLASSES_REMAIN`;
4. `ALGEBRA_OR_TYPE_FAILURE`.

Secondary loud/quiet classification must be one of:

- `LOUD_ENDS_QUIET_MIDDLE_UNIVERSAL_ON_DECLARED_LIVE_CLASS`;
- `LOUD_ENDS_QUIET_MIDDLE_CONDITIONAL_SURVIVOR_NOT_SELECTED`;
- `NO_TWO_SIDED_QUIET_MIDDLE_EVEN_ON_FIXED_RESPONSE_CONTROL`;
- `READOUT_DEPENDENT_OR_TYPE_FAILURE`.

## 9. Maximum allowed conclusion

At most, this audit may derive exact overlap, seam, middle-state, and simultaneous-Gram
compatibility laws for supplied complete pair families, and determine whether those laws do or do
not force the two-ended/intermediate response pattern. It may not select a physical universe,
identify either end with microphysics or `X_max`, resume SNe/CMB/BAO validation, derive dynamics,
or promote a surviving response family into canon.
