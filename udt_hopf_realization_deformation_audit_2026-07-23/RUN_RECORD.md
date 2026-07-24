# Run record

Date: 2026-07-23
Mode: CPU-only exact algebra; no GPU, relaxation, density scan, or dynamics

Commands:

```bash
python3 -m py_compile \
  udt_hopf_realization_deformation_audit_2026-07-23/derive_hopf_realization_deformations.py \
  udt_hopf_realization_deformation_audit_2026-07-23/verify_hopf_realization_deformations_independent.py

python3 \
  udt_hopf_realization_deformation_audit_2026-07-23/derive_hopf_realization_deformations.py \
  --output udt_hopf_realization_deformation_audit_2026-07-23/DERIVATION_RESULT.json \
  --candidate-output udt_hopf_realization_deformation_audit_2026-07-23/DEFORMATION_OUTCOMES.tsv \
  --global-output udt_hopf_realization_deformation_audit_2026-07-23/GLOBAL_COMPLETION_OUTCOMES.tsv

python3 -s \
  udt_hopf_realization_deformation_audit_2026-07-23/verify_hopf_realization_deformations_independent.py \
  --production-result udt_hopf_realization_deformation_audit_2026-07-23/DERIVATION_RESULT.json \
  --candidate-result udt_hopf_realization_deformation_audit_2026-07-23/DEFORMATION_OUTCOMES.tsv \
  --global-result udt_hopf_realization_deformation_audit_2026-07-23/GLOBAL_COMPLETION_OUTCOMES.tsv \
  --output udt_hopf_realization_deformation_audit_2026-07-23/INDEPENDENT_VERIFICATION_RESULT.json
```

The first production attempt failed closed on a SymPy hyperbolic-identity
simplification (`8/(cosh(4phi)+1)` versus `4 sech(2phi)^2`). The controller
was corrected to compare the exact exponential rewrites. No premise,
candidate, or conclusion contract changed.
