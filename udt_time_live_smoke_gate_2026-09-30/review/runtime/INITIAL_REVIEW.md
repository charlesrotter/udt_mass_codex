# Initial runtime review — REFUTED

Reviewer: `/root/smk_runtime`, actual separate conversation context, inherited
model (no claim of a different model), CPU-only. Parent startup and premise-audit
evidence are attributed in INITIAL_SOURCE_BINDING.json, not independently
replayed. Independently observed branch `grok`, HEAD
`622d1700d91705320ee17e79ed5fd92bc174d752`, and unrelated untracked dirt. No
protected payload was opened. Read on-disk AGENTS.md, CLAUDE.md scoped sections,
verifier-before-record and solver-first protocols, this work order, the small
checkpoint and runner implementations, and the frozen RHS only for its runtime
interface. No historical scientific re-proof was attempted.

Exposure: source and work-order requirements were visible before test design.
Initial source snapshots and hashes are preserved. The independently written
diagnostic invokes the implementation under review; it is adversarial engineering
regression and fault reproduction, not an independent evolution implementation.

## Defect R1: marker publication can strand a valid earlier checkpoint

`initial_source/checkpoint_io.py:39` publishes COMMITTED through `exclusive`,
which creates the destination before writing it (`:14`). SIGKILL between those
operations leaves an empty marker. `load_latest` treats every marker file as
committed (`:44–50`) and refuses to recover the prior valid record. The CPU fixture
`initial_fixtures/marker_create_before_write` reproduces the resulting
METADATA_HASH_MISMATCH with the prior valid checkpoint still present.

Smallest repair: create, fully write and fsync a temporary marker, then publish
COMMITTED atomically without overwrite, preserving corrupt-committed rejection.
Do not silently skip corrupt genuinely committed checkpoints. Recheck actual
save-path interruption before marker publication and post-publication recovery.

## Defect R2: constraint-failed endpoint can be resumed to success

`initial_source/smoke_runner.py:68` commits the state before its constraint limit
is enforced (`:73`). A failed endpoint is therefore selectable on restart.
After load, `:57` skips the loop for t=end and `:77–79` returns completion without
checking that endpoint. The CPU control-flow reproduction saved a finite
float64 endpoint whose independently computed spectral constraint maximum is
`1.0000000000000022`; the runner returned 0 and SMOKE_CONTROL_COMPLETE.

CUDA entry points were explicitly mocked to CPU for this narrow reproduction.
No GPU was used and no CUDA numerical accuracy is asserted. Smallest repair:
check finite constraint and budget at initial/resumed state before any completion;
ensure a failing checkpoint remains diagnostic-only and cannot silently restart
as an accepted state. A persistent failure marker is another possible guard if
it is reliably written and checked. Reject nonfinite residuals explicitly.

## Surviving evidence and scope

Save/load state identity, later uncommitted payload recovery, payload/metadata
hash rejection, changed signature rejection, nonfinite state rejection, tiny
output rejection, existing-run refusal and cooperative-lock refusal all behaved
as expected in these finite CPU tests. The diagnostic took 0.676 seconds with
371396 KiB peak RSS. Exact command:

```sh
timeout 180s python3 udt_time_live_smoke_gate_2026-09-30/review/runtime/initial_diagnostic.py > udt_time_live_smoke_gate_2026-09-30/review/runtime/initial_diagnostic.stdout 2> udt_time_live_smoke_gate_2026-09-30/review/runtime/initial_diagnostic.stderr
```

The initial operational gate is blocked by R1 and R2. Parent owns real GPU,
SIGTERM/SIGKILL, uninterrupted/resumed comparison and resource-harness tests;
those were not replayed here. Successful repair/review can establish readiness
only for the tested conditional control runner. No new physics, scientific
grade, native dynamics selection or broader-solver certification is claimed.
