# G250 registered commands

Run from the repository root with `PYTHONDONTWRITEBYTECODE=1` when checking a sealed copy.

```bash
python3 udt_g250_absolute_scale_anchor_type_ownership_2026-08-24/derive_absolute_scale_anchor_types.py --cases 4096
python3 udt_g250_absolute_scale_anchor_type_ownership_2026-08-24/verify_absolute_scale_anchor_types_independent.py --cases 12000
python3 udt_g250_absolute_scale_anchor_type_ownership_2026-08-24/run_catch_proofs.py
python3 udt_g250_absolute_scale_anchor_type_ownership_2026-08-24/verify_package.py
python3 verify_current_scientific_premises.py
```

The three scientific scripts write only when an explicit `--output` or
`--classification-output` path is supplied.
