# G103 preregistration — source-independent restriction ownership

Date: 2026-08-15

Status:

```text
PREREGISTERED
__OUTCOME_BLIND
__EXACT_REGULAR_ALGEBRA_AND_FIRST_JET_ONLY
```

## Whole question

After G102 supplies the complete two-source observer evaluator, do the currently owned complete-
metric equations impose any nontrivial source-independent restriction on its observable pushforward?

This is a metric-led solution-space question. It does not search for an oscillation, preferred angle,
ruler, feature, or fit. No BOSS curve, descriptor, covariance, singular vector, or feature location may
be read.

## Exact bounded arena

For one common calibrated observer `O`, each supplied regular observer--source relation `a` yields

```text
Psi_a=(Z_a,n_a) in R_+ x S_O^2,
cos(theta_ab)=g_O(n_a,n_b).
```

The complete coframe and relation are

```text
E=[[B,0],[Q S,Q]],
J_a=[Y_a;Zeta_a],
V_a=E J_a,
h_a=V_a^T eta_4 V_a.
```

`Zeta_a` denotes the screen block of the pair Jacobian and is not the observed redshift `Z_a`.
Observed redshift remains the separately typed endpoint carry `Z_a=exp(DeltaPhi_a)` under the G99
conditional middle-regime identification.

The source one- and two-point measures, selection/transfer, and branch weights remain unrestricted.
The audit asks what survives *despite* that freedom.

## Candidate restriction classes

The frozen candidate list is in `CANDIDATE_RESTRICTION_CLASSES.tsv`. It includes:

1. regular support and common-observer typing;
2. fixed-base positive-Gram terminal reachability;
3. zero-order complete-pair reachability with query realization released;
4. first-jet/time-live restrictions;
5. simultaneous ambient and sky Gram restrictions;
6. reciprocal reversal and endpoint-network composition;
7. branch criticality, caustics, and noninjectivity;
8. measure, marginal, mask, cap, and shell consistency;
9. global topology/completion; and
10. bootstrap or joint source-history admissibility.

No class may be added or deleted after execution. A newly noticed class may be recorded only as an
unexecuted open item unless separately preregistered.

## What counts as a positive restriction

A source-independent physical restriction must:

1. follow from an active UDT metric equation or exact complete-history identity;
2. hold for every regular history, query realization, branch weighting, and source pair measure in
   the declared class;
3. descend to an equation, inequality, support exclusion, multiplicity law, or cross-query relation
   on the G102 observable measure;
4. exclude at least one otherwise regular target observable pattern; and
5. be stronger than positivity, unit-sphere support, common-observer typing, finite-dimensional Gram
   realizability, estimator normalization, or generic probability-measure consistency.

## Preregistered constructive checks

1. `R-ZERO`: for invertible `E`, reconstruct any regular target pair coframe `V_*` by
   `J=E^-1 V_*`.
2. `R-SKY`: for a common unit timelike `u_O`, realize any two unit screen directions and any angle in
   `[0,pi]` with pair coframes `[T_a u_O, b_a u_O+L_a n_a]`.
3. `R-DEPTH`: extend any finite star of positive observer--source ratios by endpoint potentials
   `Phi_i=log Z_i`; then `Z_ij=exp(Phi_j-Phi_i)` composes and reverses exactly.
4. `R-FIRST`: for arbitrary target first jet, use
   `dot J=E^-1(dot V_*-dot E J)` and verify `dot(EJ)=dot V_*`.
5. `R-GRAM`: classify the common-sky Gram matrix as positive semidefinite with unit diagonal and rank
   at most three; exhibit a hostile rank-four correlation matrix that cannot be one sky.
6. `R-MEASURE`: construct symmetric finite source pair measures realizing several distinct angular
   histograms while all metric/query support conditions remain satisfied.
7. `R-FIXEDBASE`: independently replay the conditional fixed-base positive-Gram inequality and show
   exactly which extra shared-base/calibration assumptions it requires.
8. `R-GLOBAL`: distinguish local regular surjectivity from global completeness; neither direction may
   be inferred from the other.

## Hostile mutations

- freeze `J` and call the resulting response a metric-wide restriction;
- identify observer-local `h` with accumulated endpoint depth;
- drop the common observer and still form one sky angle;
- admit a non-unit sky vector or a rank-four sky Gram matrix;
- call reciprocal composition a selector of the star depths;
- use an injective pullback argument outside its image/support hypotheses;
- promote generic measure normalization into a UDT-specific pattern prediction;
- infer global or critical behavior from the local regular construction; or
- open an observational outcome while deriving the restriction.

## Certification ceiling

The strongest permitted negative landing is bounded:

```text
LOCAL_REGULAR_ZERO_AND_FIRST_JET_OBSERVABLE_SURJECTION_DERIVED
__COMMON_SKY_GRAM_AND_GENERIC_MEASURE_CONSISTENCY_ONLY
__NO_NONTRIVIAL_SOURCE_INDEPENDENT_PATTERN_RESTRICTION_OWNED_IN_FROZEN_SOURCE_UNIVERSE
__GLOBAL_CRITICAL_BOOTSTRAP_AND_SOURCE_HISTORY_JOINTS_OPEN
```

An actual stronger restriction, if found, replaces this wording and must identify its exact owner and
excluded witness. No result may reject UDT, predict BAO, select a history/source law, infer `X_max`, or
open the BOSS holdout.
