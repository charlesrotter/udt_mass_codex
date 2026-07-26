# Replay commands

All computations are CPU-only and use only the Python standard library.

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 udt_completion_scoped_realized_observable_map_2026-07-26/derive_completion_map.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 udt_completion_scoped_realized_observable_map_2026-07-26/verify_independent.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 udt_completion_scoped_realized_observable_map_2026-07-26/verify_package.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 udt_completion_scoped_realized_observable_map_2026-07-26/verify_repository_gates.py
```

The package verifier records raw production and independent stdout/stderr,
requires deterministic generated outputs, and refuses source or
preregistration drift.
