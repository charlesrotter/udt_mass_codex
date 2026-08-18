# G149 audit report — genuine spacetime complete-pair first-jet join

Date: 2026-08-17

## Landing

```text
VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_FOLLOWUP_PASS__
EXPLICIT_SMOOTH_COMPLETE_SPACETIME_QUERY_WITNESS__
PAIR_CLOCK_DERIVED_DOTPHI__LEVI_CIVITA_DERIVED_AN_OMEGA__
G148_COVARIANT_IDENTITY_EXACTLY_REALIZED__
ALL_BQS_SPACETIME_GRADIENT_FAMILIES_AND_PAIR_CLOCK_DIRECTION_YZ_FIRST_JETS_LIVE_IN_THE_REGISTERED_WITNESS__
PHYSICAL_HISTORY_DYNAMICS_REGIME_AMPLITUDES_AND_GLOBAL_COMPLETION_OPEN
```

## What was learned

G148's relation-first first-jet identity is not confined to an abstract algebraic matrix family.
On one preregistered smooth local complete metric and one smooth calibrated pair immersion, the
same geometry supplies:

- terminal pair depth and its normalized clock derivative `dot(phi_pair)`;
- the Levi-Civita connection;
- pair-frame radial acceleration component `a_n`;
- pair-screen turn `Omega`;
- the direct covariant derivative of `xi=X_max tanh(phi_pair)n`.

The direct derivative and the three-term decomposition agree exactly. Every registered `B,Q,S`
spacetime-gradient family and every pair-clock-direction `Y,Z` first-jet family changes at least one
of `dot(phi_pair),a_n,Omega` in the frozen witness.

This is a coherent local chord from one supplied geometry, not a post-processing sum.

## What remains open

- `xi=X_max tanh(phi_pair)n` remains a chosen working relation-first representation.
- One witness does not select the physical metric history or query family.
- `F_sigma_sigma` and the pair-`sigma` first jet were not tested for liveness.
- The coefficient functions `sech(phi)^2` and `tanh(phi)` do not determine the amplitudes of
  `dot(phi_pair),a_n,Omega`.
- No loud--quiet--loud physical regime law, dynamics, action, source, bootstrap condition,
  numerical `X_max`, proper length, or observation follows.
- Coincidence, reversal, cross-query carry, null/degenerate/cut/singular strata, and global
  completion remain outside this local result.

## Exact and numerical gates

```text
production exact gates: PASS
independent base identity replay: PASS
independent five-control liveness replay: PASS
base identity residual max: 8.67e-19
base production disagreement max: 1.74e-18
control-delta disagreement max: 9.10e-18
package verifier before review-file inclusion: 45/45 PASS
fresh adversarial review: REPAIR_REQUIRED
repair-only follow-up: FOLLOWUP_PASS
```

## Banking gates

1. Preregistered: yes, commit `1a30aa0d` before any result.
2. Full space or bounded scope: explicitly one local smooth witness; no full-space claim.
3. Independently verified: yes, separate NumPy implementation including all five controls.
4. Premise-audited: yes, with working representation, witness choice, and open physics explicit.

The result is therefore bankable as `VERIFIED_WITH_CAVEATS` in its narrow scope.

## Next bounded question

Do not immediately fit observations or call the witness a history law. The next metric-led question
is whether the first-jet chord has any further history-independent invariant beyond the exact G148
identity. If no such invariant exists at first order, record that ceiling and move once—rather than
surveying arbitrary witnesses—to the smallest second-jet curvature/Jacobi join that can relate how
the chord changes along a supplied co-present pair family.

