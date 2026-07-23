# Exact commands

Environment:

```text
Python 3.10.12
SymPy 1.13.1
CPU only
```

Commands:

```bash
python3 derive_observer_centered_xmax.py --write
python3 verify_observer_centered_xmax_independent.py
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/
python3 build_manifest.py
sha256sum --check MANIFEST.sha256
python3 verify_repository_gates.py
```
