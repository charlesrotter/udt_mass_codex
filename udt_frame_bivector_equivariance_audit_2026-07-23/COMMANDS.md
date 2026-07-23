# Commands

All scientific computation was CPU-only.

## Production exact algebra

```bash
PYTHONDONTWRITEBYTECODE=1 python3 derive_frame_bivector_equivariance.py
```

Python `3.10.12`; SymPy `1.13.1`, pinned in `requirements.txt`.

## Independent implementation

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_frame_bivector_independent.py
```

This implementation uses only the Python standard library and exact
`fractions.Fraction` arithmetic. It does not import the production module.

## Isolated dependency replay

The host lacks `ensurepip`/`python3-venv`. A fresh temporary dependency
directory was therefore populated with only the installed pinned
`sympy==1.13.1` and its `mpmath==1.3.0` dependency. User site loading was
disabled:

```bash
PYTHONNOUSERSITE=1 \
PYTHONPATH=/tmp/udt_frame_bivector_env_C1uigL/site-packages \
PYTHONDONTWRITEBYTECODE=1 \
python3 -s derive_frame_bivector_equivariance.py

PYTHONNOUSERSITE=1 \
PYTHONPATH=/tmp/udt_frame_bivector_env_C1uigL/site-packages \
PYTHONDONTWRITEBYTECODE=1 \
python3 -s verify_frame_bivector_independent.py
```

Both replays passed.

## Repository tests

```bash
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/
```

Result: `70 passed, 1 xfailed, 0 failed`.
