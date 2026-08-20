# G183 external-review repair preregistration

Date: 2026-08-19

External review returned `G183_REPAIR_REQUIRED` for one packaging defect only: the exact commanded
entrypoint `python3 verify_package.py` reran all children read-only but attempted to write its own
`VERIFICATION_RESULT.json` in the sealed read-only sandbox.

## Frozen repair

1. Make `verify_package.py` read-only by default, including its own result.
2. Permit result emission only when the caller explicitly sets `UDT_WRITE_VERIFICATION_RESULT=1`.
3. Update `EVIDENCE_GATES.md` to state the literal default entrypoint used.
4. Add an executable catch proving that the default verifier does not alter package hashes.
5. Build a fresh sealed intake and request a repair-only follow-up review.

No theorem, witness, numerical count, source hash, landing, scope, or conclusion ceiling may change
under this repair. Any scientific change requires a new preregistration and full review.
