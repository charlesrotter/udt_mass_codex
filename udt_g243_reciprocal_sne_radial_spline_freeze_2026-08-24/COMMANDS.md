# G243 commands

Set the external DES release directory:

```bash
export G243_DES_ROOT=/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT
```

Production and independent evaluation:

```bash
python3 -B udt_g243_reciprocal_sne_radial_spline_freeze_2026-08-24/derive_radial_spline_representation.py
python3 -B udt_g243_reciprocal_sne_radial_spline_freeze_2026-08-24/verify_radial_spline_independent.py
```

Evidence checks:

```bash
python3 -B udt_g243_reciprocal_sne_radial_spline_freeze_2026-08-24/verify_package.py
python3 -B udt_g243_reciprocal_sne_radial_spline_freeze_2026-08-24/run_catch_proofs.py
```

Read-only replay replaces each command with `--no-write`.
