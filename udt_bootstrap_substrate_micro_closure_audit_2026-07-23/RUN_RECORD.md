# Run record

Date: 2026-07-23

Mode: CPU-only exact algebra and source audit

Commands:

```text
python3 -m py_compile \
  derive_bootstrap_substrate_micro.py \
  verify_bootstrap_substrate_micro_independent.py

python3 derive_bootstrap_substrate_micro.py \
  --result DERIVATION_RESULT.json \
  --channels CHANNEL_OUTCOMES.tsv \
  --regrades PRIOR_RESULT_REGRADE.tsv \
  --fixed-point FIXED_POINT_OUTCOMES.tsv \
  --completions COMPLETION_CHANNEL_MATRIX.tsv

python3 -s verify_bootstrap_substrate_micro_independent.py \
  --production DERIVATION_RESULT.json \
  --channels CHANNEL_OUTCOMES.tsv \
  --regrades PRIOR_RESULT_REGRADE.tsv \
  --fixed-point FIXED_POINT_OUTCOMES.tsv \
  --completions COMPLETION_CHANNEL_MATRIX.tsv \
  --output INDEPENDENT_VERIFICATION_RESULT.json
```

Results:

```text
production: algebra 12/12; source checks 17/17
independent: exact 11/11; agreement 13/13; catches 11/11
```

No GPU, density scan, time-live solve, relaxation, or fitted target was used.
