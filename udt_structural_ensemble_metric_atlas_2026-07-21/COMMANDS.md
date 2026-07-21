# Reproduction commands

Run from repository root in the documented CPU environment:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B udt_structural_ensemble_metric_atlas_2026-07-21/build_structural_ensemble_atlas.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B udt_structural_ensemble_metric_atlas_2026-07-21/verify_structural_ensemble_atlas.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B udt_structural_ensemble_metric_atlas_2026-07-21/build_manifest.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B udt_structural_ensemble_metric_atlas_2026-07-21/verify_repository_gates.py
```

The builder regenerates all masks, configurations, raw shards, and interaction tables. The verifier
does not import the builder; it reconstructs every primitive two-jet, metric, raw curvature, and
Möbius term. The manifest and repository gate commands freeze and replay the completed package.
