# SMK1 — mandatory smoke gate before the extended time-live campaign

Charles: “Ok, before embarking on any multiple hour runs, do smoke checks firsts
to check everthing's working properly.” This adds a required gate to the broader
hours-to-days exploration direction. Smoke testing is an entry stage, not the
completion or replacement of that exploration.

## Immediate engineering question

Can a bounded evolution run save trustworthy immutable checkpoints, survive an
interruption, resume with the same result, reject incompatible/corrupt inputs,
respect resource/stop controls, and produce readable checked outputs? The prior
NGD1 pilot has independently checked mathematics/numerics but its producer saves
the history only at the end and has no restart entry point. It is not ready for
multi-hour use solely because its short scientific checks passed.

Use the unchanged, hash-pinned NGD1 conditional two-Killing Ric=0 RHS as a control
for operational testing. Its scientific assumptions remain conditional and its
one-spatial-coordinate coverage is unchanged. No new physical premise, geometry
selection, source, carrier, scale, X_max boundary or full3D result is introduced.
Published equations, grids and reviews remain fixed. Ordinary numerical methods
and checkpoint engineering are permitted; no numerical result is promoted here.

Workspace: udt_time_live_smoke_gate_2026-09-30/. Existing protected/unrelated
payloads are untouched. Source/versions in LAUNCH.json. One GPU worker, float64,
N32 and the three existing pilot controls on t=1..4. Reuse audited RHS and known
answers; initial data and marking are supplied comparison inputs, not UDT choices.

Immediate budget: GPU child processes sequential, total at most5 minutes,
each child at most60s; whole smoke harness180s. GPU allocated memory at most2GiB,
checkpoint/output at most64MiB per fixture and256MiB total. CPU checks/review
each180s/2GiB working data. CUDA virtual mappings retain the existing documented
128GiB capture allowance; this does not allocate that much physical memory.
Measured V10032GB initially idle. No installs, purchases or hour-long runs in
this engineering step. Stop on an unexplained mismatch, resource limit, corrupted
valid evidence or unresolved review objection; preserve all diagnostics.

## Required short checks, before outcomes

1. Runtime/device/dtype/version and current-code checks; exact saved NGD1 control
   agreement within2e-7 absolute field error. Read outputs and actual clock
   ratios from saved checkpoints, not only an exit code.
2. Fresh-process checkpoint/resume versus uninterrupted run: bitwise equality
   where the exact arithmetic schedule is identical; record any weaker guarantee
   rather than silently loosening it. Trigger a real SIGTERM stop and resume.
3. Abruptly kill only the owned worker after a committed checkpoint, then recover;
   partially written/uncommitted later checkpoints must not erase committed ones.
4. Catch proofs: reject corrupt committed payload, changed run specification,
   nonfinite state, invalid timestep, attempts to overwrite an existing run,
   concurrent worker lock, and deliberately tiny memory/output limits.
5. Relevant constraints and refinement/independent original-metric evidence are
   inherited only at unchanged NGD1 scope; the new wrapper must preserve them.
   Review actual code and failures in separate contexts, then bind the operational
   changes without regrading any scientific source.

## Gate for the later, larger campaign

Every new solver, spatial-dimension release or materially changed workload must
pass its own small end-to-end smoke run. NGD1/SMK1 passes do not certify an unbuilt
broader solver. Its gate includes lawful constraint initialization, original
equation residuals, known limits/independent anchors, basic grid/time refinement,
actual clock queries, one-device enforcement, measured memory/output/throughput,
checkpoint/restart and stop/timeout tests. Freeze tested code/specification and
record expected outputs/tolerances before the test. Exceptions remain explicit
unpassed gates, not silent waivers.

After that gate, use a short representative workload to size the first proposed
six-hour tranche and checkpointed extensions toward24–48h. The full written
production dispatch must specify actual equations, released/frozen freedoms,
case coverage, grid/dtype/device, output/timeout/resource limits, checkpoint cadence,
stop rules and return/review budget. No desired curve is an acceptance criterion.
More time in the original symmetry slice is not completion of the broader goal.
General3D evolution requires its own validated implementation and same scientific
labeling. A finite campaign maps tested families, never all possible spacetimes.

Maximum immediate conclusion: engineering smoke readiness for the tested control
runner, with explicit outstanding broader-solver gates. Saving, checks and review
do not select native UDT dynamics. Operational records route this requirement;
UDT_DEVELOPMENT.md remains the sole maintained scientific argument.
