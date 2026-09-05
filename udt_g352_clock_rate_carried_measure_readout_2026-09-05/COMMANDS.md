# G352 registered commands

After the preregistration commit, run from this directory with the system standard library only:

```bash
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S derive_clock_rate_readout.py
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S verify_clock_rate_readout_independent.py
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S run_catch_proofs.py
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S verify_package.py
```

These are exact regression and certification checks, not the analytic proof, a physical light
simulation, an observational fit, a spacetime evolution, or a scale calculation.
