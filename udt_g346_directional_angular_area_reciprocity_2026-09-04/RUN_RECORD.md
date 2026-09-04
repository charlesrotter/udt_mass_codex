# G346 run record

Date: 2026-09-04
Working directory: `udt_g346_directional_angular_area_reciprocity_2026-09-04/`
Preregistration commit: `9a037558`

No GPU or long-running process was used. Every run was CPU, bounded, dependency-free under
`python3 -S`, and executed with bytecode writes disabled.

## Production

```bash
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S derive_directional_angular_area.py
```

Result: `PASS`, `11204/11204`. Largest recorded relative error:
`3.542999227335031e-14` (stationary sewing).

## Implementation-distinct verification

```bash
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S verify_directional_angular_area_independent.py
```

Result: `PASS`, `4251/4251`. Method: independent `lambda-gamma` Simpson-log fundamental basis,
explicit metric sky musical map, independently recomputed endpoint-unit gauges, and direct
log-time RK4 Jacobi integration. Largest recorded relative error:
`9.98350167131679e-11` (full block composition).

## Hostile mutations

```bash
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S run_catch_proofs.py
```

Result: `PASS`, `20/20` caught.

## No-write status

All three scripts only printed results. The result JSON files were transcribed exactly from that
stdout with `apply_patch`; no outcome script wrote package evidence.

## Aggregate and repository guards

```bash
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S verify_package.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_current_scientific_premises.py
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -qq -p no:cacheprovider tests/
```

The package aggregate passed `19/19` after the recorded packaging-only self-reference repair. The
premise verifier passed the exact 328-row registry and all current guards through G345. The full
repository suite passed 220 tests with the one pre-existing documented xfail.

## Fresh external review and final integration

External `gpt-5.4` authenticated the 29-payload sealed intake, reproduced the `19/19` sealed
aggregate and all underlying replays, and independently reconstructed the load-bearing formulas.
It returned `ACCEPT_G346_BOUNDED_DIRECTIONAL_ANGULAR_AREA_RECIPROCITY` without required repair.
After the report and exact transmission provenance were added, the post-review aggregate passed
`21/21`. The final exact 329-row premise audit passed, and the repository suite passed 221 tests
with the one pre-existing documented xfail. Final results are recorded in `EVIDENCE_GATES.md`.
