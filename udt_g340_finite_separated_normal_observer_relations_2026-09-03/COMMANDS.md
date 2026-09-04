# G340 registered commands

From this package directory:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B -S derive_finite_pair_relations.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -S verify_finite_pair_independent.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -S run_catch_proofs.py
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S verify_package.py
```

All scripts use only the Python standard library. In `UDT_NO_WRITE=1` mode, they must not change
package evidence bytes.
