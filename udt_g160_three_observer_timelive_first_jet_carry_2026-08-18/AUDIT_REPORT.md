# G160 audit report — three-observer time-live pair-first-jet carry

Date: 2026-08-18

## Primary landing

`TIMELIVE_PAIR_FIRST_JET_CARRY_DERIVED__FULL_GLPLUS2_PULLBACK_AND_RIGHT_CONNECTION_COMPOSITION_EXACT__CARRY_CLOSURE_SUFFICIENT_NOT_NECESSARY_DUE_TO_LORENTZ_STABILIZER__ONLY_COMBINED_CARRIED_FIRST_JET_IS_LIVE_SOURCE_GAUGE_COVARIANT__JOINED_TOTAL_RATE_IS_LIVE_ENDPOINT_GAUGE_INVARIANT__KAPPA_HAS_UNIVERSAL_DETERMINANT_RATE__NO_PHI_BETA_CARRY_ONLY_LAW_ON_UNRESTRICTED_GLPLUS2__BPLUS2_SUFFICIENT_NOT_NECESSARY_FOR_EXACT_CHARACTER_LAWS__SCALAR_RATE_CLOSURE_WEAKER_THAN_MATRIX_RATE_CLOSURE__PHYSICAL_CARRY_HISTORY_QUERY_LAMBDA_AND_COMPLETION_OPEN`

## What was learned

For every supplied smooth regular carry, the transported pair first jet is

\[
\dot{\bar h}=M^T(\dot h+K^Th+hK)M,
\qquad K=\dot MM^{-1}.
\]

Direct and staged `A -> B -> C` transport agree whenever the supplied carry network closes, and
the right rates compose by `K_CA=K_CB+Ad(M_CB)K_BA`. The converse fails because Lorentz stabilizers
can hide finite and infinitesimal carry defects from `(h,dot h)`. Only the metric-self-adjoint part of `K` changes
the carried pair metric. The intrinsic/connection split itself is presentation-dependent; only the
combined carried first jet and joined total comparison rate have the lawful live-gauge behavior.

Common scale has the universal rate character

\[
\dot{\bar\kappa}=\dot\kappa+\tfrac12\operatorname{tr}K.
\]

Over unrestricted `GL+(2)`, reciprocal and shift changes also depend on the transported clock line
and target metric, so no universal carry-only law exists there. Their exact character/semidirect
laws hold on positive flag-preserving `B+(2)`, which is sufficient but not necessary for every
special exact carry. A strictly upper-triangular rate defect is invisible to both common-scale and
reciprocal scalar checks, so full matrix-rate closure remains stronger.

## Meaning

No new mechanism is needed to carry the changing local orchestra once a typed carry is supplied.
Its time-live law is forced by tensor differentiation. What remains open is not the kinematic law;
it is which cross-query carry and history are physical.

## Evidence gates

- preregistration commit `d7d81015` predates outcome execution;
- 10 exact frozen sources at `4a89d922`;
- 13 exact symbolic checks;
- independent standard-library Fraction/dual-number replay: 500 trials in each registered class,
  including general carry, `B+(2)`, nonclosed defects, terminal rates, live gauge, and composition;
- 11 algebraic mutation catches plus 4 semantic metadata guards;
- fresh adversarial repair follow-up `PASS`;
- 147-row premise verifier `PASS`;
- repository tests: 120 passed, 1 expected XFAIL;
- fail-closed package verification `PASS` after the final rerun.

## Maximum conclusion

G160 derives the full regular first-order kinematics of a supplied three-observer pair carry and the
exact boundary between universal tensor/common-scale transport and flag-dependent reciprocal/shift
characters. It does not derive the physical carry, history, query population, meaning of `lambda`,
or any downstream physics. No canonization is requested or performed.
