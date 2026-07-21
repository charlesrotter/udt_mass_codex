# Commands

Run from repository root with CPU-only scope:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_global_kinematic_assembly_p03g_2026-07-21/build_p03g_global_assembly.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_global_kinematic_assembly_p03g_2026-07-21/verify_p03g_global_assembly.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_global_kinematic_assembly_p03g_2026-07-21/verify_repository_gates.py
PYTHONDONTWRITEBYTECODE=1 python3 -B udt_global_kinematic_assembly_p03g_2026-07-21/build_manifest.py
```

Environment used for the banked run:

```text
Python 3.10.12
SymPy 1.13.1
GPU work: none
ODE/PDE work: none
```

