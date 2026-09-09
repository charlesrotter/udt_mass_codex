# Proportional review of preservation and G351 replay utility

2026-09-09, same reviewer/context as INITIAL_DIRECT_REVIEW.md. No additional
required defect. This reviews packaging/reproducibility, not G351 science.

Read all 117 lines of check_reconciliation.py, SHA256
7a916a593ddab9b18c85a7437d614c85311c609d54bcba60ac110ad28e05c2ed,
and the complete current main() G351 scratch replay block made load-bearing.
This reporting version includes the exact nested subprocess command,
stdout/stderr and package before/after file-hash dictionaries. Its earlier
version lacked that reporting; no substantive claim of a separate original
script snapshot is made here. Parent preserves execution history.

The utility independently compares the five-cell transition to the Git
baseline, checks schema/order, old current-status scientific stamps and all
11 current-row/historical-source validators, then runs the current startup
guard. Its extracted G351 AST is explicitly the actual current With block;
it still checks successful subprocess exit, the 47-check token and identical
before/after package hashes. The full main is not rewritten or treated as
passing. Later surrounding G351 external-review/current-row checks are not
executed by this selected block and are not silently certified by it.

The prior audit's 83-pin inventory is checked at the explicit baseline;
files outside the exact allowed current-file set are additionally checked
live. Five fixed controls/science documents compare to baseline, and the
tracked-write scope check allows only nine root paths and this package.
The unrelated-work check is expressly a 46-status-name check, not a content
audit of protected/untracked payloads. No checksum is a truth claim.

Read actual parent evidence:

- INITIAL_FULL_PREMISE_AUDIT.json, SHA256
  5523623b51146dc1aa9e5e7aef64f94b6877f23a80cef89a336d36b4d155b47e:
  exit 1, G325 replay_exact:DERIVATION_RESULT.json, 11.266 seconds, 2 GiB
  address-space/900-second limits. Early authority and 11 banking validators
  occur before that point in the inspected main; later main gates unreached.
- preservation_with_replay_output.json, SHA256
  fd45dbde1eee6d8263ab2c0037ef0dba088992ccd72a4505a64fc2b4bc316dd8:
  exit 0, 1.395 seconds, 84,820 KiB; 189 bounded checks. Exact command applies
  Git pack memory limits as process environment, without changing disk config.
- preservation_with_replay_output.stdout, SHA256
  1fa7bb1f05ba4f657cab100785e8d28e42ab0b3268a5c74fa2ccb435f808da12:
  nested G351 exit 0, 47/47, empty stderr and equal before/after evidence.

These are read/reused parent receipts at this stage, not executions by the
reviewer. No source theorem, complete dependency graph, observation, physical
premise, full365 pass or scientific integration follows. R1/R2 in the initial
direct review remain the sole grouped implementation repair requirements.
