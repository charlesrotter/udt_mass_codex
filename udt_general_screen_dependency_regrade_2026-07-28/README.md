# General-screen dependency regrade

Preregistered audit of which earlier selection, uniqueness, no-go, closure, Hopf/carrier,
bootstrap, action, macro, and particle claims actually depend on the newly released full angular
screen. Historical packages remain unchanged; this directory is an append-only overlay.

Read in order:

1. `AUDIT_REPORT.md`
2. `CORRECTION_LAYER.md`
3. `STATUS_LEDGER.tsv`
4. `FAMILY_IMPACT_SUMMARY.tsv`
5. `CURRENT_LOAD_BEARING_CLAIM_REGRADING.tsv`
6. `PRIMARY_CLAIM_AUTHORITY_ROUTING.tsv` and `FAMILY_AUTHORITY_ROUTING.tsv`
7. `RERUN_PRIORITY.tsv`
8. `LAY_REPORT.md`
9. `NEXT_STEP.md`
10. `VERIFICATION_RESULT.json`, `ADVERSARIAL_REVIEW_INITIAL_FAIL.md`, and
    `ADVERSARIAL_REVIEW.md`

The fixed-base discovery universe is in the `DISCOVERED_*` records. `build_regrade.py` reconstructs
the current-owner and disposition ledgers from Git objects at `e098338`; `verify_regrade.py` is a
separate fail-closed replay with exercised mutations.
