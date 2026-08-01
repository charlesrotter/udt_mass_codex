# Commands

All calculations are CPU-only from repository root.

```bash
python3 -m py_compile udt_f01_lambda_schur_check_2026-08-01/*.py
python3 udt_f01_lambda_schur_check_2026-08-01/diagnostic_spectral.py
python3 udt_f01_lambda_schur_check_2026-08-01/certify_negative_witnesses.py
python3 udt_f01_lambda_schur_check_2026-08-01/certify_free_schur.py
python3 udt_f01_lambda_schur_check_2026-08-01/verify_f01_package.py
python3 udt_f01_lambda_schur_check_2026-08-01/INDEPENDENT_VERIFIER.py
python3 udt_f01_lambda_schur_check_2026-08-01/verify_repository_gates.py
python3 udt_f01_lambda_schur_check_2026-08-01/build_package_manifest.py
python3 udt_f01_lambda_schur_check_2026-08-01/verify_package_manifest.py
```

The diagnostic is corroboration only. The two `certify_*` scripts supply the zero-excluding primary
interval bounds. The package verifier checks the frozen source bytes, branch coverage, labels,
enclosures, symbolic controls, conclusion ceiling, and ten exercised corruptions.
