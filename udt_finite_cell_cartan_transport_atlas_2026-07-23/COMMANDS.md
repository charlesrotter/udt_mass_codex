# Commands

All work was CPU-only.

Production derivation:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 derive_finite_cell_cartan_transport.py
```

Independent exact verifier:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -s verify_finite_cell_cartan_independent.py
```

Full repository test:

```bash
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/
```
