# G284 registered commands

Run from repository root:

```bash
python3 udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/verify_preregistration.py
python3 udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/derive_causal_projective.py
python3 udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/verify_independent.py
python3 udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/run_catch_proofs.py
python3 udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/verify_package.py
```

The four load-bearing recomputations use only the Python standard library. The package verifier
reruns them with `python3 -S` in an ephemeral copy containing the exact 15 frozen sources before it
examines saved evidence. `derive_causal_projective_sympy.py` is retained only as an optional,
nonregistered implementation cross-check when SymPy is available.
