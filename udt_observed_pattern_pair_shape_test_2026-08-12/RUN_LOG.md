# Run log

Date: 2026-08-12

## Production command

```bash
python3 udt_observed_pattern_pair_shape_test_2026-08-12/derive_pair_shape.py \
  --mean /media/udt-admin/ScratchDisk/Data/BAO/CobayaSampler_bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt \
  --cov /media/udt-admin/ScratchDisk/Data/BAO/CobayaSampler_bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt \
  --output udt_observed_pattern_pair_shape_test_2026-08-12/DERIVATION_RESULT.json \
  --rows-output udt_observed_pattern_pair_shape_test_2026-08-12/SHAPE_RESIDUAL_ATLAS.tsv
```

```json
{"status":"PASS","totals":{"C0":{"chi2":114.72114835807093,"constraints":6,"classification":"INCOMPATIBLE_ON_SIX_BIN_SHAPE_QUERY"},"C1":{"chi2":31.274892627884704,"constraints":6,"classification":"INCOMPATIBLE_ON_SIX_BIN_SHAPE_QUERY"}}}
```

## Independent replay

```bash
python3 udt_observed_pattern_pair_shape_test_2026-08-12/verify_independent.py \
  --mean /media/udt-admin/ScratchDisk/Data/BAO/CobayaSampler_bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt \
  --cov /media/udt-admin/ScratchDisk/Data/BAO/CobayaSampler_bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt \
  --production udt_observed_pattern_pair_shape_test_2026-08-12/DERIVATION_RESULT.json \
  --output udt_observed_pattern_pair_shape_test_2026-08-12/INDEPENDENT_VERIFICATION.json
```

Result: `PASS`; maximum per-row absolute chi-square disagreement
`1.8765017207483413e-13`.

## Hostile checks

```bash
python3 udt_observed_pattern_pair_shape_test_2026-08-12/run_catch_proofs.py \
  --result udt_observed_pattern_pair_shape_test_2026-08-12/DERIVATION_RESULT.json \
  --output udt_observed_pattern_pair_shape_test_2026-08-12/CATCH_PROOF_RESULT.json
```

Result: `PASS`, `9/9` caught.
