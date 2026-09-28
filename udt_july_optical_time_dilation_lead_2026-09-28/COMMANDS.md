# Reproduction commands and actual author runs

All commands run from `/home/udt-admin/udt_mass_codex` on `grok`.
This continuing session's baseline synchronization used `git fetch origin`,
then `git pull --ff-only origin grok`, with HEAD unchanged at 008cce0d.
The first sandboxed fetch could not write .git/FETCH_HEAD; the permissioned
fetch and ff-only pull succeeded. No reset, stash or cleanup was used.

```bash
python3 udt_july_optical_time_dilation_lead_2026-09-28/run_premise_audit.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 60s python3 udt_july_optical_time_dilation_lead_2026-09-28/check_lead.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 60s python3 udt_july_optical_time_dilation_lead_2026-09-28/check_time_dependent_followup.py
```

The audit wrapper preserves exact command, timeout, versions, input hashes,
elapsed time, exit code and stdout/stderr in premise_audit/.

Author initial run: exit 1, INITIAL_check_lead.py with author_01.stdout.txt and
author_01.stderr.txt; root author.stdout.txt/author.stderr.txt retain the same
initial diagnostic. The positivity assumption was then encoded correctly;
AUTHOR_DIAGNOSTIC.md records the change. Revised author run: exit 0,
author_02.stdout.txt/author_02.stderr.txt and CHECK_RESULT.json. Do not overwrite
these saved outputs when replaying; use a copied script in a fresh directory,
as the reviewer did. The scripts write result JSON beside their own file.

Time-dependent follow-up: exit 0, time_followup.stdout.txt and
time_followup.stderr.txt; TIME_DEPENDENT_CHECK_RESULT.json.
Exact symbolic array sizes are at most 3x3 in the author check; the independent
review includes an explicit 4D curvature computation. No GPU or observational
fit. Reviewer commands, exposures, runtime and results are recorded in review/.
