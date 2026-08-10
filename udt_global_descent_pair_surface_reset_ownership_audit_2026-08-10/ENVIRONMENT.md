# Environment

- Date: 2026-08-10
- Base commit: `eca93e1395c2f690f8357f015ea5901fec9f8310`
- Preregistration commit: `6c11c2181eaac0d5f7ff78a31a7717aa65f02ca0`
- Python: `3.10.12`
- SymPy: `1.13.1` (recorded for repository compatibility; the atlas uses standard-library exact table algebra)
- Compute: CPU only
- GPU work: none
- Protected curvature-atlas contents read: no

Commands:

```bash
python3 udt_global_descent_pair_surface_reset_ownership_audit_2026-08-10/derive_descent_atlas.py
python3 udt_global_descent_pair_surface_reset_ownership_audit_2026-08-10/verify_descent_independent.py
python3 udt_global_descent_pair_surface_reset_ownership_audit_2026-08-10/run_catch_proofs.py
python3 -m py_compile udt_global_descent_pair_surface_reset_ownership_audit_2026-08-10/*.py
```
