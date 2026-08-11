# G71 run record

Date: 2026-08-11

Environment:

```text
Python 3.10.12
NumPy 2.2.6
SciPy 1.15.3
CPU float64 plus exact fractions
GPU processes: 0
new ODE/PDE solves: 0
observational fits/anchors: 0
```

Commands from repository root:

```bash
python3 -m py_compile udt_cmb_G71_native_restriction_owner_audit_2026-08-11/derive_owner_audit.py udt_cmb_G71_native_restriction_owner_audit_2026-08-11/verify_owner_audit_independent.py udt_cmb_G71_native_restriction_owner_audit_2026-08-11/run_catch_proofs.py
python3 udt_cmb_G71_native_restriction_owner_audit_2026-08-11/derive_owner_audit.py
python3 udt_cmb_G71_native_restriction_owner_audit_2026-08-11/verify_owner_audit_independent.py
python3 udt_cmb_G71_native_restriction_owner_audit_2026-08-11/run_catch_proofs.py
python3 udt_cmb_G71_native_restriction_owner_audit_2026-08-11/verify_package.py
python3 udt_cmb_G71_native_restriction_owner_audit_2026-08-11/verify_repository_gates.py
```

The first independent-verifier run stopped before writing its result because one ledger evidence
token paraphrased rather than exactly quoted G70. The token was corrected to an exact phrase and
the complete production/independent/catch sequence reran from the beginning. No status changed.

SciPy `logm` emitted accuracy warnings of order `1e-13` on some scaled positive-definite matrices.
The preregistered shape-invariance residual remained `3.325e-13`, well below the `2e-11` gate.
