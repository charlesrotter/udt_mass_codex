# G241 commands

## Direct sealed-intake replay

These commands require only the repository-relative files included in the repaired sealed intake.
They do not write persistent outputs.

```bash
python3 udt_g241_sne_anchored_native_tidal_bridge_2026-08-23/derive_sne_tidal_bridge.py --no-write
python3 udt_g241_sne_anchored_native_tidal_bridge_2026-08-23/verify_sne_tidal_bridge_independent.py --no-write
python3 udt_g241_sne_anchored_native_tidal_bridge_2026-08-23/verify_package.py --no-write
python3 udt_g241_sne_anchored_native_tidal_bridge_2026-08-23/run_catch_proofs.py --no-write
```

## Repository integration checks

These checks require the full repository and are intentionally not presented as sealed-intake
replays.

```bash
python3 verify_current_scientific_premises.py
python3 -m pytest tests/
```
