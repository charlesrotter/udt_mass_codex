# SM2 review execution record

All commands ran from /home/udt-admin/udt_mass_codex. The existing capture
utility was inspected, not edited; SHA256
8ff5469ace76bdfc84188915242abbf3baff35516f9ee3f9ba4b1cbfeb2573ef.
It writes non-overwriting captures, applies512MiB AS/60s CPU limits and60s
wall timeout. No children overlapped in this review context. Python3.10.12,
SymPy1.13.1; exact-symbolic finite diagnostics, not floating certification.

Each invocation used this exact prefix:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py
```

The following are the exact arguments following that prefix, in execution order:

```sh
/home/udt-admin/udt_mass_codex/udt_source_metric_connection_campaign_2026-09-08/step_02/review/independent_initial /home/udt-admin/udt_mass_codex python3 -B udt_source_metric_connection_campaign_2026-09-08/step_02/review/independent_tensor_check.py
/home/udt-admin/udt_mass_codex/udt_source_metric_connection_campaign_2026-09-08/step_02/review/author_initial_replay /home/udt-admin/udt_mass_codex python3 -B udt_source_metric_connection_campaign_2026-09-08/step_02/check_tensor.py
/home/udt-admin/udt_mass_codex/udt_source_metric_connection_campaign_2026-09-08/step_02/review/author_repaired_replay /home/udt-admin/udt_mass_codex python3 -B udt_source_metric_connection_campaign_2026-09-08/step_02/check_tensor_repaired.py
/home/udt-admin/udt_mass_codex/udt_source_metric_connection_campaign_2026-09-08/step_02/review/guard_catchproof_run /home/udt-admin/udt_mass_codex python3 -B udt_source_metric_connection_campaign_2026-09-08/step_02/review/guard_catchproof.py
```

The matching JSON files preserve child command arrays, start time, duration,
return code, timeout status, AS/CPU limits and maximum RSS. The corresponding
.stdout/.stderr files preserve streams separately. The initial author replay
exit1 is an expected reproduced original harness defect, not suppressed.
All other runs returned0. Direct `cmp` verified byte identity of repaired
author stdout and initial author stderr with their preserved author versions.

Read-only source/hash checks used sha256sum, git rev-parse HEAD and explicit
scoped reads. Baseline remained cc71a324a61bf2711a4b52c8ebee8a8e4d9b8269.
No git mutation or synchronization occurred. No host-wide process audit was
performed or claimed. Worktree status was inspected without opening protected
payloads. No accepted-grade, scientific premise, canon or manuscript edit.
