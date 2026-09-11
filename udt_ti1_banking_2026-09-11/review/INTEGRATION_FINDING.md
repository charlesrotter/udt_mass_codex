# B1 — historical adapter excluded unauthenticated G413

Found in the initial integration draft. This is a real correspondence/guard
defect, not a mathematical defect in TI1 or a failure of the current396 guard.
The parent accepted the objection and will repair after the already-running
initial full396 audit completes, preserving that run and its input version.

The plan required every historical projection to exclude only an authenticated
exact G413. The new without_ti1 helper does this and is used by the backlog
guard. Eleven older guards instead add G413 to a prefix-removal list. Their
shared GR-filter snapshot authenticates G310/G312 but not G413. Consequently
they can silently remove an altered G413 while their historical hashes pass.
The direct historical replay/main prefix paths have the same unvalidated-read
pattern and need the same boundary treatment.

Actual read-only counterexample: check_projection_boundary.py substitutes
PHYSICAL_LAW_ADOPTED for NOT_PHYSICAL_ADOPTION in only the G413 line, presenting
the same changed bytes through read_bytes and read_text. No source is written.
Eleven standalone historical validators pass; only reviewed-backlog rejects
the changed exact TI1 row. Capture projection_boundary_initial exits1 with the
specific objection,0.100160099s,13:18:38.706560UTC,2GiB/60s, no timeout. The full
per-guard result and tested verifier/module hashes are in its saved stdout.

In contrast, the existing focused suite at those same initial sources reports
525 passed,1 deselected, exit0 in11.582357s. Its passing count did not cover this
case. The initial verifier/legacy-test diff, new guard and new tests are saved
as INITIAL_INTEGRATION_DIFF.patch, INITIAL_TI1_GUARD.py, INITIAL_TI1_TESTS.py and
INITIAL_INTEGRATION_PINS.json. The original baseline plus the diff reconstructs
the faulty tracked implementation; hashes alone are not relied on for recovery.

Strongest survivor: G413's complete conditional scientific transcription,
original395/source preservation and the current396 validator remain sound at
this inspected scope. No row or original scientific-source repair is requested.
The integration verdict remains pending the adapter repair and its checks.

Smallest source-preserving repair: authenticate any present G413 on the SAME
raw snapshot before historical removal. In the shared GR-filter snapshot,
retain raw after authentication so G312-only projection and its one-read
contract remain unchanged. Direct replay/main raw reads likewise authenticate
before removing G413; avoid accidentally double-removing it where the old
replay loop requires exactly one match. Retain the historical missing-G413
allowance only in isolated old-snapshot helpers; current396 still requires
exactly one. Add the concrete adverse case to durable hostile tests and rerun
the original failing probe, focused guards and the actual final full396 audit.

Reviewer pytest scratch copies are kept under ignored pytest_initial/ and later
pytest_repaired/, excluded from evidentiary manifests/staging. The checks used
the existing startup compatibility fixture machinery, including its local
historical snapshot copies; no archive research or external ScratchDisk access
was undertaken. The original46 status names and protected payload boundary are
separate from these synthetic fixtures.
