# Run environment

```text
Date: 2026-08-09
Repository base after preregistration correction: 10d807a2
Python: 3.10.12
SymPy: 1.13.1
Platform: Linux x86_64 GNU/Linux
GPU: not used
```

Commands:

```text
python3 udt_reciprocal_calibration_state_solder_audit_2026-08-09/derive_calibration_state_solder.py
python3 udt_reciprocal_calibration_state_solder_audit_2026-08-09/verify_calibration_state_solder.py
python3 udt_reciprocal_calibration_state_solder_audit_2026-08-09/verify_repository_gates.py
python3 -m pytest -q tests/
```

The independent verifier uses only the Python standard library and does not import the SymPy
controller. The mutable current-premise source is replayed from base `30bdb020`. The exact new
semantic landing has not yet received a fresh external review.
