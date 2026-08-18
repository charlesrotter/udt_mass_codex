# G163 run record

Date: 2026-08-18
Branch: `grok`
Preregistration commit: `fb7e0f8e`
Source snapshot: `21ca77db`

Commands:

```text
python3 udt_g163_xmax_dependency_reversal_audit_2026-08-18/derive_scale_free_kernel.py
python3 udt_g163_xmax_dependency_reversal_audit_2026-08-18/verify_scale_free_kernel_independent.py
python3 udt_g163_xmax_dependency_reversal_audit_2026-08-18/run_catch_proofs.py
```

Results:

```text
production: PASS; 13 exact checks; native Xmax rank 0
independent: PASS; 1,200 exact Fraction trials; native Xmax finite-difference rank 0
catches: PASS; 8/8
dependency census: 20/20 G135--G154 rows
```

No observational data, fit, GPU, long solve, action, source, bootstrap, protected package, or
stopped draft was read or used.
