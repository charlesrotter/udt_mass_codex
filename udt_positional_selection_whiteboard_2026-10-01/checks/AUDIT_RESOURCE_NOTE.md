# Post-review audit resource repair

The first full406 run, checks/final_premises.*, stopped after8.301s with exit1.
It did not reach a scientific verdict. The checker failed while asking Git for
historical AGENTS.md versions. A direct reproduction under the same2GiB address
cap exposed Git's error: a pack file could not be mapped (Cannot allocate memory).
audit_history_diagnostic.json preserves the exact error and278 partial rows.

The bounded control changes only Git's process-local read-window settings:
core.packedGitWindowSize=32m and core.packedGitLimit=128m. The same complete
history request then returned0 with307 rows and empty stderr, under the same
2GiB cap; audit_history_window_control.json records it. No Git source, object,
history, repository configuration, checker, scientific input or test is changed.

The final_premises_windowed.* retry records the exact command through `env`
GIT_CONFIG_COUNT/KEY/VALUE arguments so its Git children inherit those controls.
It retains the same2GiB process address cap, full406 checker and no wall/CPU
timeout. Its own completed receipt, not this note, determines pass/fail.
The original failed receipt remains banked. This is a resource repair of the
required historical audit, not a second scientific correction cycle or a relaxed
scientific threshold. It occurs after the fixed final scientific attestations;
those reports explicitly did not pre-certify subsequent audit/banking outcomes.
