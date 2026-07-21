# Commands

Run from repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_dynamics_branch_ruling_p04_2026-07-21/build_p04_ruling.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_dynamics_branch_ruling_p04_2026-07-21/verify_p04_ruling.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_dynamics_branch_ruling_p04_2026-07-21/verify_repository_gates.py
PYTHONDONTWRITEBYTECODE=1 python3 -B udt_dynamics_branch_ruling_p04_2026-07-21/build_manifest.py
```

Environment:

```text
Python 3.10.12
Third-party Python dependencies: none
GPU work: none
Symbolic variation: none
ODE/PDE work: none
```
