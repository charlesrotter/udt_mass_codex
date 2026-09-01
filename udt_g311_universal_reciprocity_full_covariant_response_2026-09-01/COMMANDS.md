# G311 registered checks

Run from this package directory:

```bash
python3 -S derive_covariant_response.py --output DERIVATION_RESULT.json
python3 -S verify_covariant_response_independent.py --output INDEPENDENT_VERIFICATION.json
python3 -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json
python3 -S verify_package.py
```

These four commands are the complete registered sealed replay. They use only this package and a
writable temporary directory. The hostile harness is shared-code regression evidence; the separate
dependency-free verifier is the implementation-independent check.

Upstream repository banking gates, run from the repository root, are **not part of the registered
sealed replay and are not authorized during an intake-only review**:

```bash
python3 verify_current_scientific_premises.py
python3 -m pytest tests/
```
