# G298 registered replay commands

Run from the repository root or from a writable copy of the complete sealed intake.

```bash
python3 udt_g298_causal_diamond_to_pair_germ_transfer_2026-08-29/derive_causal_pair_transfer.py --no-write
python3 udt_g298_causal_diamond_to_pair_germ_transfer_2026-08-29/verify_causal_pair_transfer_independent.py --no-write
python3 udt_g298_causal_diamond_to_pair_germ_transfer_2026-08-29/run_catch_proofs.py --no-write
python3 udt_g298_causal_diamond_to_pair_germ_transfer_2026-08-29/verify_package.py
```

The first three commands emit results to stdout and write nothing when `--no-write` is present.
