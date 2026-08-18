# G160 preregistration — three-observer time-live pair-first-jet carry

Date: 2026-08-18

Status at registration: `PREREGISTERED__NO_G160_OUTCOME_EXECUTED`

## Whole question

For supplied smooth regular observer-pair metric families and supplied typed smooth carries

\[
M_{BA}:V_A\to V_B,
\qquad M_{CB}:V_B\to V_C,
\qquad M_{CA}:V_A\to V_C,
\]

derive the exact time-live carry of `(h,dot h)` and its terminal coefficients. Determine whether
direct and staged carry agree precisely when the finite carries and their first jets close, and
separate the intrinsic target first jet from the moving-carry connection terms without promoting
that presentation split to a gauge-independent physical decomposition.

## Bounded regime

- one common supplied smooth parameter `lambda`, with no physical interpretation assigned;
- regular Lorentzian pair metrics with a supplied timelike clock column;
- arbitrary orientation-preserving `GL+(2)` carries and live endpoint carrier gauges;
- direct and composite three-observer routes;
- the existing positive upper-triangular `B+(2)` flag-preserving subcase;
- exact first derivatives only.

This is metric-led tensor algebra. It characterizes every supplied regular carry in the stated
class; it does not filter the class to a desired response.

## Premise ledger

- `pinned-by-THEORY`: G159 pair first jet and live rechart law;
- `pinned-by-THEORY`: G142 typed carry orientation and composition convention;
- `pinned-by-THEORY`: G156 determinant/half-density character;
- `free-and-explored`: all entries of `h_i`, `dot h_i`, `M_ji`, and `dot M_ji` subject only to
  regularity, orientation, and typed composition;
- `free-and-explored`: finite and first-order closed and nonclosed carry triangles;
- `pinned-by-HABIT`: none;
- `omitted`: null/degenerate/singular/cut/topology-changing strata, branch creation, path choice,
  history/query selection, observations, `X_max`, light, action, source, bootstrap, matter, mass,
  dynamics, and global completion.

## Candidate structure to test

For one carry `M=M_BA`, target metric `h_B`, and right rate `K=dot M M^-1`, test

\[
\bar h_{B|A}=M^T h_BM,
\]

\[
\dot{\bar h}_{B|A}
=M^T(\dot h_B+K^Th_B+h_BK)M.
\]

For a closed triangle `M_CA=M_CB M_BA`, test exact staged/direct equality and

\[
K_{CA}=K_{CB}+\operatorname{Ad}_{M_{CB}}K_{BA}.
\]

Test live endpoint-gauge covariance, the direct-carry defect and its first derivative, the universal
determinant/common-scale rate, and whether reciprocal/shift characters require the existing
flag-preserving `B+(2)` restriction.

## Preregistered outcome classes

Exactly one primary class will be returned:

1. `TIMELIVE_CARRY_TYPE_FAILURE`;
2. `FINITE_CARRY_COMPOSES__FIRST_JET_CARRY_FAILS`;
3. `FIRST_JET_CARRY_DERIVED__TERMINAL_RATE_CLASSIFICATION_INCOMPLETE`;
4. `TIMELIVE_PAIR_FIRST_JET_CARRY_DERIVED__FULL_GLPLUS2_TENSOR_AND_CONNECTION_COMPOSITION__TERMINAL_CHARACTER_BOUNDARY_CLASSIFIED`.

## Certification and falsification contract

Outcome 4 requires:

1. exact arbitrary-matrix derivation of direct and staged pullback first jets;
2. exact right-rate composition and direct-route defect law;
3. exact live independent endpoint-gauge covariance;
4. proof that only the metric-self-adjoint part of carry rate reaches the pulled pair first jet;
5. complete terminal-rate formulas over regular `GL+(2)` plus exact `B+(2)` character/shift control;
6. a witness that determinant/reciprocal scalar closure can miss a nonzero matrix-rate defect;
7. independent exact implementation, mutation catches, and fresh adversarial review;
8. explicit retention of physical carry, history, query, `lambda`, and global scope as open.

Any order error, frozen endpoint gauge, false scalar invariance, or promotion of the supplied carry
to physical law rejects outcome 4.

## Maximum conclusion

G160 may derive and classify the first-order kinematics of a supplied regular three-observer carry.
It may not derive which carry, query, or history Nature realizes; make the connection split an
observable; impose fixed channel ratios; or infer dynamics or downstream physics.
