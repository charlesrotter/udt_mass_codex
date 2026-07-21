# Commands

Run from repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' \
  python3 -B udt_constructive_metric_family_atlas_2026-07-21/build_constructive_atlas.py

PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' \
  python3 -B udt_constructive_metric_family_atlas_2026-07-21/verify_constructive_atlas.py

python3 udt_constructive_metric_family_atlas_2026-07-21/build_manifest.py
python3 udt_constructive_metric_family_atlas_2026-07-21/verify_repository_gates.py
```

The independent SymPy reconstruction is CPU-bound and may take about two minutes. No ODE, PDE,
relaxation, or GPU process belongs to this package.
