# G278 commands

The outcome-blind preregistration commit precedes all production commands.
The commands below are the registered sealed-intake replays. Run them from the intake root.

```bash
G236_DES_ROOT="$PWD/external_data" \
python3 udt_g278_cepheid_scale_attachment_des_holdout_2026-08-27/derive_scale_and_holdout.py

G236_DES_ROOT="$PWD/external_data" \
python3 udt_g278_cepheid_scale_attachment_des_holdout_2026-08-27/verify_independent.py

python3 udt_g278_cepheid_scale_attachment_des_holdout_2026-08-27/run_catch_proofs.py
G236_DES_ROOT="$PWD/external_data" \
python3 udt_g278_cepheid_scale_attachment_des_holdout_2026-08-27/diagnose_resolution_sensitivity.py

G236_DES_ROOT="$PWD/external_data" \
python3 udt_g278_cepheid_scale_attachment_des_holdout_2026-08-27/verify_package.py
```

The repository-wide premise audit is a separate local banking gate. It requires the full repository
and is intentionally not advertised as a sealed-intake replay.
