# Actual scientific command

Executed from `/home/udt-admin/udt_mass_codex`:

```bash
timeout 120s python3 udt_kernel_twist_information_audit_2026-09-10/whiteboard/run_record_checks.py
```

The runner's exact child argv, start/end UTC, timeout, exit, stdout/stderr and pre-run file hashes
are saved in `RECORD_CHECK_RUN.json`. It launches only `check_record_types.py`, with a 120-second
timeout, using `/usr/bin/python3`. The outer command exited 0. No retries or repairs occurred.

Scientific result files:

- `RECORD_CHECK_STDOUT.json`: full exact check residuals, constructed records and versions.
- `RECORD_CHECK_STDERR.txt`: empty.
- `RECORD_CHECK_RUN.json`: actual execution record.

Read-only source commands used `cat`, bounded `sed`, `rg`, and `nl`. Branch/hash were independently
checked using `git status --short --branch` and `git rev-parse HEAD`; no top-level startup replay.

Final source-row extraction and SHA-256 packaging command (no scientific recomputation):

```bash
timeout 120s python3 udt_kernel_twist_information_audit_2026-09-10/whiteboard/freeze_source_artifacts.py
```

The artifact manifest excludes itself. Hashes establish byte correspondence, not truth, independent
authorship or chronology. The scientific pre-run freeze hashes remain in the original run record.
