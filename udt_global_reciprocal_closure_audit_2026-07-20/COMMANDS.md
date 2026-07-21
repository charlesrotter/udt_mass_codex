# Commands and environment

All commands were run from the clean audit worktree root on CPU only.

```bash
python3 --version
python3 udt_global_reciprocal_closure_audit_2026-07-20/derive_closure_status.py
python3 udt_global_reciprocal_closure_audit_2026-07-20/verify_package.py
python3 udt_global_reciprocal_closure_audit_2026-07-20/build_manifest.py
python3 udt_global_reciprocal_closure_audit_2026-07-20/verify_repository_gates.py
git diff --check
```

No symbolic or numerical physics solve, GPU process, network query, external model review, or
research-artifact mutation was performed.
