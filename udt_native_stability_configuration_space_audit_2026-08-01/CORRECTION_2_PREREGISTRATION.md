# Cold-review correction 2 preregistration

Date: 2026-08-01  
Trigger: fresh cold adversarial review, before result banking

## Defect

The object ledger currently marks the P4 constant-moduli and field-moduli objects as simply not
belonging to the native parent type, while the parent-relation matrix records only their mutual
constant-section/pullback relation. That loses a relation explicitly stamped in the frozen P4
sources: both are conditional domains read on the registered positive-triangular/BASE coframe arena.

## Exact correction

1. Change only the `belongs_to_native_parent_type` cells for `O07` and `O08` from `no` to
   `conditional_only`.
2. Add explicit relations from each P4 object to `complete_metric_arena` with status
   `CONDITIONAL_SUBDOMAIN` and premise-preserving scope.
3. Update mechanical relation counts, verifiers, prose, and dependent hashes.

This must not select either census, equate their stationary sets, turn the registered BASE chart into
the unique complete UDT metric, or promote either conditional domain into a native realized family.
The preregistered primary outcome remains unchanged unless the corrected relation reveals an
additional native realization/variation selector; in that event, stop for re-adjudication.
