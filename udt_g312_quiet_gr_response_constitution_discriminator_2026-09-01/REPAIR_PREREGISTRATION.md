# G312 repair preregistration

Date: 2026-09-01

External verdict: `G312_REPAIRABLE_DEFECTS__LANDING_RETAINED`.

The reviewer found no scientific defect in the bounded G312 landing. This repair is frozen before
changing the intake builder. It may not alter the scientific question, either independence witness,
the premise ledger, or the bounded conclusion.

## R1 — intake-self-contained aggregate replay

Add the already registered `build_review_intake.py` to the exact package-file tuple copied by that
builder. Rebuild a fresh sealed intake and verify in a writable ephemeral copy that:

```bash
python3 -S package/verify_package.py
```

runs successfully using only files inside the intake.

Falsification: R1 fails if the builder remains absent, the aggregate replay accesses repository
state, any scientific output changes, or the repaired intake cannot reproduce 4,690 production
checks, 4,824 independent checks, and six semantic regression catches.

## Retained landing

```text
TWO_OR_MORE_INDEPENDENT_NEW_PREMISES_ARE_REQUIRED
```

The two clauses remain:

1. `FULL_QUIET_GR_PRINCIPAL_RESPONSE_OVERLAP`;
2. `LOCAL_FINITE_JET_RESPONSE_CONSTITUTION`.

A fresh repair-only external follow-up is required before G312 can be graded
`G312_ACCEPTED_WITH_TWO_PREMISE_BOUNDARY`.
