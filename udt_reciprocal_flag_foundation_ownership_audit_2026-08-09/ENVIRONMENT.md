# Run environment

```text
Date: 2026-08-09
Repository base after preregistration: 79bf151c4ec9fe66eeb1f251aabcdb793c7735e7
Python: 3.10.12
SymPy: 1.13.1
Platform: Linux 6.8.0-124-generic x86_64 GNU/Linux
GPU: not used
```

Commands:

```text
python3 udt_reciprocal_flag_foundation_ownership_audit_2026-08-09/derive_reciprocal_flag_ownership.py
python3 udt_reciprocal_flag_foundation_ownership_audit_2026-08-09/verify_reciprocal_flag_ownership.py
python3 udt_reciprocal_flag_foundation_ownership_audit_2026-08-09/verify_repository_gates.py
python3 -m pytest tests/
```

The independent verifier uses only the Python standard library and does not import the SymPy
controller.
