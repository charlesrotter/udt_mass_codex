# G299 commands

```bash
python3 udt_g299_complete_relation_kernel_domain_ownership_2026-08-29/derive_relation_domain.py
python3 udt_g299_complete_relation_kernel_domain_ownership_2026-08-29/verify_relation_domain_independent.py
python3 udt_g299_complete_relation_kernel_domain_ownership_2026-08-29/run_catch_proofs.py
python3 udt_g299_complete_relation_kernel_domain_ownership_2026-08-29/verify_package.py
```

The production derivation uses SymPy when available and falls back to exact standard-library
`Fraction` arithmetic when it is not. The minimal-image replay is therefore explicitly:

```bash
python3 -S udt_g299_complete_relation_kernel_domain_ownership_2026-08-29/derive_relation_domain.py
python3 -S udt_g299_complete_relation_kernel_domain_ownership_2026-08-29/verify_relation_domain_independent.py
python3 -S udt_g299_complete_relation_kernel_domain_ownership_2026-08-29/run_catch_proofs.py
python3 -S udt_g299_complete_relation_kernel_domain_ownership_2026-08-29/verify_package.py
```
