# G70 run record

Date: 2026-08-11

Environment:

```text
Python 3.10.12
NumPy 2.2.6
SciPy 1.15.3
CPU float64
GPU processes: 0
new ODE solves: 0
observational fits: 0
```

Commands, from repository root:

```bash
python3 -m py_compile udt_cmb_G70_query_owned_restriction_atlas_2026-08-11/derive_restriction_atlas.py
python3 udt_cmb_G70_query_owned_restriction_atlas_2026-08-11/derive_restriction_atlas.py
python3 -m py_compile udt_cmb_G70_query_owned_restriction_atlas_2026-08-11/verify_restriction_atlas_independent.py
python3 udt_cmb_G70_query_owned_restriction_atlas_2026-08-11/verify_restriction_atlas_independent.py
python3 udt_cmb_G70_query_owned_restriction_atlas_2026-08-11/run_catch_proofs.py
python3 udt_cmb_G70_query_owned_restriction_atlas_2026-08-11/verify_package.py
python3 udt_cmb_G70_query_owned_restriction_atlas_2026-08-11/verify_repository_gates.py
```

The first independent-verifier invocation exposed an empty-array shape bug for the deliberately
zero-output R00 model before it wrote a result. The verifier was corrected to restore the registered
`(0,3)` matrix shape, then rerun from the beginning. This changed no production artifact or rank.

The independent SciPy `logm` route emitted six accuracy warnings of approximately `3.4e-13` on
small covariances. Its direct `expm(logm(C))` reconstruction gate nevertheless remained below
`1.081e-14` relative, and every production matrix/rank replayed within its preregistered tolerance.
