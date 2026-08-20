# G187 repair-only follow-up request

The first review returned `G187_ACCEPTED_WITH_STATED_BOUNDS` and identified one certification
defect: literal scope sentinels were mislabeled as executable mutation catches.

Verify only the registered repair:

1. `run_catch_proofs.py` contains no literal `True` placeholder;
2. its 15 algebraic mutation catches execute and pass;
3. its 14 artifact-scope guards mutate the relevant text in memory and pass;
4. `CATCH_PROOF_RESULT.json` exactly matches live output;
5. `verify_package.py` checks the repaired counts;
6. no scientific formula, landing, premise, source, or scope ceiling changed.

Return exactly one:

- `G187_CERTIFICATION_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`
- `G187_CERTIFICATION_REPAIR_REJECTED__<EXACT_REASON>`

Do not continue the research and do not edit files.
