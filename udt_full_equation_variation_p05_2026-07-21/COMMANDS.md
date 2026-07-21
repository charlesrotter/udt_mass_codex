# P05 commands

Run from repository root with CPU-only environment:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_full_equation_variation_p05_2026-07-21/derive_p05_operators.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_full_equation_variation_p05_2026-07-21/verify_p05_operators.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_full_equation_variation_p05_2026-07-21/build_manifest.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_full_equation_variation_p05_2026-07-21/verify_repository_gates.py
```

The first command deterministically writes the operator tables, graph, result, and transcript. The
second regenerates those records, checks byte stability, independently reconstructs load-bearing
identities, and exercises corruption catches. The manifest excludes itself and
`REPOSITORY_GATES.json`; repository gates are written after manifest validation.
