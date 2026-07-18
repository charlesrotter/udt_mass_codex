# Phase R1A audit index

R1A begins the research-lane-first reorganization with one conservative
archive batch and stops before R1B. It does not relocate active research,
Python modules, opaque data, manifests, or frozen evidence.

## Read first

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
