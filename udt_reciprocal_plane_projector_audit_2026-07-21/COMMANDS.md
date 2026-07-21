# Commands

Run from repository root in a CPU-only environment with `sympy==1.13.1`:

```bash
python3 udt_reciprocal_plane_projector_audit_2026-07-21/derive_reciprocal_plane_projector.py
python3 udt_reciprocal_plane_projector_audit_2026-07-21/verify_reciprocal_plane_projector.py
python3 udt_reciprocal_plane_projector_audit_2026-07-21/build_manifest.py
python3 udt_reciprocal_plane_projector_audit_2026-07-21/verify_repository_gates.py
```

The derivation uses SymPy exact algebra. The independent verifier uses only the Python standard
library and exact `fractions.Fraction` arithmetic.
