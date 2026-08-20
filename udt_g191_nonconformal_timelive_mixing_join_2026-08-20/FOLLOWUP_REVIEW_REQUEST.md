# G191 repair-only follow-up review request

Inspect only the corrected sealed intake. Do not edit files or continue the research. Run only the
registered no-write replay.

Verify only:

1. the eight frozen upstream sources now occupy the repository-relative paths recorded by
   `SOURCE_MANIFEST.tsv`;
2. the bounded sealed replay no longer assumes the repository-wide startup verifier is present;
3. the registered replay completes end-to-end without writes;
4. `PRODUCTION_RESULT.json`, `INDEPENDENT_VERIFICATION.json`, and `CATCH_PROOF_RESULT.json` are
   byte-identical to the first reviewed intake;
5. no scientific formula, premise status, tolerance, or bounded landing changed.

Return exactly one:

- `G191_ACCEPTED_WITH_STATED_BOUNDS`;
- `G191_REPAIR_REQUIRED`;
- `G191_SCIENTIFIC_LANDING_REJECTED`.

