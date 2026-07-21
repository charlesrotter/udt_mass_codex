# Commands and environment

Run from the clean repository worktree root, CPU only:

```bash
python3 --version
python3 -c 'import sympy; print(sympy.__version__)'
python3 udt_global_coframe_cocycle_audit_2026-07-20/derive_global_coframe_cocycle.py
python3 udt_global_coframe_cocycle_audit_2026-07-20/verify_global_coframe_cocycle.py
python3 udt_global_coframe_cocycle_audit_2026-07-20/build_manifest.py
python3 udt_global_coframe_cocycle_audit_2026-07-20/verify_repository_gates.py
git diff --check
```

The derivation uses pinned SymPy `1.13.1`. The independent implementation uses only Python's standard
library `Fraction` arithmetic, integer determinants, and an independently written rational rank
algorithm.

No GPU process, nonlinear solve, external model review, network research, action adoption, topology
choice, carrier/source work, or startup-control edit was performed.
