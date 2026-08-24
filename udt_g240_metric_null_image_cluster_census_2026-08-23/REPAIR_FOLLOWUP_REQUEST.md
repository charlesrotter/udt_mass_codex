# G240 repair-only follow-up request

Review only the preregistered R1 sealed-replay repair. The bounded scientific landing is frozen.
Do not continue the research and do not inspect observational outcomes.

## Required checks

1. Confirm `verify_package.py` selects `REPOSITORY_ROOT` in the repository and
   `SEALED_SOURCES_ROOT` only when the intake-root `REVIEW_SCOPE.json` declares a sealed replay.
2. Confirm there is no silent multi-root probing or ambiguous fallback.
3. Run `python3 verify_package.py --no-write` on the sealed intake exactly as delivered. It must
   pass without mirroring, moving, or editing any evidence file.
4. Run `python3 build_review_intake.py` in a writable ephemeral copy. Confirm that its as-delivered
   replay passes and its missing-`sources/` negative control fails closed for the registered reason.
5. Verify all eleven source hashes, the repaired scope/manifest counts, and the unchanged G240
   scientific landing.
6. Confirm that no observational outcome, new physics, physical detector/transfer law, or broader
   claim entered during repair.

## Required landing

Return exactly one primary verdict:

```text
G240_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED
G240_REPAIR_INCOMPLETE__SCIENTIFIC_LANDING_RETAINED
G240_SCIENTIFIC_LANDING_REQUIRES_REOPENING
```
