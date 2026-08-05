# Conceptual object-type dependency audit

Read in this order:

1. `PREREGISTRATION.md`
2. `AUDIT_REPORT.md`
3. `LAY_REPORT.md`
4. `OBJECT_TYPE_LEDGER.tsv`
5. `CSN_PROVENANCE_CHAIN.tsv`
6. `DEPENDENCY_IMPACT.tsv`
7. `FOUR_GATES.md`

`SOURCE_INVENTORY.tsv` freezes the 28-source input universe. `AUTHORIZED_MUTATIONS.tsv` records the
three current-registry/guard changes. `verify_object_type_audit.py` is the independent semantic and
source verifier; `verify_repository_gates.py` replays repository preservation gates.

The package changes no equations or historical evidence. Its grade is `VERIFIED-WITH-CAVEATS`
because no fresh external semantic review was authorized for this exact payload.
