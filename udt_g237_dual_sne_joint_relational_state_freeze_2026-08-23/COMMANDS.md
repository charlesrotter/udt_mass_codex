# G237 commands

## Repository-side preparation

```bash
python3 -B udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23/build_chronology_proof.py

G237_DES_ROOT='/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT' \
python3 -B udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23/build_review_intake.py
```

`build_chronology_proof.py` is a repository-side exporter because it reads live Git objects. It is
not a sealed replay command.

## Self-contained sealed replay

From the sealed-intake root:

```bash
python3 -B udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23/derive_joint_state.py

G237_DES_ROOT='./external_data' \
python3 -B udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23/verify_joint_state_from_raw.py

python3 -B udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23/verify_chronology_bundle.py

python3 -B udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23/verify_package.py

python3 -B udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23/run_catch_proofs.py

python3 -B udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23/verify_repair.py
```
