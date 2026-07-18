# Phase R0 audit index

Phase R0 inventories the fixed `bfa0b9a` base snapshot and proposes navigation
only. No proposed relocation has been executed.

## Primary audit records

- [`R0_AUDIT_REPORT.md`](R0_AUDIT_REPORT.md): scope, counts, gates, baseline, and
  audit conclusions.
- [`ROOT_FILE_INVENTORY.tsv`](ROOT_FILE_INVENTORY.tsv): every one of the 1,131
  tracked root files with Git blob ID, SHA-256, size, last commit, references,
  classification, and basis.
- [`DEPENDENCY_MAP.tsv`](DEPENDENCY_MAP.tsv): static Python-import, file-path,
  Markdown-link, manifest, test, startup, and exact root-reference edges.
- [`DEPENDENCY_SUMMARY.md`](DEPENDENCY_SUMMARY.md): aggregate dependency counts
  and the unresolved/dynamic audit queue.
- [`ROOT_RETENTION.tsv`](ROOT_RETENTION.tsv): permanent and conditional root
  retention requirements with release gates.
- [`DIRTY_WORKSTATION_INVENTORY.tsv`](DIRTY_WORKSTATION_INVENTORY.tsv): Git status
  and `lstat` metadata only; file content was not opened or hashed.
- [`PROPOSED_DIRECTORY_TREE.md`](PROPOSED_DIRECTORY_TREE.md): later-phase layout
  proposal and migration constraints.
- [`TEST_BASELINE.txt`](TEST_BASELINE.txt) and
  [`TEST_BASELINE.json`](TEST_BASELINE.json): recorded existing test baseline.
- [`SCAN_SUMMARY.json`](SCAN_SUMMARY.json) and
  [`R0_VERIFY_RESULT.json`](R0_VERIFY_RESULT.json): machine-readable scan and
  independent verification results.

## Reproducers

- `build_r0_inventory.py`: bounded base-snapshot census and dependency scan.
- `build_navigation_outputs.py`: retention and dependency-summary builder.
- `run_test_baseline.py`: exact test-baseline recorder.
- `verify_r0_inventory.py`: fail-closed independent recomputation and
  catch-proof verifier.

The preregistered scope and acceptance gates are in
[`../REORGANIZATION_R0_PREREG_2026-07-18.md`](../REORGANIZATION_R0_PREREG_2026-07-18.md).
