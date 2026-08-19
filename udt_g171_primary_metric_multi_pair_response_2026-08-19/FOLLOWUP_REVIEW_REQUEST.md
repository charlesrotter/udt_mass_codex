# G171 packaging-only follow-up review

Read `REPAIR_PREREGISTRATION.md`, `EXTERNAL_ADVERSARIAL_REVIEW_RAW.md`, and
`REVIEW_EXECUTION_BOUNDARY.md` inside the corrected sealed intake.

Verify only the registered packaging repair:

1. Confirm `REVIEW_SCOPE.json` is complete and byte-exact.
2. Confirm the intake now contains `build_review_intake.py`.
3. Run:

   ```text
   python3 /intake/udt_g171_primary_metric_multi_pair_response_2026-08-19/verify_sealed_intake.py
   ```

4. Confirm it returns `gate=SEALED_INTAKE_REPLAY`, 12 source hashes, 31 production checks,
   108,000 independent checks, 14 catches, and `PASS__SEALED_G171_REPLAY` without editing the seal.
5. Confirm `VERIFICATION_RESULT.json` now identifies itself as the separate
   `REPOSITORY_OUTER_GATE`.
6. Confirm the scientific landing and boundaries were not changed.

Return exactly one:

- `PACKAGING_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`;
- `SEALED_REPLAY_STILL_NOT_REPRODUCIBLE`;
- `SCIENTIFIC_LANDING_CHANGED_OR_UNSUPPORTED`;
- or a more precise repair-only result.

Do not reopen or continue the scientific research.
