# G242 replay commands

Run from the repository root:

```bash
python3 udt_g242_sne_exact_quiet_subfamily_anchor_2026-08-24/derive_exact_quiet_anchor.py --no-write
python3 udt_g242_sne_exact_quiet_subfamily_anchor_2026-08-24/verify_exact_quiet_anchor_independent.py --no-write
python3 udt_g242_sne_exact_quiet_subfamily_anchor_2026-08-24/run_catch_proofs.py --no-write
python3 udt_g242_sne_exact_quiet_subfamily_anchor_2026-08-24/verify_package.py --no-write
```

These commands write no persistent output and read no BOSS outcome.
