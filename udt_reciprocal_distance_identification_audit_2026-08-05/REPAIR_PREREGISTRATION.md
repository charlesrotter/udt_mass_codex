# Repair preregistration — adversarial scope-gate correction

Date: 2026-08-05

External verdict: `ACCEPTED_WITH_REPAIRS`

## Defect reproduced before mutation

The external reviewer correctly found that `verify_audit.py` used
`git diff --name-only BASE` as its audit-package scope gate. That command sees tracked differences
but not new untracked package files. At review time it therefore saw only the committed
`PREREGISTRATION.md`, while the substantive audit files were present as untracked files.

The protected 83-path curvature-atlas metadata gate was valid, and the reviewer did not refute the
bounded mathematical theorem. The defective claim is specifically the mechanical assertion that
the verifier had already proved the complete changed-file scope.

## Frozen repair scope

1. Preserve the external review verbatim.
2. Define the exact expected audit-package path set.
3. Combine tracked differences from the registered base with untracked status paths.
4. Require the combined audit set to equal the expected package exactly.
5. Require all other untracked paths to equal the protected 83-path set exactly.
6. Add an exercised catch-proof that an extra untracked path outside those two sets fails.
7. Update the report and overall ledger row only to record the review and repair status.
8. Rerun the primary, independent, semantic, source-hash, protected-metadata, premise-registry,
   repository-test, and diff-hygiene gates.

No equation, derivation, countermodel, scientific status other than review closure, source artifact,
or protected curvature-atlas path may change.

## Certification contract

The repair passes only if:

- the exact expected package is present once, whether each path is tracked or still untracked;
- a synthetic extra untracked file is rejected by the same scope predicate;
- the protected set remains 83 paths with the registered path and metadata hashes;
- the external verdict remains `ACCEPTED_WITH_REPAIRS` and the required repair is disclosed;
- all prior mathematical checks and catch-proofs still pass; and
- no path outside this audit package is changed relative to base.

Maximum conclusion after a passing repair:

```text
EXTERNAL_ADVERSARIAL_REVIEW_ACCEPTED_THE_BOUNDED_THEOREM_AFTER_A_MECHANICAL_SCOPE_GATE_REPAIR;
NO_COMPLETE_PHYSICAL_DISTANCE_LAW_OR_DOWNSTREAM_PHYSICS_IS_DERIVED
```
