# G73 run record

Date: 2026-08-11

Working directory:
`udt_cmb_G73_global_sky_source_sensitivity_atlas_2026-08-11/`

Commands:

```bash
python3 derive_source_sensitivity.py
python3 verify_source_sensitivity_independent.py
python3 run_catch_proofs.py
```

Execution: CPU only; no ODE/PDE solve and no GPU work.

Production result: seven exact checks and all 21 G68 rows pass.

Independent result: 11/11 checks pass; maximum direct G68 atlas error `0.0`; maximum analytic-versus-
grid alignment error `2.1529809351994444e-06` across 400,000 unoriented directions.

Semantic catches: 9/9 pass.

Protected stopped draft: contents unread and unstaged.
