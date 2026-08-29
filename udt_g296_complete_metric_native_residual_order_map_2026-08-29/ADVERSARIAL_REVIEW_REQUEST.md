# G296 repair-only follow-up review request

The prior fresh review returned `G296_ACCEPT_WITH_REPAIRS`. Verify only repairs R1–R3 below and
that the bounded scientific landing remains unchanged:

```text
COMPLETE_METRIC_IS_A_MINIMAL_FAITHFUL_PRIMITIVE_STATE
__SECOND_METRIC_DERIVATIVE_ORDER_IS_THE_FIRST_LOCAL_NATURAL_NONIDENTITY_HOME
__CURRENT_PREMISES_DO_NOT_PRIVILEGE_ONE_RESIDUAL_FORM
```

## R1 — chronology proof

Without Git or repository access, run `verify_prereg_ancestry_proof.py`. Independently audit the raw
commit and linked tree object hashes in `PREREG_ANCESTRY_PROOF.json`. Confirm that commit
`f7a050f0` contains exactly the four declared G296 preregistration files and no implementation or
outcome files.

## R2 — self-contained dependency-free replay

In an empty writable copy, run every command in `COMMANDS.md` with the isolated environment's
Python. Confirm that:

- no third-party package is required;
- the production calculation uses the exact sparse-polynomial engine;
- the independent calculation remains the separate pointwise `Fraction` tensor reconstruction and
  imports neither production code nor output;
- all 32 production checks, 3,080 independent assertions over 128 cases, 13 hostile catches, 16
  source hashes, and the aggregate verifier pass;
- repository-wide integration gates are not misrepresented as sealed commands.

## R3 — bounded scalar wording

Confirm that `EXACT_DERIVATION.md`, `STATUS_LEDGER.tsv`, `AUDIT_REPORT.md`, and
`ARCHITECTURE_CLASSIFICATION.tsv` restrict the negative to the tested scalar-only lane—scalar
curvature, Ricci square, and Kretschmann scalar—and retain the positive nonscalar Riemann result.
Reject any unproved claim classifying every conceivable scalar construction.

## Scientific noninterference

Confirm that the repairs do not change the frozen landing, select a residual equation, promote the
G259 class, introduce a new state, import observations or field dynamics, or alter the G286
characteristic-data correction.

## Required verdict

Return one of:

- `G296_REPAIRS_VERIFIED__BOUNDED_SCIENTIFIC_LANDING_RETAINED`;
- `G296_REPAIR_INCOMPLETE`, identifying the exact failed repair;
- `G296_SCIENTIFIC_LANDING_CHANGED`, with a concrete change or refutation.

Inspect only the sealed intake. Use a writable ephemeral copy for checks. Do not edit evidence
files or continue the research.
