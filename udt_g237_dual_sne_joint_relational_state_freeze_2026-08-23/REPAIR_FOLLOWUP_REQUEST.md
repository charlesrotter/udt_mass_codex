# G237 repair-only external follow-up request

The first fresh review returned `G237_SCIENTIFIC_OR_EVIDENCE_REPAIR_REQUIRED` while accepting the
scientific core. Verify only the four repairs preregistered in `REPAIR_PREREGISTRATION.md`. Do not
reopen or continue the research.

## Required checks

1. **R1 wording:** confirm that `LAY_REPORT.md` no longer asserts statistical independence and that
   its uncertainty language remains consistent with the chosen zero cross-release covariance.
2. **R2 chronology:** run `verify_chronology_bundle.py` from the sealed intake without a live Git
   repository. Independently inspect whether it proves commit object → root tree → G237 package tree
   → preregistration blob → current preregistration content.
3. **R3 command/payload alignment:** confirm that `COMMANDS.md` separates repository-side export
   from self-contained sealed replay and that every registered replay helper is in the payload.
4. **R4 covariance label:** confirm that `INDEPENDENT_RAW_GLS.json` carries the full chosen-covariance
   caveat and that `verify_repair.py` proves this is the only change to that artifact.
5. Confirm the SHA-256 identity of `JOINT_STATE_RESULT.json`, `FROZEN_PRIMARY_K12_STATE.json`, and
   `JOINT_STATE.tsv` against the preregistered anchors.
6. Run the registered sealed replay and confirm that the scientific landing and every load-bearing
   number are unchanged.

Return exactly one:

- `G237_REPAIRS_ACCEPTED__SCIENTIFIC_LANDING_RETAINED`
- `G237_REPAIR_INCOMPLETE`
- `G237_REPAIR_CHANGED_SCIENTIFIC_RESULT`

List any required defect separately from optional improvement. Do not propose a profile, inspect a
held-out outcome, or continue the research.
