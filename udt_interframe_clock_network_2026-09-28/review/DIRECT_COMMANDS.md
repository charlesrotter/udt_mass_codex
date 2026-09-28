# Direct-stage command and exposure record

Read INITIAL_CANDIDATE.md and CANDIDATE_FREEZE.json before scientific author
code/results. Wrote reviewer-owned direct_checks.py, then ran:

```bash
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_interframe_clock_network_2026-09-28/review/direct_run /home/udt-admin/udt_mass_codex python3 udt_interframe_clock_network_2026-09-28/review/direct_checks.py
```

The script independently validates frozen artifact hashes and source-first seal;
hash-only reads do not expose artifact contents to model context. Captured
stdout/stderr/receipt are direct_run.*. No failed direct scientific run occurred.
An inline Python SHA256 command froze direct_checks.py, DIRECT_CHECKS.json and
direct_run.* in DIRECT_CHECKS_SEAL.json before author code/output content reads.

Next read check_network.py, checks/CHECK_REPAIR.md, checks/network.stderr and
checks/network_repaired.stdout. Read REPAIR.md after parent's repair dispatch.
Queried only summary fields of DIRECT_CHECKS.json and `git diff --stat` (empty).
Only review/ files were written. No source/candidate/status/protected files were
modified or staged by the reviewer.

Web method-source check: opened https://arxiv.org/abs/0708.0170 and its PDF,
https://arxiv.org/pdf/0708.0170, checking radar equations and regular local
neighborhood scope. No web-derived physical law or numerical parameter used.

DIRECT_REVIEW_SEAL.json hashes the direct report/command record, repair and
candidate snapshots plus the independent-check seal. Hashes attest byte
correspondence; staged conversation/exposure records own chronology.
