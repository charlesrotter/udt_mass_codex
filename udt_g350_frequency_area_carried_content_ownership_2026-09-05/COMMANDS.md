# G350 registered commands

Run from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -B -S derive_carried_content_ownership.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -B -S verify_carried_content_ownership_independent.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -B -S run_catch_proofs.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -B -S verify_package.py
```

No GPU or long solve is registered. Every route is dependency-free and must preserve package bytes
when `UDT_NO_WRITE=1`.
