# G288 commands

From repository root:

Self-contained standard-library scientific replay and hostile recomputation:

```bash
python3 udt_g288_smooth_center_micro_regime_jet_interlock_2026-08-28/verify_independent.py
python3 udt_g288_smooth_center_micro_regime_jet_interlock_2026-08-28/run_hostile_recomputations.py
```

Saved-artifact/semantic guard and integrity/provenance aggregation:

```bash
python3 udt_g288_smooth_center_micro_regime_jet_interlock_2026-08-28/run_catch_proofs.py
python3 udt_g288_smooth_center_micro_regime_jet_interlock_2026-08-28/build_source_manifest.py
python3 udt_g288_smooth_center_micro_regime_jet_interlock_2026-08-28/verify_package.py
```

The separate production derivation requires SymPy and is not promised in a minimal reviewer
environment:

```bash
python3 udt_g288_smooth_center_micro_regime_jet_interlock_2026-08-28/derive_micro_center.py
```
