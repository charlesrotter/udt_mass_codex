# TPS1 operation and evidence locations

This finite survey has no automatic wall or CPU-time limit, following Charles's
explicit instruction. It ends after the declared234cases or a non-time diagnostic/
resource stop. Original equations, tolerances,8GiB allocated GPU ceiling,64GiB
production artifact budget, one GPU worker and saved evidence controls remain.
WORK_ORDER.md owns scope; the previous TPP1 six-hour dispatch is historical for
this execution. Absence of a timeout does not expand the parameter grid.

Run from the repository root. `python3
udt_time_live_production_survey_2026-10-01/status.py` reads durable counts,
unfinished attempts and actual controller PID/start identity. Process liveness
must be checked in the host process namespace. The status script does not certify
scientific results. A completed solver queue still requires scientific analysis
and review. Current operational state belongs to LIVE.md and actual receipts.

Production data are retained under this package's ignored directories:
initial/production, specs/production, runs/production, production_runtime and
production_analysis. They are local raw evidence, not disposable scratch and
not automatically available in a remote clone. Compact indexes, code, reviews
and reviewed results are banked separately. Never overwrite checkpoints or
delete failed cases to obtain a passing survey.

`production_runtime/campaign.json` binds the finite queue, initial data and code.
Each attempt has launch, stdout, stderr and completion receipt. Controller logs
are first_gate.* and continuation.* (or a later resume_N.* prefix); the launch
record gives PID and Linux process-start ticks. Reused PID alone is not identity.

The first gate uses `launch_queue.py first_gate --stop-after 3`. Its expected75
return is a case-boundary pause. FIRST_GATE.json must bind passing independent
original-equation, refinement, clock and operational evidence before
`launch_queue.py continuation` can run the rest. This is an authorized staged
continuation, not a new permission request.

To stop manually, verify the live controller PID/start identity and send SIGTERM
to that capture PID. The signal forwards to the supervisor and worker, which
checks and saves a checkpoint. There is no automatic timed escalation. Inspect
the real receipt/checkpoint before any further action. For a normal signal pause
after FIRST_GATE passed, `launch_queue.py resume_1` (then a new unused index for
later resumptions) preserves the queue and elapsed telemetry. Diagnostics such
as timestep floor, equation failure or unknown/incomplete attempts require review;
the launcher never repairs or discards them automatically.

If manually interrupted before the first gate completes, use the same capture
and supervisor commands with an unused capture prefix and a case-count stop for
the remaining first cases; do not bypass FIRST_GATE. Inspect all prior successful
case IDs to choose the remaining count. No timeout utility or CPU-time limiter
belongs around these commands.

Extract only while the queue is paused or complete:
`assemble_campaign.py production_runtime/campaign.json production_runtime
--limit 3` for the first gate, with package-qualified paths from the repo root.
Omit the limit to extract every completed case. Extraction is serial so output
reservations have no concurrent writer. Independent math checks are under
review/math; producer clock_batch.py reuses the fixed TPP1 method, with source
and query freeze in CLOCK_DISPATCH.json. Independent Hamilton queries are frozen
under review/runtime. Do not interpolate rays through unsaved temporal gaps.

No timer is a numerical criterion. Conversely, no finite successful run, passed
guard, checksum, resource measurement or review selects UDT's native response law.
Keep conditional Ric=0 and the supplied periodic/CMC/harmonic setting explicit.

The reviewed CPU companion `postprocess.py` is dispatched by
POSTPROCESS_DISPATCH.json. Its fixed capture launch is in
launch_evidence/postprocess.launch.json; live logs/receipt are
production_runtime/postprocess.stdout, postprocess.stderr and postprocess.json.
Verify that capture's PID/start identity in the host namespace. It waits without
a deadline for the specified continuation controller, then requires successful
completion of all234 cases before serial assembly, mathematical checks, clocks
and frozen subset comparisons. It uses no GPU. Final candidate status is in
production_analysis/postprocess/POSTPROCESS_RESULT.json.

A diagnostic/manual/missing-receipt stop ends the companion. Inspect its receipt
and unfinished files before a new dispatch; its fixed output directory cannot
be reused by overwriting results. A newly resumed GPU controller requires a
reviewed companion dispatch for that actual controller after preserving prior
outputs. Stop the companion by verifying and signalling its own capture PID;
that does not itself stop a still-running GPU queue. To stop the entire workflow,
verify and signal both captures. No automatic timed escalation is used.

Future math reports/captures under review/math/cases and review/math/captures
are ignored and included in companion storage accounting. Only the fixed
first-three reviewed reports are explicitly banked at this checkpoint. Later
reports, automatic PASS flags and inherited reviewer-context fields do not
constitute actual new adversarial review. The next session should review the
finite atlas or unresolved diagnostic before integrating any scientific result.
