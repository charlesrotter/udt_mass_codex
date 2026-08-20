# G184 repair-only external follow-up request

## Frozen first verdict

The first external verdict was `G184_REPAIR_REQUIRED`. It independently reproduced the scientific
witnesses and identified only this defect: `verify_default_read_only_entrypoint.py` wrote its JSON
artifact on a default invocation, while `verify_package.py` trusted rather than live-replayed it.

## Permitted review scope

Verify only the preregistered repair:

1. Run `python3 verify_package.py` from the package root in the sealed read-only intake.
2. Confirm its replay table contains a successful live
   `verify_default_read_only_entrypoint.py` entry and reports `helper_live_replayed:true`.
3. Run `python3 verify_default_read_only_entrypoint.py` directly with no environment variables.
4. Confirm both commands pass and change no intake hash.
5. Inspect the two verifier scripts and confirm recursion is prevented only by the nested
   `G184_SKIP_DEFAULT_CHECK=1` path.
6. Confirm the original repair-required review remains preserved.
7. Confirm no arena, equivalence relation, witness, count, derivation, landing, choice ledger,
   falsifier, or conclusion ceiling changed.

Do not edit files, continue the research, reopen the scientific theorem, or access anything outside
the intake.

Return exactly one:

```text
G184_REPAIR_ACCEPTED
G184_REPAIR_INCOMPLETE
G184_SCIENTIFIC_LANDING_CHANGED
```
