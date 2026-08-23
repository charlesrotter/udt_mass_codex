# G238 external-review repair preregistration

This repair scope is frozen before changing the load-bearing G238 derivation, verifier, results, or
replay surface.

External verdict:
`G238_REPAIR_REQUIRED__SCIENTIFIC_LANDING_RETAINED`.

## R1 — actual frozen-knot counterfamily

Replace the idealized roots `i/11` with exact rational values parsed from the decimal spellings of
the 12 frozen G237 knots. Affinely normalize those actual values only for arithmetic conditioning;
the normalized roots must be calculated from the supplied knots rather than assumed uniform.

The registered between-knot evaluation point is the exact midpoint of the first two actual
normalized roots. The coefficient route must certify, with exact rational arithmetic:

- all 12 actual normalized knot values of `q` are zero;
- `q`, `q'`, and `q''` are nonzero at the registered midpoint;
- the result records the actual normalized roots and evaluation point.

The independent route must reconstruct the same three quantities without constructing polynomial
coefficients, using direct products and logarithmic-derivative identities over the actual roots.

Add a hostile control that perturbs one stored normalized root in the result and requires the
package validator to fail. The validator must explicitly compare recorded roots and evaluation
point against values recomputed from the frozen state.

Falsifier: any actual frozen knot fails exact zero evaluation, any registered midpoint quantity is
zero, or the two independently implemented routes disagree.

## R2 — self-contained sealed replay

Separate repository-production commands from the sealed external replay:

- repository production may write the registered JSON evidence and run the repository-wide
  premise verifier;
- sealed replay must instruct the reviewer to make an ephemeral copy writable before any registered
  write/replay command;
- the sealed command list must not claim an absent repository-wide verifier is available inside the
  intake.

The corrected intake builder must retain the restriction that checks run only in an ephemeral copy.

Falsifier: following the corrected sealed instructions from the corrected sealed intake fails due
to permissions, missing registered files, or an instruction to invoke an absent file.

## Retained bounded landing

Neither repair may change the scientific conclusion or open BOSS outcomes. The maximum retained
landing remains:

`QUERY_TYPING_INCOMPLETE__NO_OUTCOME_OPENING`
`__FROZEN_SNE_STATE_DOES_NOT_DETERMINE_CONTINUOUS_METRIC_OR_SCREEN_HISTORY`
`__COMPLETE_METRIC_EVALUATORS_REMAIN_LIVE_CONDITIONALLY`
`__TWO_SOURCE_POPULATION_AND_REFERENCE_FORWARD_MAP_OPEN`.

If either repair changes that conclusion, exposes an outcome dependency, imports an interpolation
or feature fit, or fails the independent exact replay, stop and regrade rather than accepting the
repair.
