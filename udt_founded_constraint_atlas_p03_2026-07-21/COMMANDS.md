# P03 commands

Run from repository root with CPU-only environment:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B \
  udt_founded_constraint_atlas_p03_2026-07-21/build_p03_constraint_atlas.py

PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B \
  udt_founded_constraint_atlas_p03_2026-07-21/verify_p03_constraint_atlas.py

PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B \
  udt_founded_constraint_atlas_p03_2026-07-21/build_manifest.py

PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B \
  udt_founded_constraint_atlas_p03_2026-07-21/verify_repository_gates.py
```

The main builder and independent verifier use SymPy `1.13.1` and the standard library. They launch
no ODE/PDE solve, relaxation, subprocess agent, or GPU process.
