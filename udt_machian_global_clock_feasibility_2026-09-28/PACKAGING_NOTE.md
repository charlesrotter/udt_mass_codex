# Final Git packaging diagnostic

The initial exact-stage check failed while git show tried to map a packed object
under the existing512MiB address-space cap. The failing read was an empty review
stderr blob. This is a packaging execution failure, not a scientific test failure.
Exact command, error and receipt are retained in checks/exact_stage_initial.*.

The retry keeps the same512MiB/60s resource bounds and adds per-command
core.packedGitWindowSize=8m and core.packedGitLimit=32m, alongside the existing
Git thread controls. No repository configuration or scientific source changes.
checks/exact_stage_retry.* records PASS: all81 then-staged files match disk,
all74 manifest payloads and final fidelity pins match, and52 prior untracked
names remain. The corresponding original manifest is saved as
checks/initial_stage_manifest.tsv.

Those receipts and this diagnostic were subsequently added to the package and
the current manifest regenerated. The final enlarged staged set is checked again
before committing; that non-self-containing execution receipt is retained under
/tmp/mgc1_exact_stage_final_2026-09-28.*. The final Git commit identifies the saved
artifact set. No scientific repair, new review verdict or source regrading.
