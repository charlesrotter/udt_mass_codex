# Supplemental author regression replay scope

Added after independent_01 passed and current author code was read. The independent
scientific checker is unchanged. Replaying the exact author's implementation is
regression only. Reproduce causal catches and kernel catches, and the horizon
initial simplification failure and repaired pass. Test counts are not proof.

Causal code writes only stdout and is run at its original path with the existing
512-MiB/60-second capture utility, using a review/ output stem. It imports the
inspected SHA-pinned historical diagonal tensor utility, unlike the reviewer
implementation. Kernel/horizon code write beside __file__ and explicitly set a
2-GiB hard cap. They therefore run from byte-identical copies under review/replays/
with the kernel contract copied alongside, one child at a time, 2-GiB memory,
60 CPU/wall seconds and no GPU. A short recorded subprocess invocation captures
their separate stdout/stderr and exits; the existing capture utility's 512-MiB
hard limit cannot accommodate those scripts' explicit hard-limit assignment.
No scientific source, expected result or check is modified for these replays.

The independent saved-observation arithmetic imports no author code, uses only
the existing RESULT.json and compares its output against the saved parent table.
It repeats no raw observation processing, likelihood, fit or survey assumption.
