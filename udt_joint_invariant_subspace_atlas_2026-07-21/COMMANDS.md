# Commands

Environment: Python 3.10.12, NumPy 2.2.6, CPU only.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m py_compile udt_joint_invariant_subspace_atlas_2026-07-21/invariant_subspace_core.py udt_joint_invariant_subspace_atlas_2026-07-21/build_joint_atlas.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B udt_joint_invariant_subspace_atlas_2026-07-21/build_joint_atlas.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -m py_compile udt_joint_invariant_subspace_atlas_2026-07-21/verify_joint_atlas.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B udt_joint_invariant_subspace_atlas_2026-07-21/verify_joint_atlas.py
python3 udt_joint_invariant_subspace_atlas_2026-07-21/build_manifest.py
python3 udt_joint_invariant_subspace_atlas_2026-07-21/verify_repository_gates.py
```

No GPU, ODE/PDE solve, relaxation, fitting, action solve, or physical evolution was run.
