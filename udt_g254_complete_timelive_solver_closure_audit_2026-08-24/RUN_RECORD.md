# G254 run record

Date: 2026-08-24
Device: CPU
Arithmetic: SymPy exact symbolic and standard-library `Fraction`
GPU: not launched because the stage-1 residual-ownership gate failed

## Commands

```text
python3 -m py_compile udt_g254_complete_timelive_solver_closure_audit_2026-08-24/derive_closure_census.py udt_g254_complete_timelive_solver_closure_audit_2026-08-24/verify_independent.py udt_g254_complete_timelive_solver_closure_audit_2026-08-24/run_catch_proofs.py
PYTHONDONTWRITEBYTECODE=1 python3 udt_g254_complete_timelive_solver_closure_audit_2026-08-24/derive_closure_census.py --output udt_g254_complete_timelive_solver_closure_audit_2026-08-24/DERIVATION_RESULT.json
PYTHONDONTWRITEBYTECODE=1 python3 udt_g254_complete_timelive_solver_closure_audit_2026-08-24/verify_independent.py --output udt_g254_complete_timelive_solver_closure_audit_2026-08-24/INDEPENDENT_VERIFICATION.json
PYTHONDONTWRITEBYTECODE=1 python3 udt_g254_complete_timelive_solver_closure_audit_2026-08-24/run_catch_proofs.py --output udt_g254_complete_timelive_solver_closure_audit_2026-08-24/CATCH_PROOF_RESULT.json
```

The first production replay exposed two source-token line-layout assumptions during development.
Whitespace normalization and exact registered landing tokens repaired them before the successful
scientific run. The independent calculation had already passed and no scientific artifact was
altered by those source-resolution repairs.

## External review and ephemeral replay

The authorized sealed 35-file intake at `/tmp/udt_g254_review_x6h7WMZb` had
`REVIEW_SCOPE.json` SHA-256
`1eadc6c30c803d0328daa08807f6dc3cc6d2248ebff09c713fdb1b699cd1e25b`.

Fresh external gpt-5.4 review returned `G254_VERIFIED_WITH_CAVEATS`: no scientific defect and no
required evidence-package repair. Its read-only environment prevented creation of a writable
ephemeral copy, so it used the registered no-write in-place replay. Afterward, the unchanged sealed
intake was copied to `/tmp/udt_g254_ephemeral_replay_VU9ZNzyQ`; `verify_package.py` passed there with
18 required files, 16 sources, 65 independent curvature trials, and six hostile catches. The
original scope hash remained unchanged.
