# G76 run record

Date: 2026-08-11

## Equation gate

```bash
python3 udt_cmb_G76_complete_family_whole_sky_relation_atlas_2026-08-11/derive_equations.py
```

Result: `6/6 PASS`, saved in `EQUATION_VERIFICATION.json`.

## Production

```bash
/usr/bin/time -v python3 udt_cmb_G76_complete_family_whole_sky_relation_atlas_2026-08-11/solve_complete_family.py
```

- exit: `0`;
- wall time: `8:23.40`;
- reported internal runtime: `503.0965256690979 s`;
- maximum resident set: `150984 KiB`;
- CPU: one process, `float64`, no GPU;
- raw combined terminal record: `PRODUCTION_TRANSCRIPT.txt`;
- checkpoint/restart directory: `_checkpoints/`, ignored operational data;
- protected draft contents read: `false`.

## Independent direct-metric replay

```bash
python3 udt_cmb_G76_complete_family_whole_sky_relation_atlas_2026-08-11/verify_complete_family_independent.py
```

Result: `PASS`; eight exact strata, 162 rays each, 2,048 RK4 steps, direct Christoffel formulation,
no import of the production Hamiltonian RHS. See `INDEPENDENT_VERIFICATION.json` and the preserved
fail-closed development note.

## Saved-artifact replay and catches

```bash
python3 udt_cmb_G76_complete_family_whole_sky_relation_atlas_2026-08-11/verify_artifacts_independent.py
python3 udt_cmb_G76_complete_family_whole_sky_relation_atlas_2026-08-11/run_catch_proofs.py
```

Results: artifact verifier `PASS`; `6/6` exercised corruption catches `PASS`.
