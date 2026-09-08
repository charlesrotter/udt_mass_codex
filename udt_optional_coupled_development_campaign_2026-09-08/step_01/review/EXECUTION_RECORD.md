# CD1 review execution record

Reviewer /root/cd1_data_review, 2026-09-08. All writes confined to this
step_01/review directory. Baseline grok
e1b6cdbef96f9a0ce8878d42d160a5ebe1f267f7. No shared git mutations/sync.

Source-first requirements were saved with apply_patch and hashed at
12:50:48UTC, before target question/candidate/code/output exposure. Their
immutable SHA256 is faf92d7445bd2bc4c46bdcd5f9fde58e1b64711c952268cf104b9cd2a2c8e362.
The independent flat-probe code and first run also precede full target
exposure. Exact pins arrived next; direct candidate and code inspection
followed. The target-specific rational-jet driver is post-exposure and
reuses an inspected prior reviewer geometry engine, as the review records.

Commands below were executed from /home/udt-admin/udt_mass_codex.
The existing run_capture.py was read in full before use. It refuses evidence
overwrite and captures separate stdout/stderr, command, start/duration,
returncode, timeout, AS/CPU limits and maximum child RSS. Each ordinary run
had 512MiB AS and60s CPU/wall caps; no ordinary numerical children overlapped
within this reviewer context. No GPU or production integration occurred.

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_optional_coupled_development_campaign_2026-09-08/step_01/review/independent_flat_probe_run /home/udt-admin/udt_mass_codex python3 udt_optional_coupled_development_campaign_2026-09-08/step_01/review/independent_flat_probe.py

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_optional_coupled_development_campaign_2026-09-08/step_01/review/independent_warped_jet_run /home/udt-admin/udt_mass_codex python3 -B udt_optional_coupled_development_campaign_2026-09-08/step_01/review/independent_warped_jet_check.py

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_optional_coupled_development_campaign_2026-09-08/step_01/review/author_replay_initial /home/udt-admin/udt_mass_codex python3 -B udt_optional_coupled_development_campaign_2026-09-08/step_01/check_initial_data.py

cmp udt_optional_coupled_development_campaign_2026-09-08/step_01/author_initial.stdout udt_optional_coupled_development_campaign_2026-09-08/step_01/review/author_replay_initial.stdout
```

All four commands exit0. Independent flat probe:12:51:43.138510UTC,
0.253062634s,RSS44660KiB;5 identities and5 nonzero negative controls.
Independent warped jets:12:54:26.446266UTC,0.139116205s,RSS17088KiB;
56 identities and4 actual RED assertion paths. Author replay:
12:54:45.047197UTC,0.362121132s,RSS51668KiB;17 groups and5 negative controls.
All captured stderr files are empty. Python3.10.12, SymPy1.13.1 for symbolic
checks; warped jets use stdlib exact Fraction arithmetic. No failed run or
candidate/check repair occurred. Counts remain finite diagnostics.

Startup audit exception: after reading the mandatory premise orientation,
the reviewer inadvertently executed the unwrapped command

```bash
python3 verify_current_scientific_premises.py
```

It returned exec session22247 with initially empty output, then completed
exit0/PASS as observed12:54:45UTC. The parent independently executed its
properly capped full354 audit and its receipt/output were read and hashed.
The duplicate reviewer run had no explicit timeout/memory/thread wrappers;
exact start/end, duration, resource use and separate stdout/stderr were not
captured. No such resource-compliance claim is made. Its merged tool output
is transcribed exactly to reviewer_startup354.tool-output.txt. The duplicate
is an operational omission and redundant audit, not an independent scientific
proof or necessary candidate repair. It has finished; no process remains
pending from this reviewer invocation.

No additional source hypotheses, network theorem research, profile fitting,
production solve, scientific promotion, protected-payload read/hash or shared
status edit occurred. Full audit and prior-source evidence are distinguished
from the fresh substantive CD1 review. All limitations and zero repair use
are retained in ADVERSARIAL_REVIEW_INITIAL.md.
