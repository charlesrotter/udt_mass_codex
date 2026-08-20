# G192 commands

Run from repository root:

```bash
python3 udt_g192_smooth_timelive_mixing_family_classification_2026-08-20/derive_smooth_timelive_mixing.py
python3 udt_g192_smooth_timelive_mixing_family_classification_2026-08-20/verify_smooth_timelive_mixing_independent.py
python3 udt_g192_smooth_timelive_mixing_family_classification_2026-08-20/run_catch_proofs.py
python3 verify_current_scientific_premises.py
python3 -m pytest tests/
git diff --check
```

No-write replay:

```bash
G192_NO_WRITE=1 python3 udt_g192_smooth_timelive_mixing_family_classification_2026-08-20/derive_smooth_timelive_mixing.py
G192_NO_WRITE=1 python3 udt_g192_smooth_timelive_mixing_family_classification_2026-08-20/verify_smooth_timelive_mixing_independent.py
G192_NO_WRITE=1 python3 udt_g192_smooth_timelive_mixing_family_classification_2026-08-20/run_catch_proofs.py
```
