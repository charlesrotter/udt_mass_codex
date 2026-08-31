# G307 repair-only follow-up request

Review only the corrected sealed intake. Verify the preregistered R1--R4 repairs and the unchanged
bounded G307 landing. Do not reopen or continue the research.

## Frozen scientific landing

```text
SUPPLIED_DIRECTED_GERM_SELECTS_ONE_MEMBER_PER_CHIRAL_FAMILY
__SIGNED_TRANSVERSE_SCREEN_GERM_SELECTS_ONE_MEMBER_CONDITIONALLY
__ACTIVE_PREMISES_POPULATE_NEITHER__PHYSICAL_MEMBER_REMAINS_OPEN
```

The production result, member census, metric, reciprocal kernel, and ownership boundary must be
unchanged.

## Checks

1. **R1:** From a writable copy of this sealed intake, run `build_review_intake.py` and
   `verify_repair_portability.py`. Confirm repository/sealed rebuild equivalence and rejection of
   missing and ambiguous source/current layouts.
2. **R2:** Inspect and run `verify_directed_member_independent.py`. Confirm it now reconstructs both
   family members from `(p,v)` through independently built evaluation maps, proves numerical
   injectivity, recovers `v conjugate(p)` and `conjugate(p) v`, reconstructs the full operators,
   imports no production function, and supplies at least 30,000 checks.
3. **R3:** Inspect and run `run_catch_proofs.py`. Confirm at least eight direct exact mathematical
   corruptions are exercised in addition to semantic result/ownership guards.
4. **R4:** Confirm `COMMANDS.md` clearly distinguishes sealed package replays from repository-only
   premise/pytest gates and makes no false self-contained premise-verifier promise.
5. Run the production derivation and `verify_package.py`; confirm the exact production result and
   landing are unchanged and all repaired evidence agrees.

## Required verdict

Lead with exactly one token:

- `G307_REPAIRS_ACCEPTED`
- `G307_REPAIRS_INCOMPLETE`
- `G307_SCIENTIFIC_REGRESSION`
- `G307_INCONSISTENT_OR_UNCLASSIFIED`

List defects and commands run. Distinguish replay defects from scientific regressions. Do not edit
evidence files or continue the research.
