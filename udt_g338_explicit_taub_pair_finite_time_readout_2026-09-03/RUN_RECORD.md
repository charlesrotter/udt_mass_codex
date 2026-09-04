# G338 run record

Date: 2026-09-03
Preregistration commit: `01e2110a`
Device: CPU
Arithmetic: exact rational production checks plus independent IEEE-754 reconstruction
GPU: available but not used; no grid or PDE solve is needed for this algebraic test

Commands:

```bash
python3 -S derive_explicit_taub_pair_readout.py
python3 -S verify_explicit_taub_pair_readout_independent.py
python3 -S run_catch_proofs.py
```

Outcomes:

- production: `169/169`;
- independent: `16/16`;
- hostile catches: `9/9`.
- external verdict: `ACCEPT_G338_BOUNDED_FINITE_TIME_PAIR_READOUT`.
