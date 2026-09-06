# Review command record

All commands execute from /home/udt-admin/udt_mass_codex unless the capture
record states otherwise. Scientific sources use git show with source pin
70034a6faa9264bf054eb473d5eb7a0889f3d2de. Read-only source inspections were
displayed through the tool transcript; their full source-byte SHA-256 values
are saved in source_first.stdout. No source files were changed.

Initial operational checks: `git status --short --branch`; `git rev-parse HEAD`.
Read pinned `AGENTS.md`; current bounded LIVE and HANDOFF STARTUP_CURRENT blocks;
CURRENT_RESEARCH_PROGRAM.md and CURRENT_SCIENTIFIC_PREMISES.md; CLAUDE.md;
the no-shortcuts/completeness-map/verifier-before-record SKILL.md files;
CROSS_MODEL_VERIFY.md; INDEX.md and MEMORY.md. Current-status files are
orientation only, not scientific inputs. No full premise audit by dispatch.

Source discovery/read operations:

- `git show PIN:CURRENT_SCIENTIFIC_PREMISES.tsv` piped to awk selecting only
  header and exact G261/G312/G348 rows; separately G313 ID/term/source path.
- `git show PIN:founding.md` piped to sed extracting W4 through W5 heading.
- `git show PIN:udt_g261_universal_metric_coupling_parent_operator_ownership_2026-08-25/AUDIT_REPORT.md`
- `git show PIN:startup_surface_g312_two_premise_adoption_refresh_2026-09-01/ADOPTION_RECORD.md`
- `git show PIN:udt_g312_quiet_gr_response_constitution_discriminator_2026-09-01/AUDIT_REPORT.md`
- `git show PIN:udt_g313_tracefree_ricci_solution_space_bootstrap_map_2026-09-01/AUDIT_REPORT.md`
- `git show PIN:udt_g313_tracefree_ricci_solution_space_bootstrap_map_2026-09-01/EXACT_DERIVATION.md`
- `git show PIN:udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/AUDIT_REPORT.md`
- `git show PIN:udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/EXACT_DERIVATION.md`

PIN above expands to the exact source commit stated in this record.
One `git ls-tree` guessed G313 directory name failed with exit128; the registry
resolved the correct path before evidence use. A G348 `git ls-tree` succeeded.

Campaign read-only reads: WORK_ORDER.md, step_03/QUESTION.md and run_capture.py.
Their initial SHA-256 values were respectively
61b683a90d7d4416256d1cf08779a981e56ed7c52510e9dc2cfb5e4c4f895da8,
2c4915913bc3ea808b5f8dab59d68140556ff2c5fb6142fe52c40049d95d0ba9,
8ff5469ace76bdfc84188915242abbf3baff35516f9ee3f9ba4b1cbfeb2573ef.
Temporary directory creation: `mktemp -d /tmp/tri_step03_review.XXXXXXXX`.
Review documents and scripts created only there with apply_patch.

Exact independent computational run:

```text
python3 udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /tmp/tri_step03_review.pUqgBY2V/source_first /home/udt-admin/udt_mass_codex python3 /tmp/tri_step03_review.pUqgBY2V/independent_tensor.py
```

The wrapper captures exact inner argv, UTC start, elapsed time, return code,
timeout, resource ceilings and child RSS to source_first.json. Complete child
stdout/stderr are source_first.stdout and source_first.stderr. All assertions
are exact arithmetic; no tolerance, floating convergence or sampling proof.
