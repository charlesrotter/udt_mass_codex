# Bounded repair re-review

Preserve the initial verdict and all failure evidence. Bind to repaired source
snapshots matching REPAIR_FREEZE.json. Same CPU-only 180 second / 2 GiB limit;
no GPU, installs or broader scientific re-proof.

Inject interruptions into the actual save path (during pending marker creation,
immediately before hard-link publication, and just after publication). Require
the prior valid checkpoint for both pre-publication interruptions, and complete
new checkpoint after publication. Require marker overwrite refusal and
corrupt-committed failure rather than silent fallback. Check diagnostics are
ineligible and cannot displace accepted checkpoints.

Replay R2 with CPU-mocked CUDA entry points: finite endpoint with large original
constraint must reject before success; finite state producing nonfinite derived
constraint must reject; valid endpoint must still complete. Ensure diagnostic
state is saved separately without producing a new committed checkpoint.

Version attribution: initial reviewer source 9acbf56c... differs from the first
actual GPU-run source a09bdcea... solely by the latter's extra spec-output-budget
precheck. It does not change either demonstrated failing path. Inspect and record
this diff without rewriting either preserved initial source or prior report.
