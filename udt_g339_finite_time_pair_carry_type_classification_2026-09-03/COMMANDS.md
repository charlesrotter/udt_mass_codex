# G339 replay commands

From this directory:

```bash
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S derive_carry_type_classification.py
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S verify_carry_type_independent.py
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S run_catch_proofs.py
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S verify_package.py
```

The scripts require only the Python standard library. They use no GPU, network, observations, or
repository-global Python import.
