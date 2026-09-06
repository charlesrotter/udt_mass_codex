# Execution and provenance

Working directory: `/home/udt-admin/udt_mass_codex`.
Branch/source HEAD: synchronized `grok`,
`0c9c6db68ab08618e750c57c0d8f166434aae043`.
Date: 2026-09-06. Python 3.10.12; SymPy 1.13.1. No dependency installation.

## Executed checks

`git status --short --branch`, `git rev-parse HEAD`, `git fetch origin`,
`git pull --ff-only origin grok`: inspected before work; synchronized,
already up to date. Original 46 unrelated untracked status entries remained
visible. No untracked payload contents were read for this test.

```bash
python3 verify_current_scientific_premises.py
timeout 120s python3 udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/check_witnesses.py > udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/check.stdout.txt 2> udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/check.stderr.txt
timeout 120s python3 udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/recompute_saved_witness.py > udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/recompute.stdout.txt 2> udt_g352_local_phase_measure_compatibility_candidate_2026-09-06/recompute.stderr.txt
```

All three exited zero. The premise verifier ran once in execution session
24509; its complete returned output is in `PREMISE_VERIFIER_OUTPUT.txt`.
Its output was merged by the execution interface, not separately captured.
The two short new commands have separately captured stdout/stderr plus
machine-readable results. Their stderr files are empty. Witness checks used
exact symbolic identities and rational values: no dtype/grid/tolerance,
floating-point convergence claim, GPU process, or field-equation solve.
The 120-second command timeout did not fire.

Load-bearing registry query, performed after the verifier passed:

```bash
awk -F '\t' '$1 ~ /^G(348|349|351|352)$/ {print $1 "\t" $3 "\t" $4 "\t" $8}' CURRENT_SCIENTIFIC_PREMISES.tsv
```

This read selected status/label/source fields for four exact rows, not the
335 wide rows. It confirmed current accepted conditional status, with G351
and G352 on owner-provisional premises. Historical pending-review headers
inside exact derivations do not supersede current registry and audit state.
No old physical examples, action, topology/carrier branch, protected local
package, or archive payload is a scientific dependency of this test.

## Source correspondence and closure

`SOURCE_SHA256SUMS` uses repository-root-relative paths and separates accepted
source/authority correspondence from the new package's `ARTIFACT_SHA256SUMS`.
The latter lists all package files except itself. SHA-256 proves byte
correspondence, not scientific truth, independence or trusted chronology.
Use `sha256sum -c` from the repository root to check both manifests.

`git diff --exit-code HEAD -- AGENTS.md CLAUDE.md LIVE.md HANDOFF.md
CURRENT_RESEARCH_PROGRAM.md CURRENT_SCIENTIFIC_PREMISES.md
CURRENT_SCIENTIFIC_PREMISES.tsv CANON.md` plus the G348/G349/G351/G352
source directories passed unchanged. A full tracked diff at closure is
restricted to this new candidate package. No root status/frontier, fixed-edition
manuscript, canon, source grade or protected payload change is included.

The restart audit was already accepted as sufficient for repository-only work.
Its backup-completeness and pre-reboot unsaved-state uncertainties remain
unverified; no preservation upgrade is inferred from this test. Original
untracked **path presence** is visible in git status, but protected payload
identity was intentionally not inspected. ScratchDisk remains archive-only
blocking. No disk repair/mount, worktree pruning or infrastructure refactor.

This candidate is saved as one logical evidence change. Committing/pushing
preserves it; neither action accepts its scientific claims. See
`REVIEW_RECORD.md` for the explicit uncompleted independent-review gate.
