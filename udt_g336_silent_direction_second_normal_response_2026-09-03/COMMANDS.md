# G336 registered commands

Run from this package directory:

```bash
python3 -B -S derive_silent_second_response.py --output DERIVATION_RESULT.json
python3 -B -S verify_silent_second_response_independent.py --output INDEPENDENT_VERIFICATION.json
python3 -B -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json
python3 -B -S verify_package.py --output PACKAGE_VERIFICATION_RESULT.json
```

These are dependency-free CPU checks. They do not start a long solve or mutate the metric.
