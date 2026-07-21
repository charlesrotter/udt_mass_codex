# Commands

Run from repository root with CPU-only settings:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' \
  python3 -B udt_finite_cell_completion_atlas_2026-07-21/build_completion_atlas.py

PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' \
  python3 -B udt_finite_cell_completion_atlas_2026-07-21/verify_completion_atlas.py

python3 udt_finite_cell_completion_atlas_2026-07-21/build_manifest.py
python3 udt_finite_cell_completion_atlas_2026-07-21/verify_repository_gates.py
```

No ODE, PDE, relaxation, or GPU process belongs to this package.
