# G277 commands

Run from repository root:

```bash
python3 udt_g277_observational_scale_anchor_ownership_2026-08-26/derive_anchor_ownership.py
python3 udt_g277_observational_scale_anchor_ownership_2026-08-26/verify_anchor_ownership_independent.py
python3 udt_g277_observational_scale_anchor_ownership_2026-08-26/run_catch_proofs.py
python3 udt_g277_observational_scale_anchor_ownership_2026-08-26/verify_package.py
python3 -m pytest tests/
python3 udt_g277_observational_scale_anchor_ownership_2026-08-26/build_review_intake.py
```

Registered no-write replays:

```bash
python3 udt_g277_observational_scale_anchor_ownership_2026-08-26/derive_anchor_ownership.py --no-write
python3 udt_g277_observational_scale_anchor_ownership_2026-08-26/verify_anchor_ownership_independent.py --no-write
python3 udt_g277_observational_scale_anchor_ownership_2026-08-26/run_catch_proofs.py --no-write
```
