# G331 registered commands

Run from the package directory:

```bash
python3 -S derive_nonsymmetric_eigenline.py --output DERIVATION_RESULT.json
python3 -S verify_nonsymmetric_eigenline_independent.py --output INDEPENDENT_VERIFICATION.json
python3 -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json
python3 -S verify_package.py --output PACKAGE_VERIFICATION_RESULT.json
```

All scripts are standard-library-only. The first three overwrite only their named JSON artifacts;
the aggregate verifier uses a temporary directory and does not alter registered evidence.
