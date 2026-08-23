# G238 external repair-only follow-up

Review model: external Codex reviewer (`gpt-5.4`, high reasoning, web disabled)

Sealed intake: `/tmp/udt_g238_repair_followup_benq7eo9`

`REVIEW_SCOPE.json` SHA-256:
`dd83b37673a60a949927a7d96c2da63f9b6741bff779ca4cb4b563b9934164c9`

Tree SHA-256:
`9483e18b035312e6901de46e4ebab229323536602dffaf7be11ebb55475dae3d`

Raw returned review SHA-256:
`96baa236d563866fe3e3e37d84d224da9c12d502b355b2fa2937d42b0ad41c49`

## Verdict

`G238_REPAIRS_ACCEPTED__SCIENTIFIC_LANDING_RETAINED`

## Load-bearing findings

- All 42 declared payload hashes and the tree digest matched.
- R1 passed. The coefficient route parses the actual frozen JSON decimals exactly, converts them
  to rational numbers, normalizes those actual knots, vanishes at all 12 roots, and has nonzero
  `q`, `q'`, and `q''` at the registered exact midpoint.
- The saved roots are not the idealized `i/11` grid. The independent route reconstructs the same
  quantities by direct products and logarithmic-derivative identities without building polynomial
  coefficients.
- The package validator recomputes the actual roots and midpoint from the frozen state. The hostile
  idealized-root substitution is caught.
- The bounded landing is unchanged: BOSS outcomes remain closed, no interpolation or profile fit
  was performed, the six upstream operator stages remain `OPEN`, and Q15 remains
  `QUERY_TYPING_INCOMPLETE`.

## Replay results

- R2 passed. The reviewer copied the read-only intake into a new writable disposable directory and
  ran `py_compile`, the exact derivation, independent verification, package verification, and all
  hostile catches. Every command passed.
- The sealed replay has no dependency on an intake-absent project file. It uses only package-local
  files and the 15 manifest-listed sources.

## Remaining repair

None within the preregistered R1/R2 scope.

## Maximum retained scientific conclusion

`QUERY_TYPING_INCOMPLETE__NO_OUTCOME_OPENING`
`__FROZEN_SNE_STATE_DOES_NOT_DETERMINE_CONTINUOUS_METRIC_OR_SCREEN_HISTORY`
`__COMPLETE_METRIC_EVALUATORS_REMAIN_LIVE_CONDITIONALLY`
`__TWO_SOURCE_POPULATION_AND_REFERENCE_FORWARD_MAP_OPEN`

