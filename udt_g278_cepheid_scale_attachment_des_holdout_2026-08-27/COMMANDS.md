# G278 commands

The outcome-blind preregistration commit precedes all production commands.

```bash
G236_DES_ROOT='/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT' \
python3 udt_g278_cepheid_scale_attachment_des_holdout_2026-08-27/derive_scale_and_holdout.py

G236_DES_ROOT='/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT' \
python3 udt_g278_cepheid_scale_attachment_des_holdout_2026-08-27/verify_independent.py

python3 udt_g278_cepheid_scale_attachment_des_holdout_2026-08-27/run_catch_proofs.py
python3 udt_g278_cepheid_scale_attachment_des_holdout_2026-08-27/verify_package.py
python3 verify_current_scientific_premises.py
```
