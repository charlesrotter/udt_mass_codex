#!/usr/bin/env bash
set -euo pipefail
repo=/home/udt-admin/udt_mass_codex
campaign=udt_shared_readout_metric_constraint_campaign_2026-09-06
scratch=/tmp/tri_closure_fidelity.5CGThc
pin=70034a6faa9264bf054eb473d5eb7a0889f3d2de
cd "$repo"
git rev-parse HEAD
git branch --show-current
sha256sum --check "$campaign/CLOSURE_REVIEW_INPUT_SHA256SUMS"
sha256sum --check "$campaign/PRESERVED_FILES_SHA256SUMS"
for protected_file in UDT_METRIC_KERNEL_DEVELOPMENT.md UDT_METRIC_KERNEL_COVERAGE.tsv CANON.md CURRENT_SCIENTIFIC_PREMISES.tsv; do
    git show "$pin:$protected_file" | cmp - "$protected_file"
    printf 'Accepted-pin byte match: %s\n' "$protected_file"
done
for step in step_01 step_02 step_03 step_04 step_05; do
    sha256sum --check "$campaign/$step/CANDIDATE_SHA256SUMS"
    sha256sum --check "$campaign/$step/SOURCE_SHA256SUMS"
    if [[ "$step" == step_04 ]]; then
        review_manifest=SHA256SUMS
    else
        review_manifest=REVIEW_SHA256SUMS
    fi
    (cd "$campaign/$step/review" && sha256sum --check "$review_manifest")
done
sha256sum --check "$campaign/step_05/repair/REPAIR_SHA256SUMS"
(cd "$campaign/step_05/repair/review" && sha256sum --check REVIEW_SHA256SUMS)
git diff --check -- LIVE.md HANDOFF.md CURRENT_RESEARCH_PROGRAM.md INDEX.md MEMORY.md "$campaign/CAMPAIGN_LOG.md"
for input_file in LIVE.md HANDOFF.md CURRENT_RESEARCH_PROGRAM.md INDEX.md MEMORY.md; do
    cp -- "$input_file" "$scratch/initial_$input_file"
done
cp -- "$campaign/CLOSURE_REVIEW_INPUT_SHA256SUMS" "$scratch/INITIAL_INPUT_SHA256SUMS"
for input_file in WORK_ORDER.md DECISION_BRIEF.md CAMPAIGN_LOG.md CLOSURE_CHECK_PLAN.md; do
    cp -- "$campaign/$input_file" "$scratch/initial_$input_file"
done
sha256sum AGENTS.md CLAUDE.md .claude/skills/verifier-before-record/SKILL.md .claude/skills/completeness-map/SKILL.md .claude/skills/no-shortcuts/SKILL.md CURRENT_SCIENTIFIC_PREMISES.md "$campaign/run_capture.py" "$campaign/CLOSURE_CHECK_PLAN.md" "$campaign/WORK_ORDER.md"
git diff -- LIVE.md HANDOFF.md CURRENT_RESEARCH_PROGRAM.md INDEX.md MEMORY.md
git --version
bash --version
python3 --version
sha256sum --version
printf 'All explicitly scoped correspondence checks passed.\n'
