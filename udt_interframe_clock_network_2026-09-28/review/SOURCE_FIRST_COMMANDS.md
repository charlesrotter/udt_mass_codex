# Source-first commands and exposure

All commands executed from /home/udt-admin/udt_mass_codex.

Read-only orientation: `pwd`; `git status --short --branch`; `git rev-parse HEAD`;
`cat AGENTS.md`; `cat udt_interframe_clock_network_2026-09-28/WORK_ORDER.md
udt_interframe_clock_network_2026-09-28/LAUNCH.json`.

Protocol reads: `rg -n '^#{1,4} |DRIVER TRIGGERS|repo discipline' CLAUDE.md`;
`rg --files .claude/skills`; `sed -n '9,83p;121,134p' CLAUDE.md`; `cat` of
verifier-before-record, no-shortcuts, solution-space-not-imposition and
completeness-map SKILL.md files plus CROSS_MODEL_VERIFY.md.

Scientific reads: `rg -n 'W4|W5|c_E|G_obs|dimension|G176' founding.md`;
`sed -n '61,75p;199,267p;487,546p;746,761p' founding.md`; `cat` of G220
EXACT_DERIVATION, FSL1 REVIEWED_RESULT, FCV1 REVIEWED_RESULT, current G312
AUTHORITY_RECORD and the reused run_capture.py. An inline Python read hashed
every LAUNCH source pin and selected exact G176/G220/G312 registry rows; it
did not inspect other row contents. The persisted independent script repeats
the hash check and branch/ref checks. No ICN1 candidate/proof/code/output read.

Created only this review directory and its reviewer-owned files. Script edited
before its first execution to support matrix/infinite-limit comparisons.
No failed scientific run preceded the captured successful run.

Exact outer run command:

```bash
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_interframe_clock_network_2026-09-28/review/source_first_run /home/udt-admin/udt_mass_codex python3 udt_interframe_clock_network_2026-09-28/review/source_first_checks.py
```

Resource wrapper uses 60s CPU/wall, 512MiB address space and refuses to overwrite
its stdout/stderr/JSON receipts. It is shared execution infrastructure, not
shared scientific checking code. Scientific source-first code independently
constructed in this context using Python3.10.12 and SymPy1.13.1. See captured
receipt for measured runtime/maxrss and machine JSON for exact quantities.

Sealing: SHA-256 hashes of all source-first review files are saved in
SOURCE_FIRST_SEAL.json after the report is written. This attests correspondence
of the frozen bytes; conversation stage ordering establishes exposure history,
not the hashes alone.
