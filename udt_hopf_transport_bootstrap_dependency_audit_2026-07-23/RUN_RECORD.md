# Run record

Date: 2026-07-23
Device: CPU only (`CUDA_VISIBLE_DEVICES` unset for the direct science
run and forced empty in repository gates)
Python: 3.10.12
SymPy: recorded in `DERIVATION_RESULT.json`

Commands:

```bash
python3 -m py_compile \
  udt_hopf_transport_bootstrap_dependency_audit_2026-07-23/derive_hopf_transport_bootstrap_dependencies.py \
  udt_hopf_transport_bootstrap_dependency_audit_2026-07-23/verify_hopf_transport_bootstrap_independent.py

python3 \
  udt_hopf_transport_bootstrap_dependency_audit_2026-07-23/derive_hopf_transport_bootstrap_dependencies.py \
  --output udt_hopf_transport_bootstrap_dependency_audit_2026-07-23/DERIVATION_RESULT.json

python3 -s \
  udt_hopf_transport_bootstrap_dependency_audit_2026-07-23/verify_hopf_transport_bootstrap_independent.py \
  --production-result udt_hopf_transport_bootstrap_dependency_audit_2026-07-23/DERIVATION_RESULT.json \
  --output udt_hopf_transport_bootstrap_dependency_audit_2026-07-23/INDEPENDENT_VERIFICATION_RESULT.json
```

Both science commands exited `0`. They intentionally write no stdout
or stderr on success. The repository-gate replay records deterministic
byte identity and the test baseline.
