# G349 registered commands

Date: 2026-09-04
Status: external caveat received; R1--R4 repair preregistered at `c2967132`

Run only after the preregistration and frozen scripts are committed and pushed:

```bash
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -B -S derive_finite_null_patch_area.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -B -S verify_finite_null_patch_area_independent.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -B -S run_catch_proofs.py
```

No result file may be written by these commands in no-write mode. Exact outputs and any failure or
repair will be recorded after first execution.

Aggregate replay after result assembly:

```bash
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -B -S verify_package.py
```

The first hostile run returned `20/21`; the recorded behavioral-only cusp-guard repair committed at
`134ecd4a` raised it to `21/21` without altering the scientific contract.

The external review then exposed the mixed transverse-rank-one/ordinary-rank-two null stratum.
After the separately frozen repair, the same registered commands regenerate and replay the repaired
`44321/44321`, `14321/14321`, and `22/22` evidence. The corrected sealed repair-only follow-up
independently reconstructed that witness and returned `ACCEPT_G349_R1_R4_REPAIR_FOLLOWUP`.
