# Commands

Run from repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_time_live_characteristic_flux_audit_2026-07-21/derive_time_live_flux.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_time_live_characteristic_flux_audit_2026-07-21/verify_time_live_flux.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_time_live_characteristic_flux_audit_2026-07-21/build_manifest.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_time_live_characteristic_flux_audit_2026-07-21/verify_repository_gates.py
```

The derivation uses exact SymPy algebra and performs no ODE/PDE evolution or numerical relaxation.
The independent verifier does not import the generator.
