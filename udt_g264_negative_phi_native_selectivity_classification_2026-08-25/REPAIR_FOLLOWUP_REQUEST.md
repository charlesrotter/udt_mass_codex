# G264 repair-only external follow-up request

Verify only repairs R1-R3 registered in `REPAIR_PREREGISTRATION.md` and confirm that the bounded G264
scientific landing and ownership ceiling remain unchanged.

Required checks:

1. Confirm `verify_metric_first.py` derives its tensors from metric component jets before comparing
   with target closed forms, and imports neither SymPy, production code, nor saved results.
2. Rerun `verify_metric_first.py`, `verify_independent.py`, `verify_repair_catches.py`, and
   `verify_package.py` in the writable ephemeral copy.
3. Confirm the older verifier is now consistently described as a result-blind implementation-
   distinct consistency replay, not a metric-first derivation.
4. Confirm the original landing, thresholds, counterfamily, conditional scope, and `OPEN` physical
   history/`X_max` status are unchanged.
5. Attempt bounded altered-copy attacks against the repair verifier.

Return `ACCEPT_REPAIR` or `REJECT_REPAIR`. Do not continue the research or propose a new law.
