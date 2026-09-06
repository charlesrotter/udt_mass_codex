# Stage B review execution record

Date: 2026-09-06. Exact runtime model identity: UNKNOWN.
Pinned candidate HEAD: `3c841561ca0d1529ca41ef75fb1aece465ee0098`.
Original source snapshot declared by candidate: `0c9c6db68ab08618e750c57c0d8f166434aae043`.
Argument SHA256: `034a8d200a94ebcad4ab921997eb55d614ab9f178864812b4937f7e905184e2e`.

Stage A was delivered and parent-reported as preserved before candidate disclosure.
Stage B is fully exposed to all 17 original candidate files, including the original
same-context review. No new scientific candidate/source files were changed.
The file-list command also returned review-document path names; those added
review documents were not opened in Stage B.

## Exact substantive read commands

Working directory `/home/udt-admin/udt_mass_codex`:

```bash
rg --files udt_g352_local_phase_measure_compatibility_candidate_2026-09-06 -g '!review_2026-09-06/**'
sed -n '1,320p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/CANDIDATE_ARGUMENT.md && sed -n '1,240p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/WORK_ORDER.md && sed -n '1,220p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/PREMISE_AND_COVERAGE.tsv
sed -n '1,300p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/check_witnesses.py
sed -n '1,300p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/recompute_saved_witness.py && sed -n '1,260p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/REVIEW_RECORD.md && sed -n '1,240p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/COMMANDS_AND_PROVENANCE.md
sed -n '1,200p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/README.md && sed -n '1,260p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/CHECK_RESULT.json && sed -n '1,240p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/RECOMPUTATION_RESULT.json && sed -n '1,180p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/SOURCE_SHA256SUMS && sed -n '1,180p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/ARTIFACT_SHA256SUMS
sed -n '1,260p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/REVIEW_RECORD.md && sed -n '1,260p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/COMMANDS_AND_PROVENANCE.md && sed -n '261,600p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/CHECK_RESULT.json && sed -n '1,160p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/PREMISE_VERIFIER_OUTPUT.txt && sed -n '1,120p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/check.stdout.txt && sed -n '1,120p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/check.stderr.txt && sed -n '1,120p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/recompute.stdout.txt && sed -n '1,120p' udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/recompute.stderr.txt
```

The repeated review/provenance read recovered a combined-tool output truncation.
The remainder of CHECK_RESULT.json was explicitly read; every original file was inspected.

## Exact checks and replays

Working directory `/tmp/udt-g352-separate-review-4OjAl5`:

```bash
sha256sum -c /home/udt-admin/udt_mass_codex/udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/ARTIFACT_SHA256SUMS && sha256sum udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/ARTIFACT_SHA256SUMS && awk -F '\t' '$1 ~ /^G(348|349|351|352)$/ {print $1 "\t" $3 "\t" $4 "\t" $8}' CURRENT_SCIENTIFIC_PREMISES.tsv
timeout 120s python3 -B udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/check_witnesses.py > stage_b_check.stdout.txt 2> stage_b_check.stderr.txt
timeout 120s python3 -B udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/recompute_saved_witness.py > stage_b_recompute.stdout.txt 2> stage_b_recompute.stderr.txt
timeout 120s python3 -B reviewer_stage_b_checks.py > stage_b_reviewer.stdout.txt 2> stage_b_reviewer.stderr.txt
sed -n '1,260p' REVIEWER_STAGE_B_RESULT.json && sed -n '1,120p' stage_b_check.stdout.txt && sed -n '1,120p' stage_b_check.stderr.txt && sed -n '1,120p' stage_b_recompute.stdout.txt && sed -n '1,120p' stage_b_recompute.stderr.txt && sed -n '1,120p' stage_b_reviewer.stderr.txt && sha256sum -c /home/udt-admin/udt_mass_codex/udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/ARTIFACT_SHA256SUMS && cmp udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/ARTIFACT_SHA256SUMS /home/udt-admin/udt_mass_codex/udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/ARTIFACT_SHA256SUMS
```

Every command above exited zero. All three replay stderr files are empty.
Both original JSON results reproduced their original SHA256 bytes. All 16
original manifest entries matched before and after replay; the manifest itself
matched the repository copy with `cmp`.

Final repository read-only correspondence command, working directory
`/home/udt-admin/udt_mass_codex`:

```bash
sha256sum -c udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/SOURCE_SHA256SUMS && sha256sum -c udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/ARTIFACT_SHA256SUMS && git rev-parse HEAD
```

All 19 source-manifest entries and 16 artifact-manifest entries passed; HEAD
remained the pinned hash. CANON and restart-report bytes were hashed by their
manifest entries, not read as scientific premises. Parent's live premise
verifier session 40856 exited zero at parent-reported 16:00:10 UTC with PASS335
rows. That replay is parent-performed documentary evidence, not my execution.

## Results and preserved failure evidence

- Original replay: 86 exact assertions and 8/8 declared data-level sensitivity
  rejections. Original saved-input rational recomputation also passed.
- Reviewer arithmetic: Cartesian stereographic direction `(24,36,23)/49`,
  nonzero variable-cut gradients, solid-angle density `5184/2401`, area factors
  `(4,9)`, frequencies `(1,1/2)`, rates `(5/56,5/252)` for explicitly chosen
  density `5/6` and spacing `7/3`, transfer `2/9`; fixed-square half masses
  `1/2` and `3/8` at equal total one.
- Three actual in-memory source mutations failed: reversed frequency sign,
  omitted rate frequency, and radius substituted for area. Complete expected
  failure traces are `reverse_frequency_sign.failure.txt`,
  `omit_frequency_in_rate.failure.txt`, and `area_equals_radius.failure.txt`.
- An always-zero acceleration helper survived all original 86 assertions and
  all 8 data-level mutation checks. This false pass is preserved in the JSON
  and script. The independent reviewer control `ell=(1+t)(1,0,0,1)`, on `t>-1`,
  has acceleration `(1+t)(1,0,0,1)`; it catches the mutant. The original helper
  returned the correct nonzero value. This limits test coverage, not the
  candidate's analytic Hessian proof. No original code was repaired.

`reviewer_stage_b_checks.py` was created with apply_patch, not by editing the
candidate scripts. It derives paths from its own directory, so relocation is
supported if the original candidate directory remains beside it under its exact
name. It has no workspace argument and no hard-coded absolute scratch path.
For original check_witnesses.py replay, put the exact source registry in that
same parent directory as `CURRENT_SCIENTIFIC_PREMISES.tsv`. Outputs are written
beside the reviewer script; original scripts write beside themselves. Copy the
reviewer script and exact original inputs to scratch before replaying.

Python 3.10.12; SymPy 1.13.1. Independent arithmetic uses standard-library
Fraction only; SymPy and original source code are used separately for mutation
probes. No GPU, floating-point tolerance, network, field solve, broad suite,
accepted-source package replay, or repository mutation was performed.
