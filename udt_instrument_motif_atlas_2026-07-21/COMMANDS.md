# Commands

Environment: Python 3.10.12, NumPy 2.2.6, CPU only.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m py_compile udt_instrument_motif_atlas_2026-07-21/motif_core.py udt_instrument_motif_atlas_2026-07-21/build_motif_atlas.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B udt_instrument_motif_atlas_2026-07-21/build_motif_atlas.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B udt_instrument_motif_atlas_2026-07-21/verify_motif_atlas.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B udt_instrument_motif_atlas_2026-07-21/verify_motif_margins.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B udt_instrument_motif_atlas_2026-07-21/verify_package_contract.py
PYTHONDONTWRITEBYTECODE=1 python3 -B udt_instrument_motif_atlas_2026-07-21/build_manifest.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B udt_instrument_motif_atlas_2026-07-21/verify_repository_gates.py
```

The full run performs no ODE/PDE solve, relaxation, fitting, action solve, or physical evolution.
The banked production transcript uses `script -q -e -f -c` around the exact full-run command above;
the wrapper records stdout and does not change the command's environment or arguments. Single-thread
BLAS is a CPU scheduling control for many tiny matrices; a prereplay 64-configuration benchmark
gave identical JSON and took 4.88 seconds at one thread versus 5.14, 5.15, and 5.17 seconds at the
workstation default, two, and four threads respectively.
