# Commands

Environment: Python 3.10.12, NumPy 2.2.6, CPU only.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m py_compile udt_instrument_motif_atlas_2026-07-21/motif_core.py udt_instrument_motif_atlas_2026-07-21/build_motif_atlas.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B udt_instrument_motif_atlas_2026-07-21/build_motif_atlas.py
```

The full run performs no ODE/PDE solve, relaxation, fitting, action solve, or physical evolution.
