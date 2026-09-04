# G343 registered commands

Run from this directory with no persistent script output:

```bash
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S derive_bilocal_propagator.py
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S verify_bilocal_independent.py
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S run_catch_proofs.py
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S verify_package.py
```

The aggregate verifier snapshots the package before and after its subprocess replays and fails if
any byte changes.
