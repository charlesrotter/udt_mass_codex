# G201 run record

Date: 2026-08-21

Preregistration commit: `28d48506`

Commands:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g201_primary_metric_phi_jet_regime_amplitude_2026-08-21/derive_phi_jet_regime_amplitude.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g201_primary_metric_phi_jet_regime_amplitude_2026-08-21/verify_phi_jet_amplitude_independent.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g201_primary_metric_phi_jet_regime_amplitude_2026-08-21/run_catch_proofs.py
```

Observed results:

- first production run failed closed because sequential substitution erased derivative terms;
- repaired simultaneous substitution: 20/20 symbolic assertions;
- independent: 10,000 arbitrary exact jets, 1,000 cancellation cases, 400 smooth-family controls,
  and 23,606 assertions;
- catch proofs: 9/9.
