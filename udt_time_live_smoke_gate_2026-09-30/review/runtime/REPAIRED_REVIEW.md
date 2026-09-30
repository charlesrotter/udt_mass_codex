# Repaired runtime review — VERIFIED-WITH-CAVEATS

The two demonstrated runtime defects are closed for the repaired source bytes
below. This verdict is a narrow checkpoint/runner engineering review, subject to
the parent-owned real-device smoke evidence and final integration bindings. It
does not certify an unbuilt broader solver or strengthen a scientific claim.

Reviewer: `/root/smk_runtime`, an actual separate conversation context, inherited
model; no claim of a different model. Initial source exposure, parent startup
attribution and independent local HEAD/status observation remain recorded in
INITIAL_SOURCE_BINDING.json and INITIAL_REVIEW.md. The initial refutation and its
fixtures have been preserved unchanged. No GPU, protected payload, package source
mutation, installation or scientific re-proof was performed by this reviewer.

Reviewed source versions:

- `checkpoint_io.py`: `d689de8dd525df67289862b701226dc857ec50de4a34477c32db7fdc8c2008e4`
- `smoke_runner.py`: `724bf5405dd9596bff343a0a6967393d26a0a0c7529124e9a0bfdd70e569d52f`
- Frozen unchanged RHS: `f67b50e94ae0ffcc6a5f0bc6eaa2cf16f2763fd7a77026e71e6c1159e7e40367`

Both operational files match REPAIR_FREEZE.json. Their exact bytes are preserved
under repaired_source/. The initial reviewer runner hash `9acbf56c...` predates
the first GPU harness runner `a09bdcea...`; inspected diff shows only the latter's
extra precheck rejecting a spec larger than the output budget. That single line
does not change either demonstrated defect. The actual first-run version remains
preserved separately by the parent under initial_implementation/.

The repaired marker protocol writes and fsyncs `COMMITTED.pending`, then publishes
the complete bytes with an atomic no-overwrite hard link. A pending marker is
ineligible for loading. CPU faults injected into the actual save path confirm
recovery of step 0 after interruption during pending creation or just before
publication, and recovery of complete step 1 immediately after publication. A
direct publication attempt over an existing marker raises FileExistsError and
preserves the original bytes. A committed payload corruption still raises
PAYLOAD_HASH_MISMATCH rather than being silently skipped.

The runner now validates the initial/resumed boundary and each state before
committing it. It rejects both large and nonfinite constraint residuals; failed
states are retained under diagnostics with `eligible_for_resume: false` and a
DIAGNOSTIC marker. An independently written CPU-mocked runner test reproduced
the former bad endpoint and observed CONSTRAINT_LIMIT without completion. A
finite p=1000 fixture producing a nonfinite derived residual is also rejected.
A valid endpoint still returns completion. Neither failure adds a new committed
checkpoint. Separate checkpoint tests confirm nonfinite diagnostic preservation
and exclusion from checkpoint selection.

Nine bounded repair checks passed in 0.9284011169802397 seconds, peak RSS
377476 KiB. They use production save/load and runner control flow under deliberate
fault injection; the endpoint calls explicitly map CUDA entry points to CPU.
They are engineering regression and adversarial catch evidence, not a different
implementation of the evolution equations or CUDA numerical validation.

Exact command, stdout, stderr, versions and machine-readable outcomes are saved:

```sh
timeout 180s python3 udt_time_live_smoke_gate_2026-09-30/review/runtime/repair_diagnostic.py > udt_time_live_smoke_gate_2026-09-30/review/runtime/repair_diagnostic.stdout 2> udt_time_live_smoke_gate_2026-09-30/review/runtime/repair_diagnostic.stderr
```

Not independently repeated here: real GPU evolution, real SIGTERM/SIGKILL,
end-to-end harness timeout enforcement, GPU memory measurement, uninterrupted
versus resumed CUDA arithmetic, original-metric/refinement/physical constraints
beyond the wrapper's inherited check, power loss, multi-host filesystems, and
noncooperative external GPU users. Parent owns the real-device tests; this review
does not substitute CPU mocks for them. The per-device lock is cooperative.
The reviewed marker protocol assumes the local filesystem's hard-link atomicity;
the smoke requirement is process interruption, not a power-loss certification.

No unresolved objection remains in the assigned small runtime implementation
scope. Final integrated readiness still requires the successful repaired harness
and source/output/operational-document bindings. Saving this review neither
selects native UDT dynamics nor authorizes a multi-hour broader solver campaign.
