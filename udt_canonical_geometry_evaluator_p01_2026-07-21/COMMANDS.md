# Commands

Executed from the clean worktree root on 2026-07-21.

## Deterministic evaluator

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B \
  udt_canonical_geometry_evaluator_p01_2026-07-21/run_p01_evaluator.py
```

## Independent verifier

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B \
  udt_canonical_geometry_evaluator_p01_2026-07-21/verify_p01_evaluator.py
```

The requirements are pinned in `requirements.txt`. Both commands are CPU-only fixed-size local
tensor/symbolic checks. They perform no scientific solve.

## Package and repository gates

```bash
python3 udt_canonical_geometry_evaluator_p01_2026-07-21/build_manifest.py
python3 udt_canonical_geometry_evaluator_p01_2026-07-21/verify_repository_gates.py
```

The repository gate replays P01, all prior scientific-package manifests, six frozen manifests,
navigation/frontier/current-path checks, the documented test baseline, and metadata-only preservation
of the original dirty checkout.
