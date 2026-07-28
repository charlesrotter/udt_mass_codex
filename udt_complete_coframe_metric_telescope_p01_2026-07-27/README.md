# Complete-coframe metric telescope P01

Start with [AUDIT_REPORT.md](AUDIT_REPORT.md), then [LAY_REPORT.md](LAY_REPORT.md).

Machine evidence:

- `ATLAS_RESULT.json` and five root-level `ATLAS_shell_*` checkpoints: primary
  V100 run;
- `CPU_ANCHOR_VERIFICATION.json`: independent NumPy/finite-difference check;
- `RESOURCE_REPLAY_SCOPED_VERIFICATION.json`: sub-6-GiB batch replay;
- `STRUCTURE_CENSUS.json`: deterministic descriptive census;
- `failed_production_attempt_01/` and `RESOURCE_REPLAY_VERIFICATION.json`:
  preserved fail-closed history.

The package maps bounded off-shell configurations.  It contains no background
equation, action, source, carrier, density, boundary selector, or physical
time evolution.

