# Exact commands

Run from repository root in the pinned clean Python environment:

```bash
PYTHONPATH=/tmp/udt_bootstrap_response_sympy_114_target python3 udt_metric_orchestra_rehearsal_2026-07-25/derive_orchestra_rehearsal.py
PYTHONPATH=/tmp/udt_bootstrap_response_sympy_114_target python3 udt_metric_orchestra_rehearsal_2026-07-25/verify_orchestra_independent.py
PYTHONPATH=/tmp/udt_bootstrap_response_sympy_114_target python3 udt_metric_orchestra_rehearsal_2026-07-25/verify_orchestra_audit.py
```

The environment contains the exact versions in `requirements.txt`.  This audit
is CPU-only.  No PDE, relaxation, time evolution, density sweep, or GPU process
is run.
