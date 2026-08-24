# G252 registered commands

Set `PYTHONDONTWRITEBYTECODE=1` for every no-write replay.

## Sealed-intake replays

```bash
python3 udt_g252_local_proper_clock_same_object_attachment_contract_2026-08-24/derive_local_proper_clock_attachment.py --cases 4096
python3 udt_g252_local_proper_clock_same_object_attachment_contract_2026-08-24/verify_local_proper_clock_attachment_independent.py --cases 12000
python3 udt_g252_local_proper_clock_same_object_attachment_contract_2026-08-24/run_catch_proofs.py
python3 udt_g252_local_proper_clock_same_object_attachment_contract_2026-08-24/verify_package.py
```

The three scientific scripts write only when an explicit `--output` path is supplied.

## Repository-only gate

```bash
python3 verify_current_scientific_premises.py
```

The premise verifier is not included as a sealed-intake replay.
