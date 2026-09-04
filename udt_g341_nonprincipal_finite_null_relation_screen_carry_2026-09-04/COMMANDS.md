# G341 commands

Run from this directory:

```bash
python3 -B -S derive_nonprincipal_relation.py
python3 -B -S verify_nonprincipal_independent.py
python3 -B -S run_catch_proofs.py
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S verify_package.py
```

The production and independent scripts write only their registered JSON result when
`UDT_NO_WRITE` is absent. No script needs network access, a GPU, or non-standard packages.
