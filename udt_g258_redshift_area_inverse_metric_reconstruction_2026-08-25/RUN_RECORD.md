# G258 run record

Date: 2026-08-25
Branch: `grok`
Preregistration commit: `a9f96360`

## Commands

```bash
python3 derive_inverse_metric_reconstruction.py
python3 verify_independent.py
python3 run_catch_proofs.py
python3 verify_package.py
python3 verify_repair.py
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

## External review and R1

- fresh `gpt-5.4`: `ACCEPT_WITH_REPAIRS`; scientific core accepted;
- sole finding: synthesized historical-registry compatibility weakened exact provenance;
- R1 replaces row deletion with exact sealed bytes or exact Git object
  `a9f96360:CURRENT_SCIENTIFIC_PREMISES.tsv`;
- strict sealed replay rejects a one-byte source mutation;
- five load-bearing scientific artifacts remain byte-identical;
- repair-only `gpt-5.4` follow-up independently replayed all five registered checks and returned
  `REPAIRS_ACCEPTED`; the bounded scientific landing is unchanged.
