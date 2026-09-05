# G350 registered repair commands

Run from this directory after the frozen four-command preregistration suite:

```bash
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -B -S run_semantic_mutation_checks.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -B -S verify_repair_numerics.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -B -S verify_package.py
```

These post-outcome routes are registered by `REPAIR_PREREGISTRATION.md`; they are not represented as
part of the original outcome-unseen hash freeze. No tolerance is loosened, and no physical law is
selected.
