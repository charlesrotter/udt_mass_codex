# G270 external-review repair preregistration

Date: 2026-08-26
Status: `PREREGISTERED_BEFORE_REPAIR_OUTCOME_COMPUTATION`

The external reviewer returned `ACCEPT_WITH_REPAIRS`. The scientific landing is frozen and may not
change during these repairs.

## R1 — implementation-level mutation coverage

Replace the single hand-written claim-dictionary mutation count with two honestly separated gates:

1. exact arithmetic mutations that alter the frame, pullback, completion, transported mismatch, or
   mutual-readout implementation and must be caught by mathematical invariants; and
2. typed status-ledger mutations that must remain explicitly labelled as consistency checks rather
   than implementation mutations.

Falsifier: any registered implementation mutation survives its targeted invariant, or the report
continues to describe ledger-only mutations as implementation-level evidence.

## R2 — off-axis ribbon regularity

Add a production symbolic identity for the full ribbon determinant and an exact positivity proof on
the declared half-ribbon `lambda>=0`, for all real `tau`. Add implementation-distinct rational
off-axis samples spanning positive and negative `tau`.

Falsifier: the determinant fails to remain negative on that declared domain, the independent replay
finds a non-Lorentzian off-axis sample, or the automated evidence is still described as axis-only
support for a neighborhood claim.

## Required retained landing

```text
FULL_SUPPLIED_REALIZATION_EVALUATES_TRANSPORTED_SCREEN_MISMATCH
__COMPLETED_PAIR_DUAL_RECIPROCITY_NORMALIZES_ONLY_THE_INTRINSIC_PULLBACK
__EXACT_SAME_PULLBACK_TILTED_NULL_RIBBONS_HAVE_DIFFERENT_W
__NO_UNIVERSAL_W_VALUE_POPULATION_HISTORY_DISTANCE_OR_XMAX_SELECTION
```

No observation, fit, distance attachment, history law, source, matter, `X_max`, transfer,
signalling, or canonization may enter.
