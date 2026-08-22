# G213 repair-only follow-up preregistration

Date: 2026-08-22

The fresh external reviewer returned
`G213_REQUIRES_REPAIR_BUT_BOUNDED_LANDING_SURVIVES`, found no bounded scientific defect, and
requested two certification repairs.

## Frozen repairs

1. Remove the undeclared `sympy` runtime dependency from the registered aggregate replay by
   replacing its symbolic replay pieces with dependency-free exact integer/Fraction algebra.
2. Extend the independent dependency-free verifier to replay the explicit five-mode coefficient
   rank, the G207/G208 four-column rank, and completion by the grading column.
3. Correct the evidence wording so it distinguishes independent algebraic coordinate coverage
   from the separately audited frozen-source provenance mapping.

## Frozen checks

- The registered command must pass in a sealed standard-library-only Python environment.
- Production and hostile-control scripts must import no third-party module.
- The independent verifier must report full mode rank `5`, G207/G208 union rank `4`, and grading
  completion rank `5` in addition to the existing 10,000 completed-tuple cases and exact G129 rank.
- The aggregate replay must remain fail-closed, hash all registered core evidence before and after,
  and preserve the scientific landing and all supplied-premise caveats.

## Ceiling

No equation, decomposition, source mapping, witness, premise status, global claim, physical germ
population claim, or observational conclusion may be strengthened in this repair. A scientific
change requires a new audit rather than this repair-only channel.
