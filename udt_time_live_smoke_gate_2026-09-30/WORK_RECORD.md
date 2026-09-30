# SMK1 — fixed engineering return

The repaired control passed 18 actual child-process checks in a 13.506-second
captured harness run. No multi-hour simulation was launched. This establishes
tested checkpoint/stop behavior for the existing conditional NGD1 control;
the broader spatial/time-live solver still needs its own implementation,
validation, smoke checks and representative load test.

## What changed and why

Charles requires smoke checks before hours-long production. NGD1's scientific
pilot saved history at completion and had no restart entry point. SMK1 adds an
immutable checkpoint wrapper around its unchanged, hash-pinned evolution RHS.
It does not change equations, inputs or scientific grades. WORK_ORDER.md records
the bounded engineering question, resources, exclusions and next production gate.
AGENTS.md now preserves the smoke requirement; LIVE/HANDOFF route this return.

The initial 11.160-second smoke harness passed its original tests, but two actual
separate-context reviews found missing failure cases. The initial sources,
SMOKE_FREEZE.json, SMOKE_RESULT.json, raw runs and review history are retained:
the original PASS is not the final readiness verdict.

1. A constraint-failed state was committed before rejection; restarting at the
   endpoint skipped constraint validation and reported completion. The repair
   checks finite original momentum residuals at initial/resumed boundaries and
   before each checkpoint. Failed states go to diagnostics, ineligible for restart.
2. Creating COMMITTED before writing its bytes exposed a partial marker to an
   interrupted run. The repair writes/fsyncs a temporary marker and publishes it
   with an atomic no-overwrite hard link. A pre-publication failure leaves the
   earlier committed checkpoint usable. Corrupt committed evidence still fails
   closed; it is not silently skipped.

The repair also puts interrupt polling and child completion under one 60-second
deadline and saves explicitly marked per-case clock values, not just a small
error statistic. REPAIR_FREEZE.json pins these changes before the repaired run.
The runtime review's first source snapshot preceded the initial harness freeze
by the tiny-output precheck; both source editions remain available for comparison.

## Checked behavior and limits

Actual SIGTERM and SIGKILL were sent only to owned workers after a committed
checkpoint. Fresh-process restart, graceful-stop restart and killed-worker
restart each reproduced uninterrupted final fields bit for bit. Fault injection
into the real marker-publication path preserved the previous checkpoint. New
deliberately invalid copies exercised corrupt payload, changed specification,
nonfinite data, excessive finite endpoint residual, nonfinite derived residual,
invalid timestep, overwrite refusal, cooperative worker lock, tiny memory/output
budgets and the wall stop. Failures and diagnostic fields are retained.

The repaired run used one Tesla V100-PCIE-32GB worker at a time, torch 2.5.1+cu121,
float64, N32, the three supplied controls and t=1..4. The uninterrupted run's peak
Torch allocated memory was 42,496 bytes; this is not total CUDA/device memory and
cannot size a future production run. All runs were brief engineering controls.

Saved-field agreement with the previously independently checked NGD1 control:
maximum absolute error 6.538e-13, below the frozen 2e-7 tolerance. Maximum sampled
momentum residual 6.074e-11, below 2e-6. Marked log-clock-ratio error 4.835e-14;
the actual sampled values and query appear in execution_repaired/CLOCK_READOUT.json.
These are conditional supplied-clock readouts, not native UDT predictions.

execution_repaired/SMOKE_RESULT.json contains exact values, commands, return codes
and output hashes; checks/smoke_repaired.* holds the captured outer command,
versions/provenance, stdout/stderr and resource receipt. Actual reviewer reports
and FINAL_ATTESTATION.json files under review/runtime and review/scope distinguish
CPU fault reproduction, independent readout recomputation, parent GPU checks and
version/routing review. The final integration record binds their actual verdicts.
Fresh contexts share the inherited model; different-model review is not claimed.

No all-interruption, hardware-power-loss, generic solver or full solution-space
guarantee follows from these finite checks. The cooperative GPU lock applies to
workers using this runner; external GPU users still require a device preflight.
No long-duration drift, 3D convergence, production throughput or production-memory
claim is made. Earlier NGD1 mathematics/refinement/independent Ricci work is
inherited at its unchanged scope and was not re-proved here.

## Dependency and trajectory review

UDT_DEVELOPMENT.md, its generated program, source pins, central graph, exact 406
registry, CANON and original NGD1 evidence remain byte-unchanged. Neither the
positive conditional results nor the negative scope limits acquire a new premise
or stronger conclusion. This engineering record is fixed evidence, not another
maintained scientific summary. The previous 643-path review record is preserved;
the new binding reviews only the operational/source/evidence delta and explicitly
retains earlier scientific reviews without pretending to repeat them.

The larger goal remains broader time-live exploration over hours/days. Next comes
a specified broader solver and its own small validation/smoke gate, then a short
representative load measurement and a written production dispatch for the first
proposed six-hour tranche, with checkpointed extensions toward 24–48h. Repeating
this tiny symmetry-slice control for longer would not fulfill that goal. A native
selection claim still needs a native discriminant or an explicit unadopted
connection; merely sampling more conditional Ric=0 solutions cannot supply it.
