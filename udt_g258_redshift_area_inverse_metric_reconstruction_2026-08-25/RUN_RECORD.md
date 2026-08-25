# G258 run record

Date: 2026-08-25
Branch: `grok`
Preregistration commit: `a9f96360`

## Commands

```bash
python3 derive_inverse_metric_reconstruction.py
python3 verify_independent.py
python3 run_catch_proofs.py
```

## Results

- production: 12 nodes, 10 positive adjacent changes, one negative adjacent change;
- maximum algebra residual: `2.220446049250313e-16`;
- saved relative-radius and covariance residual: `0`;
- independent: 252 Decimal assertions;
- hostile controls: 8/8;
- fitted UDT coefficients: zero;
- GPU: not used;
- protected packages: not read.
