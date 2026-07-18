# Phase R1A audit index

R1A begins the research-lane-first reorganization with one conservative
archive batch and stops before R1B. It does not relocate active research,
Python modules, opaque data, manifests, or frozen evidence.

## **Read the correction layer first**

> The original R1A tables remain immutable historical evidence. The corrected
> census is **815 occurrences / 92 sources / 16 frozen-source occurrences**;
> it supersedes the original 801/87/12 counts without overwriting them.

- [`correction_2026-07-18/CORRECTION_PREREGISTRATION.md`](correction_2026-07-18/CORRECTION_PREREGISTRATION.md):
  correction scope frozen before pointer mutation.
- [`correction_2026-07-18/OMISSION_LEDGER.tsv`](correction_2026-07-18/OMISSION_LEDGER.tsv):
  all 14 recovered occurrences and their 5 rewrite / 1 intentional co-located
  / 8 retained-target dispositions.
- [`correction_2026-07-18/CORRECTED_INBOUND_REFERENCES.tsv`](correction_2026-07-18/CORRECTED_INBOUND_REFERENCES.tsv)
  and [`correction_2026-07-18/LITERAL_GIT_GREP_COMPARISON.tsv`](correction_2026-07-18/LITERAL_GIT_GREP_COMPARISON.tsv):
  corrected census and exact independent comparison at `4c98e32`.
- [`correction_2026-07-18/CORRECTED_CONSOLIDATED_ADJUDICATION.tsv`](correction_2026-07-18/CORRECTED_CONSOLIDATED_ADJUDICATION.tsv)
  and [`correction_2026-07-18/CORRECTED_CONSOLIDATED_POINTER_PLAN.tsv`](correction_2026-07-18/CORRECTED_CONSOLIDATED_POINTER_PLAN.tsv):
  additive corrected rulings; all 17 moved files remain eligible.
- [`correction_2026-07-18/FINAL_VERIFY_RESULT.json`](correction_2026-07-18/FINAL_VERIFY_RESULT.json):
  five exact pointer corrections, moved/frozen hash gates, zero stale
  non-frozen pointers, dirty-workstation firewall, catch-proofs, and test
  baseline.

R1B has not started and is not authorized by this correction.

## Historical first-run evidence

- [`R1A_AUDIT_REPORT.md`](R1A_AUDIT_REPORT.md): final outcome and gates.
- [`PREMOVE_ADJUDICATION_REPORT.md`](PREMOVE_ADJUDICATION_REPORT.md): individual
  rulings for all 26 archive candidates and all 37 unknown/blocked files.
- [`INBOUND_REFERENCES.tsv`](INBOUND_REFERENCES.tsv): every pre-move exact
  inbound occurrence, including frozen-source status.
- [`MOVE_MAP.tsv`](MOVE_MAP.tsv): the 17 old-to-new paths with before/after
  hashes and pointer sources.
- [`PROPOSED_DIRECTORY_TREE.md`](PROPOSED_DIRECTORY_TREE.md): the superseding
  research-lane-first tree proposal.

## Verification and census

- [`PREMOVE_VERIFY_RESULT.json`](PREMOVE_VERIFY_RESULT.json): independent
  63-file/801-reference adjudication verification.
- [`MIGRATION_VERIFY_RESULT.json`](MIGRATION_VERIFY_RESULT.json): move, pointer,
  frozen-package, dirty-firewall, and test verification.
- [`POSTMOVE_POINTER_CENSUS.tsv`](POSTMOVE_POINTER_CENSUS.tsv): exhaustive old
  and new move-token audit; no stale non-frozen pointer remains.
- [`postmove_census/DEPENDENCY_MAP.tsv`](postmove_census/DEPENDENCY_MAP.tsv):
  rebuilt full static dependency census at the migration commit.
- [`postmove_census/DEPENDENCY_SUMMARY.md`](postmove_census/DEPENDENCY_SUMMARY.md):
  post-move category and unresolved-edge summary.
- [`postmove_census/VERIFY_RESULT.json`](postmove_census/VERIFY_RESULT.json):
  independent post-move census and final additions-only verification.
- [`TEST_BASELINE.txt`](TEST_BASELINE.txt) and
  [`TEST_BASELINE.json`](TEST_BASELINE.json): complete post-move test run.

The preregistered eligibility and stop contract is in
[`R1A_PREREGISTRATION.md`](R1A_PREREGISTRATION.md). R0 remains an immutable
historical snapshot under [`../reorganization_r0/`](../reorganization_r0/).
