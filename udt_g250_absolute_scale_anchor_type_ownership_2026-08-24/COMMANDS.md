# G250 registered commands

Set `PYTHONDONTWRITEBYTECODE=1` for every no-write replay.

## Sealed-intake replays

Run these four commands from either the repository root or the root of a G250 sealed intake:

```bash
python3 udt_g250_absolute_scale_anchor_type_ownership_2026-08-24/derive_absolute_scale_anchor_types.py --cases 4096
python3 udt_g250_absolute_scale_anchor_type_ownership_2026-08-24/verify_absolute_scale_anchor_types_independent.py --cases 12000
python3 udt_g250_absolute_scale_anchor_type_ownership_2026-08-24/run_catch_proofs.py
python3 udt_g250_absolute_scale_anchor_type_ownership_2026-08-24/verify_package.py
```

The three scientific scripts write only when an explicit `--output` or
`--classification-output` path is supplied.

## Repository-only gate

The current-premise verifier is a repository-wide banking gate. It is not a sealed-intake replay
and is intentionally not transmitted:

```bash
python3 verify_current_scientific_premises.py
```
