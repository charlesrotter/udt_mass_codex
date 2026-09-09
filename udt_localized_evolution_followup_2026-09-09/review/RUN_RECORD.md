# LE1 reviewer run record

Reviewer context: `/root/le1_review`, separate context, model UNKNOWN.
Workspace and baseline: `/home/udt-admin/udt_mass_codex`, grok
`2fbd422a8271de56296ad2efa4a1037887e20c91`.
Only `udt_localized_evolution_followup_2026-09-09/review/` was authored here.
Parent owned shared synchronization; reviewer independently checked status,
branch and HEAD and did not switch/fetch/pull in the shared tree.

Startup read current LIVE/HANDOFF blocks, CURRENT_RESEARCH_PROGRAM,
CURRENT_SCIENTIFIC_PREMISES, CLAUDE method sections, triggered skills,
CROSS_MODEL_VERIFY, compact INDEX/MEMORY, work order and scoped sources.
The independently executed `python3 verify_current_scientific_premises.py`
returned 1 with G325 `replay_exact:DERIVATION_RESULT.json` failure, as retained
in the tool transcript; parent's startup_full365 capture owns the repository
raw full365 receipt. It was not repaired or called passed.

Scientific CPU checks all use this existing wrapper and absolute output stem:

    python3 udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_localized_evolution_followup_2026-09-09/review/NAME /home/udt-admin/udt_mass_codex env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 [OPTIONS] SCRIPT [ARGUMENTS]

Each NAME.json contains the exact actual command, cwd, UTC start, duration,
status, timeout flag, 536870912-byte address-space limit, 60-second CPU limit
and maximum RSS; its stdout/stderr preserve raw output. The wrapper also
sets a 60-second wall timeout. Wrapper SHA256:
`8ff5469ace76bdfc84188915242abbf3baff35516f9ee3f9ba4b1cbfeb2573ef`.

Source-first sequence:

| Output stem | Start UTC | Exit | Meaning |
|---|---|---:|---|
| source_first_check | 18:36:32 | 1 | Initial unresolved symbolic-power zero comparison; preserved |
| source_first_failure_probe | 18:37:03 | 0 | Printed actual residual and q=1 control |
| source_first_recheck | 18:38:03 | 1 | First normalization still insufficient; preserved |
| power_normalization_probe | 18:38:26 | 0 | Deep power simplification and denesting both return exact zero |
| source_first_recheck_pass | 18:38:52 | 0 | Corrected normalization; full independent identities passed |

The original source_first_check.py remains unchanged. RECHECK_REPAIR.patch
reconstructs the sole one-line source_first_recheck.py change; pre-change
hash `6d63aa022df81af3f0e7c26d580942ed7808aee5ac115f036ac83c9f8985957b`.
The two `-c` probes' exact scripts are preserved in their JSON command arrays.
SOURCE_FIRST.md was sealed/transmitted before any LE1 proof/code/output
exposure; its hash is recorded in DIRECT_REVIEW.md. The computations use
Python 3.10.12 and SymPy 1.13.1. All scientific runs were sequential.

Post-exposure sequence:

| Output stem | Start UTC | Exit | Meaning |
|---|---|---:|---|
| direct_tensor_boost | 18:43:42 | 0 | New full four-dimensional Lorentz tensor check |
| author_replay | 18:43:59 | 0 | Frozen author code regression; stdout byte-identical |
| catch_absolute_equals_shape | 18:44:00 | 1 | Expected adverse assertion |
| catch_linear_blindness | 18:44:01 | 1 | Expected adverse assertion |
| catch_electric_only | 18:44:02 | 1 | Expected adverse assertion |
| catch_unit_coordinate_cone | 18:44:03 | 1 | Expected adverse assertion |

The four catch stderr files were individually read and fail at their intended
assertions, not import/resource errors. The byte comparison command was

    cmp udt_localized_evolution_followup_2026-09-09/author_check.stdout udt_localized_evolution_followup_2026-09-09/review/author_replay.stdout

It returned 0. Original candidate/source hashes were checked using
`sha256sum -c` on INITIAL_FREEZE_SHA256SUMS and SOURCE_SHA256SUMS.

Primary PDF byte hashes were independently recomputed by sha256sum using
the files in `/tmp/udt-le-method-wGuzar/`. Read-only source extraction used:

    pdftotext -layout -f 2 -l 8 /tmp/udt-le-method-wGuzar/0710.4902v1.pdf -
    pdftotext -layout -f 9 -l 10 /tmp/udt-le-method-wGuzar/0710.4902v1.pdf -
    pdftotext -layout -f 11 -l 11 /tmp/udt-le-method-wGuzar/0710.4902v1.pdf -
    pdftotext -layout -f 3 -l 6 /tmp/udt-le-method-wGuzar/1309.7591v3.pdf -
    pdftotext -layout /tmp/udt-le-method-wGuzar/1309.7591v3.pdf - | sed -n '486,622p'

The first Sbierski page range was contextual rather than section 2; a
subsequent targeted text read covered the actual section. No primary PDF was
downloaded by this reviewer, modified or copied into the repository.
Public source hashes/versions and sections are in DIRECT_REVIEW.md.

REVIEW_SHA256SUMS covers reviewer evidence, including ignored stdout files,
and excludes incidental `__pycache__` bytecode and the manifest itself.
No source preservation, grade change or scientific truth follows merely
from a checksum. Full limitations and exposed/omitted sources remain in the
two substantive review notes.
